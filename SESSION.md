# Session State — PINN Franka Project
<!-- This file is updated automatically at the end of each session.
     Do not edit by hand. CLAUDE.md imports it at every startup. -->

## Last updated
2026-06-25 (evening)

## Papers processed
| Status | File | Relevance | Novelties kept |
|--------|------|-----------|----------------|
| Processed | Djeumou et al. (2022) - Neural Networks with Physics-Informed Architectures.md | 3 (High) | N1-Djeumou (REJECT — already in grey_box_net.py); N2-Djeumou (REJECT — already in constraints.py); N3-Djeumou (INVESTIGATE — semi-supervised constraints, serves Goal 4) |
| Processed | Liu et al. (2024) - Physics-Informed Neural Networks to Model and Control Robots.md | 3 (High — PRIMARY BASELINE) | N1-Liu (REJECT — RK4 rollout conflicts with RNEA); N2-Liu (KEEP — Cholesky diagonal FrictionNet, IMPLEMENTED and MERGED); N3-Liu (KEEP — Lyapunov template, implemented in Stage 3, MERGED); N4-Liu (KEEP — --max_samples ablation, MERGED) |
| Processed | Djeumou et al. (2024) "One Model to Drift Them All" (CoRL vehicle drifting).md | 0 (None — vehicle drifting, no robot arm applicability) | N1-Djeumou-CoRL (REJECT — hierarchical rate decoupling, vehicle-specific, incompatible); N2-Djeumou-CoRL (REJECT — diffusion-based payload estimation, no implementation path) |
| Processed | Duong et al. (2024) Port-Hamiltonian Neural ODE Networks on Lie.md | 1 (Low-Medium — validates phys. structures) | N1-Duong (INVESTIGATE — Cholesky L L^T + eps*I algebraic kernel, considered in N2-Liu FrictionNet design); N2-Duong (REJECT — duplicate of N1-Duong); N3-Duong (KEEP — IMPLEMENTED sim-to-real fine-tuning, MERGED to main, commit 0aa4fdc) |
| Processed | Wang et al. (2024) Trajectory_Control_of_Multi-Axis_Robotic_Arms....md | 1 (Low-Medium — standard baseline) | N1-WangCAC (INVESTIGATE — Sobol sampling for excitation, revisit when data pipeline exists); N2-WangCAC (REJECT — trapezoidal residual, same conflict as N1-Liu); N3-WangCAC (REJECT — EKF, latency incompatible with 1 kHz control) |
| Processed | Wang et al. (2025) - Symplectic Physics-Embedded Learning (SPEL).md | 1 (Low-Medium — physics-driven design) | N1-SPEL (INVESTIGATE — sparsity mask on Cholesky friction matrix for revolute joints, considered in N2-Liu FrictionNet design); N2-SPEL (REJECT — trainable URDF constants, violates RNEA-intact invariant); N3-SPEL (REJECT — KAN activations, violates Mish/Softplus constraint) |

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

## Experiments logged
| Run ID | Date | Val loss | Notes |
|--------|------|----------|-------|
| N/A | N/A | N/A | No training runs executed yet; Stage 1 pipeline ready, awaiting GPU access |

## Current milestone
Stage 1 (PINN) — architecture finalized; N2-Liu FrictionNet diagonal design IMPLEMENTED and MERGED to main (ebc2ba3); N3-Duong sim-to-real fine-tuning IMPLEMENTED and MERGED to main (0aa4fdc); all implemented novelties (N2-Liu, N3-Liu, N4-Liu, N3-Duong) MERGED; awaiting GPU access for Stage 1 training.

## Open questions / blockers
- **GPU access blocker:** Stage 1 training cannot execute without GPU. Waiting for GPU allocation.
- **Pinocchio install failed (network error):** `pip install pin` needs C++ compiler (cmake/nmake not on Windows); `conda install -c conda-forge pinocchio` failed with ChunkedEncodingError mid-download. FIX: run `conda install -c conda-forge pinocchio` from Anaconda Prompt with stable network, or use mamba: `mamba install -c conda-forge pinocchio`. Pinocchio needed for `friction_sparsity_analysis.py` and future training data generation.
- N3-Djeumou (semi-supervised dissipativity): awaits first real motor-babbling HDF5 dataset to design and run ablation.
- N1-WangCAC (Sobol sampling): consider for the data pipeline when Isaac Sim HDF5 pipeline is built.
- Data pipeline: Isaac Sim excitation trajectories → HDF5 (q, qdot, qddot, delta, tau_real) not yet built; Fourier trajectory baseline available as fallback. Real motor-babbling dataset needed to run `training/fine_tune.py`.
- Physics validator advisories (non-blocking): (1) dissipativity multiplier currently batch-mean — consider per-sample multipliers if weak at runtime; (2) document under-sampling risk for max_samples < ~2000 in ablation study methodology; (3) Stage 3 DEFAULT_ERROR_BOUND = [5,5,5,5,2,2,2] Nm is placeholder — must recompute via `compute_lyapunov_gains(real_error_bound)` after Stage 1 validation.

## What to do next session
1. Install pinocchio from Anaconda Prompt: `conda install -c conda-forge pinocchio` (or mamba). Run `python -m pinocchio_baseline.friction_sparsity_analysis` to validate setup.
2. Run smoke tests once pinocchio is installed: `python -m training.train --synthetic --epochs 5` (baseline), then `python -m training.train --synthetic --epochs 5 --use_friction_net` (with FrictionNet).
3. When GPU available: run real Stage 1 training, extract validation RMSE per joint, call `compute_lyapunov_gains(real_error_bound)`, update DEFAULT_ERROR_BOUND in Stage 3, and resolve `TODO(stage3)` markers in `pinn_controller_node.py`.
