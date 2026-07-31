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
    joint_states                          (sensor_msgs/JointState)
    /pinn_controller/desired_trajectory   (trajectory_msgs/JointTrajectory)
Publishes:
    /panda_effort_controller/commands     (std_msgs/Float64MultiArray, one value
                                            per joint in _JOINT_NAMES order)

Default topic names match mujoco_ros2_control's ros2_control setup (see
ros2_ws/src/pinn_franka_controller/launch/mujoco_franka_moveit.launch.py):
joint_states is published by the standard joint_state_broadcaster, and
/panda_effort_controller/commands is claimed by a
forward_command_controller/ForwardCommandController (interface_name: effort,
see config/mujoco_effort_controller.yaml) that writes straight through to the
MuJoCo motor actuators. Remap both via --ros-args --remap for a different
target (e.g. a future real-hardware franka_ros2 setup).

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

import traceback

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.time import Time

from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
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

# Franka Panda arm joint names, matching pinocchio_baseline/panda.urdf. Also
# the joint order expected by panda_effort_controller's Float64MultiArray
# commands (config/mujoco_effort_controller.yaml's `joints:` list), since that
# message type carries no per-element names -- order is the only contract.
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
        # 2026-07-24 TEMPORARY DEBUG (Stage 3 investigation, remove once
        # resolved): panda_joint4/6/7 show a large, real, persistent position
        # error under active tracking with substantial correctly-signed PD
        # torque computed, yet zero measured displacement -- confirmed NOT a
        # collision (identical freeze with grasp_object moved 2.5m out of
        # reach). Default -1.0 preserves existing behavior exactly (uses
        # DEFAULT_KP/DEFAULT_KD or MANUAL_PD_KP/KD as before). Set > 0 (e.g.
        # 8.0) via --ros-args -p gain_safety_margin_override:=8.0 to instead
        # recompute Kp/Kd from DEFAULT_ERROR_BOUND at that safety_margin, as a
        # live empirical test of whether a much stronger PD push can move
        # these joints at all -- distinguishes "gain is simply too weak" from
        # "something else entirely is preventing motion regardless of gain."
        self.declare_parameter("gain_safety_margin_override", -1.0)
        # 2026-07-28 DIAGNOSTIC (Stage 4 investigation of the joint4/6/7
        # freeze): forwards to ComputedTorquePDController's disable_residual.
        # Default False preserves the validated tau_cmd composition exactly.
        # Set true via --ros-args -p disable_residual:=true to run RNEA+PD
        # only (learned GreyBoxNet/FrictionNet never called), isolating
        # whether the trained residual model is a factor in the freeze.
        self.declare_parameter("disable_residual", False)

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
        self._gain_safety_margin_override: float = (
            self.get_parameter("gain_safety_margin_override")
            .get_parameter_value()
            .double_value
        )
        self._disable_residual: bool = (
            self.get_parameter("disable_residual").get_parameter_value().bool_value
        )

        # -----------------------------------------------------------------
        # State variables
        # -----------------------------------------------------------------
        self._joint_state: JointState | None = None
        self._joint_state_stamp: Time | None = None
        # Cache mapping _JOINT_NAMES -> indices into the JointState arrays.
        # Rebuilt whenever the incoming name list changes (see _arm_indices()).
        self._arm_index_cache: list[int] | None = None
        self._arm_index_cache_names: tuple[str, ...] | None = None
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
            "joint_states",
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
            Float64MultiArray,
            "/panda_effort_controller/commands",
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
            compute_lyapunov_gains,
        )
        from controller.lyapunov_gains import DEFAULT_ERROR_BOUND

        kp, kd = (DEFAULT_KP, DEFAULT_KD) if self._use_lyapunov_gains else (
            MANUAL_PD_KP,
            MANUAL_PD_KD,
        )

        if self._gain_safety_margin_override > 0:
            kp, kd = compute_lyapunov_gains(
                DEFAULT_ERROR_BOUND, safety_margin=self._gain_safety_margin_override
            )
            # NOTE: rclpy's RcutilsLogger.warn() takes ONE pre-formatted string --
            # it does NOT support logging-module-style lazy "%s"-plus-args calls.
            # Passing them raises TypeError and kills the node at startup, which is
            # what this call did from the day it was written (2026-07-24) until
            # 2026-07-29, meaning gain_safety_margin_override (and therefore
            # launch_pinn_controller_boosted.sh) had never once run successfully.
            _default_name = "Lyapunov" if self._use_lyapunov_gains else "manual"
            self.get_logger().warn(
                f"gain_safety_margin_override={self._gain_safety_margin_override:.2f} "
                f"active -- using recomputed Kp/Kd (diag Kp="
                f"{np.diag(kp).round(2).tolist()}) instead of the {_default_name} "
                f"default. TEMPORARY debug override, not the project's validated gains."
            )

        if self._disable_residual:
            self.get_logger().warn(
                "disable_residual=true active -- the learned GreyBoxNet/FrictionNet "
                "residual will NEVER be called, tau_cmd = tau_rnea + tau_pd only. "
                "TEMPORARY diagnostic override, not the project's validated model."
            )

        try:
            self._controller = ComputedTorquePDController(
                urdf_path=self._urdf_path,
                checkpoint_path=self._checkpoint_path,
                delta=self._delta,
                device="cpu",
                kp=kp,
                kd=kd,
                disable_residual=self._disable_residual,
            )
        except Exception:
            self.get_logger().error(
                "Failed to construct ComputedTorquePDController -- controller "
                "disabled, publishing zero torques.\n" + traceback.format_exc()
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

        # expected_joint_names=_JOINT_NAMES: reorder by name instead of
        # trusting positional order -- see TrajectoryInterpolator's own
        # 2026-07-23 docstring note for why (the same class of bug already
        # fixed once in this file's own _arm_indices(), just on the
        # trajectory-input side instead of /joint_states).
        self._trajectory_interpolator = TrajectoryInterpolator(
            msg, n_joints=_N_JOINTS, expected_joint_names=_JOINT_NAMES
        )
        self._trajectory_stamp = self.get_clock().now()
        self.get_logger().info(
            f"New trajectory received with {len(msg.points)} points."
        )

    # -----------------------------------------------------------------
    # Joint-state extraction (name-based, NOT positional)
    # -----------------------------------------------------------------

    def _arm_indices(self, msg: JointState) -> list[int] | None:
        """Return the indices of the 7 arm joints (in _JOINT_NAMES order)
        within the JointState message arrays, looked up BY NAME.

        The /joint_states topic aggregates every joint in the controller
        manager -- for this system that is the two mock gripper prismatic
        joints (panda_finger_joint1, panda_finger_joint2) AND the 7 arm
        joints. Critically, the broadcaster orders them with the finger
        joints FIRST (alphabetically 'panda_finger_*' < 'panda_joint*'), so a
        naive ``position[:7]`` slice returns
        [finger1, finger2, joint1..joint5] -- the wrong joints -- feeding RNEA
        a garbage pose. This method maps by joint name instead, and caches the
        resulting index list until the incoming name ordering changes.

        Returns None if any required arm joint name is absent from the message.
        """
        names = tuple(msg.name)
        if names != self._arm_index_cache_names:
            try:
                self._arm_index_cache = [names.index(j) for j in _JOINT_NAMES]
            except ValueError:
                self._arm_index_cache = None
                self.get_logger().error(
                    "joint_states is missing one of the arm joints "
                    f"{_JOINT_NAMES}; got names={list(names)}.",
                    throttle_duration_sec=1.0,
                )
            self._arm_index_cache_names = names
        return self._arm_index_cache

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
                f"{_JOINT_STATE_TIMEOUT_SEC}s) -- holding at last known "
                f"position via gravity compensation.",
                throttle_duration_sec=1.0,
            )
            self._publish_safe_fallback()
            return

        # --- Guard: no trajectory received yet ------------------------
        if (
            self._trajectory_interpolator is None
            or self._trajectory_stamp is None
        ):
            self._publish_safe_fallback()
            return

        # --- Guard: trajectory too old --------------------------------
        traj_age_sec = (now - self._trajectory_stamp).nanoseconds * 1e-9
        if traj_age_sec > _TRAJECTORY_STALE_SEC:
            self.get_logger().warn(
                f"Trajectory stale ({traj_age_sec:.1f}s > "
                f"{_TRAJECTORY_STALE_SEC}s) -- holding at last known "
                f"position via gravity compensation.",
                throttle_duration_sec=1.0,
            )
            self._publish_safe_fallback()
            return

        # --- Interpolate desired state --------------------------------
        # Time within the trajectory is measured from when it was received.
        t_traj = traj_age_sec  # seconds since trajectory arrived
        q_des, qdot_des, qddot_des = self._trajectory_interpolator.interpolate(
            t_traj
        )

        # --- Extract measured state (BY NAME, not by slice) -----------
        idx = self._arm_indices(self._joint_state)
        if idx is None:
            # Required arm joints not present in this message -- hold safely.
            self._publish_safe_fallback()
            return
        q_meas = np.array(
            [self._joint_state.position[i] for i in idx], dtype=np.float64
        )
        qdot_meas = np.array(
            [self._joint_state.velocity[i] for i in idx], dtype=np.float64
        )

        # 2026-07-24 TEMPORARY DEBUG (Stage 3 investigation, remove once
        # resolved): panda_joint4/6/7 show literally zero net displacement
        # under an active trajectory regardless of how large or small the
        # commanded target is (ruled out: self-collision, floor/cube contact,
        # joint-name reordering both directions, actuator ranges, effort
        # controller joint order -- all confirmed correct by code audit).
        # This logs the actual q_des/q_meas/error the controller sees for
        # those 3 joints at runtime, to distinguish "e is genuinely large but
        # the PD/gain isn't producing motion from it" (a control-law issue)
        # from "e is mysteriously near zero" (a data-delivery issue upstream
        # of this point) -- can't be told apart from the existing move_to()
        # logs, which only show the FINAL target/current, not what the
        # controller computed at each tick.
        self.get_logger().info(
            "[DEBUG e] "
            f"j4: q_des={q_des[3]:+.4f} q_meas={q_meas[3]:+.4f} e={q_des[3]-q_meas[3]:+.4f} "
            f"qdot={qdot_meas[3]:+.5f} | "
            f"j6: q_des={q_des[5]:+.4f} q_meas={q_meas[5]:+.4f} e={q_des[5]-q_meas[5]:+.4f} "
            f"qdot={qdot_meas[5]:+.5f} | "
            f"j7: q_des={q_des[6]:+.4f} q_meas={q_meas[6]:+.4f} e={q_des[6]-q_meas[6]:+.4f} "
            f"qdot={qdot_meas[6]:+.5f}",
            throttle_duration_sec=1.0,
        )

        # --- Compute torques ------------------------------------------
        torques = self._compute_torques(
            q_meas, qdot_meas, q_des, qdot_des, qddot_des
        )

        # 2026-07-24 TEMPORARY DEBUG (Stage 3 investigation, remove once
        # resolved): breakdown of the combined torque into its 3 components
        # (see computed_torque_pd.py's last_tau_rnea/last_tau_res/last_tau_pd)
        # for joints 4/6/7 -- to see whether the residual is cancelling a
        # real PD contribution, whether tau_pd itself is near-zero despite a
        # real logged e (contradicting the [DEBUG e] log above), or whether
        # the unclipped total is large (real torque wanted) vs the clipped
        # tau_cmd actually published (would mean clipping is silently
        # discarding it -- unlikely given prior torque captures stayed well
        # under TORQUE_LIMITS, but not yet directly compared side by side).
        if self._controller is not None and hasattr(self._controller, "last_tau_pd"):
            rnea, res, pd_, unclipped = (
                self._controller.last_tau_rnea,
                self._controller.last_tau_res,
                self._controller.last_tau_pd,
                self._controller.last_tau_cmd_unclipped,
            )
            self.get_logger().info(
                "[DEBUG tau] "
                f"j4: rnea={rnea[3]:+.3f} res={res[3]:+.3f} pd={pd_[3]:+.3f} "
                f"unclipped={unclipped[3]:+.3f} clipped={torques[3]:+.3f} | "
                f"j6: rnea={rnea[5]:+.3f} res={res[5]:+.3f} pd={pd_[5]:+.3f} "
                f"unclipped={unclipped[5]:+.3f} clipped={torques[5]:+.3f} | "
                f"j7: rnea={rnea[6]:+.3f} res={res[6]:+.3f} pd={pd_[6]:+.3f} "
                f"unclipped={unclipped[6]:+.3f} clipped={torques[6]:+.3f}",
                throttle_duration_sec=1.0,
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
        """Publish a Float64MultiArray of the 7 joint efforts, in _JOINT_NAMES
        order, to panda_effort_controller's command topic (Float64MultiArray
        carries no per-element names -- order is the only contract, matching
        the `joints:` list in config/mujoco_effort_controller.yaml)."""
        torques = np.clip(torques, -_TORQUE_LIMITS_NP, _TORQUE_LIMITS_NP)
        msg = Float64MultiArray()
        msg.data = torques.tolist()
        self._pub_torques.publish(msg)

    def _publish_zero_torques(self) -> None:
        """Publish zero torques (safe fallback)."""
        self._publish_torques(np.zeros(_N_JOINTS, dtype=np.float64))

    def _publish_safe_fallback(self) -> None:
        """Publish gravity-compensation torque at the last known joint
        position (qdot=0, qddot=0), instead of literal zero.

        Zero torque with no drive holding the arm up causes it to free-fall
        under gravity while waiting for a trajectory. RNEA at qdot=qddot=0
        reduces to exactly the gravity term, so this holds position without
        needing any tracking error or trajectory. Falls back to literal zero
        if the controller (and therefore RNEA) never loaded, or no joint
        state has been observed yet.
        """
        if self._controller is None or self._joint_state is None:
            self._publish_zero_torques()
            return

        idx = self._arm_indices(self._joint_state)
        if idx is None:
            self._publish_zero_torques()
            return
        q = np.array(
            [self._joint_state.position[i] for i in idx], dtype=np.float64
        )
        zeros = np.zeros(_N_JOINTS, dtype=np.float64)
        try:
            tau_grav = self._controller.rnea.compute_tau_theoretical(
                q[np.newaxis, :],
                zeros[np.newaxis, :],
                zeros[np.newaxis, :],
                delta=self._controller.delta,
            ).squeeze(0)
        except Exception:
            self.get_logger().error(
                "Gravity-compensation fallback failed -- sending zero "
                "torques instead.\n" + traceback.format_exc(),
                throttle_duration_sec=1.0,
            )
            self._publish_zero_torques()
            return

        self._publish_torques(tau_grav)


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
