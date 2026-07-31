#!/bin/bash
# Stage 3 debug -- bypass pinn_controller_node entirely and publish a raw,
# constant, unambiguous torque directly to /panda_effort_controller/commands.
# Written as a script (not a pasted command) after repeated terminal
# line-wrapping corruption of the raw `ros2 topic pub` invocation (same class
# of issue as CLAUDE.md's Lesson #2).
#
# Only panda_joint4 gets nonzero torque (40 Nm); every other joint gets 0,
# so they will sag/drift under gravity with nothing holding them -- expected
# and harmless for this short, isolated test. Publishes at 50 Hz for 5
# seconds then stops on its own (no need to Ctrl+C).
#
# PREREQUISITE, ADDED 2026-07-27 -- THIS SCRIPT IS A NO-OP WITHOUT IT.
# /panda_effort_controller/commands only reaches a MuJoCo actuator when
# panda_effort_controller is ACTIVE. It is spawned --inactive (see
# launch/mujoco_franka_moveit.launch.py), and an inactive ForwardCommandController
# ACCEPTS and then DISCARDS every message: publishing succeeds, `ros2 topic echo`
# shows the data, and nothing whatsoever happens to the robot. Run
# `bash ros2_ws/switch_to_effort.sh` first and confirm it exits 0.
#
# This matters because the 2026-07-24 session used this script to conclude that
# "even a raw 40 Nm bypassing all Python cannot move panda_joint4, so the problem
# must be below the ROS2 layer" -- treated as airtight, and it steered the whole
# investigation toward MuJoCo/plugin internals. If effort mode was not active at
# the time, the test applied 0 Nm and proved nothing. Always verify effort mode
# before drawing any conclusion from a null result here.
#
# Usage: bash ros2_ws/switch_to_effort.sh && bash ros2_ws/test_joint4_raw_torque.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

echo "Publishing 40 Nm to panda_joint4 only, 0 to all others, for 5 seconds..."
timeout 5 ros2 topic pub -r 50 /panda_effort_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 40.0, 0.0, 0.0, 0.0]}"
echo "Done."
