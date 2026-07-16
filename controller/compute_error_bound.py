"""
Compute the real per-joint tau error bound from a trained checkpoint, for
feeding into controller.lyapunov_gains.compute_lyapunov_gains().

Why max, not RMSE: the Lyapunov stability guarantee (Liu et al. 2024,
Proposition 1) requires a bound that holds for EVERY sample, not an average.
Using RMSE as tau_error_bound would understate the true worst case and
silently break the stability guarantee whenever a real error exceeds it.

Reconstructs the exact same validation split used by training/train.py
(MultiPayloadDataset over the same files, random_split seed=0, 90/10),
so the reported bound matches what the reported per_joint_val_rmse in
config.json was computed on.

Usage:
    python -m controller.compute_error_bound \\
        --run_dir models/run_20260716_110933 \\
        --data data/isaac_0.0kg.h5 data/isaac_1.0kg.h5 data/isaac_3.0kg.h5
"""

from __future__ import annotations

import argparse
import json
import os

import torch

from controller.model_loader import load_grey_box_model
from network.constants import N_JOINTS, FRICTION_NET_HIDDEN
from network.friction_net import FrictionNet
from training.dataset import MultiPayloadDataset


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run_dir", type=str, required=True,
                    help="Directory containing greybox_best.pt, config.json, "
                         "and (if used) friction_net_best.pt")
    p.add_argument("--data", type=str, nargs="+", required=True,
                    help="Same HDF5 files (same order) used for training.")
    p.add_argument("--batch_size", type=int, default=512)
    args = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"

    ckpt_path = os.path.join(args.run_dir, "greybox_best.pt")
    config_path = os.path.join(args.run_dir, "config.json")
    with open(config_path) as fh:
        cfg = json.load(fh)

    net = load_grey_box_model(ckpt_path, config_path=config_path, device=device)

    friction_net = None
    fric_path = os.path.join(args.run_dir, "friction_net_best.pt")
    if cfg.get("use_friction_net") and os.path.isfile(fric_path):
        friction_net = FrictionNet(hidden_dim=FRICTION_NET_HIDDEN).to(device)
        friction_net.load_state_dict(
            torch.load(fric_path, map_location=device, weights_only=True)
        )
        friction_net.eval()
        for param in friction_net.parameters():
            param.requires_grad_(False)
        print(f"[compute_error_bound] Loaded FrictionNet from {fric_path}")

    # Reconstruct the exact same split as training/train.py::build_loaders
    full = MultiPayloadDataset(args.data, max_samples=cfg.get("max_samples"))
    n_val = max(1, int(0.1 * len(full)))
    n_train = len(full) - n_val
    _, val_ds = torch.utils.data.random_split(
        full, [n_train, n_val], generator=torch.Generator().manual_seed(0)
    )
    loader = torch.utils.data.DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)
    print(f"[compute_error_bound] Validation set: {len(val_ds)} samples")

    all_abs_err = []
    all_q, all_qdot, all_delta = [], [], []
    all_tau_real, all_tau_theo, all_tau_res, all_tau_pred = [], [], [], []

    with torch.no_grad():
        for batch in loader:
            q = batch["q"].to(device)
            qdot = batch["qdot"].to(device)
            delta = batch["delta"].to(device)
            tau_real = batch["tau_real"].to(device)
            tau_theo = batch["tau_theo"].to(device)

            tau_res = net(q, qdot, delta)
            if friction_net is not None:
                tau_res = tau_res + friction_net(q, qdot, delta)
            tau_pred = tau_theo + tau_res

            all_abs_err.append((tau_pred - tau_real).abs().cpu())
            all_q.append(q.cpu())
            all_qdot.append(qdot.cpu())
            all_delta.append(delta.cpu())
            all_tau_real.append(tau_real.cpu())
            all_tau_theo.append(tau_theo.cpu())
            all_tau_res.append(tau_res.cpu())
            all_tau_pred.append(tau_pred.cpu())

    abs_err = torch.cat(all_abs_err)       # (N, 7)
    q_all = torch.cat(all_q)
    qdot_all = torch.cat(all_qdot)
    delta_all = torch.cat(all_delta)
    tau_real_all = torch.cat(all_tau_real)
    tau_theo_all = torch.cat(all_tau_theo)
    tau_res_all = torch.cat(all_tau_res)
    tau_pred_all = torch.cat(all_tau_pred)

    rmse = torch.sqrt((abs_err ** 2).mean(dim=0))
    max_abs_err = abs_err.max(dim=0).values

    print("\nPer-joint RMSE (Nm) -- cross-check against config.json's per_joint_val_rmse:")
    print("  [" + ", ".join(f"{v:.4f}" for v in rmse.tolist()) + "]")
    print(f"\nconfig.json per_joint_val_rmse was:")
    print(f"  {cfg.get('per_joint_val_rmse')}")

    print("\nPer-joint error percentiles (Nm) -- diagnosing tail shape before "
          "trusting the max as a Lyapunov bound:")
    percentiles = [50, 90, 99, 99.9, 100]
    header = "  joint | " + " | ".join(f"p{p:>5}" for p in percentiles)
    print(header)
    for j in range(N_JOINTS):
        vals = [torch.quantile(abs_err[:, j], p / 100.0).item()
                if p < 100 else abs_err[:, j].max().item()
                for p in percentiles]
        print(f"  J{j+1:4d} | " + " | ".join(f"{v:6.3f}" for v in vals))

    print("\nWorst 5 samples per joint (for diagnosis -- inspect q/qdot/delta for "
          "outlier configs, e.g. near joint limits or high qdot):")
    for j in range(N_JOINTS):
        worst_idx = torch.topk(abs_err[:, j], k=min(5, abs_err.shape[0])).indices
        print(f"\n  --- Joint {j+1} worst offenders ---")
        for i in worst_idx.tolist():
            print(f"    err={abs_err[i, j]:.2f} Nm | delta={delta_all[i].item():.2f} kg | "
                  f"q[{j}]={q_all[i, j]:.3f} rad | qdot[{j}]={qdot_all[i, j]:.3f} rad/s | "
                  f"tau_theo={tau_theo_all[i, j]:.2f} | tau_res={tau_res_all[i, j]:.2f} | "
                  f"tau_pred={tau_pred_all[i, j]:.2f} | tau_real={tau_real_all[i, j]:.2f}")


if __name__ == "__main__":
    main()
