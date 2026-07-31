#!/bin/bash
# Stage 3/4 diagnostic -- panda_joint4/6/7 "frozen at home" symptom.
#
# 2026-07-23 UPDATE (Opus static investigation, resumed): the ORIGINAL premise
# of this script -- that joints 4/6/7 are stuck in mujoco_ros2_control's
# INTERNAL position-PID mode while 1/2/3/5 are in effort mode -- has been
# REFUTED with direct log evidence. Two independent facts kill it:
#   (B) `ros2 control list_hardware_interfaces` (run live) shows ALL 7 joints
#       uniformly effort=[claimed], position=[unclaimed]. No asymmetry.
#   (C) The ros2_control_node log (the plugin's OWN per-joint mode flags, set
#       by perform_command_mode_switch()) shows ALL 7 joints -- including
#       4/6/7 -- transitioning "position control disabled" -> "effort control
#       enabled (position, velocity disabled)" on the controller switch. A
#       scan of EVERY historical ros2_control_node log found the effort switch
#       is always all-7-or-none: there is NO run where 4/6/7 were left in
#       position mode while 1/2/3/5 went to effort. The mode-lock story is dead.
#
# So the freeze is NOT a control-mode problem at any level (controller_manager
# claim bookkeeping OR plugin-internal write() routing). Section (C) below now
# just CONFIRMS effort mode (it should always show effort). The live question
# has moved to section (D): given all 7 joints are provably in effort mode and
# receiving commands, is a genuinely VARYING torque being commanded to 4/6/7
# during a move (=> physics/actuator/tuning downstream), or is their commanded
# torque near-constant while 1/2/3/5 vary (=> the trajectory/PD *input* for
# those joints barely changes, i.e. upstream in planning/interpolation)?
#
# Run this in a fresh terminal AFTER: launch is up, pinn_controller_node is up,
# and the effort switch has been done (the exact state a pick test runs in).
#
# Usage: bash ros2_ws/diagnose_arm_modes.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

echo "===================================================================="
echo "(A) Controller states -- is panda_arm_controller inactive and"
echo "    panda_effort_controller active?"
echo "===================================================================="
ros2 control list_controllers

echo
echo "===================================================================="
echo "(B) Per-joint claimed command interface (controller_manager bookkeeping)."
echo "    HEALTHY effort setup: every panda_jointN/effort [claimed],"
echo "    every panda_jointN/position [unclaimed]. (Confirmed uniform live."
echo "    Kept as a sanity check.)"
echo "===================================================================="
ros2 control list_hardware_interfaces

echo
echo "===================================================================="
echo "(C) Per-joint LAST logged control mode from the mujoco plugin itself."
echo "    FIX 2026-07-23: the plugin logs to ~/.ros/log/<dir>/"
echo "    ros2_control_node_<pid>_<ts>.log -- NOT ~/.ros/log/latest/ (which"
echo "    only holds the launcher's tiny launch.log). The old script grepped"
echo "    latest/* and always came back empty. We now locate the newest"
echo "    ros2_control_node log that actually contains the plugin's lines."
echo "    Expected NOW (mode-lock refuted): 'effort control enabled' on ALL 7."
echo "===================================================================="
RCN=$(ls -t $(grep -rlE "Joint panda_joint[1-7]:.*control (enabled|disabled)" \
        "$HOME/.ros/log" 2>/dev/null) 2>/dev/null | head -1)
if [ -z "$RCN" ]; then
  echo "  (no ros2_control_node log with plugin mode lines found under"
  echo "   ~/.ros/log -- is the mujoco launch actually running? Its plugin"
  echo "   logs to a file named ros2_control_node_<pid>_<ts>.log.)"
else
  echo "  source log: $RCN"
  echo "  (mtime: $(stat -c %y "$RCN" | cut -d. -f1))"
  echo
  eff_count=0
  for j in 1 2 3 4 5 6 7; do
    line=$(grep -hE "Joint panda_joint$j:.*control (enabled|disabled)" "$RCN" \
             2>/dev/null | tail -1 | sed 's/.*MujocoSystemInterface\]: //')
    echo "  panda_joint$j -> ${line:-'(no control-mode line for this joint)'}"
    echo "$line" | grep -q "effort control enabled" && eff_count=$((eff_count+1))
  done
  echo
  if [ "$eff_count" -eq 7 ]; then
    echo "  => ALL 7 joints in EFFORT mode at the plugin level. Mode is NOT the"
    echo "     cause of the 4/6/7 freeze. Proceed to (D)."
  else
    echo "  => Only $eff_count/7 joints show effort mode. If EXACTLY 4/6/7 are"
    echo "     the missing ones, the mode-lock hypothesis would be RESURRECTED"
    echo "     (contradicting all prior logs -- capture this run's full log)."
    echo "     If a different/again-all-7 pattern, re-check the switch actually"
    echo "     targeted panda_effort_controller."
  fi
fi

echo
echo "===================================================================="
echo "(D) DECISIVE NEXT TEST: is a VARYING torque commanded to 4/6/7 during a"
echo "    move? pinn_controller_node publishes std_msgs/Float64MultiArray on"
echo "    /panda_effort_controller/commands with data in panda_joint1..7 order"
echo "    (clean, positional -- see pinn_controller_node._JOINT_NAMES). We"
echo "    capture a fixed window and report per-joint torque min/max/range."
echo "--------------------------------------------------------------------"
echo "    HOW TO READ THE RESULT:"
echo "      * joints 4/6/7 show a WIDE torque range (like 1/2/3/5) but the arm"
echo "        still doesn't move there  => downstream of the command: MuJoCo"
echo "        actuator ctrl mapping / forcerange / physics / gains. Next step:"
echo "        capture /joint_states position min/max for the SAME window and"
echo "        confirm 4/6/7 qpos is bit-for-bit flat while torque varies."
echo "      * joints 4/6/7 show a NARROW/near-constant torque range while"
echo "        1/2/3/5 vary widely  => the *input* barely changes for 4/6/7:"
echo "        the planned trajectory / interpolated q_des,qdot_des for those"
echo "        joints is ~constant (MoveIt IK null-space parking them), or the"
echo "        PD error for them is ~0. Look upstream in the trajectory, not the"
echo "        controller/plugin."
echo "--------------------------------------------------------------------"
echo "    >>> START THE FULL PICK TEST (test_grasp_pick.py) NOW, in another"
echo "        terminal, then this captures 25 s of commanded torque. <<<"
echo "    2026-07-23: widened from 6s to 25s -- test_grasp_pick.py opens the"
echo "    gripper (unrelated to arm torque) BEFORE calling move_to() for the"
echo "    first time, which can eat several seconds of pure gravity-comp hold"
echo "    before any real arm PD-tracking activity starts. A 6s window"
echo "    starting at process launch was too short to reliably catch the"
echo "    ~2s active-tracking burst per move; 25s comfortably spans gripper"
echo "    open + pre-approach + approach + grasp + lift, so start-time"
echo "    precision between terminals no longer matters -- just start this"
echo "    capture, then immediately start the full test in another terminal."
echo "===================================================================="
CAP=$(mktemp /tmp/effort_cmd_capture.XXXX.txt)
echo "  capturing 25 s to $CAP ..."
# A Float64MultiArray prints an empty `layout.dim: []`, then a `data:` line,
# then exactly seven `- <value>` list items (panda_joint1..7 order), ending
# with `---`.  PARSER (fixed 2026-07-23): index WITHIN each message. Reset a
# counter at every `data:` line and tag the k-th following `- value` line as
# panda_joint_k. Do NOT pool all list items globally into fixed groups-of-7 --
# the previous version did that with a regex ([0-9.eE+]+) that silently DROPPED
# any value with a negative exponent (e.g. joint1's ~e-17 values), which
# desynchronised the groups and produced a bogus identical min/max for all 7
# joints. `ros2 topic echo` also interleaves "A message was lost!!!" /
# "total count: N---" noise (sometimes with the "---" glued onto the count
# line, no newline); indexing off `data:`/`- ` lines only ignores all of it.
timeout 25 ros2 topic echo /panda_effort_controller/commands > "$CAP" 2>/dev/null
msgs=$(grep -c '^data:' "$CAP")
echo "  captured $msgs command messages."
if [ "$msgs" -gt 0 ]; then
  echo "  per-joint commanded torque over the window:"
  awk '
    /^data:[[:space:]]*$/ { inmsg=1; idx=0; next }
    inmsg==1 && /^-[[:space:]]/ {
      v=$0; sub(/^-[[:space:]]*/,"",v);
      if (v ~ /^[+-]?[0-9]/) {
        idx++;
        if (idx>=1 && idx<=7) {
          x=v+0;
          if (!(idx in mn)||x<mn[idx]) mn[idx]=x;
          if (!(idx in mx)||x>mx[idx]) mx[idx]=x;
          n[idx]++;
        }
      }
      if (idx>=7) inmsg=0;
      next
    }
    /^---/ { inmsg=0 }
    END {
      if (!(1 in mn)) { print "    (could not parse any 7-value message)"; exit }
      maxrange=0;
      for (i=1;i<=7;i++) {
        r=mx[i]-mn[i];
        printf "    panda_joint%d: n=%-6d min=%9.4f  max=%9.4f  range=%9.4f\n",
               i, n[i], mn[i], mx[i], r;
        if (r>maxrange) maxrange=r;
      }
      print "";
      # HOLD DETECTOR: if EVERY joint is near-constant, no move was captured.
      # A real tracking move drives several-Nm swings on the large joints.
      if (maxrange < 0.5) {
        print "  *** WARNING: ALL 7 joints near-constant (largest range="maxrange" Nm).";
        print "      This window caught a GRAVITY-COMPENSATION HOLD, not a move.";
        print "      It is INCONCLUSIVE for (a) vs (b) -- do NOT interpret it.";
        print "      Re-run and make sure a fresh trajectory is ACTIVELY tracking";
        print "      DURING the 6 s (start the move ~1 s before / just as this";
        print "      capture begins; the node goes stale after 2 s and reverts to";
        print "      a hold, so the move and the window must genuinely overlap).";
      } else {
        print "  (largest per-joint range="maxrange" Nm -- a real move was captured;";
        print "   compare 4/6/7 ranges vs 1/2/3/5 per the (a)/(b) guide above.)";
      }
    }' "$CAP"
else
  echo "  (nothing captured -- was a move actually running during the window?"
  echo "   without a fresh trajectory the node holds via gravity-comp, so all"
  echo "   7 will look near-constant. Re-run and trigger the move DURING the 6s.)"
fi
echo "  (raw capture left at $CAP for a manual second look.)"
