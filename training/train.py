"""
Stage 1 training loop.

Loss = MSE(tau_theo + tau_res, tau_real) + AugmentedLagrangian(torque, dissipativity)

Run a smoke test on synthetic data (no pinocchio / no real data needed):
    python -m training.train --synthetic --epochs 5

Run with FrictionNet (novelty N2, Liu et al. 2024):
    python -m training.train --synthetic --epochs 5 --use_friction_net

Run on a single HDF5 dataset:
    python -m training.train --data data/fourier_baseline_0kg.h5 --epochs 200

Multi-payload training (0 kg + 1 kg + 3 kg concatenated):
    python -m training.train --data data/fourier_baseline_0kg.h5 data/fourier_baseline_1kg.h5 data/fourier_baseline_3kg.h5 --epochs 200

Data-efficiency ablation (novelty N4 from Liu et al. 2024):
    python -m training.train --data data/fourier_baseline_0kg.h5 --max_samples 5000 --epochs 200
    Truncates the dataset to N random samples (seed=42) before splitting
    into train/val/test, enabling direct comparison against Liu et al.'s
    25 000-sample benchmark.

Black-box baseline ("MLP direct" in the school report's baseline table):
    python -m training.train --data ... --no_rnea --tag baseline-mlp-direct --epochs 200
    Drops the analytical term so the network predicts the whole torque.

Spatial-encoding ablation (asked for by the report's limitations section):
    python -m training.train --data ... --encoding raw --tag ablation-raw-q --epochs 200
    Feeds [q, qdot, delta] instead of [sin q, cos q, qdot, delta].

SPLIT NOTE. As of training/splits.py the partition is 80/10/10 train/val/test.
The number to quote in any write-up is the TEST RMSE printed at the end and
stored as ``per_joint_test_rmse`` in config.json. ``per_joint_val_rmse`` is
in-sample for checkpoint selection and is kept only as a diagnostic. Runs made
before splits.py used a different 90/10 partition and are NOT comparable.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime

import torch
from torch.utils.data import DataLoader

from network.grey_box_net import GreyBoxNet, ENCODINGS
from network.friction_net import FrictionNet
from training.constraints import AugmentedLagrangian
from training.dataset import SyntheticDataset, FrankaDynamicsDataset, MultiPayloadDataset
from training.splits import make_splits, describe, SPLIT_SEED, SPLIT_FRACTIONS


def build_dataset(args):
    """Instantiate the full dataset (before splitting), honouring --max_samples."""
    max_samples = getattr(args, "max_samples", None)

    if args.synthetic or not args.data:
        full = SyntheticDataset(n=args.synthetic_n, max_samples=max_samples)
    elif len(args.data) > 1:
        full = MultiPayloadDataset(args.data, max_samples=max_samples)
    else:
        full = FrankaDynamicsDataset(args.data[0], max_samples=max_samples)

    if max_samples is not None:
        print(f"[N4] Dataset truncated to {len(full)} samples "
              f"(max_samples={max_samples})")
    return full


def build_loaders(args):
    """Build train / validation / test DataLoaders.

    The split is an 80/10/10 partition from ``training.splits`` -- the single
    source of truth shared with ``controller/compute_error_bound.py`` and
    ``evaluation/eval_baselines.py``, so all three see the SAME test set.

    This replaces the old 90/10 train/val split, under which the reported RMSE
    and the Lyapunov bound epsilon_j were both measured on the very set used to
    select the checkpoint. See training/splits.py for the full rationale.
    """
    full = build_dataset(args)
    print(f"[split] {describe(len(full))}")
    train_ds, val_ds, test_ds = make_splits(full)
    return (
        DataLoader(train_ds, batch_size=args.batch_size, shuffle=True),
        DataLoader(val_ds, batch_size=args.batch_size, shuffle=False),
        DataLoader(test_ds, batch_size=args.batch_size, shuffle=False),
    )


def step_loss(net, al, batch, device, friction_net=None, use_rnea=True,
              apply_dissip=True):
    """Compute combined loss for one mini-batch.

    When ``friction_net`` is provided (--use_friction_net), the combined
    residual is tau_res = tau_res_grey + tau_res_fric, where the friction
    component is dissipative by construction (novelty N2, Liu et al. 2024).

    Args:
        use_rnea:     True  -> grey box, tau_pred = tau_theo + tau_res.
                      False -> black-box baseline (--no_rnea): the network alone
                      predicts the whole torque, tau_pred = tau_res. This is the
                      "MLP direct" line of the report's baseline table.
        apply_dissip: whether the dissipativity constraint is meaningful. It is
                      NOT for the black-box baseline: there tau_res is the FULL
                      joint torque, which legitimately does work on the system,
                      so tau_res . qdot <= 0 would be a physically wrong
                      constraint and would cripple the baseline unfairly. The
                      torque-limit constraint stays on in both cases -- it is a
                      statement about the actuators, true for any model.
    """
    q = batch["q"].to(device)
    qdot = batch["qdot"].to(device)
    delta = batch["delta"].to(device)
    tau_real = batch["tau_real"].to(device)
    tau_theo = batch["tau_theo"].to(device)

    tau_res = net(q, qdot, delta)
    if friction_net is not None:
        tau_res_fric = friction_net(q, qdot, delta)
        tau_res = tau_res + tau_res_fric
    tau_pred = tau_theo + tau_res if use_rnea else tau_res

    mse = torch.nn.functional.mse_loss(tau_pred, tau_real)
    # Zeroing the residual fed to the dissipativity term switches that term off
    # without touching the torque-limit term (max(0, 0 . qdot) == 0).
    tau_res_for_dissip = tau_res if apply_dissip else torch.zeros_like(tau_res)
    penalty = al.penalty(tau_pred, tau_res_for_dissip, qdot)
    return mse + penalty, mse, tau_pred, tau_res_for_dissip, qdot


@torch.no_grad()
def per_joint_rmse(net, al, loader, device, friction_net=None, use_rnea=True,
                   apply_dissip=True):
    """Per-joint RMSE (Nm) over a whole loader. Returns a (7,) CPU tensor."""
    net.eval()
    if friction_net is not None:
        friction_net.eval()
    se = torch.zeros(7)
    n = 0
    for batch in loader:
        _, _, tau_pred, _, _ = step_loss(
            net, al, batch, device, friction_net=friction_net,
            use_rnea=use_rnea, apply_dissip=apply_dissip,
        )
        tau_real_b = batch["tau_real"].to(device)
        se += (tau_pred - tau_real_b).pow(2).sum(dim=0).cpu()
        n += tau_pred.shape[0]
    return (se / max(n, 1)).sqrt()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=str, nargs="+", default=[],
                   help="One or more HDF5 dataset files. Multiple files are "
                        "concatenated (multi-payload training).")
    p.add_argument("--synthetic", action="store_true")
    p.add_argument("--synthetic_n", type=int, default=4096)
    p.add_argument("--max_samples", type=int, default=None,
                   help="Truncate dataset to N random samples (seed=42) before "
                        "train/val split. Enables data-efficiency ablation "
                        "(novelty N4, Liu et al. 2024). Default: None (use all).")
    p.add_argument("--epochs", type=int, default=100)
    p.add_argument("--batch_size", type=int, default=256)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--hidden_dim", type=int, default=256)
    p.add_argument("--n_hidden_layers", type=int, default=4)
    p.add_argument("--activation", type=str, default="mish")
    p.add_argument("--rho", type=float, default=1.0)
    p.add_argument("--use_friction_net", action="store_true",
                   help="Enable FrictionNet sub-module (novelty N2, Liu et al. "
                        "2024). Adds a structurally dissipative friction torque "
                        "tau_friction = -D*qdot to the residual.")
    p.add_argument("--no_rnea", action="store_true",
                   help="BLACK-BOX BASELINE ('MLP direct' in the report's "
                        "baseline table). Drops the analytical tau_theo term so "
                        "the network alone predicts the whole torque. Same "
                        "encoding, same capacity, same budget as the grey box, "
                        "so the measured gap is attributable to the structure "
                        "and not to capacity. Also disables the dissipativity "
                        "constraint, which is meaningless when tau_res is the "
                        "full torque (see step_loss).")
    p.add_argument("--encoding", type=str, default="sincos", choices=ENCODINGS,
                   help="Input encoding. 'sincos' (default) is [sin(q), cos(q), "
                        "qdot, delta] in R^22. 'raw' is [q, qdot, delta] in R^15 "
                        "and exists ONLY for the spatial-encoding ablation the "
                        "report's limitations section asks for. Never deploy a "
                        "'raw' model: it reintroduces the wrap discontinuity.")
    p.add_argument("--tag", type=str, default="",
                   help="Free-text label stored in config.json, e.g. "
                        "'baseline-mlp-direct'. Makes runs identifiable without "
                        "having to diff their configs.")
    p.add_argument("--out", type=str, default="models")
    args = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    train_loader, val_loader, test_loader = build_loaders(args)

    use_rnea = not args.no_rnea
    apply_dissip = use_rnea
    if args.no_rnea:
        print("[baseline] --no_rnea: BLACK BOX. tau_pred = network output alone; "
              "analytical RNEA term dropped; dissipativity constraint disabled.")
    if args.encoding != "sincos":
        print(f"[ablation] encoding={args.encoding} (default is 'sincos')")

    net = GreyBoxNet(args.hidden_dim, args.n_hidden_layers, args.activation,
                     encoding=args.encoding).to(device)
    al = AugmentedLagrangian(rho=args.rho, device=device)

    # --- FrictionNet (novelty N2, Liu et al. 2024) ---
    friction_net = None
    if args.use_friction_net:
        friction_net = FrictionNet(encoding=args.encoding).to(device)
        all_params = list(net.parameters()) + list(friction_net.parameters())
        fn_params = sum(p.numel() for p in friction_net.parameters())
        print(f"[N2] FrictionNet enabled ({fn_params} parameters)")
    else:
        all_params = list(net.parameters())

    opt = torch.optim.Adam(all_params, lr=args.lr)

    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    run_dir = os.path.join(args.out, run_id)
    os.makedirs(run_dir, exist_ok=True)
    log_path = os.path.join(run_dir, "train_log.csv")
    with open(log_path, "w") as f:
        f.write("epoch,train_loss,train_mse,val_loss,val_mse,max_torque_viol,mean_dissip_viol\n")

    best_val = float("inf")
    for epoch in range(1, args.epochs + 1):
        net.train()
        if friction_net is not None:
            friction_net.train()
        tl = tm = 0.0
        last = None
        for batch in train_loader:
            opt.zero_grad()
            loss, mse, tau_pred, tau_res, qdot = step_loss(
                net, al, batch, device, friction_net=friction_net,
                use_rnea=use_rnea, apply_dissip=apply_dissip,
            )
            loss.backward()
            opt.step()
            tl += loss.item(); tm += mse.item()
            last = (tau_pred.detach(), tau_res.detach(), qdot.detach())
        al.update_multipliers(*last)  # dual ascent once per epoch

        net.eval()
        if friction_net is not None:
            friction_net.eval()
        vl = vm = 0.0
        with torch.no_grad():
            for batch in val_loader:
                loss, mse, *_ = step_loss(
                    net, al, batch, device, friction_net=friction_net,
                    use_rnea=use_rnea, apply_dissip=apply_dissip,
                )
                vl += loss.item(); vm += mse.item()
        vl /= len(val_loader); vm /= len(val_loader)
        tl /= len(train_loader); tm /= len(train_loader)

        rep = al.violation_report(*last)
        with open(log_path, "a") as f:
            f.write(f"{epoch},{tl:.6f},{tm:.6f},{vl:.6f},{vm:.6f},"
                    f"{rep['max_torque_violation']:.4f},{rep['mean_dissip_violation']:.4f}\n")

        if epoch % max(1, args.epochs // 10) == 0 or epoch == 1:
            print(f"epoch {epoch:4d} | train {tl:.4f} (mse {tm:.4f}) | "
                  f"val {vl:.4f} (mse {vm:.4f}) | dissip_viol {rep['mean_dissip_violation']:.4f}")
            # Log FrictionNet D_diag statistics once per print epoch
            if friction_net is not None:
                with torch.no_grad():
                    # Use last batch from train_loader for D_diag logging
                    q_log = batch["q"].to(device)
                    qdot_log = batch["qdot"].to(device)
                    delta_log = batch["delta"].to(device)
                    D_mean = friction_net.forward_D(q_log, qdot_log, delta_log).mean(0)
                    D_str = ", ".join(f"{d:.4f}" for d in D_mean.tolist())
                    print(f"         D_diag mean/joint: [{D_str}]")

        if vl < best_val:
            best_val = vl
            torch.save(net.state_dict(), os.path.join(run_dir, "greybox_best.pt"))
            if friction_net is not None:
                torch.save(
                    friction_net.state_dict(),
                    os.path.join(run_dir, "friction_net_best.pt"),
                )

    # ------------------------------------------------------------------
    # Final metrics.
    #
    # The checkpoint just restored is the one selected on VALIDATION loss, so
    # validation RMSE is an in-sample number for the selection criterion and
    # must NOT be the figure reported in the paper. The TEST split has been
    # untouched by both training and selection: that is the number to quote.
    # Both are recorded so the gap between them is visible -- a large gap is
    # itself evidence of overfitting to the selection criterion.
    # ------------------------------------------------------------------
    best_ckpt = os.path.join(run_dir, "greybox_best.pt")
    if os.path.isfile(best_ckpt):
        net.load_state_dict(torch.load(best_ckpt, map_location=device,
                                       weights_only=True))
        if friction_net is not None:
            fric_ckpt = os.path.join(run_dir, "friction_net_best.pt")
            if os.path.isfile(fric_ckpt):
                friction_net.load_state_dict(
                    torch.load(fric_ckpt, map_location=device, weights_only=True)
                )
        print("\n[eval] Restored best-validation checkpoint for final metrics.")

    kw = dict(friction_net=friction_net, use_rnea=use_rnea,
              apply_dissip=apply_dissip)
    val_rmse = per_joint_rmse(net, al, val_loader, device, **kw)
    test_rmse = per_joint_rmse(net, al, test_loader, device, **kw)

    def _fmt(t):
        return "[" + ", ".join(f"{v:.4f}" for v in t.tolist()) + "]"

    print(f"\n[eval] Per-joint VAL  RMSE (Nm), in-sample for selection: {_fmt(val_rmse)}")
    print(f"[eval] Per-joint TEST RMSE (Nm), HELD OUT  -> REPORT THIS: {_fmt(test_rmse)}")
    print(f"[eval] Mean test RMSE: {test_rmse.mean().item():.4f} Nm")

    # [N2-WhenPhysics] 87 Nm vs 12 Nm torque-scale imbalance, on the test split.
    inner = test_rmse[:4].mean().item()
    outer = test_rmse[4:].mean().item()
    print(f"  Joints 1-4 (87 Nm): {inner:.4f} Nm  |  Joints 5-7 (12 Nm): {outer:.4f} Nm")
    ratio = outer / inner if inner > 0 else float("inf")
    if ratio > 2.0:
        print(f"  -> Imbalance detected (ratio {ratio:.1f}x). "
              f"Consider EMA loss balancing (beta=0.95) in training/train.py.")
    else:
        print(f"  -> Scale within tolerance (ratio {ratio:.1f}x).")

    # save config + final
    config = vars(args) | {
        "best_val_loss": best_val,
        "run_id": run_id,
        "split_seed": SPLIT_SEED,
        "split_fractions": list(SPLIT_FRACTIONS),
        "per_joint_val_rmse": val_rmse.tolist(),
        "per_joint_test_rmse": test_rmse.tolist(),
        "mean_test_rmse": test_rmse.mean().item(),
    }
    with open(os.path.join(run_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=2)
    saved = "greybox_best.pt"
    if friction_net is not None:
        saved += " + friction_net_best.pt"
    print(f"\nDone. Best val loss {best_val:.4f}. Saved to {run_dir}/ ({saved})")


if __name__ == "__main__":
    main()
