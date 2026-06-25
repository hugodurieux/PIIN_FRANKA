www.nature.com/scientificreports
OPEN Symplectic physics-embedded
learning via Lie groups Hamiltonian
formulation for serial manipulator
dynamics prediction
Fei Wang, Liping Chen & Jianwan Ding
Accurate dynamic modeling is critical for advanced robotic control, yet conventional methods struggle
with manipulator nonlinear complexity. While Hamiltonian neural networks leveraging Lie group
symmetries improve physical consistency of the network, existing methods overlook key limitations:
unconstrained sparsity in mass, dissipation, and control matrices; redundancy in mass network
outputs; and lack of validation on multi-rigid-body systems. This paper proposes a symplectic physics-
embedded learning approach (SPEL) based on Lie group Hamiltonian formulations for enhanced
dynamics modeling of serial manipulators. By systematically encoding physical priors such as Lie
group symmetries and Hamiltonian dynamics into neural network design, SPEL enforces sparsity
in mass, dissipation, and control input matrices via physics-driven constraints and replaces input-
independent matrix elements with trainable parameters. These mechanisms structurally optimize the
network topology, significantly reducing output dimensionality while preserving physical consistency
of the network. Experimental validation on simulated two-link and revolute-prismatic-revolute (RPR)
manipulators, as well as a real 6-DOF manipulator, demonstrates that SPEL reduces over 52% of the
parameters, enhances computational efficiency by more than 75%, and achieves higher prediction
accuracy. Additionally, Symplectic Physics-Embedded Learning Kolmogorov-Arnold Networks (SPEL-
KAN) reduce over 63% of the parameters and improve computational efficiency by more than 39%.
This approach embeds geometric-mechanical principles into architectures, balancing efficiency with
interpretable predictions.
Keywords Lie group, Hamiltonian dynamics, Physics-embedded, Dynamics prediction, Serial manipulator
Serial or articulated manipulator, renowned for their precision and adaptability, are increasingly employed in
various industrial and domestic applications, particularly in small and medium-sized enterprises where tasks
demand high accuracy and flexibility in dynamic and semi-structured environments1–3. These manipulators
often utilize harmonic drives as joint reducers, introducing control challenges due to joint flexibility and
significant nonlinearities in system dynamics4. In practical applications, dynamic parameters of manipulators
are often affected by environmental factors (e.g., temperature variations, material aging, assembly errors, and
external disturbances), leading to systematic deviations from theoretical design values and thus reducing the
prediction accuracy of models based on nominal parameters. As a classic example of multi-rigid-body systems,
serial manipulators consist of multiple rigid links connected by joints (revolute or prismatic), forming a
kinematic chain that inherently involves complex interactions between bodies and constrains. Effective control
and performance optimization of such robotic systems necessitate the development of accurate dynamic models
capable of predicting and identifying these nonlinear behaviors5. Model prediction involves forecasting system
outputs based on given inputs and data, while parameter identification aims to determine the system’s underlying
structure and parameters using collected data6. The primary objective is to estimate model parameters through
experimental data analysis, employing regression models and algorithms to minimize an objective function and
accurately map inputs to outputs, reflecting actual system behavior7.
Traditional methods of dynamic learning, such as inverse dynamic models using ordinary least squares,
assume a linear relationship between joint torques and inertial parameters, based on rigid links and negligible
School of Mechanical Science and Engineering, Huazhong University of Science and Technology, Wuhan 430074,
China. email: chenlp@hust.edu.cn
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 1

www.nature.com/scientificreports/
nonlinearities8. Although efficient for linear systems, these methods can yield biased and physically inconsistent
results due to measurement noise, incorrect filtering, or inadequate excitation9.
Recent advances in machine learning address dynamic prediction challenges in robotic systems, where
nonlinearities and uncertainties hinder traditional methods10,11. Machine learning models identify input-
output relationships, often replacing physics-based approaches, but conventional neural networks lack physical
interpretability and require substantial data. Physics-informed neural networks (PINNs) integrate physical
constraints into neural network loss functions via automatic differentiation12, combining physics-driven and
data-driven strengths to enhance nonlinear fitting accuracy and reduce data dependency11. Applications in
fluid dynamics, solid mechanics, chemical kinetics, and mechanics demonstrate PINNs’ predictive capabilities
comparable to conventional algorithms while enabling efficient parameter training and identification13.
However, PINNs struggle with complex systems governed by nonlinear, coupled ODEs with many
parameters14,15, whereas physics-encoded neural networks (PeNNs) incorporate geometric constraints to reduce
variance and accelerate convergence16,17. Physical system dynamics are governed by kinematic constraints and
energy conservation, which can be enhanced via prior knowledge integration, including symmetry-equivariant
networks18, graph networks for forward kinematics19, or Lagrangian/Hamiltonian architectures20–24. For serial
manipulators adhering to Lagrangian/Hamiltonian mechanics, Greydanus et al. modeled Hamiltonians using
neural networks to minimize symplectic gradient discrepancies22, with additional constraints that the mass
matrix is positive definite and the dissipation matrix is positive semi-definite when employing Hamiltonian
mechanics. Chen et al. and Zhong et al. applied adjoint methods for backpropagation through ODE solvers
without explicit time derivatives25,26. Researchers like Yang4, Wu27, and Liu28 have developed Lagrangian/
Hamiltonian-based manipulator models for system identification and control, with Yang neglecting joint
coupling and Wu approximating uncertainties via standard deep neural networks to enhance Lagrangian neural
networks.
Previous studies on Lagrangian/Hamiltonian neural networks often employed vector-valued states like Euler
angles for manipulator modeling. In contrast, serial manipulators composed of rigid bodies inherently follow
the Lie group structure, with kinematics evolving on the special Euclidean group SE(3) for spatial movements
and the special orthogonal group SO(3) for rotations29. The exponential map from Lie group theory enables
more efficient dynamic equations than traditional Denavit-Hartenberg (DH) methods. Recent advancements
combine Hamiltonian mechanics with Riemannian geometry to derive concise inverse dynamic equations30,
while Lie group Neural ODEs (NODEs) aim to preserve the Lie group structure during backpropagation in
high-dimensional spaces or local coordinates31. Duong et al. proposed port-Hamiltonian NODEs (PHNODEs)
on Lie groups for a quadrotor, establishing a novel framework for structure-preserving dynamic modeling29,32.
Recent advances in data-driven modeling include the introduction of Kolmogorov-Arnold Networks (KANs)
by Liu et al. as an alternative to Multi-Layer Perceptrons (MLPs)33,34. KANs learn activation functions using
gridded basis functions and trainable scaling factors, accelerating convergence, and reducing parameters. They
have been applied in various fields, including time series prediction.
Even with Hamiltonian or Lagrangian frameworks, accurately acquiring all physical parameters of multi-
rigid-body systems (e.g., serial manipulators) and precisely modeling complex nonlinear dissipative effects
remain extremely challenging. In existing robotic dynamics modeling, while Featherstone’s ABA algorithm35
enables efficient computation via topological sparsity, and Murray36 revealed the underlying sparse structure of
control matrices, both rely on analytical models and cannot learn nonlinear disturbances. Recent PINNs have
attempted to introduce sparsity via L1 regularization but fail to incorporate robotics-specific geometric priors
(e.g., Lie group structures). Existing Lagrangian or Hamiltonian neural networks for serial manipulator dynamics
often rely on Euler angles, and neglect input-independent elements in the mass and control input matrices,
leading to redundant outputs. While Hamiltonian neural networks on Lie groups offer improvements, they do
not comprehensively model multi-rigid-body serial manipulators and fail to account for the inherent sparsity
in mass, dissipation, and control input matrices. To address these limitations, this paper proposes a symplectic
physics-embedded learning approach (SPEL) based on Lie group Hamiltonian formulations for dynamic
prediction in serial manipulators. By systematically encoding physical priors, such as Lie group symmetries and
Hamiltonian conservation laws, into the neural architecture, it enforces sparsity in system matrices via physical
constraint-guided topology optimization and replaces input-independent matrix elements with trainable
parameters to eliminate redundancy. These methods simplify network complexity while preserving physical
consistency of the network, i.e., its ability to adhere to fundamental physical laws (e.g., energy conservation,
momentum evolution, and structural sparsity of dynamic matrices) through the embedding of physical priors37.
The structure of the remainder of this paper is as follows: Section “Preliminaries” provides an overview of
Hamiltonian dynamics on Lie groups and the PHNODEs approach. Section “Hamiltonian dynamics of serial
manipulator on Lie groups” introduces the Hamiltonian dynamics of a serial manipulator on Lie groups. Section
“Symplectic physics-embedded learning of Lie groups dynamics for serial manipulator” details the SPEL for a
serial manipulator on Lie groups. Section “Experimental validation” presents the results from simulation and
real-world experiments. Section “Conclusion” summarizes the paper and discusses future directions.
Preliminaries
Hamiltonian dynamics on Lie group
The pose of the body-fixed frame relative to the world frame is defined by the position r c R3 of the center
∈
of mass and the orientation of the body-fixed frame’s coordinate axes R SO(3). The generalized coordinate
∈
q is given by q=(r c ,R). The rigid-body position and orientation can be combined into a single pose matrix
T SE(3). The kinematic equations of motion for a rigid body are defined by the linear velocity v R3 and
ang ∈ ular velocity ω R3 of the body-fixed frame relative to the world frame, both expressed in the bo ∈ dy-frame
∈
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 2

www.nature.com/scientificreports/
coordinates. The generalized velocity ζ =(v,ω) R6 governs the rate of change of the rigid body’s pose,
| adhering to the principles of SE(3) kinematics38. |     |     |     |     |           | ∈   |      |     |     |     |     |
| ------------------------------------------------- | --- | --- | --- | --- | --------- | --- | ---- | --- | --- | --- | --- |
|                                                   |     |     |     |     | =qξ=qζˆ=q |     | ωˆ v |     |     |     |     |
|                                                   |     |     |     | q˙  |           |     |      |     |     |     | (1) |
0T 0

[ ]
ˆ
where the symbol   represents the mapping from a vector ζ R6 to a 4 4 twist matrix ξ=ζˆ  in the Lie
|     |     |     |     |     |     |     | ∈   |     | ×   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
algebra se(3) of SE(3), and from a vector ω to a 3 3 skew-symmetric matrix ωˆ in the Lie algebra so(3) of
×
SO(3).
A port-Hamiltonian generalization of Hamiltonian mechanics is utilized to model systems that incorporate
energy-storing elements (e.g., kinetic and potential energy), energy-dissipating elements (e.g., friction or
resistance), and external energy sources (e.g., control inputs), interconnected through energy ports29,39.
|     |     |     | q˙  |          |         |     | ∂H   |         |     |     |     |
| --- | --- | --- | --- | -------- | ------- | --- | ---- | ------- | --- | --- | --- |
|     |     |     |     | =(J(q,p) | R(q,p)) |     | ∂ q  | +G(q)u  |     |     | (2) |
|     |     |     | p˙  |          | −       |     | ∂ H  |         |     |     |     |
|     |     |     |     |          |         |     | [∂p] |         |     |     |     |
|     |     |     | [   | ]        |         |     |      |         |     |     |     |
where J(q,p) is a skew-symmetric interconnection matrix that represents the energy-storing elements,
R(q,p) 0 is a positive semi-definite dissipation matrix that represents the energy-dissipating elements, and
⪰
G(q) is an input matrix such that G(q)u represents the external energy sources. Energy-dissipating elements,
such as friction or drag forces, are typically modeled as a positive semi-definite R(q,p) 0 and affect only the
⪰
generalized momenta p, i.e.,
|     |     |         |     | 0 0      |          |     | 0   | I      |      | 0   |     |
| --- | --- | ------- | --- | -------- | -------- | --- | --- | ------ | ---- | --- | --- |
|     |     | R(q,p)= |     |          | ,J(q,p)= |     |     | ,G(q)= |      |     | (3) |
|     |     |         |     | 0 D(q,p) |          |     | I   | 0      | B(q) |     |     |
|     |     |         |     |          |          |     | −   |        |      |     |     |
|     |     |         | [   |          | ]        |     | [   | ]      | [    | ]   |     |
When the system is not subjected to external forces, meaning the system conserves energy, where the dissipation
T
matrix is R(q,p)=0,u=0. By vectorizing the generalized coordinates q= rT rT rT rT , the
|     |     |     |     |     |     |     |     |     |     | c 1 | 2 3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
variables of the port-Hamiltonian dynamics on SE(3) can be represented using the following interconnection  [ ]
matrix.
RT
|     |     |         |     |      | 0 0      | 0    |       | 0    | pˆ v      |     |     |
| --- | --- | ------- | --- | ---- | -------- | ---- | ----- | ---- | --------- | --- | --- |
|     |     |         | q×  | =    | rˆT rˆT  | rˆT  | ,p× = | pˆ   | pˆ        |     | (4) |
|     |     |         |     | 0    |          |      |       | v    | ω         |     |     |
|     |     |         |     | [    | 1        | 2 3] |       |      |           |     |     |
|     |     |         |     |      |          |      |       | [    | ]         |     |     |
|     |     |         |     | 0    | q×       |      | d v(  | q,p) | 0         |     |     |
|     |     | J(q,p)= |     |      | ,D(q,p)= |      |       |      |           |     | (5) |
|     |     |         |     | q T  | p        |      |       | 0    | d ω( q,p) |     |     |
|     |     |         |     | [− × | × ]      |      |       |      |           |     |     |
|     |     |         |     |      |          |      | [     |      |           | ]   |     |
where the elements d v(q,p) and d ω(q,p) correspond to linear momentum p v and angular momentum p ω,
respectively. The port-Hamiltonian’s equations on the SE(3) manifold are29,39,40:
∂H(q,p)
r˙c =R
∂p
v
|             |     | ∂H(q,p) |      |          |     |     |     |     |     |     |     |
| ------------ | --- | ------- | ---- | -------- | --- | --- | --- | --- | --- | --- | --- |
| r ˙          | = r |         | , i= | 1 , 2, 3 |     |     |     |     |     |     |     |
|  i | i   | ∂ p     |      |          |     |     |     |     |     |     |     |
× ω
|     |     | ∂H ( q ,p) |     | ∂ H ( q | ,p)      | ∂H  | ( q ,p) |          |     |     |   (6) |
| --- | --- | ---------- | --- | ------- | -------- | --- | ------- | -------- | --- | --- | ----- |
| p ˙ | = p |            | R   | T       | d v(q,p) |     |         | +b v(q)u |     |     |       |
| v   | v   |            |     |         |          |     |         |          |     |     |       |
|     | ×   | ∂ p ω      | −   | ∂ r     | c −      |     | ∂ p v   |          |     |     |       |
3
|            |     | ∂H(q,p) |     | ∂H(q,p) |     |       | ∂H(q,p) |     |          | ∂H(q,p) |       |
| ---------- | --- | ------- | --- | ------- | --- | ----- | ------- | --- | -------- | ------- | ----- |
| p ˙ω       | = p |         | + p |         | +   | r     |         |     | d ω(q,p) | +b      | ω(q)u |
|  | ω × | ∂ p     |     | v × ∂   | p   | i ×   | ∂r      | −   |          | ∂p      |       |
|            |     | ω       |     |         | v   |       |         | i   |          | ω       |       |
|            |     |         |     |         |     | i = 1 |         |     |          |         |       |
∑
T
| w her e  th | e i n pu t mat | ri x  is B | (q ) | = b v( q | )T b ω( | q ) T . |     |     |     |     |     |
| ----------- | -------------- | ---------- | ---- | -------- | ------- | ------- | --- | --- | --- | --- | --- |
|             |                |            |      | [        |         | ]       |     |     |     |     |     |
Port-Hamiltonian neural ODE networks on Lie group
Port-Hamiltonian Neural ODE Networks on Lie Group integrates Neural ODE with Port-Hamiltonian systems29.
It learns the Port-Hamiltonian function H(q,p) on Lie group, providing dynamics through Hamilton’s equations.
By embedding Hamiltonian dynamics on Lie group into the neural network model f¯(x,θ) and considering
zero-order hold control inputs u, this network extends Neural ODEs, resulting in a system described by:
|     |     |     |     |     | x˙ f(x | ,θ) |           |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | --- | --------- | --- | --- | --- | --- |
|     |     |     |     |     | =      |     | =f¯(x,θ)  |     |     |     | (7) |
|     |     |     |     |     | u ˙    | 0   |           |     |     |     |     |

|     |     |     |     | [   | ] [ | ]   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The loss function for this network resembles mean squared error (MSE) but is computed between the predicted
and actual generalized coordinates and velocities. The predicted coordinates q¯( i) =(r¯( i ),R¯( i) ) and the ground-
|                      |     |           |        |                                                           |     |     |        |         | n   | c n n |        |
| -------------------- | --- | --------- | ------ | --------------------------------------------------------- | --- | --- | ------ | ------- | --- | ----- | ------ |
| truth coordinates q( |     | i) =(r(   | i ),R( | i)) are used to compute a loss on the Lie group manifold. |     |     |        |         |     |       |        |
|                      |     | n         | c n    | n                                                         |     |     |        |         |     |       |        |
|                      | D   | N         |        |                                                           | 2   | D N |        |         | D   | N     | 2      |
|                      |     |           |        | R¯( i)R(                                                  | i)  |     | r( i ) | r¯( i ) | 2   | ζ( i) | ζ¯( i) |
| L(θ)=                |     | log∨SO(3) |        |                                                           | +   |     |        |         | +   |       |   (8)  |
|                      |     |           |        | n                                                         | n   |     | c n    | − c n   | 2   | n −   | n      |
|                      |     |           |        |                                                           | 2   |     |        |         |     |       | 2      |
  (cid:31) i=1(cid:31) n=1(cid:30) (cid:29) (cid:28)(cid:30) (cid:31) i=1(cid:31) n=1 (cid:30) (cid:30) (cid:31) i=1(cid:31) n=1(cid:30) (cid:30)
|     |     | (cid:30) |     |     | (cid:30) |     |          |          |     | (cid:30) | (cid:30) |
| --- | --- | -------- | --- | --- | -------- | --- | -------- | -------- | --- | -------- | -------- |
|     |     | (cid:30) |     |     | (cid:30) |     | (cid:30) | (cid:30) |     | (cid:30) | (cid:30) |
3
Scientific Reports |        (2025) 15:33179  | https://doi.org/10.1038/s41598-025-17935-w

www.nature.com/scientificreports/
where D represents the number of configurations q in the dataset, and N denotes the length of the time series.
Hamiltonian dynamics of serial manipulator on Lie groups
Dissipative function and potential energy
Analyzing Eq. (2), in practical scenarios, control inputs are typically precise and predictable, whereas the D(q,p)
term exerts a nonlinear influence on the system’s behavior. This component accounts for various uncertainties in
the serial manipulator, which mainly include the following factors.
Friction forces: Robot joint friction, including static and dynamic friction, introduces errors and can be
modeled using Coulomb and viscous friction models. Elastic forces: Robot components, such as linkages and
transmissions, can deform elastically under torque, generating opposing forces. Nonlinear dynamic effects: The
manipulator may exhibit nonlinear behaviors like bending, complex periodic motions, and chaos. External
disturbance forces: External forces, such as wind, vibrations, or impacts, can disrupt manipulator motion. Sensor
errors: Sensor inaccuracies, including noise and drift, can lead to errors in the dynamics equations. Other model
errors: Mathematical models may not fully capture real-world conditions, leading to errors from approximations
and unmodeled dynamics27.
For the joint friction in the serial manipulator, the actual joint module comprises components such as a servo
torque motor, joint position encoder, and joint reducer. The complex structure of these joints complicates the
joint model, affecting the dynamic performance of the robot. Joint friction primarily includes bearing and brush
friction in the motor, gear friction in the reducer, nonlinear elastic deformation between the flexible and rigid
wheels of the harmonic drive reducer, and bearing friction at the joint. Several methods exist for calculating joint
friction in serial manipulators.
F s =f s
·
e( − ζ/ζs),F v =
−
B
·
ζ (9)
where F s is Stribeck friction force; f s is Stribeck friction coefficient; ζ s is characteristic velocity; F v is viscous
friction; B is the coefficient of viscous friction. Therefore, D(q,p) in this paper needs to be established as a
neural network of q and p, or a neural network of q and ζ.
The gravitational potential energy V(q) depends on the generalized coordinate q of the serial manipulator
and is influenced by the mass of the links and rotors. It can be used for its calculation, incorporating the gravity
vector g, the total mass of each link and rotor, and their respective position vectors in the base coordinate system.
Specifics of serial manipulator dynamics on Lie groups
A serial manipulator consists of a series of links connected by joints, which can be either revolute or prismatic.
These joints are typically arranged sequentially along a single axis. In a serial manipulator, the motion of each
joint influences the position and orientation of the end-effector. The manipulator’s movement is controlled by
adjusting the angles or positions of the individual joints to execute specific tasks, such as handling, assembly,
welding, and more.
In this section, the serial manipulator’s state is defined by the generalized coordinates
q=(r c ,R),r c R3,R SO(3) evolving on the Lie group G and the generalized velocity ζ =(v,ω) R6
∈ ∈ ∈
in the Lie algebra g of G. The following diagram illustrates a schematic of a particular link in a serial manipulator.
As shown in Fig. 1, {0} denotes the base coordinate system, and {i} represents the joint coordinate system
a b t a t s a e c h c e o d o r t d o i n th a e te i - s t y h s t j e o m in , t a . n L d e t l e 0 i t R d i ∈ S R O 3 ( 3 b ) e b t e h e t h p e o r s o it t i a o t n io v n e m cto a r tr o ix f f t r h o e m i- t t h h e j o i i - n th t i j n o i t n h t e c b o a o s r e d i c n o a o t r e d s i y n s a t t e e m s y t s o t e t m he ,
which can be obtained through the ∈ homogeneous transformation matrix. Let d ci R3 be the vector from the
i-th joint to the center of mass of the i-th link, mi be the scalar mass of the i-th link ∈ , and ρ i R3 be the vector
∈
from the center of mass of the i-th link to the mass element, expressed in the i-th joint coordinate system. The
vector from the origin of the base coordinate system to the mass element is given by d i+0 i R(d ci+ρ i).
For the i-th link with prismatic freedom, ω i =0. Thus, the kinetic energy and the potential energy of the
i-th link are39
T i(R i ,d ci ,ω i)= 1 2 d˙ i+0 i − 1 R˙(d ci+ρ i)+0 i − 1 R(d˙ ci+ρ i) 2 dm(ρ i)
(cid:31)Bi
= 1 2 m i (cid:30) (cid:30)d˙ i 2 + 1 2 ωT i J i ω i+ 1 2 m i d˙ ci T d˙ ci+m i d˙ (cid:30) (cid:30) i T 0 i − 1 R S(ω i − 1 )d ci+d˙ ci (10)
+m
i
d(cid:30)
(cid:30)
T
ci
S(cid:30)
(cid:30)
T(ω
i − 1
)d˙
ci
(cid:29) (cid:28)
V i(R i ,d ci)=m i g(eT 3 d i+eT 3 0 i Rd ci) (11)
where J i =m i ST(d ci)S(d ci)+ Bi ST(ρ i)S(ρ i)dm(ρ i) is the 3 × 3 inertia matrix of the i-th object; ω i − 1
i S s ( t ω he i an 1 ) g d u e la n r o v te e s lo th ci e t y sk o e f w t - h s e y m (i m − e 1 tr ∫ ) i - c t m h a li t n r k ix r . Th ela e ti x v y e - t p o l a t n h e e o b f a t s h e e c b o a o se r d co in o a r t d e i n fr a a t m e f e r , a a m n e d s 0 i e−rv 1 e R˙ s a = s t 0 i h−e 1 ze R ro S p ( o ω te i n − t 1 ia ) l ;
−
energy reference. The total kinetic energy T and total potential energy V of the serial manipulator are
T(R,d c ,ω,d˙ c)= 1 2 (cid:31) i= n 1(cid:30) [ + m ω i (cid:29) (cid:29) T i d J ˙ i i(cid:29) (cid:29) ω 2 i + + 2 m m i i d˙ d˙ T c T i i d˙ 0 i c − i 1 + R 2 (cid:28) m S i ( d ω T ci i − S 1 T ) ( d ω ci i − + 1 ) d˙ d˙ c c i i(cid:27)(cid:26) (12)
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 4

www.nature.com/scientificreports/
Figure 1. A particular link in a serial manipulator.
n
V(R,d)= m i g(eT 3 d i +eT 3 0 i Rd ci) (13)
∑
i=1
The Lagrangian L(q,ζ) of the manipulator is defined as L(q,ζ)=T V. By applying the Legendre
−
transformation, the generalized momentum p d˙
ci
is defined as:
∂L(q,ζ) ∂L(q,ζ)
p d˙ ci = ∂d˙
ci
,p= ∂ζ =Mζ (14)
w h e r e
p= p 1 ...p d˙
ci
...p n T ,ζ = ζ 1 ...d˙ ci ...ζ n T ,q=[q 1 ...d ci ...q n]T ; M denotes the mass matrix of
the serial manipulator. Therefore, the Hamiltonian function is given by H(q,p)=pT ζ L(q,ζ)=T +V.
[ ] [ ] · −
For the i-th link with prismatic joints, the Hamiltonian canonical equations for the i-th joint are:
∂H(q,p)
d˙ ci = ∂p
 ∂H
d˙
( c q i ,p) ∂H(q,p) (15)
 p d˙ ci = − ∂r c − D d˙ ci (q,p) ∂p d˙
ci
+b d˙ ci (q)u
For the i-th link with

a revolute degree of freedom, the linear velocity v=0, d ci is a constant vector, and i i− 1R
is not the identity matrix. The time derivative of the rotation matrix i i− 1R˙ =i i− 1 RS(ω i), w i is the angular
velocity of the i-th link in the i-th joint coordinate system. The position vector from the origin of the inertial
frame to the mass element is given by d i+0 i R(d ci+ρ i). Thus, The potential energy of the i-th link is given by
Eq. (11), and the kinetic energy is39:
T i(R i ,d i ,ω i)= 1 2 d˙ i+0 i − 1 R˙(d ci+ρ i) 2 dm(ρ i)
(cid:31)Bi (16)
= 2 1 m i (cid:30) (cid:30)d˙ i 2 + 1 2 ωT i J i ω i+m (cid:30) (cid:30) i d˙T i 0 i RS(ω i)d˙ ci
(cid:30) (cid:30)
The total potential energy is given by Eq. (1(cid:30)3), a(cid:30)nd the total kinetic energy is
n
T(R,d,ω)= 1 2 m i d˙ i 2 +ωT i J i ω i+2m i d˙T i 0 i RS(ω i)d ci (17)
(cid:31) i=1(cid:30) (cid:29) (cid:29) (cid:28)
(cid:29) (cid:29)
The generalized momentum p ωi is defined as p ωi =∂L(q,ζ)/∂ω i, p=[p 1 ...p ωi ...p n]T . The generalized
velocity is ζ =[ζ 1 ...ω i ...ζ n]T . The generalized coordinates is q= q 1 ...0 i R...q n T . For the i-th link
with revolute joints, the Hamiltonian canonical equations for the i-th joint are:
[ ]
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 5

www.nature.com/scientificreports/
∂H(q,p)
r˙ij =r
ij × ∂p ωi
,j =1,2,3
 ∂H(q,p) 3 ∂H(q,p) ∂H(q,p) (18)
 p˙ ωi =p ωi × ∂p ωi +
∑
j=1
r ij × ∂r ij − D ωi (q,p) ∂p ωi +b ωi (q)u

If a link has both prismatic and rotational degrees of freedom, then the Hamiltonian equations for that link are
given by Eq. (6).
Symplectic physics-embedded learning of Lie groups dynamics for serial
manipulator
Framework overview
The dynamics of serial manipulators, governed by nonlinear and dynamically coupled ODEs with numerous
parameters, represent a complex system. PeNNs adjust architectures by embedding specific physical constraints
to ensure compliance during forward computation, thereby enhancing convergence speed and accuracy. This
study introduces a SPEL framework based on Lie groups for predicting the dynamics of serial manipulators, as
illustrated in Fig. 2.
In this method, neural networks model continuous ODEs using sequential data as input, employing ODE
solvers to control approximation errors and facilitate flexible training, while learning the unknown parts of the
Hamiltonian function and dissipation matrix that depend on the system states (q and ζ). The neural network
comprises mass networks (M-NN), dissipation networks (D-NN), control input networks (G-NN), and potential
energy networks (V-NN), collectively constructing the system’s dynamic state equations. By embedding the
state-space dynamic model into the neural network and integrating the system’s mass and inertia into the state
equations, accurate predictions can be achieved without acceleration data.
Algorithm 1 outlines the process of inputting initial generalized coordinates q 0 and velocities ζ 0 into SPEL.
Using subnetwork outputs for the mass matrix, dissipation matrix, potential energy, and control input matrix,
the Hamiltonian function is derived from mass and potential energy. Generalized coordinates and momenta
derivatives are computed via automatic differentiation with respect to q and p, followed by solving the Hamil-
tonian equations. Given that generalized momenta p are typically not directly measurable, their derivatives are
converted into generalized accelerations ζ˙ using the relationship between p and ζ. An ODE solver, initialized
with q 0 and ζ 0, computes the predicted values of q¯ 1 ,...,q¯ ∆t and ζ¯ 1 ,...,ζ¯ ∆t at time ∆t. These predictions are
compared with actual values to calculate the loss, along with a penalty loss for the positive definiteness of the
mass matrix, which is then used for backpropagation to update and optimize the neural network parameters.
Figure 2. Architecture of SPEL on Lie group: the red part represents a critical component of the framework,
wherein physical constraints are encoded into the neural network architecture; the green part denotes initial
values; the yellow part indicates sequence values.
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 6

www.nature.com/scientificreports/
Algorithm 1 SPEL on Lie group.
Physics-embedded sparse subnetwork optimization
Physical constraints can be imposed on the parameters learned by the subnetworks. Specifically, the mass matrix
must be positive definite, and the dissipation matrix must be positive semi-definite. These properties can be
ensured using Cholesky decomposition, which represents each matrix as the product of a lower triangular
matrix and its transpose, confirming their symmetry. Thus, only the diagonal elements and either the upper or
lower triangular elements need to be specified to define the entire matrix.
In the context of serial manipulator dynamics, when considering rotation about or translation along the
z-axis, the generalized velocities are expressed as angular velocity ω=[0 0 ω 1]T and linear velocity
v=[0 0 v 1]T . Therefore, in practical computations, only the elements in the last row and column of the
3 3 mass matrix on the Lie group are significant, while the other elements can be set to zero. For example,
×
in Duong’s work29, the mass matrix in the Hamiltonian dynamics of an inverted pendulum on the Lie group is
a 3 3 matrix with only one unknown parameter, while the other elements are zero. This study embeds these
×
physical insights into the mass network. To ensure the positive definiteness of the mass matrix, a small positive
constant ε is added to the diagonal elements, as shown in the Fig. 3. Therefore, the outputs of the mass network
and the dissipative network are computed as (n2+n)/2, where n is the number of diagonal elements in the
lower triangular matrix, and the mass matrix is a 3n 3n matrix.
×
Similar considerations apply to the dissipation matrix in serial manipulator dynamics. Only the elements in
the last row and column of the 3 3 dissipation matrix on the Lie group are meaningful during calculations,
×
while the remaining elements can be zero. Since the dissipation matrix is positive semi-definite, it does not
require the addition of a small positive constant ε to the diagonal elements.
Figure 3. Simplification of M-NN: ε is a small positive constant; n is the number of diagonal elements in the
lower triangular matrix.
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 7

www.nature.com/scientificreports/
The control input matrix is affected by the dynamic coupling between the joints, where each joint’s movement
influences the others. Effective control requires considering the system’s overall state and making the control
input matrix related to the coordinates of all joints. In practice, the control input matrix is often simplified by
computing it only along the z-axis, similar to the mass matrix, as shown in Fig. 4.
The potential energy is computed using a simple, fully connected neural network with a single output.
Network parameter conversion via physics-embedded outputs
For the constant values in the mass matrix and control input matrix, these constants are trained as parameters
of the network rather than as output nodes12. Define the matrix form of the generalized mass matrix M(q) as
|     |     |     |     |       | a+f 1 (q) | ... b+f | 2 (q) |     |     |      |
| --- | --- | --- | --- | ----- | --------- | ------- | ----- | --- | --- | ---- |
|     |     |     |     | M(q)= | ...       | ...     |       |     |     | (19) |
|     |     |     |     | [b+f  | (q)       | ... c   |       |     |     |      |
|     |     |     |     |       | 2         |         | ]     |     |     |      |
where a, b, c are constants, and f (q), f (q) are functions of the generalized coordinates q, with all quantities a,
|     |     |     |     | 1 2 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
b, c, f (q) and f (q) being scalar-valued. The i-th diagonal term of an n-axis manipulator’s mass matrix is the
|     | 1   | 2   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
equivalent inertia of links i to n (all links 1 to n) relative to joint i. Revolute joints use the parallel axis theorem for
inertia; prismatic joints use link masses. Non-diagonal (coupling) terms combine constants and joint position
functions. The n-th diagonal term, position-independent, is c; the first, with position-dependent components,
is a+f (q).
1
In the matrix M(q), only f (q) and f (q) depend on the input q. Constants a, b, and c are treated as network
|     |     |     |     | 1 2 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
parameters, initialized with initial values, and optimized through forward computation and backpropagation. The
functions f (q) and f (q) serve as the output nodes. This approach reduces the number of network parameters,
|     | 1   |     | 2   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
simplifies the model, avoids redundant learning, improves training efficiency, enhances interpretability, and
increases generalization. Specifically, for the mass matrix in the dynamics of the serial manipulator, this method
can be applied to optimize the network structure and improve performance.
For example, the mass matrix M rr(q) of a two-link (revolute-revolute) manipulator, as shown in Eq. (20),
includes constants J 1 and J 2, which represent the moments of inertia and are defined as J =m ST(e )S(e )
|     |     |     |     |     |     |     |     | 1   | 1   | 1 1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
and J =m ST(e )S(e ), where m 1 and m 2 are the masses of links. These constants are independent of
|     | 2   | 2   | 1 1 |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the generalized coordinates of the manipulator. Similarly, the mass matrix M rp(q) of a revolute-prismatic
(RP) manipulator, as shown in Eq. (20), includes the moments of inertia J 1 and mass m 2, both of which are
independent of the generalized coordinates. Therefore, these parameters can be iteratively optimized as part of
the network’s parameters rather than being treated as output nodes.
|              |     |        | J   | J m (q)     | J m(q) |           | J   | 0   |          |      |
| ------------ | --- | ------ | --- | ----------- | ------ | --------- | --- | --- | -------- | ---- |
|              | M   | rr(q)= | 1 + | 5 2 + 4     | 2 + 2  | ,M rp(q)= | 1   |     |          |      |
|              |     |        | J   | + 2 m( q )  | J      |           | 0   | m ( | e eT )   | (20) |
|              |     |        |     | 2           | 2      |           |     | 2·  | 3 3      |      |
|              |     |        | [   |             |        | ]         | [   |     | ]        |      |
|              |     | ST(e   | )0  | RT 0        |        |           |     |     |          |      |
| where m(q)=m |     | 2      | 1 2 | 1 RS(e 1 ). |        |           |     |     |          |      |
Equation (20) demonstrates that only part of the mass matrix for the two-link manipulator depends on the
generalized coordinates. As a result, the mass network for the RP manipulator comprises zero output nodes and
two network parameters, whereas the mass network for the two-link manipulator includes one output node and
necessitates two additional network parameters.
Experimental validation
The simulation experiments were conducted in Python 3.9.15 using the Robotics Toolbox41. For real-world
experiments, a 6-DOF serial manipulator from Zhongke Shengu was used, controlled by a system developed
with cSPACE. Software modules were developed using ARM Cortex-A and MATLAB/Simulink. The controller’s
internal processor is the TI Sitara AM4376. Joint modules use incremental encoders with 20,000 lines for motor
angle detection and absolute encoders with 17-bit resolution for joint angle measurement, achieving an angular

Figure 4. Simplification of G-NN: n is the number of output nodes.
8
Scientific Reports |        (2025) 15:33179  | https://doi.org/10.1038/s41598-025-17935-w

www.nature.com/scientificreports/

| Manipulator | θj(◦) dj(m) | aj(m) | αj(◦) | q−(◦) | q+(◦) |     |     |     |     |
| ----------- | ----------- | ----- | ----- | ----- | ----- | --- | --- | --- | --- |
|             | q1 0        | 1     | 0.0   | 180.0 | 180.0 |     |     |     |     |
| Two-Link    |             |       |       | −     |       |     |     |     |     |
|             | q2 0        | 1     | 0.0   | 180.0 | 180.0 |     |     |     |     |
−
|     | q1 0.154 | 0   | 90.0 | 170.0 | 170.0 |     |     |     |     |
| --- | -------- | --- | ---- | ----- | ----- | --- | --- | --- | --- |
−
| RPR | 90 q2 | 0.0203 | 0.0 | 0.305 | 1.27 |     |     |     |     |
| --- | ----- | ------ | --- | ----- | ---- | --- | --- | --- | --- |
−
|     | q3 0 | 0   | 0.0 | 170.0 | 170.0 |     |     |     |     |
| --- | ---- | --- | --- | ----- | ----- | --- | --- | --- | --- |
−
|     | q1 122.3 | 0   | 0.0 | 179.0 | 179.0 |     |     |     |     |
| --- | -------- | --- | --- | ----- | ----- | --- | --- | --- | --- |
−
|     | q2 0 | 0   | 90.0 | 152.0 | 152.0 |     |     |     |     |
| --- | ---- | --- | ---- | ----- | ----- | --- | --- | --- | --- |
−
|     | q3 0 | -270 | 0.0 | 146.0 | 146.0 |     |     |     |     |
| --- | ---- | ---- | --- | ----- | ----- | --- | --- | --- | --- |
−
Real
|     | q4 123.3 | -253 | 0.0 | 179.0 | 179.0 |     |     |     |     |
| --- | -------- | ---- | --- | ----- | ----- | --- | --- | --- | --- |
−
|     | q5 107.1 | 0   | 90.0 | 179.0 | 179.0 |     |     |     |     |
| --- | -------- | --- | ---- | ----- | ----- | --- | --- | --- | --- |
−
|     | q6 99.1 | 0   | 90.0 | 179.0 | 179.0 |     |     |     |     |
| --- | ------- | --- | ---- | ----- | ----- | --- | --- | --- | --- |
|     |         |     | −    | −     |       |     |     |     |     |
Table 1. DH parameters.
|             |             | I(kg m2)      |     |             | Jm (kg m2) |          |     | Tc(N)             |     |
| ----------- | ----------- | ------------- | --- | ----------- | ---------- | -------- | --- | ----------------- | --- |
| Manipulator | Links m(kg) |               |     | r(m)        |            | B(N s/m) |     |                   | G   |
|             | Link1 1     | [1,1,1,1,1,1] |     | [− 0.5,0,0] | 0          | 1.48     | 10− | 3 [0.395,− 0.435] | 1   |
×
Two-Link
|     | link2 1 | [1,1,1,1,1,1] |     | [− 0.5,0,0] | 0   | 8.17 | 10− | 4 [0.126,− 0.071] | 1   |
| --- | ------- | ------------- | --- | ----------- | --- | ---- | --- | ----------------- | --- |
×
|     | Link1 5.01 | [0.108,0.018,0.1,0,0,0] |     | [0,− 1.05,0] | 2.19 | 1.48 | 10− | 3 [0.395,− 0.435] | 1   |
| --- | ---------- | ----------------------- | --- | ------------ | ---- | ---- | --- | ----------------- | --- |
×
RPR Link2 4.25 [2.51,2.51,0.006,0,0,0] [0,0,− 6.45] 0.782 1.67 10− 3 [0.126,− 0.071] 1
×
3
|     | Link3 1.08 | [0.002,0.001,0.001,0,0,0] |     | [0,0.092,− 0.054] | 0.106 | 1.817 | 10− | [0.126,− 0.171] | 1   |
| --- | ---------- | ------------------------- | --- | ----------------- | ----- | ----- | --- | --------------- | --- |
×
Table 2. Model parameters.
resolution of 0.0045◦ . Algorithm training was performed on a system equipped with a GeForce RTX 4090 GPU
and 24 GB of memory.
Data acquisition
Numerical simulations provide effectively infinite sampling frequency and zero noise, enabling the generation
of multiple datasets to assess algorithm sensitivity across various parameter values. This study uses the Robotics
Toolbox to model a two-link and a revolute-prismatic-revolute (RPR) manipulator, with their DH parameters
and other parameters (mass, friction coefficients) detailed in Tables 1 and 2, respectively. In this work, following
the experimental design in Zhong’s work26, the control input u for each link is set to one of
|     |     |     |     |     |     |     |     |     | 2, 1,0,1,2  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- |
− −
at a sampling frequency of 20 Hz. Dynamic simulations start from 64 different initial positions, collecting
position, velocity, and force data for each joint over 1 second, ensuring data remain within normal ranges.
Angular coordinates are converted into rotation matrices using DH parameters, and translational coordinates
are extended to three dimensions. The dataset for the two-link manipulator contains 11520 samples, while the
dataset for the RPR manipulator includes 7680 samples. For training, the first 0.25 seconds of sequence data
are used, with 50% of the dataset allocated to the training set and 50% to the test set. The control input matrix
1]T. For the RPR manipulator,
| B(q) for the two-link manipulator is defined as B(q)=[0 |     |     |     |     | 0   | 1 0 0 |     |     |     |
| ------------------------------------------------------- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
1]T.
| the control input matrix B(q) is given by B(q)=[0 |     |     |     |     | 0 1 0 | 0 1 | 0 0 |     |     |
| ------------------------------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
In addition to simulation data, this study uses experimental data from a real 6-DOF manipulator to
validate the method’s effectiveness in dynamic prediction. PID control is applied to each joint with a sampling
frequency of 500Hz and a control frequency of 125Hz; for PID control, the trajectory is a sinusoidal curve with
a frequency of 1/8 Hz and an amplitude of 30◦, with tracking errors ranging from  0.4◦ to +0.4◦. Six sets of
−
different PID parameters are configured to ensure normal operation, collecting position and torque data for
each joint. Collected position data are processed using a zero-phase filter to eliminate phase delay and reduce
high-frequency noise, preserving signal phase information and improving signal quality. Velocity is calculated
using a differential method. Angular coordinates are converted into rotation matrices using DH parameters.
Data not conforming to the 4:1 ratio between sampling and control frequencies are excluded. For each set of
PID parameters, the first 1,000 samples of position, velocity, and torque are selected to form a dataset of 24,000
samples. Seventy percent of this dataset is used for training and 30% for testing.
In the experiments, the following models are employed to obtain the dynamics for both the simulated and
real manipulator on Lie groups: PHNODEs, symplectic physics-embedded learning-KAN (SPEL-KAN), and
SPEL. The PHNODEs employ Cholesky decomposition for the mass network and the dissipation network
without any additional modifications. The SPEL-KAN substitutes the MLP with KAN. All experiments adopt
the AdamW optimizer with a learning rate of 0.001. The goal is to evaluate the accuracy and physical plausibility
of the proposed methods. Performance is assessed using MSE based on training and testing trajectory errors,
and the results are compared with other models to determine relative accuracy and effectiveness.
9
Scientific Reports |        (2025) 15:33179  | https://doi.org/10.1038/s41598-025-17935-w

www.nature.com/scientificreports/
Simulation results
Two-link manipulator
The two-link manipulator is shown in Fig. 5a. The manipulator operates in the xy-plane, with uniformly
distributed material and mass along the links.
As shown in Fig. 5a, the equation of motion for the two-link manipulator on the Lie groups is given by:
0 1 R˙ =0 1 RS(ω 1 ),0 2 R˙ =0 2 RS(ω 1 +ω 2 ),0 2 R=0 1 R1 2 R (21)
cosθ sinθ 0 cosθ sinθ 0
0 1 R= sinθ 1 1 −cosθ 1 1 0 ,1 2 R= sinθ 2 2 −cosθ 2 2 0 (22)
[ 0 0 1] [ 0 0 1]
where ω 1 and ω 2 represent the angular velocities of the links, given by 0 0 θ˙ 1 T and
0 0 θ˙ 2 T , respectively, with the direction around the z-axis. S(ω 1 ) and S(ω 2 ) denote [the skew-sy]mmetric
[ matrices cor ] responding to ω 1 and ω 2.
mas I s n o t f h t e h b e a s s e e c o co n o d r l d in in k a t i e s l f o ra c m ate e d , t a h t e a c 1 en 0 1 t R er e 1 of + m 1 2 as a s 2 o 0 2 f R th e e 1 . fi e rs 1 t i l s i n th k e i s u n lo it c a v t e e c d t o a r t [1 1 2 a 1 0 0 1 Re 0] 1 T a . n Th d e th L e a c g e r n an te g r i a o n f
function of the two-link manipulator is given by:
L(R,ω)= 1 2 m 1 0 1 R˙e 1 2 + 1 2 m 2 20 1 R˙e 1 +0 2 R˙e 1 2 − m 1 geT 2 0 1 Re1− m 2 geT 2 20 1 Re1 +0 2 Re1 (23)
(cid:31) (cid:31) (cid:31) (cid:31) (cid:30) (cid:29)
The dynamic equati(cid:31)ons bas(cid:31)ed on the L(cid:31)agrangian formula(cid:31)tion can be derived as follows:
τ J +5J +4m ST(e )2RT 0RS(e ) J +2m ST(e )2RT 0RS(e ) ω˙
1 = 1 2 2 1 0 1 1 2 2 1 0 1 1 1
[ τ 2 ] [ J 2 +2m 2 ST(e 1 )2 0 RT 0 1 RS(e 1 ) J 2 ][ ω˙ 2 ]
2m 0RT 0RS(e )ω S(e )ω 4m 0RT 0RS(e )ω S(e )ω
+ − 2 2 1 2 1 m 2 0× RT 0R 1 S( 2 e − )ω 2 2 S(e 1 )ω 1 1× 2 2 (24)
[ 2 2 1 1 1× 1 1 ]
m g 0RTe e (m +2m )g 0RTe e
+ 2 2 2×
2m
1−
g 0R
1
Te
2
e
1 2× 1
[ − 2 2 2× 1 ]
where J 1 =m 1 ST(e 1 )S(e 1 ),J 2 =m 2 ST(e 1 )S(e 1 ).
The mass matrix is derived as shown in Eq. (20). The potential energy is as follows
3 1
V(q)= −2 m 1 ga 1 eT 2 0 1 Re1− 2 m 2 ga 2 eT 2 0 2 Re1 (25)
Figure 5. Schematic diagram of manipulator structure(3D visualization generated using MATLAB R2023a (
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 10

www.nature.com/scientificreports/

Figure 6. Losses for various network architectures on the two-link manipulator.
|                     | PHNODEs SPEL    | SPEL-KAN   |      |
| ------------------- | --------------- | ---------- | ---- |
| M-NN Outputs        | 21 1            | 1          |      |
| V-NN Outputs        | 1 1             | 1          |      |
| D-NN Outputs        | 21 3            | 3          |      |
| G-NN Outputs        | 6 0             | 0          |      |
| Parameters          | 277,319 56,165  | 13,604     |      |
| Activation function | tanh tanh       | learned    |      |
| Training loss       | 8.51 10− 3 8.01 | 10− 3 7.39 | 10−3 |
|                     | ×               | ×          | ×    |
| Training time(s)    | 1.81 0.31       | 0.82       |      |
| Prediction loss     | 0.194 0.113     | 0.160      |      |
Table 3. Comparison of different neural network architectures for two-link manipulator dynamics learning. 1
-KAN indicates that the internal MLP has been replaced with a KAN. 2 M-NN Outputs, V-NN Outputs, D-NN
Outputs, and G-NN Outputs denote the output nodes of the M-NN, V-NN, D-NN, and G-NN, respectively. 3
Training time includes the sum of forward computation time and backpropagation time
In summary, in SPEL and SPEL-KAN, the mass network is designed with 1 output node and 18 input nodes, with
J 1 and J 2 set as network parameters. The control input network is configured such that its values are also set as
network parameters, with zero output nodes.
Based on Fig. 6 and Table 3, the performance of SPEL in learning the dynamics of a two-link manipulator
can be evaluated. The subnetworks incorporate prior information about the manipulator’s dynamics, facilitating
the learning of the underlying physical model. The proposed methods achieve equivalent modeling with fewer
output nodes and network parameters, validating the effectiveness of the added physical constraints. The y Table
S1 presents the obtained mass matrices and verifies their properties.
The model is trained using the first 0.25s of data and test set control inputs to predict state loss (for R and ω)
over a 1s interval, thereby obtaining prediction loss. As illustrated in Table 3, Figs. 6, and 7, the proposed method
reduces the number of output nodes, thereby lowering the dimensionality of dynamic parameter estimation
and compressing the network parameter space, which in turn reduces model complexity. Specifically, SPEL and
SPEL-KAN reduce the parameter counts to 20% and 5% of the original PHNODEs model, respectively. By
minimizing the output nodes of M-NN and D-NN and eliminating G-NN, the method effectively removes
redundant computations from the original model.
SPEL-KAN  enhances  efficiency  by  substituting  fixed  tanh  activation  functions  with  learnable  ones,
maintaining lower training errors even with only 24% of SPEL’s parameter count. This demonstrates significant
parameter  efficiency,  potentially  alleviating  the  need  for  manual  network  architecture  design  through
adaptive feature extraction. Compared to fixed tanh activations, learnable activations reduce training loss by
7.7%, underscoring the importance of dynamically adjusting nonlinear features. However, this improvement
introduces additional computational overhead, increasing training time from 0.31s to 0.82s. Despite achieving
optimal training loss, SPEL-KAN exhibits higher prediction errors than SPEL, indicating potential overfitting
risks. These findings offer new insights into lightweight network design, suggesting that dynamic activations can
compensate for reduced network depth.
SPEL achieves the highest computational efficiency, running 5.8 times faster than PHNODEs, primarily
because of its reduced parameter count and simplified computational graphs. In practical engineering applications
with constrained hardware resources, SPEL optimally balances speed and accuracy. For scenarios demanding
extremely lightweight models, developing specialized acceleration algorithms for SPEL-KAN is essential.
Revolute-prismatic-revolute manipulator
In this section, experiments are conducted using an RPR manipulator, as illustrated in Fig. 5b. The RPR
manipulator, which includes an additional prismatic joint compared to the two-link manipulator, has the linear
11
Scientific Reports |        (2025) 15:33179  | https://doi.org/10.1038/s41598-025-17935-w

www.nature.com/scientificreports/
Figure 7. Comparison of predicted values for ω and θ across different networks in a two-link manipulator.
velocity of the second link denoted as v, directed along the z-axis. In the base coordinate frame, the center of mass
of the first link is located at 1 2 d 1 0 1 Re3, the center of mass of the second link is located at d 1 0 1 Re3 + 1 2 q 2 0 2 Re3,
and the center of mass of the third link is located at d 1 0 1 Re3 +q 2 0 2 Re3 + 1 2 a 3 0 3 Re3. The potential energy is
as follows
1 1
V(q)=
−2
m
1
gd
1
eT
3 1
0Re3− m
2
geT
3
(d
1
0
1
Re3 +
2
q
2
0
2
Re3 )
(26)
1
−
m
3
geT
3
(d
1
0
1
Re3 +q
2
0
2
Re3 +
2
a
3
0
3
Re3 )
In the mass matrix of the RPR manipulator, based on the physical interpretation of the mass matrix, the last
diagonal element corresponds to the moment of mass of the third link, as the third joint is a revolute joint. The
middle diagonal element corresponds to the sum of the masses of the second and third links since the second
joint is a prismatic joint.
In summary, in SPEL and SPEL-KAN, this work designs the mass network with 3 output nodes and 21 input
nodes, with two elements on the diagonal set as network parameters. The control input network is designed with
3 output nodes and 21 input nodes. Consequently, the training results are shown in the following figure.
The model is trained using the first 0.25s of data and test set control inputs to predict state loss (for R and
ω) over a 1s interval, thereby obtaining prediction loss. Based on Fig. 8 and Table 4, SPEL effectively learns the
dynamics of the RPR manipulator, which includes both prismatic and revolute joints. With a smaller network
structure and fewer parameters, SPEL incorporates prior information about the RPR manipulator’s dynamics
into its subnetworks, enabling the learning of the underlying physical model and demonstrating superior
modeling performance.
The proposed methods achieve equivalent modeling with fewer output nodes and network parameters,
validating the effectiveness of the added physical constraints. Specifically, the process reduces the number of
output nodes compared to the original PHNODEs model by integrating physical priors deeply into the network.
This approach focuses on modeling manipulator dynamics rather than full-state prediction through physical
constraints such as sparse matrices and constant elements, thereby compressing the network parameter space.
Consequently, model complexity and trainable parameters are reduced, with SPEL and SPEL-KAN having 36.7%
and 36% of the parameters of the original model, respectively.
In terms of computational efficiency, SPEL exhibits superior performance with the shortest training
time, achieving a speedup of 4.8 times compared to PHNODEs. This improvement results from reduced
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 12

www.nature.com/scientificreports/

Figure 8. Losses for various network architectures on the RPR manipulator.
|                     | PHNODEs SPEL    | SPEL-KAN |     |
| ------------------- | --------------- | -------- | --- |
| M-NN Outputs        | 45 3            | 3        |     |
| V-NN Outputs        | 1 1             | 1        |     |
| D-NN Outputs        | 45 6            | 6        |     |
| G-NN Outputs        | 9 3             | 3        |     |
| Parameters          | 329,700 121,053 | 118,812  |     |
| Activation function | tanh tanh       | learned  |     |
3
| Training loss    | 7.27 10− 6.92 | 10− 3 6.65 | 10−3 |
| ---------------- | ------------- | ---------- | ---- |
|                  | ×             | ×          | ×    |
| Training time(s) | 3.41 0.71     | 2.08       |      |
| Prediction loss  | 1.30 0.193    | 0.192      |      |
Table 4. Comparison of different neural network architectures for RPR manipulator dynamics learning. 1
-KAN indicates that the internal MLP has been replaced with a KAN. 2 M-NN Outputs, V-NN Outputs, D-NN
Outputs, and G-NN Outputs denote the output nodes of the M-NN, V-NN, D-NN, and G-NN, respectively. 3
Training time includes the sum of forward computation time and backpropagation time
backpropagation computation and simplified computational graphs. Although the training time for SPEL-KAN
increases to 2.08 seconds due to the additional computational overhead from optimizing learnable activation
functions, its parameter efficiency remains competitive. These methods are particularly significant for real-
time online learning scenarios, with SPEL being suitable for high-frequency updates and SPEL-KAN more
appropriate for offline optimization scenarios.
As illustrated in Figs. 8 and 9, prediction loss decreases from 1.30 in PHNODEs to 0.193 for SPEL and 0.192
for SPEL-KAN, marking an accuracy improvement of approximately 6.7 times. This reduction in prediction loss
is significantly greater than the improvement in training loss (8.5% vs. 85%), indicating that the models more
effectively capture the essential dynamics.
The use of learnable activations in KAN enhances nonlinear expression capabilities and improves dynamic
feature  extraction,  resulting  in  better  generalization.  Although  this  optimization  introduces  increased
computational complexity, it allows for a more compact parameter distribution. By trading off some training
speed, KAN achieves higher modeling accuracy and shows a slight advantage during the prediction phase.
Real 6-DOF manipulator
In this section, experiments are conducted using a real 6-DOF manipulator. The real 6-DOF manipulator has
six rotational degrees of freedom, as shown in the Fig. 10. The DH parameters for this manipulator are provided
in Table 1.
In SPEL and SPEL-KAN, the mass network has 20 output nodes, whereas, in PHNODEs, it has 171 output
nodes. For the control input network, both SPEL and SPEL-KAN are designed with 6 output nodes, compared to
18 output nodes in PHNODEs. Similarly, the dissipation network in SPEL and SPEL-KAN has 21 output nodes,
while PHNODEs have 171 output nodes. Consequently, the training losses are as shown in the Fig. 11. In the
training loss curves, PHNODE exhibits the most severe oscillations, followed by SPEL, while SPEL-KAN shows
a nearly flat curve. PHNODE’s unconstrained network outputs for mass, dissipation, and control matrices render
it sensitive to noise from joint friction and sensor errors. SPEL reduces overfitting by compressing the parameter
space with physical constraints, and SPEL-KAN further smooths fluctuations via learnable activation functions.
Despite PHNODE converging, SPEL and SPEL-KAN demonstrate more stable convergence, highlighting the role
of physical constraints in enhancing optimization stability and generalization, validating the study’s approach.
As shown in Table 5, the proposed method reduces redundant computations and matches the independent
matrix elements by embedding physical priors and applying constraints like sparse matrices and constant
elements. This compresses the network parameter space, reducing model complexity. SPEL and SPEL-KAN
13
Scientific Reports |        (2025) 15:33179  | https://doi.org/10.1038/s41598-025-17935-w

www.nature.com/scientificreports/
Figure 9. Comparison of predicted values for ω and θ across different networks in an RPR manipulator.
Figure 10. Real 6-DOF manipulator(Graphical reconstruction by authors based on original
macrophotography ([iqoo neo5], [2025.02.03]), with dimensional enhancement via Microsoft PowerPoint
2021(
achieve respective parameter reductions of 52.1% and 73.8% compared to PHNODEs, thereby improving
parameter efficiency and reducing memory usage.
SPEL achieves a 4.7-fold reduction in training time due to simplified gradient flows within physics-
constrained architectures. In contrast, SPEL-KAN’s training time is 1.7 times longer than SPEL, resulting from
the computational overhead associated with learning activation functions, yielding a minimal improvement in
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 14

www.nature.com/scientificreports/

Figure 11. Losses for various network architectures applied to the real manipulator.

|                     | PHNODEs    | SPEL     | SPEL-KAN    |
| ------------------- | ---------- | -------- | ----------- |
| M-NN Outputs        | 171        | 20       | 20          |
| V-NN Outputs        | 1          | 1        | 1           |
| D-NN Outputs        | 171        | 21       | 21          |
| G-NN Outputs        | 18         | 6        | 6           |
| Parameters          | 326,911    | 156,359  | 85,521      |
| Activation function | tanh       | tanh     | learned     |
|                     | 8.13 10− 3 | 7.99 10− | 3 7.96 10−3 |
| Training loss       | ×          | ×        | ×           |
| Training time(s)    | 17.70      | 3.76     | 6.44        |
3
| Test loss | 9.62 10− | 8.77 10−3 | 9.07 10− 3 |
| --------- | -------- | --------- | ---------- |
|           | ×        | ×         | ×          |
Table 5. Comparison of different neural network architectures for real manipulator dynamics learning. 1
-KAN indicates that the internal MLP has been replaced with a KAN. 2 M-NN Outputs, V-NN Outputs, D-NN
Outputs, and G-NN Outputs denote the output nodes of the M-NN, V-NN, D-NN, and G-NN, respectively. 3
Training time includes the sum of forward computation time and backpropagation time
training loss of 0.38%. The time-to-accuracy ratio of SPEL-KAN stands at 17.0 seconds per 0.01 loss reduction,
compared to 3.8 seconds for SPEL, posing questions regarding its suitability for online learning scenarios.
While SPEL achieves the lowest test loss, SPEL-KAN’s higher test error despite lower training loss reveals
a 14.0% overfitting gap, up from SPEL’s 9.8%. This implies that KAN’s flexible activations may overfit noise in
dynamics data, though its parameter efficiency partially mitigates this through inherent regularization.
Figure 12 presents the predicted joint velocities for joints 1-6 of the serial manipulator across various
networks, while Fig. 13 shows the prediction joint positions of joints 1-6 using the SPEL network. As shown in
Table 6, quantifying the prediction errors for the dynamics of a 6-DOF manipulator, SPEL reduces overall errors
by 69.1% in ζ predictions compared to PHNODEs, with the greatest improvement (77.8% reduction) observed
in joint 6 under high dynamic loads. This validates the precise modeling capability of physical constraints
for complex end-effector dynamics. Although SPEL-KAN slightly increases total error by 2.0%, it maintains
the lowest error in joint 6, indicating that the KAN structure enhances nonlinear feature extraction through
learnable activation functions.
In q predictions, SPEL-KAN achieves the best performance, representing a 0.34% reduction compared to
PHNODEs. Notably, the error for low-inertia joint 1 decreases by 39.3%, highlighting the synergistic effect of
physical constraints and adaptive activations—where physical constraints reduce overfitting risk by compressing
the parameter space, while adaptive activations improve the capture of high-frequency signals.
Conclusion
This study proposes a SPEL method for serial manipulators on Lie groups, achieving precise dynamic prediction
by integrating physical information directly into a nonlinear ordinary differential equation system. By analyzing
Hamiltonian dynamics on Lie groups, the research presents a port-Hamiltonian dynamics model for the multi-
rigid-body serial manipulator that incorporates Lie group kinematics and dynamic constraints.
The analysis emphasizes the sparse matrix properties of the mass, dissipation, and control input matrices.
Incorporating these structures into neural network design minimizes output layer nodes and trainable
parameters through leveraging known constant information. Enhancements to the dissipation network address
joint friction, while the introduction of KAN further improves accuracy and reduces trainable parameters via
learnable activation functions, extending KAN’s applicability to complex systems.
15
Scientific Reports |        (2025) 15:33179  | https://doi.org/10.1038/s41598-025-17935-w

www.nature.com/scientificreports/
Figure 12. Prediction results of various networks for ζ with experimental data.
Figure 13. Prediction results of SPEL for q with experimental data.
Evaluations using data from a two-link manipulator and an RPR manipulator, along with data from a real
6-dof manipulator, confirm high predictive accuracy and computational efficiency. Compared to PHNODEs,
both SPEL and SPEL-KAN reduce output nodes and trainable parameters, simplify the computational graph,
and improve convergence rates. SPEL shows faster computational efficiency, while SPEL-KAN has lower training
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 16

www.nature.com/scientificreports/
Model Joint 1 Joint 2 Joint 3 Joint 4 Joint 5 Joint 6 Sum
PHNODEs 1.90
×
10− 3 4.90
×
10− 3 8.60
×
10− 3 6.30
×
10− 3 1.08
×
10− 2 4.69
×
10− 2 7.93
×
10− 2
ζ SPEL 1.10
×
10−3 2.10
×
10− 3 3.20
×
10−3 3.40
×
10−3 4.30
×
10−3 1.04
×
10− 2 2.45
×
10−2
SPEL-KAN 1.30
×
10− 3 2.00
×
10−3 3.40
×
10− 3 3.80
×
10− 3 4.40
×
10− 3 1.01
×
10−2 2.50
×
10− 2
PHNODEs 6.67
×
10− 9 2.00
×
10− 4 8.08
×
10− 8 5.55
×
10− 8 2.30
×
10− 3 2.20
×
10− 3 4.707
×
10− 3
q SPEL 4.13
×
10− 9 2.00
×
10− 4 1.45
×
10−8 1.51
×
10−8 2.30
×
10− 3 2.20
×
10− 3 4.693
×
10− 3
SPEL-KAN 4.05
×
10−9 2.00
×
10− 4 3.61
×
10− 8 2.00
×
10− 8 2.30
×
10− 3 2.20
×
10− 3 4.691
×
10−3
Table 6. The data in the table represents the MSE between the actual and predicted values of ζ and q for each
joint. 1 -KAN indicates that the internal MLP has been replaced with a KAN
losses and fewer trainable parameters. These results highlight SPEL’s advantages in parameter reduction and
convergence rate, making it a preferred choice for robotic applications.
Despite these achievements, the model’s performance depends heavily on the accuracy of integrated physical
information. Although significant reductions in trainable parameters and improvements in convergence speed
were observed, further optimization of input layer nodes is required for maximum efficiency. Future work will
focus on minimizing the number of input layer nodes in SPEL on Lie groups, conducting thorough comparisons
with traditional methods, and exploring applications in parameter identification. These efforts aim to enhance
model efficiency and deepen understanding of underlying dynamics, thereby advancing robotic control and
dynamic modeling.
Data availability
The data supporting the findings of this study are available from the corresponding author upon request.
Received: 9 May 2025; Accepted: 28 August 2025
References
1. Su, H., Yang, C., Ferrigno, G. & De Momi, E. Improved human–robot collaborative control of redundant robot for teleoperated
minimally invasive surgery. IEEE Robot. Autom. Lett. 4, 1447–1453. https://doi.org/10.1109/LRA.2019.2897145 (2019).
2. Gualtieri, L., Palomba, I., Wehrle, E. & Vidoni, R. The opportunities and challenges of sme manufacturing automation: Safety and
ergonomics in human–robot collaboration. Industry 4.0 for SMEs (2020).
3. Zhou, Z. et al. Learning-based object detection and localization for a mobile robot manipulator in sme production. Robot. Comput.
Integr. Manuf. 73, 102229. https://doi.org/10.1016/j.rcim.2021.102229 (2022).
4. Yang, X. et al. Dynamic modeling and digital twin of a harmonic drive based collaborative robot joint. In 2022 International
Conference on Robotics and Automation (ICRA), 4862–4868, https://doi.org/10.1109/ICRA46639.2022.9812458 (2022).
5. Yang, X., Zhou, Z., Li, L. & Zhang, X. Collaborative robot dynamics with physical human–robot interaction and parameter
identification with pinn. Mech. Mach. Theory (2023).
6. Janot, A., Vandanjon, P.-O. & Gautier, M. A generic instrumental variable approach for industrial robot identification. IEEE Trans.
Control Syst. Technol. 22, 132–145. https://doi.org/10.1109/TCST.2013.2246163 (2014).
7. Yang, X., Du, Y., Li, L., Zhou, Z. & Zhang, X. Physics-informed neural network for model prediction and dynamics parameter
identification of collaborative robot joints. IEEE Robot. Autom. Lett. 8, 8462–8469. https://doi.org/10.1109/LRA.2023.3329620
(2023).
8. Vicentini, F. Collaborative robotics: A survey. J. Mech. Des. 143, 040802. https://doi.org/10.1115/1.4046238 (2020).
9. Leboutet, Q., Roux, J., Janot, A., Guadarrama-Olvera, J. R. & Cheng, G. Inertial parameter identification in robotics: A survey. Appl.
Sci. 11, 4303 (2021).
10. Ljung, L., Andersson, C. R., Tiels, K. & Schön, T. B. Deep learning and system identification. IFAC-PapersOnLine (2020).
11. Wang, G., Jia, Q.-S., Qiao, J., Bi, J. & Zhou, M. Deep learning-based model predictive control for continuous stirred-tank reactor
system. IEEE Trans. Neural Netw. Learn. Syst. 32, 3643–3652. https://doi.org/10.1109/TNNLS.2020.3015869 (2021).
12. Raissi, M., Perdikaris, P. & Karniadakis, G. E. Physics-informed neural networks: A deep learning framework for solving forward
and inverse problems involving nonlinear partial differential equations. J. Comput. Phys. 378, 686–707 (2019).
13. Nicodemus, J., Kneifl, J., Fehr, J. & Unger, B. Physics-informed neural networks-based model predictive control for multi-link
manipulators. IFAC-PapersOnLine55, 331–336. https://doi.org/10.1016/j.ifacol.2022.09.117 (2022).
14. Hao, Z. et al. Physics-informed machine learning: A survey on problems, methods and applications. ArXiv arXiv:abs/2211.08064
(2022).
15. Nghiem, T. X. et al. Physics-informed machine learning for modeling and control of dynamical systems. In 2023 American Control
Conference (ACC), 3735–3750, https://doi.org/10.23919/ACC55779.2023.10155901 (2023).
16. Kamp, T., Ultsch, J. & Brembeck, J. Closing the Sim-to-Real Gap with Physics-Enhanced Neural ODEs. In Gini, G., Nijmeijer,
H. & Filev, D. (eds.) 20th International Conference on Informatics in Control, Automation and Robotics (ICINCO), vol. 2, 77–84
(SCITEPRESS, Rom, Italien, 2023). ISSN: 2184-2809.
17. Haywood-Alexander, M., Liu, W., Bacsa, K., Lai, Z. & Chatzi, E. Discussing the spectrum of physics-enhanced machine learning:
a survey on structural mechanics applications. Data-Centric Eng. 5, e31. https://doi.org/10.1017/dce.2024.33 (2024).
18. Wang, R., Walters, R. & Yu, R. Incorporating symmetry into deep dynamics models for improved generalization. In International
Conference on Learning Representations (2021).
19. Sanchez-Gonzalez, A. et al. Graph networks as learnable physics engines for inference and control. In International Conference on
Machine Learning (2018).
20. Lutter, M., Ritter, C. & Peters, J. Deep lagrangian networks: Using physics as model prior for deep learning. In International
Conference on Learning Representations (2019).
21. Greydanus, S., Dzamba, M. & Yosinski, J. Hamiltonian neural networks. In Wallach, H. et al. (eds.) Advances in Neural Information
Processing Systems, vol. 32 (Curran Associates, Inc., 2019).
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 17

www.nature.com/scientificreports/
22. Cranmer, M. et al. Lagrangian neural networks. In ICLR 2020 Workshop on Integration of Deep Neural Models and Differential
Equations (2019).
23. Gupta, J. K., Menda, K., Manchester, Z. & Kochenderfer, M. Structured mechanical models for robot learning and control. In
Bayen, A. M. et al. (eds.) Proceedings of the 2nd Conference on Learning for Dynamics and Control, vol. 120 of Proceedings of
Machine Learning Research, 328–337 (PMLR, 2020).
24. Qian, J., Xu, L., Ren, X. & Wang, X. Structured deep neural network-based backstepping trajectory tracking control for lagrangian
systems. IEEE Trans. Neural Netw. Learn. Syst. 1–7. https://doi.org/10.1109/TNNLS.2024.3445976 (2024).
25. Chen, Z., Zhang, J., Arjovsky, M. & Bottou, L. Symplectic recurrent neural networks. In International Conference on Learning
Representations (2020).
26. Zhong, Y. D., Dey, B. & Chakraborty, A. Symplectic ode-net: Learning hamiltonian dynamics with control. In International
Conference on Learning Representations (2020).
27. Wu, S., Li, Z., Chen, W. & Sun, F. Dynamic modeling of robotic manipulator via an augmented deep lagrangian network. Tsinghua
Sci. Technol. 29, 1604–1614. https://doi.org/10.26599/TST.2024.9010011 (2024).
28. Liu, J., Borja, P. & Della Santina, C. Physics-informed neural networks to model and control robots: A theoretical and experimental
investigation. Adv. Intell. Syst. 6, 2300385. https://doi.org/10.1002/aisy.202300385 (2024).
29. Duong, T. P., Altawaitan, A., Stanley, J. & Atanasov, N. Port-hamiltonian neural ode networks on lie groups for robot dynamics
learning and control. IEEE Trans. Rob. 40, 3695–3715 (2024).
30. Spong, M. Remarks on robot dynamics: canonical transformations and riemannian geometry. In Proceedings 1992 IEEE
International Conference on Robotics and Automation, 554–559 1, https://doi.org/10.1109/ROBOT.1992.220234 (1992).
31. Lou, A. et al. Neural manifold ordinary differential equations. In Larochelle, H., Ranzato, M., Hadsell, R., Balcan, M. & Lin, H.
(eds.) Advances in Neural Information Processing Systems, vol. 33, 17548–17558 (Curran Associates, Inc., 2020).
32. Altawaitan, A., Stanley, J., Ghosal, S., Duong, T. & Atanasov, N. Hamiltonian dynamics learning from point cloud observations
for nonholonomic mobile robot control. CoRRabs/2309.09163, https://doi.org/10.48550/ARXIV.2309.09163 (2023).
arXiv:2309.09163.
33. Liu, Z. et al. KAN: Kolmogorov-arnold networks. In The Thirteenth International Conference on Learning Representations (2025).
34. Liu, Z., Ma, P., Wang, Y., Matusik, W. & Tegmark, M. Kan 2.0: Kolmogorov-arnold networks meet science. arXiv:abs/2408.10205
(2024).
35. Featherstone, R. Rigid Body Dyn. Algorithms (Springer, US, Boston, MA, 2008).
36. Richard M. Murray, S. S. S., Zexiang Li. A Mathematical Introduction to Robotic Manipulation (CRC Press, 1994).
37. Di Natale, L., Svetozarevic, B., Heer, P. & Jones, C. Towards scalable physically consistent neural networks: An application to data-
driven multi-zone thermal building models. Appl. Energy 340, 121071. https://doi.org/10.1016/j.apenergy.2023.121071 (2023).
38. Solà, J., Deray, J. & Atchuthan, D. A micro lie theory for state estimation in robotics (2021). arXiv:1812.01537.
39. Lee, T., Leok, M. & McClamroch, N. H. Global Formulations of Lagrangian and Hamiltonian Dynamics on Manifolds (Interaction
of Mechanics and Mathematics (Springer International Publishing, Cham, 2018).
40. Duong, T. & Atanasov, N. Hamiltonian-based Neural ODE Networks on the SE(3) Manifold For Dynamics Learning and Control.
In Proceedings of Robotics: Science and Systems. https://doi.org/10.15607/RSS.2021.XVII.086 (Virtual, 2021).
41. Corke, P. & Haviland, J. Not your grandmother’s toolbox–the robotics toolbox reinvented for python. In 2021 IEEE International
Conference on Robotics and Automation (ICRA), 11357–11363 (IEEE, 2021).
Acknowledgements
We would like to thank the reviewers for their thoughtful feedback, for the considerable improvement of our
paper. The authors would like to thank Zhongke Shengu for the robotic arm equipment technical support and
the laboratory staff for their technical assistance. This research has not received a specific grant from any funding
agency.
Author contributions
F.W, L.P.C, J.W.D participated in the writing of the paper, the work plan, the methods of analysis of sampling
and validation. F.W participated in the revision and correction of the article for the submission of the paper. All
authors have reviewed the manuscript and accepted its submission.
Declarations
Competing interests
The authors declare no competing interests.
Additional information
Supplementary Information The online version contains supplementary material available at h t t ps : / / d o i . o rg / 1
0 . 1 0 3 8 /s 4 1 5 9 8 - 0 2 5- 1 7 9 3 5 - w .
Correspondence and requests for materials should be addressed to L.C.
Reprints and permissions information is available at www.nature.com/reprints.
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations.
Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which
permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give
appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and
indicate if changes were made. The images or other third party material in this article are included in the article’s
Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included
in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or
exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy
of this licence, visit http://creativecommons.org/licenses/by/4.0/.
© The Author(s) 2025
Scientific Reports | (2025) 15:33179 | https://doi.org/10.1038/s41598-025-17935-w 18