"""
Deterministic train / validation / test splitting -- SINGLE SOURCE OF TRUTH.

WHY THIS FILE EXISTS
--------------------
Before this module, ``training/train.py`` split the data 90/10 into train/val
only.  There was no test set anywhere in the repository.  The consequences were
not cosmetic:

  * the per-joint RMSE reported in ``config.json`` (``per_joint_val_rmse``) was
    measured on the VALIDATION set;
  * the checkpoint itself was SELECTED on that same validation set
    (``if vl < best_val: torch.save(...)``);
  * ``controller/compute_error_bound.py`` then derived the Lyapunov error bound
    ``epsilon_j`` -- and therefore the live controller gains Kp/Kd -- from that
    same validation set (its own docstring says so).

So every headline number was an in-sample number for the model-selection
criterion.  That is selection bias, not a held-out measurement.  Any baseline
compared against those numbers would inherit the same flaw, so the split had to
be fixed BEFORE any baseline was measured.

CONTRACT
--------
``split_indices`` is a pure function of ``(n, seed, fractions)``.  Given the
same dataset length and seed it returns the same three index arrays on any
machine, independent of the PyTorch version -- it uses numpy's ``default_rng``,
whose stream is guaranteed stable, rather than ``torch.utils.data.random_split``
(whose generator stream is not guaranteed across releases).

The three subsets are disjoint and cover the whole dataset.

COMPATIBILITY WARNING
---------------------
This split is NOT the same partition as the old 90/10 ``random_split(seed=0)``.
Numbers produced before this module and numbers produced after it are therefore
NOT comparable, and must not be placed in the same table.  Everything reported
in the school report must be re-measured with this module.  See
``run_experiments.sh``.
"""

from __future__ import annotations

from typing import Sequence, Tuple

import numpy as np
from torch.utils.data import Dataset, Subset

# Fixed for the whole project. Changing it invalidates every recorded number.
SPLIT_SEED = 12345

# train / validation / test.  Matches what the school report claims in its
# "Identification et hygiene des donnees" section.
SPLIT_FRACTIONS: Tuple[float, float, float] = (0.8, 0.1, 0.1)


def split_indices(
    n: int,
    seed: int = SPLIT_SEED,
    fractions: Sequence[float] = SPLIT_FRACTIONS,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return disjoint (train, val, test) index arrays covering ``range(n)``.

    Args:
        n:         Total number of samples.
        seed:      RNG seed. Fixed project-wide; do not vary per experiment.
        fractions: (train, val, test), must sum to 1.0.

    Returns:
        Three sorted int64 arrays. Sorted so that iteration order is
        deterministic and cache-friendly, which does not affect the partition.

    Raises:
        ValueError: if fractions are invalid or n is too small to give every
            split at least one sample.
    """
    if len(fractions) != 3:
        raise ValueError(f"fractions must have 3 entries, got {len(fractions)}")
    if any(f < 0 for f in fractions):
        raise ValueError(f"fractions must be non-negative, got {fractions}")
    if abs(sum(fractions) - 1.0) > 1e-9:
        raise ValueError(f"fractions must sum to 1.0, got {sum(fractions)}")
    if n < 3:
        raise ValueError(f"need at least 3 samples to make 3 splits, got {n}")

    perm = np.random.default_rng(seed).permutation(n)

    # Allocate val and test by rounding, give the remainder to train. This
    # guarantees the three sizes sum to exactly n with no off-by-one.
    n_val = max(1, int(round(fractions[1] * n)))
    n_test = max(1, int(round(fractions[2] * n)))
    if n_val + n_test >= n:
        raise ValueError(
            f"n={n} too small for fractions={fractions}: "
            f"val={n_val} + test={n_test} leaves nothing for train"
        )
    n_train = n - n_val - n_test

    idx_train = np.sort(perm[:n_train])
    idx_val = np.sort(perm[n_train:n_train + n_val])
    idx_test = np.sort(perm[n_train + n_val:])
    return idx_train, idx_val, idx_test


def make_splits(
    dataset: Dataset,
    seed: int = SPLIT_SEED,
    fractions: Sequence[float] = SPLIT_FRACTIONS,
) -> Tuple[Subset, Subset, Subset]:
    """Wrap ``split_indices`` into three ``torch.utils.data.Subset`` views.

    The dataset is not copied; each Subset holds a view plus its index list.
    """
    idx_train, idx_val, idx_test = split_indices(len(dataset), seed, fractions)
    return (
        Subset(dataset, idx_train.tolist()),
        Subset(dataset, idx_val.tolist()),
        Subset(dataset, idx_test.tolist()),
    )


def describe(n: int, seed: int = SPLIT_SEED,
             fractions: Sequence[float] = SPLIT_FRACTIONS) -> str:
    """One-line human-readable summary, for printing at the top of a run."""
    tr, va, te = split_indices(n, seed, fractions)
    return (f"split(seed={seed}): train={len(tr):,} val={len(va):,} "
            f"test={len(te):,} (total {n:,})")


if __name__ == "__main__":
    # Self-checks. Run with: python -m training.splits
    for n in (3, 10, 1000, 148304):
        tr, va, te = split_indices(n)
        assert len(tr) + len(va) + len(te) == n, f"sizes do not sum for n={n}"
        union = np.concatenate([tr, va, te])
        assert len(np.unique(union)) == n, f"splits overlap or miss for n={n}"
        print(describe(n))

    # Determinism: two calls must agree exactly.
    a = split_indices(9999)
    b = split_indices(9999)
    assert all(np.array_equal(x, y) for x, y in zip(a, b)), "not deterministic"
    print("determinism OK")

    # Different seeds must give different partitions.
    c = split_indices(9999, seed=SPLIT_SEED + 1)
    assert not np.array_equal(a[2], c[2]), "seed has no effect"
    print("seed sensitivity OK")
    print("\ntraining/splits.py self-check passed")
