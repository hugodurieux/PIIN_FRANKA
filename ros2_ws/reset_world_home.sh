#!/bin/bash
# Stage 4 -- reset the MuJoCo sim to the "home" keyframe (arm at ready pose,
# gripper open, grasp_object cube back at its resting spot on the floor).
# Written as a script (not a one-line pasted command) because long ros2
# service call invocations with inline YAML have repeatedly been corrupted
# by terminal line-wrapping during paste (see CLAUDE.md's terminal-command
# lesson, and ros2_ws/gripper_open.sh/gripper_close.sh for the same fix
# applied earlier).
#
# Usage: bash ros2_ws/reset_world_home.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

ros2 service call /mujoco_ros2_control_node/reset_world mujoco_ros2_control_msgs/srv/ResetWorld "{keyframe: 'home'}"
