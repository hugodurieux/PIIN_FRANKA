"""
Stage 4 dry-run: validates the full pick/place state machine without hardware.

Uses MockGripperController and arm_controller=None (no ROS2, no Pinocchio,
no trained model required).  Run this to confirm the orchestration logic,
state transitions, and abort path all work correctly.

Run from the project root:
    python -m stage4.dry_run
"""

from __future__ import annotations

import logging
import sys

import numpy as np

from stage4.grasp_config import GraspConfig
from stage4.gripper_controller import MockGripperController, GripperState
from stage4.grasp_executor import GraspExecutor, GraspResult, GraspPhase
from stage4.demo_targets import get_target, list_targets

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s  %(name)s  %(message)s",
)
logger = logging.getLogger("stage4.dry_run")


def _assert(condition: bool, msg: str) -> None:
    if not condition:
        logger.error("ASSERTION FAILED: %s", msg)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Test 1 — Successful pick + place
# ---------------------------------------------------------------------------

def test_pick_place_success() -> None:
    logger.info("=== Test 1: successful pick + place ===")

    cfg     = GraspConfig(grasp_width=0.04, grasp_force=20.0, object_mass=0.2)
    gripper = MockGripperController(simulate_success=True)
    executor = GraspExecutor(cfg, gripper, arm_controller=None)

    _assert(executor.phase == GraspPhase.IDLE, "initial phase must be IDLE")

    pick_pose  = get_target("box_center")
    place_pose = get_target("place_tray")

    result = executor.pick(pick_pose)
    _assert(result == GraspResult.SUCCESS, f"pick() returned {result}")
    _assert(executor.phase == GraspPhase.HOLDING, f"phase after pick: {executor.phase}")

    # Verify gripper actually closed
    status = gripper.read()
    _assert(status.is_grasped, "gripper should report grasped after pick")
    _assert(status.width == cfg.grasp_width, f"gripper width: {status.width}")

    result = executor.place(place_pose)
    _assert(result == GraspResult.SUCCESS, f"place() returned {result}")
    _assert(executor.phase == GraspPhase.IDLE, f"phase after place: {executor.phase}")

    # Verify gripper opened after place
    status = gripper.read()
    _assert(not status.is_grasped, "gripper should be open after place")

    logger.info("Test 1 PASSED")


# ---------------------------------------------------------------------------
# Test 2 — Gripper failure (object not detected)
# ---------------------------------------------------------------------------

def test_grasp_failure() -> None:
    logger.info("=== Test 2: gripper reports no contact ===")

    cfg      = GraspConfig(grasp_width=0.04, grasp_force=20.0)
    gripper  = MockGripperController(simulate_success=False)
    executor = GraspExecutor(cfg, gripper, arm_controller=None)

    result = executor.pick(get_target("box_center"))
    _assert(result == GraspResult.GRIPPER_FAILED, f"expected GRIPPER_FAILED, got {result}")
    _assert(executor.phase == GraspPhase.ABORTED, f"phase: {executor.phase}")

    logger.info("Test 2 PASSED")


# ---------------------------------------------------------------------------
# Test 3 — Abort during approach
# ---------------------------------------------------------------------------

def test_abort() -> None:
    logger.info("=== Test 3: abort() during sequence ===")

    cfg      = GraspConfig(grasp_width=0.04, grasp_force=20.0)
    gripper  = MockGripperController(simulate_success=True)
    executor = GraspExecutor(cfg, gripper, arm_controller=None)

    # Trigger abort before pick so the abort flag is set
    executor.abort()
    result = executor.pick(get_target("box_center"))
    _assert(result == GraspResult.ABORTED, f"expected ABORTED, got {result}")
    _assert(executor.phase == GraspPhase.ABORTED, f"phase: {executor.phase}")

    logger.info("Test 3 PASSED")


# ---------------------------------------------------------------------------
# Test 4 — GraspConfig validation
# ---------------------------------------------------------------------------

def test_config_defaults() -> None:
    logger.info("=== Test 4: GraspConfig defaults ===")

    cfg = GraspConfig()
    _assert(0 < cfg.grasp_width <= 0.08, "grasp_width out of Franka Hand range")
    _assert(0 < cfg.grasp_force <= 70.0, "grasp_force out of Franka Hand range")
    _assert(cfg.open_width <= 0.08,      "open_width exceeds hardware max")
    _assert(cfg.pre_approach_height > 0, "pre_approach_height must be positive")
    _assert(cfg.lift_height > 0,         "lift_height must be positive")

    logger.info("Test 4 PASSED")


# ---------------------------------------------------------------------------
# Test 5 — demo_targets
# ---------------------------------------------------------------------------

def test_demo_targets() -> None:
    logger.info("=== Test 5: demo_targets ===")

    names = list_targets()
    _assert(len(names) > 0, "no targets defined")

    for name in names:
        pose = get_target(name)
        _assert(pose.shape == (4, 4), f"target '{name}' has wrong shape: {pose.shape}")
        _assert(np.allclose(pose[3], [0, 0, 0, 1]), f"target '{name}' last row not [0,0,0,1]")
        R = pose[:3, :3]
        _assert(
            np.allclose(R @ R.T, np.eye(3), atol=1e-9),
            f"target '{name}' rotation not orthogonal",
        )

    # Test copy safety
    p1 = get_target("box_center")
    p2 = get_target("box_center")
    p1[0, 3] += 99.0
    _assert(p2[0, 3] != p1[0, 3], "get_target should return independent copies")

    # Test unknown key
    try:
        get_target("does_not_exist")
        _assert(False, "should have raised KeyError")
    except KeyError:
        pass

    logger.info("Test 5 PASSED")


# ---------------------------------------------------------------------------
# Test 6 — MockGripperController state transitions
# ---------------------------------------------------------------------------

def test_mock_gripper_states() -> None:
    logger.info("=== Test 6: MockGripperController state transitions ===")

    g = MockGripperController(simulate_success=True)

    g.homing()
    s = g.read()
    _assert(s.width == 0.08, f"after homing width={s.width}")
    _assert(s.state == GripperState.OPEN, f"after homing state={s.state}")

    g.open(width=0.06, speed=0.05)
    _assert(g.read().width == 0.06, "open() should set width")

    ok = g.grasp(width=0.04, speed=0.05, force=20.0,
                 epsilon_inner=0.005, epsilon_outer=0.01)
    _assert(ok, "grasp should succeed")
    _assert(g.read().is_grasped, "gripper should report grasped")
    _assert(g.read().state == GripperState.GRASPING, "state should be GRASPING")

    g.stop()
    _assert(not g.read().is_grasped, "stop() should clear grasped flag")

    logger.info("Test 6 PASSED")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    logger.info("Stage 4 dry-run starting (no hardware required)")
    logger.info("Available targets: %s", list_targets())

    test_config_defaults()
    test_demo_targets()
    test_mock_gripper_states()
    test_pick_place_success()
    test_grasp_failure()
    test_abort()

    logger.info("")
    logger.info("All Stage 4 dry-run tests PASSED")


if __name__ == "__main__":
    main()
