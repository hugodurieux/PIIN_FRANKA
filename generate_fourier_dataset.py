#!/usr/bin/env python3
"""
Fourier-series excitation trajectory dataset generator for Franka Panda PINN.

Generates one HDF5 file per payload using bandlimited Fourier trajectories that
excite all 7 arm DOF within the Franka Panda joint and torque limits.

tau_real = tau_theo + tau_res
  tau_theo   -- RNEA(model, q, qdot, qddot) via Pinocchio
  tau_res    -- synthetic friction residual: -COULOMB*sign(qdot) - VISCOUS*qdot
                (mirrors SyntheticDataset in training/dataset.py so the training
                 pipeline can run end-to-end before real data is available)

Usage (run from WSL in the project root):
    python3 generate_fourier_dataset.py

Prerequisites:
    pip3 install pinocchio h5py numpy
    pip3 install example_robot_data   # strongly recommended — provides correct inertials

Outputs (created in data/ under the project root):
    data/fourier_baseline_0kg.h5
    data/fourier_baseline_1kg.h5
    data/fourier_baseline_3kg.h5

Random seed: 42  (logged in every HDF5 /metadata group for reproducibility).
"""

import os
import sys
import time
import numpy as np
import h5py

# ---------------------------------------------------------------------------
# Paths — derived from the location of this script, so they work whether the
# script is run from the project root or from any directory.
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
URDF_PATH    = os.path.join(PROJECT_ROOT, "pinocchio_baseline", "panda.urdf")
DATA_DIR     = os.path.join(PROJECT_ROOT, "data")

# ---------------------------------------------------------------------------
# Franka Panda physical constants
# ---------------------------------------------------------------------------
N_JOINTS = 7

# Joint position limits [rad] — extracted from panda.urdf <limit lower=... upper=...>
# Joint 4 and Joint 6 are asymmetric; q_center is computed as (lower+upper)/2 below.
Q_LOWER = np.array([-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973])
Q_UPPER = np.array([ 2.8973,  1.7628,  2.8973, -0.0698,  2.8973,  3.7525,  2.8973])

# Max joint velocities [rad/s]  (from panda.urdf <limit velocity=...>)
VEL_LIMITS = np.array([2.175, 2.175, 2.175, 2.175, 2.610, 2.610, 2.610])

# Absolute torque limits [Nm]  (from network/constants.py TORQUE_LIMITS)
TORQUE_LIMITS = np.array([87.0, 87.0, 87.0, 87.0, 12.0, 12.0, 12.0])

# ---------------------------------------------------------------------------
# Generation parameters
# ---------------------------------------------------------------------------
FREQ_HZ     = 1000      # Sampling rate [Hz]
N_SAMPLES   = 50_000    # Timesteps per payload (50 s).  Set to 600_000 for the
                        # full 10-min recording; 50k keeps memory under ~120 MB.
N_HARMONICS = 5         # Fourier harmonics per joint (k = 1 … N_HARMONICS)
N_SEGMENTS  = 10        # [N1-WangCAC] Sobol segments per payload
N_SAMPLES_PER_SEG = N_SAMPLES // N_SEGMENTS  # 5 000 samples per segment
FREQ_MIN    = 0.1       # Minimum harmonic frequency [Hz]
FREQ_MAX    = 2.0       # Maximum harmonic frequency [Hz]
VEL_SAFETY  = 0.80      # Target: peak |qdot| <= VEL_SAFETY * VEL_LIMITS
POS_SAFETY  = 0.90      # Target: |A_k| <= POS_SAFETY * half_range / N_HARMONICS
RANDOM_SEED = 42
PAYLOADS    = [0.0, 1.0, 3.0]  # [kg] — from network/constants.py PAYLOADS

# Synthetic residual coefficients (matches SyntheticDataset in training/dataset.py)
COULOMB = 1.5   # Coulomb friction [Nm]
VISCOUS = 0.8   # Viscous friction [Nm·s/rad]

# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_model():
    """
    Load the Pinocchio model.  Two attempts, in order:

    1. example_robot_data.load("panda") — ships the complete Panda URDF with
       all link inertias; strongly preferred because RNEA needs real mass data.

    2. Local pinocchio_baseline/panda.urdf — the project URDF only contains
       visual/collision geometry, so model.inertias will all be zero.  RNEA
       will return near-zero tau_theo.  A prominent WARNING is printed.

    Returns
    -------
    model          : pinocchio.Model
    pinocchio_data : pinocchio.Data
    model_nq       : int   (number of configuration DOFs; may be > N_JOINTS if
                            finger joints are present)
    has_inertials  : bool  (False ⇒ tau_theo will be ≈ 0)
    """
    import pinocchio as pin

    # --- attempt 1: cmeel-installed example-robot-data URDF (pip install example_robot_data) ---
    import glob, site
    _cmeel_candidates = []
    for sp in site.getsitepackages() + [site.getusersitepackages()]:
        _cmeel_candidates += glob.glob(
            os.path.join(sp, "cmeel.prefix", "share", "example-robot-data",
                         "robots", "panda_description", "urdf", "panda.urdf")
        )
    if _cmeel_candidates:
        _erd_urdf = _cmeel_candidates[0]
        model = pin.buildModelFromUrdf(_erd_urdf)
        pinocchio_data = model.createData()
        total_mass = sum(model.inertias[i].mass for i in range(1, model.njoints))
        has_inertials = total_mass > 1.0
        print(f"[model] cmeel example-robot-data: nq={model.nq}, nv={model.nv}, "
              f"total_mass={total_mass:.3f} kg, has_inertials={has_inertials}")
        return model, pinocchio_data, model.nq, has_inertials

    # --- attempt 2: example_robot_data Python API (alternative install) ---
    try:
        import example_robot_data as erd
        robot = erd.load("panda")
        model = robot.model
        pinocchio_data = model.createData()
        total_mass = sum(model.inertias[i].mass for i in range(1, model.njoints))
        has_inertials = total_mass > 1.0
        print(f"[model] example_robot_data: nq={model.nq}, nv={model.nv}, "
              f"total_mass={total_mass:.3f} kg, has_inertials={has_inertials}")
        return model, pinocchio_data, model.nq, has_inertials
    except Exception as exc:
        print(f"[model] example_robot_data API not available ({exc}); "
              f"falling back to local panda.urdf")

    # --- attempt 2: local URDF ---
    if not os.path.isfile(URDF_PATH):
        print(f"ERROR: URDF not found at {URDF_PATH}")
        sys.exit(1)

    # Pinocchio only needs the <inertial> / <joint> sections for dynamics;
    # mesh files referenced in <visual>/<collision> do not need to be present.
    model = pin.buildModelFromUrdf(URDF_PATH)
    pinocchio_data = model.createData()
    total_mass = sum(model.inertias[i].mass for i in range(1, model.njoints))
    has_inertials = total_mass > 1.0

    if not has_inertials:
        print(
            "\n" + "!" * 70 + "\n"
            "WARNING: panda.urdf has no <inertial> sections "
            f"(total_mass={total_mass:.4f} kg).\n"
            "         RNEA will return near-zero tau_theo values.\n"
            "         Install example_robot_data for correct results:\n"
            "             pip3 install example_robot_data\n"
            "!" * 70 + "\n"
        )
    else:
        print(f"[model] Local URDF: nq={model.nq}, nv={model.nv}, "
              f"total_mass={total_mass:.3f} kg")

    return model, pinocchio_data, model.nq, has_inertials


# ---------------------------------------------------------------------------
# Payload injection
# ---------------------------------------------------------------------------

def get_ee_joint_id(model):
    """
    Return the Pinocchio joint ID of the link on which payload mass is added.

    Tries frame names in order: panda_hand, panda_link8, panda_ee, panda_link7.
    Falls back to joint N_JOINTS (the 7th arm joint, 1-indexed in Pinocchio).
    """
    for frame_name in ["panda_hand", "panda_link8", "panda_ee", "panda_link7"]:
        if model.existFrame(frame_name):
            fid = model.getFrameId(frame_name)
            jid = model.frames[fid].parent
            if jid > 0:  # exclude the universe joint
                return jid
    # Conservative fallback: last arm joint (ID = N_JOINTS in 1-indexed scheme)
    return min(N_JOINTS, model.njoints - 1)


# ---------------------------------------------------------------------------
# Fourier trajectory
# ---------------------------------------------------------------------------

def sobol_q_centers(n_segments, seed):
    """
    [N1-WangCAC] Sample n_segments joint-space centres using Sobol low-discrepancy
    sequences (scipy.stats.qmc.Sobol). Falls back to uniform random if scipy is
    unavailable. Sobol fills the 7-D joint space more evenly than pseudo-random,
    ensuring trajectory segments visit diverse regions of configuration space.
    """
    try:
        import math
        from scipy.stats.qmc import Sobol
        n_pow2 = 2 ** math.ceil(math.log2(max(n_segments, 2)))
        sampler = Sobol(d=N_JOINTS, scramble=True, seed=seed)
        unit = sampler.random(n_pow2)[:n_segments]          # (n_segments, 7) in [0,1]
        centers = Q_LOWER + unit * (Q_UPPER - Q_LOWER)
        print(f"  [N1-WangCAC] Sobol q_centers: {n_segments} segments "
              f"(scipy.stats.qmc.Sobol, seed={seed})")
        return centers
    except ImportError:
        print("  [N1-WangCAC] scipy not found — falling back to uniform q_centers")
        rng_s = np.random.default_rng(seed)
        unit  = rng_s.uniform(0, 1, size=(n_segments, N_JOINTS))
        return Q_LOWER + unit * (Q_UPPER - Q_LOWER)


def sample_fourier_params(rng, q_center):
    """
    Draw random Fourier parameters for a trajectory centred at q_center.

    Amplitude bounds (conservative, per-harmonic):
      Position: |A_k| <= POS_SAFETY * half_range[j] / N_HARMONICS
                where half_range[j] = min(q_center[j]-Q_LOWER[j], Q_UPPER[j]-q_center[j])
      Velocity: |A_k * omega_k| <= VEL_SAFETY * VEL_LIMITS[j] / N_HARMONICS
                => |A_k| <= VEL_SAFETY * VEL_LIMITS[j] / (N_HARMONICS * omega_k)

    The tighter of the two bounds is applied.

    Returns
    -------
    amplitudes  (7, N_HARMONICS)      — per-harmonic amplitude [rad]
    frequencies (7, N_HARMONICS)      — per-harmonic frequency [Hz]
    phases      (7, N_HARMONICS)      — per-harmonic phase [rad]
    """
    half_range = np.minimum(q_center - Q_LOWER, Q_UPPER - q_center)

    frequencies = rng.uniform(FREQ_MIN, FREQ_MAX, size=(N_JOINTS, N_HARMONICS))
    phases      = rng.uniform(0.0, 2.0 * np.pi, size=(N_JOINTS, N_HARMONICS))
    amplitudes  = np.zeros((N_JOINTS, N_HARMONICS))

    for j in range(N_JOINTS):
        for k in range(N_HARMONICS):
            omega_k = 2.0 * np.pi * frequencies[j, k]
            pos_amp = POS_SAFETY * half_range[j] / N_HARMONICS
            vel_amp = VEL_SAFETY * VEL_LIMITS[j] / (N_HARMONICS * omega_k)
            amplitudes[j, k] = min(pos_amp, vel_amp)

    return amplitudes, frequencies, phases


def fourier_trajectory(t, q_center, amplitudes, frequencies, phases):
    """
    Evaluate position, velocity, and acceleration at each timestep.

    q(t)     = q_center + sum_k  A_k * sin(omega_k*t + phi_k)
    qdot(t)  =            sum_k  A_k * omega_k * cos(omega_k*t + phi_k)
    qddot(t) =            sum_k -A_k * omega_k^2 * sin(omega_k*t + phi_k)

    Parameters
    ----------
    t          : (N,)  time axis [s]
    q_center   : (7,)  trajectory centre [rad]
    amplitudes : (7, N_HARMONICS)
    frequencies: (7, N_HARMONICS) [Hz]
    phases     : (7, N_HARMONICS) [rad]

    Returns
    -------
    q, qdot, qddot : each (N, 7) float64
    """
    N = len(t)
    q     = np.tile(q_center, (N, 1)).copy()
    qdot  = np.zeros((N, N_JOINTS), dtype=np.float64)
    qddot = np.zeros((N, N_JOINTS), dtype=np.float64)

    for j in range(N_JOINTS):
        for k in range(N_HARMONICS):
            omega = 2.0 * np.pi * frequencies[j, k]
            angle = omega * t + phases[j, k]
            A     = amplitudes[j, k]
            q[:, j]     +=  A             * np.sin(angle)
            qdot[:, j]  +=  A * omega     * np.cos(angle)
            qddot[:, j] += -A * omega**2  * np.sin(angle)

    return q, qdot, qddot


def validate_trajectory(q, qdot, qddot):
    """
    Print per-joint trajectory diagnostics and return True if all limits are met.
    """
    header = (f"  {'J':>3}  {'q_min':>8} {'q_max':>8} "
              f"{'q_lo_lim':>10} {'q_hi_lim':>10}  "
              f"{'v_peak':>8} {'v_lim':>6}  {'a_peak':>8}  status")
    print(header)
    all_ok = True
    for j in range(N_JOINTS):
        q_min  = q[:, j].min()
        q_max  = q[:, j].max()
        v_peak = np.abs(qdot[:, j]).max()
        a_peak = np.abs(qddot[:, j]).max()
        pos_ok = (Q_LOWER[j] <= q_min) and (q_max <= Q_UPPER[j])
        vel_ok = v_peak <= VEL_LIMITS[j]
        ok = pos_ok and vel_ok
        if not ok:
            all_ok = False
        status = "OK" if ok else "WARN"
        print(f"  J{j+1}  {q_min:8.4f} {q_max:8.4f} "
              f"{Q_LOWER[j]:10.4f} {Q_UPPER[j]:10.4f}  "
              f"{v_peak:8.4f} {VEL_LIMITS[j]:6.3f}  {a_peak:8.4f}  {status}")
    return all_ok


# ---------------------------------------------------------------------------
# Batched RNEA
# ---------------------------------------------------------------------------

def compute_tau_theo_batch(model, pinocchio_data, q, qdot, qddot, model_nq):
    """
    Evaluate Pinocchio RNEA for each sample.

    If model_nq > N_JOINTS (model has finger DOFs), the arm state is zero-padded
    to model_nq before the call and the output is sliced to the first N_JOINTS.

    Timesteps where any |tau_i| exceeds TORQUE_LIMITS are FLAGGED (keep_mask=False)
    and excluded from the returned arrays — they are NOT silently clipped.

    Returns
    -------
    tau_theo  : (N, N_JOINTS) float64  — zeros for flagged timesteps (removed later)
    keep_mask : (N,) bool              — True = timestep is safe to keep
    """
    import pinocchio as pin

    N         = q.shape[0]
    tau_out   = np.zeros((N, N_JOINTS), dtype=np.float64)
    keep_mask = np.ones(N, dtype=bool)
    flagged   = 0
    pad       = (model_nq > N_JOINTS)  # True when finger joints are present

    for i in range(N):
        if pad:
            q_i     = np.zeros(model_nq); q_i[:N_JOINTS]     = q[i]
            qdot_i  = np.zeros(model_nq); qdot_i[:N_JOINTS]  = qdot[i]
            qddot_i = np.zeros(model_nq); qddot_i[:N_JOINTS] = qddot[i]
        else:
            q_i, qdot_i, qddot_i = q[i], qdot[i], qddot[i]

        pin.rnea(model, pinocchio_data, q_i, qdot_i, qddot_i)
        tau_i = pinocchio_data.tau[:N_JOINTS].copy()

        if np.any(np.abs(tau_i) > TORQUE_LIMITS):
            keep_mask[i] = False
            flagged += 1
        else:
            tau_out[i] = tau_i

    if flagged:
        print(f"  [safety] {flagged}/{N} timesteps flagged "
              f"(|tau| > TORQUE_LIMITS) — excluded from output.")

    return tau_out, keep_mask


# ---------------------------------------------------------------------------
# Per-payload generation and HDF5 save
# ---------------------------------------------------------------------------

def generate_and_save(payload_kg, model, pinocchio_data, model_nq,
                      has_inertials, rng):
    """
    Generate one dataset file for a given payload mass and save it to DATA_DIR.

    Steps
    -----
    1. Inject payload mass onto end-effector link.
    2. Sample Fourier parameters; build q/qdot/qddot trajectory.
    3. Validate trajectory bounds.
    4. Run RNEA batch; apply torque-limit keep_mask.
    5. Restore end-effector mass.
    6. Compute synthetic tau_res and tau_real.
    7. Save HDF5; print summary.

    Returns the path to the saved file.
    """
    out_path = os.path.join(DATA_DIR, f"fourier_baseline_{int(payload_kg)}kg.h5")

    print(f"\n{'='*68}")
    print(f"  Payload: {payload_kg} kg  →  {out_path}")
    print(f"{'='*68}")

    # 1 ── Inject payload ─────────────────────────────────────────────────────
    ee_jid = get_ee_joint_id(model)
    base_ee_mass = model.inertias[ee_jid].mass
    model.inertias[ee_jid].mass = base_ee_mass + payload_kg
    print(f"  Payload injection: joint {ee_jid}, "
          f"mass {base_ee_mass:.3f} → {model.inertias[ee_jid].mass:.3f} kg")

    # 2 ── [N1-WangCAC] Sobol segments ───────────────────────────────────────
    q_centers = sobol_q_centers(N_SEGMENTS, seed=RANDOM_SEED + int(payload_kg * 10))
    t_seg     = np.arange(N_SAMPLES_PER_SEG, dtype=np.float64) / FREQ_HZ
    seg_q, seg_qdot, seg_qddot = [], [], []
    for seg_idx, q_ctr in enumerate(q_centers):
        amp, freq, phase = sample_fourier_params(rng, q_ctr)
        qs, qds, qdds   = fourier_trajectory(t_seg, q_ctr, amp, freq, phase)
        seg_q.append(qs); seg_qdot.append(qds); seg_qddot.append(qdds)
    q     = np.concatenate(seg_q,     axis=0)
    qdot  = np.concatenate(seg_qdot,  axis=0)
    qddot = np.concatenate(seg_qddot, axis=0)
    t_global = np.concatenate([
        t_seg + seg_idx * (N_SAMPLES_PER_SEG / FREQ_HZ)
        for seg_idx in range(N_SEGMENTS)
    ])

    # 3 ── Trajectory validation ───────────────────────────────────────────────
    print("\n  Trajectory validation (before torque filtering):")
    validate_trajectory(q, qdot, qddot)

    # 4 ── RNEA ───────────────────────────────────────────────────────────────
    print(f"\n  Running RNEA on {q.shape[0]} samples "
          f"({N_SEGMENTS} segments × {N_SAMPLES_PER_SEG}, nq={model_nq}) ...")
    t_start = time.perf_counter()
    tau_theo, keep_mask = compute_tau_theo_batch(
        model, pinocchio_data, q, qdot, qddot, model_nq
    )
    elapsed = time.perf_counter() - t_start
    print(f"  RNEA completed in {elapsed:.2f} s "
          f"({q.shape[0] / elapsed:.0f} samples/s)")

    # 5 ── Restore payload ─────────────────────────────────────────────────────
    model.inertias[ee_jid].mass = base_ee_mass

    # 6 ── Apply keep_mask ─────────────────────────────────────────────────────
    q        = q[keep_mask]
    qdot     = qdot[keep_mask]
    qddot    = qddot[keep_mask]
    tau_theo = tau_theo[keep_mask]
    t_kept   = t_global[keep_mask]
    N        = q.shape[0]

    # 7 ── Synthetic residual ──────────────────────────────────────────────────
    # tau_res = -COULOMB*sign(qdot) - VISCOUS*qdot  (dissipative friction model)
    tau_res  = -COULOMB * np.sign(qdot) - VISCOUS * qdot
    tau_real = tau_theo + tau_res
    delta    = np.full(N, payload_kg, dtype=np.float64)

    # 8 ── Summary table ───────────────────────────────────────────────────────
    print(f"\n  Dataset summary  (N={N} samples kept / {len(keep_mask)} generated):")
    abs_res  = np.abs(tau_res)
    abs_theo = np.abs(tau_theo)
    hdr = (f"  {'J':>3}  {'mean|τ_res|':>12}  {'max|τ_res|':>11}  "
           f"{'mean|τ_theo|':>13}  {'max|τ_theo|':>12}  {'τ_lim':>6}")
    print(hdr)
    for j in range(N_JOINTS):
        print(f"  J{j+1}  "
              f"{abs_res[:, j].mean():12.4f}  "
              f"{abs_res[:, j].max():11.4f}  "
              f"{abs_theo[:, j].mean():13.4f}  "
              f"{abs_theo[:, j].max():12.4f}  "
              f"{TORQUE_LIMITS[j]:6.1f}")

    if not has_inertials:
        print(
            "\n  NOTE: tau_theo values above are near-zero because the URDF\n"
            "        has no <inertial> data. Install example_robot_data for\n"
            "        physically correct RNEA torques:\n"
            "            pip3 install example_robot_data"
        )

    # 9 ── Save HDF5 ───────────────────────────────────────────────────────────
    os.makedirs(DATA_DIR, exist_ok=True)

    with h5py.File(out_path, "w") as f:
        # All joint arrays: shape (N, 7), float64
        f.create_dataset("q",        data=q.astype(np.float64),        compression="gzip")
        f.create_dataset("qdot",     data=qdot.astype(np.float64),     compression="gzip")
        f.create_dataset("qddot",    data=qddot.astype(np.float64),    compression="gzip")
        f.create_dataset("tau_theo", data=tau_theo.astype(np.float64), compression="gzip")
        f.create_dataset("tau_real", data=tau_real.astype(np.float64), compression="gzip")
        f.create_dataset("tau_res",  data=tau_res.astype(np.float64),  compression="gzip")
        # Scalar arrays: shape (N,), float64
        f.create_dataset("delta",    data=delta,                        compression="gzip")
        f.create_dataset("time",     data=t_kept.astype(np.float64),   compression="gzip")
        # Metadata
        meta = f.create_group("metadata")
        meta.attrs["payload_kg"]        = float(payload_kg)
        meta.attrs["frequency_hz"]      = float(FREQ_HZ)
        meta.attrs["n_samples"]         = int(N)
        meta.attrs["fourier_harmonics"] = int(N_HARMONICS)
        meta.attrs["freq_min_hz"]       = float(FREQ_MIN)
        meta.attrs["freq_max_hz"]       = float(FREQ_MAX)
        meta.attrs["random_seed"]       = int(RANDOM_SEED)
        meta.attrs["source"]            = "fourier_baseline"
        meta.attrs["has_real_inertials"]= int(has_inertials)
        meta.attrs["coulomb_coeff"]     = float(COULOMB)
        meta.attrs["viscous_coeff"]     = float(VISCOUS)

    size_mb = os.path.getsize(out_path) / 1e6
    print(f"\n  Saved → {out_path}  ({size_mb:.1f} MB)")
    return out_path


# ---------------------------------------------------------------------------
# Verification: re-open each file and confirm key shapes
# ---------------------------------------------------------------------------

def verify_hdf5(path, payload_kg):
    """Quick sanity check: open the saved file and confirm shapes."""
    with h5py.File(path, "r") as f:
        N = f["q"].shape[0]
        checks = {
            "q":        (N, N_JOINTS),
            "qdot":     (N, N_JOINTS),
            "qddot":    (N, N_JOINTS),
            "tau_theo": (N, N_JOINTS),
            "tau_real": (N, N_JOINTS),
            "tau_res":  (N, N_JOINTS),
            "delta":    (N,),
            "time":     (N,),
        }
        all_ok = True
        for key, expected in checks.items():
            actual = tuple(f[key].shape)
            ok = (actual == expected)
            if not ok:
                all_ok = False
            tag = "OK" if ok else f"FAIL (expected {expected})"
            print(f"    {key:10s}: {str(actual):20s} {tag}")

        # Check delta value
        delta_vals = np.unique(f["delta"][:])
        delta_ok = np.allclose(delta_vals, [payload_kg], atol=1e-9)
        print(f"    {'delta_val':10s}: {delta_vals}  {'OK' if delta_ok else 'FAIL'}")

    return all_ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 68)
    print("  Franka Panda Fourier Dataset Generator")
    print("=" * 68)
    print(f"  Project root : {PROJECT_ROOT}")
    print(f"  URDF path    : {URDF_PATH}")
    print(f"  Output dir   : {DATA_DIR}")
    print(f"  Random seed  : {RANDOM_SEED}")
    print(f"  Samples/file : {N_SAMPLES}  ({N_SEGMENTS} segments × {N_SAMPLES_PER_SEG} samples)")
    print(f"  Payloads     : {PAYLOADS} kg")
    print(f"  Harmonics    : {N_HARMONICS}  freq=[{FREQ_MIN}, {FREQ_MAX}] Hz")
    print(f"  Vel safety   : {VEL_SAFETY*100:.0f}%  Pos safety: {POS_SAFETY*100:.0f}%")
    print(f"  tau_res model: -{COULOMB}·sign(qdot) - {VISCOUS}·qdot")
    print()

    # Dependency check
    missing = []
    try:
        import pinocchio as pin
        print(f"  pinocchio : {pin.__version__}")
    except ImportError:
        missing.append("pinocchio  (pip3 install pinocchio)")
    try:
        import h5py
        print(f"  h5py      : {h5py.__version__}")
    except ImportError:
        missing.append("h5py  (pip3 install h5py)")
    try:
        print(f"  numpy     : {np.__version__}")
    except Exception:
        missing.append("numpy  (pip3 install numpy)")

    if missing:
        print("\nERROR — missing dependencies:")
        for m in missing:
            print(f"  pip3 install {m}")
        sys.exit(1)

    print()

    # Load model (once, reused for all payloads)
    model, pinocchio_data, model_nq, has_inertials = load_model()

    # Single RNG shared across payloads: each payload draws different Fourier
    # parameters from successive draws, so all three trajectories differ.
    rng = np.random.default_rng(seed=RANDOM_SEED)

    saved_files = []
    for payload_kg in PAYLOADS:
        path = generate_and_save(
            payload_kg, model, pinocchio_data, model_nq, has_inertials, rng
        )
        saved_files.append((path, payload_kg))

    # Summary + verification
    print(f"\n{'='*68}")
    print("  Verification (re-reading saved files):")
    all_verified = True
    for path, payload_kg in saved_files:
        print(f"\n  {os.path.basename(path)}")
        ok = verify_hdf5(path, payload_kg)
        if not ok:
            all_verified = False

    print(f"\n{'='*68}")
    if all_verified:
        print("  All files verified OK.")
    else:
        print("  Some files have unexpected shapes — check output above.")
    print()
    print("  Usage in training:")
    print("    python -m training.train \\")
    print(f"        --data {os.path.join(DATA_DIR, 'fourier_baseline_0kg.h5')} \\")
    print("        --epochs 200")
    print()
    print("  Or multi-payload (concatenate manually or adapt dataset.py):")
    for path, _ in saved_files:
        print(f"    {path}")
    print()


if __name__ == "__main__":
    main()
