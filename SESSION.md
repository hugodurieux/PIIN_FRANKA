# Session State — PINN Franka Project
<!-- This file is updated automatically at the end of each session.
     Do not edit by hand. CLAUDE.md imports it at every startup. -->

## Last updated
2026-07-22 (MILESTONE 2 TRAJECTORY TRACKING CONFIRMED WORKING — Hypothesis 3 refuted with hard evidence, numeric motion proof captured, stale documentation corrected) — Continuation after the 2026-07-21 investigation (see marker below). Ran the diagnostic that 2026-07-21 flagged as the mandatory first step before trusting Hypothesis 3: grepped `~/.ros/log/ros2_control_node_16425_1784610107352.log` (the exact session where the frozen-arm bug was captured) for "control enabled" strings. **Result: Hypothesis 3 is REFUTED.** The log shows a single, clean position→effort mode switch at the correct time, with every joint remaining in `effort control enabled (position, velocity disabled)` continuously from that point through a `reset_world` call, a full `unload` of `panda_arm_controller`, and the entire subsequent tracking-test window, all the way to shutdown — no second switch back to position mode anywhere. This directly contradicts confidently-worded comments already written into `panda_mujoco.ros2_control.xacro` and `mujoco_franka_moveit.launch.py` on this branch, which asserted H3 as an already-confirmed fact *before* the diagnostic had actually been run — **now corrected in both files** (see "Files fixed this session" below). Independently double-checked by pulling `mujoco_system_interface.cpp` directly from `github.com/ros-controls/mujoco_ros2_control`: `perform_command_mode_switch()` and `write()` both implement correct, dynamic, per-cycle mode switching, with no "lock at registration" mechanism anywhere in the source. A new Hypothesis 4 (MuJoCo's built-in silent auto-reset-on-divergence, which can reset `mjData` to the initial keyframe without pausing `sim_->run` or logging anything through RCLCPP) was proposed as a better-supported candidate explanation but was **never confirmed or refuted** — per explicit user direction ("check first, then if it does not work we dig further"), a clean relaunch was attempted next instead of chasing H4 further, using the default `arm_control_mode:=both` with NO candidate fix applied, and **it worked**.

**DECISIVE SUCCESS — arm provably moves under Stage 3 effort control, numerically confirmed:** Two `/joint_states` captures were taken this session.
- First capture (re-sending the same already-reached target `[1.2, -0.5, -0.8, -2.0, 0.3, 2.0, 0.5]`) showed the arm sitting within ~1e-9 to 1e-8 rad of that target for the entire 6s window — real PD-holding jitter, qualitatively different from the old bug's exact bit-for-bit freeze, but inconclusive alone since no transition occurred inside that window (the arm had already arrived before the capture started).
- Second capture, properly bracketing a fresh move back toward `[0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]` starting from the position above, is decisive: every joint moved substantially and consistently toward the new target within the 8s window (joint1 1.186→0.050 rad, joint2 -0.553→-0.801 rad, joint3 -0.742→-0.036 rad, joint4 -1.970→-2.314 rad, joint5 0.226→-0.005 rad, joint6 1.913→1.558 rad, joint7 0.506→0.713 rad — all converging toward the commanded target, not stuck). **This is the first time in this project's history that Stage 3 effort-mode trajectory tracking has been empirically proven to move the arm.** Milestone 2 is now considered CLOSED.

**Root cause of the original freeze is deliberately left not fully understood.** H3 is conclusively refuted; H4 was never tested since the clean relaunch simply worked on the first retry. If the freeze recurs in a future session, H4 (silent MuJoCo divergence-reset) and the untested `arm_control_mode:=effort` candidate fix (still present on this branch, comments now accurate, default behavior `both` unchanged) are the next things to check — see the corrected comment block in `panda_mujoco.ros2_control.xacro` for the full technical account of what was checked and why H3 fell.

**Two minor items observed during validation, both understood as expected behavior, not bugs:**
- After switching to effort mode, RViz's "Plan & Execute" stopped working — expected: it executes via `panda_arm_controller`, which is deliberately deactivated while `panda_effort_controller` is active (the same controller-exclusivity tradeoff already documented for this branch). To restore Plan & Execute, switch back (deactivate effort, reactivate arm controller).
- The arm moved in MuJoCo/RViz's real robot display, but RViz's separate orange "planned path preview" ghost did not animate this time — consistent with this being genuine execution (the real, `/joint_states`-driven robot) rather than the deceptive client-side-only ghost animation noted in the 2026-07-21 entry below (which had fooled earlier investigation into thinking execution was happening when it wasn't).

**Files fixed this session:** `urdf/panda_mujoco.ros2_control.xacro` and `launch/mujoco_franka_moveit.launch.py` — corrected the stale/incorrect H3-as-fact comments to accurately describe what was actually checked, found, and left open. No functional/logic changes; `arm_control_mode` default (`both`) and behavior unchanged.

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

**Stage 2/3 (ROS2 + MoveIt2 + Controller):** **Milestone 1 FULLY CLOSED** (position-mode MoveIt2 execution validated under active trajectory tracking at 1000 Hz). **Milestone 2 NOW CLOSED (2026-07-22)** — joint-state indexing regression fixed, and Stage 3 effort-mode trajectory tracking is empirically confirmed to move the arm (numeric `/joint_states` proof, see entry above). The earlier "bit-for-bit frozen despite substantial torque" bug's proposed cause (Hypothesis 3) was refuted; a clean relaunch simply worked. Root cause of the original freeze is not fully understood but is no longer blocking. **Stage 4 (grasping) is next** — still blocked on the gaps identified 2026-07-22: fingers currently welded/mass-only with no joints or collision geometry in the MJCF, no graspable object in the scene, gripper controller only targets real hardware (not MuJoCo), `_move_arm()` stubbed, and the Stage 4 ROS2 orchestration node doesn't exist yet.

## Open questions / blockers
- **Milestone 1:** FULLY CLOSED (position-mode tracking validated under Plan & Execute).
- **Milestone 2:** **CLOSED 2026-07-22.** Joint-state indexing fix + Stage 3 effort-mode trajectory tracking both confirmed working via numeric `/joint_states` proof (real, substantial, multi-joint motion converging on commanded targets). Hypothesis 3 refuted with hard log + source evidence; root cause of the original freeze is not fully understood but no longer blocking (see entry above; H4 and the untested `arm_control_mode:=effort` fix are the leads to revisit only if the freeze recurs).
- **Stage 4 (grasping) — NOT YET STARTED, real gaps identified 2026-07-22 (before this session's Milestone 2 fix, still true now):**
  - The MJCF's hand/fingers are currently welded (no joints, no actuators, no collision geometry) — added purely as dead mass for a gravity-compensation fix. As configured, the gripper cannot physically open, close, or contact anything.
  - No graspable object exists anywhere in the MuJoCo scene.
  - `stage4/gripper_controller.py`'s only real (non-mock) implementation targets `franka_ros2`'s hardware action servers (`franka_gripper/action/Grasp` etc.) — incompatible with this MuJoCo/Jazzy stack. A MuJoCo-native gripper controller doesn't exist yet.
  - `_move_arm()` in `grasp_executor.py` still raises `NotImplementedError` — was blocked on Milestone 2 (now cleared), still needs real IK + trajectory + Stage 3 execution wiring.
  - The Stage 4 ROS2 orchestration node (joint-state subscriber + full grasp sequence loop) doesn't exist yet — only the offline, no-ROS2, no-sim `stage4/dry_run.py` exists.
- **Workflow improvements documented (carry forward):**
  - `ros2_ws/set_pinn_env.sh` sets PYTHONPATH ONLY — every fresh terminal must also source `/opt/ros/jazzy/setup.bash` and `ros2_ws/install/setup.bash`.
  - Use `ros2_ws/launch_pinn_controller.sh` (bundles all three setup commands) as standard entry point.
  - Use `/mujoco_ros2_control_node/reset_world` service for state recovery (faster than full restart).
  - If `ros2` CLI commands fail with `failed to initialize wait set: the given context is not valid`, this is a stale/corrupted `ros2 daemon`, not a real bug — `ros2 daemon stop` then `ros2 daemon start` resolved it 2026-07-22.
- **Environment fix (carry forward):** Always ensure `ros-jazzy-ros2controlcli` is installed.
- **MuJoCo-specific issues (carry forward from prior sessions):** URDF-to-MJCF conversion bug (workaround: static MJCF); zero-mass link rejection (fixed with real inertials); update_rate instability (fixed with 1000 Hz override); virtual joint TF (static publisher); gripper state (mock_components); RViz display flag — all ✓ applied. Joint state indexing fixed 2026-07-21.
- **Working tree:** All Stage 2/3 MuJoCo migration + Milestone 2 work (joint-indexing fix, moveit_plan_bridge, arm_control_mode plumbing, corrected comments) committed this session on `fix/effort-mode-actuator-lock` (the `fix/jointstate-name-indexing` branch was never actually given separate commits — both branches pointed at the same commit all along, so the work was committed as a clean series on the current branch instead of the originally-planned stack). Not merged to main — awaiting user review.

## What to do next session
1. **Milestone 1 + 2 are both closed.** Decide whether to merge `fix/effort-mode-actuator-lock` to main now, or keep iterating on this branch first.
2. **Stage 4 (grasping) is the next real body of work**, per user direction: "first version" = Franka picking up an object in MuJoCo. In dependency order: (a) give the gripper real prismatic joints + actuators + collision geometry in the MJCF, (b) add a graspable object to the scene, (c) write a MuJoCo-native gripper controller (ros2_control position/effort commands on the finger joints) to replace the hardware-only `FrankaROS2GripperController`, (d) implement `_move_arm()` in `grasp_executor.py`, (e) build the Stage 4 ROS2 orchestration node, (f) integration-test the full pick sequence live in MuJoCo.
3. Root cause of the original Milestone 2 freeze remains open but non-blocking — do not spend time on it unless it recurs.
