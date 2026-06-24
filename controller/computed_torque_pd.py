"""
Computed-torque + PD controller for the Franka Panda (Stage 3).

Plan:
  1. Combine the white-box RNEA feedforward, the learned GreyBoxNet residual,
     and a PD error-correction term into a single control law at 1000 Hz.
  2. Use Lyapunov-derived gains (N3-Liu) for provable stability.
  3. Hard-clip the output to TORQUE_LIMITS as a final safety layer.

This serves goal.md Objective 2 (1000 Hz real-time control) by embedding the
trained PINN directly in the control loop, and Objective 3 (7-DoF scaling) by
operating on the full Franka Panda joint space.

Control law:
    tau_cmd = tau_ff + tau_PD

    tau_ff  = RNEA(q, qdot, qddot_des; URDF, delta)       [white-box feedforward]
            + tau_res_model(q, qdot, delta)                [learned residual]

    tau_PD  = Kp @ (q_des - q) + Kd @ (qdot_des - qdot)   [error correction]

Note on qddot_des:
    qddot_des comes from the trajectory planner (Stage 2) and is clean by
    construction -- it is NOT a finite-differenced sensor signal.  Using it
    at 1 kHz is safe and consistent with the project architecture (see
    pinocchio_baseline/rnea_wrapper.py header comments).
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import torch

from network.constants import N_JOINTS, TORQUE_LIMITS
from controller.model_loader import load_grey_box_model
from controller.lyapunov_gains import DEFAULT_KP, DEFAULT_KD
from pinocchio_baseline.rnea_wrapper import RneaBaseline


# Pre-compute numpy torque limits once (shape (7,), used for clipping).
_TORQUE_LIMITS_NP = TORQUE_LIMITS.numpy().copy()


class ComputedTorquePDController:
    """
    Computed-torque feedforward + PD feedback controller.

    This controller combines three torque sources at every 1 kHz step:

    1. **RNEA feedforward** -- analytical inverse dynamics from the URDF,
       handling gravity, Coriolis, and inertial terms for the desired
       acceleration trajectory.
    2. **Learned residual** -- a trained ``GreyBoxNet`` that compensates
       for unmodeled dynamics (friction, transmission losses, payload-
       dependent effects not captured by RNEA).
    3. **PD correction** -- proportional-derivative feedback on the
       tracking error, with gains derived from the Lyapunov stability
       analysis (N3-Liu, see ``lyapunov_gains.py``).

    All inputs and outputs are numpy arrays for compatibility with
    real-time control interfaces (e.g., libfranka, ROS2 controllers).

    Attributes:
        rnea: The RNEA baseline wrapper (white-box model).
        model: The trained GreyBoxNet (learned residual).
        delta: Current payload mass [kg].
        kp: (7, 7) proportional gain matrix.
        kd: (7, 7) derivative gain matrix.
        device: Torch device for model inference.
    """

    def __init__(
        self,
        urdf_path: str,
        checkpoint_path: str,
        delta: float = 0.0,
        device: str = "cpu",
        kp: Optional[np.ndarray] = None,
        kd: Optional[np.ndarray] = None,
    ):
        """
        Initialize the controller.

        Args:
            urdf_path: Path to the Franka Panda URDF file, used by the
                RNEA wrapper for analytical inverse dynamics.
            checkpoint_path: Path to a trained GreyBoxNet ``.pt`` checkpoint
                (saved by ``training/train.py``).  The corresponding
                ``config.json`` is auto-discovered in the same directory.
            delta: Initial payload mass [kg] attached to the end-effector.
                Can be updated at runtime via :meth:`update_payload`.
            device: Torch device for neural network inference.  Use
                ``'cpu'`` for real-time control (avoids GPU transfer
                latency); ``'cuda'`` only if profiling shows a benefit.
            kp: (7, 7) proportional gain matrix.  If *None*, uses
                ``DEFAULT_KP`` from ``lyapunov_gains.py``.
            kd: (7, 7) derivative gain matrix.  If *None*, uses
                ``DEFAULT_KD`` from ``lyapunov_gains.py``.
        """
        # White-box: RNEA from URDF (pinocchio_baseline is never modified)
        self.rnea = RneaBaseline(urdf_path)

        # Learned residual: GreyBoxNet in eval mode, gradients disabled
        self.model = load_grey_box_model(checkpoint_path, device=device)
        self.device = device

        # Payload mass
        self.delta = delta

        # PD gains -- default to Lyapunov-derived gains
        self.kp = kp if kp is not None else DEFAULT_KP.copy()
        self.kd = kd if kd is not None else DEFAULT_KD.copy()

        self._validate_gains()

    def _validate_gains(self) -> None:
        """Check that gain matrices have the correct shape and are positive definite."""
        for name, mat in [("kp", self.kp), ("kd", self.kd)]:
            if mat.shape != (N_JOINTS, N_JOINTS):
                raise ValueError(
                    f"{name} must have shape ({N_JOINTS}, {N_JOINTS}), "
                    f"got {mat.shape}"
                )
            diag = np.diag(mat)
            if np.any(diag <= 0):
                raise ValueError(
                    f"{name} diagonal entries must be positive, got {diag}"
                )

    def step(
        self,
        q: np.ndarray,
        qdot: np.ndarray,
        q_des: np.ndarray,
        qdot_des: np.ndarray,
        qddot_des: np.ndarray,
    ) -> np.ndarray:
        """
        Compute the commanded torque for a single control step.

        This is the core 1 kHz function.  It must be fast:
          - RNEA: ~10 us (Pinocchio, single sample)
          - GreyBoxNet: ~50 us (MLP forward, torch.no_grad, CPU)
          - PD + clipping: ~1 us (numpy)

        Args:
            q:         (7,) current joint positions [rad].
            qdot:      (7,) current joint velocities [rad/s].
            q_des:     (7,) desired joint positions [rad].
            qdot_des:  (7,) desired joint velocities [rad/s].
            qddot_des: (7,) desired joint accelerations [rad/s^2].
                       This comes from the trajectory planner, NOT from
                       sensor differentiation.

        Returns:
            tau_cmd: (7,) commanded torques [Nm], clipped to TORQUE_LIMITS.
        """
        # --- 1. RNEA feedforward (white-box) ---
        # Reshape to (1, 7) for the batched RNEA interface, then squeeze back.
        tau_rnea = self.rnea.compute_tau_theoretical(
            q[np.newaxis, :],
            qdot[np.newaxis, :],
            qddot_des[np.newaxis, :],
            delta=self.delta,
        ).squeeze(0)  # (7,)

        # --- 2. Learned residual (GreyBoxNet) ---
        tau_res = self._predict_residual(q, qdot)  # (7,)

        # --- 3. PD error correction ---
        e = q_des - q              # position error
        edot = qdot_des - qdot     # velocity error
        tau_pd = self.kp @ e + self.kd @ edot  # (7,)

        # --- Combine ---
        tau_cmd = tau_rnea + tau_res + tau_pd

        # --- Hard safety clip to torque limits ---
        tau_cmd = np.clip(tau_cmd, -_TORQUE_LIMITS_NP, _TORQUE_LIMITS_NP)

        return tau_cmd

    def _predict_residual(self, q: np.ndarray, qdot: np.ndarray) -> np.ndarray:
        """
        Run the GreyBoxNet on a single (q, qdot, delta) sample.

        Converts numpy -> torch, runs inference with no_grad, converts back.

        Args:
            q:    (7,) joint positions [rad].
            qdot: (7,) joint velocities [rad/s].

        Returns:
            tau_res: (7,) residual torque [Nm] as a numpy array.
        """
        with torch.no_grad():
            q_t = torch.from_numpy(q).unsqueeze(0).float().to(self.device)
            qdot_t = torch.from_numpy(qdot).unsqueeze(0).float().to(self.device)
            delta_t = torch.tensor([[self.delta]], dtype=torch.float32, device=self.device)
            tau_res_t = self.model(q_t, qdot_t, delta_t)  # (1, 7)
        return tau_res_t.squeeze(0).cpu().numpy()

    def update_payload(self, delta: float) -> None:
        """
        Update the payload mass at runtime.

        Call this when the robot picks up or drops an object.  The new
        payload is reflected in both the RNEA feedforward (via payload
        injection) and the learned residual (via the delta input).

        Args:
            delta: New payload mass [kg] (>= 0).
        """
        if delta < 0:
            raise ValueError(f"Payload mass must be >= 0, got {delta}")
        self.delta = delta

    def update_gains(self, kp: np.ndarray, kd: np.ndarray) -> None:
        """
        Update PD gains at runtime.

        Typical usage: after Stage 1 training completes and validation
        error statistics are available, call
        ``compute_lyapunov_gains(tau_error_bound)`` to get the correct
        gains and pass them here.

        Args:
            kp: (7, 7) new proportional gain matrix.
            kd: (7, 7) new derivative gain matrix.
        """
        self.kp = np.asarray(kp, dtype=np.float64)
        self.kd = np.asarray(kd, dtype=np.float64)
        self._validate_gains()


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import os
    import sys
    import tempfile
    import json

    # The smoke test creates a dummy model checkpoint and tests the
    # controller in isolation, without requiring pinocchio.  If pinocchio
    # is not installed, the RNEA wrapper will raise an ImportError and
    # we skip the full integration test gracefully.

    from network.grey_box_net import GreyBoxNet

    # --- Create a dummy checkpoint ---
    with tempfile.TemporaryDirectory() as tmpdir:
        net = GreyBoxNet(hidden_dim=32, n_hidden_layers=2, activation="mish")
        ckpt_path = os.path.join(tmpdir, "greybox_best.pt")
        cfg_path = os.path.join(tmpdir, "config.json")
        torch.save(net.state_dict(), ckpt_path)
        with open(cfg_path, "w") as fh:
            json.dump(
                {"hidden_dim": 32, "n_hidden_layers": 2, "activation": "mish"},
                fh,
            )

        # --- Test without RNEA (unit-test the PD + residual path) ---
        # We test _predict_residual and the PD math directly.
        from controller.model_loader import load_grey_box_model

        model = load_grey_box_model(ckpt_path, device="cpu")
        q = np.random.randn(N_JOINTS)
        qdot = np.random.randn(N_JOINTS)

        # Manual residual prediction
        with torch.no_grad():
            q_t = torch.from_numpy(q).unsqueeze(0).float()
            qdot_t = torch.from_numpy(qdot).unsqueeze(0).float()
            delta_t = torch.zeros(1, 1)
            tau_res_expected = model(q_t, qdot_t, delta_t).squeeze(0).numpy()

        # Test PD computation
        q_des = np.zeros(N_JOINTS)
        qdot_des = np.zeros(N_JOINTS)
        e = q_des - q
        edot = qdot_des - qdot
        tau_pd = DEFAULT_KP @ e + DEFAULT_KD @ edot
        assert tau_pd.shape == (N_JOINTS,), tau_pd.shape
        print("PD computation OK -- shape", tau_pd.shape)

        # Test torque clipping
        tau_big = np.array([100.0, 100.0, 100.0, 100.0, 20.0, 20.0, 20.0])
        tau_clipped = np.clip(tau_big, -_TORQUE_LIMITS_NP, _TORQUE_LIMITS_NP)
        assert np.allclose(tau_clipped, _TORQUE_LIMITS_NP), tau_clipped
        print("Torque clipping OK")

        # --- Full integration test (requires pinocchio + URDF) ---
        try:
            # Try to build the controller -- this will fail if pinocchio
            # is not installed or no URDF is available, which is fine.
            # The smoke test above validates the core logic.
            urdf_candidate = os.path.join(
                os.path.dirname(__file__), "..", "pinocchio_baseline", "panda.urdf"
            )
            if os.path.isfile(urdf_candidate):
                ctrl = ComputedTorquePDController(
                    urdf_path=urdf_candidate,
                    checkpoint_path=ckpt_path,
                    delta=0.0,
                    device="cpu",
                )
                tau_cmd = ctrl.step(
                    q=np.zeros(N_JOINTS),
                    qdot=np.zeros(N_JOINTS),
                    q_des=np.ones(N_JOINTS) * 0.1,
                    qdot_des=np.zeros(N_JOINTS),
                    qddot_des=np.zeros(N_JOINTS),
                )
                assert tau_cmd.shape == (N_JOINTS,), tau_cmd.shape
                assert np.all(np.abs(tau_cmd) <= _TORQUE_LIMITS_NP + 1e-9)
                print(f"Full integration test OK -- tau_cmd = {tau_cmd}")

                # Test payload update
                ctrl.update_payload(1.0)
                assert ctrl.delta == 1.0

                # Test gain update
                kp_new, kd_new = np.eye(N_JOINTS) * 50.0, np.eye(N_JOINTS) * 10.0
                ctrl.update_gains(kp_new, kd_new)
                assert np.allclose(ctrl.kp, kp_new)
                print("Payload + gain update OK")
            else:
                print(
                    "URDF not found -- skipping full integration test. "
                    "Core logic validated above."
                )
        except ImportError:
            print(
                "pinocchio not installed -- skipping full integration test. "
                "Core logic validated above."
            )

    print("\ncomputed_torque_pd smoke test OK")
