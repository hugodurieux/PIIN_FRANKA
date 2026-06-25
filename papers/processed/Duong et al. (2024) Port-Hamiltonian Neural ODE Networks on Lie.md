IEEETRANSACTIONSONROBOTICS 1
Port-Hamiltonian Neural ODE Networks on Lie
Groups For Robot Dynamics Learning and Control
Thai Duong, Student Member, IEEE, Abdullah Altawaitan, Student Member, IEEE, Jason Stanley Student
Member, IEEE, and Nikolay Atanasov, Senior Member, IEEE
Abstract—Accurate models of robot dynamics are critical for
safe and stable control and generalization to novel operational
conditions.Hand-designedmodels,however,maybeinsufficiently
accurate, even after careful parameter tuning. This motivates
the use of machine learning techniques to approximate the
robot dynamics over a training set of state-control trajectories.
The dynamics of many robots are described in terms of their
generalizedcoordinatesonamatrixLiegroup,e.g.onSE(3)for
ground,aerial,andunderwatervehicles,andgeneralizedvelocity,
andsatisfyconservationofenergyprinciples.Thispaperproposes
aport-HamiltonianformulationoveraLiegroupofthestructure
of a neural ordinary differential equation (ODE) network to
approximatetherobotdynamics.Incontrasttoablack-boxODE
network, our formulation embeds energy conservation principle
andLiegroup’sconstraintsinthedynamicsmodelandexplicitly Fig. 1: Quadrotor trajectory tracking using a learned port-
accounts for energy-dissipation effect such as friction and drag Hamiltonian dynamics model.
forces in the dynamics model. We develop energy shaping and
damping injection control for the learned, potentially under-
actuated Hamiltonian dynamics to enable a unified approach
for stabilization and trajectory tracking with various robot the training data. Training neural network models, however,
platforms. typicallyrequireslargeamountsofdataandcomputationtime,
Index Terms—Dynamics learning, Hamiltonian dynamics, which may be impractical in mobile robotics applications.
SE(3) manifold, neural ODE networks Recent works [7]–[14] have considered a hybrid (gray-box)
approach, where prior knowledge of the physics, governing
the system dynamics, is used to assist the learning process.
SUPPLEMENTARYMATERIAL
The dynamics of physical systems obey kinematic constraints
Software and videos supplementing this paper: and energy conservation laws. These laws are known to be
https://thaipduong.github.io/LieGroupHamDL universallytruebutablack-boxmachinelearningmodelmight
struggle to infer them from the training data, causing poor
I. INTRODUCTION generalization. Instead, prior knowledge may be encoded into
thelearningmodel,e.g.,usingapriordistribution[3],agraph-
Motion planning and optimal control algorithms depend on
networkforwardkinematicmodel[15],oranetworkarchitec-
the availability of accurate system dynamics models. Models
turereflectingthestructureofLagrangian[16]orHamiltonian
obtained from first principles and calibrated over a small set
[10] mechanical systems. Moreover, many physical robot
ofparametersviasystemidentification[1]arewidelyusedfor
platforms are composed of rigid-body interconnections and
unmanned ground vehicles (UGVs), unmanned aerial vehicles
their state evolution respects the structure of a Lie group
(UAVs), and unmanned underwater vehicles (UUVs). Such
[17], e.g., the position and orientation kinematics of a rigid
models may over-simplify or even incorrectly describe the
body evolve on the SE(3) Lie group [18]. Existing works
underlying structure of the dynamical system, leading to bias
[19]–[21] on Lie group neural ODEs networks for learning
and modeling errors that cannot be corrected by adjusting a
dynamics and normalizing flows focus on preservation of the
few parameters. Data-driven techniques [2]–[6] have emerged
Lie group structure during backpropagation using an adjoint
as a powerful approach to approximate system dynamics with
method, either via a higher-dimensional space [19], [20] or
an over-parameterized machine learning model, trained over
local coordinates [21], [22].
a dataset of system state and control trajectories. Neural
The goal of this paper is to incorporate both the kinematic
networks are expressive function approximation models, ca-
structure and the energy conservation properties of physical
pableofidentifyingandgeneralizinginteractionpatternsfrom
systemswithLiegroupstatesintothestructureofadynamics
WegratefullyacknowledgesupportfromNSFCCF-2112665(TILOS). learningmodel.Wealsoaimtodesignacontrolapproachthat
The authors are with the Department of Electrical and Computer Engi- achieves stabilization or trajectory tracking using the learned
neering, University of California San Diego, La Jolla, CA 92093, USA (e-
model without requiring prior knowledge of its parameters. In
mails: {tduong,aaltawaitan,jtstanle,natanasov}@ucsd.edu). A. Altawaitan is
alsoaffiliatedwithKuwaitUniversityasaholderofascholarship. other words, the same control design should enable trajectory
4202
nuJ
11
]OR.sc[
2v02590.1042:viXra

IEEETRANSACTIONSONROBOTICS 2
tracking for learned models of different rigid-body UGVs, if permissible by the system’s degree of underactuation.
UAVs, or UUVs. • We demonstrate our dynamics learning and control ap-
Lagrangian and Hamiltonian mechanics [23], [24] provide proach extensively with simulated robot systems (a pen-
physical system descriptions that can be integrated into the dulumandaquadrotor)andseveralrealquadrotorrobots.
structure of a neural network [10], [11], [25]–[28]. Prior
work,however,hasonlyconsideredvector-valuedstates,when
II. RELATEDWORK
designing Lagrangian- or Hamiltonian-structured neural net-
works. This limits the applicability of these techniques as Data-driven techniques [35]–[39] have shown impressive
many common robot systems have states on a Lie group. results in learning robot dynamics models from state-control
For example, Hamiltonian equations of motion are available trajectories. Neural networks offer especially expressive sys-
for orientation but existing formulations rely predominantly tem models but their training requires large amounts of data,
on 3 dimensional vector parametrizations, such as Euler an- which may be impractical in mobile robot applications. Re-
gles [29], [30], which suffer from singularities. Similar to cently, a hybrid approach [7]–[14], [28], [40]–[42] has been
[19], [20], our work embeds matrix Lie groups in a higher- considered where prior knowledge about a physical system is
dimensional space Rn×n, allowing us to train the model via integratedintothedesignofamachinelearningmodel.Models
thewidelyusedneuralODEnetworkonEuclideanspace[31]. designed with structure respecting kinematic constraints [15],
However,wefocusonembeddingtheHamiltonianformulation symmetry[43],[44],Lagrangianmechanics[7]–[9],[12],[13],
of robot dynamics in the model and deriving a control policy [16], [45] or Hamiltonian mechanics [10], [11], [14], [25]–
for trajectory tracking. Concurrently, Wotte et al. [22] offer [28],[46],[47]guaranteethatthelawsofphysicsaresatisfied
an exciting approach to learn SE(3) Hamiltonian dynamics by construction, regardless of the training data.
from data using a neural ODE on Lie group, trained via local Sanchez-Gonzalez et al. [15] design graph neural networks
coordinates [21] with guarantees of satisfaction of Lie group to represent the kinematic structure of complex dynamical
constraints. The authors designed an adjoint method on the systems and demonstrate forward model learning and online
Lie algebra for neural ODE training, and a potential shaping planning via gradient-based trajectory optimization. Ruthotto
controller for stabilization of a fully actuated rigid body. et al. [43] propose a partial differential equation (PDE) in-
Our preliminary work [32] designed a neural ODE network terpretation of convolutional neural networks and derive new
[31]tocaptureHamiltoniandynamicsontheSE(3)manifold parabolicandhyperbolicResNetarchitecturesguidedbyPDE
[33], and derived a trajectory tracking control policy for theory. Wang et al. [44] design symmetry equivariant neural
potentially under-actuated systems. Our model is shown to network models, encoding rotation, scaling, and uniform mo-
provide accurate long-term trajectory predictions, respecting tion, to learn physical dynamics that are robust to symmetry
SE(3) constraints and conserve total energy with high pre- group distributional shifts.
cision. Inspired by [27], [34], we model kinetic energy and Lagrangian-based methods [7]–[9], [12], [13], [16], [45]
potential energy by separate neural networks, each governed design neural network models for physical systems based
by a set of Hamiltonian equations on SE(3). However, our on the Euler-Lagrange differential equations of motion [23],
preliminarywork[32]isdevelopedspecificallyfortheSE(3) [24], in terms of generalized coordinates q, their velocity q˙
manifold and does not model dissipation elements that drain and a Lagrangian function (q,q˙), defined as the difference
L
energy from the system, such as friction or drag forces in between the kinetic and potential energies. The energy terms
real robot systems. The Hamiltonian formulation of robot are modeled by neural networks, either separately [7], [16],
dynamicscanbegeneralizedtoport-Hamiltonianformulation, [45] or together [9].
where the dynamics are governed by energy exchange, i.e., Hamiltonian-based methods [10], [11], [14], [25]–[28] use
the law of energy conservation, energy dissipation, e.g., from a Hamiltonian formulation [23], [24] of the system dynamics,
friction, and energy injection, e.g., from control inputs. In instead, in terms of generalized coordinates q, generalized
this paper, we generalize our dynamics learning and control momentap,andaHamiltonianfunction, (q,p),representing
H
methodin[32]usingaport-HamiltonianneuralODEnetwork thetotalenergyofthesystem.Greydanusetal.[10]modelthe
to embed general matrix Lie group constraints and introduce Hamiltonian asa neural networkand update itsparameters by
an energy dissipation term, represented by another neural minimizing the discrepancy between its symplectic gradients
network, to model friction and air drag in physical systems. and the time derivatives of the states (q,p). This approach,
Wecompensateforenergydissipationinthetrajectorytracking however, requires that the state time derivatives are available
control design to provide accurate tracking performance. We in the training data set. Chen et al. [11], Zhong et al. [27]
verify our approach extensively with simulated robot systems, relax this assumption by using differentiable leapfrog integra-
including a pendulum and a Crazyflie quadrotor, and with tors [48] and differentiable ODE solvers [31], respectively.
severalrealquadrotorplatforms.Insummary,thispapermakes The need for time derivatives of the states is eliminated by
the following contributions. back-propagating a loss function measuring state discrepancy
• We design a neural ODE model that respects port- through the ODE solvers via the adjoint method. Our work
Hamiltonian dynamics over a matrix Lie group to enable extends the approach in [27], [34] by formulating the Hamil-
data-driven learning of robot dynamics. tonian dynamics over a matrix Lie group, which enforces
• We develop a unified control policy for port-Hamiltonian kinematicconstraintsintheneuralODEnetworkusedtolearn
dynamicsonaLiegroupthatachievestrajectorytracking thedynamics.Tothetal.[49]andMasonetal.[50]showthat,

IEEETRANSACTIONSONROBOTICS 3
insteadoffromstatetrajectories,theHamiltonianfunctioncan controller from stabilization to trajectory tracking. Closely
belearnedfromhigh-dimensionalimageobservations.Finziet related to our controller design, Souza et. al. [62] apply this
al. [26] show that using Cartesian coordinates with explicit techniquetodesignacontrollerforanunderactuatedquadrotor
constraints improves both the accuracy and data efficiency robot but use Euler angles as the orientation representation.
for the Lagrangian- and Hamiltonian-based approaches. In a Port-Hamiltonian structure and energy-based control design
closelyrelatedwork,Zhongetal.[34]showedthatdissipating are also used to learn distributed control policies from state-
elements, such as friction or air drag, can be incorporated control trajectories [63]–[65].
in a Hamiltonian-based neural ODE network by reformu- WeconnectHamiltonian-dynamicslearningwiththeideaof
lating the system dynamics in port-Hamiltonian form [51]. IDA-PBCcontroltoallowstabilizationofanyrigid-bodyrobot
The continuous-time equations of motions in Lagrangian or without relying on its model parameters a priori. We design a
Hamiltoniandynamicscanalsobediscretizedusingvariational trajectory-tracking controller for underactuated systems, e.g.,
integrators [52] to learn discrete-time Lagrangian and Hamil- quadrotor robots, based on the IDA-PBC approach and show
tonian systems [53]–[56] and provide long-term prediction how to construct desired pose and momentum trajectories
for control methods such as model predictive control [57]. givenonlydesiredpositionandyaw.Wedemonstratethetight
This approach eliminates the need to use an ODE solver to integrationofdynamicslearningandcontroltoachieveclosed-
roll out the dynamics but its prediction accuracy depends on loop trajectory tracking with underactuated quadrotor robots.
the discretization time step. Meanwhile, our work encodes
not only the Hamiltonian structure but also the Lie group III. PROBLEMSTATEMENT
constraints,satisfiedbythestatesofrigid-bodyrobotsystems,
Consider a robot with state x consisting of generalized
such as UGVs, UAVs and UUVs, in a neural ODE network
coordinates q evolving on a Lie group G and generalized
to learn robot dynamics from data.
velocity ξ on the Lie algebra g of G. Let x˙ = f(x,u)
Whilemostexistingdynamicslearningapproachesfocuson
characterize the robot dynamics with control input u Rm.
Euclideandynamics,manyrobotsystemshavestatesevolving ∈
For example, the state of rigid-body mobile robot, such as a
onamatrixLiegroup.RecentworksonneuralODEnetworks
UGV or UAV, may be modeled by its pose on the SE(3)
[19]–[22]onLiegroupsareclassifiedintoeitherextrinsic[19],
group, consisting of position and orientation, and its twist on
[20] or intrinsic methods [21], [22]. The extrinsic approach
these(3)Liealgebra,consistingoflinearandangularvelocity.
[19], [20] embeds a Lie group in a higher-dimensional space
The control input of an Ackermann-drive UGV may include
with Lie group constraints, enabling training with neural
its linear acceleration and steering angle rate, and that of
ODEs on Euclidean space. Our work belongs to the extrinsic
a quadrotor UAV may include the total thrust and moment
approach by enforcing matrix Lie group constraints on its
generated by the propellers. See Sec. IV-C for more details.
embedding space Rn×n, but focuses on incorporating the law
We assume that the function f specifying the robot dy-
of energy conservation, via a Hamiltonian formulation, in the
namics is unknown and aim to approximate it using a
dynamics model and providing control design for trajectory
dataset of state and control trajectories. Specifically, let
tracking.Meanwhile,theintrinsicapproach[21],[22]develops = t (Di) ,x(i) ,u(i) D consist of D state sequences x(i) ,
adjointmethodsfortrainingusinglocalcoordinatesontheLie D { 0:N 0:N }i=1 0:N
obtained by applying a constant control input u(i) to the
algebra,e.g.vialocalcharts[21],andtherefore,guaranteesLie
system with initial condition x(i) at time t (i) and sampling its
groupsconstraintsbydesign.Concurrentlytoourwork,Wotte 0 0
state x(i)(t (i) )=:x(i) at times t (i) <t (i) <...<t (i). Using
etal.[22]developaneuralODEnetworkonLiegrouptolearn n n 0 1 N
the dataset , we aim to find a function ¯f with parameters
Hamiltonian dynamics on the SE(3) manifold by deriving θ
D
θ that approximates the true dynamics f well. To optimize
an adjoint method on the Lie algebra, offering an exciting
θ, we roll out the approximate dynamics ¯f with initial state
approach for learning structure-preserving dynamics model. θ
x(i) and constant control u(i) and minimize the discrepancy
Whilefewdynamicslearningpapersconsidercontroldesign 0
based on the learned model, we develop a general trajectory between the computed state sequence x¯ 1 (i : ) N and the true state
tracking controller for Lie group Hamiltonian dynamics. The sequence x(i) in .
1:N D
Hamiltonian formulation and its port-Hamiltonian generaliza-
Problem 1. Given a dataset = t (i) ,x(i) ,u(i) D and a
tion [51] are built around the notion of system energy and, function ¯f , find the paramete D rs θ { th 0 a : t N min 0 i :N mize: }i=1
hence,arenaturallyrelatedtocontroltechniquesforstabiliza- θ
tion aiming to minimize the total energy. Since the minimum D N
(cid:88)(cid:88)
point of the Hamiltonian might not correspond to a desired min ℓ(x n (i),x¯ n (i))
θ
regulation point, the control design needs to inject additional i=1n=1 (1)
energy to ensure that the minimum of the total energy is at s.t. x¯˙(i)(t)=¯f (x¯(i)(t),u(i)), x¯(i)(t )=x(i) ,
θ 0 0
the desired equilibrium. For fully-actuated port-Hamiltonian x¯(i) =x¯(i)(t ), n=1,...,N, i=1,...,D,
systems,itissufficienttoshapethepotentialenergyonlyusing n n ∀ ∀
an energy-shaping and damping-injection (ES-DI) controller where ℓ is a distance metric on the state space.
[51].Forunderactuatedsystems,boththekineticandpotential
Further, we aim to design a feedback controller capable of
energies needs to be shaped, e.g., via interconnection and trackingadesiredstatetrajectoryx∗(t),t t ,forthelearned
0
damping assignment passivity-based control (IDA-PBC) [51], model ¯f of the robot dynamics. ≥
θ
[58]–[60]. Wang and Goldsmith [61] extend the IDA-PBC

IEEETRANSACTIONSONROBOTICS 4
Problem 2. Given an initial condition x at time t , desired Inthispaper,weconsideramatrixLiegroupelementq G
0 0
state trajectory x∗(t), t t , and learned dynamics ¯f , embedded in Rn×n, instead of its n-dimensional repres ∈ en-
0 θ
design a feedback control ≥ law u = π(x,θ,x∗(t)) such that tations, e.g., log∨q, due to potential issues of discontinuity
G
limsup ℓ(x(t),x∗(t)) is bounded. [67] and singularity [68], [69]. For example, Zhou. et al. [67]
t→∞
showthathigher-dimensionalrepresentationsofrotations,e.g.,
We consider robot kinematics on the Lie group G such
(n2 n)dimensionsforSO(n),aremoresuitableforlearning
that when there is no control input, u = 0, the dynamics −
using neural networks because they ensure continuity.
f(x,u) respect the law of energy conservation. We embed
these constraints in the structure of the parametric function Definition 6 (LeftTranslationandInvariantVectors). Theleft
¯f .WereviewmatrixLiegroups,withtheSE(3)manifoldas translation L :G G with q G is defined as:
θ q
→ ∈
an example, and Hamiltonian dynamics equations next.
L (h)=qh. (4)
q
IV. PRELIMINARIES The left-invariant vector T
e
L
q
(ξ) is defined as the derivative
A. Matrix Lie Groups of the left translation L q at h=e in the direction of ξ. This
vectordescribesthekinematicsoftheLiegroup,whichrelates
In this section, we cover the background needed to define
the velocity ξ g to the change q˙ T G of coordinates q:
Hamiltonian dynamics on a Lie group. Please refer to [17], ∈ ∈ q
[33], [66] for a more detailed overview of matrix Lie groups. q˙ =T L (ξ)=qξ. (5)
e q
Definition 1 (Dot Product). The dot product , between Given a pairing , on g∗ g (e.g., Def. 1), the dual map
two matrices ξ and ψ in Rn×m is can be chose ⟨ n · · a ⟩ s: T∗L of T L sati ⟨ s · fie ·⟩ s ×
e q e q
ξ,ψ =tr(ξ⊤ψ). (2) T∗L (η),ξ = η,T L (ξ) , (6)
⟨ ⟩ ⟨ e q ⟩ ⟨ e q ⟩
The dot product definition above is used to define the dual for any η g∗ and ξ g.
mapsinDef.6and9,andlossfunctionsinSec.V-CandV-D. ∈ ∈
Definition 7 (AdjointOperator). Forq G,theadjointAd :
q
Definition 2 (General Linear Group [17]). The general linear g g is defined as: ∈
group GL(n,R) is the group of n n invertible real matrices. →
× Ad (ψ)=qψq−1. (7)
q
Definition 3 (Matrix Lie Group [17]). A matrix Lie group G
isasubgroupofGL(n,R)withidentityelementesuchthatif The algebra adjoint ad
ξ
: g g is the directional derivative
→
anysequenceofmatrices { A n } ∞ n=0 inGconvergestoamatrix of Ad q at q=e in the direction of ξ ∈ g:
A, then either A is in G or A is not invertible. A matrix Lie (cid:12)
group is also a smooth embedded submanifold on Rn×n. ad ξ (ψ)= d Ad exp (tξ) (ψ) (cid:12) (cid:12) =[ξ,ψ]. (8)
dt G (cid:12)
t=0
Definition 4 (Tangent Space and Bundle). The tangent space
Definition8(CotangentSpaceandBundle). Thedualspaceof
T G is the set of all tangent vectors ξ to the manifold G at q.
q the tangent space T G, i.e., the space of all linear functionals
The tangent bundle TG is the set of all the pairs (q,ξ) with q
from T G to R, is called the cotangent space T∗G. At the
q G and ξ T G. q q
∈ ∈ q identity e, the cotangent space of the Lie algebra g = T e G
Definition 5 (Lie Algebra and Lie Bracket). A Lie algebra is is denoted g∗. The cotangent bundle T∗G is the set of all the
a vector space g, equipped with a Lie bracket operator [, ]: pairs (q,p) with q G and p T∗G.
· · ∈ ∈ q
g g g that satisfies:
× → Definition 9 (Coadjoint Operator). For q G, the coadjoint
∈
bilinearity: [aξ +bξ ,ξ ]=a[ξ ,ξ ]+b[ξ ,ξ ], Ad∗ : g∗ g∗ is defined as Ad∗(φ),ψ = φ,Ad (ψ) ,
1 2 3 1 3 2 3 q → ⟨ q ⟩ ⟨ q ⟩
[ξ ,aξ +bξ ]=a[ξ ,ξ ]+b[ξ ,ξ ], where φ g∗, ψ g and , is a pairing on g∗ g. The
3 1 2 3 1 3 2 ∈ ∈ ⟨· ·⟩ ×
algebra coadjoint ad∗ : g∗ g∗ is the dual map of ad ,
s J k ac e o w b - i sy id m e m nt e it t y ry : : [ξ 1 ,ξ 2 ]= − [ξ 2 ,ξ 1 ], satisfying ⟨ ad∗ ξ (φ),ψ ξ ⟩ = ⟨ φ, → ad ξ (ψ) ⟩ . ξ
The next section describes the SE(3) Lie group to illus-
[ξ ,[ξ ,ξ ]]+[ξ ,[ξ ,ξ ]]+[ξ ,[ξ ,ξ ]]=0.
1 2 3 2 3 1 3 1 2 trate the definitions above. The SE(3) Lie group is used to
Every matrix Lie group G is associated with a Lie algebra represent the position and orientation of a rigid body.
g, which is the tangent space at the identity element T G.
e
An element q G is linked with an element ξ g via the
∈ ∈ B. Example: SE(3) Manifold
exponential map exp :g G and the logarithm map log :
G g [17]. Since G tange → nt spaces of G, and in particu G lar Consider a fixed world inertial frame of reference and a
the → Lie algebra g, are isomorphic to Euclidean space, we can rigid body with a body-fixed frame attached to its center of
define a linear mapping ()∧ : Rn g and its inverse ()∨ : mass. The pose of the body-fixed frame in the world frame
g Rn, where n is the d · imension → of G. Thus, we can · map is determined by the position p = [x,y,z]⊤ R3 of the
∈
be → tween G and Rn using the compositions: center of mass and the orientation of the body-fixed frame’s
coordinate axes:
exp∧ =exp ∧, log∨ = ∨ log . (3)
G G◦ G ◦ G R= (cid:2) r r r (cid:3)⊤ SO(3), (9)
1 2 3
∈

IEEETRANSACTIONSONROBOTICS 5
wherer ,r ,r R3 aretherowsoftherotationmatrixR.A The state (q,p) T∗G evolves according to the Hamilto-
1 2 3
∈ ∈
rotation matrix is an element of the special orthogonal group: nian dynamics [33] as:
(cid:18) (cid:19)
SO(3)= (cid:8) R ∈ R3×3 :R⊤R=I,det(R)=1 (cid:9) . (10) q˙ =T e L q ∂ H ∂ (q p ,p) , (18a)
(cid:18) (cid:19)
The rigid-body position and orientation can be combined in ∂ (q,p)
a single pose matrix q SE(3), which is an element of the p˙ =ad∗ ξ (p) − T∗ e L q H ∂q +B(q)u. (18b)
∈
special Euclidean group:
Obtaining explicit expressions for ad∗(p) and T∗L (η)
ξ e q
(cid:26)(cid:20) R p (cid:21) (cid:27) with q G, ξ g, and p,η g∗ depends on the structure
SE(3)= 0⊤ 1 ∈ R4×4 :R ∈ SO(3),p ∈ R3 . (11) of the m ∈ atrix L ∈ ie algebra g an ∈ d the pairing , on g∗ g.
⟨· ·⟩ ×
AppendixIX-BprovidesdetailsandanexamplefortheSE(3)
The kinematic equations of motion of the rigid body are manifold.
determinedbythelinearvelocityv R3 andangularvelocity By comparing (14) and (18), we have:
ω R3 of the body-fixed frame w ∈ ith respect to the world
∈ ∂ (q,p)
frame, expressed in body-frame coordinates. The generalized ξ = H . (19)
velocity ζ = [v⊤, ω⊤]⊤ R6 determines the rate of change
∂p
of the rigid-body pose ac ∈ cording to the SE(3) kinematics: Let η = ∂H(q,p). When there is no control input, i.e., u=0,
∂q
the conservation of energy is guaranteed as:
(cid:20) (cid:21)
ωˆ v
q˙ =qξ =qζˆ =:q 0⊤ 0 , (12) d H (q,p) = η,q˙ + ξ,p˙ ,
dt ⟨ ⟩ ⟨ ⟩
where we overload ˆ to denote the mapping from a vector = η,T L (ξ) ξ,T∗L (η) + ξ,ad∗(p) ,
ζ R6 to a 4 4 tw · ist matrix ξ =ζˆ in the Lie algebra se(3) ⟨ e q ⟩−⟨ e q ⟩ ⟨ ξ ⟩
of ∈ SE(3)andf × romavectorω R3toa3 3skew-symmetric =0, (20)
matrix ωˆ in the Lie algebra so ∈ (3) of SO( × 3): because of Eq. (6) and, by definition,
  ξ,ad∗(p) = ad (ξ),p = [ξ,ξ],p =0. (21)
0 ω 3 ω 2 ⟨ ξ ⟩ ⟨ ξ ⟩ ⟨ ⟩
−
ωˆ = ω
3
0 ω 1. (13)
− D. Reformulation as Port-Hamiltonian Dynamics
ω ω 0
2 1
−
Thenotionofenergyindynamicalsystemsissharedacross
Please refer to [68] for an excellent introduction to the use of
multiple domains, including mechanical, electrical, and ther-
SE(3) in robot state estimation problems.
mal. A port-Hamiltonian generalization [51] of Hamiltonian
mechanics is used to model systems with energy-storing ele-
ments (e.g., kinetic and potential energy), energy-dissipating
C. Hamiltonian Dynamics on Matrix Lie Groups
elements (e.g., friction or resistance), and external energy
Inthissection,wedescribeHamilton’sequationsofmotion sources (e.g., control inputs), connected via energy ports. An
on a matrix Lie group [33], [66]. Our neural network archi- input-state-output port-Hamiltonian system has the form:
t d e y c n tu a r m e ic d s e , s w ig h n ic i h n e S n e c c o . de V b i o s th b k a i s n e e d m o a n tic L c ie on g s r t o ra u i p nts H a a n m d il e t n o e n r i g an y (cid:20) q˙ (cid:21) =( (q,p) (q,p)) (cid:34) ∂ ∂ H q (cid:35) + (q,p)u, (22)
conservation. p˙ J −R ∂H G
∂p
Consider a system with generalized coordinates q in a
where (q,p) is a skew-symmetric interconnection matrix,
matrix Lie group G and generalized velocity q˙ T G. The J
∈ q representing the energy-storing elements, (q,p) 0 is
dynamics of the state x=(q,q˙) TG satisfy: R ⪰
∈ a positive semi-definite dissipation matrix, representing the
energy-dissipating elements, and (q,p) is an input matrix
q˙ =T e L q (ξ)=qξ, (14) G
such that (q,p)u represents the external energy sources. In
G
where ξ is a element in the Lie algebra g. theabsenceofenergy-dissipatingelementsandexternalenergy
The Lagrangian on a Lie group : G g R is defined sources,theskew-symmetryof (q,p)guaranteestheenergy
as the difference between the kinet L ic ene × rgy → : G g R conservation of the system. J
and the potential energy :G R: T × → To model energy dissipating elements such as friction or
V → drag forces, we reformulate the Hamiltonian dynamics on a
(q,ξ)= (q,ξ) (q). (15) matrix Lie group (18) in port-Hamiltonian form (22). Such
L T −V
elements are often modeled [70] as a linear transformation
TheHamiltonianisobtainedusingaLegendretransformation: D(q,p) 0 of the velocity ξ and only affect the generalized
⪰
momenta p, i.e.,
(q,p)=p ξ (q,ξ), (16)
H · −L (cid:20) 0 0 (cid:21)
(q,p)= . (23)
where the momentum p is defined as: R 0 D(q,p)
∂ (q,ξ) TheHamiltoniandynamics(18)isaspecialcaseof(22),where
p= L . (17) the dissipation matrix is D(q,p) = 0, the input matrix is
∂ξ

IEEETRANSACTIONSONROBOTICS 6
(q,p) = (cid:2) 0⊤ B(q)⊤(cid:3)⊤ and the interconnection matrix where the components D (q,p) and D (q,p) correspond to
v ω
G
(q,p) can be obtained by rearranging (18) with u = 0 p and p , respectively. The equations of motions on the
J v ω
and is guaranteed to be skew-symmetric due to the energy SE(3) manifold are written in port-Hamiltonian form as:
conservation(20).Inanimplementation,thecoordinatesqand
∂ (q,p)
momentum p may be represented as vectors in Rn2, leading p˙ = R H , (30a)
to an interconnection matrix (q,p) R2n2×2n2.
∂p
v
J ∈ ∂ (q,p)
r˙ = r H , i=1,2,3 (30b)
i i × ∂p
ω
E. Example: Hamiltonian Dynamics on the SE(3) Manifold ∂ (q,p) ∂ (q,p)
p˙ = p H R⊤ H (30c)
Inthissection,weconsiderthegeneralizedcoordinateqofa v v× ∂p ω − ∂p
mobile robot consisting of its position p R3 and orientation ∂ (q,p)
R SO(3). Let q = (p,R) be the gen ∈ eralized coordinates − D v (q,p) H ∂p +b v (q)u,
and ∈ ζ = (v,ω) R6 be the generalized velocity, consisting ∂ (q,p) v ∂ (q,p)
of the body-fram ∈ e linear velocity v R3 and the body-frame p˙ ω = p ω× H ∂p +p v× H ∂p + (30d)
angularvelocityω R3.Thecoordi ∈ nateqevolvesontheLie ω v
3
∈ (cid:88) ∂ (q,p) ∂ (q,p)
group SE(3) while the generalized velocity satisfies q˙ =qξ, r H D (q,p) H +b (q)u,
where ξ =ζˆ is a twist matrix in se(3), as shown in Eq. (12). i=1 i × ∂r i − ω ∂p ω ω
The isomorphism between se(3) and R6 via (12) simplifies
where the input matrix is B(q)= (cid:2) b (q)⊤ b (q)⊤(cid:3)⊤ .
the Hamiltonian (18) and its port-Hamiltonian formulation v ω
(22) as follows. The Lagrangian function on SE(3) can be
expressed in terms of q and ζ, instead of q and ξ: F. Neural ODE Networks
In this section, we briefly describe neural ODE networks
1
(q,ζ)= ζ⊤M(q)ζ (q). (24) [31], which approximate the closed-loop dynamics x˙ =
L 2 −V
f(x,π(x)) of a system for some unknown control policy
The generalized mass matrix has a block-diagonal form when u = π(x) by a neural network ¯f (x). The parameters of
θ
the body frame is attached to the center of mass [33]: ¯f (x) are trained using a dataset = t (i) ,x(i) of
(cid:20) (cid:21) s θ tate trajectory samples x(i) = x(i D )(t (i) ) { via 0:N forw 0 a :N rd } i and
M (q) 0 n n
M(q)= v 0 M ω (q) ∈ S6 ≻ × 0 6, (25) backward passes through a differentiable ODE solver, where
the backward passes provide the gradient of the loss function.
where M (q),M (q) S3×3. The generalized momenta are Given an initial state x(i) at time t (i), a forward pass returns
defined, a v s before, ω via th ∈ e p ≻ a 0 rtial derivative of the Lagrangian predicted states at times 0 t (i) ,...,t (i 0 ):
1 N
with respect to the twist:
x¯ (i) ,...,x¯ (i) =ODESolver(x(i) ,¯f ,t (i) ,...,t (i) ). (31)
(cid:20) (cid:21) { 1 N } 0 θ 1 N
p ∂ (q,ζ)
p= v = L =M(q)ζ R6. (26) The gradient of a loss function, (cid:80)D (cid:80)N ℓ(x(i) ,x¯ (i) ), is
p ∂ζ ∈ i=1 j=1 j j
ω
back-propagated by solving another ODE with adjoint states.
The Hamiltonian function of the system becomes: Theparametersθ areupdatedbygradientdescenttominimize
the loss. For physical systems, Zhong et al. [27] extends the
1
(q,p)=p ζ (q,ζ)= p⊤M−1(q)p+ (q). (27) neural ODE by integrating the Hamiltonian dynamics on Rn
H · −L 2 V into the neural network model ¯f (x), and consider zero-order
θ
By vectorizing the generalized coordinates hold control input u, leading to a neural ODE network with
q = [p⊤ r⊤ r⊤ r⊤]⊤, the Hamiltonian dynamics the following approximated dynamics:
1 2 3
on SE(3) can be described in port-Hamiltonian form (22) (cid:20)
x˙
(cid:21) (cid:20)¯f
(x,u)
(cid:21)
[33], [71], [72] with interconnection matrix: = θ . (32)
u˙ 0
(cid:20)
0
q×(cid:21) (cid:20)
0 pˆ
(cid:21)
(q,p)= , p× = v , (28) Recently, neural ODE networks have been extended from
J − q×⊤ p× pˆ v pˆ ω EuclideanspacetoLiegroups[19]–[22],guaranteeingthatthe
Lie group constraints are satisfied by the predicted states by
and input matrix (q,p) = (cid:2) 0⊤ B(q)⊤(cid:3)⊤ , where
design.WhileitispossibletotrainourHamiltoniandynamics
(cid:20) R⊤ 0 0 G 0 (cid:21)⊤ model using a Lie group neural ODE network, we leave this
q× = . Note that the kinematics con-
0 ˆr⊤ ˆr⊤ ˆr⊤ investigation for future work due to the lack of suitable open-
1 2 3
straints q˙ = qξ of the coordinates q on SE(3), which source software for Lie group ODE integration.
guarantee that the coordinates q remain in SE(3), are not
affected by vectorization. The port-Hamiltonian formulation V. LEARNINGLIEGROUPHAMILTONIANDYNAMICS
allows us to model dissipation elements in the dynamics by
We consider a Hamiltonian system with unknown kinetic
the dissipation matrix:
energy (q), potential energy (q), input matrix B(q), dis-
(cid:20) D (q,p) 0 (cid:21) sipation T matrix D(q,p), and de V sign a structured neural ODE
D(q,p)= v S6×6, (29)
0 D ω (q,p) ∈ ≻0 network to learn these terms from state-control trajectories.

IEEETRANSACTIONSONROBOTICS 7
tomaticdifferentiation,e.g.byPytorch[75].Theapproximated
𝐱ොt dynamics function ¯f (x,u) is implemented in a neural ODE
𝖖
𝛏 𝐁
𝒱
𝒯
𝜽
𝜽
𝜽
𝖕
𝖖ሶ
ሶ
=
−T𝐞 ∗L𝖖 𝜕 𝜕 ℋ 𝖖 𝜽
T𝐞
+
L𝖖
ad
𝜕
𝛏 ∗
𝜕
ℋ
𝖕
𝖕
𝜽
−𝐃𝜽(𝖖,𝖕) 𝜕 𝜕 ℋ 𝖕
+𝐁𝜽𝖖𝐮
network architecture θ for training, shown in Fig. 2.
C. Training Process
𝐃𝜽 𝖕= 𝜕
𝜕
ℒ
𝛏
𝜽 ℒ𝜽𝖖,𝛏 =𝒯𝜽𝖖,𝛏 −𝒱𝜽𝖖
Letx¯(i)(t)denotethestatetrajectorypredictedwithcontrol
𝐮
𝛏ሶ=
d
d
t
𝜕
𝜕
ℋ
𝖕
𝜽 ℋ𝜽𝖖,𝖕 =𝖕⋅𝛏−ℒ𝜽𝖖,𝛏 input u(i) by the approximate dynamics ¯f
θ
initialized at
Hamilton’s equations of motion = 𝐟𝛉 ҧ x¯(i)(t (
0
i) ) = x(
0
i). For sequence i, forward passes through the
ODE solver in (31) return the predicted states x¯ (i) at times
0:N
Neural ODE Networks 𝐮ሶ=𝟎 𝖖ሶ 𝛏ሶ 𝐱ොሶ t t (i) , where x¯ (i) = [q¯(i)⊤ ξ¯(i)⊤ ]⊤, for n = 1,...,N. The
0:N n n n
predicted coordinates q¯(i) and the ground-truth ones q(i) are
𝜽 𝐱𝟎,𝐮 𝒕𝟏,𝒕𝟐,…,𝒕𝑵 𝐱ො𝟏,𝐱ො𝟐, …, 𝐱ො𝐍 n n
used to calculate a loss on the Lie group manifold:
Fig. 2: Architecture of port-Hamiltonian neural ODE network
on matrix Lie group. The trainable terms are shown in green. L q (θ)= (cid:88) D (cid:88) N (cid:13) (cid:13) (cid:13) (cid:13) log∨ G (cid:18) q¯ n (i) (cid:16) q( n i) (cid:17)−1 (cid:19)(cid:13) (cid:13) (cid:13) (cid:13) 2 . (34)
i=1n=1 2
A. Data Collection WeusethesquaredEuclideannormtocalculatelossesforthe
We collect a data set = t (i) ,x(i) ,u(i) D consisting generalized velocity terms:
f o o f r s n tate = se 0 q , u .. e . n , c N es . x S ( 0 u i : ) N ch D , d w a h t { a er 0 e a : r N e x( n g i) e 0 n :N e = rated [ } q b i ( n = y i) 1 ⊤ app ξ ly ( n i i ) n ⊤ g ]⊤ a L (θ)= (cid:88) D (cid:88) N ξ(i) ξ¯(i) 2. (35)
constant control input u(i) to the system and sampling the ξ ∥ n − n ∥2
i=1n=1
state x(i) = x(i)(t (i) ) at times t (i) for n = 0,...,N. The
n n n The total loss L(θ) is defined as:
generalizedcoordinatesqandvelocityξmaybeobtainedfrom
a state estimation algorithm, such as odometry algorithm for L(θ)=L (θ)+L (θ). (36)
q ξ
mobile robots [73], [74], or from a motion capture system.
In physics-based simulation the data can be generated by ap-
ThegradientofthetotallossfunctionL(θ)isback-propagated
plying random control inputs u(i). In real-world applications, by solving an ODE with adjoint states [31]. Specifically, let
where safety is a concern, data may be collected by a human a = ∂ ∂ L x¯ be the adjoint state and s = (x¯,a,∂ ∂ L θ ) be the
operator manually controlling the robot. augmented state. The augmented state dynamics are [31]:
∂¯f ∂¯f
B. Model Architecture s˙ =¯f s =(¯f θ , − a⊤ ∂x¯ θ , − a⊤ ∂θ θ ). (37)
Since robots are physical systems, their dynamics f(x,u)
The predicted state x¯, the adjoint state a, and the derivatives
satisfy the Hamiltonian formulation (Sec. IV-C). To learn the ∂L can be obtained by a single call to a reverse-time ODE
dynamics f(x,u) from a trajectory dataset , we design a ∂θ
solver starting from s =s(t ):
D N N
neuralODEnetwork(Sec.IV-F),approximatingthedynamics
(cid:18) (cid:19)
via a parametric function ¯f θ (x,u) based on Eq. (18). s = x¯ ,a , ∂ L =ODESolver(s ,¯f ,t ), (38)
To integrate the Hamiltonian equations into the structure 0 0 0 ∂θ N s N
of ¯f (x,u), we use four neural networks with parameters
θ where at each time t ,k = 1,...,N, the adjoint state a at
θ = (θ ,θ ,θ ,θ ) to approximate the kinetic energy by k k
T V D B time t is reset to ∂L . The resulting derivative ∂L is used
T θ (q,ξ),thepotentialenergyby V θ (q),thedissipationmatrix to upd k ate the param ∂ e x¯ te k rs θ using gradient descent. ∂θ Note that
by D (q,p), and the input matrix by B (q), respectively.
θ θ even though the Lie group and Hamiltonian structures are
Since the generalized momenta p are not directly available in preservedinthecontinuous-timedynamicsfunction¯f,theLie
,thetimederivativeofthegeneralizedvelocityξ isobtained
D from Eq. (19). The approximated dynamics function ¯f (x,u) groupconstraintsmightstillbeviolatedbythepredictedstates
θ when the model is trained with a neural ODE network on the
is described with an internal state p as follows: embedding space Rn×n instead of on the matrix Lie group
(cid:18) (cid:19)
q˙ =T e L q ∂ H θ ∂ ( p q,p) , (33a) [ a 2 s 1 5 ], th [ - 2 o 2 r ] d . e T r o R p u r n ev g e e n -K tt u h t i t s a , [ w 7 e 6] u , s i e n a th h e ig E h- u o c r l d id e e r a i n nte s g p r a a c t e or n , e s u u r c a h l
∂ (q,p) ODE, for which open-source software is available [31], [77].
p˙ =ad∗(p) D (q,p) H θ
ξ − θ ∂p Investigating how to train Hamiltonian models with a neural
(cid:18) (cid:19) ODE network defined directly on the Lie group [21], [22],
∂ (q,p)
− T∗ e L q H θ ∂q +B θ (q)u, (33b) [78] is an interesting future direction. For example, the Lie
group neural ODE by Wotte et al. [22] offers an approach
d ∂ (q,p)
ξ˙ = H θ , (33c) to guarantee Lie group constraints in the dynamics model.
dt ∂p
Closely related to this direction, Duruisseaux et al. [54] learn
where (q,p)=p ξ (q,ξ),and (q,ξ)= (q,ξ) discrete-time Hamiltonian dynamics while guaranteeing Lie
θ θ θ θ
(q). H The time deri · va − tiv L e d ∂Hθ(q,p) L is calculated T using au − - group constraints by design using variational integration.
V θ dt ∂p

IEEETRANSACTIONSONROBOTICS 8
D. Application to SE(3) Hamiltonian Dynamics Learning The total loss (θ) is defined as:
L
This section applies our Lie group Hamiltonian dynamics
L(θ)=L (θ)+L (θ)+L (θ). (44)
learning approach to estimate mobile robot dynamics on the R p ζ
SE(3) manifold (Sec. IV-E).
Neural ODE model architecture: When the Hamiltonian VI. ENERGY-BASEDCONTROLDESIGN
dynamics in (18) are defined on the SE(3) manifold, the
equations of motion become (30). The neural ODE network The function ¯f θ (33) learned in Sec. V satisfies the port-
architecturein(33)issimplifiedasfollows.Weusefiveneural Hamiltonian dynamics in Eq. (22) by design. This section
networks with parameters θ = (θ ,θ ,θ ,θ ,θ ) to ap- extendstheinterconnectionanddampingassignmentpassivity-
v ω V D B
proximatetheblocksM−1(q),M−1 (q)oftheinversegener- based control (IDA-PBC) approach [51], [61], [62] to Lie
v;θ ω;θ
alizedmassin(25),thepotentialenergy (q),thedissipation groups to achieve trajectory tracking (Problem 2) based on
θ
V
matrix D (q,p), and the input matrix B (q), respectively. the learned port-Hamiltonian dynamics. We further derive a
θ θ
The approximated kinetic energy is calculated as (q,p) = tracking controller specifically for learned Hamiltonian dy-
θ
1p⊤M−1(q)p, where M (q)=diag(M (q),M T (q)). namics on the SE(3) manifold in Sec. V-D. In the remainder
2 θ θ v;θ ω;θ
Neural network design: In many applications, nominal of the paper, we omit the subscript θ in the learned model for
information is available about the generalized mass matrices readability.
M−1(q), M−1 (q), the potential energy (q), the dissipa-
v;θ ω;θ V θ
tionmatrixD (q,p),andtheinputmatrixB (q),andcanbe
θ θ
included in the neural network design. A. IDA-PBC Control Design for Trajectory Tracking
LetM− v0 1(q),M− ω0 1(q),andD 0 (q,p)bethenominalvalues Consider a desired regulation point (q∗,p∗) T∗G that
of the generalized mass matrices M−1(q), M−1 (q) and the ∈
v;θ ω;θ the system should be stabilized to. The Hamiltonian function
dissipation matrix D (q,p) with Cholesky decomposition:
θ (q,p),representingthetotalenergyofthesystem,generally
H
M−1(q)=L (q)L⊤ (q), does not have a minimum at (q∗,p∗). An IDA-PBC con-
v0 v0 v0
troller [51], [58], [61] is designed to inject additional energy
M−1(q)=L (q)L⊤ (q), (39)
ω0 ω0 ω0 (q,p) such that the desired total energy:
a
D (q)=L (q)L⊤ (q). H
0 D0 D0
(q,p)= (q,p)+ (q,p) (45)
d a
The learned terms M−1(q), M−1 (q), and D (q,p) are H H H
v;θ ω;θ θ
obtained using Cholesky decomposition: achieves its minimum at (q∗,p∗). In other words, the closed-
loop system obtained by applying the controller to the port-
M−1(q)=(L (q)+L (q))(L (q)+L (q)) ⊤ +ε I,
v;θ v0 v v0 v v Hamiltonian dynamics in (22) should have the form:
M−1 (q)=(L (q)+L (q))(L (q)+L (q)) ⊤ +ε I,
D θ ω ( ; q θ ,p)=(L D ω0 0 (q,p)+ ω L D (q,p) ω ) 0 (L D0 (q, ω p)+L D (q, ω p (4 ) 0 ) ⊤ ) (cid:20) p q˙ ˙ (cid:21) =( J d (q,p) −R d (q,p)) (cid:34) ∂ ∂ ∂ H H q d d (cid:35) . (46)
∂p
where L (q), L (q), and L (q,p) are lower-triangular ma-
trices im v plement ω ed as three n D eural networks with parameters to ensure that (q∗,p∗) is an equilibrium. The control input
θ , θ , and θ respectively, and ε ,ε >0. u should be chosen so that (22) and (46) are equal. This
v ω D v ω
The potential energy (q) and the input matrix B(q) matching equation design does not directly apply to trajectory
are implemented with no V minal values (q) and B (q) as tracking, especially for underactuated systems [61], [62].
0 0
follows: V Consider a desired trajectory (q∗(t),p∗(t)) that the sys-
(q)= (q)+L (q), tem should track. Let (q (t),p (t)) denote the error in the
V θ V 0 V (41) e e
B (q)=B (q)+L (q), generalized coordinates and momentum, respectively, where
θ 0 B
q = (q∗)−1q G and p = p p∗ T∗ G. For trajectory
e w te h r e s re θ L V V a ( n q d ) θ an B d , L re B sp (q ec ) ti a v r e e ly tw . oneuralnetworkswithparam- t t r e e a r c m k s in o g f , th th e e er d r ∈ e o s r ir s e t d ate to , t w al e ith en d e e r s g − i y red H c d ∈ l ( o q s e e , q d p e -l e o ) op is dy d n efi am ne i d cs: in
Loss function: The orientation loss is calculated as:
(cid:20)
q˙
(cid:21) (cid:34) ∂Hd (cid:35)
L R (θ)= (cid:88) D (cid:88) N (cid:13) (cid:13) (cid:13) log∨ SO(3) (R¯( n i)R( n i)⊤) (cid:13) (cid:13) (cid:13) 2 2 , (42) p˙ e e =( J d (q e ,p e ) −R d (q e ,p e )) ∂ ∂ ∂ H p q e e d . (47)
i=1n=1
Matching (47) with (22) leads to the following requirement
WeusethesquaredEuclideannormtocalculatelossesforthe
for the control input:
position and generalized velocity terms:
(cid:34) (cid:35)
D N
∂Hd
L p (θ)= (cid:88)(cid:88) ∥ p( n i) − p¯( n i) ∥ 2 2 , G (q,p)u=( J d (q e ,p e ) −R d (q e ,p e )) ∂ ∂ ∂ H p q e d (48)
L ζ (θ)= i (cid:88) = D 1n (cid:88) = N 1 ∥ ζ( n i) − ζ¯( n i) ∥ 2 2 . (43) − ( J (q,p) −R (q,p)) (cid:34) ∂ ∂ ∂ ∂ H H p q (cid:35) + (cid:20) e p q˙ ˙ (cid:21) − (cid:20) p q˙ ˙ e e (cid:21) .
i=1n=1

IEEETRANSACTIONSONROBOTICS 9
The control input can be obtained from (48) as the sum andplugging (q,p)and (q,p)from(28)intothematching
J R
u=u +u of an energy-shaping component u and a equations in (48), leads to:
ES DI ES
damping-injection component u DI : 0 = J ∂ H d q× ∂ H +q˙ q˙ , (54)
(cid:32) (cid:34) ∂Hd (cid:35) (cid:20) q˙ (cid:21) 1 ∂p e − ∂p − e
u ES = G † − (q ( , J p ( ) q,p ( J ) d − (q R e , ( p q e , ) p ) )) (cid:34) ∂ ∂ ∂ H p q ∂ ∂ ∂ ∂ e e H H d p q (cid:35) − + (cid:20) p˙ p q˙ ˙ e e (cid:21)(cid:33) , (49a) B(q)u = − q× K ⊤ d ∂ ∂ ∂ ∂ H q H p e d − + J⊤ 1 D ∂ ∂ ( H q q , e d p + ) ∂ ∂ J H p 2 ∂ ∂ + H p p e ˙ d − − p˙ p e × . ∂ ∂ H p (55)
(cid:34) ∂Hd (cid:35) Assuming M d (q e ) = M(q), (54) is satisfied if we choose
u DI = −G †(q,p) R d (q e ,p e ) ∂ ∂ ∂ H p q e
e
d , (49b) J 1 = (cid:20) R 0 ⊤ ˆr 0 ⊤
e1
ˆr 0 ⊤
e2
ˆr 0 ⊤
e3
(cid:21)⊤ . Indeed, we have q˙ = q×∂ ∂ H p
(from (11) and (19)) and
p w lo s h n e e g u r d e o as - G in t † v h ( e e q rs , d e p e ) o si f re = G d (q i (cid:0) n , G t p e ⊤ ) rc . ( o q T n , h n p e e ) c G c ti o ( o q n n t , r p o m l ) (cid:1) a i − t n r 1 i p x u G t ⊤ u ( d q E , , S d p i ) s e s x i i i p s s a ts ti t o h a n e s ∂ ∂ H p e d =M− d 1p e = (cid:20) ω v e e (cid:21) = (cid:20) ω v − − R R ⊤ ⊤ R R ∗ ∗ ω v∗ ∗ (cid:21) .
J The error dynamics becomes:
matrix ,andtotalenergy satisfythefollowingmatching
d d
conditio R n for all (q,p) T∗ H G and (q ,p ) T∗G:  p˙ p˙∗
G †(q,p) (cid:32) J d (q e ,p e ) − ∈ R d (q e ,p e )) e (cid:34) ∂ ∂ ∂ ∂ H H e p q e d d ∈ (cid:35) (50) q˙ e =    r r r − ˙ ˙ ˙ e e e 3 2 1    = (cid:20) R 0 ⊤ ˆr 0 ⊤ e1 ˆr 0 ⊤ e2 ˆr 0 ⊤ e3 (cid:21)⊤(cid:20) ω v e e (cid:21) =J 1 ∂ ∂ H p e d ,
− ( J (q,p) −R (q,p)) (cid:34) ∂ ∂ ∂ ∂ H H p q (cid:35) + (cid:20) p q˙ ˙ e (cid:21) − (cid:20) p q ˙ ˙ e e (cid:21)(cid:33) =0. s p˙ ince p˙ R ∗ ˙ e = = R d d t v (R e ) R = ∗v R ∗ e = ω (cid:98)e R a v s e s . hownin[79,Sec.III-A] ( a 5 n 6 d )
− −
Thedesiredcontrolinputcanbeobtainedfrom(55)asu=
where ⊥(q,p) is a maximal-rank left annihilator of (q,p), u +u with:
G G ES DI
i.e., ⊥(q,p) (q,p)=0. (cid:18)
∂ ∂ ∂
G G u =B†(q) q×⊤ H J⊤ H d +J H d (57a)
ES ∂q − 1 ∂q 2 ∂p
e e
(cid:19)
B. Tracking Control for Port-Hamiltonian Dynamics on the p× ∂ H +D(q,p) ∂ H +p˙ p˙ ,
SE(3) Manifold − ∂p ∂p − e
∂
Consider a desired state trajectory x∗(t) = (q∗(t),ζ∗(t)) u = B†(q)K H d , (57b)
that the system should track where q∗(t) SE(3) is the DI − d ∂p e
desired pose and ζ∗(t) = (cid:2) v∗(t)⊤ ω∗(t)⊤(cid:3)∈⊤ is the desired where B†(q) = (cid:0) B⊤(q)B(q) (cid:1)−1 B⊤(q) is the pseudo-
generalized velocity expressed in the desired frame. Let p∗ = inverse of B(q). The matching condition (50) becomes:
(cid:20) R⊤R∗v∗(cid:21)
(cid:18)
M R⊤R∗ω∗ denote the desired momentum, defined based B⊥(q) q×⊤ ∂
∂
H
q −
J⊤
1
∂
∂
H
q
d +J
2
∂
∂
H
p
d
on(26)withthedesiredvelocityexpressedinthebodyframe. e e (58)
(cid:19)
Let p e = p p∗ and R e = R∗⊤R = (cid:2) r e1 r e2 r e3 (cid:3)⊤ p× ∂ H +p˙ p˙ =0.
be the positio − n error and rotation error between the current − ∂p − e
orientation R and the desired one R∗, respectively. The In this paper, we reshape the open-loop Hamiltonian (q,p)
H
vectorized error q in the generalized coordinates is: intothefollowingdesiredtotalenergy (q ,p ),minimized
e H d e e
along the desired trajectory:
q e = (cid:2) p∗ e ⊤ r⊤ e1 r⊤ e2 r⊤ e3 (cid:3)⊤ . (51) 1
(q ,p )= (p p∗)⊤K (p p∗) (59)
H d e e 2 − p −
The error in the generalized momenta is p = p p∗,
described in the body frame. The desired to e tal ener − gy is + 1 tr(K R (I R∗⊤R))+ 1 (p p∗)⊤M−1(q)(p p∗),
2 − 2 − −
defined in terms of the error state as:
where K ,K 0 are positive-definite matrices.
p R
≻
1 For an SE(3) rigid-body system with constant generalized
(q ,p )= p⊤M−1(q )p +V (q ), (52)
H d e e 2 e d e e d e mass matrix M d = M and J 2 = 0, which is a common
choice, the energy-shaping term in (57a) and the damping-
where M (q ) and V (q ) are the desired generalized mass
d e d e injection term in (57b) simplify as:
and potential energy.
(cid:18)
Choosingthefollowingdesiredinter-connectionmatrixand u (q,p)=B†(q) q×⊤ ∂V (cid:0) p× D(q,p) (cid:1) M−1p
dissipation matrix: ES ∂q − −
(cid:19)
(cid:20) 0 J (cid:21) (cid:20) 0 0 (cid:21) e(q,q∗)+p˙∗ ,
(q ,p )= 1 , (q ,p )= , −
J d e e − J⊤ 1 J 2 R d e e 0 K d (53) u DI (q,p)= B†(q)K d M−1(p p∗), (60)
− −

IEEETRANSACTIONSONROBOTICS 10
where the generalized coordinate error between q and q∗ is: VII. EVALUATION
∂V (cid:20) R⊤K (p p∗) (cid:21) We verify the effectiveness of our port-Hamiltonian neural
e(q,q∗):=J⊤ 1 ∂q d = 1(cid:0) K R∗⊤R p R − ⊤R∗K⊤(cid:1)∨ , ODE network for dynamics learning and control on matrix
e 2 R − R (61) Liegroupsusingasimulatedpendulum,asimulatedCrazyflie
quadrotor, and a real PX4 quadrotor platform, whose states
and the derivative of the desired momentum is:
evolve on the SE(3) manifold. The implementation details
p˙∗ =M
(cid:20)
R⊤R
R
∗
⊤
ω˙
p¨
∗
∗
− ωˆ
ωˆR
R
⊤
⊤
p˙
R
∗
∗ω∗
(cid:21)
. (62) for the experiments are provided in Appendix IX-A.
e
−
By expanding the terms in (60), we have: A. Pendulum
(cid:20) (cid:21) In this section, we verify our port-Hamiltonian dynamics
pˆ ω
p×M−1p = p×ζ = pˆ ω v +pˆ v , (63) learning and control approach on the SO(3) manifold. We
ω v
(cid:20) v R⊤p˙∗ (cid:21) consider a pendulum with the following dynamics:
M−1(p p∗) = − , (64)
− ω R⊤R∗ω∗ φ¨= 15sinφ+3u 0.2φ˙, (68)
− − −
(cid:34) (cid:35)
q×⊤ ∂ V =
R⊤∂V
∂
(
p
q)
. (65) where φ is the angle of the pendulum with respect to its
∂q (cid:80)3 ˆr ∂V(q) vertically-downward position and u is a scalar control input.
i=1 i ∂ri
The ground-truth mass, potential energy, friction coefficient,
Theorem 1. Consider a port-Hamiltonian system on the and the input gain are: m = 1/3, (φ) = 5(1 cosφ),
SE(3)manifoldwithdynamics(30).Assumethatthematching D(φ) = 0.2/3, and B(φ) = 1, resp V ectively. We − collected
condition (58) is satisfied, the desired momentum’s deriva- data of the form (cosφ,sinφ,φ˙) from an OpenAI Gym
tive p˙∗ is bounded, and the matrices K p , K R , and K d environment, provi { ded by [27], with } the dynamics in (68). To
are positive-definite. The control policy in (57) leads to illustrateourLiegroupneuralODElearning,werepresentthe
closed-loop error dynamics in (47), (53). The tracking er- angle φ as a rotation matrix:
ror (q ,p ) = ((p ,R ),p ) asymptotically stabilizes to
e e e e e  
cosφ sinφ 0
((0,I),0)withLyapunovfunctiongivenbythedesiredHamil-
−
tonian (q ,p ) in (59).
R=sinφ cosφ 0, (69)
H d e e 0 0 1
Proof. Since the matching condition is satisfied and the de-
siredmomentum’sderivativep˙∗ isbounded,thecontrolpolicy representing the pendulum orientation. We let ω = [0,0,φ˙]
and remove position p and linear velocity v from the Hamil-
in(57),(57b)existsandachievesthedesiredclosed-looperror
tonian dynamics in (30), restricting the system to the SO(3)
dynamics:
manifold with generalized coordinates q=[r⊤ r⊤ r⊤]⊤.
(cid:20) q˙ (cid:21) (cid:20) 0 J (cid:21)(cid:34) ∂Hd (cid:35) AsdescribedinSec.V-D,controlinputsu(i 1 ) wer 2 esam 3 pled
p˙ e e = − J⊤ 1 J 2 − 1 K d ∂ ∂ ∂ H p q e e d . (66) r o a f n 0 d . o 0 m 5s ly ,f a o n rm d i a n p g p a lie d d at t a o se t t he p = en (cid:110) du t ( l i u ) m ,q fo (i r ) fi , v ω e ( t i i ) m , e u i ( n i) t ) e (cid:111) rv D als
We have tr (cid:0) I R∗⊤R (cid:1) 0, as all entries in R SO(3) D 0:N 0:N 0:N i=1
− ≥ e ∈ with N = 5 and D = 5120. We trained an SO(3) port-
are less than 1. Since M, K and K are positive-definite
p R HamiltonianneuralODEnetworkasdescribedinSec.V-Dfor
a
m
c
a
h
t
i
r
e
i
v
ce
e
s
s
,
m
th
i
e
ni
d
m
es
u
i
m
red
va
H
lu
am
e
i
0
lto
o
n
n
ia
ly
n
H at
d
q
is p
=
osi
(
t
0
iv
,
e
I
-
)
de
a
fi
n
n
d
ite
p
, an
=
d 5000iterationswithoutanynominalmodel,i.e.,M−
ω0
1(q)=0,
e e D (q,p)=0, V (q)=0 and B (q)=0.
ω0 0 0
0, i.e., no position, rotation and momentum errors. The time
As noted in [27], [32], since the generalized momenta p
derivative of (q ,p ) can be computed as:
H d e e are not available in the dataset, the dynamics of q in (68)
∂ ⊤ ∂ ⊤ do not change if p is scaled by a factor β > 0. This is also
H ˙ d (q e ,p e )= ∂ H q d q˙ e + ∂ H p d p˙ e (67) true in our formulation as scaling p leaves the dynamics of
e e q in (30) unchanged. To emphasize this scale-invariance, let
= p⊤M−1(q)K M−1(q)p .
− e d e M β (q) = βM(q), β (q) = β (q), D β (q,p) = βD(q,p)
V V
B (q)=βB(q), and:
AsK andM(q)arepositive-definite,wehave ˙ (q ,p ) β
d H d e e ≤
0forall(q ,p )andequalityholdsat((0,I),0).ByLaSalle’s p =M (q)ω =βp, p˙ =βp˙,
e e β β β
t i o nv ti a c r a i l a l n y c c e o p n r v i e n r c g i e pl t e o [ ( 8 ( 0 0 ] , , I t ) h , e 0 t ) r . acking errors (q e ,p e ) asymp- H β (q,p)= 2 1 p⊤ β M− β 1(q)p β +V β (q)=β H (q,p), (70)
∂ (q,p) ∂H(q,p)
Withoutrequiringaprioriknowledgeofthesystemparame- H β =M−1(q)p = ,
∂p β β ∂p
ters,thecontroldesignin(57)offersaunifiedcontrolapproach β
forSE(3)Hamiltoniansystemsthatachievestrajectorytrack- guaranteeing that the equations of motions (30) still hold.
ing, if permissible by the system’s degree of underactuation. Fig.3showsthetrainingandtestingbehaviorofourSO(3)
Thus,ourcontroldesignsolvesProblem2forrigid-bodyrobot Hamiltonian ODE network. Fig. 3a and 3c show that the
systems, such as UGVs, UAVs, and UUVs, with tracking
(cid:2) M(q)−1(cid:3)
entry of the mass inverse and the [B(q)] entry
3,3 3
performance guaranteed by Theorem 1. of the input matrix with scaling factor β = 1.33 are close

IEEETRANSACTIONSONROBOTICS 11
4 5 6 G M O r t o h − u e 1 n r (q d M )[ T 3 − r , u 1 3 ( t ] q h / ) β [i,j]/β 10 5 7 . . . 0 0 5 1 1 0 0 − − 3 1 t t r e a s i t n lo lo s s s s 1 1 1 2 2 5 7 0 . . . . 5 0 5 0 Mv−1(q)[0,0]/β
3 2.5 10.0 Mv−1(q)[1,1]/β
2 0.0 10−5 7.5 M Ot ω h − e 1 r (q e ) n / t β ries
2.5 5.0
1 − 5.0 GroundTruth 10−7 2.5
0 − βV(q) 0.0
− 4 − 2 pendulu 0 mangle 2 4 − 7.5 − 4 − 2 pendulu 0 mangle 2 4 0 2000 ite 4 r 0 a 0 t 0 ions 6000 8000 0.00000.00250.00500.00 t 7 ( 5 s) 0.01000.01250.01500.0175
(a) M−1(q)/β versus φ. (b) βV(q) versus φ. (a) Loss (log scale) (b) M− v 1(q) and M− ω 1(q)
1.0 0.175 GroundTruth 3.0 βV(q) 1.0
0 0 . . 6 8 GroundTruth 0 0 0 . . . 1 1 1 0 2 5 0 5 0 β O D th ω e ( r q β )[ D 3, ω 3 ( ] q)[i,j] − − 3.2 0 0 . . 6 8 β β B B ( ( q q ) ) [ [ 0 1 , , 0 1 ] ]
0.4 β β B B ( ( q q ) ) [ [ 1 2 ] ] 0.075 − 3.4 0.4 β O B th ( e q r ) e [2 n , t 2 ri ] es
0.2 βB(q)[3] 0 0 . . 0 0 2 5 5 0 − 3.6 0.2
0.0 0.000 − 3.8 0.00000.00250.00500.00750.01000.01250.01500.0175 0.0 0.00000.00250.00500.00750.01000.01250.01500.0175
− 4 − 2 pendulu 0 mangle 2 4 − 4 − 2 pendulu 0 mangle 2 4 z t(s)
(c) V(q) (d) B (q)
(c) βB(q) versus φ. (d) βD (q) versus φ. v
ω
3 3 . . 0 5 ϕ ϕ˙ 5 u 10−6 − − 2 2 . . 6 5 0 5 learnedmass,potential,velocity
2.5 4 2.65
2.0 3 − 2.70
1.5 2 − 2.75
1.0 1 10−7 − 2.80
0.5 0 −
0.0 − 1 |det(R)−1| − 2.85
− 0.5 0 2 4 6 8 10 12 14 − 2 0 2 4 6 8 10 12 14 kRR>−Ik − 2.90
t(s) t(s) 0 1 2 3 4 5 0 1 2 3 4 5
t(s) t(s)
(e) Angle φ and velocity φ˙. (f) Control input u.
(e) SO(3) constraints. (f) Total energy.
Fig. 3: Pendulum dynamics estimation using an SO(3) port-
Fig. 4: Evaluation of SE(2) port-Hamiltonian neural ODE
Hamiltonian neural ODE network with scale factor β =1.33.
network on a simulated omnidirectional ground vehicle with
scale factor β =7.1.
to their correct values of 3 and 1, respectively, while the
other entries are close to zero. Fig. 3b indicates a constant
gapbetweenthelearnedandtheground-truthpotentialenergy, where φ is the vehicle’s yaw angle. The vehicle moves on
which can be explained by the relativity of potential energy. a flat ground with potential energy (q) = c, where c is a
dyn W a e m t i e c s s te t d o s t t h a e bil u i n za st t a io b n le of eq th u e ili p b e r n iu d m ulu a m t t b h a e se u d p o w n ar th d e p l o e s a i r t n io e n d i c n o e n r s ti t a an M t, ω an ( d q) h = as 0 g . r 0 o 5 und R -tr > u 0 th .I m ti a s s f s u V M lly v -a ( c q tu ) a = ted I w ∈ it S h 2 ≻ × c 0 o 2 n a tr n o d l
∈
φ = π, with zero velocity. Since the pendulum is a fully- input u = [f x ,f y ,τ φ ], where f x and f y are forces along the
actuatedsystem,theenergy-basedcontrollerin(60)existsand x and y axes of the body frame and τ φ is the yaw torque,
is obtained by removing the position error from the desired generated by the motors.
energy: To collect training data, the vehicle was controlled from
1 1 a random initial point to 9 different desired positions and
H d (q e ,p e )= 2 tr(K R (I − R∗⊤R))+ 2 p⊤ ω M−1(q)p ω . yaw angles using a PID controller, providing 9 one-second
(71) trajectories. The trajectories were used to generate a dataset
The controlled angle φ and angular velocity φ˙ as well as the = t (i) ,q(i) ,ζ(i) ,u(i)) D with N = 5 and D = 432.
control inputs u with gains K R =2I and K d =I are shown D The S { E 0 ( :N 2) p 0 o : r N t-Ha 0 m :N iltonian }i O =1 DE network was formulated,
overtimeinFig.3eand3f.Wecanseethatthecontrollerwas as described in Sec. V-D, by ignoring the z component
able to smoothly drive the pendulum from ϕ = 0 to ϕ = π, of the position p, and the pitch and roll components of
relying only on the learned dynamics. the rotation R. The model was trained for 8000 iterations
without a nominal model, i.e., M−1(q) = 0, M−1(q) = 0,
v0 ω0
B. Omnidirectional Ground Vehicle D (q,p) = 0, D (q,p) = 0, V (q) = 0 and B (q) = 0.
v0 ω0 0 0
In this section, we verify our port-Hamiltonian dynamics We did not consider energy dissipation such as friction in the
learning and control approach on a simulated omnidirectional simulation,andweomittedthedissipationmatrixD θ (q,p)in
ground vehicle, whose states evolve on the SE(2) manifold. the model.
Theground-truthdynamicsofthevehiclecanbeobtainedfrom Fig.4showsthetrainingresultsfortheSE(2)Hamiltonian
(30)bykeepingonlythecomponentsxandyinthepositionp ODE network. Fig. 4b and 4d show that the mass inverse and
andtheyawangleoftherotationmatrix,leadingtoanSO(2) the input gain matrix with scaling factor β = 7.1 are close
rotation matrix: to their correct values: M (q)−1 I,M (q)−1 20 and
v ω
(cid:20) cosφ sinφ (cid:21) B(q) I. Fig. 4c shows a constan ≈ t learned potent ≈ ial energy
R= sinφ − cosφ , (72) as exp ≈ ected.

IEEETRANSACTIONSONROBOTICS 12
1.0
0.5
0.0
−0.5 0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
)m(x
Position/Yaw
2
0
−2
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
)m(y
0.4
0.2
0.0
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
Time(s)
)dar(way
1.0
0.5
0.0
−0.5 0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
)s/m(x
Velocity
0.5
0.0
−0.5
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
)s/m(y
0.0
−0.5
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
Time(s)
)s/dar(ω
learned reference
(a) Tracking performance with a lemniscate trajectory.
1.00
0.75
0.50
0.25
0.00
0.25 − 0.50 − 0.75 − 2.0 1.5 1.0 0.5 0.0 0.5 1.0 1.5 2.0 − − − − y
x
1.5 learned
reference 1.0
0.5
0.0
0.5
− 1.0 − 1.5 − 0.0 0.5 1.0 1.5 2.0 2.5 y
x
trainloss
testloss 25
10−3
20
10−4 15 M M v v − − 1 1 ( ( q q ) ) [ [ 0 1 , , 0 1 ] ]
Mv−1(q)[2,2] 10−5 10 OtherMv−1(q)[i,j]
5
10−6
0
0 100 200 300 400 500 0.00000.00250.00500.00750.01000.01250.01500.0175
iterations t(s)
(a) Loss (log scale) (b) M−1(q)
v
350 0.087090 V(q)
300 0.087085
250 0.087080
200 0.087075
150 0.087070
100 M M ω ω − − 1 1 ( ( q q ) ) [ [ 0 1 , , 0 1 ] ] 0.087065 50 Mω−1(q)[2,2] 0.087060
learned 0 0.00000.00250.00500.00750.01000.0 O 1 th 2 e 5 rM 0. ω− 0 1 1 (q 5 ) 0 [i, 0 j] .0175 0.087055 0.25204 0.25206 0.25208 0.25210 0.25212
reference t(s) z
(c) M−1(q) (d) V(q)
ω
80
1.2
1.0 60 0.8 OtherBv(q) 40 B B ω ω ( ( q q ) ) [ [ 0 1 , , 1 2 ] ] 0.6 Bv(q)[2,0] Bω(q)[2,3]
0.4 20
OtherBω(q)
(b) Tracking lemniscate (left) and piecewise-linear (right) trajectories.
0.2
0
Fig. 5: Trajectories (blue) of omnidirectional ground vehicle 0.0
0.00000.00250.00500.00750.01000.01250.01500.0175 0.00000.00250.00500.00750.01000.01250.01500.0175
tracking desired trajectories (orange) with our learned SE(2) t(s) t(s)
port-Hamiltonian dynamics and IDA-PBC control design. (e) B v (q) (f) B ω (q)
0.44395
10−6 0.44390
0.44385
We verified our energy-based control design in Sec. VI by 0.44380
controlling the ground robot to track horizontal lemniscate 0.44375
10−7
andpiecewise-lineartrajectories.Fig.5bdemonstratesthatthe 0.44370
o co m n n tr i o d l i l r e e r ct a io c n h a ie l v g e r s ou su n c d c v e e s h sf i u cl l e tr c a o j n ec tr t o o l r l y ed tr b a y ck o i u n r g. en T e h r e gy c - o b n a t s r e o d l 0 1 2 t(s) 3 4 | k d R et R (R > ) − − I 1 k 5 | 0 0 . . 4 4 4 4 3 3 6 6 0 5 0 1 2 t 3 4 5
gains were chosen as: K p = 0.72I, K v = 0.8I,K R = 9.1I, (g) SO(3) constraints. (h) Total energy.
K = 3.6. Fig. 5a plots the tracking errors in the position,
ω
Fig. 6: SE(3) port-Hamiltonian neural ODE network on a
yaw angles, linear velocity, and angular velocity.
Crazyflie quadrotor in the PyBullet simulator [81].
C. Crazyflie Quadrotor
In this section, we demonstrate that our SE(3) dynamics ThetrainingandtestresultsareshowninFig.6.Thelearned
learning and control approach can achieve trajectory track- generalized mass and inertia converged to constant diagonal
ing for an underactuated system. We consider a Crazyflie matrices: M−1(q) 27.5I, M−1(q) diag([351,340,181]).
v ≈ ω ≈
quadrotor, shown in Fig. 8a, simulated in the physics-based The input matrix B (q) converged to a constant matrix with
v
(cid:2) (cid:3)
simulatorPyBullet[81].Thecontrolinputu=[f,τ]includes B (q) 1.32 while the other entries were closed to 0,
a thrust f R and a torque vector τ R3 generated con v sisten 2 t ,0 w ≈ ith the fact that the quadrotor thrust only affects
≥0
∈ ∈
by the 4 rotors. The generalized coordinates and velocity are the linear velocity along the z axis in the body-fixed frame.
q=[p⊤ r⊤ r⊤ r⊤]⊤ and ζ =[v⊤ ω⊤]⊤ as before. The input matrix B (q) converged to 76I as the motor
1 2 3 ω
∼
The quadrotor was controlled from a random starting point torques affects all components of the angular velocity ω. The
to 18 different desired poses using a PID controller [81], learned potential energy (q) was linear in the height z,
V
providing 18 2.5-second trajectories. The trajectories were agreeing with the gravitational potential.
used to generate a dataset = t (i) ,q(i) ,ζ(i) ,u(i)) D
D { 0:N 0:N 0:N }i=1 We also verified our energy-based control design in Sec.
with N = 5 and D = 1080. The SE(3) port-Hamiltonian
VI by controlling the quadrotor to track a desired trajectory
ODE network was trained, as described in Sec. V-D, for
based on the learned dynamics model. Given desired position
500 iterations without a nominal model, i.e., M v − 0 1(q) = 0, p∗ and heading ψ∗ (yaw angle), we construct an appropriate
M− ω0 1(q) = 0, D v0 (q,p) = 0, D ω0 (q,p) = 0, V 0 (q) = 0 R∗ andp∗ tobeusedwiththeenergy-basedcontrollerin(60).
and B (q)=0. We did not consider energy dissipation such
0 By expanding the terms in (60) and choosing the control gain
as drag effect in the PyBullet simulator, and we omitted the (cid:20) K 0 (cid:21)
dissipation matrix D θ (q,p) in the model design. K d of the form K d = 0 v K ω , the control input can be

IEEETRANSACTIONSONROBOTICS 13
1.0
0.5
0.0
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
)m(x
Position/Yaw
1
0
−1
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
)m(y
2
1
0
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
)m(z
0.4
0.2
0.0
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
Time(s)
)dar(way
0.4
0.2
0.0
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
)s/m(x
Velocity
0.5
0.0
−0.5
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
)s/m(y
0.5
0.0
−0.5
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
)s/m(z
2.5
0.0
−2.5
0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0
Time(s)
)s/dar(ω
done by projecting the second column of the yaw’s rotation
matrix rψ = [ sinψ,cosψ,0] onto the plane perpendicular
2 − to r∗. We have R∗ =[r∗ r∗ r∗] where:
3 1 2 3
Rτ rψ r∗
r∗ = v ,r∗ = 2 × 3 ,r∗ =r∗ r∗, (76)
3
∥
Rτ
v ∥
1
∥
rψ
2 ×
r∗
3∥
2 3× 1
andωˆ∗ =R∗⊤R˙∗.ThederivativeR˙∗ iscalculatedasfollows:
Rτ˙
r˙∗ = r∗ v r∗, (77)
3 3× Rτ × 3 v
∥ ∥
r˙ψ r∗+rψ r˙∗
r˙∗ = r∗ 2 × 3 2 × 3 r∗, (78)
1 1× rψ r∗ × 1
∥ 2 × 3∥
r˙∗ = r˙∗ r∗+r∗ r˙∗. (79) 2 3× 1 3× 1
Plugging R∗ and ω∗ back in τ , we obtain the complete
ω
control input u in (73).
learned reference
Fig. 8b shows qualitatively that the quadrotor controlled
Fig. 7: Crazyflie quadrotor trajectory (blue) tracking a desired by our energy-based controller achieves successful trajec-
diamond-shaped trajectory (orange) shown in Fig. 8. tory tracking. The control gains were chosen as: K =
p
diag([0.8,0.8,3.9]), K = 0.23I,K = diag([3.6,3.6,6.9]),
v R
K = diag([0.3,0.3,0.6]). Fig. 6 shows quantitatively the
learned reference ω
tracking errors in the position, yaw angles, linear velocity,
and angular velocity. On an Intel i9 3.1 GHz CPU with
3.0 32GB RAM, our controller’s computation time in Python 3.7
2.5
2.0 was about 2.5 ms per control input, including forward passes
z (m ) 1 1 . . 5 0 throughtheneuralnetworks,showingthatitissuitableforfast
0.5 real-time applications.
0.0
−1.5 −1.0 −0 y .5 (m 0 ) .0 0.5 1.0 1.5 1.0 0.5 0 x .0 (m − )
0.5−1.0
D. Comparison to Unstructured Neural ODE Models
(a) Crazyflie simulator (b) Trajectory tracking In this section, we show the benefits of our neural ODE ar-
chitecturebycomparing1)ourstructuredHamiltonianmodel,
Fig.8:TrajectorytrackingexperimentwithaCrazyfliequadro-
2) a black-box model, i.e., the approximated dynamics f is
tor in the PyBullet simulator [81].
representedbyamultilayerperceptronnetwork,and3)anun-
structured Hamiltonian model, i.e., the Hamiltonian function
is represented by a multilayer perceptron network instead of
written explicitly as
usingthestructureinEq.(27),intermsoftrainingconvergence
(cid:20) (cid:21)
τ
u=B†(q) v , (73) rates, satisfaction of energy conservation principle, and Lie
τ
ω group constraints. To verify energy conservation, we rolled
where out the learned dynamics and calculated the Hamiltonian via
∂ (q) (27) along the predicted trajectories for (1) the black-box
τ v = R⊤ V ∂p − pˆ v ω − R⊤K p (p − p∗) model using ground-truth mass and potential energy with the
predictedstates;(2)theunstructuredHamiltonianmodelusing
K (v R⊤p˙∗)+M (R⊤p¨∗ ωˆR⊤p˙∗), (74)
− v − 1 − the output of the multilayer perceptron Hamiltonian network;
3
(cid:88) ∂ (q) and (3) the structured Hamiltonian model using the learned
τ = ˆr V K (ω R⊤R∗ω∗)
ω i ∂r − ω − mass and potential energy networks. We check the SO(3)
i
i=1
constraints by verifying that two quantities detR 1 and
− (pˆ ω ω+pˆ v v) − 1 2 (cid:0) K R R∗⊤R − R⊤R∗K⊤ R (cid:1)∨ ∥ RR⊤ − I ∥ remain small along the predicte | d traject − orie | s.
WefirstuseapendulumasdescribedinSec.VII-Awithout
+M (R⊤R∗ω˙∗ ωˆ R⊤R∗ω∗). (75)
2 − e energy dissipation. The models are trained for 5000 iterations
Note that τ R3 is the desired thrust in the body frame from 512 0.2-second state-control trajectories and rolled out
v
∈
and depends only on the desired position p∗ and the current for a significantly longer horizon of 50 seconds. Fig. 9 plots
pose. The desired thrust is transformed to the world frame the training loss, the phase portraits, the SO(3) constraints
as Rτ . Inspired by [79], the vector Rτ should be along and the total energy (Hamiltonian) of the learned models for
v v
the z axis of the body frame, i.e., the third column r∗ of a pendulum system. As the Hamiltonian structure is imposed
3
the desired rotation matrix R∗. The second column r∗ of the in the neural ODE network architecture, our model is able
2
desired rotation matrix R∗ can be chosen so that it has the to converge faster with lower loss (Fig. 9a and Table I),
desired yaw angle ψ∗ and is perpendicular to r∗. This can be preservesthephaseportraitsforstatepredictions(Fig.9b),and
3

IEEETRANSACTIONSONROBOTICS 14
101 black-box 8 unstructuredHamiltonian 6
structuredHamiltonian 10−1 4 2 10−3 0
2 10−5 −
4
−
6
10−7
0 1000 2000 3000 4000 5000
−
2 1 0 1 2 3 iterations − − pendulumangle
(a) Training loss
yticolevralugna
10 G bl r a o c u k n -b d o t x ruth 105 9 g b r la o c u k n - d bo t x ruth
u st n r s u t c r t u u c r t e u d re H d a H m a i m lto il n t i o a n n ian 103 | k d R et R (R > ) − − I 1 k | - - b b l l a a c c k k - - b b o o x x 8 u st n r s u t c r t u u c r t e u d re H d a H m a i m lto il n t i o a n n ian 101 | k d R et R (R > ) − − I 1 k | - - u u n n s s t t r r u u c c t t u u r r e e d d H H a a m m i i l l t t o o n n i i a a n n 7
10−1 | k d R et R (R > ) − − I 1 k | - - s s t t r r u u c c t t u u r r e e d d H H a a m m i i l l t t o o n n i i a a n n 6
10−3
5
10−5
0 10 20 t(s) 30 40 50 4 0 10 20 t 30 40 50
(b) Phase portraits (c) SO(3) constraints (d) Total energy
Fig. 9: Comparison of different neural network architectures to learn pendulum dynamics: 1) black-box, i.e., the dynamics
function f is represented by a multilayer perceptron network; 2) unstructured Hamiltonian, i.e., the Hamiltonian function is
represented by a multilayer perceptron network instead of the sum of kinetic and potential energy as shown in Eq. (27); 3)
structured Hamiltonian, i.e., the Hamiltonian function has the form of Eq. (27). Initialized at ϕ=π/2, the learned pendulum
dynamicsarerolledout,showingthatourapproachwithstructuredHamiltonianpreservesthephaseportraits,SO(3)constraints,
and the conservation of energy better than the other models.
105 groundtruth unstructuredHamiltonian
structuredHamiltonian black-box
103
10−3 101 | det(R) − 1 | -black-box 1.2
10−4 1 1 0 0 − − 3 1 k | k | d d R R e e t t R R ( ( R R > > ) ) − − − − I I 1 1 k k | | - - - - b u u s l n t n a r s c s u t t k r c r u - t u b u c c o t r t u e x u d r r e e d H d a H H m a a i m m lt i o i l l t n t o i o a n n n i i a a n n 101 b u st l n r a s u c t c k r t u - u b c r o t e u x d re H d a H m a i m lto il n t i o a n n ian 0 0 1 . . . 6 8 0 z(m)
10−5
0
b u st l n r a s u c t c k r
1
t u - u b
0
c r o t
0
e u x d re H d a H m a i m lt
2
o il n
0
t i
i
o
0
a
t
n n
e
ia
r
n
ation 3 s 00 400 500
1 1 0 0 − − 7 5
0 1
k
2
RR
t
>
(s
−
)
I k
3
-structuredH
4
amiltonian
5
100
0 1 2 t 3 4 5
−1.4 −1.6
−x 1 ( . m 8 )−2.0 −2.2 −2.42.0 1.8 1.6y(
1
m
.4) 1.2 1.0 0.4
(a) Training loss (b) SO(3) constraints (c) Total energy (d) Predicted trajectories
Fig. 10: Comparison of different neural network architectures to learn quadrotor dynamics: 1) black-box, i.e., the dynamics
function f is represented by a multilayer perceptron network; 2) unstructured Hamiltonian, i.e., the Hamiltonian function is
represented by a multilayer perceptron network instead of the sum of kinetic and potential energy as shown in Eq. (27); 3)
structured Hamiltonian, i.e., the Hamiltonian function has the form of Eq. (27). Initialized at a random pose and twist, the
learnedquadrotordynamicsarerolledout,showingthatourapproachwithstructuredHamiltonianpreservesSO(3)constraints
and the conservation of energy better than the other models, and provides better state predictions.
TABLE I: Comparison of different neural network architec-
achievesthelowestanglepredictionerrorininTableI.Fig.9c
tures for pendulum and quadrotor dynamics learning.
and Table I show that the SO(3) constraints are satisfied by
our structured and unstructured Hamiltonian models as their Metrics Platform Black-box Unstructured Structured
values of detR 1 and RR⊤ I remain small along Hamiltonian Hamiltonian
| − | ∥ − ∥ Trainingloss Pendulum 0.037 6.3×10−5 2.3×10−7
a 50-second trajectory rollout initialized at ϕ = π/2. The ∥det(R)−1∥(avg.) Pendulum 1888752 1.4×10−3 1.4×10−3
constantHamiltonianinFig.9dofourstructuredHamiltonian ∥RR⊤−I∥(avg.) Pendulum 267971.6 2.1×10−3 2.1×10−3
Totalenergy(std.) Pendulum 13557.1 0.163 0.003
with lowest standard derivation value in Table I verifies that
Predictionerror(avg.) Pendulum 1.02(rad) 0.08(rad) 0.008(rad)
our model obeys the energy conservation law with high Trainingloss Quadrotor 2.2×10−3 6.4×10−4 3.92×10−6
∥det(R)−1∥(avg.) Pendulum 3741 2.9×10−6 2.6×10−7
precision, given no control input and no energy dissipation.
∥RR⊤−I∥(avg.) Quadrotor 29336.7 7.6×10−6 1.3×10−6
The Hamiltonian of the black-box model increases along the Totalenergy(std.) Quadrotor 18.1 0.074 1.64×10−6
Predictionerror(avg.) Quadrotor 0.49(m) 0.46(m) 0.02(m)
trajectory while that of the unstructured Hamiltonian model
fluctuates and slightly decreases over time.
We also tested the models using the simulated Crazyflie a constant total energy along the predicted trajectory, i.e.,
quadtoror with the same dataset of 18 trajectories as lowest standard derivation value in Table I, from our struc-
D
described in Sec. VII-C. The SE(3) port-Hamiltonian ODE turedHamiltonianmodelwithoutcontrolinputanddissipation
network was trained, as described in Sec. V-D, for 500 networks, verifying that the learned model obeys the law of
iterations. Our structured Hamiltonian model converges faster energyconservation.Fig.10dandthepredictionerrorinTable
with significantly lower loss as seen in Fig. 10a and in Table I show that our structured Hamiltonian model provides better
I. We verified that the predicted orientation trajectories from trajectory predictions compared to the other methods.
our learned models satisfy the SO(3) constraints. Fig. 10b
and Table I show two near-zero quantities detR 1 and
RR⊤ I ,obtainedbyrollingout ourlearn | eddyna − mic | sfor E. Real Quadrotor Experiments
∥ − ∥
5 seconds, while the learned black-box model significantly Inthissection,weverifyourapproachusingarealquadrotor
violatestheconstraintsafteraveryshorttime.Fig.10cshows robot, equipped with an onboard i7 Intel NUC computer and

IEEETRANSACTIONSONROBOTICS 15
(a) RaspberryPi drone (b) Intel NUC drone (c) Intel NUC drone with payload
Fig. 11: Quadrotor robots used in the experiments: (a) RaspberryPi quadrotor whose mass and inertia matrix serve as nominal
values for our learning framework, (b) Intel NUC quadrotor with a different frame, and (c) Intel NUC quadrotor carrying a
coffee can as payload.
learned reference nominal learned reference nominal learned reference nominal
2.5
4
2.0
3.5
3z 1.5
3.0
(
m) (m
)(
m)1.0
2.5 z 2 z0.5
2.0 1 0.0
0.5
1.5 −
1.0 x 0. ( 5 m) 0.0 − 0.5 − 1.0 1.0 0.5 0. y 0 (m − ) 0.5− 1.0 2 x 1 (m) 0 − 1 − 2 2 1 y 0 (m) − 1 − 2 3 2 y(m 1 ) 0 − 1 − 2 − 3 − 2− 1 0 x(m 1 ) 2 3
(a) Vertical circle (b) Vertical lemniscate (c) Piecewise linear
Fig. 12: Trajectory tracking with real quadrotors: (a) vertical circle, (b) vertical lemniscate, (c) piecewise linear trajectory.
TABLEII:Positiontrackingerrorsusingnominalandlearned
expose the normalized thrust and torque being sent to the
quadrotor models with and without payload.
motors. The firmware’s normalization of thrust and torque
Model Train Test Circle Lemniscate Piecewise- is unknown and, in fact, is learned from data via the input
with with linear gain matrix B(q). We collected 12 state-control trajectories
payload payload
by flying the quadrotor from a starting pose to 12 different
Nominal - No 0.26(m) 0.52(m) 0.62(m)
poses using a PID controller provided by the PX4 flight
Learned No No 0.13(m) 0.14(m) 0.22(m)
Learned No Yes 0.20(m) 0.40(m) 0.30(m) controller [82]. The trajectories were used to generate a
Learned Yes Yes 0.13(m) 0.12(m) 0.21(m) dataset = t (i) ,q(i) ,ζ(i) ,u(i)) D with N = 1 and
D { 0:N 0:N 0:N }i=1
D = 10000. We trained our model as described in Sec. V-D
for 5000 steps.
a PX4 flight controller (see Fig. 11b). The quadrotor’s pose
The trained model was used with the control policy in Sec.
and twist were provided by a motion capture system.
VII-Ctotrackdifferenttrajectories:averticlecircle,avertical
1) Learning quadrotor dynamics after upgrade: We con-
lemniscate,anda3Dpiecewise-lineartrajectories.Fig.12and
sider a scenario in which the quadrotor is upgraded with a
13showthatweachievebettertrackingperformanceusingour
new frame and a new onboard computer, leading to changes
learned dynamics model and energy-based control compared
in the robot dynamics that we aim to learn from data. The
tothenominalmodelandthegeometriccontrollerin[79].The
nominal model was obtained from a computer-aided design
trackingerrorsofourcontrollerwithalearnedmodelimprove
(CAD) model of another much lighter-weight Raspberry Pi
by 2 4 times compared to those of geometric control based
quadrotor with a Raspberry Pi computer and an F450 frame −
on the nominal model, as shown in Table II.
(Fig. 11a), which is less accurate and far from the unknown
ground-truth model of our upgraded quadrotors. Specifically, 2) Learning quadrotor dynamics with extra payload: In
the nominal mass and inertia matrix are M = 1.3I and this section, we demonstrate that after our dynamics model
v0
M =diag([0.12,0.12,0.2]), respectively, for the upgraded is trained, if there is a change in the quadrotor dynamics,
ω0
quadrotor in Fig. 11b. The other nominal matrices were set e.g., an extra payload is added, we are able to update the
to zero: D (q,p) = 0, D (q,p) = 0, V (q) = 0 dynamics quickly starting from the previously trained model.
v0 ω0 0
and B (q) = 0. We modified the PX4 firmware [82] to We attached a coffee can to the quadrotor frame (Fig. 11c)
0

IEEETRANSACTIONSONROBOTICS 16
|     | Position/Yaw |     |     |     |     | Velocity |     |     | Position/Yaw |     |     |     | Velocity |
| --- | ------------ | --- | --- | --- | --- | -------- | --- | --- | ------------ | --- | --- | --- | -------- |
|     |              |     |     | 0.2 |     |          |     |     |              |     |     | 0.2 |          |
0.10
| 0.1  |     |     |     | )s/m(x |     |     |     |           |     |     | )s/m(x |     |     |
| ---- | --- | --- | --- | ------ | --- | --- | --- | --------- | --- | --- | ------ | --- | --- |
| )m(x |     |     |     | 0.0    |     |     |     | )m(x 0.05 |     |     |        | 0.0 |     |
0.0
0.00
−0.2
| −0.1 |     |       |       |     |      |          |     | 0 10 | 20  | 30 40 50 60 | −0.2 | 0 10 | 20 30 40 50 60 |
| ---- | --- | ----- | ----- | --- | ---- | -------- | --- | ---- | --- | ----------- | ---- | ---- | -------------- |
| 0 10 | 20  | 30 40 | 50 60 |     | 0 10 | 20 30 40 | 50  | 60   |     |             |      |      |                |
| 1    |     |       |       |     |      |          |     | 2    |     |             |      | 1    |                |
1
| )m(y |     |     |     | )s/m(y |     |     |     | )m(y |     |     | )s/m(y |     |     |
| ---- | --- | --- | --- | ------ | --- | --- | --- | ---- | --- | --- | ------ | --- | --- |
| 0    |     |     |     | 0      |     |     |     | 0    |     |     |        | 0   |     |
|      |     |     |     | −1     |     |     |     |      |     |     |        | −1  |     |
| −1   |     |     |     |        |     |     |     | −2   |     |     |        |     |     |
0 10 20 30 40 50 60 0 10 20 30 40 50 60 0 10 20 30 40 50 60 0 10 20 30 40 50 60
4
|        |     |     |     | 1      |     |     |     |      |     |     |        | 2   |     |
| ------ | --- | --- | --- | ------ | --- | --- | --- | ---- | --- | --- | ------ | --- | --- |
|        |     |     |     | )s/m(z |     |     |     | 3    |     |     | )s/m(z |     |     |
| )m(z 3 |     |     |     | 0      |     |     |     | )m(z |     |     |        |     |     |
2
| 2   |     |     |     | −1  |     |     |     |     |     |     |     | 0   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1
0 10 20 30 40 50 60 50 0 10 20 30 40 50 60 0 10 20 30 40 50 60 50 0 10 20 30 40 50 60
| 0.05     |     |     |     | 25       |     |     |     | 0.05     |     |     |          | 25  |     |
| -------- | --- | --- | --- | -------- | --- | --- | --- | -------- | --- | --- | -------- | --- | --- |
| )dar(way |     |     |     | )s/dar(ω |     |     |     | )dar(way |     |     | )s/dar(ω |     |     |
| 0.00     |     |     |     | 0        |     |     |     |          |     |     |          | 0   |     |
0.00
| −0.05 |     |     |     | −25 |     |     |     |       |     |     | −25 |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
|       |     |     |     | −50 |     |     |     | −0.05 |     |     | −50 |     |     |
0 10 20 30 40 50 60 0 10 20 30 40 50 60 0 10 20 30 40 50 60 0 10 20 30 40 50 60
|     | Time(s)      |         |              |           |         | Time(s)  |     |     | Time(s) |              |            |         | Time(s) |
| --- | ------------ | ------- | ------------ | --------- | ------- | -------- | --- | --- | ------- | ------------ | ---------- | ------- | ------- |
|     |              | learned |              | reference | nominal |          |     |     |         | learned      | reference  | nominal |         |
|     |              |         | (a) Vertical | circle    |         |          |     |     |         | (b) Vertical | lemniscate |         |         |
|     | Position/Yaw |         |              |           |         | Velocity |     |     |         |              |            |         |         |
| 2.5 |              |         |              | 1         |         |          |     |     |         |              |            |         |         |
)s/m(x
)m(x 0.0
0
−2.5
| 0.0 2.5 | 5.0 7.5 10.0 | 12.5 15.0 | 17.5 20.0 |        | 0.0 2.5 | 5.0 7.5 10.0 12.5 | 15.0 17.5 | 20.0 |     |     |     |     |     |
| ------- | ------------ | --------- | --------- | ------ | ------- | ----------------- | --------- | ---- | --- | --- | --- | --- | --- |
| 1       |              |           |           | 1      |         |                   |           |      |     |     |     |     |     |
| )m(y    |              |           |           | )s/m(y |         |                   |           |      |     |     |     |     |     |
| 0       |              |           |           | 0      |         |                   |           |      |     |     |     |     |     |
−1
−1
| 0.0 2.5 | 5.0 7.5 10.0 | 12.5 15.0 | 17.5 20.0 |     | 0.0 2.5 | 5.0 7.5 10.0 12.5 | 15.0 17.5 | 20.0 |          |         |     |              |         |
| ------- | ------------ | --------- | --------- | --- | ------- | ----------------- | --------- | ---- | -------- | ------- | --- | ------------ | ------- |
|         |              |           |           |     |         |                   |           | (d)  | Tracking | at t=0s |     | (e) Tracking | at t=3s |
2
1.5
| )m(z |     |     |     | )s/m(z 1 |     |     |     |     |     |     |     |     |     |
| ---- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1.0
0
0.5
| 0.0 2.5 | 5.0 7.5 10.0 | 12.5 15.0 | 17.5 20.0 |     | 0.0 2.5 | 5.0 7.5 10.0 12.5 | 15.0 17.5 | 20.0 |     |     |     |     |     |
| ------- | ------------ | --------- | --------- | --- | ------- | ----------------- | --------- | ---- | --- | --- | --- | --- | --- |
| 0.1     |              |           |           | 50  |         |                   |           |      |     |     |     |     |     |
25
| )dar(way |              |           |                  | )s/dar(ω  |         |                   |           |      |          |         |     |              |          |
| -------- | ------------ | --------- | ---------------- | --------- | ------- | ----------------- | --------- | ---- | -------- | ------- | --- | ------------ | -------- |
| 0.0      |              |           |                  | 0         |         |                   |           |      |          |         |     |              |          |
| −0.1     |              |           |                  | −25       |         |                   |           |      |          |         |     |              |          |
| 0.0 2.5  | 5.0 7.5 10.0 | 12.5 15.0 | 17.5 20.0        | −50       | 0.0 2.5 | 5.0 7.5 10.0 12.5 | 15.0 17.5 | 20.0 |          |         |     |              |          |
|          | Time(s)      |           |                  |           |         | Time(s)           |           |      |          |         |     |              |          |
|          |              | learned   |                  | reference | nominal |                   |           |      |          |         |     |              |          |
|          |              |           |                  |           |         |                   |           | (f)  | Tracking | at t=9s |     | (g) Tracking | at t=12s |
|          |              | (c)       | Piecewise-linear |           |         |                   |           |      |          |         |     |              |          |
Fig. 13: Real quadrotor trajectory using our learned model and controller (blue) and using a nominal model and a geometric
| controller | [79] (green) |     | tracking | a desired | trajectory. |     |     |     |     |     |     |     |     |
| ---------- | ------------ | --- | -------- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
to change the mass and inertia matrix of the robot. We, then, for trajectory tracking based on the learned Lie group port-
collectedanewdatasetbydrivingthequadrotorto12different Hamiltonian dynamics. The learning and control designs are
poses, and trained our dynamics model for only 100 steps, notsystem-specificand,thus,canbeappliedtodifferenttypes
initialized with the trained model in Sec. VII-E1. of robots whose states evolve on Lie group. These techniques
In the presence of the coffee can payload, the tracking have the potential to enable robots to quickly adapt their
performance of the controller with the previously learned models online, in response to changing operational conditions
model degrades as shown in Fig. 14 and 15. Meanwhile, orstructuraldamage,andcontinuetomaintainstabilityduring
after a quick model update, the robot is able to track desired autonomous operation. Future work will focus on extending
trajectories accurately again. Table II shows that our updated our formulation to allow learning multi-rigid-body dynamics,
model improves the tracking errors by 1.5–4 times compared handling contact, and online adaptation to disturbances and
to the previously learned model. structural changes in the dynamics.
IX. APPENDIX
|            |          | VIII. | CONCLUSION |     |         |        |     |                   |     |         |     |     |     |
| ---------- | -------- | ----- | ---------- | --- | ------- | ------ | --- | ----------------- | --- | ------- | --- | --- | --- |
|            |          |       |            |     |         |        |     | A. Implementation |     | Details |     |     |     |
| This paper | proposed |       | a neural   | ODE | network | design | for |                   |     |         |     |     |     |
robot dynamics learning that captures Lie group kinematics, We used fully-connected neural networks whose architec-
e.g. SE(3), and port-Hamiltonian dynamics constraints by ture is shown below. The first number is the input dimension
construction. It also developed a general control approach while the last number is the output dimension. The numbers

IEEETRANSACTIONSONROBOTICS 17
updated reference previouslylearned updated reference previouslylearned updated reference previouslylearned
2.0
4
3.5 1.5
3 z
3.0
z (
m)
2
(m
) z (
m)1.0
2.5 0.5
1
2.0 0.0
1.0 x 0. ( 5 m) 0.0 − 0.5 − 1.0 1.0 0.5 0 y .0 (m) − 0.5 − 1.0 2 x 1 (m) 0 − 1 − 2 2 1 y 0 (m) − 1 y(m 2 ) 1 0 − 1 − 3 − 2 x −(m 1 ) 0 1
(a) Vertical circle (b) Vertical lemniscate (c) Piecewise linear
Fig.14:Quadrotortrajectorytrackingexperimentwithextrapayload:verticalcircle(a),verticallemniscate(b),piecewiselinear
trajectory (c).
0.1
0.0
0 5 10 15 20 25 30
)m(x
Position/Yaw
2
0
−2 0 5 10 15 20 25 30
)m(y
3
2
1
0 5 10 15 20 25 30
)m(z
0.05
0.00
−0.05
0 5 10 15 20 25 30
Time(s)
)dar(way
0.2
0.0
−0.2
0 5 10 15 20 25 30
)s/m(x
Velocity
0
−2
0 5 10 15 20 25 30
)s/m(y
2
0
0 5 10 15 20 25 30
)s/m(z
50
25
0 −25
−50
0 5 10 15 20 25 30
Time(s)
)s/dar(ω
3) Real PX4 quadrotor:
• Input dimension: 12. Action dimension: 4.
• L v (q) only takes the position p R3 as input: ∈
3 - 20 Tanh - 20 Tanh - 20 Tanh - 20 Linear - 6.
• L ω (q) only takes the rotation matrix R R3×3 as
∈
input:
9 - 20 Tanh - 20 Tanh - 20 Tanh - 20 Linear - 6.
• D v;θ (q) only takes the position p R3 as input:
∈
3 - 20 Tanh - 20 Tanh - 20 Tanh - 20 Linear - 6.
• D ω;θ (q) only takes the rotation matrix R R3×3 as
∈
input:
9 - 20 Tanh - 20 Tanh - 20 Tanh - 20 Linear - 6.
• V(q): 12 - 20 Tanh - 20 Tanh - 20 Linear - 1.
• B θ (q): 12 - 20 Tanh - 20 Tanh - 20 Linear - 24.
B. DerivationofHamiltonianDynamicsonSE(3)fromHamil-
updated reference previouslylearned
tonian Dynamics on a Matrix Lie Group
Fig. 15: Tracking a piecewise-linear trajectory with extra
TheHamiltoniandynamicsonSE(3)in(30)canbeobtained
payload using our previously learned and updated models.
from the general matrix Lie group Hamiltonian dynamics in
(18) by computing explicit expressions for the terms ad∗(p)
ξ
and T∗L (η) with η = ∂H(q,p).
in between are the hidden layers’ dimensions and activation To o e bt q ain an explicit exp ∂ r q ession for T∗L (η), we use (6)
e q
functions. The value of ε v and ε ω in (40) is set to 0.01. and the pairing in Def. 1:
1) Pendulum: T∗L (η),ξ = η,T L (ξ) = η,qξ
⟨ e q ⟩ ⟨ e q ⟩ ⟨ ⟩ (80)
• Input dimension: 9. Action dimension: 1. =tr(η⊤qξ)= q⊤η,ξ .
• L(q): ⟨ ⟩
9 - 300 Tanh - 300 Tanh - 300 Tanh - 300 Linear - 6. Thus, T∗ e L q (η) = P g∗(q⊤η), where P g∗ is an orthogonal
projectorong∗ [83,Def.3.60],whichdependsonthespecific
• V θ (q): 9 - 50 Tanh - 50 Tanh - 50 Linear - 1. matrixLiegroup.Forexample,onSE(3)[84]withA R3×3,
• B θ (q): 9 - 300 Tanh - 300 Tanh - 300 Linear - 3. a,b R3, and c R: ∈
2) Pybullet quadrotor: ∈ ∈
(cid:18)(cid:20) A a (cid:21)(cid:19) (cid:20)1(A A⊤) a (cid:21)
• • L In v p ( u q t ) d o im nl e y ns t i a o k n e : s 1 t 2 h . e A po ct s i i o ti n on di p mens R io 3 n a : s 4 i . nput: P g∗ b⊤ c = 2 0 − ⊤ 0 . (81)
3 - 400 Tanh - 400 Tanh - 400 Ta ∈ nh - 400 Linear - 6. To obtain an explicit expression for ad∗(p), we use Def. 9
ξ
• L ω (q) only takes the rotation matrix R R3×3 as and the pairing in Def. 1:
∈
input: ad∗(p),ψ = p,ad (ψ) = p,[ξ,ψ]
9 - 400 Tanh - 400 Tanh - 400 Tanh - 400 Linear - 6. ⟨ ξ ⟩ ⟨ ξ ⟩ ⟨ ⟩ (82)
=tr(p⊤(ξψ ψξ))= [ξ⊤,p],ψ .
• θ (q): 12 - 400 Tanh - 400 Tanh - 400 Linear - 1. − ⟨ ⟩
• V B θ (q): 12 - 400 Tanh - 400 Tanh - 400 Linear - 24. Thus, ad∗ ξ (p)=P g∗([ξ⊤,p]).

IEEETRANSACTIONSONROBOTICS 18
1) Expression for T∗
e
L
q
(η) on SE(3): On SE(3), we have: REFERENCES
(cid:20) (cid:21) (cid:20) (cid:21) (cid:20) (cid:21)
R p ωˆ v η η [1] L.Ljung,“SystemIdentification,”WileyEncyclopediaofElectricaland
q= 0⊤ 1 , ξ = 0⊤ 0 , η = 0⊤ R 0 p , (83) ElectronicsEngineering,1999.
[2] D.Nguyen-TuongandJ.Peters,“ModelLearningforRobotControl:A
and Survey,”Cognitiveprocessing,2011.
[3] M.DeisenrothandC.Rasmussen,“PILCO:AModel-basedandData-
⟨ η,qξ ⟩ = ⟨ η R ,Rωˆ ⟩ + ⟨ η p ,Rv ⟩ efficient Approach to Policy Search,” in International Conference on
1
MachineLearning,2011.
= (R⊤η η⊤R),ωˆ + R⊤η ,v [4] G. Williams, N. Wagener, B. Goldfain, P. Drews, J. Rehg, B. Boots,
⟨2 R− R ⟩ ⟨ p ⟩ and E. Theodorou, “Information Theoretic MPC for Model-based Re-
(cid:28)(cid:20)1(R⊤η η⊤R) R⊤η (cid:21) (cid:20) ωˆ v (cid:21)(cid:29) (84) inforcement Learning,” in IEEE International Conference on Robotics
= 2 R 0⊤ − R 0 p , 0⊤ 0 andAutomation,2017.
[5] M. Raissi, P. Perdikaris, and G. Karniadakis, “Multistep Neural Net-
= T∗L (η),ξ , works for Data-driven Discovery of Nonlinear Dynamical Systems,”
⟨ e q ⟩ arXivpreprintarXiv:1801.01236,2018.
where we used the properties tr(AB) = tr(BA) and [6] K.Chua,R.Calandra,R.McAllister,andS.Levine,“DeepReinforce-
tr(xˆA) = 1tr(xˆ(A A⊤)) of the hat map in the second ment Learning in a Handful of Trials Using Probabilistic Dynamics
2 − Models,”inAdvancesinNeuralInformationProcessingSystems,2018.
equality.
[7] M.LutterandJ.Peters,“CombiningPhysicsandDeepLearningtoLearn
2) Expression for ad∗(p) on SE(3): On se(3), we have: Continuous-timeDynamicsModels,”InternationalJournalofRobotics
ξ
Research,2023.
(cid:20) (cid:21) (cid:20) (cid:21) (cid:20) (cid:21)
aˆ b ωˆ v cˆ d [8] J.Gupta,K.Menda,Z.Manchester,andM.Kochenderfer,“AGeneral
p= 0⊤ 0 , ξ = 0⊤ 0 , ψ = 0⊤ 0 , (85) Framework for Structured Learning of Mechanical Systems,” arXiv
preprintarXiv:1902.08705,2019.
and [9] M.Cranmer,S.Greydanus,S.Hoyer,P.Battaglia,D.Spergel,andS.Ho,
“Lagrangian Neural Networks,” in ICLR Workshop on Integration of
(cid:28)(cid:20) (cid:21) (cid:20) (cid:21)(cid:29)
aˆ b [ωˆ,cˆ] ωˆd+vˆc DeepNeuralModelsandDifferentialEquations,2020.
p,[ξ,ψ] = ,
⟨ ⟩ 0⊤ 0 0 0 [10] S. Greydanus, M. Dzamba, and J. Yosinski, “Hamiltonian Neural Net-
works,”inAdvancesinNeuralInformationProcessingSystems,2019.
= aˆ,[ωˆ,cˆ] + b,ωˆd+vˆc [11] Z.Chen,J.Zhang,M.Arjovsky,andL.Bottou,“SymplecticRecurrent
⟨ ⟩ ⟨ ⟩
Neural Networks,” International Conference on Learning Representa-
= [aˆ,ωˆ],cˆ + b,vˆc + b,ωˆd
⟨ ⟩ ⟨ ⟩ ⟨ ⟩ tions,2020.
= [aˆ,ωˆ],cˆ tr(vb⊤cˆ)+ ωˆ⊤b,d [12] M. Roehrl, T. Runkler, V. Brandtstetter, M. Tokic, and S. Obermayer,
⟨ ⟩− ⟨ ⟩ “Modeling System Dynamics with Physics-Informed Neural Networks
= [aˆ,ωˆ],cˆ + 1 (vb⊤ bv⊤),cˆ + bˆω,d (86) BasedonLagrangianMechanics,”IFAC-PapersOnLine,2020.
⟨ ⟩ ⟨2 − ⟩ ⟨ ⟩ [13] Y.Lu,S.Lin,G.Chen,andJ.Pan,“ModLaNets:LearningGeneralisable
1 DynamicsviaModularityandPhysicalInductiveBias,”inInternational
= [aˆ,ωˆ]+ [bˆ,vˆ],cˆ + bˆω,d ConferenceonMachineLearning,2022.
⟨ 2 ⟩ ⟨ ⟩ [14] C.NearyandU.Topcu,“CompositionalLearningofDynamicalSystem
(cid:28)(cid:20) [aˆ,ωˆ]+ 1[bˆ,vˆ] bˆω (cid:21) (cid:20) cˆ d (cid:21)(cid:29) Models Using portHamiltonian Neural Networks,” in Learning for
= 0⊤ 2 0 , 0⊤ 0 DynamicsandControlConference,2023.
[15] A.Sanchez-Gonzalez,N.Heess,J.T.Springenberg,J.Merel,M.Ried-
= ad∗(p),ψ , miller, R. Hadsell, and P. Battaglia, “Graph Networks as Learnable
⟨ ξ ⟩ PhysicsEnginesforInferenceandControl,”inInternationalConference
where we used the hat map properties xˆ⊤ = xˆ, xˆy= yˆx, onMachineLearning,2018.
and tr(xˆA)= 1tr(xˆ(A A⊤)). − − [16] M.Lutter,C.Ritter,andJ.Peters,“DeepLagrangianNetworks:Using
2 − PhysicsasModelPriorforDeepLearning,”inInternationalConference
3) Consistency Between Hamiltonian Dynamics on a Ma- onLearningRepresentations,2018.
trix Lie Group and on SE(3): Denote the momentum in (17) [17] B.Hall,LieGroups,LieAlgebras,andRepresentations. Springer,2013.
(cid:20) p p (cid:21) (cid:20) p (cid:21) [18] K. Lynch and F. Park, Modern Robotics: Mechanics, Planning, and
asp = ωˆ v andthemomentumin(26)asp = ω , Control. CambridgeUniversityPress,2017.
ξ 0⊤ 0 ζ p v [19] L. Falorsi and P. Forre´, “Neural Ordinary Differential Equations on
where ξ =ζˆ. Let p = ∂L =µˆ. By the chain rule, we have: Manifolds,”arXivpreprintarXiv:2006.06663,2020.
ωˆ ∂ωˆ [20] K. Elamvazhuthi, X. Zhang, S. Oymak, and F. Pasqualetti, “Learning
(cid:28) (cid:29)
∂ ∂ωˆ on Manifolds: Universal Approximations Properties using Geometric
p ωi = ∂ω L = µˆ, ∂ω =2µ i , (87) ControllabilityConditionsforNeuralODEs,”inLearningforDynamics
i i andControlConference,2023.
where ω =[ω ω ω ]⊤, µ=[µ µ µ ]⊤ or [21] A. Lou, D. Lim, I. Katsman, L. Huang, Q. Jiang, S. N. Lim, and
1 2 3 1 2 3 C. De Sa, “Neural Manifold Ordinary Differential Equations,” in Ad-
1 vancesinNeuralInformationProcessingSystems,2020.
p = pˆ (88) [22] Y. Wotte, F. Califano, and S. Stramigioli, “Optimal Potential Shap-
ωˆ 2 ω ing on SE(3) via Neural ODEs on Lie Groups,” arXiv preprint
Therefore, we have: arXiv:2401.15107,2024.
[23] A.I.Lurie,AnalyticalMechanics. SpringerScience&BusinessMedia,
p =
(cid:20)1
2 pˆ ω p v
(cid:21)
,i.e., a= 1 pˆ ,b=p , (89) 2013.
ξ 0⊤ 0 2 ω v [24] D.Holm,GeometricMechanics. WorldScientificPublishingCompany,
2008.
leading to: [25] T. Bertalan, F. Dietrich, I. Mezic´, and I. Kevrekidis, “On Learning
Hamiltonian Systems from Data,” Chaos: An Interdisciplinary Journal
(cid:20)(cid:0)1pˆ ω+ 1pˆ v (cid:1)∧ pˆ ω (cid:21) ofNonlinearScience,2019.
ad∗(p )= 2 ω 2 v v , (90)
ξ ξ 0⊤ 0 [26] M. Finzi, K. A. Wang, and A. Wilson, “Simplifying Hamiltonian and
Lagrangian Neural Networks via Explicit Constraints,” in Advances in
Bypluggingin(89),(90),(84)inthematrixLiegroupHamil- NeuralInformationProcessingSystems,2020.
[27] Y.D.Zhong,B.Dey,andA.Chakraborty,“SymplecticODE-Net:Learn-
toniandynamics(18),weobtaintheHamiltoniandynamicson
ing Hamiltonian Dynamics with Control,” in International Conference
SE(3) in (30). onLearningRepresentations,2019.

| IEEETRANSACTIONSONROBOTICS |     |     |     |     |     |     |     |     |     |     |     |     |     |     | 19  |
| -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[28] J. Willard, X. Jia, S. Xu, M. Steinbach, and V. Kumar, “Integrating [53] A.HavensandG.Chowdhary,“ForcedVariationalIntegratorNetworks
Physics-based Modeling with Machine Learning: A Survey,” arXiv for Prediction and Control of Mechanical Systems,” in Learning for
| preprintarXiv:2003.04919,2020. |     |     |     |     |     |     |     | DynamicsandControl,2021. |     |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- |
[29] A.Maciejewski,“HamiltonianFormalismforEulerParameters,”Celes- [54] V. Duruisseaux, T. P. Duong, M. Leok, and N. Atanasov, “Lie Group
tialMechanics,1985. Forced Variational Integrator Networks for Learning and Control of
[30] R. Shivarama and E. Fahrenthold, “Hamilton’s Equations with Euler Robot Systems,” in Learning for Dynamics and Control Conference,
2023.
| Parameters | for | Rigid Body | Dynamics | Modeling,” |     | Journal | of Dynamic |     |     |     |     |     |     |     |     |
| ---------- | --- | ---------- | -------- | ---------- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
Systems,Measurement,andControl,2004. [55] R. Chen and M. Tao, “Data-driven Prediction of General Hamiltonian
[31] R. Chen, Y. Rubanova, J. Bettencourt, and D. Duvenaud, “Neural Dynamics via Learning Exactly-symplectic Maps,” in International
Ordinary Differential Equations,” in Advances in Neural Information ConferenceonMachineLearning,2021.
ProcessingSystems,2018. [56] O. So, G. Li, E. Theodorou, and M. Tao, “Data-driven Discovery of
[32] T. Duong and N. Atanasov, “Hamiltonian-based Neural ODE Net- Non-NewtonianAstronomyviaLearningNon-EuclideanHamiltonian,”
inICMLMachineLearningandthePhysicalSciencesWorkshop,2022.
| works | on the | SE(3) Manifold |     | For Dynamics | Learning |     | and Control,” |                                                                   |     |     |     |     |     |     |     |
| ----- | ------ | -------------- | --- | ------------ | -------- | --- | ------------- | ----------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|       |        |                |     |              |          |     |               | [57] F.Borrelli,A.Bemporad,andM.Morari,PredictiveControlforLinear |     |     |     |     |     |     |     |
inRobotics:ScienceandSystems,2021.
[33] T. Lee, M. Leok, and N. H. McClamroch, Global Formulations of andHybridSystems. CambridgeUniversityPress,2017.
LagrangianandHamiltonianDynamicsonManifolds. Springer,2017. [58] R. Ortega, M. Spong, F. Go´mez-Estern, and G. Blankenstein, “Stabi-
[34] Y. D. Zhong, B. Dey, and A. Chakraborty, “Dissipative SymODEN: lizationofaClassofUnderactuatedMechanicalSystemsviaIntercon-
|          |             |     |          |      |             |     |              | nection | and | Damping | Assignment,” | IEEE | Transactions |     | on Automatic |
| -------- | ----------- | --- | -------- | ---- | ----------- | --- | ------------ | ------- | --- | ------- | ------------ | ---- | ------------ | --- | ------------ |
| Encoding | Hamiltonian |     | Dynamics | with | Dissipation | and | Control into |         |     |         |              |      |              |     |              |
Control,vol.47,no.8,2002.
| Deep | Learning,” | in ICLR | Workshop | on  | Integration | of  | Deep Neural |             |         |             |     |            |         |         |           |
| ---- | ---------- | ------- | -------- | --- | ----------- | --- | ----------- | ----------- | ------- | ----------- | --- | ---------- | ------- | ------- | --------- |
|      |            |         |          |     |             |     |             | [59] J. A´. | Acosta, | M. Sanchez, | and | A. Ollero, | “Robust | Control | of Under- |
ModelsandDifferentialEquations,2020.
|               |     |         |             |     |         |        |             | actuated | Aerial | Manipulators | via | IDA-PBC,” | in  | IEEE Conference | on  |
| ------------- | --- | ------- | ----------- | --- | ------- | ------ | ----------- | -------- | ------ | ------------ | --- | --------- | --- | --------------- | --- |
| [35] Y. Song, | A.  | Romero, | M. Mu¨ller, | V.  | Koltun, | and D. | Scaramuzza, |          |        |              |     |           |     |                 |     |
“Reaching the Limit in Autonomous Racing: Optimal Control Versus DecisionandControl,2014.
ReinforcementLearning,”ScienceRobotics,2023. [60] O. Cieza and J. Reger, “IDA-PBC for Underactuated Mechanical Sys-
temsinImplicitPort-HamiltonianRepresentation,”inEuropeanControl
[36] T.Salzmann,E.Kaufmann,J.Arrizabalaga,M.Pavone,D.Scaramuzza,
Conference,2019.
andM.Ryll,“Real-timeNeuralMPC:DeepLearningModelPredictive
|         |                |     |           |         |             |      |          | [61] Z.WangandP.Goldsmith,“ModifiedEnergy-balancing-basedControl |     |     |     |     |     |     |     |
| ------- | -------------- | --- | --------- | ------- | ----------- | ---- | -------- | ---------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
| Control | for Quadrotors |     | and Agile | Robotic | Platforms,” | IEEE | Robotics |                                                                  |     |     |     |     |     |     |     |
andAutomationLetters,2023. fortheTrackingProblem,”IETControlTheory&Applications,2008.
[37] D.ScaramuzzaandE.Kaufmann,“LearningAgile,Vision-BasedDrone [62] C. Souza, V. Raffo, and E. Castelan, “Passivity-based Control of a
QuadrotorUAV,”IFACProceedingsVolumes,2014.
Flight:FromSimulationtoReality,”inTheInternationalSymposiumof
|     |     |     |     |     |     |     |     | [63] L. | Furieri, | C. L. Galimberti, |     | M. Zakwan, | and | G. Ferrari-Trecate, |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | -------- | ----------------- | --- | ---------- | --- | ------------------- | --- |
RoboticsResearch,2022.
“DistributedNeuralNetworkControlwithDependabilityGuarantees:A
| [38] A. Loquercio, |     | E. Kaufmann, |            | R. Ranftl, | M. Mu¨ller, | V.         | Koltun, and |                            |     |                 |     |            |             |     |              |
| ------------------ | --- | ------------ | ---------- | ---------- | ----------- | ---------- | ----------- | -------------------------- | --- | --------------- | --- | ---------- | ----------- | --- | ------------ |
|                    |     |              |            |            |             |            |             | Compositional              |     | portHamiltonian |     | Approach,” | in Learning |     | for Dynamics |
| D. Scaramuzza,     |     | “Learning    | High-speed |            | Flight in   | the Wild,” | Science     |                            |     |                 |     |            |             |     |              |
| Robotics,2021.     |     |              |            |            |             |            |             | andControlConference,2022. |     |                 |     |            |             |     |              |
[39] J.Ibarz,J.Tan,C.Finn,M.Kalakrishnan,P.Pastor,andS.Levine,“How [64] C. L. Galimberti, L. Furieri, L. Xu, and G. Ferrari-Trecate, “Hamilto-
|          |      |            |      |               |     |           |            | nian | Deep Neural | Networks | Guaranteeing |     | Nonvanishing |     | Gradients by |
| -------- | ---- | ---------- | ---- | ------------- | --- | --------- | ---------- | ---- | ----------- | -------- | ------------ | --- | ------------ | --- | ------------ |
| to Train | Your | Robot with | Deep | Reinforcement |     | Learning: | Lessons We |      |             |          |              |     |              |     |              |
Design,”IEEETransactionsonAutomaticControl,2023.
HaveLearned,”InternationalJournalofRoboticsResearch,2021.
|                 |         |             |          |             |           |            |                | [65] E. Sebastia´n, |     | T. Duong, | N. Atanasov, | E.          | Montijano,     | and | C. Sagu¨e´s, |
| --------------- | ------- | ----------- | -------- | ----------- | --------- | ---------- | -------------- | ------------------- | --- | --------- | ------------ | ----------- | -------------- | --- | ------------ |
| [40] T. X.      | Nghiem, | J. Drgonˇa, | C.       | Jones, Z.   | Nagy,     | R. Schwan, | B. Dey,        |                     |     |           |              |             |                |     |              |
|                 |         |             |          |             |           |            |                | “LEMURS:            |     | Learning  | Distributed  | Multi-robot | Interactions,” |     | in IEEE      |
| A. Chakrabarty, |         | S. Di       | Cairano, | J. Paulson, | A. Carron | et         | al., “Physics- |                     |     |           |              |             |                |     |              |
InternationalConferenceonRoboticsandAutomation,2023.
| Informed | Machine | Learning | for | Modeling | and | Control | of Dynamical |     |     |     |     |     |     |     |     |
| -------- | ------- | -------- | --- | -------- | --- | ------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Systems,”inAmericanControlConference,2023. [66] J. Marsden and T. Ratiu, Introduction to Mechanics and Symmetry: A
|                  |     |           |              |     |        |        |              | Basic | Exposition | of Classical | Mechanical |     | Systems. | Springer | Science |
| ---------------- | --- | --------- | ------------ | --- | ------ | ------ | ------------ | ----- | ---------- | ------------ | ---------- | --- | -------- | -------- | ------- |
| [41] F. Djeumou, |     | C. Neary, | E. Goubault, | S.  | Putot, | and U. | Topcu, “Neu- |       |            |              |            |     |          |          |         |
&BusinessMedia,2013.
| ral Networks |     | with Physics-informed |     | Architectures |     | and Constraints | for |               |     |            |              |     |            |     |               |
| ------------ | --- | --------------------- | --- | ------------- | --- | --------------- | --- | ------------- | --- | ---------- | ------------ | --- | ---------- | --- | ------------- |
|              |     |                       |     |               |     |                 |     | [67] Y. Zhou, | C.  | Barnes, J. | Lu, J. Yang, | and | H. Li, “On | the | Continuity of |
DynamicalSystemsModeling,”inLearningforDynamicsandControl
RotationRepresentationsinNeuralNetworks,”inIEEEConferenceon
Conference,2022.
ComputerVisionandPatternRecognition(CVPR),2019.
[42] A. Thorpe, C. Neary, F. Djeumou, M. Oishi, and U. Topcu, “Physics- [68] T.Barfoot,StateEstimationforRobotics. CambridgeUniversityPress,
informedKernelEmbeddings:IntegratingPriorSystemKnowledgewith
2017.
Data-drivenControl,”arXivpreprintarXiv:2301.03565,2023.
|     |     |     |     |     |     |     |     | [69] E. G. | Hemingway | and | O. M. O’Reilly, |     | “Perspectives | on  | Euler Angle |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --------- | --- | --------------- | --- | ------------- | --- | ----------- |
[43] L.RuthottoandE.Haber,“DeepNeuralNetworksMotivatedbyPartial
|              |             |     |         |                 |     |         |             | Singularities, |     | Gimbal | Lock, and | the Orthogonality |     | of Applied | Forces |
| ------------ | ----------- | --- | ------- | --------------- | --- | ------- | ----------- | -------------- | --- | ------ | --------- | ----------------- | --- | ---------- | ------ |
| Differential | Equations,” |     | Journal | of Mathematical |     | Imaging | and Vision, |                |     |        |           |                   |     |            |        |
andAppliedMoments,”MultibodySystemDynamics,2018.
2019.
|     |     |     |     |     |     |     |     | [70] M. | Faessler, | A. Franchi, | and D. | Scaramuzza, | “Differential |     | Flatness of |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------- | ----------- | ------ | ----------- | ------------- | --- | ----------- |
[44] R. Wang, R. Walters, and R. Yu, “Incorporating Symmetry into Deep Quadrotor Dynamics Subject to Rotor Drag for Accurate Tracking of
DynamicsModelsforImprovedGeneralization,”inInternationalCon-
High-speedTrajectories,”IEEERoboticsandAutomationLetters,2017.
ferenceonLearningRepresentations,2021.
|                 |     |           |        |         |       |            |          | [71] P.Forni,D.Jeltsema,andG.Lopes,“Port-HamiltonianFormulationof |     |     |     |     |     |     |     |
| --------------- | --- | --------- | ------ | ------- | ----- | ---------- | -------- | ----------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
| [45] M. Lutter, | K.  | Listmann, | and J. | Peters, | “Deep | Lagrangian | Networks |                                                                   |     |     |     |     |     |     |     |
Rigid-bodyAttitudeControl,”IFAC-PapersOnLine,2015.
| for End-to-end |     | Learning | of Energy-based |     | Control | for Under-actuated |     |                                                                       |     |     |     |     |     |     |     |
| -------------- | --- | -------- | --------------- | --- | ------- | ------------------ | --- | --------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|                |     |          |                 |     |         |                    |     | [72] R.Rashad,F.Califano,andS.Stramigioli,“Port-HamiltonianPassivity- |     |     |     |     |     |     |     |
Systems,” in IEEE/RSJ International Conference on Intelligent Robots based Control on SE(3) of a Fully Actuated UAV for Aerial Physical
andSystems,2019. Interaction Near-hovering,” IEEE Robotics and Automation Letters,
| [46] T.Beckers,J.Seidman,P.Perdikaris,andG.Pappas,“GaussianProcess |     |          |          |          |      |         |         | 2019.                                                         |     |     |     |     |     |     |     |
| ------------------------------------------------------------------ | --- | -------- | -------- | -------- | ---- | ------- | ------- | ------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
| portHamiltonian                                                    |     | Systems: | Bayesian | Learning | with | Physics | Prior,” | in                                                            |     |     |     |     |     |     |     |
|                                                                    |     |          |          |          |      |         |         | [73] J.DelmericoandD.Scaramuzza,“ABenchmarkComparisonofMonoc- |     |     |     |     |     |     |     |
IEEEConferenceonDecisionandControl,2022.
|     |     |     |     |     |     |     |     | ular | Visual-Inertial | Odometry | Algorithms |     | for Flying | Robots,” | in IEEE |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --------------- | -------- | ---------- | --- | ---------- | -------- | ------- |
[47] T.Beckers,“Data-drivenBayesianControlofportHamiltonianSystems,” InternationalConferenceonRoboticsandAutomation,2018.
inIEEEConferenceonDecisionandControl,2023. [74] S. A. S. Mohamed, M. Haghbayan, T. Westerlund, J. Heikkonen,
[48] B.LeimkuhlerandS.Reich,SimulatingHamiltonianDynamics. Cam- H.Tenhunen,andJ.Plosila,“ASurveyonOdometryforAutonomous
bridgeUniversityPress,2004. NavigationSystems,”IEEEAccess,2019.
[49] P.Toth,D.J.Rezende,A.Jaegle,S.Racanie`re,A.Botev,andI.Higgins, [75] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan,
| “Hamiltonian |     | Generative | Networks,” | in  | International | Conference |     | on          |     |         |             |            |     |            |          |
| ------------ | --- | ---------- | ---------- | --- | ------------- | ---------- | --- | ----------- | --- | ------- | ----------- | ---------- | --- | ---------- | -------- |
|              |     |            |            |     |               |            |     | T. Killeen, | Z.  | Lin, N. | Gimelshein, | L. Antiga, | A.  | Desmaison, | A. Kopf, |
LearningRepresentations,2019. E.Yang,Z.DeVito,M.Raison,A.Tejani,S.Chilamkurthy,B.Steiner,
[50] J.Mason,C.Allen-Blanchette,N.Zolman,E.Davison,andN.Leonard, L.Fang,J.Bai,andS.Chintala,“PyTorch:AnImperativeStyle,High-
“LearningInterpretableDynamicsfromImagesofaFreelyRotating3D PerformanceDeepLearningLibrary,”inAdvancesinNeuralInformation
RigidBody,”arXivpreprintarXiv:2209.11355,2022. ProcessingSystems32,2019.
[51] A.VanDerSchaftandD.Jeltsema,“Port-HamiltonianSystemsTheory: [76] J. R. Dormand and P. J. Prince, “A family of embedded Runge-Kutta
An Introductory Overview,” Foundations and Trends in Systems and formulae,”JournalofComputationalandAppliedMathematics,1980.
Control,2014. [77] M. Lienen and S. Gu¨nnemann, “torchode: A Parallel ODE Solver for
[52] J. E. Marsden and M. West, “Discrete Mechanics and Variational PyTorch,”inTheSymbiosisofDeepLearningandDifferentialEquations
| Integrators,”ActaNumerica,2001. |     |     |     |     |     |     |     | II,NeurIPS,2022. |     |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |

IEEETRANSACTIONSONROBOTICS 20
[78] A.Iserles,H.Z.Munthe-Kaas,S.P.Nørsett,andA.Zanna,“Lie-group NikolayAtanasov(S’07-M’16-SM’23)isanAsso-
Methods,”ActaNnumerica,2000. ciateProfessorofElectricalandComputerEngineer-
[79] T.Lee,M.Leok,andN.H.McClamroch,“Geometrictrackingcontrol ing at the University of California San Diego, La
of a quadrotor UAV on SE(3),” in IEEE Conference on Decision and Jolla,CA,USA.HeobtainedaB.S.degreeinElec-
Control,2010. trical Engineering from Trinity College, Hartford,
[80] H.K.Khalil,NonlinearSystems. Prenticehall,2002. CT, USA in 2008 and M.S. and Ph.D. degrees in
[81] J. Panerati, H. Zheng, S. Zhou, J. Xu, A. Prorok, and A. Scho¨llig, Electrical and Systems Engineering from the Uni-
“Learning to Fly: a PyBullet Gym Environment to Learn the versity of Pennsylvania, Philadelphia, PA, USA in
Control of Multiple Nano-quadcopters,” https://github.com/utiasDSL/ 2012and2015,respectively.Dr.Atanasov’sresearch
gym-pybullet-drones,2020. focuses on robotics, control theory, and machine
[82] L.Meier,D.Honegger,andM.Pollefeys,“PX4:ANode-basedMulti- learning, applied to active perception problems for
threadedOpenSourceRoboticsFrameworkforDeeplyEmbeddedPlat- autonomous mobile robots. He works on probabilistic models that unify
forms,”inIEEEInternationalConferenceonRoboticsandAutomation, geometricandsemanticinformationinsimultaneouslocalizationandmapping
2015. (SLAM) and on optimal control and reinforcement learning algorithms for
[83] N. Boumal, An introduction to optimization on smooth manifolds. minimizingprobabilisticmodeluncertainty.Dr.Atanasov’sworkhasbeenrec-
Cambridge University Press, 2023. [Online]. Available: https://www. ognizedbytheJosephandRosalineWolfawardforthebestPh.D.dissertation
nicolasboumal.net/book in Electrical and Systems Engineering at the University of Pennsylvania in
[84] P.Arathoon,“CoadjointorbitsofthespecialEuclideangroup,”Master’s 2015,theBestConferencePaperAwardattheIEEEInternationalConference
thesis,UniversityofManchester,2015. on Robotics and Automation (ICRA) in 2017, the NSF CAREER Award in
|     |     |     | 2021, and | the IEEE RAS Early | Academic Career | Award in Robotics | and |
| --- | --- | --- | --------- | ------------------ | --------------- | ----------------- | --- |
Automationin2023.
| Thai Duong | is a PhD candidate | in Electrical and |     |     |     |     |     |
| ---------- | ------------------ | ----------------- | --- | --- | --- | --- | --- |
ComputerEngineeringattheUniversityofCalifor-
nia,SanDiego.HereceivedaB.S.degreeinElec-
tronicsandTelecommunicationsfromHanoiUniver-
sityofScienceandTechnology,Hanoi,Vietnamin
2011andanM.S.degreeinElectricalandComputer
| Engineering | from Oregon State | University, Corval- |     |     |     |     |     |
| ----------- | ----------------- | ------------------- | --- | --- | --- | --- | --- |
lis,OR,in2013.Hisresearchinterestsincludema-
chinelearningwithapplicationstorobotics,mapping
| and active | exploration using | mobile robots, robot |     |     |     |     |     |
| ---------- | ----------------- | -------------------- | --- | --- | --- | --- | --- |
dynamicslearning,planningandcontrol.
| Abdullah      | Altawaitan is a      | Ph.D. student in Elec- |     |     |     |     |     |
| ------------- | -------------------- | ---------------------- | --- | --- | --- | --- | --- |
| trical and    | Computer Engineering | at the University      |     |     |     |     |     |
| of California | San Diego, La        | Jolla, CA, USA. He     |     |     |     |     |     |
receivedboththeB.S.andM.S.degreesinElectrical
EngineeringfromArizonaStateUniversity,Tempe,
AZ,USA.HeisalsoaffiliatedwiththeElectricalEn-
| gineering  | Department, College | of Engineering and |     |     |     |     |     |
| ---------- | ------------------- | ------------------ | --- | --- | --- | --- | --- |
| Petroleum, | Kuwait University,  | Safat, Kuwait. His |     |     |     |     |     |
researchinterestsincludemachinelearning,control
theory,andtheirapplicationstorobotics.
| Jason Stanley | is an undergraduate | student in the |     |     |     |     |     |
| ------------- | ------------------- | -------------- | --- | --- | --- | --- | --- |
ElectricalandComputerEngineeringdepartmentat
theUniversityofCalifornia,SanDiego(UCSD).He
ispursuingamajorinComputerEngineering,andis
planningtocontinueanddoaMastersinElectrical
| Engineering, | also at UCSD. | His research interests |     |     |     |     |     |
| ------------ | ------------- | ---------------------- | --- | --- | --- | --- | --- |
includecontroltheory,machinelearningforrobotics,
andmobilerobots.