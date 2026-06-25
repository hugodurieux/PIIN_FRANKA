Physics-informed Neural Motion Planning on Constraint Manifolds
Ruiqi Ni and Ahmed H. Qureshi
Abstract—ConstrainedMotionPlanning(CMP)aimstofind methodsforplanning.However,thesemethodsrequireexpert
a collision-free path between the given start and goal configu- training data of motion paths on the manifolds for training.
rations on the kinematic constraint manifolds. These problems
Such a dataset is usually gathered by running classical SMP
appear in various scenarios ranging from object manipulation
methods, which leads to significant computational overload
tolegged-robotlocomotion.However,thezero-volumenatureof
manifolds makes the CMP problem challenging, and the state- for training such learning-based approaches.
of-the-art methods still take several seconds to find a path and Recent advancements have led to Physics-Informed Neu-
require a computationally expansive path dataset for imitation ral Networks (PINN) that learn by directly solving Partial
learning. Recently, physics-informed motion planning methods
Differential Equations (PDE) representing a physical system
have emerged that directly solve the Eikonal equation through
[26], [29]. The PINN has also been extended to solving
neuralnetworksformotionplanninganddonotrequireexpert
demonstrations for learning. Inspired by these approaches, we robot motion planning problems under collision avoidance
proposethefirstphysics-informedCMPframeworkthatsolves constraints[22],[23].Thesemethods donotrequiretraining
the Eikonal equation on the constraint manifolds and trains data comprising robot motion paths and, instead, learn to
neural function for CMP without expert data. Our results
solve the Eikonal equation for path planning. Their results
showthattheproposedapproachefficientlysolvesvariousCMP
demonstratethatthesemethodsoutperformpriorapproaches
problems in both simulation and real-world, including object
manipulation under orientation constraints and door opening in terms of computation times, provide high success rates,
with a high-dimensional 6-DOF robot manipulator. In these and scale to high-dimensional settings such as the 6 degree-
complex settings, our method exhibits high success rates and of-freedom (DOF) robot arm. However, these PINN-based
findspathsinsub-seconds,whichismanytimesfasterthanthe
methods for motion planning have yet to be extended to
state-of-the-art CMP methods.
solving CMP problems that induce kinematic constraints in
I. INTRODUCTION addition to collision avoidance.
Inspired by the abovementioned developments, this paper
Constrained Motion Planning (CMP) is a challenging
presents the first PINN-based method called constrained
problem that aims to find a robot motion path between the
NeuralTimeFields(C-NTFields)forsolvingCMPproblems.
given start and goal configurations such that the resulting
Specifically, we extend the Eikonal equation formulation to
path is collision-free and adheres to the given kinematic
incorporate kinematic constraints and demonstrate its appli-
constraints. These kinematic constraints induce a thin mani-
cation to training neural networks without expert training
foldofzerovolumeinsiderobotconfigurationspace,making
motion paths to solve CMP problems. We showcase our
finding a path solution challenging. Surprisingly, kinematic
approach to tackling complex CMP tasks in simulations
constraints appear in a variety of scenarios [6] ranging
and the real world with a 6-DOF robot arm. These tasks
from object manipulation to solving robot locomotion tasks.
involve challenges like handling objects with specific orien-
Despite widespread applications, the existing solutions to
tationsandopeningdoors.Ourresultsshowthatourmethod
solvingCMParelimitedbytheircomputationalinefficiency.
outperforms previous methods by a significant margin in
The existing solutions to CMP broadly comprise opti-
termsofcomputationalspeed,pathquality,andsuccessrates.
mization, sampling, and learning-based methods. The first
Furthermore, we also demonstrate that the data generation
set of methods defines constraints within a differentiable
time for our method is a few minutes compared to the hours
cost function and uses numerical optimization to find a
needed to gather path trajectories for traditional imitation
path [1], [4], [8], [13], [27], [28], making them susceptible
learning-based neural planners.
to local minima. The second category is sampling-based
motion planning (SMP) [2], [5], [9], [11], [12], [15]–[19],
[30], [32] which randomly sample the constraint manifolds
II. RELATEDWORK
and construct a graph for finding a path solution. Due
In this section, we discuss the three major categories
to random sampling, these methods are computationally
of existing CMP methods. The optimization-based methods
expensive and can take significant planning times to find a
[1], [8], [13], [27], [28] incorporate constraints into cost
path. The modern techniques [20], [24], [25] leverage deep
function and leverage numerical optimization for solving
learning to approximate a sampler for generating samples
CMP tasks. However, these approaches weakly satisfy the
on and nearby constraint manifolds for the given start and
kinematicconstraintsandarepronetolocalminima.Arecent
goal configurations. These samples are then given to SMP
approach [4] solves trajectory optimization directly on the
constraintmanifold,buttheirapplicationtohigh-dimensional
The authors are with the Department of Computer Science, Purdue
University,WestLafayette,IN47907,USA{ni117,ahqureshi}@purdue.edu CMP tasks has yet to be investigated.
4202
raM
9
]OR.sc[
1v56750.3042:viXra

Incontrasttooptimization-basedmethods,theSMPmeth- Q∖Q , respectively. The objective of solving the robot
obs
ods [17]–[19] have been widely investigated in a wide range motionplanningproblemistofindapath,σ={q ,⋯,q },in
0 T
of CMP problems. These methods rely on various sampling an obstacle-free configuration space that connects the given
techniques to generate robot configuration samples on the start, q ∈ Q , and goal, q ∈ Q , i.e., σ ⊂ Q .
|     |     |     |     |     |     |     |     |     | 0   | free |     | T   | free |     | free |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | ---- | --- | ---- |
constraint manifold and build a graph or tree for path The CMP problem extends the standard motion planning
planning.Theexistingsamplingtechniqueswithintraditional problem by incorporating additional kinematic constraints.
SMPsrelyonprojection-orcontinuation-basedoperators[3], These constraints induce a thin manifold inside the robot
|     |     |     |     |     |     |     |     |     |     |     |     |     | M ⊂ Q. |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
[11], [15], [16]. The former projects the given sample to the C-space, which is denoted as Like the C-space,
manifold using iterative inverse kinematics-based numerical the manifold also comprises the obstacle, M ⊂Q , and
|     |     |     |     |     |     |     |     |     |     |     |     |     |     | obs | obs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
projection. The latter defines tangent spaces to approximate obstacle-free space, M ⊂ Q . Finally, the objective
|     |     |     |     |     |     |     |     |     |     |     | free |     | free |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- | --- |
the manifold piecewise by forming an atlas. Hence, each of CMP is to find a robot motion path, σ = {q 0 ,⋯,q T },
manifold configuration can be linearly projected along the between the given start, q ∈M , and goal, q ∈M ,
|     |     |     |     |     |     |     |     |     |     |     |     | 0   | free | T   | free |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- |
σ⊂M
tangentspaceandmappedtotheunderlyingmanifold.These such that free .
| sampling | approaches | have | been | incorporated |     | into | various |     |         |          |             |     |     |     |     |
| -------- | ---------- | ---- | ---- | ------------ | --- | ---- | ------- | --- | ------- | -------- | ----------- | --- | --- | --- | --- |
|          |            |      |      |              |     |      |         | B.  | Eikonal | Equation | Formulation |     |     |     |     |
SMPmethods,includingPRMsandRRT-Connect.Themod-
ernSMPmethods,suchasRRT*anditsvariants,areusually The Eikonal equation is a first-order non-linear PDE that
not considered in CMP due to the high computational cost findstheshortestarrivaltimeT(q ,q )fromq toq under
|     |     |     |     |     |     |     |     |     |     |     |     |     | 0 T | 0   | T   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
inducedbytheirrewiringheuristicforoptimalpathplanning. the speed constraint S(q ) as follows:
T
1
Evenwithoutoptimalplanning,thecomputationaltimeswith =∥∇ T(q )∥,
|                                                |     |     |     |     |     |     |     |     |     |     |     | qT  | 0 ,q T |     | (1) |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
| basicRRT-ConnectandPRMsinsolvingCMPproblemsare |     |     |     |     |     |     |     |     |     | S(q | )   |     |        |     |     |
T
still significantly high. where the ∇ T(q ,q ) is the partial derivative of arrival
|           |          |                |     |            |        |             |          |      |              | qT  | 0 T    |           |          |      |          |
| --------- | -------- | -------------- | --- | ---------- | ------ | ----------- | -------- | ---- | ------------ | --- | ------ | --------- | -------- | ---- | -------- |
| Recently, | a        | learning-based |     | method     | called | Constrained |          |      |              |     |        |           |          |      |          |
|           |          |                |     |            |        |             |          | time | with respect |     | to q . | Recently, | NTFields | [22] | extended |
| Motion    | Planning | Networks       | X   | (CoMPNetX) |        | [24],       | [25] has |      |              |     | T      |           |          |      |          |
theEikonalformulationforpathplanningbyformulatingthe
beenintroducedforCMP.Thismethodusesneuralnetworks
|           |          |                |               |         |         |           |          | arrival | time | in the | following | factorized | form:   |     |     |
| --------- | -------- | -------------- | ------------- | ------- | ------- | --------- | -------- | ------- | ---- | ------ | --------- | ---------- | ------- | --- | --- |
| (NN) to   | generate | robot          | configuration |         | samples | on        | and near |         |      |        |           |            |         |     |     |
|           |          |                |               |         |         |           |          |         |      |        |           |            | ∥q −q ∥ |     |     |
| manifolds | for      | the underlying |               | planner | X       | (e.g., X= | RRT-     |         |      |        |           |            | 0 T     |     |     |
|           |          |                |               |         |         |           |          |         |      |        | T(q ,q    | )=         |         |     | (2) |
Connect).TheseNNaretrainedusingimitationlearningwith 0 T τ(q ,q )
0 T
| the dataset | of paths | gathered  | from | executing |     | SMP          | planners |                                           |     |     |     |     |     |      |           |
| ----------- | -------- | --------- | ---- | --------- | --- | ------------ | -------- | ----------------------------------------- | --- | --- | --- | --- | --- | ---- | --------- |
|             |          |           |      |           |     |              |          | wherethefactorizedtimefieldisdenotedbyτ(q |     |     |     |     |     | 0 ,q | T ).Inthe |
| in given    | CMP      | problems. | Once | trained,  | the | NN generates |          |                                           |     |     |     |     |     |      |           |
NTFieldsframework,givenstartandgoalpointsasinput,the
| samples        | in unseen       | but         | similar       | CMP       | problems      | as       | training |            |         |         |           |               |           |                |           |
| -------------- | --------------- | ----------- | ------------- | --------- | ------------- | -------- | -------- | ---------- | ------- | ------- | --------- | ------------- | --------- | -------------- | --------- |
|                |                 |             |               |           |               |          |          | neural     | network | outputs | the       | factorized    | time      | field τ        | between   |
| data. Although |                 | this method | exhibits      |           | fast planning |          | speed at |            |         |         |           |               |           |                |           |
|                |                 |             |               |           |               |          |          | them,      | from    | which   | the speed | is            | predicted | using Equation | 1.        |
| test time,     | the significant |             | computational |           | training      | load     | makes    |            |         |         |           |               |           |                |           |
|                |                 |             |               |           |               |          |          | The        | ground  | truth   | speed     | is calculated | using     | the            | following |
| it less ideal  | as              | the total   | time          | to gather | such          | training | data     |            |         |         |           |               |           |                |           |
|                |                 |             |               |           |               |          |          | predefined |         | model:  |           |               |           |                |           |
surpassesthecomputationalbenefitsatruntime.Meanwhile,
s
learning-based methods are also used for learning constraint S∗(q)= const ×clip(d (p(q),X ),d ,d ) (3)
|     |     |     |     |     |     |     |     |     |     |     |     | c   | obs | min max |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- |
d max
| manifolds | [31] | and for | trajectory | generation |     | on constraint |     |     |     |     |     |     |     |     |     |
| --------- | ---- | ------- | ---------- | ---------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
manifoldsthroughreinforcementlearning[21]andoptimiza- whered and d arethepredefineddistancethresholds
|     |     |     |     |     |     |     |     |     | min |     | max |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tionmethod[14].However,thesemethodsconsiderrelatively for the function d (⋅,⋅) which returns the minimal distance
c
simple scenarios with few obstacles, and their scalability to between robot surface points p(q) at configuration q and
complex settings is yet to be explored. In this paper, we theenvironmentobstaclesX .Therobotsurfacepointsare
obs
|         |                |     |     |         |       |          |      | computed | using | forward |     | kinematics, | and the | s     | is a pre- |
| ------- | -------------- | --- | --- | ------- | ----- | -------- | ---- | -------- | ----- | ------- | --- | ----------- | ------- | ----- | --------- |
| propose | the PINN-based |     | CMP | method, | which | provides | fast |          |       |         |     |             |         | const |           |
computational speed at test time in complex environments defined speed constant. To find the shortest arrival time, the
and does not require expensive training trajectories from robot moves in the high-speed free space region and avoids
classical planners for learning. the low-speed obstacle region. Finally, the NTFields neural
framework,predictingfactorizedarrivaltime,istrainedusing
III. BACKGROUND the isotropic loss function between predicted S and ground
S∗.
In this section, we present our problem definition along truth The NTFields framework and its recent variant
with notations used to describe the proposed approach. solvethemotionplanningproblemundercollisionavoidance
|            |            |     |     |     |     |     |     | constraints. |     | Our proposed |     | framework | in  | this paper | can be |
| ---------- | ---------- | --- | --- | --- | --- | --- | --- | ------------ | --- | ------------ | --- | --------- | --- | ---------- | ------ |
| A. Problem | Definition |     |     |     |     |     |     |              |     |              |     |           |     |            |        |
seenasanapplicationofNTFieldstosolvingCMPproblems
Let the robot configuration space (C-space) and its sur- without expert training path datasets.
|          |             |     |         |     | Rm  |     | Rd, |     |     |     |     |     |     |     |     |
| -------- | ----------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rounding | environment | be  | denoted | as  | Q ∈ | and | X ∈ |     |     |     |     |     |     |     |     |
IV. PROPOSEDMETHOD
respectively.Themanddindicatetherespectivedimensions.
X
The obstacles in the workspace are designated as obs , This section formally presents our PINN framework for
leading to obstacle-free space defined as X =X ∖X . solvingtheCMPproblem.RecallthattheNTFieldsrequired
|     |     |     |     |     |     | free | obs |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ThisworkspaceobstaclesmaptorobotC-space,yieldingob- robot configuration samples, the Eikonal equation formula-
stacle and obstacle-free space denoted as Q obs and Q free = tion,speeddefinition,andstrategiestoleveragethepredicted

time field to compute the gradient steps for path generation. from the obstacles. The two distance functions, (d ,d ),
M c
We discuss these individual components and their adaptions and safety margin, ϵ are combined using the max operator.
to solve CMP problems as follows: The safety margin allows slow-speed maneuvering around
obstacles,whichisusuallypreferredoversharpturnsoffered
A. Manifold Configuration Sampling
by traditional planners. Moreover, in Eq. 4, if the distance
We formulate the kinematic constraints using implicitly of collision surpasses the margin and creates a negative
defined Task Space Regions (TSR). A TSR comprises two term ϵ−d , the max operator will return the distance to
c
SE(3)transformationmatrices,i.e.,T0 andTw,andabound the manifold since it is more important as the configuration
w e
matrix Bw. The T0 transforms from global coordinate to is already far from the obstacle. Furthermore, note that the
w
TSR frame w, also known as the object frame, whereas above distance function differs from the distance function
the Tw provides an end-effector offset in frame w. The used by NTFields, which only uses the distance from the
e
constraint manifold follows the equality constraint by an obstacles to define their speed model. Next, we define our
implicit function f(T0) = 0. Finally, the bound matrix, speed model based on distance function d as follows:
w
Bw, is a 6×2 matrix in TSR’s coordinate frame w, and it d(q,X ,ϵ)2
formalizes the translational and rotational ranges of a TSR. S∗(q)=exp(− obs ), (5)
λϵ2
Theserangesarespecificallychosenfordifferentconstraints. where λ ∈ R+ is a predefined scaling factor. This speed
Inoursetting,weimplicitlydefinethisrangebythedistance modelusesthenegativeexponential,whichsmoothlydecays
of T0 w from the constraint manifolds, i.e., ∥f(T0 w )∥ < δ, as the distance of the robot configuration from the collision-
where δ is a positive threshold, and ∥f(T0 w )∥ represents the free manifold increases. In contrast, NTFields employs the
distancetothemanifoldwhichwillbeusedforthefollowing clip function in their speed model to bind the minimum
sampling and speed definition procedures. and maximum speed based on the robot’s distance from
Furthermore, we directly sample on the TSR f(T0 w ) = 0 the obstacles. Such a function cannot define the constraint
anduseinversekinematicstodeterminerobotconfigurations manifold’s speed model as the objective is to have a higher
on the manifold. Let’s name them manifold configurations. speed on the collision-free manifold and lower everywhere
We also add random perturbations to manifold configura- else, including the non-manifold, obstacle-free space.
tions to gather off-manifold robot configurations and use
C. Eikonal Equation Formulation
the rejection strategy to gather samples within the implicit
range. Using the sampling procedure described above, we The Eikonal equation is ill-posed, i.e., the solution of Eq.
generate a dataset of randomly sampled start and goal robot 1 around low-speed regions is not unique. Since kinematic
configurations, including cases of both on-manifold and off- constraint manifolds are of infinitesimal volume, this ill-
manifold samples. posed nature of the Eikonal equation significantly affects
PINN’s performance. Recently, the progressive NTFields
B. Expert Speed Model for Constraint Manifold
[23]approachintroducedaviscositytermbasedonLaplacian
The expert speed model defines the desired speed value into Eikonal formulation, leading to a semi-linear elliptic
of a given robot configuration, q, based on kinematic and PDE with a unique solution.
1
collision avoidance constraints. The objective is to assign =∥∇ T(q ,q )∥+η∆ T(q ,q ), (6)
a maximum speed value to configuration samples on the S(q T ) qT 0 T qT 0 T
collision-freeconstraintmanifold,M
free
,andalowerspeed whereη∈Risascalingcoefficient.Thechainruleexpansion
value to collision and off-manifold samples. Let a function of the above equation becomes:
d(q,M,X obs ,ϵ) determine the distance of a given configu- S(q T )=
ration, q, from the collision-free constraint manifold, and ϵ
1
be a predefined safety margin around obstacles. We define ¿
this function as: ` ` [τ2(q 0 ,q T )−2τ(q 0 ,q T )(q T −q 0 )⋅
`
η∆ τ(q ,q )+` ∇ τ(q ,q )+∥q −q ∥2×
d(q,X
obs
,ϵ)=max(d
M
(q),ϵ−d
c
(SDF(q),X
obs
)) (4) qT 0 T `(cid:192) qT 0 T 0 T
∥∇ τ(q ,q )∥2]/τ4(q ,q )
In the above formulation, the distance d M measures the
q0 0 T 0 T
(7)
distance of a given configuration to the constraint manifold. We use the above formulation in our setting to overcome
We compute this distance following the f(⋅). Moreover, the the challenges induced by the thin constraint manifold.
f d r u o e n b fi c o n t t e io c n t o h n e d fi c g S u i d g r e a n t t e e io d rm n D i f n i r s e o t s m an t c h t e h e e F m o u i b n n s c i t m t a io c u n l m e s s. ( d S T is D o ta F a n ) c c h e o i f e o v t f e he a d r c g o , i b v w o e t n e . F ∆ ab u q o r T t v h T e e ( r e m q q 0 u o , a r q t e T i , o ) s n im f h o a i r l s a c r a o t m u o n p [ i 2 u q 3 t u a ] e t , i s o w o n e l a u u l ti s s o e i n m ∆ a p q n l T i d fi τ c a ( a i q d t 0 i s o , i n q n T . t ) F ra i i n i n n a s i l t n l e y g a , d o th u o e r f
Thesefunctionsprovideavalueofzero,positive,ornegative PINN to represent constraint manifolds successfully.
depending on whether a given obstacle point is on the robot
D. Neural Network Architecture
surface, outside the robot, or inside the robot, respectively.
Furthermore, we compute the robot’s SDF at configuration Our neural architecture is similar to progressive NTFields
q using the function SDF. Finally, for these SDFs, the methods[23].Insummary,ourframeworkcanbeformalized
function d returns the minimum distance of the robot as follows:
c

τ(q ,q )=g(γ(F(q ,Z))⊗γ(F(q ,Z))) (8) smallerdatabatchforeachtrainingepochisamoreefficient
0 T 0 T
and effective approach.
In the above formulation, F is the Fourier transform-based
environment and C-space encoder. It takes as an input F. Planning Procedure
the start and goal configurations, (q 0 ,q T ), and pre-defined Once our NN modules are trained, we use the planning
environment latent code Z, and outputs the high-frequency pipeline similar to the NTFields method. We begin by
Fourier features: computing the factorized arrival time using NN, τ(q ,q ),
0 T
F(q 0 ,Z)=[cos(2πZTq 0 ),sin(2πZTq 0 )] (9) requiredtotravelfromthestartingpointq 0 tothedestination
F(q T ,Z)=[cos(2πZTq T ),sin(2πZTq T )] pointq T .Next,τ factorizesEq.2and1tocomputeT(q 0 ,q T )
and speed fields S(q ),S(q ). Finally, the start and goal
The output features, (F(q ,Z),F(q ,Z)), are then further 0 T
0 T configurations are bidirectionally and iteratively updated
embedded by a ResNet-style encoder, γ, with skip connec-
toward each other until the terminal limit is reached, i.e.,
tions [10]. Next, a symmetry operator, ⊗, combines the
∥q −q ∥<r to find a path, i.e.,
features using the max and min operators. For instance, 0 T g
some arbitrary inputs, a and b, are combined as a⊗b = q ←q −αS2(q )∇⊥ T(q ,q )
[max(a,b),min(a,b)] and [⋅] is a concetenation operator. q 0 ←q 0 −αS2(q 0 )∇ q ⊥ 0 T( 0 q , T q ) (11)
The advantages of using a symmetric operator are discussed T T T qT 0 T
in [22], which are that it maintains the symmetric property
whereparameterα∈Risapredefinedstepsizeandr
g
∈Ris
of arrival time, i.e., the arrival time from start to goal and predefined the goal region. Besides, in contrast to NTFields,
from goal to start must be the same. Finally, the arrival time where the gradient is only tangential, in the case of CMP,
neuralnetwork,g,takesthesymmetricallycombinedfeatures thegradienthastwocomponents,tangentialandnormal,due
and outputs the τ(q ,q ). This module also leverages the to the curved nature of the manifolds. Therefore, we select
0 T
ResNet-styleneuralnetworkwithskipconnections.Theskip thetangentialcomponent∇⊥ tomovealongthemanifoldfor
connection aids in the smooth gradient flow as highlighted path planning.
in earlier works [22]. Finally, using the auto-differentiation,
V. EVALUATION
we compute the gradient ∇ τ(q ,q ) and the Laplacian
qT 0 T
In this section, we assess the performance of our method
∆ τ(q ,q ) to determine S(q ) and S(q ), as described
qT 0 T 0 T
through three sets of experiments. First, we employ ablation
in Eq. 7.
analysis to illustrate the efficacy of our novel speed model
E. Training Procedure for representing constraint manifolds. Second, we conduct
comparative experiments to evaluate our method against
Given the start and goal configuration samples dataset
several state-of-the-art CMP baselines. Third, we analyze
generated on the manifolds and nearby, we train our above-
the data generation and training times of all learning-based
mentioned neural network framework in an end-to-end man-
methods.Theseexperimentsencompassthefourproblemset-
ner. The NN module takes as an input the environment
tings: (1) A complex Bunny-shaped setting with 2D surface
embedding (Z), the start and goal configurations (q ,q ),
0 T
mesh in 3D space (Fig. 1); (2) A geometrically constrained
and outputs the factorized time τ(q ,q ). This factorized
0 T
manifoldin3Dspacewithandwithoutobstacles(Fig.2);(3)
time is then used to predict the speed using Equation X.
A door-opening task with 6-DOF UR5e robot manipulator
In addition, we also compute the ground truth speed using
(Fig. 3); (4) An object manipulation task under orientation
Equation 7. Finally, the NN can be trained by minimizing
constraints with 6-DOF UR5e robot in intricate, narrow-
thefollowingisotropiclossbetweenthepredictedandground
passage cabinet environments (Fig. 3). For manipulator sce-
speed at the given configurations:
narios, we evaluate both the simulation and the real-world
S∗ (q )/S(q )+S(q )/S∗ (q )+
β(e) 0 0 0 β(e) 0 environments. Furthermore, we perform all experiments on
(10)
S β ∗ (e) (q T )/S(q T )+S(q T )/S β ∗ (e) (q T )−4 a computing system with 3090 RTX GPU, Core i7 CPU,
Furthermore, we use the progressive speed scheduling ap- and 128GB RAM. Finally, the baseline methods and the
proach to train our networks and prevent them from con- evaluation metrics are summarized as follows:
verging to incorrect local minima. The scheduling approach Baselines:
graduallyscales downtheground truthspeedfrom higherto ● HM: The heat method (HM), a diffusion-based method
lower value over the training epoch, e, using the parameter [7] that discretizes the given C-space manifold and
β(e),i.e.,S∗ (q)=(1−β(e))+β(e)S∗(q).Thisapproach solves the Eikonal equation for path planning.
β(e)
hasalreadybeendemonstratedtoovercomethecomplexloss ● CBiRRT: Two trees grow from the start and the goal
landscape of physics-based objective functions and leads to towards each other with the projection-based method
better convergence in low-speed environments such as those that adheres them to the constraint manifold [3].
withthinmanifolds.Additionally,weemployarandombatch ● CoMPNetX: CoMPNetX provides informed samples
buffer strategy to train our PINN method. This contrasts for the underlying planner (e.g., RRT-Connect) to solve
NTFields and P-NTFields, which process the entire dataset CMP. We chose Atlas as their constraint-adherence
for each training epoch, leading to prolonged training times. method due to its best performance in CoMPNetX
However, our findings suggest that selecting a random, experiments [25].

Bunny time(sec) length margin sr(%)
Ours 0.06±0.05 3.68±1.12 0.06±0.03 90 time(sec) length margin sr(%)
P-NTFields 0.05±0.05 3.79±3.29 0.10±0.03 79 w/oobstacle
HM 0.05±0.00 3.82±1.18 0.00±0.00 100 Ours 0.09±0.00 14.32±0.00 0.02±0.00 100
CBiRRT 1.59±0.09 14.70±0.71 0.00±0.00 100
Fig. 1: From left to right images show the paths by our CoMPNetX 0.38±0.04 14.79±1.26 0.00±0.00 100
method (orange), P-NTFields (red), and HM (yellow). The wobstacle
statistical results are based on this environment’s 100 differ- Ours 0.12±0.00 17.32±0.00 0.11±0.00 100
CBiRRT 1.10±0.09 16.66±1.34 0.00±0.00 100
ent starts and goal pairs.
CoMPNetX 0.49±0.12 16.80±1.81 0.00±0.00 100
● P-NTFields: P-NTFields solve the Eikonal equation Fig. 2: Without obstacles (left) and with obstacles (right) in
and do not require expert training data [23]. Although 3D geometric constraint environments. The paths shown are
P-NTFields do not consider manifold constraints, we from our method (orange), CBiRRT (pink), and CoMPNetX
still use its speed model for evaluation purposes. (green). The table shows the statistical results for different
Evaluation Metrics: start and goal pairs in these settings.
● Time: The time (in seconds) for a planner to find a on these manifolds with and without box obstacles. We use
valid path. thesamesettingin[9]andchoose10randomseedsforSMP
● Length: The path distance as the sum of Euclidean methods,whileourmethodisdeterministic.Fig.2showsthe
distance between its waypoints. paths of all presented methods with a table presenting the
● Margin: The distance of waypoints to the constraint statistical comparison. All methods achieved 100% success
manifolds. rate. However, it can be seen that the computational time of
● Success rate: The percentage of valid paths found by our method is about 3× and 10× faster than CoMPNetX and
a planner. CBiRRT, respectively. Besides, our method does not require
expensive data for learning, whereas CoMPNetX is trained
A. Abalation Analysis
using expert demonstration paths via imitation.
This section analyzes our method’s performance on a 2D Door Opening and Object Manipulation:
surface mesh manifold (Bunny). We compare it with P- These two tasks, defined by distinct manifolds, are solved
NTFields as ablation and HM as ground truth. Fig. 1 shows through a 6-DOF UR5e Manipulator in both simulation and
paths on the Bunny mesh of all methods, with the table real-worldsettings.Thedoor-openingtaskrequiresarobotto
providing their statistical comparison. From the paths in openthedoorfromthecurrentpositiontotheopenposition.
Fig. 1, our method gets similar results to HM. However, On the other hand, the object manipulation task imposes
P-NTFields penetrates the manifold. orientationconstraintsandrequirestherobottomaintainthe
Furthermore, from the table in Fig. 1, it can be seen that object upright, i.e., without tilting, while moving it from a
our method exhibits similar performance as ground truth given start to the goal. We chose a challenging cabinet with
method HM and has a higher success rate and lower margin narrow passages as our environment for these two tasks,
to the manifold than P-NTField. This validates that our which imposes significant motion planning challenges in
speedmodeldesignissuitableforconstraintmotionplanning terms of collision avoidance and manifold constraints.
comparedtothespeedmodeldefinitioninP-NTFields,which Table I compares our method, RRT-Connect, and CoMP-
only applies to collision-avoidance constraints. Although NetX in the above-mentioned scenarios. For the object
HM works well for surface mesh examples, it requires manipulation task, all methods have similar success rates
discretization of the C-spaces and thus cannot generalize to and path lengths. However, our method is about 48× faster
higherdimensionalrobotsettings.Therefore,weexcludeHM than CBiRRT and 15× faster than CoMPNetX in terms of
and P-NTFields in the remainder experiment analysis. computational times. For the door-opening task, since the
constraint is relatively simple, all methods achieve similar
B. Comparison Analysis
results. Although our method exhibits a slight margin from
This section compares our method and other baselines on the constraint manifold while others are strictly zero, this is
2D geometric constraint manifold in 3D space and 6-DOF because we do not use a hard constraint adherence approach
manipulator environments. on top of our framework. In contrast, other baselines, i.e.,
GeometricConstraintsin3DSpace:Ourgeometriccon- CoMPNextandCBiRRT,useanatlasandprojectionoperator
straintssettingincludesthree2Dmanifoldsin3Dspacefrom thatgeneratessamplesonthemanifold.Insummary,itcanbe
[9]. These manifolds are defined by parametric functions seenthatourmethodoutperformsbothtraditionalandimita-
withparaboloidandcylindershapes.Weevaluateallmethods tion learning-based methods on complex, high-dimensional

Start Intermediate Goal
rood
nepo
puc
evom
Fig. 3: Two different real-world manipulator cases: the first row shows the door opening task, whereas the second shows
the manipulator moving an object from the cabinet’s top shelf to the lower shelf by crossing two relatively thin obstacles.
time(sec) length margin sr(%) GenerationTime Bunny Geometric Manipulator
movecup Ours 3s 3s 600s
Ours 0.14±0.11 2.32±1.21 0.04±0.03 92 P-NTFields 3s - -
CBiRRT 6.77±6.40 2.44±1.72 0.00±0.00 92 CoMPNetX - 0.8h 12h
CoMPNetX 2.12±0.92 2.43±1.56 0.00±0.00 94
opendoor TrainingTime Bunny Geometric Manipulator
Ours 0.05±0.01 1.32±0.67 0.05±0.05 100 Ours 2.5h 2.5h 4.5h
CBiRRT 0.06±0.02 1.30±0.62 0.00±0.00 100 P-NTFields 8h - -
CoMPNetX 0.05±0.01 1.29±0.65 0.00±0.00 100 CoMPNetX - 1h 3h
TABLE I: The statistical results show 100 and 30 different TABLE II: Data generation and training times of our ap-
starts and goal pairs for manipulating objects under orienta- proach, P-NTFields, and CoMPNetX in different scenarios.
tion constraints and opening doors, respectively.
NTFieldstakethelongesttimeasitprocesstheentiredataset
scenarios by directly learning to solve the Eikonal equation for each training epoch. In comparison, our method training
without any expert path dataset. timesaremuchlowerthanP-NTFieldsandsomewhatsimilar
Fig. 3 shows our method’s executions in real-world ex- to CoMPNetX due to our efficient mini-batches training
periments. The environment was scanned via the RealSense during each epoch.
sensor. The first row shows the snapshots of opening the
doorofthecabinet.Thiscasetook0.06seconds.Thesecond VI. CONCLUSIONSANDFUTUREWORK
row shows snapshots of moving a cup of cola across cabinet
shelves:themanipulatormovingfromthecabinet’stopshelf This paper presents the first physics-informed neural ma-
andcrossingtworelativelythinobstaclestoanothercornerof nipulation planning framework that finds paths on the kine-
the cabinet. This case took 0.15 seconds. We also provide a matic constraint manifolds. Unlike the imitation learning-
completetaskexecutionvideoofopeningadoorandmoving based method for CMP, which takes expert data, we show
an object under orientation constraints between multiple that our framework does not require expert demonstration
starts and goals in our supplementary material. path data and instead directly learns by solving the Eikonal
equation. This leads to data generation times of a few
C. Data Generation and Training Time Analysis
seconds compared to hours for prior methods. Finally, our
Table II shows the data generation and training times of results also show that the proposed method is about 48×
our method, P-NTFields, and CoMPNetX. Our data genera- and 15× faster than classical and imitation-learning-based
tion time is significantly low, similar to P-NTFields, as we CMP methods in computation times in high-dimensional
onlyneedtocomputerobotsamplesandtheirdistancetothe complexscenarios,includingreal-worldobjectmanipulation.
manifold.Incontrast,CoMPNetXrequiresexperttrajectories Inourfuturework,weaimtoextendourapproachtohandle
from a classical planner and takes several hours in data multimodal constraints, which often appear in legged robot
generation for supervised learning. For the training time, P- locomotion tasks under contact dynamics.

REFERENCES [23] ——,“Progressivelearningforphysics-informedneuralmotionplan-
ning,”arXivpreprintarXiv:2306.00616,2023.
[1] C.G.Atkeson,B.P.W.Babu,N.Banerjee,D.Berenson,C.P.Bove,
[24] A.H.Qureshi,J.Dong,A.Choe,andM.C.Yip,“Neuralmanipulation
X.Cui,M.DeDonato,R.Du,S.Feng,P.Franklin,etal.,“Nofalls,no
planning on constraint manifolds,” IEEE Robotics and Automation
resets:Reliablehumanoidbehaviorinthedarparoboticschallenge,”in Letters,vol.5,no.4,pp.6089–6096,2020.
2015IEEE-RAS15thInternationalConferenceonHumanoidRobots
[25] A.H.Qureshi,J.Dong,A.Baig,andM.C.Yip,“Constrainedmotion
(Humanoids). IEEE,2015,pp.623–630. planningnetworksx,”IEEETransactionsonRobotics,vol.38,no.2,
[2] D. Berenson, S. Srinivasa, and J. Kuffner, “Task space regions: A
pp.868–886,2021.
frameworkforpose-constrainedmanipulationplanning,”TheInterna-
[26] M. Raissi, P. Perdikaris, and G. E. Karniadakis, “Physics-informed
tionalJournalofRoboticsResearch,vol.30,no.12,pp.1435–1460,
neuralnetworks:Adeeplearningframeworkforsolvingforwardand
2011.
inverse problems involving nonlinear partial differential equations,”
[3] D.Berenson,S.S.Srinivasa,D.Ferguson,andJ.J.Kuffner,“Manip- JournalofComputationalphysics,vol.378,pp.686–707,2019.
ulationplanningonconstraintmanifolds,”in2009IEEEinternational
[27] N. Ratliff, M. Zucker, J. A. Bagnell, and S. Srinivasa, “Chomp:
conferenceonroboticsandautomation. IEEE,2009,pp.625–632.
Gradient optimization techniques for efficient motion planning,” in
[4] R. Bonalli, A. Bylard, A. Cauligi, T. Lew, and M. Pavone, “Tra- 2009 IEEE international conference on robotics and automation.
jectory optimization on manifolds: A theoretically-guaranteed em-
IEEE,2009,pp.489–494.
bedded sequential convex programming approach,” arXiv preprint
[28] J.Schulman,Y.Duan,J.Ho,A.Lee,I.Awwal,H.Bradlow,J.Pan,
arXiv:1905.07654,2019.
S.Patil,K.Goldberg,andP.Abbeel,“Motionplanningwithsequential
[5] R.Bordalba,L.Ros,andJ.M.Porta,“Randomizedkinodynamicplan- convexoptimizationandconvexcollisionchecking,”TheInternational
ningforconstrainedsystems,”in2018IEEEinternationalconference
JournalofRoboticsResearch,vol.33,no.9,pp.1251–1270,2014.
onroboticsandautomation(ICRA). IEEE,2018,pp.7079–7086.
[29] J.D.Smith,K.Azizzadenesheli,andZ.E.Ross,“Eikonet:Solvingthe
[6] H.Choset,K.M.Lynch,S.Hutchinson,G.A.Kantor,andW.Burgard, eikonal equation with deep neural networks,” IEEE Transactions on
Principlesofrobotmotion:theory,algorithms,andimplementations.
GeoscienceandRemoteSensing,vol.59,no.12,pp.10685–10696,
MITpress,2005.
2020.
[7] K. Crane, C. Weischedel, and M. Wardetzky, “Geodesics in heat:
[30] M.Stilman,“Taskconstrainedmotionplanninginrobotjointspace,”
A new approach to computing distance based on heat flow,” ACM in2007IEEE/RSJInternationalConferenceonIntelligentRobotsand
TransactionsonGraphics(TOG),vol.32,no.5,pp.1–11,2013.
Systems. IEEE,2007,pp.3074–3081.
[8] A. D. Dragan, N. D. Ratliff, and S. S. Srinivasa, “Manipulation
[31] G. Sutanto, I. R. Ferna´ndez, P. Englert, R. K. Ramachandran, and
planning with goal sets using constrained trajectory optimization,”
G. Sukhatme, “Learning equality constraints for motion planning on
in2011IEEEInternationalConferenceonRoboticsandAutomation.
manifolds,” in Conference on Robot Learning. PMLR, 2021, pp.
IEEE,2011,pp.4582–4588.
2292–2305.
[9] P. Englert, I. M. R. Ferna´ndez, R. K. Ramachandran, and G. S.
[32] Z. Yao and K. Gupta, “Path planning with general end-effector
Sukhatme, “Sampling-based motion planning on sequenced mani-
constraints: Using task space to guide configuration space search,”
folds,”arXivpreprintarXiv:2006.02027,2020.
in2005IEEE/RSJInternationalConferenceonIntelligentRobotsand
[10] K.He,X.Zhang,S.Ren,andJ.Sun,“Deepresiduallearningforimage Systems. IEEE,2005,pp.1875–1880.
recognition,” in Proceedings of the IEEE conference on computer
visionandpatternrecognition,2016,pp.770–778.
[11] L.JailletandJ.M.Porta,“Pathplanningwithloopclosureconstraints
usinganatlas-basedrrt,”inRoboticsResearch:The15thInternational
SymposiumISRR. Springer,2017,pp.345–362.
[12] ——, “Asymptotically-optimal path planning on manifolds,” in
Robotics:ScienceandSystems,vol.8,2013,p.145.
[13] M.Johnson,B.Shrewsbury,S.Bertrand,T.Wu,D.Duran,M.Floyd,
P. Abeles, D. Stephen, N. Mertins, A. Lesman, et al., “Team ihmc’s
lessons learned from the darpa robotics challenge trials,” Journal of
FieldRobotics,vol.32,no.2,pp.192–208,2015.
[14] P.Kicki,P.Liu,D.Tateo,H.Bou-Ammar,K.Walas,P.Skrzypczyn´ski,
andJ.Peters,“Fastkinodynamicplanningontheconstraintmanifold
withdeepneuralnetworks,”arXivpreprintarXiv:2301.04330,2023.
[15] B. Kim, T. T. Um, C. Suh, and F. C. Park, “Tangent bundle rrt:
Arandomizedalgorithmforconstrainedmotionplanning,”Robotica,
vol.34,no.1,pp.202–225,2016.
[16] Z.Kingston,M.Moll,andL.E.Kavraki,“Exploringimplicitspaces
for constrained sampling-based planning,” The International Journal
ofRoboticsResearch,vol.38,no.10-11,pp.1151–1178,2019.
[17] J.J.KuffnerandS.M.LaValle,“Rrt-connect:Anefficientapproachto
single-query path planning,” in Proceedings 2000 ICRA. Millennium
Conference.IEEEInternationalConferenceonRoboticsandAutoma-
tion. Symposia Proceedings (Cat. No. 00CH37065), vol. 2. IEEE,
2000,pp.995–1001.
[18] L. E. K. J.-C. Latombe, “Probabilistic roadmaps for robot path
planning,” Pratical motion planning in robotics: current aproaches
andfuturechallenges,pp.33–53,1998.
[19] S.M.LaValle,“Rapidly-exploringrandomtrees:Anewtoolforpath
planning,” 1998. [Online]. Available: https://api.semanticscholar.org/
CorpusID:14744621
[20] T. S. Lembono, E. Pignat, J. Jankowski, and S. Calinon, “Learning
constraineddistributionsofrobotconfigurationswithgenerativeadver-
sarialnetwork,”IEEERoboticsandAutomationLetters,vol.6,no.2,
pp.4233–4240,2021.
[21] P. Liu, D. Tateo, H. B. Ammar, and J. Peters, “Robot reinforcement
learningontheconstraintmanifold,”inConferenceonRobotLearning.
PMLR,2022,pp.1357–1366.
[22] R.NiandA.H.Qureshi,“NTFields:Neuraltimefieldsforphysics-
informedrobotmotionplanning,”inTheEleventhInternationalCon-
ferenceonLearningRepresentations,2023.