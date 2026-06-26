# Project State — PINN Franka Pipeline
_Last updated: 2026-06-26_

## 1. Objectives (from goal.md)
| # | Objective | Status | Evidence / where proven |
|---|-----------|--------|-------------------------|
| 1 | Automated "URDF-to-Model" Pipeline — accept any URDF, auto-extract kinematics via Pinocchio, generate network, produce trained dynamic model | in progress | `pinocchio_baseline/rnea_wrapper.py` (URDF -> RNEA); `network/grey_box_net.py` + `training/train.py` (architecture + training loop). N4 data-efficiency ablation flag (`--max_samples`) merged. Fourier dataset built (`generate_fourier_dataset.py`): 3 × ~50k samples, payloads 0/1/3 kg, real Pinocchio RNEA (cmeel example-robot-data), Sobol segments (N1-WangCAC). Training runs validated on CPU (val RMSE ≈ 0.22 Nm in 20 epochs). Multi-payload training not yet built. Full convergence needs GPU. |
| 2 | High-Frequency Real-Time Control at 1000 Hz (MPC integration, microsecond inference) | in progress | Stage 2: ROS2 Humble node on `stage2/moveit2-ros2-humble` publishes effort commands at 1000 Hz with MoveIt2 trajectory bridge. Stage 3: `ComputedTorquePDController.step()` on `stage3/computed-torque-pd-controller` is the 1 kHz torque computation kernel. Both scaffolded; wiring pending trained Stage 1 model. |
| 3 | Scaling to 7-DoF — Augmented Lagrangian constraints + residual friction on a full Franka Panda | in progress | `training/constraints.py` implements AL penalties (torque limits + dissipativity) for all 7 joints. Stage 3 hard-clips to per-joint TORQUE_LIMITS. N2-Liu FrictionNet IMPLEMENTED (`network/friction_net.py`): structural dissipativity guarantee via Softplus-diagonal D matrix; hard guarantee `tau_friction · qdot <= 0` always; 6,087 params; physics PASSED. No training run yet. |
| 4 | Standardized Sim-to-Real Gap resolution via physics-constrained fine-tuning | in progress | `training/fine_tune.py` on branch `novelty/duong2024-N3-simtoreal-finetune` — PASSED physics validation. Loads pre-trained GreyBoxNet, freezes all layers except last 2 nn.Linear modules, fine-tunes under full PINN loss (MSE + AL). First code implementation of Goal 4. Real data pipeline (HDF5) not yet built. |

## 2. Pipeline architecture (URDF -> trained robot)

tau_pred = RNEA(q, qdot, qddot; URDF + delta) + GreyBoxNet([sin(q), cos(q), qdot, delta]) + FrictionNet([sin(q), cos(q), qdot, delta])
Loss     = MSE(tau_pred, tau_real) + AugmentedLagrangian(torque_limits, dissipativity)

FrictionNet is optional (--use_friction_net flag). When active, its structural guarantee absorbs part of the dissipativity constraint, so the AL lambda_dissip multiplier grows more slowly — intended and correct.

### Stage 1 — PINN dynamics learning
Fully architected and pipeline validated. 5 training runs completed (CPU, 20 epochs). Fourier dataset operational. GPU needed for full convergence.

- White-box RNEA: `pinocchio_baseline/rnea_wrapper.py` — wraps `pinocchio.rnea`, handles payload injection into end-effector inertia, runs offline only.
- Residual network: `network/grey_box_net.py` — MLP (default 4x256, Mish), input X in R^22 = [sin(q), cos(q), qdot, delta], output tau_res in R^7. ReLU forbidden.
- FrictionNet: `network/friction_net.py` — 2-layer Mish MLP (22->64->64->7), output D_diag = Softplus(d) + 1e-6, tau_friction = -D_diag * qdot. Structural guarantee: tau_friction · qdot = -sum(Softplus(d_i)*qdot_i^2) <= 0 always. 6,087 parameters. Exposes `forward(q, qdot, delta) -> tau_friction` and `forward_D(q, qdot, delta) -> D_diag`. (N2-Liu, synthesising N1-Duong + N1-SPEL)
- Physics constraints: `training/constraints.py` — `AugmentedLagrangian` class; enforces |tau_pred| <= TORQUE_LIMITS and tau_res · qdot <= 0 (dissipativity) with dual-ascent multiplier updates.
- Training loop: `training/train.py` — Adam optimizer, 90/10 train/val split, CSV logging, best-checkpoint save. Supports `--synthetic` (no Pinocchio needed) and real HDF5 datasets. Accepts `--max_samples N` (N4) and `--use_friction_net` (N2-Liu); when friction net active, logs D_diag mean per joint per epoch and saves `friction_net_best.pt` alongside `greybox_best.pt`.
- Sim-to-real fine-tuning: `training/fine_tune.py` — loads pre-trained checkpoint, freezes all layers except last 2 nn.Linear modules (4th hidden layer + output layer), fine-tunes for `--max_steps` gradient steps (default=100) under full PINN loss. Saves `greybox_finetuned.pt`. (N3-Duong)
- Dataset: `training/dataset.py` — `_random_subsample_indices()` helper; both `FrankaDynamicsDataset` and `SyntheticDataset` accept `max_samples` param (seed=42, before train/val split).
- Constants: `network/constants.py` — single source of truth for joint limits, velocity limits, input/output dims, payload values, `FRICTION_NET_HIDDEN = 64`.

Data pipeline: Fourier baseline BUILT (`generate_fourier_dataset.py`) — real Pinocchio RNEA, Sobol segments, 3 × ~50k samples (0/1/3 kg payloads). Isaac Sim integration not yet built.

### Stage 2 — Motion planning (MoveIt2 / ROS2)
Scaffolded on branch `stage2/moveit2-ros2-humble` — PHYSICS PASSED (after fix). Awaiting merge and Stage 1 trained model.

- `ros2_ws/src/pinn_franka_controller/` — full ROS2 Humble package.
- `pinn_controller_node.py`: subscribes to `/franka/joint_states` and `/pinn_controller/desired_trajectory`; publishes to `/franka/effort_joint_trajectory_controller/commands` at 1000 Hz; zero-torque safe fallback; TORQUE_LIMITS clamp at publish boundary.
- `trajectory_interpolator.py`: linear interpolation of (q_des, qdot_des, qddot_des) from JointTrajectory messages.
- `launch/pinn_controller.launch.py` and `config/controller_params.yaml`.
- Integration point: `TODO(stage3)` marker in `_compute_torques()` and `_try_load_controller()` — Stage 3 `ComputedTorquePDController` plugs in here once that branch is merged.

### Stage 3 — Controller + integration
Scaffolded on branch `stage3/computed-torque-pd-controller` — PHYSICS PASSED. Awaiting merge and Stage 1 trained model.

- `controller/model_loader.py`: loads `GreyBoxNet` checkpoint from `.pt` + `config.json`.
- `controller/lyapunov_gains.py`: N3-Liu — computes `Kd = safety_margin * error_bound`, `Kp = Kd^2 / 4` (critical damping). `DEFAULT_ERROR_BOUND = [5,5,5,5,2,2,2]` Nm is a placeholder until real validation data from Stage 1 is available.
- `controller/computed_torque_pd.py`: `ComputedTorquePDController.step()` — `tau = RNEA(q, qdot, qddot_des) + tau_res(q, qdot, delta) + Kp*(q_des - q) + Kd*(qdot_des - qdot)`, hard-clipped to TORQUE_LIMITS; all I/O numpy; `torch.no_grad()` for inference.
- Wiring dependency: Stage 2's `TODO(stage3)` must be resolved after this branch is merged into main.

### Stage 4 — Grabbing (optional)
Not started.

## 3. Implemented novelties
| ID | From paper | Description | Goal served | Branch | Validated | Merged |
|----|-----------|-------------|-------------|--------|-----------|--------|
| N1-Djeumou | Djeumou et al. (2022) | Compositional grey-box structure: known analytical terms (RNEA) composed with neural residual. REJECT — already fully implemented as the project's core architecture in `grey_box_net.py`. Architecture corroborated by peer-reviewed paper. | Goal 1, Goal 3 | main | architecture match confirmed | n/a (pre-existing) |
| N2-Djeumou | Djeumou et al. (2022) | Augmented Lagrangian training with Lagrange multiplier dual-ascent for hard physics constraints. REJECT — already fully implemented in `constraints.py`. | Goal 3 | main | architecture match confirmed | n/a (pre-existing) |
| N3-Djeumou | Djeumou et al. (2022) | Semi-supervised constraint enforcement on unlabeled joint-space points to extend dissipativity guarantees beyond training trajectories. INVESTIGATE — ablation study needed. | Goal 3, Goal 4 | not started | not validated | not merged |
| N1-Liu | Liu et al. (2024) | RK4 rollout loss — augment the training loss with a 4th-order Runge-Kutta forward simulation residual. REJECT — conflicts with RNEA grey-box architecture; would destroy primary novelty. | — | rejected | — | — |
| N2-Liu | Liu et al. (2024) | Cholesky dissipativity structural constraint — FrictionNet sub-module with Softplus-diagonal D matrix; tau_friction = -D_diag * qdot; hard structural guarantee tau_friction · qdot <= 0 always. Synthesises N2-Liu (Cholesky concept) + N1-Duong (L L^T algebraic kernel, diagonal case) + N1-SPEL (revolute-joint sparsity: diagonal D, not full 28-entry Cholesky). KEEP — IMPLEMENTED in `network/friction_net.py`; `--use_friction_net` flag in `training/train.py`; logs D_diag mean per joint; saves `friction_net_best.pt`. 6,087 parameters. Physics validator advisory: lambda_dissip grows more slowly when active (intended). | Goal 3 | `novelty/N2-Liu-frictionnet` | PASSED (physics validator) | awaiting human review |
| N3-Liu | Liu et al. (2024) | Lyapunov stability template for Stage 3 controller — `Kd = safety_margin * error_bound`, `Kp = Kd^2/4` (critical damping), `DEFAULT_ERROR_BOUND = [5,5,5,5,2,2,2]` Nm placeholder. KEEP — implemented in `controller/lyapunov_gains.py`. DEFAULT_KP/DEFAULT_KD are placeholders; call `compute_lyapunov_gains(real_error_bound)` after Stage 1 training. | Goal 2 | `stage3/computed-torque-pd-controller` | PASSED (physics validator) | awaiting human review |
| N4-Liu | Liu et al. (2024) | `--max_samples` data-efficiency ablation flag — truncate training data to N random samples (seed=42, before train/val split) to quantify how few samples are needed vs. Liu's 25k-sample benchmark. KEEP — implemented. | Goal 1 | `novelty/liu2024-N4-max-samples` | PASSED (physics validator, non-blocking advisories) | awaiting human review |
| N1-Duong | Duong et al. (2024) | Cholesky-factored inverse mass sub-network — L L^T + eps*I algebraic trick (28 lower-triangular entries for 7x7 matrix, Softplus on diagonal) guarantees positive-definiteness. INVESTIGATE — algebraic input to N2-Liu FrictionNet design (diagonal case used). Folds into N2-Liu; implemented there. | Goal 3 | folds into N2-Liu | folded into N2-Liu PASSED | not separate |
| N2-Duong | Duong et al. (2024) | Separate dissipation sub-network. REJECT — duplicate of N1-Duong's algebraic core; no independent contribution beyond what N1-Duong and N2-Liu already capture. | — | rejected | — | — |
| N3-Duong | Duong et al. (2024) | 100-step payload fine-tuning protocol — freeze all layers except last 2 nn.Linear modules (4th hidden layer + output layer), fine-tune for `--max_steps` steps (default 100, range 50–200) under full PINN loss (MSE + AL), lr=1e-4 to limit catastrophic forgetting. KEEP — IMPLEMENTED in `training/fine_tune.py`. First code realisation of Goal 4. | Goal 4 | `novelty/duong2024-N3-simtoreal-finetune` | PASSED (physics validator) | awaiting human review |
| N1-WangCAC | Wang et al. (CAC 2024) | Sobol quasi-random data sampling — 10 Sobol-sampled q_center configurations per payload in `generate_fourier_dataset.py`; scipy.stats.qmc.Sobol, 7-D joint space, scrambled, per-payload seed. IMPLEMENTED — validated 2026-06-26. | Goal 1 | main | confirmed working | merged (in generate_fourier_dataset.py) |
| N2-WangCAC | Wang et al. (CAC 2024) | Trapezoidal physics residual in PINN loss — time-discretised integration of dynamics residual at 20 Hz. REJECT — conflicts with RNEA offline-qddot path (same fundamental problem as N1-Liu); 20 Hz discretisation incompatible with 1 kHz target. | — | rejected | — | — |
| N3-WangCAC | Wang et al. (CAC 2024) | EKF noise filter at PINN-NMPC interface — Extended Kalman Filter to denoise joint state estimates before feeding the PINN. REJECT — matrix inversion per control step is incompatible with sub-ms 1 kHz loop latency requirement. | — | rejected | — | — |
| N1-SPEL | Wang et al. (Scientific Reports 2025) | Physics-driven sparsity masks on friction matrix — CONFIRMED 2026-06-26 via `pinocchio_baseline/friction_sparsity_analysis.py`: all 7 Franka joints are JointModelRZ (independent revolute), URDF friction/damping all zero, 80% parameter reduction (7 vs 28 params). Diagonal D physically justified. Folds into N2-Liu FrictionNet. | Goal 3 | folds into N2-Liu | CONFIRMED via Pinocchio analysis | not separate |
| N2-SPEL | Wang et al. (Scientific Reports 2025) | URDF inertia constants as trainable scalar parameters — make Pinocchio URDF link inertias learnable during training. REJECT — violates RNEA-intact invariant; making them learnable weakens the white-box guarantee that is central to Goal 1. | — | rejected | — | — |
| N3-SPEL | Wang et al. (Scientific Reports 2025) | KAN (Kolmogorov-Arnold Network) activations replacing MLP layers. REJECT — violates Mish/Softplus-only activation constraint; also demonstrates 14% overfitting on real hardware data. | — | rejected | — | — |
| N1-E2NN | Deng et al. (Applied Soft Computing 2024) | Structural sub-term embedding — explicitly decompose inverse dynamics into inertia, Coriolis, gravity terms, each with a dedicated sub-network, per-joint. REJECT — E2NN validated on a single 1-DoF joint only; manual per-robot derivation of sub-term structure conflicts directly with Goal 1 (automated URDF-to-model pipeline). | — | rejected | — | — |
| N2-E2NN | Deng et al. (Applied Soft Computing 2024) | Liquid gating mechanism — recurrent hidden state modulates sub-network activations via tanh/sigmoid gates. REJECT — (1) recurrent state is incompatible with the stateless 1 kHz control loop; (2) tanh and sigmoid activations violate the Mish/Softplus-only constraint. | — | rejected | — | — |
| N1-CMP | Ni & Qureshi (ICRA 2024) | Eikonal PDE planner (C-NTFields) — solve the Eikonal equation on a constraint manifold to produce smooth planning-space cost fields. REJECT — CLAUDE.md mandates simple MoveIt2 for Stage 2; a custom PDE-based planner replaces rather than extends MoveIt2 and is out of scope. | — | rejected | — | — |
| N2-CMP | Ni & Qureshi (ICRA 2024) | Negative-exponential speed model inside the Eikonal solver. REJECT — planning-domain detail that has no link to the dynamics loss or Stage 1 architecture. | — | rejected | — | — |
| N1-NTF | Liu, Ni & Qureshi (IEEE T-RO/RA-L 2024) | Active NTFields extension — active sensing integrated into Eikonal planner for unknown environments. REJECT — same reasons as N1-CMP; incremental extension of C-NTFields, Stage 2 uses standard MoveIt2. | — | rejected | — | — |
| N2-NTF | Liu, Ni & Qureshi (IEEE T-RO/RA-L 2024) | Uncertainty-weighted replanning in active NTFields. REJECT — same reasons as N2-CMP; no link to dynamics loss. | — | rejected | — | — |
| N1-AdaKineNet | Fang et al. (2026) | Adaptive loss weighting (per-term scale factors adjusted during training) for multi-term IK loss balancing. REJECT — project's augmented Lagrangian dual-ascent in `training/constraints.py` already handles multi-term loss balancing; also paper domain is inverse kinematics (not dynamics) on a 10-DoF mobile platform with ReLU activations — full domain mismatch. | — | rejected | — | — |
| N2-AdaKineNet | Fang et al. (2026) | Jacobian consistency loss — auxiliary loss penalising deviation between the network Jacobian and the analytical kinematic Jacobian. REJECT — RNEA white-box term already encodes all kinematic structure analytically in grey-box architecture; redundant and domain-mismatched (kinematics vs. dynamics). | — | rejected | — | — |
| N1-WhenPhysics | Prabhakar et al. (ICLR 2026) | Equality/inequality constraint scheduling — annealing the strength of physics constraints over training epochs. REJECT — already the exact structure in `training/constraints.py` (dual-ascent augmented Lagrangian). | — | rejected | — | — |
| N2-WhenPhysics | Prabhakar et al. (ICLR 2026) | EMA momentum-smoothed per-residual loss balancing (beta=0.95). INVESTIGATE — per-joint val RMSE diagnostic LIVE in `training/train.py` (printed at end of every run). Fourier baseline result 2026-06-26: ratio 1.0× (joints 1-4: 0.239 Nm, 5-7: 0.247 Nm) — no imbalance on synthetic residual. Revisit after real robot recordings. | Goal 3 | diagnostic in main | confirmed no imbalance on Fourier data | diagnostic merged |
| N3-WhenPhysics | Prabhakar et al. (ICLR 2026) | UDE frozen-backbone fine-tuning — Universal Differential Equation approach with frozen physics backbone. REJECT — duplicate of N3-Duong already implemented in `training/fine_tune.py`. | — | rejected | — | — |
| N1-Feizi | Feizi et al. (arXiv 2025) | Few-shot PINN adaptation for Cosserat rod BVP (continuum surgical robot shape reconstruction). REJECT — full domain mismatch: Cosserat rod PDE, tanh activations, no torques, no URDF, no rigid-body chain; zero applicability to Franka 7-DoF inverse dynamics. | — | rejected | — | — |

## 3a. Primary baseline — Liu et al. (2024) competitive gaps
Liu et al. (2024): "Physics-Informed Neural Networks to Model and Control Robots:
A Theoretical and Experimental Investigation" — the primary state-of-the-art reference.

| # | Gap in Liu et al. | This project's answer |
|---|-------------------|----------------------|
| 1 | No URDF-to-model automation — equations manually derived per robot | Goal 1: fully automated URDF -> Pinocchio -> network pipeline |
| 2 | Control at 500 Hz only, no MPC integration | Goal 2: targets 1000 Hz; Stage 2 ROS2 node + Stage 3 controller scaffolded |
| 3 | No payload conditioning | Payload delta in R^1 baked into every network input ([sin(q), cos(q), qdot, delta]); tested at 0 / 1 / 3 kg |
| 4 | No sim-to-real transfer protocol | Goal 4: 2-step pre-train (sim) + fine-tune (real motor-babbling) under PINN loss; `training/fine_tune.py` implements this (N3-Duong) |
| 5 | No torque / velocity limits in loss | AL constraints enforce torque limits and dissipativity for all 7 joints; Stage 3 hard-clips at publish boundary |
| 6 | Full black-box Lagrangian — no RNEA white-box term | Grey-box: RNEA white-box + learned residual; RNEA baseline never modified |

## 3b. Physics validator advisories (non-blocking)
1. N4 branch — dissipativity multiplier is batch-mean (pre-existing, not introduced by N4 branch) — consider per-sample multipliers if enforcement is weak at runtime.
2. N4 branch — at very small max_samples (< ~2000 from a 25k dataset), random draw may under-sample high-velocity excitation regions — document this in ablation study.
3. N3-Liu (Stage 3) — DEFAULT_KP/DEFAULT_KD are placeholders computed from `DEFAULT_ERROR_BOUND = [5,5,5,5,2,2,2]` Nm. Gains must be recomputed via `compute_lyapunov_gains(real_error_bound)` once Stage 1 produces validation error statistics.
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
|   |-- __init__.py
|
|-- controller/                      [branch: stage3/computed-torque-pd-controller]
|   |-- __init__.py
|   |-- model_loader.py              Loads GreyBoxNet checkpoint from .pt + config.json
|   |-- lyapunov_gains.py            N3-Liu: Kd = safety_margin*error_bound, Kp = Kd^2/4
|   |-- computed_torque_pd.py        ComputedTorquePDController.step(); 1 kHz torque kernel
|
|-- ros2_ws/                         [branch: stage2/moveit2-ros2-humble]
|   |-- src/pinn_franka_controller/
|       |-- pinn_controller_node.py  ROS2 node: 1000 Hz effort publisher; TODO(stage3) hook
|       |-- trajectory_interpolator.py  Linear interp of (q_des, qdot_des, qddot_des)
|       |-- launch/
|       |   |-- pinn_controller.launch.py
|       |-- config/
|           |-- controller_params.yaml
|
|-- tracking/
|   |-- PROJECT_STATE.md             This file
|   |-- papers_review.csv            One row per paper processed
|
|-- papers/
|   |-- inbox/                       Drop new papers here for /process-papers
|   |   |-- (empty — all reviewed papers moved to processed/)
|   |-- processed/
|       |-- Liu et al. (2024)...     (primary baseline, see section 3a)
|       |-- Djeumou et al. (2022)... (processed)
|       |-- Duong et al. (2024)...   (processed)
|       |-- Wang et al. (CAC 2024)   (processed — Trajectory Control / NMPC)
|       |-- Wang et al. (2025)...    (processed — SPEL)
|       |-- Deng et al. (2024)...    (processed — E2NN, Applied Soft Computing; all REJECTed)
|       |-- Ni & Qureshi (2024)...   (processed — C-NTFields, ICRA 2024; all REJECTed)
|       |-- Liu Ni Qureshi (2024)... (processed — Active NTFields, IEEE T-RO/RA-L; all REJECTed)
|       |-- Jiang et al. (2025)...   (processed — PhysTwin CVPR 2025; relevance 0, no novelties)
|       |-- Deng et al. (2023)...    (DUPLICATE of Deng et al. 2024 SSRN preprint; no novelties)
|       |-- Fang et al. (2026)...    (processed — AdaKineNet, Robotics & Autonomous Systems; relevance 0, all REJECTed)
|       |-- Prabhakar et al. (2026). (processed — "When Does Physics Help?", ICLR 2026; relevance 1; N2-WhenPhysics INVESTIGATE)
|       |-- Feizi et al. (2025)...   (processed — Few-shot PINN for CTR shape, arXiv 2605.12790; relevance 0, all REJECTed)
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
- Human review and merge of `novelty/N2-Liu-frictionnet` into main (FrictionNet structural dissipativity guarantee, physics PASSED). Test command: `python -m training.train --synthetic --epochs 5 --use_friction_net`
- Human review and merge of `novelty/duong2024-N3-simtoreal-finetune` into main (Goal 4 fine-tuning, physics PASSED).
- Human review and merge of `novelty/liu2024-N4-max-samples` into main.
- Human review and merge of `stage3/computed-torque-pd-controller` into main.
- Human review and merge of `stage2/moveit2-ros2-humble` into main (merge Stage 3 first — Stage 2 depends on it via `TODO(stage3)` hook).
- After Stage 3 merge: resolve `TODO(stage3)` markers in `pinn_controller_node.py` (`_compute_torques()` and `_try_load_controller()`) to wire in `ComputedTorquePDController`.
- After Stage 1 first training run: recompute Lyapunov gains via `controller/lyapunov_gains.py::compute_lyapunov_gains(real_error_bound)` using real validation error statistics; replace `DEFAULT_ERROR_BOUND` placeholder.
- **Multi-payload training:** adapt `training/dataset.py` to concatenate all 3 HDF5 files — train on payloads 0/1/3 kg simultaneously to prove payload-conditioned generalisation (Goal 1).
- **GPU + full convergence:** run `python3 -m training.train --data data/fourier_baseline_0kg.h5 --epochs 200 --use_friction_net` for a properly converged model; extract per-joint RMSE for Lyapunov gain update.
- **Lyapunov gains:** update `DEFAULT_ERROR_BOUND` in `controller/lyapunov_gains.py` from real per-joint RMSE after convergence run.
- **Inference latency benchmark:** add a timing script to prove microsecond inference at 1000 Hz (needed for Goal 2 claim).
- N3-Djeumou (semi-supervised dissipativity): design and run ablation study; needs real motor-babbling dataset.
- N2-WhenPhysics: re-run diagnostic after real robot recordings — real per-joint friction differences may trigger EMA balancing.
- Build real motor-babbling HDF5 dataset to enable `training/fine_tune.py` (command: `python -m training.fine_tune --checkpoint models/run_XXXX/greybox_best.pt --real_data data/real_motor_babbling.h5 --max_steps 100`).
- Build Isaac Sim integration for higher-fidelity pre-training data.
- Address physics-validator advisory 1: evaluate per-sample vs. batch-mean dissipativity multiplier enforcement.
- Address physics-validator advisory 2: document under-sampling risk for max_samples < 2000 in ablation study methodology.
- Address physics-validator advisory 4 (N3-Duong): document freeze-logic assumption (last 2 nn.Linear via `named_modules()`) if architecture gains skip-connection Linear layers outside `self.net`.
- Address physics-validator advisory 5 (N2-Liu): document slower lambda_dissip growth when `--use_friction_net` active; include in ablation comparison.
- Address physics-validator advisory 6 (Prabhakar 2026 negative result): scope project claims to in-distribution trajectory following; do not claim temporal extrapolation without empirical evidence.
