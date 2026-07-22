#!/bin/bash
# Stage 2/3 -- atomic controller switch into effort mode for the Stage 3 path.
#
# Deactivates panda_arm_controller (MoveIt2's position-mode execution) AND
# activates panda_effort_controller (the ForwardCommandController that
# pinn_controller_node writes torque to) in a SINGLE switch_controller call.
#
# WHY BOTH IN ONE CALL: panda_effort_controller is spawned --inactive (see
# launch/mujoco_franka_moveit.launch.py). Deactivating the arm controller
# WITHOUT also activating the effort controller leaves NO controller writing to
# the effort command interface -- pinn_controller_node's Float64MultiArray
# messages are then silently dropped by the inactive ForwardCommandController
# and never reach the MuJoCo motor actuator (the arm looks "held" only because
# the position controller is still holding it, and produces zero motion during
# trajectory tracking). The previously documented dance (deactivate arm only)
# was incomplete.
#
# ORDERING (LESSON #1, SESSION.md): run this ONLY AFTER pinn_controller_node is
# up and has logged "Stage 3 controller loaded" and is publishing to
# /panda_effort_controller/commands, so real effort commands exist BEFORE the
# position-mode backup is removed. Otherwise the arm free-falls at the switch.
#
# Usage:  bash ros2_ws/switch_to_effort.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

ros2 service call /controller_manager/switch_controller \
    controller_manager_msgs/srv/SwitchController \
    "{activate_controllers: ['panda_effort_controller'], deactivate_controllers: ['panda_arm_controller'], strictness: 2}"

echo "--- controller states after switch ---"
ros2 control list_controllers
