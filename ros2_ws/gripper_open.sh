#!/bin/bash
# Stage 4 -- open the gripper via panda_hand_controller's GripperCommand action.
# Written as a script (not a one-line pasted command) because long ros2 action
# send_goal invocations have repeatedly been corrupted by terminal line-wrapping
# during paste (see CLAUDE.md's terminal-command lesson).
#
# Usage: bash ros2_ws/gripper_open.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

ros2 action send_goal /panda_hand_controller/gripper_cmd control_msgs/action/GripperCommand "{command: {position: 0.04, max_effort: 20.0}}"
