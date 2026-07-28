"""
Stage 2/3 -- ROS2 Jazzy launch file: MoveIt2 + MuJoCo simulated Franka Panda.

Replaces the dependency on the external ~/IsaacSim-ros_workspaces/jazzy_ws
isaac_moveit package (ros2 launch isaac_moveit isaac_moveit.launch.py). Modeled
node-for-node on that launch file (same MoveItConfigsBuilder/move_group/rviz/
robot_state_publisher/controller-spawner shape), swapping only the hardware
layer: mujoco_ros2_control's own ros2_control_node (not controller_manager's)
loading the MujocoSystemInterface plugin, pointed at a static, vendored MJCF
(mujoco/franka_emika_panda/panda_arm_mujoco.xml, from Google DeepMind's
mujoco_menagerie) via the mujoco_model hardware param in
urdf/panda_mujoco.ros2_control.xacro -- not runtime URDF-to-MJCF conversion,
which has a reproducible crash bug unrelated to this specific model (see that
xacro file's header comment).

Usage:
    ros2 launch pinn_franka_controller mujoco_franka_moveit.launch.py
    ros2 launch pinn_franka_controller mujoco_franka_moveit.launch.py headless:=true

Deactivate panda_arm_controller AND activate panda_effort_controller (see
config/mujoco_effort_controller.yaml) before routing trajectories through
pinn_controller_node. panda_effort_controller is spawned --inactive below, so
BOTH the deactivate and the activate must be in the SAME switch_controller call:
deactivating the arm controller alone leaves NO controller writing to the effort
command interface, so pinn_controller_node's effort commands are silently dropped
by the inactive ForwardCommandController and never reach the MuJoCo actuator
(arm looks "held" by the still-active position controller, zero motion during
tracking). Use ros2_ws/switch_to_effort.sh, or:

    ros2 service call /controller_manager/switch_controller \
        controller_manager_msgs/srv/SwitchController \
        "{activate_controllers: ['panda_effort_controller'], \
          deactivate_controllers: ['panda_arm_controller'], strictness: 2}"
"""

import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import EqualsSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterFile
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    headless = DeclareLaunchArgument(
        "headless",
        default_value="false",
        description="Run MuJoCo without its viewer window.",
    )

    use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation clock if true",
    )

    # 'both' -> arm joints export position+effort command interfaces + MuJoCo
    # position PID (Milestone 1 position-mode MoveIt path), switchable at runtime
    # to the Stage 3 effort path via switch_to_effort.sh. 'effort' -> arm joints
    # export ONLY the effort command interface and NO position PID; kept as a
    # lower-complexity alternative for Stage-3-only testing, not required for
    # normal use. See panda_mujoco.ros2_control.xacro's arm_control_mode comment
    # for why: an earlier session mistakenly attributed a since-refuted freeze
    # bug to 'both' mode; 'both' mode (the default) is confirmed working via
    # numeric /joint_states capture showing real multi-joint motion under Stage 3
    # effort control.
    arm_control_mode = DeclareLaunchArgument(
        "arm_control_mode",
        default_value="both",
        description="Arm command interface mode: 'both' (position+effort) or 'effort'.",
    )

    pinn_franka_controller_share = get_package_share_directory("pinn_franka_controller")
    custom_urdf_xacro = os.path.join(
        pinn_franka_controller_share, "urdf", "panda_mujoco.urdf.xacro"
    )

    # 2026-07-28: project-local override of the default
    # moveit_resources_panda_moveit_config initial_positions.yaml (see
    # panda_mujoco.ros2_control.xacro's initial_positions_file xacro:arg,
    # and this new file's own header comment for the full why -- the
    # system default disagreed with panda_arm_mujoco.xml's own 'home'
    # keyframe on panda_joint2/4/7, joint7 by a full sign flip, discovered
    # during the panda_joint4/6/7 freeze investigation).
    initial_positions_file = os.path.join(
        pinn_franka_controller_share, "config", "initial_positions.yaml"
    )

    moveit_config = (
        MoveItConfigsBuilder("moveit_resources_panda")
        .robot_description(
            file_path=custom_urdf_xacro,
            mappings={
                "headless": LaunchConfiguration("headless"),
                "arm_control_mode": LaunchConfiguration("arm_control_mode"),
                "initial_positions_file": initial_positions_file,
            },
        )
        .robot_description_semantic(file_path="config/panda.srdf")
        .trajectory_execution(file_path="config/gripper_moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl", "pilz_industrial_motion_planner"])
        .to_moveit_configs()
    )

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"use_sim_time": LaunchConfiguration("use_sim_time")},
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )

    # Without -d <config>, RViz opens with no displays added at all (a blank
    # grid, nothing else) regardless of whether the underlying robot/planning
    # data is correct -- this, not any TF/joint-state issue, was why nothing
    # rendered earlier. moveit_resources_panda_moveit_config ships its own
    # default config (RobotModel/Trajectory/PlanningScene/MotionPlanning
    # panels already added), reused as-is.
    rviz_config_file = os.path.join(
        get_package_share_directory("moveit_resources_panda_moveit_config"),
        "launch",
        "moveit.rviz",
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            moveit_config.joint_limits,
            {"use_sim_time": LaunchConfiguration("use_sim_time")},
        ],
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[
            moveit_config.robot_description,
            {"use_sim_time": LaunchConfiguration("use_sim_time")},
        ],
    )

    # config/panda.srdf's virtual_joint is type="floating" (a real 6-DOF joint,
    # not fixed), so current_state_monitor needs an actual world -> panda_link0
    # transform published somewhere -- nothing does this by default. Isaac's own
    # launch file had the equivalent (offset to match its arbitrary scene
    # placement); the MuJoCo model has the robot at the world origin, so identity.
    world_to_robot_tf_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher_world_to_robot",
        output="log",
        arguments=["0", "0", "0", "0", "0", "0", "world", "panda_link0"],
        parameters=[{"use_sim_time": LaunchConfiguration("use_sim_time")}],
    )

    # mujoco_ros2_control ships its own ros2_control_node executable (not
    # controller_manager's) that loads the MujocoSystemInterface plugin.
    # Two separate controller parameter files: moveit_resources' own
    # ros2_controllers.yaml (panda_arm_controller, panda_hand_controller,
    # joint_state_broadcaster -- unchanged) plus our new
    # mujoco_effort_controller.yaml (panda_effort_controller, Stage 3's path).
    moveit_resources_controllers_path = os.path.join(
        get_package_share_directory("moveit_resources_panda_moveit_config"),
        "config",
        "ros2_controllers.yaml",
    )
    mujoco_effort_controller_path = os.path.join(
        pinn_franka_controller_share, "config", "mujoco_effort_controller.yaml"
    )
    ros2_control_node = Node(
        package="mujoco_ros2_control",
        executable="ros2_control_node",
        emulate_tty=True,
        output="both",
        parameters=[
            {"use_sim_time": LaunchConfiguration("use_sim_time")},
            ParameterFile(moveit_resources_controllers_path),
            ParameterFile(mujoco_effort_controller_path),
        ],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    # Only spawnable in 'both' mode: panda_arm_controller is a position-mode
    # JointTrajectoryController and claims the arm's 'position' command interface,
    # which does not exist when arm_control_mode:=effort. Spawning it there would
    # just fail to claim its interfaces.
    panda_arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["panda_arm_controller", "-c", "/controller_manager"],
        condition=IfCondition(
            EqualsSubstitution(LaunchConfiguration("arm_control_mode"), "both")
        ),
    )

    # Spawned inactive: MoveIt2's default Plan & Execute uses panda_arm_controller
    # (position mode) until it's explicitly deactivated and this one activated,
    # same switch_controller dance already used with Isaac (see module docstring).
    panda_effort_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "panda_effort_controller",
            "-c",
            "/controller_manager",
            "--inactive",
        ],
    )

    # 2026-07-22: panda_finger_joint1/2 now have real physics (panda_arm_mujoco.xml,
    # panda_mujoco.ros2_control.xacro) instead of the old mock_components hand system,
    # so panda_hand_controller (position_controllers/GripperActionController, already
    # defined in moveit_resources_panda_moveit_config's ros2_controllers.yaml, loaded
    # above) can now actually be spawned and claim a real command_interface. Not
    # gated on arm_control_mode -- the gripper is independent of the arm's
    # position/effort switch. This is also what MoveIt2's own gripper_moveit_controllers.yaml
    # (loaded via .trajectory_execution() above) expects to talk to for its GripperCommand
    # action (panda_hand_controller / gripper_cmd), so this alone should make
    # MoveIt2's own gripper planning/execution work, independent of any future
    # MuJoCo-native gripper_controller.py Stage 4 work.
    panda_hand_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["panda_hand_controller", "-c", "/controller_manager"],
    )

    return LaunchDescription(
        [
            headless,
            use_sim_time,
            arm_control_mode,
            rviz_node,
            robot_state_publisher_node,
            world_to_robot_tf_node,
            move_group_node,
            ros2_control_node,
            joint_state_broadcaster_spawner,
            panda_arm_controller_spawner,
            panda_effort_controller_spawner,
            panda_hand_controller_spawner,
        ]
    )
