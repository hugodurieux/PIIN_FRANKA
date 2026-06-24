"""
Dataset for stage 1.

Reads HDF5 files produced by the data-pipeline agent (Fourier excitation + RNEA).
Each file holds: q, qdot, qddot, tau_real, tau_theo, tau_res, delta.

A synthetic generator is included so the training pipeline can be smoke-tested
end-to-end BEFORE any real data exists.
"""

from __future__ import annotations

import numpy as np
import torch
from torch.utils.data import Dataset

from network.constants import N_JOINTS

try:
    import h5py

    _HAS_H5PY = True
except ImportError:
    _HAS_H5PY = False


class FrankaDynamicsDataset(Dataset):
    """Loads (q, qdot, delta) -> tau_res, with tau_theo and tau_real kept for loss."""

    def __init__(self, h5_path: str):
        if not _HAS_H5PY:
            raise ImportError("h5py required. Install with: pip install h5py")
        with h5py.File(h5_path, "r") as f:
            self.q = torch.tensor(f["q"][:], dtype=torch.float32)
            self.qdot = torch.tensor(f["qdot"][:], dtype=torch.float32)
            self.tau_real = torch.tensor(f["tau_real"][:], dtype=torch.float32)
            self.tau_theo = torch.tensor(f["tau_theo"][:], dtype=torch.float32)
            delta = f["delta"][:]
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
    """

    def __init__(self, n: int = 4096, seed: int = 0):
        g = torch.Generator().manual_seed(seed)
        self.q = (torch.rand(n, N_JOINTS, generator=g) - 0.5) * 2 * np.pi
        self.qdot = (torch.rand(n, N_JOINTS, generator=g) - 0.5) * 2.0
        self.delta = torch.rand(n, 1, generator=g) * 3.0
        coulomb, viscous = 1.5, 0.8
        tau_res = -coulomb * torch.sign(self.qdot) - viscous * self.qdot
        self.tau_theo = torch.randn(n, N_JOINTS, generator=g) * 20.0
        self.tau_real = self.tau_theo + tau_res

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
    ds = SyntheticDataset(n=64)
    s = ds[0]
    print("SyntheticDataset smoke test OK")
    for k, v in s.items():
        print(f"  {k}: {tuple(v.shape)}")
