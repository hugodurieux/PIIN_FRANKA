Journal of Computational Science 90 (2025) 102633

Contents lists available at ScienceDirect

Journal of Computational Science

journal homepage: www.elsevier.com/locate/jocs

Physics-informed neural networks for compliant robotic manipulators
dynamic modeling

Zhiming Li a,b
a College of Automation, Beijing Information Science and Technology University, Beijing, 100192, China
b Department of Computer Science and Technology, Tsinghua University, Beijing, 100084, China

, Shuangshuang Wu a,b, Wenbai Chen a

,∗, Fuchun Sun b

,∗

A R T I C L E   I N F O

A B S T R A C T

Keywords:
Physics-informed neural networks
Rigid-body dynamics
Compliant robot
Inverse dynamic modeling

Deep learning is widely used in robotics, yet often overlooks key physical principles in dynamic modeling,
leading  to  a  lack  of  interpretability  and  generalization.  To  address  this  issue,  recent  innovations  have
introduced physics-informed neural networks (PINNs), which integrate fundamental physics into deep learning
and offer significant advantages in modeling rigid-body dynamics. This study focuses on the application of
PINNs to model compliant robotic manipulators. This requires extending PINNs to handle complex compliant
dynamics. We propose an augmented PINN model capable of comprehensively learning manipulator dynamics,
including  compliant  components.  The  model  is  tested  on  dynamic  modeling  of  two  physical  compliant
manipulators and a simulated manipulator. The results highlight its exceptional precision and generalization
across a wide range of robotic systems, from purely rigid to compliant structures.

1. Introduction

Accurate  inverse  dynamics,  which  links  joint  motion  to  applied
torque, is essential for model-based control of robotic manipulators [1].
Due  to  joint,  link,  and  actuator  interactions,  these  systems  exhibit
strong nonlinearity and coupling, making modeling challenging [2].
Modern collaborative robots often use compliant manipulators with
elastic actuators to ensure safe interaction by absorbing contact forces
[3]. While this improves safety, the introduced kinematic and elas-
tomechanical coupling further complicates the dynamic modeling pro-
cess [4,5].

Traditional  inverse  dynamics  modeling  for  robotic  manipulators
relies on known physical parameters and manual derivation using New-
tonian, Lagrangian, or Hamiltonian mechanics. Unluckily, obtaining
precise  real  numerical  values  for  the  physical  parameters  is  not  a
straightforward task, and numerous robot manufacturers opt to conceal
this information for logical safety and copyright reasons [6]. Robot
parameters can be obtained by testing individual components, but this
requires  disassembly,  which  is  both  risky  and  time-consuming  and
may alter system behavior [7]. Computer-Aided Design (CAD) models
provide an alternative, but they often neglect factors such as friction,
flexibility, and environmental variations.

Another  approach  to  obtaining  robot  parameters  is  physical  pa-
rameter identification, which uses algorithms such as least squares to
estimate the dynamic parameters of robot joints and construct inverse
dynamics models [8]. This method enhances accuracy by statistically

matching  real  sampled  data  from  the  robot  with  the  mathematical
model formulation [9]. However, due to noise and underlying assump-
tions, this method cannot ensure physically consistent parameters and
may produce unrealistic results, such as negative mass values or inertia
matrices that are not positive definite [10]. To overcome this, Gautier
et al. incorporated these constraints into the identification process using
singular value decomposition and Cholesky factorization, ensuring that
the resulting mass matrix is symmetric and positive definite [11].

Identification-based  modeling  methods  typically  construct  model
structures under rigid body assumptions using classical physical for-
mulations such as Newtonian or Lagrangian mechanics. While effective
for rigid systems, these methods struggle to handle uncertainties and
nonlinearities. Due to the linearization requirements, robot dynamics
and friction models are often simplified into linear systems [12]. Al-
though flexible joint identification is a viable approach for modeling
compliant robots, it faces challenges in accurately capturing parameters
and the nonlinear, time-varying dynamics [13]. Simplified analytical
models often overlook joint stiffness and elasticity or treat them as
linear with uncertain coefficients [14]. Nonlinear effects such as clear-
ance and frictional torque are also frequently ignored [15,16], further
reducing accuracy due to their sensitivity to environmental conditions
and  maintenance.  As  a  result,  for  low-cost  compliant  manipulators
with elastic actuators, traditional identification methods based on rigid
body assumptions struggle to capture their flexible dynamic behavior,

∗ Corresponding authors.

E-mail addresses:  Lizm@bistu.edu.cn (Z. Li), shuangsw@bistu.edu.cn (S. Wu), chenwb@bistu.edu.cn (W. Chen), fcsun@mail.tsinghua.edu.cn (F. Sun).

https://doi.org/10.1016/j.jocs.2025.102633
Received 18 September 2024; Received in revised form 18 May 2025; Accepted 19 May 2025
Available online 5 June 2025
1877-7503/© 2025 Elsevier B.V. All rights are reserved, including those for text and data mining, AI training, and similar technologies.

Z. Li et al.

Fig.  1.  The  diagram  illustrates  the  application  of  physics-informed  and  black-box
models in inverse dynamics modeling.

limiting  their  applicability  [17].  Furthermore,  existing  research  on
robot joint friction rarely models friction concurrently with overall dy-
namics [18]. Data-driven methods are increasingly applied to enhance
the  accuracy  of  inverse  dynamics  models.  Specifically,  Deep  neural
networks excel at learning and capturing complex nonlinear behaviors,
improving precision in inverse dynamics modeling [17]. However, the
black-box  nature  of  these  models  disregards  prior  knowledge  from
first principles, making them susceptible to overfitting without uncov-
ering the underlying structure [19]. This is particularly problematic
for robots, as overfitting to incorrect data can lead to unpredictable
behavior, damaging the physical system and complicating model ap-
plication in controllers [20]. Data-driven methods have been used to
model compliant manipulators [21,22], addressing complexities like
friction and flexibility with experimental data. However, these methods
lack interpretability and theoretical grounding, raising concerns about
generalization and requiring large datasets [23].

Recent research has increasingly focused on integrating physical
information with deep neural network models [24]. Physics-Informed
Neural Networks(PINNs) combines traditional knowledge with deep
networks, utilizing deep learning to uncover hidden structures while
retaining knowledge-based advantages [20]. Lagrangian and Hamilto-
nian mechanics [25] provide system descriptions that can be embedded
into neural networks. In robotics, physics-informed neural networks
like Deep Lagrangian Networks (DeLaN) [26] and Hamiltonian neural
networks (HNN) [27] integrate these mechanics with deep learning, im-
proving physical plausibility, interpretability, and generalization [28].
The differences between DeLaN and black-box models are shown in Fig.
1.

Lagrangian-based methods use neural network models to represent
physical  systems  based  on  the  Euler–Lagrange  equations  of  motion
utilizing generalized coordinates 𝑞, their velocity  ̇𝑞 and a Lagrangian
function (𝑞, ̇𝑞), which represents the difference between kinetic and
potential  energies.  These  energy  terms  are  modeled  by  neural  net-
works, either separately [26,29] or together [30]. Hamiltonian-based
methods use a Hamiltonian formulation to describe system dynam-
ics, utilizing generalized coordinates 𝑞, generalized momenta 𝑝 and
a Hamiltonian function (𝑞, 𝑝) to represent the total energy of the
system. Similarly, the energy terms are modeled by neural networks,
either separately [20,31] or together [27]. The potential of DeLaNs
and HNNs in learning the dynamics of basic physical systems has been
shown in several studies [2,20,23,31–35]. However, their application
to modeling complex robotic structures, particularly with real-world
data, is still in the early stages. DeLaNs and HNNs, based on rigid body
priors, often reduce model accuracy compared to black-box methods, as
they struggle to fully capture phenomena such as friction, hysteresis,
and contact [2,23,33]. While these models are well-suited for rigid
body dynamics, they perform suboptimally when applied to compliant
manipulators with non-rigid dynamics, limiting its application scope.

To address the limitations of PINNs in modeling friction due to
conservative dynamics, most studies focus on incorporating actuator-
induced friction into model learning for robotic manipulators [29,32,
34,36],  achieving  simultaneous  modeling  of  friction  during  overall
dynamics modeling. However, simply including primary friction is in-
sufficient for modeling compliant manipulators. PINNs constrained by

2

Journal of Computational Science 90 (2025) 102633

rigid-body dynamics priors, often fail to capture uncertainties like non-
linear friction and flexibility, limiting their effectiveness for compliant
systems. Our previous work introduced DeLaN-FFNN, an augmented
Deep Lagrangian Network that combines DeLaN with a Feed-Forward
Neural Network (FF-NN) [2]. This method expands DeLaN’s capabil-
ities to handle uncertainties beyond rigid body dynamics, effectively
learning the dynamics of both rigid and compliant manipulators while
preserving interpretability. Considering all the implications above, we
can enumerate the main contributions of this work as follows:

(1) An augmented deep Lagrangian network model with a phys-
ically  plausible  optimization  method  is  proposed  to  account
for  the  complex  nonlinear  characteristics,  enabling  the  accu-
rate construction of the inverse dynamics model for compliant
manipulators.

(2) A comprehensive experiment on compliant manipulators is con-
ducted, including the Baxter Robot and Barrett WAM, show-
ing that DeLaN underperforms compared to black-box models,
while  DeLaN-FFNN  excels  in  accuracy  and  generalization  for
non-rigid-body dynamics.

(3) A simulation rigid-body dynamics experiment is conducted, fur-
ther demonstrating that DeLaNs and HNNs are capable of recov-
ering system dynamics from ideal data, showcasing strong ex-
trapolation ability and data efficiency. DeLaN-FFNN also excels
in rigid-body dynamics modeling.

The  paper  is  organized  as  follows.  Section  2.1  introduces  robot
inverse dynamics, discussing both rigid and non-rigid body dynamics
and their differences. Section 2.2 reviews previous methods for learning
rigid  body  dynamics  using  Lagrangian  and  Hamiltonian  mechanics.
Section 2.3 covers various DeLaN and HNN architectures, followed by
Section 2.4, which describes integrating a friction model into DeLaN.
Section 3 explains the parameterization process for the DeLaN-FFNN
model and the optimization methods used. Lastly, Section 4 presents
experimental  results  comparing  DeLaNs,  HNNs,  black-box  methods,
DeLaN-Friction, and DeLaN-FFNN for both non-rigid and rigid body
dynamics.

2. Preliminaries

This section aims to present the general mathematical formulation
of robot inverse dynamics. Additionally, it offers a concise overview of
the theoretical foundations of Lagrangian and Hamiltonian mechanics,
as well as DeLaNs and HNNs.

2.1. Robot inverse dynamics

The objective of inverse dynamics modeling is to identify the func-

tion 𝑓 −1, which maps system changes to control inputs, i.e.

𝑓 −1(𝑞, ̇𝑞 , ̈𝑞 ) = 𝜏

(1)

where 𝑞,  ̇𝑞, and  ¨q represent the vectors of joint positions, velocities,
and accelerations, respectively. For a robot with 𝑛 degrees of freedom
(dof), these vectors have the dimension 𝑅𝑛. 𝜏 ∈ 𝑅𝑛 represents the
unknown joint torques to be learned. Based on these definitions, the
general inverse dynamics model for a robot is given by

𝐻(𝑞) ̈𝑞 + 𝑐(𝑞, ̇𝑞 ) + 𝑔(𝑞) + 𝜀(𝑞, ̇𝑞 , ̈𝑞 ) = 𝜏

(2)

where 𝐻(𝑞) ∈ 𝑅𝑛×𝑛 is the symmetric, positive definite mass matrix,
𝑐(𝑞, ̇𝑞) ∈ 𝑅𝑛 represents the matrix for centrifugal and Coriolis forces,
𝑔(𝑞) ∈ 𝑅𝑛 denotes the gravity vector, and 𝜀(𝑞, ̇𝑞, ̈𝑞) ∈ 𝑅𝑛 accounts for the
torque/force effects of unmodeled elements, such as viscous friction or
the nonlinear effects of serial elastic actuator (SEA) springs [37].

Various methods can be used to derive an inverse dynamics model
from the equation of motion, neglecting 𝜀(𝑞, ̇𝑞, ̈𝑞). The most common
approaches  for  modeling  robot  dynamics  are  based  on  Lagrangian

Z. Li et al.

Journal of Computational Science 90 (2025) 102633

2.2. Lagrangian and Hamiltonian dynamics

The dynamics of rigid body robots can be described using either
Lagrangian or Hamiltonian mechanics. In Lagrangian mechanics, the
state is represented by generalized coordinates 𝑞 and velocities  ̇𝑞. The
system’s behavior follows the Euler–Lagrange equation:  𝑑
−
𝑑𝑡
𝜕(𝑞, ̇𝑞)
= 𝜏, where (𝑞, ̇𝑞) = 𝑇 (𝑞, ̇𝑞, ) − 𝑉 (𝑞), with potential energy
𝜕𝑞
̇𝑞𝑇 𝐻(𝑞) ̇𝑞.

𝑉 (𝑞) ∈ 𝑅 and kinetic energy 𝑇 = 1
2

In  Hamiltonian  mechanics,  momenta  𝑝 ∈ 𝑅𝑛  replace  velocities,
where  ̇𝑞 = 𝐻 −1(𝑞)𝑝. The system follows Hamiltonian equations:  ̇𝑞 =
𝜕(𝑞,𝑝)
+ 𝜏, with (𝑞, 𝑝) = 𝑇 (𝑞, 𝑝) + 𝑉 (𝑞) representing total
𝜕𝑝

,  ̇𝑝 = − 𝜕(𝑞,𝑝)

( 𝜕(𝑞, ̇𝑞)
𝜕 ̇𝑞

)

𝜕𝑞

energy. Here, kinetic energy is defined as 𝑇 (𝑞, 𝑝) = 1
2

𝑝𝑇 𝐻 −1(𝑞)𝑝.

Substituting the kinetic and potential energy into the Euler–Lagrange
equation for  and into the Hamiltonian equation for  both yield a
second-order ordinary differential equation (ODE) described by [20]:

Fig.  2.  The  inverse  model  with  DeLaNs  predicts  the  system’s  Lagrangian    and
calculates changes via the Euler–Lagrange equations. In (a), the structured approach
uses two networks for kinetic (𝑇 ) and potential (𝑉 ) energies to compute  = 𝑇 − 𝑉 . In
(b), the black-box method directly predicts .

Fig.  3.  HNNs  predict  the  Hamiltonian    and  compute  changes  in  position  and
momentum using Hamilton’s equations. In variant (a), the structured approach employs
two networks for kinetic and potential energies, while (b) is the black-box approach,
directly predicting  with a single network.

and Hamiltonian mechanics, both derived from rigid body dynamics
principles. The robot’s rigid body dynamics (𝜏RBD) can be expressed in
a specific mathematical form.

𝐻(𝑞) ̈𝑞 + 𝑐(𝑞, ̇𝑞) + 𝑔(𝑞) = 𝜏RBD

(3)

As both Lagrangian and Hamiltonian mechanics are based on rigid body
dynamics, they often overlook factors like 𝜀(𝑞, ̇𝑞, ̈𝑞) in robot inverse
dynamics, failing to account for complex nonlinear phenomena such
as friction, hysteresis, contact, and forces arising from flexibility and
uncertainties [38]. Consequently, these methods may produce rough
approximations in inverse dynamics models, resulting in inaccurate
torque predictions and imprecise robot movements [39].

3

𝐻(𝑞) ̈𝑞 + ̇𝐻 (𝑞) ̇𝑞 −

(

1
2

̇𝑞 𝑇 𝜕𝐻(𝑞)
𝜕𝑞

)𝑇

̇𝑞

+

⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟
=𝑐(𝑞, ̇𝑞 )

= 𝜏

𝜕𝑉 (𝑞)
𝜕𝑞
⏟⏟⏟
=𝑔(𝑞)

(4)

This expression can be simplified to yield Eq. (3). The Lagrangian and
Hamiltonian methods are commonly used for inverse dynamics anal-
ysis, enabling the formulation of simplified inverse dynamics models
when uncertain forces 𝜀(𝑞, ̇𝑞 , ̈𝑞 ) are ignored.

2.3. DeLaNs and HNNs

DeLaNs utilize the principle of least action to learn a Lagrangian
function (𝑞, ̇𝑞) from trajectory data, generating dynamics through the
Euler–Lagrange framework [26], as illustrated in Fig.  2. On the other
hand, HNNs are designed to learn the Hamiltonian function (𝑞, 𝑝),
which then produces dynamics via Hamilton’s equations [27], shown
in Fig.  3. The loss functions for both DeLaNs and HNNs are calculated
as the mean squared error (MSE) between the actual torques 𝜏𝑅 and
the predicted torques ̂𝜏.

𝐿𝑜𝑠𝑠 = 𝑀𝑆𝐸(𝜏𝑅, ̂𝜏 )

(5)

Both the Lagrangian  and Hamiltonian  can be parameterized using
two networks: one for the mass matrix (or its inverse) and the other
for potential energy, known as the structured Lagrangian/Hamiltonian
models (Figs.  2(a) and 3(a)). Alternatively, a single network can be
used,  forming  the  black-box  Lagrangian/Hamiltonian  models  (Figs.
2(b) and 3(b)). It is worth noting that in subsequent models, friction or
uncertain forces are introduced, and the model used is the structured
DeLaN.

2.4. Introducing friction to model learning

DeLaN is unable to directly model friction due to its conservative
dynamics. Most studies on DeLaN focus on integrating major friction
components in robotic manipulators [29,32,34,36], with [36] having
applied this to the Baxter Robot’s compliant manipulator. These ap-
proaches assume that motor friction depends only on the velocity of
the 𝑖th joint  ̇𝑞𝑖, independent of other joints. Depending on the model’s
complexity, static, viscous, or Stribeck friction is used as a prior, and
the combined effects are expressed as:

(

̂𝜏𝑓𝑖

= −

𝜏𝐶𝑣

+ 𝜏𝐶𝑠

exp

))

(

̇𝑞2
𝑖
𝑣

−

sign( ̇𝑞𝑖) − 𝑑 ̇𝑞𝑖

(6)

{

Where 𝜏𝐶𝑣  represents static friction, 𝑑 is viscous friction, and 𝜏𝐶𝑠 and
𝑣  are  the  Stribeck  friction  coefficients.  The  friction  coefficients  are
}
abbreviated as 𝜑 =
. The friction force ̂𝜏𝑓𝑖 is incorporated
into the Lagrangian model [29], with 𝜑 learned as network weights.
We name the method that integrates friction into DeLaN learning as
DeLaN-Friction, which is used as the subsequent experimental baseline.

, 𝜏𝐶𝑠

, 𝑣, 𝑑

𝜏𝐶𝑣

Z. Li et al.

Journal of Computational Science 90 (2025) 102633

Fig. 4.  DeLaN-FFNN predicts dynamics by dividing forces into those following rigid body dynamics and those resulting from flexibility, nonlinear friction, and other uncertainties.
In the model, the orange section represents DeLaN, and the blue section denotes the standard deep network. This model incorporates all force components in the robot’s inverse
dynamics.

3. Proposed algorithms

3.1. Compliant robot dynamic

For compliant robotic manipulators, which involve non-rigid body
dynamics  as  shown  in  Eq.  (2),  it  is  crucial  not  only  to  model  the
dynamics of rigid body components Eq. (3), but also to capture the
additional complex dynamics 𝜀(𝑞, ̇𝑞, ̈𝑞) inherent in elastic joints, such as
friction and elasticity. These dynamics are essential for linking applied
torques  to  motion  [5].  As  a  result,  models  like  DeLaN,  which  are
designed for rigid robots, are often inadequate for elastic manipulators.
Thus, elastic robots require more advanced modeling techniques to
address their complex dynamics [40].

However, identifying compliant robot parameters related to 𝜀(𝑞, ̇𝑞, ̈𝑞)
is mathematically challenging [4]. The mathematical intractability mo-
tivates the use of data-driven methods for compliant dynamic model-
ing [17]. As mentioned in Section 2.4, most of the existing improve-
ments based on the DeLaN model focus primarily on incorporating
the main joint friction into the model learning, enabling the improved
DeLaN-Friction to model friction concurrently with overall dynamics.
However, for the complex compliant dynamics 𝜀(𝑞, ̇𝑞, ̈𝑞), friction is only
a part of it. Considering only frictional dynamics outside of rigid body
dynamics still cannot fully capture the complex dynamic phenomena
of compliant robotic manipulators. These factors drive us to design a
more effective physics-informed neural network structure to improve
the modeling performance for compliant robotic manipulators.

Fig. 5.  Diagram of the mass matrix including a feed-forward neural network, a non-
negative shift for diagonal entries, and the Cholesky decomposition.

𝜙), and ̂𝜀(𝑞, ̇𝑞, ̈𝑞; 𝜓), where 𝜃, 𝜙, and 𝜓 represent the respective network
parameters. The orange section depicts the DeLaN structure, while the
blue section represents the FF-NN. FF-NN is a standard neural network,
used to model the uncertainty term 𝜀(𝑞, ̇𝑞, ̈𝑞) as ̂𝜀(𝑞, ̇𝑞, ̈𝑞; 𝜓). Substituting

̂𝜏 = ̂𝑓 −1(𝑞, ̇𝑞 , ̈𝑞 ; 𝜃, 𝜙, 𝜓)

(7)

the approximated robotic manipulator’ inverse model can be described
by

3.2. Introducing uncertainty force to model learning

−1

̂𝑓

(𝑞, ̇𝑞 , ̈𝑞 ; 𝜃, 𝜙, 𝜓) = ̂𝐻 (𝑞; 𝜃) ̈𝑞 +

+ ̂𝜀 (𝑞, ̇𝑞 , ̈𝑞 ; 𝜓)

To overcome the limitations of DeLaN, which only accounts for
rigid-body dynamics 𝜏RBD and lacks the capacity to model forces be-
yond this scope, we incorporate the learning of uncertain forces in-
duced  by  complex  nonlinear  dynamic  phenomena  𝜀(𝑞, ̇𝑞, ̈𝑞)  into  the
model.

3.2.1. Network structure

By combining DeLaN with a standard deep network, our model
incorporates all force components from Eq. (2), including inertial forces
𝐻(𝑞) ̈𝑞, Coriolis and Centrifugal forces 𝑐(𝑞, ̇𝑞), gravitational forces 𝑔(𝑞),
and uncertain forces 𝜀(𝑞, ̇𝑞, ̈𝑞). This augmented deep Lagrangian net-
work, called DeLaN-FFNN, integrates physics-informed and standard
deep networks, providing a structure that better aligns with the dy-
namics of compliant robotic manipulators.

The structure of DeLaN-FFNN is shown in Fig.  4, with three fully
connected networks used to parameterize the parameters  ̂𝐻(𝑞; 𝜃),  ̂𝑉 (𝑞;

4

𝜕 ̂𝑉 (𝑞, 𝜙)
𝜕𝑞
⏟⏞⏞⏟⏞⏞⏟
̂𝑔 (𝑞;𝜙)
(

+ ̂̇𝐻 (𝑞; 𝜃) ̇𝑞 −

1
2

̇𝑞 𝑇 𝜕 ̂𝐻 (𝑞; 𝜃)
𝜕𝑞

⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟
̂𝑐 (𝑞, ̇𝑞 ;𝜃)

)

̇𝑞

(8)

3.2.2. Positive-definite mass matrix

To ensure physically plausible kinetic energy 𝑇 = 1
2

̇𝑞𝑇 𝐻(𝑞) ̇𝑞, the
mass matrix 𝐻(𝑞) must be positive definite, guaranteeing positive ki-
netic energy for all non-zero velocities. This is achieved by applying the
Cholesky decomposition [11], which decomposes a symmetric positive
definite matrix into the product of a lower triangular matrix and its
transpose. Therefore, the predicted mass matrix  ̂𝐻(𝑞; 𝜃) of the physical
system  can  be  expressed  in  the  form  of  a  Cholesky  decomposition
plus a positive regularization offset 𝜀, which guarantees the positive
definiteness of  ̂𝐻(𝑞; 𝜃), i.e.
̂𝐻 (𝑞; 𝜃) = ̂𝐿 (𝑞; 𝜃) ̂𝐿 (𝑞; 𝜃)𝑇 + 𝜀𝐼

(9)

Z. Li et al.

Journal of Computational Science 90 (2025) 102633

4. Experiment

In these experiments, DeLaN-FFNN is used to learn the non-linear
dynamics of both real and simulated systems, compared with baselines
like DeLaNs, HNNs, DeLaN-Friction, and black-box methods. For real
systems, the models are applied to compliant manipulators such as the
Baxter Robot and the Barrett WAM, testing PINNs where rigid-body
priors do not apply. DeLaN-FFNN’s performance is evaluated against
these baselines to address DeLaN’s limitations in non-rigid dynamics.
In simulations, a 3-dof manipulator is used to test the advantages of
PINNs in modeling rigid body dynamics.

4.1. Experiment setup

In the experiments, DeLaNs and HNNs that use a single network
for the Lagrangian or Hamiltonian are termed black-box DeLaN/HNN.
When two networks represent the mass matrix and potential energy,
this  is  called  structured  DeLaN/HNN.  Structured/black-box  DeLaN,
structured/black-box HNN, black-box feedforward network (FF-NN),
DeLaN-Friction, and DeLaN-FFNN are evaluated for inverse dynamics
modeling in different systems. Structured/black-box HNN is assessed
only in simulations, as real systems lack momentum data 𝑝.

In the experiments, mean square error (MSE), normalized mean
square error (nMSE), and the coefficient of determination (𝑅2) are used
to evaluate the accuracy and predictive performance of the models.
These metrics offer a comprehensive evaluation of model performance.
The 𝑅2 is defined as follows:

𝑅2 = 1 −

∑𝑁

𝑖=1 (𝜏𝑖 − ̂𝜏𝑖 )2

∑𝑁

𝑖=1 (𝜏𝑖 −

2
−
𝜏 )

(11)

where,  𝜏𝑖  and  ̂𝜏𝑖  represent  the  actual  and  predicted  torque  values,
−
𝜏 is the dataset’s mean torque value. The 𝑅2 value,
respectively, while
ranging from 0 to 1, measures how well a model explains the variance
in  the  data,  with  higher  values  indicating  better  predictions  and  1
representing perfect accuracydof [23].

4.1.1. Plants

In the experiments, the model learning techniques are applied to the
Baxter Robot, the Barrett WAM, and a simulated three-link manipula-
tor.

Baxter Robot. A collaborative and compliant robot, features two arms,
each with 7-dof, and is equipped with SEAs, is shown in Fig.  6. These
SEAs, unlike rigid actuators, include a spring between the motor gear
and  the  actuator  end,  enabling  them  to  absorb  contact  forces  to  a
degree  and  provide  passive  compliance.  Additionally,  Baxter  has  a
passive  spring  in  its  second  joint,  further  augmenting  the  dynamic
complexity of the robot manipulator [5].

Barrett WAM. A robot with direct cable drives, generates high torques
leading to fast and agile movements but results in complex dynamics.
The variability in stiffness and lengths of the cables makes it chal-
lenging for rigid-body dynamics models to accurately capture these
dynamics [26,41].

Three-link Manipulator. The three-link manipulator, with continuous
revolute joints, operates in the vertical 𝑥–𝑧 plane under gravity, en-
abling it to reach any position within its workspace. Notably, complex
friction effects are absent in its motion. The simulation is conducted
using the Pybullet physics engine.

4.1.2. Neural network training details

In each experiment, the dynamics models are trained on a fixed
dataset until convergence and evaluated on a separate test dataset.
To reduce variability from random seed training, results are averaged
over  5  seeds.  The  neural  networks  are  built  using  JAX,  leveraging

Fig. 6.  Baxter manipulator. Joints S0 and S1 form the shoulder, joints E0 and E1 form
the elbow, and joints W0, W1, and W2 constitute the wrist.

where  ̂𝐿(𝑞; 𝜃) is a lower triangular matrix with positive diagonal ele-
ments, and  ̂𝐿 (𝑞; 𝜃) consists of ̂𝑙𝑑 (𝑞; 𝜃) for predicting diagonal elements
and ̂𝑙0 (𝑞; 𝜃) for predicting other elements. The diagonal elements ̂𝑙𝑑 (𝑞; 𝜃)
are  predicted  using  activation  functions  such  as  Softplus  or  ReLU
to ensure non-negativity, with a small scalar 𝜀𝐼 added to guarantee
positive definiteness, 𝐼 is identity matrix and 𝜀 is a hyperparameter that
should be selected to be small-enough but strictly positive. For further
details, see Fig.  5.

3.2.3. Optimization method

For Eq. (2), most rigid or near-rigid robots, typically equipped with
high-ratio gearboxes, often assume 𝜀(𝑞, ̇𝑞, ̈𝑞) = 0 in dynamic modeling,
as the torque contributions from 𝜏𝑅𝐵𝐷 are much larger than those from
𝜀(𝑞, ̇𝑞, ̈𝑞) [2,5]. If DeLaN-FFNN uses a simple mean square error loss
function as shown in Eq. (5), it may, in some cases, cause the potential
and kinetic energy to be neglected, and result in the uncertain force
network dominating the predicted dynamics. This is clearly inconsistent
with real-world scenarios, which drives us to design a more physically
plausible optimization method that better aligns with actual conditions.
To prevent potential and kinetic energy from being neglected, and
to avoid the uncertain force network dominating the predicted dynam-
ics, additional penalty terms are introduced. This ensures that in rigid
or near-rigid body dynamics, DeLaN’s output torque is maximized while
minimizing  𝜀(𝑞, ̇𝑞, ̈𝑞).  However,  for  compliant  manipulators,  𝜀(𝑞, ̇𝑞, ̈𝑞)
plays a crucial role [5]. Therefore, to make DeLaN-FFNN applicable
to most robotic manipulators, whether a purely rigid manipulator or
a non-rigid manipulator, such as one with a compliant structure, our
optimization objective is defined as follows:
(

(𝜃∗, 𝜙∗, 𝜓 ∗) = arg min

𝜃,𝜙,𝜓

̂𝑓 −1(𝑞, ̇𝑞, ̈𝑞; 𝜃, 𝜙, 𝜓) − 𝜏𝑅
‖
‖
‖

‖
‖
‖

2

+ 𝜆 ̂𝜀(𝑞, ̇𝑞, ̈𝑞; 𝜓)2

)

𝑊𝜏𝑅

(10)

In  this  model,  𝜏𝑅  represents  the  actual  torque  measured  from  the
physical manipulator, which is compared with the network’s output
torque  ̂𝜏  to  compute  the  loss.  To  avoid  inaccuracies  in  the  torque
modeling of the upper joints, caused by significant differences in the
magnitude  of  the  torques  among  different  joints.  The  Mahalanobis
norm ‖·‖𝑊  is used, with 𝑊𝜏𝑅 representing the diagonal covariance
matrix of generalized forces. Normalizing the loss with the covariance
matrix helps account for varying residual magnitudes across different
joints. The value of 𝜆 must be positive to ensure that the rigid-body
dynamics component of DeLaN-FFNN’s output dominates, while the
torque output from the uncertain force network remains secondary.
However, the value of 𝜆 needs to be adjusted based on the compliance
of the robotic manipulator to ensure that DeLaN-FFNN is applicable to
robotic manipulators with varying degrees of non-rigidity.

5

Z. Li et al.

Journal of Computational Science 90 (2025) 102633

Fig. 7.  (a–d) show the inverse dynamics modeling performance for the first four joints of each system on the selected sub-trajectories, with the learned inverse model averaged
over 5 seeds.

Table 1
The hyperparameters used for the dynamics models vary across the different dynamical
systems.

  Total Dof
  Activation
  Network Dimension

Baxter Robot
7
ReLu
[2×128]

Barrett WAM
7
Tanh
[4×300]

3-Dof manipulator
3
Tanh
[2×256]

its automatic differentiation for computing partial derivatives in the
dynamics model.

For all systems, the ADAM optimizer is used with a batch size of
512, a learning rate of 10−4, and a weight decay of 10−5. Hyperparam-
eters for each system’s dynamics models are detailed in Table  1. Here,
in the Network Dimension, for example, [2 × 128] denotes two hidden
layers, with 128 neurons in each layer.

4.2. Non-rigid body dynamics modeling

In non-rigid body dynamics modeling experiments, dynamics mod-
els are applied to the Baxter Robot and Barrett WAM to assess the ef-
fectiveness of PINNs when rigid-body priors are inapplicable. The goal
is to evaluate whether DeLaN-FFNN maintains interpretability while
offering better modeling performance and generalization compared to
other baselines.

4.2.1. Dataset construction

The datasets for the Baxter Robot and Barrett WAM are sourced
from publicly available real system datasets. Detailed descriptions of
these datasets are provided below.

Barrett WAM Dataset. This dataset is specifically designed for tackling
an inverse dynamics problem associated with a 7-dof Barrett WAM
manipulator. The dataset contains 12,000 training samples of seven

Table 2
Classification of trajectories in Baxter Robot training and testing data, and the number
of data samples for each type.

Training trajectories

Test trajectories

Trajectory
Random trajectories
Spiral trajectories
Helical trajectories
Circular trajectory XY
Circular trajectory XZ
Square trajectory
Helical trajectory

Number of samples
5661
28 395
62 220

5651
5659
5663
5661

degrees of freedom 𝑞,  ̇𝑞,  ̈𝑞, and corresponding 𝜏, as well as 3000 test
samples [42]. The dataset can be accessed online at thislink.

Baxter Robot Dataset. This dataset contains the 𝑞,  ̇𝑞, and correspond-
ing 𝜏 of a 7-dof Baxter Robot compliant manipulator. However, this
dataset does not provide acceleration data  ̈𝑞. In real-world systems,
̈𝑞  is  usually  unobserved  and  estimated  via  finite  differences,  which
can amplify high-frequency noise [20,43]. To address this, low-pass
filters  are  applied  for  more  accurate  estimates.  Following  [20,43],
we compute accelerations using finite differences combined with low-
pass filtering. Based on the different trajectories executed by the end
effector, this dataset is categorized. The training set includes random
trajectories, helical trajectories, and spiral trajectories, while the test
set  comprises  a  square  trajectory,  a  helical  trajectory,  and  circular
trajectories on the XY and XZ plane. For more data details, please refer
to Table  2 and the paper [5]. The dataset can be accessed online at
thislink.

4.2.2. Prediction performance evaluation

The Barrett WAM dataset, along with the helical trajectories from
the Baxter Robot training and test sets, is used to assess the accuracy
of non-rigid dynamics modeling for each model. For the Barrett WAM,
there are 12,000 training samples and 3000 test samples, while for the
Baxter Robot, the training set consists of 62,220 samples, and the test
set includes 5661 samples. The modeling results for the Barrett WAM
and Baxter Robot, including detailed results for each of the 7-dof and
the overall modeling accuracy, are presented in Table  3.

For joint modeling accuracy (Table  3), FF-NN and DeLaN-FFNN
achieve the lowest MSEs in both the Barrett WAM and Baxter Robot.
In the Barrett WAM, FF-NN, DeLaN-Friction, and DeLaN-FFNN outper-
form structured/black-box DeLaN, especially in the first four joints,
which are key to its dynamics as they primarily drive the system’s
dynamic behavior. For the coefficient of determination (𝑅2), DeLaN-
FFNN, DeLaN-Friction, and FF-NN perform similarly with values near
1, surpassing structured/black-box DeLaN.

In the Baxter Robot, DeLaN-FFNN and FF-NN also show high 𝑅2,
while DeLaN-Friction performs better than structured/black-box DeLaN
but remains lower. The system’s non-rigid dynamics, with its more
pronounced  elasticity,  make  friction  alone  insufficient.  To  illustrate
the modeling effectiveness, visualizations of the first four joints, which
dominate the dynamics, are provided. In the test set, the first 200 data
samples from the Barrett WAM and 500 from the Baxter Robot are
selected as sub-trajectories for clearer visualization, with the results
displayed in Fig.  7.

The above results indicate that DeLaNs, which incorporate rigid
body dynamics priors, are less effective for non-rigid systems, while
DeLaN-Friction  improves  accuracy  by  compensating  for  torque  out-
put. However, it still underperforms compared to black-box models,

6

Z. Li et al.

Journal of Computational Science 90 (2025) 102633

Table 3
The MSE of each joint in the Barrett WAM and Baxter Robot as well as the corresponding confidence interval averaged over 5 seeds. The coefficient of determination 𝑅2 is
calculated on the entire set for each system.

Structured Lagrangian
Black-Box Lagrangian
Feed-forward Network
Introducing Friction
An Augmented DeLaN

  Barrett WAM # Test samples = 3000
  DeLaN
  DeLaN
  FF-NN
  DeLaN-Friction
  DeLaN-FFNN
  Baxter Robot # Test samples = 5661
  DeLaN
  DeLaN
  FF-NN
  DeLaN-Friction
  DeLaN-FFNN
Note: The bolded part refers to best results.

Structured Lagrangian
Black-Box Lagrangian
Feed-forward Network
Introducing Friction
An Augmented DeLaN

Inverse model (MSE)
Joint 0
1.2e+0 ± 2.7e−2
1.8e+0 ± 8.2e−2
5.3e−3 ± 3.2e−3
1.3e−2 ± 1.1e−3
6.0e−3 ± 2.8e−3
Joint 0
4.5e−1 ± 3.6e−2
3.1e+0 ± 6.7e−1
1.9e−1 ± 2.3e−2
4.2e−1 ± 5.9e−2
1.9e−1 ± 1.2e−2

Joint 1
1.6e+1 ± 1.5e+0
1.7e+1 ± 7.7e−1
9.7e−3 ± 6.3e−3
7.6e−2 ± 9.8e−3
8.3e−2 ± 4.9e−3
Joint 1
9.6e−1 ± 8.8e−2
3.2e+0 ± 2.0e+0
2.5e−1 ± 4.5e−2
8.6e−1 ± 2.2e−1
2.2e−1 ± 2.6e−2

Joint 2
1.3e−1 ± 4.0e−2
1.4e−1 ± 2.2e−2
3.6e−4 ± 7.5e−4
2.8e−3 ± 4.4e−4
4.9e−4 ± 3.1e−4
Joint 2
2.0e−1 ± 3.8e−2
1.3e+0 ± 3.8e−1
1.0e−1 ± 1.9e−2
1.8e−1 ± 2.9e−2
9.8e−2 ± 7.7e−3

Joint 3
2.4e−2 ± 2.2e−3
1.0e−1 ± 5.3e−2
2.9e−4 ± 7.9e−5
1.1e−3 ± 3.7e−4
3.2e−4 ± 3.0e−4
Joint 3
1.0e+0 ± 3.4e−1
2.0e+0 ± 1.5e+0
6.1e−2 ± 4.5e−3
8.7e−1 ± 5.3e−1
6.9e−2 ± 9.8e−3

Joint 4
2.1e−3 ± 2.2e−4
2.6e−3 ± 3.3e−4
3.0e−5 ± 1.4e−5
1.6e−4 ± 6.7e−5
2.9e−5 ± 2.1e−5
Joint 4
1.6e−2 ± 1.4e−3
2.3e−2 ± 3.8e−3
6.3e−3 ± 8.0e−4
1.6e−2 ± 1.8e−3
6.1e−3 ± 5.3e−4

Joint 5
6.7e−4 ± 3.4e−4
5.4e−4 ± 2.1e−4
2.5e−5 ± 6.6e−6
1.0e−4 ± 3.1e−5
2.9e−5 ± 2.5e−5
Joint 5
2.1e−2 ± 3.4e−3
2.6e−2 ± 4.0e−3
8.8e−3 ± 1.3e−3
2.1e−2 ± 1.4e−3
8.0e−3 ± 1.2e−3

Joint 6
2.8e−4 ± 6.4e−4
7.7e−5 ± 1.9e−5
1.2e−6 ± 1.5e−5
4.1e−5 ± 2.9e−5
1.6e−5 ± 1.5e−5
Joint 6
1.2e−2 ± 4.0e−3
1.4e−3 ± 5.7e−4
4.3e−4 ± 2.1e−5
1.2e−2 ± 1.6e−3
5.0e−4 ± 3.3e−5

𝑅2
0.943 ± 5.09e−3
0.939 ± 2.83e−3
0.999 ± 2.15e−5
0.999 ± 3.69e−5
0.999 ± 2.19e−5
𝑅2
0.990 ± 1.65e−3
0.964 ± 1.35e−2
0.998 ± 3.12e−4
0.991 ± 1.95e−3
0.998 ± 1.59e−4

Table 4
The MSE of each joint in the Baxter Robot across three test trajectories, as well as the corresponding confidence interval averaged over 5 seeds. The coefficient of determination
𝑅2 is calculated on the entire set for each system.

  Circular Trajectory XY #Samples = 5651
Structured Lagrangian
  DeLaN
Black-Box Lagrangian
  DeLaN
Feed-forward Network
  FF-NN
Introducing Friction
  DeLaN-Friction
  DeLaN-FFNN
An Augmented DeLaN
  Circular Trajectory XZ #Samples = 5659
Structured Lagrangian
  DeLaN
Black-Box Lagrangian
  DeLaN
Feed-forward Network
  FF-NN
Introducing Friction
  DeLaN-Friction
An Augmented DeLaN
  DeLaN-FFNN
  Square Trajectory #Samples = 5663
  DeLaN
  DeLaN
  FF-NN
  DeLaN-Friction
  DeLaN-FFNN
Note: The bolded part refers to best results.

Structured Lagrangian
Black-Box Lagrangian
Feed-forward Network
Introducing Friction
An Augmented DeLaN

Inverse Model (MSE)
Joint 0
4.4e−1 ± 9.7e−2
4.2e+0 ± 3.1e+0
2.0e−1 ± 2.9e−2
3.6e−1 ± 2.9e−2
2.0e−1 ± 3.9e−2
Joint 0
3.7e−1 ± 3.9e−2
4.7e+0 ± 5.7e−1
8.8e−1 ± 1.6e−1
2.7e−1 ± 3.6e−2
5.8e−1 ± 1.5e−1
Joint 0
7.2e−1 ± 1.3e−1
1.3e+1 ± 3.3e+0
8.8e−1 ± 5.5e−1
5.4e−1 ± 7.5e−2
6.7e−1 ± 5.1e−1

Joint 1
1.1e+0 ± 5.0e−1
2.0e+0 ± 2.3e+0
3.9e−1 ± 1.6e−1
8.0e−1 ± 1.6e−1
3.3e−1 ± 3.2e−2
Joint 1
1.3e+0 ± 1.8e−1
3.8e+0 ± 6.4e−1
2.8e−1 ± 6.9e−2
9.5e−1 ± 6.8e−1
2.7e−1 ± 1.3e−1
Joint 1
2.1e+0 ± 6.1e−1
4.3e+0 ± 3.7e+0
1.2e+0 ± 4.9e−1
1.0e+0 ± 3.9e−1
8.3e−1 ± 1.8e−1

Joint 2
2.9e−1 ± 4.9e−2
2.3e+0 ± 8.6e−1
1.4e−1 ± 5.7e−2
2.0e−1 ± 1.5e−2
1.5e−1 ± 4.2e−2
Joint 2
2.1e−1 ± 7.0e−2
1.0e+0 ± 4.0e−1
4.8e−1 ± 1.3e−1
1.5e−1 ± 2.9e−2
2.9e−1 ± 7.5e−2
Joint 2
3.7e−1 ± 2.4e−1
4.3e+0 ± 9.8e−1
6.6e−1 ± 4.0e−1
3.8e−1 ± 1.2e−1
6.2e−1 ± 2.4e−1

Joint 3
1.3e+0 ± 6.0e−1
1.9e+0 ± 1.5e+0
3.9e−2 ± 5.8e−3
1.4e+0 ± 1.7e+0
4.0e−2 ± 8.9e−3
Joint 3
1.0e+0 ± 5.3e−1
1.6e+0 ± 7.8e−1
6.9e−2 ± 4.9e−2
9.9e−1 ± 7.9e−1
7.6e−2 ± 3.5e−2
Joint 3
1.6e+0 ± 6.9e−1
2.0e+0 ± 1.6e+0
1.6e−1 ± 6.0e−2
1.6e+0 ± 6.5e−1
1.7e−1 ± 8.7e−2

Joint 4
1.7e−2 ± 7.8e−4
1.0e−2 ± 1.4e−3
5.2e−3 ± 1.1e−3
1.6e−2 ± 7.2e−4
5.7e−3 ± 9.0e−4
Joint 4
1.2e−2 ± 2.2e−3
1.4e−2 ± 2.0e−3
1.5e−2 ± 3.3e−3
1.3e−2 ± 2.7e−3
1.2e−2 ± 7.3e−3
Joint 4
5.5e−2 ± 2.4e−2
2.3e−2 ± 6.1e−3
3.3e−2 ± 1.2e−2
4.5e−2 ± 2.6e−2
2.3e−2 ± 5.0e−3

Joint 5
1.5e−2 ± 3.9e−3
1.6e−2 ± 4.6e−3
5.3e−3 ± 3.8e−4
1.2e−2 ± 2.3e−3
5.2e−3 ± 1.2e−3
Joint 5
1.7e−2 ± 8.6e−3
1.1e−2 ± 2.6e−3
9.0e−3 ± 2.9e−3
1.8e−2 ± 6.1e−3
8.6e−3 ± 3.4e−3
Joint 5
7.2e−2 ± 1.5e−2
7.7e−2 ± 1.1e−1
4.2e−2 ± 1.1e−2
7.3e−2 ± 1.4e−2
4.7e−2 ± 1.7e−2

Joint 6
8.4e−3 ± 2.5e−3
3.0e−3 ± 2.0e−3
6.0e−4 ± 1.2e−4
8.3e−3 ± 6.1e−3
7.4e−4 ± 1.8e−4
Joint 6
1.4e−2 ± 5.8e−3
1.0e−2 ± 7.8e−3
2.1e−3 ± 5.5e−4
1.2e−2 ± 4.4e−3
2.2e−3 ± 9.9e−4
Joint 6
3.6e−2 ± 1.4e−2
9.7e−3 ± 7.0e−3
2.5e−3 ± 9.5e−4
2.2e−2 ± 4.0e−3
2.2e−3 ± 1.5e−3

𝑅2
0.953 ± 2.37e−2
0.986 ± 4.97e−3
0.996 ± 7.05e−4
0.987 ± 7.52e−3
0.997 ± 4.19e−4
𝑅2
0.988 ± 2.38e−3
0.955 ± 5.63e−3
0.993 ± 1.48e−3
0.990 ± 6.00e−3
0.995 ± 4.68e−4
𝑅2
0.972 ± 7.38e−3
0.864 ± 3.24e−2
0.983 ± 4.76e−3
0.979 ± 4.93e−3
0.986 ± 3.77e−3

highlighting that adding friction alone is insufficient. DeLaN-FFNN, by
learning non-linear dynamics, including non-rigid elements, maintains
interpretability while achieving superior accuracy.

accuracy for compliant manipulators and better generalization for un-
known trajectories. To illustrate this, Fig.  8 visualizes the first 500 data
samples from the first four joints across the three test trajectories.

4.2.3. Generalization experiment

To assess the generalization capabilities of each dynamics model, all
training trajectories of the Baxter Robot, including random, spiral, and
helical trajectories, totaling 96,276 data samples, are used for model
training. The models are then tested on circular trajectory XY, circular
trajectory XZ, and square trajectory test sets, none of which appeared
in the training data. A generalizable inverse dynamics model should
accurately predict torque values for any trajectory, regardless of the
training trajectory used [5].

The modeling results, including joint-specific and overall accuracy,
are shown in Table  4. For the 𝑅2 metric across the three test trajecto-
ries, the black-box DeLaN performs the worst with the lowest 𝑅2 values.
Although the structured DeLaN shows some improvement, it still un-
derperforms compared to FF-NN, DeLaN-Friction, and DeLaN-FFNN.
This indicates that DeLaNs have lower accuracy and generalization for
compliant manipulators than black-box models. DeLaN-Friction also
lags  behind  FF-NN,  suggesting  that  friction  alone  is  not  enough  to
improve accuracy. DeLaN-FFNN, with 𝑅2 scores near 1 across all tra-
jectories, outperforms all other models, showing superior accuracy and
generalization for compliant manipulators without rigid-body dynamics
constraints.

Table   4  analyzes  the  modeling  accuracy  for  each  joint.  For  the
circular XY trajectory test data, DeLaN-FFNN and FF-NN consistently
show the highest accuracy, emphasizing their advantage of not being
restricted by rigid-body dynamics priors. For the circular XZ and square
trajectories, DeLaN-FFNN performs best for most joints, with a few
exceptions in other models. This demonstrates DeLaN-FFNN’s superior

4.2.4. Summary and discussion

Synthesizing the experimental results, we conclude that PINNs con-
strained  by  rigid-body  dynamics  are  insufficient  for  compliant  ma-
nipulators, showing limited accuracy and poor generalization. Adding
friction to DeLaN improves accuracy but still falls short of ideal inverse
dynamics modeling and generalization, especially compared to black-
box methods that are not constrained by any assumptions. In contrast,
DeLaN-FFNN maintains physical interpretability while achieving supe-
rior modeling accuracy for the Barrett WAM and Baxter Robot, with
better generalization for unknown trajectories. These findings show
that DeLaN-FFNN overcomes the limitations of rigid-body dynamics,
making it suitable for a wider range of physical systems.

Flexible multibody dynamics involves strong nonlinear coupling, es-
pecially under finite rotations [44]. This complexity intensifies in com-
pliant mechanisms with large deformations or complex serial-parallel
structures, where the main challenges lie in modeling coupled nonlin-
ear behaviors, managing topological redundancy, and balancing accu-
racy with generality [45].

The Baxter Robot used in this study is a compliant manipulator
equipped with SEAs and passive springs, offering limited passive com-
pliance. However, it is not a flexure-based mechanism and exhibits only
small joint-level deformations, forming a simple serial structure without
the  topological  complexity  of  parallel  or  hybrid  configurations  [5].
Thus,  experiments  on  this  platform  are  insufficient  to  validate  the
effectiveness of DeLaN-FFNN for highly deformable compliant systems,
which require further investigation.

DeLaN-FFNN introduces an uncertainty force term to extend the
original DeLaN model beyond rigid-body assumptions, enabling it to

7

Z. Li et al.

Journal of Computational Science 90 (2025) 102633

Fig. 8.  (a–d) show the inverse dynamics modeling performance for the first four joints of each test trajectory (circular trajectory XY, circular trajectory XZ and square trajectory)
on the selected sub-trajectories, with the learned inverse model averaged over 5 seeds.

capture certain compliant behaviors. However, since DeLaN was origi-
nally designed for rigid serial manipulators, the current framework re-
mains limited in handling compliant mechanisms with complex serial-
parallel topologies. Future work should focus on adapting its architec-
ture to better model such systems.

4.3. Rigid body dynamics modeling

For  the  rigid  body  dynamics  experiments,  our  goal  is  to  assess
whether the PINNs can learn and recover the underlying system dy-
namics with ideal observations.

4.3.1. Dataset construction

To ensure smooth velocity and direction changes without abrupt
reactions in the robotic manipulator, we base trajectory planning on
sinusoidal functions. This allows for a gradual transition from the initial
angle (𝑞0) to the final angle (𝑞𝑓 ), minimizing sudden accelerations or
decelerations at the start and end. The trajectory for the 𝑖th joint is
defined as follows:
𝑓 − 𝑞𝑖
𝑞𝑖
𝑇

( 2𝜋
𝑇

𝑡 = 𝑞𝑖
𝑞𝑖

))
𝑡

(12)

0 +

𝑇
2𝜋

𝑡 −

sin

(

0

collected, each containing 400 data points, resulting in 80,000 data sets
for training. These include joint positions 𝑞, velocities  ̇𝑞, accelerations ̈𝑞,
momenta 𝑝, their derivatives  ̇𝑝, and joint torques 𝜏, uniformly covering
the state domain. Inverse dynamics is calculated using the Newton-
Euler method in Pybullet. Three additional trajectories are collected for
testing, as shown in Fig.  9(a).

4.3.2. Prediction performance evaluation

The results of the rigid body inverse model experiments are summa-
rized in Table  5 and shown in Fig.  10. All models effectively learned an
inverse model that fits the test set. On average, PINNs achieved lower
MSE than FF-NN. Structured Lagrangian/Hamiltonian methods showed
better  accuracy  than  their  corresponding  black-box  models.  DeLaN-
FFNN and DeLaN-Friction performed similarly to structured DeLaN,
outperforming other models. Notably, DeLaN-Friction and DeLaN-FFNN
performed well even with data containing only conservative forces.
This is because DeLaN-Friction trains friction coefficients as network
weights, while DeLaN-FFNN reduces the output of the uncertainty force
network when there are no uncertainties to learn.

4.3.3. Torque decomposition experiment

In  this  setup,  𝑇   is  the  total  movement  time,  and  𝑡  represents  the
current time. Within the robot’s joint angle limits, 200 random sets
of initial and final angles for three joints are generated. With an 8-
second sampling period and a frequency of 50 Hz, 200 trajectories are

In the decomposition of torque into inertial, centrifugal, Coriolis,
and gravitational forces, all models performed well. As seen in Table
5, PINNs consistently outperformed FF-NN in terms of nMSE across all
torque components. For inertial and Coriolis torques, only structured

Fig. 9.  (a) Depicts the three test trajectories of the simulated 3-dof robotic manipulator operating in the 𝑥–𝑧 plane. (b) Shows each dynamics model perform when applied to
increased velocities, assessing their capability to extrapolate to new velocity conditions(the gray areas represent the test data where velocities are increased) and (c) presents the
assessment of inverse dynamics modeling accuracy for each dynamics model as the number of training trajectories increases from 10 to 200, with each trajectory containing 400
data samples.

8

Z. Li et al.
Table 5
The normalized mean squared error for dynamics modeling, as well as the corresponding confidence interval averaged over 5 seeds.

Journal of Computational Science 90 (2025) 102633

  3-Dof Manipulator # Test Samples = 1200
Structured Lagrangian
  DeLaN
Black-Box Lagrangian
  DeLaN
Structured Hamiltonian
  HNN
Black-Box Hamiltonian
  HNN
Feed-Forward Network
  FF-NN
Introducing Friction
  DeLaN-Friction
  DeLaN-FFNN
An Augmented DeLaN
Note: The bolded part refers to better results.

Inverse Model (nMSE)
Torque 𝜏
4.35e−7 ± 1.44e−7
3.91e−3 ± 6.04e−4
1.59e−6 ± 1.94e−7
1.99e−3 ± 1.27e−3
5.46e−3 ± 2.21e−3
9.42e−7 ± 1.29e−6
7.42e−7 ± 3.63e−7

Inertial Torque 𝜏𝐼
1.97e−6 ± 1.75e−6
2.55e−3 ± 1.83e−3
1.92e−4 ± 1.07e−4
6.80e−1 ± 2.20e−1
1.30e−1 ± 3.15e−2
5.16e−6 ± 8.66e−6
6.14e−6 ± 1.65e−6

Coriolis Torque 𝜏𝑐
1.04e−5 ± 2.89e−6
1.38e−1 ± 2.22e−2
3.58e−4 ± 9.91e−5
8.96e−1 ± 1.25e−1
1.82e−1 ± 7.95e−2
2.40e−5 ± 2.88e−5
2.10e−5 ± 1.14e−5

Gravitational Torque 𝜏𝑔
2.06e−7 ± 9.29e−8
9.99e−6 ± 7.30e−6
6.34e−7 ± 2.28e−7
1.01e−4 ± 3.01e−5
1.75e−4 ± 1.25e−4
2.90e−7 ± 3.62e−7
2.29e−7 ± 6.00e−8

DeLaN, DeLaN-Friction, and DeLaN-FFNN showed superior results be-
cause they learned the true and reasonable mass matrix of the system
during training. In modeling gravitational force, all models except FF-
NN and black-box HNN demonstrated higher accuracy. Structured La-
grangian/Hamiltonian methods were notably more effective than their
black-box counterparts, especially for inertial and Coriolis torques.

4.3.4. Velocity extrapolation and data efficiency experiments

In  addition  to  inverse  dynamics  modeling  and  force  decomposi-
tion, we evaluate the models’ ability to extrapolate to new velocity
conditions (Fig.  9(b)) and their performance as training data volume
increased (Fig.  9(c)). Initially trained at a velocity scale of 1×, the
models were tested at higher velocities. At 2.5×, FF-NN and black-
box DeLaN/HNN were no longer viable, while structured DeLaN/HNN,
DeLaN-Friction, and DeLaN-FFNN still maintained accuracy, even out-
performing the black-box models at 1×. Structured DeLaN had the best
velocity extrapolation, as its input domain includes only 𝑞, making
it unaffected by velocity changes. Models like FF-NN, black-box De-
LaN, and HNNs, which depend on (𝑞, ̇𝑞, ̈𝑞), (𝑞, ̇𝑞), or (𝑞, 𝑝), were more
affected. DeLaN-FFNN and DeLaN-Friction showed similar extrapola-
tion to structured DeLaN. Fig.  9(c) highlights structured DeLaN/HNN,
DeLaN-Friction, and DeLaN-FFNN achieving lower test MSEs than FF-
NN and black-box DeLaN/HNN, with the gap widening as the training
set grows, demonstrating their better data efficiency.

4.3.5. Summary

In summary, the rigid body dynamics experiments demonstrate that
PINNs effectively capture the underlying structure of the dynamical

system. In inverse dynamics modeling, torque decomposition, velocity
extrapolation, and data efficiency, structured DeLaN/HNN outperform
their black-box counterparts and FF-NN. Across all rigid body dynamics
modeling tests, structured DeLaN achieves the best results, followed
closely by DeLaN-FFNN and DeLaN-Friction. DeLaN-FFNN’s results are
very similar to those of structured DeLaN, partly due to the optimiza-
tion objective in Eq. (10), which emphasizes the role of structured
DeLaN when the dynamics being learned consist solely of rigid-body
dynamics.

5. Conclusion

This  paper  introduces  PINNs  like  DeLaNs  and  HNNs,  which  in-
corporate  rigid-body  dynamics  priors  to  effectively  learn  the  struc-
ture  of  simulated  rigid-body  systems.  However,  they  struggle  with
non-rigid  systems  like  compliant  manipulators.  To  address  this,  an
augmented deep Lagrangian network (DeLaN-FFNN) is proposed, com-
bining physics-informed and standard deep networks to model both
rigid  and  non-rigid  dynamics.  Experiments  with  compliant  manipu-
lators,  including  the  Baxter  Robot,  Barrett  WAM,  and  a  rigid-body
simulated  robot,  show  that  DeLaN-FFNN  matches  the  performance
of PINNs for rigid systems while excelling in compliant systems. It
provides precise modeling, improved generalization, and retained in-
terpretability across a range of manipulators. However, its effectiveness
in highly deformable compliant systems still requires further validation,
and it remains limited in handling compliant mechanisms with complex
serial-parallel structures. Future work should focus on adapting and ex-
tending the network architecture to make it more suitable for modeling
such systems.

Fig. 10.  (a) Displays the learned inverse model using the training dataset, with three test trajectories not included in the training set and results averaged over 5 seeds. The
subsequent columns provide the predicted force decomposition. (b) Illustrates the inertial force 𝐻(𝑞) ̈𝑞, (c) shows the Coriolis and Centrifugal forces 𝑐(𝑞, ̇𝑞), and (d) depicts the
gravitational force 𝑔(𝑞).

9

Z. Li et al.

CRediT authorship contribution statement

Zhiming Li: Writing – original draft, Visualization, Software, Method-
ology, Investigation, Formal analysis, Data curation, Conceptualization.
Shuangshuang Wu: Writing – review & editing, Validation, Supervi-
sion, Software, Methodology, Conceptualization. Wenbai Chen: Writ-
ing  –  review  &  editing,  Supervision,  Resources,  Project  administra-
tion, Funding acquisition. Fuchun Sun: Writing – review & editing,
Supervision, Project administration, Investigation, Funding acquisition.

Declaration of competing interest

The  authors  declare  that  they  have  no  known  competing  finan-
cial interests or personal relationships that could have appeared to
influence the work reported in this paper.

Funding

This research was funded by the National Key Research and Devel-
opment Program of China (No. 2021ZD0114505), the National Natural
Science Foundation of China (62276028), the Major Research Plan of
the  National  Natural  Science  Foundation  of  China  (92267110),  the
Beijing Municipal Natural Science Foundation–Xiaomi Innovation Joint
Fund (L233006), the Qin Xin Talents Cultivation Program at Beijing
Information Science & Technology University (QXTCP A202102), and
the  Beijing  Information  Science  and  Technology  University  School
Research Fund (No. 2023XJJ12).

Data availability

Data will be made available on request.

References

[1] A.  Dalla  Libera,  R.  Carli,  A  data-efficient  geometrically  inspired  polynomial
kernel for robot inverse dynamic, IEEE Robot. Autom. Lett. 5 (1) (2019) 24–31.
[2] S. Wu, Z. Li, W. Chen, F. Sun, Dynamic modeling of robotic manipulator via
an augmented deep Lagrangian network, Tsinghua Sci. Technol. 29 (5) (2024)
1604–1614.

[3] M. Giuliani, C. Lenz, T. Müller, M. Rickert, A. Knoll, Design principles for safety

in human-robot interaction, Int. J. Soc. Robot. 2 (2010) 253–274.

[4] C.  Lee,  S.  Kwak,  J.  Kwak,  S.  Oh,  Generalization  of  series  elastic  actuator
configurations and dynamic behavior comparison, in: Actuators, vol. 6, (3) MDPI,
2017, p. 26.

[5] B. Valencia-Vidal, E. Ros, I. Abadía, N.R. Luque, Bidirectional recurrent learning
of inverse dynamic models for robots with elastic joints: a real-time real-world
implementation, Front. Neurorobotics 17 (2023) 1166911.

[6] W. Deng, F. Ardiani, K.T. Nguyen, M. Benoussaad, K. Medjaher, Physics informed
machine learning model for inverse dynamics in robotic manipulators, Appl. Soft
Comput. 163 (2024) 111877.

[7] B. Armstrong, O. Khatib, J. Burdick, The explicit dynamic model and inertial
parameters of the PUMA 560 arm, in: Proceedings. 1986 IEEE International
Conference on Robotics and Automation, vol. 3, IEEE, 1986, pp. 510–518.
[8] J. Zhang, F. Zhang, M. Cheng, R. Ding, B. Xu, H. Zong, Parameter identification
of hydraulic manipulators considering physical feasibility and control stability,
IEEE Trans. Ind. Electron. 71 (1) (2023) 718–728.

[9] A.K. Tangirala, Principles of System Identification: Theory and Practice, CRC

Press, 2018.

[10] J.-A. Ting, M.N. Mistry, J. Peters, S. Schaal, J. Nakanishi, A Bayesian approach to
nonlinear parameter identification for rigid body dynamics, in: Robotics: Science
and Systems, Citeseer, 2006, pp. 32–39.

[11] M. Gautier, G. Venture, Identification of standard dynamic parameters of robots
with positive definite inertia matrix, in: 2013 IEEE/RSJ International Conference
on Intelligent Robots and Systems, IEEE, 2013, pp. 5815–5820.

[12] J.  Swevers,  W.  Verdonck,  J.  De  Schutter,  Dynamic  model  identification  for

industrial robots, IEEE Control Syst. Mag. 27 (5) (2007) 58–71.

[13] G.A.  Pratt,  M.M.  Williamson,  Series  elastic  actuators,  in:  Proceedings  1995
IEEE/RSJ International Conference on Intelligent Robots and Systems. Human
Robot Interaction and Cooperative Robots, vol. 1, IEEE, 1995, pp. 399–406.
[14] C.  Lee,  S.  Kwak,  J.  Kwak,  S.  Oh,  Generalization  of  series  elastic  actuator
configurations and dynamic behavior comparison, in: Actuators, vol. 6, (3) MDPI,
2017, p. 26.

Journal of Computational Science 90 (2025) 102633

[15] E.  Madsen,  O.S.  Rosenlund,  D.  Brandt,  X.  Zhang,  Comprehensive  modeling
and identification of nonlinear joint dynamics for collaborative industrial robot
manipulators, Control Eng. Pract. 101 (2020) 104462.

[16] A. Calanca, L.M. Capisani, A. Ferrara, L. Magnani, MIMO closed loop identifi-
cation of an industrial robot, IEEE Trans. Control Syst. Technol. 19 (5) (2010)
1214–1224.

[17] A.S. Polydoros, L. Nalpantidis, V. Krüger, Real-time deep learning of robotic
manipulator inverse dynamics, in: 2015 IEEE/RSJ International Conference on
Intelligent Robots and Systems, IROS, IEEE, 2015, pp. 3442–3448.

[18] M. Ruderman, M. Iwasaki, Sensorless torsion control of elastic-joint robots with
hysteresis and friction, IEEE Trans. Ind. Electron. 63 (3) (2015) 1889–1899.
[19] K. Laddach, R. Łangowski, T.A. Rutkowski, B. Puchalski, An automatic selec-
tion of optimal recurrent neural network architecture for processes dynamics
modelling purposes, Appl. Soft Comput. 116 (2022) 108375.

[20] M.  Lutter,  J.  Peters,  Combining  physics  and  deep  learning  to  learn
continuous-time dynamics models, Int. J. Robot. Res. 42 (3) (2023) 83–107.
[21] A.S. Polydoros, E. Boukas, L. Nalpantidis, Online multi-target learning of inverse
dynamics models for computed-torque control of compliant manipulators, in:
2017  IEEE/RSJ  International  Conference  on  Intelligent  Robots  and  Systems,
IROS, IEEE, 2017, pp. 4716–4722.

[22] A. Carron, E. Arcari, M. Wermelinger, L. Hewing, M. Hutter, M.N. Zeilinger,
Data-driven model predictive control for trajectory tracking with a robotic arm,
IEEE Robot. Autom. Lett. 4 (4) (2019) 3758–3765.

[23] Z. Li, S. Wu, W. Chen, F. Sun, Extrapolation of physics-inspired deep networks

in learning robot inverse dynamics, Mathematics 12 (16) (2024) 2527.

[24] B.Z. Cunha, C. Droz, A.-M. Zine, S. Foulard, M. Ichchou, A review of machine
learning methods applied to structural dynamics and vibroacoustic, Mech. Syst.
Signal Process. 200 (2023) 110535.

[25] S.J.  Malham,  An  Introduction  to  Lagrangian  and  Hamiltonian  Mechanics,
Maxwell  Institute  for  Mathematical  Sciences  &  School  of  Mathematical  and
Computer Sciences Heriot-Watt University, Edinburgh EH14 4AS, UK, 2014.
[26] M. Lutter, C. Ritter, J. Peters, Deep lagrangian networks: Using physics as model
prior for deep learning, in: International Conference on Learning Representations,
2019.

[27] S. Greydanus, M. Dzamba, J. Yosinski, Hamiltonian neural networks, Adv. Neural

Inf. Process. Syst. 32 (2019).

[28] W.  Zhai,  D.  Tao,  Y.  Bao,  Parameter  estimation  and  modeling  of  nonlinear
dynamical  systems  based  on  Runge–Kutta  physics-informed  neural  network,
Nonlinear Dynam. 111 (22) (2023) 21117–21130.

[29] M.  Lutter,  K.  Listmann,  J.  Peters,  Deep  lagrangian  networks  for  end-to-end
learning of energy-based control for under-actuated systems, in: 2019 IEEE/RSJ
International Conference on Intelligent Robots and Systems, IROS, IEEE, 2019,
pp. 7718–7725.

[30] M. Cranmer, S. Greydanus, S. Hoyer, P. Battaglia, D. Spergel, S. Ho, Lagrangian

neural networks, 2020, arXiv preprint arXiv:2003.04630.

[31] T. Duong, A. Altawaitan, J. Stanley, N. Atanasov, Port-Hamiltonian neural ODE
networks on Lie groups for robot dynamics learning and control, IEEE Trans.
Robot. (2024).

[32] H. Hu, Z. Shen, C. Zhuang, A PINN-based friction-inclusive dynamics modeling

method for industrial robots, IEEE Trans. Ind. Electron. (2024).

[33] J. Liu, P. Borja, C. Della Santina, Physics-informed neural networks to model and
control robots: A theoretical and experimental investigation, Adv. Intell. Syst. 6
(5) (2024) 2300385.

[34] M. Lahoud, G. Marchello, M. D’Imperio, A. Müller, F. Cannella, A deep learning
framework for non-symmetrical Coulomb friction identification of robotic ma-
nipulators, in: 2024 IEEE International Conference on Robotics and Automation,
ICRA, IEEE, 2024, pp. 10510–10516.

[35] C. Feng, J. Wang, Y. Shen, Q. Wang, Y. Xiong, X. Zhang, J. Fan, Physics-informed
neutral network with physically consistent and residual learning for excavator
precision operation control, Appl. Soft Comput. 167 (2024) 112402.

[36] X. Li, W. Shang, S. Cong, Offline reinforcement learning of robotic control using
deep kinematics and dynamics, IEEE/ASME Trans. Mechatronics (2023).
[37] D. Nguyen-Tuong, J. Peters, Using model knowledge for learning inverse dynam-
ics, in: 2010 IEEE International Conference on Robotics and Automation, IEEE,
2010, pp. 2677–2682.

[38] M. Lutter, J. Silberbauer, J. Watson, J. Peters, A differentiable newton euler
algorithm for multi-body model learning, 2020, arXiv preprint arXiv:2010.09802.
[39] K. Hitzler, F. Meier, S. Schaal, T. Asfour, Learning and adaptation of inverse dy-
namics models: A comparison, in: 2019 IEEE-RAS 19th International Conference
on Humanoid Robots, Humanoids, IEEE, 2019, pp. 491–498.

[40] E.  Madsen,  O.S.  Rosenlund,  D.  Brandt,  X.  Zhang,  Comprehensive  modeling
and identification of nonlinear joint dynamics for collaborative industrial robot
manipulators, Control Eng. Pract. 101 (2020) 104462.

[41] V.  Shaj,  P.  Becker,  D.  Büchler,  H.  Pandya,  N.  van  Duijkeren,  C.J.  Taylor,
M. Hanheide, G. Neumann, Action-conditional recurrent kalman networks for
forward and inverse dynamics learning, in: Conference on Robot Learning, PMLR,
2021, pp. 765–781.

[42] D.  Nguyen-Tuong,  M.  Seeger,  J.  Peters,  Model  learning  with  local  gaussian

process regression, Adv. Robot. 23 (15) (2009) 2015–2034.

[43] M. Reuss, N. van Duijkeren, R. Krug, P. Becker, V. Shaj, G. Neumann, End-to-end
learning of hybrid inverse dynamics models for precise and compliant impedance
control, 2022, arXiv preprint arXiv:2205.13804.

10

Journal of Computational Science 90 (2025) 102633

Wenbai Chen received the B.S. degree from Northeastern
University at Qinhuangdao in 2007, the M.S. degree from
Yanshan University in 2004, and the Ph.D. degree from the
Beijing University of Posts and Telecommunications in 2011.
He is currently a Professor with the school of automation,
Beijing Information Science and Technology University. His
current research interests include intelligent robot, artificial
intelligence, sensor fusion, machine learning and wireless
sensor network. He is the director of Chinese Association
for Artificial Intelligence.

Fuchun  Sun  received  the  Ph.D.  degree  from  Tsinghua
University, Beijing, China, in 1998. From 1998 to 2000,
he  was  a  Post-Doctoral  Fellow  with  the  Department  of
Automation, Tsinghua University, where he is currently a
Professor with the Department of Computer Science and
Technology. His current research interest includes robotic
perception and cognition. Mr. Sun was a recipient of the
National Science Fund for Distinguished Young Scholars. He
serves as the Editor-in-Chief for Cognitive Computation and
Systems and an Associate Editor for a series of international
journals, including the IEEE TRANSACTIONS ON SYSTEMS,
MAN, AND CYBERNETICS: SYSTEMS, the IEEE TRANSAC-
TIONS ON FUZZY SYSTEMS, Mechatronics, and Robotics
and Autonomous Systems.

Z. Li et al.

[44] A.A.  Shabana,  Flexible  multibody  dynamics:  review  of  past  and  recent

developments, Multibody Syst. Dyn. 1 (1997) 189–222.

[45] M. Ling, L.L. Howell, J. Cao, G. Chen, Kinetostatic and dynamic modeling of
flexure-based compliant mechanisms: a survey, Appl. Mech. Rev. 72 (3) (2020)
030802.

Zhiming  Li  received  the  B.Eng.  degree  in  Automation
from Lanzhou Jiaotong University, China, in 2022. He is
currently pursuing a Master’s degree in Control Science and
Engineering  at  Beijing  Information  Science  and  Technol-
ogy University, China. His main research interests include
physics-informed neural networks, operator learning, AI for
Science, and robotic modeling and control.

Shuangshuang Wu received the BEng degree in Automation
and  Ph.D.  degree  in  control  science  and  from  Yanshan
University,  China,  in  2014  and  2020,  respectively.  She
was  a  Post-Doctoral  Researcher  with  the  Department  of
Computer Science and Technology in Tsinghua University,
from 2020 to 2022. She is currently a lecturer with school
of Automation, Beijing Information Science and Technology
University,  China.  She  current  research  interests  include
time-delay systems, and intelligent Modeling and Control.

11

