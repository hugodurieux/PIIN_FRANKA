IEEETRANSACTIONSONAUTOMATIONSCIENCEANDENGINEERING,VOL.22,2025 2241
Data-Driven Methods Applied to Soft Robot
Modeling and Control: A Review
Zixi Chen , Graduate Student Member, IEEE, Federico Renda , Member, IEEE,
Alexia Le Gall, Student Member, IEEE, Lorenzo Mocellin , Matteo Bernabei , Théo Dangel ,
Gastone Ciuti , Senior Member, IEEE, Matteo Cianchetti , Member, IEEE,
and Cesare Stefanini , Member, IEEE
Abstract—Soft robots show compliance and have infinite state-of-the-artdata-drivenmethodsandsurveythreeapproaches
degrees of freedom. Thanks to these properties, such robots can widely utilized. This review also compares the performance of
be leveraged for surgery, rehabilitation, biomimetics, unstruc- these methods, considering some important features like data
tured environment exploring, and industrial grippers. In this amount requirement, control frequency, and target task. The
case, they attract scholars from a variety of areas. However, features of each approach are summarized, and we discuss the
nonlinearity and hysteresis effects also bring a burden to robot possible future of this area.
modeling. Moreover, following their flexibility and adaptation,
IndexTerms—Softrobot,data-drivenmethod,physicalmodel,
soft robot control is more challenging than rigid robot control.
Jacobianmatrix,statisticalmodel,neuralnetwork,reinforcement
In order to model and control soft robots, a large number
learning.
of data-driven methods are utilized in pairs or separately.
This review first briefly introduces two foundations for data-
driven approaches, which are physical models and the Jacobian I. INTRODUCTION
matrix, then summarizes three kinds of data-driven approaches,
which are statistical method, neural network, and reinforcement SOFT robots have been developed for a large number of
learning. This review compares the modeling and controller applications. Owing to their infinite degrees of freedom
features,e.g.,modeldynamics,datarequirement,andtargettask,
(DOFs) and flexibility, soft robots are leveraged in robot
within and among these categories. Finally, we summarize the
assistant surgery, especially minimally invasive surgery [1].
features of each method. A discussion about the advantages and
limitations of the existing modeling and control approaches is Compared with their rigid counterparts, soft robots are rela-
presented, and we forecast the future of data-driven approaches tivelysafeduetotheirsoftnessandhavesignificantadvantages
in soft robots. A website (https://sites.google.com/view/23zcb) is in assisting elderly and disabled people with daily tasks [2]
built for this review and will be updated frequently.
and cooperating with humans [3]. Moreover, they are used as
handrecoverydevices[4]andwearabledevices[5]forvarious
Note to Practitioners—This work is motivated by the need for
a review introducing soft robot modeling and control methods medical purposes like rehabilitation and human motion moni-
in parallel. Modeling and control play significant roles in robot toring. Animals are composed of soft tissues, and researchers
research,andtheyarechallengingespeciallyforsoftrobots.The in the bioinspired area apply soft materials like silicone to
nonlinear and complex deformation of such robots necessitates
build soft robots and mimic the behaviors of living beings,
specific modeling and control approaches. We introduce the
such as octopus [6], elephant [7], and earthworm [8]. These
robots produce specific motions and manipulations by imi-
Manuscript received 19 February 2024; accepted 11 March 2024. Date of
tating the structures and behaviors of soft animals. With the
publication 20 March 2024; date of current version 5 February 2025. This
article was recommended for publication by Associate Editor H. Lu and help of such soft biomimetic robots, some exploring tasks in
EditorL.Zhanguponevaluationofthereviewers’comments.Thisworkwas various environments like underwater [9] and walls [10] can
supportedinpartbyEuropeanUnion(EU)bytheNextGenerationEUProject
be achieved. Soft robot hands are adaptative to objects and
“Ecosistema dell’Innovazione” Tuscany Health Ecosystem [Tuscany Health
Ecosystem (THE), Piano Nazionale di Ripresa e Resilienza (PNRR), Spoke commonly applied for grasping tasks involving fragile [11]
4:Spoke9:RoboticsandAutomationforHealth]underGrantECS00000017; and diverse [12] objects. To summarize, unique properties
inpartbyU.S.OfficeofNavalResearchGlobalunderGrantN62909-21-1-
like infinite DOFs, compliance, and safety for humans lead
2033; and in part by Khalifa University under Grant RC1-2018-KUCARS.
(Correspondingauthor:ZixiChen.) to the high potential of soft robots. Hence, soft robot study is
Zixi Chen, Alexia Le Gall, Lorenzo Mocellin, Matteo Bernabei, a research area highly attractive to robotics scholars.
Théo Dangel, Gastone Ciuti, Matteo Cianchetti, and Cesare Stefanini
Followed by the aforementioned advantages and applica-
are with The BioRobotics Institute and the Department of Excel-
lence in Robotics and AI, Scuola Superiore Sant’Anna, 56127 Pisa, tions, the most considerable drawback of soft robots is the
Italy (e-mail: zixi.chen@santannapisa.it; alexiamarie.legall@santannapisa. challenge of modeling and control. Deformable materials
it; lorenzo.mocellin@santannapisa.it; matteo.bernabei@santannapisa.it; theo.
lead to the nonlinear and delayed responses of soft robots.
dangel@santannapisa.it; gastone.ciuti@santannapisa.it; matteo.cianchetti@
santannapisa.it;cesare.stefanini@santannapisa.it). Moreover,infiniteDOFsmakeitcomplicatedtobuildaccurate
Federico Renda is with the Khalifa University Center for Autonomous models for soft robots. The physical properties of soft robots
Robotic Systems, Khalifa University, Abu Dhabi, United Arab Emirates
will also vary due to the aging of soft materials. Owing to
(e-mail:federico.renda@ku.ac.ae).
DigitalObjectIdentifier10.1109/TASE.2024.3377291 the above characteristics, the modeling of soft robots is more
©2024TheAuthors.ThisworkislicensedunderaCreativeCommonsAttribution4.0License.
Formoreinformation,seehttps://creativecommons.org/licenses/by/4.0/

2242 IEEETRANSACTIONSONAUTOMATIONSCIENCEANDENGINEERING,VOL.22,2025
Fig.1. Diagramofsoftrobotmodelingandcontrolprocesses.Robotdesign(grey)providesaspecificsoftrobotstructureandactuationpattern.Thesensing
system(green)obtainsrobotinformationviathesensorsofsucharobot.Modeling fθ isafunctionthatpredictstherobotstate p(blue),asendpositionand
robotpose,accordingtotheactuationvariablesa(red.)Controlgτ aimstodecideactuationvariablesawiththedesiredstate pd andsensinginputs.Finally,
sucharobotsystemcanachieveavarietyoftasks.θ andτ representtheparametersinthedata-drivenmethodsofmodelingandcontrol,respectively.
complexthanthatoftheirrigidcounterparts,whichalsoleads close loop control [38]. Moreover, they can also be utilized
to challenging control tasks [13], [14]. Therefore, modeling for observer [39] which includes modeling as prediction and
and control play essential roles in soft robot research. sensing characterization [40] which can be applied in control.
TheworkingprocessofsoftrobotsissummarizedinFig.1. This review aims to present and compare data-driven meth-
Various kinds of robot designs are used in soft robots, like 1 ods applied to soft robot modeling and control in parallel.
DOF soft fingers [15], 3 DOF continuum robots [16], parallel Althoughsomereviewsarerelatedtosoftrobotmodelingand
robots [17], concentric tube robots [18] and so on. To actuate control [14], [41], [42], [43], they do not introduce modeling
a soft robot, the researchers apply actuation approaches like and control simultaneously. In this review, first we briefly
fluid-drivenmethods[19],cable-drivenmethod[20],electroac- introduce foundations for data-driven approaches, which are
tive polymers [21], shape memory alloy (SMA) [22], etc. physical models and the Jacobian matrix. Physical models
Also, there are multiple categories of sensors, e.g., optical provide simulation environments and insight into soft robots,
markers [23], EM trackers [24], flex sensors [25] and Fiber while the Jacobian matrix infers the data relationship for
|               |     |       |       |            |         |            |     | data-driven | approaches. |     | Then, | we classify | data-driven |     | meth- |
| ------------- | --- | ----- | ----- | ---------- | ------- | ---------- | --- | ----------- | ----------- | --- | ----- | ----------- | ----------- | --- | ----- |
| Bragg Grating |     | (FBG) | [26], | [27]. Some | reviews | detailedly |     |             |             |     |       |             |             |     |       |
introducesoftrobotswithmechanicalaspects[28],[29].Based ods applied to soft robot modeling and control into three
on these hardware implementations, soft robot modeling can categories: statistical method, neural network, and reinforce-
be seen as a function that takes actuation a as the input and ment learning. We introduce the corresponding modeling and
robot state p, such as end position, orientation, and shape, control approaches for each kind of data-driven approach par-
as the output. Meanwhile, soft robot control is the inverse allelly and compare them within and among these categories.
process of modeling, which takes the desired robot state p Finally, conclusions on data-driven approaches applied to soft
d
and the sensing signal s as the input and actuation a as the robot modeling and control are proposed, and we discuss the
output. The input and output choices may change considering challenges and emerging directions of this area. Fig. 2 shows
the control strategy. For example, the open control strategy the paper number of different methods cited in this review
in [30] only requires the target positions p for the trajectory according to the publishment time. In Fig. 2-(a), one paper
d
following, but the close loop control approach in [23] utilizes mayfallintomultiplecategoriesifitinvolvesseveralmethods,
both the target position p and the previous end positions butonepaperonlyfallsintoonecategoryconsideringthemain
d
from the sensing system s. Each mapping requires a model, method in this paper in Fig. 2-(b). Fig. 3-(a) and Fig. 3-(b)
f or g, and the parameter θ or τ, which are partly influenced summarizethenumberofpapersaccordingtothepublishment
by robot design and sensing system. Finally, such control timeandmethodcategory,respectively.Thesummaryofdata-
methods are leveraged for simple tasks, like target reach driven method categories is shown in Table I.
| [31] and | trajectory | following |     | [32], and | challenging | tasks, | like |     |     |     |     |     |     |     |     |
| -------- | ---------- | --------- | --- | --------- | ----------- | ------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
interaction adaptation [3] and navigation [33]. II. FOUNDATIONSFORDATA-DRIVENAPPROACHES
Duetothevarietyofstructuresandthecomplexityofbehav-
|     |     |     |     |     |     |     |     | In this | section, | we  | introduce | two significant |     | foundations |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | -------- | --- | --------- | --------------- | --- | ----------- | --- |
iors,itischallengingtoproposeaccuratephysicalmodelsand
|     |     |     |     |     |     |     |     | for data-driven |     | methods, | which | are physical |     | models | and the |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | -------- | ----- | ------------ | --- | ------ | ------- |
correspondingcontrolstrategiesforeverysoftrobot.However,
Jacobianmatrix.Bothofthemareverypopularandeffectivein
| data-driven       | methods      |           | have shown | considerable  |          | benefits.         | Data-  |                   |           |                     |            |              |              |                 |         |
| ----------------- | ------------ | --------- | ---------- | ------------- | -------- | ----------------- | ------ | ----------------- | --------- | ------------------- | ---------- | ------------ | ------------ | --------------- | ------- |
|                   |              |           |            |               |          |                   |        | rigid robot       | modeling  | and                 | control.   | In this      | case,        | the researchers |         |
| driven approaches |              | summarize |            | the features  |          | of data collected |        |                   |           |                     |            |              |              |                 |         |
|                   |              |           |            |               |          |                   |        | also try          | to employ | them                | in         | soft robots. | They         | stimulate       | the     |
| from robot        | motions      |           | without    | the necessity |          | of robot          | design |                   |           |                     |            |              |              |                 |         |
|                   |              |           |            |               |          |                   |        | development       | of        | data-driven         | approaches |              | by providing |                 | simula- |
| knowledge.        | Furthermore, |           | compared   | with          | physical | approaches        |        |                   |           |                     |            |              |              |                 |         |
|                   |              |           |            |               |          |                   |        | tors or inferring |           | data relationships. |            |              |              |                 |         |
basedonsimplificationsandhypotheses,datafromrealrobots
| can illustrate | the  | real        | features | of soft    | robots. | Thanks to   | these |             |        |     |     |     |     |     |     |
| -------------- | ---- | ----------- | -------- | ---------- | ------- | ----------- | ----- | ----------- | ------ | --- | --- | --- | --- | --- | --- |
|                |      |             |          |            |         |             |       | A. Physical | Models |     |     |     |     |     |     |
| advantages,    | some | data-driven |          | approaches | can     | be proposed | for   |             |        |     |     |     |     |     |     |
robot modeling and control with optimization [34] or learning Physicalmodelsaresignificantinsoftroboticsbecausethey
| [19]. Data-driven |     | approaches |     | can be | applied | for various | kinds |                |     |        |         |              |     |              |     |
| ----------------- | --- | ---------- | --- | ------ | ------- | ----------- | ----- | -------------- | --- | ------ | ------- | ------------ | --- | ------------ | --- |
|                   |     |            |     |        |         |             |       | can illustrate | the | nature | of soft | robot motion | and | deformation. |     |
of modeling and control strategies, like kinematics modeling Also, they are fundamental to data-driven methods by provid-
[35], dynamic modeling [36], open loop control [37], and ing simulation environments and data. Discretization methods

CHENetal.:DATA-DRIVENMETHODSAPPLIEDTOSOFTROBOTMODELINGANDCONTROL:AREVIEW 2243
TABLEI
SUMMARYOFMETHODCATEGORIES
Fig.2. Papernumberfor(a)includedmethodsand(b)themainmethod.
Fig.3. Papernumberforthemainmethodaccordingto(a)yearsand(b)categories.
likeFEMhavebeenappliedforrobotsimulation.TheCosserat is applied in the simulator SOFA [48] for deformation and
model and its discretization method, like geometric variable- interaction simulation. Moreover, a series of works [17], [49],
strain (GVS), provide simulators specifically for soft robots. [50]focusonFEMapplicationsforreal-timecontrol.Inorder
Piecewise constant curvature (PCC) can be seen as a special tocopewiththishighlycomplicatedmodel,methodslikelocal
caseofGVSandiswidelyappliedtothesoftrobotsimulation linearization [17] and reduced-order control model [50] are
based on the assumption of deformation shape. Some specific employed for the trade-off between the model accuracy and
models, like the pseudo-rigid model and the concentric tube control frequency.
model, are proposed for specific soft robots. Some typical Besides the discretization of 3D small elements, the dis-
physicalmodelsareshowninFig.4.Inrobotcontrol,methods cretization of 1D Cosserat rod is also applied. Cosserat rod
considering physical models or parameters are model-based, models soft continuum robots with a series of rigid cross-
while approaches only employing data and not using physical sections, and includes bend, twist, stretch, and shear. The
relationshipsinherentinrobotscanbeseenasmodel-free[44]. simulator PyElastica [51] applies a discrete geometric form
FEM is a popular discretization simulation method in of the Cosserat rod model for soft robot simulation. The most
robotics.Thismethodcanbeappliedtovarioussoftrobots,for general strain-based discretization method of the Cosserat rod
example, soft foam robot hand [45], soft pneumatic actuator is GVS [52], which discretizes the continuous Cosserat rod
[46], and PneuNet bending actuator [47]. This model can modelintoafinitesetofstrainbasisfunctions.SoRoSim[53]
provide high-accuracy simulation with the requirement of integrates GVS for soft, rigid, and hybrid robotic system sim-
material parameters such as mass density, Young’s modulus, ulation. PCC is a special GVS, which only includes bending
and Poisson’s ratio. Generally, FEM works as an offline mod- and simulates a continuum robot with several curves in some
elingmethod,suchasproducingadataset[46]forNNlearning bendingangles[54].OriginalPCConlyshowsthegeometrical
and building an exploring environment for RL [45]. FEM informationanddynamicPCCmodelsincludespatialdynamic

2244 IEEETRANSACTIONSONAUTOMATIONSCIENCEANDENGINEERING,VOL.22,2025
TABLEII
PHYSICALMODELPAPERCOMPARISON
Fig.4. Diagramsof(a)FEM,(b)PCCwithpseudo-rigidmodel,(c)Cosserat
rodmodel,and(d)concentrictubemodel.Elementmotionanddeformation
| in (a) represent | the         | soft         | robot deformation. |              | The grey | soft      | robot in (b)    | is      |         |                 |     |        |            |              |          |
| ---------------- | ----------- | ------------ | ------------------ | ------------ | -------- | --------- | --------------- | ------- | ------- | --------------- | --- | ------ | ---------- | ------------ | -------- |
| represented      | by a series | of           | constant           | curves,      | and the  | augmented | rigid robots    |         |         |                 |     |        |            |              |          |
|                  |             |              |                    |              |          |           |                 | Fig. 5. | Diagram | of the Jacobian |     | matrix | estimation | and control. | Based on |
| model the        | soft robot  | dynamically. |                    | The Cosserat | rod      | model     | in (c) includes |         |         |                 |     |        |            |              |          |
theJacobianmatrixinitialization,theJacobianmatrixisupdatedbasedonthe
| forces andmoments |     | inherently.The |     | concentric | tubemodel | in  | (d)represents |     |     |     |     |     |     |     |     |
| ----------------- | --- | -------------- | --- | ---------- | --------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
therobotmotionwiththeconfigurationsl1 ,l2 ,θ andθ 2. sensings.Then,theestimatedJacobianmatrixisappliedforcontrol.
1
|         |          |          |     |              |       |     |           | accurate | and explicit |     | models | for soft | robots, | optimization | is  |
| ------- | -------- | -------- | --- | ------------ | ----- | --- | --------- | -------- | ------------ | --- | ------ | -------- | ------- | ------------ | --- |
| effects | [55] and | external |     | interactions | [56]. | Of  | note, PCC |          |              |     |        |          |         |              |     |
is a simplification of the nonlinear Euler-Bernoulli beam, utilized for Jacobian matrix estimation instead of directly
|           |            |     |          |       |          |       |          | linearizing | explicit | models. |     | The included |     | robot model | is just |
| --------- | ---------- | --- | -------- | ----- | -------- | ----- | -------- | ----------- | -------- | ------- | --- | ------------ | --- | ----------- | ------- |
| which can | be applied |     | for soft | robot | modeling | under | external |             |          |         |     |              |     |             |         |
|           |            |     |          |       |          |       |          |             |          |         | =   | (a)          |     |             |         |
interaction without the constant curvature assumption [57]. a general model like p fθ instead of an explicit and
There are also some physical models for specific kinds of physical one, and it is only employed for illustration instead
|              |             |     |            |     |      |         |             | of calculation |     | [34]. |     |     |     |     |     |
| ------------ | ----------- | --- | ---------- | --- | ---- | ------- | ----------- | -------------- | --- | ----- | --- | --- | --- | --- | --- |
| soft robots. | Considering |     | concentric |     | tube | robots, | the authors |                |     |       |     |     |     |     |     |
of[18]leveragerotationsandtranslationsoftubesasactuation The Jacobian matrix estimation and control process is
|           |         |            |     |            |        |     |          | summarized | in  | Fig. 5. | The | first work | applying | the | Jacobian |
| --------- | ------- | ---------- | --- | ---------- | ------ | --- | -------- | ---------- | --- | ------- | --- | ---------- | -------- | --- | -------- |
| variables | for the | concentric |     | tube robot | model, |     | as shown | in         |     |         |     |            |          |     |          |
Fig.4-(d).Thecontroltasksareachievedbyfindingtheinverse matrix in the main approach is [34]. For Jacobian matrix
kinematic solutions. Neural networks are utilized for both initialization, each actuator should be actuated with a small
|          |             |     |         |       |         |        |          | incremental | amount | in  | order | to estimate |     | the initial | Jacobian |
| -------- | ----------- | --- | ------- | ----- | ------- | ------ | -------- | ----------- | ------ | --- | ----- | ----------- | --- | ----------- | -------- |
| modeling | and control |     | in [58] | based | on this | model. | The con- |             |        |     |       |             |     |             |          |
centrictubemodelhasalsobeenusedforRLcontrolin[31]to matrix J [34], [62], [63], [64]. Then, the Jacobian matrix is
0
updatedaccordingtotheactuationandendpositionchangein
provideactionvariables.Pseudo-rigidmodelscanapproximate
softrobotswithrigidcounterparts[59]asshowninFig.4-(b), the last step. The matrix update strategy can be shown as
andthesophisticatedmotionsofsoftrobotsaresimulatedwith
|     |     |     |     |     |     |     |     |     |     | min | ∥△J | ˆ∥  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2
| the help | of pseudo | springs | [60] | and | dampers | [61]. |     |     |     | Jˆk+1 |     |     |     |     |     |
| -------- | --------- | ------- | ---- | --- | ------- | ----- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
In conclusion, the research of physical models deepens the s.t. △xk = ˆk+1W△yk
J
understanding of soft robot nature and produce various soft ˆk+1 = ˆk +△J ˆ
|                  |     |     |             |             |     |     |            |     |     |     | J   | J   |     |     | (1) |
| ---------------- | --- | --- | ----------- | ----------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
| robot simulators |     | for | data-driven | approaches. |     | A   | comparison |     |     |     |     |     |     |     |     |
of some typical papers applying physical models is shown △xk △yk
|     |     |     |     |     |     |     |     | where | and |     | are the | end | effector | displacement | and |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ------- | --- | -------- | ------------ | --- |
in Table II. This table includes the simulator SOFA based actuation change at step k, respectively. J = [J J ... J ]
|     |     |     |     |     |     |     |     |     |     |     |     |     |     | 1   | 2 n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
on FEM [48], the simulator PyElastica based on Cosserat is the Jacobian matrix and n is the dimension of the actuation
|     |     |     |     |     |     |     |     |     | =diag(∥J |     |     | ,∥J | ,...,∥J | )isaweighting |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | ------- | ------------- | --- |
rod [51], the simulator SoRoSim based on GVS [53], and RL variable y.W ∥ ∥ n ∥
|     |     |     |     |     |     |     |     |     | ˆ   |     | 1 2 | 2 2 |     | 2   | ˆk  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
works using the specific model concentric tube model [31]. matrix and J = JW−1 is the unit Jaocbian matrix. J and
|     |     |     |     |     |     |     |     | J ˆk+1 |          |          |        |     |         | k k+1. |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | -------- | -------- | ------ | --- | ------- | ------ | --- |
|     |     |     |     |     |     |     |     | are    | the unit | Jacobian | matrix |     | at step | and    |     |
B. Jacobian Matrix The actuation variables are derived as the cost function in
|              |     |        |     |       |                  |     |         | an optimization |     | problem | considering |     | the | constraints | of the |
| ------------ | --- | ------ | --- | ----- | ---------------- | --- | ------- | --------------- | --- | ------- | ----------- | --- | --- | ----------- | ------ |
| The Jacobian |     | matrix | can | infer | the relationship |     | between |                 |     |         |             |     |     |             |        |
Jacobianmatrixandtargetendpositionforcontrol.Thecontrol
| the actuation | and              | position |     | velocities     | by model |          | linearization. |          |          |     |        |       |     |     |     |
| ------------- | ---------------- | -------- | --- | -------------- | -------- | -------- | -------------- | -------- | -------- | --- | ------ | ----- | --- | --- | --- |
|               |                  |          |     |                |          |          |                | strategy | for step | k+1 | can be | shown | as  |     |     |
| Thanks        | to its concision |          | and | effectiveness, | the      | Jacobian | matrix         |          |          |     |        |       |     |     |     |
+△yk+1∥
is widely applied in rigid robots, whose explicit physical min ∥yk
2
models are easy to propose. Also, it is possible to linearize △yk+1
such models. However, due to the difficulties of building s.t. △x = J ˆk+1W△yk+1
d

CHENetal.:DATA-DRIVENMETHODSAPPLIEDTOSOFTROBOTMODELINGANDCONTROL:AREVIEW 2245
TABLEIII
JACOBIANMATRIXPAPERCOMPARISON
yk +△yk+1 ≥ y last work [69] take inspiration from the Jacobian matrix in
min
yk +△yk+1 ≤ y (2) [68] and implement RL based on the same robot.
max
| where △x | is the | desired | displacement |     | for | the end | effector. |     |     |     |     |     |     |     |     |
| -------- | ------ | ------- | ------------ | --- | --- | ------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
d
|                                 |           |     | +△yk+1 |     |             |       |             |     | III. | STATISTICALMETHOD |     |     |     |     |     |
| ------------------------------- | --------- | --- | ------ | --- | ----------- | ----- | ----------- | --- | ---- | ----------------- | --- | --- | --- | --- | --- |
| The actuat                      | ion value | yk  |        | is  | constrained |       | between the |     |      |                   |     |     |     |     |     |
| minimalandmaximalactuationvalue |           |     |        |     | y           | and y | according   |     |      |                   |     |     |     |     |     |
min max Statistical methods are utilized to build the mapping func-
to the robot structure. Except for the optimization control tions between different variable spaces with only data, and
| method | in Eq. | 2, the inverse |     | Jacobian | matrix | is  | also utilized |     |     |     |     |     |     |     |     |
| ------ | ------ | -------------- | --- | -------- | ------ | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
physicalrelationshipsamongthesespacesareunnecessary.For
| for control | [39].  |              |      |            |     |             |             |                 |             |           |            |           |               |          |     |
| ----------- | ------ | ------------ | ---- | ---------- | --- | ----------- | ----------- | --------------- | ----------- | --------- | ---------- | --------- | ------------- | -------- | --- |
|             |        |              |      |            |     |             |             | example,        | the authors | of        | [70] infer | the       | relationship  | between  |     |
| Considering |        | nonlinearity | and  | hysteresis |     | of soft     | robots, the |                 |             |           |            |           |               |          |     |
|             |        |              |      |            |     |             |             | the actuation   | input       | and image | feedback   |           | for kinematic | control, |     |
| Jacobian    | matrix | in the       | last | step may   | not | be accurate | and         |                 |             |           |            |           |               |          |     |
|             |        |              |      |            |     |             |             | and the authors | of          | [21] plan | the        | actuation | variables     | based    | on  |
suitableforthisstep.ItischallengingfortheoriginalJacobian the temporal values. There are many regression approaches
| estimation      | method      | to            | face | complex     | tasks    | due    | to its over- |             |              |               |        |            |            |       |        |
| --------------- | ----------- | ------------- | ---- | ----------- | -------- | ------ | ------------ | ----------- | ------------ | ------------- | ------ | ---------- | ---------- | ----- | ------ |
|                 |             |               |      |             |          |        |              | utilized in | soft robots, | like          | linear | regression | [71],      | local | weight |
| simplification. | Therefore,  |               | some | researchers |          | try to | adapt this   |             |              |               |        |            |            |       |        |
|                 |             |               |      |             |          |        |              | regression  | (LWR)        | [72], support |        | vector     | regression | (SVR) | [73],  |
| method          | for various | applications. |      | For         | example, |        | the authors  |             |              |               |        |            |            |       |        |
|                 |             |               |      |             |          |        |              | Gaussian    | process      | regression    | (GPR)  | [25],      | and        | local | weight |
of[64]alsoemphasizethattheremaybeasignificantdeviation
|           |               |     |           |               |            |         |          | projection      | regression   | (LWPR)  | [16].   | Other | than          | the regression |     |
| --------- | ------------- | --- | --------- | ------------- | ---------- | ------- | -------- | --------------- | ------------ | ------- | ------- | ----- | ------------- | -------------- | --- |
| between   | the estimated |     | and       | real Jacobian |            | matrix, | and they |                 |              |         |         |       |               |                |     |
|           |               |     |           |               |            |         |          | methods,        | the Gaussian | mixture |         | model | (GMM)         | [74] summa-    |     |
| alleviate | this issue    | by  | smoothing | the           | activation | values. | Force-   |                 |              |         |         |       |               |                |     |
|           |               |     |           |               |            |         |          | rizes collected | data         | with    | a joint | data  | distribution, | and            | the |
displacementmodelisincludedforforcecontrolin[20].When
|     |     |     |     |     |     |     |     | extended | Kalman | filter (EKF) |     | [39] estimates |     | robot states | as  |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ------------ | --- | -------------- | --- | ------------ | --- |
endeffectorandactuationdisplacementbetweenonlyonestep
an observer.
| is involved    | in [34],     | the        | displacement |             | among    | multiple    | steps      | is            |        |     |     |     |     |     |     |
| -------------- | ------------ | ---------- | ------------ | ----------- | -------- | ----------- | ---------- | ------------- | ------ | --- | --- | --- | --- | --- | --- |
| utilized       | in [65].     | Also,      | the Jacobian | matrix      |          | is adjusted | in [66]    |               |        |     |     |     |     |     |     |
| by multiplying |              | a rotating | matrix       | considering |          | the         | difference |               |        |     |     |     |     |     |     |
|                |              |            |              |             |          |             |            | A. Regression | Method |     |     |     |     |     |     |
| between        | the intended |            | and measured |             | motions. | The         | fusion of  |               |        |     |     |     |     |     |     |
sensing information from a camera and FBG provides accu- Regression methods with different models are employed in
rate positions in [63] for stable and precise Jacobian matrix soft robot modeling and control. These methods aim to fit
estimation. the training data with a specific model, like a linear function
Although so many adaptations have been proposed, the or a Gaussian process, by optimizing the parameters and
Jacobian matrix is still an initial solution for many labs decreasing the loss. Then, the trained regression model can
and motivates applying the other approaches, especially data- take some observation samples as model input and predict the
driven ones. A neural network is applied for control in [67], correspondingvalues.Forinstance,linearregression,asimple
which is based on the Jacobian matrix estimation process. regression approach, is applied in [71] to map FBG signals
A honeycomb pneumatic networks arm is controlled by the into soft robot end position for sensing. A linear function is
inverse Jacobian matrix in [68], and the same soft robot is included for fitting, and the parameter matrix is optimized.
includedin[69]forchallengingmanipulationtasks.Thelatter Similarly, LWR employs the linear function but considers
work employs the Jacobian matrix in a low-level behavior the distance between the collected data and the observation
controller and compares it with RL. samples for fitting. In [72], data from human demonstrations
In summary, the Jacobian matrix is a concise and simple is used for fitting. The temporal value is taken as input to
method for soft robots. The matrix is updated online with decide action for control.
a high frequency in most cases, which can be achieved SVR is utilized in [73] for the forward kinematic modeling
due to the simple structure. Meanwhile, the oversimplified and in [75] for the close loop position controller. It has been
linearization necessitates online updating and high control proven in [75] that SVR gets better approximation accuracy
frequency. A comparison of some typical papers using the than NN on a simple function, but this model requires more
Jacobian matrix is shown in Table III. This table contains the convergence time than NN on a large amount of data (15625
firstpaperemployingtheJacobianmatrixforsoftrobotcontrol samples) in [73], which may be caused by the different
[34]. Force control is achieved in [20] considering a force optimization strategies or mature NN optimization software.
modelinthecontroloptimizationproblem.Theauthorsofthe The SVR modeling and control algorithm in [75] can be

2246 IEEETRANSACTIONSONAUTOMATIONSCIENCEANDENGINEERING,VOL.22,2025
summarized as models and weighs them with Gaussian kernels. The covari-
M n ances of these kernels are decided by an incremental gradient
1X X
min ∥w ∥2+C L(µ ), descent based on stochastic leave-one-out cross validation
j i
W,B 2
j=1 i=1 criterion[76],[77].Tofindtheoptimizationoftheparameters
s.t. µ =∥y −(φ(x )W +B)∥ inlinearmodels,whichisaredundancyproblem,anull-space
i i i
behavior is defined as a guide. This user-defined behavior is
W =[w ,w ,...,w ] (3)
1 2 M applied in a cost function and attracts the actual behaviors.
where d,M are the dimensions of the mapping input x and For example, the robot elongation is minimized in [16] for
i
output y, and n is the size of the learning dataset. The a relatively straight shape, and the overall inflated chamber
i
function φ(x )W + B aims to estimate the mapping output pressures are minimized during the control process in [78].
i
with a nonlinear transformation φ(·) : R1×d → R1×h and
the optimized matrices W ∈ h × M and B ∈ 1× M. L(·) B. Gaussian Mixture Model
is a loss function and the extended Vapnik ϵ-insensitive loss
GMM encodes collected data into a data distribution com-
functionbasedonL2-normisappliedin[75].C isthetradeoff
posed of multiple Gaussian components. In the fitting step,
parameterthatadjuststheestimationerrorsandregularization.
GMM parameters are optimized to fit the collected data. Dur-
For kinematics modeling, SVR takes the actuation as input x
ing the prediction step, the input data works as the prior, and
and estimates y as the robot state. For control, which can be
the posterior of GMM under some input data will be used as
seen as the inverse process of modeling, SVR receives the
predictionoutput.Ofnote,onceaGMMisbuilt,eachkindof
desired displacement as input and decides the actuation.
dataplaysthesameroleinprinciple.Insuchajointprobability
GPR employs the Gaussian process, a probability distribu-
densityfunction,everydimensioncanbeappliedasapriorand
tion over functions, for fitting. For modeling, GPR predicts
derive expectations on the remaining dimensions. In this case,
robotstates,suchaspositionorshapeparameters,basedonthe
GMMin[74]producesbothforwardkinematicsmodelingand
training dataset and current actuation variables. For example,
position control strategy with actuation variables and desired
GPRisappliedin[25]topredicttheactuatorcurvature.Given
endpositionsastheprior,respectively.Thecatheterkinematic
N training inputs X = [x ,x ,...,x ]T ∈ RN×i and N
1 2 N GMM is represented by the joint probability density function:
curvatures as the training outputs Y = [y ,y ,...,y ]T ∈
1 2 N
RN×1, where i represents the dimension of each input x. The P[p[k+1],p[k],a], (6)
prediction process based on the test input x can be shown as
t
where p[k] denotes the robot state at step k. The forward
µ(x )=k (X,x )TK(X,X)−1Y,
t ∗ t modeling process can be shown as
(cid:54)(x t )=k(x t ,x t )−k ∗ (X,x t )TK(X,X)−1k ∗ (X,x t ), (4) E[p[k+1]|p[k],a], (7)
where µ(x ) and (cid:54)(x ) are the predictive mean and vari-
t t
ance. k(·,·) ∈ R is the kernel function applied in GPR, which is the conditional mean of the model Eq. 6 given the
a squared-exponential kernel function in most cases, and robot state p[k] and actuation a. The control strategy is
k
K ∗ (
(
X
X
,
,x
X t )
)
∈
=
RN
[k
×
(
N
x
1 i
,
s
x
a t
),
c
k
ov
(x
a 2 ri
,
a
x
n t c
)
e
,.
m
..
a
,
tr
k
i
(
x
x
N w
,
it
x
h t
)
e
]T
ntri
∈
es K
RN×
=
1.
E[a|p d [k+1],p[k]], (8)
ij
k(x ,x ),i, j = 1,2,...,N. The above prediction process
i j which is the conditional mean of the model Eq. 6 given the
supposes that the prior mean is zero, and one can preprocess robot state p[k] and desired state p [k+1].
d
the sample output Y by zeroing the mean before fitting and
In addition to modeling and control, such data encoding
prediction.Itshouldbenoticedthatthenoiseofthemappingis
characteristic develops some planning solutions. For exam-
considered in [70], which is assumed as white Gaussian noise
ple, the authors of [21] encode pose and temporal value
with zero mean and variance σ2. In this case, the prediction
n into a GMM for navigating through narrow holes based on
can be derived as
human demonstration. Moreover, other task parameters like
µ(x )=k (X,x )T(K(X,X)+σ2I)−1 Y, the rotation matrix of the coordinate system are included as
t ∗ t n
the planning objects in the GMM of [79]. Making use of
(cid:54)(x )=k(x ,x )−k (X,x )T(K(X,X)+σ2I)−1 k (X,x ).
t t t ∗ t n ∗ t its encoding ability, GMM transfers demonstrations on rigid
(5) robots to the STIFF-FLOP continuum robot in [80].
With the forward model derived from GPR, the authors of [4]
C. Extended Kalman Filter
propose a control strategy by minimizing a cost function
containing the predicted errors and actuation variables. GPR Considering one existing model and its prediction, the
is also employed in close-loop kinematics control in [70] by Kalman filter can be applied as an observer and corrects
predicting desired actuation variables based on the robot state the predicted values with measurement. Due to the nonlinear
feedback. The authors of [15] aim to predict the difference of responses from soft robots, most modeling process is non-
robot states instead of only the next states as the modeling linear, and the extended Kalman filter (EKF), instead of the
part in optimal control. original linear Kalman filter, is widely applied in soft robots.
Based on LWR, which utilizes each training data as a P,Q,R represent the estimation covariance, process noise
local model, LWPR projects training data into several linear covariance, and measurement noise covariance, respectively.

CHENetal.:DATA-DRIVENMETHODSAPPLIEDTOSOFTROBOTMODELINGANDCONTROL:AREVIEW 2247
In prediction, the state at the k+1 step is predicted as p k+1|k modeling in [70]. Then, only one online learning GPR model
based on the state p k|k and actuation a k at the k step. is employed to model the whole working space in [15], and
a meta-learning GPR model is employed in [90] for multiple
p = f(p ,a ),
k+1|k k|k k new unknown working spaces.
P k+1|k = A k P k|k A k T +Q k , (9) Statisticalmethodsmakedatadistributionassumptionsfrom
where f(·,·) represents the nonlinear forward modeling, A the perspective of statistics. They can attain an acceptable
k
isthelocallinearizationof f(·,·).Thecorrectionprocesscor- performance even with a small amount of data and become
more effective with more data. Moreover, most of them can
rectsthepredictionstateto p k+1|k+1 consideringmeasurement
be leveraged for both modeling and control. A comparison of
output s from sensing.
k
some typical papers applying statistical methods is shown in
K = P CT(C P CT + R )−1, Table IV. This table first includes a simple regression model
k k+1|k k k k+1|k k k
p = p +K (s −g(p )), SVR in [75], then includes two regression approaches GPR
k+1|k+1 k+1|k k k k+1|k
in [15] and LWPR in [16]. Finally, the observer EKF in [81]
P k+1|k+1 =(I −K k C k )P k+1|k , (10) is introduced.
whereg(·)representsthemeasurementprocess,C k isthelocal IV. NEURALNETWORK
linearizationof g(·). K istheKalmanGainandevaluatesthe
k Considerable efforts have been focused on NN applications
reliability of measurement and prediction. EKF is commonly
in the soft robot field. In the early years, extreme learning
leveraged since it adjusts the modeling process and provides
machines (ELM) [91] and radial basis function (RBF) [35]
an accurate robot state estimation. For example, the authors
werepopularchoices.Nowadays,researchersprefermultilayer
of[81]mapactuatorvariablesandsegmentparametersintothe
perceptron (MLP) [92] and recurrent neural network (RNN)
robot pose to build the nonlinear forward modeling with the
[93] due to their generalized and sequence-related structures,
transformation matrices, and the sensing signal from position
respectively. Moreover, for some special proposes like image
sensors is applied for correction. The authors of [82] aim to
processing, autoencoder (AE) [94] and convolutional neural
estimate robot poses and physical parameters and apply pose
network (CNN) [95] are utilized. Some typical NNs are
measurement for correction. NNs like wavelet networks [83]
shown in Fig. 6.
are also employed as the forward model in EKF for curvature
angle estimation. In their following research, the authors A. ELM and RBF
of[84]alsoestimatetheexternalforceastheunknownsystem
ELMonlycomprisesaninputlayerandanoutputlayer.The
input based on the state estimation from a similar EKF.
input layer weights and bias are randomly assigned before
Similarly,theunknownexternalforcesaretakenasthesystem
training and fixed during training, while the output layer
state p and accurately estimated in [85]. Furthermore, due to
weights are trained to decrease loss. A simple loss is utilized
the modular structure of the snake robot in [86], the EKF is
in [96] for kinematics control, which only aims to decrease
adaptedbychangingthedimensionofstatevariablesaccording
the estimation error. The ELM is
to the advancing or retracting motion for shape estimation.
aˆ = Wout · f(Winp· p+B), (11)
D. Summary Statistical Method where aˆ,p denote the estimated actuation value and the robot
Because statistical models only consider data relationships, state,Wout,Winp denotetheoutputandinputlayerweights, B
such models have shown high potential to cope with vari- denotesbias,and f(x)=(1+e−x)−1isthesigmoidactivation
ous kinds of data. At first, statistical models only include function.ThetrainingprocessoftheoriginalELMin[96]can
robot actuation for modeling [87]. Then, position feedback be shown as
is involved in [75] for adaptive modeling and control. Fur- min ∥A− A ˆ∥,
thermore, temporal values are applied for control in [21] and Wout
[72]. The authors of [70] even include visual information for s.t. A ˆ = Wout · P, (12)
kinematic control. Recently, sensing information from various
where A and P are all the real actions and input layer output
sensors like resistance and force sensors has been employed
ˆ
in the training dataset, and A is the ELM estimation based on
in [84] and [88] for modeling adjustment. Most statistical
P. The optimized output layer weights are W ˆout = A · P†,
approachescanbeappliedforbothmodelingandcontrolwith
where P† is the pseudo-inverse of the input layer output P.
different inputs, like two SVR models in [75].
In addition to estimation error, the authors of [97] and [98]
Besides data categories, the methods also evolve over time.
involvethenormoftheoutputweightmatrixintooptimization
For instance, the Jacobian matrix is involved in the EKF
errorasaregularizationtermtoavoidtoolargeoutputweights
in [85], and the pseudo rigid robot model takes its place
forkinematicscontrol.Constraintsontherangeofoutputsare
in[89].Theauthorsof[39]applytheadaptativeKalmanfilter,
applied in the ELM controller [3] according to the constraints
which shows strong robustness against the model nonlinear-
of the real actuation. The training process can be shown as
ity and uncertainty instead of EKF. Recently, the unscented
N
Kalmanfilterisleveragedin[88],whichcanapplytheimplicit min X ∥a −aˆ ∥2+α·∥Wout∥2,
Gaussian process for robot modeling. Also, GPR also evolves i i
Wout
over time. The whole working space is divided into several
i=0
s.t. aˆ = Wout · f(Winp·p+B),
regions, and each part requires a single GPR model for local

2248 IEEETRANSACTIONSONAUTOMATIONSCIENCEANDENGINEERING,VOL.22,2025
TABLEIV
STATISTICALMETHODPAPERCOMPARISON
Fig. 6. Diagrams of (a) MLP, (b) RNN, and (c) CNN. MLP is composed of multiple layers. Parameters W∗ ,B∗ in one layer are in parallel and can be
trained simultaneously. RNN takes the input data x sequentially, and each bar shares the same weights WS ,Wx ,Wy ,bx , and by. CNN obtains matrix with
channelC1,height H1,andwidthW1 asinput.Inthenetworkfeedforward,thechannelnumberimproveswhilethewidthandheightdecreaseusingkernels.
Finally,CNNoutputsamatrixwithdimension(Cn ,1,1),andafullyconnectedlayerisemployedtomaptothetargetdimensionk.
∂
aˆ(p)>0:∀p∈(cid:127), i =1,...,n control, the desired and real robot states are input, and MLP
∂p
i can provide the estimated actuation.
a min <aˆ(p)<a max :∀p∈(cid:127), i =1,...,n (13) The first paper utilizing MLP in the soft robot field is [99],
which is also the first paper utilizing NN. This work designs
where a is the real actuation value, α is the regulation
a particular parameter updating strategy for control instead of
parameter, N isthesizeofthetrainingdataset,nisthedegrees
the backpropagation widely applied now. Similarly, training
ofactuation,and(cid:127)representsasetofsamplesbasicallycover
data is normalized in [92] with principal component analysis
the input space. The second condition guarantees that ELM
(PCA) instead of batch and layer normalization, which are
has the same actuation direction as the real conditions, and
widely employed currently. MLP has many hyperparameters
the third is the actuation range constraint. Recently, ELM has
and changeable components, and plenty of papers have been
been utilized for online pose estimation in [40] thanks to its
conducted on them. For example, the authors of [100] com-
simple structure and fewer parameters compared with other
pare the performance of MLPs composed of different neuron
complicated NNs.
numbers on position control tasks. Three activation functions
Based on the structure of ELM, RBF changes the activa-
(i.e., log-sigmoid, linear, and tan-sigmoid) are tested in [47]
tion function from a sigmoid activation function to multiple
forpneumaticrobotmodeling.Thestochasticgradientdescent
Gaussian functions in [35] for forward kinematic modeling.
(SGD) optimizer is applied in [101] instead of the popular
Clustering can be applied to the training dataset to select
Adam optimizer. The authors of [24] comprehensively inves-
the center of the Gaussian functions [98]. Although ELM
tigate the influence of hidden layer number, neuron number,
and RBF include some basic elements of NN, e.g., activation
and batch size on training time and validation loss of sensing
functionsandneurons,theycontainsomedesignedconstraints
tasks. In general, there is no optimal combination of the
forspecifictasksandwasteapartoftheirpotentialmainlydue
hyperparameters and component structures for all tasks, but
to the fixed parameters.
mostchoicescanobtainacceptableperformanceonmosttasks.
The detailed influence of each hyperparameter on the MLP
B. MLP performance has yet to be fully explored and explained.
Some uncommon MLPs have been applied to soft robots.
MLPisthemostpopularNN.ThediagramofMLPisshown
Theauthorsof[22]providetargetstothehiddenneuronsofthe
in Fig. 6-(a). Generally, MLP can be shown as
MLP directly, similar to the conditional generative adversarial
y = W · f(W · f(...W · f(x)+B ...)+B )+B , network (CGAN), which takes advantage of the information
n n−1 0 0 n−1 n
thatisindirectlyrelatedtothemappingbutrestrictsthepoten-
(14)
tial of NN. A U-Net-like MLP is leveraged in [102] for robot
whereW ,B representnetworkweightandbiasofn-thlayer, modelinginmodelpredictivecontrol(MPC), whichconnects
n n
and y,x are the output and input of MLP. To model a robot, the former and latter layers sequentially. Multiple MLPs are
the input is actuation, and the output is the robot state. For connected in [103], which have different applications, e.g.,

CHENetal.:DATA-DRIVENMETHODSAPPLIEDTOSOFTROBOTMODELINGANDCONTROL:AREVIEW 2249
forward kinematics modeling in simulation and sim-to-real behaviors. In summary, RNNs perform satisfactorily on vari-
transfer learning. The combined MLP can collect actions in oustasksduetotheirsequentialstructuresandmemoryability.
| simulation | and   | estimate | the | corresponding | robot | states. |          |            |     |     |     |     |     |     |
| ---------- | ----- | -------- | --- | ------------- | ----- | ------- | -------- | ---------- | --- | --- | --- | --- | --- | --- |
|            |       |          |     |               |       |         |          | D. Special | NN  |     |     |     |     |     |
| For soft   | robot | modeling | and | control,      | some  | unique  | features |            |     |     |     |     |     |     |
of MLP are developed. For example, the inputs of some There are some NNs that take advantage of visual infor-
MLPs take physical models into consideration. Based on the mation in soft robot control. For example, AE is utilized to
concentric tube model, the translations and rotations of the extract features from the images of soft robots in [94] and
| concentric | tubes | are | employed | into | MLP | inputs | in [104] |          |             |            |           |        |     |           |
| ---------- | ----- | --- | -------- | ---- | --- | ------ | -------- | -------- | ----------- | ---------- | --------- | ------ | --- | --------- |
|            |       |     |          |      |     |        |          | estimate | the robot’s | shape. CNN | estimates | shapes |     | [115] and |
for modeling. Furthermore, the authors of [105] compare jointvalues[116]basedonrobotimages.ThediagramofCNN
different joint space forms of the concentric tubes as input is shown in Fig. 6-(c). Also, CNN can predict the orientation
on the forward modeling estimation tasks. Similarly, PCC is of the placenta in [95] and encodes robot deformation for
included in [54] by taking curvatures and curve lengths as shape estimation with the help of markers inside the chamber
| MLP input. | The | authors | of  | [106] utilize | MLP | to  | estimate |           |              |          |     |        |      |         |
| ---------- | --- | ------- | --- | ------------- | --- | --- | -------- | --------- | ------------ | -------- | --- | ------ | ---- | ------- |
|            |     |         |     |               |     |     |          | in [117]. | Furthermore, | although | RNN | is the | most | popular |
physicalparameterslikemassinertiamatrix,whichisamodel- choice for sequential information processing, CNN can also
basedapproachwithNN.Duetothetime-delayedmotion,end be applied for dynamic modeling using rearranged pressure
positionsinthecurrentandpasttimestepsarefedintotheMLP inputs [118]. The space relationship in a matrix is leveraged
in [107] for control. to infer the sequential relationship of an actuation sequence
|     |     |     |     |     |     |     |     | for hysteresis | modeling. | A 3D         | NN    | is employed | in  | [119] for |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --------- | ------------ | ----- | ----------- | --- | --------- |
|     |     |     |     |     |     |     |     | a segmental    | surgical  | manipulator, | which | considers   |     | the time  |
C. RNN
|     |           |     |         |             |     |              |     | sequence | betweenlayers | and | the segmentalsequence |     |     | between |
| --- | --------- | --- | ------- | ----------- | --- | ------------ | --- | -------- | ------------- | --- | --------------------- | --- | --- | ------- |
| RNN | is a kind | of  | NN that | is designed |     | specifically | for |          |               |     |                       |     |     |         |
neuronsforplanning.Spatialsequencesofsoftmodularrobots
| sequential | data. | The diagram |     | of RNN | is shown | in Fig. | 6-(b). |     |     |     |     |     |     |     |
| ---------- | ----- | ----------- | --- | ------ | -------- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- |
areconsideredin[120]byutilizingbidirectionalRNN.Agen-
| Although | MLP | can also | receive | temporal | data, | it is | fed into |     |     |     |     |     |     |     |
| -------- | --- | -------- | ------- | -------- | ----- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
erativeadversarialnetwork(GAN)isutilizedforsyntheticdata
| networks | simultaneously |     | and | fails to infer | the | sequential | rela- |           |     |     |     |     |     |     |
| -------- | -------------- | --- | --- | -------------- | --- | ---------- | ----- | --------- | --- | --- | --- | --- | --- | --- |
|          |                |     |     |                |     |            |       | in [121]. |     |     |     |     |     |     |
tionship.RNNtakesdatainsequenceusingrecurrentstructure.
The n-th bar in Fig. 6-(b) can be represented as E. Summary Neural Network
S = f(W ·x +W ·S +b ), TheapplicationofNNinsoftrobotsstartedwith[99].First,
|     |     | n   | x n | s   | n−1 | x   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
y =g(W ·S +b ), (15) somesimplenetworkslikeELMandRBFareincluded.Then,
|     |     | n   | y n | y   |     |     |     |          |             |        |     |             |      |        |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | ------ | --- | ----------- | ---- | ------ |
|     |     |     |     |     |     |     |     | with the | development | of NN, | the | researchers | give | up the |
where W ,b are the RNN weight and bias parameters, S constraints of ELM, change the activation function of RBF,
|     | ∗ ∗ |     |     |     |     |     |     | n   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
f(),g()
is the hidden state of the step n, and are activation and enlarge the network. In this case, MLP becomes a good
functions. As shown in Fig. 6-(b), the network of each step tool for both modeling and control. Furthermore, due to the
takesthehiddenstatefromthepreviousstep.Suchastructure
|     |     |     |     |     |     |     |     | hysteresis | of soft robots, | RNN | is applied | to  | deal with | time- |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --------------- | --- | ---------- | --- | --------- | ----- |
infers the sequential relationship of data while the other NNs related data. AE and CNN are employed to process images.
take the data input simultaneously. In this case, RNN is more To summarize, owing to the large variety of structures,
suitable than the other networks like MLP and CNN for soft NN is attractive to soft robot research. For most issues in
robots, which provide delayed responses. The modeling and soft robot modeling and control, it is highly possible to find
| control with | RNN | share | the | same data | category | requirement |     |           |              |          |      |        |         |         |
| ------------ | --- | ----- | --- | --------- | -------- | ----------- | --- | --------- | ------------ | -------- | ---- | ------ | ------- | ------- |
|              |     |       |     |           |          |             |     | a related | NN solution. | However, | such | models | require | a large |
with MLP mentioned in Eq. 14, but RNN needs data from amount of data due to their complicated structures, and it is
multiple time steps instead of a single time step. challenging to update them online. A comparison of some
The first RNN applied is modified Elman NN in [108], typical papers applying NNs is shown in Table V. This table
which restores information in previous steps with context begins with a simple NN, RBF [122]. Then, a common NN,
| nodes for | dynamic | control. | Then, | researchers |     | leverage | a non- |             |            |            |              |     |            |     |
| --------- | ------- | -------- | ----- | ----------- | --- | -------- | ------ | ----------- | ---------- | ---------- | ------------ | --- | ---------- | --- |
|           |         |          |       |             |     |          |        | MLP [24],is | includedin | thistable. | Finally,LSTM |     | forcontrol |     |
linear autoregressive network with exogenous inputs (NARX) [32]andCNNformodeling[118]aresummarizedinTableV.
inaseriesofpapers[19],[67],[93]fordynamiccontrol.This
| kind of | RNN receives |     | outputs | in previous | steps | as  | a part of |     |     |     |     |     |     |     |
| ------- | ------------ | --- | ------- | ----------- | ----- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
V. REINFORCEMENTLEARNING
| input in | the current | step. |     |     |     |     |     |     |     |     |     |     |     |     |
| -------- | ----------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Long short-term memory (LSTM) is a kind of RNN pro- RL copes with high-level tasks by exploring the environ-
posedforlong-termdependenceissues.Thisnetworkhasbeen ment and exploiting data collected during exploration. This
used on endoscopic robot distal force prediction [109], [110] strategy trains an agent for complicated tasks and requires a
|              |       |          |     |               |            |     |        | long learning | time | and a massive | amount | of  | data. | The agent |
| ------------ | ----- | -------- | --- | ------------- | ---------- | --- | ------ | ------------- | ---- | ------------- | ------ | --- | ----- | --------- |
| and external | force | position |     | and magnitude | prediction |     | [111]. |               |      |               |        |     |       |           |
Moreover, such a network can cope with sensing signals from istrainedconsideringdefinedrewardfunctions.Thisapproach
nonlinear time-variant soft sensors and achieves tasks like cannot be used for modeling. Moreover, it requires exploring
position prediction [112], object recognition [113], and shape environments, which may be provided by modeling methods.
| reconstruction |     | [94]. In | addition | to perception, |     | the | authors |     |     |     |     |     |     |     |
| -------------- | --- | -------- | -------- | -------------- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
of [32] dynamically control a robotic catheter with LSTM to A. RL Implementation
decrease contact force. The authors of [114] employ LSTM In the early years, statistical models were applied as the
as an offline dynamic controller to cope with the nonlinear agents in RL instead of NN. A GPR model named Gaussian

2250 IEEETRANSACTIONSONAUTOMATIONSCIENCEANDENGINEERING,VOL.22,2025
TABLEV
NEURALNETWORKPAPERCOMPARISON
TABLEVI
REINFORCEMENTLEARNINGPAPERCOMPARISON
process temporal difference method is employed in [123] to The infinite DOFs lead to wide actuation and state spaces,
control an octopus arm. As the RL agent, a GMM is trained whichbringaburdentoexplorethewholeenvironment.Inthis
to estimate robot shape and contact in [124] and control a case, most researchers discretize these spaces. The action
flexible surgical robot to go through a tube in [125]. For spacein[123]isrestrictedtoonlysixavailableactions,andthe
roboticcathetercontrolinsideanarrowtube,ajointprobability authors of [37] discretize the workspace into a 3D grid with
distribution is learned considering various variables like tip a resolution of 0.01 m. Although discretization limits the RL
andentrancepoints,touchstate,andactionin[33].Q-learning potential,itproducessimplespacesanddecreasesthetraining
isimplementedwithaQtableorQfunctionastheagent.The time. The soft robot in [131] is able to keep the end position
A S invariant while changing the orientation with the help of RL.
| agent decides | the | action | based on | the state | and | a certain |     |     |     |     |     |     |     |
| ------------- | --- | ------ | -------- | --------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
ϵ
policy like greedy. The training process of the Q table or OneofthemostconsiderablechallengesofRLisexploring
function can be shown as the real world, which has a high time cost and may damage
Q(S ,A )←α[R(S ,A )+γ maxQ(S ,a)−Q(S ,A )] robots. Therefore, modeling in simulation, especially with
| t   | t   | t   | t   | t+1 |     | t t |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
a physical methods, is widely utilized in the training process.
+Q(S,A ), (16) The authors of [132] first train an RL strategy to control a
t t
roboticcathetersysteminasimulatornamedCoppeliaSimand
| where S | is the | state at | time t, A is | the action | decided | by the |     |     |     |     |     |     |     |
| ------- | ------ | -------- | ------------ | ---------- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- |
t t then test it on the real robot. Constant curvature (CC), a soft
| Q table or | function | according | to the | state | S, and | R(S,A ) | is  |     |     |     |     |     |     |
| ---------- | -------- | --------- | ------ | ----- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- |
|            |          |           |        |       | t      | t t     |     |     |     |     |     |     |     |
therewardfunction.α andγ robot modeling method, provides a simulation environment
arethelearningrateanddiscount
|                          |     |     |                          |     |     |     | for [133] | at first, and | the | NN agent | continues | to  | learn in |
| ------------------------ | --- | --- | ------------------------ | --- | --- | --- | --------- | ------------- | --- | -------- | --------- | --- | -------- |
| rate,respectively.maxQ(S |     |     | ,a)meansthemaximalQvalue |     |     |     |           |               |     |          |           |     |          |
t+1 the real world using the Deep Deterministic Policy Gradient
a
| for the state | S t+1    | and        | every possible | action     | a. For             | example,    |               |               |             |           |               |             |            |
| ------------- | -------- | ---------- | -------------- | ---------- | ------------------ | ----------- | ------------- | ------------- | ----------- | --------- | ------------- | ----------- | ---------- |
|               |          |            |                |            |                    |             | method        | (DDPG). In    | most        | cases,    | the explored  | environment |            |
| the authors   | of [69]  | exploit    | Q-learning     | for        | many sophisticated |             |               |               |             |           |               |             |            |
|               |          |            |                |            |                    |             | is modeled    | by a trained  | NN.         | For       | example,      | MLP         | is applied |
| control tasks | like     | turning    | a handwheel,   |            | unscrewing         | a bottle    |               |               |             |           |               |             |            |
|               |          |            |                |            |                    |             | for modeling  | in [134]      | as the      | exploring | environment.  |             | Also,      |
| cap, drawing  | a        | line with  | a ruler, and   | so on.     |                    |             |               |               |             |           |               |             |            |
|               |          |            |                |            |                    |             | RNNs are      | utilized in   | [23], [38], | which     | are           | NARX and    | LSTM       |
| With the      | help     | of NN      | as an agent,   | RL         | not only           | achieves    |               |               |             |           |               |             |            |
|               |          |            |                |            |                    |             | respectively, | for forward   | modeling    |           | of segmented  | pneumatic   |            |
| simple tasks  | like     | position   | reach [126]    | and        | trajectory         | follow-     |               |               |             |           |               |             |            |
|               |          |            |                |            |                    |             | robots. Then, | RL agents     | are         | trained   | and validated | in          | reality.   |
| ing [127]     | but also | addresses  | some           | complex    | issues             | like gait   |               |               |             |           |               |             |            |
| design [128]. | A        | soft snake | robot is       | controlled | to                 | move on the |               |               |             |           |               |             |            |
|               |          |            |                |            |                    |             | C. Summary    | Reinforcement |             | Learning  |               |             |            |
groundandarriveattargetpositionsin[128].Itischallenging
| to control | the robot | gait | with traditional | control | methods, | but |                |     |             |       |        |          |         |
| ---------- | --------- | ---- | ---------------- | ------- | -------- | --- | -------------- | --- | ----------- | ----- | ------ | -------- | ------- |
|            |           |      |                  |         |          |     | RL application | in  | soft robots | first | starts | with the | help of |
RL is utilized for gait design and obstacle avoidance in [129]. statistical models as agents, and then NNs take the place due
The authors of [130] fuse the visual and shape information totheirgeneralization.DiscretizationiswidelyappliedforRL
with NN in RL and control a flexible endoscopy to navigate. in soft robots. Meanwhile, RL leverages soft robot simulators
|          |             |     |     |     |     |     | and stimulates | their              | development. |      | With such   | RL     | strategies, |
| -------- | ----------- | --- | --- | --- | --- | --- | -------------- | ------------------ | ------------ | ---- | ----------- | ------ | ----------- |
| B. RL in | Soft Robots |     |     |     |     |     |                |                    |              |      |             |        |             |
|          |             |     |     |     |     |     | now soft       | robots can achieve |              | some | complicated | tasks. |             |
SoftrobotscantakeadvantageofvariousuniqueRLstrate- Compared with other approaches, RL requires the most
gies specifically for soft robots to cope with some challenges. enormous amount of data. More critically, a predefined agent

CHENetal.:DATA-DRIVENMETHODSAPPLIEDTOSOFTROBOTMODELINGANDCONTROL:AREVIEW 2251
TABLEVII
SUMMARYOFPAPERSAFTER2019
andinteractionwiththeenvironmentarenecessary.Following which is more complicated, and RNN [19], which can cope
such a high cost, RL can fulfill complex and high-level with time-related data, have shown their benefits. Similar to
tasks. With some adaptation strategies like discretization and statistical models, NN can also be applied for both modeling
simulation transfer learning, the time and resource costs can and control. RL shows good performance on position control
be reduced to some extent. A comparison of typical papers [38],planning[31],andevensomesophisticatedmanipulation
applying RL is shown in Table VI. This table begins with an tasks [69]. Generally, RL does not provide a robot model but
RLstrategyapplyingthestatisticalmodelGaussianprocessas exploits an existing environment. The papers based on data-
agent[123],andtheauthorsof[127]applyNNsforRL.Then, driven methods, which are cited in this review and published
twostrategiesforsoftrobotRLareincluded.RLstrategieslike after 2019, are summarized in Table VII.
discretization are employed in [37], and the authors of [133] It is apparent that sophisticated models like RL require a
pretrain the agent in simulation and test it in reality. larger amount of data while achieving better performance,
|     |     |     |     |     |     |     | but they | also | improve | the | computation | cost. | Oversimplified |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---- | ------- | --- | ----------- | ----- | -------------- |
VI. CONCLUSIONANDDISCUSSIONS approaches like the Jacobian matrix are only feasible for
|                |                          |               |                  |               |             |       | limited          | simple   | tasks,          | but they | are                | easy to     | understand and |
| -------------- | ------------------------ | ------------- | ---------------- | ------------- | ----------- | ----- | ---------------- | -------- | --------------- | -------- | ------------------ | ----------- | -------------- |
| In this        | section, we summarize    |               | the foundations, |               | data-driven |       |                  |          |                 |          |                    |             |                |
|                |                          |               |                  |               |             |       | can achieve      | a        | high control    |          | frequency.         | Considering | both cost      |
| methods,       | and their representative |               | papers           | in Subsection |             | VI-A. |                  |          |                 |          |                    |             |                |
|                |                          |               |                  |               |             |       | and performance, |          | each            | model    | has                | its own     | advantages and |
| The benefits   | and limitations          |               | of data-driven   |               | approaches  |       |                  |          |                 |          |                    |             |                |
|                |                          |               |                  |               |             |       | disadvantages,   |          | and there       | is       | no optimal         | solution    | for all tasks. |
| involved       | in the review            | are           | included         | and           | compared    | in    |                  |          |                 |          |                    |             |                |
| Subsection     | VI-B. Finally,           | we            | forecast         | the emerging  | directions  |       |                  |          |                 |          |                    |             |                |
| for soft robot | research                 | in Subsection | VI-C.            |               |             |       |                  |          |                 |          |                    |             |                |
|                |                          |               |                  |               |             |       | B. Advantages    |          | and Limitations |          |                    |             |                |
|                |                          |               |                  |               |             |       | Statistical      | modeling |                 | and      | control approaches |             | are moderate   |
A. Summary
|     |     |     |     |     |     |     | and flexible | approaches |     | in  | these methods. |     | Generally, they |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ---------- | --- | --- | -------------- | --- | --------------- |
Thisreviewsummarizesthedata-drivenapproachesapplied only require a moderate amount of data, which is less than
in soft robot modeling and control. The physical approaches the NN requirement but more than the requirement of the
provide simulators for data-driven methods, like SOFA [48], Jacobian matrix. Also, the control frequency is lower than
Pyelastica [36], and SoRoSim [53]. The Jacobian matrices that of the Jacobian matrix but higher than the RL frequency.
describe soft robots and control the robots with the inverse One statistical model can be applied for both modeling and
Jacobian matrix or optimization. The authors of [34] firstly controlonline,butsomemodelsareonlylocalmodelsandlack
utilize the Jacobian matrix in the main approach. generalization ability, which can be proven by the working
Statisticalmodelsaimtoachievemodelingandcontrolwith space segmentation in [70]. NN is very suitable for soft
datasets. Regression methods like GPR [70] and LWPR [16] robot modeling and control due to the nonlinear activation
can estimate the mapping functions, and each trained model functionsandcomplexnetworkstructure.Thismodelshowsits
can be applied for either modeling or control according to general applicability. However, the data amount requirement
the input of the training data. GMM [74] encodes the dataset accelerates the aging of soft robots and takes a long time for
into a joint data distribution, which can be applied for both data collection. NN cannot be a fast and online approach due
modeling and control. Observers like EKF [88] can estimate to the slow training process. By exploring the environment
robotstatesbasedononeexistingmodelingmethod.Recently, and exploiting the data, RL can achieve some high-level tasks
NN has been the most compelling tool for soft robots. ELM like navigation. Careful planning is not required even for
[3] was a popular choice in early years, and now MLP [100], sophisticated tasks. Meanwhile, RL has a high requirement

2252 IEEETRANSACTIONSONAUTOMATIONSCIENCEANDENGINEERING,VOL.22,2025
for time and computation resources. Exploring the real world [5] J.Tolvanen,J.Hannu,andH.Jantunen,“Stretchableandwashablestrain
may damage the robots, and some environments, like the sensorbasedoncrackingstructureforhumanmotionmonitoring,”Sci.
human body, cannot be applied for exploring. Highly realistic Rep.,vol.8,no.1,p.13241,Sep.2018.
|     |     |     |     |     |     |     |     | [6] C. Laschi, | M.  | Cianchetti, | B. Mazzolai, | L.  | Margheri, | M. Follador, | and |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ----------- | ------------ | --- | --------- | ------------ | --- |
simulatorsarerequirediftheRLagentistrainedinsimulation. P.Dario,“Softrobotarminspiredbytheoctopus,”Adv.Robot.,vol.26,
To summarize, RL is a useful but consuming approach. no.7,pp.709–727,Jan.2012.
[7] S.Joe,M.Totaro,H.Wang,andL.Beccai,“Developmentoftheultra-
|     |     |     |     |     |     |     |     | light | hybrid | pneumatic | artificial | muscle: | Modelling | and optimization,” |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------ | --------- | ---------- | ------- | --------- | ------------------ | --- |
C. Emerging Directions PLoSONE,vol.16,no.4,Apr.2021,Art.no.e0250325.
|     |     |     |     |     |     |     |     | [8] A. | Menciassi, | S. Gorini, | G.  | Pernorio, | L. Weiting, | F.  | Valvo, and |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ---------- | ---------- | --- | --------- | ----------- | --- | ---------- |
P.Dario,“Design,fabricationandperformancesofabiomimeticrobotic
| In the   | other research | areas | like     | computer |           | vision | and natural  |             |     |          |           |              |              |     |            |
| -------- | -------------- | ----- | -------- | -------- | --------- | ------ | ------------ | ----------- | --- | -------- | --------- | ------------ | ------------ | --- | ---------- |
|          |                |       |          |          |           |        |              | earthworm,” |     | in Proc. | IEEE Int. | Conf. Robot. | Biomimetics, |     | Aug. 2004, |
| language | processing,    | the   | original | NN       | is simple | at     | first [135]. |             |     |          |           |              |              |     |            |
pp.274–278.
| Then, more | complex | NNs | with | large | sizes | and | different |     |     |     |     |     |     |     |     |
| ---------- | ------- | --- | ---- | ----- | ----- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
[9] R.K.Katzschmann,J.DelPreto,R.MacCurdy,andD.Rus,“Exploration
structuresareproposed,likeChatGPT,BERT[136]andYOLO ofunderwaterlifewithanacousticallycontrolledsoftroboticfish,”Sci.
[137]. Similarly, the size and complexity of NN in soft robots Robot.,vol.3,no.16,2018,Art.no.eaar3449.
|     |     |     |     |     |     |     |     | [10] J.Sun,L.Bauman,L.Yu,andB.Zhao,“Gecko-and-inchworm-inspired |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
willimprove.Suchmodelscanachievemorechallengingtasks untetheredsoftrobotforclimbingonwallsandceilings,”CellRep.Phys.
comparedwithsimpleNNs.However,largemodelsleadtolow Sci.,vol.4,no.2,Feb.2023,Art.no.101241.
frequencyforcontrolimplementation,andoneshouldconsider [11] K.C.Gallowayetal.,“Softroboticgrippersforbiologicalsamplingon
deepreefs,”SoftRobot.,vol.3,no.1,pp.23–33,Mar.2016.
| balancing       | the model | complexity  |              | and | computation |     | cost based |                                                                |     |     |     |     |     |     |     |
| --------------- | --------- | ----------- | ------------ | --- | ----------- | --- | ---------- | -------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|                 |           |             |              |     |             |     |            | [12] C.Firth,K.Dunn,M.H.Haeusler,andY.Sun,“Anthropomorphicsoft |     |     |     |     |     |     |     |
| on the modeling |           | and control | requirement. |     |             |     |            |                                                                |     |     |     |     |     |     |     |
roboticend-effectorforusewithcollaborativerobotsintheconstruction
industry,”Autom.Construct.,vol.138,Jun.2022,Art.no.104218.
| The research |          | on soft | robots | begins | with      | the application | of         |               |     |               |     |            |          |          |          |
| ------------ | -------- | ------- | ------ | ------ | --------- | --------------- | ---------- | ------------- | --- | ------------- | --- | ---------- | -------- | -------- | -------- |
|              |          |         |        |        |           |                 |            | [13] K. Chin, | T.  | Hellebrekers, | and | C. Majidi, | “Machine | learning | for soft |
| one single   | approach | and     | simple | tasks. | Recently, |                 | there have |               |     |               |     |            |          |          |          |
roboticsensingandcontrol,”Adv.Intell.Syst.,vol.2,no.6,Jun.2020,
| been some | papers | combining | multiple |     | methods | to  | solve diffi- |     |     |     |     |     |     |     |     |
| --------- | ------ | --------- | -------- | --- | ------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Art.no.1900171.
cult problems like model mismatch. For example, the authors [14] J. Wang and A. Chortos, “Control strategies for soft robot systems,”
of [114] apply offline RNN and online kinematics model for Adv.Intell.Syst.,vol.4,no.5,May2022,Art.no.2100165.
control. MPC and iterative learning controller are combined [15] Z.Q.Tang,H.L.Heung,K.Y.Tong,andZ.Li,“Aprobabilisticmodel-
|     |     |     |     |     |     |     |     | based | online | learning | optimal | control | algorithm | for soft | pneumatic |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------ | -------- | ------- | ------- | --------- | -------- | --------- |
in [60]. Two NNs are included in [138] for RL agent and actuators,” IEEE Robot. Autom. Lett., vol. 5, no. 2, pp.1437–1444,
| modelmismatchadjustment.AsdiscussedinSubsection |       |     |     |            |     |                | VI-B, | Apr.2020.                                                            |     |     |     |     |     |     |     |
| ----------------------------------------------- | ----- | --- | --- | ---------- | --- | -------------- | ----- | -------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|                                                 |       |     |     |            |     |                |       | [16] K.-H.Leeetal.,“Nonparametriconlinelearningcontrolforsoftcontin- |     |     |     |     |     |     |     |
| each method                                     | shows | its | own | advantages | and | disadvantages. |       |                                                                      |     |     |     |     |     |     |     |
uumrobot:Anenablingtechniqueforeffectiveendoscopicnavigation,”
The usage of multiple methods can take advantage of every SoftRobot.,vol.4,no.4,pp.324–337,Dec.2017.
approach and achieve better performance. [17] C. Duriez, “Control of elastic soft robots based on real-time finite
|             |     |              |     |        |        |      |             | element | method,” | in  | Proc. IEEE | Int. Conf. | Robot. | Autom., | May 2013, |
| ----------- | --- | ------------ | --- | ------ | ------ | ---- | ----------- | ------- | -------- | --- | ---------- | ---------- | ------ | ------- | --------- |
| The medical |     | environment, |     | as one | of the | most | significant |         |          |     |            |            |        |         |           |
pp.3982–3987.
| applications | of  | soft robots, | has | a high | standard |     | for safety, |                                                                   |     |     |     |     |     |     |     |
| ------------ | --- | ------------ | --- | ------ | -------- | --- | ----------- | ----------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|              |     |              |     |        |          |     |             | [18] P.E.Dupont,J.Lock,B.Itkowitz,andE.Butler,“Designandcontrolof |     |     |     |     |     |     |     |
efficiency, and convenience. To involve soft robots in medical concentric-tuberobots,”IEEETrans.Robot.,vol.26,no.2,pp.209–225,
| applications, | some | advanced | modeling |     | and | control | strategies | Apr.2010. |     |     |     |     |     |     |     |
| ------------- | ---- | -------- | -------- | --- | --- | ------- | ---------- | --------- | --- | --- | --- | --- | --- | --- | --- |
are required. Although so many works achieve controlling the [19] T. G. Thuruthel, E. Falotico, M. Manti, and C. Laschi, “Stable open
loopcontrolofsoftroboticmanipulators,”IEEERobot.Automat.Lett.,
robot end pose, it is challenging to control the whole robot vol.3,no.2,pp.1292–1298,Apr.2018.
shape and avoid contact which may damage the human body. [20] M. C. Yip and D. B. Camarillo, “Model-less hybrid position/force
control:Aminimalistapproachforcontinuummanipulatorsinunknown,
| NN and | RL lack | interpretability |     | and | are challenging |     | to apply |             |     |                |      |        |        |             |           |
| ------ | ------- | ---------------- | --- | --- | --------------- | --- | -------- | ----------- | --- | -------------- | ---- | ------ | ------ | ----------- | --------- |
|        |         |                  |     |     |                 |     |          | constrained |     | environments,” | IEEE | Robot. | Autom. | Lett., vol. | 1, no. 2, |
inrealsurgery.Also,itisimpossibleforRLtoexploreinvivo,
pp.844–851,Jul.2016.
| and RL | agents | can only | be trained | in  | simulation |     | or physical |                                                            |     |     |     |     |     |     |     |
| ------ | ------ | -------- | ---------- | --- | ---------- | --- | ----------- | ---------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|        |        |          |            |     |            |     |             | [21] H.Wang,J.Chen,H.Y.K.Lau,andH.Ren,“Motionplanningbased |     |     |     |     |     |     |     |
onlearningfromdemonstrationformultiple-segmentflexiblesoftrobots
| simulators.  | The  | automatic  | medical | soft   | robot | control            | is still | in       |     |               |            |      |        |        |                |
| ------------ | ---- | ---------- | ------- | ------ | ----- | ------------------ | -------- | -------- | --- | ------------- | ---------- | ---- | ------ | ------ | -------------- |
|              |      |            |         |        |       |                    |          | actuated | by  | electroactive | polymers,” | IEEE | Robot. | Autom. | Lett., vol. 1, |
| its nascence | from | the aspect | of      | safety | and   | data requirements. |          |          |     |               |            |      |        |        |                |
no.1,pp.391–398,Jan.2016.
Cooperation among robotics researchers, doctors, and related [22] C. Cheng, J. Cheng, and W. Huang, “Design and development of
departments is required to address these issues. a novel SMA actuated multi-DOF soft robot,” IEEE Access, vol. 7,
pp.75073–75080,2019.
|     |     |     |     |     |     |     |     | [23] T. G. | Thuruthel,    | E.  | Falotico,    | F. Renda,   | and     | C. Laschi, | “Model- |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------------- | --- | ------------ | ----------- | ------- | ---------- | ------- |
|     |     |     |     |     |     |     |     | based      | reinforcement |     | learning for | closed-loop | dynamic | control    | of soft |
REFERENCES
roboticmanipulators,”IEEETrans.Robot.,vol.35,no.1,pp.124–134,
| [1] M. Cianchetti, |     | T. Ranzani, | G.  | Gerboni, | I. De | Falco, C. | Laschi, and | Feb.2019. |     |     |     |     |     |     |     |
| ------------------ | --- | ----------- | --- | -------- | ----- | --------- | ----------- | --------- | --- | --- | --- | --- | --- | --- | --- |
A. Menciassi, “STIFF-FLOP surgical manipulator: Mechanical design [24] X.T.Haetal.,“Shapesensingofflexiblerobotsbasedondeeplearning,”
IEEETrans.Robot.,vol.39,no.2,pp.1580–1593,Apr.2023.
| and | experimental | characterization |     | of the | single | module,” | in Proc. |     |     |     |     |     |     |     |     |
| --- | ------------ | ---------------- | --- | ------ | ------ | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
IEEE/RSJInt.Conf.Intell.RobotsSyst.,Nov.2013,pp.3576–3581. [25] J. Jung, M. Park, D. Kim, and Y.-L. Park, “Optically sensorized
|     |     |     |     |     |     |     |     | elastomer | air | chamber | for proprioceptive |     | sensing | of soft | pneumatic |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------- | ------------------ | --- | ------- | ------- | --------- |
[2] Y.Ansari,M.Manti,E.Falotico,M.Cianchetti,andC.Laschi,“Multi-
objectiveoptimizationforstiffnessandpositioncontrolinasoftrobot actuators,” IEEE Robot. Autom. Lett., vol. 5, no. 2, pp.2333–2340,
| arm | module,” | IEEE Robot. | Autom. | Lett., | vol. 3, | no. 1, | pp.108–115, | Apr.2020. |     |     |     |     |     |     |     |
| --- | -------- | ----------- | ------ | ------ | ------- | ------ | ----------- | --------- | --- | --- | --- | --- | --- | --- | --- |
Jan.2018. [26] X. T. Ha et al., “Contact localization of continuum and flexible robot
[3] J. F. Queißer, K. Neumann, M. Rolf, R. F. Reinhart, and J. J. Steil, using data-driven approach,” IEEE Robot. Autom. Lett., vol. 7, no. 3,
pp.6910–6917,Jul.2022.
| “An | active compliant | control | mode | for | interaction | with | a pneumatic |     |     |     |     |     |     |     |     |
| --- | ---------------- | ------- | ---- | --- | ----------- | ---- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
softrobot,”inProc.IEEE/RSJInt.Conf.Intell.RobotsSyst.,Sep.2014, [27] Z.Dongetal.,“Shapetrackingandfeedbackcontrolofcardiaccatheter
pp.573–579. using MRI-guided robotic platform—Validation with pulmonary vein
[4] Z.Q.Tang,H.L.Heung,X.Q.Shi,K.Y.Tong,andZ.Li,“Probabilistic isolation simulator in MRI,” IEEE Trans. Robot., vol. 38, no. 5,
model-basedlearningcontrolofasoftpneumaticgloveforhandreha- pp.2781–2798,Oct.2022.
bilitation,” IEEE Trans. Biomed. Eng., vol. 69, no. 2, pp.1016–1028, [28] C.Leeetal.,“Softrobotreview,”Int.J.Control,Autom.Syst.,vol.15,
| Feb.2022. |     |     |     |     |     |     |     | no.1,pp.3–15,Feb.2017. |     |     |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |

CHENetal.:DATA-DRIVENMETHODSAPPLIEDTOSOFTROBOTMODELINGANDCONTROL:AREVIEW 2253
[29] K.Liu,W.Chen,W.Yang,Z.Jiao,andY.Yu,“Reviewoftheresearch [51] M.Gazzola,L.Dudte,A.McCormick,andL.Mahadevan,“Forwardand
progressinsoftrobots,”Appl.Sci.,vol.13,no.1,p.120,Dec.2022. inverse problems in the mechanics of soft filaments,” Roy. Soc. Open
[30] J.M.Bern,Y.Schnider,P.Banzet,N.Kumar,andS.Coros,“Softrobot Sci.,vol.5,no.6,2018,Art.no.171628,doi:10.1098/rsos.171628.
controlwithalearneddifferentiablemodel,”inProc.3rdIEEEInt.Conf. [52] F. Renda, C. Armanini, V. Lebastard, F. Candelier, and F. Boyer, “A
SoftRobot.(RoboSoft),May2020,pp.417–423. geometricvariable-strainapproachforstaticmodelingofsoftmanipula-
[31] K.Iyengar,S.Spurgeon,andD.Stoyanov,“Deepreinforcementlearning torswithtendonandfluidicactuation,”IEEERobot.Autom.Lett.,vol.5,
for concentric tube robot path following,” IEEE Trans. Med. Robot. no.3,pp.4006–4013,Jul.2020.
Bionics,vol.6,no.1,pp.18–29,Feb.2024. [53] A. T. Mathew, I. M. B. Hmida, C. Armanini, F. Boyer, and F. Renda,
[32] D. Wu et al., “Deep-learning-based compliant motion control of a “SoRoSim: A MATLAB toolbox for hybrid rigid–soft robots based
pneumatically-driven robotic catheter,” IEEE Robot. Automat. Lett., onthegeometricvariable-strainapproach,”IEEERobot.Autom.Mag.,
vol.7,no.4,pp.8853–8860,Oct.2022. vol.30,no.3,pp.106–122,Sep.2022.
[33] A. T. Tibebu, B. Yu, Y. Kassahun, E. Vander Poorten, and P. T. Tran, [54] H.Jiangetal.,“Atwo-levelapproachforsolvingtheinversekinematics
“Towards autonomous robotic catheter navigation using reinforcement of an extensible soft arm considering viscoelastic behavior,” in Proc.
learning,” in Proc. 4th Joint Workshop New Technol. Comput./Robot IEEEInt.Conf.Robot.Autom.(ICRA),May2017,pp.6127–6133.
Assist.Surg.,2014,pp.163–166.
[55] I.S.Godage,G.A.Medrano-Cerda,D.T.Branson,E.Guglielmino,and
[34] M. C. Yip and D. B. Camarillo, “Model-less feedback control of D.G.Caldwell,“Dynamicsforvariablelengthmultisectioncontinuum
continuum manipulators in constrained environments,” IEEE Trans. arms,”Int.J.Robot.Res.,vol.35,no.6,pp.695–722,2016.
Robot.,vol.30,no.4,pp.880–889,Aug.2014. [56] E. Milana, F. Stella, B. Gorissen, D. Reynaerts, and C. D. Santina,
[35] A.Melingui,C.Escande,N.Benoudjit,R.Merzouki,andJ.B.Mbede, “Model-based control can improve the performance of artificial cilia,”
“Qualitative approach for forward kinematic modeling of a compact in Proc. IEEE 4th Int. Conf. Soft Robot. (RoboSoft), Apr. 2021,
| bionic | handling | assistant | trunk,” | IFAC | Proc. Volumes, |     | vol. 47, no. | 3,  |     |     |     |     |     |     |     |
| ------ | -------- | --------- | ------- | ---- | -------------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
pp.527–530.
pp.9353–9358,2014.
|     |     |     |     |     |     |     |     | [57] M. H. | Namdar | Ghalati, | H. Ghafarirad, | A.  | A. Suratgar, | M.  | Zareinejad, |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | -------- | -------------- | --- | ------------ | --- | ----------- |
[36] M. T. Gillespie, C. M. Best, E. C. Townsend, D. Wingate, and andM.A.Ahmadi-Pajouh,“Staticmodelingofsoftreinforcedbending
M. D. Killpack, “Learning nonlinear dynamic models of soft robots actuatorconsideringexternalforceconstraints,”SoftRobot.,vol.9,no.4,
formodelpredictivecontrolwithneuralnetworks,”inProc.IEEEInt. pp.776–787,Aug.2022.
Conf.SoftRobot.(RoboSoft),Apr.2018,pp.39–45.
[58] R.Grassmann,V.Modes,andJ.Burgner-Kahrs,“Learningtheforward
| [37] S. Satheeshbabu, |     | N.  | K. Uppalapati, | G.  | Chowdhary, | and | G. Krishnan, |     |                    |     |            |            |      |           |       |
| --------------------- | --- | --- | -------------- | --- | ---------- | --- | ------------ | --- | ------------------ | --- | ---------- | ---------- | ---- | --------- | ----- |
|                       |     |     |                |     |            |     |              | and | inverse kinematics |     | of a 6-DOF | concentric | tube | continuum | robot |
“Openlooppositioncontrolofsoftcontinuumarmusingdeepreinforce-
|     |     |     |     |     |     |     |     | in SE(3),” | in  | Proc. IEEE/RSJ |     | Int. Conf. | Intell. Robots | Syst. | (IROS), |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | -------------- | --- | ---------- | -------------- | ----- | ------- |
ment learning,” in Proc. Int. Conf. Robot. Autom. (ICRA), May 2019, Oct.2018,pp.5125–5132.
pp.5133–5139. [59] C.DellaSantina,R.K.Katzschmann,A.Biechi,andD.Rus,“Dynamic
[38] A. Centurelli, L. Arleo, A. Rizzo, S. Tolu, C. Laschi, and controlofsoftrobotsinteractingwiththeenvironment,”inProc.IEEE
E. Falotico, “Closed-loop dynamic control of a soft manipulator using Int.Conf.SoftRobot.(RoboSoft),Apr.2018,pp.46–53.
| deep | reinforcement | learning,” |     | IEEE Robot. | Autom. | Lett., | vol. 7, no. | 2,         |       |              |     |          |            |          |           |
| ---- | ------------- | ---------- | --- | ----------- | ------ | ------ | ----------- | ---------- | ----- | ------------ | --- | -------- | ---------- | -------- | --------- |
|      |               |            |     |             |        |        |             | [60] Z. Q. | Tang, | H. L. Heung, | K.  | Y. Tong, | and Z. Li, | “A novel | iterative |
pp.4741–4748,Apr.2022.
learningmodelpredictivecontrolmethodforsoftbendingactuators,”in
[39] M. Li, R. Kang, D. T. Branson, and J. S. Dai, “Model-free control Proc.Int.Conf.Robot.Autom.(ICRA),May2019,pp.4004–4010.
forcontinuumrobotsbasedonanadaptiveKalmanfilter,”IEEE/ASME [61] Z. Wang and S. Hirai, “Soft gripper dynamics using a line-segment
Trans.Mechatronics,vol.23,no.1,pp.286–297,Feb.2018. model with an optimization-based parameter identification method,”
| [40] X. Wang | et  | al., “Learning-based |     | visual-strain |     | fusion | for eye-in-hand |     |     |     |     |     |     |     |     |
| ------------ | --- | -------------------- | --- | ------------- | --- | ------ | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
IEEERobot.Autom.Lett.,vol.2,no.2,pp.624–631,Apr.2017.
| continuum | robot | pose | estimation | and | control,” | IEEE | Trans. Robot., |     |     |     |     |     |     |     |     |
| --------- | ----- | ---- | ---------- | --- | --------- | ---- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
[62] X.Wangetal.,“Experimentalvalidationofrobot-assistedcardiovascular
vol.39,no.3,pp.2448–2467,Jun.2023.
catheterization:Model-basedversusmodel-freecontrol,”Int.J.Comput.
| [41] T. George | Thuruthel, |     | Y. Ansari, | E. Falotico, | and | C. Laschi, | “Control |     |     |     |     |     |     |     |     |
| -------------- | ---------- | --- | ---------- | ------------ | --- | ---------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Assist.Radiol.Surg.,vol.13,pp.797–804,2018.
| strategies | for | soft robotic | manipulators: |     | A survey,” | Soft | Robot., vol. | 5,  |     |     |     |     |     |     |     |
| ---------- | --- | ------------ | ------------- | --- | ---------- | ---- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
[63] X.Wangetal.,“Eye-in-handvisualservoingenhancedwithsparsestrain
no.2,pp.149–163,Apr.2018. measurement for soft continuum robots,” IEEE Robot. Autom. Lett.,
| [42] C. D. | Santina, | C. Duriez, | and | D. Rus, | “Model-based |     | control of soft |     |     |     |     |     |     |     |     |
| ---------- | -------- | ---------- | --- | ------- | ------------ | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
vol.5,no.2,pp.2161–2168,Apr.2020.
| robots: | A survey | of  | the state | of the | art and | open challenges,” | IEEE |     |     |     |     |     |     |     |     |
| ------- | -------- | --- | --------- | ------ | ------- | ----------------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
[64] Y.-Y.WuandN.Tan,“Model-lessfeedbackcontrolforsoftmanipulators
ControlSyst.,vol.43,no.3,pp.30–65,Jun.2023.
|                 |     |               |     |          |              |     |              | with | Jacobian | adaptation,” | in  | Proc. Int. | Symp. | Auto. | Syst. (ISAS), |
| --------------- | --- | ------------- | --- | -------- | ------------ | --- | ------------ | ---- | -------- | ------------ | --- | ---------- | ----- | ----- | ------------- |
| [43] C. Laschi, | T.  | G. Thuruthel, |     | F. Lida, | R. Merzouki, | and | E. Falotico, |      |          |              |     |            |       |       |               |
Dec.2020,pp.217–222.
“Learning-basedcontrolstrategiesforsoftrobots:Theory,achievements,
IEEE Control Syst. Mag., [65] M. C. Yip, J. A. Sganga, and D. B. Camarillo, “Autonomous control
and future challenges,” vol. 43, no. 3, ofcontinuumrobotmanipulatorsforcomplexcardiacablationtasks,”J.
pp.100–113,Jun.2023.
Med.Robot.Res.,vol.2,no.1,2017,Art.no.1750002.
| [44] B. Zhang | and | P. Liu, | “Model-based | and | model-free | robot | control: | A   |     |     |     |     |     |     |     |
| ------------- | --- | ------- | ------------ | --- | ---------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
[66] M.Verghese,F.Richter,A.Gunn,P.Weissbrod,andM.Yip,“Model-
| review,” | in  | Proc. 8th | Int. Conf. | Robot | Intell. | Technol. | Appl. (RiTA). |      |                |     |           |       |              |     |             |
| -------- | --- | --------- | ---------- | ----- | ------- | -------- | ------------- | ---- | -------------- | --- | --------- | ----- | ------------ | --- | ----------- |
|          |     |           |            |       |         |          |               | free | visual control | for | continuum | robot | manipulators | via | orientation |
Singapore:Springer,2021,pp.45–55.
|     |     |     |     |     |     |     |     | adaptation,” |     | in Proc. | Int. Symp. | Robot. | Res. | Cham, | Switzerland: |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | -------- | ---------- | ------ | ---- | ----- | ------------ |
[45] C.Schlagenhaufetal.,“Controloftendon-drivensoftfoamrobothands,”
in Proc. IEEE-RAS 18th Int. Conf. Humanoid Robots (Humanoids), Springer,2019,pp.959–970.
Nov.2018,pp.1–7. [67] T.GeorgeThuruthel,E.Falotico,M.Manti,A.Pratesi,M.Cianchetti,
andC.Laschi,“Learningclosedloopkinematiccontrollersforcontin-
| [46] G. Runge, | M.  | Wiese, | and A. | Raatz, “FEM-based |     | training | of artificial |     |              |                 |     |                |     |              |         |
| -------------- | --- | ------ | ------ | ----------------- | --- | -------- | ------------- | --- | ------------ | --------------- | --- | -------------- | --- | ------------ | ------- |
|                |     |        |        |                   |     |          |               | uum | manipulators | in unstructured |     | environments,” |     | Soft Robot., | vol. 4, |
neuralnetworksformodularsoftrobots,”inProc.IEEEInt.Conf.Robot.
no.3,pp.285–296,2017.
Biomimetics(ROBIO),Dec.2017,pp.385–392.
|                |     |                 |     |        |        |               |           | [68] Y. Jin | et al., | “Model-less | feedback | control | for | soft manipulators,” |     |
| -------------- | --- | --------------- | --- | ------ | ------ | ------------- | --------- | ----------- | ------- | ----------- | -------- | ------- | --- | ------------------- | --- |
| [47] M. Wiese, | G.  | Runge-Borchert, |     | and A. | Raatz, | “Optimization | of neural |             |         |             |          |         |     |                     |     |
networkhyperparametersformodelingofsoftpneumaticactuators,”in in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS), Sep. 2017,
pp.2916–2922.
NewTrendsinMedicalandServiceRobotics:AdvancesinTheoryand
|     |     |     |     |     |     |     |     | [69] H. Jiang | et  | al., “Hierarchical |     | control | of soft manipulators |     | towards |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ------------------ | --- | ------- | -------------------- | --- | ------- |
Practice.Cham,Switzerland:Springer,2019,pp.199–206.
|               |     |             |     |             |           |     |                 | unstructured |     | interactions,” | Int. | J. Robot. | Res., | vol. | 40, no. 1, |
| ------------- | --- | ----------- | --- | ----------- | --------- | --- | --------------- | ------------ | --- | -------------- | ---- | --------- | ----- | ---- | ---------- |
| [48] F. Faure | et  | al., “SOFA: | A   | multi-model | framework |     | for interactive |              |     |                |      |           |       |      |            |
pp.411–434,2021.
physicalsimulation,”inSoftTissueBiomechanicalModelingforCom-
puterAssistedSurgery(StudiesinMechanobiology,TissueEngineering [70] G.Fangetal.,“Vision-basedonlinelearningkinematiccontrolforsoft
and Biomaterials), vol. 11, Y. Payan, Ed. Berlin, Germany: Springer, robots using local Gaussian process regression,” IEEE Robot. Autom.
Jun.2012,pp.283–321.[Online].Available:https://inria.hal.science/hal- Lett.,vol.4,no.2,pp.1194–1201,Apr.2019.
00681539 [71] S. Sefati, R. Hegeman, F. Alambeigi, I. Iordachita, and M. Armand,
“FBG-basedpositionestimationofhighlydeformablecontinuummanip-
| [49] F. Largilliere, |     | V. Verona, | E. Coevoet, |     | M. Sanz-Lopez, |     | J. Dequidt, and |     |     |     |     |     |     |     |     |
| -------------------- | --- | ---------- | ----------- | --- | -------------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
C. Duriez, “Real-time control of soft-robots using asynchronous finite ulators: Model-dependent vs. data-driven approaches,” in Proc. Int.
element modeling,” in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), Symp.Med.Robot.(ISMR),Apr.2019,pp.1–6.
May2015,pp.2550–2555. [72] W.Xu,J.Chen,H.Y.K.Lau,andH.Ren,“Automatesurgicaltasksfor
[50] M. Thieffry, A. Kruszewski, C. Duriez, and T.-M. Guerra, “Control aflexibleserpentinemanipulatorvialearningactuationspacetrajectory
|     |     |     |     |     |     |     |     |     |     |     | Proc. | IEEE Int. | Conf. Robot. | Autom. | (ICRA), |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --------- | ------------ | ------ | ------- |
design for soft robots based on reduced-order model,” IEEE Robot. from demonstration,” in
Autom.Lett.,vol.4,no.1,pp.25–32,Jan.2019. May2016,pp.4406–4413.

2254 IEEETRANSACTIONSONAUTOMATIONSCIENCEANDENGINEERING,VOL.22,2025
[73] I.M.Loutfi,A.B.Boutchouang,A.Melingui,O.Lakhal,F.B.Motto, [94] G.Soter,A.Conn,H.Hauser,andJ.Rossiter,“Bodilyawaresoftrobots:
and R. Merzouki, “Learning-based approaches for forward kinematic Integrationofproprioceptiveandexteroceptivesensors,”inProc.IEEE
modeling of continuum manipulators,” IFAC-PapersOnLine, vol. 53, Int.Conf.Robot.Autom.(ICRA),May2018,pp.2448–2453.
no.2,pp.9899–9904,2020.
|     |     |     |     |     |     |     |     | [95] | M. A. | Ahmad, | C. Gruijthuijsen, |     | M.  | Ourak, | J. Deprest, |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | ----- | ------ | ----------------- | --- | --- | ------ | ----------- |
[74] B. Yu, J. d. G. Fernández, and T. Tan, “Probabilistic kinematic model E. Vander Poorten, and T. Vercauteren, “Shared control of an
ofaroboticcatheterfor3Dpositioncontrol,”SoftRobot.,vol.6,no.2, automatically aligning endoscopic instrument based on convolutional
pp.184–194,2019. neural networks,” in Proc. 9th Joint Workshop New Technol.
[75] A. Melingui, J. J. Mvogo Ahanda, O. Lakhal, J. B. Mbede, and Comput./RobotAssist.Surg.,Genoa,Italy,2019,pp.1–2.
R. Merzouki, “Adaptive algorithms for performance improvement of a [96] W.Xu,J.Chen,H.Y.Lau,andH.Ren,“Data-drivenmethodstowards
| class | of continuum |     | manipulators,” | IEEE | Trans. | Syst., | Man, Cybern., |     |          |            |           |                    |     |                  |      |
| ----- | ------------ | --- | -------------- | ---- | ------ | ------ | ------------- | --- | -------- | ---------- | --------- | ------------------ | --- | ---------------- | ---- |
|       |              |     |                |      |        |        |               |     | learning | the highly | nonlinear | inverse kinematics |     | of tendon-driven | sur- |
Syst.,vol.48,no.9,pp.1531–1541,Sep.2018. gicalmanipulators,”Int.J.Med.Robot.Comput.Assist.Surg.,vol.13,
[76] G.Fagogenis,C.Bergeles,andP.E.Dupont,“Adaptivenonparametric no.3,p.e1774,2017.
kinematicmodelingofconcentrictuberobots,”inProc.IEEE/RSJInt. [97] R. F. Reinhart and J. J. Steil, “Hybrid mechanical and data-driven
Conf.Intell.RobotsSyst.(IROS),Oct.2016,pp.4324–4329. modeling improves inverse kinematic control of a soft robot,” Proc.
[77] Z. Tang, P. Wang, W. Xin, and C. Laschi, “Learning-based approach Technol.,vol.26,pp.12–19,Jan.2016.
for a soft assistive robotic arm to achieve simultaneous position and [98] R.Reinhart,Z.Shareef,andJ.Steil,“Hybridanalyticalanddata-driven
forcecontrol,”IEEERobot.Autom.Lett.,vol.7,no.3,pp.8315–8322,
modelingforfeed-forwardrobotcontrol,”Sensors,vol.17,no.2,p.311,
Jul.2022.
Feb.2017.
| [78] J. D. | Ho et | al., “Localized |     | online | learning-based | control | of a soft |      |              |       |         |               |     |          |           |
| ---------- | ----- | --------------- | --- | ------ | -------------- | ------- | --------- | ---- | ------------ | ----- | ------- | ------------- | --- | -------- | --------- |
|            |       |                 |     |        |                |         |           | [99] | D. Braganza, | D. M. | Dawson, | I. D. Walker, | and | N. Nath, | “A neural |
redundant manipulator under variable loading,” Adv. Robot., vol. 32, networkcontrollerforcontinuumrobots,”IEEETrans.Robot.,vol.23,
| no.21,pp.1168–1183,2018. |     |     |     |     |     |     |     |     | no.6,pp.1270–1277,Dec.2007. |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | --- | --- | --- |
[79] M. Malekzadeh, J. Queißer, and J. J. Steil, “Learning the end-effector [100] M.Giorelli,F.Renda,M.Calisti,A.Arienti,G.Ferri,andC.Laschi,
| pose | from demonstration |     | for | the bionic | handling | assistant | robot,” | in  |     |     |     |     |     |     |     |
| ---- | ------------------ | --- | --- | ---------- | -------- | --------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
“NeuralnetworkandJacobianmethodforsolvingtheinversestaticsofa
| Proc. | 9th Int. | Workshop | Hum.-Friendly |     | Robot. | Genoa, | Italy: Springer, |     |     |     |     |     |     |     |     |
| ----- | -------- | -------- | ------------- | --- | ------ | ------ | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
cable-drivensoftarmwithnonconstantcurvature,”IEEETrans.Robot.,
2016,pp.101–107.
vol.31,no.4,pp.823–834,Aug.2015.
| [80] S. Calinon, |     | D. Bruno, | M.  | S. Malekzadeh, |     | T. Nanayakkara, | and |     |     |     |     |     |     |     |     |
| ---------------- | --- | --------- | --- | -------------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[101] T.Baaijetal.,“Learning3Dshapeproprioceptionforcontinuumsoft
| D. G. | Caldwell, | “Human–robot |     | skills | transfer | interfaces | for a flexible |     |     |     |     |     |     |     |     |
| ----- | --------- | ------------ | --- | ------ | -------- | ---------- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Comput. Methods Programs Biomed., robots with multiple magnetic sensors,” Soft Matter, vol. 19, no. 1,
| surgical | robot,” |     |     |     |     |     | vol. 116, no. | 2,  | pp.44–56,2023. |     |     |     |     |     |     |
| -------- | ------- | --- | --- | --- | --- | --- | ------------- | --- | -------------- | --- | --- | --- | --- | --- | --- |
pp.81–96,2014.
|               |     |                 |     |                 |     |              |           | [102] | P. Hyatt | and M. D. | Killpack, | “Real-time | nonlinear | model | predictive |
| ------------- | --- | --------------- | --- | --------------- | --- | ------------ | --------- | ----- | -------- | --------- | --------- | ---------- | --------- | ----- | ---------- |
| [81] A. Ataka | et  | al., “Real-time |     | pose estimation |     | and obstacle | avoidance |       |          |           |           |            |           |       |            |
controlofrobotsusingagraphicsprocessingunit,”IEEERobot.Autom.
| for multi-segment |     | continuum |     | manipulator | in  | dynamic | environments,” |     |     |     |     |     |     |     |     |
| ----------------- | --- | --------- | --- | ----------- | --- | ------- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Lett.,vol.5,no.2,pp.1468–1475,Apr.2020.
| in Proc. | IEEE/RSJ | Int. | Conf. | Intell. | Robots | Syst. (IROS), | Oct. 2016, |     |     |     |     |     |     |     |     |
| -------- | -------- | ---- | ----- | ------- | ------ | ------------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
[103] G.Fang,Y.Tian,Z.-X.Yang,J.M.P.Geraedts,andC.C.L.Wang,
pp.2827–2832.
|     |     |     |     |     |     |     |     |     | “Efficient | jacobian-based | inverse | kinematics | with | Sim-to-Real | transfer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | -------------- | ------- | ---------- | ---- | ----------- | -------- |
[82] C.Jang,J.Ha,P.E.Dupont,andF.C.Park,“Towardon-lineparameter
estimationofconcentrictuberobotsusingamechanics-basedkinematic of soft robots by learning,” IEEE/ASME Trans. Mechatronics, vol. 27,
model,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS), no.6,pp.5296–5306,Dec.2022.
Oct.2016,pp.2400–2405. [104] A. Kuntz, A. Sethi, R. J. Webster, and R. Alterovitz, “Learning the
|            |         |          |       |          |       |           |             |     | complete | shape of concentric |     | tube robots,” | IEEE | Trans. | Med. Robot. |
| ---------- | ------- | -------- | ----- | -------- | ----- | --------- | ----------- | --- | -------- | ------------------- | --- | ------------- | ---- | ------ | ----------- |
| [83] J. Y. | Loo, K. | C. Kong, | C. P. | Tan, and | S. G. | Nurzaman, | “Non-linear |     |          |                     |     |               |      |        |             |
Bionics,vol.2,no.2,pp.140–147,May2020.
| system | identification |     | and state | estimation | in  | a pneumatic | based soft |     |     |     |     |     |     |     |     |
| ------ | -------------- | --- | --------- | ---------- | --- | ----------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
[105] R.GrassmannandJ.Burgner-Kahrs,“Onthemeritsofjointspaceand
continuumrobot,”inProc.IEEEConf.ControlTechnol.Appl.(CCTA),
Aug.2019,pp.39–46. orientationrepresentationsinlearningtheforwardkinematicsinSE(3),”
[84] J. Y. Loo, Z. Y. Ding, E. Davies, S. G. Nurzaman, and C. P. Tan, in Proc. Robot., Sci. Syst. Conf., 2019, pp.1–10. [Online]. Available:
“Curvature and force estimation for a soft finger using an EKF with http://www.roboticsproceedings.org/rss15/p17.pdf
unknown input optimization,” IFAC-PapersOnLine, vol. 53, no. 2, [106] J.Liu,P.Borja,andC.D.Santina,“Physics-informedneuralnetworks
pp.8506–8512,2020. to model and control robots: A theoretical and experimental investiga-
tion,”2023,arXiv:2305.05375.
| [85] D. C. | Rucker  | and R. | J. Webster,   | “Deflection-based |     | force | sensing for   |       |           |                  |     |               |     |                      |     |
| ---------- | ------- | ------ | ------------- | ----------------- | --- | ----- | ------------- | ----- | --------- | ---------------- | --- | ------------- | --- | -------------------- | --- |
|            |         |        |               |                   |     | Proc. | IEEE/RSJ Int. | [107] | F. Pique, | H. T. Kalidindi, |     | L. Fruzzetti, | C.  | Laschi, A.Menciassi, |     |
| continuum  | robots: | A      | probabilistic | approach,”        |     | in    |               |       |           |                  |     |               |     |                      |     |
Conf.Intell.RobotsSyst.,Sep.2011,pp.3764–3769. and E.Falotico, “Controlling soft robotic arms using continual learn-
[86] S.Tully,G.Kantor,M.A.Zenati,andH.Choset,“Shapeestimationfor ing,” IEEE Robot. Autom. Lett., vol. 7, no. 2, pp.5469–5476,
| image-guided |     | surgery | with a | highly articulated |     | snake | robot,” in Proc. |     | Apr.2022. |     |     |     |     |     |     |
| ------------ | --- | ------- | ------ | ------------------ | --- | ----- | ---------------- | --- | --------- | --- | --- | --- | --- | --- | --- |
IEEE/RSJInt.Conf.Intell.Robot.Syst.,Sep.2011,pp.1353–1358. [108] A. Melingui, O. Lakhal, B. Daachi, J. B. Mbede, and R. Mer-
[87] C. Kim, S. C. Ryu, and P. E. Dupont, “Real-time adaptive kinematic zouki, “Adaptive neural network control of a compact bionic handling
arm,”IEEE/ASMETrans.Mechatronics,vol.20,no.6,pp.2862–2875,
| model                                                | estimation | of  | concentric | tube | robots,” | in Proc. | IEEE/RSJ Int. |     |           |     |     |     |     |     |     |
| ---------------------------------------------------- | ---------- | --- | ---------- | ---- | -------- | -------- | ------------- | --- | --------- | --- | --- | --- | --- | --- | --- |
| Conf.Intell.RobotsSyst.(IROS),Sep.2015,pp.3214–3219. |            |     |            |      |          |          |               |     | Dec.2015. |     |     |     |     |     |     |
[88] K.Tan,Q.Ji,L.Feng,andM.Törngren,“Edge-enabledadaptiveshape [109] X.Lietal.,“Deeplearningforhapticfeedbackofflexibleendoscopic
estimation of 3D printed soft actuators with Gaussian processes and robot without prior knowledge on sheath configuration,” Int. J. Mech.
unscented Kalman filters,” IEEE Trans. Ind. Electron., vol. 71, no. 3, Sci.,vol.163,Nov.2019,Art.no.105129.
pp.3044–3054,Mar.2024. [110] S. Yao, R. Tang, L. Bai, H. Yan, H. Ren, and L. Liu, “An
[89] D. Lunni, G. Giordano, E. Sinibaldi, M. Cianchetti, and B. Mazzolai, RNN-LSTM enhanced compact and affordable micro force sensing
|     |     |     |     |     |     |     |     |     | system for | interventional | continuum | robots | with | interchangeable | end- |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | -------------- | --------- | ------ | ---- | --------------- | ---- |
“ShapeestimationbasedonKalmanfiltering:Towardsfullysoftpropri-
oception,”inProc.IEEEInt.Conf.SoftRobot.(RoboSoft),Apr.2018, effector instruments,” IEEE Trans. Instrum. Meas., vol. 72, 2023,
| pp.541–546. |     |     |     |     |     |     |     |     | Art.no.4008711. |     |     |     |     |     |     |
| ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- | --- |
[90] Z. Tang et al., “Meta-learning-based optimal control for soft robotic [111] Z. Y. Ding, J. Y. Loo, V. M. Baskaran, S. G. Nurzaman, and
manipulators to interact with unknown environments,” in Proc. IEEE C. P. Tan, “Predictive uncertainty estimation using deep learning for
softrobotmultimodalsensing,”IEEERobot.Autom.Lett.,vol.6,no.2,
Int.Conf.Robot.Autom.(ICRA),May2023,pp.982–988.
pp.951–957,Apr.2021.
| [91] K. Neumann, |             | M. Rolf, | and J.  | J. Steil, | “Reliable  | integration | of contin-      |       |                  |     |          |         |        |            |             |
| ---------------- | ----------- | -------- | ------- | --------- | ---------- | ----------- | --------------- | ----- | ---------------- | --- | -------- | ------- | ------ | ---------- | ----------- |
|                  |             |          |         |           |            | Int.        | J. Uncertainty, | [112] | T. G. Thuruthel, | B.  | Shih, C. | Laschi, | and M. | T. Tolley, | “Soft robot |
| uous             | constraints | into     | extreme | learning  | machines,” |             |                 |       |                  |     |          |         |        |            |             |
FuzzinessKnowl.-BasedSyst.,vol.21,pp.35–50,Dec.2013. perceptionusingembeddedsoftsensorsandrecurrentneuralnetworks,”
[92] M.Giorelli,F.Renda,G.Ferri,andC.Laschi,“Afeed-forwardneural Sci.Robot.,vol.4,no.26,2019,Art.no.eaav1488.
networklearningtheinversekineticsofasoftcable-drivenmanipulator [113] Z.Zhouetal.,“Asensorysoftroboticgrippercapableoflearning-based
movinginthree-dimensionalspace,”inProc.IEEE/RSJInt.Conf.Intell. object recognition and force-controlled grasping,” IEEE Trans. Autom.
Sci.Eng.,vol.21,no.1,pp.844–854,Jan.2024.
RobotsSyst.,Nov.2013,pp.5033–5039.
[93] T.G.Thuruthel,E.Falotico,F.Renda,andC.Laschi,“Learningdynamic [114] Z.Chen,X.Ren,M.Bernabei,V.Mainardi,G.Ciuti,andC.Stefanini,
models for open loop predictive control of soft robotic manipulators,” “A hybrid adaptive controller for soft robot interchangeability,” IEEE
BioinspirationBiomimetics,vol.12,no.6,2017,Art.no.066003. Robot.Automat.Lett.,vol.9,no.1,pp.875–882,Jan.2024.

CHENetal.:DATA-DRIVENMETHODSAPPLIEDTOSOFTROBOTMODELINGANDCONTROL:AREVIEW 2255
[115] E. Almanzor, F. Ye, J. Shi, T. G. Thuruthel, H. A. Wurdemann, and [136] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “BERT: Pre-
F. Iida, “Static shape control of soft continuum robots using deep trainingofdeepbidirectionaltransformersforlanguageunderstanding,”
visual inverse kinematic models,” IEEE Trans. Robot., vol. 39, no. 4, 2018,arXiv:1810.04805.
pp.2973–2988,Aug.2023. [137] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, “You only look
[116] N.Liang,R.M.Grassmann,S.Lilge,andJ.Burgner-Kahrs,“Learning- once:Unified,real-timeobjectdetection,”inProc.IEEEConf.Comput.
based inverse kinematics from shape as input for concentric tube Vis.PatternRecognit.(CVPR),Jun.2016,pp.779–788.
continuum robots,” in Proc. IEEE Int. Conf. Robot. Automat. (ICRA), [138] M. S. Nazeer, D. Bianchi, G. Campinoti, C. Laschi, and E. Falotico,
“Policyadaptationusinganonlineregressingnetworkinasoftrobotic
May/Jun.2021,pp.1387–1393.
|          |         |       |                |     |          |        |       |         | arm,” in Proc. | IEEE Int. Conf. | Soft | Robot. | (RoboSoft), | Apr. 2023, |
| -------- | ------- | ----- | -------------- | --- | -------- | ------ | ----- | ------- | -------------- | --------------- | ---- | ------ | ----------- | ---------- |
| [117] U. | Yoo, H. | Zhao, | A. Altamirano, |     | W. Yuan, | and C. | Feng, | “Toward |                |                 |      |        |             |            |
pp.1–7.
| zero-shot | sim-to-real |     | transfer | learning | for | pneumatic | soft | robot 3D |     |     |     |     |     |     |
| --------- | ----------- | --- | -------- | -------- | --- | --------- | ---- | -------- | --- | --- | --- | --- | --- | --- |
proprioceptivesensing,”inProc.IEEEInt.Conf.Robot.Autom.(ICRA),
May2023,pp.544–551.
|            |           |         |          |                |      |            |               |       |     | Zixi Chen | (Graduate  | Student  | Member,      | IEEE)        |
| ---------- | --------- | ------- | -------- | -------------- | ---- | ---------- | ------------- | ----- | --- | --------- | ---------- | -------- | ------------ | ------------ |
| [118] Y.   | Zhang,    | J. Gao, | H. Yang, | and L.         | Hao, | “A novel   | hysteresis    | mod-  |     |           |            |          |              |              |
|            |           |         |          |                |      |            |               |       |     | received  | the M.Sc.  | degree   | in control   | systems from |
| elling     | method    | with    | improved | generalization |      | capability | for pneumatic |       |     |           |            |          |              |              |
|            |           |         |          |                |      |            |               |       |     | Imperial  | College in | 2021. He | is currently | pursuing     |
| artificial | muscles,” | Smart   | Mater.   | Struct.,       | vol. | 28, no.    | 10, Oct.      | 2019, |     |           |            |          |              |              |
thePh.D.degreeinbioroboticsfromScuolaSuperi-
Art.no.105014.
oreSant’AnnaofPisa.Hisresearchinterestincludes
[119] Y.Chenetal.,“Safety-enhancedmotionplanningforflexiblesurgical optical tactile sensors and soft robot control with
manipulatorusingneuraldynamics,”IEEETrans.ControlSyst.Technol., neuralnetworks.
vol.25,no.5,pp.1711–1723,Sep.2017.
[120] Z.Chen,M.Bernabei,V.Mainardi,X.Ren,G.Ciuti,andC.Stefanini,
“AnovelandaccurateBiLSTMconfigurationcontrollerformodularsoft
robotswithmodulenumberadaptability,”2024,arXiv:2401.10997.
| [121] S. | Sapai, J. | Y. Loo, | Z. Y. | Ding, | C. P. Tan, | V. M. | Baskaran, | and |     |     |     |     |     |     |
| -------- | --------- | ------- | ----- | ----- | ---------- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- |
S. G. Nurzaman, “A deep learning framework for soft robots with FedericoRenda(Member,IEEE)receivedtheB.Sc.
|     |     |     |     |     |     |     |     |     |     | and M.Sc. | degrees | in biomedical | engineering | from |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | ------- | ------------- | ----------- | ---- |
syntheticdata,”SoftRobot.,vol.10,no.6,pp.1224–1240,Dec.2023.
theUniversityofPisa,Pisa,Italy,in2007and2009,
[122] A.Melingui,R.Merzouki,J.B.Mbede,C.Escande,andN.Benoudjit,
|         |          |       |          |     |         |           |          |      |     | respectively, | and the | Ph.D. | degree | in biorobotics |
| ------- | -------- | ----- | -------- | --- | ------- | --------- | -------- | ---- | --- | ------------- | ------- | ----- | ------ | -------------- |
| “Neural | networks | based | approach | for | inverse | kinematic | modeling | of a |     |               |         |       |        |                |
compactbionichandlingassistanttrunk,”inProc.IEEE23rdInt.Symp. from The BioRobotics Institute, Scuola Superiore
Ind.Electron.(ISIE),Jun.2014,pp.1239–1244. Sant’Anna,Pisa,in2014.
|          |           |               |        |               |          |            |            |     |     | He is currently | an            | Associate | Professor    | with the      |
| -------- | --------- | ------------- | ------ | ------------- | -------- | ---------- | ---------- | --- | --- | --------------- | ------------- | --------- | ------------ | ------------- |
| [123] Y. | Engel, P. | Szabo,        | and D. | Volkinshtein, |          | “Learning  | to control | an  |     |                 |               |           |              |               |
|          |           |               |        |               |          |            |            |     |     | Department      | of Mechanical |           | Engineering, | Khalifa       |
| octopus  | arm       | with Gaussian |        | process       | temporal | difference | methods,”  | in  |     |                 |               |           |              |               |
|          |           |               |        |               |          |            |            |     |     | University,     | Abu Dhabi,    | United    | Arab         | Emirates. His |
Proc.Adv.NeuralInf.Process.Syst.,vol.18,2005,pp.1–8.
|          |           |        |     |           |          |           |     |           |     | research | interests include |     | dynamic | modeling and |
| -------- | --------- | ------ | --- | --------- | -------- | --------- | --- | --------- | --- | -------- | ----------------- | --- | ------- | ------------ |
| [124] Y. | Kassahun, | B. Yu, | and | E. Vander | Poorten, | “Learning |     | catheter- |     |          |                   |     |         |              |
controlofsoftandcontinuumrobotsusingprinciples
aorta interaction model using joint probability densities,” in Proc. ofgeometricmechanics.
| 3rd | Joint Workshop |     | New Technol. | Comput./Robot |     | Assist. | Surg., | 2013, |     |     |     |     |     |     |
| --- | -------------- | --- | ------------ | ------------- | --- | ------- | ------ | ----- | --- | --- | --- | --- | --- | --- |
pp.158–160.
|                |     |       |         |         |         |          |              |     |     | Alexia Le | Gall (Student | Member, |     | IEEE) received |
| -------------- | --- | ----- | ------- | ------- | ------- | -------- | ------------ | --- | --- | --------- | ------------- | ------- | --- | -------------- |
| [125] J. Chen, | H.  | Y. K. | Lau, W. | Xu, and | H. Ren, | “Towards | transferring |     |     |           |               |         |     |                |
skills to flexible surgical robots with programming by demonstration the Engineering degree in mechanical conception
andreinforcementlearning,”inProc.8thInt.Conf.Adv.Comput.Intell. and the M.Sc. degree in mechatronics from the
(ICACI),Feb.2016,pp.378–384. University of Technology of Compiègne, France,
[126] X. Dong, J. Zhang, L. Cheng, W. Xu, H. Su, and T. Mei, “A policy in2022.SheiscurrentlypursuingthePh.D.degree
|          |           |             |     |      |                |     |         |          |     | in biorobotics | from | Scuola | Superiore | Sant’Anna, |
| -------- | --------- | ----------- | --- | ---- | -------------- | --- | ------- | -------- | --- | -------------- | ---- | ------ | --------- | ---------- |
| gradient | algorithm | integrating |     | long | and short-term |     | rewards | for soft |     |                |      |        |           |            |
withaspecializationinsoftrobotic.
| continuum | arm | control,” | Sci. | China | Technol. | Sci., | vol. 65, | no. 10, |     |     |     |     |     |     |
| --------- | --- | --------- | ---- | ----- | -------- | ----- | -------- | ------- | --- | --- | --- | --- | --- | --- |
pp.2409–2419,Oct.2022. Her research interests include mechanical design
andsoftroboticactuationandfabricationmethods.
| [127] G. | Ji et al., | “Towards | safe | control | of continuum | manipulator |     | using |     |     |     |     |     |     |
| -------- | ---------- | -------- | ---- | ------- | ------------ | ----------- | --- | ----- | --- | --- | --- | --- | --- | --- |
shieldedmultiagentreinforcementlearning,”IEEERobot.Autom.Lett.,
vol.6,no.4,pp.7461–7468,Oct.2021.
| [128] X. | Liu, R. | Gasoto, | Z. Jiang, | C.  | Onal, | and J. Fu, | “Learning | to  |     |         |          |          |           |           |
| -------- | ------- | ------- | --------- | --- | ----- | ---------- | --------- | --- | --- | ------- | -------- | -------- | --------- | --------- |
|          |         |         |           |     |       |            |           |     |     | Lorenzo | Mocellin | received | the B.Sc. | degree in |
locomotewithartificialneural-networkandCPG-basedcontrolinasoft
biomedicalengineeringfromtheUniversityofPadua
snakerobot,”inProc.IEEE/RSJInt.Conf.Intell.RobotsSyst.(IROS), in 2019 and the M.Sc. degree in bioengineering
Oct.2020,pp.7758–7765. from the University of Trieste in 2022, with a
[129] X. Liu, C. Onal, and J. Fu, “Learning contact-aware CPG-based thesis on cardiovascular fluid mechanics modeling.
locomotioninasoftsnakerobot,”2021,arXiv:2105.04608. HeiscurrentlypursuingthePh.D.degreewithThe
BioRoboticsInstitute,ScuolaSuperioreSant’Anna.
[130] Y.Luetal.,“Autonomousintelligentnavigationforflexibleendoscopy
usingmonoculardepthguidanceand3-Dshapeplanning,”inProc.IEEE He works with the Surgical Robotics Labora-
Int.Conf.Robot.Autom.(ICRA),May2023,pp.1–7. tory on the design and development of surgical
[131] Y. Gan et al., “A reinforcement learning method for motion control robotictools.Hisresearchinterestsincludeminiatur-
with constraints on an HPN arm,” IEEE Robot. Autom. Lett., vol. 7, izedmedicaldevices,surgicalroboticend-effectors,
origami-inspiredstructures,compliantmechanisms,andbiomaterials.
no.4,pp.12006–12013,Oct.2022.
| [132] O. | Mumini | Omisore, | T. Akinyemi, |     | W. Duan, | W. Du, | and | L. Wang, |     |     |     |     |     |     |
| -------- | ------ | -------- | ------------ | --- | -------- | ------ | --- | -------- | --- | --- | --- | --- | --- | --- |
“A novel sample-efficient deep reinforcement learning with episodic Matteo Bernabei
|     |     |     |     |     |     |     |     |     |     |     |     | received | the bachelor’s | degree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | -------------- | ------ |
policytransferforPID-basedcontrolincardiaccatheterizationrobots,” in industrial engineering and the master’s degree
2021,arXiv:2110.14941.
|          |         |           |             |       |                     |          |            |     |     | in biomedical       | engineering |          | from the  | Campus Bio-  |
| -------- | ------- | --------- | ----------- | ----- | ------------------- | -------- | ---------- | --- | --- | ------------------- | ----------- | -------- | --------- | ------------ |
| [133] Y. | Li, X.  | Wang, and | K.-W.       | Kwok, | “Towards            | adaptive | continuous |     |     |                     |             |          |           |              |
|          |         |           |             |       |                     |          |            |     |     | Medico University   |             | of Rome, | Italy,    | in 2020 and  |
| control  | of soft | robotic   | manipulator |       | using reinforcement |          | learning,” | in  |     |                     |             |          |           |              |
|          |         |           |             |       |                     |          |            |     |     | 2022, respectively. |             | He is    | currently | pursuing the |
Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS), Oct. 2022, Ph.D. degree in biorobotics with Scuola Superi-
pp.7074–7081. ore Sant’Anna (SSSA), Italy. In 2021, as part of
[134] Q.Wuetal.,“Positioncontrolofcable-drivenroboticsoftarmbased his formation, he spent six months as a Research
on deep reinforcement learning,” Information, vol. 11, no. 6, p.310, Intern with Boston Children’s Hospital to work on
2020.
|     |     |     |     |     |     |     |     |     |     | advanced | methods for | analysis | of EEG | signals for |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | -------- | ------ | ----------- |
[135] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based theoptimizationofpre-surgeryplanninginchildren
learningappliedtodocumentrecognition,”Proc.IEEE,vol.86,no.11, withdrug-resistantepilepsy.Hiscurrentresearchinterestsincludeendoluminal
| pp.2278–2324,Nov.1998. |     |     |     |     |     |     |     |     | andminimallyinvasivesurgicalrobotics. |     |     |     |     |     |
| ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- |

2256 IEEETRANSACTIONSONAUTOMATIONSCIENCEANDENGINEERING,VOL.22,2025
Théo Dangel received the M.Eng. degree in Matteo Cianchetti (Member, IEEE) received the
mechanical engineering from SUPMICROTECH- M.Sc. degree (cum laude) in biomedical engineer-
ENSMM, Besançon, France, and the M.S. degree ing from the University of Pisa, Italy, in 2007,
inelectronicsfromTokyoDenkiUniversity,Tokyo, and the Ph.D. degree in biorobotics from Scuola
Japan, in 2022. He is currently pursuing the Superiore Sant’Anna. He is currently an Assistant
Ph.D. degree in biorobotics with Scuola Superiore Professor with The BioRobotics Institute, Scuola
Sant’Anna,Pisa,Italy.Hisresearchinterestsinclude SuperioreSant’Anna,leadingtheSoftMechatronics
actuatorsforsoftrobotic. forBioroboticsLaboratory.Heistheauthororcoau-
thor of more than 100 international peer-reviewed
articles.HehasbeeninvolvedinEU-fundedprojects
with a main focus on the development of soft
roboticstechnologies.Hismainresearchinterestsincludebioinspiredrobotics
and the study and development of new systems and technologies based on
soft/flexiblematerialsforsoftactuators,smartcompliantsensors,andflexible
mechanisms.HeistheChairoftheIEEETConSoftRobotics.Heregularly
servesasareviewerformorethanteninternationaljournals.
Gastone Ciuti (Senior Member, IEEE) received
the master’s degree (Hons.) in biomedical engi- Cesare Stefanini (Member, IEEE) received the
neering from the University of Pisa, Pisa, Italy, M.Sc.degree(Hons.)inmechanicalengineeringand
in2008,andthePh.D.degree(Hons.)inbiorobotics thePh.D.degree(Hons.)inmicroengineeringfrom
from The BioRobotics Institute, Scuola Superiore Scuola Superiore Sant’Anna (SSSA), Pisa, Italy, in
Sant’Anna, Pisa, in 2011. He has been a Visiting 1997and2002,respectively.
Professor with Sorbonne University, Paris, France, HehasbeenaVisitingResearcherwiththeCenter
andBeijingInstituteofTechnology,Beijing,China; for Design Research, Stanford University, and the
and a Visiting Student with Vanderbilt University, Director of the Healthcare Engineering Innovation
Nashville, TN, USA, and the Imperial College Center,KhalifaUniversity,AbuDhabi,UnitedArab
London, London, U.K. He is currently an Asso- Emirates.HeiscurrentlyaProfessorandtheDirec-
ciateProfessorofBioengineeringwithScuolaSuperioreSant’Anna,leading torofTheBioRoboticsInstitute,SSSA,whereheis
the Healthcare Mechatronics Laboratory. He is the coauthor of more than also the Head of the Creative Engineering Laboratory. He is the author or
110internationalpeer-reviewedarticlesonmedicalroboticsandtheinventor coauthor of more than 200 articles in refereed international journals and on
of more than 15 patents. His research interests include robot/computer- international conference proceedings. He is the inventor of 15 international
assisted platforms, such as teleoperated and autonomous magnetic-based patents,nineofwhichareindustriallyexploitedbyinternationalcompanies.
robotic platforms for navigation, localization, and tracking of smart and His research activity is applied to different fields, including underwater
innovative devices in guided and targeted minimally invasive surgical and robotics, bioinspired systems, biomechatronics, and micromechatronics for
diagnosticapplications,e.g.,advancedcapsuleendoscopy.Heisamemberof medicalandindustrialapplications.
theTechnicalCommitteeinbioroboticsoftheIEEEEngineeringinMedicine Prof. Stefanini is a member of the Academy of Scientists of United
and Biology Society (EMBS). He is an Associate Editor of IEEE JOUR- ArabEmiratesandtheIEEESocietiesRoboticsandAutomation(RAS)and
NALOFBIOMEDICALANDHEALTHINFORMATICS, IEEETRANSACTIONS Engineering in Medicine and Biology (EMBS). He was a recipient of the
ONBIOMEDICALENGINEERING, and IEEETRANSACTIONSONMEDICAL “Intuitive Surgical Research Award.” He received international recognition
ROBOTICSANDBIONICS. forthedevelopmentofnovelactuatorsformicrorobots.
Open Access funding provided by ‘Scuola Superiore ''S.Anna'' di Studi Universitari e di Perfezionamento’
within the CRUI CARE Agreement