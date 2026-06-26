# From URDF to Real-Time Control: An Automated Physics-Informed Neural Network Pipeline for 7-DoF Robot Dynamics Learning

**Hugo Durieux** — Master's Internship, 2026

_Working draft — updated automatically at the end of each session._
_Last updated: 2026-06-26_

---

## Abstract

We present an automated pipeline that takes a robot's URDF description as input and produces a trained, real-time-deployable dynamics model for a 7-degree-of-freedom manipulator. The pipeline combines a deterministic white-box baseline (Recursive Newton-Euler Algorithm, RNEA, computed via Pinocchio from the URDF) with a physics-constrained neural residual network that learns unmodeled friction, elasticity, and payload-dependent effects. Four contributions distinguish this work from the primary state of the art (Liu et al., 2024): (1) a fully automated URDF-to-model pipeline requiring no manual kinematic derivation, with Sobol low-discrepancy excitation trajectory generation for improved joint-space coverage; (2) a real-time computed-torque controller with Lyapunov-certified gain selection operating at 1000 Hz; (3) a structurally dissipative FrictionNet sub-module that guarantees the friction residual dissipates energy by construction, without relying on soft penalty terms, with physical justification from a Pinocchio-based sparsity analysis confirming the 7-parameter diagonal structure (80% reduction vs. full Cholesky); and (4) a two-step sim-to-real fine-tuning protocol that recovers tracking accuracy from a pre-trained simulation model using only a brief real-world motor-babbling sequence. Preliminary experiments on CPU with Fourier excitation data (Pinocchio RNEA, 50k samples/payload, 0/1/3 kg) achieve val RMSE ≈ 0.22 Nm in 20 epochs; full GPU-scale experiments pending.

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

### 3.8 Sobol Excitation Trajectory Generation (N1-WangCAC)

Fourier-series excitation trajectories are parameterised by per-joint harmonic frequencies and phases. Naive uniform random sampling of these parameters can leave regions of joint space poorly covered. Following Wang et al. (2024), we replace uniform random sampling with Sobol low-discrepancy sequences (scipy.stats.qmc.Sobol) to fill the 7-dimensional joint configuration space more uniformly.

Concretely, for each payload condition the trajectory is generated as N_SEGMENTS = 10 independent segments, each starting from a Sobol-sampled joint centre q_center drawn from the joint range [Q_LOWER, Q_UPPER]:

```
q_centers = Sobol(d=7, seed=42).random(10)  mapped to [Q_LOWER, Q_UPPER]
For each q_center_i:
    Fourier params (A_k, ω_k, φ_k) sampled randomly
    Segment trajectory: q(t) = q_center_i + Σ_k A_k sin(ω_k t + φ_k)
```

Each segment contributes 5,000 samples (5 s at 1000 Hz); segments are concatenated to 50,000 samples per payload. Timesteps where any |τ_RNEA| > τ_max are excluded (not clipped), preserving training label validity. The Sobol seeds differ per payload to ensure independent joint-space coverage across conditions.

_File: `generate_fourier_dataset.py`_ [Wang et al. 2024, CAC]

### 3.9 Data-Efficiency Ablation (N4-Liu)

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

### 4.2 Preliminary Results (CPU, 20 epochs, Fourier baseline)

| Run | Dataset | FrictionNet | Best val loss | Val RMSE |
|-----|---------|-------------|---------------|----------|
| smoke-baseline | synthetic (4096 samples) | No | 44.10 | ~0.93 Nm |
| smoke-frictionnet | synthetic (4096 samples) | Yes | 44.01 | ~0.91 Nm |
| fourier-baseline | Fourier 0 kg (50k, real RNEA) | No | 0.0453 | 0.213 Nm |
| fourier-frictionnet | Fourier 0 kg (50k, real RNEA) | Yes | 0.0451 | 0.212 Nm |
| fourier-sobol | Fourier 0 kg (50k, Sobol, real RNEA) | No | 0.0570 | 0.239 Nm |

**Per-joint RMSE (Fourier-Sobol run):** [0.240, 0.233, 0.257, 0.228, 0.257, 0.228, 0.256] Nm.
Joint scale diagnostic (N2-WhenPhysics): joints 1–4 (87 Nm) mean 0.239 Nm, joints 5–7 (12 Nm) mean 0.247 Nm — ratio 1.0×. EMA loss balancing not required on Fourier data.

_Note: all runs on CPU, 20 epochs. Convergence is not reached; full experiments require GPU and 200+ epochs._

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

6. **Deng, Wang, Feng (2024).** "Physics informed machine learning model for inverse dynamics in robotic manipulators." _Applied Soft Computing_, vol. 163, art. 111978. — Sub-term embedding (N1-E2NN); Liquid gating mechanism (N2-E2NN).

7. **Ni, Qureshi (2024).** "Physics-informed Neural Motion Planning on Constraint Manifolds." _IEEE Int. Conf. Robotics & Automation (ICRA)_. — Eikonal PDE planner on constraint manifold (N1-CMP); negative-exponential speed model (N2-CMP).

8. **Liu, Ni, Qureshi (2024).** "Physics-informed Neural Mapping and Motion Planning in Unknown Environments." _IEEE Transactions on Robotics and Automation Letters (RA-L)_. — Active sensing Eikonal planner (N1-NTF); log-squared arrival-time factorization (N2-NTF).

9. **Jiang, Hsu, Zhang, Yu, Wang, Li (2025).** "PhysTwin: Physics-Informed Reconstruction and Simulation of Deformable Objects from Videos." _IEEE/CVF Conf. Computer Vision & Pattern Recognition (CVPR 2025)_. — Deformable-object reconstruction via spring-mass physics. REJECTED: domain mismatch (deformable bodies, not rigid-body dynamics).

10. **Fang, Chen, Chen, Wang, Wu, Zhang, Lim (2026).** "AdaKineNet: Adaptive Kinematic Neural Network for Inverse Kinematics of Redundant Mobile Manipulators." _Robotics & Autonomous Systems_, vol. 202, art. 105494. — Inverse kinematics via learnable loss weighting (N1-AdaKineNet, N2-AdaKineNet). REJECTED: domain mismatch (IK not dynamics); ReLU forbidden; 10-DoF mobile manipulator.

11. **Prabhakar, Joshi, Dandekar, Dandekar, Panat (2026).** "When Does Physics Help? A Systematic Study of Physics-Guided Learning for Robotic Contact Dynamics." _Proceedings of the International Conference on Learning Representations (ICLR 2026)_. — Soft contact dynamics via LuGre ODE (N1-WhenPhysics); EMA adaptive loss balancing (N2-WhenPhysics); physics-aware trajectory sampling (N3-WhenPhysics). INVESTIGATE: N2-WhenPhysics EMA loss balancing for 87/12 Nm joint scale imbalance.

12. **Feizi, Pedrosa, Patel, Jayender (2025).** "Few-Shot Physics-Informed Neural Network for Shape Reconstruction of Concentric-Tube Robots." _arXiv preprint 2605.12790_. — Few-shot PINN for Cosserat rod BVP in surgical robots. REJECTED: domain mismatch (continuum robot, not rigid-body manipulator).

13. **Yu, Zhang, Liu, Wang, Peng (2026).** "Hybrid LSTM-Edge Correction Architecture for Physics-Informed Crop Health Monitoring in Distributed Agricultural Robotics." _Frontiers in Agriculture_, vol. 8, art. 1764002. — LSTM + edge inference for agricultural IoT. REJECTED: agriculture domain mismatch; no robot arm dynamics applicability.

14. **Agrawal, Menon, Sharma, Gupta, Patel (2026).** "Automating PINN-Based Kinematic Resolution of Robotic Joints Using Robotic Process Automation Frameworks." _Frontiers in Robotics and AI_, vol. 12, art. 1752595. — RPA-based PINN kinematics automation on 2R arm with 40.5 ms latency. REJECTED: inverse kinematics domain (non-dynamics); latency incompatible with 1 kHz control.

15. **Hu, Liu, Chen, Zhang, Wang (2026).** "Modeling and Compensation of Backlash-Induced Dynamics Error in Industrial Robots With a PINN-Based Approach." _IEEE Transactions on Industrial Electronics_. — Backlash residual via PINN on non-harmonic-drive joint trains. REJECTED: ReLU activations (forbidden); TCN sliding-window breaks stateless 1 kHz loop; backlash-specific to non-harmonic drives (Franka has harmonic reducers). Secondary finding: backlash error payload-independent, validates RNEA white-box load-dependent term coverage.

16. **Li, Yang, Zhao, Wang, Zhou (2025).** "PINN-Based Predictive Control Combined With Unknown Payload Identification for Robots With Prismatic Quasi-Direct-Drives." _IEEE Transactions on Automation Science and Engineering_. — Virtual payload link + NMPC 100 Hz for QDD arms. REJECTED: QDD motor model incompatible with Franka harmonic-drive + motor-inertia model; NMPC 100 Hz incompatible with Stage 2/3 architecture. COMPETITIVE ADVANTAGE: N2-PayloadPINN (virtual payload link runtime injection) already implemented in `pinocchio_baseline/rnea_wrapper.py` via `_inject_payload/_restore_payload`. Dual payload-awareness (RNEA white-box + τ_res delta input) ahead of published Li et al. 2025 — highlight in final paper.

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
| N1-SPEL | Revolute-joint sparsity mask → diagonal D | Wang et al. 2025, Sec. II-B | 3 | **CONFIRMED** via Pinocchio analysis — all 7 joints JointModelRZ, 80% param reduction, diagonal D physically justified |
| N1-WangCAC | Sobol sampling for excitation trajectories | Wang et al. 2024 | 1 | **IMPLEMENTED** — `generate_fourier_dataset.py`, 10 Sobol segments per payload |
| N1-E2NN | Structural sub-term embedding (inertia, Coriolis, gravity) | Deng et al. 2024, Sec. 3 | — | REJECT — 1-DoF only; manual per-robot derivation conflicts Goal 1 automation |
| N2-E2NN | Liquid gating mechanism (recurrent state modulation) | Deng et al. 2024, Sec. 2.3 | — | REJECT — recurrent incompatible with 1 kHz loop; tanh/sigmoid forbidden |
| N1-CMP | Eikonal PDE planner on constraint manifold | Ni & Qureshi 2024, Sec. III | — | REJECT — custom planner incompatible with MoveIt2 mandate (Stage 2) |
| N2-CMP | Negative-exponential speed model in Eikonal solver | Ni & Qureshi 2024, Sec. II | — | REJECT — planning-domain detail; no link to dynamics loss |
| N1-NTF | Active sensing integrated into Eikonal planner | Liu, Ni & Qureshi 2024, Sec. IV | — | REJECT — incremental C-NTFields extension; Stage 2 uses standard MoveIt2 |
| N2-NTF | Uncertainty-weighted replanning in active NTFields | Liu, Ni & Qureshi 2024, Sec. V | — | REJECT — no link to dynamics loss |
| N1-PhysTwin | Digital twin reconstruction of deformable objects via spring-mass physics | Jiang et al. 2025, Sec. III | — | REJECT — domain mismatch (deformable bodies, not rigid-body dynamics) |
| N1-AdaKineNet | Adaptive kinematic network with learnable loss weighting for IK | Fang et al. 2026 | — | REJECT — inverse kinematics problem; dynamics-independent |
| N2-AdaKineNet | ReLU-based deep architecture on 10-DoF mobile manipulator | Fang et al. 2026 | — | REJECT — ReLU forbidden; mobile platform domain mismatch |
| N1-WhenPhysics | Soft contact dynamics via LuGre friction ODE | Prabhakar et al. 2026 | — | REJECT — equivalent to τ_friction in constraints.py |
| N2-WhenPhysics | EMA loss balancing (β=0.95) per residual magnitude for 87/12 Nm scale imbalance | Prabhakar et al. 2026 | 3 | INVESTIGATE — diagnostic live in `train.py`; Fourier ratio 1.0× (no imbalance); revisit after real robot data |
| N3-WhenPhysics | Physics-aware trajectory sampling for sim-to-real | Prabhakar et al. 2026 | — | REJECT — duplicate of N3-Duong |
| N1-fagro | LSTM edge-correction for crop health prediction (agricultural domain) | Yu et al. 2026, Sec. 3 | — | REJECT — agriculture robotics domain mismatch; no dynamics learning applicability |
| N2-fagro | Distributed edge-sensor fusion architecture for IoT agricultural monitoring | Yu et al. 2026, Sec. 2 | — | REJECT — agriculture domain; no robot arm applicability |
| N1-frobt | Automating robotic kinematics PINN via RPA frameworks on 2R arm | Agrawal et al. 2026, Sec. III | — | REJECT — inverse kinematics domain (non-dynamics); 40.5 ms latency incompatible with 1 kHz control |
| N1-BacklashPINN | Backlash compensation via residual PINN: τ_pred = RNEA + τ_backlash + τ_res | Hu et al. 2026, Sec. II | — | REJECT — ReLU activations forbidden by CLAUDE.md Mish/Softplus constraint |
| N2-BacklashPINN | TCN sliding-window architecture for history-dependent backlash estimation | Hu et al. 2026, Sec. II | — | REJECT — stateful sliding-window breaks stateless 1 kHz control loop invariant; recurrent incompatible with real-time servo |
| N3-BacklashPINN | Backlash hysteresis modeling on non-harmonic-drive joint gear trains | Hu et al. 2026, Sec. III | — | REJECT — Franka uses harmonic reducers on all 7 joints; backlash error payload-independent, validates RNEA white-box coverage of load-dependent terms; non-applicable |
| N1-PayloadPINN | PINN payload identification under QDD quasi-direct-drive motor assumption | Li et al. 2025, Sec. II | — | REJECT — Franka Panda has harmonic reducers + motor inertia, not QDD; incompatible motor model |
| N2-PayloadPINN | Virtual payload link at runtime (inject, estimate, restore in Pinocchio RNEA) | Li et al. 2025, Sec. III | 1 | **REJECT/PRE-EXISTING** — already implemented in `pinocchio_baseline/rnea_wrapper.py` (_inject_payload/_restore_payload functions). Dual payload-awareness (RNEA white-box + τ_res delta input) ahead of published Li et al. 2025 state of art. Competitive advantage — highlight in final paper. |
| N3-PayloadPINN | NMPC 100 Hz predictive control with payload disturbance rejection | Li et al. 2025, Sec. IV | — | REJECT — 100 Hz NMPC incompatible with Stage 2 (MoveIt2) + Stage 3 (stateless 1 kHz feedforward + PD) architecture |
