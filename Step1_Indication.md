# Methodology of Pillar 1: Physics-Informed Dynamics Modeling Pipeline (Grey-Box)

Pillar 1 establishes the physical intelligence of the system. Its objective is to automatically generate a highly accurate dynamic model (an "Oracle") for a robotic manipulator by merging deterministic classical mechanics with the adaptability of deep learning.

This grey-box architecture is generated and trained offline through a sequential five-step pipeline, detailed below with their governing equations.

## 1. Data Generation and Excitation Simulation (Isaac Sim)
To map the physical limits of the robot, the neural network must be exposed to a comprehensive spectrum of dynamic states.
* **Process:** Optimal excitation trajectories, typically based on Fourier series, are executed in a high-fidelity physics simulator (e.g., NVIDIA Isaac Sim). These trajectories simultaneously excite the 7 degrees of freedom at varying velocities and accelerations.
* **Payload Variation:** The payload mass ($\delta$) is dynamically altered during simulation to capture load-dependent inertia.
* **State Vector & Ground Truth:** The process yields a massive dataset where each sample $i$ contains the kinematic state, the payload, and the measured real-world electrical torque:
  $$X^{(i)} = \left[ q^{(i)}, \dot{q}^{(i)}, \ddot{q}^{(i)}, \delta^{(i)} \right], \quad Y^{(i)} = \tau_{real}^{(i)}$$

## 2. Analytical Foundation (White-Box via Pinocchio)
The architecture delegates known physical laws (gravity, Coriolis forces, inertia) to a deterministic mathematical solver, ensuring the AI does not waste capacity relearning classical mechanics.
* **Process:** The robot's structural definition (URDF file) is loaded into a rigid-body dynamics library (Pinocchio).
* **Computation:** For every data point, the Recursive Newton-Euler Algorithm (RNEA) computes the theoretical ideal torque ($\tau_{RBD}$):
  $$\tau_{RBD} = M(q)\ddot{q} + C(q,\dot{q})\dot{q} + G(q)$$
  *(Where $M$ is the inertia matrix, $C$ the Coriolis/centrifugal matrix, and $G$ the gravity vector).*

## 3. Neural Corrector Architecture (Black-Box via PyTorch)
A neural network is designed to exclusively learn the "residual dynamics"—the discrepancy between perfect theory and mechanical reality (e.g., non-linear friction, elasticity, wear).
* **Preprocessing:** To ensure spatial continuity and prevent wrapping singularities (the $360^\circ$ jump), joint angles ($q$) are mapped to trigonometric representations:
  $$x_{in} = \left[ \sin(q), \cos(q), \dot{q}, \delta \right]$$
* **Prediction:** A Multi-Layer Perceptron (MLP) with smooth, differentiable activation functions (e.g., Mish) processes $x_{in}$ to predict the residual torque ($\tau_{res}$), parameterized by weights $\theta$:
  $$\tau_{res} = f_{\theta}(x_{in})$$
* **Architecture Output:** The final prediction fuses the analytical and learned components:
  $$\tau_{pred} = \tau_{RBD} + \tau_{res}$$

## 4. Physics-Informed Training (PINN Loss Formulation)
The optimization of the network weights $\theta$ is governed by a composite loss function ($\mathcal{L}_{total}$) that enforces strict compliance with mechanical constraints.
$$\mathcal{L}_{total} = \mathcal{L}_{data} + \lambda_{smooth}\mathcal{L}_{smooth} + \lambda_{phys}\mathcal{L}_{phys}$$
* **Data Fidelity ($\mathcal{L}_{data}$):** Minimizes the Mean Squared Error (MSE) between the total predicted torque and the measured torque:
  $$\mathcal{L}_{data} = \frac{1}{N} \sum_{i=1}^{N} \left\| \tau_{pred}^{(i)} - \tau_{real}^{(i)} \right\|_2^2$$
* **Kinematic Smoothness ($\mathcal{L}_{smooth}$):** Penalizes high-frequency variations (jerk) in the residual prediction to prevent actuator vibrations:
  $$\mathcal{L}_{smooth} = \frac{1}{N} \sum_{i=1}^{N} \left\| \nabla_t \tau_{res}^{(i)} \right\|_2^2$$
* **Safety Constraint ($\mathcal{L}_{phys}$):** An Augmented Lagrangian penalty that exponentially sanctions predictions exceeding the manufacturer's maximum torque limits ($\tau_{max}$) for each joint $j$:
  $$\mathcal{L}_{phys} = \sum_{j=1}^{7} \max\left(0, |\tau_{pred, j}| - \tau_{max, j}\right)^2$$

## 5. Resolution of Simulation Bias (Sim-to-Real Fine-Tuning)
The final step bridges the reality gap between the simulated physics and the actual physical hardware.
* **Process:** The network, pre-trained on millions of simulated data points ($\theta_{sim}$), has its initial layers frozen. It undergoes fine-tuning using a small dataset of real-world physical sensor data ($D_{real}$).
  $$\theta^* = \arg\min_{\theta} \mathcal{L}_{total}(\theta, D_{real})$$
* **Benefit:** Guided by the physics-informed loss function, the network safely adapts to the unique mechanical signature of the physical robot (e.g., temperature-dependent grease friction) without overfitting to real-world sensor noise.