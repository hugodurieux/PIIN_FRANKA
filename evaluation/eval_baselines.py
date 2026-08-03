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

import numpy as np
import torch
from torch.utils.data import DataLoader

from network.constants import N_JOINTS, TORQUE_LIMITS, FRICTION_NET_HIDDEN
from network.friction_net import FrictionNet
from training.dataset import MultiPayloadDataset, FrankaDynamicsDataset
from training.splits import make_splits, describe, SPLIT_SEED
from training.segment_splits import (make_segment_splits, segment_ids,
                                     report_group_sizes)

KINDS = ("rnea", "greybox", "mlp")


def dataset_signature(paths) -> str:
    """Short hash of the ordered file list, to catch mismatched comparisons."""
    h = hashlib.sha256("|".join(paths).encode()).hexdigest()[:10]
    return h


def build_test_loader(data_paths, batch_size=512, split_mode="sample",
                      split_seed=SPLIT_SEED):
    """Load the dataset and return ONLY its test split, plus its size.

    ``split_mode`` and ``split_seed`` MUST match what the checkpoints were
    trained under. Evaluating a segment-split checkpoint on the sample-split
    test set scores it on trajectories it was trained on, which is the very
    leak the segment mode exists to remove. :func:`check_split_agreement`
    enforces this against each checkpoint's own config.json.
    """
    if len(data_paths) > 1:
        full = MultiPayloadDataset(data_paths)
    else:
        full = FrankaDynamicsDataset(data_paths[0])

    if split_mode == "segment":
        gids = segment_ids(data_paths)
        print(f"[eval] mode=segment, {np.unique(gids).size} trajectories, "
              f"{len(full):,} samples, seed={split_seed}")
        _, _, test_ds = make_segment_splits(full, data_paths, seed=split_seed)
        print(report_group_sizes(
            gids,
            np.empty(0, dtype=np.int64),
            np.empty(0, dtype=np.int64),
            np.asarray(test_ds.indices),
        ))
    else:
        print(f"[eval] mode=sample, {describe(len(full))}")
        _, _, test_ds = make_splits(full, seed=split_seed)
    loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
    return loader, len(test_ds)


def check_split_agreement(run_dirs, split_mode, split_seed):
    """Fail loudly if a checkpoint was trained under a different partition.

    A silent mismatch here does not crash and does not look wrong -- it just
    reports a model on data it has already seen. That is exactly the class of
    defect this whole line of work exists to remove, so it is a hard error.
    """
    for run_dir in run_dirs:
        cfg_path = os.path.join(run_dir, "config.json")
        if not os.path.exists(cfg_path):
            print(f"[eval] WARNING: {run_dir} has no config.json; cannot "
                  "verify it was trained under the same split.")
            continue
        with open(cfg_path) as f:
            cfg = json.load(f)
        # Runs predating --split_mode have no such key and are sample-wise.
        got_mode = cfg.get("split_mode", "sample")
        got_seed = cfg.get("split_seed", SPLIT_SEED)
        if got_mode != split_mode or got_seed != split_seed:
            raise SystemExit(
                f"SPLIT MISMATCH for {run_dir}:\n"
                f"  trained with  split_mode={got_mode!r} "
                f"split_seed={got_seed}\n"
                f"  evaluating as split_mode={split_mode!r} "
                f"split_seed={split_seed}\n"
                "Its test split would contain data it was trained on. Pass "
                "--split_mode/--split_seed matching the checkpoints, or "
                "retrain them under this partition."
            )


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


LABEL = {"rnea": "RNEA seul (analytique)",
         "mlp": "MLP direct (boîte noire)",
         "greybox": "\\textbf{Gris} \\code{isaac-satfix}"}

# What each model is actually CONSTRAINED to, as implemented -- not as one
# might assume. --no_rnea keeps the torque-limit penalty (a statement about
# actuators, true for any model) and disables only dissipativity (meaningless
# when tau_res is the whole torque). Calling the black box "aucune" would
# understate it and flatter the grey box.
GUARANTEES = {
    "rnea": "aucune (non entraîné)",
    "mlp": "limites de couple seules",
    "greybox": "limites + dissipativité",
}

# Decimal points are left as points on purpose: the report loads siunitx with
# locale=FR and output-decimal-marker={,}, so \num{1.456} already renders as
# "1,456". Substituting commas here would be a second, redundant conversion.


def latex_summary_table(results) -> str:
    """Baseline summary: mean RMSE, worst joint, torque violations, guarantees."""
    lines = [
        "% Généré par: python -m evaluation.eval_baselines --latex",
        f"% Même split de test pour toutes les lignes (seed={SPLIT_SEED}).",
        "\\begin{tabular}{@{}lcccc@{}}",
        "\\toprule",
        "Modèle & RMSE moyenne & RMSE pire axe & Éch. hors limites "
        "& Garanties \\\\",
        " & [\\si{\\newton\\meter}] & [\\si{\\newton\\meter}] & de couple & \\\\",
        "\\midrule",
    ]
    for r in results:
        pct = 100.0 * r["n_samples_over_torque_limit"] / max(r["n_test"], 1)
        lines.append(
            f"{LABEL.get(r['kind'], r['kind'])} & "
            f"\\num{{{r['mean_rmse']:.3f}}} & "
            f"\\num{{{max(r['per_joint_rmse']):.3f}}} & "
            f"{r['n_samples_over_torque_limit']} "
            f"(\\SI{{{pct:.2f}}}{{\\percent}}) & "
            f"{GUARANTEES.get(r['kind'], '')} \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def latex_per_joint_table(results) -> str:
    """Per-joint RMSE for every model. This is the table that shows J7."""
    lines = [
        "% Généré par: python -m evaluation.eval_baselines --latex",
        f"% Même split de test pour toutes les lignes (seed={SPLIT_SEED}).",
        "\\begin{tabular}{@{}lccccccc@{}}",
        "\\toprule",
        "RMSE de test [\\si{\\newton\\meter}] & J1 & J2 & J3 & J4 & J5 & J6 & J7 \\\\",
        "\\midrule",
    ]
    for r in results:
        cells = " & ".join(f"\\num{{{v:.3f}}}" for v in r["per_joint_rmse"])
        lines.append(f"{LABEL.get(r['kind'], r['kind'])} & {cells} \\\\")
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
    p.add_argument("--split_mode", type=str, default="sample",
                   choices=("sample", "segment"),
                   help="MUST match how the checkpoints were trained; this is "
                        "verified against each config.json. 'segment' splits "
                        "by whole trajectory (see training/segment_splits.py).")
    p.add_argument("--split_seed", type=int, default=SPLIT_SEED,
                   help="MUST match training. Also verified.")
    p.add_argument("--latex", action="store_true",
                   help="Also print the report's table body.")
    p.add_argument("--json_out", type=str, default=None,
                   help="Write all results to this JSON file.")
    args = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    sig = dataset_signature(args.data)
    print(f"[eval] dataset signature {sig} over {len(args.data)} file(s)")
    print("[eval] every model below is scored on this exact test split.")

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

    # Verify BEFORE loading data: a mismatch is a hard error, and finding it
    # after a full dataset load wastes the run.
    check_split_agreement(
        [rd for _, rd in jobs if rd], args.split_mode, args.split_seed
    )
    loader, _ = build_test_loader(
        args.data, args.batch_size,
        split_mode=args.split_mode, split_seed=args.split_seed,
    )

    results = []
    for kind, run_dir in jobs:
        r = evaluate(kind, loader, device, run_dir)
        r["dataset_signature"] = sig
        # Recorded so a JSON of results can never be read as the wrong
        # partition, and so the two modes cannot be tabulated together.
        r["split_mode"] = args.split_mode
        r["split_seed"] = args.split_seed
        print_result(r)
        results.append(r)

    if args.latex:
        order = {"rnea": 0, "mlp": 1, "greybox": 2}
        ordered = sorted(results, key=lambda r: order.get(r["kind"], 9))
        print("\n" + "=" * 68)
        print("% ---- TABLE 1: résumé des lignes de base ----")
        print(latex_summary_table(ordered))
        print("\n% ---- TABLE 2: RMSE par axe (montre l'axe 7) ----")
        print(latex_per_joint_table(ordered))

        # Flag any joint where a learned model is WORSE than doing nothing.
        rnea = next((r for r in results if r["kind"] == "rnea"), None)
        if rnea is not None:
            for r in results:
                if r["kind"] == "rnea":
                    continue
                worse = [
                    (j + 1, r["per_joint_rmse"][j], rnea["per_joint_rmse"][j])
                    for j in range(N_JOINTS)
                    if r["per_joint_rmse"][j] > rnea["per_joint_rmse"][j]
                ]
                if worse:
                    print(f"\n!! {r['kind']} ({r['tag']}) is WORSE than RNEA alone on:")
                    for j, got, ref in worse:
                        print(f"     J{j}: {got:.4f} Nm vs RNEA {ref:.4f} Nm "
                              f"({got / max(ref, 1e-9):.1f}x worse)")
                    print("   The learned residual is adding error on joints the "
                          "analytical model already gets right.")

    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(results, fh, indent=2)
        print(f"\n[eval] wrote {args.json_out}")


if __name__ == "__main__":
    main()
