"""
Stage 2 -- ROS2 Jazzy controller node for the PINN Franka pipeline.

PLAN (3 sentences):
This node bridges MoveIt2 trajectory output with the PINN-based torque controller
by subscribing to joint states and desired trajectories, interpolating the desired
state at each control tick, and publishing effort commands.  It serves goal.md
objective #2 (high-frequency real-time control at 1000 Hz) by running a timer-driven
control loop at the configured rate.  Torque computation is delegated to Stage 3's
ComputedTorquePDController.

Topics
------
Subscribes:
    isaac_joint_states                    (sensor_msgs/JointState)
    /pinn_controller/desired_trajectory   (trajectory_msgs/JointTrajectory)
Publishes:
    isaac_joint_commands                  (sensor_msgs/JointState, effort field only)

Default topic names match Isaac Sim's ROS2 bridge (isaacsim.ros2.bridge
ROS2PublishJointState / ROS2SubscribeJointState -> IsaacArticulationController,
which accepts effort commands directly). Remap both via --ros-args --remap for a
different target (e.g. a future real-hardware franka_ros2 setup).

Parameters
----------
    urdf_path          (str)   -- path to the Franka URDF (needed by the controller)
    checkpoint_path    (str)   -- path to the trained PINN checkpoint (.pt)
    delta              (float) -- payload mass in kg, default 0.0 (see network/constants.PAYLOADS)
    control_rate_hz    (int)   -- control loop frequency, default 1000
    use_lyapunov_gains (bool)  -- whether Stage 3 should use Lyapunov-derived gains
                                  (True) or the conservative manual fallback (False)
"""

from __future__ import annotations

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.time import Time

from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory

from pinn_franka_controller.trajectory_interpolator import TrajectoryInterpolator

try:
    from network.constants import N_JOINTS as _N_JOINTS
    from network.constants import TORQUE_LIMITS as _TORQUE_LIMITS_TENSOR
    _TORQUE_LIMITS_NP = _TORQUE_LIMITS_TENSOR.numpy()
except ImportError:
    # Fallback when network package is not on the ROS2 Python path.
    # Values must match network/constants.py exactly: [87,87,87,87,12,12,12] Nm.
    _N_JOINTS = 7
    _TORQUE_LIMITS_NP = np.array([87.0, 87.0, 87.0, 87.0, 12.0, 12.0, 12.0])

# Franka Panda arm joint names, matching pinocchio_baseline/panda.urdf and the
# Isaac Sim Franka USD asset.
_JOINT_NAMES = [f"panda_joint{i}" for i in range(1, 8)]

# Maximum age (seconds) for a joint-state message before it is considered stale.
_JOINT_STATE_TIMEOUT_SEC = 0.1

# Maximum age (seconds) for a trajectory before the node stops tracking it.
_TRAJECTORY_STALE_SEC = 2.0


class PinnControllerNode(Node):
    """ROS2 node that runs the PINN torque controller at a configurable rate.

    The node interpolates a desired trajectory at each control tick, feeds the
    desired and measured states into the controller, and publishes the resulting
    joint torques.  If the controller failed to load (bad/missing checkpoint or
    URDF path) or no valid trajectory/state is present yet, it publishes zero
    torques as a safe fallback.
    """

    def __init__(self) -> None:
        super().__init__("pinn_franka_controller")

        # -----------------------------------------------------------------
        # Declare ROS2 parameters
        # -----------------------------------------------------------------
        self.declare_parameter("urdf_path", "")
        self.declare_parameter("checkpoint_path", "")
        self.declare_parameter("delta", 0.0)
        self.declare_parameter("control_rate_hz", 1000)
        self.declare_parameter("use_lyapunov_gains", True)

        self._urdf_path: str = (
            self.get_parameter("urdf_path").get_parameter_value().string_value
        )
        self._checkpoint_path: str = (
            self.get_parameter("checkpoint_path").get_parameter_value().string_value
        )
        self._delta: float = (
            self.get_parameter("delta").get_parameter_value().double_value
        )
        self._control_rate_hz: int = (
            self.get_parameter("control_rate_hz").get_parameter_value().integer_value
        )
        self._use_lyapunov_gains: bool = (
            self.get_parameter("use_lyapunov_gains").get_parameter_value().bool_value
        )

        # -----------------------------------------------------------------
        # State variables
        # -----------------------------------------------------------------
        self._joint_state: JointState | None = None
        self._joint_state_stamp: Time | None = None
        self._trajectory_interpolator: TrajectoryInterpolator | None = None
        self._trajectory_stamp: Time | None = None
        self._controller = None  # Will hold the Stage 3 controller instance

        # -----------------------------------------------------------------
        # Attempt to load the Stage 3 controller
        # -----------------------------------------------------------------
        self._try_load_controller()

        # -----------------------------------------------------------------
        # Subscribers
        # -----------------------------------------------------------------
        self._sub_joint_state = self.create_subscription(
            JointState,
            "isaac_joint_states",
            self._joint_state_cb,
            10,
        )
        self._sub_trajectory = self.create_subscription(
            JointTrajectory,
            "/pinn_controller/desired_trajectory",
            self._trajectory_cb,
            10,
        )

        # -----------------------------------------------------------------
        # Publisher
        # -----------------------------------------------------------------
        self._pub_torques = self.create_publisher(
            JointState,
            "isaac_joint_commands",
            10,
        )

        # -----------------------------------------------------------------
        # Control-loop timer
        # -----------------------------------------------------------------
        timer_period_sec = 1.0 / max(self._control_rate_hz, 1)
        self._timer = self.create_timer(timer_period_sec, self._control_loop)

        self.get_logger().info(
            f"PinnControllerNode started "
            f"(rate={self._control_rate_hz} Hz, delta={self._delta:.2f}, "
            f"lyapunov_gains={self._use_lyapunov_gains})"
        )

    # -----------------------------------------------------------------
    # Controller loading
    # -----------------------------------------------------------------

    def _try_load_controller(self) -> None:
        """Instantiate the Stage 3 ComputedTorquePDController.

        Falls back to zero-torque safe mode (self._controller stays None) if
        the required parameters are missing or loading fails -- a bad
        checkpoint/URDF path should never crash the node, it should just
        withhold torque commands.
        """
        if not self._checkpoint_path:
            self.get_logger().warn(
                "No checkpoint_path set -- controller disabled, publishing zero "
                "torques.  Set the 'checkpoint_path' parameter to enable control."
            )
            return

        if not self._urdf_path:
            self.get_logger().error(
                "checkpoint_path is set but urdf_path is empty -- controller "
                "disabled, publishing zero torques.  Set the 'urdf_path' "
                "parameter (needed by RNEA)."
            )
            return

        from controller import (
            ComputedTorquePDController,
            DEFAULT_KP,
            DEFAULT_KD,
            MANUAL_PD_KP,
            MANUAL_PD_KD,
        )

        kp, kd = (DEFAULT_KP, DEFAULT_KD) if self._use_lyapunov_gains else (
            MANUAL_PD_KP,
            MANUAL_PD_KD,
        )

        try:
            self._controller = ComputedTorquePDController(
                urdf_path=self._urdf_path,
                checkpoint_path=self._checkpoint_path,
                delta=self._delta,
                device="cpu",
                kp=kp,
                kd=kd,
            )
        except Exception:
            self.get_logger().error(
                "Failed to construct ComputedTorquePDController -- controller "
                "disabled, publishing zero torques.",
                exc_info=True,
            )
            self._controller = None
            return

        self.get_logger().info(
            f"Stage 3 controller loaded "
            f"(urdf={self._urdf_path}, checkpoint={self._checkpoint_path}, "
            f"gains={'lyapunov' if self._use_lyapunov_gains else 'manual'})."
        )

    # -----------------------------------------------------------------
    # Subscriber callbacks
    # -----------------------------------------------------------------

    def _joint_state_cb(self, msg: JointState) -> None:
        """Store the latest joint-state message."""
        self._joint_state = msg
        self._joint_state_stamp = self.get_clock().now()

    def _trajectory_cb(self, msg: JointTrajectory) -> None:
        """Store a new desired trajectory and build an interpolator."""
        if len(msg.points) == 0:
            self.get_logger().warn("Received empty trajectory -- ignoring.")
            return

        self._trajectory_interpolator = TrajectoryInterpolator(
            msg, n_joints=_N_JOINTS
        )
        self._trajectory_stamp = self.get_clock().now()
        self.get_logger().info(
            f"New trajectory received with {len(msg.points)} points."
        )

    # -----------------------------------------------------------------
    # Control loop
    # -----------------------------------------------------------------

    def _control_loop(self) -> None:
        """Called at ``control_rate_hz`` Hz.  Computes and publishes torques."""
        now = self.get_clock().now()

        # --- Guard: no joint state yet --------------------------------
        if self._joint_state is None or self._joint_state_stamp is None:
            self._publish_zero_torques()
            return

        # --- Guard: joint state too old -------------------------------
        js_age_sec = (now - self._joint_state_stamp).nanoseconds * 1e-9
        if js_age_sec > _JOINT_STATE_TIMEOUT_SEC:
            self.get_logger().warn(
                f"Joint state stale ({js_age_sec:.3f}s > "
                f"{_JOINT_STATE_TIMEOUT_SEC}s) -- sending zero torques.",
                throttle_duration_sec=1.0,
            )
            self._publish_zero_torques()
            return

        # --- Guard: no trajectory received yet ------------------------
        if (
            self._trajectory_interpolator is None
            or self._trajectory_stamp is None
        ):
            self._publish_zero_torques()
            return

        # --- Guard: trajectory too old --------------------------------
        traj_age_sec = (now - self._trajectory_stamp).nanoseconds * 1e-9
        if traj_age_sec > _TRAJECTORY_STALE_SEC:
            self.get_logger().warn(
                f"Trajectory stale ({traj_age_sec:.1f}s > "
                f"{_TRAJECTORY_STALE_SEC}s) -- sending zero torques.",
                throttle_duration_sec=1.0,
            )
            self._publish_zero_torques()
            return

        # --- Interpolate desired state --------------------------------
        # Time within the trajectory is measured from when it was received.
        t_traj = traj_age_sec  # seconds since trajectory arrived
        q_des, qdot_des, qddot_des = self._trajectory_interpolator.interpolate(
            t_traj
        )

        # --- Extract measured state -----------------------------------
        q_meas = np.array(
            self._joint_state.position[:_N_JOINTS], dtype=np.float64
        )
        qdot_meas = np.array(
            self._joint_state.velocity[:_N_JOINTS], dtype=np.float64
        )

        # --- Compute torques ------------------------------------------
        torques = self._compute_torques(
            q_meas, qdot_meas, q_des, qdot_des, qddot_des
        )

        # --- Publish --------------------------------------------------
        self._publish_torques(torques)

    # -----------------------------------------------------------------
    # Torque computation (Stage 3)
    # -----------------------------------------------------------------

    def _compute_torques(
        self,
        q_meas: np.ndarray,
        qdot_meas: np.ndarray,
        q_des: np.ndarray,
        qdot_des: np.ndarray,
        qddot_des: np.ndarray,
    ) -> np.ndarray:
        """Compute joint torques using the Stage 3 controller.

        Parameters
        ----------
        q_meas : np.ndarray, shape (7,)
            Measured joint positions [rad].
        qdot_meas : np.ndarray, shape (7,)
            Measured joint velocities [rad/s].
        q_des : np.ndarray, shape (7,)
            Desired joint positions [rad].
        qdot_des : np.ndarray, shape (7,)
            Desired joint velocities [rad/s].
        qddot_des : np.ndarray, shape (7,)
            Desired joint accelerations [rad/s^2].

        Returns
        -------
        np.ndarray, shape (7,)
            Joint torques [Nm].
        """
        if self._controller is not None:
            return self._controller.step(
                q_meas, qdot_meas, q_des, qdot_des, qddot_des
            )

        # Safe fallback: zero torques (robot holds position via its own
        # gravity compensation if available, or is e-stopped).
        return np.zeros(_N_JOINTS, dtype=np.float64)

    # -----------------------------------------------------------------
    # Publishing helpers
    # -----------------------------------------------------------------

    def _publish_torques(self, torques: np.ndarray) -> None:
        """Publish a JointState with the 7 joint efforts (positions/velocities
        left empty so Isaac's ArticulationController only applies the effort
        command)."""
        torques = np.clip(torques, -_TORQUE_LIMITS_NP, _TORQUE_LIMITS_NP)
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = _JOINT_NAMES
        msg.effort = torques.tolist()
        self._pub_torques.publish(msg)

    def _publish_zero_torques(self) -> None:
        """Publish zero torques (safe fallback)."""
        self._publish_torques(np.zeros(_N_JOINTS, dtype=np.float64))


def main(args=None) -> None:
    """Entry point for the ``pinn_controller_node`` executable."""
    rclpy.init(args=args)
    node = PinnControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down (KeyboardInterrupt).")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
