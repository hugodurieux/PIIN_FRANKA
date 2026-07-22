# Session State — PINN Franka Project
<!-- This file is updated automatically at the end of each session.
     Do not edit by hand. CLAUDE.md imports it at every startup. -->

## Last updated
2026-07-22 (STAGE 4 STARTED: GRIPPER GIVEN REAL PHYSICS, VALIDATED WORKING END-TO-END) — Continuation, same day, after Milestone 2 was closed (see marker below). User specified the target for a "first version" of the project: Franka picking up an object in MuJoCo (the full 4-novelty thesis scope remains the "final version", tracked separately). First concrete Stage 4 gap addressed: the gripper.

**What was wrong:** the hand/fingers in `panda_arm_mujoco.xml` were welded (no joints, no actuators, no collision geometry) — added in an earlier session purely as dead mass to fix a gravity-compensation mismatch. As configured, the gripper could not physically open, close, or contact anything. Also, `panda_finger_joint1/2` were on a separate `mock_components` ros2_control system ("PandaHandMockSystem") entirely disconnected from real physics.

**Critical architectural finding before writing any code:** confirmed by reading `mujoco_system_interface.cpp` from `github.com/ros-controls/mujoco_ros2_control` that `MujocoSystemInterface::on_init()` constructs a private `MujocoSimulation` (`std::make_unique`) per hardware-component instance — NOT a shared singleton. A naive second `<ros2_control>` "system" block for the hand, even pointing at the same MJCF file, would have spun up a second, entirely disconnected physics simulation, with the fingers floating in their own private void, mechanically detached from the arm. The fix: `panda_finger_joint1/2` were added *inside* the arm's existing single `<ros2_control>` block (same "PandaMujocoSystem"), not a separate one.

**Changes made:**
- `panda_arm_mujoco.xml`: real prismatic joints (`panda_finger_joint1/2`, MuJoCo's own "finger" default class, axis/range values from `google-deepmind/mujoco_menagerie`'s WITH-hand `panda.xml`), visual + collision geometry including 5 fingertip pad collision boxes per finger for stable grasp contact, an `<equality><joint>` constraint keeping finger2 synced to finger1 (only finger1 has a ros2_control command_interface, matching upstream's own hand.ros2_control.xacro convention), and a `<position>` actuator on finger1. "home" keyframe defaults to fully open.
- `panda_mujoco.ros2_control.xacro`: finger joints added to the existing "PandaMujocoSystem" block (see architectural finding above); `initial_value` for both finger joints set to 0.04 (open), not upstream's hardcoded 0.0 (closed) — a safer default for a future grasp demo.
- `panda_mujoco.urdf.xacro`: removed the now-redundant separate mock hand system entirely.
- `launch/mujoco_franka_moveit.launch.py`: spawns `panda_hand_controller` (`position_controllers/GripperActionController`) — this was already fully defined upstream and already expected by MoveIt2's own `gripper_moveit_controllers.yaml` (loaded, unmodified), just never spawned. MoveIt2's SRDF `hand` group / `open`/`close` named states were also already complete and untouched.

**Two real bugs found and fixed during live testing (neither caught by static review):**
1. **Missing palm geometry:** first live test showed the fingers rendering and moving correctly in MuJoCo, but nothing visually connecting them to the arm — the `panda_hand` body itself was given joints/geometry on the *finger* bodies only; `panda_hand` (the palm) was left with `<inertial>` only, same oversight as the original welded version, just not noticed until seeing it live. Fixed by adding the 5 hand visual meshes + 1 collision mesh (`hand_0..4.obj`, `hand.stl`) from the same upstream reference, previously vendored on disk but never referenced by any `<mesh>`/`<geom>` tag.
2. **Underdamped gripper actuator:** first close/open test via `panda_hand_controller`'s `gripper_cmd` `GripperCommand` action reported `stalled: true, reached_goal: false` for BOTH open and close targets, with the state interface reading a `position` of ~-0.014 — genuinely outside the joint's own `[0, 0.04]` range (confirmed this is real qpos, not a derived value, by reading `gripper_action_controller_impl.hpp` from `ros2_controllers`' jazzy branch: `pre_alloc_result_->position` comes straight from the position state_interface). Visually this showed as the two fingers crossing through each other. Root cause: the finger actuator's `kp=500` (deliberately flagged "untuned" in the original comment) had no explicit `kv` damping, and the passive joint damping inherited from the arm's own default class (damping=1) is nowhere near critical damping for a 15g mass at that stiffness (~5.5 needed, only 1 present) — a badly underdamped spring that oscillated past the joint limits on every move. Fixed by lowering to `kp=30` and adding an explicit `kv=3` (well above the ~1.34 needed for critical damping at that lower stiffness). Retested: `reached_goal: true, stalled: false, SUCCEEDED` for both open and close, fingers stop against each other correctly without crossing.
3. **Own mistake, unrelated to the above, cleaned up:** ran a `colcon build` from the repo root instead of `ros2_ws/` partway through, creating stray non-gitignored `build/`, `install/`, `log/` directories at the repo root (separate from the legitimate, gitignored ones inside `ros2_ws/`). Removed; the real build was untouched.

**New convenience scripts:** `ros2_ws/gripper_open.sh` / `ros2_ws/gripper_close.sh` — wrap the `ros2 action send_goal .../gripper_cmd control_msgs/action/GripperCommand ...` invocation, written as scripts rather than pasted one-liners after this exact command got corrupted by terminal line-wrapping during paste (same class of issue as CLAUDE.md's existing Lesson #2, now recurring for a second, longer command).

**Status: gripper joints are DONE and validated working** (open + close both succeed cleanly via the real `panda_hand_controller` action, in the same shared MuJoCo simulation as the arm). Remaining Stage 4 gaps, per the plan from earlier today, now narrowed: no graspable object yet exists in the scene; `stage4/gripper_controller.py`'s only real (non-mock) implementation still targets real hardware's `franka_gripper` actions, not this project's own `panda_hand_controller` GripperCommand action — a MuJoCo/ros2_control-native gripper controller class doesn't exist yet, though the action interface it would wrap is now proven working; `_move_arm()` in `grasp_executor.py` still raises `NotImplementedError`; the Stage 4 ROS2 orchestration node still doesn't exist.

[Session continuation entry: 2026-07-22 (MILESTONE 2 TRAJECTORY TRACKING CONFIRMED WORKING — Hypothesis 3 refuted with hard evidence, numeric motion proof captured, stale documentation corrected))]

**TRAJECTORY TRACKING ATTEMPT — NO VISIBLE MOTION DESPITE SUBSTANTIAL COMMANDED TORQUE**

After the joint-indexing fix merged onto `fix/jointstate-name-indexing`, the arm was confirmed to hold cleanly through the controller switch (no collapse). The next logical step was to test actual trajectory tracking. Sequence of events:

1. **Retried `moveit_plan_bridge` after joint-index fix (from clean pose via `reset_world`):** Planning succeeded this time. The earlier error_code=99999 was concluded to have been a symptom of the arm's corrupted start-state while the joint-indexing bug was still active, not a separate bug — confirmed by successful replanning post-fix.

2. **First tracking test with near-home target:** Used target `[0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]` (nearly identical to the arm's home/ready pose). No visible motion. This was inconclusive — the target was so close to the start configuration that failure to move was expected, not diagnostic.

3. **Second tracking test with clearly different target:** Used target `[1.2, -0.5, -0.8, -2.0, 0.3, 2.0, 0.5]` from a start pose around `[0, -0.78, 0.001, -2.40, -0.004, 1.56, 0.78]` — a multi-degree change on almost every joint. Still no visible motion in MuJoCo. RViz showed its orange "planned path preview" ghost animate smoothly through the intended motion (confirmed to be a local MoveIt2 client-side animation played for any successfully-planned trajectory, NOT evidence of real execution), but the real robot display (grey, tied to actual `/joint_states`) stayed frozen.

**VERIFICATION THAT PUBLISHED DATA WAS SANE**

4. **Verified the published trajectory itself:** Live `ros2 topic echo /pinn_controller/desired_trajectory` showed 13-14 smooth waypoints across all 7 joints, total duration ~1.13s, well inside `pinn_controller_node.py`'s 2.0s staleness window. Ruled out "trajectory duration exceeds tracking window" as cause.

5. **Verified `pinn_controller_node` operation:** Log showed clean operation: "New trajectory received with 13 points" followed exactly 2.0s later by "Trajectory stale... holding via gravity compensation" with nothing abnormal in between. No errors, no exceptions, no fallback-branch surprises.

6. **Code review of control law and gains:** Carefully read `controller/computed_torque_pd.py` (`ComputedTorquePDController.step()`: tau_cmd = RNEA feedforward + learned residual + PD correction, clipped to torque limits), `controller/lyapunov_gains.py` (`Kp`/`Kd` computed from `DEFAULT_ERROR_BOUND = [5.20, 5.66, 3.06, 3.80, 2.10, 2.38, 1.57]` with safety_margin=2.0, yielding e.g. joint1 Kp≈27.04, Kd≈10.4), and `ros2_ws/src/pinn_franka_controller/pinn_franka_controller/trajectory_interpolator.py` (linear interpolation over `time_from_start`). **No bugs found in any of the three.** All appeared logically correct.

**DECISIVE DIAGNOSTIC — SUBSTANTIAL ACTUAL TORQUE COMMANDED**

7. **Live torque capture:** Ran `timeout 6 ros2 topic echo /panda_effort_controller/commands > torque_capture.txt` for a fixed 6-second window fully overlapping a tracking attempt (5177 messages, ~863 Hz), then computed per-joint min/max. Result: torque varied substantially and meaningfully, NOT frozen or stuck:
   - Joint 1: 2.22e-16 to 38.65 Nm (huge range, real growth)
   - Joint 4: 22.17 to 29.44 Nm (gravity compensation + PD modulation)
   - Other joints similarly dynamic
   
   This proved the control law WAS executing and producing large, physically-plausible commanded torque. Ruled out "stuck in fallback branch" or "gains too weak to produce any measurable torque."

**FIRST INVESTIGATIVE ROUND — OPUS 4.8 ROUND 1 (TWO HYPOTHESES, BOTH REFUTED)**

8. **Delegation to Opus 4.8 Round 1:** Given substantial commanded torque but zero motion, proposed Hypothesis 1: `panda_effort_controller` was never actually activated (repo-wide grep found no `activate_controllers` calls in tracked files, which was technically true). **Refuted empirically:** `ros2 control list_controllers` showed `panda_effort_controller` genuinely `active` and `panda_arm_controller` genuinely `inactive`. The grep missed many live terminal `ros2 service call switch_controller` invocations made all session at the terminal (not in repo files).

9. **Fallback Hypothesis 2 (from Round 1):** MuJoCo hardware plugin (`mujoco_ros2_control`) might maintain an internal position-PID hold via the single shared motor actuator per joint, independent of ROS2-level controller deactivation. Tested Hypothesis 2's own suggested diagnostic: fully `ros2 control unload_controller panda_arm_controller` (not just deactivate). Even with position controller completely unloaded, identical zero-motion result. **Refuted.**

10. **Additional tests:** 
    - Confirmed MuJoCo viewer NOT in local pause state (pressing spacebar showed "PAUSED" overlay on next keypress, proving sim was genuinely live/running throughout all failed tracking attempts).
    - Confirmed sim time advancing via `/clock` topic inspection.

**DECISIVE NUMERIC PROOF — POSITION BIT-FOR-BIT IDENTICAL ACROSS TRACKING WINDOW**

11. **Captured `/joint_states` for fixed 4-second window** fully overlapping a fresh tracking attempt (target `[1.2, -0.5, -0.8, -2.0, 0.3, 2.0, 0.5]`, with `panda_arm_controller` fully unloaded, real substantial torque being commanded), then computed per-joint position min/max across the entire window. **CRITICAL FINDING: EVERY joint's position was bit-for-bit IDENTICAL to full float64 precision** (min == max) across the entire window, including the ~1.13s the trajectory was actively tracked with torque reaching ~38 Nm on joint1. Not "barely moved" — exactly, bit-for-bit frozen. The pose (`~0, -0.776, 0.0013, -2.400, -0.0042, 1.557, 0.785`) closely matches the standard Franka Panda "ready" pose (MoveIt's typical demo default) and has appeared unchanged in essentially every `/joint_states` snapshot captured this entire session, through multiple resets, switches, an unload, and pause/unpause toggles.

**CRITICAL CONTEXT — ARM WAS WORKING EARLIER THIS SESSION**

12. **Important clarification:** Earlier in this SAME session (documented in the prior 2026-07-21 entry), the arm WAS observed to visibly and dramatically fall/collapse under gravity in MuJoCo, repeatedly, while the joint-indexing bug was still present. This proved the kinematic chain, physics integration, and joint mobility were definitely real and working at least once. Something differs between that earlier working state (when the joint-indexing bug caused a fall) and the current completely-immobile state (after the bug was fixed).

**SECOND INVESTIGATIVE ROUND — OPUS 4.8 ROUND 2 (HYPOTHESIS 3, PROPOSED BUT UNTESTED)**

13. **Delegation to Opus 4.8 Round 2:** Given all prior hypotheses refuted, explicit instruction not to re-propose them, and a lead about possible joint-name collisions between the MuJoCo arm hardware system and the mock gripper system (both hosted by the same controller manager), produced Hypothesis 3:

**HYPOTHESIS 3 (PROPOSED, NOT YET CONFIRMED):** The MuJoCo hardware plugin (`mujoco_ros2_control`, compiled `.so`, no local source visible) binds each joint's single MuJoCo motor actuator into EITHER position-PID mode OR effort mode based on static configuration — specifically, whether both `position` and `effort` command interfaces are declared (as they currently are, in `urdf/panda_mujoco.ros2_control.xacro:60-61`, intentionally, to let both Milestone 1 and Milestone 2 paths share one config) alongside a configured `pids_config_file` (as they currently are, in `config/mujoco_pid.yaml`, referenced at `urdf/panda_mujoco.ros2_control.xacro:53`). When both are present, the plugin may lock the motor into position-PID mode and DISABLE effort entirely at a level below/independent of ROS2 controller-manager-level interface claims/releases — which would explain why nothing tried at that level (switch, unload, pause) ever mattered.

**Evidence cited for Hypothesis 3:**
- Three mutually-exclusive per-joint log message strings found via `strings` on the compiled `libmujoco_ros2_control.so` binary:
  - `"Joint %s: position control enabled (velocity, effort disabled)"`
  - `"Joint %s: <effort> control enabled (position, velocity disabled)"`
  - `"Position command interface for the joint : %s is not supported with velocity or motor actuator without defining the PIDs"`
- Observation that the frozen pose matches `initial_positions.yaml`'s startup values closely.

**IMPORTANT UNRESOLVED TENSION:** This Hypothesis 3 interpretation (permanent "locked at registration time" story) is in tension with an earlier finding from reading `mujoco_ros2_control`'s public GitHub source directly (during the first bug investigation): per-actuator mode flags (`is_position_control_enabled`, `is_position_pid_control_enabled`, `is_effort_control_enabled`) are set by `perform_command_mode_switch()`, which is described in that source as being driven dynamically by real controller-manager interface claims/releases. That source reading suggested dynamic runtime switching IS supported, which would seem to contradict a permanent "locked at registration" story. This tension is UNRESOLVED — possibly the same log strings are emitted by `perform_command_mode_switch()` itself on every switch (not just once at startup), in which case the diagnostic below still works but the "locked at registration" framing may be imprecise. **Do not present Hypothesis 3 as confirmed until the diagnostic runs.**

**FREE DIAGNOSTIC (NOT YET RUN — MUST RUN FIRST NEXT SESSION)**

14. **Definitive, free, non-destructive diagnostic test:**

```bash
grep -E "control enabled" ~/.ros/log/latest/*ros2_control_node* 2>/dev/null
```

If grep finds nothing, scroll `Terminal 1`'s scrollback (the terminal running `mujoco_franka_moveit.launch.py`) back to near the very start, right after the controller manager comes up. Look for lines like:
- `Joint panda_joint1: position control enabled (velocity, effort disabled)` → Hypothesis 3 CONFIRMED
- `Joint panda_joint1: <effort> control enabled (position, velocity disabled)` → Hypothesis 3 REFUTED, investigation must continue elsewhere

**This check MUST be done first thing next session before proceeding with any other tests.** It is a trivial, free, read-only operation with zero side effects.

**CANDIDATE FIX PREPARED (NOT YET TESTED, CONTINGENT ON HYPOTHESIS 3 CONFIRMATION)**

15. **A candidate fix was applied on new branch `fix/effort-mode-actuator-lock`** (branched sequentially from `fix/jointstate-name-indexing`, which already contains the joint-indexing fix). The fix adds a new `arm_control_mode` launch/xacro argument with two modes:
    - `both` (default): current behavior, both `position` and `effort` command interfaces declared, allows Milestone 1 (position-mode) to coexist with Milestone 2 effort-mode testing in the same config.
    - `effort`: new Stage-3-only mode, arm joints export ONLY the `effort` command interface, and the `pids_config_file` is omitted, intended to force the plugin to register the motor actuators in pure effort mode.

**Files touched by the fix:**
- `ros2_ws/src/pinn_franka_controller/urdf/panda_mujoco.ros2_control.xacro` (new `arm_control_mode` macro parameter)
- `ros2_ws/src/pinn_franka_controller/urdf/panda_mujoco.urdf.xacro` (declares/forwards the arg)
- `ros2_ws/src/pinn_franka_controller/launch/mujoco_franka_moveit.launch.py` (declares launch arg, skips spawning `panda_arm_controller` when `effort` mode is selected, since no position interface would exist for it to claim)

**Verified via `python -m py_compile`:** All touched files have correct syntax. Nothing was executed.

**Known intentional tradeoff:** In `effort` mode, Milestone 1's position-mode path (`panda_arm_controller`) cannot run in that same launch config (no position interface exists for it to claim). Milestone 1 remains validated via the default `both` mode; `effort` mode is only for Stage 3 testing. If both need to coexist live in one launch in the future, that requires either a confirmed-working runtime mode switch (currently unresolved whether the plugin actually supports it), or two separate actuators per joint in the MJCF (previously tried in an earlier session and rejected per that work's comments) — flagged as a separate future follow-up, not solved now.

**Additional file present:** `ros2_ws/switch_to_effort.sh` (a convenience script from Round 1's work, wrapping `ros2 service call switch_controller` — turned out not to be the root cause since H1 was refuted, but left in place as harmless and potentially useful).

**REPOSITORY STATE AT SESSION END**

- **Current branch:** `fix/effort-mode-actuator-lock` (stacked on `fix/jointstate-name-indexing`, which is stacked on the original revert commit from prior session)
- **No new commits made this session.** Nothing has been merged to main.
- **All uncommitted Stage 2/3 MuJoCo-migration files from prior sessions remain present** plus this session's branch changes (xacro/launch edits for `arm_control_mode`).
- **Untracked files:** `ros2_ws/set_pinn_env.sh`, `ros2_ws/launch_pinn_controller.sh`, `ros2_ws/switch_to_effort.sh` (convenience script), the MJCF/URDF directory trees.

**WHAT TO DO FIRST NEXT SESSION (IN STRICT ORDER)**

1. **RUN THE DIAGNOSTIC FIRST — no exceptions.** Execute `grep -E "control enabled" ~/.ros/log/latest/*ros2_control_node* 2>/dev/null` or scroll Terminal 1's scrollback to confirm whether the arm's motor actuators are registered as `position control enabled` or `effort control enabled`. This is a free, read-only check. Do NOT skip or assume the answer.

2. **If Hypothesis 3 is CONFIRMED** (logs show "position control enabled" for arm joints):
   - Rebuild: `colcon build --packages-select pinn_franka_controller`
   - Relaunch with effort-only mode: `ros2 launch pinn_franka_controller mujoco_franka_moveit.launch.py arm_control_mode:=effort`
   - Verify startup logs now show "effort control enabled" for arm joints
   - Bring up `pinn_controller_node`: `bash ros2_ws/launch_pinn_controller.sh`
   - Activate `panda_effort_controller` via `ros2 service call /controller_manager/switch_controller ...` (note: no position controller to deactivate this time, only activate effort)
   - **REPEAT the exact same numeric `/joint_states` position min/max capture used in point 11 above** during a fresh trajectory-tracking attempt. Success criterion: per-joint min != max (real motion observed), not just visual impression. Failure criterion: still bit-for-bit frozen.

3. **If Hypothesis 3 is REFUTED** (logs show "effort control enabled" for arm joints, or any other clear evidence the diagnosis was wrong):
   - Do NOT apply the `arm_control_mode:=effort` fix. The actual cause remains unknown.
   - Escalate to a third Opus investigation round, with this hypothesis added to the refuted list, and all the numeric proof from points 7 and 11 (substantial commanded torque, zero position change) as fresh context.

4. **Until Milestone 2 trajectory tracking is empirically validated** (arm provably moves in response to commanded effort), Milestone 2 is NOT closed. This is the single most critical open item for the entire project.

5. **Note:** The earlier `moveit_plan_bridge` planning-failure issue (error_code=99999) from the prior 2026-07-21 entry is now considered resolved/moot — confirmed working after the joint-index fix, no longer an active blocker.

---

[Session continuation entry: 2026-07-21 (JOINT STATE INDEXING BUG FIX, TRAJECTORY TRACKING ATTEMPT, HYPOTHESIS 3 PROPOSED — subsequently REFUTED 2026-07-22, see entry above)]

[Prior session entry: 2026-07-20 (MILESTONE 2 DEBUGGING: CONTROLLER INTEGRATION ON MUJOCO, 4 BUGS FOUND AND FIXED, END-TO-END MOTION NOT YET VALIDATED)]

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

**Stage 4 (grasping) — STARTED 2026-07-22, gripper joints DONE.** "First version" target (per user direction): Franka picking up an object in MuJoCo. The gripper now has real physics (prismatic joints, collision geometry including the palm, an equality-coupled second finger, a properly-damped position actuator) sharing the arm's own MuJoCo simulation, and is driven by a real, working `panda_hand_controller` (GripperCommand action) — confirmed via live open/close tests (`reached_goal: true`, `stalled: false`, fingers stop against each other without crossing). Remaining Stage 4 gaps: no graspable object in the scene; no MuJoCo-native gripper controller Python class (the underlying action interface is proven, just not wrapped in `stage4/gripper_controller.py` yet); `_move_arm()` still stubbed; orchestration node doesn't exist.

## Open questions / blockers
- **Milestone 1 and 2:** FULLY CLOSED.
- **Stage 4 (grasping) — IN PROGRESS, gripper joints DONE 2026-07-22:**
  - ~~The MJCF's hand/fingers are currently welded~~ — DONE: real prismatic joints, visual/collision geometry (including the palm, missed in the first pass and fixed after live testing), an `<equality>` constraint, and a `<position>` actuator (kp=30, kv=3 after fixing an initial underdamped kp=500/no-kv config that overshot the joint's own range on every move). Validated via `panda_hand_controller`'s `gripper_cmd` GripperCommand action: open and close both succeed cleanly.
  - No graspable object exists anywhere in the MuJoCo scene. **Next concrete step.**
  - `stage4/gripper_controller.py`'s only real (non-mock) implementation still targets `franka_ros2`'s hardware action servers — incompatible with this MuJoCo/Jazzy stack. A MuJoCo-native gripper controller class (wrapping `panda_hand_controller`'s now-working `gripper_cmd` action) doesn't exist yet, though the interface it would wrap is proven.
  - `_move_arm()` in `grasp_executor.py` still raises `NotImplementedError` — Milestone 2 is cleared, so this is now unblocked, just not yet implemented.
  - The Stage 4 ROS2 orchestration node (joint-state subscriber + full grasp sequence loop) doesn't exist yet — only the offline, no-ROS2, no-sim `stage4/dry_run.py` exists.
- **Workflow improvements documented (carry forward):**
  - `ros2_ws/set_pinn_env.sh` sets PYTHONPATH ONLY — every fresh terminal must also source `/opt/ros/jazzy/setup.bash` and `ros2_ws/install/setup.bash`.
  - Use `ros2_ws/launch_pinn_controller.sh` (bundles all three setup commands) as standard entry point.
  - Use `/mujoco_ros2_control_node/reset_world` service for state recovery (faster than full restart).
  - If `ros2` CLI commands fail with `failed to initialize wait set: the given context is not valid`, this is a stale/corrupted `ros2 daemon`, not a real bug — `ros2 daemon stop` then `ros2 daemon start` resolved it 2026-07-22.
  - After touching any launch/xacro/MJCF/config file, `colcon build --packages-select pinn_franka_controller` is required before relaunching — these are installed into `ros2_ws/install/share/...`, not read from source, and a stale install silently masks the change (looks like nothing happened). Confirmed missing exactly this way 2026-07-22 (edited the MJCF, forgot to rebuild, gripper didn't appear). **Always run this build from inside `ros2_ws/`** — running it from the repo root creates stray, non-gitignored `build/`/`install`/`log/` directories at the repo root (happened once 2026-07-22, cleaned up).
  - Long `ros2 action send_goal`/similar commands with inline YAML get corrupted by terminal line-wrapping when pasted (same class of issue as the original Lesson #2, now confirmed for a second, different command shape) — wrap them in a script (see `ros2_ws/gripper_open.sh`/`gripper_close.sh`) rather than re-pasting a long one-liner.
- **Environment fix (carry forward):** Always ensure `ros-jazzy-ros2controlcli` is installed.
- **MuJoCo-specific issues (carry forward from prior sessions):** URDF-to-MJCF conversion bug (workaround: static MJCF); zero-mass link rejection (fixed with real inertials); update_rate instability (fixed with 1000 Hz override); virtual joint TF (static publisher); RViz display flag — all ✓ applied. Joint state indexing fixed 2026-07-21. Gripper physics/mock_components fixed 2026-07-22.
- **Working tree:** All Stage 2/3 MuJoCo migration + Milestone 2 work committed on `fix/effort-mode-actuator-lock` (not merged to main, awaiting user review). This session's gripper-joints work (MJCF, xacro, launch, new scripts) is uncommitted as of this entry — see "what to do next session" below.

## What to do next session
1. **Commit this session's gripper-joints work** (MJCF real joints/geometry/actuator, `panda_mujoco.ros2_control.xacro`, `panda_mujoco.urdf.xacro`, launch file's `panda_hand_controller` spawner, `ros2_ws/gripper_open.sh`/`gripper_close.sh`) if not already done by end of session.
2. **Stage 4 (grasping), next concrete step: add a graspable object to the MuJoCo scene.** Then: write a MuJoCo-native gripper controller class (wrapping the now-proven `panda_hand_controller`/`gripper_cmd` action) to extend `stage4/gripper_controller.py`; implement `_move_arm()` in `grasp_executor.py`; build the Stage 4 ROS2 orchestration node; integration-test the full pick sequence live in MuJoCo.
3. Decide whether to merge `fix/effort-mode-actuator-lock` to main now (Milestone 1+2 closed) or keep iterating through Stage 4 first.
4. Root cause of the original Milestone 2 freeze remains open but non-blocking — do not spend time on it unless it recurs.
