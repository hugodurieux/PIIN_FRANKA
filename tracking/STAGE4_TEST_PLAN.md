# Stage 4 — Configuration Validation Plan

**Created:** 2026-07-29
**Purpose:** turn "`pick()` worked at one pose" into a characterised capability with
real numbers, per SESSION.md's priority 1. Nothing here should be written up as a
Stage 4 result until the relevant phase below has run.

## Why this exists

As of run35, `pick()` succeeds at exactly one configuration: cube at
x=0.65, y=0, on the floor (z=0.02), axis-aligned, 64 g. Several of the fixes made
on 2026-07-29 were tuned against that single pose and may not generalise — the
flange-to-fingertip offset, the 45 deg finger alignment, the KDL IK budget, and
`gain_safety_margin_override:=4.0`.

Worse, the one pose we have is **marginal**. Counting every run at x=0.65:

| Run | Result | Note |
|-----|--------|------|
| 25 | FAIL | `Unable to sample any valid states for goal tree` |
| 27 | FAIL (1/2 attempts) | same message |
| 30 | SUCCESS | grasp error 0.0066 |
| 31 | SUCCESS | grasp error 0.0186 — cleared tolerance by 1.4 mm |
| 32 | **FALSE PASS** | grasped, then dropped during the lift; test reported success |
| 33 | FAIL | planning, sub-step 4/5, 5.01 s IK exhaustion |
| 34 | FAIL | planning, sub-step 4/5, identical |
| 35 | SUCCESS | grasp error 0.0064, width 0.039996 |

**3 clean successes in 8 runs.** x=0.65 sits near the IK envelope and is a poor
baseline. Establishing a reliable configuration is therefore phase A's real job,
not a formality.

---

## Standing protocol (applies to every run)

1. **One fresh sim per configuration.** Any MJCF change forces a rebuild anyway.
   Runs starting with a stale planning scene (33, 34) are the two that failed
   with leftover state; runs starting fresh (32, 35) both reached the grasp. Not
   proof, but free to control for.
2. **`reset_world_home.sh` between repeats** — never the reset service directly,
   or effort mode is silently lost and every torque is discarded.
3. **Verify the 5 cube sites agree before every configuration change** (see
   below). A mismatch means MoveIt2 plans to one place and MuJoCo puts the cube
   in another, and nothing reports it.
4. **3 runs minimum per configuration.** One run is an anecdote. Record the
   spread, not just pass/fail.
5. **Tee every run to `stage4/test_grasp_pick_runNN.log`**, incrementing NN.

### The 5 sites that must stay in sync

| # | File | What it governs |
|---|------|-----------------|
| 1 | `panda_arm_mujoco.xml` `grasp_object` body `pos` | where the cube starts at load |
| 2 | `panda_arm_mujoco.xml` `home` keyframe freejoint qpos | where `reset_world` puts it |
| 3 | `demo_targets.py` `"grasp_object"` entry | where the arm reaches |
| 4 | `test_grasp_pick.py` `add_collision_box` | what MoveIt2 avoids |
| 5 | `test_grasp_pick.py` `collision_object_position` | where it is re-placed before attach |

Sites 1 and 2 govern *different moments*: disagreement means the first run tests
one configuration and every run after a reset tests another.

### What to record per run

| Field | Source |
|-------|--------|
| Configuration | x, y, z, yaw, mass |
| Planning time per sub-step | gap between "converged" and next "planning succeeded" |
| Final grasp error | approach sub-step 2/2 line (tolerance 0.0200 m) |
| Final gripper width | `final gripper status` — `~0.040` held, `~0.020` dropped |
| Worst joint + `panda_joint5` bias | per-joint diffs |
| Result | SUCCESS / ARM_TIMEOUT / OBJECT DROPPED |

---

## Phase A — Distance (x). **No prep. Running now.**

| x [m] | Status | Expectation |
|-------|--------|-------------|
| 0.55 | in progress (run36+) | should have real IK margin |
| 0.65 | 3/8 (above) | near IK envelope |
| 0.45 | todo | short reach = a *different* singularity, never tested |
| 0.70 | todo | expect failure; likely needs a relaxed grasp orientation, not more solver time |

**Goal:** find the most reliable x and adopt it as the baseline for phases B, D, F.

### Results — x = 0.55

| Run | Result | Final grasp err | Final width | Worst joint | Max joint5 bias | Plan times |
|-----|--------|-----------------|-------------|-------------|-----------------|------------|
| 36 (first attempt) | **VOID** | — | — | — | — | effort mode never asserted after the fresh sim; `force_effort_mode.sh` step 1 returned `ok=False, "panda_arm_controller is already active"`, proving it. Arm sat at home, joint7 at -0.78529 (the documented discarded-torque fingerprint). Not a distance result. |
| 36 | SUCCESS | 0.0143 | 0.040029 | joint5 (4 of 8 waypoints) | -0.047 | all ~15 ms |
| 37 | SUCCESS | 0.0139 | 0.039989 | joint5 | -0.043 | all ~15 ms |
| 38 | SUCCESS | 0.0149 | 0.039995 | joint5 | -0.031 | all ~15 ms |

**x = 0.55: 3/3 success.** Grasp error 0.0139-0.0149 m, a **1.0 mm spread**,
against x=0.65's three successes at 0.0066 / 0.0186 / 0.0064 (a 12 mm spread, one
of them clearing tolerance by 1.4 mm). 0.55 is both more reliable AND far more
repeatable, which is what a results table needs. Planning stayed ~15 ms
throughout, never approaching the seconds-long searches that preceded the 0.65
failures.

`panda_joint5` was the worst joint at the FINAL grasp pose in all three runs,
always negative (-0.047 / -0.043 / -0.031). Clean signal for phase F.

### Results — x = 0.45 (folded arm)

| Run | Result | Final grasp err | Final width | Note |
|-----|--------|-----------------|-------------|------|
| 39 | SUCCESS | **0.0051** | 0.039990 | tightest grasp error of any run to date |
| 40 | **DROPPED** | — | 0.020014 | exactly the commanded setpoint (0.040 - 0.020 overtravel) |
| 41 | SUCCESS | — | 0.040537 | slightly wide of nominal; contact geometry differed a little |

**x = 0.45: 2/3.** Grasps more precisely than 0.55 on its good runs, but dropped one.

### Phase A summary

| x | Rate | Grasp error | Character |
|---|------|-------------|-----------|
| 0.45 | 2/3 | 0.0051 | folded arm, different singularity; one drop |
| 0.55 | **3/3** | 0.0139-0.0149 (1.0 mm spread) | fast planning, most repeatable |
| 0.65 | 3/8 * | 0.0064-0.0186 (12 mm spread) | planner failures |
| 0.70 | 3/3 | 0.0107-0.0135 | succeeds, but via a large detour every run; margins 0.0-0.4 mm |

**Baseline adopted: x = 0.55** — the only distance that is reliable, repeatable
AND free of reconfiguration detours.

**\* CAVEAT — x=0.65's 3/8 is NOT comparable to the others and must not be
tabulated beside them as-is.** It spans several code versions: runs 25 and 27
predate the gripper-geometry and KDL IK fixes, and runs 33/34 ran with the
damped-fallback controller change now in `stash@{0}`. The only same-code,
same-session figures are 0.45 = 2/3, 0.55 = 3/3, 0.70 = 3/3. **Re-run x=0.65
three times on current code before the report quotes any of this.**

**Note the rate ordering is non-monotone** (0.65 worse than 0.70 on current
numbers), which is itself evidence the 0.65 sample is contaminated rather than
evidence of a strange reachability island. Resolve it by re-measuring, not by
theorising.

### Two findings that outlive phase A

**1. The drop check was necessary, and it fired.** run40 returned
`GraspResult.SUCCESS` with `is_grasped=True` while the cube was on the floor.
Without the post-lift width check, x=0.45 would have been recorded as 3/3. Every
configuration in phases B-E depends on this check to produce honest numbers.

**2. Doubling the grip overtravel did NOT eliminate drops.** Grip is 2 N per
finger, nominally 6.4x the static requirement for a 64 g cube, and run40 still
lost it during the lift. Tally: 4 held / 1 dropped since the change, versus
2 held / 1 dropped before it. The static-margin calculation is therefore the
wrong model for what happens during a lift — acceleration and off-centre contact
matter more than the standing friction budget. **This is a phase D blocker**: a
1 kg cube weighs 15x what this one does, and the grip already fails on the light
one. Grip force needs to be derived from the lift dynamics, not from statics.

**3. `panda_joint5`'s bias is always negative and SCALES WITH REACH.**

| x | typical joint5 bias [rad] |
|---|---------------------------|
| 0.45 | ~-0.044 |
| 0.55 | ~-0.047 |
| 0.65 | ~-0.050 |
| 0.70 | ~-0.066 |

Monotone with extension, so it is load-dependent rather than a constant offset —
consistent with `e_ss = tau/Kp`, where a further-extended arm carries more torque
on that joint. This sharpens phase F: if the learned residual is what mispredicts
that load, disabling it should change the SLOPE of this trend, not merely shift
it. Measure the bias at two distances with and without the residual, not one.

### Results — x = 0.70 (envelope edge)

| Run | Result | Final grasp err | Final width | sub-step 5/5 trajectory | 5/5 margin |
|-----|--------|-----------------|-------------|-------------------------|------------|
| 42 | SUCCESS | 0.0130 | 0.039990 | **51 points / 4.91 s** | 0.4 mm |
| 43 | SUCCESS | 0.0107 | 0.040548 | **47 points / 4.57 s** | 0.2 mm |
| 44 | SUCCESS | 0.0135 | 0.041500 | **56 points / 5.47 s (at sub-step 4/5)** | **0.0 mm** |

run44 put the detour at sub-step 4/5 rather than 5/5, so the reconfiguration is
structural to the POSE while its position in the sub-step chain varies. It also
produced the worst numbers in the sweep: sub-step 4/5 converged at exactly
0.0400 against a 0.0400 tolerance (zero margin), with joint7 at -0.129 and
joint3 at -0.108 rad. Final width 0.0415 — the cube held noticeably askew.

**x = 0.70 succeeds, but not healthily.** Both runs showed the same large
detour — the arm swings AWAY from the target before returning — and both scraped
their convergence tolerance by a fraction of a millimetre. run42 also converged
its lift at 0.0299 against a 0.0300 tolerance (0.1 mm).

**Mechanism: null-space reconfiguration.** Every other waypoint in the sweep
plans 12-20 points in ~1.2 s. Sub-step 5/5 at 0.70 plans ~50 points over ~4.7 s,
reproducibly across both runs, because pre-approach sub-steps 1-4 leave the arm
in one elbow configuration while the final pre-approach pose requires another,
and the only collision-free joint-space path between them goes the long way
round. Reproducible => geometry, not OMPL sampling variance.

**Reportable conclusion:** the envelope edge is not a binary reach limit. Before
planning fails outright (as at x=0.65), the system first degrades into long
reconfiguration detours and sub-millimetre convergence margins. On hardware the
unannounced swing through a large workspace volume is a safety concern in its own
right, independent of whether the pick succeeds.

Note vs x=0.65: planning is ~15 ms per sub-step here, against 2.5 s in the runs
that then failed at 0.65. `panda_joint5` is the worst joint more often at 0.55
than at 0.65 (where joint7 usually was), and its bias is larger, which makes
phase F more interesting rather than less.

**Watch:** planning time is the leading indicator. run35 planned each sub-step in
~15 ms; runs 33/34 took 2.5 s and then failed. A jump into seconds means the
start state is drifting into contorted null-space configurations — the arm can
satisfy a Cartesian flange tolerance while the elbow is somewhere useless (run34
ended with `joint1 = -0.359 rad`, ~21 deg off-axis, for a cube at y=0).

## Phase B — Lateral offset (y). **No prep.**

y = -0.25 / 0 / +0.25 at phase A's best x.

Everything so far has been at y=0 — the worst case for KDL but the best case for
symmetry. Off-axis grasps load `panda_joint1` and the wrist differently.

**Watch:** whether the `panda_joint5` bias grows, shrinks, or flips sign.

## Phase F — Residual ablation. **No prep. Do early, right after phase A.**

Re-run the best configuration with `disable_residual:=true`
(`ros2_ws/launch_pinn_controller_no_residual.sh`), RNEA + PD only.

`panda_joint5` carries a systematic, always-negative steady-state bias
(~0.013-0.063 rad) at every waypoint in every run, untouched by every fix made
this session. This is the one open question that could implicate Stage 1.

- Bias **vanishes** -> the learned residual introduces a systematic torque bias
  on that joint. A real result for goal.md objective 2, not a debugging step.
- Bias **persists** -> it is the PD/gravity structure, not the model.

Either answer belongs in the report. Cheapest high-value test in this plan.

### RESULT — the residual DEGRADES tracking under sim-to-sim transfer

Run with `ros2_ws/launch_pinn_controller_ablation.sh 4.0` (NOT
`launch_pinn_controller_no_residual.sh` — see that script's header: it omits the
gain override and would have changed Kp and the residual simultaneously,
invalidating the comparison). x=0.55, margin 4.0, everything else identical.

Final grasp pose (approach sub-step 2/2):

| Run | Residual | joint5 [rad] | joint3 | joint4 | Flange err [m] |
|-----|----------|--------------|--------|--------|----------------|
| 36 | on | -0.0264 | -0.0155 | -0.0104 | 0.0141 |
| 37 | on | -0.0434 | -0.0183 | -0.0095 | 0.0139 |
| 38 | on | -0.0312 | -0.0162 | -0.0111 | 0.0149 |
| 45 | **off** | **-0.0011** | -0.0003 | +0.0003 | **0.0076** |
| 46 | **off** | **-0.0019** | -0.0007 | -0.0010 | **0.0073** |

**Mean joint5 bias -0.0337 -> -0.0015 (22x reduction). Mean flange error
0.0143 -> 0.0075 (halved).** Every joint improved by roughly an order of
magnitude, not just joint5. run46's approach sub-step 1/2 converged at 0.0039 m,
better than any residual-on run anywhere in the sweep.

**The gain confound pushes the OTHER way**, which is why the result survives it:
had the launcher failed to pass `gain_safety_margin_override`, Kp would be lower
and `e_ss = tau/Kp` would make errors LARGER. They are much smaller.

#### Interpretation — state this carefully

Defensible: **the Isaac-trained residual degrades tracking when transferred to
MuJoCo.** The checkpoint is `isaac-multipayload-frictionnet-satfix`, trained to
predict `tau_real - tau_RNEA` on Isaac Sim data. It learned the discrepancy
between RNEA and *Isaac's* dynamics (friction, damping, contact) and is being
applied to a MuJoCo model that does not have those characteristics — i.e. it is
evaluated out of distribution, and a systematic offset is exactly what that
predicts. RNEA + PD alone is closer to MuJoCo's true dynamics than
RNEA + Isaac-residual is.

NOT defensible from this data: that the grey-box approach fails, or that the
residual is wrong. Nothing here evaluates the residual against the dynamics it
was trained on.

**This directly motivates the sim-to-real fine-tuning novelty (N3-Duong,
already implemented, frozen-backbone) and gives it a measured baseline to beat.**
The obvious follow-up, which would turn a negative result into a positive one:
fine-tune the residual on MuJoCo data and re-run this exact comparison. If the
fine-tuned residual beats RNEA+PD, that is the strongest Stage 1 result the
project could produce, and this ablation is its control.

**Caveat on scope:** measured at ONE distance (0.55) with n=2 vs n=3. Before the
report quotes the 22x figure, repeat at a second distance — 0.70 is the natural
choice, since the joint5 bias scales with reach and the residual's contribution
should scale with it too if this reading is right.

## Phase C — Object orientation (yaw). **Needs a small code change.**

Cube rotated about z by 15 / 30 / 45 deg.

**Prep:** the grasp yaw is currently **hardcoded** — `_TOP_DOWN_FINGERS_ALIGNED`
assumes an axis-aligned cube. It must be derived from the object's pose.
**Also:** the MJCF freejoint qpos carries 3 position + 4 quaternion values; the
body `quat` and the keyframe quaternion must both change, so sites 1 and 2 gain a
rotational component.

## Phase D — Mass / payload. **Needs real prep. Highest scientific value.**

This is the only test that exercises `ComputedTorquePDController.update_payload(delta)`
— Stage 1's residual is payload-conditioned, trained at 0/1/3 kg, and that path
has **never** been run in a real grasp. It is a direct test of goal.md's
payload-conditioning novelty rather than a robustness check.

**Prep 1 — grip force.** Squeeze is `kp * overtravel` = `200 N/m * 0.010 m` =
**2 N per finger**. With mu=1 across two fingers that holds roughly **0.4 kg**. A
1 kg cube weighs 9.8 N and will drop every time. The MJCF finger actuator's `kp`
must be raised (and the result re-verified — the overtravel mechanism itself was
"NOT YET LIVE-VALIDATED" until run32 disproved the 3.2x static margin).

**Prep 2 — wire `delta`.** `update_payload(delta)` must actually be called when
the grasp closes, and reset on release.

**Test masses:** 0.064 kg (current), then masses matching the training deltas —
1 kg and 3 kg.

**The actual experiment**, beyond pass/fail: run each mass **with the correct
`delta` and with `delta=0`**, and compare tracking error during the lift. That
isolates what payload conditioning buys, which is the claim the report needs to
support.

## Phase E — Table / support height. **Needs the attach-ordering fix first.**

**Prep — attach ordering.** `_attach_object()` currently attaches at the
pre-approach pose, while the cube is still on the floor, so MoveIt2 stores it
~0.31 m below the flange and the *phantom* cube follows the gripper down through
any support surface. This is why the floor box had to be deleted. A table cannot
be deleted the same way.

Fix: attach only **after** the gripper closes (what MoveIt's own pick pipeline
does, and what is physically true), add a `finally` detach in `GraspExecutor` so
an abort cannot leak the attachment, then restore the floor collision box.

**Then:** add a table to **both** the MJCF (a real body, so physics is right) and
the MoveIt2 planning scene (a collision object). The two must agree exactly, like
the 5 cube sites.

**Test heights:** table top at ~0.2 m and ~0.4 m.

**Watch:** the arm sits higher and less extended, so re-check the joint5 bias and
the wrist chatter that was visible at stretched poses with `safety_margin=4.0`.

---

## Order of work

1. **Phase A** (running) — establish a reliable baseline x.
2. **Phase F** — one run, answers the Stage 1 question.
3. **Phase B** — no prep, extends the envelope map.
4. **Phase E prep** (attach ordering) — also fixes a known correctness bug
   independent of the table.
5. **Phase D prep** (grip force + `delta` wiring) — then phase D.
6. **Phases C and E** — last, both need the code changes above.

## Open defects that this plan does not fix

Recorded so they are not mistaken for test failures:

- **Ctrl-C drops the arm.** No shutdown handoff exists; effort mode is safe only
  while `pinn_controller_node` is publishing. On hardware this is what brakes are
  for. A handoff to position mode is the fix, but position mode is an untuned PID
  (`mujoco_pid.yaml`, self-documented as buzzing), so the handoff needs the
  setpoint-provenance question answered first.
- **`ResetWorld` produced an uncommanded fast slew once** (2026-07-29). Root
  cause not established. Candidates: the 7-second window in position mode during
  `force_effort_mode.sh`, and/or the old undamped gravity-only fallback.
- **A damped-hold fallback fix exists but is stashed** (`stash@{0}`), held back so
  Stage 3 stays byte-identical to the run35 baseline. Reapply and re-validate
  once the sweep has a stable reference.
- **`move_group` logs `Found empty JointState message`** at every convergence
  check. Unexplained; probably benign.

## Phase B — lateral offset (y), at x = 0.55, residual ON, margin 4.0

**Sample-size caveat: phase B was run at n=1 per offset**, unlike phase A's n=3.
Treat these as indicative, not as rates. Repeat before quoting.

| Run | y | Result | Final grasp err | joint5 at final grasp | joint3 | joint1 | Planning |
|-----|---|--------|-----------------|------------------------|--------|--------|----------|
| 36-38 | 0 | 3/3 | 0.0139-0.0149 | -0.026 to -0.043 | ~-0.016 | ~1e-4 | healthy |
| 48 | +0.25 | SUCCESS | 0.0175 | **-0.0510** | -0.0219 | 0.0019 | healthy, no detours |

**Off-axis costs tracking, not planning.** Planning stayed healthy (15-19 points,
no detours, no "still converging" ticks), but the final grasp error rose to
within 2.5 mm of tolerance and joint5's bias grew ~50% over the on-axis mean —
the largest seen at this distance.

**joint1 stayed small (0.0019)** despite carrying the off-axis reach, so the
difficulty is NOT landing on the joint that does the lateral swing. joint5
absorbs it, consistent with the load-dependent bias seen across the reach sweep.

---

# STATUS AND NEXT SESSION

**As of end of 2026-07-29.**

## Status board

| Phase | What | Status |
|-------|------|--------|
| A | Distance x = 0.45 / 0.55 / 0.65 / 0.70 | **DONE** (0.65 needs a same-code re-run, see caveat above) |
| F | Residual ablation at x=0.55 | **DONE, major result** (n=2 vs n=3) |
| B | Lateral offset y | **PARTIAL** — y=+0.25 done (n=1). y=-0.25 is CONFIGURED BUT NOT RUN |
| C | Object yaw | NOT STARTED — needs code change |
| D | Mass / payload | NOT STARTED — needs MJCF + code change |
| E | Height / table | NOT STARTED — needs the attach-ordering fix first |

## IMPORTANT — the repo is left mid-configuration

The five cube sites are currently set to **x=0.55, y=-0.25, z=0.02**, staged for
the phase B run that was not executed. The next session either runs it (run49) or
changes the configuration before running anything. Do not assume y=0.

`stash@{0}` holds the **damped safe-fallback fix** for `pinn_controller_node.py`.
It was deliberately held back so Stage 3 stayed byte-identical to the run35
baseline through the whole sweep. It is a real fix for a real defect (the old
fallback was gravity-compensation-only: no damping, no position hold, recomputed
at the current measured q every tick, so the arm was neutrally buoyant and drifted
freely). Reapply with `git stash pop` and re-validate, but NOT in the middle of a
measurement series.

## Phase B — remaining

1. **y = -0.25** — already configured, just run it. **Not a mirror of +0.25**:
   `panda_hand` carries a -45 deg twist and the grasp orientation compensates with
   a fixed `Rz(+45)`. The compensation is identical on both sides, but the wrist
   reaches it through different parts of its range depending on which way joint1
   swung. If -0.25 is markedly worse than +0.25, the fixed 45 deg correction is
   the first suspect — and that finding feeds directly into phase C.
2. **Top up to n=3** at each offset. Phase B currently runs at n=1 while phase A
   used n=3; the numbers are indicative, not rates.

## Phase C — object yaw. Prep required.

**The blocker:** the grasp yaw is hardcoded. `demo_targets.py` uses
`_TOP_DOWN_FINGERS_ALIGNED = _TOP_DOWN @ Rz(+45 deg)`, a fixed world-frame
orientation that assumes an axis-aligned cube. A rotated cube needs the yaw
derived from the object's pose.

**Work:**
1. Add a yaw parameter to the `grasp_object` target, or derive it from the
   collision object's orientation, so the fingers stay square to the cube's faces
   rather than to the world.
2. The MJCF freejoint qpos carries **3 position + 4 quaternion** values. Both the
   body `quat` AND the keyframe quaternion must be set, so sites 1 and 2 gain a
   rotational component. A qpos shorter than `nq` is silently zero-padded by
   MuJoCo's compiler — the documented cause of the cube once teleporting to the
   origin with a degenerate w=0 quaternion.
3. Test 15 / 30 / 45 deg about z.

**Success criterion is the gripper width, not the flange error.** A wrong yaw
still converges the flange fine and then closes on the cube's diagonal: 0.0566 m
for this cube (0.04*sqrt(2)), less corner squeeze. run29 measured exactly that
(0.0526 m). Width is the instrument here.

## Phase D — mass / payload. Prep required. HIGHEST SCIENTIFIC VALUE.

This is the only test that exercises
`ComputedTorquePDController.update_payload(delta)`. Stage 1's residual is
payload-conditioned, trained at 0/1/3 kg, and that code path has **never** been
run in a real grasp. It is a direct test of goal.md's payload-conditioning
novelty rather than a robustness check.

### The numbers, worked out

Cube: `<geom type="box" size="0.02 0.02 0.02" density="1000">` = a 0.04 m cube,
volume 6.4e-5 m^3, mass **0.064 kg**. To change mass, change `density`:

| Target mass | density |
|-------------|---------|
| 0.064 kg (current) | 1000 |
| 1 kg | 15625 |
| 3 kg | 46875 |

`GraspConfig.object_mass` must be updated to match, in `test_grasp_pick.py`.

### Grip force is the blocker, and there is a hard ceiling

Finger actuator (`panda_arm_mujoco.xml`):
`<position name="panda_finger_joint1_position" kp="200" kv="3" ctrlrange="0 0.04" forcerange="-20 20"/>`

Squeeze force = `kp * (overtravel per finger)`. Currently
`200 * 0.010 = 2 N` per finger. Holding mass m by friction (mu=1, two contacts)
needs `F >= m*g/2`:

| Mass | Force needed per finger | kp needed at 0.010 m overtravel |
|------|--------------------------|----------------------------------|
| 0.064 kg | 0.31 N | 31 (have 200) |
| 1 kg | 4.9 N | **490** |
| 3 kg | 14.7 N | **1470** |

**Two hard limits:**
- `ctrlrange="0 0.04"` means maximum achievable overtravel is 0.02 m per finger
  (commanding fully closed on a 0.04 m cube). At kp=200 that caps squeeze at
  **4 N per finger — about 0.8 kg**. A 1 kg cube cannot be held at all without
  raising kp.
- `forcerange="-20 20"` caps force at 20 N per finger regardless of kp, so the
  absolute ceiling is ~4 kg at mu=1. **3 kg leaves only ~1.4x margin** — and
  run40 showed a 6.4x STATIC margin still dropped a 64 g cube during the lift.
  Expect 3 kg to be genuinely marginal; treat it as a limit-finding run, not an
  expected pass.

**Raising kp also needs kv re-tuned.** Critical damping is `c = 2*sqrt(kp*m)`
with finger mass ~0.015 kg; kv=3 pairs with kp=200. At kp=1000, kv should be
~8. The MJCF's own actuator comment documents an earlier underdamped-overshoot
problem from getting this wrong — read it before changing anything.

### `delta` must actually be wired

`update_payload(delta)` exists but is never called. It needs to be invoked when
the grasp closes and reset on release. Until that is done, the residual runs at
`delta=0.00` no matter what is being carried.

### The actual experiment

Beyond pass/fail: run each mass **with the correct `delta` AND with `delta=0`**,
and compare tracking error during the lift. That isolates what payload
conditioning buys, which is the claim the report needs to support.

**Note the interaction with phase F's result.** The Isaac-trained residual already
degrades tracking in MuJoCo at delta=0. If the payload conditioning also mispredicts
under transfer, the delta=0 case may well track BETTER than the correct-delta case.
That would be an honest and interesting result, and phase F is its control — but it
must not be reported as "payload conditioning does not work" without the sim-to-real
fine-tuning comparison, for exactly the reasons in phase F's interpretation section.

## Phase E — height / table. Prep required. DO THE ATTACH FIX FIRST.

**The blocker, and it is not optional here.** `GraspExecutor._attach_object()`
attaches the cube at the pre-approach pose, while the cube is still on the floor.
MoveIt2 therefore stores it ~0.31 m below the flange, and on the descent the
*phantom* attached cube follows the gripper down through whatever is underneath.
This is why the floor collision box had to be deleted on 2026-07-29. A table
cannot be deleted the same way — it has to be in the planning scene, because the
arm must not plan through it.

**Work, in this order:**
1. Attach only **after** the gripper closes (what MoveIt's own pick pipeline does,
   and what is physically true).
2. Add a `finally` detach in `GraspExecutor` so an abort cannot leak the
   attachment into `move_group`, which survives restarts of the test script.
3. Restore the floor collision box in `test_grasp_pick.py`.
4. Only then add the table.

**Adding the table:** it must exist in **both** the MJCF (a real body, so physics
is right) and the MoveIt2 planning scene (a collision object), and the two must
agree exactly — the same discipline as the 5 cube sites, with the same silent
failure mode if they disagree. The cube's z in all five sites also moves to
`table_top + 0.02`.

**Test heights:** table top at ~0.2 m and ~0.4 m.

**Watch:** the arm sits higher and less extended, so re-check the joint5 bias
(which scales with reach — it should DROP at table height, and that is a
prediction worth testing) and the wrist chatter seen at stretched poses with
`safety_margin=4.0`.

## Also outstanding, not part of the sweep

- **Ctrl-C drops the arm.** No shutdown handoff exists. On hardware this is what
  brakes are for. Fix is a handoff to position mode, but that PID is untuned
  (`mujoco_pid.yaml`, self-documented as buzzing), so the setpoint-provenance
  question has to be answered first: *where does the arm go when position mode
  engages from a pose that is not home?* One experiment answers it.
- **`ResetWorld` produced an uncommanded fast slew once.** Not reproduced since
  the damped fallback was written — but that fix is stashed, so the exposure is
  back. Candidates: the ~7 s window in position mode during `force_effort_mode.sh`
  (measured: teleport at t=744.4, effort restored at t=751.5), and/or the
  undamped fallback.
- **`move_group` logs `Found empty JointState message`** at every convergence
  check. Unexplained, probably benign, never chased.
- **x=0.65 needs 3 runs on current code** so phase A's table stops mixing code
  versions.
