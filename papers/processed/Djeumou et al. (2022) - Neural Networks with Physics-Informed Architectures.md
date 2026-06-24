ProceedingsofMachineLearningResearchvol168:1–15,2022 4thAnnualConferenceonLearningforDynamicsandControl
Neural Networks with Physics-Informed
Architectures and Constraints for Dynamical Systems Modeling
FranckDjeumou*1 FDJEUMOU@UTEXAS.EDU
CyrusNeary*1 CNEARY@UTEXAS.EDU
EricGoubault2 GOUBAULT@LIX.POLYTECHNIQUE.FR
SylviePutot2 PUTOT@LIX.POLYTECHNIQUE.FR
UfukTopcu1 UTOPCU@UTEXAS.EDU
1TheUniversityofTexasatAustin,UnitedStates
2LIX,CNRS,E´colePolytechnique,InstitutPolytechniquedeParis,France
Editors:R.Firoozi,N.Mehr,E.Yel,R.Antonova,J.Bohg,M.Schwager,M.Kochenderfer
Abstract
Effectiveinclusionofphysics-basedknowledgeintodeepneuralnetworkmodelsofdynamicalsys-
temscangreatlyimprovedataefficiencyandgeneralization. Suchaprioriknowledgemightarise
from physical principles (e.g., conservation laws) or from the system’s design (e.g., the Jacobian
matrix of a robot), even if large portions of the system dynamics remain unknown. We develop
a framework to learn dynamics models from trajectory data while incorporating a priori system
knowledge as inductive bias. More specifically, the proposed framework uses physics-based side
information to inform the structure of the neural network itself, and to place constraints on the
values of the outputs and the internal states of the model. It represents the system’s vector field
asacompositionofknownandunknownfunctions,thelatterofwhichareparametrizedbyneural
networks. The physics-informed constraints are enforced via the augmented Lagrangian method
duringthemodel’straining. Weexperimentallydemonstratethebenefitsoftheproposedapproach
onavarietyofdynamicalsystems–includingabenchmarksuiteofroboticsenvironmentsfeatur-
inglargestatespaces,non-lineardynamics,externalforces,contactforces,andcontrolinputs. By
exploitingapriorisystemknowledgeduringtraining, theproposedapproachlearnstopredictthe
systemdynamicstwoordersofmagnitudemoreaccuratelythanabaselineapproachthatdoesnot
includepriorknowledge,giventhesametrainingdataset.
Keywords: Physics-constrainedlearning;neuralordinarydifferentialequations;nonlinearsystem
identification;dynamicalsystems.
1. Introduction
Owing to their tremendous capability to learn complex relationships from data, neural networks
offer promise in their ability to model unknown dynamical systems from trajectory observations.
Such models of system dynamics can then be used to synthesize control strategies, to perform
model-basedreinforcementlearning,ortopredictthefuturevaluesofquantitiesofinterest.
However, purely data-driven approaches to learning can result in poor data efficiency and in
model predictions that violate physical principles. These deficiencies become particularly empha-
sized when the training dataset is relatively small – the neural network must learn to approximate
*Theseauthorscontributedequally.
Projectcodeisfreelyavailableathttps://github.com/wuwushrek/physics constrained nn.
©2022F.Djeumou,C.Neary,E.Goubault,S.Putot&U.Topcu.

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
|     |     | Physics-Informed | Neural ODE |     |     |     |
| --- | --- | ---------------- | ---------- | --- | --- | --- |
·
|     | Training data |     | g1  |        |           |     |
| --- | ------------- | --- | --- | ------ | --------- | --- |
|     |               | ·   |     | Vector | Predicted |     |
x
|                       |           |     |           | field ODE | nextstate | Loss |
| --------------------- | --------- | --- | --------- | --------- | --------- | ---- |
|                       |           | ... | . (cid:0) |           |           |      |
| Physics-Informed      | Structure |     | . F ···)  | Solver    |           | J(·) |
| (cid:0)               | (cid:1)   | u   | .         |           |           |      |
| x˙ =F x,u,g1(·),...,g | (·)       |     |           |           |           |      |
|                       | d         | ·   |           |           |           |      |
g
| e.g., q¨=M−1(q)[C(q,q˙) |     | ·   | d   |     |     |     |
| ----------------------- | --- | --- | --- | --- | --- | --- |
EnforceΨThroughout
| +τ(q,q˙,u)+J(q)F(q,q˙,u)] |             |     |             | StateSpace |     |            |
| ------------------------- | ----------- | --- | ----------- | ---------- | --- | ---------- |
|                           |             |     | g1(·),...,g | (·)        |     |            |
| Physics-Informed          | Constraints |     |             | d          |     | Constraint |
| (cid:0)                   | (cid:1)     |     |             |            |     |            |
| Ψ x,u,g1(·),...,g         | d (·) ≤0    |     |             |            |     | violations |
Ψ(·)
|     |     |     |     | Training | Unlabelled |     |
| --- | --- | --- | --- | -------- | ---------- | --- |
e.g.,Fnorm(q,q˙,u)≥0,||Ftang(q,q˙,u)||≤µ∗Fnorm(q,q˙,u)
Figure1: An illustration of the proposed framework. A priori physics knowledge is captured by a
structuredrepresentationofthevectorfield(blue)–unknowncomponentsarerepresented
by neural networks (red). Physics-based constraints are enforced on the outputs of the
modelnotonlyonthelabeledtrainingdatapoints,butalsoonanyunlabeledpointswithin
thestatespacewheretheconstraintsareknowntoholdtrue(yellow).
a high-dimensional and non-linear map from a limited number of state trajectories. This limited
reliabilityinthescarcedataregimecanrenderneural-network-baseddynamicsmodelsimpractical
fortheaforementionedapplications.
On the other hand, useful a priori system knowledge is often available, even in circumstances
when the exact dynamics remain unknown. Such knowledge might stem from a variety of sources
–basicprinciplesofphysics,geometryconstraintsarisingfromthesystem’sdesign,orempirically
validatedinvariantsetsinthestatespace. Thecentralthesisofthispaperisthateffectiveinclusion
of a priori knowledge into the training of deep neural network models of dynamical systems can
greatly improve data efficiency and model generalization to previously unseen regions of the state
space,whilealsoensuringthatthelearnedmodelrespectsphysicalprinciples.
Wedevelopaframeworktoincorporateawidevarietyofpotentialsourcesofaprioriknowledge
intodata-drivenmodelsofdynamicalsystems. Theframeworkusesneuralnetworkstoparametrize
thedynamicalsystem’svectorfieldandusesnumericalintegrationschemestopredictfuturestates,
asopposedtoparametrizingamodelthatpredictsthenextstatedirectly. Physics-basedknowledge
isincorporatedasinductivebiasinthemodelofthevectorfieldviatwodistinctmechanisms:
1. Physics-informed model structure. We represent the system’s vector field as compositions
ofunknowntermsthatareparametrizedasneuralnetworksandknowntermsthatarederivedfrom
a priori knowledge. For example, Figure 1 illustrates a robotics environment in Brax (Freeman
etal.,2021)whoseequationsofmotionweassumetobepartiallyknown;therobot’smassmatrixis
available,whiletheremainingtermsinitsequationsofmotion(i.e. itsactuationandcontactforces)
must be learned. Neural networks representing the unknown terms are composed with the known
massmatrixtoobtainamodelofthesystem’svectorfield,asisillustratedinFigure1.
2. Physics-informed constraints. We additionally enforce physics-based constraints on the val-
uesoftheoutputsandtheinternalstatesofthemodel. Suchconstraintscould,forexample,encode
known system equilibria, invariants, or symmetries in the dynamics. We note that while only a
limited number of datapoints may be available for supervised learning, constraints derived from a
2

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
10−2
10−4
10−6
0 1 2 3
GradientSteps(·104)
ssoLgnitseT Baseline K1 K2
10−1
10−2
10−3
1 15 25 50
Num. TrainingTrajectories
rorrEtuolloR
.gvA
Figure2: Incorporationofaprioriknowledgeresultsinasignificantimprovementindataefficiency
and out-of-sample prediction accuracy. K1 corresponds to the incorporation of basic
vector field knowledge: dx = v. K2 corresponds to knowledge of the mass matrix of
dt
the robot. The Testing Loss plot illustrates the model’s prediction errors during training.
The Avg. Rollout Error plot illustrates a measure of the error over an entire predicted
trajectorybeginningfromanout-of-sampleinitialstate,aftertraininghasconverged.
prioriknowledgewillholdoverlargesub-setsofthestatespace,andpotentiallyoverthestatespace
initsentirety. Ensuringthatthelearnedmodelsatisfiestherelevantconstraintsthroughoutthestate
space, while also fitting the available trajectory data, leads to a semi-supervised learning scheme
thatgeneralizestheavailabletrainingdatatotheunlabeledportionsofthestatespace.
We train the model on time-series data of state and control input observations. The physics-
informed model of the vector field is integrated in time to obtain predictions of the future state.
These predictions are in turn compared against the true future state values obtained from training
data to define the model’s loss. During the model’s training, we enforce the physics-informed
constraintsonacollectionofpointsinthestatespace,bothlabeledandunlabeled,viatheaugmented
Lagrangianmethod(Luetal.,2021;Hestenes,1969).
Weexperimentallydemonstratetheeffectivenessoftheproposedapproachonadoublependu-
lumsystemaswellasonasuiteofcontrolledrigidmulti-bodysystemssimulatedinBrax(Freeman
et al., 2021). This suite includes systems with nonlinear dynamics, control inputs, contact forces,
and states with hundreds of dimensions. We are the first to consider such a suite of experiments
in the context of physics-informed neural networks. We consider symmetries in the system vector
fields, knowledge of the mass and Jacobian matrices of the robotic systems, and constraints that
encode the laws of friction to help learn contact forces. We examine the extent to which these
different sources of side information aid in improving the data efficiency and the out-of-sample
prediction accuracy of the learned models. By exploiting a priori system knowledge during train-
ing, the proposed approach learns to predict system dynamics more than two orders of magnitude
more accurately than a baseline approach that does not include any prior knowledge, as illustrated
inFigure2. Theexperimentsdemonstratetheviabilityoftheproposedframeworkfortheefficient
learning of complex systems that are often used as challenging benchmark environments for deep
reinforcementlearningandmodel-basedcontrol(Duanetal.,2016;Freemanetal.,2021).
2. Physics-InformedNeuralArchitectures
Weconsiderarbitrarynon-lineardynamicsthatcanbeexpressedintermsofanordinarydifferential
equation (ODE) of the form x˙ = h(x,u). The state x : R (cid:55)→ X is a continuous-time signal,
+
3

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
R
the control input u : + (cid:55)→ U is a (possibly non-continuous) signal of time, and the vector field
h : X×U (cid:55)→ Rnisassumedtobeunknownandpossiblynon-linear. Here,ndenotesthedimension
of the state. We note that it is straightforward to explicitly include time dependency in the ODE
representingthesystemdynamics,however,weomititforclarityandnotationalsimplicity.
Throughoutthepaper,weassumethatafinitedatasetDofsystemtrajectories–time-seriesdata
of states and control inputs – is available, in lieu of the system’s model. That is, we are given a
set D = {τ ,...,τ } of trajectories τ = {(x ,u ),(x ,u ),...,(x ,u )}, where x = x(t ) is
|     | 1   | |D| |     |     |     | 0 0 | 1   | 1   | T   | T   | i   | i   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the state at time t i , u i = u(t i ) is the control input applied at time t i , and t 0 < t 1 < ... < t T is
an increasing sequence of points in time. We seek to learn a function to predict future state values
x ,...,x ,giventhecurrentstatevaluex andasequenceofcontrolinputsu ,...,u .
| k+1 | k+nr+1 |     |     |     |     | k   |     |     |     |     | k   | k+nr |
| --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
We propose to parametrize and to learn the unknown vector field h, as opposed to learning a
prediction function that maps directly from a history of states and control inputs to the predicted
nextstate. Thischoicetoparametrizeamodelofthevectorfieldisprimarilymotivatedbythetwo
following points: (1) a priori knowledge derived from physical principles is typically most easily
expressed in terms of the system’s vector field; (2) Chen et al. (2018) recently demonstrated that
parametrizing the vector field results in models that are able to approximate time-series data with
more accuracy than approaches that directly estimate the next state. We thus build a framework
capableoflearningthevectorfieldhfromthedatasetDoftrajectories,whilealsotakingadvantage
ofpriorknowledgesurroundingthefunctionalformofthevectorfield.
CompositionalRepresentationoftheVectorField. Werepresentthevectorfieldofthedynam-
ical system as the composition of a known function – derived from a priori knowledge – and a
collectionofunknownfunctionsthatmustbelearnedfromdata.
|     |     |     | x˙  | = h(x,u) | = F(x,u,g |     | (·),...,g | (·)) |     |     |     | (1) |
| --- | --- | --- | --- | -------- | --------- | --- | --------- | ---- | --- | --- | --- | --- |
|     |     |     |     |          |           |     | 1         | d    |     |     |     |     |
Here, F is a known differentiable function encoding available prior knowledge on the system’s
model. The functions g ,...,g encode the unknown terms within the underlying model. The
|     |     |     | 1   | d   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
inputstothesefunctionscouldthemselvesbearbitraryfunctionsofthestatesandcontrolinputs,or
evenoftheoutputsoftheotherunknownterms.
End-To-End Training of the Model. Using the available training data, we learn the unknown
functions g θ1 ,g θ2 ,...,g θ in an end-to-end fashion. We parametrize g 1 ,g 2 ,...,g d by a collection
d
of neural networks g ,g ,...,g , where θ ,θ ,...,θ are the parameter vectors of each of the
|     |     | θ1  | θ2  | θ   | 1   | 2   | d   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
d
individual networks. For notational simplicity, we define Θ = (θ ,...,θ ) and we denote the
|                             |     |     |     |           |     |       |     |     | 1   | d   |     |     |
| --------------------------- | --- | --- | --- | --------- | --- | ----- | --- | --- | --- | --- | --- | --- |
| collectionofneuralnetworksg |     |     |     | ,g ,...,g |     | byG Θ | .   |     |     |     |     |     |
|                             |     |     | θ1  | θ2        | θ d |       |     |     |     |     |     |     |
ForfixedvaluesoftheparametersΘ,weintegratethecurrentestimateofthedynamicsF(·,·,G )
Θ
usingadifferentiableODEsolvertoobtainpredictionsofthefuturestate. Morespecifically,given
an increasing sequence of n distinct points in time t < t < ... < t , an initial state x ,
|     |     |     | r   |     |     |     | i   | i+1 |     | i+nr |     | i   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
and a sequence of control input values u i ,...u i+nr , we use (2) to solve for the model-predicted
sequence of future states xΘ ,...,xΘ . We assume the control input has a constant value u
|                       |     |     | i+1   | i+nr+1 |     |     |     |     |     |     |     | i   |
| --------------------- | --- | --- | ----- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
| overthetimeinterval[t |     |     | ,t ). |        |     |     |     |     |     |     |     |     |
i i+1
|     |     | xΘ ,...,xΘ |        | =   | ODESolve(x |     | ,u ,...,u |      | ;F(·,·,G | ))  |     | (2) |
| --- | --- | ---------- | ------ | --- | ---------- | --- | --------- | ---- | -------- | --- | --- | --- |
|     |     | i+1        | i+nr+1 |     |            |     | k i       | i+nr |          | Θ   |     |     |
ThelossfunctionJ(Θ)canthenbeconstructedtominimizethestatepredictionerroroverthefixed
|                 |     |           |     | (cid:80) | (cid:80)     |     | (cid:80)i+nr | ∥xΘ |     | ∥2,foragivennorm. |     |     |
| --------------- | --- | --------- | --- | -------- | ------------ | --- | ------------ | --- | --- | ----------------- | --- | --- |
| rollouthorizonn |     | ,asinJ(Θ) | =   |          |              |     |              |     | −x  |                   |     |     |
|                 |     | r         |     | τ        | ∈D (xi,ui)∈τ |     | j=i          | j+1 | j+1 |                   |     |     |
|                 |     |           |     | l        |              |     | l            |     |     |                   |     |     |
4

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
Finally,assumingthatF isdifferentiable,wecanupdatetheweightsinΘusingeitherautomatic
differentiation, or using the adjoint sensitivity method (Chen et al., 2018). We note that for each
datapoint (x ,u ) within each trajectory τ , we use the model to roll out predictions of the next n
|     | i i |     |     | l   |     |     |     |     | r   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
states, which are in turn used to define the loss function. This use of rollouts instead of one-step
predictionswhiledefiningthelossfunctionresultsinareductioninerroraccumulation.
3. Physics-InformedNeuralNetworkConstraints
Inadditiontousingaprioriphysics-basedknowledgetodictatethestructureoftheneuralnetwork,
wealsousesuchknowledgetoderiveconstraintsontheoutputsandtheinternalstatesofthemodel.
Moreformally,supposewederiveaparticularphysics-informedmodelF(x,u,G )ofthesystem’s
Θ
vectorfieldwithunknowntermsparametrizedbythecollectionofneuralnetworksG . Recallthat
Θ
Θ = (θ 1 ,θ 2 ,...,θ d ) and that by G Θ we denote g θ1 ,...,g θ . Our objective is to solve for a set of
d
parametervaluesminimizingthelossJ(Θ)overthetrainingdatasetwhilealsosatisfyingallofthe
knownphysics-basedconstraints. Thatis,weaimtosolvetheoptimizationproblem(3)-(4).
|     |     | min J(Θ)s.t. | Φ   | (x,u,G | ) = 0, ∀(x,u) | ∈ C ,i | ∈ [v], |     | (3) |
| --- | --- | ------------ | --- | ------ | ------------- | ------ | ------ | --- | --- |
|     |     |              |     | i      | Θ             | Φi     |        |     |     |
Θ
|     |     |     | Ψ   | (x,u,G | ) ≤ 0, ∀(x,u) | ∈ C ,j | ∈ [l] |     | (4) |
| --- | --- | --- | --- | ------ | ------------- | ------ | ----- | --- | --- |
|     |     |     |     | j      | Θ             | Ψj     |       |     |     |
Here, Φ (x,u,G ) and Ψ (x,u,G ) are differentiable functions capturing the physics-informed
| i   | Θ   | j   | Θ   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
equality and inequality constraints respectively. We use [v] = {1,...,v} and [l] = {1,...,l} to
denotethesetsindexingtheseconstraints. Foreachconstraint,weadditionallyassumethereissome
sub-setC ,C ⊆ X ×U,alsoderivedfromaprioriknowledge,overwhichtheconstraintshould
Φi Ψj
holdtrue. Aselements(x,u) ∈ C ,C arenotnecessarilyincludedinthetrajectorydatausedfor
Φi Ψj
training,theconstraintsthusprovideusefulinformationaboutpotentiallyunlabeledpoints.
EnforcingConstraintsThroughouttheStateSpace. While(3)-(4)specifiesthateachconstraint
shouldholdoversomeknownsubsetofthestatespace,thisformulationleadstoapossiblyinfinite
numberofconstraints. Toapproximatelysolvetheproblemnumerically,weinsteadselectafiniteset
Ω = {(x ,u ),(x ,u ),...(x ,u )} ⊆ X ×U of points at which we enforce the constraints.
| 1   | 1   | 2 2 |Ω| | |Ω| |     |     |     |     |     |     |
| --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
That is, we replace the possibly infinite sets of constraints given by (3)-(4) with the finite set of
constraintsgivenby(5)–(6).
|     |     | Φ (x,u,G |     | ) = 0,∀(x,u) | ∈ Ω∩C | ,i ∈ [v] |     |     | (5) |
| --- | --- | -------- | --- | ------------ | ----- | -------- | --- | --- | --- |
|     |     | i        |     | Θ            |       | Φi       |     |     |     |
|     |     | Ψ (x,u,G |     | ) ≤ 0,∀(x,u) | ∈ Ω∩C | ,j ∈ [l] |     |     | (6) |
|     |     | i        |     | Θ            |       | Ψj       |     |     |     |
Intuitively,byoptimizingthelossfunctionJ(Θ)in(3)subjectto(5)–(6),wearefindingthesolution
that fits the training data as well as possible, while also satisfying all of the relevant constraints at
eachpointwithinafinitesetΩofrepresentativestatesthroughoutX ×U.
The Augmented Lagrangian Method. In order to solve this optimization problem, we use a
stochasticgradientdescent(SGD)variantoftheaugmentedLagrangianmethod,asproposedby(Lu
etal.,2021;Toussaint,2014)forthenumericalsolutionofconstrainedoptimizationproblems. For
each constraint in(5)-(6), we define a separate Lagrangevariable. That is, wedefine an individual
λeq
variable for each equality constraint Φ ,i ∈ [v] evaluated at each point (x ,u ) ∈ Ω∩ C ,
| i,k |     |     |     | i   |     |     | k k |     | Φi  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
and similarly λineq at each point (x ,u ) ∈ Ω ∩ C for all the inequality constraints Ψ . The
|     | j,k |     | k   | k   | Ψj  |     |     | j   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
augmentedLagrangianoftheoptimizationproblemisgivenby(7).
5

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
L(Θ,µ,λ) = J(Θ)+ (cid:88) µΦ (x ,u ,G )2+ (cid:88) λeqΦ (x ,u ,G ) (7)
i k k Θ i,k i i i Θ
i∈[v] i∈[v]
(x
k
,u
k
)∈Ω∩CΦi (x
k
,u
k
)∈Ω∩CΦi
+ (cid:88) µ[λineq > 0∨Ψ > 0]Ψ (x ,u ,G )2+ (cid:88) λineqΨ (x ,u ,G )
j,k j j k k Θ j,k j k k Θ
j∈[l] j∈[l]
(x
k
,u
k
)∈Ω∩CΨj (x
k
,u
k
)∈Ω∩CΨj
The Proposed Training Algorithm. Algorithm 1 outlines the proposed approach to optimizing
the loss function J(Θ) in (3) subject to (5)–(6) via the augmented Lagrangian method. In the
algorithm, we use the notation x = max{0,x}. We initialize values for µ and λ and minimize
+
L(Θ,µ,λ) via SGD over Θ while holding the values of µ and λ fixed. To prevent the gradient
descentfromgettingstuckinlocalminima,Algorithm1randomlysamplesasubsetofpointsfrom
Ω at each gradient update, instead of including the entire set in the definition of L(Θ,µ,λ). This
random selection of points at which to evaluate the constraint violations is akin to the random
sampling of minibatches of training data during traditional SGD. Once this inner loop SGD has
converged, we update the values of µ and λ according to the update rules outlined in Algorithm 1.
Thisprocessisrepeateduntiltheconstraintsareallsatisfied,towithinanallowedtolerancevalueϵ.
Algorithm1TrainingAlgorithm
Input: F(·),{Φ (·)} ,{Ψ (·)} ,D,Ω
i i∈[v] j j∈[l]
Parameter: ϵ,µ ,µ ,N ,N
0 mult trainBatch constrBatch
Output: ModelparametersΘ.
1: InitializeparametersΘ;λe i, q k ← 0;λi j n ,k eq ← 0;µ ← µ 0 .
(cid:80) (cid:80) (cid:80) (cid:80)
2: while i k |Φ i (x k ,u k ,G Θ )|+ j k (Ψ j (x k ,u k ,G Θ )) + ≥ ϵdo
3: whilenotSGDStoppingCriterion()do
4: D batch ← Sample(D,N trainBatch );Ω batch ← Sample(Ω,N constrBatch )
5: Θ ← optimUpdate(L,Θ,D batch ,Ω batch )
6: endwhile
7: λe i, q k ← λe i, q k +2∗µ∗Φ i (x k ,u k ,G Θ );λi j n ,k eq ← (λi j n ,k eq+2∗µ∗Ψ j (x k ,u k ,G Θ )) +
8: µ ← µ∗µ mult
9: endwhile
4. ExperimentalResults
4.1. LearningtheDynamicsofaDoublePendulum
Thedynamicsofthedoublependulumaredescribedby(8).
ϕ¨ = (g −α g )/(1−α α ); ϕ¨ = (−α g +g )/(1−α α ) (8)
1 1 1 2 1 2 2 2 1 2 1 2
Here, ϕ and ϕ specify the angular position of the first and second links of the pendulum,
1 2
α (ϕ ,ϕ ) ∝ cos(ϕ −ϕ ),α (ϕ ,ϕ ) ∝ cos(ϕ −ϕ ),andg (ϕ ,ϕ ,ϕ˙ ,ϕ˙ ),g (ϕ ,ϕ ,ϕ˙ ,ϕ˙ )
1 1 2 1 2 2 1 2 2 1 1 1 2 1 2 2 1 2 1 2
are both complicated trigonometric functions of the state variables. By setting x = ϕ , x = ϕ ,
1 1 2 2
x = ϕ˙ , and x = ϕ˙ we can thus express the dynamics as x˙ = h(x), where h (x) = x ,
3 1 4 2 1 3
h (x) = x ,andh (x),h (x)arebothgivenby(8). Werefertotheextendedversionofthepaper
2 4 3 4
formoredetailssurroundingthedynamics(Djeumouetal.,2021).
6

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
10−3
10−4
0.0 0.5 1.0 1.5 2.0 2.5 3.0
TrainingSteps(·103)
ssoLgnitseT
10−1
Baseline K1 K2
10−2
10−3
0.0 0.5 1.0 1.5 2.0 2.5 3.0
TrainingSteps(·103)
ssoLtniartsnoC
Figure3: Doublependulumnumericalresults. Asingletrajectorythatis3secondsinlengthisused
astrainingdata. Theshadedareasillustratethevarianceoftheresultsoverfiveruns.
DefiningaBaselineforComparison. Asabaseline,weparametrizethevectorfieldhbyasingle
neural network g . In terms of the framework outlined in the previous sections, we thus have
θ1
Θ = θ andF(x,G ) = g (x).
1 Θ θ1
(K1) Incorporating Knowledge of Equation (8). In order to demonstrate how arbitrary knowl-
edgesurroundingthesystem’svectorfieldcanbeincorporatedintothedynamicsmodel,weassume
thatequation(8)isknown,alongwithα (·)andα (·). However,weassumeg (·)andg (·)areun-
1 2 1 2
known. Weparametrizeg andg bytwoneuralnetworksg andg ,respectively. Theproposed
1 2 θ1 θ2
model for the vector field may thus be expressed as F (x,G ) = x , F (x,G ) = x , and with
1 Θ 3 2 Θ 4
F (x,G ),F (x,G )bothbeingfunctionsofα ,α ,g ,g ,asinequation(8).
3 Θ 4 Θ 1 2 θ1 θ2
(K2) Incorporating Symmetry Constraints on g and g . To demonstrate that the proposed
1 2
trainingalgorithmproperlyenforcesconstraintsonthesystem’sdynamics,weimposeequalitycon-
straintsong ,g derivedfromsymmetriesinthevectorfield. Inparticular,weimposefoursepa-
θ1 θ2
rate equality constraints, an example of which is as follows: g (x ,x ) = −g (−x ,x ).
1 1:2 3:4 1 1:2 3:4
These equality constraints are enforced at a collection of points Ω that are sampled uniformly
throughoutthestatespace.
Experimental Setup. Each neural network g (x) is a multilayer perceptron (MLP) with ReLu
θi
activationfunctionsandtwohiddenlayerswith128nodeseach. Weusearollouthorizonofn = 5
r
when defining the loss function and we randomly sample |Ω| = 10000 points throughout the state
spaceX atwhichweenforcetheaboveequalityconstraints. Forfurtherdetailsonthesetupofthe
experiment,werefertotheextendedversionofthepaper(Djeumouetal.,2021).
ExperimentalResults. Figure3plotstheresultsoftrainingthevariousphysics-informedmodels
usingonlyasingletrajectoryofdata,whichequivalentto3secondsworthofobservations. Weob-
servethatintermsofpredictionlosses,(K1)performsbetterthanthebaseline,and(K2)performs
better than both the baseline and (K1); its testing loss at convergence is roughly an order of mag-
nitude lower than that of (K1). Furthermore, we observe that the constraint loss of (K2) – which
measures the average value of the model’s violation of the equality constraints – is roughly two
ordersofmagnitudelowerthanthatof(K1). Theseresultsdemonstratetheproposedframework’s
effectivenessatincorporatingapriorisystemknowledgeintothedynamicsmodel. Asmoredetailed
knowledgeisincludedintothemodel,thetestinglossatconvergenceissignificantlyreduced. Fur-
thermore, the gap in constraint loss between (K1) and (K2) demonstrates the effectiveness of the
proposedframeworkinlearningtofitthetrainingdatawhilesimultaneouslyenforcingconstraints.
7

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
Ant Fetch Humanoid Reacher UR5EArm
Figure4: Illustrationofthesuiteofsimulatedroboticsystemsusedduringtesting.
4.2. LearningtheDynamicsofControlled,Rigid,Multi-BodySystems
In this section we apply the proposed framework to a suite of robotic systems simulated in Brax
(Freeman et al., 2021). These systems feature control inputs, non-linear dynamics, and external
forces. Figure4illustratesthespecificroboticsystemsweusefortesting.
The Governing Equations of Motion. The dynamics of all of the environments listed in Figure
4canbedescribedbythegeneralequationsofmotiongivenin(9).
q¨= M(q)−1[C(q,q˙)+τ(q,q˙,u)+J(q)F(q,q˙,u)] (9)
Here, q and q˙ represent the system state and its time derivative respectively, M(q) represents the
system’s mass matrix, C(q,q˙) is a vector representing the Coriolis forces, τ(q,q˙,u) is a vector
representing the actuation forces (given the control input u), J(q) is the system’s Jacobian matrix,
and F(q,q˙,u) is a vector representing the contact forces. By setting x = q and x = q˙, we may
1 2
re-writethesystemintheformx˙ = h(x,u).
DefiningaBaselineforComparison. Similarlytothedoublependulumbaseline,weuseasingle
neuralnetworktoparametrizethevectorfield,i.e. F(x,u,G ) = g (x,u).
Θ θ1
(K1)IncorporatingBasicKnowledgeontheVectorField. Arelativelysimplepieceofapriori
knowledge is that x˙ = x . This follows directly from our formulation of the system’s dynamics,
1 2
and it provides a useful piece of inductive bias surrounding the structure of the vector field. In
our proposed framework, we again parametrize the vector field using a single neural network g ,
θ1
however,wenowhaveF (x,u,G ) = x andF (x,u,G ) = g (x,u).
1 Θ 2 2 Θ θ1
(K2) Incorporating Knowledge of the Mass Matrix. We now assume the mass matrix M(x )
1
and the Coriolis force C(x ,x ) terms are known a priori. To use this a priori knowledge, we
1 2
parametrizetheactuationforcetermandthecontactforcetermusingindividualneuralnetworksg
θ1
and g . Our structured neural network model of the system dynamics may be written as follows:
θ2
F (x,u,G ) = x andF (x,u,G ) = M−1(x )C(x ,x )+g (x,u)+g (x,u).
1 Θ 2 2 Θ 1 1 2 θ1 θ2
(K3)IncorporatingKnowledgeoftheJacobianMatrix. Weassume,inadditiontotheapriori
knowledgeassumedin(K3),thatthesystem’sJacobianmatrixJ(x )isalsoknown: F (x,u,G ) =
1 1 Θ
x ,F (x,u,G ) = M−1(x )C(x,x )+g +J(x )g .
2 2 Θ 1 2 θ1 1 θ2
(K4) Incorporating Contact Force Constraints. We use the laws of friction to derive con-
straints on the contact forces between the robotic systems and the ground. In particular, we have
F (x,u) ≤ 0and||F (x,u)|| ≥ µF (x,u),whereF representsthenormalcompo-
norm tang norm norm
nentofthecontactforcesandF isthetangentialforcevector. Weassume(K4)hasaccesstothe
tang
same amount of a priori knowledge as (K3), and that it additionally imposes the above inequality
constraintsontheneuralnetworkg ,whichrepresentsthecontactforceterm.
θ2
8

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
rorrEtuolloR
ssoLgnitseT 10−0.5
1·10−1
10−1
| 4·10−2 |       | .gvA  |       |                      |         |
| ------ | ----- | ----- | ----- | -------------------- | ------- |
|        |       |       | 0 100 | 200 300              | 400 500 |
| 0 2    | 4 6 8 | 10 12 |       |                      |         |
|        |       |       | Num.  | TrainingTrajectories |         |
TrainingSteps(·103)
rorrEnoitciderP ssoLtniartsnoC
| 10−0.8 |     |     | 102 |     |     |
| ------ | --- | --- | --- | --- | --- |
100
| 10−1 |     | 10−2 |     |     |     |
| ---- | --- | ---- | --- | --- | --- |
10−4
| 10−1.2 |     | 10−6 |     |     |     |
| ------ | --- | ---- | --- | --- | --- |
10−8
10−10
| 0 2            | 4 6                                       | 8   | 0 2                 | 4 6 | 8 10 12 |
| -------------- | ----------------------------------------- | --- | ------------------- | --- | ------- |
| Time[s](·10−2) |                                           |     | TrainingSteps(·104) |     |         |
|                | Baseline                                  | K1  | K2 K3               | K4  |         |
| Figure5:       | NumericalresultsfortheFetchroboticsystem. |     |                     |     |         |
Fetch
Experimental Setup. We provide the experimental results for the robotic system. This
robot has a 143-dimensional state space and a 10-dimensional control input space. To parametrize
each unknown term g we use a multilayer perceptron (MLP) with ReLu activation functions and
θi
twohiddenlayersof256nodeseach. Weusearollouthorizonofn r = 5todefinethelossfunction.
Furtherdetails,aswellastheexperimentalresultsfortheotherrobots,areprovidedintheextended
versionofthepaper(Djeumouetal.,2021).
Experimental Results. Figure 5 illustrates the results. Similarly to the double pendulum study,
weobservefromFigure5thatasweincreasetheamountofaprioriknowledgeincorporatedintothe
model,theaveragepredictionerrorcorrespondinglydecreases. Inparticular,theAvg. RolloutError
plot shows that by incorporating a priori knowledge of the mass matrix, (K2) consistently makes
moreaccuratepredictionsthaneitherthebaselineor(K1),regardlessofthenumberoftrajectories
included in the training dataset. From the Constraint Loss plot we observe a gap of four orders of
|     |     | (K3) (K4): |     |     |     |
| --- | --- | ---------- | --- | --- | --- |
magnitude between the constraint loss of and the proposed algorithm learns a model
thateffectivelyenforcesthecontactforceconstraintsincorporatedinto(K4).
5. RelatedWork
Techniquesfornonlinearsystemidentification–theconstructionofmathematicalmodelsofdynam-
icalsystemsfromempiricalobservations–oftenrelyonaprioriknowledgeofasuitablecollection
ofnonlinearbasisfunctions(Bruntonetal.,2016a,b;Williamsetal.,2014,2015). However,choos-
ingsuchsetsofbasisfunctionscanbechallenging,particularlyforsystemswithcomplexdynamics
andhigh-dimensionalstatespaces. Lietal.(2017);Takeishietal.(2017);Championetal.(2019);
Yeungetal.(2019)thususeneuralnetworkstolearnappropriatecollectionsofnonlinearfunctions
to be used in conjunction with these techniques. More closely related to our work, Raissi et al.
9

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
(2018);Luetal.(2018);Dupontetal.(2019);Kellyetal.(2020);Massarolietal.(2020)useneural
networks to represent differential equations. Chen et al. (2018) introduce the neural ODE; neural
networksparametrizingordinarydifferentialequations. However,theaboveworksdonotconsider
howphysics-basedknowledgemightbeincorporatedintoneuralnetworks, norhowphysics-based
constraintscanbeenforcedduringtraining. Thesearetheprimaryfocusesofthispaper.
Theinclusionofphysics-basedknowledgeinthetrainingofneuralnetworkshas,however,been
studied extensively over the past several years. In particular, Lu et al. (2021); Raissi et al. (2019);
Raissi (2018); Han et al. (2018); Sirignano and Spiliopoulos (2018); Long et al. (2018, 2019) use
neural networks for the solution and discovery of partial differential equations (PDE). Our work
insteadfocusesonusingneuralnetworkstoparametrizethevectorfieldofdynamicalsystems.
Morecloselyrelatedtoourwork,acollectionofrecentpapersstudyhowphysics-basedknowl-
edgecanbeincorporatedintoneuralnetworksforthelearningofdynamicsmodelsfromtrajectory
data (Zhong et al., 2021a; Herna´ndez et al., 2021; Rackauckas et al., 2020). Many of these works
either use the Lagrangian or the Hamiltonian formulation of dynamics to inform the structure of
a neural ODE, as in Cranmer et al. (2020); Lutter et al. (2019); Roehrl et al. (2020); Zhong and
Leonard(2020);Allen-Blanchetteetal.(2020)vs. Greydanusetal.(2019);Matsubaraetal.(2020);
Toth et al. (2020). Finzi et al. (2020) use the method of Lagrange multipliers to explicitly en-
forceholonomicconstraintsonthestatevariablesinLagrangianandHamiltonianneuralnetworks.
A number of works have also studied physics-informed neural ODEs in the context of learning
control-orienteddynamicsmodels(Zhongetal.,2020a,b;Roehrletal.,2020;DuongandAtanasov,
2021;Guptaetal.,2020;Mendaetal.,2019;Zhongetal.,2021b;Shietal.,2019). Wenotehowever,
that the majority of the above works employ a specific neural ODE structure, rendering them less
flexible than the general framework that we propose. Furthermore, the examples explored in these
workstypicallyfeaturelow-dimensionalstatespacesthatoftendonotincludeenergydissipationor
externalforces. Bycontrast, weapplytheproposedapproachtoavarietyofhigh-dimensionaland
complexsystems. Finally,theaboveworksdonotenforcegeneralphysics-basedconstraintsonthe
dynamicsmodel.
A number of other recent works have also studied imposing constraints on the outputs of deep
neuralnetworks(Ma´rquez-Neilaetal.,2017;Fiorettoetal.,2021;Nandwanietal.,2019;Kervadec
et al., 2019). Similarly to our work, Lu et al. (2021); Dener et al. (2020) consider an augmented
Lagrangian approach to the enforcement of physics-based constraints. However, they do so in dif-
ferentcontextsthanours;theformerfocusesonPDE-constrainedinversedesignproblemswhilethe
latterusesneuralnetworkstoapproximatetheFocker-Planckoperatorusedinfusionsimulations.
6. Conclusions
In this work we present a framework for the incorporation of a priori physics-based knowledge
into neural network models of dynamical systems. This physics based knowledge is incorporated
either by influencing the structure of the neural network, or as constraints on the model’s outputs
and internal states. We present a suite of numerical experiments that exemplify the effectiveness
of the proposed approach: the inclusion of increasingly detailed forms of side-information leads
to increasingly accurate model predictions. We also demonstrate that the framework effectively
enforces physics-based constraints on the outputs and internal states of the models. Future work
willaimtousethesephysics-informeddynamicsmodelsforcontrol.
10

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
Acknowledgments
ThisworkwassupportedinpartbyONRN00014-22-1-2254,AFOSRFA9550-19-1-0005,and
NSF1646522.
References
Christine Allen-Blanchette, Sushant Veer, Anirudha Majumdar, and Naomi Ehrich Leonard.
Lagnetvip: A lagrangian neural network for video prediction, 2020. URL https://arxiv.
org/abs/2010.12932.
StevenLBrunton,JoshuaLProctor,andJNathanKutz. Discoveringgoverningequationsfromdata
bysparseidentificationofnonlineardynamicalsystems. Proceedingsofthenationalacademyof
sciences,113(15):3932–3937,2016a.
StevenLBrunton,JoshuaLProctor,andJNathanKutz.Sparseidentificationofnonlineardynamics
withcontrol(sindyc). IFAC-PapersOnLine,49(18):710–715,2016b.
KathleenChampion,BethanyLusch,JNathanKutz,andStevenLBrunton. Data-drivendiscovery
ofcoordinatesandgoverningequations. ProceedingsoftheNationalAcademyofSciences,116
(45):22445–22451,2019.
Ricky T. Q. Chen, Yulia Rubanova, Jesse Bettencourt, and David K Duvenaud. Neural ordinary
differentialequations. InAdvancesinNeuralInformationProcessingSystems,volume31.Cur-
ran Associates, Inc., 2018. URL https://proceedings.neurips.cc/paper/2018/
file/69386f6bb1dfed68692a24c8686939b9-Paper.pdf.
Miles Cranmer, Sam Greydanus, Stephan Hoyer, Peter Battaglia, David Spergel, and Shirley Ho.
Lagrangianneuralnetworks,2020. URLhttps://arxiv.org/abs/2003.04630.
Alp Dener, Marco Andres Miller, Randy Michael Churchill, Todd Munson, and Choong-Seock
Chang. Training neural networks under physical constraints using a stochastic augmented la-
grangianapproach,2020. URLhttps://arxiv.org/abs/2009.07330.
Franck Djeumou, Cyrus Neary, Eric Goubault, Sylvie Putot, and Ufuk Topcu. Neural networks
withphysics-informedarchitecturesandconstraintsfordynamicalsystemsmodeling,2021.URL
https://arxiv.org/abs/2109.06407.
Yan Duan, Xi Chen, Rein Houthooft, John Schulman, and Pieter Abbeel. Benchmarking deep
reinforcementlearningforcontinuouscontrol. InInternationalconferenceonmachinelearning,
pages1329–1338.PMLR,2016.
ThaiDuongandNikolayAtanasov. Hamiltonian-basedneuralodenetworksonthese(3)manifold
fordynamicslearningandcontrol. InRobotics: ScienceandSystems(RSS),2021.
Emilien Dupont, Arnaud Doucet, and Yee Whye Teh. Augmented neural odes. In
Advances in Neural Information Processing Systems, volume 32. Curran Associates,
Inc., 2019. URL https://proceedings.neurips.cc/paper/2019/file/
21be9a4bd4f81549a9d1d241981cec3c-Paper.pdf.
11

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
Marc Finzi, Ke Alexander Wang, and Andrew G Wilson. Simplifying hamiltonian
and lagrangian neural networks via explicit constraints. In Advances in Neural
Information Processing Systems, volume 33, pages 13880–13889. Curran Associates,
Inc., 2020. URL https://proceedings.neurips.cc/paper/2020/file/
9f655cc8884fda7ad6d8a6fb15cc001e-Paper.pdf.
FerdinandoFioretto,PascalVanHentenryck,TerrenceW.K.Mak,CuongTran,FedericoBaldo,and
MicheleLombardi.Lagrangiandualityforconstraineddeeplearning.InYuxiaoDong,Georgiana
Ifrim, Dunja Mladenic´, Craig Saunders, and Sofie Van Hoecke, editors, Machine Learning and
Knowledge Discovery in Databases. Applied Data Science and Demo Track, pages 118–135,
Cham,2021.SpringerInternationalPublishing. ISBN978-3-030-67670-4.
C.DanielFreeman,ErikFrey,AntonRaichuk,SertanGirgin,IgorMordatch,andOlivierBachem.
Brax–adifferentiablephysicsengineforlargescalerigidbodysimulation,2021. URLhttps:
//arxiv.org/abs/2106.13281.
Samuel Greydanus, Misko Dzamba, and Jason Yosinski. Hamiltonian neural networks.
In Advances in Neural Information Processing Systems, volume 32. Curran Asso-
ciates, Inc., 2019. URL https://proceedings.neurips.cc/paper/2019/file/
26cd8ecadce0d4efd6cc8a8725cbd1f8-Paper.pdf.
Jayesh K Gupta, Kunal Menda, Zachary Manchester, and Mykel Kochenderfer. Structured me-
chanical models for robot learning and control. In Learning for Dynamics and Control, pages
328–337.PMLR,2020.
JiequnHan,ArnulfJentzen,andEWeinan. Solvinghigh-dimensionalpartialdifferentialequations
using deep learning. Proceedings of the National Academy of Sciences, 115(34):8505–8510,
2018.
Quercus Herna´ndez, Alberto Bad´ıas, David Gonza´lez, Francisco Chinesta, and El´ıas Cueto.
Structure-preservingneuralnetworks. JournalofComputationalPhysics,426:109950,2021.
Magnus R Hestenes. Multiplier and gradient methods. Journal of optimization theory and
applications,4(5):303–320,1969.
Jacob Kelly, Jesse Bettencourt, Matthew J Johnson, and David K Duvenaud. Learn-
ing differential equations that are easy to solve. In Advances in Neural Information
Processing Systems, volume 33, pages 4370–4380. Curran Associates, Inc.,
2020. URL https://proceedings.neurips.cc/paper/2020/file/
2e255d2d6bf9bb33030246d31f1a79ca-Paper.pdf.
Hoel Kervadec, Jose Dolz, Jing Yuan, Christian Desrosiers, Eric Granger, and Ismail Ben Ayed.
Constrained deep networks: Lagrangian optimization via log-barrier extensions, 2019. URL
https://arxiv.org/abs/1904.04205.
Qianxiao Li, Felix Dietrich, Erik M Bollt, and Ioannis G Kevrekidis. Extended dynamic mode
decomposition with dictionary learning: A data-driven adaptive spectral decomposition of the
koopman operator. Chaos: An Interdisciplinary Journal of Nonlinear Science, 27(10):103111,
2017.
12

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
Zichao Long, Yiping Lu, Xianzhong Ma, and Bin Dong. Pde-net: Learning pdes from data. In
InternationalConferenceonMachineLearning,pages3208–3216.PMLR,2018.
Zichao Long, Yiping Lu, and Bin Dong. Pde-net 2.0: Learning pdes from data with a numeric-
symbolichybriddeepnetwork. JournalofComputationalPhysics,399:108925,2019.
LuLu,RaphaelPestourie,WenjieYao,ZhichengWang,FrancescVerdugo,andStevenGJohnson.
Physics-informed neural networks with hard constraints for inverse design. SIAM Journal on
ScientificComputing,43(6):B1105–B1132,2021.
Yiping Lu, Aoxiao Zhong, Quanzheng Li, and Bin Dong. Beyond finite layer neural networks:
Bridgingdeeparchitecturesandnumericaldifferentialequations. InInternationalConferenceon
MachineLearning,pages3276–3285.PMLR,2018.
Michael Lutter, Christian Ritter, and Jan Peters. Deep lagrangian networks: Using physics as
model prior for deep learning. In International Conference on Learning Representations. Open-
Review.net,2019. URLhttps://openreview.net/forum?id=BklHpjCqKm.
Stefano Massaroli, Michael Poli, Jinkyoo Park, Atsushi Yamashita, and Hajime Asama. Dissect-
ing neural odes. In Advances in Neural Information Processing Systems, volume 33, pages
3952–3963. Curran Associates, Inc., 2020. URL https://proceedings.neurips.cc/
paper/2020/file/293835c2cc75b585649498ee74b395f5-Paper.pdf.
TakashiMatsubara,AiIshikawa,andTakaharuYaguchi. Deepenergy-basedmodelingofdiscrete-
time physics. In Advances in Neural Information Processing Systems, volume 33, pages
13100–13111. Curran Associates, Inc., 2020. URL https://proceedings.neurips.
cc/paper/2020/file/98b418276d571e623651fc1d471c7811-Paper.pdf.
Kunal Menda, Jayesh K Gupta, Zachary Manchester, and Mykel J Kochenderfer. Structured me-
chanical models for efficient reinforcement learning. In Workshop on Structure and Priors in
ReinforcementLearning,InternationalConferenceonLearningRepresentations,pages138–171,
2019.
PabloMa´rquez-Neila, MathieuSalzmann, andPascalFua. Imposinghardconstraintsondeepnet-
works: Promisesandlimitations,2017. URLhttps://arxiv.org/abs/1706.02025.
Yatin Nandwani, Abhishek Pathak, Mausam, and Parag Singla. A primal dual formulation for
deep learning with constraints. In Advances in Neural Information Processing Systems, vol-
ume 32. Curran Associates, Inc., 2019. URL https://proceedings.neurips.cc/
paper/2019/file/cf708fc1decf0337aded484f8f4519ae-Paper.pdf.
Christopher Rackauckas, Yingbo Ma, Julius Martensen, Collin Warner, Kirill Zubov, Rohit Su-
pekar,DominicSkinner,AliRamadhan,andAlanEdelman. Universaldifferentialequationsfor
scientificmachinelearning,2020. URLhttps://arxiv.org/abs/2001.04385.
Maziar Raissi. Deep hidden physics models: Deep learning of nonlinear partial differential equa-
tions. TheJournalofMachineLearningResearch,19(1):932–955,2018.
13

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
Maziar Raissi, Paris Perdikaris, and George Em Karniadakis. Multistep neural networks for data-
driven discovery of nonlinear dynamical systems, 2018. URL https://arxiv.org/abs/
1801.01236.
Maziar Raissi, Paris Perdikaris, and George E Karniadakis. Physics-informed neural networks: A
deep learning framework for solving forward and inverse problems involving nonlinear partial
differentialequations. JournalofComputationalPhysics,378:686–707,2019.
ManuelARoehrl,ThomasARunkler,VeronikaBrandtstetter,MichelTokic,andStefanObermayer.
Modelingsystemdynamicswithphysics-informedneuralnetworksbasedonlagrangianmechan-
ics. IFAC-PapersOnLine,53(2):9195–9200,2020.
Guanya Shi, Xichen Shi, Michael O’Connell, Rose Yu, Kamyar Azizzadenesheli, Animashree
Anandkumar, Yisong Yue, and Soon-Jo Chung. Neural lander: Stable drone landing control
usinglearneddynamics. InInternationalConferenceonRoboticsandAutomation,pages9784–
9790,2019.
JustinSirignanoandKonstantinosSpiliopoulos.Dgm: Adeeplearningalgorithmforsolvingpartial
differentialequations. Journalofcomputationalphysics,375:1339–1364,2018.
NaoyaTakeishi, YoshinobuKawahara, andTakehisaYairi. Learningkoopmaninvariantsubspaces
for dynamic mode decomposition. In Advances in Neural Information Processing Systems,
volume 30. Curran Associates, Inc., 2017. URL https://proceedings.neurips.cc/
paper/2017/file/3a835d3215755c435ef4fe9965a3f2a0-Paper.pdf.
Peter Toth, Danilo J. Rezende, Andrew Jaegle, Se´bastien Racanie`re, Aleksandar Botev, and
Irina Higgins. Hamiltonian generative networks. In International Conference on Learning
Representations. OpenReview.net, 2020. URL https://openreview.net/forum?id=
HJenn6VFvB.
MarcToussaint. Anovelaugmentedlagrangianapproachforinequalitiesandconvergentany-time
non-centralupdates,2014. URLhttps://arxiv.org/abs/1412.4329.
Matthew O. Williams, Clarence W. Rowley, and Ioannis G. Kevrekidis. A kernel-based approach
to data-driven koopman spectral analysis, 2014. URL https://arxiv.org/abs/1411.
2260.
Matthew O Williams, Ioannis G Kevrekidis, and Clarence W Rowley. A data–driven approxima-
tion of the koopman operator: Extending dynamic mode decomposition. Journal of Nonlinear
Science,25(6):1307–1346,2015.
Enoch Yeung, Soumya Kundu, and Nathan Hodas. Learning deep neural network representations
forkoopmanoperatorsofnonlineardynamicalsystems. InAmericanControlConference,pages
4832–4839.IEEE,2019.
Yaofeng Desmond Zhong and Naomi Leonard. Unsupervised learning of lagrangian dy-
namics from images for prediction and control. In Advances in Neural Information
Processing Systems, volume 33, pages 10741–10752. Curran Associates, Inc.,
2020. URL https://proceedings.neurips.cc/paper/2020/file/
79f56e5e3e0e999b3c139f225838d41f-Paper.pdf.
14

PHYSICS-CONSTRAINEDNEURALODESFORDYNAMICALSYSTEMSMODELING
Yaofeng Desmond Zhong, Biswadip Dey, and Amit Chakraborty. Symplectic ode-net: Learning
hamiltonian dynamics with control. In International Conference on Learning Representations.
OpenReview.net,2020a. URLhttps://openreview.net/forum?id=ryxmb1rKDS.
Yaofeng Desmond Zhong, Biswadip Dey, and Amit Chakraborty. Dissipative symoden: Encoding
hamiltoniandynamicswithdissipationandcontrolintodeeplearning. InICLR2020Workshop
onIntegrationofDeepNeuralModelsandDifferentialEquations,2020b.
YaofengDesmondZhong,BiswadipDey,andAmitChakraborty.Benchmarkingenergy-conserving
neuralnetworksforlearningdynamicsfromdata. InLearningforDynamicsandControl,pages
1218–1229.PMLR,2021a.
YaofengDesmondZhong,BiswadipDey,andAmitChakraborty. Extendinglagrangianandhamil-
tonian neural networks with differentiable contact models, 2021b. URL https://arxiv.
org/abs/2102.06794.
15