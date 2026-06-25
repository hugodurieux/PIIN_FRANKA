d
e
w
Physics informed machine learning model for inverse
dynamics in robotic manipulators
e
i
WeikunDeng,FabioArdiani,KhanhT.P.Nguyen,MouravdBenoussaad,Kamal
Medjaher
e
LaboratoireGéniedeProduction,LGP,UniversitédeToulouse,INP-ENIT,47Av.d’Azereix,65016,
Tarbes,France.
r
r
e
Abstract
e
Inthefieldofroboticmodeling,identifyingsystemparameterswithlimitedjoint
monitoringdataposeschallengesforbothtraditionalphysics-basedandmachine
learning (ML) methods. Physicps-based methods (PBMs) struggle with modeling
uncertainties, time-variant working conditions, diverse robotic configurations,
andincompletesystemparam eters. MLmethods,suchasneuralnetworks(NNs),
lackphysicalconsistency,tinterpretability,anddemandlargeinformationforef-
fective training. Furothermore, PBMs are highly dependent on the understand-
ing of specific structure of the robotic arm and are difficult to modify once the
model is established. Similarly, ML models, once trained, require retraining to
n
adapt to new data if there is a need to change the model’s target or monitoring
data distribution. Both approaches lack flexibility. The challenges in existing
approaches have prompted the development of a hybrid framework that com-
t
bines the strengths of PBM and ML to overcome their weaknesses. The Equa-
n
tionEmbeddedNeuralNetwork(E2NN)withaninnovativeincorporatedLiquid
mechanism is therefore proposed and verified in this paper. E2NN uses inverse
i
dynamicsequationsasaguidetocreateacustomizedneuralnetworklayersand
r
connections between layers for the robotic manipulators’ inverse dynamics and
pdynamic planning. In addition, the embedded liquid mechanism enables E2NN
real-time adaptation to change inputs and robotic motion equations, enhancing
eflexibility and performance. E2NN outperforms standard deep networks in pre-
dictingtorqueandidentifyingincompleteinversedynamicsmodel‘sparameters
r
P Emailaddress: weikun.deng@enit.fr(WeikunDeng)
PreprintsubmittedtoAppliedSoftComputing June26,2023
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
underlimitedjointmonitoringdataandfrictionconditions,capturingtheunder-
lyingstructureofrobotdynamicsmoreeffectively.
e
Keywords: Physics-informedmachinelearning,Roboticmanipulators,Inverse
dynamics,Equationembeddedneuralnetwork,Liquidmechaniism.
v
1. Introduction e
In the field of robotics, model-based torque-level control offers advantages in
r
terms of accuracy and computation cost compared to speed or position-level
robot control. However, the system characterist ic parameters of the robot must
be accurately identified. Building a controllinrg model for robotic manipulators
has traditionally relied on two primaryephysical modeling methods [1]: kine-
matic and dynamic modeling. Kinematic modeling is an analytical mathemat-
ical relationship established by analyzing the geometry and kinematics of the
e
robotstructure[2],suchastheoptimizationrelationsbetweentheend-effector’s
position and the joint positions by the Vortex Search algorithm [3]. Dynamic
p
modeling is used to relate the motion of robot joints to the required forces and
torques. Dynamic modeling takes the robot’s joint displacement, velocity and
acceleration into account in the modeling process. Therefore, the identification
t
ofthemodelparametersinthesetwomethodsisimportantforthedesignofthe
o
final control laws. The process of parameter identification is iterative, involv-
ing multiple stages, each with its distinct tuning attributes. The stages depend
on the model’snintended application and desired performance outcomes. Some
comprehensive surveys of parameter identification in robotics can be found in
workspublish edbyWu[4]andLe[5].
The physictal formulations of these methods are often described and approxi-
matednby using the Newton-Euler and Lagrange-Euler (LE) equations. Specifi-
cally,numericalvaluesofthesemodels’parametersmustbewellchosenthrough
physicalexperimentationoneachindividualpartoftherobot,bycomputer-aided
i
dresign (CAD), or by identification techniques. Among them, the identification
techniqueisthemostwidelyusedsinceiteliminatestheneedtodisassemblethe
p
robotandismoreaccuratethantheothermethods. Itreliesonstatisticalmatch-
ing of real data sampled from robot trajectories to the mathematical equations
e
[6,7].
These models take the form of parametric representations. Achieving precise
r
parametricrepresentationischallengingduetovariousuncertainties,including
Penvironmental uncertainties, sensor noise, and dynamics uncertainty [8]. Un-
2
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
modeled effects such as friction, flexibility, and sub-excitation of parameters [9]
further complicate the modeling process. The parameters can change dynam-
e
ically during run-time or different robotic configurations, influenced by time-
varying conditions. Traditional physics model-based methods are unable to be
i
flexibletodescribethesevaryingconditionsbecausethemodelisfixedwhenthe
v
configurationandoperationconditionsarefixed. Inthiscontext,ML-baseddata-
drivenmethods,suchasneuralnetworks(NNs),offerthealternativeapproaches
e
fromaphysics-agnosticperspective. Themainadvantageslieintheadaptability
to cope with the robotic model variations in real-time [10]. ML methods focus
r
on fitting the relations and time dependencies between system parameters and
motion data by stacking multiple ML models [11], allowing for the capture of
complex relations and accurate predictions writhout the need for detailed mech-
anism analysis or physics-based inductieon [12] in the human–robot collabora-
tion. Therefore,itiscrucialtoacknowledgetheinherentlimitationsofML.One
noteworthy drawback is the absence of physics consistency and interpretabil-
e
ity within the generated models. Moreover, the training process for ML used in
roboticmanipulatormodelingnecessitatesasubstantialquantityoflabeleddata
p
and computational resources. Over-fitting is another prevalent challenge. It oc-
curswhenthenetworkbecomesexcessivelyspecializedinthetrainingdataand
failstogeneralizeeffectivelytounseendata.
t
Toovercomethelimitationsofthe abovetwoapproaches,thispaperintroduces
o
a novel paradigm called Equation Embedded Neural Network (E2NN). It is a
flexible, robust, and physically consistent framework inspired by the concept of
n
PhysicalInteractionModelingLearning(PIML)[13]. Therestpartsofthispaper
areorganizedasfollows: Anoverviewofexistingmodelidentificationsolutions
basedonahy bridframeworkisprovidedinSection2. Then,theproposedE2NN
structure istpresented in Section 3. In Section 4, the effectiveness of the frame-
worknis validated using both simulation data and real-world scenarios. Finally,
Section 5 concludes the work and discusses potential future research directions
inPiIMLforrobots.
r
p2. Relatedworks
Ahybridframeworkistypicallydefinedasthedevelopmentofasemi-parametric
e
model. For example, the study conducted by [14] employed semi-parametric
models with Rigid Body Dynamics and a kernel function incorporated within
r
an online learning mechanism. This paper proposes a threefold classification
Pof state-of-the-art based on the distinct roles of ML in inverse dynamics (ID):
3
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
Parameter Approximate Substitution (PAS), Parameter Approximate Estimator
(PAE), and Parameter Approximate Matcher (PAM). The proposed taxonomy is
e
elucidatedasfollows:
1. PAS: ML signifies an unknown term in a physical equatiion, thereby con-
tributingtothefinalsystemmodelinahybridML-evquationform.
2. PAE: ML estimates system parameters that facilitate the resolution of ki-
e
neticequationsandvalidatetheadherencetoanalyticallaws.
3. PAM: ML identifies suitable inverse dynamrics (ID) solutions by match-
ing system models and parameters across the entire workspace, within a

knownselectionscope.
r
Withinthatperspective,Table.1summaerizestherelatedliterature.
Table1:Summaryofhybridmeethodsforroboticmanipulatoridentification.
| Application | Hybridmethod |     | Advantages |     | Futurework | Taxonomy |
| ----------- | ------------ | --- | ---------- | --- | ---------- | -------- |
p
| UR5 robot | Combines | imitation      | Without | re-    | How to        | learn PAS |
| --------- | -------- | -------------- | ------- | ------ | ------------- | --------- |
| manip-    | learning | and reinforce- | quiring | demon- | a generalized |           |

ulators. ment learning (RL). ML strator action controller from
initializedtby
| [15] | is                    |          | solving information, |          | numerous   |     |
| ---- | --------------------- | -------- | -------------------- | -------- | ---------- | --- |
|      | a supeorvised         | learning | learning             | directly | demonstra- |     |
|      | problem               | that     | uses from            | a single | tions?     |     |
|      | the n expert’s        | state    | and demonstration    |          |            |     |
|      | actionpairstolearnthe |          | trajectory.          |          |            |     |
inversedynamics.

Barrett Lagrangian induction Guarantee phys- Only simulate PAS
t
| WAM,                 | semi-parametric |              | for ically    | plausible | articulatedrigid |     |
| -------------------- | --------------- | ------------ | ------------- | --------- | ---------------- | --- |
| Kukan-LWR            | estimating      | robotic      | pa- dynamics. |           | bodies without   |     |
| robot.               | rameters,       | and equation |               |           | contact and      | re- |
| iconsistency[16,17]. |                 |              |               |           | liesonknowing    |     |
r
and observing
the generalized
p
coordinates.
e
r
P
4
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
| A bench-    | Physics-based |           | side     | Improvesdataef- |     |        | Use          | the PAS   |
| ----------- | ------------- | --------- | -------- | --------------- | --- | ------ | ------------ | --------- |
| mark suite  | information   |           | shapes   | ficiencyandgen- |     |        | physics-e    |           |
| of robotics | network       | structure | and      | eralization     |     | of the | informed     |           |
| environ-    | constraints   |           | output   | model.          |     |        | dynamiics    | mod-      |
| ments.      | values        | and       | internal |                 |     |        | elvs         | to design |
|             | states[18].   |           |          |                 |     |        | controllaws. |           |
| Soft pneu-  | Embedding     |           | physical | Enhanced        |     | pree-  | Apply        | PIRNN PAS |
matic actu- models into RNN re- diction accuracy, to more practi-
ators. cursive computations and effectiveness r cal engineering
|     | [19]. |     |     | across |     | diverse | problems | in  |
| --- | ----- | --- | --- | ------ | --- | ------- | -------- | --- |

|     |     |     |     | types | of  | RNNs | softrobotics. |     |
| --- | --- | --- | --- | ----- | --- | ---- | ------------- | --- |
r
|     |     |     |     | and | soft | robotics |     |     |
| --- | --- | --- | --- | --- | ---- | -------- | --- | --- |
pleatforms.
| MICO | Using Generative |     | Ad- | More | data | ef- | Reduce | the re- PAS |
| ---- | ---------------- | --- | --- | ---- | ---- | --- | ------ | ----------- |
and Fetch versarial Networks to ficiency, better dundancy and
e
| roboticma- | compensate | analytical    |     | performance, |     |     | computational |        |
| ---------- | ---------- | ------------- | --- | ------------ | --- | --- | ------------- | ------ |
| nipulator. | models’    | approximation |     | andaccuracy. |     |     | cost.         | Try to |
p
|     | errors[20]. |     |     |     |     |     | adapt | to sparse |
| --- | ----------- | --- | --- | --- | --- | --- | ----- | --------- |
data.
Da Vinci Design each joint’s The identifica- The necessary PAE
surgical NN that recteives input tion method can force infor-
| robot. | measuroements |              | from | be               | improved |      | mation | may       |
| ------ | ------------- | ------------ | ---- | ---------------- | -------- | ---- | ------ | --------- |
|        | all robot     | joints       | and  | with             | more     | data | not    | always    |
|        | outputs       | torque/force |      | setsandtraining. |          |      | be     | available |
n
|     | estimation,    | using       | the       |     |     |     | in a         | surgical |
| --- | -------------- | ----------- | --------- | --- | --- | --- | ------------ | -------- |
|     | identification |             | error for |     |     |     | setting      | so that  |
|     |   training     | supervision |           |     |     |     | the          | method   |
|     | t[21].         |             |           |     |     |     | needs        | further  |
| n   |                |             |           |     |     |     | development. |          |
Dielectric Differentiable model ≤5% simulation Improvecontrol PAE
| elasitomer | combining       | a       | mate-  | error     | compared |         | and        | inference |
| ---------- | --------------- | ------- | ------ | --------- | -------- | ------- | ---------- | --------- |
| ractuators | rial properties |         | neural | to finite |          | element | algorithms |           |
| control.   | network         | for PBM | pa-    | models    | and      | low     | for        | real and  |
p
|     | rameter | estimations   |     | timecost. |     |     | multi-DOF | soft |
| --- | ------- | ------------- | --- | --------- | --- | --- | --------- | ---- |
|     | and     | an analytical |     |           |     |     | robot     |      |
e
|     | dynamics  | model       | for |     |     |     |     |     |
| --- | --------- | ----------- | --- | --- | --- | --- | --- | --- |
|     | responses | calculation |     |     |     |     |     |     |
r [22].
P
5
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
Multi-link The derivatives of the Efficient Enhance PINNs PAE
roboticma- residuals at a finite gradient-based to handlee more
| nipulators. | number               |       | of             | matched | algorithms     | for     | complex         | con- |     |
| ----------- | -------------------- | ----- | -------------- | ------- | -------------- | ------- | --------------- | ---- | --- |
|             | pointsweredesignedas |       |                |         | the underlying |         | trol acitions   | and  |     |
|             | physical             |       | loss functions |         | optimal        | control | invitialvalues. |      |     |
|             | to                   | guide | the            | PINN to | problem.       |         |                 |      |     |
|             | approximate          |       | the            | true    |                |         | e               |      |     |
responses[23].
| KUKA    | Use |       | meta-learning |     | Quickadaptation | r   | Investigate |        | PAE |
| ------- | --- | ----- | ------------- | --- | --------------- | --- | ----------- | ------ | --- |
| robotic | to  | learn | structured,   |     | tochangesindy-  |     | the         | state- |     |

| manipula- | state-dependent |     |     | loss | namics. |     | dependent |     |     |
| --------- | --------------- | --- | --- | ---- | ------- | --- | --------- | --- | --- |
r
| tors. | functions |       | for        | updating |      |     | loss. | Explore |     |
| ----- | --------- | ----- | ---------- | -------- | ---- | --- | ----- | ------- | --- |
|       | the       | model | parameters |          | eits |     |       | perfor- |     |
|       | [24].     |       |            |          |      |     | mance | in more |     |
parameters’
e
estimation.
Simulated Two novel physics- Superior perfor- Extending to PAE
p
| 7-DOF   | informedlossfunctions |     |       |     | mance  | to using | multi-body      |     |     |
| ------- | --------------------- | --- | ----- | --- | ------ | -------- | --------------- | --- | --- |
| robotic | about                 | the | space | ve- | normal | deep     | contact,explore |     |     |
manipula- locity contro l error models, easy to the effect of
| tors. | [25,26]. |     | tdesign. |     |     |     | adaptively |      |     |
| ----- | -------- | --- | -------- | --- | --- | --- | ---------- | ---- | --- |
|       |          | o   |          |     |     |     | tuning     | the  |     |
|       |          |     |          |     |     |     | trade-off  | loss |     |
weight.
n
| Simulated  | Optimizing |     | end      | ef-  | Low        | compu- | Testing       | on      | PAM |
| ---------- | ---------- | --- | -------- | ---- | ---------- | ------ | ------------- | ------- | --- |
| multi-DOF  | fector     |     | position | with | tation     | cost,  | various       | robotic |     |
| roboticma- |   wave     |     | function | and  | acceptable | per-   | manipulators, |         |     |
nipulators.tMonte Carlo method formance on the exploring dif-
| nto |                       | satisfy        | the | Euclid | simulationdata |     | ferent     | fitness |     |
| --- | --------------------- | -------------- | --- | ------ | -------------- | --- | ---------- | ------- | --- |
|     | fitnessthroughthepar- |                |     |        |                |     | functions, | and     |     |
|     | ticle                 | swmanipulators |     |        |                |     | evaluating |         |     |
i
| roptimization |     |            |     | [27, 28] |     |     | its          | practical |     |
| ------------- | --- | ---------- | --- | -------- | --- | --- | ------------ | --------- | --- |
|               | or  | artificial | bee | colony   |     |     | performance. |           |     |
p
[29].
Simulated
e
6 joints
robot
r
P
6
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
Different Artificial Neural Net- Easy to design, Explore the PAM
multi-joint works [30], Multi-layer high precision, flexibilityeofthe
robotic perceptron, Long modeltheuncer- model and the
manipula- Short-Term Memory, tainfactors. identifiicationof
torss, such Gated Recurrent Unit kevy influencing
as ABB [31], Fuzzy NN [32]) parameters
Industrial nonlinearly fits and ein the model,
Robot. matches end-effector and expand its
position/orientation application.
r
parameters to joint
configurations in the
entireworkingspace. r
e
These studies consistently highlight several advantages, such as improved per-
formance, enhanced data efficiencye, increased physical consistency. Specially,
these studies focus on embedding dynamical equations into NN structures [16,
33] and building NNs under phpysical constraints [17], especially in the applica-
tionofsoft-bodiedrobots[19]showthepositiveeffectsincombiningtraditional
incomplete analytical mode ls with ML. However, their vision for future work
necessitatesfurtherexplotrationofthemodels’flexibility,thegeneralmethodol-
ogy employed for embedding physics knowledge in various ML structures, and
o
practical validation, particularly with respect to uncertainties like the different
working conditions. Furthermore, these studies primarily focus on improving
n
controlperformancesthroughML-basednonlineardatafitting,ratherthanfind-
ing fixed patterns. Therefore, the objective of this paper is to provide a flexible
andinterpretablePIMLframeworkforroboticmanipulatormodelingandparam-
t
eter identification. It consists of a physics-informed structure method with the
n
ability in generalizing on new data from unknown working conditions. Hereby
inthevalidationprocess,thisstudywilldemonstratetheeffectivenessofthepro-
i
poseddesignbycomparingtheperformancebeforeandafterusingtheproposed
r
frameworktomodifyanexistingalgorithm.
p
3. Proposedframework
e
Motivated by the research published in [34] which proposes implementing the
flux–tendency relations directly into establishing neural network structure to
r
inherently respect the conservation laws, this research develops the penulti-
Pmate hidden layer and interlayer connections enforcing robot dynamics in the
7
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
proposed equation embedded neural network (E2NN). In addition, for adapting
to the different working modes, a liquid inter-layer connection paradigm is ex-
e
plored. TheproposedframeworkisshowninFig.1.
i
v
e
r
r
e
e
Figure1:ImplementationframeworkforE2NN
p
The implementation process involves building an inverse dynamics model us-
ing analytic derivation first. Next, the neural network’s neurons are designed
based on basic computational functions in the analytical relations incomplete
t
model,suchassineandcosine. Theseneuronsformlayersthatexpresssub-term
transformation relatioons for the inverse dynamics model. Then inter-layer con-
nections are designed based on the relations between sub-terms. Finally, a fully
connected layernrepresents the summation operation relations. Each step of the
computation is implemented through substitution using the neural network. A
detailed descr iption of the proposed framework is shown in the following sec-
tions,espectiallytheinnovativepartsaregiveninthesubsections. 3.1and3.2.
n
3.1. Incompleteanalyticalinversedynamicsmodel
The inverse dynamics model of a 7-DOF robotic manipulator can be written re-
i
grardingitsparametersasshowninEq.(1):
p
τ = W(q,q˙,q¨)β +ρ (1)
ewhereW(q,q˙,q¨) ∈ Rr×nb istheregressioncalculatorobtainedfromevaluating
f (q,q˙,q¨)mtimes,withr = n×minEq.(2). misthenumberofroboticjoints. ρ
i
ristheunmodelledeffects. τ isthetorquevectoroftheroboticmanipulator. β ∈
st
P
8
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
Rnst
isthevectorofthen standardparametersdescribingthemanipulator:
st
|     |     |            |     |    |              |    | e   |     |
| --- | --- | ---------- | --- | --- | ------------ | --- | --- | --- |
|     |     |            |     |     | f (q ,q˙ ,q¨ | )   |     |     |
|     |     |            |     |     | 1 1 1        | 1   |     |     |
|     |     |            |     |    | f (q ,q˙ ,q¨ | )  |     |     |
|     |     |            |     |    | 2 2 2        | 2  |     |     |
|     |     | W(q,q˙,q¨) |     | =   | .            |     | i   | (2) |
|     |     |            |     |    | .            |    |     |     |
|     |     |            |     |    | .            |    |     |     |
v
|     |     |     |     | f   | (q ,q˙ ),q¨ | )   |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | --- | --- |
|     |     |     |     |     | m m m       | m   |     |     |
e
|     |     |     |     | (cid:104) | . (cid:105)T |     |     |     |
| --- | --- | --- | --- | --------- | ------------ | --- | --- | --- |
|     |     |     | β = |           | .            |     |     |     |
|     |     |     |     | βT        | βT .βT       |     |     | (3) |
|     |     |     | st  | 1st       | 2st nst      |     |     |     |
r
y(τ) ∈ Rr isthevectorofjointtorques:

|     |     |     |     |    | r  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
τ
1
|     |     |     |     | eτ |    |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |    | 2  |     |     |     |
|     |     |     |     | τ = | .   |     |     | (4) |
|     |     |     |     |    | .  |     |     |     |
|     |     |     |     |    | .  |     |     |     |
eτ
m
The vectors q, q˙, and q¨ are joipnt positions, velocities, and accelerations respec-
tively. TheyareapproximatedbythefiniteFourierseries[35]inEq.(5).

|       |     | Ni (cid:18) | a     |      | b     |     | (cid:19) |     |
| ----- | --- | ----------- | ----- | ---- | ----- | --- | -------- | --- |
|       |     | (cid:88) t  | l,i   |      | l,i   |     |          |     |
| q (t) | =   |             | sin(ω | lt)− | cos(ω | lt) | +q       |     |
| i     |     |             |       | f    |       | f   | i0       |     |
|       | of  |             | ω l   |      | ω l   |     |          |     |
f
l=1
Ni
(cid:88)
| q˙n(t) | =   | (a  | cos(ω | lt)+b | sin(ω | lt)) |     | (5) |
| ------ | --- | --- | ----- | ----- | ----- | ---- | --- | --- |
| i      |     |     | l     | f     | l f   |      |     |     |
l=1
Ni
 (cid:88)
| q¨(t) | =   | (−a | ω lsin(ω |     | lt)+b ω | lcos(ω | lt)) |     |
| ----- | --- | --- | -------- | --- | ------- | ------ | ---- | --- |
| ti    |     |     | l f      |     | f l f   |        | f    |     |
l=1
n
where ω represents the fundamental pulsation of the Fourier series, and N in-
| f   |     |     |     |     |     |     |     | i   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
dicaitestheorderofthehmanipulatorsonic. Theparametersa andb correspond
|     |     |     |     |     |     |     | l l |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
torthe
amplitudes of the sine and cosine functions, while q denotes the initial
0
p positionaroundwhichthejointoscillates.
Friction working conditions are expressed by ρ, the Coulomb friction model is
introduced from the research published in [36]. Its friction coefficient can vary
e
based on the direction of joint motion. To account for this, a parameter τ is
offj
usedtocombinetheasymmetricalCoulombfrictioncoefficientandotheroffsets
r
P
9
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
causedbysensorsandamplifiers,asshowninEq.(6):
e
|     |     |     | τ   | = f | q˙ +f | sign(q˙ | )+τ |      |     | (6) |
| --- | --- | --- | --- | --- | ----- | ------- | --- | ---- | --- | --- |
|     |     |     | fj  | vj  | j     | cj      | j   | offj |     |     |
where τ represents the joint friction torque, f is the viscouis friction coeffi-
| fj  |     |     |     |     |     |     | vj  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
cient, f is the Coulomb friction coefficient. Therefore, su v bstituting Eq.(5) and
cj
Eq.(6) into Eq.(1), the one joint torque modelis achieved to build informd-NN is
e
showninEq.(7).
| (cid:80) m | (cid:0) |     |     |     |     |     |     | r   |     | (cid:1) |
| ---------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | ------- |
τ = β f w cos(q ),w sin(q ),w sign(q ) ,w q ,w q′ ,w q′′...w q .
| i   | ist i | 1i  | it  | 2i    | it  | 3i        |     | it 4i | it 5i it 6i it | nj it |
| --- | ----- | --- | --- | ----- | --- | --------- | --- | ----- | -------------- | ----- |
| i=1 |       |     |     |       |     |           |     |       |                |       |
|     |       | +β  | f   | q˙ +β |     | f sign(q˙ |     | )+β   | τ              |       |
|     |       |     | m+1 | vj j  | m+2 | cj        | rj  |       | m+3 offj       |       |
(7)
The detailed mathematical expressions feor the overall nonlinear mapping func-
tion f and the coefficients β to β and w to w are to be learned from
| i               |     |     |     | 1   | m+3 |     | 1i  |     | nj  |     |
| --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| monitoringdata. |     |     |     |     | e   |     |     |     |     |     |
3.2. Proposedmethodology
p
TheprocessofMLmodelingistolearnparametersβ toβ . Theseparameters
|     |     |     |     |     |     |     |     | 1   | m+1 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
arecombinedwithdifferent transformations. Additionally,thelearnedrelations
need to be flexible to accommodate t variations in working conditions and adapt
to different input data. To satisfy these requirements, a specific NN structure is
o
designedaccordingtoEq.(7). ThedetailsareshowninFig.2andsubsection.3.2.1.
Thearchitecture’scoreisunderpinnedbytheimplementationofcustomdesign.
n
Within the “Mimetic Nonlinear Transforms Layers”, the foundational physical
relations are simulated for each input to effectively create a symbolic represen-

tation of the physics involved. Subsequent to this transformation, the “Combi-
t
nationLayers”amalgamatethissymbolicrelationintoanoutputthatalignswith
n
the prescribed dynamic formulation. In the “Combination Layers”, the weights,
symbolizingtheparametersoftheroboticmanipulators,aresubjecttoautomated
adjuistmentthroughaniterativelearningprocess.
r
p3.2.1. NNlayerswithembeddeddomainequations
E2NN uses the customer layers to simulate the basic nonlinear transformation
eterms,asshowninFig.4.
r
P
10
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
e
i
v
e
r
r
e
Figure 2: Architecture of the Equation-Embedded Neural Network (E2NN) for one joint. (The
blue components represent the physics-informed parts of the traditional neural network. The
circularnodesrepresentindividualneurons,whiletherectangularnodesdenotecustomlayers.
e
Theinterconnectedcirculargroupwithintheliquidlayersignifiestheirdynamicconnections.In
theLiquidlayers,theconnectionisindeterminateandisthereforerepresentedbythestacking
patternoftheneuronpool.TherelatiponshipbetweenthephysicalequationandtheNNstructure
isgivenbythedarkbluearrow.)
t
q
1
o
n
n
q CustomLayer
(cid:80)b
h (ω q )+b g
2 i i i 1−n
i=1
t
n
q n
n (cid:80)
h ( ω q +b)
u i i
i i=1
r
Figure3:Customlayerstorepresentbasicarithmeticunits.
p
eWhereh representsaseriesofpartiallyknownphysicsnonlinearelementsf in
i
Eq.(7). n isthetypenumberofthebasicitemsinvolved. h consistsofthebasics
b i
rmathematical terms such as cos(q), sin(q), sign(q¨), and linear transformation
relationsofq,q˙,q¨. FortheunknownelementsinEq.(7),E2NNusesthetraditional
P
11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
ML layer h to fit the potential transformation. Thus far, E2NN has performed
u
thepolynomialfittingoftheindependentvariablescontainedinf forEq.(7). In
ei
particular,thebiastermbofthelasthiddenlayercorrespondstoτ .
offj
In the deeper hidden layers, E2NN designs custom layers to simulate the basic
i
mathematicalcombinationsoftheabovebasicelements,asillustratedinFig.4.
v
g e
1
r
g CustomLayer k ( (cid:80)
n
k ω q +b) y
2 iri i 1−n
i=1
e
g e
n
Figure4:Customlayerstoreprpesentanalyticcombinationrelationsforpolynomials
Wherek representsaseriesofknownmathematicalrelationsconsistingofsquares,
i t
radicals,varioustypesofquadraticoperations,etc. n isthetypenumberofthe
k
o
basiccombinationrelationsinvolvedinEq.(7).
3.2.2. NNinterlanyerconnection
To fit a polynomial function of degree n to a set of data points in Eq.(7) , n+1
j
coefficients ar e needed to define the polynomial. These pending coefficients β ,
i
where i rantges from 1 to n , can be represented by the weights and biases of a
j
singlenhidden layer with n neurons. The input of these hidden neurons is re-
j
sponsibleforprovidingthevaluesoff inEq.(7),andtheoutputneuronproduces
thefiinalpredictedtorquevalueτ.
r
3.2.3. Liquidmechanismtoenhancethemodelgeneralizationperformance
p
The structure presented in Fig. 5 incorporates the dynamics equation as a hard
constraint, resulting in a model with strong physical consistency. However, the
e
existingPIMLworkshavefixednodeandconnectivityconfigurationsaftertrain-
ing. Thisrestrictsthemodel’spotentialforadaptingtonovelworkingconditions,
r
particularly in cases where the underlying equations differ across diverse oper-
Patingconditions. Whenitcomestoastraightforwardpredictiontask,traininga
12
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
|     |            | Mimeticnonlinear | Combinatorics |     |     |
| --- | ---------- | ---------------- | ------------- | --- | --- |
|     | Inputlayer | transforms       | bymimesis     |     |     |
e
|     | q¨  | h   | k   |     |     |
| --- | --- | --- | --- | --- | --- |
|     |     | 1   | 1   |     |     |
β
1st i
v
|     | q˙  | h   | k β   | Outputlayer |     |
| --- | --- | --- | ----- | ----------- | --- |
|     |     | 2   | 2 2st |             |     |
e
τ
β i
3st
|     | q   | h   | k r |     |     |
| --- | --- | --- | --- | --- | --- |
|     |     | 3   | 3   |     |     |
β
nst

r
|     |     | h   | k   |     |     |
| --- | --- | --- | --- | --- | --- |
|     |     | n   | n   |     |     |
e
|     |     | h   | e   |     |     |
| --- | --- | --- | --- | --- | --- |
u
Figure5: Thestructureofthecustompinter-layerconnectionintheEquationembeddedneural
network layers (the dashed line in the figure indicates that the hidden layer in the middle is
omitted).

t
complexneuralnetworkforamobilemanipulatorrobotisnotanoptimalchoice
o
intermsoftimeefficiency[37]sothattheconnectivitybetweennodesofthepro-
posedmodelinE2NNmustbeabletochangedynamically. Therefore,theliquid
n
mechanism is proposed to build custom dynamics inter-layer connection based
on the current input and previous state of the network. Inspired by the “Liquid

time-constantneuralnetwork”researchpublishedin[38],thispaperintroduces
t
the “Liquid mechanism” to address the robust performance issue. A gating unit
has been n incorporated between the physics-informed layers. It comprises a gat-
ing controller and a nonlinear transformer which regulate the information flow
anditransformationbetweenthelayers,asshowninFig.6. Thecolorsrepresent
r
the different connectivity patterns when the E2NN layer processes different in-
pputs. These connectivity patterns refer to the number of connections, between
each neuron and other neurons, and the Eq.(8) based gating control connection
eweights.
|     |     | z = σ(W | h+U l) |     |     |
| --- | --- | ------- | ------ | --- | --- |
z z
| r   |     | g = tanh(W | h+U (α⊙h)) |     | (8) |
| --- | --- | ---------- | ---------- | --- | --- |
g g
|     |     | k′ = (1−z)⊙k | +z ⊙g |     |     |
| --- | --- | ------------ | ----- | --- | --- |
P
13
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
Mimeticnonlinear
transforms Liquidlayer
e
h l
1 1
i
Combinatoricvs
h l bymimesis
2 2
e
h l Output: k (t) = Wouth (t)
n 3 ri i
r
l
4
e
l n e
Updaterule: Eq.6
p
Figure6:E2NNlayerwithvariantinputdependentconnectionsandhiddenstateupdaterule.
Intheformula(8),histhetinputvectorofthecurrentlayer,kistheoutputvector
ofthecurrentlayer,zoisthegatingunit,g isthenon-lineartransformer,W ,U ,
z z
W , U are model parameters, σ, and tanh are activation functions, and ⊙ de-
g g
notes element-wnise multiplication. The third equation in the formula indicates
that the new output k′ is calculated by a non-linear transformation g controlled
bythegating unitz,incombinationwiththepreviouslayeroutput.
It is noted that the leakage rate α plays a key role in controlling the scale of
t
theoutputhoftheupperlevelinthenonlineartransformationg. Typically,αis
n
relatedtothetimeconstantτ,towhichisassignedapre-determinedvalue. How-
ever, to achieve input-related dynamics leakage rate and consider the dynamic
i
physicsconstraintsinside,α canbecalculatedusingα = sigmoid(h).
r
p
3.2.4. Interpretableparameters
The parameter β of Eq.(7) in the E2NN represents the weights of polynomial
e
termsthatcorrespondtochannelweightsinthehiddenlayerofaneuralnetwork,
as shown in Fig. 5. To enhance the performance of the E2NN, a customized loss
rfunction that takes into account both the layer parameters and the underlying
Pphysics equations has been developed and incorporated into the loss calcula-
14
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
tion. This ensures that the E2NN can achieve optimal values for both the NN
structuralparametersandthepolynomialweightsduringtraining. InFig.7. The
e
q
|     | w ( 1) |     |     | i   |     |
| --- | ------ | --- | --- | --- | --- |
1,
1
v
|     | 1 ) l |     |     |     |     |
| --- | ----- | --- | --- | --- | --- |
| (   | 1 1   |     |     |     |     |
| . w | 2 ,   |     |     |     |     |
| q   |       |     | τ   |     |     |
eLoss
(1 ) l
|     | w ,2 n |     |     |     |     |
| --- | ------ | --- | --- | --- | --- |
3
| ..  |     |     | r   |     |     |
| --- | --- | --- | --- | --- | --- |
q

r
Figure7:Dynamicsequationembeddedlossfunction.Thebluedashedlineindicatestheparam-
e
eterusedtocalculatethefinalloss,andtheblackdashedlinerepresentstheintermediatehidden
layerthatpassesfrominputqtooutputτ.
e
loss function is composed of two parts: the mean squared error (MSE) between
thepredicted(τ′)andtrue(τ)vpalues,andaphysicalformulatermthataccounts
for the dynamics of the robotic manipulators movements. The physical formula
termisdefinedas:
t
|        | n            | n            | nj       |                  |     |
| ------ | ------------ | ------------ | -------- | ---------------- | --- |
|        | 1 (cid:88) k | 1 (cid:88) k | (cid:88) |                  |     |
| loss = | o(τ −τ′)2    | +            | (τ − β   | f (q ,q˙ ,q¨ ))2 |     |
|        |              |              | inn      | i it it it       | (9) |
|        | n            | n            |          |                  |     |
|        | k            | k            |          |                  |     |
|        | i=1          | i=1          | i=1      |                  |     |
n
4. Verificationoftheproposedmethodologyinlimiteddataconditions

The efficacy of the E2NN is affirmed through simulation and experimental pro-
t
cedures conducted on a robotic manipulators system, as will be detailed in Sub-
n
section 4.1. The architectural choice for this paper is the Residual Block-E2NN,
which employs a residual neural network as a critical component of the E2NN
framieworkthatisintroducedinSubsection4.2.
Theevaluationmetricsemployed
r
to assess the performance of the proposed methods are explained in Subsec-
ption4.3. ValidationresultsareshownandanalyzedinSubsection4.4and4.5.
e
r
P
15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
4.1. Applicationcases
The knowledge about the dynamics equation is shown in Eq. (10). To simulate
e
incompletedata,thispaperutilizesdatafromasinglejoint.
i
|    |                                            | 0.06cos(q)−0.22sin(q)   |         |         |     |       |
| --- | ------------------------------------------ | ----------------------- | ------- | ------- | --- | ----- |
|    |                                            | (0.22cos(q)+0.06sin(q)) |         |         | v   |      |
|    |                                            |                         |         |         |     |      |
|    |                                            |                         | −0.04q¨ |         |     |      |
|    |                                            |                         |         |         |     |      |
|    | (0.06cos(q)−0.22sin(q))2−(0.22cos(q)+0.06s |                         |         | in(q))2 |     |    |
|    |                                            |                         |         | e       |     |  β   |
 q˙ ( 0 . 22 c o s ( q )+ 0 . 0 6 s in (q )) − 0 . 0 06 s i n ( q ) − ( q ˙ + 0 . 4 9 )( 0 . 2 2 c o s ( q ) + 0 . 0 6 s in (q ) ) − 0 .1 0 98 c o s ( q )  1
|    |     |     |     |     |     |   β 2 |
| --- | --- | --- | --- | --- | --- | -------- |
τ =  0 . 1 1 si n ( q ) − 0. 0 0 6 2 c os (q ) − (q ˙ + 0 . 4 9 ) ( 0 . 0 6 c o s( q ) − 0 . 2 2 s in ( q ) ) + q ˙( 0 . 0 6 co s ( q) − 0 .2 2 si n ( q ) )   ... 
|    |     |                        |                     |           |     |     |
| --- | --- | ---------------------- | ------------------- | --------- | --- | ------ |
|    |     | 4 . 9 0 s in           | ( q ) − 0 . 0 2 6 c | o s ( q ) |     |     |
|    |     |                        |                     | r         |     |       |
|    |     | 4.90cos(q)+0.026sin(q) |                     |           |     |  β 10 |
|    |     |                        |                     |           |     |       |
|    |     |                        | sign(q˙)            |           |     |       |
|    |     |                        |                     |           |     |       |
|    |     |                        | q˙                  |           |     |       |
|     |     |                        | 1.0                 | r         |     |        |
(10)
e
4.1.1. Simulationtest
e
To simulate the movement of a 7-DOF robotic manipulator, the following steps
areconsidered:
p
1. Definetherobot’sdynamicequations.
2. Specifytherobot’sph ysicalparameters.
t
3. Simulatedirect-servo,friction,andinertiaworkingconditionsfortherobot
o
manipulator. Infrictionmode,Coulomb,viscous,andstaticfrictionforces
apply,respectivelyarisingwhenjointsarestationary,movethroughavis-
mednium,
| cous | and | due to adhesive | forces | between | joints. | Inertia mode |
| ---- | --- | --------------- | ------ | ------- | ------- | ------------ |
includes effects of the robot’s mass and moments of inertia, determining
resistan cetomotionchanges,particularlyduringfastmovements.
t
4. Usetheprovidedequationsandinputstoemulatetherobot’smotionover
n
aspecifieddurationusingnumericalintegrationmethodsliketheEuleror
Runge-Kutta.
i
Trhe robot trajectories are generated according to the configuration shown in
Fig.8. Thetrainingdataconsistof26988movementrecordingpointsfrom“Direct-
p
servo”in“Inertia”workingconditions. Thetestingdatainclude53976movement
recordingpointsfrom frictionworkingconditions. For testingrobustness,addi-
e
tional data from “direct-servo” and “Inertia” working conditions are used as a
secondtrainingdataset,buttheE2NNavoidsretrainingonit. Thedatafromthe
r
“Friction”workingconditionareusedfortestinggeneralizationability.
P
16
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
e
i
v
e
r
r
e
e
p
Figure8:ParametersandlinkframesoftheKUKALBRiiwa14R820[39].
4.1.2. Experimentaltest
t
In the experimental validation, the 7-DOF KUKA Sunrise OS is used to interpo-
o
latethetrajectorypointsandcreatethedisplacement,velocity,andacceleration
profiles with the Spline and PTP motion types. With reference to [40] and [41],
n
these excitation trajectories are specifically generated for parameter identifica-
tion and could not be applied when executing a task. The Fast Robot Interface
(FRI) library provided by KUKA is used to continuously exchange data in real
time betweten the robot controller and a C++ client application on an external
systemn. Theclientapplicationrecordeddatafromtherobotatitshighestpossible
rate of 1000 Hz. For the commanded signals, the data are first down-sampled to
50Hiz,andthenvelocitiesandaccelerationsarecalculatedfromthecommanded
prosition. Asecond-orderdigitalButterworthfilterwithacutofffrequencyof3.5
Hz in both directions is applied before the down-sampling process. A total of
p
42,977roboticmanipulatorpositiondatapointsarecollected.
e
4.2. E2NNwithresidualblocks
TheE2NNframeworkisimplementedwithinadeepresidualshrinkagenetwork
r
(DRSN) architecture, as depicted in Fig. 10. This E2NN-ResNet model is com-
Ppared with a conventional ResNet, which is illustrated in Fig. 9. The primary
17
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
distinctionbetweenthesetwomodelsliesintheapplicationofaspecializedresid-
ualblockthatemploystrigonometricoperations(specificallysineandcosine)to
e
compute the sum and difference of inputs, a feature not present in the vanilla
ResNet architecture. In this paper, deep residual shrinkage network (DRSN) has
i
v
e
r
r
e
e
p
t
o
n
t
n
Figure9:Theframeworkofthedeepresidualshrinkagenetwork(DRSN).
threieinputs,allofwhichyielda(batchsize,1)inputforthesubsequentlayers. It
r
consistsof6residualblockswithafullyconnectedlayer. Theoutputoftheblock
pissummedwithashortcutconnectionbyaddingaresidualconnectionwiththe
ReLUactivation function. Thismodeluses themeansquare errorof torquepre-
edictionasthelossfunctionandistrainedusingtheAdamoptimizer.
The E2NN is innovatively implemented to refine the DRSN model by modify-
ing the activation function and the interconnections within the residual block,
r
therebyhighlightingthedistinctivenessofE2NNinFig.10.
P
18
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
e
i
v
e
r
r
e
e
p
t
o
Figure10:E2NNn:DeepResidualShrinkageNetworkwithanembeddedequationproposal.
TheE2NNdemonstratesconsiderableprowessinmimickingtheinversedynam-
t
ics process subjected to physical constraints, thus offering a notable improve-
n
menttoexistingmethods. ThestructureofthemodelcomprisesResidualShrink-
ageBlocksandaLiquidLayer. ThefirstoftheResidualShrinkageBlocks,"RDB1",
i
calculates the cosine of q (shortcut = tf.cos (q)) and maps it to the filters via a
r
dense layer. The second block "RDB2" processes q˙ and q¨. The "Concat" layer
p
then merges the three outputs processed by the residual shrinkage block. Addi-
tionally,theirproducts(R1×R1,R1×R2)areconcatenated. The"Liquid"layer
eassimilatesthesecomponentsandfitsthemtoτ inanapproximatemathematical
form. This methodical and systematic approach to equation representation and
rassimilationformstheessenceoftheE2NN’ssuperiorfunctionality.
P
19
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
4.3. Evaluationmetrics
To quantify the performance of the proposed method regarding the adaptation
e
degreeoftherobotmanipulatorstrajectory,meansquareerror(MSE),theFréchet
distance[42],andthePolygonAreadifference[43])areusedasmetric.
i
v
4.3.1. PolygonAreaDifference
PolygonareaiscalculatedbyusingShoelace’sformulaEq.(11):
e
|     |     |                     | (cid:12)             |       |     |            |     |     |     | (cid:12)     |      |
| --- | --- | ------------------- | -------------------- | ----- | --- | ---------- | --- | --- | --- | ------------ | ---- |
|     |     |                     | (cid:12)(cid:88) n−2 |       |     |            |     |     |     | (cid:12)     |      |
|     |     | Area = 0.5·(cid:12) |                      | (q ·y | −q  | ·y )+(qr·y |     |     | −q  | ·y )(cid:12) | (11) |
|     |     |                     | (cid:12)             | i i+1 |     | i+1 i      | n−1 | 0   | 0   | n−1 (cid:12) |      |
|     |     |                     | (cid:12) i=0         |       |     |            |     |     |     | (cid:12)     |      |

where (q ,y ), i = 0,1,...,n − 1, characterirze the polygon vertices. Next, the
|     |     | i i |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
absolutedifferencebetweentheareasofethepredictedandobservedtrajectories
isshowninEq.(12).
|     |     |     |     | (cid:12)       | e         |       |        | (cid:12) |     |     |      |
| --- | --- | --- | --- | -------------- | --------- | ----- | ------ | -------- | --- | --- | ---- |
|     |     |     |     | =              |           | −Area |        |          |     |     |      |
|     |     |     |     | D (cid:12)Area | predicted |       | actual | (cid:12) |     |     | (12) |
p
A smaller value of D indicates a better match between the predicted and the
actualtrajectories.

|     | 4.3.2. | FréchetDistance |     | t   |     |     |     |     |     |     |     |
| --- | ------ | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
This metric measures o the similarity between two curves, taking into account
the location and arrangement of points. It is particularly useful for comparing
robotmanipulators’trajectoriesasittakesintoaccounttheirspatialandtemporal
n
aspects. Given two curves P and Q represented by sequences of points, the
Discrete Fréchet Distance (DFD) can be calculated by dynamic programming.

TheequationfortheDFDisrecursivelydefinedasfollows:
t
|     |     | n   |     | DFD(P,Q) |     | = c(|P|,|Q|) |     |     |     |     | (13) |
| --- | --- | --- | --- | -------- | --- | ------------ | --- | --- | --- | --- | ---- |
Wheirec(i,j)isafunctiondefinedas:
r

|     |     | d(P | ,Q ) | ifi | = 1andj | =   | 1   |     |     |     |     |
| --- | --- | --- | ---- | --- | ------- | --- | --- | --- | --- | --- | --- |
| p  |     | i   | j    |     |         |     |     |     |     |     |     |


|     |        | max(d(P | ,Q  | ), min(c(i−1,j),c(i−1,j |         |     |     | −1),c(i,j |     | −1))) |      |
| --- | ------ | -------- | --- | ----------------------- | ------- | --- | --- | --------- | --- | ----- | ---- |
|     | c(i,j) | =        | i   | j                       |         |     |     |           |     |       | (14) |
| e   |        |          |     | ifi                     | > 1andj | >   | 1   |           |     |       |      |

 

|     |     | ∞   |     | otherwise |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
r
PWhere
d(P ,Q ) is the Euclidean distance between points P and Q , and |P|
|     |     | i j |     |     |     |     |     |     | i   | j   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
20
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
and|Q|arethelengthsofthetrajectoriesP andQrespectively. Asmallervalue
meansabetterfit.
e
4.3.3. Timecost
i
Apartfromprecision,computationalefficiencyisalsoacriticalfactorthatdeter-
v
minesthesuitabilityofanIDalgorithmforreal-timeapplications. Therefore,the
evaluationtakesintoaccounttheexpectedcomputationtimeforeachpoint,and
e
thefinalassessmentwillincludetheaveragepredictiontimeforasinglepoint.
r
4.4. Validation of the E2NN performance through simulated robotic manipulators
dynamics
In this section, the E2NN fitting results for srimulated robotic manipulator dy-
namicsarepresented.
e
4.4.1. Performanceevaluation
e
TheproposedmodelistrainedinTensorFlowwithearlystoppingafter60epochs
without improvement and a checkpoint to save model parameters at the mini-
p
mum training loss. At training convergence, the MAE of the Benchmark DRSN
modelis0.10415andtheMAEofE2NNis0.10716. Usingthemetricsproposedin
Section.4.3,thetestresultsonthe53976movementrecordingpointsareshown
in Table.4 and Fig. 12. Motreover, the E2NN has a smaller model size and faster
response speed thanothe benchmark DRSN, which makes it a more efficient and
practical solution for robot trajectory fitting tasks. The results also show that
whilethebenchnmarkmodelandtheproposedmethodhavesimilarerrormetrics
values, the benchmark model’s performance is achieved through over-fitting to
local points, r esulting in a group of large and discrete prediction points around
theangulartvelocityscopein(-5,5). Theerrors’maximumvalueisequalto44.431
N·m, which reflects ML’s violation of physical facts. In contrast, the proposed
n
E2NNarchitectureexhibitedanoveralltrendthatisclosertothegroundtruth.
i
Table2:Comparisonofdifferentmethodsonvariousmetrics.
r
p Metrics
Method Responsetime Parameters
MSE AreaDifference FréchetDistance
ANN 0.6 42.9 56.7 3.3×10−4 66753
e
E2NN 0.5 8.3 14.3 1.1×10−4 56223
r
ThetrajectoryfittingresultsrevealedthattheE2NNisabletomoreaccuratelyfit
PtherobottrajectorytothegroundtruthcomparedtothebenchmarkDRSN.The
21
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
difference in performance between conventional DRSN and E2NN when tested
illustratestheexistenceofover-fittinginDRSN,especiallyastheyperformsim-
e
ilarlyintraining.
i
v
e
r
r
e
e
p
t
o
n
Figure11:ComparisonoftheperformanceoftheDRSN(above)andE2NN(below).
t
The dnifference between the training and final test results can be attributed to
the fact that the training and test data are generated from different simulations.
Speciifically, the training data are generated from “direct-servo” and “inertia”,
wrhile the test data are generated from “friction”, which covers a wider range of
pworkingconditionsandhasdifferentactualtorquefunctions. However,E2NNis
abletocompensateforsomeofthemissinginformationfrom“simulatedtraining
data”byembeddingitscorrespondingequations.
e
4.4.2. Identificationofinversedynamicsparameters
r
The average weights of the E2NN dense layer are used as β values for the re-
Pconstructed robot manipulator’s torque trajectory. The fitting performance is
22
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
Table3:Resultsofβ estimationfortheroboticmanipulatorstorquemodel
βi 1 2 3 4 5 6 7 8e9 10
Real 0 0.600 0 0 0 0.010 0.015 0.200 0.100 0.300
Prosedmethods -0.0132 0.617 0.146 0.023 0.0987 0.0134 0.126 0.303 0.116 0.312
i
v
evaluated by comparing the reconstructed trajectory with the ground truth tra-
jectory. TheobtainedresultsareshowninTable.3andFig.12. Thereconstructed
e
trajectories using E2NN’s weights have a high torque fitting accuracy reaching
97.1%(asitstrajectoryisshowninFig.13).
r
r
e
e
p
t
o
Figure12:ReconstructedtorquebyusingMatlab.
n
4.4.3. InvestigationontheE2NN’srobustness
This paper em ploys data generated under the "Friction" working condition to
evaluatethterobustnessofE2NN.Thisprocessinvolvesapplyingthebenchmark
model and E2NN, which have been trained on the same dataset, directly to the
n
newtestwithoutanyadditionaltraining. Thesizeofthenewtestsampleis8996.
The prediction results of the two models are presented in Table 4. During the
i
r
Table4:Comparisonoftherobustnessofdifferentmethodsacrossvariousmetricswhenapplied
ptonewdata.
Metrics
eMethod Responsetime Parameters
MSE AreaDifference FréchetDistance
DRSN 1.1 14.4 8.2 1.2×10−4 66753
rE2NN 0.3 1.6 1.6 8.8×10−5 56223
P
23
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
e
i
v
e
r
r
e
e
p
t
o
n
t
n
i
Figure13:ComparisonbetweentherobustnessperformanceoftheE2NN(below)modelandthe
r
benchmarkDRSN(above).
p
e
r
P
24
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
steady-statemotionoftherobotmanipulatorsintheangularvelocityrangeof-2
to 2, it can be observed that the benchmark DRSN model produces large outlier
e
pointsandanextremelyunstablepredictedcurves. ThemaximumerrorofDRSN
model is 5.3, which is higher than that of the E2NN, and there are significant
i
outliersintheslewingprocessaround-3and3. Inaddition,thebenchmarkmodel
v
showsthatthepredictionresultsdeviatesignificantlyfromtheobsevationinthe
enlargedviewoftheentiresteady-statemovementformation. Ontheotherhand,
e
theE2NNisstillabletofittheactualtrajectorywithpromisedtrendtracking.
4.5. TestE2NNperformanceonrealdata r
During the testing process, it is observed that th e dynamic equations of the ac-
tual robot manipulators are not known. Howrever, it is noted that the equations
could be represented as a polynomial with ten coefficients, comprising various
e
mathematical functions such as sine, cosine, and sign functions. Therefore, in
light of this observation, the architecture presented in Fig. 10 is still deemed
e
appropriateforuseintheexperimentationprocess.
Table5:pValidationonreal-worlddata.
Metric
Method Onepointcalculationtime
MSE AreaDifference FréchetDistance
E2NN 0.001 1. t 2 0.17 6.3×10−5
o
n
t
n
i
r
p
e Figure14:Predictionresultsonrealrobotmanipulators.
r
Based on the results, one can see that E2NN can accurately fit the trajectory
Pwith high precision and computational efficiency under real friction conditions,
25
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
while also exhibiting a good fit to the robot manipulator’s motion. The model’s
performanceisbetterthanthesimulationdata,whichsuggeststhattheimpactof
e
frictionontherobotmanipulatorsduringsingle-jointmotionislesspronounced
in the real-world scenario than in the simulation. Consequently, the difference
i
betweenthetrainingandtestdataisrelativelysmall.
v
5. Conclusionandfutureworks e
This study presented a novel Physics-informed machine learning framework,
r
calledEquationEmbeddedNeuralNetwork(E2NN)forsolvinginversedynamics
problemsinroboticsystems. TheE2NNisevalua tedbyusingsimulationandthe
real-world data collected from 7-degree-of-frreedom (7-DOF) robotic manipula-
tors, achieving high accuracy in torque prediction and fast computation times
e
evenwithlimitedjointdata.
Several contributions are introduced in this study. Firstly, to the best of our
e
knowledge, hybrid framework techniques combining physical knowledge and
ML are the first to be reviewed and summarised. Three different paradigms
p
are proposed. Secondly, a novel framework, E2NN, is proposed and validated.
Thirdly,aphysicsregulatorisincorporatedtosupervisetheE2NNandfacilitate
thelearningoftheseunknow nparameters. Lastly,adynamic"liquid"mechanism
isdesignedtoadaptthemtodelworkingconditionsbyadjustingthehiddenlayer
connections. The vaolidation results demonstrate that the framework is flexible
fordifferentoperatingconditions,iscomputationallytime-saving,andishighly
accurate. n
Futureworkcouldfocusonincorporatinginformationfrommultiplejoints,such
asmulti-joint spatialfreemotionandcollaborativehuman-machinemotion. Ar-
chitecturally, E2NN on this condition can be generalized by sharing parameters
t
acrossmultiplesub-networks. However,acomparisonofapplicationandframe-
n
workparametersinamultitaskingscenarioisneededtofurthervalidatethepro-
posedmethodology.
i
r
References
p
[1] B.Siciliano,L.Sciavicco,L.Villani,G.Oriolo,Robotics: modelling,planning
eandcontrol,SpringerScience&BusinessMedia,2010.
[2] H. Ye, D. Wang, J. Wu, Y. Yue, Y. Zhou, Forward and inverse kinematics
r
of a 5-dof hybrid robot for composite material machining, Robotics and
P Computer-IntegratedManufacturing65(2020)101961.
26
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
[3] M.Toz,Chaos-basedvortexsearchalgorithmforsolvinginversekinematics
problem of serial robot manipulators with offset wrist, Applied Soft Com-
e
puting89(2020)106074.
[4] J. Wu, J. Wang, Z. You, An overview of dynamic parameiter identification
v
of robots, Robotics and computer-integrated manufacturing 26 (5) (2010)
414–419.
e
[5] Q. Leboutet, J. Roux, A. Janot, J. R. Guadarrama-Olvera, G. Cheng, Iner-
tial parameter identification in robotics: A surrvey, Applied Sciences 11 (9)
(2021)4303.
r
[6] B. W. Mooring, Z. S. Roth, M. R. Driels, Fundamentals of manipulator cali-
bration,Wiley-interscience,1991. e
[7] J. Santolaria, M. GinéS, Uncertainty estimation in robot kinematic calibra-
e
tion, Robotics and Computer-Integrated Manufacturing 29 (2) (2013) 370–
384.
p
[8] T.Xu,J.Fan,Y.Chen,X.Ng,M.H.Ang,Q.Fang,Y.Zhu,J.Zhao,Dynamic
identification of the ku ka lbr iiwa robot with retrieval of physical parame-
tersusingglobalopttimization,IEEEAccess8(2020)108018–108031.
o
[9] M. Ramirez-Neria, G. Ochoa-Ortega, N. Lozada-Castillo, M. A. Trujano-
Cabrera, J. P. Campos-Lopez, A. Luviano-Juárez, On the robust trajectory
n
trackingtaskforflexible-jointroboticarmwithunmodeleddynamics,IEEE
Access4(2016)7816–7827.
[10] R.Mutkhopadhyay,R.Chaki,A.Sutradhar,P.Chattopadhyay,Modellearn-
inngforroboticmanipulatorsusingrecurrentneuralnetworks,in: TENCON
2019 - 2019 IEEE Region 10 Conference (TENCON), 2019, pp. 2251–2256.
doi:10.1109/TENCON.2019.8929622.
i
r
[11] F. Semeraro, A. Griffiths, A. Cangelosi, Human-robot collaboration and
p
machine learning: A systematic review of recent research, Robotics and
Computer-IntegratedManufacturing79(2022).
e
[12] L.Jin,S.Li,B.Hu,M.Liu,Asurveyonprojectionneuralnetworksandtheir
applications,AppliedSoftComputing76(2019)533–544.
r
P
27
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
[13] G. E. Karniadakis, I. G. Kevrekidis, L. Lu, P. Perdikaris, S. Wang, L. Yang,
Physics-informed machine learning, Nature Reviews Physics 3 (6) (2021)
e
422–440.
[14] D. Romeres, M. Zorzi, R. Camoriano, S. Traversaro, A. Chiiuso, Derivative-
v
freeonlinelearningofinversedynamicsmodels,IEEETransactionsonCon-
trolSystemsTechnology28(3)(2019)816–830.
e
[15] B. S. Pavse, F. Torabi, J. Hanna, G. Warnell, P. Stone, Ridm: Reinforced in-
verse dynamics modeling for learning from arsingle observed demonstra-
tion,IEEERoboticsandAutomationLetters5(4)(2020)6262–6269.
r
[16] M. Lutter, J. Peters, Combining physics and deep learning to learn
continuous-timedynamicsmodels,earXivpreprintarXiv:2110.01894(2021).
[17] X. Wang, X. Liu, L. Chen, H. Hu, Deep-learning damped least squares
e
method for inverse kinematics of redundant robots, Measurement 171
(2021)108821.
p
[18] F. Djeumou, C. Neary, E. Goubault, S. Putot, U. Topcu, Neural networks
withphysics-informed architecturesandconstraintsfordynamicalsystems
modeling,in: LearnitngforDynamicsandControlConference,PMLR,2022,
pp.263–277. o
[19] W. Sun, N. Akashi, Y. Kuniyoshi, K. Nakajima, Physics-informed recurrent
n
neural networks for soft pneumatic actuators, IEEE Robotics and Automa-
tionLetters7(3)(2022)6862–6869.
[20] H. Retn, P. Ben-Tzvi, Learning inverse kinematics and dynamics of a
rnobotic manipulator using generative adversarial networks, Robotics and
AutonomousSystems124(2020)103386.
i
[21] N.Yilmaz,J.Y.Wu,P.Kazanzides,U.Tumerdem,Neuralnetworkbasedin-
r
versedynamicsidentificationandexternalforceestimationonthedavinci
p
research kit, in: 2020 IEEE International Conference on Robotics and Au-
tomation (ICRA), 2020, pp. 1387–1393. doi:10.1109/ICRA40945.2020.
e9197445.
[22] M. Lahariya, C. Innes, C. Develder, S. Ramamoorthy, Learning physics-
r
informed simulation models for soft robotic manipulation: A case study
P
28
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
with dielectric elastomer actuators, in: 2022 IEEE/RSJ International Con-
ference on Intelligent Robots and Systems (IROS), IEEE, 2022, pp. 11031–
e
11038.
[23] C. Rodwell, P. Tallapragada, Physics-informed reinforcemient learning for
v
motioncontrolofafish-likeswimmingrobot(2022).
[24] K. Morse, N. Das, Y. Lin, A. S. Wang, A. Rai,eF. Meier, Learning state-
dependent losses for inverse dynamics learning, in: 2020 IEEE/RSJ Inter-
national Conference on Intelligent Robots anrd Systems (IROS), IEEE, 2020,
pp.5261–5268.
[25] F.Cursi,D.Chappell,P.Kormushev,Augrmentinglossfunctionsoffeedfor-
ward neural networks with differeential relationships for robot kinematic
modelling, in: 2021 20th International Conference on Advanced Robotics
(ICAR),IEEE,2021,pp.201–207.
e
[26] G.Pizzuto,M.Mistry,Physics-penalisedregularisationforlearningdynam-
p
ics models with contact, in: Learning for Dynamics and Control, PMLR,
2021,pp.611–622.
[27] S. Dereli, R. Köker, A meta-heuristic proposal for inverse kinematics solu-
t
tion of 7-dof serial robotic manipulator: quantum behaved particle swarm
o
algorithm,ArtificialIntelligenceReview53(2020)949–964.
n
[28] R. Ram, P. M. Pathak, S. Junco, Inverse kinematics of mobile manipulator
usingbidirectionalparticleswarmoptimizationbymanipulatordecoupling,
Mechan ismandMachineTheory131(2019)385–405.
t
[29] S. Dereli, R. Köker, Simulation based calculation of the inverse kinematics
n
solution of 7-dof robot manipulator using artificial bee colony algorithm,
SNAppliedSciences2(2020)1–11.
i
r
[30] M. Alebooyeh, R. J. Urbanic, Neural network model for identifying
pworkspace, forward and inverse kinematics of the 7-dof yumi 14000 abb
collaborativerobot,IFAC-PapersOnLine52(10)(2019)176–181.
e
[31] J.S.Toquica,P.S.Oliveira,W.S.Souza,J.M.S.Motta,D.L.Borges,Anan-
alytical and a deep learning model for solving the inverse kinematic prob-
r
lemofanindustrialparallelrobot,Computers&IndustrialEngineering151
P (2021)106682.
29
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
[32] J. Demby’s, Y. Gao, G. N. DeSouza, A study on solving the inverse kine-
matics of serial robots using artificial neural network and fuzzy neural
e
network, in: 2019 IEEE international conference on fuzzy systems (FUZZ-
IEEE),IEEE,2019,pp.1–6.
i
v
[33] M. Lutter, J. Peters, Combining physics and deep learning to learn
continuous-time dynamics models, The International Journal of Robotics
e
Research42(3)(2023)83–107.
[34] P. O. Sturm, A. S. Wexler, Conservation lawsrin a neural network architec-
ture: enforcingtheatombalanceofajulia-basedphotochemicalmodel(v0.
2.0),GeoscientificModelDevelopment15(8)(2022)3417–3431.
r
[35] J. Jia, M. Zhang, X. Zang, H. Zhange, J. Zhao, Dynamic parameter identifi-
cation for a manipulator with joint torque sensors based on an improved
experimentaldesign,Sensors1e9(10)(2019)2248.
[36] P. Hamon, M. Gautier, P. Garrec, A. Janot, Dynamic identification of robot
p
with a load-dependent joint friction model, in: 2010 IEEE Conference on
Robotics,AutomationandMechatronics,IEEE,2010,pp.129–135.
[37] Y.Dai,J.Wang,J.Li,Dtynamicenvironmentpredictiononunmannedmobile
manipulator roobot via ensemble convolutional randomization networks,
AppliedSoftComputing125(2022)109136.
n
[38] R.Hasani,M.Lechner,A.Amini,D.Rus,R.Grosu,Liquidtime-constantnet-
works, in: Proceedings of the AAAI Conference on Artificial Intelligence,
Vol.35,2021,pp.7657–7666.
t
[39] An. Fabio, B. Mourad, A. Janet, On the dynamic parameter identification
of collaborative manipulators: Application to a kuka iiwa, in: 2022 17th
International Conference on Control, Automation, Robotics and Vision
i
r(ICARCV),IEEE,2022,pp.468–473.
p
[40] F. Ardiani, M. Benoussaad, A. Janot, Improving recursive dynamic param-
eter estimation of manipulators by knowing robot’s model integrated in
ethe controller, IFAC-PapersOnLine 55 (2022) 223–228. doi:10.1016/j.
ifacol.2022.09.099.
r
P
30
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725

d
e
w
[41] J. Jin, N. Gans, Parameter identification for industrial robots with a fast
and robust trajectory design approach, Robotics and Computer Integrated
e
Manufacturing31(1)(2015)21–29.
[42] L. Tonin, F. C. Bauer, J. d. R. Millán, The role of the contriol framework for
v
continuousteleoperationofabrain–machineinterface-drivenmobilerobot,
IEEETransactionsonRobotics36(1)(2019)78–91.
e
[43] H. Shen, L. Pan, J. Qian, Research on large-scale additive manufacturing
basedonmulti-robotcollaborationtechnologry,AdditiveManufacturing30
(2019)100906.
r
e
e
p
t
o
n
t
n
i
r
p
e
r
P
31
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4542725