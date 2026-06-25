Robotics and Autonomous Systems 202 (2026) 105494
Contents lists available at ScienceDirect
Robotics and Autonomous Systems
journal homepage: www.elsevier.com/locate/robot
AdaKineNet: Adaptive Kinematic Neural Network for inverse kinematics of
redundant mobile manipulators
Shihui Fanga, Min Chena,*, Yaran Chena, Jia Wanga, Jinghua Wub, Zhihua Zhangc,
Eng Gee Lima
aSchool of Advanced Technology, Xi’an Jiaotong-Liverpool University, Suzhou, 215123, China
bHefei Institutes of Physical Science, Chinese Academy of Sciences, Hefei, 230088, China
cRobotics Laboratory, Changzhou Institute of Advanced Manufacturing Technology, Changzhou, 213164, China
A R T I C L E I N F O A B S T R A C T
Keywords: Redundant mobile manipulators offer superior operational flexibility for logistics and warehousing applications,
Redundant manipulator however, their inverse kinematics (IK) solutions remain challenged by singularity susceptibility, computational
Inverse kinematics inefficiency, and physical infeasibility in conventional approaches. This paper introduces the Adaptive Kinematic
Deep learning algorithms Neural Network (AdaKineNet)—an adaptive physics-informed neural network (PINN) that integrates rigid-body
Physics-informed neural networks
transformations via automatic differentiation to achieve exact Jacobian evaluation. A dynamically weighted loss
function balances positional accuracy, orientation precision, and joint constraints, while a modular architecture
supports scalable deployment of manipulators with varying degrees of freedom through a unified parametric
framework. Experimental validation on a 10-DoF mobile manipulator demonstrates significant improvements:
positional and orientation errors are substantially reduced compared to numerical IK solvers and data-driven
baselines, and joint-limit violations remain near negligible levels. The framework achieves real-time inference
speeds, outperforming iterative methods by orders of magnitude, with accelerated convergence via adaptive
gradient optimization. These advances establish AdaKineNet as an industrially viable IK solver, ensuring both
physical feasibility and computational efficiency for safety-critical complex robotic control tasks, such as
container unloading and agile manufacturing.
1. Introduction leading to significant joint updates, oscillatory behavior, or failure to
converge [6]. Moreover, in dynamic environments requiring real-time
Redundant mobile manipulators, which combine high-degree-of- replanning (typically <50 ms per control cycle), optimization-based IK
freedom (DoF) robotic arms with mobile platforms, are widely used in approaches often struggle to produce feasible solutions within the
logistics automation, warehouse handling, and container unloading available time budget, owing to the non-convexity and high dimen-
tasks [1,2]. Their extended workspace and task flexibility make them sionality of the configuration space [3,10]. Their applicability is limited
ideal for unstructured environments and complex object manipulation. in dynamic logistics settings where fast, reliable, and physically feasible
However, solving the inverse kinematics (IK) for such systems remains a solutions are required.
core challenge due to their redundancy, sensitivity to singularities, and In response to these challenges, recent work has increasingly
the mechanical constraints that must be satisfied in real-time [3–5]. explored data-driven approaches as a practical alternative to traditional
Traditional analytical IK methods such as closed-form solutions, analytical methods. Deep neural networks, including feedforward,
Jacobian-based iterations, and optimization-based techniques are convolutional, and recurrent architectures, have demonstrated strong
commonly applied to industrial manipulators. While numerical iterative performance on inverse-kinematics tasks for conventional 6-DoF or 7-
solvers (Newton-Raphson or Levenberg-Marquardt) are commonly used, DoF fixed-base manipulators. However, they often lack explicit phys-
they exhibit critical instability in singularity-dense scenarios typical of ical priors needed to guarantee safe and physically feasible motions in
logistics tasks. Specifically, as the manipulator approaches wrist-lock or novel or redundant configurations [7–9]. A notable failure case occurs
elbow-lock singularities, the Jacobian matrix becomes ill-conditioned, when these networks extrapolate to unseen workspace regions, they
* Corresponding author.
E-mail address: Min.Chen@xjtlu.edu.cn(M. Chen).
https://doi.org/10.1016/j.robot.2026.105494
Received 25 October 2025; Received in revised form 3 April 2026; Accepted 22 April 2026
Available online 24 April 2026
0921-8890/© 2026 Elsevier B.V. All rights are reserved, including those for text and data mining, AI training, and similar technologies.

S. Fang et al. R o b o t ic s a n d A u t o n o m o u s S y s t e m s 202 (2026) 105494
frequently predict joint configurations that are mathematically valid for optimal parameter combination. Combined with adaptive gradient
the end-effector pose but physically impossible, resulting in clipping and domain decomposition, this mechanism accelerates
self-collisions or violations of joint limits (predicting an angle of 190◦for convergence and substantially reduces joint limit violations and
a joint limited to 180◦ [12,13]. Unlike analytical methods that inher- orientation drift in complex trajectories.
ently respect geometry, pure deep learning models often exhibit 3) A physics-informed dataset pipeline combining stratified workspace
"orientation drift," where the end-effector position is accurate, but the sampling, singularity filtering and collision-aware augmentation is
orientation vector deviates significantly from the target due to the lack developed to ensure kinematic diversity and physical feasibility.
of rotational constraints in the loss function [7,10]. Trained on this dataset, AdaKineNet was validated on a physical 10-
In addition, optimization-augmented approaches such as adaptive DoF mobile manipulator prototype across warehouse unloading
particle swarm optimization (APSO) improve positional accuracy but tasks, demonstrating stable, constraint-compliant trajectory plan-
are vulnerable to Jacobian ill-conditioning in singularity-prone regions ning suitable for industrial deployment.
[10]. Hybrid methods, such as Fusion IK, which combine evolutionary
algorithms with neural networks, improve efficiency but fail to enforce This paper is organized as follows: Section 2 formulates the kine-
the physical priors required to maintain joint compliance and orienta- matics and inverse-kinematics problem for the 10-DoF mobile manipu-
tion tracking [11]. Overfitting and poor generalization to novel trajec- lator. Section 3 details the AdaKineNet architecture, emphasizing its
tories or geometries remain persistent issues [12,13]. physics-constrained layers and adaptive optimization mechanisms.
To address the issue of physical interpretability in data-driven Section 4evaluates the performance of AdaKineNet through compara-
methods, researchers have integrated neural networks with explicit tive analysis, systematic simulation, and real-robot experiments. Section
system dynamics models, giving rise to physics-informed neural net- 5discusses broader applications in flexible manufacturing and disaster
works (PINNs). PINNs demonstrate promise in balancing computational response, while outlining future research directions.
efficiency with kinematic feasibility [14–17]. The KineNN framework
introduces a modular architecture that enables adaptation to different 2. Problem formulation
robotic configurations by resizing the network, facilitating
cross-platform deployment without retraining [18]. By eliminating the A 10-DoF mobile manipulator comprising a planar mobile base (3
need for post-processing steps such as trajectory correction, DoF), a linear vertical extension (1 DoF), and a 6-DoF manipulator arm
physics-informed frameworks help ensure mechanical safety, particu- is intentionally adopted to reflect industrial container-unloading and
larly when manipulating fragile or delicate payloads [19]. This flexi- warehouse handling scenarios where (i) workspace extension via base
bility contrasts with traditional numerical IK solvers, which are prone to motion and linear axes interacts nontrivially with arm kinematics, (ii)
failure in singularity-dense scenarios, and purely data-driven models, redundancy amplifies singularity and coupling effects, and (iii) real-
which often lack physical plausibility and generalization capacity [13]. time, physically feasible IK is required across a broad workspace, as
Nonetheless, existing PINN architectures still face challenges in gener- illustrated in Fig. 1[20]. A lower-DOF, fixed-base arm would not expose
alizing across diverse robot geometries and dynamic payload conditions. these cross-coupled effects (base yaw and arm Jacobian, extension, and
Their reliance on predefined kinematic templates or static hyper- reachability) that motivate our physics-informed, modular design.
parameters often limits adaptability in real-world logistics scenarios. Importantly, AdaKineNet’s modular encoder-decoder supports
This motivates the development of a more flexible, constraint-aware, straightforward reduction to lower-DOF configurations (by removing
and real-time PINN framework for high-degree-of-freedom mobile corresponding modules or neurons) without redesign, enabling
manipulators. cross-platform transferability, however, demonstrating performance on
These limitations highlight a critical gap: the absence of a universal the representative 10-DoF setup provides a stronger stress test of scal-
IK solver that balances physical consistency, adaptability, and real-time ability and constraint enforcement (see Sections 3 and 4.1.1).
performance. Therefore, this study develops a universal inverse kine- The forward kinematics of the whole system maps the joint config-
matics (IK) solver, Adaptive Kinematic Neural Network (AdaKineNet), uration vector q∈R10, which includes all actuated DoFs of the manip-
for redundant mobile manipulators in logistics, addressing the limita- ulator and the mobile platform, to the end-effector pose xee ∈R6,
tions of conventional methods in balancing physical consistency with defined by the 3D position and orientation of the tool centre point in Eq.
computational efficiency. AdaKineNet eliminates post-processing for (1).
trajectory correction, ensuring mechanical feasibility in handling fragile
payloads. Modular designs enable rapid adaptation to diverse robotic
xee =f(q) (1)
geometries by adding or removing neurons, facilitating knowledge By taking the time derivative of Eq. (2), the mapping from joint ve-
transfer across manipulators without costly retraining. Generalization locities to end-effector velocities is obtained:
and robustness by encoding rigid body transformations and joint con-
straints, AdaKineNet avoids overfitting to training data, ensuring reli- x˙ ee =J(q)⋅q˙ (2)
able performance in unseen scenarios such as cluttered workspaces or
here, q˙ ∈R10 denotes the vector of joint velocities, and J(q)∈R6×10
dynamic obstacles. This contrasts with traditional numerical IK solvers,
denotes the geometric Jacobian relating joint-space velocities to task-
which struggle with singularity-rich configurations, and with purely
space end-effector velocities [21,22].
data-driven models, which lack physical consistency. The key contri-
The inverse kinematics problem is to compute a joint configuration q
butions of this study can be summarized as follows:
such that the end-effector attains the target pose xtarget ∈R6. This is
1) This paper introduces AdaKineNet, an adaptive PINN framework that formulated in the form of a constrained optimization that integrates
directly embeds rigid-body transforms and computes Jacobians via data-driven objectives and physical constraints, as shown in Eq. (3).
automatic differentiation to guarantee Jacobian consistency and q ∗=argmin‖xee (cid:0) xtarget ‖2+λ 1 L jac +λ 2 L bound (3)
robustness to singularities. The architecture produces real-time, q
physically consistent inverse kinematics solutions for high-DoF mo- In this formulation, λ 1 and λ 2 are task-dependent scalar weights,
bile manipulators without costly symbolic derivations. while L jac and L bound are physics-based regularization terms ensuring
2) Based on the AdaKineNet model, a loss function with adaptive
kinematic consistency and joint limit compliance, respectively. This
weighting mechanisms is proposed to dynamically balance posi-
formulation supports generalizable, physically informed IK solutions in
tional accuracy, orientation precision, and joint limits using learn-
high-dimensional configuration spaces. Since inverse kinematics for
able parameters to auto-optimize objective weights to achieve the
2

S. Fang et al.                                                                                                                                                                                    R  o  b  o  t ic  s   a  n  d    A  u  t o n  o  m   o u  s   S  y  s t e  m  s  202 (2026) 105494
Fig. 1. Kinematic model representation of the 10-DoF mobile manipulator.
redundant manipulators is inherently multi-valued, Eq. (3) is not  The Jacobian matrix of the entire system is constructed by concate-
interpreted as recovering a unique global inverse. Instead, it selects one  nating the Jacobians of the mobile platform and the manipulator:
| physically feasible solution branch that satisfies the target pose and the  |     |     |     |     |     | J=[Jbase | ]   |     |     |      |
| --------------------------------------------------------------------------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | ---- |
|                                                                             |     |     |     |     |     | Jarm     |     |     |     | (7)  |
imposed constraints, the Jacobian-consistency and joint-limit regulari-
zation terms discourage averaged or physically invalid outputs. The  ∈R6×3 models the platform’s translational contribution
where, Jbase
| p r im a r y   o | b je c t i v e  t e r m |   m i n i m iz es  t h e  C | a rt e s ia n  t r a c k i | n g  e r r o r  b | e t w e en   |            | ×                     |                          |                            |                                  |
| ---------------- | ----------------------- | --------------------------- | -------------------------- | ----------------- | ------------ | ---------- | --------------------- | ------------------------ | -------------------------- | -------------------------------- |
|                  |                         |                             |                            |                   |              | a n d  J ∈ | R 6 7  r e p r e se n | t s  t h e   c o m b i n | e d  e f fe c t   o f   th | e   li n e ar   a x i s  a n d   |
| th e  p r e d i  | c te d   e n d - e ff e | c t or   p o se  x an d     |  t h e  t a rg e t   p o s | e  x .  T         | h e   co m - | ar m       |                       |                          |                            |                                  |
ee   ta r ge t a r m   jo i nt s,  w h ich   a r e  d e ri v e d   u s i n g  a u t o m a ti c  d i f f e r e n ti a t io n  t o   e n s u r e
| ponents L         | and L                                                    | serve as physics-informed regularization  |     |     |     |                                                                   |     |     |     |     |
| ----------------- | -------------------------------------------------------- | ----------------------------------------- | --- | --- | --- | ----------------------------------------------------------------- | --- | --- | --- | --- |
|                   | jac                                                      | bound                                     |     |     |     | singularity-free operation [24].                                  |     |     |     |     |
| terms. Briefly, L | jac enforces the differential kinematic relationship (x˙ |                                           |     |     |     |                                                                   |     |     |     |     |
|                   |                                                          |                                           |     |     | ee  | The inverse-kinematics problem for the 10-DoF mobile manipulator  |     |     |     |     |
=J(q)⋅q˙) to maintain Jacobian consistency and stabilize the solver near
is formulated as a constrained optimization that balances task-space
singularities. Meanwhile, L
bound  utilizes a soft-penalty formulation to
accuracy with physics-based regularizers, as described in Eq. (3),
strictly constrain the joint configuration within its mechanical bound-
while the unified system Jacobian underpins manipulability and sin-
| aries [q | ,q ]. The detailed mathematical derivations and imple- |     |     |     |     |     |     |     |     |     |
| -------- | ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
min max gularity analysis. Current analytical solutions are intractable for such
mentations of these regularization terms are presented in Section 3.2.
tightly coupled, high-DoF systems and numerical solvers suffer insta-
To express velocities consistently between the robot-local frame and
bility near singularities, these limitations motivate a learned solver that
| the world frame, planar twists are represented as 3 × |     |     |     | 1 vectors x˙ = |     |     |     |     |     |     |
| ----------------------------------------------------- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- |
[ ] enforces kinematic consistency and constraint compliance by design.
| ,vy ,ω | ⊤∈R3, where vx | ,vy are linear velocities and ω |     |               |     |     |     |     |     |     |
| ------ | -------------- | ------------------------------- | --- | ------------- | --- | --- | --- | --- | --- | --- |
| vx     | z              |                                 |     | z is the yaw  |     |     |     |     |     |     |
rate. The mapping from the robot frame to the world frame uses a 3 ×3  3. Methodology
| homogeneous rotation matrix R(θ)∈R3×3  |     |     | with the following block  |     |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- |
structure as shown in Eq. (4).
To address the inverse-kinematics challenges of tightly coupled,
| [   | ]   | [   | ]   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
( θ ) θ (cid:0) θ redundant mobile manipulators, this paper proposes AdaKineNet, a
| R(θ)= R | 2 02 ×1 | , (θ)= c o s | s i n |     |     |     |     |     |     |     |
| ------- | ------- | ------------ | ----- | --- | --- | --- | --- | --- | --- | --- |
R2 θ θ (4)  modular physics-informed neural architecture. Section 3 outlines the
|     | 0 1 × 2 1 | s in | c o s |     |     |     |     |     |     |     |
| --- | --------- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- |
technical components and implementation details required to reproduce
To express the planar velocity of the robot in the world frame, a 2D  the method: Section 3.1describes the encoder–decoder architecture and
rotation matrix R(θ)∈R3×3 is applied, where θ is the base yaw angle,  module interfaces used to represent varying DoF, Section 3.2formalizes
and x˙ r denotes the velocity in the robot’s local frame, as shown in Eq.  the physics-informed loss terms and the adaptive weighting mechanism,
(5).  Section  3.3 presents  dataset  generation,  training  procedure,  and
implementation details (automatic differentiation for forward kine-
x˙ =R(θ)⋅x˙
w r (5)  matics / Jacobians and adaptive optimization settings). The subsequent
Thus, both x˙ r and x˙ w are 3 ×1 vectors, and this statement clarifies  Section 4reports numerical and hardware evaluations that quantify the
R3×3
that  the  2 × 2 planar  rotation is  embedded  in  only for  efficacy of these design choices.
homogeneous-twist bookkeeping, the last row or column preserves the
yaw rate unchanged.
|     |     |     |     |     |     | 3.1. Architecture of AdaKineNet for inverse kinematics |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------------------------------------ | --- | --- | --- | --- |
Denote the world-to-base (mobile platform) homogeneous transform
| base(q | ), the fixed transform from base to arm root by T |     |     |     | ar m |     |     |     |     |     |
| ------ | ------------------------------------------------- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
by T w base b a se  AdaKineNet  is  designed  as  a  learning-based,  physics-informed
(constant), and the manipulator forward-kinematics from arm joint  framework that generalizes across robot configurations by combining
angles q to the end-effector by data-driven function approximation with embedded robotic priors.
arm
Tee (q )∈SE(3). The world-to-end-effector transform is therefore:  Instead of deriving explicit IK equations, AdaKineNet learns a differen-
arm
tiable mapping, as shown in Eq. (8).
| T ee(q)=T | base(q )T ar | m Tee (q )                                |     |     | (6)  |                    |     |     |     |      |
| --------- | ------------ | ----------------------------------------- | --- | --- | ---- | ------------------ | --- | --- | --- | ---- |
| w         | w base b     | a se arm                                  |     |     |      |                    |     |     |     |      |
|           | [            | ]                                         |     |     |      | ̂ (cid:0)1:xtarget |     |     |     |      |
|           |              | ⊤                                         |     |     |      | f ↦q̂              |     |     |     | (8)  |
| Where, q= | q⊤ ,         | q⊤ is the full system configuration and q |     |     | ∈    |                    |     |     |     |      |
|           | base         | arm                                       |     |     | arm  |                    |     |     |     |      |
R6 denotes the joint angles of the manipulator arm [23]. Any additional
where inverse kinematics refers to the problem of determining a feasible
(⋅)for brevity.
fixed tool transforms are included inside Tee joint configuration q̂∈R10 that produces a desired end-effector pose
3

S. Fang et al. R o b o t ic s a n d A u t o n o m o u s S y s t e m s 202 (2026) 105494
xtarget ∈R6,consisting of both position and orientation. of ReLU supports the requirement for real-time inference latency (<50
AdaKineNet is trained to minimize both cartesian task error and ms), while its induced sparsity aids in learning robust feature repre-
physical inconsistency. By incorporating forward kinematics, Jacobian sentations for the high-dimensional configuration space. Optional
consistency, and joint limit enforcement into its loss formulation, Ada- dropout is included for regularization. Residual connections are inte-
KineNet avoids the brittleness of numerical IK solvers while maintaining grated to improve gradient propagation and training stability. The ar-
physical plausibility and safety. As illustrated in the structural schematic chitecture is designed to be modular and adaptable to various robot
in Fig. 2, the architecture of the proposed AdaKineNet comprises three morphologies and task scenarios.
interconnected core modules: the Data-driven model, the Governing For trajectory-based IK tasks, the MLP outputs a time-dependent
Equations, and the Optimization Process. (1) The Data-driven model is joint configuration q̂(t)∈R10, which represents the continuous evolu-
a deep neural network (DNN) encoder-decoder that maps task-space tion of the mobile manipulator’s full joint state. A decoder module re-
inputs X (target poses or trajectories) to predicted joint-space configu- constructs these trajectories from the latent representation learned by
rations q. (2) The Governing Equations module embeds the physical the network, producing smooth joint motions that realize the specified
laws of the mobile manipulator. It receives the predicted joint configu- end-effector path. To ensure physical consistency throughout the mo-
rations q to compute the forward kinematics and precise analytical de- tion, the framework embeds kinematic ordinary differential equation
rivatives (Jacobian matrices J(q)) via automatic differentiation. These (ODE) constraints via the system Jacobian J(q̂(t))∈R6×10. Specif-
computations generate the physical residuals required to enforce kine- ically, the model enforces the differential kinematics relationship in Eq.
matic feasibility and boundary constraints. (3) The Optimization (9).
Process integrates these residuals into a hybrid loss function. An
adaptive weighting mechanism dynamically balances the data-driven
x˙(t)=J(q̂(t))⋅q̂˙
(t) (9)
and physics-informed loss terms, and the TPE (Tree-structured Parzen
Estimator) optimizer systematically updates the network parameters η across all time steps t, ensuring that joint velocities produce consistent
end-effector velocities.
to minimize the overall objective. This figure delineates the complete
high-level information flow from input to weight update, serving as a
Additionally, temporal bounda(cid:0)ry )conditions, such as fixed initial or
roadmap for the explicit mathematical formulations detailed in the final configuration q̂(t0 ) = q 0 , q̂ tf = q f , are imposed to guarantee
subsequent subsections. feasibility and smooth transitions. This integration of spatial and tem-
AdaKineNet integrates a deep neural network (DNN) encoder- poral priors allows AdaKineNet to handle both point-to-point IK and
decoder with physics-based constraints. The DNN maps task-space tra- continuous motion generation with a unified and physically grounded
jectories to joint-space solutions, while embedded Jacobian relation- architecture.
ships ensure kinematic feasibility [25]. Singularity metrics and mitigation. Automatic differentiation pro-
The input to AdaKineNet consists of either a static target pose vides accurate numerical Jacobian entries, which improves gradient fi-
xtarget ∈R6 or a time-dependent end-effector trajectory x(t)∈R6. Both delity during training, but it does not change the singular-value
spectrum of the Jacobian J(q) nor eliminate rank-deficient kinematic
represent the desired task-space motion in terms of 3D position and
states. To make the treatment of singularities precise and reproducible,
orientation. When applicable, additional joint-space information such as
initial joint configuration q ∈R10 or motion context descriptors (e.g., the following metrics and mitigation strategies are introduced.
0
obstacle proximity, payload type) can be concatenated to the input
(i) Singularity or proximity metrics. Singularity is measured by prox-
vector. Because a single task-space target may correspond to multiple
imity using standard quantities: Yoshikawa manipulability in Eq.
admissible joint configurations, AdaKineNet is trained to predict one
(10).
feasible solution branch rather than to enumerate all possible IK solu-
√̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅
tions. When available, the initial joint configuration q 0 and motion- w(q)= det(J(q)J(q)⊤) (10)
context descriptors are concatenated to the input vector to disambig-
uate branch selection and reduce solution ambiguity.
The input is processed by a deep multilayer perceptron (MLP), which
serves as the core of AdaKineNet. This neural module consists of several
fully connected layers. Rectified Linear Unit (ReLU) activations are the smallest singular value σ min (J(q)), and the condition number κ(J) =
employed for the hidden layers specifically to mitigate the vanishing σ max /σ min. In practice, configurations are flagged as near singular if
gradient problem inherent in training deep networks with physics-based σ min (J)<σ th (we used σ th =10(cid:0)3 in data filtering for the experiments
derivative constraints. Furthermore, the low computational complexity
reported here) or equivalently if w(q)<wth. These thresholds are
Fig. 2. Architecture of the proposed AdaKineNet for inverse kinematics.
4

S. Fang et al.                                                                                                                                                                                    R  o  b  o  t ic  s   a  n  d    A  u  t o n  o  m   o u  s   S  y  s t e  m  s  202 (2026) 105494
reported explicitly in Section 3.3.2and can be adjusted for other robot  automatic differentiation [27].
geometries.
∑ N
|                                                                    |     |     |     |     |     |       | 1 ‖x˙ |               | )q˙ ‖2 |     |     |       |
| ------------------------------------------------------------------ | --- | --- | --- | --- | --- | ----- | ----- | ------------- | ------ | --- | --- | ----- |
|                                                                    |     |     |     |     |     | L jac | =     | i (cid:0) J(q |        |     |     | (13)  |
|                                                                    |     |     |     |     |     |       | N     |               | i i 2  |     |     |       |
| (ii) Mitigation strategies. Our approach combines three pragmatic  |     |     |     |     |     |       | i= 1  |               |        |     |     |       |
elements:
where J(q)is computed in real-time via automatic differentiation from
i
forward kinematics, eliminating explicit analytical derivations. This
1) Data filtering or augmentation. During dataset construction, grossly
singular configurations (as above) are excluded to avoid training on  term ensures the consistency of the predicted Jacobian matrix with the
physically degenerate examples, low-manipulability examples are  kinematic model. The Jacobian consistency loss requires paired velocity
samples (q˙,x˙). Although the core dataset is built from pose samples,
also augmented for robustness experiments (see Section 4.3).
2) Loss  regu(cid:0)la(cid:0)rizatio)n).  A  manipulability  penalty  velocity pairs are generated reproducibly by constructing short micro-
L (q)=1/ w q2+ϵ is included in the physics-informed loss to  trajectories around sampled configurations. Concretely, for a given
sing
accepted configuration q(i), a small neighboring configuration q(i,+)=
discourage low-manipulability solutions when task performance
|           |       |                     |             | Λ        |          | q(i)+Δq is sampled where Δq is a random perturbation drawn from  |                                                                         |     |     |     |     |     |
| --------- | ----- | ------------------- | ----------- | -------- | -------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------- | --- | --- | --- | --- | --- |
| permits.  | This  | term  is  weighted  | adaptively  | by  the  | network  |                                                                  |                                                                         |     |     |     |     |     |
|           |       |                     |             |          |          | U((cid:0)                                                        | δ,δ)per joint and scaled to respect joint limits and collision checks.  |     |     |     |     |     |
described in Section 3.2.
Using a fixed artificial time-step Δt (Δt=10 ms is used in training by
3) Numerical damping in deployment. When inverting or pseudo-
inverting J, Tikhonov or damped least-squares regularization is  default), finite-difference velocities are computed by central or forward
applied in Eq. (11).  differences as appropriate in Eq. (14).
|     |     |     |     |     |     |     |     |     | (   |     | )   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:0) )
| † = | ⊤ ⊤+λ2I | (cid:0)1 |     |     |       |      |                    |       |           | (q(i,+))(cid:0)1xee (q(i)) |     |       |
| --- | ------- | -------- | --- | --- | ----- | ---- | ------------------ | ----- | --------- | -------------------------- | --- | ----- |
| J λ | J JJ    |          |     |     | (11)  |      | q(i,+)(cid:0) q(i) | Log   | SE(3) xee |                            |     |       |
|     |         |          |     |     |       | q˙ ≈ |                    | ,x˙ ≈ |           |                            |     | (14)  |
|     |         |          |     |     |       |      | Δt                 |       |           | Δt                         |     |       |
(⋅)produces the 6D twist vector (translational and rota-
|     |     |     |     |     |     | where Log | SE(3) |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | ----- | --- | --- | --- | --- | --- |
where λ is cho(cid:0)sen ada)ptively based on the local singular-value spectrum  tional rates). For trajectory data (when available), velocity estimates are
(e.g., λ=λ / σ +ϵ with small ϵ>0), this yields numerically more  computed using central differences across successive time steps. A small
|     | 0 min |     |     |     |     |     |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
amount of zero-phase lowpass filtering (Butterworth, cutoff 50 Hz) is
stable updates near singularities.
applied to reduce numerical noise before loss computation. These
By unifying data-driven learning with kinematic principles, AdaKi-
choices are implementation parameters, sensitivity to δ and Δt is re-
neNet provides a structured approach to solving inverse kinematics,
ported in the ablation section (Section 4.3).
| particularly  | suited  | for  redundant  | manipulators  | where  traditional  |     |     |     |     |     |     |     |     |
| ------------- | ------- | --------------- | ------------- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
methods struggle with complexity and singularities. The Jacobian consistency loss itself is implemented as Eq. (15).
∑
|     |     |     |     |     |     |     | 1 N ve | l             | (cid:0) )       |     |     |       |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------------- | --------------- | --- | --- | ----- |
|     |     |     |     |     |     | L   | =      | ‖x˙(k)(cid:0) | J q (k) q˙(k)‖2 |     |     | (15)  |
jac N
| 3.2. Physical-informed loss function design of AdaKineNet |     |     |     |     |     |     | vel k = | 1   |     |     |     |     |
| --------------------------------------------------------- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
where J(q)
The loss function design in AdaKineNet integrates physics-informed  is computed via automatic differentiation of the forward-
(q). This loss enforces local kinematic consis-
constraints  and  adaptive  optimization  mechanisms  to  ensure  kinematics mapping xee
singularity-free solutions, physical feasibility, and real-time perfor- tency between the network’s predicted mappings and the instantaneous
mance for redundant mobile manipulators. The framework comprises  velocity relation.
three core components: data-driven loss, physics-constrained regulari- Joint angle boundary conditions ensure that the predicted joint an-
zation, and adaptive weighting mechanisms, which are detailed below. gles respect the physical limits of the joints, and the joint limit penalty
The data-driven loss term measures the mean squared error of the  imposes smooth constraints on joint angles using the Softplus regulari-
neural network’s predicted joint angles and the target end-effector po- zation [28], as shown in Eq. (16).
|                 |       |           |                       |           | =        |     | ∑N  | ∑10 [ | (   | )   | ( )] |     |
| --------------- | ----- | --------- | --------------------- | --------- | -------- | --- | --- | ----- | --- | --- | ---- | --- |
| s ition  [26].  | F or  | a  given  | target  end-effector  | position  | xtarget  |     | 1   |       |     |     |      |     |
[ ] L = softplus qi,j (cid:0) qm ax +softplus qm in(cid:0) qi,j (16)
|     | T   |     |     |     |     | bound | N   |     |     | j   | j   |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
p ,Rtarget and the corresponding predicted end-effector pose xpred  i=1 j=1
target
| [   | ]   |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
= ,Rpred T where qi,j is the j-th joint angle of the i-th sample, qm in and qm ax
| p   | , this loss term can be expressed as Eq. (12).  |     |     |     |     |     |     |     |     |     | j   | j  are  |
| --- | ----------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- |
pred
mechanical limits. This term enforces the boundary conditions on the
|     | ∑ ( |     |     | )   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1 N ‖2 j o i n t   a n g l e s  a n d   t h e  f o rm u la tion avoids gradient discontinuities caused
| L = | ‖pi | (cid:0) pi | ‖2 +‖Ri (cid:0) Ri |     | (12)  |     |     |     |     |     |     |     |
| --- | --- | ---------- | ------------------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
data 2 N pred target 2 pred target F b y   t r a d i ti o n a l  s t e p   fu n c tio n s.
i= 1
The final total loss function is the weighted sum of the above terms, a
| where pi | and Ri |     |     |     |     |     |     |     |     |     |     |     |
| -------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
pred  are the predicted position and rotation matrix for  learnable  weighting  strategy  dynamically  balances  multi-objective
pred
the i-th sample. It is worth noting that while the geodesic distance on  optimization during training [29], as shown in Eq. (17).
SO(3)represents the intrinsic rotational error, its gradient calculation  =λ +λ +λ
|     |     |     |     |     |     | L total | 1 L data | 2 L | jac 3 L | bound |     | (17)  |
| --- | --- | --- | --- | --- | --- | ------- | -------- | --- | ------- | ----- | --- | ----- |
involves an inverse cosine function, which suffers from singularity
| (infinite gradient) as the error approaches zero. Therefore, the Frobenius  |     |     |     |     |     | where λ | ,λ ,λ |                                                          |     |     |     |     |
| --------------------------------------------------------------------------- | --- | --- | --- | --- | --- | ------- | ----- | -------------------------------------------------------- | --- | --- | --- | --- |
|                                                                             |     |     |     |     |     |         | 1 2   | 3 are weighting factors generated by a lightweight sub-  |     |     |     |     |
norm is adopted as a computationally efficient and numerically stable  network that balance the contributions of the different loss terms. Un-
surrogate for training. Minimizing the Frobenius norm monotonically  like static hyperparameters, these coefficients are computed in real time
reduces the geodesic error, ensuring convergence without the risk of  based on the homoscedastic uncertainty for each task. Specifically, the
gradient explosion typically associated with direct geodesic optimiza- sub-network inputs the vector of gradient standard deviations as shown
tion [34]. This term guarantees precise mapping from joint space to  in Eq. (18), which is computed over the current mini batch.
| Cartesian space. |     |     |     |     |     |     | [    | (cid:0) | )     | ]      |     |     |
| ---------------- | --- | --- | --- | --- | --- | --- | ---- | ------- | ----- | ------ | --- | --- |
|                  |     |     |     |     |     | =   | σ(∇L | ),σ ∇L  | ,σ(∇L | ) T∈R3 |     |     |
The physical constraint loss terms ensure that the solution adheres to  st data jac bound (18)
kinematic equations (Jacobian relations) and joint angle boundary
|     |     |     |     |     |     | The architecture of Λ |     |     | consists of a fully connected layer with 16  |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | -------------------------------------------- | --- | --- | --- |
conditions, as shown in Eq. (12). The Jacobian Matrix constraint ensures  ϕ
hidden units using ReLU activation, followed by an output layer with a
that the predicted joint angles satisfy the Jacobian relationship via
5

S. Fang et al.                                                                                                                                                                                    R  o  b  o  t ic  s   a  n  d    A  u  t o n  o  m   o u  s   S  y  s t e  m  s  202 (2026) 105494
Softmax activation function as shown in Eq. (19).  configuration s pace, each  joint variable qj is sampled from a uniform
|     |     |     |     |     |     |     |     | (   | )   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[λ ,λ ,λ ]T=Softmax(W2 ⋅ReLU(W1 ⋯ +b1 )+b2 ) distribution U qm in,qm ax defined by its mechanical limits. Using these
| 1 2 3 |     |     | t   |     |     | (19)  |     | j   | j   |     |     |
| ----- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
∑ joint  variables,  the  corresponding  end-effector  pose  x=
| This Softmax normalization ensures that  |     |     |     | 3   | λ =1 preventing  |     |     |     |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- |
i=1 i [x,y,z,ϕ,θ,ψ]⊤∈R6 is computed via the forward kinematics function
gradient explosion. By learning to attenuate the weights of loss terms
f(q), where x,y,z represent the position and ϕ,θ,ψ the orientation in
with high variance (high uncertainty) and increase the weights of stable
roll, pitch, yaw format. To characterize the set of achievable end-effector
terms, this mechanism eliminates the need for manual hyperparameter  orientations at a fixed Cartesian position x∗, multiple kinematic solu-
tuning and adapts to scenarios involving high-precision tracking or
tions are generated via Jacobian nullspace perturbations. For a reference
obstacle avoidance, such as unloading tasks. =x∗, the right nullspace basis N(q
|     |     |     |     |     |     |     | solution q   | satisfying xee                                 | (q ) |     | )of the  |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ---------------------------------------------- | ---- | --- | -------- |
|     |     |     |     |     |     |     |              | 0                                              | 0    |     | 0        |
|     |     |     |     |     |     |     | Jacobian J(q | )is computed. Joint-space perturbations Δq=N(q |      |     | )v are   |
|     |     |     |     |     |     |     |              | 0                                              |      |     | 0        |
3.3. Training framework and dataset generation sampled with v∼U((cid:0) δ,δ)r (r=nullity), and then projected onto the
feasible joint limits and collision-free set. The feasible perturbed joint
3.3.1. AdaKineNet training algorithm configurations are collected as q =q +Δq. For each feasible q, the
|             |                                                    |     |     |     |     |     |     |     | i 0 |     | i   |
| ----------- | -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Algorithm 1 | implements adaptive gradient clipping to mitigate  |     |     |     |     |     |     |     |     |     |     |
end-effector orientation is represented as a unit quaternion. In this way,
| gradient  | instability  | and  accelerate  | convergence  | [30].  | The  | hyper- |     |     |     |     |     |
| --------- | ------------ | ---------------- | ------------ | ------ | ---- | ------ | --- | --- | --- | --- | --- |
multiple valid joint configurations corresponding to the same Cartesian
parameters in Table 4are optimized using the Optuna-TPE framework  target x∗are retained in the dataset, enabling the network to learn the
[31], which significantly reduces the number of training iterations  multi-solution structure of redundant inverse kinematics.
compared to conventional training schemes while maintaining solution  ˉ
The orientation samples are summarized by the quaternion mean q
| accuracy [32]. |     |     |     |     |     |     |                             |     | ∑                                        |     |     |
| -------------- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | ---------------------------------------- | --- | --- |
|                |     |     |     |     |     |     | (principal eigenvector of S |     | = qiq⊤ ) and the RMS angular dispersion  |     |     |
|                |     |     |     |     |     |     |                             |     | i i                                      |     |     |
as shown in Eq. (20).
3.3.2. Dataset generation
√̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅
| The dataset generation process plays a pivotal role in training Ada- |     |     |     |     |     |     |     | √     |     |     |     |
| -------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
|                                                                      |     |     |     |     |     |     |     | √ ∑ M | ˉ   |     |     |
K i n e N e t  t o   s ol v e   th e   i n v e rs e  k i n e m a t i c s  o f  r e d u n d a n t   m o b i l e   m a n i p u - σ = √ 1 (2arccos(|〈qi ,q 〉|))2
|                 |                 |                       |              |                           |                |                 | θ   |      |     |     | (20)  |
| --------------- | --------------- | --------------------- | ------------ | ------------------------- | -------------- | --------------- | --- | ---- | --- | --- | ----- |
| la t o r s.   O | u r   m e t h o | d o l o g y   e m p h | a s iz e s   | t w o   c r it ic a l   a | s p ec t s :   | e n h a n c e d |     | M i= |     |     |       |
1
workspace coverage through stratified sampling strategies, and rigorous
physical consistency enforcement during data augmentation. ˉ  ˉ
|     |     |     |     |     |     |     | where qand σ | θ are used in figures: qis plotted as a small coordinate  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --------------------------------------------------------- | --- | --- | --- |
The original dataset was generated using the forward kinematic
frame at the workspace point and σ
θ is visualized via a color map indi-
| equations mentioned in Section 2. First, a set of random joint configu- | [   |     |     | ]   |     |     |        |                           |                                |     |     |
| ----------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | ------ | ------------------------- | ------------------------------ | --- | --- |
|                                                                         |     |     |     | ⊤   |     |     | cati n | g   l o c a l  o rie nt a | t io n   v a r i ab i l it y . |     |     |
ra t i o n s   q = x , y ,θ , h , θ , θ , θ , θ ,θ , θ ∈ R 10  i s   g e n e ra t e d ,  w h e r e   { }
b b b l 1 2 3 4 5 6 A   t o t a l  o f  N = 2 0 , 0 0 0   jo i n t  c o n fi gurations  q(i) N are generated via
x , y , θ  d en o t e  t h e  p l a n a r  p o s i t io n  a n d  o r i e n ta ti on  o f  t h e   m o b i le   b as e ,  h i=1
| b b b |     |     |     |     |     |     | l   |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
is the linear actuator extension, and θ ,θ ,…,θ 6 are the joint angles of  a  U n if o r m  M o n te   C a r l o   sa m p l in g   o v e r  t h e   f e a si b le   c o n fi g u ra t io n   sp a c e
|             |               |     | 1       | 2                      |     |          | R   |                        |                                        |                            |                               |
| ----------- | ------------- | --- | ------- | ---------------------- | --- | -------- | --- | ---------------------- | -------------------------------------- | -------------------------- | ----------------------------- |
|             |               |     |         |                        |     |          | C ⊂ | 1 0 .  Th is  s to c h | a s t i c  a p pr o a c h   m i ti g a | t e s   th e   cu r s e  o | f  d i m e n si o n al i ty   |
| the  6-DoF  | manipulator.  | To  | ensure  | unbiased  exploration  |     | of  the  |     |                        |                                        |                            |                               |
Algorithm 1
AdaKineNet training procedure.
1: Input:
| Training dataset D |     | ={X,y}(end-effector poses and joint angles) |     |     |     |     |     |     |     |     |     |
| ------------------ | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2:                 |     | train                                       |     |     |     |     |     |     |     |     |     |
3:  Validation dataset D
val
4:  Physics module P (forward kinematics and Jacobian computation)
| Hyperparameters: epochs T, initial learning rate η, adaptive weight bounds [λ |     |     |     |     |     | ,λ  | ]   |     |     |     |     |
| ----------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5:                                                                            |     |     |     |     |     | min | max |     |     |     |     |
6: Output:
7:  Trained AdaKineNet model parameters θ∗
8: Initialize
9: Set random seed, configure device and logging.
| 10: Fit and save normalizer (scaler) on D |     |     | train (input / output scaling). |     |     |     |     |     |     |     |     |
| ----------------------------------------- | --- | --- | ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
11: Initialize model components: encoder fenc, decoder fdec, adaptive-weight network Λ, physics module P.
12: Initialize optimizer (AdamW) and learning-rate scheduler.
13: for epoch =1 to T(cid:0) do
)
| 14:  for each batch Xb |                                    | ,yb ∈D t(cid:0)rain do) |     |     |     |     |     |     |     |     |     |
| ---------------------- | ---------------------------------- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 15:  Xn                | ,yn ← sc(cid:0)aler. tran)sform Xb |                         | ,yb |     |     |     |     |     |     |     |     |
| 16:  qpred             | ←fdec fenc                         | (Xn )                   |     |     |     |     |     |     |     |     |     |
17:  Jacobian J calculation:
18:  if physics computations are performed in physical units, then
| 19:  | qphys  ← scaler. inverse transform (qpred) |     |     |     |     |     |     |     |     |     |     |
| ---- | ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20:  | J ← P. Jacobian (qphys)                    |     |     |     |     |     |     |     |     |     |     |
| 21:  | else J ← P. Jacobian (qpred)               |     |     |     |     |     |     |     |     |     |     |
22:  Loss components computation:
| 23:  | L data  ← position error term |     |     |     |     |     |     |     |     |     |     |
| ---- | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
L ← Jacobian / kinematic consistency term
| 24:  | jac                                            |     |     |     |     |     |     |     |     |     |     |
| ---- | ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 25:  | L ← joint-limit (cid:0)/ regula)rization term] |     |     |     |     |     |     |     |     |     |     |
boun[d
| 26:  | ∇ ←E(∇L      | ),Var∇L      | ,E(∇L | )     |     |     |     |     |     |     |     |
| ---- | ------------ | ------------ | ----- | ----- | --- | --- | --- | --- | --- | --- | --- |
|      | stats        | data         | jac   | bound |     |     |     |     |     |     |     |
| 27:  | λ ,λ jac∑ ,λ | ←Λ(∇ stats ) |       |       |     |     |     |     |     |     |     |
|      | data bound   |              |       |       |     |     |     |     |     |     |     |
| 28:  | L ←          | λ L          |       |       |     |     |     |     |     |     |     |
total i i
| 29:  | Optimizer. zero grad (), | L total.backward() |     |     |     |     |     |     |     |     |     |
| ---- | ------------------------ | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Clip gradients (threshold =grad clip thresh),optimizer. step()
30:
31: end for
| 32: scheduler. step() as configured,evaluate on D |     |     |     | → L ,log validation metrics |     |     |     |     |     |     |     |
| ------------------------------------------------- | --- | --- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- |
val  val
| 33: Save checkpoint if L                                 |     | val improved (use L | val for early stopping/model selection) |     |     |     |     |     |     |     |     |
| -------------------------------------------------------- | --- | ------------------- | --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| 34: returnθ∗←checkpointwithbestvalidationperformance(byL |     |                     |                                         |     | )   |     |     |     |     |     |     |
val
6

S. Fang et al. R o b o t ic s a n d A u t o n o m o u s S y s t e m s 202 (2026) 105494
associated with the 10-DoF system, avoiding the combinatorial explo- hardware configuration and a robust software environment, which are
sion associated with grid-based sampling (e.g., 1010 samples for 10 integral to the successful implementation of our proposed methodology.
discretization levels per joint). This feasible space C is strictly defined The hardware configuration of the mobile manipulator platform
by joint angle limits qmin<q <qmax and collision-avoidance con- utilized in this study is composed of the following key components, as
i i i
straints, ensuring that each sampled configuration q(i) is kinematically shown in Fig. 3. The FR07 mobile line-controlled chassis serves as the
and physically valid. Singularity detection employs a multi-threshold foundational structure, providing mobility and stability essential for
algorithm to reject kinematically degenerate configurations. Although navigating various operational environments. The DELTA-ECM-AL3-
N=20,000 might appear limited for high-dimensional supervised C20807 linear module is integrated into the system to facilitate pre-
learning, it is sufficient for AdaKineNet. By embedding the exact kine- cise linear motion, enhancing the manipulator's ability to execute tasks
matics and Jacobian consistency into the loss function, the model is accurately. The AUBO-i10 collaborative robotic arm is employed for its
continuously regularized by physical laws, enabling strong generaliza- versatility and safety features, making it suitable for tasks that involve
tion from sparse samples through physics-informed gradients. Conse- interaction with human operators. The ASP130×240.AFZ-H3 integrated
quently, AdaKineNet relies on physical gradients rather than dense vacuum gripper is utilized as the end-effector, enabling effective
discrete data points alone, drastically reducing the required sample handling and manipulation of a variety of objects during operational
complexity. tasks.
This rigorous sampling of the feasible configuration space provides This combination of hardware components allows the redundant
the foundational dataset required for robust redundancy resolution and mobile manipulator to perform complex tasks efficiently while ensuring
multi-solution handling. Specifically, a fundamental challenge in 10- high levels of precision and safety. The experiments were conducted in a
DoF redundant manipulators is the ill-posed nature of mapping a sin- GPU-accelerated training environment to optimize the computational
gle task-space target to an infinite manifold of valid joint configurations. performance of the AdaKineNet. The experiments were conducted on a
To prevent the 'mode averaging' phenomenon inherent in standard laptop model PIRM15NU, equipped with an Intel Core i7–10750H CPU
regression-based IK solvers—where the model predicts the non-physical operating at 2.60 GHz. This powerful processor is capable of handling
mean of multiple valid modes—AdaKineNet reformulates the mapping the intensive computations required for neural network training and
as a physics-constrained multi-objective optimization task. Formulating kinematic simulations. The system is equipped with an NVIDIA Quadro
the training objective with automatically differentiated Jacobian and P620 GPU, which significantly enhances the speed of training and
forward kinematics yields a continuous, differentiable energy landscape. inference processes, allowing for efficient handling of large datasets and
The physics-informed terms, L jac and L bound, act as structural regu- complex model architectures. Specific software tools are utilized in the
larizers that resolve the redundancy by penalizing proximity to kine- experiments, ensuring transparency and reproducibility. These tools
matic singularities and joint boundaries. Consequently, rather than include libraries and frameworks essential for implementing neural
learning a stochastic multi-valued mapping, the network is guided to networks and conducting kinematic analyses, which are critical for the
converge toward a unique, consistent, and smooth trajectory within the successful application of the AdaKineNet approach. This comprehensive
redundancy manifold that implicitly adheres to the minimum-norm hardware and software configuration provides a solid foundation for
criterion, guaranteeing physical validity. conducting experiments, enabling a thorough evaluation of the pro-
posed method's effectiveness in addressing the inverse kinematics
challenges associated with redundant mobile manipulators.
4. Experiments and results
4.1.2. Dataset generation
4.1. Experimental design
A physics-informed dataset generation pipeline was established to
train AdaKineNet with kinematically diverse and physically valid sam-
4.1.1. Experimental setup
ples. An initial set of 20,000 joint configurations was created using
The experimental setup for evaluating the performance of AdaKi-
Monte Carlo sampling within the feasible configuration space, defined
neNet in solving the inverse kinematics of redundant mobile manipu-
by joint limits and collision-avoidance constraints. Workspace bound-
lators is detailed in this section. The setup comprises a carefully selected
Fig. 3. Hardware and software architecture of the experimental redundant mobile manipulator platform.
7

S. Fang et al. R o b o t ic s a n d A u t o n o m o u s S y s t e m s 202 (2026) 105494
aries are enforced: mobile platform coordinates satisfy 1.5m≤xb ≤ 3.1.
1.5m, (cid:0) 1.5m≤yb ≤1.5m, and the linear actuator height is con- Position Accuracy (RMSE), Euclidean distance between the pre-
strained within 0.1m≤hl ≤1.5m. Fig. 4visualizes the resulting distri- dicted and reference end-effector positions, as shown in Eq. (21) [33].
bution of 20,000 end-effector positions and orientations across the √ √ ̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅
robo A t ’ p s h o y p s e ic r s a - t i i n o f n o a rm l w ed o r s k a s m pa p c l e in . g strategy was developed to address the RMSEpos = √ √ N 1 ∑N ‖p ( p i r ) e (cid:0) p ( r i e ) f ‖2 (21)
i=1
inherent challenges of redundant mobile manipulator kinematics that
systematically enhance workspace coverage. Workspace sampling where p∈R3 denotes the end-effector position measured in millimeters
employed a structured 3D grid comprising 12 ×12 ×8 cells, supple-
(mm), and N represents the number of samples.
mented by 12 discrete base orientations and four actuator height offsets.
Orientation error, is computed using the geodesic distance on the
As shown in Fig. 5, the enhanced dataset achieves 15.44% greater
special orthogonal group SO(3) between the predicted and reference
c
fr
o
o
n
m
ve
7
x
8
h
.2 u
9
ll
%
vo
t
l
o
u m
93
e
. 7
co
3
v
%
er
.
a
E
g
n
e
d
c
-e
o
f
m
fe
p
c
a
to
re
r
d
p o
to
s e
t
s
h
w
e o
e
r
r
i
e
g
c
in
o
a
m
l
p
ra
u
n
te
d
d
o m
via
s a
fo
m
r
p
w
l
a
in
rd
g orientations. Let Rref ,Rest ∈SO(3) and Rerr =R⊤
ref
Rest. The orientation
error is shown in Eq. (22) [34].
kinematics, and invalid samples were filtered using multi-threshold ( )
s in in c g re u a la se ri d t y o r d i e e t n e t c a t t i i o o n n , d w i h ve ic r h si t e y l i b m y i n 1 a 1 t . e 1 d % 4 . 1.4% of infeasible states, and θ err =cos (cid:0)1 trace(R 2 err )(cid:0) 1 (22)
As summarized in Table 1, this dataset generation framework en-
sures kinematic diversity while eliminating singularities, providing a with θ is converted to degrees.
robust foundation for training AdaKineNet and enabling reliable inverse Joint-limit violation rate, a critical quantitative measure of the
kinematics learning across diverse configurations. network's intrinsic 'failure rate' with respect to physical feasibility. It is
defined as the percentage of inverse kinematics solutions exceeding
4.1.3. Adaptive hyperparameter optimization mechanical joint constraints, as shown in Eq. (23) [35]. It is important to
This study employs the Optuna framework to implement adaptive clarify that while any physically infeasible solutions would be strictly
hyperparameter tuning, utilizing the Tree-structured Parzen Estimator discarded or clamped by low-level safety controllers during practical
(TPE) algorithm for efficient exploration of the parameter space. The hardware deployment, monitoring this raw violation rate is essential for
objective of optimization is to minimize the validation loss of algorithm evaluation. It directly indicates how effectively the learning
AdaKineNet. architecture has internally encoded the mechanical priors (via the
To improve optimization efficiency, a median-based pruning strat- L bound loss term) compared to standard data-driven baselines, which
egy was employed to terminate underperforming trials early. Specif- frequently generate invalid configurations that would disrupt contin-
ically, no pruning was applied during the initial five trials and the first uous real-time control.
t
e
e
v
n
a l
t
u
r
a
a
t
i
i
n
o
i
n
n
.
g steps of each trial, ensuring sufficient exploration before
ViolationRate(%)= 1
∑N
1
{
∃j:q (i)
〈
qminorq (i)
〉
qmax
}
× 100% (23)
N j j j j
This approach effectively reduced unnecessary computational over- i=1
head. The hyperparameter search process also incorporated dynamic
adjustment of the parameter distribution based on historical perfor- where q ( j i) denotes joint j at sample i, qm j in,qm j axare joint limits, and 1{⋅}
mance, which directed the search toward regions with higher potential. is the indicator function.
Table 2lists the hyperparameter search spaces used in the Optuna TPE
optimization. After completing 150 trials, the optimal set of hyper-
4.2. Real-robot metrics
parameters was identified and is summarized in Table 3.
Position tracking error (PTerr), defined as the root-mean-square
4.1.4. Evaluation metrics
error (RMSE) between the estimated end-effector position obtained
To rigorously assess the effectiveness of AdaKineNet in solving the
from forward kinematics and the ground-truth position measured by the
inverse kinematics problem of redundant mobile manipulators, four
motion capture system, as shown in Eq. (24).
evaluation metrics are introduced, reflecting physical feasibility, √̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅
√
c
c
o
o
m
nv
p
e
u
n
t
t
a
io
ti
n
o
a
n
l
a l
e v
e
a
ffi
lu
c
a
ie
ti
n
o
c
n
y ,
p
a
ra
n
c
d
t i
i
c
n
e
d
s,
u s
t
t
h
r
e
ia
f
l
r
a
a
p
m
p
e
l
w
ic
o
a
r
b
k
il i
i
t
s
y .
a l
C
ig
o
n
n
e
si
d
s t
w
en
it
t
h
w
t
i
h
th
e PTerr=
√
√ N 1
∑N
‖pe e s e t(tk )(cid:0) pg ee t(tk )‖2 2 (24)
physics-informed dataset generation methodology outlined in Section k=1
Fig. 4. Spatial distribution of end-effector positions and orientations within the operational workspace (20,000 samples).
8

S. Fang et al.                                                                                                                                                                                    R  o  b  o  t ic  s   a  n  d    A  u  t o n  o  m   o u  s   S  y  s t e  m  s  202 (2026) 105494
Fig. 5. Comparison of configuration metrics between original and enhanced datasets.
metric.
Table 1
Task success rate: fraction of trials that reached the final waypoint
Statistical comparison of original and enhanced datasets. =10 mm.
within position tolerance rtol
| Metric | Original Enhanced | Improvement |     |     |     |     |
| ------ | ----------------- | ----------- | --- | --- | --- | --- |
Failure taxonomy, failures categorized as No-solution, Collision,
Workspace Coverage (%) 78.29 93.73 15.44% Timeout, Non-convergence, or Singularity.
Singular Configurations (%) 41.41 0.00 100% These definitions are used to compute the entries in Table 6(Section
Position Diversity (std) 0.609 0.612 0.49% 4.4). Measured values will be provided in the revised submission.
| Orientation Diversity (std) | 1.126 1.251 | 11.10% |     |     |     |     |
| --------------------------- | ----------- | ------ | --- | --- | --- | --- |
4.3. Comparative analysis
Table 2
4.3.1. Performance benchmarks
Parameter space definition.
AdaKineNet is evaluated against a standard numerical IK solver and
| Metric | Parameters | Sampling method |     |     |     |     |
| ------ | ---------- | --------------- | --- | --- | --- | --- |
three representative data-driven baselines: ANN, CNN, and LSTM. The
Network  Hidden layers (3 to 6), Units per  Uniform integer /  numerical IK baseline used the Levenberg–Marquardt algorithm (Dam-
| architecture | layer (32 to 256) | Log-uniform |     |     |     |     |
| ------------ | ----------------- | ----------- | --- | --- | --- | --- |
Optimizer Learning rate (10–4 to 10–2), Weight  Log-uniform ped Least Squares) implemented via the SciPy library in Python. To
decay (10–5 to 10–3) ensure a fair comparison of convergence behavior, this solver was
Batch size {32, 64,128} Categorical configured with a maximum of 100 iterations and a termination toler-
λ 1 (10–3 to 1.0), λ 2 (10–3 to 0.1), λ ance of 1 ×10 –4 m. Performance is assessed using three physical metrics
| Loss weights |     | 3  Uniform |     |     |     |     |
| ------------ | --- | ---------- | --- | --- | --- | --- |
(0.1 to 1.0)
defined in Section 4.1.4and inference latency (ms). It is important to
| Regularization | Dropout rate (0.1 to 0.5), Gradient  | Uniform |                                |     |                                     |     |
| -------------- | ------------------------------------ | ------- | ------------------------------ | --- | ----------------------------------- | --- |
|                |                                      |         | note that while a compiled C++ |     | implementation would significantly  |     |
clip (0.1 to 1.0)
reduce execution time compared to the Python implementation used
here, the primary bottleneck in the numerical solver was algorithmic
instability (non-convergence) near kinematic singularities, rather than
Table 3
computational latency. All reported statistics are mean ±standard de-
Optimal hyperparameter configuration.
viation over the indicated number of independent runs, as shown in
| Parameter |     | Value |     |     |     |     |
| --------- | --- | ----- | --- | --- | --- | --- |
Table 4.
Number of hidden layers 3 Table 4 summarizes the primary benchmark results. AdaKineNet
| Hidden layer sizes |     | [54, 37, 229] |     |     |     |     |
| ------------------ | --- | ------------- | --- | --- | --- | --- |
attains a mean positional error of 0.91 ± 0.42 mm, an orientation error
Learning rate 0.00144 of 0.23 ± 0.32◦, a joint-limit violation rate of 0.75%, and a median
| Weight decay |     | 0.00049                 |          |     |     |     |
| ------------ | --- | ----------------------- | -------- | --- | --- | --- |
| Batch size   |     | 64                      |          |     |     |     |
| λ 1/λ /λ     |     | 0.0028 / 0.0018 / 0.875 |          |     |     |     |
| 2  3         |     |                         | Table 4  |     |     |     |
Dropout rate 0.475 Comparative evaluation of AdaKineNet versus baseline methods.
| Gradient clip threshold |     | 0.839 |       |                        |                       |       |
| ----------------------- | --- | ----- | ----- | ---------------------- | --------------------- | ----- |
|                         |     |       | Model | Position  Orientation  | Violation  Inference  | Task  |
error (◦)
|     |     |     |     | error  | rate (%) time (ms) | Success  |
| --- | --- | --- | --- | ------ | ------------------ | -------- |
where N denotes the number of synchronized samples during execution,  (mm) Rate (%)
|     |     |     | AdaKineNet | 0.91 ± 0.23 ±0.32 | 0.75 41.49 | 98.2 |
| --- | --- | --- | ---------- | ----------------- | ---------- | ---- |
tk denotes the k-th synchronized time instant after temporal alignment
|     |     | st(tk )∈ |     | 0 . 4 2 |     |     |
| --- | --- | -------- | --- | ------- | --- | --- |
between the robot controller and the motion capture system, p e 1 ± 2.23 ±0.57
|     |     | e e | Numerical  | 2 . 1 | 0.0 26,004 | 86.4 |
| --- | --- | --- | ---------- | ----- | ---------- | ---- |
R3 is the estimated end-effector position at time tk, computed via for- IK solver 0.76
|                                                   |     | g t(tk )∈R3 denotes  | ANN [12] | 2.11 ± 2.30 ±0.50 | 57.15 47.53 | 41.5 |
| ------------------------------------------------- | --- | -------------------- | -------- | ----------------- | ----------- | ---- |
| ward kinematics from measured joint angles and pe |     | e                    |          |                   |             |      |
0.72
the ground-truth end-effector position at time tk, measured by the mo- 2.11 ± 2.29 ±0.51
|                      |     |     | CNN [12] |      | 54.80 45.05 | 44.1 |
| -------------------- | --- | --- | -------- | ---- | ----------- | ---- |
| tion capture system. |     |     |          | 0.72 |             |      |
Inference latency, per-query forward-pass wall-clock time on the  LSTM [12] 2.03 ± 2.36 ±0.50 60.60 42.19 38.5
on-board compute, the median percentile (ms) is reported for this  0.72
9

S. Fang et al. R o b o t ic s a n d A u t o n o m o u s S y s t e m s 202 (2026) 105494
inference latency of 41.49 ms. By contrast, the numerical IK solver solution in the redundant configuration space. This highlights that
shows substantially larger positional and orientation errors (2.11 ±0.76 AdaKineNet's advantage lies not only in computational speed but also in
mm and 2.23 ± 0.57◦, respectively) and orders of magnitude higher global convergence stability.
runtime in our Python implementation (reported median 26,004 ms).
Regarding runtime, it is acknowledged that a compiled C++ imple- 4.3.2. Comparative analysis
mentation would significantly reduce the execution latency compared to To further evaluate the performance of AdaKineNet, a comparative
the Python implementation reported here (26,004 ms), while the nu- analysis is conducted between AdaKineNet and baseline models. Fig. 6
merical solver frequently failed to converge within the iteration limit provides a consolidated visualization of these results, capturing how
due to the non-convexity of the 10-DoF configuration space. This different models evolve during training, how well they generalize to
resulted in a lower effective success rate compared to AdaKineNet, unseen data, and how their prediction errors are distributed. By inte-
which maintains deterministic inference time. Compared with learning grating these complementary perspectives into a single comparison, the
baselines (ANN, CNN, and LSTM), AdaKineNet reduces position error by figure highlights both the accuracy gains and the robustness improve-
roughly 57% and dramatically reduces problematic violation rates for ments achieved by AdaKineNet, thereby establishing a comprehensive
many data-driven models (baseline violation rates range from ~54% to basis for the subsequent discussion on constraint compliance and
~61%). These results indicate that embedding kinematic priors and computational efficiency.
adaptive loss weighting yield higher accuracy and physically feasible The experimental results demonstrate that AdaKineNet achieves
outputs. superior accuracy compared to both numerical and learning-based
Beyond mean error metrics, the Task Success Rate was analyzed, baselines. Across five runs, its mean positional error is 0.91 ± 0.42
which was defined as the percentage of solutions achieving a position mm, a 56–59% reduction compared with numerical IK and ANN/CNN/
error <5 mm without joint limit violations. AdaKineNet achieved a LSTM. This is enabled by broader dataset coverage (93.7% workspace)
success rate of 98.2% across the test set. In contrast, the numerical solver and orientation augmentation that prevents singularities and improves
achieved a success rate of only 76.4%, primarily due to convergence generalization. Orientation accuracy is likewise enhanced (0.23 ±
failures (getting stuck in a local minimum) when initialized far from the 0.32◦ versus 2.30◦–2.36◦ for ANN/LSTM), owing to diverse sampling
Fig. 6. Comparative evaluation of IK solvers on the 10-DOF mobile manipulator. AdaKineNet achieves faster convergence with lower physics-consistency residuals,
reduced end-effector position error, and enhanced physical-constraint compliance compared with the baseline models.
10

S. Fang et al. R o b o t ic s a n d A u t o n o m o u s S y s t e m s 202 (2026) 105494
and angle-bound constraints. Together, these measures yield lower diverse motion patterns, simulations were conducted using three
mean errors and tighter distributions for both translation and rotation. representative trajectories: spiral, circular, and zigzag. These trajec-
Joint-limit violations are nearly eliminated, with AdaKineNet at tories were chosen to reflect varying levels of complexity, including
0.75% versus 48–61% for baselines, reflecting a 98% reduction. This smooth curvature transitions in circular paths, frequent directional
arises from physics-based regularization and expanded yet constrained changes in zigzag motion, and compound movement in spiral
sampling ranges. Excluding sensitive poses and enforcing Jacobian trajectories.
consistency further ensures stable solutions near singularities, where Baseline comparisons include numerical inverse kinematics (IK),
numerical solvers often fail to converge. Thus, the model not only im- artificial neural networks, convolutional neural networks, long short-
proves nominal accuracy but also mitigates rare but critical failure term memory networks, and the state-of-the-art KineNN architecture.
modes. Evaluation focused on key performance metrics, specifically the posi-
AdaKineNet converges in 2500 iterations, 30% faster than base- tional mean error (PME) and maximum positional error (MPE), quan-
lines, aided by adaptive gradient clipping and residual blocks. Inference tifying average and worst-case deviations between predicted and
runs at 41.5 ms on CPU, vastly outperforming the numerical solver reference end-effector positions.
(26,004 ms) while preserving feasibility. On high-curvature trajectories
such as zigzag tests, where numerical IK reached an MPE of 31.1 mm, 4.4.2. Performance analysis of trajectory prediction of AdaKineNet
AdaKineNet maintained accuracy by dynamically rebalancing position A detailed summary of the simulation results is presented in Fig. 7.
and orientation losses. This adaptability, absent in conventional or Table 5compares the positional tracking accuracy across different tra-
physics-informed baselines like KineNN, removes the need for manual jectory types, highlighting the relative performance of AdaKineNet and
parameter tuning and extends robustness to unstructured tasks. baseline models in maintaining end-effector path fidelity.
The proposed AdaKineNet demonstrates significant advancements Based on the quantitative results in Table 5and the trajectory visu-
over existing approaches for solving inverse kinematics (IK) in redun- alizations in Fig. 7, AdaKineNet consistently demonstrates superior po-
dant mobile manipulators. Compared to the deep learning (DL) archi- sitional accuracy and robust tracking performance across all evaluated
tectures evaluated in [11], which primarily focus on fixed 6-DOF paths. For the spiral trajectory, it achieved a positional mean error
manipulators using networks like BiLSTM, AdaKineNet introduces a (PME) of 1.74 mm and a maximum positional error (MPE) of 11.50
physics-informed neural network (PINN) framework that inherently mm, improving upon the numerical IK solver (PME: 2.38 mm, MPE:
embeds kinematic constraints and dynamic adaptability. While [11] 15.16 mm) and substantially outperforming ANN (PME: 10.39 mm,
highlights the robustness of BiLSTM under noise and geometric MPE: 70.63 mm). On the circular trajectory, AdaKineNet maintained
complexity, its reliance on purely data-driven learning limits general- sub-centimeter deviations, with a PME of 2.19 mm, corresponding to a
ization to highly redundant systems where analytical solutions are 19.4% reduction relative to numerical IK and >68% improvement
intractable. In contrast, AdaKineNet integrates rigid-body kinematics over LSTM. Even in the challenging zigzag trajectory involving abrupt
directly into the loss function, ensuring physical feasibility of solutions directional changes, AdaKineNet achieved a PME of 3.27 mm, out-
even for hyper-redundant configurations. performing numerical IK by 26% and ANN by 72%. The absence of
Furthermore, compared to the KineNN framework, which employs oscillations or overshoot at curvature transitions, as shown in Fig. 7,
homogeneous transformation matrices (HTM) or dual quaternions (DQ) further confirms the effectiveness of the adaptive loss weighting strategy
for modular kinematics [15], AdaKineNet eliminates the need for in balancing positional and orientation objectives, thereby ensuring
explicit DH parameter tuning. KineNN’s strength lies in its trans- both precision and smoothness in closed-loop trajectory tracking.
ferability across robotic architectures but requires retraining when In summary, the trajectory-level simulations confirm that AdaKine-
encountering unseen redundancy or dynamic environments. AdaKine- Net not only delivers higher positional accuracy than both numerical
Net, however, leverages adaptive activation functions and real-time and learning-based baselines but also sustains stable tracking under
parameter adjustment, enabling seamless adaptation to varying DOF
configurations and external disturbances, a critical advantage for mobile
manipulators operating in unstructured environments. Table 5
Positional error comparison across trajectories (Units: mm).
Trajectory Numerical ANN CNN KineNN LSTM AdaKineNet
4.4. Simulation of trajectory prediction IK
Spiral 2.38 10.39 6.66 36.11 6.87 1.74
4.4.1. Experimental design and trajectory specification Circle 2.72 6.97 4.79 25.26 6.23 2.19
To evaluate the capability of AdaKineNet to predict dynamically Zigzag 4.39 11.57 10.46 22.86 8.80 3.27
feasible joint trajectories for redundant mobile manipulators under
Fig. 7. Trajectory tracking results of AdaKineNet for (a) spiral, (b) circle, and (c) zigzag paths. AdaKineNet predictions (blue) closely follow reference trajectories
(red) across diverse motion patterns, achieving superior positional accuracy and stability compared to baseline models.
11

S. Fang et al. R o b o t ic s a n d A u t o n o m o u s S y s t e m s 202 (2026) 105494
diverse path geometries. The model consistently reduced mean and Table 6
maximum errors across spiral, circular, and zigzag trajectories while Quantitative real-robot metrics comparison.
avoiding oscillations or overshoot at curvature transitions. These results Method PTerr Success Failure Singularity Latency
underscore the effectiveness of its adaptive loss weighting and physics- (mm) rate (%) rate (%) (%) median
informed regularization in maintaining smooth, feasible, and precise (ms)
motion, thereby demonstrating its suitability for real-time closed-loop AdaKineNet 8.5 ± 95 5 1.7 11.5
control of redundant mobile manipulators in complex environments 2.1
such as container unloading scenarios. Numerical 9.8 ± 85 15 3.3 46
IK 6.2
TRAC-IK 10.6 ± 90 10 3.3 7.5
4.5. Experiments on the real robot 4.1
To validate AdaKineNet on hardware and to bridge simulation re-
tracking error (PTerr) of 8.5 ±2.1 mm, demonstrating tighter spatial
sults with real-world performance, the trained model was deployed on a
precision than Numerical IK (9.8 ±6.2 mm) and TRAC-IK (10.6 ±4.1
10-DoF prototype mobile manipulator and executed a sequence of
mm) under unmodeled physical dynamics. The framework guarantees
representative warehouse handling tasks, including approach, grasp,
high operational reliability, recording a 95% task success rate and
transport, and placement. The experimental platform is the prototype
limiting overall failures to 5%. Crucially, the physics-informed archi-
designed in Section 4.1.1, and the qualitative execution examples are
tecture effectively navigates the redundant configuration space to avoid
shown in Fig. 8.
kinematic locking, reducing the singularity rate to 1.7% compared to
To quantitatively evaluate the sim-to-real transferability of the pro-
3.3% for both baseline numerical solvers. Although TRAC-IK provides
posed framework, AdaKineNet was benchmarked against standard Nu-
the lowest median latency (7.5 ms), AdaKineNet processes trajectory
merical IK and TRAC-IK solvers on the physical hardware prototype, as
predictions in 11.5 ms, comfortably satisfying the sub-50 ms latency
shown in Table 6.
threshold required for real-time closed-loop control while strictly
In this study, N=60 hardware trials per method (3 representative
enforcing physical constraint compliance.
trajectories × 20 randomized starts) are conducted, ground truth
For each trial, the model produced joint-space trajectories online
controller traces are recorded, and the metrics defined in Section 4.1.4
from perception-provided target poses, a standard low-level velocity
are computed. Table 6summarizes the measured real-robot results for
controller executed trajectories without post-hoc optimization. Infer-
each evaluated method, including a dedicated column for the near-
ence latency (median 41.5 ms on CPU) supported control-relevant query
singular query subset (smallest singular values sampled in log-space
rates and enabled reactive adjustments during transport. Hardware runs
between 10(cid:0)5 and 10(cid:0)2).
produced smooth, physically plausible motions that respected joint
As detailed in Table 6, AdaKineNet achieves a superior positional
Fig. 8. The prototype experimental results of trajectory planning using AdaKineNet. (a-d) Approach. (e-h) Grasp. (i-l) Transport. (m-p) Placement.
12

S. Fang et al. R o b o t ic s a n d A u t o n o m o u s S y s t e m s 202 (2026) 105494
limits and avoided oscillations typical of unguided data-driven IK. References
Failures were mainly due to perception errors, and near-singular base
configurations were excluded rather than the solver itself. [1] D. Benˇco, I. Kubasa´kov´a, J. Kub´anˇov´a, A. Kalaˇsov´a, Automated robots in logistics,
In summary, prototype experiments confirm AdaKineNet’s practical Transport. Res. Procedia 87 (2025) 103–111, https://doi.org/10.1016/j.
trpro.2025.04.114.
transfer to hardware: it delivers real-time, constraint-aware inverse ki- [2] H. Xiong, R. Mendonca, K. Shaw, D. Pathak, Adaptive mobile manipulation for
nematics for redundant mobile manipulators and eliminates the need for articulated objects In the open world, (2024). https://doi.org/10.48550/arXiv.2
401.14403.
iterative post-processing in the tested pick-and-place scenarios.
[3] A.G. Jiokou Kouabon, A. Melingui, J.J.B. Mvogo Ahanda, O. Lakhal, V. Coelen,
M. Kom, R. Merzouki, A learning framework to inverse kinematics of high DOF
5. Conclusion redundant manipulators, Mech. Mach Theory 153 (2020) 103978, https://doi.org/
10.1016/j.mechmachtheory.2020.103978.
[4] M. Sereinig, W. Werth, L.-M. Faller, A review of the challenges in mobile
This paper presented AdaKineNet, an adaptive physics-informed manipulation: systems design and RoboCup challenges: recent developments with
neural network (PINN) framework for solving inverse kinematics of a special focus on the RoboCup, Elektrotech. Inftech. 137 (2020) 297–308, https://
redundant mobile manipulators. The framework makes three key con- doi.org/10.1007/s00502-020-00823-8.
[5] A. Calzada-Garcia, J.G. Victores, F.J. Naranjo-Campos, C. Balaguer, A review on
tributions. Firstly, embedding forward kinematic structure via auto- inverse kinematics, control and planning for robotic manipulators with and
matic differentiation to guarantee physically consistent, exact Jacobian without obstacles via deep neural networks, Algorithms 18 (2025) 23, https://doi.
evaluation via automatic differentiation computation. Then, introduces org/10.3390/a18010023.
[6] A. Aristidou, J. Lasenby, Inverse kinematics: a Review of Existing Techniques and
a learnable, dynamically weighted loss function that balances end-
Introduction of a New Fast Iterative Solver (Technical Report CUED/F-INFENG/
effector accuracy with joint constraints. Finally, adopting a modular, TR-632, Department of Engineering, University of Cambridge, 2009. Available,
scalable architecture capable of accommodating varying degrees of http://www.andreasaristidou.com/publications/CUEDF-INFENG,%20TR-632.pdf.
[7] Z. Li, S. Li, Recursive recurrent neural network: a novel model for manipulator
freedom via flexible input-output layer resizing. Comprehensive simu-
control with different levels of physical constraints, CAAI Trans. Intel. Tech. 8
lation and hardware tests show AdaKineNet provides accurate, real- (2023) 622–634, https://doi.org/10.1049/cit2.12125.
time, and physically feasible IK, outperforming conventional numeri- [8] N. Tan, P. Yu, S. Liao, Z. Sun, Recurrent neural networks as kinematics estimator
and controller for redundant manipulators subject to physical constraints, Neural.
cal solvers and data-driven baselines in tracking and manipulation. It
Netwo. 153 (2022) 64–75, https://doi.org/10.1016/j.neunet.2022.05.021.
reduces mean end-effector position error to 0.91 ± 0.42 mm, eliminates [9] Y. Ning, T. Li, W. Du, C. Yao, Y. Zhang, J. Shao, Inverse kinematics and planning/
singular configurations, cuts joint-limit violations to 0.75% compared to control co-design method of redundant manipulator for precision operation: design
48–61% for baselines, and converges roughly 30% faster. Validated on a and experiments, Robot. Comput. Integr. Manuf. 80 (2023) 102457, https://doi.
org/10.1016/j.rcim.2022.102457.
10-DoF prototype, the method achieves a median CPU inference latency [10] Z.H. Zhan, J. Zhang, Y. Li, H.S.H. Chung, Adaptive particle swarm optimization,
of nearly 41.5 ms and generates smooth, constraint-compliant closed- IEEE Trans. Syst., Man, Cybern. B 39 (2009) 1362–1381, https://doi.org/10.1109/
loop trajectories, supporting practical cross-platform deployment. TSMCB.2009.2015956.
[11] S. Rice, A. Azab, S. Saad, Fusion IK: solving inverse kinematics using a hybridized
Future work will extend AdaKineNet to multi-manipulator collabo- deep learning and evolutionary approach, Manufactur. Lett. 41 (2024) 9–18,
ration and dynamic environments, including integration with percep- https://doi.org/10.1016/j.mfglet.2024.09.005.
tion and motion planning modules. Additionally, systematic [12] N. Wagaa, H. Kallel, N. Mellouli, Analytical and deep learning approaches for
solving the inverse kinematic problem of a high degrees of freedom robotic arm,
benchmarking protocols will be developed to evaluate generalization,
Eng. Appl. Artif. Intell. 123 (2023) 106301, https://doi.org/10.1016/j.
robustness, and long-term deployment in industrial applications. engappai.2023.106301.
[13] D. Cagigas-Mun˜iz, Artificial Neural networks for inverse kinematics problem in
articulated robots, Eng. Appl. Artif. Intell. 126 (2023) 107175, https://doi.org/
CRediT authorship contribution statement
10.1016/j.engappai.2023.107175.
[14] J. Liu, P. Borja, C.D. Santina, Physics-informed neural networks to model and
Shihui Fang: Writing – original draft, Visualization, Validation, control robots: a theoretical and experimental investigation, Adv. Intell. Syst. 6
(2024) 2300385, https://doi.org/10.1002/aisy.202300385.
Software, Project administration, Methodology, Formal analysis, Data
[15] J.D. Toscano, V. Oommen, A.J. Varghese, Z. Zou, N.A. Daryakenari, C. Wu, G.
curation, Conceptualization. Min Chen: Writing – review & editing, E. Karniadakis, From PINNs to PIKANs: recent advances in physics-informed
Resources, Project administration, Methodology, Formal analysis, machine learning, Mach. Learn. Comput. Sci. Eng. 1 (2025), https://doi.org/
Conceptualization. Yaran Chen: Writing – review & editing, Method- 10.1007/s44379-025-00015-1.
[16] M. Raissi, P. Perdikaris, G.E. Karniadakis, Physics-informed neural networks: a
ology. Jia Wang: Visualization, Conceptualization. Jinghua Wu: Su- deep learning framework for solving forward and inverse problems involving
pervision, Conceptualization. Zhihua Zhang: Resources, nonlinear partial differential equations, J. Comput. Phys. 378 (2019) 686–707,
Conceptualization. Eng Gee Lim: Resources. https://doi.org/10.1016/j.jcp.2018.10.045.
[17] G.E. Karniadakis, I.G. Kevrekidis, L. Lu, P. Perdikaris, S. Wang, L. Yang, Physics-
informed machine learning, Nat. Rev. Phys. 3 (2021) 422–440, https://doi.org/
Declaration of competing interest 10.1038/s42254-021-00314-5.
[18] M.R. Diprasetya, J. Po¨ppelbaum, A. Schwung, KineNN: kinematic Neural Network
for inverse model policy based on homogeneous transformation matrix and dual
The authors declare that they have no known competing financial
quaternion, Robot. Comput. Integr. Manuf. 94 (2025) 102945, https://doi.org/
interests or personal relationships that could have appeared to influence 10.1016/j.rcim.2024.102945.
the work reported in this paper. [19] H. Li, Y. Chai, B. Lv, L. Ruan, H. Zhao, Y. Zhao, J. Luo, Physics-informed neural
network predictive control for quadruped locomotion, (2025). https://doi.org/10.
48550/arXiv.2503.06995.
Acknowledgements [20] S. Fang, M. Chen, Y. Chen, J. Wu, S. Liu, Extending workspace of robotic container
unloading system via additional linear axis, in: Proceedings of the 2024 4th
International Joint Conference on Robotics and Artificial Intelligence, ACM,
This work was supported by the National Natural Science Foundation
Shanghai, China, 2024, pp. 78–83, https://doi.org/10.1145/3696474.3696497.
of China (NSFC) Regional Innovation and Development Joint Fund [21] B. Siciliano, L. Sciavicco, L. Villani, G. Oriolo, Robotics: Modelling, Planning and
(U24A20277) and the Science and Technology Major Project of Jiangsu Control, Springer, London, 2009, https://doi.org/10.1007/978-1-84628-642-1.
[22] S.R. Buss, Introduction to Inverse Kinematics With Jacobian Transpose,
(BG2025029).
Pseudoinverse and Damped Least Squares methods, Technical Report (UCSD),
2004. Available, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/ikmethods/iks
Data availability urvey.pdf.
[23] M.W. Spong, S. Hutchinson, M. Vidyasagar, Robot Modeling and Control, 1st ed,
John Wiley & Sons, Hoboken, NJ, 2005.
Data will be made available on request. [24] A.G. Baydin, B.A. Pearlmutter, A.A. Radul, J.M. Siskind, Automatic differentiation
in machine learning, J. Mach. Learn. Res. 18 (2018) 1–43.
[25] B. Stephan, I. Dontsov, S. Müller, H.-M. Gross, On learning of inverse kinematics
for highly redundant robots with neural networks, in: 2023 21st International
Conference on Advanced Robotics (ICAR), IEEE, Abu Dhabi, United Arab. Emirate.,
2023, pp. 402–408, https://doi.org/10.1109/icar58858.2023.10406939.
13

S. Fang et al. R o b o t ic s a n d A u t o n o m o u s S y s t e m s 202 (2026) 105494
[26] A. Malik, Y. Lischuk, T. Henderson, R. Prazenica, A deep reinforcement-learning [31] T. Akiba, S. Sano, T. Yanase, T. Ohta, M. Koyama, Optuna: a next-generation
approach for inverse kinematics solution of a high degree of freedom robotic hyperparameter optimization framework, (2019). https://doi.org/10.4855
manipulator, Robotics 11 (2022) 44, https://doi.org/10.3390/robotics11020044. 0/arXiv.1907.10902.
[27] A. Paszke, S. Gross, S. Chintala, G. Chanan, E. Yang, Z. DeVito, Z. Lin, A. [32] R. Sharma, V. Shankar, Accelerated training of physics-informed neural networks
Desmaison, Automatic differentiation in PyTorch, in: 31st Conference on Neural (PINNs) using meshless discretizations, (2023). https://doi.org/10.48550/arXiv.22
Information Processing Systems (NIPS 2017), Long Beach, CA, USA, 2017. 05.09332.
[28] M. Mujica, M. Crespo, M. Benoussaad, S. Junco, J.Y. Fourquet, Robust variable [33] J. Schulman, Y. Duan, J. Ho, A. Lee, I. Awwal, H. Bradlow, J. Pan, S. Patil,
admittance control for human–robot co-manipulation of objects with unknown K. Goldberg, P. Abbeel, Motion planning with sequential convex optimization and
load, Robot. Comput. Integr. Manuf. 79 (2023) 102408, https://doi.org/10.1016/j. convex collision checking, Int. J. Rob. Res. 33 (2014) 1251–1270, https://doi.org/
rcim.2022.102408. 10.1177/0278364914528132.
[29] R. Cipolla, Y. Gal, A. Kendall, Multi-task learning using uncertainty to weigh losses [34] B.K.P. Horn, Closed-form solution of absolute orientation using unit quaternions,
for scene geometry and semantics, in: 2018 IEEE/CVF Conference on Computer J. Opt. Soc. Am. A 4 (1987) 629, https://doi.org/10.1364/JOSAA.4.000629.
Vision and Pattern Recognition, IEEE, Salt. Lake. City, UT, USA, 2018, [35] D.E. Schinstock, T.N. Faddis, R.B. Greenway, Robust inverse kinematics using
pp. 7482–7491, https://doi.org/10.1109/cvpr.2018.00781. damped least squares with dynamic weighting, American Institute of Aeronautics
[30] H. Zhang, Y.N. Dauphin, T. Ma, Fixup initialization: residual learning without and Astronautics paper AIAA-94-1299-CP, NASA/Johnson Space Center, (1994).
normalization, (2019). https://doi.org/10.48550/arXiv.1901.09321. https://ntrs.nasa.gov/api/citations/19950005142/downloads/19950005142.
14