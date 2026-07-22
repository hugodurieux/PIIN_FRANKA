"""
ArmMotionClient — Stage 4's arm-motion backend for GraspExecutor._move_arm().

Converts a Cartesian target_pose (a (4, 4) homogeneous transform in the
Franka base frame, see demo_targets.py's convention) into arm motion by:
  1. Planning a Cartesian-goal MoveGroup request. MoveIt2's own KDL IK
     solver (moveit_resources_panda_moveit_config's kinematics.yaml) handles
     the pose -> joint conversion internally -- no separate IK step needed.
  2. Handing the resulting trajectory to the already-running
     pinn_controller_node (Stage 3's ComputedTorquePDController) via
     /pinn_controller/desired_trajectory -- the exact same plan-then-handoff
     pattern ros2_ws/.../moveit_plan_bridge.py already validated during
     Milestone 2, just parameterized by pose instead of joint values, and
     wrapped as a reusable class (instantiate once, call move_to() many
     times across a pick sequence) instead of a one-shot CLI script.
  3. Waiting for the trajectory to actually play out (Stage 3's own 1 kHz
     loop, not this node) and confirming the arm's /joint_states converged
     near the planned trajectory's own last waypoint, not just that the
     handoff itself succeeded.

Requires a live ROS2 environment (move_group + pinn_controller_node already
running, see moveit_plan_bridge.py's own Usage docstring for the manual
launch sequence this depends on) and the caller to have already called
rclpy.init() -- this class does not call it itself, unlike
MuJoCoGripperController, since GraspExecutor's future ROS2 orchestration node
is expected to own one shared rclpy context across the arm client, the
gripper controller, and its own node.
"""

from __future__ import annotations

import time
from typing import Optional

import numpy as np
import rclpy
from geometry_msgs.msg import Pose
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import (
    Constraints,
    MoveItErrorCodes,
    OrientationConstraint,
    PositionConstraint,
)
from rclpy.action import ActionClient
from rclpy.node import Node
from sensor_msgs.msg import JointState
from shape_msgs.msg import SolidPrimitive
from trajectory_msgs.msg import JointTrajectory

# Matches pinocchio_baseline/panda.urdf and pinn_controller_node.py's own
# _JOINT_NAMES -- the arm's 7 joints, in canonical order (NOT /joint_states'
# own alphabetical-sort order, which puts the 2 finger joints first).
_JOINT_NAMES = [f"panda_joint{i}" for i in range(1, 8)]


def _rotation_matrix_to_quaternion(R: np.ndarray) -> tuple[float, float, float, float]:
    """Convert a 3x3 rotation matrix to a (x, y, z, w) quaternion (Shepperd's method)."""
    trace = np.trace(R)
    if trace > 0:
        s = 0.5 / np.sqrt(trace + 1.0)
        w = 0.25 / s
        x = (R[2, 1] - R[1, 2]) * s
        y = (R[0, 2] - R[2, 0]) * s
        z = (R[1, 0] - R[0, 1]) * s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = 2.0 * np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2])
        w = (R[2, 1] - R[1, 2]) / s
        x = 0.25 * s
        y = (R[0, 1] + R[1, 0]) / s
        z = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = 2.0 * np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2])
        w = (R[0, 2] - R[2, 0]) / s
        x = (R[0, 1] + R[1, 0]) / s
        y = 0.25 * s
        z = (R[1, 2] + R[2, 1]) / s
    else:
        s = 2.0 * np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1])
        w = (R[1, 0] - R[0, 1]) / s
        x = (R[0, 2] + R[2, 0]) / s
        y = (R[1, 2] + R[2, 1]) / s
        z = 0.25 * s
    return (x, y, z, w)


class ArmMotionClient(Node):
    """
    Args:
        node_name: Name of the ROS2 node this class creates.
        group_name: MoveIt2 planning group, default "panda_arm".
        base_frame: Planning/base frame, matches demo_targets.py's convention.
        tip_link: IK reference link, matches panda.srdf's panda_arm chain
            tip_link (confirmed: base_link="panda_link0" tip_link="panda_link8").
            NOTE: this is the flange link, not necessarily the fingertip TCP --
            demo_targets.py's existing hardcoded poses were written before any
            real IK integration existed and may need recalibrating once a real
            pick is actually attempted; not resolved here.
        planning_time: allowed_planning_time per MoveGroup request [s].
        position_tolerance: radius [m] of the spherical position constraint region.
        orientation_tolerance: per-axis orientation tolerance [rad].
    """

    def __init__(
        self,
        node_name: str = "stage4_arm_motion",
        group_name: str = "panda_arm",
        base_frame: str = "panda_link0",
        tip_link: str = "panda_link8",
        planning_time: float = 5.0,
        position_tolerance: float = 0.01,
        orientation_tolerance: float = 0.05,
    ) -> None:
        super().__init__(node_name)
        self._group_name = group_name
        self._base_frame = base_frame
        self._tip_link = tip_link
        self._planning_time = planning_time
        self._position_tolerance = position_tolerance
        self._orientation_tolerance = orientation_tolerance

        self._pub_trajectory = self.create_publisher(
            JointTrajectory, "/pinn_controller/desired_trajectory", 10
        )
        self._action_client = ActionClient(self, MoveGroup, "move_action")
        self._joint_state: Optional[JointState] = None
        self.create_subscription(JointState, "/joint_states", self._joint_state_cb, 10)

    def _joint_state_cb(self, msg: JointState) -> None:
        self._joint_state = msg

    def _current_joint_positions_by_name(self) -> Optional[dict]:
        """
        Return {joint_name: position} from the latest /joint_states message.

        Looked up BY NAME, not a fixed positional slice: /joint_states carries
        9 joints (7 arm + 2 fingers), alphabetically sorted by
        joint_state_broadcaster -- the exact class of bug already found and
        fixed in pinn_controller_node.py (2026-07-21) from assuming a fixed
        slice on this same topic.
        """
        if self._joint_state is None:
            return None
        return dict(zip(self._joint_state.name, self._joint_state.position))

    def _build_pose_constraints(self, target_pose: np.ndarray) -> Constraints:
        position = target_pose[:3, 3]
        qx, qy, qz, qw = _rotation_matrix_to_quaternion(target_pose[:3, :3])

        position_constraint = PositionConstraint()
        position_constraint.header.frame_id = self._base_frame
        position_constraint.link_name = self._tip_link
        position_constraint.constraint_region.primitives.append(
            SolidPrimitive(type=SolidPrimitive.SPHERE, dimensions=[self._position_tolerance])
        )
        region_pose = Pose()
        region_pose.position.x = float(position[0])
        region_pose.position.y = float(position[1])
        region_pose.position.z = float(position[2])
        region_pose.orientation.w = 1.0
        position_constraint.constraint_region.primitive_poses.append(region_pose)
        position_constraint.weight = 1.0

        orientation_constraint = OrientationConstraint()
        orientation_constraint.header.frame_id = self._base_frame
        orientation_constraint.link_name = self._tip_link
        orientation_constraint.orientation.x = qx
        orientation_constraint.orientation.y = qy
        orientation_constraint.orientation.z = qz
        orientation_constraint.orientation.w = qw
        orientation_constraint.absolute_x_axis_tolerance = self._orientation_tolerance
        orientation_constraint.absolute_y_axis_tolerance = self._orientation_tolerance
        orientation_constraint.absolute_z_axis_tolerance = self._orientation_tolerance
        orientation_constraint.weight = 1.0

        constraints = Constraints()
        constraints.position_constraints = [position_constraint]
        constraints.orientation_constraints = [orientation_constraint]
        return constraints

    # 2026-07-22, found live: MoveIt2's own default trajectory timing (no
    # velocity/acceleration scaling requested) is aggressive -- a first test
    # move produced a 5-point, 0.35s trajectory across several joints, which
    # Stage 3's PD controller could not track accurately in that little time;
    # the resulting error was still ~0.3 rad on one joint 28 SECONDS later
    # (waiting longer did not help -- confirmed this is not a "just needed
    # more time" situation, since pinn_controller_node's own 2s staleness
    # timeout falls back to a gravity-compensation HOLD at whatever position
    # it drifted to, no longer trying to reach the original target at all).
    #
    # That same 2s staleness cutoff is a fixed wall-clock window from receipt,
    # NOT tied to the trajectory's own declared duration -- so slowing down
    # too aggressively creates a DIFFERENT failure mode: a trajectory that
    # legitimately needs more than 2s to complete would get cut off by
    # staleness partway through, before ever reaching the target, which would
    # look like the exact same symptom (never converges). 0.3 is a first,
    # untested-at-this-exact-value guess intended to roughly halve or third
    # the original 0.35s duration (comfortably under 2s) while still being
    # meaningfully slower/smoother than the untrackable default -- confirm the
    # actual resulting trajectory duration empirically (this class now logs
    # it) and adjust if it's still not converging or if it's creeping close
    # to 2s on a larger move.
    _VELOCITY_SCALING = 0.3
    _ACCELERATION_SCALING = 0.3

    # 2026-07-22, found live (after fixing the above): with a 0.3-scaled,
    # 1.11s/13-point trajectory, 6 of 7 arm joints converged to within 0.04
    # rad, but panda_joint3 settled with a persistent ~0.14 rad (~8 deg)
    # residual that did not improve with more waiting time -- consistent with
    # ordinary PD steady-state tracking error under gravity load (a PD-only
    # controller with no integral term is expected to have some), not a bug.
    # 0.05 (the original guess) was simply tighter than what this controller
    # can actually achieve; 0.15 accepts this real, observed behavior while
    # still catching genuine failures (the earlier untuned-speed attempt had
    # errors up to 0.3 rad, well outside this). If steady-state error turns
    # out to matter for actually grasping objects, the real fix is Stage 3
    # gain/gravity-comp tuning, not further loosening this number.
    _CONVERGENCE_TOLERANCE = 0.15

    def move_to(self, target_pose: np.ndarray, speed: float, timeout: float = 10.0) -> bool:
        """
        Plan a Cartesian-goal path to target_pose and execute it via Stage 3.

        speed [m/s] is accepted for interface compatibility with GraspConfig's
        *_speed fields but is NOT mapped to it literally: converting a desired
        Cartesian end-effector speed into MoveIt2's 0-1 joint-space velocity
        scaling factor isn't a direct unit conversion, and moveit_plan_bridge.py
        (this class's own reference pattern) doesn't attempt it either. Instead
        a fixed, conservative _VELOCITY_SCALING/_ACCELERATION_SCALING is applied
        to every request (see class-level comment for why this was necessary,
        not optional). Revisit with a real speed mapping if a pick sequence
        needs distinguishably different approach/lift speeds.

        `timeout` is a single overall budget covering planning AND execution
        (not split into separate phase timeouts) -- keep it generous;
        GraspConfig.arm_motion_timeout is the field this should come from.

        Returns True if planning succeeded, the trajectory was handed off,
        AND the arm's /joint_states converged near the planned trajectory's
        last waypoint (by name, in whatever order MoveIt2 reports
        trajectory.joint_names -- not assumed to match this project's own
        canonical order) within `timeout` seconds total. Returns False on any
        planning failure, handoff failure, or timeout.
        """
        deadline = time.monotonic() + timeout

        if not self._action_client.wait_for_server(timeout_sec=max(timeout, 0.1)):
            self.get_logger().error("move_to(): move_action server not available")
            return False

        goal = MoveGroup.Goal()
        goal.request.group_name = self._group_name
        goal.request.num_planning_attempts = 1
        goal.request.allowed_planning_time = self._planning_time
        goal.request.max_velocity_scaling_factor = self._VELOCITY_SCALING
        goal.request.max_acceleration_scaling_factor = self._ACCELERATION_SCALING
        goal.request.goal_constraints = [self._build_pose_constraints(target_pose)]
        goal.planning_options.plan_only = True

        send_goal_future = self._action_client.send_goal_async(goal)
        while not send_goal_future.done():
            rclpy.spin_once(self, timeout_sec=0.05)
            if time.monotonic() > deadline:
                self.get_logger().error("move_to(): timed out waiting for goal acceptance")
                return False
        goal_handle = send_goal_future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error("move_to(): MoveGroup goal rejected")
            return False

        result_future = goal_handle.get_result_async()
        while not result_future.done():
            rclpy.spin_once(self, timeout_sec=0.05)
            if time.monotonic() > deadline:
                self.get_logger().error("move_to(): timed out waiting for planning result")
                return False
        result = result_future.result().result
        if result.error_code.val != MoveItErrorCodes.SUCCESS:
            self.get_logger().error(f"move_to(): planning failed, error_code={result.error_code.val}")
            return False

        trajectory = result.planned_trajectory.joint_trajectory
        if not trajectory.points:
            self.get_logger().error("move_to(): planned trajectory has no points")
            return False

        target_by_name = dict(zip(trajectory.joint_names, trajectory.points[-1].positions))
        traj_duration = trajectory.points[-1].time_from_start
        traj_duration_s = traj_duration.sec + traj_duration.nanosec * 1e-9
        self.get_logger().info(
            f"move_to(): planning succeeded ({len(trajectory.points)} points, "
            f"{traj_duration_s:.2f}s trajectory duration, "
            f"{deadline - time.monotonic():.2f}s of overall timeout remaining) "
            f"-- handing off to Stage 3"
        )

        self._pub_trajectory.publish(trajectory)
        # Same DDS-discovery grace period as moveit_plan_bridge.py's own
        # plan_and_handoff() -- without it, a freshly-created publisher's
        # first message can be silently dropped before pinn_controller_node's
        # subscriber has finished discovering it.
        for _ in range(20):
            rclpy.spin_once(self, timeout_sec=0.05)
        time.sleep(0.5)

        # Give the trajectory time to actually play out (Stage 3's own 1 kHz
        # control loop in pinn_controller_node, not this node) before checking
        # convergence.
        min_wait_deadline = min(time.monotonic() + traj_duration_s, deadline)
        while time.monotonic() < min_wait_deadline:
            rclpy.spin_once(self, timeout_sec=0.05)
        self.get_logger().info(
            f"move_to(): trajectory should have finished playing out, "
            f"{deadline - time.monotonic():.2f}s left to confirm convergence"
        )

        last_diffs_by_name: dict = {}
        while time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.05)
            current_by_name = self._current_joint_positions_by_name()
            if current_by_name is not None:
                last_diffs_by_name = {
                    name: current_by_name[name] - target
                    for name, target in target_by_name.items()
                    if name in current_by_name
                }
                if last_diffs_by_name and max(abs(d) for d in last_diffs_by_name.values()) < self._CONVERGENCE_TOLERANCE:
                    return True

        # Log the actual per-joint (current - target) diffs at timeout, not just
        # "didn't converge" -- this is the difference between "still mid-motion,
        # just needed more time/budget" (small, shrinking diffs) and "never
        # moved at all" (diffs close to the full initial error) or "moved but
        # to the wrong place" (large diffs on specific joints).
        self.get_logger().warning(
            f"move_to(): trajectory handed off, but the arm did not converge to "
            f"the planned target within the timeout. Final per-joint "
            f"(current - target) diffs [rad]: {last_diffs_by_name}"
        )
        return False
