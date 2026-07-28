#!/bin/bash
# Stage 3/4 -- FORCE mujoco_ros2_control back into effort mode after a world reset.
#
# RUN THIS AFTER EVERY reset_world_home.sh. Not optional.
#
# THE BUG (found 2026-07-29, after this cost roughly a week):
# mujoco_ros2_control's ResetWorld service silently reverts each joint to its
# INTERNAL position PID (config/mujoco_pid.yaml). It does not route that change
# through perform_command_mode_switch(), so:
#   * the plugin logs NOTHING -- its last line still reads "effort control enabled"
#   * controller_manager still reports panda_effort_controller ACTIVE
#   * ros2 control list_controllers looks perfectly healthy
#   * and every torque published to /panda_effort_controller/commands is ignored
# Measured proof, immediately after a reset, with 40 Nm commanded to joint4 alone:
#   joint1 commanded  0.0 Nm -> measured -87.0 Nm (PID saturated, oscillating)
#   joint3 commanded  0.0 Nm -> measured +87.0 Nm (PID saturated, oscillating)
#   joint4 commanded 40.0 Nm -> measured +23.5 Nm  = 500 * (home - current)
#                                                  = the p=500 position PID, not our command
#
# The arm then sits at (home_keyframe - tau_gravity/p_position_pid), pinned to
# ~1e-5 rad and unresponsive. That equilibrium is the "panda_joint4/6/7 freeze"
# that consumed 2026-07-23 through 2026-07-29. All seven joints are frozen in it;
# only the joints whose target is far from home LOOK frozen, which is why the
# symptom masqueraded as a per-joint physics/plugin fault for a week.
#
# WHY switch_to_effort.sh CANNOT FIX THIS: panda_effort_controller is still
# ACTIVE from controller_manager's point of view, so a switch that activates it
# is rejected as a no-op ("Controller with name 'panda_effort_controller' is
# already active", ok=False) and perform_command_mode_switch() is never called.
# The plugin therefore stays in position mode. The ONLY way back is a real
# deactivate -> activate cycle, which is what this script does.
#
# ORDERING (same trap as switch_to_effort.sh's LESSON #1): run this ONLY WHILE
# pinn_controller_node is up and publishing to /panda_effort_controller/commands.
# Step 2 hands the arm from the position PID (which was holding it rigid) to
# effort control, and if nothing is publishing torque at that moment the arm
# simply falls. Confirmed live 2026-07-29: with the controller stopped, the arm
# went limp the instant this script finished -- which is the correct sanity check
# that the fix worked, but is not what you want before a real test.
#
# Usage:  bash ros2_ws/force_effort_mode.sh

source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

SRV=/controller_manager/switch_controller
TYPE=controller_manager_msgs/srv/SwitchController

# Step 1: hand the arm back to panda_arm_controller and drop the effort controller.
# Activating the arm controller in the SAME call means the arm is never left with
# no controller writing to it, so it does not free-fall during the swap.
echo "--- Step 1/2: effort -> position (forces a real mode switch) ---"
ros2 service call "$SRV" "$TYPE" "{activate_controllers: ['panda_arm_controller'], deactivate_controllers: ['panda_effort_controller'], strictness: 2}"

sleep 2

# Step 2: swap back. THIS call is the one that makes the plugin re-run
# perform_command_mode_switch() and re-enable effort control per joint.
echo "--- Step 2/2: position -> effort (re-enables effort control in the plugin) ---"
ros2 service call "$SRV" "$TYPE" "{activate_controllers: ['panda_effort_controller'], deactivate_controllers: ['panda_arm_controller'], strictness: 2}"

sleep 2

# Verify against the PLUGIN'S OWN LOG, not controller_manager's opinion of it.
# controller_manager is exactly the layer that lies here, so checking it proves
# nothing; only the plugin's per-joint "effort control enabled" lines are evidence.
echo
echo "--- Plugin's own last per-joint control-mode lines ---"
LOG=$(ls -t "$HOME"/.ros/log/ros2_control_node_*.log 2>/dev/null | head -1)
if [ -z "$LOG" ]; then
    echo "!! Could not find a ros2_control_node log under ~/.ros/log/ -- verify manually."
    exit 1
fi
echo "(log: $LOG)"

# The check below must compare the LAST "<mode> control enabled" event and ask
# which mode it names. Two ways this went wrong on 2026-07-29, both fixed here:
#
#  1. Filtering for "effort control enabled" and then testing that the result
#     contains "effort control enabled" is a tautology -- it can never fail.
#     It reported success while the lines printed directly above it read
#     "position control enabled". Grep for BOTH modes, then inspect the last hit.
#
#  2. The plugin writes its mode-switch lines on a later control cycle than the
#     one that answers the service call, and the log is block-buffered, so a
#     single read right after the call can miss step 2 entirely and see only
#     step 1's "position control enabled". Observed live: service returned at
#     ~t+0, plugin logged at ~t+2s, the check read in between and reported the
#     wrong mode. Poll for up to ~10s for an effort line NEWER than the last
#     position line instead of reading once.
LAST_MODE=""
for _ in $(seq 1 10); do
    LAST_MODE=$(grep -E "Joint panda_joint1: (effort|position) control enabled" "$LOG" | tail -1)
    case "$LAST_MODE" in
        *"effort control enabled"*) break ;;
    esac
    sleep 1
done

grep -E "Joint panda_joint[1-7]: (effort|position) control enabled" "$LOG" | tail -7

echo
case "$LAST_MODE" in
    *"effort control enabled"*)
        echo "OK: plugin's most recent per-joint mode event is EFFORT control."
        echo "    Torques now reach the MuJoCo actuators."
        echo
        echo "    Sanity check it for real: the arm should now SAG under gravity if"
        echo "    pinn_controller_node is not running. If it holds itself rigidly,"
        echo "    the position PID is still active and this did NOT work."
        ;;
    *)
        echo "!! Plugin's most recent mode event is NOT effort control:"
        echo "!!   $LAST_MODE"
        echo "!! DO NOT run a test -- every torque will be silently discarded."
        exit 1
        ;;
esac
