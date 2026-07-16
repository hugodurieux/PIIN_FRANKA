"""
Stage 2/3 -- Milestone 2 bridge: plan with MoveIt2, execute with the Stage 3
PINN controller instead of MoveIt2's own execution path.

PLAN (3 sentences):
This node sends a plan-only MoveGroup goal (moveit_msgs/action/MoveGroup,
planning_options.plan_only=True) for the panda_arm group to move_group's
existing move_action server -- the same server RViz's "Plan & Execute" button
uses -- so move_group never invokes its own trajectory_execution_manager
(panda_arm_controller). On success, it republishes the planned
trajectory_msgs/JointTrajectory once onto /pinn_controller/desired_trajectory,
which pinn_controller_node already subscribes to (Milestone 1), so Stage 3's
RNEA + trained residual + Lyapunov-gain PD controller -- not MoveIt2's default
position execution -- is what actually commands the robot.

Prerequisite (manual, one-time, NOT done by this node): panda_arm_controller
must be deactivated first, since its hardware interface continuously publishes
position commands to isaac_joint_commands every control cycle and would
otherwise race pinn_controller_node's effort commands on the same topic:

    ros2 service call /controller_manager/switch_controller \
        controller_manager_msgs/srv/SwitchController \
        "{deactivate_controllers: ['panda_arm_controller'], strictness: 2}"

Usage:
    ros2 run pinn_franka_controller moveit_plan_bridge
    ros2 run pinn_franka_controller moveit_plan_bridge --ros-args \
        -p target_joint_positions:="[0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]"

Parameters
----------
    group_name             (str)         -- MoveIt2 planning group, default "panda_arm"
    target_joint_positions (float[7])    -- joint-space goal [rad], default the
                                             SRDF "extended" pose (visibly
                                             different from the typical "ready"
                                             start, so success is obvious)
    joint_tolerance         (float)       -- +/- tolerance per joint [rad], default 0.01
    planning_time            (float)      -- allowed_planning_time [s], default 5.0
"""

from __future__ import annotations

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, JointConstraint, MoveItErrorCodes
from trajectory_msgs.msg import JointTrajectory

# Franka Panda arm joint names, matching pinocchio_baseline/panda.urdf.
_JOINT_NAMES = [f"panda_joint{i}" for i in range(1, 8)]

# SRDF "extended" named state (panda_moveit_config/config/panda.srdf) --
# collision-free, visibly different from the typical "ready" start pose.
_DEFAULT_TARGET = [0.0, 0.0, 0.0, 0.0, 0.0, 1.571, 0.785]


class MoveitPlanBridge(Node):
    """Plans once via MoveGroup (plan_only) and hands the trajectory to Stage 3."""

    def __init__(self) -> None:
        super().__init__("moveit_plan_bridge")

        self.declare_parameter("group_name", "panda_arm")
        self.declare_parameter("target_joint_positions", _DEFAULT_TARGET)
        self.declare_parameter("joint_tolerance", 0.01)
        self.declare_parameter("planning_time", 5.0)

        self._group_name: str = self.get_parameter("group_name").value
        self._target: list[float] = list(
            self.get_parameter("target_joint_positions").value
        )
        self._tolerance: float = self.get_parameter("joint_tolerance").value
        self._planning_time: float = self.get_parameter("planning_time").value

        if len(self._target) != len(_JOINT_NAMES):
            raise ValueError(
                f"target_joint_positions must have {len(_JOINT_NAMES)} values, "
                f"got {len(self._target)}"
            )

        self._pub_trajectory = self.create_publisher(
            JointTrajectory, "/pinn_controller/desired_trajectory", 10
        )
        self._action_client = ActionClient(self, MoveGroup, "move_action")

    def plan_and_handoff(self) -> None:
        self.get_logger().info("Waiting for move_action server...")
        self._action_client.wait_for_server()

        goal = MoveGroup.Goal()
        goal.request.group_name = self._group_name
        goal.request.num_planning_attempts = 1
        goal.request.allowed_planning_time = self._planning_time
        goal.request.goal_constraints = [self._build_joint_constraints()]
        goal.planning_options.plan_only = True

        self.get_logger().info(
            f"Sending plan-only goal for '{self._group_name}' -> {self._target}"
        )
        send_goal_future = self._action_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()

        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error("Goal rejected by move_group.")
            return

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result().result

        if result.error_code.val != MoveItErrorCodes.SUCCESS:
            self.get_logger().error(
                f"Planning failed, error_code={result.error_code.val}"
            )
            return

        trajectory = result.planned_trajectory.joint_trajectory
        n_points = len(trajectory.points)
        self.get_logger().info(
            f"Planning succeeded ({n_points} points) -- publishing to "
            f"/pinn_controller/desired_trajectory for Stage 3 to execute."
        )
        self._pub_trajectory.publish(trajectory)

    def _build_joint_constraints(self) -> Constraints:
        constraints = Constraints()
        for name, position in zip(_JOINT_NAMES, self._target):
            jc = JointConstraint()
            jc.joint_name = name
            jc.position = position
            jc.tolerance_above = self._tolerance
            jc.tolerance_below = self._tolerance
            jc.weight = 1.0
            constraints.joint_constraints.append(jc)
        return constraints


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MoveitPlanBridge()
    try:
        node.plan_and_handoff()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
