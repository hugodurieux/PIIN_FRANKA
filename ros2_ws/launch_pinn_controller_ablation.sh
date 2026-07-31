#!/bin/bash
# Phase F ablation launcher (2026-07-29) -- tracking/STAGE4_TEST_PLAN.md.
#
# PURPOSE: run Stage 3 with the learned residual DISABLED while holding every
# other variable identical to the phase A baseline runs, so the only thing that
# changes between the two conditions is the model.
#
# WHY THIS EXISTS instead of launch_pinn_controller_no_residual.sh: that script
# passes disable_residual:=true but NOT gain_safety_margin_override. Every phase
# A run (36-44) used margin 4.0, i.e. Kp diag
#     [108.16, 128.14, 37.45, 57.76, 17.64, 22.66, 9.86]
# so the no_residual script would silently ALSO revert the gains to the Lyapunov
# default. Steady-state error is e_ss = tau/Kp, so changing Kp moves exactly the
# quantity phase F is trying to measure (panda_joint5's bias). Running the
# ablation with that script would change the residual AND the gains at once and
# produce an uninterpretable result -- the same trap SESSION.md records for
# debug_mujoco_internals.py, which compared two control paths and two arm
# configurations simultaneously and misled the investigation for a day.
#
# The ONLY difference between this script and launch_pinn_controller_boosted.sh
# is disable_residual:=true. Keep it that way: if the baseline launcher's
# arguments change, change them here too, or the comparison silently rots.
#
# Single-line ros2 launch invocation on purpose -- multi-line backslash
# continuations and long pasted commands have repeatedly been corrupted by
# terminal line-wrapping in this project (CLAUDE.md's Lesson #2; it silently
# dropped checkpoint_path and invalidated run18).
#
# Usage: bash ros2_ws/launch_pinn_controller_ablation.sh [margin]
#   margin defaults to 4.0, matching the phase A baseline runs.
source /home/hci-student/projects/pinn_franka/ros2_ws/set_pinn_env.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

MARGIN="${1:-4.0}"
echo "ABLATION: disable_residual=true, gain_safety_margin_override=${MARGIN}"
echo "Baseline for comparison: runs 36-38 (x=0.55) and 42-44 (x=0.70), margin 4.0, residual ON."

ros2 launch pinn_franka_controller pinn_controller.launch.py urdf_path:=/home/hci-student/projects/pinn_franka/pinocchio_baseline/panda.urdf checkpoint_path:=/home/hci-student/projects/pinn_franka/models/run_20260716_121302/greybox_best.pt gain_safety_margin_override:=${MARGIN} disable_residual:=true
