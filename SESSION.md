# Session State — PINN Franka Project
<!-- This file is updated automatically at the end of each session.
     Do not edit by hand. CLAUDE.md imports it at every startup. -->

## Last updated
2026-07-29 (STAGE 4 SOLVED AND WORKING END-TO-END — "JOINT 4/6/7 FREEZE" ROOT CAUSE FOUND: `ResetWorld` SILENTLY REVERTS mujoco_ros2_control TO ITS INTERNAL POSITION PID. FIVE FURTHER BUGS FIXED BEHIND IT. FULL pick() SUCCEEDS 2/2 AT x=0.65: CUBE GRASPED AND LIFTED.)

**Goal for the day:** Re-test the untested `initial_positions.yaml` fix with correct rebuild/restart methodology, then get a working Stage 4 pick.

**High-level outcome: THE WEEK-LONG "panda_joint4/6/7 FREEZE" IS SOLVED, AND `pick()` NOW COMPLETES END-TO-END — cube grasped and lifted, twice in a row.** The freeze was never physics, never the MJCF, never the trained model, and NOT the `mujoco_ros2_control` command pathway either (the 2026-07-28 conclusion — see the correction banner below). It is this:

> **`mujoco_ros2_control`'s `ResetWorld` service silently reverts every joint to its INTERNAL position PID** (`config/mujoco_pid.yaml`). It does not route the change through `perform_command_mode_switch()`, so **nothing reports it**: the plugin logs no mode line, `controller_manager` still lists `panda_effort_controller` as ACTIVE, `ros2 control list_controllers` looks healthy, commands still publish and `ros2 topic echo` shows them, and the arm holds itself up convincingly. Every torque published to `/panda_effort_controller/commands` is discarded. The arm settles at `(home_keyframe - tau_gravity / p_position_pid)`, pinned to ~1e-5 rad.

**Why it survived a week:**
1. **All seven joints freeze**, but only joints whose target is far from home LOOK frozen. The symptom therefore presented as a "joint 4/6/7" problem and sent three sessions hunting for what those three joints have in common. They have nothing in common — 4/6/7 simply had far targets. Joints 1/2/3/5 were equally frozen.
2. **Every status layer reports healthy.** The only signal that ever contradicted it was arithmetic: `p * (home - measured)` reproducing the measured effort.
3. **`reset_world_home` is exactly what you run between tests to get a clean start** — so the more carefully a test was isolated, the more reliably the bug was reintroduced.

**Decisive evidence (all live):**
- Runs 13/14/15 (2026-07-24) hold **bit-identical** positions across three separate runs, each equal to `home - tau_gravity/p`, on three joints with two different gains, agreeing to **1e-5 rad**:
  `joint4: 22.351/500 -> -1.61549 (logged -1.61540)`, `joint6: 2.085/150 -> +1.55689 (logged +1.55691)`, `joint7: 0.000/150 -> -0.78530 (logged -0.78529)`.
- Raw 40 Nm to joint4 after a reset: **commanded 40 Nm, measured effort +23.5 Nm** = `500 * (home - current)`, i.e. the position PID, not the command. Joints 1/3 commanded 0 Nm read **±87 Nm saturated** and oscillated — the same PID unstable.
- Running `force_effort_mode.sh` with the controller stopped made the arm **go limp instantly**. Same sim, same second, opposite behaviour. That is the proof.

**Why `switch_to_effort.sh` cannot fix it:** `panda_effort_controller` is still ACTIVE from `controller_manager`'s point of view, so a switch activating it is rejected as a no-op (`ok=False, "already active"`) and `perform_command_mode_switch()` is never called. Only a real deactivate -> activate cycle works.

### Fixes made (all live-validated unless stated)

**1. The freeze — `ros2_ws/force_effort_mode.sh` (NEW).** Forces effort -> position -> effort so the plugin re-runs `perform_command_mode_switch()`. Verifies against the PLUGIN'S OWN LOG (`controller_manager` is the layer that lies). **`ros2_ws/reset_world_home.sh` now calls it automatically** whenever `panda_effort_controller` is active — the trap is defused where it cannot be forgotten. (It fired a third time mid-session and silently invalidated run26 before this was added.)

**2. Steady-state tracking — `gain_safety_margin_override:=4.0`.** Flange error 0.054 m -> 0.005-0.027 m; worst joint 0.10 rad -> ~0.01-0.05. Predicted from `e_ss = tau_residual/Kp` and matched to three decimals. Passed via `ros2_ws/launch_pinn_controller_boosted.sh 4.0`. NOT yet made the default in `controller/lyapunov_gains.py`.

**3. Latent crash in the gain-override path — `pinn_controller_node.py`.** `get_logger().warn()` was called with logging-style lazy `%s` args; rclpy's `RcutilsLogger` takes ONE pre-formatted string and raises `TypeError`. This killed the node at startup, so `launch_pinn_controller_boosted.sh` had been **dead on arrival since it was written on 2026-07-24** — the "do stronger gains move joints 4/6/7?" experiment was never actually run.

**4. Leaked planning-scene attachment — `stage4/test_grasp_pick.py`.** `pick()` attaches `grasp_object` before the approach and, on an `ARM_TIMEOUT` there, aborts without reaching `_detach_object()`. The planning scene lives in `move_group`, so the attachment survives every restart of the test script. Confirmed via `/get_planning_scene`: a phantom box hanging **0.307 m** off `panda_hand` at a tumbled orientation, riding along with every plan and rejecting goals `run20` had planned fine minutes earlier. Now cleared defensively at startup (`detach_object` + `remove_collision_object`).

**5. Attach-before-descent vs the floor box — floor registration REMOVED.** `_attach_object()` runs at the pre-approach pose while the cube is still on the floor, so MoveIt stores it at `0.02 - 0.3299 = -0.3099 m` below the flange. On the descent the *phantom* cube follows the gripper down to `z = -0.08`, through any floor box. There is no floor height both deep enough to clear it and shallow enough to be useful. The floor box was itself added 2026-07-24 for the disproven freeze theory; MuJoCo's real floor plane still stops the arm physically. **Proper fix, deferred:** do not attach before the descent — attach only after the gripper closes (what MoveIt's own pick pipeline does, and what is physically true), then the floor box can return.

**6. IK reliability at longer reach — `config/kinematics.yaml` (NEW), wired via `MoveItConfigsBuilder.robot_description_kinematics()`.** Stock KDL gets `kinematics_solver_timeout: 0.05`; near-singular top-down goals at x=0.65 then failed intermittently with `Unable to sample any valid states for goal tree` (run25 planned approach 1/2 and failed 2/2; run27 failed 1/2 — same poses). Raised to 0.25 s + explicit attempts. `num_planning_attempts` 1 -> 10 in `arm_motion_client.py` as well (not sufficient alone — every attempt re-samples through the same under-budgeted solver).

**7. Flange-to-fingertip offset — `stage4/demo_targets.py`, 0.2099 -> 0.1029 m.** The chain opened with "panda_link8 -> panda_hand = 0.107", but that 0.107 is `panda_link7 -> panda_link8`. In `pinocchio_baseline/panda.urdf` the hand is mounted on link8 with `xyz="0 0 0"` — **zero translation**, pure -45 deg rotation. Since the IK target IS link8, the term was counted twice and held the fingertips ~10 cm too high. Measured live: run28 closed to **0.0336 m** through empty air.

**8. Gripper 45 deg mount — `_TOP_DOWN_FINGERS_ALIGNED` in `demo_targets.py`.** The fingers slide along `panda_hand`'s y-axis, but the grasp target is specified for `panda_link8`, and the hand carries a -45 deg twist (`rpy="0 0 -0.785398"`). Plain `_TOP_DOWN` therefore presents the fingers **diagonally across** the cube. Measured live: run29 stopped at **0.0526 m** = the cube's diagonal (`0.04*sqrt(2) = 0.0566`) less corner squeeze. Right-multiplying by `Rz(+45 deg)` makes the HAND axis-aligned while leaving the approach axis at `(0,0,-1)`.

**Note that bugs 7 and 8 both come from ONE line of the robot description** — `panda_hand_joint`, `xyz="0 0 0" rpy="0 0 -0.785398"`. Zero translation caused the height error; the rotation caused the diagonal grasp.

### Result: Stage 4 pick() WORKS

Cube moved 0.50 -> **0.65 m** (5 sites kept in sync: MJCF body pos, MJCF `home` keyframe freejoint qpos, `demo_targets.py`, and two in `test_grasp_pick.py`).

| | run30 | run31 |
|---|---|---|
| All 5 pre-approach sub-steps | converged | converged |
| Approach 1/2, 2/2 | converged | converged |
| Final grasp error | **0.0066 m** (tol 0.0200) | **0.0186 m** (tol 0.0200) |
| Gripper width (target 0.040) | **0.03999612** | **0.03990805** |
| Lift 0.150 m | converged | converged |
| Result | **SUCCESS** | **SUCCESS** |

Gripper width worked as a measuring instrument across the diagnosis: `0.0336` (air, too high) -> `0.0526` (diagonal corners) -> `0.0400` (flat faces, held).

### Corrections to prior sessions' recorded conclusions
- **2026-07-28's "the bug IS in `mujoco_ros2_control` plugin / ros2_control command pathway" is WRONG.** It rested on Test F, whose measured joint4 position (-1.61542) IS the discarded-torque fingerprint (-1.61549). The evidence for the plugin theory was the bug itself. Static source reading found nothing wrong with the plugin because nothing is wrong with the plugin.
- **The `initial_positions.yaml` fix is real but was NOT the freeze fix.** It genuinely seeds MuJoCo's `qpos` (joint7's `+0.785` sign flip proves it — the arm rests at the YAML pose, see run16), so keeping it is correct hygiene. It does not cause or cure the freeze.
- **2026-07-24's `safety_margin` 2.0 -> 4.0 revert was based on a misattribution** — already retracted in `lyapunov_gains.py`'s own 2026-07-27 note. Margin 4.0 is now live-validated as good.
- **The `_transit_waypoints`, floor-box and `conaffinity="0"` mitigations were all aimed at the disproven freeze theory.** `conaffinity="0"` is retained (harmless, arguably correct); the floor box is now removed; `_transit_waypoints` is retained as generically good practice.
- **The 2026-07-27 diagnosis in `switch_to_effort.sh`'s header was RIGHT ALL ALONG** — including the numeric fingerprint — and was discarded the next day. The answer sat in the repo for two days.

### Repo state
Branch `fix/effort-mode-actuator-lock`, not merged to main. Everything from 2026-07-23/24/28/29 committed together this session (see commit message for the full list). `school_report/rapport/main.tex` §5.4 still describes the freeze with the physics/plugin framing and **still needs a prose rewrite** — deliberately left for a dedicated pass.

---

[Session continuation entry: 2026-07-28 — **CONCLUSION SUPERSEDED, SEE 2026-07-29 ABOVE.** This entry's headline finding ("the bug is in the mujoco_ros2_control plugin or the ros2_control command pathway") is incorrect; it was derived from a test that was itself measuring the discarded-torque bug. The diagnostic tools built here (`debug_mujoco_internals.py`, `test_direct_joint_bypass.py`) remain useful and are kept. Original text preserved below for the record.]

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

**Stage 4 (grasping) — WORKING END-TO-END as of 2026-07-29.** `pick()` completes successfully: cube grasped and lifted, **2/2 consecutive runs** (`test_grasp_pick_run30/31.log`), with the cube at x=0.65 m (30% farther than the original 0.50 m placement). Final grasp convergence 0.0066 / 0.0186 m against a 0.0200 m tolerance; gripper closes to 0.03999612 / 0.03990805 m against a 0.040 m target; `is_grasped=True`.

The blocking "panda_joint4/6/7 freeze" is SOLVED: **`mujoco_ros2_control`'s `ResetWorld` silently reverts every joint to its internal position PID**, bypassing `perform_command_mode_switch()` so no layer reports it, and every effort command is discarded. Fixed by `ros2_ws/force_effort_mode.sh`, now called automatically from `reset_world_home.sh`. The 2026-07-28 conclusion (plugin command pathway) was **wrong** — see the correction section in the 2026-07-29 entry. Five further bugs were fixed behind it, each only reachable once the previous was cleared: the gain-override startup crash, a leaked planning-scene attachment, the attach-before-descent floor conflict, KDL IK budget at longer reach, and two gripper-geometry errors (both traceable to `panda_hand_joint`'s `xyz="0 0 0" rpy="0 0 -0.785"`).

## Open questions / blockers
- **Milestone 1 and 2:** FULLY CLOSED (Stage 2/3, unrelated to this session's work).
- **Stage 4 (grasping) — CORE OBJECTIVE ACHIEVED 2026-07-29, `pick()` works end-to-end (2/2 runs).** Remaining items:
  - **MANDATORY OPERATING RULE:** every `reset_world_home` MUST be followed by `force_effort_mode.sh`, or all torques are silently discarded. This is now automatic inside `reset_world_home.sh` — do not bypass it by calling the reset service directly.
  - **Reliability sample is only 2 runs.** run31's final grasp came in at 0.0186 m against a 0.0200 m tolerance — a thin margin, and the worst joint shifted from joint5 to joint2. Run several more picks before treating the numbers as a characterised success rate for the report.
  - **`panda_joint5` has a systematic, one-signed steady-state bias** (~0.013-0.053 rad, always negative, at every waypoint in every run). It no longer breaks the pick but is untouched by every fix made this session. This is the one genuinely model-shaped open question. **Cleanest test: re-run with `disable_residual:=true`** (RNEA + PD only, learned network never called). If the bias vanishes, the learned residual introduces it — a real result for goal.md objective 2, not just a debugging step.
  - **`_attach_object()` attaches before the descent, which is physically wrong** and forced the floor collision box to be removed. Proper fix: attach only after the gripper closes (what MoveIt's own pick pipeline does), then restore the floor box. Also: `GraspExecutor` should detach in a `finally` so an abort cannot leak the attachment — the startup cleanup in `test_grasp_pick.py` is belt-and-braces, not a fix for the leak itself.
  - **`gain_safety_margin_override:=4.0` is passed at launch, not made the default.** Consider promoting it in `controller/lyapunov_gains.py` — but note the wrist Kd (8.4-9.5) then sits near the 12 Nm limit, and visible chatter was observed at stretched, near-singular poses. `lyapunov_gains.py`'s own note on choosing Kp from a target tracking error (rather than from Kd's stability lower bound) is the principled fix and is still unimplemented.
  - Stage 4 ROS2 orchestration node still doesn't exist — no longer blocked, a working `pick()` now exists to build on.
- **Workflow lessons (carry forward, all earned expensively):**
  - **(2026-07-29, the big one) A check that cannot fail is worse than no check.** This bug survived a week because every status layer reported healthy while torques were discarded. `switch_to_effort.sh`'s verification passed; `verify_effort_mode.sh` passed (it reads `controller_manager`, which is exactly the layer that lies); an early `force_effort_mode.sh` verification was tautological (it grepped for effort lines, then asserted the result contained effort lines) and reported OK while printing `position control enabled` directly above. **Verify against the layer that actually acts** — here, the plugin's own per-joint mode log — and make the check able to fail.
  - **(2026-07-29) Read the log of the component that failed BEFORE forming a hypothesis.** `GOAL_STATE_INVALID` and `Unable to sample any valid states for goal tree` were sitting in `move_group`'s log the whole time and named both planning failures outright; two edits (shrinking the cube box, lowering the floor box) were made against guessed causes before that log was read. Same mistake at project scale: `switch_to_effort.sh`'s header had the correct diagnosis, with numbers, two days before it was acted on.
  - **(2026-07-29) Distinguish planning failure from tracking failure before blaming the model.** `planning failed, error_code=99999` means MoveIt rejected the goal and NO torque was ever computed. Timing separates the sub-cases: ~1.8 ms = goal in collision; ~5 s = IK sampler exhausted; full 10 s timeout with `still converging` = a genuine tracking problem. Only the last one implicates Stage 1/3.
  - **(2026-07-29) State leaks between runs.** Restarting the test script clears nothing: the planning scene lives in `move_group` and the control mode lives in the plugin. "Clean" re-runs were not clean.
  - **(2026-07-28, still valid) Standalone scripts that bypass a layer are powerful** for isolating where a bug lives — but they must hold every other variable constant, or they mislead (`debug_mujoco_internals.py` compared two different control paths AND two different arm configurations at once).
  - **(carry forward) Long pasted commands get corrupted by terminal line-wrapping.** It happened again on 2026-07-29 and silently dropped `checkpoint_path`, invalidating run18 — the exact failure `launch_pinn_controller_boosted.sh` had already been written to prevent. Use the scripts; do not paste multi-argument `ros2 launch` lines.
- **Environment fix (carry forward):** Always ensure `ros-jazzy-ros2controlcli` is installed.
- **Working tree:** all of 2026-07-23/24/28/29 committed on `fix/effort-mode-actuator-lock` (NOT merged to main, not pushed). `school_report/rapport/main.tex` §5.4 still carries the old physics/plugin framing and needs a prose rewrite.

## What to do next session
**Startup sequence that works (use exactly this order):**
1. **Terminal 1:** `bash ros2_ws/rebuild_and_relaunch_sim.sh` — kills stale processes, verifies they are gone, rebuilds, and only then launches. Wait for `OK: build succeeded` and the sim to come up.
2. **Terminal 2:** `bash ros2_ws/launch_pinn_controller_boosted.sh 4.0` — confirm it prints `gain_safety_margin_override=4.00 active` and NOT `No checkpoint_path set`.
3. **Terminal 3:** `bash ros2_ws/switch_to_effort.sh` — must exit 0. (On a FRESH sim this is the right call; after any reset use `reset_world_home.sh`, which re-asserts effort mode itself.)
4. **Terminal 3:** run the pick, teeing to a log:
   `source /opt/ros/jazzy/setup.bash && source ~/projects/pinn_franka/ros2_ws/install/setup.bash && source ~/projects/pinn_franka/ros2_ws/set_pinn_env.sh && python3 ~/projects/pinn_franka/stage4/test_grasp_pick.py 2>&1 | tee stage4/test_grasp_pick_runNN.log`
5. Between picks: `bash ros2_ws/reset_world_home.sh` (re-asserts effort mode automatically), then re-run step 4.

**Suggested priorities:**
1. **VALIDATE ACROSS CONFIGURATIONS BEFORE CLAIMING `pick()` WORKS.** 2026-07-29's result is **2/2 at exactly one pose** (cube at x=0.65, y=0, on the floor at z=0.02, axis-aligned, 64 g). That is a working demo, NOT a validated capability, and it must not be written up as one. Several things fixed on 2026-07-29 were tuned against that single pose and may not generalise — the flange-to-fingertip offset, the 45 deg finger alignment, the KDL IK budget, and `gain_safety_margin_override:=4.0`. Test matrix to run before the report claims Stage 4 works:
   - **Distance (x):** 0.45 / 0.55 / 0.65 / 0.70 m. 0.65 already sits near the IK envelope (see the `config/kinematics.yaml` note); expect 0.70 to need a relaxed grasp orientation rather than more solver time. Also check SHORT reach — a folded-in arm is a different singularity, never tested.
   - **Lateral offset (y):** -0.25 / 0 / +0.25 m. Everything so far has been at y=0, exactly on the robot's x-axis, which is the WORST case for KDL but the BEST case for symmetry. Off-axis grasps exercise joint1 and the wrist differently and may expose the `panda_joint5` bias more (or less).
   - **Height / support surface:** put the cube on a **table** instead of the floor. This is the important one and it is not just a z-offset:
       * A table must be added to BOTH the MJCF (as a real body, so physics is right) and the MoveIt2 planning scene (as a collision object) — the two must agree, exactly like the 5 cube-position sites do.
       * It re-opens the **attach-before-descent flaw** (item 3 below), and this time there is no workaround: with the cube at table height the phantom attached object descends into the TABLE, and unlike the floor box the table cannot simply be deleted from the planning scene. **Fix the attach ordering FIRST, then add the table.**
       * It changes the arm's configuration substantially (higher, less extended), so re-check the joint5 bias and the wrist chatter there.
   - **Object orientation:** rotate the cube about z by 15/30/45 deg. The 45 deg finger alignment fix assumes an axis-aligned cube; a rotated one needs the grasp yaw derived from the object's pose, not hardcoded. Currently it is hardcoded.
   - **Object size / mass:** vary the cube. **This is the one that exercises the project's actual scientific contribution** — Stage 1's residual is payload-conditioned (`delta`, trained at 0/1/3 kg) and `ComputedTorquePDController.update_payload(delta)` exists but has NEVER been exercised in a real grasp. Picking a heavier object and updating `delta` on grasp is a direct test of goal.md's payload-conditioning novelty, not just a robustness check. Highest scientific value of anything in this list.
   - **Record success rate and the spread of the final grasp error per configuration.** run31 cleared its 0.0200 m tolerance by only 1.4 mm, so the margin is thin and probably configuration-dependent. The report needs a table of real numbers, not an anecdote.
2. **Settle the joint5 bias — the one open question that could touch Stage 1.** Re-run with `disable_residual:=true` and compare joint5's steady-state error against the current ~0.013-0.053 rad. If it vanishes, the learned residual is introducing a systematic torque bias on that joint; if it persists, it is the PD/gravity structure, not the model. Either answer belongs in the report (goal.md objective 2).
3. **Fix the attach ordering properly.** Attach after the gripper closes, not before the descent; add a `finally` detach in `GraspExecutor`; then restore the floor collision box in `test_grasp_pick.py`.
4. **Rewrite `school_report/rapport/main.tex` §5.4.** It still describes the freeze with the physics/plugin framing. The true story is stronger: a control-mode configuration fault that perfectly mimicked a physics fault, invisible to every status layer, plus a quantified limitation of Liu et al.'s Proposition 1 (Kp derived from a stability lower bound gives `e_ss = 4/(m^2 * eps)`, so better-modelled joints track WORSE — already derived in `controller/lyapunov_gains.py`'s own comment, and confirmed live this session).
5. **Then Stage 4 orchestration node** — no longer blocked.

**Diagnostic tools available:**
- `ros2_ws/force_effort_mode.sh` — recover effort mode after any reset. Verifies against the plugin's own log.
- `ros2_ws/rebuild_and_relaunch_sim.sh` — one-command kill/verify/build/launch cycle.
- `ros2_ws/verify_effort_mode.sh` — pre/post-test gate. **Caveat: it reads `controller_manager`, which is exactly the layer that lies about the reset revert.** Trust `force_effort_mode.sh`'s plugin-log check over this one.
- `stage4/debug_mujoco_internals.py` — physics-vs-stack isolation via the raw `mujoco` package (`--settle N` runs zero-torque free-fall first). Hold all other variables constant when using it.
- `ros2_ws/test_joint{4,6,7}_raw_torque.sh` — single-joint isolation. **Only meaningful if effort mode is verified at the plugin log first.**
- `stage4/test_direct_joint_bypass.py` — deterministic joint-space targets, no MoveIt2 variability.

**Do NOT re-open:** physics/MJCF model audit, plugin indexing, MoveIt2/OMPL IK variability as the freeze cause, or the trained model as the freeze cause. All are ruled out — the freeze was `ResetWorld`'s silent position-PID revert, fixed and verified.
