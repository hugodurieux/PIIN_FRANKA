#!/usr/bin/env python3
"""
generate_isaac_dataset.py

Isaac Sim physics-based training data generator for Stage 1 PINN.

WHY ISAAC SIM vs. generate_fourier_dataset.py
----------------------------------------------
generate_fourier_dataset.py uses a hand-tuned synthetic friction residual
(Coulomb + viscous). The network learns this artificial model, which does
not match the real Franka Panda's friction, damping, and actuator dynamics.

This script uses Isaac Sim's physics engine (joint friction, damping, gear
compliance from the Franka USD) as the source of tau_real. The residual:

    tau_res = tau_real(Isaac Sim) - tau_theo(Pinocchio RNEA)

reflects REAL unmodelled joint dynamics. The GreyBoxNet and FrictionNet learn
physically meaningful friction and compliance signatures that transfer to the
real Franka.

USAGE — run from inside Isaac Sim's Python environment (not system Python):

    cd /path/to/isaac-sim-root
    ./python.sh /path/to/pinn_franka/generate_isaac_dataset.py --payload 0.0
    ./python.sh /path/to/pinn_franka/generate_isaac_dataset.py --payload 1.0
    ./python.sh /path/to/pinn_franka/generate_isaac_dataset.py --payload 3.0

    # Or all three payloads in sequence:
    for P in 0.0 1.0 3.0; do
        ./python.sh /path/to/pinn_franka/generate_isaac_dataset.py --payload $P
    done

OUTPUT — same HDF5 schema as fourier_baseline_*.h5 (training code unchanged):
    data/isaac_0.0kg.h5
    data/isaac_1.0kg.h5
    data/isaac_3.0kg.h5

TRAINING (same command, different --data paths):
    python3 -m training.train \\
        --data data/isaac_0.0kg.h5 data/isaac_1.0kg.h5 data/isaac_3.0kg.h5 \\
        --epochs 200 --use_friction_net

PREREQUISITES:
    - Isaac Sim 4.x installed (provides isaacsim, omni.isaac.core, etc.)
    - pinocchio (pip install pin) inside Isaac Sim's Python environment
    - h5py (pip install h5py) inside Isaac Sim's Python environment
    - scipy (pip install scipy) — optional, for Sobol sampling
    - Nucleus server running (or local asset cache) for Franka USD
"""

# Isaac Sim MUST be initialized before any omni.* imports
from isaacsim import SimulationApp
_sim_app = SimulationApp({"headless": True, "anti_aliasing": 0})

import argparse
import os
import sys
import time

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# isaacsim imports — only valid after SimulationApp() is constructed
# NOTE: Isaac Sim 5.0+/6.x renamed omni.isaac.* -> isaacsim.*.
# Articulation (single-robot) moved to isaacsim.core.prims.SingleArticulation;
# get_assets_root_path moved to isaacsim.storage.native.nucleus.
from isaacsim.core.api import World
from isaacsim.core.prims import SingleArticulation as Articulation
from isaacsim.core.utils.types import ArticulationAction
from isaacsim.core.utils.stage import add_reference_to_stage
from isaacsim.storage.native.nucleus import get_assets_root_path
from pxr import UsdPhysics

try:
    import h5py
except ImportError:
    print("ERROR: h5py not installed inside Isaac Sim Python.")
    print("       Run: ./python.sh -m pip install h5py")
    sys.exit(1)

try:
    from scipy.stats.qmc import Sobol as _Sobol
    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False


# `pin` (pinocchio) ships prebundled with the isaacsim.robot_motion.pink
# extension via the `cmeel` build system: the real package lives under
# .../pip_prebundle/cmeel.prefix/lib/python3.X/site-packages/pinocchio, and
# cmeel.pth (in pip_prebundle) is what's supposed to add that nested dir to
# sys.path via `import cmeel_pth`. setup_python_env.sh already puts
# pip_prebundle itself on PYTHONPATH (confirmed: cmeel_pth.py sits directly
# inside it), but plain PYTHONPATH entries don't trigger .pth processing, so
# the nested site-packages dir never gets added and `import pinocchio` fails.
# Since cmeel_pth is already reachable on sys.path, import it directly —
# this is exactly what cmeel.pth would do, without relying on
# site.addsitedir()'s .pth auto-processing (which proved unreliable here).
try:
    import cmeel_pth  # noqa: F401  (side effect: extends sys.path for pinocchio)
except ImportError:
    import site
    _ISAAC_PATH = os.environ.get("ISAAC_PATH", "")
    for _ext in ("isaacsim.robot_motion.pink", "isaacsim.robot_motion.cumotion"):
        _prebundle = os.path.join(_ISAAC_PATH, "exts", _ext, "pip_prebundle")
        if os.path.isdir(_prebundle):
            site.addsitedir(_prebundle)

try:
    import pinocchio as pin
except ImportError:
    print("ERROR: pinocchio not importable inside Isaac Sim Python.")
    print(f"       ISAAC_PATH={os.environ.get('ISAAC_PATH', '<unset>')}")
    print("       sys.path:")
    for _p in sys.path:
        print(f"         {_p}")
    raise

from network.constants import N_JOINTS, TORQUE_LIMITS  # [87,87,87,87,12,12,12] Nm
TORQUE_LIMITS = TORQUE_LIMITS.numpy()  # this script is pure numpy, no torch elsewhere

# ---------------------------------------------------------------------------
# Franka Panda joint limits (from URDF / Franka specs)
# ---------------------------------------------------------------------------
Q_LOWER = np.array([-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973])
Q_UPPER = np.array([ 2.8973,  1.7628,  2.8973, -0.0698,  2.8973,  3.7525,  2.8973])

# ---------------------------------------------------------------------------
# Generation parameters — mirror generate_fourier_dataset.py for comparability
# ---------------------------------------------------------------------------
N_SEGMENTS    = 10
N_PER_SEGMENT = 5_000     # 5 s at 1 kHz
N_HARMONICS   = 5
SIM_DT        = 1.0 / 1_000.0   # 1 kHz physics step
WARMUP_STEPS  = 200              # steps before recording (physics settle)

ARM_JOINT_NAMES = [f"panda_joint{i}" for i in range(1, 8)]
EE_LINK_NAME    = "panda_hand"
FRANKA_USD_REL  = "/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd"
FRANKA_PRIM     = "/World/Franka"


# ===========================================================================
# Trajectory generation (Sobol + Fourier) — same excitation design as
# generate_fourier_dataset.py for cross-method comparability
# ===========================================================================

def _sobol_q_centers(n: int, seed: int) -> np.ndarray:
    """Return n joint configurations via Sobol low-discrepancy sampling."""
    if _HAS_SCIPY:
        raw = _Sobol(d=N_JOINTS, scramble=True, seed=seed).random(n)
        print(f"  [N1-WangCAC] Sobol sampling  seed={seed}")
    else:
        raw = np.random.default_rng(seed).uniform(size=(n, N_JOINTS))
        print("  [N1-WangCAC] scipy not found — uniform fallback")
    return Q_LOWER + raw * (Q_UPPER - Q_LOWER)


def _fourier_segment(q_center: np.ndarray, n_steps: int,
                     dt: float, rng: np.random.Generator):
    """Generate one Fourier excitation segment around q_center.

    Returns (q, qdot, qddot) each shaped (n_steps, 7), dtype float32.
    qddot is analytical from the Fourier parametrisation — used for RNEA.
    """
    t   = np.arange(n_steps) * dt
    A   = rng.uniform(0.05, 0.30, (N_HARMONICS, N_JOINTS))
    wn  = rng.uniform(0.50, 3.00, (N_HARMONICS, N_JOINTS))
    ph  = rng.uniform(0.00, 2.0 * np.pi, (N_HARMONICS, N_JOINTS))

    q     = q_center + sum(
        A[k] * np.sin(np.outer(t, wn[k]) + ph[k]) for k in range(N_HARMONICS)
    )
    qdot  = sum(
        A[k] * wn[k] * np.cos(np.outer(t, wn[k]) + ph[k]) for k in range(N_HARMONICS)
    )
    qddot = sum(
        -A[k] * wn[k]**2 * np.sin(np.outer(t, wn[k]) + ph[k]) for k in range(N_HARMONICS)
    )
    q = np.clip(q, Q_LOWER + 0.05, Q_UPPER - 0.05)
    return (q.astype(np.float32),
            qdot.astype(np.float32),
            qddot.astype(np.float32))


# ===========================================================================
# Pinocchio RNEA — white-box analytical baseline (tau_theo)
# ===========================================================================

def _load_pin_model(urdf_path: str, payload_kg: float):
    full_model = pin.buildModelFromUrdf(urdf_path)

    # panda.urdf has 7 revolute arm joints + 2 prismatic finger joints (nq=9).
    # Isaac Sim commands the fingers to stay fixed at 0 throughout data
    # generation (see q_cmd/qdot_cmd, only arm_idx is driven), so the RNEA
    # model must match: lock both finger joints at 0 to reduce nq -> 7 and
    # line up with the 7-column q/qdot/qddot arrays collected from the sim.
    finger_joints = ["panda_finger_joint1", "panda_finger_joint2"]
    joints_to_lock = [full_model.getJointId(j) for j in finger_joints]
    reference_q = pin.neutral(full_model)
    model = pin.buildReducedModel(full_model, joints_to_lock, reference_q)
    data  = model.createData()
    if payload_kg > 0.0:
        ee_id   = model.getFrameId(EE_LINK_NAME)
        body_id = model.frames[ee_id].parent
        inertia = model.inertias[body_id]
        inertia.mass += payload_kg
        model.inertias[body_id] = inertia
        print(f"  [pinocchio] Payload {payload_kg} kg injected into '{EE_LINK_NAME}'")
    return model, data


def _rnea_batch(model, data, q: np.ndarray,
                qdot: np.ndarray, qddot: np.ndarray) -> np.ndarray:
    n   = q.shape[0]
    tau = np.zeros((n, N_JOINTS), dtype=np.float32)
    for i in range(n):
        pin.rnea(model, data,
                 q[i].astype(float), qdot[i].astype(float), qddot[i].astype(float))
        tau[i] = data.tau[:N_JOINTS]
    return tau


# ===========================================================================
# Isaac Sim helpers
# ===========================================================================

def _build_world() -> tuple:
    """Create Isaac Sim World and load the built-in Franka Panda USD."""
    world = World(physics_dt=SIM_DT, stage_units_in_meters=1.0)

    assets_root = get_assets_root_path()
    if assets_root is None:
        raise RuntimeError(
            "Isaac Sim Nucleus not reachable.\n"
            "Ensure the Nucleus server is running, or set the OMNI_ASSET_ROOT "
            "environment variable to a local cached assets directory."
        )
    usd_path = assets_root + FRANKA_USD_REL
    add_reference_to_stage(usd_path=usd_path, prim_path=FRANKA_PRIM)

    robot = Articulation(prim_path=FRANKA_PRIM, name="franka")
    world.scene.add(robot)
    world.reset()
    return world, robot


def _arm_indices(robot: Articulation) -> np.ndarray:
    """Return the DoF index for each of the 7 arm joints."""
    names   = list(robot.dof_names)
    missing = [n for n in ARM_JOINT_NAMES if n not in names]
    if missing:
        raise ValueError(
            f"Expected arm joints {missing} not found in articulation.\n"
            f"Available DoF names: {names}"
        )
    return np.array([names.index(n) for n in ARM_JOINT_NAMES])


def _attach_payload(stage, payload_kg: float):
    """Add payload mass to the end-effector link — mirrors pinocchio _inject_payload."""
    if payload_kg <= 0.0:
        return
    ee_path = f"{FRANKA_PRIM}/{EE_LINK_NAME}"
    prim    = stage.GetPrimAtPath(ee_path)
    if not prim.IsValid():
        print(f"  [payload] WARNING: '{ee_path}' not found — payload not attached.")
        return
    mass_api = UsdPhysics.MassAPI.Apply(prim)
    prev = mass_api.GetMassAttr().Get() or 0.0
    mass_api.GetMassAttr().Set(float(prev) + payload_kg)
    print(f"  [payload] +{payload_kg} kg on {ee_path}  (prev {prev:.3f} kg)")


# ===========================================================================
# Main data generation loop
# ===========================================================================

def generate_and_save(payload_kg: float, out_dir: str,
                      urdf_path: str, seed: int = 42) -> str:

    sep = "=" * 64
    print(f"\n{sep}")
    print(f"  Isaac Sim dataset  —  payload {payload_kg} kg  —  seed {seed}")
    print(sep)

    # -- Pinocchio --
    print("\n[1/4] Pinocchio model")
    pin_model, pin_data = _load_pin_model(urdf_path, payload_kg)
    print(f"      nv={pin_model.nv}  nq={pin_model.nq}")

    # -- Isaac Sim world --
    print("\n[2/4] Isaac Sim world")
    world, robot = _build_world()
    n_dof = robot.num_dof
    _attach_payload(world.stage, payload_kg)
    world.reset()
    arm_idx = _arm_indices(robot)
    print(f"      {n_dof} DoF  |  arm indices: {arm_idx.tolist()}")

    # Live joint-drive gains — a stiff position/velocity servo can turn a small
    # tracking error into a large "measured" torque that looks like residual
    # dynamics but is really PD correction, not physical friction/compliance.
    dof_props = robot.dof_properties
    print("      joint drive gains (stiffness, damping) per arm joint:")
    for j, idx in enumerate(arm_idx):
        print(f"        J{j+1}: stiffness={dof_props['stiffness'][idx]:.1f}  "
              f"damping={dof_props['damping'][idx]:.1f}  "
              f"maxEffort={dof_props['maxEffort'][idx]:.1f}")

    # -- Trajectory generation --
    print("\n[3/4] Simulating Fourier+Sobol trajectories")
    q_centers = _sobol_q_centers(N_SEGMENTS,
                                 seed=seed + int(payload_kg * 100))
    rng = np.random.default_rng(seed)

    all_q, all_qdot, all_qddot = [], [], []
    all_tau_real, all_delta    = [], []
    all_q_ref, all_qdot_ref    = [], []  # commanded reference, for tracking-error diagnostic

    for seg_i, q_center in enumerate(q_centers):
        q_ref, qdot_ref, qddot_ref = _fourier_segment(
            q_center, N_PER_SEGMENT, SIM_DT, rng
        )

        # Full-DoF command buffers (gripper fingers stay at 0)
        q_cmd    = np.zeros((N_PER_SEGMENT, n_dof), dtype=np.float32)
        qdot_cmd = np.zeros((N_PER_SEGMENT, n_dof), dtype=np.float32)
        q_cmd[:, arm_idx]    = q_ref
        qdot_cmd[:, arm_idx] = qdot_ref

        # Warmup: set initial pose and let physics settle
        init_q = np.zeros(n_dof, dtype=np.float32)
        init_q[arm_idx] = q_ref[0]
        robot.set_joint_positions(init_q)
        robot.set_joint_velocities(np.zeros(n_dof, dtype=np.float32))
        for _ in range(WARMUP_STEPS):
            world.step(render=False)

        seg_q, seg_qdot, seg_tau = [], [], []

        for t in range(N_PER_SEGMENT):
            # Drive arm to Fourier reference via position+velocity targets
            action = ArticulationAction(
                joint_positions=q_cmd[t],
                joint_velocities=qdot_cmd[t],
                joint_indices=np.arange(n_dof),
            )
            robot.apply_action(action)
            world.step(render=False)

            # Read actual physics state and measured joint efforts (tau_real)
            seg_q.append(robot.get_joint_positions()[arm_idx].copy())
            seg_qdot.append(robot.get_joint_velocities()[arm_idx].copy())
            seg_tau.append(robot.get_measured_joint_efforts()[arm_idx].copy())

        seg_q    = np.array(seg_q,    dtype=np.float32)
        seg_qdot = np.array(seg_qdot, dtype=np.float32)
        seg_tau  = np.array(seg_tau,  dtype=np.float32)

        # Filter timesteps where any joint exceeds its torque limit
        valid   = np.all(np.abs(seg_tau) <= TORQUE_LIMITS, axis=1)
        n_valid = int(valid.sum())
        n_filt  = N_PER_SEGMENT - n_valid
        if n_filt:
            print(f"    seg {seg_i+1}: {n_filt} over-torque samples removed")

        all_q.append(seg_q[valid])
        all_qdot.append(seg_qdot[valid])
        all_qddot.append(qddot_ref[valid])  # analytical from Fourier parametrisation
        all_tau_real.append(seg_tau[valid])
        all_delta.append(np.full(n_valid, payload_kg, dtype=np.float32))
        all_q_ref.append(q_ref[valid])
        all_qdot_ref.append(qdot_ref[valid])

        total = sum(len(a) for a in all_q)
        print(f"    seg {seg_i+1:2d}/{N_SEGMENTS}  valid={n_valid:5d}  "
              f"cumulative={total:6d}")

    world.stop()

    # -- Concatenate --
    q_all        = np.concatenate(all_q)
    qdot_all     = np.concatenate(all_qdot)
    qddot_all    = np.concatenate(all_qddot)
    tau_real_all = np.concatenate(all_tau_real)
    delta_all    = np.concatenate(all_delta)
    q_ref_all    = np.concatenate(all_q_ref)
    qdot_ref_all = np.concatenate(all_qdot_ref)

    # -- Tracking-error diagnostic --
    # tau_theo is computed from (q_actual, qdot_actual, qddot_REFERENCE) — a mix
    # of simulated state and analytical Fourier acceleration. That's only a
    # valid approximation if the Isaac Sim joint drive tracks the Fourier
    # reference tightly. Large tracking error would leak into tau_res as an
    # artifact, not real unmodelled physics — check before trusting residuals.
    q_track_rmse    = np.sqrt(np.mean((q_all - q_ref_all)**2, axis=0))
    qdot_track_rmse = np.sqrt(np.mean((qdot_all - qdot_ref_all)**2, axis=0))
    print("\n[diagnostic] trajectory tracking error (actual vs. Fourier reference):")
    for j in range(N_JOINTS):
        print(f"    J{j+1}: q_rmse={q_track_rmse[j]:.4f} rad   "
              f"qdot_rmse={qdot_track_rmse[j]:.4f} rad/s")

    # -- Pinocchio RNEA → tau_theo --
    print(f"\n[4/4] Pinocchio RNEA for {len(q_all):,} samples ...")
    t0 = time.time()
    tau_theo_all = _rnea_batch(pin_model, pin_data, q_all, qdot_all, qddot_all)
    print(f"      {time.time()-t0:.1f}s")

    tau_res_all = (tau_real_all - tau_theo_all).astype(np.float32)

    # -- Residual diagnostic --
    # Non-zero residual = Isaac Sim adds dynamics beyond the URDF RNEA model.
    # If residuals are near zero, check that the Franka USD has friction/damping.
    per_joint_rmse = np.sqrt(np.mean(tau_res_all**2, axis=0))
    mean_res = float(np.mean(np.abs(tau_res_all)))
    print(f"\n[diagnostic] tau_res per-joint RMSE (Nm):")
    for j, v in enumerate(per_joint_rmse):
        print(f"    J{j+1}: {v:.4f} Nm")
    if mean_res < 0.01:
        print(
            "  WARNING: mean residual < 0.01 Nm — residuals are near zero.\n"
            "  The Franka USD may share inertials with the URDF, reducing\n"
            "  the residual to numerical noise. Verify joint friction/damping\n"
            "  is set in the Franka USD (Physics > Drive > Damping/Friction)."
        )
    else:
        print(f"  Mean |tau_res|: {mean_res:.4f} Nm  ✓  non-zero residuals confirmed")

    # -- Save HDF5 --
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"isaac_{payload_kg:.1f}kg.h5")
    with h5py.File(out_path, "w") as f:
        f.create_dataset("q",        data=q_all)
        f.create_dataset("qdot",     data=qdot_all)
        f.create_dataset("qddot",    data=qddot_all)
        f.create_dataset("tau_real", data=tau_real_all)
        f.create_dataset("tau_theo", data=tau_theo_all.astype(np.float32))
        f.create_dataset("tau_res",  data=tau_res_all)
        f.create_dataset("delta",    data=delta_all)
        # Metadata
        f.attrs["payload_kg"]  = payload_kg
        f.attrs["n_segments"]  = N_SEGMENTS
        f.attrs["n_harmonics"] = N_HARMONICS
        f.attrs["sim_dt"]      = SIM_DT
        f.attrs["source"]      = "isaac_sim"
        f.attrs["seed"]        = seed
    print(f"\nSaved {len(q_all):,} samples  →  {out_path}")
    return out_path


def main():
    p = argparse.ArgumentParser(
        description="Generate Franka Panda training data via Isaac Sim physics"
    )
    p.add_argument("--payload", type=float, default=0.0,
                   help="End-effector payload in kg (default: 0.0)")
    p.add_argument("--out", type=str, default="data",
                   help="Output directory for HDF5 files (default: data/)")
    p.add_argument(
        "--urdf", type=str,
        default=os.path.join(PROJECT_ROOT, "pinocchio_baseline", "panda.urdf"),
        help="Path to Franka URDF for Pinocchio RNEA"
    )
    p.add_argument("--seed", type=int, default=42,
                   help="Random seed for trajectory generation")
    args = p.parse_args()

    out_path = generate_and_save(
        payload_kg=args.payload,
        out_dir=args.out,
        urdf_path=args.urdf,
        seed=args.seed,
    )
    print(f"\nDone — {out_path}")
    _sim_app.close()


if __name__ == "__main__":
    main()
