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

# ---------------------------------------------------------------------------
# 2026-07-27: VERIFY the switch actually took, and fail loudly if it did not.
#
# WHY THIS BLOCK EXISTS. Until now this script fired the service call and
# printed the controller list for a human to eyeball. Nobody eyeballed it, and
# an un-switched stack is INDISTINGUISHABLE from a broken robot: the arm still
# holds itself up (panda_arm_controller's position PID is doing that, see
# config/mujoco_pid.yaml), pinn_controller_node still logs plausible torques,
# and /panda_effort_controller/commands still accepts messages -- they are just
# dropped by the inactive ForwardCommandController and never reach the MuJoCo
# actuator, exactly as this script's own header warns.
#
# That state was reverse-engineered out of the 2026-07-24 Stage 4 logs after it
# had consumed most of two sessions under the name "the intermittent
# panda_joint4/6/7 freeze". Its fingerprint, for reference: every arm joint sits
# at (home_keyframe_position - tau_gravity / p_position_pid), pinned to ~1e-5
# rad and completely unresponsive to the commanded effort. Measured from
# stage4/test_grasp_pick_run13-15.log against the [DEBUG tau] RNEA values:
#   panda_joint4: 22.351 Nm / p=500 = 0.0447 rad sag -> -1.61549 (logged -1.61540)
#   panda_joint6:  2.085 Nm / p=150 = 0.0139 rad sag -> +1.55689 (logged +1.55691)
#   panda_joint7:  0.000 Nm / p=150 = 0.0000 rad sag -> -0.78530 (logged -0.78529)
# Two different p gains, three joints, all matching. Not a physics bug at all.
#
# A machine check costs one extra service round-trip; a missed switch costs a
# session. Exits nonzero so any wrapper script stops instead of continuing into
# a test whose result cannot mean anything.
# ---------------------------------------------------------------------------
STATES=$(ros2 control list_controllers 2>/dev/null)
EFFORT_OK=$(echo "$STATES" | grep -c "panda_effort_controller.*active")
ARM_STILL_ACTIVE=$(echo "$STATES" | grep "panda_arm_controller" | grep -vc "inactive")

echo
if [ "$EFFORT_OK" -ge 1 ] && [ "$ARM_STILL_ACTIVE" -eq 0 ]; then
  echo "OK: panda_effort_controller is ACTIVE and panda_arm_controller is not."
  echo "    Stage 3 effort commands now reach the MuJoCo actuators."
  exit 0
fi

echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "!! EFFORT MODE IS *NOT* ACTIVE. DO NOT RUN A PICK/TRACKING TEST.    !!"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
if [ "$EFFORT_OK" -lt 1 ]; then
  echo "  * panda_effort_controller is not active -> every torque"
  echo "    pinn_controller_node publishes is silently discarded."
fi
if [ "$ARM_STILL_ACTIVE" -ne 0 ]; then
  echo "  * panda_arm_controller is still active -> its position PID"
  echo "    (config/mujoco_pid.yaml, p=500 on joints 1-4, p=150 on 5-7) is"
  echo "    holding the arm, which LOOKS like working gravity compensation."
fi
echo
echo "  Likely causes: pinn_controller_node was not up yet (see ORDERING"
echo "  above, strictness:2 aborts the whole switch if activation fails), or"
echo "  the mujoco launch was restarted after the last successful switch."
echo "  Fix: confirm pinn_controller_node logged 'Stage 3 controller loaded',"
echo "  then re-run this script."
exit 1
