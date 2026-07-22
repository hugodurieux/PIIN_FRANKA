"""
Franka Hand gripper controller for Stage 4 force-controlled grasping.

Architecture:
  BaseGripperController  — abstract interface
  FrankaROS2GripperController — concrete implementation via ROS2 action clients
      (franka_gripper/action/Grasp, Move, Homing), targets real hardware
  MuJoCoGripperController — concrete implementation via this project's own
      panda_hand_controller (control_msgs/action/GripperCommand), targets
      the MuJoCo simulation (Stage 2/3's own stack, see
      ros2_ws/.../urdf/panda_mujoco.ros2_control.xacro and
      mujoco/franka_emika_panda/panda_arm_mujoco.xml)
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
# MuJoCo implementation (this project's own Stage 2/3 simulation stack)
# ---------------------------------------------------------------------------

class MuJoCoGripperController(BaseGripperController):
    """
    Gripper controller backed by this project's own MuJoCo/ros2_control stack.

    Targets panda_hand_controller (position_controllers/GripperActionController,
    see ros2_ws/.../launch/mujoco_franka_moveit.launch.py), which exposes a
    single control_msgs/action/GripperCommand action
    (/panda_hand_controller/gripper_cmd) driving panda_finger_joint1's real
    physics in MuJoCo -- panda_finger_joint2 follows via the MJCF's <equality>
    constraint, see mujoco/franka_emika_panda/panda_arm_mujoco.xml.

    Unlike FrankaROS2GripperController's three separate actions
    (Grasp/Move/Homing), GripperCommand is a single, simpler action: a target
    position + max_effort, with the result reporting whether the goal was
    reached or the gripper stalled. That "stalled" signal is genuinely
    ambiguous on its own -- it means success when closing against a real
    object (the fingers can't reach the fully-closed target because something
    is in the way), and meant failure during this project's own 2026-07-22
    actuator-tuning session (an underdamped actuator overshooting past its
    own joint limits before settling). grasp() below disambiguates the same
    way the real franka_gripper Grasp action does: by checking whether the
    final width, whatever it settled at, falls within the requested
    epsilon tolerance band, not by trusting "stalled" alone.

    width (this class's units, matching BaseGripperController's own
    docstrings and HARDWARE_MAX_WIDTH=0.08) is the TOTAL separation between
    the two fingers. The actuator only drives panda_finger_joint1 directly
    (MJCF range 0-0.04, i.e. half of the total width), so width is halved
    before being sent as the action's `position` field, and doubled back when
    reading a result.

    speed is accepted on open()/grasp() for interface compatibility with
    BaseGripperController but is NOT used: GripperCommand has no speed field,
    and neither GripperActionController nor the MuJoCo position actuator
    expose a runtime speed knob -- motion speed here is entirely a function
    of the actuator's own kp/kv tuning (see the MJCF actuator's own comment).
    """

    HARDWARE_MAX_WIDTH = 0.08  # m, matches MockGripperController and grasp_config.py

    # Matches the MJCF actuator's own forcerange (panda_finger_joint1_position,
    # panda_arm_mujoco.xml) -- used as the default max_effort for open()/homing(),
    # which (unlike grasp()) have no force parameter of their own to use instead.
    _DEFAULT_MAX_EFFORT = 20.0

    def __init__(
        self,
        node_name: str = "stage4_gripper_mujoco",
        controller_name: str = "panda_hand_controller",
        timeout_wait: float = 5.0,
    ) -> None:
        try:
            import rclpy
            from rclpy.action import ActionClient
            from control_msgs.action import GripperCommand
            from sensor_msgs.msg import JointState as JointStateMsg
        except ImportError as exc:
            raise ImportError(
                "ROS2 + control_msgs are required for MuJoCoGripperController. "
                "Either install them or use MockGripperController for testing."
            ) from exc

        rclpy.init()
        self._node = rclpy.create_node(node_name)
        self._rclpy = rclpy
        self._GripperCommand = GripperCommand

        action_name = f"/{controller_name}/gripper_cmd"
        self._client = ActionClient(self._node, GripperCommand, action_name)
        if not self._client.wait_for_server(timeout_sec=timeout_wait):
            raise RuntimeError(
                f"Action server '{action_name}' not available after "
                f"{timeout_wait}s — is panda_hand_controller active?"
            )

        # Populated by _joint_state_cb from the shared /joint_states topic (9 joints,
        # 7 arm + 2 fingers, alphabetically sorted by joint_state_broadcaster) --
        # looked up BY NAME, not by fixed index: this project already found and fixed
        # a real bug elsewhere (pinn_controller_node.py, 2026-07-21) from assuming a
        # fixed positional slice on this exact topic.
        self._finger1_pos: float = float("nan")
        self._finger2_pos: float = float("nan")
        self._last_grasp_succeeded: bool = False
        self._goal_handle = None

        self._node.create_subscription(JointStateMsg, "/joint_states", self._joint_state_cb, 10)

    def _joint_state_cb(self, msg) -> None:
        for name, pos in zip(msg.name, msg.position):
            if name == "panda_finger_joint1":
                self._finger1_pos = pos
            elif name == "panda_finger_joint2":
                self._finger2_pos = pos

    def _send_goal_sync(self, position: float, max_effort: float, timeout: float):
        """Send a GripperCommand goal and block until it finishes or times out."""
        goal = self._GripperCommand.Goal()
        goal.command.position = float(position)
        goal.command.max_effort = float(max_effort)

        future = self._client.send_goal_async(goal)
        deadline = time.monotonic() + timeout
        while not future.done():
            self._rclpy.spin_once(self._node, timeout_sec=0.05)
            if time.monotonic() > deadline:
                return None
        goal_handle = future.result()
        if not goal_handle.accepted:
            return None
        self._goal_handle = goal_handle

        result_future = goal_handle.get_result_async()
        while not result_future.done():
            self._rclpy.spin_once(self._node, timeout_sec=0.05)
            if time.monotonic() > deadline:
                return None
        return result_future.result().result

    def homing(self, timeout: float = 10.0) -> bool:
        # No physical encoder to calibrate in simulation; reinterpreted as moving
        # to a known reference state (fully open) instead of a true no-op, so it
        # still does something meaningful before the first real grasp attempt.
        return self.open(width=self.HARDWARE_MAX_WIDTH, speed=0.1, timeout=timeout)

    def open(self, width: float, speed: float, timeout: float = 5.0) -> bool:
        result = self._send_goal_sync(
            position=width / 2.0, max_effort=self._DEFAULT_MAX_EFFORT, timeout=timeout
        )
        self._last_grasp_succeeded = False
        if result is None:
            return False
        return bool(result.reached_goal)

    def grasp(
        self,
        width: float,
        speed: float,
        force: float,
        epsilon_inner: float,
        epsilon_outer: float,
        timeout: float = 5.0,
    ) -> bool:
        result = self._send_goal_sync(position=width / 2.0, max_effort=force, timeout=timeout)
        if result is None:
            self._last_grasp_succeeded = False
            return False
        final_width = 2.0 * result.position
        success = (width - epsilon_inner) <= final_width <= (width + epsilon_outer)
        self._last_grasp_succeeded = success
        return success

    def read(self) -> GripperStatus:
        # 2026-07-22 correction: a zero-timeout spin_once does not wait at all --
        # it only picks up whatever was ALREADY sitting in the queue at that
        # exact instant, so even looping it many times in a tight burst (tried
        # first) can complete faster than a genuinely fresh message arrives and
        # still return stale, mid-action data (confirmed live: open() correctly
        # reported reached_goal=True, but a read() immediately after, using that
        # zero-timeout loop, still showed a partially-closed width). /joint_states
        # publishes at ~500 Hz, so spinning with a real, nonzero timeout for a
        # short window guarantees picking up several genuinely fresh messages.
        deadline = time.monotonic() + 0.1
        while time.monotonic() < deadline:
            self._rclpy.spin_once(self._node, timeout_sec=0.02)
        if np.isnan(self._finger1_pos) or np.isnan(self._finger2_pos):
            width = float("nan")
        else:
            width = self._finger1_pos + self._finger2_pos
        if np.isnan(width):
            state = GripperState.UNKNOWN
        elif self._last_grasp_succeeded:
            state = GripperState.GRASPING
        elif width >= 0.065:
            # 0.075 (FrankaROS2GripperController's threshold, copied initially)
            # was too strict for this actuator's actual observed settling
            # values: open() reliably lands around 0.072-0.08, not pinned
            # exactly at 0.08, which read as CLOSED under the tighter
            # threshold. 0.065 cleanly separates open (~0.07-0.08) from
            # closed/grasping (~0.04-0.06) as actually observed live.
            state = GripperState.OPEN
        else:
            state = GripperState.CLOSED
        return GripperStatus(
            width=width,
            max_width=self.HARDWARE_MAX_WIDTH,
            is_grasped=self._last_grasp_succeeded,
            temperature=-1.0,
            state=state,
        )

    def stop(self) -> None:
        if self._goal_handle is not None:
            try:
                self._goal_handle.cancel_goal_async()
            except Exception:
                pass
        self._node.get_logger().warn("stop(): cancelled active gripper goal")


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
