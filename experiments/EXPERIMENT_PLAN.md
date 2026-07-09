# Experiment Plan — PINN Franka Paper

_Status: **PLAN ONLY**. Nothing here is implemented yet. This document defines every
experiment we intend to run for the publication. Implementation comes later (blocked on
GPU + Isaac Sim data)._

_Last updated: 2026-07-09_

---

## Purpose

Every experiment in this plan exists to **defend one specific claim** so a reviewer cannot
say "you never showed this matters." Experiments are organised in three reference frames:

1. **External comparison** — our method vs. other people's work (Liu et al. 2024, black-box
   MLP, pure RNEA, optionally DeLaN). This is what makes the paper a *comparison* paper.
2. **Internal ablation (blocks A–I)** — each component of our own method turned on/off.
   Proves each piece earns its place.
3. **Physics sanity** — constraint satisfaction, torque smoothness, inference latency.
   Proves the claims that are not about raw accuracy.

### Critical rule for the external comparison

To compare against Liu et al. (2024) we must **reproduce their metric**, not only ours.
They report a 2 s rollout error (Table 6, PyBullet sim: LNN = **8.884 rad²**; Table 8, real
Panda 500 Hz: LNN = **2.681 rad**). Our per-joint RMSE in Nm is **not** comparable to that
number. We must also compute the 2 s rollout error on our own model — that single value is
our headline external result.

### Fairness rule for every block

Within a block, **hold everything else fixed** (same dataset, same `seed=42`, same epochs,
same optimizer, same architecture except the axis under test). Only the named axis varies.

---

## Open decisions (to settle at implementation time)

- **DeLaN external baseline (optional, high value):** currently our only *learned* comparator
  is a black-box MLP. Adding DeLaN (Lutter et al. ICLR 2019 — learns structure from scratch,
  no URDF) gives the classic 3-way story: *no structure (black-box) / learned structure
  (DeLaN) / injected structure (our grey-box)*. Strong defence of grey-box sample efficiency,
  but real extra implementation work. **Decision pending.**
- **Goal-4 sim-to-real timing:** we have no real motor-babbling data yet. We can run the
  entire Goal-4 fine-tuning study *now* as a **sim-to-sim proxy** (pretrain on one model,
  fine-tune on a friction/damping-perturbed "real" model, or use Pinocchio-analytical as
  "sim" and Isaac as "real"). This unblocks Goal 4 without the GPU/real-robot dependency.
  Replace/augment with real-data results when available. **Decision pending.**

---

## Headline experiments (one per goal — the must-haves)

| # | Goal | Experiment | Key comparison | Headline metric |
|---|------|-----------|----------------|-----------------|
| H1 | 1 | Data-efficiency curve | Grey-box vs black-box MLP, sweep `--max_samples` | Val RMSE vs N — grey-box hits target accuracy at ≪25k (Liu's budget) |
| H2 | 3 | Structure ladder | RNEA-only → black-box → grey-box → +AL → +FrictionNet (full) | Per-joint RMSE + dissipativity-violation rate down the ladder |
| H3 | 2 | Inference latency + closed-loop tracking | Full model vs RNEA-only vs black-box feedforward, 1 kHz sim loop | p50/p99 forward-pass time (<1 ms); closed-loop tracking RMSE (rad) |
| H4 | 4 | Sim-to-real (sim-to-sim proxy) | No-finetune / full-retrain / frozen-backbone at N={10,50,100,500} | RMSE recovery on the "real" (perturbed) model |

---

## Ablation matrix (blocks A–I)

### A. Model structure — defends the grey-box claim (Goals 1, 3)

| Variant | RNEA | Residual net | FrictionNet | AL | Role |
|---|---|---|---|---|---|
| M1 | ✓ | — | — | — | White-box lower bound |
| M2 | — | ✓ (predicts full τ) | — | — | Black-box MLP (Liu's comparator) |
| M3 | ✓ | ✓ | — | — | Grey-box, unconstrained |
| M4 | ✓ | ✓ | — | ✓ | + soft constraints |
| M5 | ✓ | ✓ | ✓ | — | + hard dissipativity |
| **M6** | ✓ | ✓ | ✓ | ✓ | **Full method** |

- **Claim defended:** injecting URDF structure (grey-box) beats both pure physics (M1) and
  pure data (M2); each added component improves accuracy and/or constraint satisfaction.
- **Metrics:** per-joint RMSE, dissipativity-violation rate, sample efficiency.

### B. FrictionNet — defends N2-Liu + the sparsity claim (N1-SPEL)

| Axis | Variants | What it proves |
|---|---|---|
| On/off | M3 vs M5 | FrictionNet lowers RMSE and/or kills dissipativity violations |
| **Diagonal vs full Cholesky** | 7-param diagonal `D` vs 28-param `LLᵀ` | Accuracy is equal → the 75% param reduction is justified, not a shortcut. **This is the experiment that defends Section 3.5.** |
| Soft vs hard dissipativity | AL-only (M4) vs FrictionNet-only (M5) vs both (M6) | Test-time dissipativity-violation rate — hard structural guarantee → exactly 0 |

- Run via `--use_friction_net` on/off; diagonal-vs-Cholesky requires a config switch in
  `network/friction_net.py`.

### C. Augmented Lagrangian — defends N2-Djeumou (Goal 3)

| Axis | Variants | Metric |
|---|---|---|
| Constraint mode | none / fixed-λ soft penalty / full dual-ascent AL | Torque-limit violation rate vs RMSE trade-off |
| Penalty weight ρ | {0.1, 1, 10} | Convergence stability, violation rate |

- **Claim defended:** the augmented Lagrangian dual-ascent enforces limits better than a
  fixed penalty, without wrecking accuracy.

### D. Activations — defends the Mish/Softplus rule

| Variants | Metric |
|---|---|
| Mish / Softplus / (ReLU, tanh as *forbidden* comparators) | **Torque smoothness** (jerk or spectral-arc-length of predicted τ along a test trajectory) + RMSE |

- **Claim defended:** smooth activations produce smooth torques that don't excite motor
  resonances. ReLU should predict visibly jagged torque → turns our assertion into a number.
- Note: ReLU/tanh are run **only as comparators for this figure**, never shipped (CLAUDE.md
  forbids them in the actual model).

### E. Input encoding — defends design choices (Goal 1)

| Axis | Variants | Proves |
|---|---|---|
| Angle encoding | [sin,cos,q̇,δ] vs raw [q,q̇,δ] | sin/cos avoids angle-wrap singularities |
| δ-conditioning | with vs without δ input | Payload conditioning matters (feeds block G) |

### F. Excitation trajectory — defends N1-WangCAC (Goal 1)

| Variants (same sample budget) | Metric |
|---|---|
| Sobol vs uniform-random vs grid centres | Joint-space coverage (occupancy / discrepancy) **and** downstream test RMSE on held-out configs |

- **Claim defended:** Sobol low-discrepancy sampling covers joint space better and yields a
  more accurate model *at equal sample count*.

### G. Payload generalization — defends payload conditioning (Goal 1)

| Split | Tests |
|---|---|
| Train {0,1,3} conditioned vs 3 separate single-payload models | One-model-fits-all penalty |
| **Interpolation:** train {0,3}, test 1 | Does δ interpolate? |
| **Extrapolation:** train {0,1}, test 3 | Does δ extrapolate? (harder — report honestly) |

- **Metrics:** per-payload RMSE, interpolation gap, extrapolation gap.

### H. Payload identification — defends Section 3.9 (requires `identify_payload` implemented)

| Axis | Metric |
|---|---|
| N samples {5,10,20}, sensor-noise level, config spread | δ̂ estimation error; then downstream tracking error with estimated vs true vs wrong δ |

- **Prerequisite:** `controller/payload_identification.py` is currently a stub — implement
  before running this block.

### I. Controller gains — defends N3-Liu (Goal 2)

| Variants | Metric |
|---|---|
| Lyapunov-certified gains vs manual PD vs high-gain; sweep `safety_margin` | Closed-loop tracking RMSE + stability margin |

- **Prerequisite:** recompute `DEFAULT_ERROR_BOUND` from real per-joint RMSE after Stage 1
  training (currently a placeholder `[5,5,5,5,2,2,2]` Nm).

---

## Metrics glossary (define once, use everywhere)

| Metric | Unit | Used by | Notes |
|---|---|---|---|
| Per-joint RMSE | Nm | A,B,C,E,F,G | Primary accuracy; report per joint (87/12 Nm scale split matters) |
| 2 s rollout error | rad² / rad | External (Liu) | **The Liu-comparable metric — non-negotiable for the external claim** |
| Dissipativity-violation rate | % of samples | A,B | Fraction with τ_res·q̇ > 0; hard-guarantee variants → 0 |
| Torque-limit violation rate | % of samples | C | Defends AL |
| Torque smoothness | jerk / SAL | D | Spectral-arc-length or jerk of predicted τ along a trajectory |
| Inference latency | ms (p50/p99) | H3 | Per-call, CPU and GPU, vs network width; target <1 ms |
| Closed-loop tracking RMSE | rad | H3, I | Stage 3, 1 kHz sim |

---

## Reference commands (for later implementation)

Known training entry points (from PAPER_DRAFT §3.10). Exact flags for new ablation axes
(structure variants, activation swap, diagonal-vs-Cholesky, constraint mode) will need to be
added to the CLI when implemented.

```bash
# Full method, multi-payload, Isaac Sim data (paper results)
python3 -m training.train \
  --data data/isaac_0.0kg.h5 data/isaac_1.0kg.h5 data/isaac_3.0kg.h5 \
  --epochs 200 --use_friction_net

# Data-efficiency sweep (H1 / N4-Liu) — repeat per N
python3 -m training.train --data <files> --epochs 200 --max_samples <N>

# Smoke test — synthetic Fourier data (no Isaac Sim / GPU required)
python3 -m training.train \
  --data data/fourier_baseline_0kg.h5 data/fourier_baseline_1kg.h5 data/fourier_baseline_3kg.h5 \
  --epochs 20 --use_friction_net
```

> Reminder (CLAUDE.md): never run Python code without explicit human authorization. This
> plan lists commands for the human to run; agents only write/edit code.

---

## Mapping: experiment → goal → claim

| Block | Goal(s) | Claim it defends |
|---|---|---|
| A | 1, 3 | Grey-box beats pure-physics and pure-data |
| B | 3 | FrictionNet + diagonal sparsity (75% param cut) justified; hard dissipativity |
| C | 3 | Augmented Lagrangian enforces limits better than fixed penalty |
| D | — (physics) | Mish/Softplus produce smooth, motor-safe torques |
| E | 1 | sin/cos encoding + δ-conditioning are the right inputs |
| F | 1 | Sobol excitation improves coverage and accuracy at equal budget |
| G | 1 | Single δ-conditioned model generalises across payloads |
| H | 1 | Runtime payload identification is accurate and cheap (<5 ms) |
| I | 2 | Lyapunov-certified gains track better than hand-tuned PD |
| H1–H4 | 1,2,3,4 | Headline evidence, one per goal |
| External | all | Direct comparison to Liu 2024 via shared rollout metric |
