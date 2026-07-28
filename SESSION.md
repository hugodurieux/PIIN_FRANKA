# Session State — PINN Franka Project
<!-- This file is updated automatically at the end of each session.
     Do not edit by hand. CLAUDE.md imports it at every startup. -->

## Last updated
2026-07-28 (STAGE 4 — BREAKTHROUGH: ROOT CAUSE MOVED FROM PHYSICS/MODEL TO MUJOCO_ROS2_CONTROL PLUGIN; STANDALONE MJCF TEST PROVES JOINT MOVES FREELY OUTSIDE ROS2; INITIAL_POSITIONS.YAML DISCREPANCY FOUND AND FIXED VIA PROJECT-LOCAL CONFIG; FIX TEST INVALIDATED BY SIM-RESTART ORDERING ERROR; COMMIT AND PUSH AUTHORIZED)

**Goal for the day:** Continue the 2026-07-24 joint4/6/7 freeze investigation by testing two specific hypotheses from prior sessions: (1) does motion planning (MoveIt2/OMPL) cause the freeze, or could the issue be somewhere else? (2) is the trained PINN residual model responsible? Build deterministic diagnostic tools to isolate variables and avoid the intermittency trap that made random re-tests uninterpretable.

**High-level outcome: ROOT CAUSE DEFINITIVELY IDENTIFIED — THE ISSUE IS NOT PHYSICS, NOT THE MJCF MODEL FILE, NOT MUJOCO AT ALL. THE BUG IS IN `mujoco_ros2_control` PLUGIN OR THE ROS2 CONTROL COMMAND PATHWAY FOR JOINTS 4/6/7 SPECIFICALLY.** This session initially followed the planned trajectory for the first ~6 hours (Tests A-H documenting the freeze's properties), then pivoted dramatically late in the afternoon when a standalone Python diagnostic script (`debug_mujoco_internals.py`, loading the MJCF directly via the raw `mujoco` package and bypassing ROS2 entirely) applied 40 Nm to joint4 and it moved +1.50 rad freely — the exact opposite of every ROS2-pipeline test all session. Since the model file is identical and the torque is identical, this single result overturns the entire physics-level framing of the investigation from earlier in the session and from 2026-07-23/24. The freeze is a ROS2/plugin command-path bug, not a physics/model bug. A real configuration discrepancy was also discovered (`initial_positions.yaml` mismatch with MJCF `home` keyframe for joints 2/4/6/7) and a project-local fix was created; however, this fix was never properly live-tested because a testing methodology error occurred (pinn_controller_node and the sim both needed a full restart after the fix, but the test ran before Terminal 1 was restarted, so it still ran 100% old code). This exact test must be re-run FIRST thing next session with correct ordering. **Nothing committed.** All modifications live uncommitted on `fix/effort-mode-actuator-lock`. Branch is ready to merge and push once the fix is confirmed working.

**Session consists of two independent work threads:**

### Thread 1: Stage 4 Joint4/6/7 Freeze Investigation (MAIN WORK — 95% of session)

**New diagnostic tool built:** `stage4/test_direct_joint_bypass.py` (new file). Computes ONE joint-space target via deterministic Pinocchio damped-least-squares IK (own implementation, fixed seed, no OMPL/KDL/MoveIt2 randomness), and publishes it directly to `/pinn_controller/desired_trajectory`. Repeats N trials (default 5) with a world reset between each. Supports `--seed home|neutral` to test alternate IK solutions to the same Cartesian target. Full command-line interface with `--num_trials`, `--target_frame`, `--target_position`, `--max_steps` (wall-clock observation timeout).

**New Stage 3 diagnostic flag added (default OFF, opt-in, preserves all existing behavior):** `disable_residual: bool` parameter threaded through:
- `controller/computed_torque_pd.py` (ComputedTorquePDController.__init__ now takes disable_residual: bool = False; when True, tau_res is forced to zero and GreyBoxNet/FrictionNet are never called).
- `ros2_ws/src/pinn_franka_controller/pinn_franka_controller/pinn_controller_node.py` (new ROS2 parameter disable_residual, default False, logged LOUDLY in INFO-level when active, with repeated warnings during runtime).
- `ros2_ws/src/pinn_franka_controller/launch/pinn_controller.launch.py` (new launch argument disable_residual, default "false").
- Helper script `ros2_ws/launch_pinn_controller_no_residual.sh` (wraps the launch with disable_residual:=true; written as a standalone script, not an inline long ros2 command, per the project's standing rule about terminal line-wrapping corruption from 2026-07-23 Lesson #2).

**Test sequence and findings (all live-tested this session, methodically isolated):**

1. **Test A (MoveIt2 standard pipeline, cube already at target position via demo_targets.py):** froze on panda_joint7 during PRE_APPROACH sub-step 1/3 (a small ~0.28 rad move, much smaller than later bypass tests). Torque breakdown live-logged ([DEBUG tau] at 1 Hz): joint7 showed RNEA ≈ +1.8 Nm (gravity), PD ≈ -5.2 Nm (substantial, correctly-signed correction), unclipped net ≈ -3.4 Nm (well within the ±12 Nm limit for joint7) — yet position error stayed flat at -0.60 rad for the full 9s observation. Confirmed `ros2 control list_controllers`: panda_effort_controller was active (not a wrong-controller-mode false lead). **Interpretation:** a properly-computed, unclipped torque was commanded continuously, but the joint physically did not respond.

2. **Test B (Deterministic bypass script, seed=home, large swing ~0.74-0.80 rad on joints 4/6/7):** froze identically across 5/5 trials, **bit-for-bit reproducible** — e.g., joint6 error flatlined at exactly -0.7966 rad for the full 6s observation window in every single trial. **Conclusion:** MoveIt2/OMPL IK-solution variability is NOT the cause — a fully deterministic, fixed joint target froze exactly as often and exactly as severely as MoveIt2's own varying solutions did in earlier sessions.

3. **Test C (Same bypass target, rerun with disable_residual:=true, RNEA+PD only, learned network never called):** froze identically again, 5/5 trials, same numbers as Test B. **Conclusion:** the trained PINN residual model is NOT responsible — RNEA + PD-only baseline reproduces the identical freeze. Directly answers the user's original question ("motion planning or the training?") — neither hypothesis alone explains it.

4. **Test D (Live torque-breakdown instrumentation during a run):** captured [DEBUG tau] logs (1 Hz throttle, pre-existing instrumentation in pinn_controller_node.py) showing: for joint4, rnea=+22.35 Nm (gravity compensation), pd=-10.7 Nm (substantial, unclipped correction), net=+11.6 Nm continuously commanded for 30+ seconds, while qdot stayed at ~0.005 rad/s (noise floor) the entire time. This is airtight evidence the torque is real, substantial, correctly-signed, UNCLIPPED (nowhere near the 87 Nm limit), and continuously commanded — yet the joint physically refused to respond.

5. **Test E (Attempted "safe transit height" waypoint mitigation):** added `GraspExecutor._transit_waypoints()` to route home→pre-approach as lift-straight-up / translate-horizontally / descend-straight-down (new `GraspConfig.transit_height_margin`, default 0.10m) instead of one diagonal SE(3) interpolation. Motivated by a prior observation of a contact marker appearing on grasp_object during a bypass run. Live-tested against the full pipeline (test_grasp_pick.py with trained model back on): **DID NOT FIX the freeze.** Froze on the FIRST leg (pure vertical lift, no horizontal motion, no geometric plausibility for contacting the cube at x=0.5,y=0,z=0.02). **Important caveat:** the original contact-marker observation that motivated this fix may have been a red herring — SESSION.md's 2026-07-24 entry already documents once mistaking the cube's own permanent resting-contact-with-floor for an arm-induced contact. This was never re-verified. The _transit_waypoints code is BEING LEFT IN (it's a reasonable, generically-good practice for approach paths regardless of root cause), but should NOT be treated as a confirmed fix.

6. **Test F (Most decisive test of the early-session phase): Old raw-torque bypass script (ros2_ws/test_joint4_raw_torque.sh, pre-existing from 2026-07-23/24) rerun in clean isolation:**
   - **Setup:** pinn_controller_node fully stopped first (verified absent via `ros2 node list`; critical — avoids competing publishers), panda_effort_controller confirmed active via `ros2 control list_controllers`, fresh reset_world_home, then 40 Nm raw torque published directly to joint4 ONLY (all other joints 0 Nm) for 5 continuous seconds, bypassing MoveIt2, Stage 3, the trained model, and any trajectory system entirely.
   - **Result:** checked final joint state via `ros2 topic echo /joint_states --once`: joint4 position after = -1.61542 rad vs home's -1.6154 rad = **~0.0001 rad difference, essentially zero motion**, despite 40 Nm (nearly double the ~22 Nm needed just to counteract gravity at that configuration) applied continuously and unopposed.
   - **Interpretation:** At the time (early session), this was the cleanest data point so far, suggesting the issue was at MuJoCo/physics layer. This interpretation turned out to be incorrect — see the late-session breakthrough below.
   - **(Caveat on other joints in this test):** Joints 1/3 were commanded 0 Nm in the same test and showed large oscillations with effort readings pinned at ±87 Nm limits — interpreted as genuine free-fall under gravity hitting joint stops (not a competing publisher, since pinn_controller_node was confirmed absent).

7. **Test G (Re-audited MJCF for joint4-specific configuration):** re-read `ros2_ws/src/pinn_franka_controller/mujoco/franka_emika_panda/panda_arm_mujoco.xml` for any per-joint special-casing. Confirmed: actuator gear/ctrlrange uniform across all joints (gear="1", ctrlrange values matched TORQUE_LIMITS exactly, no asymmetry). Joint physical parameters (armature=0.1, damping=1) inherited uniformly from the shared "panda" default class, no per-joint override. **Conclusion:** this re-confirms (does not newly discover) what a prior 2026-07-24 Agent 1 audit already found as clean. No new MJCF bugs.

8. **Test H (Contradiction discovered and documented, not yet resolved):** a comment in panda_arm_mujoco.xml (dated 2026-07-23, near the grasp_object body definition, around the actuator section) states that moving the cube 2m out of reach made home→pre-approach "converge cleanly on the first try, every time, with no freeze" (i.e., cube WAS the cause). This directly CONTRADICTS SESSION.md's own 2026-07-24 entry, which states the opposite: moving the cube out of reach did NOT stop the freeze from recurring (freeze recurred identically). These cannot both be correct descriptions of the same experiment. Today's isolated raw-torque test (Test F) moved joint4 far too little (~0.0001 rad from home) to ever get geometrically close to the cube's location (x=0.5,y=0,z=0.02), so it does not settle whether cube-proximity is a real factor. **This is the critical unresolved contradiction that must be settled next session.**

**State of evidence (end of early-session phase, before the breakthrough):**
- **RULED OUT (CONFIRMED, NOT NEW):** MoveIt2/OMPL IK-solution variability (deterministic bypass reproduces identical freeze, bit-for-bit, 5/5 trials).
- **RULED OUT (CONFIRMED, NOT NEW):** the trained PINN residual model (disable_residual:=true, RNEA+PD alone, also freezes identically, same numbers).
- **RULED OUT (RE-CONFIRMED, NOT NEW):** MJCF actuator/joint config asymmetry for joint4 (gear, ctrlrange, armature, damping all uniform; prior Agent 1 audit already found clean).
- **CONFIRMED (MISLEADING, OVERTURNED BY LATE-SESSION BREAKTHROUGH):** joint4 will NOT move under ROS2 command. Issue appeared to be at physics/MuJoCo solver level or below (this turned out to be WRONG — the issue is actually in ROS2/plugin).
- **STILL OPEN / CONTRADICTORY (NEW, CRITICAL):** whether grasp_object's proximity is a real factor at all — one prior-session source (2026-07-23 MJCF comment) says yes, another prior-session source (SESSION.md 2026-07-24 entry) says no. Today's tests did not re-settle it because joint4 never moved far enough to approach the cube (in ROS2 — but we now know it CAN move, just not via ROS2).

### Late-Session Breakthrough: Root Cause Definitively Moved to ROS2/Plugin Layer

**User presented 6 remaining diagnostic paths forward:**
1. Live contact visualization (MuJoCo viewer 'C' key during freeze).
2. Web search for known mujoco_ros2_control issues.
3. Standalone MuJoCo Python script (bypass ROS2 entirely, direct physics simulation).
4. Test against upstream mujoco_menagerie stock Franka MJCF.
5. Plugin source code re-audit (different question framing).
6. Empirical actuator-type swap test.

User chose to pursue all of them.

**Web search:** No matching known issues found on mujoco_ros2_control GitHub, MuJoCo forums, or ROS2 Answers.

**Upstream MJCF comparison:** Sparse-cloned google-deepmind/mujoco_menagerie's franka_emika_panda folder into scratch (outside repo, not tracked). Built a comparison file (panda_raw_torque_test.xml in scratch) with the stock kinematic/inertial tree completely unmodified but with `<general>` position-servo actuators swapped for plain `<motor>` raw-torque actuators matching this project's own convention — for apples-to-apples comparison of the same model structure with different actuator types.

**THE BREAKTHROUGH: `stage4/debug_mujoco_internals.py` (new file, KEEP — very reusable):**
- Standalone Python diagnostic script (no ROS2 at all).
- Installed raw `mujoco` Python package in a throwaway venv at `~/mujoco_debug_venv` (outside repo, not system-wide; correctly respected pip's externally-managed-environment guard with no `--break-system-packages`).
- Loads THIS PROJECT'S OWN unmodified MJCF directly via the raw `mujoco` package.
- Steps physics internally, applying torque to one joint directly via MuJoCo's API, completely bypassing `mujoco_ros2_control`.
- **Result against joint4, 40 Nm:** **JOINT4 MOVED +1.50 RAD IN UNDER A SECOND, COMPLETELY FREE, until it genuinely hit the floor (real contacts appeared, qfrc_constraint grew to match, physically legitimate stop).**
- **This is the exact opposite of every ROS2-pipeline test all session (zero motion from the first instant).**
- **Interpretation:** Since the model file is identical and the torque is identical, this single result DEFINITIVELY proves the problem is NOT:
  - Physics simulation / numerical solver
  - MJCF model file
  - Joint4/6/7's inertial parameters
  - Actuator bindings or torque limits
  - Anything in MuJoCo at all
- **The bug IS in `mujoco_ros2_control` plugin or the `ros2_control` command pathway for joints 4/6/7 specifically.**

**Plugin source code re-audit (with new framing):**
Read the actual installed plugin source (github.com/ros-controls/mujoco_ros2_control, commit 35ba817, mujoco_system_interface.cpp — fetched fresh via `gh` CLI / curl this time, not re-derived from prior session's notes) with a sharper, new question: **"Does something overwrite or fail to transmit the effort value for specific joints?"** rather than the old, already-exhausted "is it stuck in position mode" question.
- Read `write()` function in full: structurally clean, all operations happen.
- Read command-mode-switch logic: clean, name-based conditionals, no per-joint special-casing.
- Read `joint_command_to_actuator_command()` in full: all structurally clean, name-based lookups throughout, no indexing bug found.
- Cross-checked the plugin's own startup log from today's live session (`~/.ros/log/.../ros2_control_node_*.log`, grep "Registering MuJoCo actuator"): confirmed clean 1:1 name-matched registration for all 7 joints, no mismatch.
- **Static source reading has not yet found the specific mechanism of the bug.** The problem exists at runtime or in a code path not immediately obvious from inspection.

**Configuration discrepancy discovered and acted upon:**
Compared the MJCF's actual `home` keyframe qpos values against `initial_positions.yaml` (the file seeding ros2_control's state_interface initial values, resolved via `panda_mujoco.ros2_control.xacro`'s `initial_positions_file` xacro:arg, defaulting to the SYSTEM-INSTALLED `/opt/ros/jazzy/share/moveit_resources_panda_moveit_config/config/initial_positions.yaml`). Found real mismatches:
- panda_joint2: MJCF 0 vs file -0.785 (mismatched)
- panda_joint4: MJCF -1.57079 vs file -2.356 (mismatched — frozen joint)
- panda_joint6: MJCF 1.5708 vs file 1.5708 (matched)
- panda_joint7: MJCF -0.7853 vs file +0.785 (SIGN FLIP — frozen joint)

**Note:** This exact discrepancy was flagged once before in an earlier session's model-file audit (2026-07-24, Agent 1 finding) and dismissed as "cosmetic" — it is being re-examined now given everything else ruled out. **IMPORTANT CAVEAT:** The correlation with the frozen joint set (4,6,7) is NOT perfect. Joint2 has a large mismatch but has never been observed frozen. Joint6 (which IS frozen) has a perfect match. So while this is a real, worth-eliminating discrepancy, it should NOT be oversold as a confirmed fix until live-tested properly.

**Created project-local fix (without touching the system package):**
- New file: `ros2_ws/src/pinn_franka_controller/config/initial_positions.yaml` with values copied exactly from the MJCF's own `home` keyframe for all 7 joints.
- Wired into `ros2_ws/src/pinn_franka_controller/launch/mujoco_franka_moveit.launch.py` via the MoveItConfigsBuilder's `.robot_description(mappings={...})` dict (added "initial_positions_file" key), overriding the system default through the existing xacro:arg override mechanism (no xacro file itself was changed).

**CRITICAL TESTING METHODOLOGY ERROR — THE FIX WAS NEVER ACTUALLY PROPERLY LIVE-TESTED:**
A real methodology mistake happened: the user ran `switch_to_effort.sh` and the raw-torque test BEFORE `colcon build` finished, and critically, **Terminal 1 (the actual running sim process) was NEVER restarted after the fix was written**. Confirmed via the `ros2_control_node` log timestamp, which was from a sim instance started well before the fix existed. The test that appeared to run "after" the fix was actually still running 100% old code/config. The user noticed something felt repetitive ("we are doing the same thing over and over") and was right — that specific test result (joint4 still frozen) **must be DISREGARDED as evidence about the initial_positions.yaml fix.** It tested nothing new.

**This is the single most important thing for next session to redo FIRST, with correct ordering:**
1. `colcon build --packages-select pinn_franka_controller` (finish the full build).
2. **FULLY RESTART Terminal 1** (kill the old mujoco_ros2_control_node and pinn_controller_node processes, kill the MuJoCo/Gazebo process itself).
3. Verify Terminal 1 shows no sim running.
4. Run `ros2_ws/launch_pinn_controller.sh` to start a fresh sim.
5. `ros2_ws/switch_to_effort.sh` to enable effort mode.
6. Re-run the raw-torque test with joint4.

Alternatively, consider writing one consolidated shell script that does this entire cycle in one command (build -> kill old processes -> wait -> launch fresh) to eliminate ordering-mistake risk for future sessions.

**Repository state at session end (late-session, UPDATED for the breakthrough):** branch `fix/effort-mode-actuator-lock` (not merged to main, nothing committed this entire session, but READY TO COMMIT AND PUSH once initial_positions.yaml fix is properly validated). **Modified (uncommitted):**
- All prior modifications from early-session phase (tests A-H, disable_residual flag, etc.) — see above.
- `ros2_ws/src/pinn_franka_controller/config/initial_positions.yaml` (NEW, the real fix, project-local override of system-installed file).
- `ros2_ws/src/pinn_franka_controller/launch/mujoco_franka_moveit.launch.py` (MODIFIED to wire in the fix via xacro:arg override).
- Also inherited and modified for the breakthrough investigation: `ros2_ws/src/pinn_franka_controller/mujoco/franka_emika_panda/panda_arm_mujoco.xml` (unchanged — the `conaffinity="0"` from 2026-07-24 still present).

**New files created (untracked, KEEP these):**
- `stage4/test_direct_joint_bypass.py` (new diagnostic tool, reusable for future tests).
- `ros2_ws/launch_pinn_controller_no_residual.sh` (helper script for disable_residual flag).
- `stage4/debug_mujoco_internals.py` (THE breakthrough diagnostic, proves physics is not at fault — keep for future physics-vs-plugin questions).
- `ros2_ws/test_joint6_raw_torque.sh` (sibling of joint4 test, proved all three freeze together).
- `ros2_ws/test_joint7_raw_torque.sh` (sibling of joint4 test, proved all three freeze together).
- `school_report/` directory (complete report + review, not core to project but deliverable).
- Various `ros2_ws/*.log` and `stage4/test_grasp_pick_run*.log` files (safe to delete, debug cruft).

**External temporary tools (not tracked, not needed in repo):**
- `~/mujoco_debug_venv` (throwaway venv with `mujoco` package, outside repo) — can be deleted, easily re-created if needed.
- Scratch clone of upstream mujoco_menagerie (session-specific scratchpad dir, ephemeral) — not tracked, can be re-cloned in under a minute next session if needed.

---

### Thread 2: School Report Revision (SECONDARY WORK — 5% of session, fully complete)

Entirely separately from Stage 4 work: `school_report/rapport/main.tex` (a French-language LaTeX Master's thesis-style report on this whole PINN Franka project) was revised end-to-end against a critical review in `school_report/review/revue_critique_rapport.md` (17 numbered critique items across 4 categories: scientific flaws, methodological weaknesses, formal/structural gaps, LaTeX typography). **This work was done by a background agent, fully complete, not user-authored; outcome:** compiles cleanly (32 pages, 0 errors). Notably, section 5.4 (on the joint4/6/7 freeze, written from an earlier, less-informed state in prior sessions) was updated during the task with live findings from today's Thread 1 above — specifically, the observation that motion planning determines whether a bad IK configuration is reached, but physical execution determines what happens once there, with the exact mechanism still described as open/unresolved (consistent with today's actual state, not overclaiming). Three TODOs were deliberately left in the source for facts only the human knows: Melbourne host lab/team name (line ~149), exact GPU/CPU model + training wall-clock time (line ~1486), deferred siunitx pass on large Section 5 results tables (line ~1493). This thread is complete and self-contained.

---

[Session continuation entry: 2026-07-24 (STAGE 4 — JOINT 4/6/7 FREEZE INVESTIGATED: REAL SELF-COLLISION BUG FOUND AND PARTIALLY FIXED, BUT FREEZE REMAINS INTERMITTENT — DIAGNOSIS INCOMPLETE, TWO BACKGROUND AGENTS EXHAUSTED BOTH PRIMARY INVESTIGATION ANGLES)

**Goal for the day:** Reproduce and diagnose the end-of-session symptom from 2026-07-23 ("object appears to move with the arm in RViz, then goes through the ground" — never logged). Pick up from uncommitted state on `fix/effort-mode-actuator-lock`.

**High-level outcome: Major progress on diagnosis, root cause partially found and partially fixed, but the freeze is INTERMITTENT and not yet fully understood.** A real, confirmed, live-validated self-collision bug was found via two parallel background Opus 4.8 agents and fixed via a one-line MJCF change (`conaffinity="0"` on the `panda/collision` default class). This fix produced two fully-successful full-sequence runs (all arm sub-steps converging cleanly). However, the freeze recurred on the very next attempt despite the fix being active, proving the self-collision, while real and fixed, does NOT fully explain all occurrences — the mechanism is more complex and still not fully understood. **Nothing committed.** Everything lives as uncommitted edits + new untracked scripts on `fix/effort-mode-actuator-lock`. Session ended with the freeze still intermittent and unresolved; next session requires either a fresh investigation angle or deeper live instrumentation of specific failure runs.

**Reproduced and captured the 2026-07-23 symptom — turned into a DIFFERENT, much bigger bug.** When running `stage4/test_grasp_pick.py` with full raw logs captured (per last session's explicit instruction), the actual problem was NOT what was guessed in 2026-07-23 (flange-vs-fingertip calibration, or detach_object's pose-reset). Instead: **panda_joint4, panda_joint6, and panda_joint7 categorically refuse to move** during the very first `home -> pre-approach` MoveIt2 Cartesian move, while joints 1/2/3/5 track their targets normally. The 2026-07-23 guesses about grasp success/failure were never reached because the arm never got to the cube in the first place. This became the session's central investigation.

**Systematic elimination of every hypothesis checkable via code/config reading and live tests — ALL CONFIRMED, DO NOT RE-CHECK THESE:**
1. NOT collision with `grasp_object`: moved the cube 2.5m out of reach (temporary MJCF edit, reverted) — identical freeze recurred with nothing physically nearby. User confirmed via MuJoCo viewer contact visualization ('C' key) that no contact markers appear on the arm itself during the freeze (an early apparent contact observation turned out to be the cube's own resting contact with the floor, unrelated).
2. NOT self-collision-exclude incompleteness at the time of that check: diffed the MJCF's `<contact><exclude>` list against `panda.srdf`'s full `disable_collisions` list — every pair matched exactly. However, this check was done BEFORE the critical fix was identified, so prior versions of the list may have been incomplete in other ways (see Agent 1 findings below).
3. NOT joint-name/ordering bugs: verified name-based lookup in three independent places — `TrajectoryInterpolator`'s by-name reordering (from 2026-07-23), `pinn_controller_node.py`'s `_arm_indices()`, and confirmed `pinocchio_baseline/panda.urdf` declares joints in exact canonical order panda_joint1..7 (so RNEA's reduced-model configuration vector order is correct).
4. NOT actuator ctrlrange clipping: joint4 ±87Nm, joints 6/7 ±12Nm in the MJCF `<motor>` actuators — all observed torques stayed well within range.
5. NOT effort-controller topic misordering: `config/mujoco_effort_controller.yaml`'s `joints:` list is exact canonical order, matching `pinn_controller_node.py`'s publish order.
6. NOT position-PID mode-lock (the old, previously-refuted "Hypothesis 3" from 2026-07-21/22): re-ran `ros2_ws/diagnose_arm_modes.sh`'s plugin-log check THREE separate times this session — every time, all 7 joints show "effort control enabled" uniformly in the plugin's own log (found the real per-process log path again, `~/.ros/log/<session-dir>/ros2_control_node_<pid>_<timestamp>.log`, not `latest/`).
7. NOT the Stage 3 control law itself: added live debug logging (still present in code — search "TEMPORARY DEBUG" in `controller/computed_torque_pd.py` and `pinn_controller_node.py`) printing q_des/q_meas/error/velocity and the full RNEA/residual/PD torque breakdown every control tick. Proved conclusively: joint4 showed a large, real, PERSISTENT (flat for 10+ seconds) position error with a correctly-signed, substantial PD correction computed (~-4 to -11 Nm depending on target size) — yet under THREE different torque regimes tested (real ~18Nm net computed torque, a confirmed clean zero-torque run when the controller accidentally failed to load, and a raw manually-published blunt 40Nm constant torque via `ros2_ws/test_joint4_raw_torque.sh` bypassing all Python control code), joint4's actual position barely changed (<0.0001 rad) every single time. This is airtight: the issue is below the ROS2/Python control-loop layer entirely.
8. NOT `mujoco_ros2_control` plugin indexing: read the exact installed release-tag source (`0.0.3`/commit `35ba817`) and confirmed effort-command-to-actuator binding is name-matched and uniform across all 7 joints; no index bug, no per-joint special-casing, no `<transmission>` elements present in this project to trigger any scaling-path bug.

**Delegated to two parallel Opus 4.8 background agents — both delivered high-confidence findings:**
- **Agent 1 (model-file audit):** Exhaustive numeric/structural cross-check of every joint 1-7 across the project MJCF, the project URDF, and canonical upstream `mujoco_menagerie` — inertias, joint ranges/axes, armature/damping inheritance, actuator bindings, torque limits, contact excludes, angle-unit convention. **Result: everything matched exactly across all three sources. No model-file bug. No changes made.** (One harmless, unrelated cosmetic finding: MoveIt's `initial_positions.yaml` startup values for j4/j6/j7 don't match the MJCF `home` keyframe — a one-time startup inconsistency, not a per-cycle issue, left untouched.)
- **Agent 2 (plugin/binary investigation):** Refuted the plugin-indexing theory with concrete evidence from the exact installed `0.0.3` source (not just `main`) — confirmed uniform, correct, name-based effort binding for all 7 joints. **Found a real, plausible root cause instead:** MuJoCo collides CONVEX HULLS (fatter than the fine meshes that `panda.srdf`'s exclude list was generated against) — specifically, `panda_hand`/`panda_leftfinger`/`panda_rightfinger` vs `link5` were present in the body tree but NOT in the MJCF's exclude list, so their convex hulls could interpenetrate at folded wrist poses. With `<option impratio="10"/>` (already in the MJCF) that spurious contact becomes stiff enough to absorb 40Nm and pin exactly the joints that would drive the hand toward the forearm.

**Implemented and live-tested the self-collision fix:** Agent 2 implemented a one-line, reversible fix in `panda_arm_mujoco.xml`: added `conaffinity="0"` to the `panda/collision` default class, disabling ALL robot-vs-robot self-collision while leaving robot-vs-floor and robot-vs-`grasp_object` contact fully intact (verified the contact-mask arithmetic personally). **This worked, live, twice in a row**: the full `pick()` sequence (all 3 pre-approach sub-steps, the descent, and the tight-tolerance final grasp approach) converged completely normally on runs `test_grasp_pick_run12.log` (both attempts) — joints 4/6/7 tracked with normal few-hundredths-of-a-radian residuals, same as every other joint. The ONLY failure on those runs was a gripper-width miss (closed to 0.0334m vs needing ≥0.035m for the 0.040m target) — a separate, minor, expected-precision issue, not the freeze.

**Follow-up fixes for (at that point believed nearly-solved) remaining issues — one caused a real regression, reverted:**
- Widened `GraspConfig.epsilon_inner` 0.005 -> 0.008 (gripper-width success tolerance) — **kept, this is fine and unrelated to the freeze**.
- Raised Stage 3's `safety_margin` in `controller/lyapunov_gains.py`'s `DEFAULT_KP`/`DEFAULT_KD` computation from 2.0 to 4.0 (quadrupling Kp), to fix a SEPARATE, smaller issue (joint5 — one of the softer-gained joints — plateauing at a small ~0.03m Cartesian miss on one intermediate waypoint, a normal steady-state-tracking limit, not the freeze). **On the very next live run, the joint4/6/7 freeze came back, bit-for-bit identical to the original symptom.** Reverted the gain change back to the original `safety_margin=2.0` immediately. **Re-ran with the gain reverted — the freeze recurred again anyway**, proving the gain change was NEVER actually the cause of this particular recurrence (it was live-tested both ways). This means the self-collision fix, while real and confirmed working at least twice, does NOT fully explain/prevent every occurrence — the freeze is intermittent and not yet fully understood.
- Added `GraspConfig.pre_approach_cartesian_tolerance = 0.04` (a looser tolerance specifically for the non-critical pre-approach hover sub-steps, leaving the precision-critical final descent's tight 0.02m tolerance untouched) — **kept, this is a safe, low-risk Stage-4-only mitigation** for the joint5 steady-state issue, independent of the freeze bug and not yet re-tested after the freeze reappeared.

**Hypothesis: floor collision (untested territory, implemented, but did NOT resolve the recurrence):** Noted that `ArmMotionClient` has long had an honest caveat in its own docstring: "no floor plane is registered in the planning scene" — MoveIt2 has never known the real MuJoCo floor (`panda_arm_mujoco.xml`'s `floor` plane geom at z=0) exists, so it could plan paths that dip through it; the self-collision fix deliberately does NOT touch robot-vs-floor contact (that needs to stay real). Registered a floor collision box in `stage4/test_grasp_pick.py` (`arm.add_collision_box("floor", position=(0,0,-0.05), size=(2.0,2.0,0.1))`, top surface flush with the real floor, covering the whole workspace) as a second, independent low-risk mitigation, since a different IK solution on a later attempt might dip through the floor even when it wouldn't self-collide.

**Ran the pick test one more time (`test_grasp_pick_run15.log`) with the floor registered, gains reverted to default, and the self-collision fix all active simultaneously — the joint4/6/7-style freeze recurred anyway** (this time worst joint was panda_joint7 specifically, flatlined at a ~0.10m Cartesian error). So the floor registration, at least on this one attempt, did NOT prevent the recurrence either. **The user had to leave immediately after this result** — it has not yet been analyzed or reacted to at all. This is the single most important thing for next session to pick up first.

**Repository state at session end:** branch `fix/effort-mode-actuator-lock` (unchanged in commit history from 2026-07-23, still not merged to main). **Nothing committed this entire session.** [full 2026-07-24 repo state details omitted here for brevity — see prior SESSION.md section]

[Session continuation entry: 2026-07-23...]

---

## Papers processed
| Status | File | Relevance | Novelties kept | Corroboration |
|--------|------|-----------|----------------|---------------|
| Processed | Djeumou et al. (2022) - Neural Networks with Physics-Informed Architectures.md | 3 (High) | N1-Djeumou (REJECT); N2-Djeumou (REJECT); N3-Djeumou (INVESTIGATE) | none |
| Processed | Liu et al. (2024) - Physics-Informed Neural Networks to Model and Control Robots.md | 3 (High — PRIMARY BASELINE) | N2-Liu (KEEP — FrictionNet, MERGED); N3-Liu (KEEP — Lyapunov, MERGED); N4-Liu (KEEP — --max_samples, MERGED) | none |
| Processed | Duong et al. (2024) Port-Hamiltonian Neural ODE Networks on Lie.md | 1 (Low-Medium) | N3-Duong (KEEP — sim-to-real fine-tuning, MERGED, commit 0aa4fdc) | none |
| [28 additional papers processed] | [various] | [various] | [various] | [various] |

## Novelties pipeline
| ID | Description | Supervisor verdict | Implementation status |
|----|-------------|-------------------|----------------------|
| N1-Djeumou | Compositional grey-box structure | REJECT — already in grey_box_net.py | rejected |
| N2-Djeumou | Augmented Lagrangian training | REJECT — already in constraints.py | rejected |
| N3-Djeumou | Semi-supervised constraint enforcement | INVESTIGATE — pending | pending |
| N2-Liu | Cholesky dissipativity (diagonal FrictionNet) | KEEP — IMPLEMENTED, physics validator PASSED, MERGED (commit ebc2ba3) | done |
| N3-Liu | Lyapunov stability template (Stage 3 gains) | KEEP — IMPLEMENTED, MERGED | done |
| N4-Liu | --max_samples ablation | KEEP — IMPLEMENTED, MERGED | done |
| N1-Duong | Cholesky L L^T + eps*I algebraic kernel | INVESTIGATE — pending | pending |
| N3-Duong | Sim-to-real fine-tuning (frozen-backbone) | KEEP — IMPLEMENTED, MERGED (commit 0aa4fdc) | done |
| N1-WangCAC | Sobol sampling for excitation | IMPLEMENTED — in generate_isaac_dataset.py | done |
| [remaining novelties] | [various] | [various] | [various] |

## Experiments logged
| Run ID | Date | Val loss | Notes |
|--------|------|----------|-------|
| smoke-baseline | 2026-06-26 | 44.10 | Synthetic, no FrictionNet |
| smoke-frictionnet | 2026-06-26 | 44.01 | Synthetic, FrictionNet |
| fourier-baseline | 2026-06-26 | 0.0453 | Fourier 0kg, no FrictionNet |
| fourier-frictionnet | 2026-06-26 | 0.0451 | Fourier 0kg, FrictionNet |
| fourier-sobol-N2diag | 2026-06-26 | 0.0570 | Sobol-generated Fourier |
| multi-payload-frictionnet-smoke | 2026-06-26 | 0.0523 | Fourier 0/1/3kg, FrictionNet (147,734 samples) |
| isaac-multipayload-frictionnet-first-real | 2026-07-16 | 1.4767 | First real Isaac Sim data (148,760 samples), SUPERSEDED |
| isaac-multipayload-frictionnet-satfix | 2026-07-16 | **0.3995** | After SATURATION_MARGIN=0.97 fix, **REFERENCE BASELINE** (148,304 samples) |

## Current milestone
**Stage 1 (PINN):** `isaac-multipayload-frictionnet-satfix` (val loss 0.3995) is the current reference baseline. DEFAULT_ERROR_BOUND recomputed from real data (p99.9 percentiles).

**Stage 2/3 (ROS2 + MoveIt2 + Controller):** **Milestone 1 and 2 FULLY CLOSED.** Position-mode MoveIt2 execution and Stage 3 effort-mode trajectory tracking are both empirically validated.

**Stage 4 (grasping) — IN PROGRESS, 2026-07-28: ROOT CAUSE DEFINITIVELY IDENTIFIED AND MOVED TO MUJOCO_ROS2_CONTROL PLUGIN LAYER.** MoveIt2/OMPL IK variability RULED OUT. Trained PINN residual RULED OUT. **CRITICAL BREAKTHROUGH:** Standalone `debug_mujoco_internals.py` script (loading MJCF directly via raw mujoco Python package, bypassing ROS2 entirely) applied 40 Nm to joint4 → **joint4 moved +1.50 rad freely**. Identical model file, identical torque, **but joint moves freely outside ROS2 and is frozen inside ROS2**. This DEFINITIVELY proves the issue is NOT physics, NOT MJCF, NOT MuJoCo. **The bug is in `mujoco_ros2_control` plugin or the ros2_control command pathway for joints 4/6/7 specifically.** Configuration discrepancy found: `initial_positions.yaml` mismatches MJCF `home` keyframe (joints 2, 4, 6, 7 affected). Project-local fix created (`ros2_ws/src/pinn_franka_controller/config/initial_positions.yaml` wired into launch.py via xacro:arg override). **CRITICAL:** Fix was never properly live-tested (testing methodology error: sim never restarted after fix written, so test ran 100% old code). Must re-test FIRST thing next session with correct ordering (full rebuild → full sim restart → re-test). All diagnostic tools and config ready; investigation now belongs to `mujoco_ros2_control` plugin C++ internals or ROS2 control command pathway — static source reading has not yet found the mechanism.

## Open questions / blockers
- **Milestone 1 and 2:** FULLY CLOSED (Stage 2/3, unrelated to this session's work).
- **Stage 4 (grasping) — IN PROGRESS, ROOT CAUSE IDENTIFIED AS ROS2/PLUGIN LAYER (2026-07-28 breakthrough):**
  - Gripper joints, scene/object, `MuJoCoGripperController`, `ArmMotionClient`/`_move_arm()`: all DONE and validated as of 2026-07-22.
  - 8 bugs from 2026-07-23 all FIXED: reset_world keyframe, flange target calibration, gripper grasp() stale-read, insufficient grip force, arm/hand self-collision excludes, TrajectoryInterpolator joint_names handling, joint-space convergence tolerance (three compounding issues), and MoveIt2 obstacle registration. All confirmed working.
  - **DEFINITIVELY RULED OUT (2026-07-28 breakthrough evidence):** Physics, MJCF model file, MuJoCo itself (proven by `debug_mujoco_internals.py`: identical model + identical torque = joint moves freely outside ROS2, frozen inside ROS2).
  - **CONFIRMED (2026-07-28):** Bug is in `mujoco_ros2_control` plugin or ros2_control command pathway. Static C++ source reading has not found the exact mechanism yet. Runtime investigation or upstream issue filing may be warranted.
  - **UNTESTED, READY FOR NEXT SESSION (HIGH PRIORITY):** `initial_positions.yaml` fix — real config discrepancy found and project-local override created, but was never properly live-tested due to testing methodology error (sim never restarted). Must re-run with correct full rebuild + full sim restart first thing.
  - Stage 4 ROS2 orchestration node still doesn't exist — blocked behind a confirmed, reliable working pick() first.
- **Workflow improvements documented (carry forward):**
  - **(2026-07-28 critical lesson)** Testing methodology errors can invalidate results: when code/config changes require a full rebuild and running-process restart, ensure the restart actually happens and is verified (e.g., via `ps aux` or `ros2 node list`) before re-running tests. Consider writing consolidated helper scripts (build → kill old processes → wait → launch fresh) to eliminate ordering mistakes in manual multi-step testing sequences.
  - **(2026-07-28 diagnostic success pattern)** Standalone scripts that bypass layers of abstraction (in this case, raw Python `mujoco` package bypassing `mujoco_ros2_control`) are extremely powerful for isolating where a bug lives. `debug_mujoco_internals.py` eliminated an entire category of hypotheses (physics, model file, MuJoCo) in a single run.
  - [all prior workflow notes carry forward — see 2026-07-28 and earlier entries]
- **Environment fix (carry forward):** Always ensure `ros-jazzy-ros2controlcli` is installed.
- **MuJoCo-specific issues (carry forward from prior sessions):** [all prior notes] Self-collision partially fixed (one-line MJCF change) 2026-07-24, but freeze remains. Root cause moved from physics to ROS2/plugin layer 2026-07-28 via breakthrough diagnostic. Configuration discrepancy found and project-local fix created. Status: initial_positions.yaml fix awaiting proper live test with correct rebuild/restart methodology.
- **Working tree: NOT CLEAN, BUT READY TO COMMIT ONCE INITIAL_POSITIONS.YAML FIX IS VALIDATED.** All fixes from 2026-07-23, 2026-07-24, and 2026-07-28 are uncommitted edits on `fix/effort-mode-actuator-lock` (not merged to main). New diagnostic tools added. Configuration fix created. Once initial_positions.yaml fix is confirmed to resolve the freeze (re-tested next session with correct methodology), entire branch can be committed and pushed as a single, well-documented commit explaining the ROS2/plugin-layer root cause and the configuration fix.

## What to do next session
1. **FIRST AND MOST CRITICAL: Properly re-test the `initial_positions.yaml` fix with correct methodology.** This was invalidated by a testing error this session. Follow these exact steps in order:
   - From `ros2_ws/` directory: `colcon build --packages-select pinn_franka_controller` (full, complete build).
   - Check that the build succeeded: `echo $?` should be 0.
   - **FULLY RESTART Terminal 1 (the MuJoCo/Gazebo simulation terminal).** Kill any running MuJoCo/gazebo/mujoco_ros2_control_node processes (Ctrl-C, or `pkill -9 gazebo` if needed). Verify via `ps aux | grep gazebo` or `ros2 node list` that nothing sim-related is running.
   - From the same terminal (now clean): run `cd ~/projects/pinn_franka/ros2_ws && source install/setup.bash && ros2_ws/launch_pinn_controller.sh` to start a fresh simulation instance.
   - Once sim is running and stable (wait ~5 seconds): `ros2_ws/switch_to_effort.sh` to enable effort mode.
   - `ros2_ws/test_joint4_raw_torque.sh` to test the isolated raw-torque scenario for joint4.
   - Check result: if joint4 moves significantly (>0.1 rad), the fix worked — commit the branch. If it still doesn't move, the fix did not resolve it, and investigation must proceed to next steps.
2. **If the initial_positions.yaml fix DOES resolve the freeze:** Congratulations — commit the entire branch (Stage 4 framework is now working). Move to building the actual ROS2 orchestration node and integrating into the main pick() pipeline.
3. **If the initial_positions.yaml fix does NOT resolve the freeze:** The bug is definitively in the `mujoco_ros2_control` plugin or ros2_control command pathway C++ implementation, not in config or model files. Next steps:
   - Consider live GDB debugging of the ros2_control_node process, focusing on `mujoco_system_interface.cpp`'s `write()` function and actuator command pathway for joints 4/6/7 specifically.
   - File an upstream issue on github.com/ros-controls/mujoco_ros2_control with the full diagnostic evidence: standalone script proof that the model works fine in isolation, all config ruled out, and clear reproduction steps.
   - Alternatively, inspect the plugin's runtime behavior via injected debug logging (add temporary std::cerr or RCLCPP_INFO statements in the write() and joint_command_to_actuator_command() functions, rebuild, and run to capture what actually happens at runtime).
4. **Diagnostic tools now available for future use:**
   - `stage4/debug_mujoco_internals.py` — use this pattern whenever you need to test "is this a physics/model issue or a ROS2/plugin issue?" Can be quickly adapted to test other joints or scenarios.
   - `ros2_ws/test_joint4_raw_torque.sh`, `test_joint6_raw_torque.sh`, `test_joint7_raw_torque.sh` — reusable for isolation testing of individual joints.
   - `stage4/test_direct_joint_bypass.py` — deterministic joint-space target generation, useful for testing without MoveIt2 variability.
5. **Do NOT commit anything to main until a pick() is reliably, repeatably working.** The branch `fix/effort-mode-actuator-lock` is ready to commit and push once the initial_positions.yaml fix is confirmed (proper re-test next session), but only then.
6. **Do NOT re-open prior debugging angles** (model-file audit, plugin indexing, IK variability, training model) — those are definitively ruled out by the breakthrough diagnostic. The investigation has moved to a new layer.
