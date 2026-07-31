#!/bin/bash
# 2026-07-28 DIAGNOSTIC -- Stage 4 investigation of the joint4/6/7 freeze.
# Same as launch_pinn_controller.sh but with disable_residual:=true, so
# tau_cmd = tau_rnea + tau_pd only (the learned GreyBoxNet/FrictionNet is
# never called). Written as a script, not a pasted long ros2 launch
# one-liner, because long ros2 CLI commands with inline args have
# repeatedly been corrupted by terminal line-wrapping on paste (see
# CLAUDE.md's terminal-command lesson) -- exactly what just happened when
# this was pasted directly (checkpoint_path silently dropped, controller
# fell back to publishing zero torques with no model loaded at all).
#
# Usage: bash ros2_ws/launch_pinn_controller_no_residual.sh
source /home/hci-student/projects/pinn_franka/ros2_ws/set_pinn_env.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash
ros2 launch pinn_franka_controller pinn_controller.launch.py \
    urdf_path:=/home/hci-student/projects/pinn_franka/pinocchio_baseline/panda.urdf \
    checkpoint_path:=/home/hci-student/projects/pinn_franka/models/run_20260716_121302/greybox_best.pt \
    disable_residual:=true
