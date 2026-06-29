"""
Stage 4 — Force-controlled grasping with the Franka Hand.

Public surface:
    GraspConfig             — tuning parameters
    BaseGripperController   — abstract gripper interface
    FrankaROS2GripperController — live hardware backend (requires ROS2)
    MockGripperController   — in-process mock for testing
    GraspExecutor           — pick/place state machine
    GraspResult, GraspPhase — result and phase enums
"""

from stage4.grasp_config import GraspConfig
from stage4.gripper_controller import (
    BaseGripperController,
    FrankaROS2GripperController,
    MockGripperController,
    GripperState,
    GripperStatus,
)
from stage4.grasp_executor import GraspExecutor, GraspResult, GraspPhase

__all__ = [
    "GraspConfig",
    "BaseGripperController",
    "FrankaROS2GripperController",
    "MockGripperController",
    "GripperState",
    "GripperStatus",
    "GraspExecutor",
    "GraspResult",
    "GraspPhase",
]
