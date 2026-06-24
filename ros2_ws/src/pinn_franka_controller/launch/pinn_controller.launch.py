"""
Stage 2 -- ROS2 Humble launch file for the PINN Franka controller node.

Usage
-----
    ros2 launch pinn_franka_controller pinn_controller.launch.py \
        urdf_path:=/path/to/franka.urdf \
        checkpoint_path:=/path/to/model.pt \
        delta:=0.0

To launch alongside franka_ros2 and MoveIt2
--------------------------------------------
In a separate terminal (or via a top-level launch file that includes this one):

    # 1. Start the franka_ros2 hardware interface:
    ros2 launch franka_bringup franka.launch.py robot_ip:=<ROBOT_IP>

    # 2. Start MoveIt2 (generates trajectories on
    #    /pinn_controller/desired_trajectory):
    ros2 launch franka_moveit_config moveit.launch.py

    # 3. Start this controller node:
    ros2 launch pinn_franka_controller pinn_controller.launch.py \
        urdf_path:=/path/to/franka.urdf \
        checkpoint_path:=/path/to/model.pt

You may also remap topics if your MoveIt2 setup publishes trajectories on a
different topic, e.g. by adding:
    --ros-args --remap /pinn_controller/desired_trajectory:=/your/topic
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
