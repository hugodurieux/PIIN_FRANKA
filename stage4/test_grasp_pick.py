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
        # (panda_arm_mujoco.xml: pos="0.65 0 0.02") and demo_targets.py's
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
        # 2026-07-29: top surface DROPPED from z=0.0 to z=-0.03 (position
        # -0.05 -> -0.08, size unchanged). With the top flush at z=0.0 this box
        # touched the grasp cube, which rests at z=0.02 with 0.04 sides and so
        # spans z=[0.0, 0.04]. Coincident surfaces alone would be marginal, but
        # MoveIt2 pads collision geometry (~0.01 m default) on BOTH bodies, so
        # the padded box and the padded cube overlapped by ~0.02 m. The moment
        # GraspExecutor._attach_object() attached the cube to panda_hand it was
        # therefore already in collision with the floor, and the very next plan
        # request (approach sub-step 1/2) was rejected instantly --
        # error_code=99999 (MoveItErrorCodes::FAILURE) returned in ~1.6 ms,
        # far too fast to be a search timeout. Observed live in
        # test_grasp_pick_run20.log, the first run where the arm actually
        # reached this stage. _attach_object()'s own 2026-07-27 fix (shrink the
        # world box from its inflated 0.12 m planning size back to the real
        # 0.04 m footprint just before attaching) was necessary but not
        # sufficient: even the bare cube still touches a floor whose top is at
        # exactly z=0.0. Dropping the top 3 cm clears both padding envelopes
        # while still blocking any planned path that dips meaningfully below
        # the real floor -- and MuJoCo's actual floor plane at z=0 remains the
        # true physical stop regardless of what MoveIt2 plans.
        #
        # NOTE: this box was originally added 2026-07-24 to mitigate the
        # "joint4/6/7 freeze", on the theory that MoveIt2 was planning paths
        # through the floor. That theory is void -- the freeze was
        # mujoco_ros2_control silently reverting to its internal position PID
        # after every reset_world (see ros2_ws/force_effort_mode.sh). The box
        # is kept because bounding the planner below the floor is good practice
        # on its own, not because it fixes the freeze.
        # 2026-07-29: clear any grasp_object left ATTACHED to the gripper by a
        # previous aborted run, BEFORE registering anything. The planning scene
        # lives in move_group, not in this script, so it survives every restart
        # of this process -- only relaunching move_group clears it. pick()
        # attaches grasp_object before the approach, and on an ARM_TIMEOUT there
        # it aborts without ever reaching GraspExecutor._detach_object(), so the
        # attachment leaks into every subsequent run.
        #
        # This is not hypothetical: queried live from /get_planning_scene after
        # run20 aborted at the approach, the scene held
        #   attached_collision_objects=[link_name='panda_hand', id='grasp_object',
        #                               pose=(-0.002, 0.014, 0.307), quat=(0.92, 0.40, ...)]
        # -- a phantom box hanging 0.307 m off the gripper at a tumbled
        # orientation (the stale grasp-time transform). It rides along with every
        # planned motion, so at the last pre-approach waypoint (flange at
        # z=0.3299, pointing down) it sweeps down to about floor level and
        # collides with the floor box. Result: GOAL_STATE_INVALID on a goal pose
        # that run20 itself had planned successfully minutes earlier -- runs 21,
        # 22 and 23 all failed there deterministically, and raising
        # num_planning_attempts 1 -> 10 could not help, because no IK solution
        # for that goal is collision-free while the phantom is attached.
        #
        # Detach returns it to the world; remove then deletes that world copy, so
        # the add_collision_box calls below start from a genuinely empty slate.
        # Both are no-ops on a clean scene, so this is safe on a first run.
        log.info("Clearing any stale grasp_object attachment from a previous run...")
        arm.detach_object("grasp_object")
        arm.remove_collision_object("grasp_object")

        # 2026-07-29: FLOOR REGISTRATION REMOVED. It is fundamentally incompatible
        # with GraspExecutor's attach-before-descent design, and it was added for a
        # reason that has since been disproven.
        #
        # THE INCOMPATIBILITY. _attach_object() attaches grasp_object to panda_hand
        # while the arm is still at the PRE-APPROACH pose, 0.10 m above the grasp
        # (deliberately: the descent cannot be planned while the cube is still a
        # world obstacle the open fingers must straddle). MoveIt2 attaches an object
        # at its CURRENT world pose, so the stored transform is
        #     0.02 (cube) - 0.3299 (flange) = -0.3099 m below the flange
        # -- confirmed live by querying /get_planning_scene, which reported the
        # attached object at z=0.307 off panda_hand. That transform then rides with
        # the gripper. When the flange descends to the grasp pose at z=0.2299 the
        # phantom cube follows to
        #     0.2299 - 0.3099 = -0.08 m, spanning [-0.10, -0.06]
        # i.e. BELOW the real floor -- because MoveIt2 now believes a cube still
        # sitting on the ground moves downward with the gripper that has not yet
        # grasped it. Any floor box overlapping that range rejects the goal
        # instantly (~1.8 ms, vs the ~5 s an IK/search failure takes).
        # Live evidence: with the floor top at z=0.0 this killed approach sub-step
        # 1/2 (run20); dropping the top to z=-0.03 let 1/2 through and killed 2/2
        # instead (run25), since the phantom sinks further on the final step. There
        # is no floor height that is both deep enough to clear the phantom and
        # shallow enough to be worth having.
        #
        # WHY REMOVING IT IS SAFE. The box was added 2026-07-24 to mitigate the
        # "joint4/6/7 freeze" on the theory that MoveIt2 was planning paths through
        # the floor. That theory is void: the freeze was mujoco_ros2_control
        # silently reverting to its internal position PID after every reset_world
        # (see ros2_ws/force_effort_mode.sh). The box never fixed anything -- the
        # freeze recurred with it active -- and MuJoCo's own `floor` plane geom at
        # z=0 remains the real physical stop regardless of what MoveIt2 plans.
        #
        # THE PROPER FIX, deferred: do not attach before the descent at all.
        # Instead remove grasp_object from the world for the descent, and attach it
        # only after the gripper has actually closed on it -- which is both what
        # MoveIt's own pick pipeline does and what is physically true. Then the
        # floor box can come back safely. That is a structural change to
        # GraspExecutor.pick()'s phase order, worth doing deliberately rather than
        # at the end of a debugging session.
        log.info("Floor collision box intentionally NOT registered (see comment).")

        # 2026-07-29: inflation reduced 0.12 -> 0.06 (real cube is 0.04). The 3x
        # inflation was added 2026-07-23 to give the pre-approach moves planning
        # margin around a static obstacle, but it also walls off the corridor the
        # final pre-approach descent has to fly down: at 0.12 the box spans
        # z=[-0.04, 0.08] and +/-0.06 in x/y, so the open fingers (0.08 span) must
        # thread past a volume 3x the object they are reaching for. Observed live
        # as a FLAKY failure, which is the signature of a too-tight corridor
        # rather than a hard collision: test_grasp_pick_run20.log cleared
        # sub-step 5/5 fine, run21 failed it with error_code=99999 after 5.15s of
        # planning. That 5s is an OMPL search timeout -- contrast run20's attach
        # collision, which came back in 1.6ms. A goal in collision is rejected
        # instantly; a goal that is merely hard to reach burns the full budget.
        # 1.5x still keeps a real margin around the cube while leaving the
        # descent corridor open. The box is shrunk again to its true 0.04
        # footprint just before attaching (GraspExecutor._attach_object()).
        log.info("Registering grasp_object in the MoveIt2 planning scene...")
        arm.add_collision_box(
            "grasp_object",
            position=(0.65, 0.0, 0.02),
            size=(0.06, 0.06, 0.06),
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
            collision_object_position=(0.65, 0.0, 0.02),
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
