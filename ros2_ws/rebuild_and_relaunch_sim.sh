#!/bin/bash
# Stage 2/3/4 -- ONE command that does the whole "make a config/code change take
# effect" cycle for the MuJoCo sim: kill every stale process, rebuild, verify the
# rebuild succeeded, and only then launch a fresh simulation.
#
# WHY THIS EXISTS (2026-07-29). The 2026-07-28 session lost its single most
# important test to a pure ordering mistake: config/initial_positions.yaml was
# edited, but Terminal 1's already-running ros2_control_node was never restarted,
# so the "post-fix" test ran 100% pre-fix code and its null result meant nothing.
# SESSION.md's own closing note asked for exactly this script. The failure mode is
# insidious because a stale sim is indistinguishable from a fresh one at a glance:
# same topics, same nodes, same RViz window, just serving old config.
#
# It also removes a second trap: SESSION.md's next-session plan said to "run
# ros2_ws/launch_pinn_controller.sh to start a fresh sim", but that script starts
# the CONTROLLER NODE (Terminal 2), not the sim. The sim is
# mujoco_franka_moveit.launch.py, which is what this script launches.
#
# THIS SCRIPT IS TERMINAL 1 ONLY. It blocks (the sim runs in the foreground).
# Terminal 2 is still pinn_controller_node via launch_pinn_controller.sh, and
# Terminal 3 is still ad-hoc diagnostics -- unchanged.
#
# Usage:  bash ros2_ws/rebuild_and_relaunch_sim.sh
#
# NOTE: deliberately NOT `set -u`. ROS 2's own /opt/ros/jazzy/setup.bash reads
# AMENT_TRACE_SETUP_FILES before defining it, so `set -u` aborts this script on
# its very first line. ROS setup files are not nounset-safe; every check below is
# written to be explicit rather than relying on `set -u`.

WS=/home/hci-student/projects/pinn_franka/ros2_ws

source /opt/ros/jazzy/setup.bash

# --- 1. Kill every process that could be holding stale config -----------------
# ros2_control_node is the one that actually loads the MJCF and the URDF built
# from initial_positions.yaml, so it is the critical one; the others are killed
# too so RViz/move_group can't display or plan against a stale robot description.
echo "--- Killing stale sim processes ---"
for proc in ros2_control_node move_group robot_state_publisher rviz2 pinn_controller_node mujoco; do
    if pkill -f "$proc" 2>/dev/null; then
        echo "  killed: $proc"
    fi
done

# pkill returns immediately; give the OS a moment to actually reap them before
# asserting they are gone, otherwise the verification below races the kill.
sleep 3

# --- 2. Verify they are actually gone (do not trust the kill) -----------------
echo "--- Verifying no stale processes remain ---"
STALE=$(pgrep -af "ros2_control_node|move_group|pinn_controller_node" | grep -v pgrep || true)
if [ -n "$STALE" ]; then
    echo "!! STILL RUNNING after pkill -- refusing to continue:"
    echo "$STALE"
    echo "!! Kill these manually (pkill -9 -f ros2_control_node) and re-run."
    exit 1
fi
echo "  OK: nothing stale running."

# --- 3. Rebuild ---------------------------------------------------------------
# Built BEFORE launching (not after) so the launch below can only ever pick up
# freshly-installed files. This ordering is the entire point of the script.
echo "--- Building pinn_franka_controller ---"
cd "$WS" || exit 1
colcon build --packages-select pinn_franka_controller
BUILD_RC=$?
if [ "$BUILD_RC" -ne 0 ]; then
    echo "!! BUILD FAILED (exit $BUILD_RC). NOT launching -- fix the build first."
    echo "!! Launching now would silently run the previous install/ contents."
    exit "$BUILD_RC"
fi
echo "  OK: build succeeded."

# --- 4. Launch a fresh sim ----------------------------------------------------
# Sourced AFTER the build so the new install/ is what gets picked up.
source "$WS/install/setup.bash"
echo "--- Launching fresh MuJoCo + MoveIt2 sim (Ctrl-C to stop) ---"
exec ros2 launch pinn_franka_controller mujoco_franka_moveit.launch.py
