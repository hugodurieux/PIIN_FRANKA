# Project State — PINN Franka Pipeline
_Last updated: 2026-06-24_

## 1. Objectives (from goal.md)
| # | Objective | Status | Evidence / where proven |
|---|-----------|--------|-------------------------|
| 1 | Automated "URDF-to-Model" Pipeline — accept any URDF, auto-extract kinematics via Pinocchio, generate network, produce trained dynamic model | in progress | `pinocchio_baseline/rnea_wrapper.py` (URDF -> RNEA); `network/grey_box_net.py` + `training/train.py` (architecture + training loop). No training run yet. |
| 2 | High-Frequency Real-Time Control at 1000 Hz (MPC integration, microsecond inference) | not started | Architecture designed to exclude qddot from the 1 kHz path (see rnea_wrapper.py comments); no controller or MPC built yet. |
| 3 | Scaling to 7-DoF — Augmented Lagrangian constraints + residual friction on a full Franka Panda | in progress | `training/constraints.py` implements AL penalties (torque limits + dissipativity) for all 7 joints. Corroborated by Djeumou et al. (2022). No training run yet. |
| 4 | Standardized Sim-to-Real Gap resolution via physics-constrained fine-tuning | not started | Methodology described in `Step1_Indication.md` (freeze base layers, fine-tune on real motor-babbling data under PINN loss). Not implemented in code yet. |

## 2. Pipeline architecture (URDF -> trained robot)

tau_pred = RNEA(q, qdot, qddot; URDF + delta) + GreyBoxNet([sin(q), cos(q), qdot, delta])
Loss     = MSE(tau_pred, tau_real) + AugmentedLagrangian(torque_limits, dissipativity)

### Stage 1 — PINN dynamics learning
Fully architected in code; no training runs executed yet.

- White-box RNEA: `pinocchio_baseline/rnea_wrapper.py` — wraps `pinocchio.rnea`, handles payload injection into end-effector inertia, runs offline only.
- Residual network: `network/grey_box_net.py` — MLP (default 4x256, Mish), input X in R^22 = [sin(q), cos(q), qdot, delta], output tau_res in R^7. ReLU forbidden.
- Physics constraints: `training/constraints.py` — `AugmentedLagrangian` class; enforces |tau_pred| <= TORQUE_LIMITS and tau_res . qdot <= 0 (dissipativity) with dual-ascent multiplier updates.
- Training loop: `training/train.py` — Adam optimizer, 90/10 train/val split, CSV logging, best-checkpoint save. Supports synthetic data (no Pinocchio needed) and real HDF5 datasets.
- Constants: `network/constants.py` — single source of truth for joint limits, velocity limits, input/output dims, payload values.

Data pipeline (not yet built): excitation trajectories in Isaac Sim -> HDF5 dataset with (q, qdot, qddot, delta, tau_real).

### Stage 2 — Motion planning (MoveIt2 / ROS2)
Not started. Planned: standard MoveIt2, minimal setup to showcase Stage 1 model.

### Stage 3 — Controller + integration
Not started. Planned: computed-torque feedforward using trained GreyBoxNet + PD correction at 1000 Hz.

### Stage 4 — Grabbing (optional)
Not started.

## 3. Implemented novelties
| ID | From paper | Description | Goal served | Branch | Validated | Merged |
|----|-----------|-------------|-------------|--------|-----------|--------|
| N1-Djeumou | Djeumou et al. (2022) | Compositional grey-box structure: known analytical terms (RNEA) composed with neural residual. REJECT — already fully implemented as the project's core architecture in `grey_box_net.py`. Architecture corroborated by peer-reviewed paper. | Goal 1, Goal 3 | main | architecture match confirmed | n/a (pre-existing) |
| N2-Djeumou | Djeumou et al. (2022) | Augmented Lagrangian training with Lagrange multiplier dual-ascent for hard physics constraints. REJECT — already fully implemented in `constraints.py`. | Goal 3 | main | architecture match confirmed | n/a (pre-existing) |
| N3-Djeumou | Djeumou et al. (2022) | Semi-supervised constraint enforcement on unlabeled joint-space points to extend dissipativity guarantees beyond training trajectories. INVESTIGATE — ablation study needed. | Goal 3, Goal 4 | not started | not validated | not merged |

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
|   |-- constants.py                 Franka Panda physical constants (TORQUE_LIMITS etc.)
|   |-- grey_box_net.py              GreyBoxNet MLP + encode_state(); the learned residual
|   |-- __init__.py
|
|-- training/
|   |-- constraints.py               AugmentedLagrangian: torque-limit + dissipativity
|   |-- dataset.py                   SyntheticDataset + FrankaDynamicsDataset (HDF5)
|   |-- train.py                     Main training loop (Adam + AL dual ascent)
|   |-- __init__.py
|
|-- pinocchio_baseline/
|   |-- rnea_wrapper.py              RneaBaseline: URDF -> batched RNEA, payload injection
|   |-- __init__.py
|
|-- tracking/
|   |-- PROJECT_STATE.md             This file
|   |-- papers_review.csv            One row per paper processed
|
|-- papers/
|   |-- inbox/                       Drop new papers here for /process-papers
|   |   |-- Djeumou et al. (2022)... (processed, not yet moved to processed/)
|   |   |-- Liu et al. (2024)...     (not yet processed)
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
- Move `papers/inbox/Djeumou et al. (2022)...` to `papers/processed/` now that it is reviewed.
- Process Liu et al. (2024) — the main reference paper — through /process-papers.
- N3 (Djeumou): design and run ablation study comparing training with vs. without semi-supervised dissipativity enforcement on off-trajectory unlabeled points. Needs an implementation branch.
- Build data pipeline: Isaac Sim excitation trajectories -> HDF5 dataset (q, qdot, qddot, delta, tau_real).
- Run first training experiment on synthetic data to validate the full training loop end-to-end (`python -m training.train --synthetic --epochs 5`).
- Stage 1 sim-to-real fine-tuning (Objective 4): implement frozen-layer fine-tuning on real motor-babbling data.
- Stage 2 (MoveIt2 / ROS2): not started.
- Stage 3 (1 kHz controller): not started; requires trained model from Stage 1.
