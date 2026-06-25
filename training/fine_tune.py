"""
Sim-to-real fine-tuning for a pre-trained GreyBoxNet checkpoint.

Plan (3 sentences):
  Novelty N3-Duong (goal.md Objective 4 -- Standardised Sim-to-Real Gap Resolution).

  Reference:
    Duong, Altawaitan, Stanley, Atanasov (2024). "Port-Hamiltonian Neural ODE
    Networks on Lie Groups For Robot Dynamics Learning and Control."
    IEEE Transactions on Robotics.
    Borrowed: the empirical finding (Section IV-D, Table III) that freezing all
    but the last layers of a pretrained physics-informed model and running ~100
    gradient steps on real hardware data recovers tracking accuracy after a
    payload/mass change. Only the layer-freezing strategy and step budget are
    borrowed -- no port-Hamiltonian, ODE rollout, or Lie-group components are used.

Usage:
    python -m training.fine_tune \\
        --checkpoint models/run_XXXX/greybox_best.pt \\
        --real_data  data/real_motor_babbling.h5 \\
        --max_steps  100

What happens:
  1. The pre-trained GreyBoxNet is loaded via controller/model_loader.py.
  2. ALL layers are frozen EXCEPT the last two nn.Linear modules in the MLP
     (i.e., the final hidden-to-hidden projection and the hidden-to-output
     projection).  This follows the Duong et al. finding that the early
     layers encode transferable feature extraction while the final layers
     need adaptation for domain-specific residuals.
  3. The model is fine-tuned on a real-data HDF5 file for --max_steps gradient
     steps (default 100, per Duong et al.) using the SAME loss as Stage 1
     training: MSE(tau_pred, tau_real) + AugmentedLagrangian(torque_limits,
     dissipativity).  The physics constraints are NOT skipped -- they act as a
     regulariser that prevents overfitting to noisy real-world measurements
     (goal.md Objective #4 key claim).
  4. The fine-tuned checkpoint is saved alongside the original.

Architecture constraints:
  - Activations remain Mish/Softplus (never ReLU) -- inherited from pre-trained
    checkpoint via config.json; no activation layers are modified.
  - pinocchio_baseline/ is NOT touched.
  - The RNEA white-box term is NOT modified; only the residual head adapts.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from typing import List, Tuple

import torch
from torch.utils.data import DataLoader

from controller.model_loader import load_grey_box_model
from network.grey_box_net import GreyBoxNet
from training.constraints import AugmentedLagrangian
from training.dataset import FrankaDynamicsDataset


# ---------------------------------------------------------------------------
# Layer freezing logic
# ---------------------------------------------------------------------------

def _find_linear_layers(net: GreyBoxNet) -> List[Tuple[str, torch.nn.Linear]]:
    """Return all nn.Linear modules inside ``net.net`` (the Sequential MLP),
    ordered from input to output.

    The GreyBoxNet architecture (grey_box_net.py) stores the MLP in
    ``self.net = nn.Sequential(Linear, Act, Linear, Act, ..., Linear)``.
    This function walks that Sequential and collects every Linear layer
    together with its qualified name (e.g. ``'net.0'``, ``'net.4'``).

    Returns:
        List of (name, module) tuples for every nn.Linear in the MLP,
        in forward-pass order.
    """
    linears: List[Tuple[str, torch.nn.Linear]] = []
    for name, module in net.named_modules():
        if isinstance(module, torch.nn.Linear):
            linears.append((name, module))
    return linears


def freeze_all_except_last_n_linears(
    net: GreyBoxNet,
    n: int = 2,
) -> List[str]:
    """Freeze the entire model, then unfreeze the last *n* Linear layers.

    This implements the Duong et al. (2024) fine-tuning strategy:
    freeze feature-extraction layers, adapt only the task-specific head.

    For the default GreyBoxNet (4 hidden layers, Mish):
        Sequential layout = [L0, Act, L1, Act, L2, Act, L3, Act, L4_out]
        5 Linear layers total.  The last 2 are L3 (last hidden) and L4_out
        (output projection).

    Args:
        net:  A GreyBoxNet instance (already loaded with pre-trained weights).
        n:    Number of trailing Linear layers to keep trainable (default 2).

    Returns:
        List of parameter names that remain trainable (for logging).
    """
    # Step 1: freeze everything
    for param in net.parameters():
        param.requires_grad_(False)

    # Step 2: find all Linear layers in forward order
    linears = _find_linear_layers(net)
    if len(linears) < n:
        raise ValueError(
            f"Model has only {len(linears)} Linear layers but "
            f"freeze_all_except_last_n_linears was asked to unfreeze {n}."
        )

    # Step 3: unfreeze the last n
    unfrozen_names: List[str] = []
    for layer_name, layer_module in linears[-n:]:
        for pname, param in layer_module.named_parameters():
            param.requires_grad_(True)
            full_name = f"{layer_name}.{pname}"
            unfrozen_names.append(full_name)

    return unfrozen_names


# ---------------------------------------------------------------------------
# Fine-tuning loss (identical to train.py::step_loss)
# ---------------------------------------------------------------------------

def _step_loss(
    net: GreyBoxNet,
    al: AugmentedLagrangian,
    batch: dict,
    device: str,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Compute the full PINN loss: MSE + Augmented-Lagrangian penalty.

    This is intentionally identical to ``training.train.step_loss`` so that
    fine-tuning operates under the exact same physics constraints as
    pre-training.  We re-implement it here (instead of importing) to keep
    fine_tune.py self-contained and avoid circular-import fragility.

    Args:
        net:    The GreyBoxNet (partially frozen).
        al:     AugmentedLagrangian instance (fresh multipliers for fine-tuning).
        batch:  Dict with keys q, qdot, delta, tau_real, tau_theo.
        device: Torch device string.

    Returns:
        (total_loss, mse, tau_pred, tau_res, qdot) -- same contract as
        ``training.train.step_loss``.
    """
    q = batch["q"].to(device)
    qdot = batch["qdot"].to(device)
    delta = batch["delta"].to(device)
    tau_real = batch["tau_real"].to(device)
    tau_theo = batch["tau_theo"].to(device)

    tau_res = net(q, qdot, delta)
    tau_pred = tau_theo + tau_res

    mse = torch.nn.functional.mse_loss(tau_pred, tau_real)
    penalty = al.penalty(tau_pred, tau_res, qdot)
    return mse + penalty, mse, tau_pred, tau_res, qdot


# ---------------------------------------------------------------------------
# Main fine-tuning routine
# ---------------------------------------------------------------------------

def fine_tune(
    checkpoint_path: str,
    real_data_path: str,
    max_steps: int = 100,
    batch_size: int = 256,
    lr: float = 1e-4,
    rho: float = 1.0,
    config_path: str | None = None,
    output_dir: str | None = None,
    max_samples: int | None = None,
) -> str:
    """Run sim-to-real fine-tuning on a pre-trained GreyBoxNet.

    This is the programmatic entry point.  The CLI ``__main__`` block below
    parses arguments and delegates here.

    Args:
        checkpoint_path: Path to the pre-trained ``.pt`` state_dict.
        real_data_path:  Path to HDF5 file with real motor-babbling data
                         (same format as ``FrankaDynamicsDataset``).
        max_steps:       Total number of gradient steps (default 100,
                         per Duong et al. 2024 precedent; valid range 50-200).
        batch_size:      Mini-batch size for the fine-tuning DataLoader.
        lr:              Learning rate (default 1e-4, lower than pre-training
                         to avoid catastrophic forgetting).
        rho:             Initial penalty weight for AugmentedLagrangian
                         (same as pre-training default).
        config_path:     Optional explicit path to config.json.  If None,
                         ``load_grey_box_model`` looks in the same directory
                         as the checkpoint.
        output_dir:      Where to save the fine-tuned checkpoint.  If None,
                         saved next to the original checkpoint.
        max_samples:     If not None, subsample the real dataset to at most
                         this many entries (seed=42), reusing N4 machinery.

    Returns:
        Path to the saved fine-tuned checkpoint file.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # ---- 1. Load pre-trained model -------------------------------------------
    print(f"[fine_tune] Loading pre-trained checkpoint: {checkpoint_path}")
    net = load_grey_box_model(checkpoint_path, config_path=config_path, device=device)

    # load_grey_box_model sets eval mode and disables all gradients.
    # We need to re-enable training mode and selectively unfreeze.
    net.train()
    unfrozen = freeze_all_except_last_n_linears(net, n=2)

    n_trainable = sum(p.numel() for p in net.parameters() if p.requires_grad)
    n_total = sum(p.numel() for p in net.parameters())
    print(f"[fine_tune] Unfrozen parameters ({len(unfrozen)} tensors, "
          f"{n_trainable:,} / {n_total:,} values):")
    for name in unfrozen:
        print(f"  - {name}")

    # ---- 2. Load real-data dataset -------------------------------------------
    print(f"[fine_tune] Loading real data: {real_data_path}")
    dataset = FrankaDynamicsDataset(real_data_path, max_samples=max_samples)
    print(f"[fine_tune] Dataset size: {len(dataset)} samples")
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True,
                        drop_last=False)

    # ---- 3. Set up optimiser and constraints ---------------------------------
    # Only pass the unfrozen parameters to the optimiser to be explicit.
    trainable_params = [p for p in net.parameters() if p.requires_grad]
    opt = torch.optim.Adam(trainable_params, lr=lr)
    al = AugmentedLagrangian(rho=rho, device=device)

    # ---- 4. Fine-tuning loop -------------------------------------------------
    # We iterate over mini-batches from the DataLoader, counting gradient steps
    # (not epochs).  When the DataLoader is exhausted we wrap around.
    print(f"[fine_tune] Starting fine-tuning for {max_steps} gradient steps "
          f"(lr={lr}, batch_size={batch_size}, rho={rho})")

    step = 0
    log_rows = []
    last_tensors = None  # for multiplier update

    while step < max_steps:
        for batch in loader:
            if step >= max_steps:
                break

            opt.zero_grad()
            loss, mse, tau_pred, tau_res, qdot = _step_loss(net, al, batch, device)
            loss.backward()
            opt.step()

            last_tensors = (
                tau_pred.detach(),
                tau_res.detach(),
                qdot.detach(),
            )

            step += 1

            # Log every 10 steps or on first/last step
            if step == 1 or step % 10 == 0 or step == max_steps:
                report = al.violation_report(*last_tensors)
                print(f"  step {step:4d}/{max_steps} | loss {loss.item():.6f} "
                      f"(mse {mse.item():.6f}) | "
                      f"dissip_viol {report['mean_dissip_violation']:.4f}")
                log_rows.append({
                    "step": step,
                    "loss": loss.item(),
                    "mse": mse.item(),
                    "max_torque_viol": report["max_torque_violation"],
                    "mean_dissip_viol": report["mean_dissip_violation"],
                })

        # Dual-ascent multiplier update at the end of each pass through the data
        if last_tensors is not None:
            al.update_multipliers(*last_tensors)

    # ---- 5. Save fine-tuned checkpoint and log --------------------------------
    if output_dir is None:
        output_dir = os.path.dirname(checkpoint_path)
    os.makedirs(output_dir, exist_ok=True)

    save_path = os.path.join(output_dir, "greybox_finetuned.pt")
    torch.save(net.state_dict(), save_path)
    print(f"\n[fine_tune] Fine-tuned checkpoint saved to: {save_path}")

    # Save fine-tuning config for provenance
    ft_config = {
        "source_checkpoint": os.path.abspath(checkpoint_path),
        "real_data": os.path.abspath(real_data_path),
        "max_steps": max_steps,
        "batch_size": batch_size,
        "lr": lr,
        "rho": rho,
        "max_samples": max_samples,
        "n_trainable_params": n_trainable,
        "n_total_params": n_total,
        "unfrozen_layers": unfrozen,
        "timestamp": datetime.now().isoformat(),
        "device": device,
        "final_loss": log_rows[-1]["loss"] if log_rows else None,
        "final_mse": log_rows[-1]["mse"] if log_rows else None,
    }
    ft_config_path = os.path.join(output_dir, "finetune_config.json")
    with open(ft_config_path, "w") as fh:
        json.dump(ft_config, fh, indent=2)
    print(f"[fine_tune] Fine-tuning config saved to: {ft_config_path}")

    # Save step-level log
    log_path = os.path.join(output_dir, "finetune_log.csv")
    with open(log_path, "w") as fh:
        fh.write("step,loss,mse,max_torque_viol,mean_dissip_viol\n")
        for row in log_rows:
            fh.write(f"{row['step']},{row['loss']:.6f},{row['mse']:.6f},"
                     f"{row['max_torque_viol']:.4f},{row['mean_dissip_viol']:.4f}\n")
    print(f"[fine_tune] Step log saved to: {log_path}")

    return save_path


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    """Parse command-line arguments and run fine-tuning."""
    p = argparse.ArgumentParser(
        description=(
            "Sim-to-real fine-tuning for a pre-trained GreyBoxNet checkpoint. "
            "Implements the Duong et al. (2024) protocol: freeze all but the "
            "last 2 linear layers, fine-tune for ~100 gradient steps on real "
            "hardware data under the full PINN loss (MSE + AugmentedLagrangian)."
        ),
    )
    p.add_argument(
        "--checkpoint", type=str, required=True,
        help="Path to pre-trained .pt state_dict (e.g. models/run_XXX/greybox_best.pt).",
    )
    p.add_argument(
        "--config", type=str, default=None,
        help="Path to config.json for the checkpoint. If omitted, looks in the "
             "same directory as --checkpoint.",
    )
    p.add_argument(
        "--real_data", type=str, required=True,
        help="Path to HDF5 file with real motor-babbling data (same format as "
             "FrankaDynamicsDataset: q, qdot, tau_real, tau_theo, delta).",
    )
    p.add_argument(
        "--max_steps", type=int, default=100,
        help="Number of gradient steps (default 100, per Duong et al. 2024; "
             "recommended range 50-200).",
    )
    p.add_argument(
        "--batch_size", type=int, default=256,
        help="Mini-batch size for the fine-tuning DataLoader (default 256).",
    )
    p.add_argument(
        "--lr", type=float, default=1e-4,
        help="Learning rate for Adam (default 1e-4, lower than pre-training "
             "to avoid catastrophic forgetting).",
    )
    p.add_argument(
        "--rho", type=float, default=1.0,
        help="Initial penalty weight for AugmentedLagrangian (default 1.0).",
    )
    p.add_argument(
        "--max_samples", type=int, default=None,
        help="Subsample real data to at most N entries (seed=42). Useful for "
             "ablation: how few real samples suffice for sim-to-real transfer?",
    )
    p.add_argument(
        "--out", type=str, default=None,
        help="Output directory for fine-tuned checkpoint. If omitted, saves "
             "alongside the source checkpoint.",
    )
    args = p.parse_args()

    # Validate max_steps range
    if args.max_steps < 1:
        p.error("--max_steps must be >= 1.")
    if args.max_steps < 50 or args.max_steps > 200:
        print(f"[fine_tune] WARNING: --max_steps={args.max_steps} is outside the "
              f"Duong et al. (2024) recommended range of 50-200. Proceeding anyway.")

    fine_tune(
        checkpoint_path=args.checkpoint,
        real_data_path=args.real_data,
        max_steps=args.max_steps,
        batch_size=args.batch_size,
        lr=args.lr,
        rho=args.rho,
        config_path=args.config,
        output_dir=args.out,
        max_samples=args.max_samples,
    )


# ---------------------------------------------------------------------------
# Smoke test (runs with synthetic data via a temporary checkpoint)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # If CLI args are provided, run the real fine-tuning entry point.
    if len(sys.argv) > 1:
        main()
    else:
        # No args: run the smoke test to verify the module works end-to-end.
        import tempfile
        import numpy as np

        print("=" * 60)
        print("fine_tune.py smoke test (no CLI args detected)")
        print("=" * 60)

        # --- Create a temporary pre-trained checkpoint ---
        from network.grey_box_net import GreyBoxNet as _Net
        _net = _Net(hidden_dim=64, n_hidden_layers=3, activation="mish")

        with tempfile.TemporaryDirectory() as tmpdir:
            ckpt = os.path.join(tmpdir, "greybox_best.pt")
            cfg = os.path.join(tmpdir, "config.json")
            torch.save(_net.state_dict(), ckpt)
            with open(cfg, "w") as fh:
                json.dump({
                    "hidden_dim": 64,
                    "n_hidden_layers": 3,
                    "activation": "mish",
                }, fh)

            # --- Create a temporary HDF5 "real data" file ---
            try:
                import h5py
            except ImportError:
                print("SKIP: h5py not installed — cannot create synthetic HDF5 "
                      "for smoke test. Install with: pip install h5py")
                sys.exit(0)

            h5_path = os.path.join(tmpdir, "real_data.h5")
            n_samples = 128
            rng = np.random.default_rng(99)
            with h5py.File(h5_path, "w") as f:
                f.create_dataset("q", data=rng.standard_normal((n_samples, 7)).astype(np.float32))
                f.create_dataset("qdot", data=rng.standard_normal((n_samples, 7)).astype(np.float32) * 0.5)
                f.create_dataset("tau_real", data=rng.standard_normal((n_samples, 7)).astype(np.float32) * 20)
                f.create_dataset("tau_theo", data=rng.standard_normal((n_samples, 7)).astype(np.float32) * 20)
                f.create_dataset("delta", data=rng.random((n_samples,)).astype(np.float32) * 3)

            # --- Run fine-tuning with 10 steps ---
            save_path = fine_tune(
                checkpoint_path=ckpt,
                real_data_path=h5_path,
                max_steps=10,
                batch_size=32,
                lr=1e-3,
                rho=1.0,
                output_dir=tmpdir,
            )

            assert os.path.isfile(save_path), f"Fine-tuned checkpoint not found: {save_path}"
            assert os.path.isfile(os.path.join(tmpdir, "finetune_config.json"))
            assert os.path.isfile(os.path.join(tmpdir, "finetune_log.csv"))

            # Verify the saved checkpoint loads correctly
            loaded = torch.load(save_path, map_location="cpu", weights_only=True)
            assert isinstance(loaded, dict)
            print(f"\nFine-tuned checkpoint has {len(loaded)} state_dict entries.")

            # --- Verify freeze correctness ---
            # Re-load and check that freezing works as expected
            net2 = _Net(hidden_dim=64, n_hidden_layers=3, activation="mish")
            net2.load_state_dict(torch.load(ckpt, map_location="cpu", weights_only=True))
            unfrozen = freeze_all_except_last_n_linears(net2, n=2)
            # 3 hidden layers + 1 output = 4 linear layers total.
            # Last 2 = layer indices 2 and 3.
            # Each Linear has weight + bias = 2 params per layer, so 4 unfrozen tensors.
            assert len(unfrozen) == 4, f"Expected 4 unfrozen param tensors, got {len(unfrozen)}: {unfrozen}"
            frozen_count = sum(1 for p in net2.parameters() if not p.requires_grad)
            trainable_count = sum(1 for p in net2.parameters() if p.requires_grad)
            assert trainable_count == 4, f"Expected 4 trainable param tensors, got {trainable_count}"
            print(f"Freeze check: {frozen_count} frozen, {trainable_count} trainable -- OK")

        print("\n" + "=" * 60)
        print("fine_tune.py smoke test PASSED")
        print("=" * 60)
