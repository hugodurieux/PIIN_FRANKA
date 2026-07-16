# Project State — PINN Franka Pipeline
_Last updated: 2026-07-16 (Stage 2 + Stage 3 integration session: first working MoveIt2 motion-planning setup targeting simulated Franka Panda in Isaac Sim, Stage 3 ComputedTorquePDController wired into the ROS2 node for the first time, Milestone 1 of Stage 2/3 end-to-end integration achieved and confirmed working — changes NOT YET COMMITTED)_

## 1. Objectives (from goal.md)
| # | Objective | Status | Evidence / where proven |
|---|-----------|--------|-------------------------|
| 1 | Automated "URDF-to-Model" Pipeline — accept any URDF, auto-extract kinematics via Pinocchio, generate network, produce trained dynamic model | in progress | `pinocchio_baseline/rnea_wrapper.py` (URDF -> RNEA); `network/grey_box_net.py` + `training/train.py` (architecture + training loop). N4 data-efficiency ablation flag (`--max_samples`) merged. **`pinocchio_baseline/panda.urdf` mass/inertia fix (2026-07-16, commit c179740):** the URDF shipped with zero `<inertial>` tags on any link; RNEA had been running on Pinocchio's placeholder inertias, not real Franka mass properties, for the project's entire prior history. Fixed with official `franka_description` values; discovered via first-ever comparison against an independently-massed physics engine (Isaac Sim). **Isaac Sim 6.0.1 data pipeline VALIDATED end-to-end** (`generate_isaac_dataset.py`, GPU machine): all 3 payloads (0/1/3 kg, ~49k samples each) generated with corrected URDF. A second data-quality issue (actuator-saturation-contaminated samples inflating the residual tail) was found and fixed — see Stage 1 section below. **First real (GPU) training runs DONE**: see `tracking/experiments_log.csv` — `isaac-multipayload-frictionnet-satfix` is the current reference baseline (val RMSE 0.80/0.88/0.90/0.54/0.37/0.36/0.30 Nm per joint). Li et al. (2025) payload-ID review and Li et al. (2025) compliant-PINN review both independently confirm dual payload-awareness (RNEA white-box + tau_res delta input) is ahead of the published art. |
| 2 | High-Frequency Real-Time Control at 1000 Hz (MPC integration, microsecond inference) | in progress | Stage 2: MoveIt2 motion planning working end-to-end against a simulated Franka Panda in Isaac Sim (Milestone 1, this session — see Stage 2 section). Stage 3: `ComputedTorquePDController` is now wired into `pinn_controller_node.py`'s control loop for the first time (this session), closing a gap where the node previously always published zero torques. **Not yet proven at 1000 Hz driven by the trained model** — Milestone 1's Plan & Execute currently runs through MoveIt2's own default `joint_trajectory_controller` (position commands), not through `pinn_controller_node`/Stage 3; that routing is Milestone 2, not yet done. Inference-latency benchmark still not written. |
| 3 | Scaling to 7-DoF — Augmented Lagrangian constraints + residual friction on a full Franka Panda | in progress | `training/constraints.py` implements AL penalties (torque limits + dissipativity) for all 7 joints. Stage 3 hard-clips to per-joint TORQUE_LIMITS. N2-Liu FrictionNet IMPLEMENTED (`network/friction_net.py`): structural dissipativity guarantee via Softplus-diagonal D matrix; hard guarantee `tau_friction · qdot <= 0` always; 6,087 params; physics PASSED. Hu et al. (2026) review passively validates that RNEA covers load-dependent terms and tau_res captures motion-state residuals. |
| 4 | Standardized Sim-to-Real Gap resolution via physics-constrained fine-tuning | in progress | `training/fine_tune.py` on branch `novelty/duong2024-N3-simtoreal-finetune` — PASSED physics validation. Loads pre-trained GreyBoxNet, freezes all layers except last 2 nn.Linear modules, fine-tunes under full PINN loss (MSE + AL). First code implementation of Goal 4. Real data pipeline (HDF5) not yet built. |

## 2. Pipeline architecture (URDF -> trained robot)

tau_pred = RNEA(q, qdot, qddot; URDF + delta) + GreyBoxNet([sin(q), cos(q), qdot, delta]) + FrictionNet([sin(q), cos(q), qdot, delta])
Loss     = MSE(tau_pred, tau_real) + AugmentedLagrangian(torque_limits, dissipativity)

FrictionNet is optional (--use_friction_net flag). When active, its structural guarantee absorbs part of the dissipativity constraint, so the AL lambda_dissip multiplier grows more slowly — intended and correct.

### Stage 1 — PINN dynamics learning
Fully architected and pipeline validated. 6 CPU smoke-test runs completed (20 epochs, pre-URDF-fix, mechanics-only validation) plus **2 real GPU training runs (200 epochs, Isaac Sim data, corrected URDF)** — see `tracking/experiments_log.csv`. Current reference baseline: `isaac-multipayload-frictionnet-satfix` (`models/run_20260716_121302/`), best val loss 0.3995, per-joint val RMSE [0.80, 0.88, 0.90, 0.54, 0.37, 0.36, 0.30] Nm.

**Actuator-saturation data-quality fix (2026-07-16):** the first real training run (`isaac-multipayload-frictionnet-first-real`) trained successfully (best val loss 1.4767) but `controller/compute_error_bound.py` — written to get a real error bound for the Stage 3 Lyapunov gains — found per-joint *maximum* validation error of 91-110 Nm, exceeding the joint's own 87 Nm torque limit. Root cause: Isaac Sim's simulated actuator saturating at `maxEffort` under aggressive trajectory tracking; `tau_real` for those samples was the clamp value, not real dynamics, while `tau_theo` (computed from the *reference* acceleration) assumed the trajectory was actually achieved. The prior over-torque filter (`|tau| > limit`) didn't catch these since clamped samples sit exactly *at* the limit. Fixed via `SATURATION_MARGIN = 0.97` in `generate_isaac_dataset.py` (excludes samples within 3% of the limit); all 3 payload datasets regenerated (148,304 samples, down from 148,760) and retrained. Result: best val loss improved ~4x (1.4767 -> 0.3995), and the augmented-Lagrangian `dissip_viol` term changed from oscillating (never settling, up to 0.0657) to smoothly converging to 0.0006 — the contaminated samples were destabilizing training broadly, not just inflating a diagnostic tail. A smaller, distinct residual outlier population remains on joints 1-4 (p99.9 of 3-6 Nm, true max 26-65 Nm on ~0.09% of samples) attributed to transient PD-servo correction spikes at trajectory-segment starts, not saturation; this is now the basis for the Stage 3 Lyapunov error bound (below) via a p99.9-not-max methodology, documented as a deliberate weakening of the formal worst-case guarantee.

- White-box RNEA: `pinocchio_baseline/rnea_wrapper.py` — wraps `pinocchio.rnea`, handles payload injection into end-effector inertia, runs offline only.
- Residual network: `network/grey_box_net.py` — MLP (default 4x256, Mish), input X in R^22 = [sin(q), cos(q), qdot, delta], output tau_res in R^7. ReLU forbidden.
- FrictionNet: `network/friction_net.py` — 2-layer Mish MLP (22->64->64->7), output D_diag = Softplus(d) + 1e-6, tau_friction = -D_diag * qdot. Structural guarantee: tau_friction · qdot = -sum(Softplus(d_i)*qdot_i^2) <= 0 always. 6,087 parameters. Exposes `forward(q, qdot, delta) -> tau_friction` and `forward_D(q, qdot, delta) -> D_diag`. (N2-Liu, synthesising N1-Duong + N1-SPEL)
- Physics constraints: `training/constraints.py` — `AugmentedLagrangian` class; enforces |tau_pred| <= TORQUE_LIMITS and tau_res · qdot <= 0 (dissipativity) with dual-ascent multiplier updates.
- Training loop: `training/train.py` — Adam optimizer, 90/10 train/val split, CSV logging, best-checkpoint save. Supports `--synthetic` (no Pinocchio needed) and real HDF5 datasets. Accepts `--max_samples N` (N4) and `--use_friction_net` (N2-Liu); when friction net active, logs D_diag mean per joint per epoch and saves `friction_net_best.pt` alongside `greybox_best.pt`.
- Sim-to-real fine-tuning: `training/fine_tune.py` — loads pre-trained checkpoint, freezes all layers except last 2 nn.Linear modules (4th hidden layer + output layer), fine-tunes for `--max_steps` gradient steps (default=100) under full PINN loss. Saves `greybox_finetuned.pt`. (N3-Duong)
- Dataset: `training/dataset.py` — `_random_subsample_indices()` helper; `FrankaDynamicsDataset` (single HDF5), `MultiPayloadDataset` (list of HDF5, concatenates tensors then subsamples combined pool), and `SyntheticDataset` all accept `max_samples` param (seed=42, before train/val split). `--data` CLI arg accepts one or more paths (multi-payload training validated 2026-06-26, 147,734 samples).
- Constants: `network/constants.py` — single source of truth for joint limits, velocity limits, input/output dims, payload values, `FRICTION_NET_HIDDEN = 64`.

Data pipeline:
- **Isaac Sim generator VALIDATED end-to-end** (`generate_isaac_dataset.py`) — PRIMARY training data source, Isaac Sim 6.0.1 (`isaacsim.*` namespace). Plays Fourier+Sobol trajectories inside Isaac Sim physics engine; tau_real from `get_measured_joint_efforts()` (Isaac Sim Franka USD friction/damping); tau_theo from Pinocchio RNEA (corrected panda.urdf). tau_res is non-zero and physically meaningful. Filters both over-torque and near-saturation samples (`SATURATION_MARGIN = 0.97`, see Stage 1 section above). Outputs `data/isaac_{payload}kg.h5` (same HDF5 schema). Run via Isaac Sim's bundled Python (`./python.sh generate_isaac_dataset.py --payload N`) from the Isaac Sim install directory — output lands in `<cwd>/data/`, must be moved to the project's `data/` directory before training.
- **Fourier baseline** (`generate_fourier_dataset.py`) — SMOKE-TEST ONLY. tau_res = synthetic Coulomb+viscous (hand-tuned). Useful for CPU pipeline validation; does not produce paper-quality residuals. Outputs `data/fourier_baseline_{payload}kg.h5`.

### Stage 2 — Motion planning (MoveIt2 / ROS2)
**First working implementation this session (2026-07-16), NOT YET COMMITTED to git.** Targets a *simulated* Franka Panda in Isaac Sim, not real hardware yet.

- **MoveIt2 config source changed:** instead of a hand-built SRDF/kinematics config, this now uses NVIDIA's official `IsaacSim-ros_workspaces` (`jazzy_ws/isaac_moveit` package) directly. Deliberate simplification per CLAUDE.md's "keep it simple, just enough to showcase Stage 1" directive for Stage 2 — avoids maintaining a duplicate hand-authored MoveIt2 config for a robot NVIDIA already ships one for.
- **ROS2 distro corrected:** runs on **ROS2 Jazzy**, matching this machine's Ubuntu 24.04. The project's earlier ROS2 scaffold (branch `stage2/moveit2-ros2-humble`, see below) had incorrectly assumed Humble.
- **New `simulation/` top-level directory** (untracked, new): `simulation/isaac_franka_moveit_bridge.py` — an Isaac Sim standalone script exposing the Franka Panda over ROS2 topics `isaac_joint_states` (state, published) / `isaac_joint_commands` (position/velocity/effort, subscribed). This is the "simulated hardware" counterpart that `isaac_moveit` needs to talk to; adapted from NVIDIA's own bundled reference example rather than written from scratch.
- **Milestone 1 — ACHIEVED and confirmed working end-to-end this session:** MoveIt2 Plan & Execute in RViz successfully drives the simulated Franka Panda in Isaac Sim via this bridge. Currently this goes through MoveIt2's own default `joint_trajectory_controller` (position commands) — **NOT yet through `pinn_controller_node`/Stage 3.** That routing is Milestone 2 (see below), not yet started.
- Pre-existing scaffold (branch `stage2/moveit2-ros2-humble`, `ros2_ws/src/pinn_franka_controller/`) still exists on disk and has been edited this session (see Stage 3 below for what changed in `pinn_controller_node.py`) but is not yet the thing MoveIt2 talks to for Milestone 1 — it becomes relevant again at Milestone 2.
- `trajectory_interpolator.py`: linear interpolation of (q_des, qdot_des, qddot_des) from JointTrajectory messages — unchanged this session.
- `launch/pinn_controller.launch.py` and `config/controller_params.yaml` — both edited this session (see git diff; ROS2 Jazzy path/parameter updates).

**Milestone 2 (immediate next step, not yet started):** route MoveIt2's planned trajectory through `pinn_controller_node` so that Stage 3's trained-model-driven torque control — not MoveIt2's default position execution — actually drives the simulated robot.

### Stage 3 — Controller + integration
`ComputedTorquePDController` (fully implemented and tested since the earlier `stage3/computed-torque-pd-controller` merge) **is now wired into the ROS2 node for the first time this session** — the integration gap is closed, but NOT YET COMMITTED.

- `controller/model_loader.py`: loads `GreyBoxNet` checkpoint from `.pt` + `config.json`. Unchanged this session.
- `controller/lyapunov_gains.py`: N3-Liu — computes `Kd = safety_margin * error_bound`, `Kp = Kd^2 / 4` (critical damping). `DEFAULT_ERROR_BOUND = [5.20, 5.66, 3.06, 3.80, 2.10, 2.38, 1.57]` Nm, recomputed 2026-07-16 (earlier session) from real validation data. **This session added `MANUAL_ERROR_BOUND = [5,5,5,5,2,2,2]` Nm + `MANUAL_PD_KP`/`MANUAL_PD_KD` (safety_margin=1.0)** — a conservative fixed fallback run through the same critical-damping formula, used by the ROS2 node when its `use_lyapunov_gains` parameter is `False`. Previously that parameter had no effect (the node had no fallback gains to switch to); now it does.
- `controller/compute_error_bound.py`: reconstructs the exact train/val split used by `training/train.py`, evaluates a checkpoint (GreyBoxNet + optional FrictionNet) on the validation set, and reports per-joint RMSE, percentiles (p50/p90/p99/p99.9/max), and worst-5-samples-per-joint. Unchanged this session.
- `controller/computed_torque_pd.py`: `ComputedTorquePDController.step()` — `tau = RNEA(q, qdot, qddot_des) + tau_res(q, qdot, delta) + Kp*(q_des - q) + Kd*(qdot_des - qdot)`, hard-clipped to TORQUE_LIMITS; all I/O numpy; `torch.no_grad()` for inference. `update_payload(delta)` updates delta at runtime (e.g. after grasping). Unchanged this session.
- `controller/payload_identification.py`: still a TODO stub, unchanged this session.
- **`ros2_ws/src/pinn_franka_controller/pinn_franka_controller/pinn_controller_node.py` — wiring closed this session.** Previously this file had a `TODO(stage3)` stub in `_compute_torques()` that always published zero torques regardless of the loaded model or gains — `ComputedTorquePDController` existed as a tested class but was never actually invoked by the control loop. That gap is now closed: the node instantiates and calls `ComputedTorquePDController.step()` per control tick, selecting Lyapunov-computed gains (`DEFAULT_KP`/`DEFAULT_KD`) or the new manual fallback gains (`MANUAL_PD_KP`/`MANUAL_PD_KD`) based on the `use_lyapunov_gains` parameter.
- **Not yet proven under real load:** this wiring has NOT yet been exercised end-to-end against Isaac Sim — Milestone 1 (this session) used MoveIt2's own default `joint_trajectory_controller`, not `pinn_controller_node`. Milestone 2 (routing through `pinn_controller_node`) is the test that will actually exercise this new code path.
- Files touched this session (uncommitted): `controller/__init__.py`, `controller/lyapunov_gains.py`, `ros2_ws/src/pinn_franka_controller/pinn_franka_controller/pinn_controller_node.py`, `ros2_ws/src/pinn_franka_controller/config/controller_params.yaml`, `ros2_ws/src/pinn_franka_controller/launch/pinn_controller.launch.py`, `ros2_ws/src/pinn_franka_controller/package.xml`, `ros2_ws/src/pinn_franka_controller/setup.py`.

### Stage 4 — Grasping (optional)
Scaffolded and merged to main (commit b86f335). Fully isolated — zero modifications to Stages 1-3.

- `stage4/grasp_config.py`: `GraspConfig` dataclass — all grasping parameters in one place: grasp_width/force/speed, epsilon_inner/outer, open_width/speed, pre_approach_height/speed, lift_height/speed, max_torque_error, gripper_timeout, arm_motion_timeout, object_mass.
- `stage4/gripper_controller.py`: `BaseGripperController` ABC + `FrankaROS2GripperController` (ROS2 Humble, franka_gripper Grasp/Move/Homing action clients, joint_states subscriber for `read()`, goal cancellation in `stop()`) + `MockGripperController` (no-hardware testing).
- `stage4/grasp_executor.py`: `GraspExecutor` state machine — `pick()` and `place()` methods; phases IDLE -> PRE_APPROACH -> APPROACH -> GRASPING -> LIFTING -> HOLDING -> RELEASING -> ABORTED. After successful grasp calls `arm.update_payload(object_mass)` to update Stage 3 controller payload estimate.
- `stage4/demo_targets.py`: named poses (box_center, box_left, box_right, place_tray, home); orientations TOP_DOWN and TILTED_30; `get_target(name)` returns (4,4) homogeneous transform in Franka base frame.
- `stage4/dry_run.py`: 6 offline tests (successful pick+place, gripper failure, abort, GraspConfig defaults, demo_targets validation, MockGripperController transitions) — all pass without hardware / ROS2 / trained model. Run with: `python -m stage4.dry_run`.

**Progress note (2026-07-16, this session):** `_move_arm()`'s blocker was "Stage 2+3 validated end-to-end integration." Milestone 1 of that integration (MoveIt2 Plan & Execute driving simulated Franka Panda in Isaac Sim) is now done — Stage 4 is one step closer. Still blocked on Milestone 2 (routing through the actual trained-model-driven `pinn_controller_node`, not just MoveIt2's default execution) before `_move_arm()` can be implemented against a real control path rather than a placeholder.

Remaining gaps (blocked on Stages 2+3 Milestone 2):
- `_move_arm()` in `grasp_executor.py` raises `NotImplementedError`; needs IK (Pinocchio or MoveIt2) + trajectory generation (Stage 2) + 1 kHz execution via Stage 3. `TODO(stage4-arm-motion)` marks the integration point.
- Stage 4 ROS2 orchestration node (joint-state subscriber + full grasp sequence).

## 3. Implemented novelties
| ID | From paper | Description | Goal served | Branch | Validated | Merged |
|----|-----------|-------------|-------------|--------|-----------|--------|
| N1-Djeumou | Djeumou et al. (2022) | Compositional grey-box structure: known analytical terms (RNEA) composed with neural residual. REJECT — already fully implemented as the project's core architecture in `grey_box_net.py`. Architecture corroborated by peer-reviewed paper. | Goal 1, Goal 3 | main | architecture match confirmed | n/a (pre-existing) |
| N2-Djeumou | Djeumou et al. (2022) | Augmented Lagrangian training with Lagrange multiplier dual-ascent for hard physics constraints. REJECT — already fully implemented in `constraints.py`. | Goal 3 | main | architecture match confirmed | n/a (pre-existing) |
| N3-Djeumou | Djeumou et al. (2022) | Semi-supervised constraint enforcement on unlabeled joint-space points to extend dissipativity guarantees beyond training trajectories. INVESTIGATE — ablation study needed. | Goal 3, Goal 4 | not started | not validated | not merged |
| N1-Liu | Liu et al. (2024) | RK4 rollout loss — augment the training loss with a 4th-order Runge-Kutta forward simulation residual. REJECT — conflicts with RNEA grey-box architecture; would destroy primary novelty. | — | rejected | — | — |
| N2-Liu | Liu et al. (2024) | Cholesky dissipativity structural constraint — FrictionNet sub-module with Softplus-diagonal D matrix; tau_friction = -D_diag * qdot; hard structural guarantee tau_friction · qdot <= 0 always. Synthesises N2-Liu (Cholesky concept) + N1-Duong (L L^T algebraic kernel, diagonal case) + N1-SPEL (revolute-joint sparsity: diagonal D, not full 28-entry Cholesky). KEEP — IMPLEMENTED in `network/friction_net.py`; `--use_friction_net` flag in `training/train.py`; logs D_diag mean per joint; saves `friction_net_best.pt`. 6,087 parameters. Physics validator advisory: lambda_dissip grows more slowly when active (intended). | Goal 3 | `novelty/N2-Liu-frictionnet` | PASSED (physics validator) | **MERGED to main (commit ebc2ba3)** |
| N3-Liu | Liu et al. (2024) | Lyapunov stability template for Stage 3 controller — `Kd = safety_margin * error_bound`, `Kp = Kd^2/4` (critical damping), `DEFAULT_ERROR_BOUND = [5,5,5,5,2,2,2]` Nm placeholder. KEEP — implemented in `controller/lyapunov_gains.py`. DEFAULT_KP/DEFAULT_KD recomputed from real data (2026-07-16); a separate `MANUAL_PD_KP`/`MANUAL_PD_KD` fallback (fixed, safety_margin=1.0) was added this session for `use_lyapunov_gains=False` deployments — see Stage 3 section. | Goal 2 | `stage3/computed-torque-pd-controller` | PASSED (physics validator) | **MERGED to main** |
| N4-Liu | Liu et al. (2024) | `--max_samples` data-efficiency ablation flag — truncate training data to N random samples (seed=42, before train/val split) to quantify how few samples are needed vs. Liu's 25k-sample benchmark. KEEP — implemented. | Goal 1 | `novelty/liu2024-N4-max-samples` | PASSED (physics validator, non-blocking advisories) | **MERGED to main** |
| N1-Duong | Duong et al. (2024) | Cholesky-factored inverse mass sub-network — L L^T + eps*I algebraic trick (28 lower-triangular entries for 7x7 matrix, Softplus on diagonal) guarantees positive-definiteness. INVESTIGATE — algebraic input to N2-Liu FrictionNet design (diagonal case used). Folds into N2-Liu; implemented there. | Goal 3 | folds into N2-Liu | folded into N2-Liu PASSED | not separate |
| N2-Duong | Duong et al. (2024) | Separate dissipation sub-network. REJECT — duplicate of N1-Duong's algebraic core; no independent contribution beyond what N1-Duong and N2-Liu already capture. | — | rejected | — | — |
| N3-Duong | Duong et al. (2024) | 100-step payload fine-tuning protocol — freeze all layers except last 2 nn.Linear modules (4th hidden layer + output layer), fine-tune for `--max_steps` steps (default 100, range 50–200) under full PINN loss (MSE + AL), lr=1e-4 to limit catastrophic forgetting. KEEP — IMPLEMENTED in `training/fine_tune.py`. First code realisation of Goal 4. | Goal 4 | `novelty/duong2024-N3-simtoreal-finetune` | PASSED (physics validator) | **MERGED to main (commit 0aa4fdc)** |
| N1-WangCAC | Wang et al. (CAC 2024) | Sobol quasi-random data sampling — 10 Sobol-sampled q_center configurations per payload in `generate_fourier_dataset.py`; scipy.stats.qmc.Sobol, 7-D joint space, scrambled, per-payload seed. IMPLEMENTED — validated 2026-06-26. | Goal 1 | main | confirmed working | merged (in generate_fourier_dataset.py) |
| N2-WangCAC | Wang et al. (CAC 2024) | Trapezoidal physics residual in PINN loss — time-discretised integration of dynamics residual at 20 Hz. REJECT — conflicts with RNEA offline-qddot path (same fundamental problem as N1-Liu); 20 Hz discretisation incompatible with 1 kHz target. | — | rejected | — | — |
| N3-WangCAC | Wang et al. (CAC 2024) | EKF noise filter at PINN-NMPC interface — Extended Kalman Filter to denoise joint state estimates before feeding the PINN. REJECT — matrix inversion per control step is incompatible with sub-ms 1 kHz loop latency requirement. | — | rejected | — | — |
| N1-SPEL | Wang et al. (Scientific Reports 2025) | Physics-driven sparsity masks on friction matrix — CONFIRMED 2026-06-26 via `pinocchio_baseline/friction_sparsity_analysis.py`: all 7 Franka joints are JointModelRZ (independent revolute), URDF friction/damping all zero, 80% parameter reduction (7 vs 28 params). Diagonal D physically justified. Folds into N2-Liu FrictionNet. | Goal 3 | folds into N2-Liu | CONFIRMED via Pinocchio analysis | not separate |
| N2-SPEL | Wang et al. (Scientific Reports 2025) | URDF inertia constants as trainable scalar parameters — make Pinocchio URDF link inertias learnable during training. REJECT — violates RNEA-intact invariant; making them learnable weakens the white-box guarantee that is central to Goal 1. | — | rejected | — | — |
| N3-SPEL | Wang et al. (Scientific Reports 2025) | KAN (Kolmogorov-Arnold Network) activations replacing MLP layers. REJECT — violates Mish/Softplus-only activation constraint; also demonstrates 14% overfitting on real hardware data. | — | rejected | — | — |
| N1-WhenPhysics | Prabhakar et al. (ICLR 2026) | Equality/inequality constraint scheduling — annealing the strength of physics constraints over training epochs. REJECT — already the exact structure in `training/constraints.py` (dual-ascent augmented Lagrangian). | — | rejected | — | — |
| N2-WhenPhysics | Prabhakar et al. (ICLR 2026) | EMA momentum-smoothed per-residual loss balancing (beta=0.95). INVESTIGATE — per-joint val RMSE diagnostic LIVE in `training/train.py` (printed at end of every run). Fourier baseline result 2026-06-26: ratio 1.0× (joints 1-4: 0.239 Nm, 5-7: 0.247 Nm) — no imbalance on synthetic residual. Revisit after real robot recordings. | Goal 3 | diagnostic in main | confirmed no imbalance on Fourier data | diagnostic merged |
| N3-WhenPhysics | Prabhakar et al. (ICLR 2026) | UDE frozen-backbone fine-tuning — Universal Differential Equation approach with frozen physics backbone. REJECT — duplicate of N3-Duong already implemented in `training/fine_tune.py`. | — | rejected | — | — |
| N1-BacklashPINN | Hu et al. (IEEE/ASME T-Mech 2026) | Amplitude-weighted training loss — weight loss by motion amplitude to emphasise high-excitation segments when backlash is dominant. REJECT — redundant with N2-WhenPhysics EMA balancing (same motivation, same mechanism); also validated only on SIASUN/ROKAE 6-DoF with ReLU activations (forbidden). | — | rejected | — | — |
| N2-BacklashPINN | Hu et al. (IEEE/ASME T-Mech 2026) | Gaussian basis-function output head — replace final linear layer with a Gaussian RBF layer to localise backlash responses. REJECT — requires labeled backlash windows (unavailable for Franka); ReLU used throughout (forbidden activation). | — | rejected | — | — |
| N3-BacklashPINN | Hu et al. (IEEE/ASME T-Mech 2026) | TCN (Temporal Convolutional Network) sliding-window inference — replace MLP with causal TCN to capture hysteresis history. REJECT — stateful sliding window breaks the stateless 1 kHz control loop; incompatible with the project's real-time constraint. | — | rejected | — | — |
| N1-PayloadPINN | Li et al. (IEEE RA-L 2025) | QDD current-based payload identification — estimate payload inertia from quasi-direct-drive motor currents, no torque sensor needed. REJECT — Franka uses gearboxes (not QDD), making current-to-torque mapping nonlinear and unreliable; architecture mismatch. | — | rejected | — | — |
| N2-PayloadPINN | Li et al. (IEEE RA-L 2025) | Virtual payload link injection in Pinocchio for white-box payload awareness. REJECT — ALREADY FULLY IMPLEMENTED: `pinocchio_baseline/rnea_wrapper.py` uses `_inject_payload()` / `_restore_payload()` methods that modify the end-effector link inertia in Pinocchio before each RNEA call. This project's implementation predates and exceeds the paper's. | — | n/a (pre-existing) | architecture match confirmed | n/a (pre-existing) |
| N3-PayloadPINN | Li et al. (IEEE RA-L 2025) | PINN-inside-NMPC at 100 Hz — embed the trained PINN as a forward model inside a nonlinear MPC predict-and-optimise loop at 100 Hz. REJECT — CLAUDE.md mandates Stage 2 uses standard MoveIt2; NMPC replaces rather than extends MoveIt2, and 100 Hz is below the 1 kHz target. | — | rejected | — | — |
| N1-CompliantPINN | Li et al. (2025) — compliant manipulators | DeLaN-FFNN grey-box with explicit compliance terms (spring/damper contact model appended to RNEA). REJECT — harmful for Franka rigid-body dynamics: adding compliance terms to a rigid-body RNEA introduces model error, not model improvement; Franka has harmonic reducers, not compliant joints. Paper valuable as Related Work citation confirming independent validation of the grey-box DeLaN approach. | — | rejected | — | — |
| N2-CompliantPINN | Li et al. (2025) — compliant manipulators | Payload-weighted loss scaling (scale loss by estimated payload effect per joint). REJECT — weaker duplicate of N2-WhenPhysics EMA diagnostic; N2-WhenPhysics per-joint RMSE diagnostic already implemented in `training/train.py` with exponential smoothing option; no new mechanism. | — | rejected | — | — |
| N1-PIKANs | Toscano et al. (2025) | PIKAN (Physics-Informed Kolmogorov-Arnold Network) — replace MLP layers with B-spline/wavelet KAN layers throughout the PINN architecture. REJECT — KAN activations violate CLAUDE.md Mish/Softplus-only smoothness constraint; duplicate of N3-SPEL rejection reason. Toscano et al. survey broadly corroborates existing design choices (grey-box, AL constraints, frozen-backbone fine-tuning). | — | rejected | — | — |
| N2-SNRDiag | Toscano et al. (2025) | Spectral normalisation of residual diagonal (SNR) — apply spectral normalisation to the output layer of the residual network to enforce Lipschitz continuity. REJECT — serves no goal.md objective; project's AL dissipativity constraint already enforces energy-consistent behaviour; adding spectral normalisation would complicate the gradient landscape without a clear physics motivation. | — | rejected | — | — |
| N1-DeLaN4EC | Lutter, Listmann, Peters (IROS 2019) | Energy coherence loss — joint training loss enforcing T + V = H (kinetic + potential = Hamiltonian) across the Lagrangian network during rollout. REJECT — requires explicit T/V output heads that are absent from the grey-box RNEA-residual architecture; adding them would require learning H(q, qdot) explicitly, breaking the RNEA-intact invariant (Goal 1). | — | rejected | — | — |
| N2-DeLaN4EC | Lutter, Listmann, Peters (IROS 2019) | Forward + inverse model consistency loss — enforce that the forward model (M(q)qddot = tau) and inverse model (tau_pred) agree on the same trajectory. REJECT — requires computing H^{-1}(q) at 7-DoF (7x7 matrix inversion per sample); computationally expensive and introduces the same conflict as N1-Liu (RK4 rollout) with the RNEA white-box path. | — | rejected | — | — |
| N3-DeLaN4EC | Lutter, Listmann, Peters (IROS 2019) | Parametric Stribeck friction model — augment the Lagrangian network output with a Stribeck curve parameterised by static friction, Coulomb friction, and Stribeck velocity (tanh/sign-based). REJECT — sign(qdot) is non-smooth and violates the Mish/Softplus smoothness constraint; Stribeck static-friction peak is not present in Franka's harmonic-reducer joints; FrictionNet (N2-Liu, MERGED) already provides a structurally superior smooth dissipation parameterisation. | — | rejected | — | — |
| N1-DeLaN | Lutter, Ritter, Peters (ICLR 2019) | Cholesky L(q)L(q)^T parameterisation for the full inertia matrix H(q) — learn a lower-triangular L(q) such that H = L L^T guarantees positive definiteness everywhere. REJECT — the project's RNEA (via Pinocchio) already provides H(q) analytically from the URDF, making a learned H superfluous; Cholesky concept already absorbed into N1-Duong and ultimately the diagonal FrictionNet (N2-Liu, MERGED). Seminal paper: original source for Cholesky+Softplus diagonal design pattern in physics-structured NNs. | — | rejected | — | — |
| N2-DeLaN | Lutter, Ritter, Peters (ICLR 2019) | Online in-loop model update at 200 Hz — re-run a few gradient steps on the Lagrangian network during closed-loop execution to adapt to changing conditions. REJECT — breaks the stateless 1 kHz control loop invariant (no gradient computation at runtime); N3-Duong offline fine-tuning (MERGED) already covers the model-update goal without runtime overhead. | — | rejected | — | — |
| N1-DiffNEA | Sutanto et al. (L4DC 2020) | Differentiable Newton-Euler Algorithm (DiffNEA) with learnable inertial parameters — make URDF link masses and inertias differentiable and jointly optimised with the neural residual. REJECT — violates the RNEA-intact invariant: making URDF parameters learnable destroys the white-box analytical guarantee that is the core of Goal 1 (automated URDF-to-model pipeline). | — | rejected | — | — |
| N2-DiffNEA | Sutanto et al. (L4DC 2020) | Per-joint theta^2 viscous damping term — add a quadratic velocity-dependent damping d_i * qdot_i^2 per joint in the RNEA output. REJECT — weaker variant of the existing FrictionNet (N2-Liu, MERGED): FrictionNet learns a full nonlinear D(q, qdot, delta) * qdot dissipation, which subsumes the fixed quadratic approximation; Sutanto's quadratic form also ignores payload conditioning. | — | rejected | — | — |
| N3-DiffNEA | Sutanto et al. (L4DC 2020) | Online payload adaptation via gradient descent on RNEA inertial parameters — update payload-related link inertias online by backpropagating through the differentiable RNEA. REJECT — subsumed by the existing dual payload-awareness mechanism: `_inject_payload()` in `rnea_wrapper.py` (white-box path) + delta conditioning of tau_res (residual path). Running gradients through RNEA at 1 kHz is computationally incompatible with real-time control. | — | rejected | — | — |

## 3a. Primary baseline — Liu et al. (2024) competitive gaps
Liu et al. (2024): "Physics-Informed Neural Networks to Model and Control Robots:
A Theoretical and Experimental Investigation" — the primary state-of-the-art reference.

| # | Gap in Liu et al. | This project's answer |
|---|-------------------|----------------------|
| 1 | No URDF-to-model automation — equations manually derived per robot | Goal 1: fully automated URDF -> Pinocchio -> network pipeline |
| 2 | Control at 500 Hz only, no MPC integration | Goal 2: targets 1000 Hz; Stage 2 MoveIt2 planning working end-to-end against simulated Franka in Isaac Sim (Milestone 1, 2026-07-16); Stage 3 controller wired into the ROS2 node (2026-07-16); Milestone 2 (routing planned trajectories through the trained-model controller) not yet done |
| 3 | No payload conditioning | Payload delta in R^1 baked into every network input ([sin(q), cos(q), qdot, delta]); tested at 0 / 1 / 3 kg |
| 4 | No sim-to-real transfer protocol | Goal 4: 2-step pre-train (sim) + fine-tune (real motor-babbling) under PINN loss; `training/fine_tune.py` implements this (N3-Duong) |
| 5 | No torque / velocity limits in loss | AL constraints enforce torque limits and dissipativity for all 7 joints; Stage 3 hard-clips at publish boundary |
| 6 | Full black-box Lagrangian — no RNEA white-box term | Grey-box: RNEA white-box + learned residual; RNEA baseline never modified |

## 3b. Secondary validations from paper reviews (no implementation required)
Independent papers reviewed have produced secondary findings that strengthen existing design choices:

1. **Backlash error is payload-independent and motion-state-dependent** (Hu et al., IEEE/ASME T-Mech 2026): Paper shows backlash manifests as a function of velocity direction and joint position, not payload mass. This passively validates the grey-box decomposition: RNEA correctly accounts for all load-dependent (inertia, Coriolis, gravity) terms, and the learned tau_res cleanly captures the motion-state-dependent residual (including backlash-like phenomena) without entanglement with payload dynamics.

2. **Dual payload-awareness is ahead of the published state of the art** (Li et al., IEEE RA-L 2025): Li et al. propose virtual payload link injection in Pinocchio as a novel contribution. This project already implements exactly this mechanism in `pinocchio_baseline/rnea_wrapper.py` (`_inject_payload()` / `_restore_payload()`), and additionally conditions the learned residual network on the payload scalar delta — providing a second, independent pathway for payload adaptation that Li et al. do not have. No code changes needed; this is a documented advantage over the published baseline.

3. **DeLaN-FFNN grey-box architecture independently validated** (Li et al., 2025 — compliant manipulators): Li et al. apply a DeLaN-style FFNN grey-box (analytical structured terms + neural residual) to compliant robotic manipulators and confirm it outperforms pure black-box models. This is an independent peer-reviewed validation of the grey-box design philosophy used in this project, from a different domain (compliant vs. rigid-body). Useful citation for PAPER_DRAFT.md Section 2 (Related Work).

4. **Broad survey corroborates existing design choices** (Toscano et al., 2025 — PIKANs survey): A comprehensive survey of PINNs vs. PIKANs confirms that grey-box compositions with analytical physics terms, augmented Lagrangian constraint enforcement, and frozen-backbone fine-tuning are recognised best practices in the current state of the art. No architectural changes warranted; serves as a broad citation for PAPER_DRAFT.md Section 2.

5. **DeLaN lineage confirms RNEA-intact superiority and FrictionNet design** (Lutter et al. IROS 2019 + ICLR 2019; Sutanto et al. L4DC 2020 — processed 2026-06-30): The three foundational papers of the Lagrangian-NN / differentiable-RNEA lineage all converge on the same limitation: learning H(q) (DeLaN) or making URDF inertias differentiable (DiffNEA) provides flexibility at the cost of breaking the analytical white-box guarantee. The project's RNEA-intact grey-box approach avoids this trade-off entirely. Secondary findings: (a) Sutanto et al. confirm Pinocchio's suitability for 7-DoF batched RNEA at training time; (b) Sutanto et al. identify a static-friction gap in their DiffNEA that the project's FrictionNet (N2-Liu, MERGED) + augmented Lagrangian dissipativity directly address; (c) Lutter ICLR 2019 is the original source for the Cholesky + Softplus-diagonal design pattern that N2-Liu FrictionNet descends from — cite in PAPER_DRAFT.md Section 2 as the lineage anchor. All three papers are cite-worthy in the Related Work section.

## 3c. Physics validator advisories (non-blocking)
1. N4 branch — dissipativity multiplier is batch-mean (pre-existing, not introduced by N4 branch) — consider per-sample multipliers if enforcement is weak at runtime.
2. N4 branch — at very small max_samples (< ~2000 from a 25k dataset), random draw may under-sample high-velocity excitation regions — document this in ablation study.
3. N3-Liu (Stage 3) — DEFAULT_KP/DEFAULT_KD are placeholders computed from `DEFAULT_ERROR_BOUND = [5,5,5,5,2,2,2]` Nm. Gains must be recomputed via `compute_lyapunov_gains(real_error_bound)` once Stage 1 produces validation error statistics. **RESOLVED 2026-07-16** — see Stage 1/Stage 3 sections; a separate fixed `MANUAL_PD_KP`/`MANUAL_PD_KD` fallback was added this session (uncommitted) for the `use_lyapunov_gains=False` path, which previously had no gains to fall back to.
4. N3-Duong (`training/fine_tune.py`) — freeze logic uses `named_modules()` to select "last 2" nn.Linear modules. If a future architecture revision adds skip-connection Linear layers outside `self.net`, the count could shift. Document this assumption when the architecture evolves.
5. N2-Liu FrictionNet — `lambda_dissip` in AugmentedLagrangian will grow more slowly when `--use_friction_net` is active, because FrictionNet structurally absorbs part of the dissipativity constraint. This is intended and correct behaviour; document in ablation comparison between runs with and without the flag.
6. Prabhakar et al. (ICLR 2026) key negative result: physics constraints HURT temporal extrapolation beyond the training window (+6-10% error increase). Scope project claims to in-distribution trajectory following accordingly; do not claim out-of-distribution extrapolation without evidence.

## 4. Current repository structure
```
pinn_franka/
|-- goal.md                          4 scientific objectives (north star)
|-- Step1_Indication.md              Full Stage 1 methodology (5-step pipeline)
|-- CLAUDE.md                        Architecture rules and agent permissions
|-- SESSION.md                       Cross-session state (maintained by session-scribe)
|-- requirements.txt                 Python dependencies
|
|-- network/
|   |-- constants.py                 Franka Panda physical constants; FRICTION_NET_HIDDEN=64
|   |-- grey_box_net.py              GreyBoxNet MLP + encode_state(); the learned residual
|   |-- friction_net.py              FrictionNet: 2-layer Mish MLP (22->64->64->7);
|   |                                D_diag = Softplus(d)+1e-6; tau_friction = -D_diag*qdot;
|   |                                hard structural guarantee tau_f·qdot <= 0; 6,087 params
|   |-- __init__.py
|
|-- training/
|   |-- constraints.py               AugmentedLagrangian: torque-limit + dissipativity
|   |-- dataset.py                   SyntheticDataset + FrankaDynamicsDataset (HDF5);
|   |                                _random_subsample_indices() for N4 ablation
|   |-- train.py                     Main training loop (Adam + AL dual ascent);
|   |                                --max_samples CLI arg (N4);
|   |                                --use_friction_net flag (N2-Liu): adds FrictionNet
|   |                                params to optimizer, logs D_diag mean per joint per
|   |                                epoch, saves friction_net_best.pt
|   |-- fine_tune.py                 N3-Duong: frozen-layer fine-tuning on real data;
|   |                                last 2 nn.Linear unfrozen; --max_steps default=100
|   |-- __init__.py
|
|-- pinocchio_baseline/
|   |-- rnea_wrapper.py              RneaBaseline: URDF -> batched RNEA, payload injection
|   |                                (_inject_payload / _restore_payload); ahead of Li 2025
|   |-- __init__.py
|
|-- controller/                      [branch: stage3/computed-torque-pd-controller; wiring
|   |                                  changes 2026-07-16 UNCOMMITTED, see Stage 3 section]
|   |-- __init__.py                  UNCOMMITTED changes this session (2026-07-16)
|   |-- model_loader.py              Loads GreyBoxNet checkpoint from .pt + config.json
|   |-- lyapunov_gains.py            N3-Liu: Kd = safety_margin*error_bound, Kp = Kd^2/4;
|   |                                UNCOMMITTED this session: added MANUAL_ERROR_BOUND +
|   |                                MANUAL_PD_KP/MANUAL_PD_KD fallback gains (safety_margin=1.0)
|   |-- computed_torque_pd.py        ComputedTorquePDController.step(); 1 kHz torque kernel;
|   |                                update_payload() for runtime delta changes; NOW WIRED
|   |                                into pinn_controller_node.py (2026-07-16, uncommitted)
|   |-- payload_identification.py    TODO stub: least-squares payload ID from static torque
|   |                                measurements; RNEA linearity in mass → 1-unknown
|   |                                closed-form regression; call before 1 kHz loop
|
|-- simulation/                      NEW this session (2026-07-16), UNTRACKED/UNCOMMITTED
|   |-- isaac_franka_moveit_bridge.py  Isaac Sim standalone script: exposes Franka Panda
|                                      over ROS2 topics isaac_joint_states (state, pub) /
|                                      isaac_joint_commands (pos/vel/effort, sub); adapted
|                                      from NVIDIA's bundled IsaacSim-ros_workspaces example;
|                                      "simulated hardware" counterpart to isaac_moveit
|
|-- ros2_ws/                         [branch: stage2/moveit2-ros2-humble — distro now
|   |                                  actually ROS2 Jazzy on this machine; NOT the primary
|   |                                  MoveIt2 path for Milestone 1, see Stage 2 section]
|   |-- src/pinn_franka_controller/
|       |-- pinn_controller_node.py  UNCOMMITTED this session: TODO(stage3) stub RESOLVED —
|       |                            now instantiates + calls ComputedTorquePDController.step()
|       |                            per tick; selects Lyapunov vs manual gains via
|       |                            use_lyapunov_gains param
|       |-- trajectory_interpolator.py  Linear interp of (q_des, qdot_des, qddot_des);
|       |                            unchanged this session
|       |-- launch/
|       |   |-- pinn_controller.launch.py   UNCOMMITTED changes this session
|       |-- config/
|           |-- controller_params.yaml      UNCOMMITTED changes this session
|
|-- stage4/                          [merged to main: commit b86f335]
|   |-- grasp_config.py              GraspConfig dataclass: all grasping parameters
|   |-- gripper_controller.py        BaseGripperController ABC; FrankaROS2GripperController
|   |                                (ROS2 Humble action clients); MockGripperController
|   |-- grasp_executor.py            GraspExecutor state machine: pick()/place(), 8 phases;
|   |                                calls arm.update_payload() after successful grasp;
|   |                                _move_arm() still NotImplementedError — one step closer
|   |                                after Stage 2/3 Milestone 1 (2026-07-16), still blocked
|   |                                on Milestone 2
|   |-- demo_targets.py              Named poses + orientations; get_target() -> (4,4) SE3
|   |-- dry_run.py                   6 offline tests; run: python -m stage4.dry_run
|
|-- tracking/
|   |-- PROJECT_STATE.md             This file
|   |-- papers_review.csv            One row per paper processed
|
|-- papers/
|   |-- inbox/                       EMPTY — 3 unacquired papers remain outside repo
|   |                                (s11433-025-2810-1, s41598-026-50630-y_reference,
|   |                                ssrn-6550385); refill manually when obtained
|   |-- processed/
|       |-- Liu et al. (2024)...     (primary baseline, see section 3a)
|       |-- Djeumou et al. (2022)... (processed)
|       |-- Duong et al. (2024)...   (processed)
|       |-- Wang et al. (CAC 2024)   (processed — Trajectory Control / NMPC)
|       |-- Wang et al. (2025)...    (processed — SPEL)
|       |-- Prabhakar et al. (2026). (processed — "When Does Physics Help?", ICLR 2026; relevance 1; N2-WhenPhysics INVESTIGATE)
|       |-- Hu et al. (2026)...      (processed — Backlash PINN, IEEE/ASME T-Mech; relevance 1, all REJECTed; secondary finding: backlash payload-independence validates RNEA decomposition)
|       |-- Li et al. (2025)...      (processed — Payload ID PINN, IEEE RA-L; relevance 1, all REJECTed; secondary finding: dual payload-awareness already implemented, ahead of paper)
|       |-- Li et al. (2025)...      (processed — compliant manipulator PINN, DeLaN-FFNN; relevance 2, N1-CompliantPINN + N2-CompliantPINN REJECTed; secondary finding: independent validation of grey-box design; cite in Related Work Section 2)
|       |-- Toscano et al. (2025)... (processed — PINNs to PIKANs survey; relevance 1, N1-PIKANs + N2-SNRDiag REJECTed; secondary finding: survey corroborates grey-box + AL + frozen-backbone design; cite in Related Work Section 2)
|       |-- Lutter, Listmann, Peters (IROS 2019)... (processed — DeLaN for energy-based control of under-actuated systems; relevance 1, all REJECTed; bibliographic value: foundational DeLaN predecessor, cite as origin of Lagrangian NN lineage)
|       |-- Lutter, Ritter, Peters (ICLR 2019)...  (processed — Deep Lagrangian Networks seminal paper; relevance 1, all REJECTed; bibliographic value: original source for Cholesky+Softplus-diagonal PD-matrix design; cite in Related Work Section 2)
|       |-- Sutanto et al. (L4DC 2020)...          (processed — Differentiable Newton-Euler Algorithm; relevance 1, all REJECTed; secondary findings: Pinocchio suitability for 7-DoF confirmed; static friction gap in DiffNEA validates FrictionNet + AL design)
|
|-- docs/
|   |-- HOW_TO_USE.md
|   |-- STAGE1_README.md
|
|-- .claude/
    |-- agents/                      Agent role definitions
    |-- commands/process-papers.md   /process-papers workflow
    |-- skills/paper-review-format.md
    |-- hooks/                       block-python-run.sh + session-end-reminder.sh
```

## 5. Open items / next steps

### Done since last update (2026-07-16, Stage 2/3 integration session)
- [x] **Stage 2 first working implementation** — MoveIt2 motion planning against a *simulated* Franka Panda in Isaac Sim, using NVIDIA's official `IsaacSim-ros_workspaces` (`jazzy_ws/isaac_moveit`) rather than a hand-built SRDF/kinematics config; ROS2 Jazzy (correcting the earlier scaffold's incorrect Humble assumption).
- [x] **New `simulation/isaac_franka_moveit_bridge.py`** — Isaac Sim standalone bridge exposing Franka Panda over `isaac_joint_states`/`isaac_joint_commands` ROS2 topics, the counterpart `isaac_moveit` needs.
- [x] **Milestone 1 achieved and confirmed working**: MoveIt2 Plan & Execute in RViz successfully drives the simulated Franka Panda in Isaac Sim (via the default `joint_trajectory_controller`, not yet via Stage 3).
- [x] **Stage 3 `ComputedTorquePDController` wired into `pinn_controller_node.py` for the first time** — the previous `TODO(stage3)` zero-torque stub is resolved; the node now actually calls `.step()` per control tick.
- [x] **`controller/lyapunov_gains.py`: added `MANUAL_PD_KP`/`MANUAL_PD_KD` fallback gains** (fixed conservative error bound, safety_margin=1.0) for the node's `use_lyapunov_gains=False` path, which previously had no effect.
- [ ] **NOT YET COMMITTED** — all of the above is still in the working tree: `controller/__init__.py`, `controller/lyapunov_gains.py`, `ros2_ws/src/pinn_franka_controller/pinn_franka_controller/pinn_controller_node.py`, `ros2_ws/src/pinn_franka_controller/config/controller_params.yaml`, `ros2_ws/src/pinn_franka_controller/launch/pinn_controller.launch.py`, `ros2_ws/src/pinn_franka_controller/package.xml`, `ros2_ws/src/pinn_franka_controller/setup.py`, and the new untracked `simulation/` directory. Commit and push before starting further Stage 2/3 work.

### Immediate next step — Stage 2/3 Milestone 2 (not yet started)
- **Route MoveIt2's planned trajectory through `pinn_controller_node`** so that Stage 3's trained-model-driven torque control — not MoveIt2's default position execution via `joint_trajectory_controller` — actually drives the simulated robot. This is what will, for the first time, exercise the newly-wired `ComputedTorquePDController` end-to-end against a live (simulated) robot rather than only in isolated tests.
- Once Milestone 2 is done, revisit `stage4/grasp_executor.py`'s `_move_arm()` — it can then be implemented against the real Stage 2/3 control path instead of remaining a `NotImplementedError` stub.

### Done since prior update (2026-07-16, earlier Stage 1 session)
- [x] **`pinocchio_baseline/panda.urdf` mass/inertia fix** — added real Franka `franka_description` inertials to every link; RNEA was previously running on Pinocchio placeholder inertias. Commit `c179740`, pushed to `origin/main`.
- [x] **Isaac Sim 6.0.1 data pipeline validated end-to-end** — namespace migration (`isaacsim.*`), pinocchio/cmeel import fix, Franka USD asset path, `TORQUE_LIMITS` dtype, `world.stop()` API, RNEA reduced-model (locking finger joints), tracking-error + drive-gain diagnostics. Same commit as above.
- [x] **First two real GPU training runs completed and logged** (`tracking/experiments_log.csv`): initial run found an actuator-saturation data-quality bug via a newly-written diagnostic tool (`controller/compute_error_bound.py`); fixed in `generate_isaac_dataset.py` (`SATURATION_MARGIN = 0.97`); re-generated + retrained. `isaac-multipayload-frictionnet-satfix` is now the reference baseline (best val loss 0.3995, see Stage 1 section for full writeup).
- [x] **Stage 3 Lyapunov gains recomputed from real data** — `DEFAULT_ERROR_BOUND` in `controller/lyapunov_gains.py` replaced with real per-joint p99.9 validation error, no longer a `[5,5,5,5,2,2,2]` Nm placeholder. Methodology (p99.9 vs. max, and why) documented in code comments and PAPER_DRAFT.md §3.6.
- [x] `experiments/EXPERIMENT_PLAN.md` Block G extended with a fine-grained payload-interpolation test (eval-only 0.5/1.5/2.5 kg against the {0,1,3} kg trained model).
- [x] PAPER_DRAFT.md updated: URDF-fix methodological note (§3.2), Lyapunov error-bound methodology (§3.6), new §4.3 "First GPU Training Results" documenting the saturation-fix before/after comparison.

### Blocked on GPU
- None — GPU access is unblocked and in active use on the `hci-student` machine.

### Not yet done (successor to the old "blocked on GPU" items)
- **Full ablation matrix** (`experiments/EXPERIMENT_PLAN.md` blocks A-I, headline H1-H4) — plan exists, CLI flags for new ablation axes (structure variants, diagonal-vs-Cholesky, activation swap, constraint mode) not yet implemented. Redirected this session in favor of Stage 2/3 integration work; resume once Milestone 2 is done or in parallel.
- **Liu et al. (2024) 2s-rollout metric** — required for the external comparison claim, not yet implemented (per-joint RMSE in Nm alone is not comparable to their rad²/rad metric).
- **Remaining J1-J4 transient-spike outliers** (p99.9 3-6 Nm, true max 26-65 Nm on ~0.09% of validation samples) — not blocking, but root cause (suspected: PD servo snapping to the first velocity target at each Fourier segment start) not yet confirmed or fixed. Revisit if time permits; currently worked around via the p99.9-not-max Lyapunov bound methodology.
- **Re-run one prior CPU smoke-test experiment** on the corrected URDF for a clean before/after comparison at matched settings (optional — the two real GPU runs already provide a clean before/after story for the saturation fix specifically).

### Blocked on real robot data
- Build real motor-babbling HDF5 dataset to enable `training/fine_tune.py` (Goal 4): `python -m training.fine_tune --checkpoint models/run_XXXX/greybox_best.pt --real_data data/real_motor_babbling.h5 --max_steps 100`
- N3-Djeumou (semi-supervised dissipativity): design and run ablation study.
- N2-WhenPhysics: re-run diagnostic on real data — real per-joint friction differences may trigger EMA balancing (ratio 1.0× on synthetic, may differ on hardware).

### Stage wiring (pending Stage 1 convergence / Milestone 2)
- ~~Resolve `TODO(stage3)` markers in `pinn_controller_node.py`~~ **DONE this session (2026-07-16, uncommitted)** — `ComputedTorquePDController` now wired in; see Stage 3 section. Remaining: exercise this wiring end-to-end via Milestone 2 (routing MoveIt2 trajectories through this node rather than the default `joint_trajectory_controller`).
- Resolve `TODO(stage4-arm-motion)` in `stage4/grasp_executor.py` (`_move_arm()`) — one step closer after Milestone 1, still blocked on Milestone 2.
- **Inference latency benchmark:** add a timing script to confirm sub-1 ms per forward pass (required to substantiate Goal 2 claim at 1000 Hz). Still not started; more relevant now that Stage 3 is actually wired into the control loop.

### Paper / write-up
- **Add Related Work citations** (PAPER_DRAFT.md Section 2):
  - Lutter et al. (ICLR 2019) — original Cholesky+Softplus-diagonal source; lineage anchor for FrictionNet design.
  - Lutter et al. (IROS 2019) — foundational DeLaN predecessor for energy-based control lineage.
  - Sutanto et al. (L4DC 2020) — DiffNEA; confirm RNEA-intact advantage and FrictionNet static-friction motivation.
  - Li et al. (2025) compliant PINN — DeLaN-FFNN independent validation.
  - Toscano et al. (2025) PIKANs survey — broad corroboration of grey-box + AL + frozen-backbone.
- **Dual payload-awareness competitive advantage:** document in paper that `_inject_payload()` in `rnea_wrapper.py` + delta conditioning of tau_res predates and exceeds Li et al. (2025) payload-ID and Li et al. (2025) compliant PINN single-pathway approaches.
- **Scope physics claims to in-distribution trajectories:** following Prabhakar et al. (ICLR 2026) negative result — do not claim temporal extrapolation without empirical evidence.
- **Physics-validator advisories to address in paper methodology section:** (1) per-sample vs. batch-mean dissipativity multiplier; (2) under-sampling risk for max_samples < 2000; (3) slower lambda_dissip growth with FrictionNet (intended — document in ablation).
- **Document the Stage 2 simplification decision:** using NVIDIA's official `isaac_moveit` MoveIt2 config instead of a hand-authored one — justify in the methodology section as a deliberate scope decision (CLAUDE.md "keep it simple") rather than an oversight.

### Future (optional)
- **Implement `controller/payload_identification.py`**: fill in the 3-step least-squares body (replace `raise NotImplementedError`). ~10 lines numpy. Requires Franka joint-torque sensor access (libfranka or ROS2 `/joint_states` effort field). Priority: before first real-robot deployment.
- 3 papers not yet obtained: s11433-025-2810-1, s41598-026-50630-y_reference, ssrn-6550385.
- Real motor-babbling HDF5 recording (needed for N3-Duong fine-tuning and N3-Djeumou ablation).
