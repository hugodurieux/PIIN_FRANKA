"""
Dataset for stage 1.

Reads HDF5 files produced by the data-pipeline agent (Fourier excitation + RNEA).
Each file holds: q, qdot, qddot, tau_real, tau_theo, tau_res, delta.

A synthetic generator is included so the training pipeline can be smoke-tested
end-to-end BEFORE any real data exists.

Multi-payload training: use ``MultiPayloadDataset`` to concatenate several HDF5
files (e.g. 0 kg, 1 kg, 3 kg) into a single dataset before splitting into
train/val. Subsampling (novelty N4) is applied on the combined pool so the
ablation budget is shared proportionally across payloads.

Novelty N4-Liu (goal.md Objective 1 -- Automated URDF-to-Model Pipeline,
data-efficiency sub-claim):

  Reference:
    Liu, Borja, Della Santina (2024). "Physics-Informed Neural Networks to Model
    and Control Robots: A Theoretical and Experimental Investigation."
    Advanced Intelligent Systems (Wiley), vol. 6, no. 5.
    Borrowed: the 25 000-sample training benchmark reported for the Franka Panda
    (Section IV-B, Table I). The ``max_samples`` flag enables ablation studies
    that quantify how few samples our URDF-seeded grey-box approach needs versus
    Liu et al.'s 25 000-sample black-box baseline, directly proving Goal 1's
    data-efficiency claim. Subsampling uses seed=42 for reproducibility.
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np
import torch
from torch.utils.data import Dataset

from network.constants import N_JOINTS

try:
    import h5py

    _HAS_H5PY = True
except ImportError:
    _HAS_H5PY = False


# ---------------------------------------------------------------------------
# Utility: reproducible random subsampling
# ---------------------------------------------------------------------------

_SUBSAMPLE_SEED = 42  # fixed for reproducibility across experiments


def _random_subsample_indices(n_total: int, max_samples: int) -> np.ndarray:
    """Return ``max_samples`` unique indices drawn from [0, n_total) with a
    fixed random seed so that every run selects the same subset.

    Args:
        n_total:     Total number of samples available.
        max_samples: Desired subset size (clamped to n_total if larger).

    Returns:
        Sorted 1-D int64 numpy array of selected indices.
    """
    if max_samples >= n_total:
        return np.arange(n_total)
    rng = np.random.default_rng(seed=_SUBSAMPLE_SEED)
    idx = rng.choice(n_total, size=max_samples, replace=False)
    idx.sort()  # keep original order for deterministic iteration
    return idx


class FrankaDynamicsDataset(Dataset):
    """Loads (q, qdot, delta) -> tau_res, with tau_theo and tau_real kept for loss.

    Args:
        h5_path:     Path to the HDF5 dataset file.
        max_samples: If not None, randomly subsample the dataset to at most
                     this many entries (reproducible, seed=42).  Enables
                     data-efficiency ablation (novelty N4).
    """

    def __init__(self, h5_path: str, max_samples: Optional[int] = None):
        if not _HAS_H5PY:
            raise ImportError("h5py required. Install with: pip install h5py")
        with h5py.File(h5_path, "r") as f:
            q = f["q"][:]
            qdot = f["qdot"][:]
            tau_real = f["tau_real"][:]
            tau_theo = f["tau_theo"][:]
            delta = f["delta"][:]

        # --- Subsample if requested (novelty N4) ---
        n_total = q.shape[0]
        if max_samples is not None and max_samples > 0:
            idx = _random_subsample_indices(n_total, max_samples)
            q = q[idx]
            qdot = qdot[idx]
            tau_real = tau_real[idx]
            tau_theo = tau_theo[idx]
            delta = delta[idx]

        self.q = torch.tensor(q, dtype=torch.float32)
        self.qdot = torch.tensor(qdot, dtype=torch.float32)
        self.tau_real = torch.tensor(tau_real, dtype=torch.float32)
        self.tau_theo = torch.tensor(tau_theo, dtype=torch.float32)
        self.delta = torch.tensor(delta, dtype=torch.float32).reshape(-1, 1)

    def __len__(self) -> int:
        return self.q.shape[0]

    def __getitem__(self, i: int) -> dict:
        return {
            "q": self.q[i],
            "qdot": self.qdot[i],
            "delta": self.delta[i],
            "tau_real": self.tau_real[i],
            "tau_theo": self.tau_theo[i],
        }


class MultiPayloadDataset(Dataset):
    """Concatenates multiple HDF5 payload files into a single dataset.

    Each file typically corresponds to one payload condition (0 kg, 1 kg, 3 kg).
    All files are loaded individually, their tensors are concatenated along the
    sample axis, and then ``max_samples`` subsampling (novelty N4) is applied on
    the combined pool — so the ablation budget is shared across all payloads.

    Args:
        h5_paths:    List of paths to HDF5 dataset files.
        max_samples: If not None, randomly subsample the combined dataset to at
                     most this many entries (reproducible, seed=42).
    """

    def __init__(self, h5_paths: List[str], max_samples: Optional[int] = None):
        if not _HAS_H5PY:
            raise ImportError("h5py required. Install with: pip install h5py")
        if not h5_paths:
            raise ValueError("h5_paths must contain at least one file path.")

        qs, qdots, tau_reals, tau_theos, deltas = [], [], [], [], []

        for path in h5_paths:
            with h5py.File(path, "r") as f:
                qs.append(f["q"][:])
                qdots.append(f["qdot"][:])
                tau_reals.append(f["tau_real"][:])
                tau_theos.append(f["tau_theo"][:])
                deltas.append(f["delta"][:])
            n = qs[-1].shape[0]
            print(f"[MultiPayload] Loaded {n:>7,} samples from {path}")

        q = np.concatenate(qs, axis=0)
        qdot = np.concatenate(qdots, axis=0)
        tau_real = np.concatenate(tau_reals, axis=0)
        tau_theo = np.concatenate(tau_theos, axis=0)
        delta = np.concatenate(deltas, axis=0)

        print(f"[MultiPayload] Combined: {q.shape[0]:,} samples from {len(h5_paths)} files")

        # --- Subsample on the combined pool (novelty N4) ---
        n_total = q.shape[0]
        if max_samples is not None and max_samples > 0:
            idx = _random_subsample_indices(n_total, max_samples)
            q = q[idx]
            qdot = qdot[idx]
            tau_real = tau_real[idx]
            tau_theo = tau_theo[idx]
            delta = delta[idx]
            print(f"[MultiPayload] Subsampled to {q.shape[0]:,} samples (max_samples={max_samples})")

        self.q = torch.tensor(q, dtype=torch.float32)
        self.qdot = torch.tensor(qdot, dtype=torch.float32)
        self.tau_real = torch.tensor(tau_real, dtype=torch.float32)
        self.tau_theo = torch.tensor(tau_theo, dtype=torch.float32)
        self.delta = torch.tensor(delta, dtype=torch.float32).reshape(-1, 1)

    def __len__(self) -> int:
        return self.q.shape[0]

    def __getitem__(self, i: int) -> dict:
        return {
            "q": self.q[i],
            "qdot": self.qdot[i],
            "delta": self.delta[i],
            "tau_real": self.tau_real[i],
            "tau_theo": self.tau_theo[i],
        }


class SyntheticDataset(Dataset):
    """
    Fake data for smoke-testing the pipeline without pinocchio or real recordings.
    tau_res is set to a plausible velocity-dependent friction so the network has
    something dissipative to learn: tau_res = -c * sign(qdot) - b * qdot.

    Args:
        n:           Number of synthetic samples to generate.
        seed:        RNG seed for data generation.
        max_samples: If not None, randomly subsample the generated data to at
                     most this many entries (reproducible, seed=42).  Enables
                     data-efficiency ablation (novelty N4).
    """

    def __init__(self, n: int = 4096, seed: int = 0,
                 max_samples: Optional[int] = None):
        g = torch.Generator().manual_seed(seed)
        q = (torch.rand(n, N_JOINTS, generator=g) - 0.5) * 2 * np.pi
        qdot = (torch.rand(n, N_JOINTS, generator=g) - 0.5) * 2.0
        delta = torch.rand(n, 1, generator=g) * 3.0
        coulomb, viscous = 1.5, 0.8
        tau_res = -coulomb * torch.sign(qdot) - viscous * qdot
        tau_theo = torch.randn(n, N_JOINTS, generator=g) * 20.0
        tau_real = tau_theo + tau_res

        # --- Subsample if requested (novelty N4) ---
        if max_samples is not None and max_samples > 0 and max_samples < n:
            idx = _random_subsample_indices(n, max_samples)
            idx_t = torch.from_numpy(idx).long()
            q = q[idx_t]
            qdot = qdot[idx_t]
            delta = delta[idx_t]
            tau_theo = tau_theo[idx_t]
            tau_real = tau_real[idx_t]

        self.q = q
        self.qdot = qdot
        self.delta = delta
        self.tau_theo = tau_theo
        self.tau_real = tau_real

    def __len__(self) -> int:
        return self.q.shape[0]

    def __getitem__(self, i: int) -> dict:
        return {
            "q": self.q[i],
            "qdot": self.qdot[i],
            "delta": self.delta[i],
            "tau_real": self.tau_real[i],
            "tau_theo": self.tau_theo[i],
        }


if __name__ == "__main__":
    # Smoke test 1: full synthetic dataset
    ds = SyntheticDataset(n=64)
    s = ds[0]
    print("SyntheticDataset smoke test OK")
    for k, v in s.items():
        print(f"  {k}: {tuple(v.shape)}")

    # Smoke test 2: truncated synthetic dataset (novelty N4)
    ds_trunc = SyntheticDataset(n=64, max_samples=20)
    assert len(ds_trunc) == 20, f"Expected 20, got {len(ds_trunc)}"
    print(f"\nSyntheticDataset(n=64, max_samples=20) -> len={len(ds_trunc)} OK")

    # Smoke test 3: max_samples larger than dataset -- should keep all
    ds_big = SyntheticDataset(n=64, max_samples=200)
    assert len(ds_big) == 64, f"Expected 64, got {len(ds_big)}"
    print(f"SyntheticDataset(n=64, max_samples=200) -> len={len(ds_big)} OK (clamped)")

    # Smoke test 4: reproducibility -- two calls with same max_samples
    ds_a = SyntheticDataset(n=64, max_samples=20)
    ds_b = SyntheticDataset(n=64, max_samples=20)
    assert torch.equal(ds_a.q, ds_b.q), "Reproducibility check failed!"
    print("Reproducibility check passed (same subsample both times)")
