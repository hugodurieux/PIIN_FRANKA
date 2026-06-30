Deep Lagrangian Networks for end-to-end learning of energy-based
|     |     |     |     | control |     | for under-actuated |               |     |     | systems       |     |     |     |     |
| --- | --- | --- | --- | ------- | --- | ------------------ | ------------- | --- | --- | ------------- | --- | --- | --- | --- |
|     |     |     |     | Michael |     | Lutter1,           | Kim Listmann2 |     | and | Jan Peters1,3 |     |     |     |     |
Abstract—Applying
|                     |     |          | Deep Learning   |          | to control | has      | a lot of |     |     |     |     |     |     |     |
| ------------------- | --- | -------- | --------------- | -------- | ---------- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- |
| potential           | for | enabling | the intelligent |          | design     | of robot | control  |     |     |     |     |     |     |     |
| laws. Unfortunately |     | common   | deep            | learning | approaches |          | to con-  |     |     |     |     |     |     |     |
trol,suchasdeepreinforcementlearning,requireanunrealistic
| amount | of interaction |     | with the | real system, |     | do not yield | any |     |     |     |     |     |     |     |
| ------ | -------------- | --- | -------- | ------------ | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
9102 guA 3  ]OR.sc[  2v98440.7091:viXra performanceguarantees,anddonotmakegooduseofextensive
| insights        | from        | control theory. | In        | particular,     | common | black-box  |         |     |     |     |     |     |     |     |
| --------------- | ----------- | --------------- | --------- | --------------- | ------ | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| approaches      | –           | that abandon    | all       | insight         | from   | control –  | are not |     |     |     |     |     |     |     |
| suitable        | for complex | robot           | systems.  |                 |        |            |         |     |     |     |     |     |     |     |
| We              | propose     | a deep          | control   | approach        | as     | a bridge   | between |     |     |     |     |     |     |     |
| the solid       | theoretical | foundations     |           | of energy-based |        | control    | and     |     |     |     |     |     |     |     |
| the flexibility |             | of deep         | learning. | To accomplish   |        | this goal, | we      |     |     |     |     |     |     |     |
extendDeepLagrangianNetworks(DeLaN)tonotonlyadhere
toLagrangianMechanicsbutalsoensureconservationofenergy
andpassivityofthelearnedrepresentation.Thisnovelextension
|             |     |          |        |         |     |            |        | Fig.         | 1. The | physical Cartpole         | and Furuta pendulum |      | used to | evaluate the |
| ----------- | --- | -------- | ------ | ------- | --- | ---------- | ------ | ------------ | ------ | ------------------------- | ------------------- | ---- | ------- | ------------ |
| is embedded |     | within a | energy | control | law | to control | under- |              |        |                           |                     |      |         |              |
|             |     |          |        |         |     |            |        | energy-based |        | control of under-actuated | systems             | with | learned | models. (a)  |
actuated systems. The resulting DeLaN for energy control The Cartpole consists of a horizontally moving cart driven by a rack and
(DeLaN 4EC) is the first model learning approach using pinion drive. The passive pendulum is attached to the cart and the cart
generic function approximation that is capable of learning the pendulum can be swung-up and balanced. The front (b) and top (c)
energy control because existing approaches cannot learn the view of the Furuta pendulum consisting of an actuated rotary pendulum
systemenergiesdirectly.DeLaN4ECexhibitsexcellentreal-time withapassiveverticalpendulum.Theverticalpendulumcanbeswung-up
andbalancedbymovingthehorizontalrotarylink.Videosfortheswing-up
controlonthephysicalFurutapendulumandlearnstoswing-up
usingthedifferentmodelsareavailableathttps://youtu.be/m3JRYq7Gmgo
| the pendulum |     | while the | control | law using | system | identification |     |     |     |     |     |     |     |     |
| ------------ | --- | --------- | ------- | --------- | ------ | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
does not.
I. Introduction
Controllawsareessentialtoachieveintelligentrobotsthat and require extensive reward shaping to the desired solution
enable industrial automation, human-robot interaction and [5] or random seeds [6].
locomotion. The common approach is to manually derive We propose to bridge this gap by combining the flexi-
the system dynamics, measure the masses, lengths, inertias bility of deep learning with the theoretical insights from
of the disassembled mechanical system [1] and finally use control theory in order to achieve learning of control that
| these | equations | to engineer |     | a control | law | for this | specific |     |             |                |            |     |      |          |
| ----- | --------- | ----------- | --- | --------- | --- | -------- | -------- | --- | ----------- | -------------- | ---------- | --- | ---- | -------- |
|       |           |             |     |           |     |          |          | is  | independent | of the system, | applicable | for | real | systems, |
system. Therefore, this engineering approach requires sig- cannot yield degenerate solutions and requires little engi-
nificant effort. In stark contrast, many learning to control neering. Therefore, we combine existing control laws for
approaches, such as Deep Reinforcement Learning [2], [3], energybasedcontrolwithmodellearning.Suchcombination
[4], try to learn the control law using black-box methods, cannot be achieved by standard black-box model learning
| and hence, | do  | not require | any | engineering |     | for the | specific |            |     |                     |         |       |         |       |
| ---------- | --- | ----------- | --- | ----------- | --- | ------- | -------- | ---------- | --- | ------------------- | ------- | ----- | ------- | ----- |
|            |     |             |     |             |     |         |          | techniques |     | [7], [8], [9], [10] | because | these | methods | learn |
system. These black-box methods abandon all insights from the mapping from joint state {q, q(cid:219), q(cid:220)} to motor torques
control and physics, require millions of samples from the , but cannot learn the underlying ODE1 nor the potential
τττ
M
physical systems, do not yield any performance guarantees and kinetic energies, because these components are not
|     |     |     |     |     |     |     |     | observable |                 | and hence, cannot | be learned | supervised. |     | Only    |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --------------- | ----------------- | ---------- | ----------- | --- | ------- |
|     |     |     |     |     |     |     |     | our        | novel extension | of Deep           | Lagrangian | Networks    |     | (DeLaN) |
ThisprojecthasreceivedfundingfromtheEuropeanUnion’sHorizon [12] is capable of learning the underlying ODE from data
2020researchandinnovationprogramundergrantagreementNo#640554 using the joint configurations and motor torques. Compared
| (SKILLS4ROBOTS). |     | Furthermore, |     | this research | was | also supported | by  |     |     |     |     |     |     |     |
| ---------------- | --- | ------------ | --- | ------------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
grantsfromABB,NVIDIAandtheNVIDIADGXStation. to the previous DeLaN, we extend DeLaN to also encode
1MichaelLutterandJanPetersarewiththeDepartmentofComputer energy conservation and coherence besides the Lagrangian
Science, Technische Universität Darmstadt, 64289 Darmstadt, Germany Mechanics prior. Therefore, our novel extension of DeLaN
| {lutter, | peters}@ias.tu-darmstadt.de |     |     |     |     |     |     |     |     |     |     |     |     |     |
| -------- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2Kim learnsthemass-matrix,thecentrifugal,Coriolis,gravitational
|          | Listmann    | is  | with     | ABB Corporate |            | Research | Center  |     |     |     |     |     |     |     |
| -------- | ----------- | --- | -------- | ------------- | ---------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| Germany, | Wallstadter |     | Str. 59, | 68526         | Ladenburg, |          | Germany |     |     |     |     |     |     |     |
kim.listmann@de.abb.com 1One can also not infer the components of the ODE using the Com-
3Jan Peters is with the Max Planck Institute for Intel- posite Rigid body algorithm [11] in combination with the learned inverse
ligent Systems, Spemannstr. 41, 72076 Tübingen, Germany dynamicsmapping,becausetheblack-boxfunctionapproximationviolates
| jan.peters@tuebingen.mpg.de |     |     |     |     |     |     |     | theunderlyingassumptions. |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- |

and frictional forces as well as the potential and kinetic under-actuated systems have been proposed [16], [17], [18],
energy using unsupervised learning. Hence, DeLaN enables [19]. These papers manually derive the dynamics for each
the combination of energy control with learned models system using Lagrangian Mechanics and use the specific
withouttheknowledgeofthesystemkinematics,whichmust equations to derive control laws. For the resulting control
be known for standard system identification techniques [13]. laws the stability can be analyzed and guaranteed given
In the following we will refer to this combination as DeLaN the true model [18]. Therefore, the control laws achieve
for energy control (DeLaN 4EC) the desired behaviour and cannot exploit ill-posed reward
To demonstrate the performance, we apply DeLaN 4EC functionsbutrequireengineeringofthedynamicsandcontrol
under-actuated systems. This control problem is challenging law. With DeLaN 4EC we use the control perspective and
as the controller must exploit the inherent system dynamics embed a control law within a learning architecture to learn
to solve the task and cannot use high-gain feedback control thecompletecontrolapproach.Ratherthanusingthespecific
to cancel the system dynamics. For example the swing-up system dynamics for deriving the control law, we use the
task of the Cartpole and the Furuta pendulum requires the generic Euler-Lagrange ODE, which describes any mechan-
|          |               |     |        |           |     |             |      | ical system | including | closed-loop |     | kinematics, |     | and learn the |
| -------- | ------------- | --- | ------ | --------- | --- | ----------- | ---- | ----------- | --------- | ----------- | --- | ----------- | --- | ------------- |
| repeated | amplification |     | of the | amplitude | of  | the passive | pen- |             |           |             |     |             |     |               |
dulum before the pendulum can be swung-up. Furthermore, ODE describing the model from data.
| these tasks | are | a standard | evaluation |     | task | for learning | for |          |           |     |           |     |      |              |
| ----------- | --- | ---------- | ---------- | --- | ---- | ------------ | --- | -------- | --------- | --- | --------- | --- | ---- | ------------ |
|             |     |            |            |     |      |              |     | Learning | the model |     | from data | has | been | addressed in |
control [14]. In contrast to most previous research, we apply the literature by either system identification or supervised
thecontrollawsalsotothephysicalFurutapendulum(Figure black-box function approximation. For system identification
| 1) and learn | the | control | without | pre-training |     | in simulation. |     |               |         |               |            |           |     |                |
| ------------ | --- | ------- | ------- | ------------ | --- | -------------- | --- | ------------- | ------- | ------------- | ---------- | --------- | --- | -------------- |
|              |     |         |         |              |     |                |     | the knowledge | of      | the kinematic |            | structure | is  | exploited such |
|              |     |         |         |              |     |                |     | that the      | linkage | physics       | parameters | can       | be  | inferred using |
Contribution
linearregression[13].However,thelearnedparametersmust
The contribution of this paper is the novel extension of not necessarily be physically plausible [20], can only be
DeLaN and the combination of DeLaN and energy control linear combinations and can only be applied to kinematic
| (DeLaN | 4EC) for | controlling |     | under-actuated |     | systems. | First, |             |                |     |      |               |     |            |
| ------ | -------- | ----------- | --- | -------------- | --- | -------- | ------ | ----------- | -------------- | --- | ---- | ------------- | --- | ---------- |
|        |          |             |     |                |     |          |        | trees [21]. | In combination |     | with | the composite |     | rigid body |
we extend DeLaN to incorporate energy conservation and algorithm [11] the parameters of the Euler-Lagrange ODE
| frictional | forces. | Therefore, |     | the extended |     | DeLaN | not only |           |                 |     |     |              |     |              |
| ---------- | ------- | ---------- | --- | ------------ | --- | ----- | -------- | --------- | --------------- | --- | --- | ------------ | --- | ------------ |
|            |         |            |     |              |     |       |          | including | the mass-matrix |     | can | be inferred. | For | the function |
adherestotheLagrangianMechanicsbutalsoensuresenergy approximations standard machine learning techniques such
conservation, temporal coherence of the energy and the pas- asLinearRegression[7],[22],GaussianMixtureRegression
| sivity of | the learned | representation. |     |     | Second, | we demonstrate |     |             |          |         |     |            |       |            |
| --------- | ----------- | --------------- | --- | --- | ------- | -------------- | --- | ----------- | -------- | ------- | --- | ---------- | ----- | ---------- |
|           |             |                 |     |     |         |                |     | [23], [24], | Gaussian | Process |     | Regression | [25], | [9], [26], |
that this combination can achieve energy-control for the SupportVectorRegression[8],[27],feedforward-[28],[29],
Cartpole and the Furuta pendulum. This is demonstrated [30], [10] or recurrent neural networks [31] have been used.
in simulation and on the physical Furuta pendulum in real- These models learn the forward or inverse mapping from
time at 500Hz and without pre-training in simulation. The joint configuration {q, q(cid:219), q(cid:220)} to motor torque . Therefore,
|             |     |          |     |     |          |        |        |               |        |        |     |         | τττ   | M              |
| ----------- | --- | -------- | --- | --- | -------- | ------ | ------ | ------------- | ------ | ------ | --- | ------- | ----- | -------------- |
| performance | is  | compared | to  | the | analytic | models | of the |               |        |        |     |         |       |                |
|             |     |          |     |     |          |        |        | these learned | models | cannot | be  | used to | infer | the parameters |
manufacturer as well as the standard system identification of the Euler-Lagrange ODE and do not allow a combination
approach [13]. withclassicalcontrolbesidesinversedynamicsornon-linear
| In the        | following | we        | provide   | an       | overview   | about      | related |              |          |          |     |          |       |            |
| ------------- | --------- | --------- | --------- | -------- | ---------- | ---------- | ------- | ------------ | -------- | -------- | --- | -------- | ----- | ---------- |
|               |           |           |           |          |            |            |         | feed-forward | control  | [26].    |     |          |       |            |
| work (Section | II),      | briefly   | summarize |          | Deep       | Lagrangian | Net-    |              |          |          |     |          |       |            |
|               |           |           |           |          |            |            |         | In contrast  | to these | existing |     | methods, | DeLaN | learns the |
| works [12]    | and       | highlight | the       | proposed | extensions |            | to this |              |          |          |     |          |       |            |
Euler-LagrangeODEdirectlyfromdata,doesnotrequireany
approach(SectionIII).Subsequently,wederiveourproposed knowledge of the kinematic structure and is not restricted to
| control   | approach,        | DeLaN | for     | energy | control  | (DeLaN | 4EC)     |           |                   |     |       |        |     |              |
| --------- | ---------------- | ----- | ------- | ------ | -------- | ------ | -------- | --------- | ----------------- | --- | ----- | ------ | --- | ------------ |
|           |                  |       |         |        |          |        |          | kinematic | trees. Therefore, |     | DeLaN | learns | the | mass matrix, |
| and state | the energy-based |       | control | law    | (Section | IV).   | Finally, |           |                   |     |       |        |     |              |
thecentrifugal-,Coriolis-,gravitational-andfrictionalforces
the experiments in Section V evaluate the control perfor- aswellasthesystemenergyusingunsupervisedlearningand
| mance for | simulated | and | physical    | under-actuated |     | systems. |     |                |      |         |         |     |     |     |
| --------- | --------- | --- | ----------- | -------------- | --- | -------- | --- | -------------- | ---- | ------- | ------- | --- | --- | --- |
|           |           |     |             |                |     |          |     | fits naturally | with | control | theory. |     |     |     |
|           |           | II. | RelatedWork |                |     |          |     |                |      |         |         |     |     |     |
Controlling under-actuated systems has been addressed III. DeepLagrangianNetworks
| from various | perspectives |     | including |     | reinforcement |     | learning |     |     |     |     |     |     |     |
| ------------ | ------------ | --- | --------- | --- | ------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
and control theory. For reinforcement learning the swing-up FirstinSectionIII-A,theconceptofDeepLagrangianNet-
ofpassivependulumsisastandardbenchmarkforcontinuous works[12]issummarizedandnovelextensionsareproposed
state- and action spaces. These methods learn the control in the subsequent sections. Section III-B extends the cost
policy by treating the control task as black-box and improve function with the forward model. Section III-C introduces
the policy using only scalar rewards as feedback. However, friction such that the Lagrangian Mechanics prior is not
most reinforcement learning algorithms can only be used in violated. Finally, section III-D adds energy conservation as
simulation due to the high sample complexity. Only PILCO additional constraint to model learning. Thus, the extended
[15] learned the Cartpole swing-up on the physical system. DeLaN not only complies with Lagrangian Mechanics but
From a control perspective many control laws for specific also ensures energy conservation and coherence.

Fig.2. ThecomputationalgraphoftheDeepLagrangianNetworkforcontrol(DeLaN4EC).Showninblueandgreenistheneuralnetworkwiththethree
separate heads computing the potential energyV and the mass-matrix H. The orange boxes construct represent the physics transformations constructing
Euler-Lagrangeequation.Forenergy-basedcontrolthesecomponentsaredirectlyinterfacedtothecontrollawtodeterminethemotor-torque.Fortraining,
thegradientsarebackpropagatedthroughallverticeshighlightedinorange.
A. Deep Lagrangian Networks including energy control, as these use the inverse of the
mass matrix. Therefore, incorporating the forward model
Deep Lagrangian Networks use the knowledge from La-
within the learning of the parameters should yield better
grangian Mechanics and encode this prior within a deep
learningarchitecture.Therefore,alllearnedmodelsguarantee
approximationoftheinverse.SolvingEquation1forq(cid:220) yields
t M ha o t re th c e o s n e c m re o te d l e y l , s le m t u th st e c L o a m g p ra ly ng w ia it n h b L e a d g e ra fi n n g e i d an as M L e = ch T an − ic V s , . H−1(q) (cid:32) (cid:213) τττ −H(cid:219)(q)q(cid:219)+ 1 (cid:18) ∂ (cid:16) q(cid:219)TH(q)q(cid:219) (cid:17) (cid:19)T − ∂V (cid:33) =q(cid:220).
i 2 ∂q ∂q
whereT=1/2q(cid:219)TH(q)q(cid:219) isthekineticenergy,V thepotential
i
energy and H the positive definite mass matrix. Substituting Thusthelossfunctioncanbeextendedtominimizetheerror
L into the Euler-Lagrange differential equation yields the of the inverse and forward model, i.e.,
ODE described by
(θ∗,ψ∗)=argmin(cid:96) (cid:16) f ˆ (θ,ψ), q(cid:220) (cid:17) +
H(q)q(cid:220)+H(cid:219)(q)q(cid:219)− 1 (cid:18) ∂ (cid:16) q(cid:219)TH(q)q(cid:219) (cid:17) (cid:19)T + ∂V = (cid:213) τττ (1) θ,ψ i (3)
(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32) 2 (cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32) ∂ (cid:32)(cid:32) q (cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32) ∂q i i (cid:96) i (cid:16) f ˆ−1(θ,ψ), τττ M (cid:17) +λΩ(θ,ψ)
(cid:124) (cid:123)(cid:122) (cid:125)
(cid:66)C(q,q(cid:219))q(cid:219) where Ω is the l2 weight regularization.
where τττ are the non-conservative generalized forces includ-
i
ing motor and frictional forces. Approximating H and V C. Introducing Friction to Model Learning
using deep networks, i.e., Incorporating friction within model learning in a non
black-box fashion is non-trivial because friction is an ab-
Hˆ =Lˆ (q;θ)LˆT (q;θ)+(cid:15)I V ˆ =V ˆ (q;ψ) (2) stractionto combinevariousphysical effects.Forrobot arms
in free space the friction of the motors dominates, for
where ˆ. refers to an approximation, Lˆ is a lower triangular
mechanical systems dragging along a surface the friction
matrixwithanon-negativediagonal,θ andψ arethenetwork
at surface dominates while for legged locomotion the fric-
parameters and (cid:15) a small positive constant, one can encode
tion between the feet and floor dominates but also varies
the ODE by exploiting the full differentiability of the neural
with time. Therefore, defining a general case for all types
networks[12].Additionally,themassmatrixHisguaranteed
of friction in compliance with the Lagrangian Mechanics
tobepositivedefiniteandtheeigenvaluesarelower-bounded
is challenging. Various approaches to incorporate friction
by (cid:15). The network parameters can be learned online and
modelscanbefoundin[32],[33].Furthermore,ifthefriction
end-to-end, by minimizing the error of the ODE using the
model includes stiction the dynamics are not invertible
samples {q,q(cid:219),q(cid:220),τττ } recorded on the physical system, i.e.
M because multiple motor-torques can generate the same joint
minimizingthe(cid:96) normbetweenthepredictionofEquation1
i acceleration [34].
and the observed motor torque τττ . Therefore, the super-
M This paper focuses on friction caused by the actuators.
position of the different forces is learned supervised, while
For actuator friction different models have been proposed
the decomposition into inertial, Coriolis, centripetal and
[35], [1], [36], [37]. These models assume that the motor
gravitational forces is learned unsupervised.
friction only depends on the joint velocity q(cid:219) of theith-joint
i
B. Introducing the Forward Model and is independent of the other joints [35], [1], [36], [37].
Depending on model complexity a combination of static,
Unlike many model learning techniques, DeLaN can be
viscous or Stribeck friction is assumed as model prior and
used as forward and inverse dynamics model, by solving
the superposition is described by
Equation 1 w.r.t. q(cid:220). Therefore, one can incorporate the loss
of the forward model within the learning of the parameters. (cid:16) (cid:16) (cid:17)(cid:17)
τττ =− τ +τ exp −q(cid:219)2/ν sign(q(cid:219) )−dq(cid:219) (4)
This is especially important for many control approaches, fi Cv Cs i i i

whereτ isthecoefficientofstaticfriction,d thecoefficient The resulting equations cannot be directly used as a loss
Cv
of viscous friction, and τ and ν are the coefficients of because the true kinetic- and potential energy of the con-
Cs
S ab tr b i r b e e v c i k at f e r d ic a ti s on φ . = In { t τ he , fo τ llo , w ν i , n d g } t . h S e i f n r c ic e ti t o h n e c fr o i e c ffi tio c n ie a n l t f s or a c r e e fi cu g r u r r e a n t t io a n pp q ro t+ x δ i t ma is tio u n nk o n f o V ˜ w a n n . d T T ˜ he a r s ef t o a r r e g , et w v e alu b e oo a t n s d tra d p o n th o e t
Cv Cs
τττ isafunctionofthegeneralizedcoordinates,thefrictional propagate the gradients through these estimates. In addition,
f
force is a non-conservative and generalized force and can the energy for a specific joint configuration q∗ is clamped to
simply be added to the Lagrange Euler ODE (Equation 1). a pre-specified value as in [38], i.e. E(q∗,q(cid:219)∗)(cid:66)0. Adding
For other types of friction this is not true and one needs energy conservation (Equation 7) and energy coherence
to explicitly ensure that one can express the frictional force (Equation 8 & Equation 9) to the optimization problem of
as generalized force. Given the model prior of Equation 4 Equation 3 yields the loss for DeLaN 4EC.
the friction coefficients φ can be learned by treating the
IV. DeepLagrangianNetworksforEnergyControl
coefficients as network weights.
In the previous section, we showed that DeLaN can learn
D. Introducing Energy to Model Learning
the mass matrix, the centripetal, gravitational and frictional
Besides the Lagrangian Mechanics objective, incorporat-
forces as well as the kinetic and potential energies using
ingenergyconservationandenergycoherence,i.e.,ensuring
onlythejointmeasurements(q,q(cid:219),q(cid:220))andtheactuatortorques
that E i (t)∀t≥0isatleastofClassC2,isnaturalbecausethe τττ . Using these properties, energy control can be achieved
M
Lagrangian L contains the system energy. In order to ensure by embedding the learned energies within a energy-based
the conservation of energy, the total energy of the system
control law. Therefore, DeLaN 4EC enables the control of a
must be equal to the summation of the initial system energy
large-class of under-actuated systems, because these systems
E0 ,theworkdonebytheactuatorsW m andtheenergylosses are mainly controlled using energy-based control laws and
due to friction E th , i.e., other black-box identification techniques cannot learn the
E(t)=T(t)+V(t)=E0 +W
M
(t)+E
th
(t) ∀t ≥0. (5) system energy and hence, cannot be applied . For energy
control,thecontrollawproposedbySponget.al.[17],which
The actuator work or the losses to friction can be computed
is applicable to the Furuta pendulum, the Cartpole and the
by numerical integration described by
Acrobot is used. This control law regulates the energy of
∫ q(t) ∫ t the pendulum E to obtain the desired energy E∗ and adds
W j (t)= τττT j (q) dq= τττT j (q(u))q(cid:219)(u) du (6) an additional P- p controller on the active joints to avoid the
q(0) 0
jointlimits.Forsystemswithhighfrictionanadditionalterm
where τττ iseitherthefrictionaltorque τττ oractuatortorque
j F to compensate the friction of the actuator can be added.
τττ and W (0)(cid:66)0. This can also be expressed in using the
M j Expressing this control law using the mass-matrix and the
change in energy, i.e.,
potential energy is described by
E(cid:219) =q(cid:219)T(τττ +τττ )=T(cid:219)+V(cid:219)
M F 1 ∂V (7) u E =k E (cid:0) E p −E∗(cid:1) sign(cid:0) q(cid:219) p cos(q p (cid:1)+K p (cid:0) q∗ a −q a (cid:1) (10)
=q(cid:219)THq(cid:220)+ q(cid:219)TH(cid:219) q(cid:219)+q(cid:219)T .
2 ∂q with the pendulum energy E
p
=1/8 q(cid:219)T
p
H22q(cid:219)
p
+V(q) and
Following[21]andrecognizingthatτττ +τττ isthetotalforce the desired energy E∗(q∗,q(cid:219)∗) at the desired joint configura-
M F
actingonthemechanicalsystem,Equation7notonlyensures tion q∗.
energy conservation but also the passivity of the learned
V. Experiments
system,becausethisequalityensuresthelowerboundonthe
We apply DeLaN 4EC to control two under-actuated
total energy, i.e., E(T)−E(0)≥−E(0) ∀T >0. Therefore,
systems: the Cartpole (Figure 1a) and the Furuta pendulum
the learned model representation is guaranteed to be passive
(Figure 1b). The Cartpole is a horizontally moving cart with
on the training domain given sufficiently low training error.
an attached passive pendulum. Moving the cart horizontally
ThispropertyofDeLaNimpliesthattheuncontrolledsystem
indirectly controls the pendulum and using this indirect con-
described by the learned dynamics is stable. For black-box
trol the pendulum can be swung-up and balanced. Similarly,
functionapproximationmethodsthismustnotbenecessarily
theFurutapendulum(alsoreferredtoaswhirlingpendulum)
be true because these methods can learn an active system
consists of an actuated rotary pendulum with a vertical
that is optimal w.r.t. the given cost function. Besides the
passive pendulum. Using the rotary pendulum the vertical
conservation of energy, the energy coherence can be used
link can be swung-up and balanced. These experiments are
as additional constraint ensuring that both the kinetic and
standard experiments for learning to control. However, most
potential energy is continuous and differentiable w.r.t. time,
i.e., T,V ∈C1. Using a first order Taylor approximation this previousresearchonlyusedsimulationswhileweapplythese
methods to the physical Cartpole and Furuta pendulum.
constraint can be expressed as
1
T ˜ (q t+δt ;θ)=T ˆ (q t ;ψ)+q(cid:219)T t Hq(cid:220) t δ t + 2 q(cid:219)T t H(cid:219) q(cid:219)T t δ t (8) A. Experimental Setup
Tolearnthecontroltask,asmoothexplorationpolicy,i.e.,
ˆ
V ˜ (q t+δt ;ψ)=V ˆ (q t ;ψ)+q(cid:219)T t ∂ ∂ V q δ t . (9) T the se e c n o e n rg d y s c w o i n th tro t l h le e r s u y s s i t n e g m th a e nd an g a e ly n t e ic ra m tes od d e a l, ta in c te o r n a t c a t i s ni f n o g r

|     | ×101 τM | ×101 q¨ | ×101 | H(q)q¨ | c(q,q˙) |     | ×10−1 | g(q) |      | τF  |     | ×10−1 | Ekin |
| --- | ------- | ------- | ---- | ------ | ------- | --- | ----- | ---- | ---- | --- | --- | ----- | ---- |
|     |         | +3.0    |      |        |         |     | +7.5  |      |      |     |     |       |      |
|     |         |         | +1.0 | +2.0   |         |     | +5.0  |      | +4.0 |     |     |       |      |
]2s/m[noitareleccA +2.0
]mN[euqroT +1.0 ]mN[euqroT +0.5 ]mN[euqroT +1.0 ]mN[euqroT +2.5 ]mN[euqroT +2.0 ]J[ygrenE +4.0
| 0tnioJ            |      | +1.0 |      |      |     |     |      |     |      |     |     |      |     |
| ----------------- | ---- | ---- | ---- | ---- | --- | --- | ---- | --- | ---- | --- | --- | ---- | --- |
|                   |      | +0.0 | +0.0 | +0.0 |     |     | +0.0 |     | +0.0 |     |     |      |     |
|                   | +0.0 |      |      |      |     |     |      |     |      |     |     | +2.0 |     |
| eloptraCdetalumiS |      | −1.0 | −0.5 | −1.0 |     |     | −2.5 |     | −2.0 |     |     |      |     |
|                   |      |      | −1.0 |      |     |     | −5.0 |     |      |     |     |      |     |
|                   |      | −2.0 |      | −2.0 |     |     |      |     | −4.0 |     |     |      |     |
|                   | −1.0 |      |      |      |     |     | −7.5 |     |      |     |     | +0.0 |     |
t0 τM tN t0 q¨ tN t0 H(q)q¨ tN t0 c(q,q˙) tN t0 g(q) tN t0 τF tN t0 Epot tN
+7.5 ×10−1 ×102 +7.5 ×10−1 +7.5 ×10−1 +7.5 ×10−1 +7.5 ×10−1 ×10−1
|        |            | +1.0               |            |            |     |            |      |     |            |     |           | +0.0 |     |
| ------ | ---------- | ------------------ | ---------- | ---------- | --- | ---------- | ---- | --- | ---------- | --- | --------- | ---- | --- |
|        | +5.0       | ]2s/m[noitareleccA | +5.0       | +5.0       |     |            | +5.0 |     | +5.0       |     |           |      |     |
|        | ]mN[euqroT |                    | ]mN[euqroT | ]mN[euqroT |     | ]mN[euqroT |      |     | ]mN[euqroT |     |           | −1.0 |     |
| 1tnioJ | +2.5       | +0.5               | +2.5       | +2.5       |     |            | +2.5 |     | +2.5       |     | ]J[ygrenE |      |     |
|        | +0.0       |                    | +0.0       | +0.0       |     |            | +0.0 |     | +0.0       |     |           | −2.0 |     |
|        | −2.5       | +0.0               | −2.5       | −2.5       |     |            | −2.5 |     | −2.5       |     |           | −3.0 |     |
|        | −5.0       |                    | −5.0       | −5.0       |     |            | −5.0 |     | −5.0       |     |           |      |     |
|        |            | −0.5               |            |            |     |            |      |     |            |     |           | −4.0 |     |
−7.5 t0 tN t0 tN −7.5 t0 tN −7.5 t0 tN −7.5 t0 tN −7.5 t0 tN t0 tN
|     | τM  |     |     |     |     |     |     |     |     | τF  |     |     | Ekin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
×101 +2.0 ×101 q¨ ×101 H(q)q¨ c(q,q˙) +7.5 ×10−1 Data g(q) AnalyticalModel ×101 SystemIdentification ×10−1 DeLaN
|     |      |                    | +2.0 |      |     |     |      |     | +1.5 |     |     |      |     |
| --- | ---- | ------------------ | ---- | ---- | --- | --- | ---- | --- | ---- | --- | --- | ---- | --- |
|     | +1.0 | ]2s/m[noitareleccA |      | +5.0 |     |     | +5.0 |     |      |     |     | +8.0 |     |
|     |      |                    | +1.0 |      |     |     |      |     | +1.0 |     |     |      |     |
0tnioJ ]mN[euqroT +0.0 +0.0 ]mN[euqroT ]mN[euqroT +2.5 ]mN[euqroT +2.5 ]mN[euqroT +0.5 ]J[ygrenE +6.0
|                  |      |       | +0.0  | +0.0  |     |     |         |     |       |     |     |      |     |
| ---------------- | ---- | ----- | ----- | ----- | --- | --- | ------- | --- | ----- | --- | --- | ---- | --- |
|                  | −1.0 |       |       |       |     |     | +0.0    |     | +0.0  |     |     | +4.0 |     |
|                  | −2.0 | −2.0  | −1.0  | −2.5  |     |     | −2.5    |     |       |     |     |      |     |
|                  |      |       |       |       |     |     |         |     | −0.5  |     |     | +2.0 |     |
| eloptraClacisyhP | −3.0 |       | −2.0  | −5.0  |     |     | −5.0    |     |       |     |     |      |     |
|                  |      | −4.0  |       |       |     |     |         |     | −1.0  |     |     | +0.0 |     |
|                  | t0   | tN t0 | tN t0 | tN t0 |     | tN  | −7.5 t0 |     | tN t0 |     | tN  | t0   | tN  |
×10−1 τM ×102 q¨ ×10−1 H(q)q¨ ×10−1 c(q,q˙) ×10−1 g(q) ×10−1 τF ×10−1 Epot
|     | +7.5 |                         | +7.5 | +7.5 |     |     | +7.5 |     | +7.5 |     |     | +0.0 |     |
| --- | ---- | ----------------------- | ---- | ---- | --- | --- | ---- | --- | ---- | --- | --- | ---- | --- |
|     | +5.0 | ]2s/m[noitareleccA +0.5 | +5.0 | +5.0 |     |     | +5.0 |     | +5.0 |     |     | −1.0 |     |
]mN[euqroT +2.5 +0.0 ]mN[euqroT +2.5 ]mN[euqroT +2.5 ]mN[euqroT +2.5 ]mN[euqroT +2.5
| 1tnioJ |      |      |      |      |     |     |      |     |      |     | ]J[ygrenE | −2.0 |     |
| ------ | ---- | ---- | ---- | ---- | --- | --- | ---- | --- | ---- | --- | --------- | ---- | --- |
|        | +0.0 | −0.5 | +0.0 | +0.0 |     |     | +0.0 |     | +0.0 |     |           |      |     |
−3.0
|     | −2.5 | −1.0 | −2.5 | −2.5 |     |     | −2.5 |     | −2.5 |     |     |     |     |
| --- | ---- | ---- | ---- | ---- | --- | --- | ---- | --- | ---- | --- | --- | --- | --- |
−4.0
|     | −5.0 | −1.5  | −5.0  | −5.0  |     |     | −5.0 |                 | −5.0  |     |                      | −5.0 |       |
| --- | ---- | ----- | ----- | ----- | --- | --- | ---- | --------------- | ----- | --- | -------------------- | ---- | ----- |
|     | −7.5 |       | −7.5  | −7.5  |     |     | −7.5 |                 | −7.5  |     |                      |      |       |
|     | t0   | tN t0 | tN t0 | tN t0 |     | tN  | t0   |                 | tN t0 |     | tN                   | t0   | tN    |
|     |      |       |       |       |     |     | Data | AnalyticalModel |       |     | SystemIdentification |      | DeLaN |
Fig. 3. The motor-, centrifugal-, Coriolis-, gravitational- and frictional forces, the joint acceleration as well as the kinetic and potential energy for the
swing-up of the simulated and physical Cartpole. Using only the super-imposed motor torques and joint accelerations as supervising feedback, DeLaN
learnstodisambiguatebetweentheindividualforcecomponentsandsystemenergies.
|     |     |     |     |     | up           | task the      | systems      | are         | first stabilized |               | to the | desired          | energy    |
| --- | --- | --- | --- | --- | ------------ | ------------- | ------------ | ----------- | ---------------- | ------------- | ------ | ---------------- | --------- |
|     |     |     |     |     | E∗           | of the        | balancing    | point       | using            | energy        |        | control          | and then  |
|     |     |     |     |     | balanced     |               | at the       | unstable    | equilibrium      |               | using  | a PD-controller. |           |
|     |     |     |     |     | Both,        | controller    |              | operate     | at 500Hz         | and           | the    | gains            | are tuned |
|     |     |     |     |     | for          | each          | system       | using       | the analytic     |               | model  | provided         | by the    |
|     |     |     |     |     | manufacturer |               | and          | fixed       | afterwards       | for           | each   | experiment.      |           |
|     |     |     |     |     |              | The simulated |              | experiments |                  | are performed |        | using            | Bullet    |
|     |     |     |     |     | [39]         | with          | joint torque | as          | control          | input.        | The    | physical         | experi-   |
mentsareperformedusingtheCartpole(Fig.1a)andFuruta
pendulum(Fig.1b)manufacturedbyQuanser.Thesephysical
|     |     |     |     |     | systems      | are             | directly  | controlled |            | using           | the DC      | motor         | voltage.   |
| --- | --- | --- | --- | --- | ------------ | --------------- | --------- | ---------- | ---------- | --------------- | ----------- | ------------- | ---------- |
|     |     |     |     |     | For          | the experiments |           | the        | voltage    | to motor-torque |             | conversion    |            |
|     |     |     |     |     | is           | performed       | using     | the        | parameters |                 | of the      | manufacturer. |            |
|     |     |     |     |     | Furthermore, |                 | both      | physical   | systems    |                 | have        | unique        | properties |
|     |     |     |     |     | that         | make            | the model | learning   |            | and the         | control     | challenging.  |            |
|     |     |     |     |     | The          | linear          | actuation | of the     | Cartpole   |                 | is a pinion | &             | rack drive |
causingsignificantstictionandthisstictionrendersthemodel
|      |                   |              |                      |             | learning |     | challenging. | In    | contrast, | the | links | of the | Furuta    |
| ---- | ----------------- | ------------ | -------------------- | ----------- | -------- | --- | ------------ | ----- | --------- | --- | ----- | ------ | --------- |
|      |                   |              |                      |             | pendulum |     | are very     | light | weight    | and | even  | small  | errors of |
| Fig. | 4. The normalized | mean squared | error of the forward | and inverse |          |     |              |       |           |     |       |        |           |
modelsforthesimulatedandphysicalplatformsonthetestset. motor voltages push the active joints to its joint limit and
stop the episode.
| {q,q(cid:219),q(cid:220),τττ | }1...N | . For the Furuta | pendulum | the interaction |     |     |     |     |     |     |     |     |     |
| ---------------------------- | ------ | ---------------- | -------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
M
time is 120s while the interaction time for the Cartpole is The performance of DeLaN 4EC is compared to the
240s. Using these highly correlated samples the control is dynamics parameters of the manufacturer and the white-box
learnedoffline.Afterlearningthecontroller,theperformance system identification introduced by [13] with the extension
isevaluatedusingthenormalizedmeansquareerror(nMSE) of viscous friction as in [20]. For system identification the
on the test data (Section V-B) as well as the online control mass matrix is computed using the Composite Rigid Body
performanceontheswing-uptasks(SectionV-C).Theonline algorithm [11] and the potential energy is computed using
control evaluation is the more relevant performance measure the analytic expression V(q)=mgl(cos(q)+1), where only
as the nMSE can be deceiving and a low nMSE does not the mass m is inferred from data while the gravitational
necessarilyimplyagoodcontrolperformance.Fortheswing- constant and pendulum length are pre-defined con-
|     |     |     |     |     |     |     | g   |     |     |     | l   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

(c)SimulatedFurutaPendulum
+15.0
+10.0
+5.0
+0.0
5.0
−
10.0
−
15.0
−
π π/2 0 +π/2 +π
− −
θ[rad]
]s/dar[θ˙
(a)SimulatedCartpole
ledoMlacitylanA
+15.0
+10.0
+5.0
+0.0
5.0
−
10.0
−
15.0
−
noitacfiitnedImetsyS
]s/dar[θ˙
+15.0
+10.0
+5.0
+0.0
5.0
−
10.0
−
15.0
−
3.0 2.0 1.0 +0.0 +1.0 +2.0 +3.0
− − −
θ[rad]
NaLeD ]s/dar[θ˙
(b)PhysicalCartpole (d)PhysicalFurutaPendulum
3.0 2.0 1.0 +0.0 +1.0 +2.0 +3.0 π π/2 0 +π/2 +π
− − − − −
θ[rad] θ[rad]
Manufacturer/GroundTruth SystemIdentification DeLaN4EC
Fig. 5. The position θ and velocity θ(cid:219) orbits recorded using energy control to swing-up the passive pendulums. The rows show the different models,
i.e.,theanalyticmodel,thesystemidentificationmodelandtheDeLaNmodelwhilethecolumnsshowthedifferentsimulatedandphysicalsystems.The
dahsed orbit highlights the desired energy E∗. While the learned and the analytic model can swing-up the simulated system and physical Cartpole only
theanalyticmodelandDeLaN4ECcanswing-upthephysicalFurutapendulum,whiletheenergycontrollerusingtheSystemIdentificationmodelcannot.
stants. These requirements are in stark contrast to DeLaN scaled coherently such that the energy conservation holds
4EC, because the white-box system identification approach as enforced by Equation 9. Furthermore, DeLaN learns the
requires the kinematic structure defining the link length, highstictionτττ ofthepinionandrackdriveandpredictsthe
F
connection between links and gravitational constant, while closetozeroaccelerationsq(cid:220) andnon-zeromotortorquesτττ
M
DeLaN4ECmustlearnthekinematicanddynamicstructure duringbalancingofthephysicalCartpole,givenasufficiently
from data. Furthermore, the assumption of knowing the good initialization of the friction model. The analytic model
kinematic structure simplifies the learning of the potential and system identification cannot represent the stiction and
energytomerelyfittingtheamplitudeofthepotentialenergy predicteitherzerotorquesandnon-zeroaccelerationsorzero
while DeLaN 4EC must not only learn the amplitude but torques and zero acceleration. Both predictions oppose the
also learn the shape. We do not compare to other black- measureddata.However,DeLaNsuffersfromhighfrequency
boxlearningtechniquessuchasneuralnetworksorGaussian noise on the passive pendulum or close to zero components,
process regression because these techniques cannot learn whereas the white box models do not because the white
energy and hence, cannot be applied to energy control. box models consist of global parameters, which are not
susceptible to noise and these models can exploit the known
B. Offline Evaluation kinematic structure to infer zero Coriolis or gravitational
Figure 3 shows the learned dynamics model and energies forces.
of the simulated and physical Cartpole executing a swing-up Figure 4 shows the quantitative comparison using the
usingthecontrollawdescribedbyu .Thedynamicslearned nMSE defined as
E
byDeLaNcloselyresemblethedataaswellasthefrictional- (cid:205)N (cid:107)x −xˆ (cid:107) 2
, inertial-, centrifugal-, Coriolis- and gravitational forces nMSE= i=0 i i 2 (11)
(cid:205)N (cid:107)x +δ(cid:107) 2
predicted by the analytic model. Furthermore, the kinetic i=0 i 2
andpotentialenergiesarelearned.Onlythelearnedpotential whereas δ is a small constant for numerical stability. The
andkineticenergyforthephysicalsystemareslightlyscaled nMSEisevaluatedontestdataperformingaswing-up,which
similar to the system identification model. Although the in the case of the Cartpole is identical to the data shown in
energiesarescaled,boththekineticandpotentialenergyare Figure 3. For the simulations the analytic model is the true

model, which has a non-zero nMSE because noise is added controller because the system identification model swings-
to the torques during simulation and the accelerations are up the pendulum with slightly too much or too low energy
computed using finite differences and are low-pass filtered such that the PD-controller fails to stabilize the pendulum.
because this signal-processing is required for the physical Furthermore,theresultingtrajectoriesforthelearnedmodels
system.ThecomparisonshowsthatDeLaNobtainsasimilar are indistinguishable. For the physical Cartpole all models
nMSE as system identification and the analytic model for achievesmoothreal-timecontrolandswing-upthependulum
the forward model of the simulated systems. For the inverse for30consecutivetimesfromvaryingstartingconfigurations.
model of the simulated systems, DeLaN obtains comparable For the physical Furuta pendulum only the analytic model
nMSE for the actuated joint but slightly increased nMSE and DeLaN 4EC achieve the successful swing-up, while the
for the passive joints because DeLaN is susceptible to noise system identification model can only stabilize the pendulum
and the nMSE is very sensitive to the noise of the passive toalowamplitudecycle,whichdoesnotreachthebalancing
jointasτττ (cid:66)0.Forthephysicalsystems,DeLaNandsystem point. For 30 trials, DeLaN 4EC achieves the successful
p
identification obtain a lower nMSE than the analytic model completion for 27 trials. The three unsuccessful trials are
for the forward model. For the inverse model, both learned caused by the PD-Controller not being able to stabilize the
models achieve better performance than the analytic model pendulumbecauseDeLaN4ECswingsupthependulumwith
on the active joint and only for the passive joint DeLaN slightlylessenergythantheanalyticmodelandthebalancing
performs slightly worse due to the noise. This noise is PD-Controller is very sensitive to these changes in velocity
negligible during optimization and control because the MSE at the switching point. Tuning the PD-controller gains w.r.t.
is dominated by the actuated joint and only the nMSE per to DeLaN 4EC resultsin the successful completion of all 30
jointamplifiestheimpactofthenoise.Overall,thequalitative trials but decreases the performance of the analytic model.
and quantitative evaluation showed that the performance of For fair comparison the gains were fixed between the ex-
the learned models in comparison to the analytic model periments and optimized for the analytic model. The system
achieve comparable performance for the simulated systems identification model fails to swing-up the pendulum because
and a slightly better performance for the physical systems. this approach learns a too low mass for the pendulum and
|     |     |     |     |     |     |     | hence, can | only | stabilize | the | pendulum | to  | a low amplitude |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ---- | --------- | --- | -------- | --- | --------------- | --- |
TABLEI oscillation. The learning fails because the regressor of the
Percentageofsuccessfulswing-upsofsimulatedandphysical
|     |     |     |     |     |     |     | system identification |     | has | too | low rank | and | can only | infer a |
| --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | -------- | --- | -------- | ------- |
CartpoleandFurutapendulumforthedifferentmodels. linear combination of the dynamics parameters [40].
|     |     |     |          |     |        |     | DeLaN | 4EC | is capable | of  | solving | the swing-up |     | for the |
| --- | --- | --- | -------- | --- | ------ | --- | ----- | --- | ---------- | --- | ------- | ------------ | --- | ------- |
|     |     |     | Cartpole |     | Furuta |     |       |     |            |     |         |              |     |         |
Sim Real Sim Real simulated and physical Cartpole and Furuta pendulum using
Model
AnalyticModel 1.00 1.00 1.00 1.00 a 500Hz real-time control loop. The performance of DeLaN
|     | SystemIdentification |     | 1.00 | 1.00 | 0.93 0.00 |     |                   |                |     |              |          |         |           |         |
| --- | -------------------- | --- | ---- | ---- | --------- | --- | ----------------- | -------------- | --- | ------------ | -------- | ------- | --------- | ------- |
|     |                      |     |      |      |           |     | 4EC is comparable |                | to  | the analytic | model    | and     | DeLaN     | 4EC     |
|     | DeLaN                |     | 1.00 | 1.00 | 1.00 0.90 |     |                   |                |     |              |          |         |           |         |
|     |                      |     |      |      |           |     | achieves          | the swing-up   |     | of the       | physical | Furuta  | pendulum, |         |
|     |                      |     |      |      |           |     | where system      | identification |     | does         | not,     | despite | having    | a lower |
nMSEcomparedtotheanalyticmodel.Thisshowsthatalow
| C.  | Online Control | Evaluation |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | -------------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
nMSEdoesnotnecessarilyimplygoodcontrolperformance.
|      | For the online | control     | experiments | the energy-based |      | con-   |     |     |     |            |     |     |     |     |
| ---- | -------------- | ----------- | ----------- | ---------------- | ---- | ------ | --- | --- | --- | ---------- | --- | --- | --- | --- |
|      |                |             |             |                  |      |        |     |     | VI. | Conclusion |     |     |     |     |
| trol | law described  | in Equation | 10          | is applied       | with | a con- |     |     |     |            |     |     |     |     |
trol frequency of 500Hz to 30 different initial joint con- In this paper, we introduced the concept of Deep La-
figurations. Therefore, all models must achieve real-time grangian Networks for energy control (DeLaN 4EC), a
computation of at least 500Hz on the physical system to learning to control approach that combines the flexibility of
be able to solve the task. For the simulated experiments, deep learning with the insights from control theory. This
the starting configuration is randomly sampled while the combination is enabled only because DeLaN 4EC imposes
physical experiments are performed sequentially and hence, Lagrangian Mechanics, conservation of energy and energy
the starting configuration naturally changes. For the physical coherence on a generic deep network and hence, learns a
Cartpole we augment the energy controller with an negative physically plausible model. We showed that DeLaN is able
derivativegaintocompensatethelargeviscousfrictionofthe to learn the inertial-, centripetal-, Coriolis-, gravitational-
pinion and rack drive. The percentage of successful swing- and frictional forces and the potential and kinetic energy
upsissummarizedinTableIandthecorrespondingposition from sensor data containing only joint configuration and
|     | and velocity | θ(cid:219) orbits | for two | starting configurations |     | of  |                                                        |     |     |     |     |     |     |     |
| --- | ------------ | ----------------- | ------- | ----------------------- | --- | --- | ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
| θ   |              |                   |         |                         |     |     | motortorque.Therefore,learningtheseforcesandenergiesis |     |     |     |     |     |     |     |
the passive pendulum are shown in Figure 5. Videos of unsupervised and does not require any knowledge about the
the swing-up of the physical Cartpole and physical Furuta kinematic structure. Other model learning algorithms either
pendulum can be found at https://youtu.be/m3JRYq7Gmgo. require the kinematic structure to learn these components
For the simulated systems the analytic and the learned such as system identification or cannot learn the force
models achieve the successful completion of the swing- components or system energies such as neural networks or
up. Only the system identification model fails on 2 trials. Gaussianprocessregression.Thequalitativeandquantitative
These unsuccessful completions are caused by the balancing offlineevaluationshowedthatthenormalizedMSEofDeLaN

| in comparison |     | to the analytic |     | model is | comparable | for the |            |        |                |     |               |     |            |          |
| ------------- | --- | --------------- | --- | -------- | ---------- | ------- | ---------- | ------ | -------------- | --- | ------------- | --- | ---------- | -------- |
|               |     |                 |     |          |            |         | [21] M. W. | Spong, | S. Hutchinson, |     | M. Vidyasagar | et  | al., Robot | modeling |
simulatedsystemsandbetterforthephysicalsystems.Forthe andcontrol. WileyNewYork,2006,vol.3.
|                |       |       |     |              |     |          | [22] M. Haruno, |     | D. M.    | Wolpert,      | and M. | Kawato,      | “Mosaic | model for |
| -------------- | ----- | ----- | --- | ------------ | --- | -------- | --------------- | --- | -------- | ------------- | ------ | ------------ | ------- | --------- |
| online control | task, | DeLaN | 4EC | accomplishes | the | swing-up |                 |     |          |               |        |              |         |           |
|                |       |       |     |              |     |          | sensorimotor    |     | learning | and control,” |        | computation, |         | vol. 13,  |
Neural
ofthephysicalCartpoleandFurutapendulumfromdifferent no.10,pp.2201–2220,2001.
starting configurations by computing the system energies [23] S. Calinon, F. D’halluin, E. L. Sauser, D. G. Caldwell, and A. G.
withina500Hzreal-timecontrolloop.Incontrast,thesystem Billard, “Learning and reproduction of gestures by imitation,” IEEE
Robotics&AutomationMagazine,vol.17,no.2,pp.44–54,2010.
identificationmodelonlyachievesthesuccessfulswing-upof [24] S. M. Khansari-Zadeh and A. Billard, “Learning stable nonlinear
the physical Cartpole but not the physical Furuta pendulum, dynamicalsystemswithgaussianmixturemodels,”IEEETransactions
onRobotics,vol.27,no.5,pp.943–957,2011.
| despite having | comparable |     | nMSE | to DeLaN | 4EC. |     |     |     |     |     |     |     |     |     |
| -------------- | ---------- | --- | ---- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[25] J.Kocijan,R.Murray-Smith,C.E.Rasmussen,andA.Girard,“Gaus-
|                       |     |           |            |              |             |          | sian                 | process    | model | based predictive        | control,” |            | in        |              |
| --------------------- | --- | --------- | ---------- | ------------ | ----------- | -------- | -------------------- | ---------- | ----- | ----------------------- | --------- | ---------- | --------- | ------------ |
|                       |     |           | References |              |             |          |                      |            |       |                         |           |            | American  | Control      |
|                       |     |           |            |              |             |          | Conference,vol.3.    |            |       | IEEE,2004,pp.2214–2219. |           |            |           |              |
|                       |     |           |            |              |             |          | [26] D. Nguyen-Tuong |            | and   | J. Peters,              | “Using    | model      | knowledge | for learn-   |
| [1] A. Albu-Schäffer, |     | “Regelung | von        | Robotern mit | elastischen | Gelenken |                      |            |       |                         |           |            |           |              |
|                       |     |           |            |              |             |          | ing inverse          | dynamics.” |       | in International        |           | Conference | on        | Robotics and |
amBeispielderDLR-Leichtbauarme,”Ph.D.dissertation,Technische
| UniversitätMünchen,2002. |     |     |     |     |     |     | Automation,2010,pp.2677–2682. |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | --- | --- | --- | ----------------------------- | --- | --- | --- | --- | --- | --- | --- |
[27] J.P.Ferreira,M.Crisostomo,A.P.Coimbra,andB.Ribeiro,“Simula-
| [2] T. P. | Lillicrap, | J. J. Hunt, | A.  | Pritzel, N. Heess, | T.  | Erez, Y. Tassa, |     |     |     |     |     |     |     |     |
| --------- | ---------- | ----------- | --- | ------------------ | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
tioncontrolofabipedrobotwithsupportvectorregression,”inIEEE
D.Silver,andD.Wierstra,“Continuouscontrolwithdeepreinforce-
|     |     |     |     |     |     |     | International |     | Symposium | on  | Intelligent | Signal | Processing. | IEEE, |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --------- | --- | ----------- | ------ | ----------- | ----- |
mentlearning,”arXivpreprintarXiv:1509.02971,2015.
2007,pp.1–6.
[3] J.Schulman,S.Levine,P.Abbeel,M.I.Jordan,andP.Moritz,“Trust [28] M. Jansen, “Learning an accurate neural model of the dynamics of
regionpolicyoptimization.”inIcml,vol.37,2015,pp.1889–1897.
|     |     |     |     |     |     |     | a typical | industrial | robot,” | in  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---------- | ------- | --- | --- | --- | --- | --- |
[4] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, International Conference on Artificial
NeuralNetworks,1994,pp.1257–1260.
| “Proximal | policy | optimization |     | algorithms,” | arXiv | preprint |               |       |          |     |            |           |          |      |
| --------- | ------ | ------------ | --- | ------------ | ----- | -------- | ------------- | ----- | -------- | --- | ---------- | --------- | -------- | ---- |
|           |        |              |     |              |       |          | [29] I. Lenz, | R. A. | Knepper, | and | A. Saxena, | “Deepmpc: | Learning | deep |
arXiv:1707.06347,2017.
latentfeaturesformodelpredictivecontrol.”inRobotics:Scienceand
| [5] M.J.Mataric,“Rewardfunctionsforacceleratedlearning,”inMachine |     |           |                           |            |     |             | Systems,2015. |         |     |              |                               |     |     |      |
| ----------------------------------------------------------------- | --- | --------- | ------------------------- | ---------- | --- | ----------- | ------------- | ------- | --- | ------------ | ----------------------------- | --- | --- | ---- |
| LearningProceedings1994.                                          |     |           | Elsevier,1994,pp.181–189. |            |     |             |               |         |     |              |                               |     |     |      |
|                                                                   |     |           |                           |            |     |             | [30] F. D.    | Ledezma | and | S. Haddadin, | “First-order-principles-based |     |     | con- |
| [6] P. Henderson,                                                 |     | R. Islam, | P. Bachman,               | J. Pineau, | D.  | Precup, and |               |         |     |              |                               |     |     |      |
structivenetworktopologies:Anapplicationtorobotinversedynam-
| D. Meger, | “Deep | reinforcement |     | learning that | matters,” | in Thirty- |       |             |               |     |            |     |          |           |
| --------- | ----- | ------------- | --- | ------------- | --------- | ---------- | ----- | ----------- | ------------- | --- | ---------- | --- | -------- | --------- |
|           |       |               |     |               |           |            | ics,” | in IEEE-RAS | International |     | Conference | on  | Humanoid | Robotics, |
SecondAAAIConferenceonArtificialIntelligence,2018.
|     |     |     |     |     |     |     | 2017. | IEEE,2017,pp.438–445. |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --------------------- | --- | --- | --- | --- | --- | --- |
[7] S. Schaal, C. G. Atkeson, and S. Vijayakumar, “Scalable techniques [31] E.Rueckert,M.Nakatenus,S.Tosatto,andJ.Peters,“Learninginverse
| from                                    | nonparametric | statistics | for    | real time     | robot learning,” |                |               |        |            |             |           |            |       |           |
| --------------------------------------- | ------------- | ---------- | ------ | ------------- | ---------------- | -------------- | ------------- | ------ | ---------- | ----------- | --------- | ---------- | ----- | --------- |
|                                         |               |            |        |               |                  | Applied        | dynamics      | models | in         | o (n) time  | with lstm | networks,” |       | in        |
| Intelligence,vol.17,no.1,pp.49–60,2002. |               |            |        |               |                  |                |               |        |            |             |           |            |       | IEEE-RAS  |
|                                         |               |            |        |               |                  |                | International |        | Conference | on Humanoid |           | Robotics.  | IEEE, | 2017, pp. |
| [8] Y. Choi,                            | S.-Y.         | Cheong,    | and N. | Schweighofer, | “Local           | online support |               |        |            |             |           |            |       |           |
811–816.
vectorregressionforlearningcontrol,”inInternationalSymposiumon
|     |     |     |     |     |     |     | [32] A. I. | Lurie, | Analytical | mechanics. |     | Berlin, | Heidelberg: | Springer |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | ---------- | ---------- | --- | ------- | ----------- | -------- |
ComputationalIntelligenceinRoboticsandAutomation. IEEE,2007, Science&BusinessMedia,2013.
pp.13–18.
[33] D.A.Wells,Schaum’soutlineoftheoryandproblemsoflagrangian
[9] D.Nguyen-Tuong,M.Seeger,andJ.Peters,“Modellearningwithlocal
|     |     |     |     |     |     |     | dynamics. | McGraw-Hill,1967. |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----------------- | --- | --- | --- | --- | --- | --- |
gaussianprocessregression,”AdvancedRobotics,vol.23,no.15,pp.
[34] N.Ratliff,F.Meier,D.Kappler,andS.Schaal,“Doomed:Directonline
2015–2034,2009.
optimizationofmodelingerrorsindynamics,”Bigdata,vol.4,no.4,
[10] A. Sanchez-Gonzalez, N. Heess, J. T. Springenberg, J. Merel, pp.253–268,2016.
| M. Riedmiller, |     | R. Hadsell, | and | P. Battaglia, | “Graph | networks as |     |     |     |     |     |     |     |     |
| -------------- | --- | ----------- | --- | ------------- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
[35] H.Olsson,K.J.Åström,C.C.DeWit,M.Gäfvert,andP.Lischinsky,
| learnable | physics | engines | for inference | and | control,” |                |                                                              |     |     |     |     |     |     |     |
| --------- | ------- | ------- | ------------- | --- | --------- | -------------- | ------------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
|           |         |         |               |     |           | arXiv preprint | “Frictionmodelsandfrictioncompensation,”Eur.J.Control,vol.4, |     |     |     |     |     |     |     |
arXiv:1806.01242,2018.
no.3,pp.176–195,1998.
[11] M.W.WalkerandD.E.Orin,“Efficientdynamiccomputersimulation
|     |     |     |     |     |     |     | [36] B. Bona | and | M.  | Indri, “Friction | compensation |     | in  | robotics: an |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | ---------------- | ------------ | --- | --- | ------------ |
of robotic mechanisms,” Journal of Dynamic Systems, Measurement, overview,”inDecisionandControl,2005and2005EuropeanControl
andControl,vol.104,no.3,pp.205–211,1982.
|     |     |     |     |     |     |     | Conference.CDC-ECC’05.44thIEEEConferenceon. |     |     |     |     |     |     | IEEE,2005, |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- | ---------- |
[12] M.Lutter,C.Ritter,andJ.Peters,“Deeplagrangiannetworks:Using
pp.4360–4367.
physicsasmodelpriorfordeeplearning,”inInternationalConference
|     |     |     |     |     |     |     | [37] A. Wahrburg, |     | J. Bös, | K. D. | Listmann, | F. Dai, | B.  | Matthias, and |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | ------- | ----- | --------- | ------- | --- | ------------- |
onLearningRepresentations,2019. H. Ding, “Motor-current-based estimation of cartesian contact forces
[13] C.G.Atkeson,C.H.An,andJ.M.Hollerbach,“Estimationofinertial and torques for robotic manipulators and its application to force
parametersofmanipulatorloadsandlinks,”TheInternationalJournal
control,”IEEETransactionsonAutomationScienceandEngineering,
ofRoboticsResearch,vol.5,no.3,pp.101–119,1986.
vol.15,no.2,pp.879–886,2018.
| [14] Y. Duan, | X.  | Chen, R. | Houthooft, | J. Schulman, | and | P. Abbeel, |                     |     |         |        |                   |     |             |        |
| ------------- | --- | -------- | ---------- | ------------ | --- | ---------- | ------------------- | --- | ------- | ------ | ----------------- | --- | ----------- | ------ |
|               |     |          |            |              |     |            | [38] M. Riedmiller, |     | “Neural | fitted | q iteration–first |     | experiences | with a |
“Benchmarking deep reinforcement learning for continuous control,” data efficient neural reinforcement learning method,” in
European
in International Conference on Machine Learning, 2016, pp. 1329– ConferenceonMachineLearning. Springer,2005,pp.317–328.
1338.
[39] E.CoumansandY.Bai,“Pybullet,apythonmoduleforphysicssim-
| [15] M. Deisenroth |     | and C. | E. Rasmussen, | “Pilco: | A model-based | and |     |     |     |     |     |     |     |     |
| ------------------ | --- | ------ | ------------- | ------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ulationforgames,roboticsandmachinelearning,”http://pybullet.org,
| data-efficient |     | approach | to policy | search,” in | Proceedings | of the 28th |     |     |     |     |     |     |     |     |
| -------------- | --- | -------- | --------- | ----------- | ----------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
2016–2018.
International Conference on machine learning (ICML-11), 2011, pp. [40] B.SicilianoandO.Khatib,Springerhandbookofrobotics. Springer,
| 465–472. |     |     |     |     |     |     | 2016. |     |     |     |     |     |     |     |
| -------- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
[16] C.C.ChungandJ.Hauser,“Nonlinearcontrolofaswingingpendu-
lum,”automatica,vol.31,no.6,pp.851–862,1995.
| [17] M. W. | Spong,    | “Energy | based       | control of a | class of | underactuated  |     |     |     |     |     |     |     |     |
| ---------- | --------- | ------- | ----------- | ------------ | -------- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| mechanical | systems,” | IFAC    | Proceedings | Volumes,     | vol.     | 29, no. 1, pp. |     |     |     |     |     |     |     |     |
2828–2832,1996.
| [18] I. Fantoni    | and | R. Lozano,                          |            |         |     |               |     |     |     |     |     |     |     |     |
| ------------------ | --- | ----------------------------------- | ---------- | ------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|                    |     |                                     | Non-linear | control | for | underactuated |     |     |     |     |     |     |     |     |
| mechanicalsystems. |     | SpringerScience&BusinessMedia,2002. |            |         |     |               |     |     |     |     |     |     |     |     |
[19] M.Ishitobi,Y.Ohta,Y.Nishioka,andH.Kinoshita,“Swing-upofa
cart—pendulumsystemwithfrictionbyenergycontrol,”Proceedings
oftheInstitutionofMechanicalEngineers,PartI:JournalofSystems
andControlEngineering,vol.218,no.5,pp.411–415,2004.
| [20] J.-A. | Ting, M. | Mistry, | J. Peters, | S. Schaal, | and J. | Nakanishi, “A |     |     |     |     |     |     |     |     |
| ---------- | -------- | ------- | ---------- | ---------- | ------ | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
bayesianapproachtononlinearparameteridentificationforrigidbody
dynamics.”inRobotics:ScienceandSystems,2006,pp.32–39.