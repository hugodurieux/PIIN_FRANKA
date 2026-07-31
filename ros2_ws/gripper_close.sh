#!/bin/bash
# Stage 4 -- close the gripper via panda_hand_controller's GripperCommand action.
# See gripper_open.sh for why this is a script rather than a pasted one-liner.
#
# Usage: bash ros2_ws/gripper_close.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

ros2 action send_goal /panda_hand_controller/gripper_cmd control_msgs/action/GripperCommand "{command: {position: 0.0, max_effort: 20.0}}"
