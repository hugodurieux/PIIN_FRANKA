"""
Stage 2 -- ROS2 Jazzy launch file for the PINN Franka controller node.

Usage
-----
    ros2 launch pinn_franka_controller pinn_controller.launch.py \
        urdf_path:=/path/to/franka.urdf \
        checkpoint_path:=/path/to/model.pt \
        delta:=0.0

To launch alongside Isaac Sim + MoveIt2 (current simulation target)
---------------------------------------------------------------------
In separate terminals:

    # 1. Start Isaac Sim with the Franka scene + ROS2 bridge:
    ~/isaac-sim/python.sh /path/to/simulation/isaac_franka_moveit_bridge.py

    # 2. Start MoveIt2 (isaac_moveit config, plans against the isaac_joint_*
    #    topics the bridge script above publishes/subscribes):
    ros2 launch isaac_moveit isaac_moveit.launch.py

    # 3. Start this controller node -- subscribes to isaac_joint_states and
    #    /pinn_controller/desired_trajectory, publishes effort commands on
    #    isaac_joint_commands (Isaac's ArticulationController accepts effort
    #    commands directly):
    ros2 launch pinn_franka_controller pinn_controller.launch.py \
        urdf_path:=/path/to/franka.urdf \
        checkpoint_path:=/path/to/model.pt

Note: as of the current Stage 2/3 integration, MoveIt2's default execution
path drives Isaac Sim directly via isaac_joint_commands (position control),
bypassing this node. Routing MoveIt2's planned trajectory into this node's
/pinn_controller/desired_trajectory topic instead (so the Stage 3 PINN
controller is what actually commands the robot) is tracked as follow-up work.

For a future real-hardware target (franka_ros2), remap both topics, e.g.:
    --ros-args --remap isaac_joint_states:=/franka/joint_states \
               --remap isaac_joint_commands:=/franka/effort_joint_trajectory_controller/commands
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Generate the launch description for pinn_controller_node."""

    # ---- Declare launch arguments -----------------------------------
    urdf_path_arg = DeclareLaunchArgument(
        "urdf_path",
        default_value="",
        description="Absolute path to the Franka Panda URDF file.",
    )

    checkpoint_path_arg = DeclareLaunchArgument(
        "checkpoint_path",
        default_value="",
        description="Absolute path to the trained PINN checkpoint (.pt).",
    )

    delta_arg = DeclareLaunchArgument(
        "delta",
        default_value="0.0",
        description="Payload conditioning parameter (0.0 = no payload).",
    )

    control_rate_hz_arg = DeclareLaunchArgument(
        "control_rate_hz",
        default_value="1000",
        description="Control loop frequency in Hz.",
    )

    use_lyapunov_gains_arg = DeclareLaunchArgument(
        "use_lyapunov_gains",
        default_value="true",
        description="Use Lyapunov-based gain tuning (Stage 3).",
    )

    # ---- Controller node --------------------------------------------
    controller_node = Node(
        package="pinn_franka_controller",
        executable="pinn_controller_node",
        name="pinn_franka_controller",
        output="screen",
        parameters=[
            {
                "urdf_path": LaunchConfiguration("urdf_path"),
                "checkpoint_path": LaunchConfiguration("checkpoint_path"),
                "delta": LaunchConfiguration("delta"),
                "control_rate_hz": LaunchConfiguration("control_rate_hz"),
                "use_lyapunov_gains": LaunchConfiguration("use_lyapunov_gains"),
            }
        ],
    )

    return LaunchDescription(
        [
            urdf_path_arg,
            checkpoint_path_arg,
            delta_arg,
            control_rate_hz_arg,
            use_lyapunov_gains_arg,
            controller_node,
        ]
    )
