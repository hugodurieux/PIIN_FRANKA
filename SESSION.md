# Session State — PINN Franka Project
<!-- This file is updated automatically at the end of each session.
     Do not edit by hand. CLAUDE.md imports it at every startup. -->

## Last updated
2026-06-26

## Papers processed
| Status | File | Relevance | Novelties kept |
|--------|------|-----------|----------------|
| Processed | Djeumou et al. (2022) - Neural Networks with Physics-Informed Architectures.md | 3 (High) | N1-Djeumou (REJECT — already in grey_box_net.py); N2-Djeumou (REJECT — already in constraints.py); N3-Djeumou (INVESTIGATE — semi-supervised constraints, serves Goal 4) |
| Processed | Liu et al. (2024) - Physics-Informed Neural Networks to Model and Control Robots.md | 3 (High — PRIMARY BASELINE) | N1-Liu (REJECT — RK4 rollout conflicts with RNEA); N2-Liu (KEEP — Cholesky diagonal FrictionNet, IMPLEMENTED and MERGED); N3-Liu (KEEP — Lyapunov template, implemented in Stage 3, MERGED); N4-Liu (KEEP — --max_samples ablation, MERGED) |
| Processed | Djeumou et al. (2024) "One Model to Drift Them All" (CoRL vehicle drifting).md | 0 (None — vehicle drifting, no robot arm applicability) | N1-Djeumou-CoRL (REJECT — hierarchical rate decoupling, vehicle-specific, incompatible); N2-Djeumou-CoRL (REJECT — diffusion-based payload estimation, no implementation path) |
| Processed | Duong et al. (2024) Port-Hamiltonian Neural ODE Networks on Lie.md | 1 (Low-Medium — validates phys. structures) | N1-Duong (INVESTIGATE — Cholesky L L^T + eps*I algebraic kernel, considered in N2-Liu FrictionNet design); N2-Duong (REJECT — duplicate of N1-Duong); N3-Duong (KEEP — IMPLEMENTED sim-to-real fine-tuning, MERGED to main, commit 0aa4fdc) |
| Processed | Wang et al. (2024) Trajectory_Control_of_Multi-Axis_Robotic_Arms....md | 1 (Low-Medium — standard baseline) | N1-WangCAC (INVESTIGATE — Sobol sampling for excitation, revisit when data pipeline exists); N2-WangCAC (REJECT — trapezoidal residual, same conflict as N1-Liu); N3-WangCAC (REJECT — EKF, latency incompatible with 1 kHz control) |
| Processed | Wang et al. (2025) - Symplectic Physics-Embedded Learning (SPEL).md | 1 (Low-Medium — physics-driven design) | N1-SPEL (INVESTIGATE — sparsity mask on Cholesky friction matrix for revolute joints, considered in N2-Liu FrictionNet design); N2-SPEL (REJECT — trainable URDF constants, violates RNEA-intact invariant); N3-SPEL (REJECT — KAN activations, violates Mish/Softplus constraint) |
| Processed | Deng et al. (2024) E2NN (Applied Soft Computing).md | 1 (Low-Medium) | N1-E2NN (REJECT — 1-DoF only, manual per-robot sub-term structure conflicts with Goal 1 automation); N2-E2NN (REJECT — recurrent Liquid gating + forbidden tanh/sigmoid activations) |
| Processed | Ni & Qureshi (2024) C-NTFields (ICRA 2024).md | 1 (Low-Medium) | N1-CMP (REJECT — custom Eikonal PDE planner incompatible with Stage 2 MoveIt2 mandate); N2-CMP (REJECT — planning-domain detail, no dynamics link) |
| Processed | Liu, Ni & Qureshi (2024) Active NTFields (IEEE T-RO/RA-L).md | 1 (Low-Medium) | N1-NTF (REJECT — incremental extension of C-NTFields, Stage 2 stays simple MoveIt2); N2-NTF (REJECT — uncertainty-weighted replanning, no dynamics link) |
| Processed | Jiang et al. (2025) PhysTwin (CVPR 2025).md | 0 (None — deformable bodies domain mismatch) | N/A (no applicable novelties) |
| Processed | Deng et al. (2023) SSRN preprint.md | 0 (Duplicate) | DUPLICATE of Deng et al. (2024); no new novelties |
| Processed | Fang et al. (2026) AdaKineNet (Robotics & Autonomous Systems).md | 0 (None — inverse kinematics, not dynamics) | N1-AdaKineNet (REJECT — inverse kinematics problem, dynamics-independent); N2-AdaKineNet (REJECT — ReLU forbidden, 10-DoF mobile manipulator domain mismatch) |
| Processed | Prabhakar et al. (2026) "When Does Physics Help?" (ICLR 2026).md | 1 (Low-Medium — negative result on temporal extrapolation) | N1-WhenPhysics (REJECT — soft contact dynamics (LuGre ODE), already in constraints.py); N2-WhenPhysics (INVESTIGATE — EMA per-residual loss balancing for 87/12 Nm torque scale imbalance, gated on first training run); N3-WhenPhysics (REJECT — duplicate of N3-Duong sim-to-real fine-tuning) |
| Processed | Feizi et al. (2025) Few-Shot PINN for Concentric-Tube Robots (arXiv 2605.12790).md | 0 (None — Cosserat rod BVP, surgical robot domain) | N/A (no applicable novelties) |

## Novelties pipeline
| ID | Description | Supervisor verdict | Implementation status |
|----|-------------|-------------------|----------------------|
| N1-Djeumou | Compositional grey-box structure (known analytical terms + neural residual) | REJECT — already core architecture in grey_box_net.py | rejected |
| N2-Djeumou | Augmented Lagrangian training with Lagrange multiplier dual-ascent | REJECT — already implemented in constraints.py | rejected |
| N3-Djeumou | Semi-supervised constraint enforcement on unlabeled joint-space points to extend dissipativity guarantees | INVESTIGATE — ablation study needed once data exists | pending |
| N1-Liu | RK4 rollout loss (4th-order forward simulation residual in training loss) | REJECT — conflicts with RNEA grey-box architecture | rejected |
| N2-Liu | Cholesky dissipativity structural constraint (diagonal FrictionNet sub-module with Softplus diagonal D parameterization, tau_friction = -D * qdot, 7 diagonal + 6 biases params) | KEEP — IMPLEMENTED on branch novelty/N2-Liu-frictionnet, physics validator PASSED, MERGED to main (commit ebc2ba3) | done |
| N3-Liu | Lyapunov stability template for Stage 3 controller (Kd = safety_margin * error_bound, Kp = Kd^2/4; DEFAULT_ERROR_BOUND = [5,5,5,5,2,2,2] Nm placeholder) | KEEP — IMPLEMENTED on branch stage3/computed-torque-pd-controller, MERGED to main | done |
| N4-Liu | --max_samples data-efficiency ablation flag (truncate training data to N random samples, seed=42, before train/val split) | KEEP — IMPLEMENTED on branch novelty/liu2024-N4-max-samples, MERGED to main | done |
| N1-Duong | Cholesky L L^T + eps*I algebraic kernel for parameterizing positive-definite dissipative matrices | INVESTIGATE — 28 lower-triangular entries, Softplus diagonal; considered and rejected in favor of diagonal D for N2-Liu (Franka serial-chain independent motors justify sparsity) | pending |
| N2-Duong | (duplicate of N1-Duong in port-Hamiltonian formulation) | REJECT — no new content beyond N1-Duong | rejected |
| N3-Duong | Sim-to-real fine-tuning via frozen-backbone learning: load GreyBoxNet checkpoint, freeze all but last 2 nn.Linear layers, fine-tune for --max_steps (default=100) under full PINN loss | KEEP — IMPLEMENTED on branch novelty/duong2024-N3-simtoreal-finetune, physics validator PASSED, MERGED to main (commit 0aa4fdc) | done |
| N1-WangCAC | Sobol sampling (low-discrepancy sequences) for excitation trajectory generation to improve coverage | INVESTIGATE — consider for data pipeline when Isaac Sim pipeline is built | pending |
| N2-WangCAC | Trapezoidal collocation loss (residual on acceleration from finite differences) | REJECT — same RK4 vs RNEA grey-box conflict as N1-Liu | rejected |
| N3-WangCAC | Extended Kalman Filter for state estimation under sensor latency | REJECT — latency > 1 ms incompatible with 1 kHz control rate | rejected |
| N1-SPEL | Physics-driven sparsity mask on Cholesky friction matrix: structurally-zero entries for revolute joints in 7x7 symmetric matrix | INVESTIGATE — considered and rejected in favor of diagonal D for N2-Liu FrictionNet; Pinocchio pass deferred | pending |
| N2-SPEL | Trainable URDF constants (link masses, inertias, friction coefficients) in neural augmentation | REJECT — violates RNEA-intact white-box invariant in grey-box architecture | rejected |
| N3-SPEL | KAN (Kolmogorov-Arnold Networks) activations for physics-informed learning | REJECT — violates Mish/Softplus smoothness constraint from CLAUDE.md | rejected |
| N1-E2NN | Structural sub-term embedding (Deng et al. 2024): explicitly decompose inverse dynamics into inertia, Coriolis, gravity terms per-joint | REJECT — E2NN validated on 1-DoF only; manual per-robot sub-term derivation conflicts with Goal 1 automation | rejected |
| N2-E2NN | Liquid gating mechanism (recurrent hidden state modulation) | REJECT — recurrent incompatible with stateless 1 kHz control; tanh/sigmoid forbidden activations | rejected |
| N1-CMP | Eikonal PDE planner on constraint manifold (C-NTFields, Ni & Qureshi 2024) | REJECT — custom planner incompatible with Stage 2 MoveIt2 mandate in CLAUDE.md | rejected |
| N2-CMP | Negative-exponential speed model in Eikonal solver | REJECT — planning-domain detail, no link to dynamics loss | rejected |
| N1-NTF | Active sensing in Eikonal planner (Liu, Ni & Qureshi 2024) | REJECT — incremental extension of C-NTFields; Stage 2 uses standard MoveIt2 | rejected |
| N2-NTF | Uncertainty-weighted replanning in active NTFields | REJECT — no link to dynamics loss | rejected |
| N1-AdaKineNet | Adaptive kinematic network with attention mechanism for inverse kinematics (Fang et al. 2026) | REJECT — inverse kinematics problem; dynamics-independent of torque learning | rejected |
| N2-AdaKineNet | ReLU-based deep IK architecture on 10-DoF mobile manipulator | REJECT — ReLU forbidden; mobile manipulator domain incompatible with fixed Franka 7-DoF | rejected |
| N1-WhenPhysics | Soft contact dynamics via LuGre friction ODE for prediction accuracy on unknown payloads | REJECT — equivalent to τ_friction in constraints.py augmented Lagrangian | rejected |
| N2-WhenPhysics | EMA loss balancing (β=0.95) per residual magnitude to mitigate 87/12 Nm torque scale imbalance across joints | INVESTIGATE — diagnostic: after first synthetic training run, if outer joints (5-7, 12 Nm) show higher val MSE than inner joints (1-4, 87 Nm), implement in training/train.py | pending |
| N3-WhenPhysics | Physics-aware trajectory sampling for sim-to-real transfer (Prabhakar et al. 2026) | REJECT — duplicate of N3-Duong 100-step frozen-backbone fine-tuning | rejected |

## Experiments logged
| Run ID | Date | Val loss | Notes |
|--------|------|----------|-------|
| smoke-baseline | 2026-06-26 | 44.10 (mse 0.87) | `--synthetic --epochs 5`, no FrictionNet. MSE 3.41→0.87, dissip_viol=0. Saved: models/run_20260626_104119/ |
| smoke-frictionnet | 2026-06-26 | 44.01 (mse 0.83) | `--synthetic --epochs 5 --use_friction_net`. D_diag converged to ~1.0-1.3 (joint 1 highest, physically plausible). dissip_viol=0. Saved: models/run_20260626_104318/ |

## Current milestone
Stage 1 (PINN) — pipeline fully operational. 15 papers processed. All KEEP novelties (N2-Liu FrictionNet, N3-Liu Lyapunov gains, N4-Liu max_samples, N3-Duong sim-to-real fine-tuning) implemented and merged to main. Smoke tests passed on 2026-06-26: baseline and FrictionNet both train correctly on synthetic data in WSL (Ubuntu 24.04). Pinocchio 4.0.0 confirmed working. Awaiting GPU access and real dataset for full training run.

## Open questions / blockers
- **GPU access blocker:** Stage 1 training cannot execute at scale without GPU. Waiting for GPU allocation.
- **Pinocchio — RESOLVED:** Installed via `pip3 install pin --break-system-packages` in WSL Ubuntu 24.04. Version 4.0.0. Run all training commands from WSL: `cd "/mnt/c/Users/Hugo Durieux/Desktop/Stage 3A/LESTAGE/pinn_franka" && python3 -m training.train ...`
- **N2-WhenPhysics diagnostic:** Smoke tests do not expose per-joint val MSE. After first real training run, inspect per-joint val MSE comparing joints 5-7 (12 Nm limit) vs. joints 1-4 (87 Nm limit). If outer joints show elevated error relative to torque budget, implement EMA loss balancing (beta=0.95) in training/train.py.
- N3-Djeumou (semi-supervised dissipativity): awaits first real motor-babbling HDF5 dataset to design and run ablation.
- N1-WangCAC (Sobol sampling): consider for the data pipeline when Isaac Sim HDF5 pipeline is built.
- Data pipeline: Isaac Sim excitation trajectories → HDF5 (q, qdot, qddot, delta, tau_real) not yet built; Fourier trajectory baseline available as fallback. Real motor-babbling dataset needed to run `training/fine_tune.py`.
- Physics validator advisories (non-blocking): (1) dissipativity multiplier currently batch-mean — consider per-sample multipliers if weak at runtime; (2) document under-sampling risk for max_samples < ~2000 in ablation study methodology; (3) Stage 3 DEFAULT_ERROR_BOUND = [5,5,5,5,2,2,2] Nm is placeholder — must recompute via `compute_lyapunov_gains(real_error_bound)` after Stage 1 validation; (4) N3-Duong freeze logic via `named_modules()` — document assumption if future architecture changes; (5) N2-Liu FrictionNet lambda_dissip grows slower when active (intended).
- **papers/inbox/ workflow improved:** /process-papers now renames archived papers to "MAIN_CONTRIBUTOR et al. (YEAR) TITLE.md" format and skips duplicates by checking if (first_author, year) already exists in papers_review.csv. Reduces manual file cleanup.

## What to do next session
1. **GPU + real dataset:** run full Stage 1 training on real dataset (q, qdot, qddot, delta, tau_real) from WSL. Extract per-joint validation RMSE.
2. **Lyapunov gains:** call `compute_lyapunov_gains(real_error_bound)` with real RMSE values, update DEFAULT_ERROR_BOUND in Stage 3 controller (currently placeholder [5,5,5,5,2,2,2] Nm).
3. **N2-WhenPhysics diagnostic:** inspect outer-joint (5-7, 12 Nm) vs inner-joint (1-4, 87 Nm) val MSE after real training run. If imbalanced, implement EMA loss balancing (beta=0.95) in training/train.py.
4. **Data pipeline:** build Isaac Sim excitation trajectory → HDF5 pipeline. Consider Sobol sampling (N1-WangCAC) at this stage.
