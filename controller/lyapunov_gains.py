"""
Lyapunov-based PD gain computation (N3-Liu).

Plan:
  1. Given a per-joint model error bound, compute minimum Kp and Kd gains that
     guarantee Lyapunov stability of the closed-loop computed-torque + PD system.
  2. Provide sensible default gains from a conservative placeholder error bound.
  3. Expose a function so gains can be recomputed after Stage 1 training produces
     real validation error statistics.

Novelty N3-Liu (goal.md Objective 2 -- High-Frequency Real-Time Control).

Reference:
  Liu, Borja, Della Santina (2024). "Physics-Informed Neural Networks to Model
  and Control Robots: A Theoretical and Experimental Investigation."
  Advanced Intelligent Systems (Wiley), vol. 6, no. 5.
  Borrowed: Proposition 1 (Section III-C) -- Lyapunov stability condition for a
  computed-torque + PD controller under bounded model error, yielding the
  critical-damping gain formula Kp = Kd^2 / 4 and minimum Kd = safety_margin
  * error_bound.

Background (Liu et al. 2024, Proposition 1):
  For a computed-torque controller  tau = M_hat(q) qddot_des + h_hat(q,qdot)
  + Kd * edot + Kp * e,  where  e = q_des - q,  if the model error satisfies
  |tau_model - tau_true| <= epsilon  (per joint), then the tracking error
  converges to zero provided:
    - Kd > 0,  Kp > 0   (positive definite diagonal)
    - The gains dominate epsilon with sufficient margin.
  The critical-damping condition  Kp_j = Kd_j^2 / 4  ensures the error dynamics
  are non-oscillatory (fastest convergence without overshoot).
"""

from __future__ import annotations

import numpy as np

from network.constants import N_JOINTS


# ---------------------------------------------------------------------------
# Default error bound (placeholder until real validation data is available)
# ---------------------------------------------------------------------------
# Conservative per-joint bound on |tau_pred - tau_real| [Nm].
# Joints 1-4 (large) get 5 Nm; joints 5-7 (small wrist) get 2 Nm.
DEFAULT_ERROR_BOUND = np.array([5.0, 5.0, 5.0, 5.0, 2.0, 2.0, 2.0])


def compute_lyapunov_gains(
    tau_error_bound: np.ndarray,
    safety_margin: float = 2.0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute minimum diagonal PD gains for Lyapunov stability.

    The derivation follows from the closed-loop error dynamics of a
    computed-torque controller with bounded model error (Liu et al. 2024,
    Proposition 1).  For each joint *j*:

        Kd_min[j]  =  safety_margin  *  tau_error_bound[j]
        Kp_min[j]  =  Kd_min[j]^2 / 4     (critical damping)

    The *safety_margin* (>= 1) provides a multiplicative buffer above the
    minimum theoretically required gain. A value of 2.0 means the gains are
    twice the minimum needed, giving robustness against unmodeled disturbances
    beyond the training-set error bound.

    Args:
        tau_error_bound: (7,) array -- per-joint maximum absolute model error
            |tau_pred - tau_real| observed on validation data [Nm].  A larger
            bound produces larger (stiffer) gains.
        safety_margin: Multiplicative factor (>= 1.0) applied to the minimum
            Kd.  Default 2.0.

    Returns:
        kp: (7, 7) diagonal numpy array -- proportional gain matrix.
        kd: (7, 7) diagonal numpy array -- derivative gain matrix.

    Raises:
        ValueError: If inputs have wrong shape or safety_margin < 1.
    """
    tau_error_bound = np.asarray(tau_error_bound, dtype=np.float64)
    if tau_error_bound.shape != (N_JOINTS,):
        raise ValueError(
            f"tau_error_bound must have shape ({N_JOINTS},), "
            f"got {tau_error_bound.shape}"
        )
    if safety_margin < 1.0:
        raise ValueError(
            f"safety_margin must be >= 1.0, got {safety_margin}"
        )
    if np.any(tau_error_bound < 0):
        raise ValueError("tau_error_bound entries must be non-negative")

    kd_diag = safety_margin * tau_error_bound          # (7,)
    kp_diag = (kd_diag ** 2) / 4.0                     # critical damping

    kp = np.diag(kp_diag)  # (7, 7)
    kd = np.diag(kd_diag)  # (7, 7)
    return kp, kd


# ---------------------------------------------------------------------------
# Pre-computed defaults (available as module-level constants)
# ---------------------------------------------------------------------------
DEFAULT_KP, DEFAULT_KD = compute_lyapunov_gains(DEFAULT_ERROR_BOUND)


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Default error bound:", DEFAULT_ERROR_BOUND)
    print()
    print("DEFAULT_KP (diagonal):", np.diag(DEFAULT_KP))
    print("DEFAULT_KD (diagonal):", np.diag(DEFAULT_KD))
    print()

    # Verify shapes
    assert DEFAULT_KP.shape == (N_JOINTS, N_JOINTS), DEFAULT_KP.shape
    assert DEFAULT_KD.shape == (N_JOINTS, N_JOINTS), DEFAULT_KD.shape

    # Verify positive definiteness (all diagonal entries > 0)
    assert np.all(np.diag(DEFAULT_KP) > 0), "Kp must be positive definite"
    assert np.all(np.diag(DEFAULT_KD) > 0), "Kd must be positive definite"

    # Verify critical damping: Kp = Kd^2 / 4
    kd_diag = np.diag(DEFAULT_KD)
    kp_diag = np.diag(DEFAULT_KP)
    assert np.allclose(kp_diag, kd_diag**2 / 4.0), "Critical damping violated"

    # Verify with custom error bound
    custom_bound = np.array([1.0, 2.0, 3.0, 4.0, 0.5, 0.5, 0.5])
    kp_c, kd_c = compute_lyapunov_gains(custom_bound, safety_margin=3.0)
    assert kd_c.shape == (7, 7)
    assert np.allclose(np.diag(kd_c), 3.0 * custom_bound)

    print("lyapunov_gains smoke test OK")
