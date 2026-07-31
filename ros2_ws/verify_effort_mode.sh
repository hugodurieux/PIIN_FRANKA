#!/bin/bash
# Stage 3/4 -- IS THE RESULT I JUST GOT EVEN VALID?
#
# Run this immediately BEFORE and immediately AFTER any tracking/pick test.
# Exits 0 only if the stack is in a state where a null result MEANS something.
#
# WHY THIS EXISTS (2026-07-29). For one week the "panda_joint4/6/7 freeze" was
# investigated as a physics bug. It was not. It was panda_arm_controller's
# position PID holding the arm while panda_effort_controller sat INACTIVE and
# silently discarded every torque pinn_controller_node published. Proof, from
# stage4/test_grasp_pick_run13/14/15.log -- three separate runs, bit-identical
# positions, each equal to the MJCF home keyframe minus tau_gravity/p_position_pid:
#   panda_joint4: home -1.57079, tau 22.351 Nm, p=500 -> -1.61549   (logged -1.61540)
#   panda_joint6: home +1.57079, tau  2.085 Nm, p=150 -> +1.55689   (logged +1.55691)
#   panda_joint7: home -0.78530, tau  0.000 Nm, p=150 -> -0.78530   (logged -0.78529)
# Three joints, two different gains, agreement to 1e-5 rad.
#
# The trap is that ALL SEVEN joints are frozen in this state, but only the joints
# whose target is far from home LOOK frozen -- which is why the symptom presented
# as a "joint 4/6/7 freeze" and sent the investigation hunting for what those
# three joints had in common. They have nothing in common. They just had far
# targets. Joints 1/2/3/5 were equally frozen and equally unresponsive.
#
# switch_to_effort.sh already verifies the switch at the moment it runs. This
# script answers the different, and in hindsight more important, question: was
# effort mode still active when the test actually ran? Cheap to run, and it makes
# an uninterpretable null result impossible to mistake for evidence.
#
# Usage:  bash ros2_ws/verify_effort_mode.sh

source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

STATES=$(ros2 control list_controllers 2>/dev/null)
if [ -z "$STATES" ]; then
    echo "!! controller_manager not reachable -- is the sim (Terminal 1) running?"
    exit 1
fi

echo "--- controller states ---"
echo "$STATES"
echo

EFFORT_ACTIVE=$(echo "$STATES" | grep "panda_effort_controller" | grep -c "[^in]active")
ARM_ACTIVE=$(echo "$STATES" | grep "panda_arm_controller" | grep -vc "inactive")

VALID=1
if [ "$EFFORT_ACTIVE" -lt 1 ]; then
    echo "  FAIL: panda_effort_controller is NOT active."
    echo "        Every torque published to /panda_effort_controller/commands is"
    echo "        being accepted and then DISCARDED. Any freeze you just observed"
    echo "        is this bug, not a physics or plugin problem."
    VALID=0
fi
if [ "$ARM_ACTIVE" -ne 0 ]; then
    echo "  FAIL: panda_arm_controller is STILL ACTIVE."
    echo "        Its position PID (config/mujoco_pid.yaml, p=500 on joints 1-4,"
    echo "        p=150 on 5-7) is holding the arm. This looks exactly like working"
    echo "        gravity compensation and exactly like a frozen joint."
    VALID=0
fi

if [ "$VALID" -eq 0 ]; then
    echo
    echo "  >> THE TEST RESULT IS NOT INTERPRETABLE. Do not record it as evidence."
    echo "  >> Fix: ensure pinn_controller_node (Terminal 2) logged 'Stage 3"
    echo "  >>      controller loaded', then run: bash ros2_ws/switch_to_effort.sh"
    echo "  >>      and confirm it exits 0 before re-running the test."
    exit 1
fi

echo "  OK: panda_effort_controller ACTIVE, panda_arm_controller not."
echo "  OK: torques reach the MuJoCo actuators. A freeze observed now is real."
exit 0
