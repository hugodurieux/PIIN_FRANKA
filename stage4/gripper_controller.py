"""
Franka Hand gripper controller for Stage 4 force-controlled grasping.

Architecture:
  BaseGripperController  — abstract interface
  FrankaROS2GripperController — concrete implementation via ROS2 action clients
      (franka_gripper/action/Grasp, Move, Homing)
  MockGripperController  — in-process mock for unit tests / CI without hardware

The ROS2 implementation targets franka_ros2 (ROS2 Humble) with the standard
franka_gripper package. Action server names follow the franka_ros2 defaults:
  /fr3/franka_gripper/grasp
  /fr3/franka_gripper/move
  /fr3/franka_gripper/homing
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

import numpy as np


class GripperState(Enum):
    OPEN = auto()
    CLOSED = auto()
    GRASPING = auto()
    UNKNOWN = auto()


@dataclass
class GripperStatus:
    """Snapshot of the gripper state returned by read()."""
    width: float          # current finger separation [m]
    max_width: float      # hardware maximum [m]
    is_grasped: bool      # True if the gripper reports a successful grasp
    temperature: float    # motor temperature [°C], -1 if unavailable
    state: GripperState


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class BaseGripperController(ABC):
    """Minimal interface that all gripper backends must implement."""

    @abstractmethod
    def homing(self, timeout: float = 10.0) -> bool:
        """
        Run the gripper homing procedure (calibrates the encoder).
        Must be called once before any grasp command.

        Returns True on success.
        """

    @abstractmethod
    def open(self, width: float, speed: float, timeout: float = 5.0) -> bool:
        """
        Open fingers to `width` [m] at `speed` [m/s].

        Returns True if the target width was reached within tolerance.
        """

    @abstractmethod
    def grasp(
        self,
        width: float,
        speed: float,
        force: float,
        epsilon_inner: float,
        epsilon_outer: float,
        timeout: float = 5.0,
    ) -> bool:
        """
        Close fingers until contact at `force` [N].

        The action succeeds if the final width is in
        [width - epsilon_inner, width + epsilon_outer].

        Returns True on success (object grasped).
        """

    @abstractmethod
    def read(self) -> GripperStatus:
        """Return the current gripper status."""

    @abstractmethod
    def stop(self) -> None:
        """Emergency stop — cut motor power immediately."""


# ---------------------------------------------------------------------------
# ROS2 implementation
# ---------------------------------------------------------------------------

class FrankaROS2GripperController(BaseGripperController):
    """
    Gripper controller backed by franka_ros2 action servers.

    Requires a live ROS2 Humble environment with franka_gripper running.
    Import is deferred so the module can be imported in non-ROS environments
    (the class will raise ImportError at construction time, not import time).

    Args:
        node_name: Name of the ROS2 node this controller creates.
        robot_name: Prefix used in action server names (default "fr3").
        timeout_wait: How long to wait for action servers to come up [s].
    """

    def __init__(
        self,
        node_name: str = "stage4_gripper",
        robot_name: str = "fr3",
        timeout_wait: float = 5.0,
    ) -> None:
        try:
            import rclpy
            from rclpy.action import ActionClient
            from franka_msgs.action import Grasp, Move, Homing
        except ImportError as exc:
            raise ImportError(
                "ROS2 + franka_msgs are required for FrankaROS2GripperController. "
                "Either install them or use MockGripperController for testing."
            ) from exc

        rclpy.init()
        self._node = rclpy.create_node(node_name)

        prefix = f"/{robot_name}/franka_gripper"
        self._grasp_client = ActionClient(self._node, Grasp, f"{prefix}/grasp")
        self._move_client  = ActionClient(self._node, Move,  f"{prefix}/move")
        self._home_client  = ActionClient(self._node, Homing, f"{prefix}/homing")

        # Wait for servers
        for client, name in [
            (self._grasp_client, "grasp"),
            (self._move_client,  "move"),
            (self._home_client,  "homing"),
        ]:
            if not client.wait_for_server(timeout_sec=timeout_wait):
                raise RuntimeError(
                    f"Action server '{prefix}/{name}' not available after "
                    f"{timeout_wait}s — is franka_gripper running?"
                )

        self._Grasp      = Grasp
        self._Move       = Move
        self._Homing     = Homing
        self._rclpy      = rclpy
        self._robot_name = robot_name
        self._setup_state_subscriber()

    def _send_goal_sync(self, client, goal, timeout: float):
        """Send an action goal and block until it completes or times out."""
        import rclpy
        future = client.send_goal_async(goal)
        deadline = time.monotonic() + timeout
        while not future.done():
            rclpy.spin_once(self._node, timeout_sec=0.05)
            if time.monotonic() > deadline:
                return None
        goal_handle = future.result()
        if not goal_handle.accepted:
            return None
        result_future = goal_handle.get_result_async()
        while not result_future.done():
            rclpy.spin_once(self._node, timeout_sec=0.05)
            if time.monotonic() > deadline:
                return None
        return result_future.result()

    def homing(self, timeout: float = 10.0) -> bool:
        goal = self._Homing.Goal()
        result = self._send_goal_sync(self._home_client, goal, timeout)
        return result is not None

    def open(self, width: float, speed: float, timeout: float = 5.0) -> bool:
        goal = self._Move.Goal()
        goal.width = float(width)
        goal.speed = float(speed)
        result = self._send_goal_sync(self._move_client, goal, timeout)
        return result is not None and result.result.success

    def grasp(
        self,
        width: float,
        speed: float,
        force: float,
        epsilon_inner: float,
        epsilon_outer: float,
        timeout: float = 5.0,
    ) -> bool:
        goal = self._Grasp.Goal()
        goal.width          = float(width)
        goal.speed          = float(speed)
        goal.force          = float(force)
        goal.epsilon.inner  = float(epsilon_inner)
        goal.epsilon.outer  = float(epsilon_outer)
        result = self._send_goal_sync(self._grasp_client, goal, timeout)
        return result is not None and result.result.success

    def _setup_state_subscriber(self) -> None:
        """
        Subscribe to the gripper joint_states topic to track finger width.

        franka_gripper publishes sensor_msgs/JointState on
        /{robot_name}/franka_gripper/joint_states with two joints:
          [0] panda_finger_joint1  — position = half the total width
          [1] panda_finger_joint2  — mirror of joint1

        Called once from __init__ after action clients are confirmed live.
        """
        from sensor_msgs.msg import JointState as JointStateMsg
        self._gripper_width: float = float("nan")
        self._gripper_is_grasped: bool = False

        topic = f"/{self._robot_name}/franka_gripper/joint_states"

        def _cb(msg: JointStateMsg) -> None:
            if len(msg.position) >= 2:
                # Total width = sum of both finger positions
                self._gripper_width = float(msg.position[0] + msg.position[1])

        self._node.create_subscription(JointStateMsg, topic, _cb, 10)

    def read(self) -> GripperStatus:
        import rclpy
        rclpy.spin_once(self._node, timeout_sec=0.0)  # flush pending callbacks
        width = self._gripper_width
        is_grasped = self._gripper_is_grasped
        if np.isnan(width):
            state = GripperState.UNKNOWN
        elif is_grasped:
            state = GripperState.GRASPING
        elif width >= 0.075:
            state = GripperState.OPEN
        else:
            state = GripperState.CLOSED
        return GripperStatus(
            width=width,
            max_width=0.08,
            is_grasped=is_grasped,
            temperature=-1.0,
            state=state,
        )

    def stop(self) -> None:
        # franka_ros2 has no dedicated "stop" action; cancel all active goals.
        for client in (self._grasp_client, self._move_client):
            try:
                client._cancel_goal_async(client._goal_handle)
            except Exception:
                pass
        self._node.get_logger().warn("stop(): cancelled active gripper goals")


# ---------------------------------------------------------------------------
# Mock implementation (no hardware / no ROS2 required)
# ---------------------------------------------------------------------------

class MockGripperController(BaseGripperController):
    """
    In-process mock that simulates the Franka Hand without hardware.

    Useful for unit tests, CI, and dry-runs of the GraspExecutor state machine.
    The `simulate_success` flag controls whether grasp() returns True or False.
    """

    HARDWARE_MAX_WIDTH = 0.08  # m

    def __init__(self, simulate_success: bool = True) -> None:
        self._width = self.HARDWARE_MAX_WIDTH
        self._is_grasped = False
        self._simulate_success = simulate_success

    def homing(self, timeout: float = 10.0) -> bool:
        self._width = self.HARDWARE_MAX_WIDTH
        self._is_grasped = False
        return True

    def open(self, width: float, speed: float, timeout: float = 5.0) -> bool:
        self._width = min(width, self.HARDWARE_MAX_WIDTH)
        self._is_grasped = False
        return True

    def grasp(
        self,
        width: float,
        speed: float,
        force: float,
        epsilon_inner: float,
        epsilon_outer: float,
        timeout: float = 5.0,
    ) -> bool:
        if self._simulate_success:
            self._width = width
            self._is_grasped = True
        return self._simulate_success

    def read(self) -> GripperStatus:
        state = GripperState.GRASPING if self._is_grasped else GripperState.OPEN
        return GripperStatus(
            width=self._width,
            max_width=self.HARDWARE_MAX_WIDTH,
            is_grasped=self._is_grasped,
            temperature=-1.0,
            state=state,
        )

    def stop(self) -> None:
        self._is_grasped = False
