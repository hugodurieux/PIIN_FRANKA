# Scientific and Technical Contributions: Physics-Informed Dynamics and Control Framework

While recent literature establishes the theoretical viability of Physics-Informed Neural Networks (PINNs) and grey-box modeling for robotic dynamics, transferring these concepts into applied, real-time industrial robotics remains a challenge. 

This project bridges the gap between theoretical physics-informed machine learning and high-performance robotic control. The proposed framework introduces four major contributions to the state-of-the-art:

## 1. Automated "URDF-to-Model" Pipeline
Current research often relies on manually derived mathematical equations hardcoded for specific robotic platforms. This project introduces a generalized, plug-and-play software infrastructure.
* **Mechanism:** The framework accepts any standard Universal Robot Description Format (URDF) file as input. It automatically extracts the kinematic tree using rigid-body dynamics libraries (e.g., Pinocchio), generates the corresponding PyTorch neural network architecture, orchestrates excitation trajectories in a physics simulator (e.g., Isaac Sim), and outputs a trained dynamic model.
* **Impact:** It democratizes the use of grey-box PINNs by removing the need for manual, robot-specific mathematical derivation, allowing researchers to generate highly accurate dynamic oracles for any manipulator automatically.

## 2. High-Frequency Real-Time Control (1000 Hz MPC Integration)
Most existing literature evaluates PINN accuracy exclusively offline or on pre-recorded datasets. 
* **Mechanism:** This research embeds the trained PINN directly into a Model Predictive Control (MPC) solver operating at 1000 Hz. The MPC algorithm continuously queries the PyTorch-based grey-box model multiple times within a single millisecond to simulate future states and select the optimal torque command.
* **Impact:** Achieving microsecond-level inference times for a neural network embedded inside an optimization loop proves that grey-box architectures are not just theoretical modeling tools, but viable, stable, and computationally lightweight solutions for real-time robotic control.

## 3. Scaling to High-Dimensional Systems (7-DoF)
Fundamental proofs of concept for Physics-Informed Neural Networks (such as Lagrangian Neural Networks) are frequently validated on low-dimensional, simple systems like inverted pendulums or 2-axis arms.
* **Mechanism:** This framework applies Augmented Lagrangian constraints and residual friction learning to a highly complex, non-linear, 7-Degree-of-Freedom (7-DoF) industrial manipulator (the Franka Panda) operating in 3D space. 
* **Impact:** Successfully converging the optimization of a PINN loss function over a highly complex Coriolis and inertia matrix demonstrates that physics-informed architectures can scale to handle the dimensionality and non-linearity required by modern industrial robotics.

## 4. Standardized Resolution of the Sim-to-Real Gap
Transferring policies from simulation to physical hardware consistently degrades performance due to unmodeled real-world phenomena (e.g., temperature-dependent friction, actuator wear).
* **Mechanism:** The framework integrates a systematic two-step training methodology. The model undergoes massive pre-training in simulation to learn the foundational dynamics, followed by a constrained fine-tuning phase using brief recordings of real-world "motor babbling." 
* **Impact:** The physics-informed loss function acts as a robust filter during the fine-tuning phase. It prevents the neural network from overfitting to real-world sensor noise, effectively neutralizing the Sim-to-Real gap and resulting in a highly accurate, deployable physical model.