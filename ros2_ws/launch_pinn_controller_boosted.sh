#!/bin/bash
# Stage 3 debug -- same as launch_pinn_controller.sh but with
# gain_safety_margin_override set, to empirically test whether a much
# stronger PD push can move panda_joint4/6/7 (see pinn_controller_node.py's
# gain_safety_margin_override parameter comment). Written as a script, not a
# long pasted command, after two consecutive attempts at pasting the raw
# multi-argument ros2 launch line got silently corrupted by terminal
# line-wrapping (same class of issue as CLAUDE.md's Lesson #2).
#
# Usage: bash ros2_ws/launch_pinn_controller_boosted.sh [margin]
#   margin defaults to 8.0 if not given.
source /home/hci-student/projects/pinn_franka/ros2_ws/set_pinn_env.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

MARGIN="${1:-8.0}"
echo "Using gain_safety_margin_override=${MARGIN}"

ros2 launch pinn_franka_controller pinn_controller.launch.py urdf_path:=/home/hci-student/projects/pinn_franka/pinocchio_baseline/panda.urdf checkpoint_path:=/home/hci-student/projects/pinn_franka/models/run_20260716_121302/greybox_best.pt gain_safety_margin_override:=${MARGIN}
