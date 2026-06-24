"""
RNEA wrapper — the WHITE-BOX baseline.

Computes tau_theoretical = RNEA(q, qdot, qddot) using Pinocchio, from the URDF.
This is the analytical rigid-body inverse dynamics. It is NEVER learned and NEVER
modified — the network only learns the residual on top of it.

Grounding in Liu et al. (2024):
  - Liu avoids acceleration measurements entirely (they integrate with RK4) because
    qddot is hard to obtain on hardware. Our grey-box NEEDS qddot to evaluate RNEA,
    but ONLY OFFLINE during dataset preparation. At 1 kHz control time we use
    qddot_desired (clean by construction), never measured qddot.

The payload mass delta is injected here by updating the end-effector inertia BEFORE
calling RNEA, so the known part of the load is handled analytically and only the
unmodeled part is left to the residual network.
"""

from __future__ import annotations

import numpy as np

try:
    import pinocchio as pin

    _HAS_PINOCCHIO = True
except ImportError:  # keep the file importable without pinocchio installed
    _HAS_PINOCCHIO = False


class RneaBaseline:
    """Thin wrapper around pinocchio.rnea for batched dataset preparation."""

    def __init__(self, urdf_path: str, ee_frame: str = "panda_hand"):
        if not _HAS_PINOCCHIO:
            raise ImportError(
                "pinocchio is required. Install with: pip install pin"
            )
        self.model = pin.buildModelFromUrdf(urdf_path)
        self.data = self.model.createData()
        self.ee_frame = ee_frame
        self._base_ee_mass = None  # cache for payload injection

    def compute_tau_theoretical(
        self,
        q: np.ndarray,
        qdot: np.ndarray,
        qddot: np.ndarray,
        delta: float = 0.0,
    ) -> np.ndarray:
        """
        Batched RNEA. pinocchio.rnea works one sample at a time, so we loop.
        This runs OFFLINE during dataset prep, never in the control loop.

        Args:
            q, qdot, qddot: (N, 7) arrays
            delta: payload mass [kg] added to the end-effector before RNEA
        Returns:
            tau_theo: (N, 7) array
        """
        if delta:
            self._inject_payload(delta)

        N = q.shape[0]
        tau = np.zeros((N, self.model.nq))
        for i in range(N):
            tau[i] = pin.rnea(self.model, self.data, q[i], qdot[i], qddot[i])

        if delta:
            self._restore_payload()
        return tau

    def _inject_payload(self, delta: float) -> None:
        """Add delta [kg] to the end-effector link inertia."""
        fid = self.model.getFrameId(self.ee_frame)
        jid = self.model.frames[fid].parent
        self._base_ee_mass = self.model.inertias[jid].mass
        self.model.inertias[jid].mass = self._base_ee_mass + delta

    def _restore_payload(self) -> None:
        """Restore the original end-effector mass."""
        if self._base_ee_mass is None:
            return
        fid = self.model.getFrameId(self.ee_frame)
        jid = self.model.frames[fid].parent
        self.model.inertias[jid].mass = self._base_ee_mass
        self._base_ee_mass = None


if __name__ == "__main__":
    if not _HAS_PINOCCHIO:
        print("pinocchio not installed here — wrapper imports fine, "
              "run this on your machine after `pip install pin`.")
    else:
        print("pinocchio available — provide a URDF path to test RneaBaseline.")
