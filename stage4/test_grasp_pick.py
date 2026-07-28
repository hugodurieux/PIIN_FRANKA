"""
Manual live smoke test for GraspExecutor.pick() against the real grasp_object
cube in MuJoCo -- the first end-to-end integration of ArmMotionClient and
MuJoCoGripperController together, not just each backend individually.

Prerequisites (same live stack as test_arm_motion.py / test_mujoco_gripper.py):
  - mujoco_franka_moveit.launch.py running (move_group + MuJoCo + ros2_control).
  - pinn_controller_node running (bash ros2_ws/launch_pinn_controller.sh).
  - panda_effort_controller ACTIVE (bash ros2_ws/switch_to_effort.sh) --
    ArmMotionClient hands off via /pinn_controller/desired_trajectory, which
    has no authority while panda_arm_controller (position mode) still claims
    the arm's command interface.
  - panda_hand_controller running (spawned by the launch file already) --
    MuJoCoGripperController needs its gripper_cmd action server up.

KNOWN, FLAGGED, UNRESOLVED ISSUE this test is specifically expected to surface:
demo_targets.py's "grasp_object" entry targets panda_link8 (the flange),
not the fingertip TCP (see arm_motion_client.py's own tip_link docstring and
demo_targets.py's own comment on that entry). The real flange-to-fingertip
offset was never measured or compensated for. This test's PRIMARY purpose is
to make that offset empirically visible -- expect the fingers to NOT land
squarely on the cube on the first attempt. A failed grasp() with a sensible,
non-NaN final width is useful diagnostic data (how far off, in which
direction), not just a pass/fail result -- read the logged GraspResult and
gripper width closely rather than only checking the return code.

Order of construction matters: MuJoCoGripperController.__init__() calls
rclpy.init() itself (see gripper_controller.py). ArmMotionClient does NOT
call rclpy.init() (see its own docstring -- it expects a context to already
exist). So the gripper is constructed FIRST here to establish the shared
rclpy context, then the arm client second. Do not reorder.

Usage:
    source /opt/ros/jazzy/setup.bash
    source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash
    source /home/hci-student/projects/pinn_franka/ros2_ws/set_pinn_env.sh
    python3 stage4/test_grasp_pick.py
"""

from __future__ import annotations

import logging
import sys

import rclpy

from stage4.arm_motion_client import ArmMotionClient
from stage4.demo_targets import get_target
from stage4.grasp_config import GraspConfig
from stage4.grasp_executor import GraspExecutor, GraspResult
from stage4.gripper_controller import MuJoCoGripperController

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("test_grasp_pick")


def main() -> int:
    # Gripper first: its __init__ calls rclpy.init(). See module docstring.
    gripper = MuJoCoGripperController()
    arm = ArmMotionClient()

    try:
        # 2026-07-23 (Opus 4.8): make MoveIt2 AWARE of grasp_object before any
        # planning. Until now the cube existed only in MuJoCo physics, never as
        # a MoveIt2 collision object, so OMPL planned the home->pre-approach move
        # straight through the cube's real location and MuJoCo physics pinned
        # the arm against it (frozen joints, torque absorbed by contact -- the
        # root cause found live 2026-07-23). Registering it here makes every
        # plan route around it. Position matches the MJCF grasp_object body
        # (panda_arm_mujoco.xml: pos="0.5 0 0.02") and demo_targets.py's
        # documented placement; frame defaults to panda_link0 (the base). This
        # is done in the TEST/orchestration layer (not ArmMotionClient.__init__),
        # keeping the client generic and the cube's literal numbers out of it.
        # GraspExecutor is told the object's id (collision_object_name) so it
        # attaches/detaches it to the gripper at the right phases -- see
        # ArmMotionClient.attach_object()'s docstring for why the attach is
        # needed (else MoveIt2 refuses to descend into a known obstacle).
        #
        # 2026-07-23 correction: registering the box at its bare 0.04m size
        # (the object's real geometry) was CONFIRMED live to be insufficient.
        # Diagnostic: moving the real cube 2m out of reach (nothing to hit)
        # made the freeze disappear completely, with this SAME registration
        # still active -- proving the registration itself wasn't the problem,
        # but that MoveIt2's planned path (which does clear a bare-sized box)
        # left no margin for Stage 3's real tracking error. This project has
        # repeatedly measured several cm of steady-state/tracking error on
        # ordinary moves this session (see arm_motion_client.py's own
        # tolerance-related comments) -- a bare-size collision box gives the
        # planner zero cushion for that, so the ACTUALLY EXECUTED path can
        # drift just far enough off-plan to clip the real object, which
        # MuJoCo then registers as a genuine contact (commanded torque
        # absorbed by it, reads exactly like a physical block). Inflated to
        # 0.12m (adds ~4cm of clearance per side beyond the object's own 4cm
        # size) -- comfortably larger than the ~1.5-6cm tracking errors
        # observed on convergent moves this session, while still small enough
        # that the pre-approach waypoint (10cm above the cube's true center)
        # clears it with room to spare. Only affects PLANNING margin around
        # the object while it's a world obstacle (pre-approach); once
        # attach_object() runs (right before the actual descent), MoveIt2
        # stops treating it as an obstacle at all, so this inflation has no
        # effect on how closely the fingers can actually approach/close on
        # the real (bare-sized) object.
        # 2026-07-24: register the floor too. MoveIt2's planning scene has
        # NEVER had a floor collision object (see ArmMotionClient's own
        # get_current_pose docstring / attach_object's honest caveat: "no
        # floor plane is registered in the planning scene") -- only the
        # MuJoCo physics scene has a real floor (panda_arm_mujoco.xml's
        # `floor` plane geom at z=0). This session's self-collision fix
        # (panda_arm_mujoco.xml's conaffinity="0") made the joint4/6/7 freeze
        # much rarer but NOT disappear entirely -- it recurred on a later
        # attempt with a DIFFERENT IK solution for the same pre-approach
        # target, which fits floor contact better than self-collision (self-
        # collision is now structurally impossible via conaffinity=0, so a
        # freeze recurring afterward must be a different contact -- floor is
        # the one contact type the self-collision fix deliberately did NOT
        # touch, since robot-vs-floor contact needs to stay real). A box
        # spanning z=-0.1..0 (top surface flush with the real floor) covering
        # the whole reachable workspace so MoveIt2 stops planning any path
        # that dips the forearm through it, regardless of which IK solution
        # it picks. NOT YET LIVE-VALIDATED.
        log.info("Registering the floor in the MoveIt2 planning scene...")
        arm.add_collision_box(
            "floor",
            position=(0.0, 0.0, -0.05),
            size=(2.0, 2.0, 0.1),
        )

        log.info("Registering grasp_object in the MoveIt2 planning scene...")
        arm.add_collision_box(
            "grasp_object",
            position=(0.5, 0.0, 0.02),
            size=(0.12, 0.12, 0.12),
        )

        cfg = GraspConfig(
            grasp_width=0.04,
            grasp_force=20.0,
            object_mass=0.064,
            collision_object_name="grasp_object",
            # 2026-07-27: real (bare) geometry, matching the MJCF grasp_object
            # body -- see GraspExecutor._attach_object()'s 2026-07-27 comment.
            # Used to shrink the collision object back down right before
            # attach, so it no longer overlaps the floor collision box below.
            collision_object_bare_size=(0.04, 0.04, 0.04),
            collision_object_position=(0.5, 0.0, 0.02),
        )
        executor = GraspExecutor(cfg, gripper, arm_controller=arm)

        target = get_target("grasp_object")
        log.info("pick('grasp_object')...\n%s", target)
        result = executor.pick(target)
        log.info("pick() -> %s (final phase: %s)", result, executor.phase)

        status = gripper.read()
        log.info("final gripper status: %s", status)

        if result != GraspResult.SUCCESS:
            log.warning(
                "pick() did NOT succeed. This is expected/diagnostic on the "
                "first attempt -- see module docstring re: flange-vs-fingertip "
                "offset. Check the gripper width above against cfg.grasp_width "
                "(%.3f m) to gauge how far off the approach was, and check the "
                "controller logs for arm convergence diffs if result is "
                "ARM_TIMEOUT.",
                cfg.grasp_width,
            )
            return 1

        log.info("ALL CHECKS PASSED — cube grasped and lifted")
        return 0
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    sys.exit(main())
