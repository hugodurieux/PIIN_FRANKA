# Session State — PINN Franka Project
<!-- This file is updated automatically at the end of each session.
     Do not edit by hand. CLAUDE.md imports it at every startup. -->

## Last updated
2026-06-25 (evening)

## Papers processed
| Status | File | Relevance | Novelties kept |
|--------|------|-----------|----------------|
| Processed | Djeumou et al. (2022) - Neural Networks with Physics-Informed Architectures.md | 3 (High) | N1-Djeumou (REJECT — already in grey_box_net.py); N2-Djeumou (REJECT — already in constraints.py); N3-Djeumou (INVESTIGATE — semi-supervised constraints, serves Goal 4) |
| Processed | Liu et al. (2024) - Physics-Informed Neural Networks to Model and Control Robots.md | 3 (High — PRIMARY BASELINE) | N1-Liu (REJECT — RK4 rollout conflicts with RNEA); N2-Liu (INVESTIGATE — Cholesky FrictionNet, serves Goal 3); N3-Liu (KEEP — Lyapunov template, implemented in Stage 3, MERGED); N4-Liu (KEEP — --max_samples ablation, MERGED) |
| Processed | Djeumou et al. (2024) "One Model to Drift Them All" (CoRL vehicle drifting).md | 0 (None — vehicle drifting, no robot arm applicability) | N1-Djeumou-CoRL (REJECT — hierarchical rate decoupling, vehicle-specific, incompatible); N2-Djeumou-CoRL (REJECT — diffusion-based payload estimation, no implementation path) |
| Processed | Duong et al. (2024) Port-Hamiltonian Neural ODE Networks on Lie.md | 1 (Low-Medium — validates phys. structures) | N1-Duong (INVESTIGATE — Cholesky L L^T + eps*I algebraic kernel, fold into N2-Liu FrictionNet); N2-Duong (REJECT — duplicate of N1-Duong); N3-Duong (KEEP — IMPLEMENTED sim-to-real fine-tuning, branch novelty/duong2024-N3-simtoreal-finetune, pending merge) |
| Processed | Wang et al. (2024) Trajectory_Control_of_Multi-Axis_Robotic_Arms....md | 1 (Low-Medium — standard baseline) | N1-WangCAC (INVESTIGATE — Sobol sampling for excitation, revisit when data pipeline exists); N2-WangCAC (REJECT — trapezoidal residual, same conflict as N1-Liu); N3-WangCAC (REJECT — EKF, latency incompatible with 1 kHz control) |
| Processed | Wang et al. (2025) - Symplectic Physics-Embedded Learning (SPEL).md | 1 (Low-Medium — physics-driven design) | N1-SPEL (INVESTIGATE — sparsity mask on Cholesky friction matrix for revolute joints, fold into N2-Liu FrictionNet); N2-SPEL (REJECT — trainable URDF constants, violates RNEA-intact invariant); N3-SPEL (REJECT — KAN activations, violates Mish/Softplus constraint) |

## Novelties pipeline
| ID | Description | Supervisor verdict | Implementation status |
|----|-------------|-------------------|----------------------|
| N1-Djeumou | Compositional grey-box structure (known analytical terms + neural residual) | REJECT — already core architecture in grey_box_net.py | rejected |
| N2-Djeumou | Augmented Lagrangian training with Lagrange multiplier dual-ascent | REJECT — already implemented in constraints.py | rejected |
| N3-Djeumou | Semi-supervised constraint enforcement on unlabeled joint-space points to extend dissipativity guarantees | INVESTIGATE — ablation study needed once data exists | pending |
| N1-Liu | RK4 rollout loss (4th-order forward simulation residual in training loss) | REJECT — conflicts with RNEA grey-box architecture | rejected |
| N2-Liu | Cholesky dissipativity structural constraint (Softplus-diagonal Cholesky inside FrictionNet sub-module) | INVESTIGATE — feasibility study needed; synthesis with N1-Duong + N1-SPEL | pending |
| N3-Liu | Lyapunov stability template for Stage 3 controller (Kd = safety_margin * error_bound, Kp = Kd^2/4; DEFAULT_ERROR_BOUND = [5,5,5,5,2,2,2] Nm placeholder) | KEEP — IMPLEMENTED on branch stage3/computed-torque-pd-controller, MERGED to main | done |
| N4-Liu | --max_samples data-efficiency ablation flag (truncate training data to N random samples, seed=42, before train/val split) | KEEP — IMPLEMENTED on branch novelty/liu2024-N4-max-samples, MERGED to main | done |
| N1-Duong | Cholesky L L^T + eps*I algebraic kernel for parameterizing positive-definite dissipative matrices | INVESTIGATE — 28 lower-triangular entries, Softplus diagonal; fold into N2-Liu FrictionNet design | pending |
| N2-Duong | (duplicate of N1-Duong in port-Hamiltonian formulation) | REJECT — no new content beyond N1-Duong | rejected |
| N3-Duong | Sim-to-real fine-tuning via frozen-backbone learning: load GreyBoxNet checkpoint, freeze all but last 2 nn.Linear layers, fine-tune for --max_steps (default=100) under full PINN loss | KEEP — IMPLEMENTED on branch novelty/duong2024-N3-simtoreal-finetune, physics validator PASSED, PENDING HUMAN REVIEW/MERGE | in-progress |
| N1-WangCAC | Sobol sampling (low-discrepancy sequences) for excitation trajectory generation to improve coverage | INVESTIGATE — consider for data pipeline when Isaac Sim pipeline is built | pending |
| N2-WangCAC | Trapezoidal collocation loss (residual on acceleration from finite differences) | REJECT — same RK4 vs RNEA grey-box conflict as N1-Liu | rejected |
| N3-WangCAC | Extended Kalman Filter for state estimation under sensor latency | REJECT — latency > 1 ms incompatible with 1 kHz control rate | rejected |
| N1-SPEL | Physics-driven sparsity mask on Cholesky friction matrix: structurally-zero entries for revolute joints in 7x7 symmetric matrix | INVESTIGATE — fold into N2-Liu FrictionNet design; requires Pinocchio analytical pass on Franka URDF | pending |
| N2-SPEL | Trainable URDF constants (link masses, inertias, friction coefficients) in neural augmentation | REJECT — violates RNEA-intact white-box invariant in grey-box architecture | rejected |
| N3-SPEL | KAN (Kolmogorov-Arnold Networks) activations for physics-informed learning | REJECT — violates Mish/Softplus smoothness constraint from CLAUDE.md | rejected |

## Experiments logged
| Run ID | Date | Val loss | Notes |
|--------|------|----------|-------|
| N/A | N/A | N/A | No training runs executed yet; Stage 1 pipeline ready, awaiting GPU access |

## Current milestone
Stage 1 (PINN) — architecture finalized and all implemented novelties merged to main; Stages 2 and 3 scaffolded and merged; N3-Duong (sim-to-real fine-tuning) implemented and physics-validated, pending human review/merge; N2-Liu FrictionNet now requires synthesis of 3 investigation streams (N2-Liu, N1-Duong, N1-SPEL).

## Open questions / blockers
- **GPU access blocker:** Stage 1 training cannot execute without GPU. Waiting for GPU allocation.
- **Branch novelty/duong2024-N3-simtoreal-finetune pending human review and merge:** N3-Duong (sim-to-real fine-tuning) is ready; physics validator passed; implements Goal 4 (domain adaptation). Location: `training/fine_tune.py`. Advisory: freeze logic using `named_modules()` to identify "last 2 nn.Linear" is brittle if future architecture adds skip-connection Linear outside `self.net`.
- **N2-Liu FrictionNet synthesis:** Now has THREE investigation inputs to synthesize: (1) N2-Liu Cholesky dissipativity idea; (2) N1-Duong algebraic kernel L L^T + eps*I (28 lower-triangular entries, Softplus diagonal); (3) N1-SPEL revolute-joint sparsity mask (which entries of 7x7 friction matrix are structurally zero). Requires analytical Pinocchio pass on Franka URDF to determine sparsity before prototyping FrictionNet sub-module.
- N3-Djeumou (semi-supervised dissipativity): awaits first real motor-babbling HDF5 dataset to design and run ablation.
- N1-WangCAC (Sobol sampling): consider for the data pipeline when Isaac Sim HDF5 pipeline is built.
- Data pipeline: Isaac Sim excitation trajectories → HDF5 (q, qdot, qddot, delta, tau_real) not yet built; Fourier trajectory baseline available as fallback. Real motor-babbling dataset needed to run `training/fine_tune.py`.
- Physics validator advisories (non-blocking): (1) dissipativity multiplier currently batch-mean — consider per-sample multipliers if weak at runtime; (2) document under-sampling risk for max_samples < ~2000 in ablation study methodology; (3) Stage 3 DEFAULT_ERROR_BOUND = [5,5,5,5,2,2,2] Nm is placeholder — must recompute via `compute_lyapunov_gains(real_error_bound)` after Stage 1 validation.

## What to do next session
1. Human review and merge branch `novelty/duong2024-N3-simtoreal-finetune` (sim-to-real fine-tuning, Goal 4, physics-validated); address brittleness advisory on freeze logic in `training/fine_tune.py`.
2. Synthesize N2-Liu FrictionNet: perform analytical Pinocchio pass on Franka URDF to extract revolute-joint sparsity pattern; design FrictionNet sub-module integrating N2-Liu Cholesky idea, N1-Duong algebraic kernel (L L^T + eps*I), and N1-SPEL sparsity mask; prototype on synthetic data.
3. When GPU access is available: run Stage 1 training with `python -m training.train --synthetic --epochs 5` (smoke test), then real data training pipeline.
