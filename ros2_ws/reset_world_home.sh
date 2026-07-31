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

# ---------------------------------------------------------------------------
# 2026-07-29: ALWAYS re-assert effort mode after a reset. Not optional, and
# deliberately folded in here rather than left as a separate step to remember.
#
# WHY: mujoco_ros2_control's ResetWorld silently reverts every joint to its
# INTERNAL position PID (config/mujoco_pid.yaml). It bypasses
# perform_command_mode_switch(), so nothing reports it -- the plugin logs no
# mode line, controller_manager still lists panda_effort_controller as ACTIVE,
# `ros2 control list_controllers` looks healthy, commands still publish and
# echo fine, and the arm holds itself up convincingly. Every torque published
# to /panda_effort_controller/commands is discarded, and the arm sits at
# (home_keyframe - tau_gravity / p_position_pid), pinned to ~1e-5 rad. That
# equilibrium is the "panda_joint4/6/7 freeze" which cost 2026-07-23..29.
#
# Forgetting this step is not a hypothetical: it silently invalidated
# test_grasp_pick_run26.log, whose ros2_control_node log reads
#   ...189 effort control enabled   (last real switch)
#   ...768 Reset world service called   (no mode event after it)
#   ...793 run26 starts                 (running on the position PID)
# and which duly reproduced the freeze fingerprint to 1e-8 rad. The run tested
# nothing. Three separate sessions have lost results to exactly this.
#
# Guarded so this stays a no-op when the effort controller is not in use (e.g.
# plain MoveIt2 position-mode work, where reverting to position is correct).
# ---------------------------------------------------------------------------
if ros2 control list_controllers 2>/dev/null | grep "panda_effort_controller" | grep -q "[^in]active"; then
    echo
    echo "--- panda_effort_controller is active: re-asserting effort mode after reset ---"
    bash /home/hci-student/projects/pinn_franka/ros2_ws/force_effort_mode.sh
else
    echo
    echo "panda_effort_controller is not active -- leaving control mode alone."
    echo "(If you intended Stage 3 effort control, run switch_to_effort.sh first.)"
fi
