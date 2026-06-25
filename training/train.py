"""
Stage 1 training loop.

Loss = MSE(tau_theo + tau_res, tau_real) + AugmentedLagrangian(torque, dissipativity)

Run a smoke test on synthetic data (no pinocchio / no real data needed):
    python -m training.train --synthetic --epochs 5

Run with FrictionNet (novelty N2, Liu et al. 2024):
    python -m training.train --synthetic --epochs 5 --use_friction_net

Run on a real HDF5 dataset:
    python -m training.train --data data/dataset_1kg_xxx.h5 --epochs 200

Data-efficiency ablation (novelty N4 from Liu et al. 2024):
    python -m training.train --data data/dataset.h5 --max_samples 5000 --epochs 200
    Truncates the dataset to N random samples (seed=42) before splitting
    into train/val, enabling direct comparison against Liu et al.'s
    25 000-sample benchmark.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime

import torch
from torch.utils.data import DataLoader

from network.grey_box_net import GreyBoxNet
from network.friction_net import FrictionNet
from training.constraints import AugmentedLagrangian
from training.dataset import SyntheticDataset, FrankaDynamicsDataset


def build_loaders(args):
    """Build train and validation DataLoaders.

    When ``args.max_samples`` is set (novelty N4), the dataset is truncated
    to that many samples *before* the 90/10 train/val split, so both
    partitions see only the reduced data budget.
    """
    max_samples = getattr(args, "max_samples", None)

    if args.synthetic or not args.data:
        full = SyntheticDataset(n=args.synthetic_n, max_samples=max_samples)
    else:
        full = FrankaDynamicsDataset(args.data, max_samples=max_samples)

    if max_samples is not None:
        print(f"[N4] Dataset truncated to {len(full)} samples "
              f"(max_samples={max_samples})")

    n_val = max(1, int(0.1 * len(full)))
    n_train = len(full) - n_val
    train_ds, val_ds = torch.utils.data.random_split(
        full, [n_train, n_val], generator=torch.Generator().manual_seed(0)
    )
    return (
        DataLoader(train_ds, batch_size=args.batch_size, shuffle=True),
        DataLoader(val_ds, batch_size=args.batch_size, shuffle=False),
    )


def step_loss(net, al, batch, device, friction_net=None):
    """Compute combined loss for one mini-batch.

    When ``friction_net`` is provided (--use_friction_net), the combined
    residual is tau_res = tau_res_grey + tau_res_fric, where the friction
    component is dissipative by construction (novelty N2, Liu et al. 2024).
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
    tau_pred = tau_theo + tau_res

    mse = torch.nn.functional.mse_loss(tau_pred, tau_real)
    penalty = al.penalty(tau_pred, tau_res, qdot)
    return mse + penalty, mse, tau_pred, tau_res, qdot


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=str, default="")
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
    p.add_argument("--out", type=str, default="models")
    args = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    train_loader, val_loader = build_loaders(args)

    net = GreyBoxNet(args.hidden_dim, args.n_hidden_layers, args.activation).to(device)
    al = AugmentedLagrangian(rho=args.rho, device=device)

    # --- FrictionNet (novelty N2, Liu et al. 2024) ---
    friction_net = None
    if args.use_friction_net:
        friction_net = FrictionNet().to(device)
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

    # save config + final
    config = vars(args) | {"best_val_loss": best_val, "run_id": run_id}
    with open(os.path.join(run_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=2)
    saved = "greybox_best.pt"
    if friction_net is not None:
        saved += " + friction_net_best.pt"
    print(f"\nDone. Best val loss {best_val:.4f}. Saved to {run_dir}/ ({saved})")


if __name__ == "__main__":
    main()
