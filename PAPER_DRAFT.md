# From URDF to Real-Time Control: An Automated Physics-Informed Neural Network Pipeline for 7-DoF Robot Dynamics Learning

**Hugo Durieux** — Master's Internship, 2026

_Working draft — updated automatically at the end of each session._
_Last updated: 2026-06-25 (evening)_

---

## Abstract

We present an automated pipeline that takes a robot's URDF description as input and produces a trained, real-time-deployable dynamics model for a 7-degree-of-freedom manipulator. The pipeline combines a deterministic white-box baseline (Recursive Newton-Euler Algorithm, RNEA, computed via Pinocchio from the URDF) with a physics-constrained neural residual network that learns unmodeled friction, elasticity, and payload-dependent effects. Four contributions distinguish this work from the primary state of the art (Liu et al., 2024): (1) a fully automated URDF-to-model pipeline requiring no manual kinematic derivation; (2) a real-time computed-torque controller with Lyapunov-certified gain selection operating at 1000 Hz; (3) a structurally dissipative FrictionNet sub-module that guarantees the friction residual dissipates energy by construction, without relying on soft penalty terms; and (4) a two-step sim-to-real fine-tuning protocol that recovers tracking accuracy from a pre-trained simulation model using only a brief real-world motor-babbling sequence. Experiments on the Franka Panda arm with payloads of 0, 1, and 3 kg are planned pending GPU allocation.

---

## 1. Introduction

Learning accurate dynamics models for robotic manipulators is a prerequisite for high-performance model-based control. Physics-Informed Neural Networks (PINNs) offer a promising middle ground between pure data-driven models and fully analytical approaches: they inject known physical structure into the network architecture and training objective, reducing data requirements and improving generalisation.

Liu et al. (2024) demonstrated that a Lagrangian/Hamiltonian neural network trained on 25,000 samples from a Franka Panda achieves substantially lower prediction error than a black-box baseline, and that the learned model can drive a stable PD-augmented computed-torque controller on real hardware at 500 Hz. However, their approach has several limitations that this work addresses:

| Gap in Liu et al. (2024) | This work's answer |
|--------------------------|-------------------|
| Equations manually derived per robot | Automated URDF → Pinocchio → network pipeline |
| Control at 500 Hz, no MPC | 1000 Hz target; Lyapunov-certified gains |
| No payload conditioning | Payload mass δ ∈ {0, 1, 3} kg as network input |
| No sim-to-real transfer protocol | 2-step pre-train (sim) + fine-tune (real, ~100 steps) |
| No torque/velocity limits in loss | Augmented Lagrangian constraints on all 7 joints |
| Full black-box Lagrangian | Grey-box: RNEA white-box + learned residual |
| Soft dissipativity only | FrictionNet: hard structural dissipativity guarantee |

---

## 2. Related Work

### 2.1 Primary Baseline

**Liu, Borja, Della Santina (2024).** "Physics-Informed Neural Networks to Model and Control Robots: A Theoretical and Experimental Investigation." _Advanced Intelligent Systems_ (Wiley), vol. 6, no. 5.

This is the direct state-of-the-art reference for this project. Liu et al. extend Lagrangian and Hamiltonian Neural Networks (LNNs/HNNs) to handle dissipative forces and non-collocated actuation — two obstacles that prevented prior LNN/HNN work from transferring to real robots. They replace direct acceleration supervision with an RK4 rollout loss to avoid the need for measured joint accelerations, and prove Lyapunov stability for the resulting computed-torque controller. All four novelties of this project are defined relative to this baseline.

### 2.2 Physics-Informed Architecture and Constraints

**Djeumou, Neary, Goubault, Putot, Topcu (2022).** "Neural Networks with Physics-Informed Architectures and Constraints for Dynamical Systems Modeling." _L4DC 2022_, PMLR vol. 168.

Establishes the compositional grey-box architecture (known analytical terms + neural residual, Eq. 1-2) and the Augmented Lagrangian training algorithm with dual-ascent multiplier updates (Algorithm 1) used in this project. The grey-box decomposition tau_pred = RNEA + tau_res and the augmented Lagrangian constraint enforcement are both corroborated by this paper. Semi-supervised constraint enforcement on unlabelled joint-space points (N3-Djeumou) is identified as a future direction for extending dissipativity guarantees.

### 2.3 Cholesky Dissipativity and Fine-Tuning

**Duong, Altawaitan, Stanley, Atanasov (2024).** "Port-Hamiltonian Neural ODE Networks on Lie Groups For Robot Dynamics Learning and Control." _IEEE Transactions on Robotics_.

Two concepts are extracted from this paper. (1) The L L^T + ε I algebraic kernel for parameterising positive-definite dissipation matrices via a lower-triangular Cholesky factor (Section II-C), which informs the FrictionNet design. (2) The empirical finding (Section IV-D, Table III) that a pretrained physics-informed model can recover tracking accuracy after a payload change using only ~100 gradient steps on real hardware data — the direct precedent for our sim-to-real fine-tuning protocol. The port-Hamiltonian, ODE rollout, and Lie-group infrastructure are not used.

### 2.4 Geometric Sparsity in Dissipation Matrices

**Wang, Chen, Ding (2025).** "Symplectic Physics-Embedded Learning via Lie Groups Hamiltonian Formulation for Serial Manipulator Dynamics Prediction." _Scientific Reports_ (Nature), vol. 15, art. 33179.

Provides the sparsity argument for the FrictionNet design: for revolute joints rotating about a single axis, the per-link SE(3) dissipation matrix has structural zeros, collapsing to a per-joint scalar in joint space for a serial independent-motor chain (Section II-B). Applied to the Franka Panda (7 independent revolute joints), this reduces the FrictionNet output from 28 lower-triangular Cholesky entries to 7 diagonal entries — a 75% parameter reduction with full physical justification. The SPEL forward-simulation ODE architecture is not used.

### 2.5 Excluded Papers

**Djeumou et al. (2024)** (CoRL, vehicle drifting via conditional diffusion) and **Wang et al. (2024)** (CAC, PINN-NMPC on 3-DoF planar arm): domain mismatch (vehicles, 3-DoF simulation) and architectural incompatibilities (ReLU, ODE rollouts, no RNEA) preclude any direct contribution.

---

## 3. Method

### 3.1 Problem Formulation

Given a URDF file describing a 7-DoF manipulator and a dataset of trajectories {q, q̇, q̈, δ, τ_real}, learn a model τ_pred(q, q̇, q̈, δ) that:
- Predicts joint torques accurately (low MSE)
- Respects joint torque limits |τ_pred| ≤ τ_max
- Produces a dissipative residual (τ_res · q̇ ≤ 0)
- Runs in under 1 ms at inference time

### 3.2 White-Box Baseline: RNEA from URDF

The URDF is loaded via Pinocchio. The Recursive Newton-Euler Algorithm computes the theoretical rigid-body torque:

```
τ_RBD = M(q)q̈ + C(q,q̇)q̇ + G(q)
```

where M is the inertia matrix, C the Coriolis/centrifugal matrix, and G the gravity vector. A known payload mass δ is injected by augmenting the end-effector link inertia before the RNEA call. The RNEA baseline is computed **offline** during dataset preparation and is **never modified**.

_File: `pinocchio_baseline/rnea_wrapper.py`_

### 3.3 Grey-Box Residual Network

A neural network (GreyBoxNet) learns the residual between RNEA and the true torque:

```
τ_res = f_θ([sin(q), cos(q), q̇, δ])    ∈ R^7
τ_pred = τ_RBD + τ_res
```

The sin/cos encoding prevents angle-wrapping singularities. The residual captures unmodelled friction, elasticity, and load-dependent effects. Activations are **Mish only** — smooth activations prevent torque discontinuities that would excite motor resonances. ReLU is forbidden.

_Architecture: 4 × 256 hidden units, Mish, input R^22, output R^7._
_File: `network/grey_box_net.py`_ [Djeumou et al. 2022, Eq. 1-2; Liu et al. 2024]

### 3.4 Physics-Informed Training Loss

The loss combines data fidelity with two Augmented Lagrangian constraints:

```
L_total = L_data + L_AL

L_data = (1/N) Σ ||τ_pred - τ_real||²

L_AL = λ_torque · ψ_torque + (ρ/2) ψ²_torque
     + λ_dissip · ψ_dissip + (ρ/2) ψ²_dissip

ψ_torque = max(0, |τ_pred| - τ_max)    [per joint, per sample]
ψ_dissip = max(0, τ_res · q̇)           [energy injection penalty]
```

Multipliers are updated by dual ascent: λ ← max(0, λ + ρ · g̅).

_File: `training/constraints.py`_ [Djeumou et al. 2022, Algorithm 1; Liu et al. 2024]

### 3.5 FrictionNet: Structural Dissipativity (N2-Liu)

The Augmented Lagrangian dissipativity constraint is a _soft_ penalty. FrictionNet makes dissipativity a _hard structural guarantee_ for the friction component.

A lightweight sub-network predicts a state-dependent diagonal damping matrix:

```
d = MLP([sin(q), cos(q), q̇, δ])            ∈ R^7   (2 × 64 hidden, Mish)
D(q, q̇, δ) = diag(Softplus(d) + ε)        ∈ R^{7×7},  ε = 1e-6
τ_friction = −D · q̇                          ∈ R^7
```

Dissipativity is guaranteed analytically:
```
τ_friction · q̇ = −q̇^T D q̇ = −Σ_i Softplus(d_i) · q̇_i² ≤ 0   always
```

The combined residual is:
```
τ_res = GreyBoxNet(q, q̇, δ) + FrictionNet(q, q̇, δ)
```

**Design justification (3 sources):**
- _Cholesky idea_: Liu et al. (2024), Section III-B, D-NN sub-network.
- _L L^T algebraic kernel_: Duong et al. (2024), Section II-C. Diagonal case: Softplus(d_i) = L_ii².
- _Diagonal sparsity (7 params not 28)_: Wang et al. (2025), Section II-B. For Franka's 7 independent-motor revolute joints, the joint-space friction matrix has no off-diagonal coupling.

_File: `network/friction_net.py`_ | Branch merged: `novelty/N2-Liu-frictionnet`
_Activated by:_ `python -m training.train --use_friction_net`

### 3.6 Stage 3 Controller: Lyapunov-Certified PD Gains (N3-Liu)

The computed-torque controller is:

```
τ = RNEA(q, q̇, q̈_des) + τ_res(q, q̇, δ) + K_d(q̇_des − q̇) + K_p(q_des − q)
```

Gains are computed from Liu et al. (2024) Proposition 1 (Section III-C):

```
K_d[j] = safety_margin × ε_j        (ε_j = per-joint model error bound)
K_p[j] = K_d[j]² / 4               (critical damping — fastest convergence without overshoot)
```

_Default error bound: [5, 5, 5, 5, 2, 2, 2] Nm (placeholder — to be updated after Stage 1 training)._
_File: `controller/lyapunov_gains.py`_ [Liu et al. 2024, Proposition 1] | Merged: `stage3/computed-torque-pd-controller`

### 3.7 Sim-to-Real Fine-Tuning (N3-Duong)

Following Duong et al. (2024), a pre-trained GreyBoxNet checkpoint is adapted to real hardware by:

1. Freezing all layers except the last two `nn.Linear` modules (early layers encode transferable features; final layers adapt to hardware-specific friction signatures).
2. Fine-tuning for ~100 gradient steps on a real motor-babbling HDF5 dataset.
3. Keeping the full PINN loss (MSE + Augmented Lagrangian) active during fine-tuning — the physics constraints act as a regulariser preventing overfitting to sensor noise.

```
python -m training.fine_tune --checkpoint models/run_XXXX/greybox_best.pt \
    --real_data data/real_motor_babbling.h5 --max_steps 100
```

_File: `training/fine_tune.py`_ [Duong et al. 2024, Section IV-D, Table III] | Merged: `novelty/duong2024-N3-simtoreal-finetune`

### 3.8 Data-Efficiency Ablation (N4-Liu)

To quantify the advantage of the URDF-seeded grey-box approach over Liu et al.'s 25,000-sample black-box baseline, training supports a `--max_samples N` flag that truncates the dataset to N random samples (seed=42) before the train/val split.

```
python -m training.train --data data/dataset.h5 --max_samples 5000 --epochs 200
```

_File: `training/dataset.py`_ [Liu et al. 2024, Section IV-B, Table I] | Merged: `novelty/liu2024-N4-max-samples`

---

## 4. Experiments

_Pending GPU allocation. This section will be populated after Stage 1 training._

### 4.1 Planned Experiments

| Experiment | Metric | Baseline |
|-----------|--------|----------|
| Stage 1 smoke test | Val loss convergence | N/A |
| Torque prediction RMSE per joint | RMSE [Nm] | Liu et al. 2024: 2.68 rad² over 2 s |
| Data-efficiency ablation (N4) | Val RMSE vs. N_samples | Liu et al.: 25k samples |
| FrictionNet ablation (N2) | Val RMSE, dissipation violation rate | Baseline GreyBoxNet |
| Sim-to-real transfer (N3-Duong) | RMSE before/after fine-tuning at N steps | No fine-tuning |
| Stage 3 tracking on real hardware | Tracking error [rad] at 1000 Hz | Liu et al.: 500 Hz |

### 4.2 Results

_No training runs executed yet. GPU access pending._

---

## 5. Conclusion

_To be written after experiments._

---

## 6. References

1. **Liu, Borja, Della Santina (2024).** "Physics-Informed Neural Networks to Model and Control Robots: A Theoretical and Experimental Investigation." _Advanced Intelligent Systems_ (Wiley), vol. 6, no. 5. — **Primary baseline.**

2. **Djeumou, Neary, Goubault, Putot, Topcu (2022).** "Neural Networks with Physics-Informed Architectures and Constraints for Dynamical Systems Modeling." _L4DC 2022_, PMLR vol. 168. — Grey-box architecture (N1-Djeumou) and Augmented Lagrangian training (N2-Djeumou).

3. **Duong, Altawaitan, Stanley, Atanasov (2024).** "Port-Hamiltonian Neural ODE Networks on Lie Groups For Robot Dynamics Learning and Control." _IEEE Transactions on Robotics_. — Cholesky L L^T kernel (N1-Duong, informs FrictionNet); sim-to-real 100-step fine-tuning (N3-Duong).

4. **Wang, Chen, Ding (2025).** "Symplectic Physics-Embedded Learning via Lie Groups Hamiltonian Formulation for Serial Manipulator Dynamics Prediction." _Scientific Reports_ (Nature), vol. 15, art. 33179. — Revolute-joint sparsity mask for diagonal FrictionNet (N1-SPEL).

5. **Wang, Xia, Jin, Xu, Zhang (2024).** "Trajectory Control of Multi-Axis Robotic Arms Based on Physics-Informed Neural Networks and Nonlinear Model Predictive Control." _2024 China Automation Congress (CAC)_, IEEE. — Sobol sampling idea (N1-WangCAC, future data pipeline).

---

## Appendix A — Novelty Tracking

| ID | Description | Source | Goal | Status |
|----|-------------|--------|------|--------|
| N1-Djeumou | Compositional grey-box (RNEA + residual) | Djeumou et al. 2022, Eq. 1-2 | 1, 3 | Pre-existing architecture — validated |
| N2-Djeumou | Augmented Lagrangian dual-ascent training | Djeumou et al. 2022, Alg. 1 | 3 | Pre-existing — validated |
| N3-Djeumou | Semi-supervised dissipativity on unlabelled points | Djeumou et al. 2022, Sec. IV | 3, 4 | INVESTIGATE — needs dataset |
| N1-Liu | RK4 rollout loss | Liu et al. 2024, Sec. III-A | — | REJECT — conflicts with RNEA path |
| N2-Liu | FrictionNet diagonal Cholesky dissipativity | Liu et al. 2024, Sec. III-B | 3 | **MERGED** — `network/friction_net.py` |
| N3-Liu | Lyapunov PD gains (Kp = Kd²/4) | Liu et al. 2024, Prop. 1 | 2 | **MERGED** — `controller/lyapunov_gains.py` |
| N4-Liu | --max_samples data-efficiency ablation | Liu et al. 2024, Sec. IV-B | 1 | **MERGED** — `training/dataset.py` |
| N1-Duong | L L^T + εI Cholesky kernel | Duong et al. 2024, Sec. II-C | 3 | Folded into N2-Liu FrictionNet |
| N3-Duong | 100-step frozen-backbone sim-to-real fine-tuning | Duong et al. 2024, Sec. IV-D | 4 | **MERGED** — `training/fine_tune.py` |
| N1-SPEL | Revolute-joint sparsity mask → diagonal D | Wang et al. 2025, Sec. II-B | 3 | Folded into N2-Liu FrictionNet |
| N1-WangCAC | Sobol sampling for excitation trajectories | Wang et al. 2024 | 1 | INVESTIGATE — needs data pipeline |
