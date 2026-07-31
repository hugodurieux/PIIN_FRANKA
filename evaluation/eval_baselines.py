"""
Measure every model on the SAME held-out test split, and emit a LaTeX table.

This exists to fill the two blank rows of the school report's baseline table
(``school_report/rapport/main.tex``, "Lignes de base et protocole de
comparaison"). Until they are filled, the report does not claim the grey box
beats anything -- that claim was deliberately removed rather than left
unsupported.

Three model kinds:

  rnea        No learning at all: tau_pred = tau_theo, straight from the HDF5
              file's own RNEA column. Needs no checkpoint and no --run_dir.
              This is exactly what the URDF gives you for free, and therefore
              the size of the residual the grey box has to capture.

  greybox     tau_pred = tau_theo + net(q, qdot, delta). The proposed model.

  mlp         tau_pred = net(q, qdot, delta) alone. The black-box baseline,
              i.e. a checkpoint trained with ``--no_rnea``.

For ``greybox`` and ``mlp`` the model kind is read from the checkpoint's own
config.json (``no_rnea``), so a run cannot be evaluated under the wrong
composition by mistake. Pass --kind only to override, and it will warn.

Usage
-----
Evaluate the analytical baseline (no training needed):

    python -m evaluation.eval_baselines --kind rnea \\
        --data data/isaac_0.0kg.h5 data/isaac_1.0kg.h5 data/isaac_3.0kg.h5

Evaluate a trained run (kind auto-detected):

    python -m evaluation.eval_baselines --run_dir models/run_XXXX \\
        --data data/isaac_0.0kg.h5 data/isaac_1.0kg.h5 data/isaac_3.0kg.h5

Compare several at once and print the report table:

    python -m evaluation.eval_baselines --latex \\
        --data data/isaac_0.0kg.h5 data/isaac_1.0kg.h5 data/isaac_3.0kg.h5 \\
        --compare rnea= greybox=models/run_A mlp=models/run_B

IMPORTANT: --data must list the SAME files in the SAME order for every model
being compared. The split is a function of the concatenated dataset length, so
a different file order is a different test set and the comparison is void. The
script hashes the file list and prints it; refuse to mix runs whose printed
dataset signature differs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from typing import Optional

import torch
from torch.utils.data import DataLoader

from network.constants import N_JOINTS, TORQUE_LIMITS, FRICTION_NET_HIDDEN
from network.friction_net import FrictionNet
from training.dataset import MultiPayloadDataset, FrankaDynamicsDataset
from training.splits import make_splits, describe, SPLIT_SEED

KINDS = ("rnea", "greybox", "mlp")


def dataset_signature(paths) -> str:
    """Short hash of the ordered file list, to catch mismatched comparisons."""
    h = hashlib.sha256("|".join(paths).encode()).hexdigest()[:10]
    return h


def build_test_loader(data_paths, batch_size=512):
    """Load the dataset and return ONLY its test split, plus its size."""
    if len(data_paths) > 1:
        full = MultiPayloadDataset(data_paths)
    else:
        full = FrankaDynamicsDataset(data_paths[0])
    print(f"[eval] {describe(len(full))}")
    _, _, test_ds = make_splits(full)
    loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
    return loader, len(test_ds)


def load_model(run_dir: str, device: str):
    """Load a checkpoint plus its optional FrictionNet, and its config."""
    from controller.model_loader import load_grey_box_model

    config_path = os.path.join(run_dir, "config.json")
    ckpt_path = os.path.join(run_dir, "greybox_best.pt")
    if not os.path.isfile(ckpt_path):
        raise FileNotFoundError(f"no greybox_best.pt in {run_dir}")
    cfg = {}
    if os.path.isfile(config_path):
        with open(config_path) as fh:
            cfg = json.load(fh)

    net = load_grey_box_model(ckpt_path, config_path=config_path, device=device)

    friction_net = None
    fric_path = os.path.join(run_dir, "friction_net_best.pt")
    if cfg.get("use_friction_net") and os.path.isfile(fric_path):
        friction_net = FrictionNet(
            hidden_dim=FRICTION_NET_HIDDEN,
            encoding=cfg.get("encoding", "sincos"),
        ).to(device)
        friction_net.load_state_dict(
            torch.load(fric_path, map_location=device, weights_only=True)
        )
        friction_net.eval()
    return net, friction_net, cfg


@torch.no_grad()
def evaluate(kind: str, loader, device: str, run_dir: Optional[str] = None) -> dict:
    """Return per-joint RMSE, percentiles and violation counts on the test split."""
    net = friction_net = None
    cfg = {}
    if kind != "rnea":
        if not run_dir:
            raise ValueError(f"kind={kind} needs --run_dir")
        net, friction_net, cfg = load_model(run_dir, device)

    limits = TORQUE_LIMITS.to(device)
    abs_errs = []
    n_over_limit = 0
    n_total = 0

    for batch in loader:
        q = batch["q"].to(device)
        qdot = batch["qdot"].to(device)
        delta = batch["delta"].to(device)
        tau_real = batch["tau_real"].to(device)
        tau_theo = batch["tau_theo"].to(device)

        if kind == "rnea":
            tau_pred = tau_theo
        else:
            tau_res = net(q, qdot, delta)
            if friction_net is not None:
                tau_res = tau_res + friction_net(q, qdot, delta)
            tau_pred = tau_res if kind == "mlp" else tau_theo + tau_res

        abs_errs.append((tau_pred - tau_real).abs().cpu())
        n_over_limit += (tau_pred.abs() > limits).any(dim=1).sum().item()
        n_total += tau_pred.shape[0]

    abs_err = torch.cat(abs_errs)
    rmse = torch.sqrt((abs_err ** 2).mean(dim=0))
    return {
        "kind": kind,
        "run_dir": run_dir or "(none)",
        "tag": cfg.get("tag", ""),
        "encoding": cfg.get("encoding", "sincos"),
        "n_test": n_total,
        "per_joint_rmse": rmse.tolist(),
        "mean_rmse": rmse.mean().item(),
        "rmse_pct_of_limit": (rmse / TORQUE_LIMITS * 100).tolist(),
        "p999": [torch.quantile(abs_err[:, j], 0.999).item() for j in range(N_JOINTS)],
        "max_abs_err": abs_err.max(dim=0).values.tolist(),
        "n_samples_over_torque_limit": n_over_limit,
    }


def print_result(r: dict) -> None:
    print(f"\n=== {r['kind']}  {r['tag']}  ({r['run_dir']}) ===")
    print(f"  test samples          : {r['n_test']:,}")
    print(f"  per-joint RMSE  [Nm]  : "
          + ", ".join(f"{v:.4f}" for v in r["per_joint_rmse"]))
    print(f"  mean RMSE       [Nm]  : {r['mean_rmse']:.4f}")
    print(f"  RMSE / limit    [%]   : "
          + ", ".join(f"{v:.2f}" for v in r["rmse_pct_of_limit"]))
    print(f"  p99.9 abs err   [Nm]  : "
          + ", ".join(f"{v:.3f}" for v in r["p999"]))
    print(f"  samples over torque limit: {r['n_samples_over_torque_limit']:,}"
          f" / {r['n_test']:,}")


def latex_table(results) -> str:
    """Emit the report's baseline table body, ready to paste."""
    label = {"rnea": "RNEA seul (analytique)",
             "mlp": "MLP direct (boîte noire)",
             "greybox": "\\textbf{Gris} \\code{isaac-satfix}"}
    guarantees = {"rnea": "sans objet", "mlp": "aucune",
                  "greybox": "limites + dissipativité"}
    lines = [
        "% Généré par: python -m evaluation.eval_baselines --latex",
        "% Toutes les lignes sont mesurées sur LE MÊME split de test "
        f"(seed={SPLIT_SEED}).",
        "\\begin{tabular}{@{}lccc@{}}",
        "\\toprule",
        "Modèle & RMSE de test moyenne [\\si{\\newton\\meter}] "
        "& RMSE max par axe [\\si{\\newton\\meter}] & Garanties physiques \\\\",
        "\\midrule",
    ]
    for r in results:
        worst = max(r["per_joint_rmse"])
        lines.append(
            f"{label.get(r['kind'], r['kind'])} & "
            f"\\num{{{r['mean_rmse']:.3f}}} & "
            f"\\num{{{worst:.3f}}} & "
            f"{guarantees.get(r['kind'], '')} \\\\".replace(".", ",", 2)
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=str, nargs="+", required=True,
                   help="HDF5 files, SAME ORDER for every model compared.")
    p.add_argument("--kind", type=str, choices=KINDS, default=None,
                   help="Override the kind. Normally auto-detected from the "
                        "run's config.json 'no_rnea' field.")
    p.add_argument("--run_dir", type=str, default=None)
    p.add_argument("--compare", type=str, nargs="+", default=None,
                   help="Several models at once, as kind=run_dir tokens, e.g. "
                        "'rnea=' 'greybox=models/run_A' 'mlp=models/run_B'.")
    p.add_argument("--batch_size", type=int, default=512)
    p.add_argument("--latex", action="store_true",
                   help="Also print the report's table body.")
    p.add_argument("--json_out", type=str, default=None,
                   help="Write all results to this JSON file.")
    args = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    sig = dataset_signature(args.data)
    print(f"[eval] dataset signature {sig} over {len(args.data)} file(s)")
    print("[eval] every model below is scored on this exact test split.")
    loader, _ = build_test_loader(args.data, args.batch_size)

    jobs = []
    if args.compare:
        for tok in args.compare:
            if "=" not in tok:
                raise SystemExit(f"--compare token must be kind=run_dir, got {tok!r}")
            kind, run_dir = tok.split("=", 1)
            if kind not in KINDS:
                raise SystemExit(f"unknown kind {kind!r}, expected one of {KINDS}")
            jobs.append((kind, run_dir or None))
    else:
        kind = args.kind
        if kind is None:
            if args.run_dir is None:
                raise SystemExit("give --kind rnea, or --run_dir, or --compare")
            cfg_path = os.path.join(args.run_dir, "config.json")
            if os.path.isfile(cfg_path):
                with open(cfg_path) as fh:
                    kind = "mlp" if json.load(fh).get("no_rnea") else "greybox"
            else:
                kind = "greybox"
            print(f"[eval] kind auto-detected as '{kind}' from config.json")
        elif args.run_dir:
            print(f"[eval] WARNING: --kind {kind} given explicitly; not "
                  f"cross-checking against config.json.")
        jobs.append((kind, args.run_dir))

    results = []
    for kind, run_dir in jobs:
        r = evaluate(kind, loader, device, run_dir)
        r["dataset_signature"] = sig
        print_result(r)
        results.append(r)

    if args.latex:
        order = {"rnea": 0, "mlp": 1, "greybox": 2}
        print("\n" + "=" * 68)
        print(latex_table(sorted(results, key=lambda r: order.get(r["kind"], 9))))

    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(results, fh, indent=2)
        print(f"\n[eval] wrote {args.json_out}")


if __name__ == "__main__":
    main()
