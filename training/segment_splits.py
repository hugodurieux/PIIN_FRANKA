"""
Group-wise (per-trajectory) train / validation / test splitting.

WHY THIS FILE EXISTS
--------------------
``training/splits.py`` fixed a real defect: the checkpoint used to be selected
on the same set whose RMSE was reported, and ``epsilon_j`` -- hence the live
controller gains -- was derived from it too.  That fix stands and is not
undone here.

It did NOT fix a second, independent defect.  ``split_indices`` draws a uniform
permutation over INDIVIDUAL SAMPLES, but the data is not i.i.d. samples.  It is
30 continuous trajectories (``generate_isaac_dataset.py``: ``N_SEGMENTS = 10``
Fourier segments per payload, 3 payloads) sampled at 1 kHz
(``SIM_DT = 1/1000``).  Two consecutive rows are 1 ms of motion apart, so a
sample-wise split puts near-duplicates of every test point into the training
set.  That is temporal leakage, and the "held-out" test set is not held out in
the sense the school report claims.

WHY IT MATTERS DIFFERENTLY FOR DIFFERENT MODELS
-----------------------------------------------
The leakage is not a uniform inflation that cancels out of a comparison:

  * the RNEA baseline fits nothing, so a 1 ms neighbour is worth nothing to it;
  * the grey box only has to learn a residual, inertia and gravity being
    supplied analytically;
  * the black box (``--no_rnea``) has to reconstruct the whole map from data,
    so it benefits most from having memorised a neighbouring sample.

Corroborating evidence that this is actually happening: ``training/dataset.py``
never loads ``qddot`` into the batch, so the black box's input is (q, qdot,
delta) and it is structurally incapable of representing the inertial torque
M(q) qddot -- yet it beat the grey box by 28 % on the sample-wise split.  With
only 30 trajectories, (q, qdot) very nearly identifies which trajectory and
which phase you are on, which makes qddot recoverable by memorisation.  A
group-wise split removes exactly that shortcut.

WHAT THIS MODULE DOES
---------------------
Splits by TRAJECTORY SEGMENT, so no test trajectory is ever seen in training.

Segment boundaries were not written into the HDF5 files, but they are exactly
recoverable.  Each file stores ``attrs["n_segments"]`` (= 10), and each segment
restarts from an independent Sobol centre, so the largest ``n_segments - 1``
jumps in ||q[i+1] - q[i]|| inside a file are its internal boundaries.  Taking a
KNOWN COUNT of largest jumps is deliberate: a bare magnitude threshold would
also fire on the gaps left mid-segment by the saturation filter
(``SATURATION_MARGIN``), which removes runs of timesteps and so creates real
but smaller discontinuities.

The split is stratified BY FILE: each payload contributes the same proportion
of segments to train/val/test.  Without this, an unlucky seed can put all test
segments in one payload and the comparison then measures payload transfer
rather than trajectory generalisation.

STATISTICAL HEALTH WARNING
--------------------------
80/10/10 over 30 groups leaves only 3 test trajectories.  That is a far smaller
effective sample than 14,830 correlated rows suggests, and a single seed is not
a result.  Run at least 3 seeds (``--split_seed``) and report mean and spread.
``report_group_sizes`` prints what each split actually contains so this is
visible rather than assumed.

NOT A DROP-IN REPLACEMENT
-------------------------
This partition is NOT the same as ``training/splits.py``'s, and numbers from
the two are NOT comparable and must not share a table.  Both are kept so the
already-recorded sample-wise numbers stay reproducible and the comparison
between the two split modes is itself measurable.

Self-check (reads the real HDF5 files, trains nothing)::

    python -m training.segment_splits --data data/isaac_0.0kg.h5 \\
        data/isaac_1.0kg.h5 data/isaac_3.0kg.h5
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

import numpy as np
from torch.utils.data import Dataset, Subset

# Same project-wide default as training/splits.py, so that "seed 12345" means
# the same intent in both modes even though the partitions differ.
SPLIT_SEED = 12345
SPLIT_FRACTIONS: Tuple[float, float, float] = (0.8, 0.1, 0.1)

try:  # h5py is optional at import time; only needed to read segment structure
    import h5py

    _HAS_H5PY = True
except ImportError:  # pragma: no cover
    _HAS_H5PY = False


# ---------------------------------------------------------------------------
# Segment recovery
# ---------------------------------------------------------------------------
def segment_starts_in_file(q: np.ndarray, n_segments: int) -> np.ndarray:
    """Indices at which a new trajectory segment begins, within one file.

    Args:
        q:          (n, 7) joint positions, in the file's stored row order.
        n_segments: How many segments the file holds. Read from the file's own
            ``attrs["n_segments"]`` by :func:`segment_ids`; passing it in
            explicitly is what makes this robust to the saturation filter's
            mid-segment gaps (see module docstring).

    Returns:
        Sorted int64 array of length ``n_segments``, always starting with 0.

    Raises:
        ValueError: if ``n_segments`` is not achievable for this array.
    """
    q = np.asarray(q)
    if q.ndim != 2:
        raise ValueError(f"q must be 2-D (n, dof), got shape {q.shape}")
    n = q.shape[0]
    if n_segments < 1:
        raise ValueError(f"n_segments must be >= 1, got {n_segments}")
    if n_segments > n:
        raise ValueError(
            f"n_segments={n_segments} exceeds the {n} rows in this file"
        )
    if n_segments == 1:
        return np.zeros(1, dtype=np.int64)

    # Per-step motion. A boundary is a jump to an independent Sobol centre and
    # is far larger than 1 ms of continuous motion; the saturation filter's
    # gaps sit in between, which is why we take a known COUNT and not a
    # threshold.
    step = np.linalg.norm(np.diff(q, axis=0), axis=1)  # (n-1,)

    # argpartition: the (n_segments - 1) largest jumps, order irrelevant.
    k = n_segments - 1
    cut_after = np.argpartition(step, -k)[-k:]
    starts = np.concatenate([[0], np.sort(cut_after) + 1]).astype(np.int64)

    # Separation check: the smallest accepted jump should stand clear of the
    # largest rejected one. If it does not, the file's structure is not what
    # attrs claims and silently splitting on it would be worse than failing.
    accepted_min = step[cut_after].min()
    mask = np.ones(step.shape[0], dtype=bool)
    mask[cut_after] = False
    rejected_max = step[mask].max() if mask.any() else 0.0
    if accepted_min <= rejected_max:
        raise ValueError(
            "Segment boundaries are not separable: the smallest boundary jump "
            f"({accepted_min:.4g}) does not exceed the largest within-segment "
            f"step ({rejected_max:.4g}). Expected {n_segments} segments. The "
            "file's structure does not match its n_segments attribute."
        )
    return starts


def segment_ids(
    h5_paths: Sequence[str],
    n_segments_per_file: Optional[Sequence[int]] = None,
) -> np.ndarray:
    """Per-sample trajectory id over files concatenated in the given order.

    The order must be the SAME list, in the SAME order, that was handed to
    ``MultiPayloadDataset``: that class concatenates files in argument order,
    so ids computed here line up with dataset row indices.

    Args:
        h5_paths: Dataset files, in the dataset's own concatenation order.
        n_segments_per_file: Override the per-file segment count. Defaults to
            each file's ``attrs["n_segments"]``.

    Returns:
        (n_total,) int64 array. Ids are globally unique across files, so
        segment 0 of file 1 does not collide with segment 0 of file 0.

    Raises:
        ImportError: if h5py is unavailable.
        ValueError: on unreadable structure.
    """
    if not _HAS_H5PY:
        raise ImportError("h5py required. Install with: pip install h5py")
    if not h5_paths:
        raise ValueError("h5_paths must contain at least one file path.")

    all_ids: List[np.ndarray] = []
    next_id = 0
    for f_i, path in enumerate(h5_paths):
        with h5py.File(path, "r") as f:
            q = f["q"][:]
            if n_segments_per_file is not None:
                n_seg = int(n_segments_per_file[f_i])
            elif "n_segments" in f.attrs:
                n_seg = int(f.attrs["n_segments"])
            else:
                raise ValueError(
                    f"{path} has no 'n_segments' attribute; pass "
                    "n_segments_per_file explicitly"
                )

        starts = segment_starts_in_file(q, n_seg)
        ids = np.zeros(q.shape[0], dtype=np.int64)
        for local_i, s in enumerate(starts):
            ids[s:] = next_id + local_i
        all_ids.append(ids)
        next_id += n_seg

    return np.concatenate(all_ids, axis=0)


# ---------------------------------------------------------------------------
# Group-wise partition
# ---------------------------------------------------------------------------
def group_split_indices(
    group_ids: np.ndarray,
    seed: int = SPLIT_SEED,
    fractions: Sequence[float] = SPLIT_FRACTIONS,
    strata: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Partition SAMPLES by whole group, optionally stratified.

    Args:
        group_ids: (n,) group id per sample, e.g. from :func:`segment_ids`.
        seed:      RNG seed for the group permutation.
        fractions: (train, val, test) over GROUPS, not samples. The resulting
            sample counts will not match these fractions exactly, because
            segments differ in length after saturation filtering.
        strata:    (n,) optional stratum per sample (here: the source file, so
            each payload is represented in every split). Constant within a
            group; the group's first sample decides.

    Returns:
        Three sorted int64 arrays of SAMPLE indices, disjoint, covering all n.

    Raises:
        ValueError: on invalid fractions, or too few groups to fill 3 splits.
    """
    group_ids = np.asarray(group_ids)
    if group_ids.ndim != 1:
        raise ValueError(f"group_ids must be 1-D, got shape {group_ids.shape}")
    if len(fractions) != 3:
        raise ValueError(f"fractions must have 3 entries, got {len(fractions)}")
    if any(f < 0 for f in fractions):
        raise ValueError(f"fractions must be non-negative, got {fractions}")
    if abs(sum(fractions) - 1.0) > 1e-9:
        raise ValueError(f"fractions must sum to 1.0, got {sum(fractions)}")

    uniq = np.unique(group_ids)
    if uniq.size < 3:
        raise ValueError(
            f"need at least 3 groups to make 3 splits, got {uniq.size}. "
            "A group-wise split is not meaningful on this dataset."
        )

    if strata is None:
        strata_of_group = np.zeros(uniq.size, dtype=np.int64)
    else:
        strata = np.asarray(strata)
        if strata.shape != group_ids.shape:
            raise ValueError("strata must have the same shape as group_ids")
        first = {g: np.flatnonzero(group_ids == g)[0] for g in uniq}
        strata_of_group = np.array([strata[first[g]] for g in uniq])

    rng = np.random.default_rng(seed)
    train_g: List[int] = []
    val_g: List[int] = []
    test_g: List[int] = []

    for s in np.unique(strata_of_group):
        gs = uniq[strata_of_group == s]
        gs = rng.permutation(gs)
        m = gs.size
        # At least one group to val and test whenever the stratum can spare it,
        # so no split silently loses a payload.
        n_val = max(1, int(round(fractions[1] * m))) if m >= 3 else 0
        n_test = max(1, int(round(fractions[2] * m))) if m >= 3 else 0
        if n_val + n_test >= m:
            n_val = min(n_val, max(0, m - 2))
            n_test = min(n_test, max(0, m - 1 - n_val))
        val_g.extend(gs[:n_val].tolist())
        test_g.extend(gs[n_val:n_val + n_test].tolist())
        train_g.extend(gs[n_val + n_test:].tolist())

    for name, gl in (("train", train_g), ("val", val_g), ("test", test_g)):
        if not gl:
            raise ValueError(
                f"the {name} split received no groups; too few groups "
                f"({uniq.size}) for fractions={fractions}"
            )

    def samples_of(groups: List[int]) -> np.ndarray:
        if not groups:
            return np.empty(0, dtype=np.int64)
        return np.sort(
            np.flatnonzero(np.isin(group_ids, np.asarray(groups)))
        ).astype(np.int64)

    return samples_of(train_g), samples_of(val_g), samples_of(test_g)


def make_segment_splits(
    dataset: Dataset,
    h5_paths: Sequence[str],
    seed: int = SPLIT_SEED,
    fractions: Sequence[float] = SPLIT_FRACTIONS,
    stratify_by_file: bool = True,
) -> Tuple[Subset, Subset, Subset]:
    """Wrap :func:`group_split_indices` into three ``Subset`` views.

    Args:
        dataset:   The dataset built from ``h5_paths`` IN THAT ORDER and with
            no subsampling, so row indices correspond.
        h5_paths:  Same list, same order, as used to build ``dataset``.
        seed:      RNG seed.
        fractions: (train, val, test) over groups.
        stratify_by_file: Keep every payload present in every split.

    Returns:
        (train, val, test) Subsets.

    Raises:
        ValueError: if the recovered ids do not cover the dataset exactly --
            which is what a mismatched file list looks like.
    """
    gids = segment_ids(h5_paths)
    if len(gids) != len(dataset):  # type: ignore[arg-type]
        raise ValueError(
            f"segment ids cover {len(gids)} samples but the dataset holds "
            f"{len(dataset)}. "  # type: ignore[arg-type]
            "h5_paths must be the same files, in the same order, used to "
            "build the dataset, and the dataset must not be subsampled."
        )

    strata = None
    if stratify_by_file:
        if not _HAS_H5PY:
            raise ImportError("h5py required. Install with: pip install h5py")
        counts = []
        for path in h5_paths:
            with h5py.File(path, "r") as f:
                counts.append(f["q"].shape[0])
        strata = np.concatenate(
            [np.full(c, i, dtype=np.int64) for i, c in enumerate(counts)]
        )

    idx_train, idx_val, idx_test = group_split_indices(
        gids, seed=seed, fractions=fractions, strata=strata
    )
    return (
        Subset(dataset, idx_train.tolist()),
        Subset(dataset, idx_val.tolist()),
        Subset(dataset, idx_test.tolist()),
    )


def report_group_sizes(
    group_ids: np.ndarray,
    idx_train: np.ndarray,
    idx_val: np.ndarray,
    idx_test: np.ndarray,
) -> str:
    """Human-readable summary: groups and samples per split, and disjointness.

    Prints groups, not just samples, because the group count is the real
    effective sample size of a group-wise split.
    """
    lines = []
    for name, idx in (("train", idx_train), ("val", idx_val), ("test", idx_test)):
        g = np.unique(group_ids[idx]) if idx.size else np.empty(0, dtype=np.int64)
        lines.append(
            f"  {name:<5} {idx.size:>8,} samples   {g.size:>3} segments   "
            f"ids={sorted(g.tolist())}"
        )
    tr = set(np.unique(group_ids[idx_train]).tolist()) if idx_train.size else set()
    va = set(np.unique(group_ids[idx_val]).tolist()) if idx_val.size else set()
    te = set(np.unique(group_ids[idx_test]).tolist()) if idx_test.size else set()
    overlap = (tr & va) | (tr & te) | (va & te)
    lines.append(
        "  segment overlap between splits: "
        + ("NONE (correct)" if not overlap else f"{sorted(overlap)} <-- BUG")
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Self-check
# ---------------------------------------------------------------------------
def _main() -> int:
    import argparse

    p = argparse.ArgumentParser(
        description="Recover trajectory segments and show the group-wise split."
    )
    p.add_argument("--data", type=str, nargs="+", required=True,
                   help="HDF5 files, in the same order the dataset uses.")
    p.add_argument("--split_seed", type=int, default=SPLIT_SEED)
    p.add_argument("--no_stratify", action="store_true",
                   help="Disable per-file stratification (not recommended).")
    args = p.parse_args()

    print("Recovering segment boundaries from |q[i+1] - q[i]| ...")
    gids = segment_ids(args.data)
    uniq, counts = np.unique(gids, return_counts=True)
    print(f"  {len(args.data)} files -> {uniq.size} segments, "
          f"{gids.size:,} samples total")
    print(f"  segment lengths: min={counts.min():,} max={counts.max():,} "
          f"mean={counts.mean():,.0f}")
    print("  (unequal lengths are expected: the saturation filter removes "
          "near-limit timesteps)")

    strata = None
    if not args.no_stratify:
        strata_parts = []
        for i, path in enumerate(args.data):
            with h5py.File(path, "r") as f:
                strata_parts.append(np.full(f["q"].shape[0], i, dtype=np.int64))
        strata = np.concatenate(strata_parts)

    tr, va, te = group_split_indices(
        gids, seed=args.split_seed, strata=strata
    )
    print(f"\nGroup-wise split (seed={args.split_seed}, "
          f"stratified={'no' if args.no_stratify else 'by file'}):")
    print(report_group_sizes(gids, tr, va, te))

    total = tr.size + va.size + te.size
    assert total == gids.size, f"splits cover {total} of {gids.size} samples"
    print(f"\nOK: 3 splits, disjoint by segment, covering all "
          f"{gids.size:,} samples.")
    print("\nNOTE: only a handful of test TRAJECTORIES, however many samples "
          "they contain.\n      Run >= 3 seeds and report mean and spread.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
