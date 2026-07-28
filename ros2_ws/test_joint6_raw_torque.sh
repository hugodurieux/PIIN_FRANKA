#!/bin/bash
# Stage 3 debug -- sibling of test_joint4_raw_torque.sh (2026-07-23/24),
# written 2026-07-28. Bypasses pinn_controller_node entirely and publishes a
# raw, constant, unambiguous torque directly to
# /panda_effort_controller/commands, this time isolating panda_joint6 alone.
#
# WHY: every prior observation of panda_joint6 freezing happened while it was
# being commanded ALONGSIDE panda_joint4 in a multi-joint move -- it has never
# been tested completely alone. Joint4's own isolated immobility is now
# confirmed independent of motion planning, the trained model, and
# grasp_object's proximity (see SESSION.md's 2026-07-28 entry). This script
# checks whether joint6 shares that same isolated-immobility property, or
# whether it only ever appeared stuck as a side effect of joint4's own issue
# (e.g. via a shared trajectory/timing path), which would mean joint6 is not
# an independent instance of the same underlying problem.
#
# 10 Nm: safely under panda_joint6's +/-12 Nm ctrlrange, and roughly 5x its
# ~2 Nm gravity-compensation torque at the 'home' configuration (see
# pinn_controller_node's [DEBUG tau] logs, rnea~=+2.09 Nm for j6 near home) --
# a decisively substantial, unopposed torque if the joint is actually free.
#
# PREREQUISITE, SAME AS test_joint4_raw_torque.sh: panda_effort_controller
# must be ACTIVE (bash ros2_ws/switch_to_effort.sh) and pinn_controller_node
# must NOT be running (otherwise its 1kHz stream overwrites this script's
# 50Hz publishes on the same topic -- confirmed live 2026-07-28 as a real
# confound, not hypothetical). Verify with `ros2 node list` before trusting
# any result from this script.
#
# Usage: bash ros2_ws/switch_to_effort.sh && bash ros2_ws/test_joint6_raw_torque.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

echo "Publishing 10 Nm to panda_joint6 only, 0 to all others, for 5 seconds..."
timeout 5 ros2 topic pub -r 50 /panda_effort_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 0.0]}"
echo "Done."
