"""
GraspExecutor — orchestrates force-controlled pick-and-place for Stage 4.

State machine:
  IDLE
    -> PRE_APPROACH  (arm moves above grasp pose)
    -> APPROACH      (arm descends to grasp pose)
    -> GRASPING      (gripper closes with force control)
    -> LIFTING       (arm rises with object; payload updated in Stage 3 controller)
    -> HOLDING       (object held, awaiting place or release command)
    -> RELEASING     (gripper opens, arm returns to pre-approach)
    -> IDLE

The executor delegates arm motion to an ArmMotionClient (stage4/arm_motion_client.py,
which plans via MoveIt2 and hands off to Stage 3's ComputedTorquePDController
through the already-running pinn_controller_node) and gripper commands to a
BaseGripperController backend.  It never modifies any Stage 1/2/3 code — it
only calls their public interfaces.

Known gap (2026-07-22, not yet solved): update_payload() calls below are
guarded by hasattr(self.arm, "update_payload") and silently skipped for
ArmMotionClient, which has no such method -- Stage 3's live payload estimate
lives inside pinn_controller_node's own in-process ComputedTorquePDController,
not reachable from this external process without a new ROS2 interface
(service/topic/param) on that node. Grasping still works without it; the
controller just won't know a payload was picked up.

Usage (with mock, no hardware):
    from stage4.grasp_config import GraspConfig
    from stage4.gripper_controller import MockGripperController
    from stage4.grasp_executor import GraspExecutor

    cfg = GraspConfig(grasp_width=0.04, grasp_force=20.0, object_mass=0.2)
    gripper = MockGripperController(simulate_success=True)
    executor = GraspExecutor(cfg, gripper, arm_controller=None)  # None = dry-run
    result = executor.pick(grasp_pose=np.eye(4))
"""

from __future__ import annotations

import logging
import time
from enum import Enum, auto
from typing import Optional

import numpy as np
from scipy.spatial.transform import Rotation, Slerp

from stage4.grasp_config import GraspConfig
from stage4.gripper_controller import BaseGripperController, GripperState

logger = logging.getLogger(__name__)


class GraspPhase(Enum):
    IDLE         = auto()
    PRE_APPROACH = auto()
    APPROACH     = auto()
    GRASPING     = auto()
    LIFTING      = auto()
    HOLDING      = auto()
    RELEASING    = auto()
    ABORTED      = auto()


class GraspResult(Enum):
    SUCCESS = auto()
    GRIPPER_FAILED   = auto()   # gripper action returned failure
    ARM_TIMEOUT      = auto()   # arm did not reach pose in time
    TORQUE_OVERLOAD  = auto()   # Stage 3 reported excessive torque error
    ABORTED          = auto()   # explicit abort() call


class GraspExecutor:
    """
    Orchestrates a complete pick sequence.

    Args:
        config: GraspConfig with all tuning parameters.
        gripper: A BaseGripperController backend (MuJoCo, real hardware, or Mock).
        arm_controller: An ArmMotionClient instance (stage4/arm_motion_client.py).
            Pass None for dry-run / testing without arm hardware.
    """

    def __init__(
        self,
        config: GraspConfig,
        gripper: BaseGripperController,
        arm_controller=None,
    ) -> None:
        self.config  = config
        self.gripper = gripper
        self.arm     = arm_controller
        self._phase  = GraspPhase.IDLE
        self._abort_requested = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def phase(self) -> GraspPhase:
        return self._phase

    def abort(self) -> None:
        """Request an abort at the next safe checkpoint."""
        self._abort_requested = True
        self.gripper.stop()
        logger.warning("GraspExecutor: abort requested")

    def pick(self, grasp_pose: np.ndarray) -> GraspResult:
        """
        Execute a complete pick sequence targeting `grasp_pose`.

        Args:
            grasp_pose: (4, 4) homogeneous transform of the grasp frame
                in the robot base frame.  The gripper approach axis is
                assumed to be the z-axis of this frame.

        Returns:
            GraspResult indicating success or the failure mode.
        """
        self._abort_requested = False

        # 1. Open gripper
        logger.info("Opening gripper to %.3f m", self.config.open_width)
        ok = self.gripper.open(
            width=self.config.open_width,
            speed=self.config.open_speed,
            timeout=self.config.gripper_timeout,
        )
        if not ok:
            return self._fail(GraspResult.GRIPPER_FAILED, "gripper open failed")

        # 2. Pre-approach
        # 2026-07-28: routed via a safe transit height (see
        # _transit_waypoints's docstring) instead of a direct diagonal SE(3)
        # interpolation -- CONFIRMED LIVE that the direct interpolation let
        # the forearm/hand clip grasp_object while still far from the target,
        # producing the joint4/6/7 freeze independent of controller or IK
        # solver (see GraspConfig.transit_height_margin's comment for the
        # full investigation). Falls back to the original single-move
        # behavior when the arm backend can't report its current pose
        # (dry-run, or FK/pinocchio unavailable).
        pre_pose = self._pre_approach_pose(grasp_pose)
        self._phase = GraspPhase.PRE_APPROACH
        current_pose = None
        if self.arm is not None and hasattr(self.arm, "get_current_pose"):
            current_pose = self.arm.get_current_pose()
        if current_pose is not None:
            pre_approach_waypoints = self._transit_waypoints(current_pose, pre_pose)
        else:
            pre_approach_waypoints = [pre_pose]
        for i, wp_pose in enumerate(pre_approach_waypoints):
            logger.info(
                "Moving to pre-approach pose, sub-step %d/%d",
                i + 1,
                len(pre_approach_waypoints),
            )
            result = self._move_arm(
                wp_pose,
                speed=self.config.approach_speed,
                cartesian_tolerance=self.config.pre_approach_cartesian_tolerance,
            )
            if result is not None:
                return result

        # 2026-07-23 (Opus 4.8): attach the (world-registered) grasp object to
        # the gripper NOW -- after pre-approach positioned the arm above the
        # cube and committed to the grasp, but BEFORE descending. If the cube
        # stayed a plain world obstacle, MoveIt2 would refuse to plan the
        # descent whose open fingers straddle it; attaching removes it as an
        # obstacle for the descent/grasp/lift and lets the fingers touch it.
        # See _attach_object() / ArmMotionClient.attach_object() for the full
        # rationale. No-op unless config.collision_object_name is set and the
        # arm backend supports it. Deliberately placed after the pre-approach
        # move (which NEEDS the cube as an obstacle to route around) and before
        # the descent (which needs it NOT to be one).
        self._attach_object()

        # 3. Approach (descend to grasp pose)
        self._phase = GraspPhase.APPROACH
        logger.info("Approaching grasp pose")
        # 2026-07-23: tighter tolerance than the default -- found live that
        # the default 0.15 rad let the arm report "converged" while the
        # gripper was actually 10-15cm away from grasp_object (a settle
        # pause before grasping made no difference, ruling out timing and
        # pointing at real, stable positioning error at that tolerance). See
        # GraspConfig.approach_convergence_tolerance's own comment.
        #
        # 2026-07-23 (Opus 4.8): split the descent into N Cartesian sub-steps
        # (approach_num_waypoints) instead of one jump -- see that config
        # field's comment. Intermediate waypoints pass through at the loose
        # default tolerance; only the final grasp pose uses the tight one.
        # This pairs with ArmMotionClient's keep-target-fresh fix (the actual
        # root-cause fix for the earlier "joint3 drifts away / joint5 plateaus
        # / never reaches 0.03 rad" timeout -- the controller was abandoning
        # the target to a gravity-comp hold 2s after receipt; see
        # ArmMotionClient._HOLD_REFRESH_INTERVAL's comment).
        descent_poses = self._descent_waypoints(pre_pose, grasp_pose)
        for i, wp_pose in enumerate(descent_poses):
            is_final = i == len(descent_poses) - 1
            # Only the FINAL sub-step (the actual grasp pose) is held to the
            # tight tolerance; intermediate waypoints pass through loosely.
            # Both a Cartesian tolerance (primary, FK-based) and the legacy
            # radian tolerance (FK-unavailable fallback) are supplied so the
            # tight bound applies whichever check ArmMotionClient ends up using.
            tol = self.config.approach_convergence_tolerance if is_final else None
            cart_tol = self.config.approach_cartesian_tolerance if is_final else None
            logger.info(
                "Approach sub-step %d/%d%s",
                i + 1,
                len(descent_poses),
                " (final grasp pose, tight tolerance)" if is_final else "",
            )
            result = self._move_arm(
                wp_pose,
                speed=self.config.approach_speed,
                convergence_tolerance=tol,
                cartesian_tolerance=cart_tol,
            )
            if result is not None:
                return result

        # 2026-07-23: settle pause -- move_to() reports success the instant
        # joint error first drops under its tolerance, which can still be
        # mid-settle (see GraspConfig.pre_grasp_settle_sec's own comment).
        # Found live: the gripper closing immediately on "converged" grasped
        # empty space because the arm was still finishing its descent.
        if self._abort_requested:
            return self._fail(GraspResult.ABORTED, "abort requested")
        time.sleep(self.config.pre_grasp_settle_sec)

        # 4. Grasp
        self._phase = GraspPhase.GRASPING
        logger.info(
            "Grasping: width=%.3f m, force=%.1f N",
            self.config.grasp_width,
            self.config.grasp_force,
        )
        grasped = self.gripper.grasp(
            width=self.config.grasp_width,
            speed=self.config.grasp_speed,
            force=self.config.grasp_force,
            epsilon_inner=self.config.epsilon_inner,
            epsilon_outer=self.config.epsilon_outer,
            timeout=self.config.gripper_timeout,
        )
        if not grasped:
            # Grasp failed -- the cube is NOT in hand, so return the (attached)
            # planning-scene object to the world before bailing, keeping the
            # MoveIt2 scene faithful (no phantom object stuck to the gripper).
            self._detach_object()
            return self._fail(GraspResult.GRIPPER_FAILED, "grasp contact not detected")

        # 5. Update arm controller payload (object is now in hand)
        if self.arm is not None and hasattr(self.arm, "update_payload"):
            logger.info("Updating arm payload to %.2f kg", self.config.object_mass)
            self.arm.update_payload(self.config.object_mass)

        # 6. Lift
        self._phase = GraspPhase.LIFTING
        lift_pose = self._lift_pose(grasp_pose)
        logger.info("Lifting %.3f m", self.config.lift_height)
        result = self._move_arm(lift_pose, speed=self.config.lift_speed)
        if result is not None:
            # Object slipped or arm failed — open gripper, return the object to
            # the world in the planning scene, and report.
            self.gripper.open(
                width=self.config.open_width,
                speed=self.config.open_speed,
                timeout=self.config.gripper_timeout,
            )
            self._detach_object()
            return result

        self._phase = GraspPhase.HOLDING
        logger.info("Pick complete — object held")
        return GraspResult.SUCCESS

    def place(self, place_pose: np.ndarray) -> GraspResult:
        """
        Execute a place sequence: move to place_pose, release, retract.

        Should be called after a successful pick().

        Args:
            place_pose: (4, 4) homogeneous transform of the release frame.

        Returns:
            GraspResult.SUCCESS or a failure mode.
        """
        if self._phase != GraspPhase.HOLDING:
            logger.warning(
                "place() called in phase %s — expected HOLDING", self._phase
            )

        # 1. Move to place pose
        result = self._move_arm(place_pose, speed=self.config.approach_speed)
        if result is not None:
            return result

        # 2. Release
        self._phase = GraspPhase.RELEASING
        logger.info("Releasing object")
        self.gripper.open(
            width=self.config.open_width,
            speed=self.config.open_speed,
            timeout=self.config.gripper_timeout,
        )

        # 3. Reset payload in arm controller and return the object to the world
        #    in the planning scene (it is released at place_pose, no longer held).
        if self.arm is not None and hasattr(self.arm, "update_payload"):
            self.arm.update_payload(0.0)
        self._detach_object()

        # 4. Retract above place pose
        pre_place = self._pre_approach_pose(place_pose)
        result = self._move_arm(pre_place, speed=self.config.lift_speed)
        if result is not None:
            return result

        self._phase = GraspPhase.IDLE
        logger.info("Place complete")
        return GraspResult.SUCCESS

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _fail(self, reason: GraspResult, msg: str) -> GraspResult:
        logger.error("GraspExecutor FAILED [%s]: %s", reason.name, msg)
        self._phase = GraspPhase.ABORTED
        return reason

    # 2026-07-23 (Opus 4.8): MoveIt2 planning-scene attach/detach. Guarded by
    # hasattr exactly like update_payload above -- ArmMotionClient exposes
    # attach_object/detach_object, the Mock/dry-run arm (None) does not, so a
    # dry-run silently no-ops. Attaching converts the (already world-registered)
    # grasp object from a static obstacle MoveIt2 would refuse to descend into,
    # into part of the robot for the descent/grasp/lift phases; see
    # ArmMotionClient.attach_object()'s and GraspConfig.collision_object_name's
    # docstrings for the full why. Failures are logged inside ArmMotionClient
    # and are non-fatal here (a scene-sync hiccup should not abort a pick that
    # MuJoCo physics can still complete).
    def _attach_object(self) -> None:
        name = self.config.collision_object_name
        if not (name and self.arm is not None and hasattr(self.arm, "attach_object")):
            return
        # 2026-07-27: shrink the object back to its real (bare) collision
        # geometry immediately before attaching. The world registration is
        # deliberately INFLATED (see test_grasp_pick.py's 2026-07-23 comment)
        # to give the pre-approach move planning margin around a static
        # obstacle -- but attach_object() reuses that SAME geometry for the
        # attached copy, which then rides with the gripper through the
        # descent. Confirmed via static read: the inflated box (pos z=0.02,
        # size 0.12m -> z spans [-0.04, 0.08]) statically overlaps the floor
        # collision box added the previous session (z spans [-0.1, 0.0]) by
        # 4cm -- so the instant the object is attached, the robot state is
        # already in collision with the floor, and every plan requested right
        # after (e.g. the first approach sub-step) fails outright with a
        # generic MoveIt2 FAILURE (error_code=99999), deterministically, not
        # intermittently. This contradicts attach_object()'s own docstring
        # ("nothing else is registered... for the attached box to falsely
        # collide with") -- true when written, before the floor box existed.
        # Resizing to the real footprint just before attach removes the
        # overlap without touching the pre-approach planning margin (which
        # only matters while the object is still a free-standing world
        # obstacle). NOT YET LIVE-VALIDATED.
        if (
            self.config.collision_object_bare_size is not None
            and self.config.collision_object_position is not None
            and hasattr(self.arm, "add_collision_box")
        ):
            self.arm.add_collision_box(
                name,
                position=self.config.collision_object_position,
                size=self.config.collision_object_bare_size,
            )
        logger.info(
            "Attaching '%s' to %s in MoveIt2 planning scene",
            name,
            self.config.attach_link,
        )
        self.arm.attach_object(name, link=self.config.attach_link)

    def _detach_object(self) -> None:
        name = self.config.collision_object_name
        if name and self.arm is not None and hasattr(self.arm, "detach_object"):
            logger.info("Detaching '%s' in MoveIt2 planning scene", name)
            self.arm.detach_object(name, link=self.config.attach_link)

    def _move_arm(
        self,
        target_pose: np.ndarray,
        speed: float,
        convergence_tolerance: Optional[float] = None,
        cartesian_tolerance: Optional[float] = None,
    ) -> Optional[GraspResult]:
        """
        Command the arm to move to `target_pose`.

        In this scaffolded implementation the arm motion is a no-op when
        self.arm is None (dry-run / mock mode). Otherwise self.arm is
        expected to be an ArmMotionClient (see stage4/arm_motion_client.py),
        which plans a Cartesian-goal MoveIt2 request and hands the resulting
        trajectory to the already-running pinn_controller_node (Stage 3).

        convergence_tolerance [rad] is the FALLBACK-only joint-space tolerance
        (used by ArmMotionClient only when FK is unavailable).
        cartesian_tolerance [m], if given, overrides ArmMotionClient's default
        Cartesian (flange-position) convergence tolerance -- the primary check.
        pick()'s final approach step passes the tight approach_cartesian_tolerance
        here. See ArmMotionClient.move_to()'s 2026-07-23 docstring for why the
        convergence check moved from radians to Cartesian metres.

        Returns None on success, or a GraspResult on failure.
        """
        if self._abort_requested:
            return self._fail(GraspResult.ABORTED, "abort requested")

        if self.arm is None:
            # Dry-run: simulate motion delay
            logger.debug("DRY-RUN: would move arm to\n%s", target_pose)
            time.sleep(0.01)
            return None

        ok = self.arm.move_to(
            target_pose,
            speed=speed,
            timeout=self.config.arm_motion_timeout,
            convergence_tolerance=convergence_tolerance,
            cartesian_tolerance=cartesian_tolerance,
        )
        if not ok:
            return self._fail(GraspResult.ARM_TIMEOUT, "arm did not reach target pose")
        return None

    def _descent_waypoints(
        self, pre_pose: np.ndarray, grasp_pose: np.ndarray
    ) -> list[np.ndarray]:
        """Return the intermediate + final poses for the pre->grasp descent.

        Splits the straight-line descent from `pre_pose` down to `grasp_pose`
        into ``config.approach_num_waypoints`` equal Cartesian position steps.
        Orientation is held constant (pre_pose and grasp_pose share it by
        construction -- _pre_approach_pose only shifts the translation along
        the grasp frame's z-axis), so only the translation column is
        interpolated. The list always ENDS with grasp_pose exactly (no
        floating-point drift on the final, precision-critical pose). With
        approach_num_waypoints=1 this returns just [grasp_pose], i.e. the
        original single-move behavior.
        """
        n = max(1, int(self.config.approach_num_waypoints))
        start_pos = pre_pose[:3, 3]
        end_pos = grasp_pose[:3, 3]
        poses: list[np.ndarray] = []
        for k in range(1, n + 1):
            if k == n:
                poses.append(grasp_pose.copy())  # exact final pose
                break
            frac = k / n
            wp = grasp_pose.copy()  # inherits the (shared) orientation
            wp[:3, 3] = (1.0 - frac) * start_pos + frac * end_pos
            poses.append(wp)
        return poses

    @staticmethod
    def _interpolate_pose_waypoints(
        start_pose: np.ndarray, end_pose: np.ndarray, n: int
    ) -> list[np.ndarray]:
        """Return N intermediate + final poses interpolating start_pose ->
        end_pose in full SE(3) (position lerp + orientation slerp).

        2026-07-24: unlike _descent_waypoints (position-only lerp, valid
        there because pre_pose and grasp_pose share an orientation by
        construction), the home->pre-approach leg's start (wherever the arm
        actually is) and end (pre-approach, TOP_DOWN) generally do NOT share
        an orientation. Interpolating position only would leave the full
        reorientation to happen inside the FIRST sub-step's IK solution,
        defeating the point of splitting -- if the large joint4/6/7 swing
        found live 2026-07-24 is driven mainly by the ORIENTATION change (not
        the translation), a position-only split would not have reduced it at
        all. Slerp distributes the rotation across every sub-step too, so
        each individual move asks for a smaller angular change on every
        joint, not just a smaller translation.
        List always ENDS with end_pose exactly (no interpolation drift on the
        final, real target -- same convention as _descent_waypoints).
        """
        n = max(1, int(n))
        start_pos = start_pose[:3, 3]
        end_pos = end_pose[:3, 3]
        rotations = Rotation.from_matrix(
            np.stack([start_pose[:3, :3], end_pose[:3, :3]])
        )
        slerp = Slerp([0.0, 1.0], rotations)
        poses: list[np.ndarray] = []
        for k in range(1, n + 1):
            if k == n:
                poses.append(end_pose.copy())  # exact final pose
                break
            frac = k / n
            wp = np.eye(4)
            wp[:3, 3] = (1.0 - frac) * start_pos + frac * end_pos
            wp[:3, :3] = slerp([frac])[0].as_matrix()
            poses.append(wp)
        return poses

    def _transit_waypoints(
        self, current_pose: np.ndarray, pre_pose: np.ndarray
    ) -> list[np.ndarray]:
        """Route current_pose -> pre_pose via a safe transit height instead
        of a direct diagonal interpolation.

        2026-07-28: CONFIRMED LIVE (test_direct_joint_bypass.py) that a
        direct SE(3) interpolation only controls the FLANGE's Cartesian
        path -- it says nothing about the elbow/forearm, which can still dip
        low while the flange is still translating horizontally far from the
        target. That let the forearm clip grasp_object mid-sweep, producing
        a real MuJoCo contact (observed directly via the viewer) that pins
        whichever joints happen to be driving the sweep, independent of the
        controller or which IK solution was used to reach the endpoints.

        Three legs, so the arm is never both low AND horizontally far from
        the target at once:
          1. Lift straight up from current_pose to transit height (position
             only -- orientation held at current_pose's own, no reorientation
             risk during this leg).
          2. Translate horizontally at transit height (position AND
             orientation, via _interpolate_pose_waypoints's slerp, split into
             config.pre_approach_num_waypoints sub-steps -- same reasoning as
             that method's own docstring for why orientation must be blended
             gradually here, not dumped into one step).
          3. Descend straight down onto pre_pose (position only -- both
             endpoints already share pre_pose's orientation from leg 2, so
             this is a pure vertical move, no reorientation).

        transit height = max(current_z, target_z) + config.transit_height_margin,
        so both the lift and descent legs are monotonic (never revisit a
        height lower than either endpoint).
        """
        current_z = current_pose[2, 3]
        target_z = pre_pose[2, 3]
        transit_z = max(current_z, target_z) + self.config.transit_height_margin

        lift_pose = current_pose.copy()
        lift_pose[2, 3] = transit_z

        transit_end_pose = pre_pose.copy()
        transit_end_pose[2, 3] = transit_z

        n = max(1, int(self.config.pre_approach_num_waypoints))
        waypoints = [lift_pose]
        waypoints.extend(
            self._interpolate_pose_waypoints(lift_pose, transit_end_pose, n)
        )
        waypoints.append(pre_pose.copy())
        return waypoints

    def _pre_approach_pose(self, grasp_pose: np.ndarray) -> np.ndarray:
        z_axis = grasp_pose[:3, 2]
        pre = grasp_pose.copy()
        pre[:3, 3] -= self.config.pre_approach_height * z_axis
        return pre

    @staticmethod
    def _lift_pose_static(grasp_pose: np.ndarray, height: float) -> np.ndarray:
        """Return a pose `height` metres above `grasp_pose` in the world z direction."""
        lifted = grasp_pose.copy()
        lifted[2, 3] += height  # straight up in world frame
        return lifted

    def _lift_pose(self, grasp_pose: np.ndarray) -> np.ndarray:
        return self._lift_pose_static(grasp_pose, self.config.lift_height)
