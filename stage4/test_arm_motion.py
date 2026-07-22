"""
Manual live smoke test for ArmMotionClient.

Prerequisites (same launch sequence as the rest of this project's Stage 2/3
live tests):
  - mujoco_franka_moveit.launch.py running (move_group + MuJoCo + ros2_control).
  - pinn_controller_node running (bash ros2_ws/launch_pinn_controller.sh).
  - panda_effort_controller ACTIVE (bash ros2_ws/switch_to_effort.sh) --
    ArmMotionClient hands off to Stage 3's controller via
    /pinn_controller/desired_trajectory, which has no authority to move the
    arm while panda_arm_controller (position mode) is still the active
    controller claiming the arm's command interface.

This is the FIRST live test of Cartesian pose-goal planning in this project
-- moveit_plan_bridge.py (validated during Milestone 2) only ever exercised
joint-space targets. Start conservative: this requests a move to
demo_targets' "home" pose, NOT "grasp_object" directly, to validate the
pose -> IK -> trajectory -> execution pipeline itself first.

Usage:
    source /opt/ros/jazzy/setup.bash
    source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash
    source /home/hci-student/projects/pinn_franka/ros2_ws/set_pinn_env.sh
    python3 stage4/test_arm_motion.py
"""

from __future__ import annotations

import logging
import sys

import rclpy

from stage4.arm_motion_client import ArmMotionClient
from stage4.demo_targets import get_target

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("test_arm_motion")


def main() -> int:
    rclpy.init()
    try:
        arm = ArmMotionClient()

        target = get_target("home")
        log.info("move_to('home')...\n%s", target)
        ok = arm.move_to(target, speed=0.05, timeout=30.0)
        log.info("move_to() -> %s", ok)
        if not ok:
            log.error("FAIL: arm did not reach the 'home' target")
            return 1

        log.info("ALL CHECKS PASSED")
        return 0
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    sys.exit(main())
