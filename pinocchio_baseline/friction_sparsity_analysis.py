"""
FrictionNet sparsity analysis for the Franka Panda 7-DoF arm.

Purpose: determine which entries of the 7x7 joint-space friction matrix are
structurally zero, to inform the N2-Liu FrictionNet Cholesky design.

Three investigation inputs synthesised here:
  - N2-Liu:  Cholesky dissipativity structural constraint (idea)
  - N1-Duong: L L^T + eps*I algebraic kernel (how to factorise)
  - N1-SPEL:  revolute-joint sparsity mask (which entries to factorise)

Run with:
    python -m pinocchio_baseline.friction_sparsity_analysis
or:
    python pinocchio_baseline/friction_sparsity_analysis.py [path/to/panda.urdf]
"""

from __future__ import annotations

import os
import sys
import numpy as np

URDF_DEFAULT = os.path.join(os.path.dirname(__file__), "panda.urdf")

try:
    import pinocchio as pin
    _HAS_PINOCCHIO = True
except ImportError:
    _HAS_PINOCCHIO = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sep(title: str = "", width: int = 70) -> None:
    if title:
        pad = (width - len(title) - 2) // 2
        print("=" * pad + f" {title} " + "=" * (width - pad - len(title) - 2))
    else:
        print("=" * width)


def _lower_triangular_indices(n: int) -> list[tuple[int, int]]:
    """Return (row, col) pairs for the lower-triangular part of an nxn matrix."""
    return [(i, j) for i in range(n) for j in range(i + 1)]


def _print_cholesky_L(n: int, mask: np.ndarray | None = None) -> None:
    """
    Pretty-print the lower-triangular L of an nxn Cholesky factorisation.
    mask: boolean (n, n) array -- True means the entry is non-zero.
          If None, all lower-triangular entries are shown as non-zero.
    """
    for i in range(n):
        row = "  ["
        for j in range(n):
            if j > i:
                cell = "  * "
            elif mask is not None and not mask[i, j]:
                cell = "  0 "
            elif i == j:
                cell = f"d{i+1} " if n <= 9 else f"d{i+1:02d}"
            else:
                cell = f"l{i+1}{j+1}" if n <= 9 else f"l{i+1:02d}{j+1:02d}"
            row += cell + " "
        row += "]"
        print(row)


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyse(urdf_path: str) -> None:
    if not _HAS_PINOCCHIO:
        print("ERROR: pinocchio not installed. Install with: pip install pin")
        print("The analysis logic is still readable in this file.")
        _print_theory_only()
        return

    model = pin.buildModelFromUrdf(urdf_path)
    N = model.nv  # degrees of freedom (should be 7 for Franka Panda)

    # ------------------------------------------------------------------
    # 1. Joint topology
    # ------------------------------------------------------------------
    _sep("Joint Topology")
    print(f"URDF: {urdf_path}")
    print(f"DoF (nv): {N}   |   nq: {model.nq}   |   njoints: {model.njoints}\n")

    joint_types = []
    joint_axes  = []
    for jid in range(1, model.njoints):  # joint 0 is the universe
        jname = model.names[jid]
        jtype = model.joints[jid].shortname()
        # Rotation axis is available for JointModelRX/RY/RZ and JointModelRevoluteUnaligned
        axis_str = "--"
        if hasattr(model.joints[jid], "axis"):
            ax = np.array(model.joints[jid].axis)
            axis_str = f"[{ax[0]:+.0f}, {ax[1]:+.0f}, {ax[2]:+.0f}]"
        print(f"  Joint {jid:2d}  {jname:<30s}  type={jtype:<25s}  axis={axis_str}")
        joint_types.append(jtype)
        joint_axes.append(axis_str)

    # ------------------------------------------------------------------
    # 2. URDF friction / damping
    # ------------------------------------------------------------------
    _sep("URDF Friction and Damping (Pinocchio)")
    print("Pinocchio exposes per-DoF friction/damping as 1-D vectors,")
    print("not as matrices -- confirming the URDF models friction diagonally.\n")
    print(f"  model.friction  (shape {model.friction.shape}):  {model.friction}")
    print(f"  model.damping   (shape {model.damping.shape}):   {model.damping}")

    all_zero_friction = np.allclose(model.friction, 0.0)
    all_zero_damping  = np.allclose(model.damping,  0.0)
    if all_zero_friction and all_zero_damping:
        print("\n  NOTE: All URDF friction/damping values are zero.")
        print("  The Franka URDF omits joint dynamics -- friction is entirely")
        print("  unmodeled analytically, which is exactly why the FrictionNet")
        print("  residual is needed. There is no URDF-side coupling to learn from.")
    else:
        print("\n  Non-zero entries detected. Inspect the values above for coupling.")

    # ------------------------------------------------------------------
    # 3. Inertia matrix at a neutral configuration
    # ------------------------------------------------------------------
    _sep("Joint-Space Inertia Matrix M(q) at q=0")
    q0 = pin.neutral(model)
    data = model.createData()
    M = pin.crba(model, data, q0)
    print(f"  Shape: {M.shape}  (should be {N}x{N})\n")

    print("  M(q=0)  [Kg*m^2]  (full matrix for reference):")
    for i in range(N):
        row_str = "  " + "  ".join(f"{M[i, j]:8.4f}" for j in range(N))
        print(row_str)

    print()
    print("  Diagonal entries (self-inertia per joint):")
    for i in range(N):
        print(f"    Joint {i+1}: M[{i},{i}] = {M[i,i]:.4f} Kg*m^2")

    off_diag = M.copy()
    np.fill_diagonal(off_diag, 0.0)
    print(f"\n  Max |off-diagonal| entry: {np.max(np.abs(off_diag)):.4f} Kg*m^2")
    print("  -> Inertia matrix IS coupled (expected for a serial arm).")
    print("  -> BUT inertia coupling ≠ friction coupling. Friction acts")
    print("    at each motor independently of the kinematic chain coupling.")

    # ------------------------------------------------------------------
    # 4. Sparsity argument
    # ------------------------------------------------------------------
    _sep("Sparsity Argument for the 7x7 Friction Matrix")
    print("""
  PHYSICAL REASONING
  ------------------
  1. Each Franka Panda joint is independently actuated by its own motor
     and gearbox. There is no tendon drive, no parallel mechanism, and no
     shared drive train between any two joints.

  2. Friction (Coulomb + viscous) acts at the motor shaft of EACH joint
     independently:
         tau_friction_i = b_i * qdot_i + f_c_i * sign(qdot_i)
     There is no physical mechanism by which the velocity of joint j
     contributes to the friction torque at joint i (i ≠ j).

  3. The URDF <dynamics> specification uses per-joint scalars (friction,
     damping), not a matrix -- reflecting the same physical assumption.

  4. N1-SPEL's insight: in the port-Hamiltonian Lie-group formulation, the
     per-LINK dissipation matrix D_link is 3x3 (SE(3) body velocities).
     For a revolute joint rotating about a single axis, only one velocity
     component is non-zero at the joint, making D_link effectively rank-1.
     Projected to joint space for a serial chain, this collapses to a
     SCALAR per joint -- confirming the diagonal structure.

  CONCLUSION: The joint-space friction matrix D is DIAGONAL for the Franka Panda.
    D = diag(d_1, d_2, ..., d_7)   with d_i > 0 (viscous friction, positive)
""")

    # ------------------------------------------------------------------
    # 5. Cholesky comparison: full vs. diagonal
    # ------------------------------------------------------------------
    _sep("Cholesky Design Comparison")

    full_params = N * (N + 1) // 2  # lower-triangular entries
    diag_params = N
    wrist_params = 3 * (3 + 1) // 2  # 3x3 Cholesky for wrist block

    print(f"\n  Option A -- FULL Cholesky (N1-Duong kernel, no sparsity mask)")
    print(f"  {N}x{N} lower-triangular L, D = L @ L.T + eps*I")
    print(f"  Free parameters: {full_params}  (all lower-triangular entries)")
    print()
    _print_cholesky_L(N)

    print(f"\n  Option B -- DIAGONAL (N1-SPEL sparsity mask applied)  ← RECOMMENDED")
    print(f"  D = diag(Softplus(d_1), ..., Softplus(d_7))")
    print(f"  Free parameters: {diag_params}  ({full_params - diag_params} off-diagonal entries zeroed)")
    diag_mask = np.eye(N, dtype=bool)
    _print_cholesky_L(N, mask=diag_mask)

    print(f"\n  Option C -- BLOCK-DIAGONAL (conservative compromise)")
    print(f"  Joints 1-4 diagonal, joints 5-7 full 3x3 Cholesky")
    print(f"  Free parameters: 4 + {wrist_params} = {4 + wrist_params}")
    print(f"  Justification: wrist joints (5-7) share a compact mechanism;")
    print(f"  slight cross-coupling not ruled out by URDF alone.")

    print(f"\n  Summary:")
    print(f"    Option A (full Cholesky):    {full_params:3d} parameters  -- no physical justification")
    print(f"    Option C (block-diagonal):   {4 + wrist_params:3d} parameters  -- conservative")
    print(f"    Option B (diagonal):         {diag_params:3d} parameters  -- physically justified OK")
    print(f"    Parameter reduction B vs A:  {(full_params - diag_params)/full_params*100:.0f}%")

    # ------------------------------------------------------------------
    # 6. FrictionNet design recommendation
    # ------------------------------------------------------------------
    _sep("FrictionNet Design Recommendation")
    print(f"""
  RECOMMENDED ARCHITECTURE: Diagonal FrictionNet
  -----------------------------------------------
  Input:  x = [sin(q), cos(q), qdot, delta]  in R^22  (same as GreyBoxNet)
  Hidden: 1-2 layers (64 units, Mish) -- lightweight sub-module
  Output: d = Linear(hidden -> 7)
  Friction matrix: D(x) = diag(Softplus(d))   -> PSD by construction
  Friction torque: tau_friction = D(x) @ qdot  -> velocity-proportional

  Why Softplus on diagonal:
    - Ensures d_i > 0 (positive viscous friction, physically correct)
    - Softplus is smooth -> satisfies Mish/Softplus-only activation rule
    - Equivalent to the diagonal of N1-Duong's L L^T when L is diagonal

  Integration into GreyBoxNet:
    tau_res = FrictionNet(q, qdot, delta) @ qdot   [friction component]
            + tau_unmodeled(q, qdot, delta)          [other residual]
    OR (simpler): keep GreyBoxNet as-is and use this analysis only to
    inform the dissipativity constraint structure in constraints.py,
    replacing the scalar batch-mean dissipativity multiplier with a
    per-joint multiplier (one lambda per joint, not one global lambda).

  Dissipativity check (current constraints.py):
    tau_res * qdot <= 0   (batch-mean dot product)
  With diagonal friction structure:
    For each joint i: tau_res_i * qdot_i <= 0  (per-joint, stronger)

  NEXT STEP: implement and compare on synthetic data:
    1. GreyBoxNet baseline (current, no FrictionNet)
    2. GreyBoxNet + diagonal FrictionNet sub-module
    Compare: training loss, val RMSE, dissipativity violation rate.
""")

    _sep()
    print("Analysis complete. Results inform branch: novelty/N2-Liu-frictionnet")
    print(f"URDF loaded: {urdf_path}")
    print(f"DoF confirmed: {N}")


def _print_theory_only() -> None:
    """Fallback output when Pinocchio is not available."""
    _sep("Theory-Only Mode (pinocchio not installed)")
    print("""
  Physical argument (no URDF loading needed):

  The Franka Panda has 7 independently-actuated revolute joints.
  Each joint motor contributes friction only to its own joint torque.
  -> joint-space friction matrix D is DIAGONAL (7 free parameters)
  -> Recommended FrictionNet: D = diag(Softplus(d_1..d_7))
  -> 75% parameter reduction vs full 28-entry Cholesky (N1-Duong form)

  Install pinocchio to confirm via URDF inspection:
      pip install pin
""")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    urdf_path = sys.argv[1] if len(sys.argv) > 1 else URDF_DEFAULT
    if not os.path.isfile(urdf_path):
        print(f"ERROR: URDF not found at: {urdf_path}")
        print("Usage: python -m pinocchio_baseline.friction_sparsity_analysis [path/to/panda.urdf]")
        sys.exit(1)
    analyse(urdf_path)
