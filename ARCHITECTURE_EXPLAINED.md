# Project Architecture — Plain Language Explanations

> This file is a static reference. It is not updated automatically.

---

## 1. What is RNEA?

RNEA stands for **Recursive Newton-Euler Algorithm**. It is a classical robotics algorithm that computes the **inverse dynamics** of a rigid-body robot: given the joint positions, velocities, and accelerations, it returns the joint torques needed to produce that motion.

### The physics it encodes

For a robot arm, Newton's second law at each joint gives:

```
τ = M(q)·q̈ + C(q,q̇)·q̇ + g(q)
```

| Symbol | Name | Meaning |
|---|---|---|
| `M(q)` | Inertia matrix | Resistance to acceleration |
| `C(q,q̇)·q̇` | Coriolis and centrifugal forces | Forces due to joint velocities |
| `g(q)` | Gravity torques | Weight of links pulling on joints |
| `τ` | Joint torques | What you want to compute |

RNEA computes this **exactly and efficiently** by walking up and down the kinematic chain twice — hence "recursive." It reads all link masses, inertias, and geometry directly from the **URDF file** via Pinocchio.

### Why it matters for the project

| Property | Consequence |
|---|---|
| Exact physics | The baseline torque is correct by construction — no learning needed for the main dynamics |
| URDF-driven | Works for any robot automatically (Goal 1) |
| Offline only | Needs `q̈` (joint acceleration), computed from recorded data — not available at runtime, so RNEA runs at training time only |
| Fixed | Never modified — it is the "white box" in grey-box |

### What RNEA cannot capture

It assumes **perfect rigid bodies** with **no friction, no flexibility, no payload uncertainty**. That gap is exactly what the neural residual `τ_res` is trained to fill.

---

## 2. The Grey-Box Architecture

"Grey-box" means **known physics + learned correction**. It sits between a pure white-box (100% equations) and a pure black-box (100% neural network).

### The equation

```
τ_pred = RNEA(q, q̇, q̈) + τ_res(q, q̇, δ)
```

| Term | Type | What it does |
|---|---|---|
| `RNEA(q, q̇, q̈)` | White box | Computes exact rigid-body torques from the URDF via Pinocchio |
| `τ_res(q, q̇, δ)` | Neural network | Learns the residual: friction, flexibility, unmodeled dynamics |
| `δ` | Payload vector | Mass + center-of-mass offset of the carried object |

### The network input

`τ_res` takes a **22-dimensional input vector**:

```
X = [sin(q), cos(q), q̇, δ]
  =   [7]  +  [7]  + [7] + [1 or 3]
  = 22 values
```

- `sin(q)` and `cos(q)` instead of `q` directly — avoids angle wraparound at ±π
- `q̇` — joint velocities (friction depends on velocity)
- `δ` — payload description (mass, or mass + center-of-mass offset)

### The network structure

```
Input (22-dim)
      ↓
[Linear → Mish] × N hidden layers
      ↓
FrictionNet sub-module:
   D = Softplus(d_diag)      ← 7 positive diagonal values
   τ_friction = -D · q̇      ← dissipative by construction
      ↓
τ_res = τ_res_grey + τ_friction
τ_pred = RNEA + τ_res
```

Key constraints on the network:
- **Mish or Softplus only** — smooth activations → smooth torque commands → no motor jerk
- **No recurrence** — stateless, so inference takes < 1 ms at 1 kHz
- **Dissipativity**: FrictionNet ensures friction always opposes motion (`τ_friction · q̇ ≤ 0`)

### Why this beats Liu et al. (2024)

| Liu et al. | This project |
|---|---|
| Network learns M, C, g from scratch | RNEA provides M, C, g exactly — network only learns the residual |
| Large network needed | Small network — residual is a small fraction of total torque |
| Needs lots of data | Data-efficient — less to learn |
| No payload generalization | `δ` in input + virtual payload link in RNEA |
| No torque-limit enforcement | Augmented Lagrangian hard constraints |

The core insight: **the harder you make the physics do, the less the network needs to learn.**

---

## 3. The Loss Function

The loss has **3 distinct terms**:

```
Loss = MSE(τ_pred, τ_real)
     + λ_torque · ψ_torque + (ρ/2) · ψ_torque²
     + λ_dissip · ψ_dissip + (ρ/2) · ψ_dissip²
```

| Term | What it enforces | Activates when |
|---|---|---|
| **MSE** | Prediction accuracy: `τ_pred` close to measured `τ_real` | Always |
| **Torque limits** | `\|τ_pred[i]\| ≤ [87,87,87,87,12,12,12]` Nm per joint | Torque exceeds safe range |
| **Dissipativity** | `τ_res · q̇ ≤ 0` — residual must dissipate energy, not inject it | Residual pushes in the direction of motion |

Terms 2 and 3 are Augmented Lagrangian penalties — each has its own independent Lagrange multiplier (`λ_torque` and `λ_dissip`) that self-adjusts during training.

---

## 4. The Augmented Lagrangian

### The problem it solves

You want to minimize a loss **subject to a constraint**:

```
minimize  MSE(τ_pred, τ_real)
subject to  g(x) ≤ 0
```

You can't just use gradient descent on MSE alone — it ignores the constraint entirely.

### The naive approach: penalty method

Add a penalty when the constraint is violated:

```
Loss = MSE + (ρ/2) · max(0, g)²
```

Problem: to enforce the constraint tightly, you need ρ → ∞, which makes the loss landscape extremely steep and kills gradient descent numerically.

### The augmented Lagrangian fix

Add a **Lagrange multiplier λ** alongside the penalty:

```
Loss = MSE + λ · ψ + (ρ/2) · ψ²
```

where `ψ = max(0, g)` is the constraint violation (zero when satisfied).

Now λ does the heavy lifting — ρ can stay small and finite. The multiplier λ is **not a network parameter** — it lives outside the network and is updated separately.

### The dual ascent update

After each epoch, λ is updated:

```
λ ← max(0,  λ + ρ · mean(g))
```

In plain English:
- If the constraint was violated on average this epoch → `g > 0` → λ **increases** → the penalty term gets heavier next epoch → the network is pushed harder to fix it
- If the constraint was already satisfied → `g ≤ 0` → λ stays the same or is clamped at 0 → no extra pressure

It is a feedback loop: **the more the network violates the constraint, the more it gets penalized next epoch.**

### Concretely in the project

Two separate constraints, each with its own λ:

#### Constraint 1 — Torque limits
```
g_torque = |τ_pred[i]| - limit[i]   ≤ 0   for each joint i

ψ_torque = max(0, g_torque)
term_torque = λ_torque · ψ_torque + (ρ/2) · ψ_torque²

update: λ_torque ← max(0, λ_torque + ρ · mean(g_torque))
```

#### Constraint 2 — Dissipativity
```
g_dissip = τ_res · q̇   ≤ 0   (friction must oppose motion)

ψ_dissip = max(0, g_dissip)
term_dissip = λ_dissip · ψ_dissip + (ρ/2) · ψ_dissip²

update: λ_dissip ← max(0, λ_dissip + ρ · mean(g_dissip))
```

### Why it works better than a plain penalty

| Plain penalty | Augmented Lagrangian |
|---|---|
| ρ must be huge to enforce constraint | ρ stays small (e.g. 1.0) |
| Very steep loss landscape | Smooth, trainable landscape |
| Fixed pressure regardless of violation | Pressure adapts — grows only when needed |
| Hard to tune | Self-regulating via λ feedback |

---

## 5. The FrictionNet

### What problem it solves

The neural residual `τ_res` is a general MLP — it can output anything, including torques that **inject energy** into the system (pushing in the direction of motion). Real friction always opposes motion. The dissipativity constraint in the AL enforces this softly, but FrictionNet enforces it **structurally** — it is impossible for the network to violate it, by construction.

### The physics

Viscous friction is modeled as:

```
τ_friction = -D · q̇
```

Where `D` is a **positive-definite diagonal matrix** of friction coefficients. The sign means: if the joint moves forward (`q̇ > 0`), friction pushes backward (`τ_friction < 0`). Energy dissipation is guaranteed:

```
τ_friction · q̇ = -q̇ᵀ D q̇ ≤ 0   always   (since D > 0)
```

No matter what values D takes — as long as it is positive — dissipativity is satisfied.

### How the network parameterizes D

You can't just output D directly because gradient descent might push entries negative. Instead:

```python
d_diag = nn.Parameter(torch.ones(7))   # raw unconstrained parameters
D = Softplus(d_diag)                    # guaranteed > 0
τ_friction = -D · q̇
```

`Softplus(x) = log(1 + eˣ)` maps any real number to a strictly positive value. So D is always positive, and dissipativity is always satisfied — **the constraint cannot be violated, ever.**

### Where it fits in the architecture

```
Input X (22-dim)
      ↓
   GreyBoxNet MLP
      ↓
  τ_res_grey  (general residual, 7-dim)
      ↓  +
  FrictionNet: τ_friction = -Softplus(d_diag) · q̇
      ↓
  τ_res = τ_res_grey + τ_friction

  τ_pred = RNEA + τ_res
```

FrictionNet only needs `q̇` as input. It is a **7-parameter sub-module** — just 7 learnable scalars, one per joint.

### Why diagonal D (not full 7×7 matrix)

A full 7×7 friction matrix would have 28 lower-triangular entries (Cholesky). The diagonal case has only 7. The justification is physical:

- All 7 Franka joints are **independent revolute joints** (`JointModelRZ` in Pinocchio)
- There is no mechanical coupling between joints in the gearbox
- Cross-joint friction terms would be physically meaningless

This was confirmed by Pinocchio analysis: the diagonal is not an approximation — it is the **correct** structure. 75% fewer parameters than full Cholesky, with no loss of expressiveness.

### What it learns in practice

From smoke runs on synthetic data:

| Joint | D value (converged) |
|---|---|
| J1 | ~2.05 (highest — largest joint, most friction) |
| J2–J4 | ~1.5–1.8 |
| J5–J7 | ~1.2–1.4 (smaller joints, less friction) |

The ordering is **physically plausible** — larger joints with bigger gearboxes have higher viscous friction coefficients. The network discovered this from data alone, with no supervision on the D values themselves.

---

## 6. The Training Loop — Step by Step

### Before training starts (setup)

```
1. Load dataset → split 90% train / 10% validation (fixed seed=0, reproducible)
2. Build GreyBoxNet (MLP with Mish, 4 hidden layers × 256 units)
3. Optionally build FrictionNet (7 parameters)
4. Build AugmentedLagrangian (λ_torque=0, λ_dissip=0, ρ=1.0)
5. Build Adam optimizer over all network parameters
6. Create run folder: models/run_YYYYMMDD_HHMMSS/
```

### Each epoch (repeated N times)

#### Phase 1 — Training (mini-batches of 256 samples)

For each batch:

```
Step 1 — Forward pass
   Read from batch: q, q̇, δ, τ_real, τ_theo (τ_theo = RNEA, precomputed)

   τ_res_grey = GreyBoxNet(q, q̇, δ)
   τ_res_fric = FrictionNet(q, q̇, δ)    ← only if --use_friction_net
   τ_res      = τ_res_grey + τ_res_fric
   τ_pred     = τ_theo + τ_res

Step 2 — Compute loss
   MSE     = mean((τ_pred - τ_real)²)
   penalty = λ_torque·ψ_torque + (ρ/2)·ψ_torque²
           + λ_dissip·ψ_dissip + (ρ/2)·ψ_dissip²
   Loss    = MSE + penalty

Step 3 — Backward pass
   Loss.backward()   ← compute gradients w.r.t. network weights
   Adam.step()       ← update network weights
   opt.zero_grad()   ← clear gradients for next batch
```

Note: **λ values do NOT change during mini-batches** — only network weights update here.

#### Phase 2 — Lagrange multiplier update (once per epoch, after all batches)

```
Using the last batch of the epoch:
   λ_torque ← max(0, λ_torque + ρ · mean(|τ_pred| - limit))
   λ_dissip ← max(0, λ_dissip + ρ · mean(τ_res · q̇))
```

This is the **dual ascent** step. Multipliers grow if constraints were violated during this epoch.

#### Phase 3 — Validation (no gradients)

```
For each batch in the validation set:
   Forward pass only → compute loss and MSE
   No backward pass, no weight updates

Average val loss and val MSE across all val batches
```

#### Phase 4 — Logging and checkpoint

```
Write to train_log.csv:
   epoch, train_loss, train_mse, val_loss, val_mse,
   max_torque_violation, mean_dissip_violation

Every 10% of epochs: print to console
   → also print D_diag per joint if FrictionNet is active

If val_loss < best so far:
   → save greybox_best.pt  (and friction_net_best.pt if FrictionNet active)
```

Only the **best validation checkpoint** is kept — not the final epoch weights.

### After all epochs — diagnostics

```
Per-joint RMSE on validation set:
   Joints 1-4 (87 Nm limit) vs Joints 5-7 (12 Nm limit)

   If ratio > 2.0x → warn about torque scale imbalance
                    → suggests EMA loss balancing
   Else            → "scale within tolerance"

Save config.json: all hyperparameters + best_val_loss + per_joint_rmse
```

### The full picture as a timeline

```
Epoch 1
  ├── batch 1: forward → loss → backward → Adam step
  ├── batch 2: forward → loss → backward → Adam step
  ├── ...
  ├── batch N: forward → loss → backward → Adam step
  ├── [dual ascent]  update λ_torque, λ_dissip
  ├── [validation]   compute val loss (no gradients)
  └── [checkpoint]   save if best val loss

Epoch 2 ... same structure, λ values now updated
...
Epoch 200
  └── [diagnostics]  per-joint RMSE + save config.json
```

### Key design choices

| Choice | Why |
|---|---|
| 90/10 train/val split, seed=0 | Reproducible across runs |
| Adam optimizer | Adaptive learning rate per parameter |
| λ updated once per epoch, not per batch | Keeps multiplier dynamics slow and stable |
| Best val checkpoint saved | Guards against overfitting at late epochs |
| `τ_theo` precomputed in dataset | RNEA runs offline — never called per-batch at training time |
| Mish activation | Smooth, non-monotonic — better gradient flow than ReLU, smooth torque output |
