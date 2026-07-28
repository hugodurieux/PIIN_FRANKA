"""
Stage 4 diagnostic (2026-07-28) -- standalone MuJoCo internals inspector for
the panda_joint4/6/7 immobility investigation.

WHY THIS EXISTS: every diagnostic so far (ROS2/MoveIt2 bypass, disable_residual
ablation, isolated raw-torque tests via /panda_effort_controller/commands) can
only observe /joint_states -- position, velocity, and a reaction "effort"
value whose exact meaning (commanded vs sensed) was never fully pinned down.
None of them can see what MuJoCo's own constraint solver is actually doing:
which contacts are active, how much force each is exerting, and how the
commanded torque splits into qfrc_bias (gravity/Coriolis/centrifugal),
qfrc_passive (damping/friction/springs), and qfrc_constraint (everything the
solver added to enforce contacts, equality constraints, and joint limits).
This script goes around ROS2 and mujoco_ros2_control ENTIRELY: it loads an
MJCF directly with the raw `mujoco` Python package, applies a constant torque
to exactly one joint (everything else 0, matching the project's existing
ros2_ws/test_jointN_raw_torque.sh pattern), steps physics itself, and prints
the full internal breakdown every N steps.

Requires the `mujoco` Python package (NOT the ROS2 mujoco_ros2_control
plugin -- a separate, standalone pip package):
    pip install mujoco

Usage (against THIS project's own modified MJCF -- the actual live scene):
    python3 stage4/debug_mujoco_internals.py \\
        --model ros2_ws/src/pinn_franka_controller/mujoco/franka_emika_panda/panda_arm_mujoco.xml \\
        --joint panda_joint4 --torque 40 --duration 5

Usage (against the STOCK, unmodified upstream comparison file -- see
panda_raw_torque_test.xml, a copy of mujoco_menagerie's panda.xml with its
stock <general> position-servo actuators swapped for plain <motor> raw-torque
actuators matching this project's own convention, nothing else touched):
    python3 stage4/debug_mujoco_internals.py \\
        --model /tmp/.../mujoco_menagerie_reference/franka_emika_panda/panda_raw_torque_test.xml \\
        --joint joint4 --torque 40 --duration 5

Comparing the two runs answers Path D directly: if the STOCK file also shows
joint4 not responding to 40 Nm, the cause is upstream of this project's own
modifications (plugin, MuJoCo version, or something inherent to this exact
kinematic/inertial tree). If the stock file moves normally, the cause is
somewhere in this project's own modifications despite every static-file
comparison so far (actuator gear/ctrlrange, joint armature/damping,
equality constraints, contact excludes) coming back identical.

This script NEVER touches MoveIt2, Stage 3, the trained model, or any ROS2
topic -- it is a pure physics-engine-level test, one level below every other
diagnostic built this session.
"""

from __future__ import annotations

import argparse
import sys

try:
    import mujoco
    import numpy as np
except ImportError:
    print(
        "ERROR: the 'mujoco' Python package is not installed.\n"
        "Install it with:  pip install mujoco\n"
        "(This is the standalone MuJoCo Python package, unrelated to the "
        "ROS2 mujoco_ros2_control plugin already used elsewhere in this "
        "project -- it lets this script load an MJCF and step physics "
        "directly, with no ROS2 involved at all.)",
        file=sys.stderr,
    )
    sys.exit(1)


def _find_actuator_for_joint(model: "mujoco.MjModel", joint_name: str) -> int:
    """Return the actuator id whose transmission target is `joint_name`.

    Raises ValueError if no actuator drives that joint (nothing to command)
    or the joint name doesn't exist at all -- both are configuration
    mistakes the caller should fix, not silently ignore.
    """
    joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, joint_name)
    if joint_id < 0:
        raise ValueError(
            f"Joint {joint_name!r} not found in this model. Available joints: "
            f"{[mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i) for i in range(model.njnt)]}"
        )
    for act_id in range(model.nu):
        # trnid[0] holds the target joint id for jnt-type transmissions
        # (mjTRN_JOINT), which is what every actuator in both MJCFs this
        # script targets uses (<motor joint="..."/> and <general joint="..."/>).
        if model.actuator_trntype[act_id] == mujoco.mjtTrn.mjTRN_JOINT and model.actuator_trnid[act_id, 0] == joint_id:
            return act_id
    raise ValueError(
        f"No actuator drives joint {joint_name!r} -- nothing to command. "
        f"Check the MJCF's <actuator> section."
    )


def _contact_summary(model: "mujoco.MjModel", data: "mujoco.MjData") -> list[str]:
    """Return a human-readable line per active contact, including the
    normal force magnitude (via mj_contactForce, which accounts for the
    solver's actual constraint impulse -- not just geometric penetration)."""
    lines = []
    for i in range(data.ncon):
        con = data.contact[i]
        geom1 = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, con.geom1) or f"geom{con.geom1}"
        geom2 = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, con.geom2) or f"geom{con.geom2}"
        force6 = np.zeros(6, dtype=np.float64)
        mujoco.mj_contactForce(model, data, i, force6)
        normal_force = force6[0]  # force6[0] = normal component in the contact frame
        lines.append(
            f"    contact[{i}]: {geom1} <-> {geom2}, dist={con.dist:+.5f} m, "
            f"normal_force={normal_force:+.3f} N"
        )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True, help="Path to the MJCF file to load.")
    parser.add_argument("--joint", required=True, help="Name of the single joint to torque (e.g. panda_joint4 or joint4).")
    parser.add_argument("--torque", type=float, default=40.0, help="Constant torque [Nm] applied to --joint. Default 40.")
    parser.add_argument("--duration", type=float, default=5.0, help="Simulated seconds to run. Default 5.")
    parser.add_argument("--keyframe", default="home", help="Keyframe name to reset to before applying torque. Default 'home'; falls back to qpos0 if not found.")
    parser.add_argument("--print-every", type=float, default=0.5, help="Print an internal-state snapshot every this many simulated seconds. Default 0.5.")
    parser.add_argument(
        "--settle",
        type=float,
        default=0.0,
        help=(
            "Simulated seconds to step with ZERO torque on every actuator BEFORE applying "
            "--torque. Default 0.0 (apply torque immediately at step 0). "
            "WHY THIS EXISTS (2026-07-29): the ROS2-side comparison this script was "
            "originally written against (ros2_ws/test_jointN_raw_torque.sh) does NOT apply "
            "its torque at the instant of reset_world_home -- seconds pass while "
            "switch_to_effort.sh runs, the shell sources ROS, and topic discovery "
            "completes. Throughout that gap every joint is commanded 0 Nm with no gravity "
            "compensation (pinn_controller_node is deliberately stopped for that test), so "
            "the arm free-falls and collapses; SESSION.md's own 2026-07-28 notes record "
            "joints 1/3 oscillating with effort pinned at the +/-87 Nm stops during exactly "
            "that test. This script, by contrast, applied its torque to a pristine home "
            "pose at step 0. The 'identical model, identical torque, opposite outcome' "
            "conclusion that redirected the whole investigation to the mujoco_ros2_control "
            "plugin therefore rested on a comparison where TWO variables differed at once: "
            "the software layer AND the arm's physical configuration when the torque "
            "landed. Set --settle to a few seconds to hold the layer constant and vary "
            "only the configuration. If the joint refuses to move after settling, the "
            "freeze is reproducible in pure physics with no ROS2 involved, and the plugin "
            "is NOT implicated."
        ),
    )
    args = parser.parse_args()

    print(f"Loading model: {args.model}")
    model = mujoco.MjModel.from_xml_path(args.model)
    data = mujoco.MjData(model)

    key_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, args.keyframe)
    if key_id >= 0:
        mujoco.mj_resetDataKeyframe(model, data, key_id)
        print(f"Reset to keyframe {args.keyframe!r}.")
    else:
        mujoco.mj_resetData(model, data)
        print(f"Keyframe {args.keyframe!r} not found -- reset to model default qpos0 instead.")

    joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, args.joint)
    qpos_adr = model.jnt_qposadr[joint_id]
    dof_adr = model.jnt_dofadr[joint_id]
    act_id = _find_actuator_for_joint(model, args.joint)

    print_every_steps = max(1, int(args.print_every / model.opt.timestep))

    q_reset = data.qpos[qpos_adr]

    if args.settle > 0.0:
        # Reproduce the ROS2 test's real starting conditions: every actuator at 0,
        # no gravity compensation, arm free-falling, for as long as the gap between
        # reset_world_home and the torque actually arriving on the wire.
        print(
            f"\n--- SETTLING {args.settle:.1f}s with ZERO torque on all {model.nu} actuators "
            f"(reproducing the un-compensated free-fall gap in test_joint4_raw_torque.sh) ---"
        )
        data.ctrl[:] = 0.0
        settle_steps = int(args.settle / model.opt.timestep)
        for step in range(settle_steps):
            mujoco.mj_step(model, data)
            if step % print_every_steps == 0 or step == settle_steps - 1:
                t = step * model.opt.timestep
                print(
                    f"  settle t={t:6.2f}s  q={data.qpos[qpos_adr]:+.5f}  "
                    f"qdot={data.qvel[dof_adr]:+.5f}  "
                    f"qfrc_constraint={data.qfrc_constraint[dof_adr]:+8.3f}  ncon={data.ncon}"
                )
        for line in _contact_summary(model, data):
            print(line)
        print(
            f"--- SETTLED. {args.joint} drifted {data.qpos[qpos_adr] - q_reset:+.5f} rad "
            f"from the keyframe during free-fall. Torque applied from here. ---\n"
        )

    q_start = data.qpos[qpos_adr]
    print(
        f"Target joint: {args.joint!r} (joint_id={joint_id}, actuator_id={act_id}). "
        f"Starting position: {q_start:+.5f} rad. Commanding {args.torque:+.2f} Nm, "
        f"everything else 0, for {args.duration:.1f}s (timestep={model.opt.timestep:.5f}s, "
        f"integrator={mujoco.mjtIntegrator(model.opt.integrator).name})."
    )

    data.ctrl[:] = 0.0
    data.ctrl[act_id] = args.torque

    n_steps = int(args.duration / model.opt.timestep)

    for step in range(n_steps):
        mujoco.mj_step(model, data)
        if step % print_every_steps == 0 or step == n_steps - 1:
            t = step * model.opt.timestep
            q = data.qpos[qpos_adr]
            qd = data.qvel[dof_adr]
            qfrc_bias = data.qfrc_bias[dof_adr]
            qfrc_passive = data.qfrc_passive[dof_adr]
            qfrc_constraint = data.qfrc_constraint[dof_adr]
            qfrc_actuator = data.qfrc_actuator[dof_adr]
            print(
                f"t={t:6.2f}s  q={q:+.5f} (delta={q - q_start:+.5f})  qdot={qd:+.5f}  "
                f"qfrc[actuator={qfrc_actuator:+8.3f} bias={qfrc_bias:+8.3f} "
                f"passive={qfrc_passive:+8.3f} constraint={qfrc_constraint:+8.3f}]  "
                f"ncon={data.ncon}"
            )
            for line in _contact_summary(model, data):
                print(line)

    q_end = data.qpos[qpos_adr]
    print("=" * 70)
    print(
        f"FINAL: {args.joint} moved {q_end - q_start:+.5f} rad over {args.duration:.1f}s "
        f"under a constant {args.torque:+.2f} Nm (unopposed by anything else commanded)."
    )
    if abs(q_end - q_start) < 0.01:
        print(
            "Essentially zero motion -- matches the ROS2-level symptom. "
            "Check the qfrc_constraint values and contact list printed above: "
            "a large, persistent qfrc_constraint or an active contact means "
            "something is physically resisting it; if qfrc_constraint stays "
            "near zero and no contacts ever appear, the block is NOT a "
            "contact/constraint at all, and the actuator/joint definition "
            "itself needs a much closer look (e.g. gainprm/biasprm on a "
            "<general> actuator effectively fighting the motor, if such an "
            "actuator is also present and mistakenly still active)."
        )
    else:
        print("The joint moved a meaningful amount in this standalone test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
