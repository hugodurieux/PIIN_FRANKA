#!/usr/bin/env python3
"""
generate_mujoco_dataset.py

In-domain training data generator for Stage 1, sourced from the SAME MuJoCo
model the Stage 3/4 controller is actually deployed against.

WHY THIS FILE EXISTS
--------------------
The 2026-07-29 closed-loop ablation measured that the residual currently in the
loop makes tracking WORSE, not better:

    residual ON   panda_joint5 bias -0.0337 rad,  flange error 14.3 mm
    residual OFF  panda_joint5 bias -0.0015 rad,  flange error  7.5 mm

That is a 22x bias reduction and a halved Cartesian error from switching the
learned model OFF. The cause is not that the grey-box approach fails. The
checkpoint in the loop (models/run_20260716_121302) was trained on Isaac Sim
data and is evaluated in MuJoCo: it learned the gap between RNEA and *Isaac's*
dynamics, and is adding that to a simulator which does not have them. It is
being asked to extrapolate out of its training domain, and it does so badly.

This script closes that gap by generating tau_real from MuJoCo itself, so the
residual learns the gap that actually exists at deployment.

WHAT THE RESIDUAL WILL ACTUALLY LEARN HERE -- STATED PLAINLY
------------------------------------------------------------
panda_arm_mujoco.xml gives every arm joint `armature="0.1" damping="1"` and no
frictionloss. So the MuJoCo-minus-RNEA gap is, to a very good approximation:

    tau_res  =  -1.0 * qdot      (viscous damping, in qfrc_passive)
                +0.1 * qddot     (rotor inertia, added to M's diagonal)

The damping term is linear in qdot and is exactly the form FrictionNet's
dissipative D(q,qdot) qdot structure is built to represent, so it should fit
almost perfectly and D should converge near 1.0 on every joint -- a far more
physically meaningful outcome than the Isaac run, where D_44 diverged to 3.86
while D_11 collapsed to 0.

The armature term is NOT representable: the network's input is (q, qdot, delta)
and never sees qddot (training/dataset.py does not load it). That is a known,
bounded floor on the achievable residual error, not a bug.

Be honest about what this buys: a residual that works here is evidence the
PIPELINE works end to end, not evidence that it would identify real Franka
friction. MuJoCo's gap is a linear coefficient the MJCF declares openly. Real
hardware is Coulomb, stiction, temperature drift and backlash. This makes the
demo work and exercises every stage; it does not settle the sim-to-real claim.

WHY INVERSE DYNAMICS RATHER THAN A SERVO ROLLOUT
------------------------------------------------
generate_isaac_dataset.py commands a trajectory through a joint drive and
records what the drive did. That couples the data to the servo: when the drive
saturates, the recorded torque is the clamp value rather than the dynamics, and
tau_theo (computed from the *reference* acceleration the servo never achieved)
disagrees with it enormously. That is the entire reason SATURATION_MARGIN=0.97
exists there, and it silently discards timesteps.

MuJoCo exposes mj_inverse, which answers the question directly: given a state
(q, qdot) and a desired acceleration qddot, what generalised force is required?
There is no servo, no tracking error, no saturation, and no filtering. Every
sample is exact, and (q, qdot, qddot, tau_real) is consistent by construction --
which is precisely the quadruple RNEA needs to be compared against.

Contacts are DISABLED during collection (mjDSBL_CONTACT). The residual is a
free-space dynamics model; the controller runs it in free space; and leaving
contacts on would let the floor and the loose grasp_object inject constraint
forces into qfrc_inverse that RNEA has no way to model.

USAGE
-----
    # one-off: the project venv does not ship mujoco
    .venv/bin/pip install mujoco

    .venv/bin/python generate_mujoco_dataset.py --payload 0.0
    .venv/bin/python generate_mujoco_dataset.py --payload 1.0
    .venv/bin/python generate_mujoco_dataset.py --payload 3.0

OUTPUT
------
    data/mujoco_0.0kg.h5, data/mujoco_1.0kg.h5, data/mujoco_3.0kg.h5

Same HDF5 schema as the Isaac files (q, qdot, qddot, tau_real, tau_theo,
tau_res, delta), so training/, evaluation/ and controller/ need no changes.
Unlike those files this one also writes an explicit `segment_id` dataset, so
training/segment_splits.py can partition by trajectory exactly instead of
recovering boundaries from the largest jumps in ||q[i+1] - q[i]||.
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np

try:
    import mujoco
except ImportError:
    sys.exit(
        "ERROR: the `mujoco` package is required and is not in this interpreter.\n"
        "       Install it into the project venv:  .venv/bin/pip install mujoco\n"
        "       (it is NOT the same environment as ~/mujoco_debug_venv)"
    )

try:
    import pinocchio as pin
except ImportError:
    sys.exit(
        "ERROR: pinocchio not importable. Run with the project venv:\n"
        "       .venv/bin/python generate_mujoco_dataset.py ...\n"
        "       (system python3 has neither pinocchio nor torch)"
    )

try:
    import h5py
except ImportError:
    sys.exit("ERROR: h5py required.  .venv/bin/pip install h5py")

try:
    from scipy.stats import qmc as _qmc
    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from network.constants import N_JOINTS, TORQUE_LIMITS  # noqa: E402

TORQUE_LIMITS = np.asarray(TORQUE_LIMITS, dtype=np.float64).reshape(-1)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DEFAULT_MJCF = os.path.join(
    _HERE, "ros2_ws", "src", "pinn_franka_controller", "mujoco",
    "franka_emika_panda", "panda_arm_mujoco.xml",
)
DEFAULT_URDF = os.path.join(_HERE, "pinocchio_baseline", "panda.urdf")

ARM_JOINT_NAMES = [f"panda_joint{i}" for i in range(1, 8)]
EE_LINK_NAME = "panda_hand"

# ---------------------------------------------------------------------------
# Joint limits (URDF <limit>) -- identical to the Isaac generator
# ---------------------------------------------------------------------------
Q_LOWER = np.array([-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973])
Q_UPPER = np.array([ 2.8973,  1.7628,  2.8973, -0.0698,  2.8973,  3.7525,  2.8973])
VEL_LIMITS = np.array([2.175, 2.175, 2.175, 2.175, 2.610, 2.610, 2.610])

# ---------------------------------------------------------------------------
# Generation parameters
#
# N_SEGMENTS is deliberately much larger than the Isaac generator's 10. The
# 2026-08-03 group-wise split showed that 30 trajectories is far too few: best
# validation loss landed at EPOCH 1 for both learned models and rose
# monotonically afterwards, so the selected checkpoint was barely trained and
# tau_pred collapsed onto RNEA. 148k rows looked like a lot of data; 30
# trajectories is the number that actually mattered.
#
# mj_inverse costs microseconds per sample and needs no rollout, so trajectory
# diversity here is nearly free -- there is no reason to inherit that limit.
# ---------------------------------------------------------------------------
N_SEGMENTS = 50            # trajectories per payload (Isaac generator: 10)
N_PER_SEGMENT = 2_000      # 2 s at 1 kHz
N_HARMONICS = 5
SIM_DT = 1.0 / 1_000.0
RANDOM_SEED = 42

# Velocity guard. The Fourier parametrisation below can in principle exceed the
# Panda's rated joint velocity; samples above this fraction of the limit are
# dropped rather than clipped, because clipping qdot would desynchronise it from
# the q and qddot of the same analytical curve and corrupt the RNEA comparison.
VEL_SAFETY = 0.95


# ===========================================================================
# Excitation: Sobol centres + Fourier segments
# Identical design to generate_isaac_dataset.py so the two datasets stay
# comparable; only the segment COUNT differs.
# ===========================================================================

def _sobol_q_centers(n: int, seed: int) -> np.ndarray:
    """Return n joint configurations via Sobol low-discrepancy sampling."""
    if _HAS_SCIPY:
        raw = _qmc.Sobol(d=N_JOINTS, scramble=True, seed=seed).random(n)
        print(f"  [N1-WangCAC] Sobol sampling  seed={seed}  n={n}")
    else:
        raw = np.random.default_rng(seed).uniform(size=(n, N_JOINTS))
        print("  [N1-WangCAC] scipy not found -- uniform fallback")
    return Q_LOWER + raw * (Q_UPPER - Q_LOWER)


def _fourier_segment(q_center: np.ndarray, n_steps: int, dt: float,
                     rng: np.random.Generator):
    """One Fourier excitation segment around q_center.

    Returns (q, qdot, qddot), each (n_steps, 7) float64. qddot is the analytical
    second derivative of the same curve, so the triple is exactly consistent --
    which is what makes the RNEA comparison meaningful.
    """
    t = np.arange(n_steps) * dt
    A = rng.uniform(0.05, 0.30, (N_HARMONICS, N_JOINTS))
    wn = rng.uniform(0.50, 3.00, (N_HARMONICS, N_JOINTS))
    ph = rng.uniform(0.00, 2.0 * np.pi, (N_HARMONICS, N_JOINTS))

    q = q_center + sum(
        A[k] * np.sin(np.outer(t, wn[k]) + ph[k]) for k in range(N_HARMONICS)
    )
    qdot = sum(
        A[k] * wn[k] * np.cos(np.outer(t, wn[k]) + ph[k]) for k in range(N_HARMONICS)
    )
    qddot = sum(
        -A[k] * wn[k] ** 2 * np.sin(np.outer(t, wn[k]) + ph[k])
        for k in range(N_HARMONICS)
    )

    # Clip POSITION into the joint range. Note this does desynchronise q from
    # qdot/qddot on any clipped row; such rows are dropped below rather than
    # kept, for the same reason the velocity guard drops instead of clipping.
    q_clipped = np.clip(q, Q_LOWER + 0.05, Q_UPPER - 0.05)
    clipped_row = np.any(np.abs(q_clipped - q) > 1e-12, axis=1)

    return q_clipped, qdot, qddot, clipped_row


# ===========================================================================
# MuJoCo: the deployment-domain ground truth
# ===========================================================================

def _load_mujoco(mjcf_path: str, payload_kg: float):
    """Load the live MJCF, inject the payload, and disable contacts.

    Returns (model, data, qpos_adr, dof_adr) where the two address arrays map
    arm joint i -> its scalar qpos / qvel index.
    """
    if not os.path.isfile(mjcf_path):
        sys.exit(f"ERROR: MJCF not found: {mjcf_path}")

    model = mujoco.MjModel.from_xml_path(mjcf_path)
    data = mujoco.MjData(model)

    # --- address lookup, by NAME (never by index) ---------------------------
    qpos_adr = np.empty(N_JOINTS, dtype=int)
    dof_adr = np.empty(N_JOINTS, dtype=int)
    for i, name in enumerate(ARM_JOINT_NAMES):
        jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
        if jid < 0:
            sys.exit(f"ERROR: joint {name!r} not in {mjcf_path}")
        qpos_adr[i] = model.jnt_qposadr[jid]
        dof_adr[i] = model.jnt_dofadr[jid]

    # --- payload: mass only, mirroring rnea_wrapper._inject_payload ---------
    # Pinocchio's injection adds mass and leaves the rotational inertia and COM
    # untouched. MuJoCo must do exactly the same or the two disagree about the
    # payload and the residual is handed a discrepancy that is an artefact of
    # this script rather than a property of the simulator.
    if payload_kg > 0.0:
        bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, EE_LINK_NAME)
        if bid < 0:
            sys.exit(f"ERROR: body {EE_LINK_NAME!r} not in {mjcf_path}")
        prev = float(model.body_mass[bid])
        model.body_mass[bid] = prev + payload_kg
        # body_mass feeds derived constants (subtree masses); recompute them.
        mujoco.mj_setConst(model, data)
        print(f"  [mujoco]    payload +{payload_kg} kg on {EE_LINK_NAME} "
              f"(was {prev:.3f} kg)")

    # --- contacts off -------------------------------------------------------
    # The scene contains a floor plane and a free-floating grasp_object. With
    # contacts enabled, qfrc_constraint leaks into qfrc_inverse and the residual
    # would be asked to explain forces RNEA cannot see.
    model.opt.disableflags |= mujoco.mjtDisableBit.mjDSBL_CONTACT

    # --- actuation off ------------------------------------------------------
    # mj_inverse ignores actuators entirely: it returns the total generalised
    # force required, with no opinion about which actuator supplies it. The
    # forward round-trip check must therefore see zero actuator force too, or it
    # compares two different systems.
    #
    # This matters concretely rather than theoretically. The finger actuator
    # (MJCF line 489) is a <position> servo with kp=200, so ctrl=0 does NOT mean
    # zero force -- it means "drive the finger to 0", which at the home keyframe
    # width of 0.04 m is about -8 N pushing on the hand. Left enabled, that force
    # would appear in forward dynamics but not in the inverse pass, and the
    # round-trip check would fail for a reason that has nothing to do with the
    # data being wrong.
    model.opt.disableflags |= mujoco.mjtDisableBit.mjDSBL_ACTUATION

    print("  [mujoco]    contacts and actuation DISABLED "
          "(free-space rigid-body dynamics only)")

    return model, data, qpos_adr, dof_adr


def _mujoco_inverse_batch(model, data, qpos_adr, dof_adr,
                          q: np.ndarray, qdot: np.ndarray, qddot: np.ndarray):
    """tau_real via mj_inverse, one row at a time.

    For each sample the full state is reset from the `home` keyframe first, so
    the fingers and the free-floating cube always hold valid values (a freejoint
    needs a normalised quaternion; leaving qpos at whatever the previous row set
    would be both invalid and a hidden coupling between samples). Only the seven
    arm entries are then overwritten.
    """
    n = q.shape[0]
    tau = np.empty((n, N_JOINTS), dtype=np.float64)

    key_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, "home")

    for i in range(n):
        if key_id >= 0:
            mujoco.mj_resetDataKeyframe(model, data, key_id)
        else:
            mujoco.mj_resetData(model, data)

        # Everything not driven by us is held still: a nonzero cube velocity or
        # acceleration would be irrelevant to the arm's rows but makes the
        # round-trip self-check below harder to read.
        data.qvel[:] = 0.0
        data.qacc[:] = 0.0

        data.qpos[qpos_adr] = q[i]
        data.qvel[dof_adr] = qdot[i]
        data.qacc[dof_adr] = qddot[i]

        mujoco.mj_inverse(model, data)
        tau[i] = data.qfrc_inverse[dof_adr]

    return tau


def _selfcheck_roundtrip(model, data, qpos_adr, dof_adr,
                         q: np.ndarray, qdot: np.ndarray, qddot: np.ndarray,
                         n_check: int = 64) -> None:
    """Verify mj_inverse against forward dynamics, and FAIL LOUDLY if it drifts.

    This is the check the project's own hard-won lesson demands -- it is written
    so that it CAN fail. Feeding qfrc_inverse back in as qfrc_applied must
    reproduce the acceleration that produced it. If the sign convention, the
    address mapping, or the contact/passive/actuation accounting were wrong,
    this diverges immediately, whereas printing "tau computed OK" would pass no
    matter what was in the array.

    The round trip is done on the FULL generalised-force vector, not just the
    seven arm columns. The hand and fingers sit in the same kinematic tree as
    the arm, so they are coupled through the mass matrix: applying only the arm
    torques would let the fingers accelerate freely, the coupling would change,
    and the arm's acceleration would not come back exact. Applying the whole
    vector reproduces the whole commanded state -- arm at qddot, everything else
    held at zero -- which is the condition the data was actually generated under.
    """
    rng = np.random.default_rng(0)
    idx = rng.choice(q.shape[0], size=min(n_check, q.shape[0]), replace=False)
    key_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, "home")

    worst_arm = 0.0
    worst_all = 0.0
    for i in idx:
        # --- inverse pass: rebuild the exact state, keep the FULL force -----
        if key_id >= 0:
            mujoco.mj_resetDataKeyframe(model, data, key_id)
        else:
            mujoco.mj_resetData(model, data)
        data.qvel[:] = 0.0
        data.qacc[:] = 0.0
        data.qpos[qpos_adr] = q[i]
        data.qvel[dof_adr] = qdot[i]
        data.qacc[dof_adr] = qddot[i]

        qpos_ref = data.qpos.copy()
        qvel_ref = data.qvel.copy()
        qacc_ref = data.qacc.copy()

        mujoco.mj_inverse(model, data)
        qfrc_full = data.qfrc_inverse.copy()

        # --- forward pass: does that force reproduce that acceleration? -----
        data.qpos[:] = qpos_ref
        data.qvel[:] = qvel_ref
        data.qacc[:] = 0.0
        data.qfrc_applied[:] = qfrc_full
        data.ctrl[:] = 0.0

        mujoco.mj_forward(model, data)

        err_all = np.abs(data.qacc - qacc_ref)
        worst_all = max(worst_all, float(np.max(err_all)))
        worst_arm = max(worst_arm, float(np.max(err_all[dof_adr])))

    print(f"  [selfcheck] inverse->forward round trip on {len(idx)} samples:")
    print(f"                max |qacc err| over the 7 arm joints = {worst_arm:.3e} rad/s^2")
    print(f"                max |qacc err| over all {model.nv} DOFs      = {worst_all:.3e}")

    tol = 1e-6
    if not np.isfinite(worst_all) or worst_all > tol:
        sys.exit(
            f"ERROR: the round trip did NOT close (max error {worst_all:.3e} > {tol:.0e}).\n"
            "       qfrc_inverse does not reproduce the commanded acceleration, so\n"
            "       tau_real is NOT the torque the motors would have to supply and\n"
            "       the residual would be fitted to a quantity with no physical\n"
            "       meaning. DO NOT TRAIN ON THIS DATA.\n"
            "       Check, in order: the qpos/dof address mapping; that contacts\n"
            "       AND actuation are actually disabled (the finger <position>\n"
            "       servo applies force at ctrl=0); and that no keyframe writes a\n"
            "       nonzero qvel that is not being cleared."
        )


# ===========================================================================
# Pinocchio RNEA -- the white-box term, unchanged and never modified
# ===========================================================================

def _load_pin_model(urdf_path: str, payload_kg: float):
    full_model = pin.buildModelFromUrdf(urdf_path)

    # panda.urdf carries 7 revolute arm joints + 2 prismatic finger joints
    # (nq=9). The fingers are held at 0 throughout collection, so lock them to
    # reduce nq -> 7 and line the model up with the 7-column arrays.
    finger_joints = ["panda_finger_joint1", "panda_finger_joint2"]
    joints_to_lock = [full_model.getJointId(j) for j in finger_joints]
    model = pin.buildReducedModel(full_model, joints_to_lock, pin.neutral(full_model))
    data = model.createData()

    if payload_kg > 0.0:
        ee_id = model.getFrameId(EE_LINK_NAME)
        body_id = model.frames[ee_id].parent
        inertia = model.inertias[body_id]
        inertia.mass += payload_kg
        model.inertias[body_id] = inertia
        print(f"  [pinocchio] payload +{payload_kg} kg on {EE_LINK_NAME}")

    return model, data


def _rnea_batch(model, data, q, qdot, qddot) -> np.ndarray:
    n = q.shape[0]
    tau = np.empty((n, N_JOINTS), dtype=np.float64)
    for i in range(n):
        tau[i] = pin.rnea(model, data,
                          q[i].astype(np.float64),
                          qdot[i].astype(np.float64),
                          qddot[i].astype(np.float64))
    return tau


# ===========================================================================
# Driver
# ===========================================================================

def generate_and_save(payload_kg: float, out_dir: str, mjcf_path: str,
                      urdf_path: str, n_segments: int, n_per_segment: int,
                      seed: int) -> str:
    print("=" * 70)
    print(f"  MuJoCo in-domain dataset  --  payload {payload_kg} kg  --  seed {seed}")
    print("=" * 70)

    model, data, qpos_adr, dof_adr = _load_mujoco(mjcf_path, payload_kg)
    pin_model, pin_data = _load_pin_model(urdf_path, payload_kg)

    if pin_model.nq != N_JOINTS:
        sys.exit(f"ERROR: reduced pinocchio model has nq={pin_model.nq}, expected {N_JOINTS}")

    centers = _sobol_q_centers(n_segments, seed=seed + int(payload_kg * 100))
    rng = np.random.default_rng(seed + int(payload_kg * 1000))

    all_q, all_qd, all_qdd, all_seg = [], [], [], []
    n_dropped_clip = n_dropped_vel = 0

    for s in range(n_segments):
        q, qd, qdd, clipped = _fourier_segment(centers[s], n_per_segment, SIM_DT, rng)

        too_fast = np.any(np.abs(qd) > VEL_SAFETY * VEL_LIMITS, axis=1)
        drop = clipped | too_fast
        n_dropped_clip += int(np.sum(clipped))
        n_dropped_vel += int(np.sum(too_fast & ~clipped))

        keep = ~drop
        if not np.any(keep):
            print(f"    seg {s+1:3d}/{n_segments}  ALL rows dropped -- skipped")
            continue

        all_q.append(q[keep])
        all_qd.append(qd[keep])
        all_qdd.append(qdd[keep])
        all_seg.append(np.full(int(np.sum(keep)), s, dtype=np.int32))

        if (s + 1) % 10 == 0 or s == 0:
            print(f"    seg {s+1:3d}/{n_segments}  kept {int(np.sum(keep)):5d}"
                  f" / {n_per_segment}")

    if not all_q:
        sys.exit("ERROR: every segment was dropped -- nothing to write.")

    q = np.concatenate(all_q).astype(np.float64)
    qdot = np.concatenate(all_qd).astype(np.float64)
    qddot = np.concatenate(all_qdd).astype(np.float64)
    seg_id = np.concatenate(all_seg)
    n = q.shape[0]

    print(f"\n  Kept {n:,} samples "
          f"({n_dropped_clip:,} dropped at a position limit, "
          f"{n_dropped_vel:,} over {VEL_SAFETY:.0%} of the velocity limit)")

    print("  Computing tau_real via mj_inverse ...")
    tau_real = _mujoco_inverse_batch(model, data, qpos_adr, dof_adr, q, qdot, qddot)

    _selfcheck_roundtrip(model, data, qpos_adr, dof_adr, q, qdot, qddot)

    print("  Computing tau_theo via Pinocchio RNEA ...")
    tau_theo = _rnea_batch(pin_model, pin_data, q, qdot, qddot)

    tau_res = tau_real - tau_theo

    # --- report, do not filter ---------------------------------------------
    # No saturation filter here: mj_inverse involves no actuator, so nothing can
    # clamp. A sample whose required torque exceeds the motor limit is still
    # perfectly valid DYNAMICS -- it just is not reachable on hardware. It is
    # reported so the number is visible, and kept so the torque-limit constraint
    # in the augmented Lagrangian has something to act on.
    over = np.any(np.abs(tau_real) > TORQUE_LIMITS, axis=1)
    print(f"\n  tau_real over the motor limit on {int(np.sum(over)):,} / {n:,} "
          f"samples ({100.0 * np.mean(over):.2f} %) -- kept, not filtered")

    rms_res = np.sqrt(np.mean(tau_res ** 2, axis=0))
    print("  Residual RMS per joint [Nm]: "
          + ", ".join(f"{v:.3f}" for v in rms_res))

    # The expected signature, given the MJCF: -damping*qdot + armature*qddot.
    pred = -1.0 * qdot + 0.1 * qddot
    corr = np.array([
        np.corrcoef(tau_res[:, j], pred[:, j])[0, 1] for j in range(N_JOINTS)
    ])
    print("  Correlation of tau_res with (-1.0*qdot + 0.1*qddot) per joint: "
          + ", ".join(f"{c:.3f}" for c in corr))
    print("  (near 1.0 is EXPECTED and healthy -- it confirms the gap this data\n"
          "   carries is MuJoCo's declared damping and armature, nothing more.)")

    # --- write --------------------------------------------------------------
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"mujoco_{payload_kg:.1f}kg.h5")
    with h5py.File(out_path, "w") as f:
        f.create_dataset("q", data=q.astype(np.float32))
        f.create_dataset("qdot", data=qdot.astype(np.float32))
        f.create_dataset("qddot", data=qddot.astype(np.float32))
        f.create_dataset("tau_real", data=tau_real.astype(np.float32))
        f.create_dataset("tau_theo", data=tau_theo.astype(np.float32))
        f.create_dataset("tau_res", data=tau_res.astype(np.float32))
        f.create_dataset("delta", data=np.full(n, payload_kg, dtype=np.float32))
        # Explicit boundaries: segment_splits.py can use these directly rather
        # than recovering them from the largest jumps in ||q[i+1] - q[i]||.
        f.create_dataset("segment_id", data=seg_id)

        f.attrs["source"] = "mujoco_inverse_dynamics"
        f.attrs["mjcf"] = os.path.relpath(mjcf_path, _HERE)
        f.attrs["urdf"] = os.path.relpath(urdf_path, _HERE)
        f.attrs["payload_kg"] = payload_kg
        f.attrs["n_segments"] = n_segments
        f.attrs["n_per_segment"] = n_per_segment
        f.attrs["sim_dt"] = SIM_DT
        f.attrs["seed"] = seed
        f.attrs["contacts_disabled"] = True

    print(f"\n  Wrote {out_path}  ({n:,} samples, {n_segments} segments)")
    return out_path


def main() -> None:
    p = argparse.ArgumentParser(
        description="Generate Stage 1 training data from the deployed MuJoCo model."
    )
    p.add_argument("--payload", type=float, default=0.0,
                   help="End-effector payload [kg] (default: 0.0)")
    p.add_argument("--out_dir", type=str, default=os.path.join(_HERE, "data"))
    p.add_argument("--mjcf", type=str, default=DEFAULT_MJCF,
                   help="MJCF to source ground truth from (default: the live one)")
    p.add_argument("--urdf", type=str, default=DEFAULT_URDF)
    p.add_argument("--n_segments", type=int, default=N_SEGMENTS)
    p.add_argument("--n_per_segment", type=int, default=N_PER_SEGMENT)
    p.add_argument("--seed", type=int, default=RANDOM_SEED)
    args = p.parse_args()

    generate_and_save(
        payload_kg=args.payload,
        out_dir=args.out_dir,
        mjcf_path=args.mjcf,
        urdf_path=args.urdf,
        n_segments=args.n_segments,
        n_per_segment=args.n_per_segment,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
