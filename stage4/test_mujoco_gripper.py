"""
Manual live smoke test for MuJoCoGripperController, against an already-running
mujoco_franka_moveit.launch.py (panda_hand_controller must be active).

Not a pytest suite -- stage4/dry_run.py already covers MockGripperController
offline; this is specifically for exercising the real ROS2 action path live,
the same way ros2_ws/gripper_open.sh / gripper_close.sh did manually before
this class existed.

Usage:
    source /opt/ros/jazzy/setup.bash
    source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash
    source /home/hci-student/projects/pinn_franka/ros2_ws/set_pinn_env.sh
    python3 stage4/test_mujoco_gripper.py
"""

from __future__ import annotations

import logging
import math
import sys

from stage4.gripper_controller import MuJoCoGripperController

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("test_mujoco_gripper")


def main() -> int:
    gripper = MuJoCoGripperController()

    log.info("homing() -- should move to fully open...")
    ok = gripper.homing()
    status = gripper.read()
    log.info("  homing() -> %s, read() -> %s", ok, status)
    # homing()'s own return value (reached_goal, from the action's own,
    # authoritative result) is the real pass/fail signal. read()'s width is a
    # separate, out-of-band /joint_states snapshot taken immediately after --
    # it can lag slightly behind the controller's own looser internal
    # tolerance (observed live: reached_goal=True with width still ~0.0725,
    # not a bug, just residual settling / read timing slop), so it's only
    # worth a warning here, not a hard failure. NaN specifically (Python
    # comparisons like "nan < 0.075" are always False, so a NaN would
    # otherwise silently look fine) still gets called out explicitly.
    if not ok:
        log.error("FAIL: homing() itself reported failure")
        return 1
    if math.isnan(status.width):
        log.error("FAIL: read() never received a valid /joint_states reading")
        return 1
    if status.width < 0.07:
        log.warning("read() width %.4f is lower than expected after homing() (informational only)", status.width)

    log.info(
        "grasp(width=0.04, force=20) -- NOTE: this only exercises the gripper "
        "joint itself, not whether the arm is actually positioned over "
        "grasp_object. _move_arm() doesn't exist yet, so wherever the arm "
        "happens to be sitting is where this closes to. A 'success' here just "
        "means the final width landed in tolerance, in whatever the fingers "
        "found (or didn't find) at the arm's current position -- it is NOT "
        "yet proof of a real grasp on the cube."
    )
    ok = gripper.grasp(width=0.04, speed=0.05, force=20.0, epsilon_inner=0.02, epsilon_outer=0.02)
    status = gripper.read()
    log.info("  grasp() -> %s, read() -> %s", ok, status)
    if not ok:
        log.warning(
            "grasp() reported failure -- check whether grasp_object is actually "
            "between the fingers (the arm hasn't been moved there yet, this test "
            "only exercises the gripper joint itself)."
        )

    log.info("open() -- release...")
    ok = gripper.open(width=0.08, speed=0.1)
    status = gripper.read()
    log.info("  open() -> %s, read() -> %s", ok, status)
    if not ok:
        log.error("FAIL: open() itself reported failure")
        return 1
    if math.isnan(status.width):
        log.error("FAIL: read() never received a valid /joint_states reading")
        return 1
    if status.width < 0.07:
        log.warning("read() width %.4f is lower than expected after open() (informational only)", status.width)

    log.info("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
