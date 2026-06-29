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

The executor delegates arm motion to Stage 3's ComputedTorquePDController and
gripper commands to a BaseGripperController backend.  It never modifies any
Stage 1/2/3 code — it only calls their public interfaces.

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
        gripper: A BaseGripperController backend (ROS2 or Mock).
        arm_controller: A ComputedTorquePDController instance (Stage 3).
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
        pre_pose = self._pre_approach_pose(grasp_pose)
        self._phase = GraspPhase.PRE_APPROACH
        logger.info("Moving to pre-approach pose")
        result = self._move_arm(pre_pose, speed=self.config.approach_speed)
        if result is not None:
            return result

        # 3. Approach (descend to grasp pose)
        self._phase = GraspPhase.APPROACH
        logger.info("Approaching grasp pose")
        result = self._move_arm(grasp_pose, speed=self.config.approach_speed)
        if result is not None:
            return result

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
            # Object slipped or arm failed — open gripper and report
            self.gripper.open(
                width=self.config.open_width,
                speed=self.config.open_speed,
                timeout=self.config.gripper_timeout,
            )
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

        # 3. Reset payload in arm controller
        if self.arm is not None and hasattr(self.arm, "update_payload"):
            self.arm.update_payload(0.0)

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

    def _move_arm(
        self, target_pose: np.ndarray, speed: float
    ) -> Optional[GraspResult]:
        """
        Command the arm to move to `target_pose`.

        In this scaffolded implementation the arm motion is a no-op when
        self.arm is None (dry-run / mock mode).  Real integration with
        Stage 3 / Stage 2 trajectory generation happens here.

        Returns None on success, or a GraspResult on failure.
        """
        if self._abort_requested:
            return self._fail(GraspResult.ABORTED, "abort requested")

        if self.arm is None:
            # Dry-run: simulate motion delay
            logger.debug("DRY-RUN: would move arm to\n%s", target_pose)
            time.sleep(0.01)
            return None

        # --- Real arm motion (stub for Stage 2/3 integration) ---
        # When Stage 2 (MoveIt2) and Stage 3 (ComputedTorquePDController) are
        # available, this method should:
        #   1. Convert target_pose to a joint configuration via IK (Stage 2).
        #   2. Generate a trajectory to that configuration (Stage 2 / MoveIt2).
        #   3. Execute the trajectory using Stage 3's controller.step() at 1 kHz.
        #
        # The TODO marker below is the integration point.
        # TODO(stage4-arm-motion): call Stage 2 IK + trajectory generation,
        #   then execute via Stage 3 ComputedTorquePDController.
        raise NotImplementedError(
            "Real arm motion not yet wired. "
            "Pass arm_controller=None for dry-run, or implement the "
            "Stage 2/3 integration at the TODO marker in _move_arm()."
        )

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
