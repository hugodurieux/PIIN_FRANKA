1
Rod models in continuum and soft robot control: a
review
Carlo Alessi1,†,∗, Camilla Agabiti2,3,∗, Daniele Caradonna2,3,∗, Cecilia Laschi4, Federico Renda5,
Egidio Falotico2,3,†
Abstract—Continuum and soft robots can transform automa-
tion tasks requiring compliant interaction in constrained or
unstructured environments, including healthcare, agriculture,
marine, and space applications. However, their complex me-
chanicsintroducesignificantchallengesinmodelingandcontrol. Learning-based Discrete material Geometric Mechanical
Low-dimensional continuum mechanical models, such as rod Artificial Neural Network Pseudo-rigid Piecewise constant curvature FEM Rod
(3D) (1D)
theories, effectively capture the large deformations of slender
bodies in contact-rich scenarios while balancing accuracy and Link
computational efficiency. This paper presents a vertical survey Joint
of rod models for continuum and soft robots, spanning their
mathematical foundations, robot modeling, and control applica-
tions. We review the main rod theories adopted in soft robotics Data-driven Analytical and Numerical
and introduce a deformation-based classification of rod models
for continuum and soft robots. Furthermore, we survey recent Fig. 1. Overview of modeling techniques for continuum and soft robots
model-basedandlearning-basedcontrolstrategiesleveragingrod (Sec. III). This review focuses on rod models, from their mathematical
models, highlighting their role in manipulation and physical formulationtocontrolapplications.
interaction tasks. Finally, we discuss advantages, limitations,
researchgaps,andemergingdirectionsofrod-basedapproaches.
This paper aims to serve as a reference for developing models and can assume various morphologies. In this paper, we refer
and control strategies for continuum and soft robots. to both classes, considering their partial overlap.
Note to Practitioners—This paper is motivated by the chal- Continuum and soft robots can deform due to the inherent
lenge of modeling and controlling continuum and soft robots compliance of soft materials [3], making them promising
for compliant interaction in complex environments. To balance for automation tasks requiring safe, dexterous interaction in
physicalaccuracyandcomputationalefficiency,thepaperfocuses
constrainedorunstructuredenvironments.Advancesindesign
onrodtheories,whicheffectivelydescribethelargedeformations
and manufacturing technologies are accelerating the develop-
of slender structures. We review the literature on rod theories
in soft robotics, covering mathematical foundations, continuum ment of highly dexterous robotic systems [4], [5]. Despite
and soft robot models, and control strategies based on model- this progress, modeling and controlling soft robots remain
basedanddeeplearningapproaches.Finally,thepaperdiscusses challenging. Indeed, soft materials may introduce extreme
themainadvantages,limitations,andopenchallengesofcurrent
hyper-redundancyandcomplexnonlinearbehaviors,including
rod-based methods, outlining future directions for automation
hysteresis and stress softening. One of the earliest contin-
and contact-rich manipulation tasks. The presented perspectives
can support the development of more reliable and deployable uum formulations for hyper-redundant robots represented a
continuum and soft robotic systems. manipulator as a smooth backbone curve with distributed
Index Terms—Modeling, Control, and Learning for Soft parameters and derived partial differential equations (PDEs)
Robots for its dynamics [6], [7]. Since then, many researchers have
developed diverse modeling techniques characterized by dif-
ferent assumptions, mathematical frameworks, and trade-offs
I. INTRODUCTION
between accuracy and computational cost [8], [9]. As sum-
Continuum robots are robots with distributed deformations marized in Figure 1, soft robotics encompasses four model
alongtheirstructure,resultinginaninfinitenumberofdegrees classes:data-driven,discrete,geometrical,andcontinuumme-
of freedom (DoFs). This property creates a hyper-redundant chanical. Concurrently, innovative control strategies emerged
configuration space, allowing the robot tip to reach any point toleveragethesemodels[10]–[12].Inthispaper,wefocuson
inthethree-dimensional(3D)workspacewithvirtuallyinfinite the achievements of rod theories from modeling to control.
configurations [1]. Soft robots, built with soft materials or Rod theories are a fundamental framework for modeling,
deformable structures [2], are a subset of continuum robots simulation,andcontrolincontinuumandsoftrobotics.Despite
their extensive use, the literature still lacks a comprehensive
†Correspondingauthor.∗Authorscontributedequally.1IstitutoItalianodi andstructuredreviewconsolidatingtheirkeycontributions.To
Tecnologia,16163Genoa,Italy.2TheBioRoboticsInstitute,ScuolaSuperiore addressthisgap,thispaperinvestigatestheroleofrodtheories
Sant’Anna,Pisa,Italy.3DepartmentofExcellenceinRoboticsandAI,Scuola
in continuum and soft robots from a vertical perspective.
SuperioreSant’Anna,Pisa,Italy.4AdvancedRoboticsCentreandDepartment
of Mechanical Engineering, National University of Singapore, Singapore, We guide the reader from the mathematical formulation of
Singapore. 5 Khalifa University Center for Autonomous Robotics System rod theories, through their application to continuum and soft
and the Department of Mechanical & Nuclear Engineering, Khalifa Univer-
robot modeling, to recent developments in model-based and
sity of Science & Technology, Abu Dhabi 127788, United Arab Emirates.
carlo.alessi@iit.itegidio.falotico@santannapisa.it learning-based control. We structure the modeling literature
6202
nuJ
9
]OR.sc[
3v68850.7042:viXra

2
around deformation modes, providing both a synthesis of work for modeling biomedical continuum robots, compar-
the state of the art and a practical reference for researchers ing Cosserat rod and general continuum formulations while
developing new continuum and soft robotic systems. discussing trade-offs between model accuracy and computa-
First,wereportrelatedsurveysonsoftroboticsthatprovide tional cost. With a similar emphasis on clinical applications,
valuable complementary perspectives, where rod models are [14] reviews the modeling and control of several continuum
treatedmarginally(Sec.II).Second,wecharacterizethemajor robot architectures, including tendon-driven, multibackbone,
modelingtechniquestoidentifytheirstrengthsandlimitations concentric tube, magnetic, and soft designs. For a broader
|              |     |            |       |       |       |          |         | perspective | on  | medical | continuum | robotics, | we  | also refer the |
| ------------ | --- | ---------- | ----- | ----- | ----- | -------- | ------- | ----------- | --- | ------- | --------- | --------- | --- | -------------- |
| with respect | to  | rod models | (Sec. | III). | Then, | the main | contri- |             |     |         |           |           |     |                |
butions of this paper are as follows: reader to the survey by Burgner-Kahrs et al. [15].
|       |             |                |        |             |            |     |          | Several   | surveys | instead   | adopt | a broader        | soft      | robotics per- |
| ----- | ----------- | -------------- | ------ | ----------- | ---------- | --- | -------- | --------- | ------- | --------- | ----- | ---------------- | --------- | ------------- |
| • A   | comparative |                | review | of          | four major |     | rod the- |           |         |           |       |                  |           |               |
|       |             |                |        |             |            |     |          | spective. | The     | review by | [16]  | spans the entire | pipeline, | high-         |
| ories | and         | discretization |        | techniques. |            | We  | present  |           |         |           |       |                  |           |               |
the Cosserat-Reissner, Kirchhoff-Love, Timoshenko, and lighting key technical challenges from design and actuation
Euler-Bernoulli to modeling and control. Likewise, the perspective article by
|      |            | rod   | models      | with | a consistent | mathemat- |           |                |     |          |              |     |             |         |
| ---- | ---------- | ----- | ----------- | ---- | ------------ | --------- | --------- | -------------- | --- | -------- | ------------ | --- | ----------- | ------- |
|      |            |       |             |      |              |           |           | [17] discusses |     | embodied | intelligence | in  | soft robots | through |
| ical | framework, | which | facilitates |      | comparison   |           | and high- |                |     |          |              |     |             |         |
light connections to alternative approaches (Sec. IV). We a unified modeling formulation and analyzes its theoretical
consider the modeling of actuation-induced distributed implications. In contrast, we bridge mathematical foundations
|       |               |     |          |          |       |     |     | and control-oriented |     | applications |     | specifically | for | rod theories. |
| ----- | ------------- | --- | -------- | -------- | ----- | --- | --- | -------------------- | --- | ------------ | --- | ------------ | --- | ------------- |
| loads | for different |     | actuator | routings | (Sec. | V). |     |                      |     |              |     |              |     |               |
• A structured review of rod-based models for con- Other surveys concentrate on specific computational
tinuum and soft robots. We organize rod models into paradigms. The review by [18] emphasizes real-time finite
|     |     |     |     |     |     |     |     | element | method | (FEM)-based |     | approaches | for soft | robot mod- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------ | ----------- | --- | ---------- | -------- | ---------- |
ninedeformationclasses,providinganovelreferencefor
the further development of soft robot models (Sec. VI). eling and control, while [19] focuses on model order reduc-
Deformation modes, such as bending and stretching, tion (MOR) techniques and reduced order models (ROMs),
|      |             |           |              |      |              |              |     | discussing      | constitutive |          | laws,   | solution strategies, |       | and reduced |
| ---- | ----------- | --------- | ------------ | ---- | ------------ | ------------ | --- | --------------- | ------------ | -------- | ------- | -------------------- | ----- | ----------- |
| are  | fundamental | behaviors |              | that | collectively | define       | how |                 |              |          |         |                      |       |             |
|      |             |           |              |      |              |              |     | representations |              | for soft | robotic | systems.             | While | these works |
| soft | robots      | move      | and interact |      | with their   | environment. |     |                 |              |          |         |                      |       |             |
Classifying the literature by these modes highlights the primarily address theoretical and computational aspects, we
|            |          |         |              |             |               |     |         | additionally | discuss | experimental |          | validation  | and | practical im-   |
| ---------- | -------- | ------- | ------------ | ----------- | ------------- | --- | ------- | ------------ | ------- | ------------ | -------- | ----------- | --- | --------------- |
| mechanical |          | effects | of actuation |             | and clarifies | the | associ- |              |         |              |          |             |     |                 |
|            |          |         |              |             |               |     |         | plications   | of rod  | models.      | Finally, | [8] broadly |     | classifies soft |
| ated       | modeling | and     | control      | approaches. |               |     |         |              |         |              |          |             |     |                 |
A comprehensive review of model-based control for robot models into continuum mechanics, geometrical, discrete
•
continuum soft manipulators (CSMs) using rod mod- material, and surrogate approaches, analyzing their theoretical
|      |          |         |     |            |      |              |     | foundations | and | applicability. |     | However, | control | aspects are |
| ---- | -------- | ------- | --- | ---------- | ---- | ------------ | --- | ----------- | --- | -------------- | --- | -------- | ------- | ----------- |
| els. | We cover | a range | of  | approaches | from | foundational |     |             |     |                |     |          |         |             |
methods, such as inverse kinematics, inverse dynamics, addressed only marginally. In contrast, we investigate rod
and feedback linearization, to advanced techniques like models in greater depth as a specific subset of continuum
|       |            |         |     |         |         |       |       | mechanics | approaches, |     | emphasizing | the | role of | deformation |
| ----- | ---------- | ------- | --- | ------- | ------- | ----- | ----- | --------- | ----------- | --- | ----------- | --- | ------- | ----------- |
| model | predictive | control | and | optimal | control | (Sec. | VII). |           |             |     |             |     |         |             |
• A review of learning-based controllers leveraging rod modes in both modeling and control.
models. We emphasize Reinforcement Learning (RL) as Control-oriented surveys: Regarding control, [10] provide
|             |     |             |     |         |              |     |         | a broad | overview | of  | model-based | and | model-free | control |
| ----------- | --- | ----------- | --- | ------- | ------------ | --- | ------- | ------- | -------- | --- | ----------- | --- | ---------- | ------- |
| a promising |     | key enabler | to  | achieve | contact-rich |     | manipu- |         |          |     |             |     |            |         |
lation tasks with CSMs (Sec. VIII). strategies for CSMs, however, without concern for the model-
ing.Buildingonthis,[20]providesasystematicreviewofMa-
| Throughout | the | paper, | we provide |     | insights | and critiques | on  |     |     |     |     |     |     |     |
| ---------- | --- | ------ | ---------- | --- | -------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
chineLearning(ML)forcontinuumrobotcontrol,highlighting
| the reviewed | methods, |       | consolidating |     | the discussion |       | on major |            |               |     |             |            |       |               |
| ------------ | -------- | ----- | ------------- | --- | -------------- | ----- | -------- | ---------- | ------------- | --- | ----------- | ---------- | ----- | ------------- |
|              |          |       |               |     |                |       |          | model-free | approaches    |     | for inverse | kinematics | and   | closed-loop   |
| trends,      | research | gaps, | and emerging  |     | challenges     | (Sec. | IX).     |            |               |     |             |            |       |               |
|              |          |       |               |     |                |       |          | control,   | and outlining |     | trends      | to handle  | model | uncertainties |
Althoughthisreviewfocusesonrodtheoriesformodelingand
|             |               |               |     |            |          |        |          | with data-driven |     | methods.  | Similarly, | [21]       | reviews | actuation    |
| ----------- | ------------- | ------------- | --- | ---------- | -------- | ------ | -------- | ---------------- | --- | --------- | ---------- | ---------- | ------- | ------------ |
| control,    | the presented | perspectives  |     | contribute |          | to the | broader  |                  |     |           |            |            |         |              |
|             |               |               |     |            |          |        |          | mechanisms       | and | controls, | including  | open-loop, |         | closed-loop, |
| advancement | of            | soft robotics |     | research.  | Finally, | we     | conclude |                  |     |           |            |            |         |              |
with a summary of the main lessons learned (Sec. X). andautonomousmethods.Theydiscussemergentdirectionsin
thecontrol-actuatorinterface,underactuation,andtheadoption
|     |     |     |             |     |     |     |     | of artificial | intelligence. |     | Subsequently, | [11] | describe | the prob- |
| --- | --- | --- | ----------- | --- | --- | --- | --- | ------------- | ------------- | --- | ------------- | ---- | -------- | --------- |
|     |     | II. | RELATEDWORK |     |     |     |     |               |               |     |               |      |          |           |
lemofmodel-basedcontrolofCSMsthroughamodel-agnostic
Soft robotics has been the subject of extensive surveys, formulation of soft robot dynamics. Then, they discuss shape
reviews, and perspectives, which represent a wealth of knowl- controlandtrackingproblems,exploringopenchallengessuch
| edge and | a growing | interest | in  | a thriving | research | field. |     |                    |     |               |     |              |          |        |
| -------- | --------- | -------- | --- | ---------- | -------- | ------ | --- | ------------------ | --- | ------------- | --- | ------------ | -------- | ------ |
|          |           |          |     |            |          |        |     | as underactuation, |     | environmental |     | interaction, | actuator | dynam- |
Modeling-oriented surveys: Early surveys on continuum ics,andtask-spacecontrol.Finally,[12]explorehowdifferent
robot modeling mainly focused on kinematic representations. models influence the design and performance of learning-
The seminal work of [13] reviews kinematic models of based controllers. In contrast, we investigate model-based and
piecewise constant curvature (PCC) for continuum robots, learning-based controllers with a focus on rod models.
presenting robot-specific and robot-independent mappings. In Insummary,thisreviewcomplementsexistingsurveyswith
contrast, our work provides a comprehensive treatment of rod limited overlap by providing a focused and control-oriented
models,whichextendPCCformulationstoscenariosinvolving treatmentofrodtheoriesforcontinuumandsoftrobots.While
significant interaction forces, such as manipulation tasks. most prior works present broad overviews of modeling or
Subsequent works progressively incorporated mechanics- control approaches, we connect the mathematical foundations
basedformulations.Forinstance,[9]presentsaunifiedframe- of rod theories to their implications for robot modeling and

3
| control. | In  | particular, | we  | structure | the | literature | around | defor- |     |     |     |     |     |     |     |
| -------- | --- | ----------- | --- | --------- | --- | ---------- | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
TABLEI
FEATURESOFSOFTROBOTICSMODELS(SEC.III).RODMODELS
mationmodes,offeringanovelperspectivethatbridgestheory,
COMBINEPHYSICALMODELINGCAPABILITIESWITHTRACTABLE
| practical | modeling, |     | and | recent | control | strategies, | including |     |     |     |     |     |     |     |     |
| --------- | --------- | --- | --- | ------ | ------- | ----------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
FORMULATIONSFORSIMULATIONANDCONTROL.
| both        | model-based |                           | and learning-based |          |          | methods.  |              |         |                              |     |     |                |     |          |         |
| ----------- | ----------- | ------------------------- | ------------------ | -------- | -------- | --------- | ------------ | ------- | ---------------------------- | --- | --- | -------------- | --- | -------- | ------- |
|             |             |                           |                    |          |          |           |              |         | Features                     |     |     | ML Geometrical |     | Discrete | Rod FEM |
|             |             |                           |                    |          |          |           |              |         |                              |     |     | ✓              | ✓   |          | ✗       |
|             | III.        | FEATURESOFSOFTROBOTMODELS |                    |          |          |           |              |         | ComputationalEfficiency      |     |     |                |     | ∼        | ∼       |
|             |             |                           |                    |          |          |           |              |         | AccurateforComplexGeometries |     |     | ∼              | ✗   | ∼        | ∼ ✓     |
| The         | soft        | robotics                  | community          |          | proposed | various   | techniques   |         |                              |     |     |                |     |          |         |
|             |             |                           |                    |          |          |           |              |         | UsableinReal-timeControl     |     |     | ✓              | ✓   | ∼        | ∼ ✗     |
| to describe |             | continuum                 |                    | and soft | robots.  | According |              | to [8], |                              |     |     |                |     |          |         |
|             |             |                           |                    |          |          |           |              |         | Data-drivenAdaptability      |     |     | ✓              | ∼   | ∼        | ∼ ∼     |
| soft        | robotics    | encompasses               |                    | four     | model    | classes:  | data-driven, |         |                              |     |     |                |     |          |         |
|             |             |                           |                    |          |          |           |              |         | HandlesLargeDeformations     |     |     | ∼              | ∼   | ∼        | ✓ ✓     |
discrete, geometrical, and continuum mechanical (Figure 1). IncorporatesMaterialModels ✗ ∼ ∼ ✓ ✓
Clearly, each strategy has advantages and limitations, which EaseofFormulation/Implementation ✓ ✓ ✓ ∼ ✗
depend on the purpose and objectives. Also, some approaches GeneralizationtoNewTasks ✗ ∼ ∼ ✓ ✓
couldpartiallyoverlaporbecombinedtoderivehybridmodels ModelInterpretability ✗ ✓ ✓ ✓ ✓
|       |        |         |             |     |     |          |           |     | HandlesPhysicalInteractions |     |     | ∼   | ∼   | ∼   | ✓ ✓ |
| ----- | ------ | ------- | ----------- | --- | --- | -------- | --------- | --- | --------------------------- | --- | --- | --- | --- | --- | --- |
| [12]. | In the | context | of modeling |     | and | control, | we answer | the |                             |     |     |     |     |     |     |
(✓)=HighlySuitableorAdvantageous
| following | question: |     | What | are the | advantages |     | and disadvan- |     |     |     |     |     |     |     |     |
| --------- | --------- | --- | ---- | ------- | ---------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
(∼)=ModeratelySuitableorPartiallyEffective
tages of rod models with respect to other techniques? To this (✗)=LessSuitableorChallenging
| end,         | we provide | a              | concise    | characterization |           | of   | the features | of      |             |                  |                |                          |             |       |            |
| ------------ | ---------- | -------------- | ---------- | ---------------- | --------- | ---- | ------------ | ------- | ----------- | ---------------- | -------------- | ------------------------ | ----------- | ----- | ---------- |
| the existing |            | modeling       | techniques |                  | and their | role | in the       | control |             |                  |                |                          |             |       |            |
|              |            |                |            |                  |           |      |              |         | Geometrical | models           | reduce         | the infinite-dimensional |             |       | contin-    |
| problem.     | We         | also           | report     | the main         | features  | in   | Table I.     |         |             |                  |                |                          |             |       |            |
|              |            |                |            |                  |           |      |              |         | uum problem | by directly      | parameterizing |                          | the         | robot | shape with |
|              |            |                |            |                  |           |      |              |         | a finite    | set of kinematic | variables.     |                          | In contrast | to    | continuum  |
| A. Machine   |            | Learning-based |            | Models           |           |      |              |         |             |                  |                |                          |             |       |            |
mechanicsapproaches,thisreductionisintroducedatthelevel
MLisapowerfuldata-drivenapproachtoderivetheforward of the kinematic representation, and the resulting models do
modelofCSMs[22].Unlikeanalyticalmethods,whichrequire not rely on the underlying continuum PDEs when deriving
explicit geometrical and physical descriptions of the robot static or dynamic equations. Instead, the governing equations
mechanics,MLonlyrequirestrainingartificialneuralnetworks are constructed directly from the generalized coordinates cho-
(ANNs) on descriptive motion data to approximate the map sen to represent the geometry. These variables can then be
between actuation and task space [23]. The advantages of used within static or dynamic equilibrium formulations, for
this approach include independence from the robot, the com- example, through energy-based or virtual work principles.
| putational | efficiency |     | of the | forward | model, | and | the potential |     |     |     |     |     |     |     |     |
| ---------- | ---------- | --- | ------ | ------- | ------ | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Duetotheirlow-dimensionalstructureandintuitivegeomet-
implicit representation of complex physical phenomena, such ric interpretation, these models are particularly attractive for
ashysteresis[12].Indeed,learnedforwardmodelswereeffec- real-timeestimationandcontrol.Indeed,geometricalrepresen-
| tively | employed | within | control | policies |     | for tracking | [24], | [25] |              |                   |     |          |     |                     |     |
| ------ | -------- | ------ | ------- | -------- | --- | ------------ | ----- | ---- | ------------ | ----------------- | --- | -------- | --- | ------------------- | --- |
|        |          |        |         |          |     |              |       |      | tations have | been successfully |     | employed |     | in both model-based |     |
and throwing [26]. However, they might become unsuitable [30] and learning-based control frameworks [31]. However,
for complex manipulation tasks due to the challenges of theiraccuracystronglydependsonthevalidityoftheassumed
collecting and labeling representative interaction data [27]. shape parametrization. In highly constrained interactions or
Other limitations include the lack of interpretability of the under complex distributed loading conditions, the imposed
forward model and the tendency to overfit the training data. geometric representation may become insufficient to capture
|     |     |     |     |     |     |     |     |     | localized | deformations, | shear, | torsion, | or  | material-dependent |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | ------------- | ------ | -------- | --- | ------------------ | --- |
B. Geometrical Models effects unless enriched with additional theories [32].
| Geometrical |     | models | describe |     | the configuration |     | of  | CSMs |     |     |     |     |     |     |     |
| ----------- | --- | ------ | -------- | --- | ----------------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
throughafinite-dimensionalparametrizationoftheirbackbone
|        |           |         |          |             |            |               |        |          | C. Discrete | Models |          |        |     |                  |     |
| ------ | --------- | ------- | -------- | ----------- | ---------- | ------------- | ------ | -------- | ----------- | ------ | -------- | ------ | --- | ---------------- | --- |
| shape. | Rather    | than    | deriving | the         | robot      | configuration |        | directly |             |        |          |        |     |                  |     |
|        |           |         |          |             |            |               |        |          | The concept | behind | discrete | models |     | is to discretize | the |
| from   | continuum | balance |          | laws, these | approaches |               | assume | that     |             |        |          |        |     |                  |     |
the deformed backbone can be represented by a predefined system at the beginning of the modeling process. The main
family of curves or shape functions, whose parameters con- approachesinthiscategoryarelumped-massandpseudo-rigid.
Lumped-mass:Thelumped-massmethodapproximatesthe
| stitute | the generalized |     | coordinates |     | of  | the system | [8]. | Typical |     |     |     |     |     |     |     |
| ------- | --------------- | --- | ----------- | --- | --- | ---------- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- |
examples include curvature, arc length, modal amplitudes, CSM as a set of lumped masses, springs, and dampers [33].
or spline control points. Within this class, the most widely In this case, the configuration variables represent the spatial
|         |          |     |        |                  |     |     |           |       | displacements | of each | lumped | mass. | The | modularity | of this |
| ------- | -------- | --- | ------ | ---------------- | --- | --- | --------- | ----- | ------------- | ------- | ------ | ----- | --- | ---------- | ------- |
| adopted | approach |     | is the | PCC formulation, |     |     | where the | robot |               |         |        |       |     |            |         |
is approximated as a sequence of circular arcs with constant approach can be adapted to represent arbitrarily complex
curvatureandnegligibletorsion[13].PCCmodelsareparticu- phenomena (e.g., nonlinear friction) and morphologies (e.g.,
larlyeffectiveforslendercontinuummanipulatorsactuatedby hybridkinematicchains).Ontheotherhand,todescribeCSMs
tendons or pressure chambers arranged parallel to the back- with the same fidelity of continuum mechanics, they require a
bone, since these actuation patterns naturally induce constant- highnumberoflumpedmassesthatentailcomputationaleffort
curvature deformations in free space. Extensions based on in addition to data-intensive system identification. Nonethe-
variable curvature [28], polynomial curvature [29], modal less, the adoption of this method is facilitated by open-source
representations, and spline-based parameterizations have also simulators like SoMo [34] and Titan [35].
been proposed to improve the trade-off between model accu- Pseudo-rigid:Conversely,thepseudo-rigidapproachrepre-
racy and computational efficiency. sents CSMs with a chain of rigid links connected by joints,

4
| finding an        | equivalent   |               | hyper-redundant |             | rigid      | robot.              | Their        | for-    |     |     |     |     |     |     |     |
| ----------------- | ------------ | ------------- | --------------- | ----------- | ---------- | ------------------- | ------------ | ------- | --- | --- | --- | --- | --- | --- | --- |
| mulation          | allows       | us to         | exploit         | the         | standard   | controllers         |              | from    |     |     |     |     |     |     |     |
| rigid robotics    |              | directly      | [36].           | Therefore,  |            | pseudo-rigid        |              | models  |     |     |     |     |     |     |     |
| can provide       | satisfactory |               | approximations  |             |            | for hyper-redundant |              |         |     |     |     |     |     |     |     |
| arms [37].        | However,     |               | accurately      | reproducing |            | smooth              |              | contin- |     |     |     |     |     |     |     |
| uous deformations |              | and           | large           | curvatures  |            | generally           | requires     | a       |     |     |     |     |     |     |     |
| high number       | of           | discrete      | joints          | and         | DoFs,      | increasing          |              | model   |     |     |     |     |     |     |     |
| complexity        | and          | computational |                 | cost.       | Therefore, |                     | pseudo-rigid |         |     |     |     |     |     |     |     |
| methods           | can be       | less          | practical       | for         | modeling   | the                 | continuous   |         |     |     |     |     |     |     |     |
elasticstructuresfoundinsoftrobotics.Nonetheless,[38],[39]
| successfully | adapted |                | the MuJoCo |              | simulator | [40] | to describe |     |                  |        |           |                 |           |            |      |
| ------------ | ------- | -------------- | ---------- | ------------ | --------- | ---- | ----------- | --- | ---------------- | ------ | --------- | --------------- | --------- | ---------- | ---- |
| CSMs and     | train   | learning-based |            | controllers. |           |      |             |     |                  |        |           |                 |           |            |      |
|              |         |                |            |              |           |      |             |     | Fig. 2. Overview | of rod | theories. | Euler-Bernoulli | considers | an elastic | rod, |
supposedtobeunstretchableandunshearable,thatcanonlybendinoneplane.
TimoshenkoextendstheEuler-Bernoulliformulationbyconsideringshearand
| D. Continuum |     | Mechanical |     | Models |     |     |     |     |     |     |     |     |     |     |     |
| ------------ | --- | ---------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
bending.Kirchhoffintroducestheconceptofdirectors,modelingbendingand
Finally, continuum mechanical models apply the principles torsion.Fromthedirectors’idea,CosseratRodTheoryexpandstheKirchhoff
of continuum mechanics to characterize soft robots with RodTheory,includingalsolineardeformations,suchasshearandelongation.
| continuous          | configuration |       | spaces      | and        | define     | deformations |            | in      |              |          |               |          |        |                     |     |
| ------------------- | ------------- | ----- | ----------- | ---------- | ---------- | ------------ | ---------- | ------- | ------------ | -------- | ------------- | -------- | ------ | ------------------- | --- |
| physical            | terms.        | This  | formulation |            | enables    | the          | simulation | of      |              |          |               |          |        |                     |     |
|                     |               |       |             |            |            |              |            |         | manipulation | [27].    | For these     | reasons, | rod    | theories constitute |     |
| physical            | interactions  |       | (e.g.,      | contact    | with       | objects      | or         | fluids) |              |          |               |          |        |                     |     |
|                     |               |       |             |            |            |              |            |         | the main     | focus of | the remainder | of this  | paper. |                     |     |
| and the             | in-depth      | study | of          | robot      | mechanics, | particularly |            | for     |              |          |               |          |        |                     |     |
| large deformations. |               | These |             | properties | make       | them         | promising  |         |              |          |               |          |        |                     |     |
towards CSMs interacting with unstructured environments. IV. BACKGROUNDONRODTHEORIES
| Depending | on  | the dimensionality |     |     | and | approximation |     | level, |            |        |         |         |       |          |         |
| --------- | --- | ------------------ | --- | --- | --- | ------------- | --- | ------ | ---------- | ------ | ------- | ------- | ----- | -------- | ------- |
|           |     |                    |     |     |     |               |     |        | An elastic | rod is | a quasi | 1D body | whose | length L | is much |
we can consider 3D models based on the FEM and low- larger than the radius of its cross-section. Under this assump-
dimensional formulations such as rod models. tion,deformationisprimarilydescribedalongthelongitudinal
| FEM: | The FEM | is  | one of | the most | widely | used | numerical |     |     |     |     |     |     |     |     |
| ---- | ------- | --- | ------ | -------- | ------ | ---- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
axis,whilecross-sectionaldeformationsareneglected.Slender
approaches for solving PDEs, particularly for modeling 3D elastic structures are widespread in nature (e.g., hairs, muscle
elastic bodies. FEM discretizes the soft robot volume into fibers,DNAstrands,flagella),andprovideaneffectiveapprox-
| a mesh, | a set | of interconnected |     |     | finite | elements | (e.g., | line |             |                |     |          |         |                 |     |
| ------- | ----- | ----------------- | --- | --- | ------ | -------- | ------ | ---- | ----------- | -------------- | --- | -------- | ------- | --------------- | --- |
|         |       |                   |     |     |        |          |        |      | imation for | many continuum |     | and soft | robots. | Mathematically, |     |
segments, triangles, tetrahedra). The points defining these the configuration of an elastic rod is represented by a time-
elements are called nodes, where physical quantities like varying curve, commonly referred to as the backbone. The
displacementorstressarecomputed.Then,thecontinuousso-
backboneisparameterizedbythematerialcurvilinearabscissa
lutioncanbeapproximatedbyinterpolatingvaluesbetweenthe s∈[0,L], where each point, denoted by r(s,t), is expressed
nodes.This approachenablesaccurate simulation ofcomplex, with respect to an inertial frame {I} = {O ;x ,y ,z }.
|     |     |     |     |     |     |     |     |     |     |     |     |     |     | I I | I I |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
nonlinear deformations to the extent of high computational s = 0 s = L
|           |             |     |              |     |              |     |         |     | The points | corresponding |        | to       | and           | are  | referred |
| --------- | ----------- | --- | ------------ | --- | ------------ | --- | ------- | --- | ---------- | ------------- | ------ | -------- | ------------- | ---- | -------- |
| costs and | an involved |     | mathematical |     | formulation. |     | Indeed, | the |            |               |        |          |               |      |          |
|           |             |     |              |     |              |     |         |     | to as the  | base and      | tip of | the rod, | respectively. | Each | cross-   |
solutions provided by standard commercial software (e.g., section is characterized by geometric and material properties,
Abaqus, Ansys, COMSOL) would impede real-time control. includingthecross-sectionalareaA(s),thesecondmomentof
Therefore,theywereoftenlimitedtodesigningandsimulating
|     |     |     |     |     |     |     |     |     | area tensor | J = diag(J |     | x (s),J y (s),J | z (s)), | the mass | density |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ---------- | --- | --------------- | ------- | -------- | ------- |
soft robotic components [41] or as a benchmark. Nonetheless, ρ(s), the Young’s modulus E(s), and the shear modulus
recent MOR techniques implemented in the SOFA simulator G(s) = E(s)/2(1+ν), where ν denotes the Poisson ratio.
| [42]–[44] | are making |     | 3D mechanical |     | models | more | affordable |     |               |     |         |          |               |          |     |
| --------- | ---------- | --- | ------------- | --- | ------ | ---- | ---------- | --- | ------------- | --- | ------- | -------- | ------------- | -------- | --- |
|           |            |     |               |     |        |      |            |     | In this work, | Lie | Algebra | notation | is frequently | adopted, |     |
even for learning-based control [45], [46]. and the corresponding mathematical operators are reported
Rod: When the robot is slender, it can be efficiently repre- in Appendix B. Elastic rods may exhibit bending, torsion,
| sented using | elastic | rod | formulations, |     | which | approximate |     | the |            |             |     |               |     |                  |     |
| ------------ | ------- | --- | ------------- | --- | ----- | ----------- | --- | --- | ---------- | ----------- | --- | ------------- | --- | ---------------- | --- |
|              |         |     |               |     |       |             |     |     | stretching | (elongation | or  | compression), | and | shear. Different |     |
body as a one-dimensional (1D) continuum. In particular, the rod formulations capture different combinations of these de-
Cosserat rod theory (CRT) can effectively describe all modes formation modes, leading to trade-offs between accuracy and
| of deformations |     | in  | CSMs | [47]–[49]. |     | The CRT | associates |     |     |     |     |     |     |     |     |
| --------------- | --- | --- | ---- | ---------- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
computationalcomplexityforsimulationandcontrol.Figure2
a reference system to each cross-section along the CSM. summarizes the strain modes considered by the main rod
Each cross-section can translate and rotate relative to the theoriesemployedinsoftrobotics,namelyCosserat–Reissner,
adjacentcross-sectionstosimulatebending,twisting,shearing, Kirchhoff–Clebsch–Love, Euler–Bernoulli, and Timoshenko–
| and stretching.    |     | Thanks    | to the | low-dimensional |      |     | yet physics-  |          |            |           |          |        |           |           |     |
| ------------------ | --- | --------- | ------ | --------------- | ---- | --- | ------------- | -------- | ---------- | --------- | -------- | ------ | --------- | --------- | --- |
|                    |     |           |        |                 |      |     |               |          | Ehrenfest, | which are | reviewed | in the | following | sections. |     |
| based formulation, |     | rod       | models | retain          | most | of  | the           | benefits |            |           |          |        |           |           |     |
| of continuum       |     | mechanics | at     | a fraction      | of   | the | computational |          |            |           |          |        |           |           |     |
cost of FEM. A limitation of rod models is their underlying A. Cosserat Rod Theory
assumption of structural slenderness, although heterogeneous The CRT [53] describes all strain modes of the rod.
rodassembliescanbeusedtorepresentmorecomplexsystems This model is useful for describing CSMs that interact with
[50], [51]. Beyond modeling, rod models are also gaining cluttered environments, in which shear and elongation de-
popularity in model-based control [52] and learning-based formations play a fundamental role. Each cross-section s is

5
associated with a reference system {S s } = {O s ; x s ,y s ,z s }, • The External Forces Wrench F e = (cid:2) m⊤ e n⊤ e (cid:3)⊤ ∈ R6
whose axes are called directors. The relative roto-translation representsthedistributedexternalloadappliedtotheRod.
between {S } and {I} is expressed by the homogeneous For instance, the effect of gravity can be computed as
s
matrix g(s,t)∈SE(3) defined as
F =M (cid:0) Ad−1G (cid:1) , (7)
(cid:20) (cid:21) e g
R(s,t) r(s,t)
g(s,t)= , (1)
0⊤ 1 where G ∈ R6 is the gravity acceleration twist w.r.t. the
inertial frame and M = ρdiag(J ,J ,J ,A,A,A) is
where R(s,t) ∈ SO(3) is the rotation matrix that represents x y z
the cross-sectional inertia matrix.
r c e r l o a s t s iv -s e ec ro ti t o a n tio s n t . o T f h r e ee m ly ai r n ot i a d te ea an o d f t t h ra e n C sl R at T e i r s el t a o tiv a e ll l o y w . every • T R h 6 e e A xp c r tu es a s t e io s n th F e or i c n e t s ern W a r l en a c c h tiv F e a for = ces (cid:2) m ex ⊤ a erted n⊤ a b (cid:3) y ⊤ th ∈ e
1) Kinematics: Letthestraintwist ξ(s,t)∈R6 bedefined
actuators. Refer to Sec. V for more details.
as
For clarity, the distributed wrenches (F , F , F ) represent
(cid:20) (cid:21) i a e
ξ(s,t)= (cid:0) g−1(s,t)g′(s,t) (cid:1)∨ , ξ(s,t)= κ(s,t) , (2) theforcesandtorquesactingonaparticularcross-section(s=
σ(s,t)
s¯), rather than force or torque densities distributed along the
whereκ(s,t)∈R3 aretheangularstrainmodes(bendingand body’s length.
torsion), σ(s,t) ∈ R3 are the linear strain modes (shear and Afterdefiningthesequantities,itispossibletocomputethe
elongation/compression),and(·)′ = ∂ (·)isthespatialpartial Dynamics of an elastic rod using the Poincare´ equations [55]
∂s
derivative. Similarly, it is possible to define the velocity twist
Mη˙ +ad∗ (Mη)=(F −F )′+ad∗(F −F )+F .
η(s,t)∈R6 as η i a ξ i a e
(8)
(cid:20) (cid:21)
η(s,t)= (cid:0) g−1(s,t)g˙(s,t) (cid:1)∨ , η(s,t)= ω(s,t) , (3) The EoMs (8) is a set of PDEs of a Cosserat Rod in the local
v(s,t) frame. It is common also to find the same set of PDEs in an
explicit form and expressed in the inertial frame, such as [48]
where ω(s,t),v(s,t) ∈ R3 are the angular and linear veloc-
ities of cross-section s, and (· ˙ ) = ∂ (·) is the time partial ρAv˙I = (cid:0) nI (cid:1)′ +nI
derivative. The strain and velocity tw ∂t ists are both expressed ρIω˙I +ωI ∧ (cid:0) ρIωI(cid:1) = (cid:0) m i, I a (cid:1)′ +r e ′∧nI +mI , (9)
in the local frame {S } and represent the evolution of the rod i,a i,a e
s
over space and time. Thanks to the mixed partial derivatives
where (·)I denotes a variable expressed in the inertial frame,
equality, it is possible to derive a kinematic relation between
I = RJR⊤ is the second moment of the area expressed in
the strain and velocity twist, such as
the inertial frame, and n =n −n and m =m −m
i,a i a i,a i a
(cid:90) s
η(s)=Ad Ad ξ˙(ζ)dζ. (4) are the contributions of the internal and actuation forces.
g−1 g 3) Strain Parameterization: The Configuration Space (5)
0
and PDEs (8) show the infinite DoFs of an elastic rod.
whereζ denotesanintegrationvariableinsteadofthematerial
From a control and numerical implementation perspective, it
abscissa s.
is convenient to find a method to discretize the continuum
From a mathematical point of view, the main idea of the CRT
body. [56] and [54] proposed a Strain Parameterization, also
can be well condensed in the Configuration Space, defined as
known as Geometrical Variable Strain (GVS) [57], expressing
C =SE(3)×SE(3)×···×SE(3)×... . (5) the Kinematics and the Dynamics of the elastic rod in terms
of strain twist ξ(s,t). Let us again consider the definition of
Definition(5)indicatestheinfiniteDoFsofanelasticrod.The the strain twist (2), which is easily rewritten as g′ = gξˆ.
Configuration Space results in a functional space of curves
Assuming that the initial condition g(0) = g is known, the
in SE(3) [54]. While the infinite-dimensional configuration 0
functiong(s)canbeunivocallydeterminedbythestraintwist.
space is a unique feature of soft robots, it also makes control
The Configuration Space can be considered the Shape Space
particularly challenging.
S of the elastic rod, which is a functional space of the s-
2) Dynamics: To describe the equations of motion (EoMs) parameterized curves in R6, such as
of an elastic rod, it is necessary to define three distributed
wrenches along the length of the rod: C =S={ξ :s∈[0,L]→ξ(s)∈R6}. (10)
• The Internal Forces Wrench F i = (cid:2) m⊤ i n⊤ i (cid:3)⊤ ∈ R6 This functional space can be generated by an infinite-
expressestheinternalloadappliedbythematerial,includ-
dimension basis matrix B (s), such as
ing elastic and damping effects. Assuming small strains, q
a linear viscoelastic constitutive model relates the strain
ξ(s,t)=B (s)q(t)+ξ∗, (11)
field ξ and the internal forces wrench F . q
i
F (s)=Σ(ξ−ξ∗)+Υξ˙, (6) where B q ∈ R6×n and q ∈ Rn is a vector of generalized
i coordinates, with n→∞. The main idea of the discretization
where ξ∗ ∈ R6 is the stress-free strain twist, technique is to truncate the basis matrix to a finite number
Σ = diag(GJ ,EJ ,EJ ,EA,GA,GA) = of n columns, reducing the discretized Shape Space to C =
x y z
diag(Σ , Σ ) ∈ R6×6 is the stiffness matrix and Rn. This approach allows the user to choose the degree of
κ σ
Υ = βdiag(J ,3J ,3J ,3A,A,A) ∈ R6×6 is the approximation or neglect certain strain modes. To solve the
x y z
viscosity matrix. PDEs, the proposed method uses the Magnus Expansion [58],

6
resulting in a convenient Product of Exponentials, which is other nodes and external forces. In addition, it is possible to
widely used in classical robotics [59] associate kinematic and dynamic quantities to each node and
(cid:16) (cid:17) segmenttosolve(16).Inthediscretedomain,somequantities,
g(s)=g 0 exp Ωˆ(s) , (12) suchascurvature,mustbeexpressedinanintegratedformover
the domain D [48]. This domain corresponds to the Voronoi
where Ωˆ(s) ∈ se(3) denotes the Magnus expansion of the region D associated with the interior nodes i∈[1,N −1],
i
strain twist. Thanks to that, it is possible to rewrite the
Differential Kinematics with a well-known form, such as D =(ℓ +ℓ )/2, (17)
i i−1 i
η(s,t)=J(q,s)q˙, (13) where ℓ = |r − r | is the length of the i-th segment.
i i+1 i
where J(q,s) ∈ R6×n denotes the Soft Geometric Jacobian. Then, the discrete curvature and bending stiffness matrix can
be written as
Similarly, the Dynamics can be rewritten in a classical La-
grangian form log (cid:0) R⊤R (cid:1)
κ¯ = i i−1
i D¯
Mq¨+Cq˙+Kq+Dq˙ =Bτ +F e . (14) Σ¯ ℓ + i Σ¯ ℓ , (18)
The EoMs (14) can be solved using a standard time solver, B¯ i = κ,i i 2D¯ κ,i−1 i−1
i
such as Runge-Kutta or Explicit Euler, as implemented in the
SoRoSim simulator [60]. with i∈[1, N −1]. Finally, the discretized EoMs of the rod
Recently,theAuthorsshowedhowtocomputetheanalytical can be rewritten in algorithmic form as follows:
derivativesoftheGVSapproach[61],evolvingSoRoSimasa (cid:32) R (cid:0) Σ¯ σ (cid:1)(cid:33)
differentiablesimulator.Inthiswork,theAuthorsalsoshowed m v˙I =∆h j σ,j j +F¯
the benefits of the implicit time-integration schemes, such as i i e i
j
the Implicit Euler and the Newmark-β methods. J¯ (cid:18) B¯ κ¯ (cid:19) (cid:18) κ ∧B¯ κ (cid:19)
Finally, to fully describe soft robots interacting with the jω˙ =∆h i i +Ah i i iD +
e j E3 E3 i
environment, [62] proposed an extension of (14), including j i i , (19)
(cid:18) (cid:19)
frictional contacts with rigid and soft bodies. + (cid:0) R⊤r′ ∧Σ¯ σ (cid:1) ℓ¯ + J¯ ω j ∧ω +
4) Discrete Elastic Rod: Another method to discretize j j σ,j j j j e j
j
the continuum nature of elastic rods was introduced in the J¯ω
pioneering work of [48]. First, the Authors derived the EoMs + j e2 j e˙ j +C j
(9), including an elongation/compression ratio defined as j
e = ds/ds¯, where s¯ is the curvilinear abscissa in the rest where m is the point-wise mass associated with the node,
i
configuration. This ratio is present because the length is E = D /D¯ is a domain dilation factor, ∆h and Ah are the
i i i
parameterized using the curvilinear abscissa differently from discrete difference and the averaging operator defined in [48].
(9). In the presence of axial stretching, the stretching ratio e In the first equation of (19), i ∈ [0,N], and j ∈ [0,N −1].
scales the geometrical quantities In contrast, in the second equation, i ranges [1,N−1], while
A¯ J¯ (cid:18) 1 1 (cid:19) κ¯ j still ranges from [0,N−1]. This distinction arises from the
A= , J = , Σ=diag , Σ¯, κ= (15) definition of discrete curvature and bending stiffness within
e e2 e2 e e
the interior nodes set.
wherethebarsign( ¯ ·)indicatesthegeometricquantitiesinthe For the time integration of the discretized EoMs (19), the
rest configuration. The EoMs can be finally written as authorsproposedaSecond-OrderPositionVerlet timeintegra-
tor,whichexhibitsagoodbalancebetweennumericalaccuracy
(cid:32) (cid:33)′
nI and computational cost [48]. To ensure numerical stability,
ρAv˙I = i,a +enI
e e insteadofenforcingrigorousCourant-Friedrichs-Levystability
conditions [64], they proposed an empirical law to choose the
(cid:18) J (cid:19) (cid:18) J (cid:19) (cid:16)m (cid:17)′ κ∧m
ρ ω˙ +ω∧ ρ ω = i,a + i,a integration time step as dt≈0.01L. The discrete EoMs (19)
e e e3 e3 . (16) were implemented in the PyElastic N a simulator [65].
(cid:18) r′(cid:19)
+R⊤ ∧n
e i,a
B. Kirchhoff Rod Theory
(cid:18) (cid:19)
J
+ ρ ω e˙+em
e2 e The Kirchhoff rod theory (KRT) [66] is a special case
of CRT that considers an elastic rod unstretchable and un-
It is worth highlighting that (16) contains an additional con- shearable [48], [67], [68]. It is particularly suitable for CSMs
tribution with respect to (8), which depends on the time that bend around any axis and twist. Notably, it introduces
derivative of stretching ratio e˙. Furthermore, scaling the ge- the notion of a directed curve, assigning a specific reference
ometrical quantities partially relaxes the assumption of rigid systemtoeachcross-section.TheEoMsofKirchhoffrodscan
cross-sections. To numerically resolve the EoMs (16), they be computed by specializing the EoMs of Cosserat, that is (8)
extendedforaCosseratrodthespatialdiscretizationalgorithm or (9). In particular, the constraint of an unstretchable and
proposed in a previous study [63], which discretizes the rod unshearable rod can be written as
in a sequence of N rigid segments connecting N +1 nodes.
(cid:2) (cid:3)⊤
For each node, the EoMs consider the interactions with the σ = 1 0 0 . (20)

7
The constraint (20) enforces e(t) ≡ 1, which implies e˙ = 0 Cartesianposeofeverycross-sectionsisuniquelydetermined
[48]. Incorporating this constraint into the EoMs leads to the by the curvature, i.e.
following modified equations of motion: (cid:90) s
x(s)=L cos(α(ζ)) dζ,
ρAv˙I = (cid:0) nI (cid:1)′ +nI
i,a e 0
(cid:90) s
ρJω˙ +ω∧(ρJω)=(m i,a )′+κ∧m i,a . (21) y(s)=L sin(α(ζ)) dζ, (26)
+ (cid:0) R⊤r′(cid:1) ∧n +m 0
i,a e (cid:90) s
α(s)= κ (ζ)dζ.
The linear internal force n serves as a Lagrangian mul- z
i,a 0
tiplier and it is a virtual internal force that constrains the rod
Furthermore, from (26), it is possible to derive the EoM
from stretching or shearing. As stated in [48], inserting the
following the Lagrangian approach. Similarly to the Strain
constraintofanunshearableandunstretchablerodcanincrease
Parameterization,theyproposetoconsiderthecurvatureκ (s)
the computational time. z
as an infinite sum of monomials in s, i.e.
In the case of Strain Parameterization, it is sufficient to
apply the constraint (20) in the strain twist n−1
(cid:88) (cid:16)s(cid:17)i
κ (s)= θ withn→∞. (27)
(cid:104) (cid:105)⊤ z i L
ξ(s,t)= κ⊤(s,t) (cid:0) 1 0 0 (cid:1)⊤ . (22) i=0
The geometrical meaning of the polynomial curvature is to
Therefore,thebasisfunctionmatrixonlygeneratestheangular
constraintheshapeofthebackbonecurvetobeaGeneralized
strainmodevectorκ(s,t).Unlikethepreviousapproach,(22)
CornuSpiral,i.e.,acurvewithapolynomialcurvature[29].It
does not apply as a constraint, and the EoMs can be solved
is worth highlighting that the (27) is equivalent to write (11)
without considering any Lagrangian multipliers.
withapolynomialbasisfunction,relatedonlytothecurvature
κ [52]. Defining q = (cid:2) θ θ ··· θ (cid:3)⊤ ∈ Rn as joint
z 0 1 n−1
C. Euler-Bernoulli Rod Theory variables, it is possible to write the EoMs as
The Euler-Bernoulli rod theory (EBRT) [69] is one of the Mq¨+Cq˙+G+Kq+Dq˙ =A(q)τ, (28)
simplest rod theories in which the rod can only bend around
oneaxis.Itcanbeconsideredthe2DcaseoftheKRTwithout where A(q) ∈ Rn×na is transposed orientation jacobian for
the twist. Here, the assumption is that the slope angle of the n a actuators and τ ∈Rna are the pure actuators’ torque.
rodisequaltothetangentangleofthebackbonecurve.Below,
we report linear and nonlinear versions.
D. Timoshenko Rod Theory
1) Linear Euler-Bernoulli: Let us consider the rod in the
The Timoshenko-Ehrenfest rod theory [72] extends the
x-y plane. Unlike the previous theories, the backbone curve
is described by the displacement w(x,t) ∈ R from the x- EBRT, relaxing the unshearability constraint. Therefore, the
equality between the tangent angle and the cross-sections’
axis. Recalling the assumption of the EBRT, the slope angle
α(x,t)∈R of the beam can be written as angleisnolongervalid(i.e.,α(x)̸=∂w/∂x).Forthisreason,
the EoMs of a Timoshenko rod considers the angle α(x,t) as
∂w an independent variable. Its dynamics can be written as
α(x,t)= . (23)
∂x
(cid:18) ∂2w (cid:19) ∂
From the minimization of the strain energy, the EoM of the ρA ∂t2 =m e,z (x,t)+ ∂x n i,y (x,t)
rod can be computed as (29)
(cid:18) ∂2α (cid:19) ∂
∂4w(x,t) ∂2w(x,t) ρJ z ∂t2 = ∂x m i,z (x,t)+n i,y (x,t).
EJ +ρA =m (x,t), (24)
z ∂x4 ∂t2 e,z
The standard formulation assumes a linear constitutive law
where m e,z (x,t) is the distributed external moments around with bending moment m i,z and shear force n i,y defined as
the z-axis. The EoM (24) is linear, assuming that the consti-
(cid:18) (cid:19)
tutive law of the bending moment m (x,t) is ∂α ∂w
i,z m =EJ n =γGA −α , (30)
i,z z ∂x i,y ∂x
∂2w
m i,z =EJ z∂x2 , (25) where γ is the Timoshenko shear coefficient, which depends
on the cross-section geometry. We can see that the shear
where m ∈ R is the z-component of the internal moment
i,z force contribution is proportional to the difference between
m . For control purposes, the linearity of (24) facilitates the
i the tangent angle ∂w/∂x and the angle of cross-section α.
useofefficientcontrollersfromtheclassiccontroltheory[70].
2) Nonlinear Euler-Bernoulli: In the nonlinear EBRT
(or Euler’s Elastica), the rod length is parameterized by the
V. MODELINGACTUATION
arclength s. Recalling the Fundamental Theorem of the local The distinction between physical and robotic models lies in
theory of Curves in the 2D case, every regular curve can be the inclusion of actuation. In soft robotics, actuation sources
determined by the curvature [71]. From this concept, [29] greatly differ from those used in rigid robots. In particular,
reformulated Elastica in a classical robotic formulation. Let the most used technologies are cables and fluidic chambers,
κ (s) be the z-component of the curvature twist κ(s). The which guarantee distributed active loads F (s).
z a

8
strainmodesinducedbytheactuators.Fromacontrolperspec-
tive, this information is related to the system’s reachability.
B. Actuators-Strain Mapping
Fromthedefinitionofactuationmatrix(35),itispossibleto
map the actuation magnitude vector to the distributed active
load F . [56] propose a statics-based method to relate the
a
actuators with excited strain modes. In particular, let be the
statics of a Cosserat Rod as
(F −F )′+ad∗(F −F )=0, (36)
i a i a
assuming no external forces and the strain twist is discretized
withtheStrainParameterizationapproach,i.e.(11).Byinvok-
ing the D’Alembert Principle, it is possible to derive
(cid:90) L (cid:90) L
B⊤F ds= B⊤F ds. (37)
q i q a
0 0
Finally, substituting the constitutive relation (6) and the defi-
nition of actuation forces (34), we derive
(cid:32) (cid:33) (cid:32) (cid:33)
Fig. 3. Cross section of a soft robot with equally spaced actuators (e.g., (cid:90) L (cid:90) L
pneumatic chambers, cables). The vector di(s) is the position of the i-th B
q
⊤ΣB
q
ds q = B
q
⊤B
τ
ds τ. (38)
actuatorinthelocalframe{Ss}.
0 0
From this equality, [73] propose a trivial form of the static
A. The Actuation Matrix equation, choosing the implicit parametrization
Consider a Cosserat rod with n a actuators. Let be d i (s)∈ ξ(s)−ξ∗(s)=Σ−1(s)B (ξ,s)q. (39)
R3 the distance from the center of the cross-section s and the τ
i-thactuator(Figure3).Eachactuatorappliesaninternalactive Consequentially, the static equation degenerates in a trivial
wrench that depends on the actuator routing. We can express form, such as
the internal active wrench F(i) applied by the actuator i as (cid:32) (cid:33) (cid:32) (cid:33)
a (cid:90) L (cid:90) L
F( a i) = (cid:20) d˜ i ( t s) ( t s i ) (s) (cid:21) τ i , (31) 0 B q ⊤B τ ds q = 0 B q ⊤B τ ds τ, (40)
i
q =τ.
where t (s) is the unit vector tangent to the actuator path and
i
Thefunctionalbasisderivedfromtheimplicitparametrization
τ is the magnitude of the actuator. For example, τ can be
i i
(39)usestheinformationofactuationroutingcontainedinB ,
(cid:40) τ
T if cable-driven actuation to provide the minimum set of functional bases. In particular,
τ = , (32)
i pA if fluidic actuation these functional bases describe the excited strain modes and
in
their optimal static representation. Furthermore, B in (35)
q
where T is the cable tension, p is the pneumatic pressure and also considers the geometrical and the material information
A in is the internal cross-section area of the fluidic chamber. of the robot, contained in Σ. Finally, (39) provides a useful
The expression of the tangent unit vector is derived as starting point for constructing the optimal functional basis
t (s)= (cid:2) g−1(gd i )′(cid:3) 3 = (cid:104) ξˆ(s)d i (s)+d′ i (s) (cid:105) 3 , (33) w m h a i t l r e ix p B res q e , r a v v in o g id a in c g cu r r e a d c u y n a d n a d nt c o o r m i p n u e t f a fi t c io ie n n a t l s e h ffi ap ci e en fu cy n . ctions
i
∥
(cid:2)
g−1(gd i
)′(cid:3)
3 ∥ ∥
(cid:104)
ξˆ(s)d i (s)+d′ i (s)
(cid:105)
∥
3 VI. RODMODELSFORCONTINUUMANDSOFTROBOTS
whered (s)isexpressedinhomogeneouscoordinatesandthe
i We categorize rod models based on the deformation modes
operator [·] extracts the first three rows of a homogeneous
3 they represent, independently of the underlying actuation
vector. The resultant of the contributions of n actuators is
a technology. From a control perspective, the specific actuation
(cid:88) na method (e.g., tendons, pneumatic chambers) is secondary to
F (s)= F(i)(s)=B (s)τ, (34)
a a τ thetypeofstrainitproduces,suchaselongationorcontraction,
i=1 torsion, or bending. The admissible deformation modes also
whereτ ∈Rna intheinternalactivewrenchandB
τ
∈R6×na implicitly determine the suitable rod theory. For example,
is the actuation matrix a robot limited to planar bending is consistent with the
(cid:20)(cid:18) d˜(s)t (s) (cid:19)na (cid:21) Euler-Bernoulli framework, while more complex deformation
B τ (s)= i t (s i ) . (35) behaviorsmightrequireCosserattheory.Whileseveralstudies
i i=1 formally employ the Cosserat rod formulation, in practice,
The actuation matrix B (s) is crucial for designing control they restrict the model to a limited subset of strain modes,
τ
algorithms because it contains valuable information about the effectively reducing it to simpler formulations. By explicitly

9
|     |     |     |     |     | to the moving |     | platform. | Beyond | kinematics, |     | [82] | developed a |
| --- | --- | --- | --- | --- | ------------- | --- | --------- | ------ | ----------- | --- | ---- | ----------- |
| A   |     |     |     | B   |               |     |           |        |             |     |      |             |
Cosseratrodmodelforcontinuummanipulators,incorporating
|     |     |     |     |     | external    | forces, | tendon | forces | and     | friction, | with      | experimental |
| --- | --- | --- | --- | --- | ----------- | ------- | ------ | ------ | ------- | --------- | --------- | ------------ |
|     |     |     |     |     | validation. | Dynamic | planar |        | bending | has       | also been | addressed    |
Stretching through variational approaches. In particular, [83] proposed
(contraction) a Lie group variational integration framework experimentally
Bending
|     |     |     |     |     | validated  | on  | magnetically |     | actuated | CSMs, | achieving | sub- |
| --- | --- | --- | --- | --- | ---------- | --- | ------------ | --- | -------- | ----- | --------- | ---- |
| C   |     |     |     |     | millimeter | tip | accuracy.    |     |          |       |           |      |
|     | OFF | ON  | OFF |     |            |     |              |     |          |       |           |      |
OFF OFF ON ON OFF ON Planarbendingmodelswerealsoappliedtoinvestigateloco-
motionstrategies.[84]modeledperistalticlocomotionwithan
|     |     |     |     |     | Euler–Bernoulli |           | rod, and | [85]      | used       | a planar | Cosserat  | rod with |
| --- | --- | --- | --- | --- | --------------- | --------- | -------- | --------- | ---------- | -------- | --------- | -------- |
|     |     |     |     |     | adjustable      | curvature | to       | reproduce | snake-like |          | swimming. | As a     |
Bending further extension, [86] developed a dynamic Euler–Bernoulli
Stretching modelofacaterpillar-inspiredrobotwithshapememoryalloy
|         |           | (elongation)           |           | Twisting           |         |            |            |            |         |           |                    |           |
| ------- | --------- | ---------------------- | --------- | ------------------ | ------- | ---------- | ---------- | ---------- | ------- | --------- | ------------------ | --------- |
|         |           |                        |           |                    | (SMA)   | actuators, | linking    | undulation |         | mechanics |                    | to ground |
|         |           |                        |           |                    | contact | forces.    | Similarly, | [87]       | applied |           | an Euler–Bernoulli |           |
| Fig. 4. | Principal | deformations exhibited | by common | continuum and soft |         |            |            |            |         |           |                    |           |
manipulators.A-B)Cable-drivenmanipulatorsstretch(contraction),bend,and formulation to predict rolling and crawling in a magnetically
twist,basedontheactuators’pathalongthecenterlineandthecross-section.
|     |     |     |     |     | actuated | soft robot. | These | works | prove | the | versatility | of rod |
| --- | --- | --- | --- | --- | -------- | ----------- | ----- | ----- | ----- | --- | ----------- | ------ |
C)Similarly,pneumaticmanipulatorsmostlystretch(elongate)andbend.
|     |     |     |     |     | models beyond |         | manipulation. |         |     |         |        |          |
| --- | --- | --- | --- | --- | ------------- | ------- | ------------- | ------- | --- | ------- | ------ | -------- |
|     |     |     |     |     | Spatial       | bending | (3D):         | Spatial |     | bending | occurs | when de- |
classifying models according to the combination of strain formation is not confined to a single plane but involves
modes they allow, we highlight such modeling choices. Out curvature around multiple axes, eventually accompanied by
|        |         |                       |                |        | torsion.These |     | casestypically |     | requireCosserat |     | orTimoshenko |     |
| ------ | ------- | --------------------- | -------------- | ------ | ------------- | --- | -------------- | --- | --------------- | --- | ------------ | --- |
| of the | fifteen | possible combinations | of deformation | modes, |               |     |                |     |                 |     |              |     |
formulationstoaccuratelycapturethecompleterangeofstrain
| only | nine classes | emerged. | We summarize | the deformation |     |     |     |     |     |     |     |     |
| ---- | ------------ | -------- | ------------ | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
classes in Table II to facilitate the literature comprehension, modes. CRT, despite its higher complexity, has extensively
|     |     |     |     |     | contributed | to  | bending | modeling | in  | cable-driven |     | robots [88]. |
| --- | --- | --- | --- | --- | ----------- | --- | ------- | -------- | --- | ------------ | --- | ------------ |
wherewearbitrarilyreportrepresentativearticlestodistilleach
AnearlyexampleofCRT-basedbendingmodelingisprovided
| class andhighlight |     | the versatilityof | rod models.An | advanced |     |     |     |     |     |     |     |     |
| ------------------ | --- | ----------------- | ------------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Scopus query aided the initial selection of the articles (see by [89], who modeled the kinematics of a cable-driven soft
|          |     |                   |                 |            | arm with     | non-uniform |            | cross-sections |     | and     | derived | its inverse |
| -------- | --- | ----------------- | --------------- | ---------- | ------------ | ----------- | ---------- | -------------- | --- | ------- | ------- | ----------- |
| Appendix | A). | We also discussed | articles beyond | the query. |              |             |            |                |     |         |         |             |
|          |     |                   |                 |            | model using  | the         | Jacobian   | matrix.        |     |         |         |             |
|          |     |                   |                 |            | In pneumatic |             | actuators, | CRT            | was | coupled | with    | nonlinear   |
A. Bend
|     |     |     |     |     | constitutive | laws | (e.g., | Mooney–Rivlin |     | hyperelasticity) |     | to im- |
| --- | --- | --- | --- | --- | ------------ | ---- | ------ | ------------- | --- | ---------------- | --- | ------ |
Bending is a prevalent deformation in continuum and soft proveaccuracy[90].Similarly,[91]computedthestaticshape
robots due to the natural propensity of slender structures of a semicylindrical soft fiber-reinforced pneumatic bending
to bend (Figure 4). Various rod models were employed to actuatorunderexternalforceconstraints,usingaNeo-Hookean
predictthebendingmotionfordifferentactuationmechanisms, model to derive the pressure-angle relationship in free motion
stiffness modulation strategies, or dynamic interactions with [92]. CRT was also applied to soft robots embedding smart
theenvironment.Toclarifythedifferentapproaches,wedistin- actuators [93]–[95]. Beyond kinematic descriptions, dynamic
guish between planar (2D) bending and spatial (3D) bending. models mainly based on CRT, provide more suitability for
Planar bending (2D): Planar bending assumes that defor- dynamic tasks and allow the integration of actuation into its
mation occurs in a single plane, which significantly simplifies formulation [96]. Further refinements in CRT-based cable-
the mathematical formulation. Among the approaches, the driven robot models included friction effects arising from
EBRT is particularly suitable for modeling simple soft robots interactions between cables and the robot structure [97]. CRT
thatbendduetoitssimplicity.Indeed,EBRTmodeledvarious was also leveraged to model tasks involving interaction with
roboticarchitectures,achievingsub-millimetertippositionac- external objects. [98] introduced a CRT-based framework to
curacy in multi-backbone continuum robots [74] and enabling analyze the coupled dynamics of tendon-driven cooperative
shape modeling in parallel continuum manipulators (PCMs) continuum robots interacting with flexible objects. Likewise,
via its non-linear formulation [75]. The Timoshenko rod [99] proposed a dynamic Cosserat rod model for a tendon-
theory, which is suitable for planar deformations (Figure 2), drivencontinuumroboticfinger,wherethegraspingforcesare
was used to model planar bending in cable-driven soft robots modeledasexternalforcesactingonthebackbone.Thesestud-
withcomplexgeometries,suchastriangularnotchedstructures ies highlight the effectiveness of CRT in dynamic interaction
[76]. Pneumatically actuated soft robots also benefited from tasks, including tip force estimation in cable-driven catheters,
rod models. EBRT captured the relationship between internal as demonstrated by [100], who used a Be´zier-based shape
pressure and bending deformation [77], later extended to interpolationandanoptimizationapproach.Anotherimportant
handle large deflections and non-linear strains [78], [79]. [80] aspectofdynamicinteractionsconcernsworkspaceestimation,
introducedaROMandadiscretizedformulationoftheSTIFF- namely the determination of the spatial region that the soft
FLOProbotusingEBRT,demonstratinghighaccuracy,numer- robot’send-effectorisabletoreachgivenitsactuationandme-
ical robustness, and near real-time performances. EBRT has chanicalconstraints.[101]developedaquasi-staticCRTmodel
alsobeenappliedformodelingplanarPCMwithtwoindepen- withacontinuationalgorithmtomapworkspaceboundariesin
dentflexiblepanels[81],integratinggeometricconstraintsdue tendon-driven manipulators, addressing self-collision, elastic

10
instabilities,andactuatorsaturation.Thestudyfoundthatcom- numerical robustness and computational efficiency. For ex-
plexCSMconfigurationscouldleadtoisolatedboundariesand ample, [55] introduced the piecewise constant strain (PCS)
voids, which are essential to consider for accurate workspace method to discretize a continuous Cosserat rod into segments
predictions. Beyond kinematic and dynamic predictions, stiff- with constant strain. This method extends the PCC approach
nessmodulationalsoplaysanimportantroleinpredictingsoft [13] by incorporating shear and torsion. In parallel, [49]
robots behavior [102] as well as mitigating undesired effects proposed a real-time discretization technique that transforms
such as buckling, which can hinder precise movements [103]. the PDEs of a Cosserat rod into a boundary value problem
Notable advancements involve variable stiffness continuum (BVP)bydiscretizingtimederivatives,significantlyimproving
manipulators, which, leveraging CRT-based modeling can computational performance.
increasestiffnessuptotentimes,resultinginimprovedcontrol Incorporating external forces such as buoyancy, drag, and
precision[104].Othertechniquesincludetheadditionoflayer added mass is essential for accurately modeling the inter-
jamming sheaths to control stiffness both along the axial and actions between soft robots and their surroundings. In this
transverse directions [105]. In parallel, research on a simple context, [47], [112] analyzed the static and dynamic behavior
rod-shaped silicone soft robot, modeled using CRT, investi- of a silicone arm in a dense medium, capturing its coupled
gatedstiffnesspropertiesbyapplyinghorizontalpullingforces tendon conditions and external loads. The model was further
at the free ends of the rod [106]. Two material models were developed in a unified Cosserat rod framework applied to
examined: a linear viscoelastic model and a nonlinear Saint underwater robots [50]. By accounting for nonlinearities and
Venant-Kirchhoff material model. The damping mechanism hydrodynamic effects, this approach enabled the evaluation of
was analyzed, revealing that linear damping can be assumed soft robot designs under submerged conditions.
for small to medium oscillations. However, non-linear effects For pneumatic actuators, [113] extended the PCS method
become relevant when oscillations reach higher amplitudes, by integrating Screw Theory, allowing flexible routing of
enhancingthemodel’saccuracy.[107]presentedaCRTmodel fluidic and tendon actuators along arbitrary paths. In PCMs,
of a soft bending actuator with an additional fabric layer to [114]adaptedthePCSformulationtoclosed-chainsoftrobotic
modify the actuator stiffness, modeled as boundary condition systems, facilitating the modeling and design optimization of
of the Cosserat model. This adjustment improved bending structures like the Fin-Ray finger.
behavior while preventing longitudinal stretching. Material nonlinearities, such as hysteresis, can significantly
FEM was widely used to augment and validate rod-based affect the performance of soft robots. [115] incorporated non-
models, particularly for pneumatic actuators. For instance, linear material effects by proposing a fractional-order Bouc-
[108] proposed a five-parameter constitutive relation for a Wen model within a Cosserat rod. The model demonstrated
pneumatic soft arm, with parameters identified via FEM superioraccuracyincapturingthelargedeformationsofpneu-
simulations under different loading conditions. Conversely, matic soft actuators compared to traditional approaches.
[109] integrated Pythagorean Hodograph (PH) curves with an Extensive validation of CRT models is essential for ensur-
EBRT framework to reconstruct actuator shapes from virtual ing their predictive accuracy. Cable-driven soft robots were
control points, establishing a link between control inputs and widely studied and experimentally validated. For example,
geometry. Both approaches, as well as more recent formu- [112]validatedastaticCosseratmodelofatendon-drivensoft
lations [81], were validated through FEM and experimental arm using FEM simulations and experimental comparisons.
results,confirmingtheiraccuracy.Inparallel,[110]developed The dynamic extension of this model [47] was experimen-
a high-fidelity lumped-parameter dynamic model for cable- tally verified by replicating characteristic octopus movements.
driven continuum robots, based on the principle of virtual Later, [50] demonstrated the effectiveness of their unified
power. It captured curvature variations while accounting for dynamic framework using an underwater robotic system. Fur-
inertial, actuation, friction, elastic, and gravitational effects. ther validation of discretization-based approaches was per-
formed in [55] and [49], confirming the numerical robustness
of their methods. Conversely, [116] investigated deflection
B. All Deformations
and stiffness in robots subject to constant axial tendon dis-
Assoftroboticsadvanced,theresearchcommunityexplored placement and environmental loads, comparing parallel and
the use of continuum and soft robots in unstructured environ- converging actuator paths. They validated the Cosserat rod
ments. In this context, the CRT emerged as a fundamental model on a CSM subject to tip loads in the 0 − 0.05 kg
frameworkformodelingtheirdeformation.Indeed,interaction range, providing actuations to reach bending angles up to
withirregularlyshapedobjectsmakessheareffectssignificant, 60◦.Thesimulationresultsalignedwellwiththeexperimental
whileadvancesinactuationtechnologiesrequirethemodeling data. However, as the authors noted, limitations emerged for
ofstretchingandtorsionaldeformations.Arecentcontribution larger curvatures due to the increased role of friction, which
by[111]furtherconsolidatesCRTasastandardframeworkfor was not included in the model. For pneumatic soft robots,
continuum robots. The authors rigorously derived equivalent [117], [118] developed geometrically exact CRT models and
Newtonian and Lagrangian formulations for multi-segment validated them on fiber-reinforced pneumatic manipulators,
tendon-driven robots, providing practical guidelines for nu- achieving significantly higher accuracy than constant curva-
merical implementation. ture models. The screw-theoretic PCS formulation [113] was
As discussed in Sec. IV, the CRT describes the motion of validated on the STIFF-FLOP arm, while [119] tested their
an elastic rod with an infinite DoFs. Discretization techniques pneumatic Cosserat rod model experimentally, reporting an
playakeyroleinnumericallysolvingthegoverningequations 8.7%L tip position error. Also, FEM was extensively used
of Cosserat rods. Several methods were developed to enhance to compare and validate CRT models. Indeed, [120] derived

11
analytical solutions for quasi-static Cosserat rods and verified as in concentric tube robots (CTRs) for minimally invasive
them against FEM simulations under external loads. Simi- surgery (MIS) [130]–[132] and eccentric tube robots (ETRs)
larly, [121] conducted a comparative study between FEM and for multi-arm sheaths [133]–[135]. Safety-critical domains
CRT models for pneumatic actuators, proposing a parameter also utilize bending-twisting compliance analysis to predict
identification process. Further refinement was made by [122], deformations under external loads [136].
who obtained a static Cosserat model from detailed FEM Twisting deformations are usually induced by particular ca-
simulations, validating it experimentally across various load- bleortendonrouting.Tendon-drivencontinuumrobotsemploy
ing conditions. For PCMs, [123] investigated elastic stability non-straight tendon paths that wrap around the backbone to
using Cosserat rod models and experimentally validated their generate both bending and twisting. Early work by Rucker et
stabilityconditions.Inparallel,[124]introducedakinetostatic al. [137] established Cosserat rod formulations where curved
CRT framework for PCMs, achieving high accuracy in force tendon paths produce distributed loads along the backbone.
sensingandmanipulabilityanalysis.Then,[125]extendedthis Similarly, [138] developed a CSM with three tendons spi-
approach, developing a comprehensive CRT-based framework raling around a nitinol backbone, extending their previous
for tendon-driven PCMs, experimentally achieving a median untwisted setup [139]. They further refined this approach
pose accuracy of 3.4%L. for real-time control using a stable moment-based algorithm
Cosseratrodmodelsfoundwidespreadapplicationsinbioin- [140]. Twisting was also demonstrated in robotic tails [141],
spired robotics and biomechanical studies. [126] proposed a octopus-inspired manipulators [142], [143], tendon-actuated
unifiedframeworkformodelingthelocomotionofbioinspired extensiblerobots[144],andmulti-sectiontendonrobots[145].
robots with soft appendages. They analyzed flapping flight In fluidic actuation, torsional effects are less common but can
and passive swimming, comparing two different modeling be induced through asymmetric or fiber-reinforced chambers.
approaches based on Newton-Euler dynamics. Similarly, [51] For example, Uppalapati et al. [146] modeled a CSM with
implemented Cosserat rod simulations in PyElastica [65], as- two asymmetric pneumatic actuators capable of bending and
semblingheterogeneousstructurestoreplicatemusculoskeletal rotating,whichwerelaterextendedwithanadditionalrotating
architectures (e.g., snakes, bird wings). Their work demon- actuator [147]. Other approaches include models based on
strated the effectiveness of CRT in bioengineering design, Euler-Bernoulli for micro-tube pneumatics [148] and gener-
simulating complex musculoskeletal interactions in biological alized PneuNet structures, combining bending and twisting
androboticapplications.Then,[127]exploredtheintersection predictions validated against FEM [149].
of CRT and optimal control theory, revealing fundamental Cosserat rods were extensively applied to tendon-driven
insights into the singularity of dynamic continuum robot sim- systems, while Euler-Bernoulli or energy-based methods are
ulations.Byreformulatingtheproblemasaminimizationtask, often preferred for pneumatic networks due to their simpler
their approach provided a novel perspective on the statics and kinematics. Examples include asymmetric pneumatic actua-
dynamics of continuum robots, validated through simulations tors capable of torsion [146], [147], micro-tube pneumatics
of bioinspired continuum swimmers. modeled with multi-segment Euler-Bernoulli rods [148], and
Finally, to find optimal bases for the GVS approach, [128] PneuNet actuators modeled analytically with energy mini-
introduced a data-driven reduction method based on Proper mization [149]. These models capture how chamber geom-
Orthogonal Decomposition (POD). Their approach begins by etry, reinforcement, and pressurization induce coupled bend-
creating a high-fidelity GVS digital twin from experimental ing and twisting modes. However, the majority of bending-
data, which is then simulated to generate a comprehensive twisting continuum robots are tendon-driven, concentric-tube,
dataset of strains. By applying Singular Value Decomposition or eccentric-tube systems. These architectures require a geo-
(SVD)tothisdataandtruncatingtheleastsignificantsingular metrically exact description of distributed loads and torsional
values,themodel’sdimensionalityisreducedwhilepreserving effects, which is naturally expressed through the CRT.
its accuracy. This process yields an optimal linear basis of the Concerning CTRs, [150] adapted the piecewise variable-
form B (s). A subsequent study extended the search to strain [57] to simulate multi-section CTRs by including the
bmq
thenonlinearcase(i.e.,B (q,s)),employingautoencodersto tubes’ sliding motion. Rotation motions of the tubes are
q
identify a more expressive and compact representation [129]. includedasgeneralizedcoordinatesratherthanboundarykine-
matic conditions. Notably, this procedure led to a minimal set
ofclosed-formalgebraicequationssolvableforboththeshape
C. Bend & Twist
variables, the actuation forces, and the torques. The resulting
Bending and twisting are fundamental deformation modes equations also facilitate control, design optimization, and sta-
thatenableCSMstoachievecomplex3Dshapesanddexterous bility assessment. Unlike beam simplifications, Cosserat rods
movements. Modeling these modes is particularly important account for coupling between bending and torsion and handle
in applications where interaction with the environment is not spatially varying loads from tendon paths, external wrenches,
limited to planar motions but requires full spatial maneu- and contact. This explains why most bending-twisting works
verability. In many cases, incorporating twisting alongside intheliteratureadopttheCosseratrodformalism[133]–[135],
bending provides the best trade-off between accuracy and [137], [138], [140]–[145].
computational efficiency. This allows continuum robots to Buckling: Buckling instability is another important non-
follow arbitrary curves in space, which is essential for tasks linear phenomenon to consider. When modeling thermally
such as wrapping around an object, executing dexterous ma- activated twisted and coiled polymer (TCP) muscles, [151]
neuvers, or navigating constrained environments. Biomedical employed KRT, since the small-strain assumptions and direct
applications especially benefit from bending-twisting modes, link to coil load-twist relations simplify the actuation model.

12
TABLEII
OVERVIEWOFROD-BASEDMODELSOFCONTINUUMANDSOFTROBOTS.
| DeformationClass |     | Subclass | Ref. Contribution                                  |     |     |     |     | RodModel |
| ---------------- | --- | -------- | -------------------------------------------------- | --- | --- | --- | --- | -------- |
|                  |     |          | [88] Staticmodelforreal-timeshapeestimationofCSMs. |     |     |     |     | CRT      |
Cable [99] Dynamicmodelofacontinuumfingerforplanargrasping. CRT
|     |     |     | [82] ModelofnotchedcontinuummanipulatorforMIS. |     |     |     |     | CRT |
| --- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- |
[108] Derivationofconstitutivelawofaplanarbendingactuator. EBRT
Bend Pneumatic [80] ROMandrodmodelswithabsoluteandrelativestatesvalidatedonSTIFF-FLOP. EBRT
[86] Dynamicmodelinspiredbycaterpillarmotiontoanalyseondulationmechanics. EBRT
Smart
[93] ModelingthecouplingbetweenCSMbodyandthermalactuation. CRT
|     |     | Parallel | [75] ShapemodelingofaPCMmadeofsoftpanels. |     |     |     |     | EBRT |
| --- | --- | -------- | ----------------------------------------- | --- | --- | --- | --- | ---- |
Tubular [155] EstimationofstiffnessvariationonamonolithictubeforMIS. CRT
[137] Derivedexactmodelsfortheforwardkinematics,statics,anddynamicsofCSMswithgeneraltendonrouting.
|     |     | Cable | [47] Studiedthedynamicinteractionofanoctopus-inspiredCSMwithadensemedium. |     |     |     |     |     |
| --- | --- | ----- | ------------------------------------------------------------------------- | --- | --- | --- | --- | --- |
[116] PredicteddeflectionandstiffnessinCSMssubjecttoconstantactuationandexternalloads.
AllDeformations Pneumatic [118] ModelvalidationofCSMwithfiber-reinforcedactuatorsvaryingbaseorientation. CRT
[123] StudiedandexperimentallyvalidatedtheelasticstabilityofPCMs.
|     |     | Parallel | [114] Modeledclosed-chainsoftPCMswithvalidationonasoft-rigidfinger. |     |     |     |     |     |
| --- | --- | -------- | ------------------------------------------------------------------- | --- | --- | --- | --- | --- |
[125] Studiedreachability,singularities,manipulability,andcomplianceofPCMs.
[51] Simulatesmusculoskeletalsystemsassemblingheterogeneousactive/passiverods.
Bioinspired
[127] StudiedthelinkbetweenCRTandoptimalcontrolsimulatinglocomotorsandswimmers.
Cable [145] Tutorialonthedynamicmodelingoftendon-drivencontinuumrobotsthatbendandtwist. CRT
Pneumatic [147] DesignandmodelingofaCSMwithparallelasymmetricfiber-reinforcedelastomers. CRT
Bend&Twist [132] DynamicmodelofCTRsvalidatedfortissuegraspingandsnapping. CRT
Tubular [135] ModelingofasuperelasticETRsheathforbiomedicalprocedures. CRT
[150] AdaptedthepiecewisevariablestraintoCTRsincludingthetubes’slidingmotion. CRT
Smart [151] TCPsmusclesincorporatingcoilloadandtwistintoactuationmodel. KRT
Buckling [154] Studyrelationshipbetweenbucklingandκonsimulatedcantileverrods. CRT
[102] Addressedstiffnessregulationforasoftarmwithaslidingbackbone,achieving+57.7%stiffness. CRT
Cable [156] AugmentsthePCCwitharodmodeltoquicklysolvetheCSMdeformationunderFe. EBRT
[157] UtilizestheRitz-Galerkinmethodtoreducethecontinuousstatespaceofrodmodels. CRT
Bend&Stretch [158] ExperimentallyvalidatedofaCSMmodelonbendingmotionsgeneratedbysquarepulseactuations. CRT
Pneumatic [159] Characterizedbending,naturalfrequency,anddampingofacantileveredextensileartificialmuscle. EBRT
[160] Ablationstudyofmodeladdressingmanufacturinguncertaintiesina3D-printedCSM. CRT
[161] DesignandmodelingofahybridCSMincorporatinganantagonisticcompliantmechanism. EBRT
Smart [162] Simulatedlocomotionofacaterpillar-inspiredsoftrobotactuatedbySMAs. CRT
Rod-driven [79] Design,staticsmodeling,andnumericalworkspaceanalysisofanextensiblerod-drivenPCM. CRT
[163] Simulatedthecoupledtendondriveformulti-sectionCSMshighlightingtheroleoftwist.
[164] ComparedtheKelvinviscoelasticmaterialmodelvsapurelyelasticmodelonarealsiliconicarm.
Cable [165] CombinedFEMtomodeltherobotbodywithCRTtomodelactuation. CRT
Bend&Twist&Stretch
[90] Investigatedpneumaticstiffnessregulationonacable-drivenCSMusingthehyperelasticmaterialmodel.
Tubular [166] ReconstructedtheshapeofacontinuumendoscopegivenexternalforcesexertedonthedistalendFe(L). CRT
Parallel [167] Modeledasix-linkPCMstartingfromanexperimentalvalidationofasingleelasticrod. CRT
|     |     | Tubular | [168] Experimentallyvalidatesamodelformulti-backbonecontinuumrobot. |     |     |     |     |     |
| --- | --- | ------- | ------------------------------------------------------------------- | --- | --- | --- | --- | --- |
Bend&Stretch&Shear Pneumatic [169] ModelsasoftpneumaticactuatorcombiningrodsandANNs CRT
|                  |     | —   | [170] ProposedanovelFEM-inspireddiscretizationtechniqueandtheSimSoftsimulator. |     |     |     |     |     |
| ---------------- | --- | --- | ------------------------------------------------------------------------------ | --- | --- | --- | --- | --- |
| Bend&Twist&Shear |     |     |                                                                                |     |     |     |     | CRT |
Tubular [171] Proposedaforcemodelandassociatedcostmetricforsaferandclinicallyrelevantformotionplanning.
Stretch&Shear Bioinspired [172] StudiedtheperistalticlocomotionoftheearthwormLumbricusterrestristomodelsoftrobots. CRT
Stretch Bioinspired [173] Studiedtheperistalticlocomotionofacaterpillar-inspiredsoftrobot. CRT
Similarly, Kirchhoff rods were used in micrometer-scale par- environments [130], [135].
| allel continuum | robots | [152] | and bacteria-inspired | flagel- |     |     |     |     |
| --------------- | ------ | ----- | --------------------- | ------- | --- | --- | --- | --- |
latedswimmersexploitingbucklinginstabilitiesforpropulsion D. Bend & Stretch
| [153]. Conversely, |     | Cosserat | rods were applied | to study global |     |     |     |     |
| ------------------ | --- | -------- | ----------------- | --------------- | --- | --- | --- | --- |
Simultaneousbendingandstretchingbehaviorsarefrequent
| buckling | in soft robotic | arms | [154], where | large deflections |     |     |     |     |
| -------- | --------------- | ---- | ------------ | ----------------- | --- | --- | --- | --- |
inCSMsactuatedbycablesorpneumatics(Figure4).Notably,
and intrinsic curvature control are essential. Thus, Kirchhoff this category excludes twist and shear effects for several
| rods often | appear | in actuation-centric | or  | microscale studies |     |     |     |     |
| ---------- | ------ | -------------------- | --- | ------------------ | --- | --- | --- | --- |
reasons:theactuatorsarelinearandapplyforcesalongthecen-
| where analytical | tractability |     | is crucial, while | Cosserat rods |                         |           |                    |              |
| ---------------- | ------------ | --- | ----------------- | ------------- | ----------------------- | --------- | ------------------ | ------------ |
|                  |              |     |                   |               | terline, not generating | torsional | or shear stresses; | interactions |
dominate in large-deformation, shape-control analyses. with the environment are either neglected or primarily induce
Workspace analysis: Finally, workspace analysis requires axialandbendingloads.Asaresult,thedeformationbehavior
accurate models of bending and twisting under actuation and can be described in terms of bending and axial stretching. We
loading. Tendon-driven Cosserat models enable forward kine- summarize several Bend & Stretch works in Table II. Herein,
| matics and | Jacobian-based |     | control for workspace | prediction |     |     |     |     |
| ---------- | -------------- | --- | --------------------- | ---------- | --- | --- | --- | --- |
wefocusthediscussiononmanufacturingvariability,stiffness
[140]. For pneumatic robots, static workspace matching was regulation, and fiber-reinforced actuators.
validated experimentally with asymmetric actuators modeled Manufacturing variabilities: Manufacturing variability, as
by Cosserat rods [146], [147]. PneuNet and micro-tube ac- well as material degradation, are critical concerns in soft
tuator models [148], [149] allow for workspace design and robotic systems, as they can significantly affect actuator be-
optimizationbylinkingactuatorgeometryandpressureinputs havior, model accuracy, and control performance. Variations
to achievable curves. In biomedical contexts, concentric and in geometry, material stiffness, or the positioning of actuators
eccentric tube models predict reachable poses in confined during fabrication can cause substantial differences between

13
the modeled behavior and the robot’s actual motion. While the total length. Simulation studies demonstrate that inserting
several experimentally validated rod models were developed the nitinol backbone can enhance the kinematic workspace
for pneumatic soft arms [157], [158], [174]–[177] and fingers and increase stiffness by 57%. Two manipulation case studies
[178], [179], relatively few have focused specifically on the demonstrated the potential application of hybrid actuation for
effects of manufacturing irregularities. Below, we discuss two stiffness regulation. Another compliant rod-driven mechanism
works using Cosserat rod models to address manufacturing enablingstiffnessregulationwasintroducedinasoftarmwith
uncertainties in pneumatic soft robots. Eugster et al. [180] pneumatic actuation [161]. While an Euler-Bernoulli model
described the kinematics of a soft arm using a nonlinear was adapted to demonstrate the benefit of the mechanism in
pressure-dependent constitutive law, the principle of virtual experiments of way-point tracking, the investigation of the
work, and modeled the actuator with strain energy functions. stiffening behavior remains future work.
Manufacturing imperfections are considered by scaling the Fiber-reinforced actuators: Fiber-reinforced soft pneu-
relationsofextensionalandbendingstiffnessandbyaconstant maticactuatorspresentsignificantmodelingchallengesdueto
shift of the actuator position d (s). Assuming the pressure nonlineardeformationunderpressure.Severalworksleveraged
i
dilates the chambers, the model also considers cross-section variationsofrodtheoriestomoreaccuratelycapturetheircom-
deformations with a pressure-dependent diameter D(p). The plexbending,elongation,andcross-sectionalbehaviors.Sadati
model is validated experimentally for static stretching and et al. [157], [174], [175] performed comprehensive investi-
bending motions, in vertical and horizontal mountings, com- gations of several modeling approaches—experimentally val-
paringconstantorpressure-dependentchamberradius,withor idated on the well-known STIFF-FLOP arm—addressing the
withoutchamberrepositioning,andalinearorOgdenmaterial challenge of cross-section deformation, captured analytically
law. Similarly, Alessi et al. [160] presented a dynamic model through geometry deformation and CRT. This approach out-
for a 3D-printed CSM with actuators that exhibited different performedconstantcurvatureapproachesby13%andvariable
stretching when subject to equal actuation. They captured curvature by 7%. More recently, [182] introduced a Cosserat
this effect by tuning the pressure-strain relation ϵ(p) for each rodmodeltodeepentheunderstandingofthepressure-induced
actuator introducing strain gains γ(i) that tune the pressure- deformation of a fiber-reinforced soft pneumatic actuator with
strain relation ϵ(p) for each actuator three DoFs. Specifically, they considered the compression
effects of lateral pneumatic chamber walls by converting
p(i)A(i)
the inner chamber pressure into an equivalent force. Their
ϵ(p(i))=γ(i) in , (41)
EA model, validated against FEM simulations, obtained a mean
where A is the interior actuator area. An ablation study tip position error up to 11%. Conversely, [183] accounted for
in
conducted on dynamic motions investigated the contribution the effect of radial pressure by proposing an inhomogeneous
of different model components, uncovering that neglecting Cosserat rod model with a nonlinear strain-force relationship.
manufacturing uncertainties can indeed degrade performance The proposed method outperformed the standard CRT by
upto5%L.Inpractice,manufacturingirregularitiescanaffect about 15%. Meanwhile, [184] explored the effects of self-
every soft robotic system but remain unexplored outside the gravity and external loads on the configuration of an actuator
Bend & Stretch class. We attribute this to the fact that, for with a semicircular cross-section through an EBRT.
linear actuators, it is easier to quantify the expected motion
and thus identify model discrepancies.
E. Bend & Twist & Stretch
Stiffness regulation: Stiffness modeling and regulation are
central to advancing the adaptability and precision of soft A few works explored the combination of bending, twist-
robotic systems. However, in many designs, limitations such ing, and stretching, especially in cable-driven systems. [163]
as single-mode actuation, the absence of antagonistic mech- presented a general geometrically exact static CRT for cable-
anisms, or the lack of a structural backbone can restrict the driven CSMs. The work enabled the simulation of coupled
abilitytomodulatestiffnesseffectively.Toaddressthesechal- tendon drives for multiple sections through various design
lenges, Sun et al. [181] presented a novel design of a hybrid parameters and highlighted the role of torsional deformation.
continuum robot whose actuators combine pneumatic muscles Although the study was conducted only in simulation, it
withembeddedelasticrods.Therobotcanregulateitsstiffness provided a solid foundation for future full dynamic analyses
through a locking mechanism, switching between large-scale (Sec. VI-B). Similarly, [164] modeled a cable-driven conic
movementenabledbypneumaticsandfinepositioningenabled CSM made of silicone by combining a geometrically exact
bypush-pulloftherods.Stiffnesstestsrevealedthattherobot dynamic Cosserat rod with the Kelvin viscoelastic material
increasesitsstructuralstiffnessby65%duringfinepositioning model. Experimental validation with real-world data included
(locked mode) and reduces the repetitive positioning error by tests with the arm fixed in a cantilever configuration under
62%. To model this behavior, they improved a static KRT gravity, without actuation (τ = 0) or executing 2D and
calculating the elastic deformation through the minimal total 3D motions through different cable actuation combinations
potential energy principle in an optimal control framework. (τ ̸= 0). The authors found that the Kelvin model matched
Similarly, [102] addressed stiffness regulation for a tendon- the experimental data better than a purely elastic model.
drivensoftCTRwithanitinoltubebackbone,whichcanslide Also,[165]describedthedynamicsofcable-drivensoftrobots
insidethesoftbodyforposeorstiffnessregulation.ACosserat by combining FEM for modeling the robot structure with a
rod model was validated in several scenarios by varying the discrete Cosserat rod representation for the actuation system.
joint-space tendon inputs and the task-space external contact The differential equations were integrated using an implicit
force, achieving an average tip position error below 1% of backward Euler time-stepping scheme to ensure numerical

14
stability, while both direct and inverse simulations demon-
strated the suitability of the approach for robots actuated by
cables or rods. Recently, Roshanfar et al. [90] investigated
stiffness regulation in a cable-driven CSM equipped with
a central linear pneumatic chamber. The authors captured
both robot motion and pressure-induced stiffening behavior
by augmenting the classical Cosserat rod formulation with a
Fig.5. GeneralblockdiagramoftheMBcontrolarchitecture.
hyperelastic material model.
In conclusion, while the Bend & Twist & Stretch class
comprisesfewerworksthanthefourmaindeformationclasses, It describes normal and frictional forces along the shaft as
it has consistently contributed to the modeling of cable-driven a function of the planned needle path, the friction model
systems.Thisclassmayberegardedasaparticularcaseofthe with its parameters, and the piercing force. The proposed
All Deformation category, in which shear strains are assumed force model and associated cost metric are safer and more
negligible and therefore omitted. Additional works belonging clinically relevant for motion planning. They fit and validate
to this class are reported in Table II. the model through physical needle robot experiments in a gel
phantom. The force model defines a cost function for motion
F. Bend & Stretch & Shear planning,andwasevaluatedagainstapath-lengthcostfunction
in random environments, reducing the peak force by 62%.
The Bend & Stretch & Shear deformation class, similar to
the previous class, emerges by neglecting torsion. Chen et al.
[168] proposed a variable curvature static-kinematic Cosserat H. Axial Deformations
rodmodelformulti-backbonecontinuumrobots,incorporating
Axialdeformations(stretchingandshearing)arecommonin
multi-backbone structural constraints. The model is validated
peristaltic locomotion, where waves of contraction, extension,
on a robot with two multi-backbone continuum segments,
and shear generate propulsion along the robot body.
each with four nitinol rods. A push-pull actuation bends the
Stretch&Shear:Theperistalticlocomotionofearthworms
continuum robot and transmits shear forces. The experiments
was studied with a continuous model of compressible and
evaluate the tip positioning accuracy for circular trajectories
incompressible slender bodies represented as Cosserat rods
and the shape discrepancy when the robot is subject to an
[172]. Incompressibility is enforced as an internal constraint
end-point load in two configurations. They also implement
using Green and Naghdi’s theory of a directed rod. Two
an inverse kinematics in a real-time open-loop controller for
linearly elastic isotropic material models are assumed, with
tracking a rectangular path, with and without tip load. The
material parameters identified experimentally for small defor-
proposed model outperforms the PCC. Note that the torsion-
mations. Motion effects from actuators or muscle contraction
free assumption did not hold in all experiments. Indeed, when
are modeled as external compressive loads using a doublet
out-of-plane external forces were applied to cause torsion, the
function for an assigned centerline force and a uniform pres-
tip position error raised to 19% of the length. Differently,
sure for a pair of assigned director forces. The method is
[169] developed a hybrid model combining the classical CRT
showcased in simulation on a soft robotic device.
with a data-driven stiffness estimation. Rather than solving
Stretch: In a bioinspired robotics application, [173] mod-
numerically nonlinear constitutive equations, the model relies
eled a caterpillar soft robot using a network of linear and
on a work point-dependent linear stress-strain relationship for
torsional springs connected by massless rods represented as
computational efficiency. Experimental validation is carried
planar discrete elastic rods [162].
out by identifying the stretching and bending stiffness of a
soft pneumatic actuator and learning the actuation to stiffness
maps using ANNs. VII. MODEL-BASEDCONTROLLERSFORRODMODELS
Controlling continuum and soft robots can be challenging
G. Bend & Twist & Shear due to material nonlinearities (e.g., hysteresis), the infinite-
dimensional configuration space, and under-actuation. These
Another special case is when robots bend, twist, and shear,
propertiesmaketheimplementationofwell-knowncontrollers
without stretching. Grazioso et al. [170] proposed a FEM-
for rigid manipulators difficult or impossible. The control
inspired spatial discretization technique where the rod is
literature for rigid robots primarily focuses on controlling
dividedintoseveralnodes,definingahelicoidalshapefunction
the end-effector in terms of pose, velocity, or force. For
for the interpolation. Thanks to the specific choice of the
continuum robots, the natural equivalent task is tip control.
shape function, they formulated the Cosserat rod dynamics
To enable continuum and soft robots to achieve capabilities
with Lie Groups. The proposed method was implemented in
beyond those of rigid robots, researchers have proposed two
a new simulator called SimSOFT and validated on the pure
additional control tasks:
bendingofacantileversoftarmandthepurein-planerotation
of a soft arm with varying external conditions. In addition, • Multi-Point (MP) control, which regulates the pose of a
they experimentally validated the coupling between bending, set of cross-sections,
torsion, and shear on the Princeton arm benchmark, achieving • Shape control, which regulates the robot backbone, fully
excellent accuracy and computational efficiency. Shifting to utilizing the potential of continuum structures.
clinical applications, Bentley et al. [171] derived a tissue The model-based (MB) control strategy involves leveraging
and needle force model with a Cosserat string formulation. prior knowledge of the robot to guide it toward achieving

15
a specific task. The motivation behind developing MB con- A valid change of coordinates h(q) can be expressed as
trollers is the possibility of mathematically guaranteeing the (cid:20) (cid:21) (cid:20) (cid:21)
|     |     |     |     |     |     |     |     |     | g(q) |     | 0   |     | 0   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
stability and performance of the controlled system. However, h(q)= + na×na na×n−na q, (44)
|     |     |     |     |     |     |     |     |     | 0   |     | 0   |     | I   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
implementing controllers in physical prototypes can be chal- n−na n−na×na n−na
|     |     |     |     |     |     |     |     |     | Rn  | Rna |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
lenging, often requiring an extensive identification procedure. where g : → is the coordinate transformation in
Inthiscontext,thespatialdiscretizationtechniqueiscrucialto the actuated coordinates θ . For continuum robots modeled
a
balance accuracy and computational efficiency. Therefore, the with Cosserat rod theory (CRT), g(q) has a clear physical
model selection and the discretization technique are integral interpretation. The actuated coordinates correspond to the
parts of the control design process. lengths of the individual actuators, such as
| Formalization: | To  | formalize | the | control | problem, | let us |     |     |    |    |     |     |     |     |     |
| -------------- | --- | --------- | --- | ------- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
L
|     | q ∈ R n |     |     |     |     |     |     |     | a , 1 |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
c o n s i d e r a g en e ric c o n fi g ura t io n v e c tor , wh a t e v er L (cid:32) (cid:90) (cid:18) (cid:20) (cid:21)(cid:19) (cid:33)na
|     |     |     |     |     |     |     |     |     |  a , 2 |    | L   |     | 0   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
d is c r e t iz at ion a lg ori th m i s us e d . T o f o rm a li z e t he c o n t ro l g(q)=  = B⊤ ξ+ ds , (45)
|                   |                 |                |        |            |               |     |     |     |  . . |    |     | τ,i | d′  |     |     |
| ----------------- | --------------- | -------------- | ------ | ---------- | ------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
| problem,          | let us consider |                | q ∈ Rn | a generic  | configuration |     |     |     | .     |     |     |     | i   |     |     |
|                   |                 |                |        |            |               |     |     |     |      |    | 0   |     |     | i=1 |     |
| vector, admitting | any             | discretization |        | algorithm. | According     |     | to  |     | L     |     |     |     |     |     |     |
a,na
| [11], the     | shape control  | problem | can      | be particularized |            | in two   |       |        |     |               |            |      |                |           |     |
| ------------- | -------------- | ------- | -------- | ----------------- | ---------- | -------- | ----- | ------ | --- | ------------- | ---------- | ---- | -------------- | --------- | --- |
|               |                |         |          |                   |            |          | where | L      | ∈R  | denotes       | the length | of   | the i-th       | actuator. |     |
| sub-problems: | (i) regulation |         | and (ii) | trajectory        | tracking   | (TT).    |       | a,i    |     |               |            |      |                |           |     |
|               |                |         |          |                   |            |          | The   | change |     | of coordinate |            | (45) | is significant | because   | it  |
| In the TT     | case, the      | goal of | shape    | control           | is to find | an input |       |        |     |               |            |      |                |           |     |
associatesasubsetofthegeneralizedcoordinateswithaphys-
| τ(t) such | that |     |     |     |     |     |        |            |     |          |      |     |           |          |        |
| --------- | ---- | --- | --- | --- | --- | --- | ------ | ---------- | --- | -------- | ---- | --- | --------- | -------- | ------ |
|           |      |     |     |     |     |     | ically | meaningful |     | quantity | that | can | be easily | measured | [185]. |
(cid:20) (cid:21) (cid:20) (cid:21) For example, for a tendon-driven continuum soft manipulator
|     |     | q(t) | q   | d e s (t) |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ---- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
l im = , (42) (CSM), the actuated variables θ can be directly obtained
|     | t → | ∞ q˙(t) | q˙  | (t) |     |     |     |     |     |     |     | a   |     |     |     |
| --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
d e s
|     |     |     |     |     |     |     | using | encoders. |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- |
where q , q˙ ∈ Rn are the desired configuration and In these collocated coordinates, the equations of motion
|     | des des |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
its time derivative, respectively. The condition (42) can be (EoMs) take the partially decoupled form, such as
q˙
particularized in the regulation case, imposing des = 0. (cid:20) (cid:21)
|     |     |     |     |     |     |     |     | θ¨+C |     | θ˙+G |     |     | θ˙ I |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- | --- | ---- | --- | --- |
Similarly to rigid robots, it is possible to formalize the tip M +K θ+D = na τ, (46)
|                  |           |          |             |       |        |         |       | θ   | θ       |           | θ       | θ   | θ                 | 0         |     |
| ---------------- | --------- | -------- | ----------- | ----- | ------ | ------- | ----- | --- | ------- | --------- | ------- | --- | ----------------- | --------- | --- |
| control problem, | rewriting |          | (42) in the | task  | space, | such as |       |     |         |           |         |     |                   |           |     |
|                  |           |          |             |       |        |         | where | M   | θ , C θ | , G θ , K | θ , and | D θ | are the inertial, | Coriolis, |     |
|                  | lim       | g(L,t)=g |             | (L,t) |        |         |       |     |         |           |         |     |                   |           |     |
des gravitational, stiffness, and damping matrices, respectively,
|     | t→∞ |          |     |       | ,   | (43) |           |     |        |            |             |     |     |     |     |
| --- | --- | -------- | --- | ----- | --- | ---- | --------- | --- | ------ | ---------- | ----------- | --- | --- | --- | --- |
|     |     |          |     |       |     |      | expressed |     | in the | collocated | coordinates |     | θ.  |     |     |
|     | lim | η(L,t)=η | des | (L,t) |     |      |           |     |        |            |             |     |     |     |     |
t→∞ Adopting this change of coordinates is promising for facil-
where g (L,t) ∈ SE(3) and η (L,t) ∈ R6 are the itating the transfer of control methods developed for under-
|              | des          |     |          | des      |            |         |             |     |                |     |                  |     |                    |         |         |
| ------------ | ------------ | --- | -------- | -------- | ---------- | ------- | ----------- | --- | -------------- | --- | ---------------- | --- | ------------------ | ------- | ------- |
|              |              |     |          |          |            |         | actuated    |     | rigid systems. |     | For instance,    |     | [185] demonstrates |         | the     |
| desired pose | and velocity |     | twist of | the tip. | Similarly, | the tip |             |     |                |     |                  |     |                    |         |         |
|              |              |     |          |          |            |         | application |     | of classical   |     | controllers—such |     | as                 | PD with | gravity |
poseregulationconditioncanbeobtained,particularizing(43)
with η (L,t) = 0. Lastly, the MP control problem can be andelasticitycompensation[186],[187]anditsvariantP-satI-
des
|            |               |       |           |        |         |           | D   | [188],         | a PID | controller | with     | integral | saturation—directly |     |      |
| ---------- | ------------- | ----- | --------- | ------ | ------- | --------- | --- | -------------- | ----- | ---------- | -------- | -------- | ------------------- | --- | ---- |
| formalized | by extending  | (43)  | in a      | set of | desired | poses and |     |                |       |            |          |          |                     |     |      |
|            |               |       |           |        |         |           | to  | the collocated |       | variables. | Finally, |          | this formulation    | not | only |
| velocity   | twists of the | cross | sections. |        |         |           |     |                |       |            |          |          |                     |     |      |
To address these control problems, the MB control frame- enhances the understanding of the system dynamics and sim-
|     |     |     |     |     |     |     | plifies | control | design, |     | but also | enables | the | design of | linear |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | ------- | --- | -------- | ------- | --- | --------- | ------ |
workcanberepresentedthroughthegeneralschemeshownin
|           |           |           |        |        |         |         | controllers |     | in the | collocated |     | coordinates | without | approxima- |     |
| --------- | --------- | --------- | ------ | ------ | ------- | ------- | ----------- | --- | ------ | ---------- | --- | ----------- | ------- | ---------- | --- |
| Figure 5. | The block | “Sensors” | refers | to the | sensors | mounted |             |     |        |            |     |             |         |            |     |
on the robotic platform, mapping q, q˙ in the measurements tions. Notably, the control laws remain nonlinear due to the
| Rp.                     |                 |             |                  |           |     |            | inherent | nonlinearity |     | of  | the mapping |     | g(q). |     |     |
| ----------------------- | --------------- | ----------- | ---------------- | --------- | --- | ---------- | -------- | ------------ | --- | --- | ----------- | --- | ----- | --- | --- |
| y ∈                     | The “Estimator” |             | block implements |           | the | Shape Es-  |          |              |     |     |             |     |       |     |     |
| timation/Reconstruction |                 | algorithms, |                  | providing | an  | estimation |          |              |     |     |             |     |       |     |     |
of q, q˙, defined as qˆ, qˆ˙ ∈ Rn. Finally, the MB controller B. Control by Model Inversion
block computes the input τ, processing the error between The most direct approach to controlling a continuum robot
the estimated configuration and the desired one. Following is through its kinematic model. This strategy, known as In-
| this general | scheme, | many | works | on MB | control | occurred, |     |     |     |     |     |     |     |     |     |
| ------------ | ------- | ---- | ----- | ----- | ------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
verseKinematics(IK),computestheactuationinputsrequired
thanks to the development of accurate and computationally to drive the robot’s tip to a desired pose. Early studies
efficientrodmodels.Below,wereviewthecontributions,while demonstratedeffectiveplanartrajectorytrackingandvibration
| Table III     | reports the | key points. |     |     |     |     |             |               |        |            |        |               |               |                 |          |
| ------------- | ----------- | ----------- | --- | --- | --- | --- | ----------- | ------------- | ------ | ---------- | ------ | ------------- | ------------- | --------------- | -------- |
|               |             |             |     |     |     |     | suppression |               | using  | simplified |        | models        | such as       | Euler-Bernoulli |          |
|               |             |             |     |     |     |     | rod         | theory        | (EBRT) | [189],     | [190]. | To            | better handle | real            | hard-    |
|               |             |             |     |     |     |     | ware        | complexities, |        | these      | models | were          | extended      | with            | online   |
| A. Collocated | Form        |             |     |     |     |     |             |               |        |            |        |               |               |                 |          |
|               |             |             |     |     |     |     | observers,  |               | which  | compensate |        | for phenomena |               | such as         | variable |
To address the underactuated nature of continuum robots, a stiffness caused by changes in inflation pressure [189].
recent method proposed by [185] reformulates the dynamic Toachievehigheraccuracyandaddresscomplexspatialde-
model (14) in a collocated form. This approach decouples formations, recent work shifted towards the more comprehen-
the actuated variables from the passive ones via a change of sive CRT, enabling advanced capabilities such as micrometer-
coordinates, θ = h(q). The resulting state vector θ ∈ Rn is levelpositioninginparallelcontinuumrobots[152]andmulti-
partitioned into actuated coordinates, θ ∈ Rna, and passive point orientation control along a manipulator’s body [191].
a
∈Rn−na.
coordinates, θ u Since the accuracy of CRT may increase the computational

16
cost, limiting real-time use, researchers considered quasi- andexternaldisturbances.AdaptivevariantsofSMCwerede-
static formulations and actuator nonlinearity compensation velopedtohandlelimitationssuchasactuatorsaturationwhile
to improve efficiency [192]. These kinematic models are guaranteeingmarginalstability[201].Aclassicaldrawbackof
continuously being generalized to accommodate more com- SMC is the high-frequency “chattering” in the control signal.
plex physical designs, including manipulators with arbitrary, This issue was mitigated by integrating fuzzy logic to smooth
discontinuous, or overlapping actuator routings [193]. the discontinuous control law, leading to smoother actuation
While kinematic models determine the robot’s shape, dy- profiles [202]. The methodology continues to evolve with ad-
namic models are required for high-speed maneuvers and in- vanced variants, such as terminal SMC, which achieves faster
teractions with the environment. Controllers based on Inverse finite-time convergence. It was combined with algorithms for
Dynamics (ID) account for forces such as inertia, gravity, and high-level tasks such as obstacle avoidance [203].
external contacts. Such methods achieved full shape control, Whenperformanceiscriticalandconstraintsmustbeexplic-
with some approaches combining geometric methods with itly respected, Model Predictive Control (MPC) is the method
EBRT to balance accuracy and computational speed [109]. of choice. MPC solves a finite-horizon optimization problem
Because dynamic models are computationally demanding, ateachtimestep,enablingittonaturallyenforceinputbounds
recent work explored decentralized control architectures that while optimizing complex objectives. This capability makes it
distribute computation across modules, improving real-time particularly suitable for medical applications, such as catheter
feasibility [194]. control, where the robot must apply a constant force to
tissue while tracking a trajectory [204]. MPC is also highly
C. Managing Nonlinearities and Under-actuation effective for motion planning, as it can generate the complex,
oscillatory actuation signals required for behaviors like fish-
A central challenge in continuum robotics arises from the
like swimming, even under disturbances [205]. However, the
strong nonlinearities and inherent under-actuation of these
limitationofMPCremainsitscomputationalcost,whichoften
systems. Feedback Linearization (FL) is a powerful technique
necessitatesmodelsimplifications(e.g.,linearization)forreal-
that cancels nonlinear terms, transforming the system dynam-
time implementation.
ics into a simpler, linear form. FL was successfully applied
Beyond traditional methods, emerging paradigms include
in cascade control architectures to compensate for gravity
optimal control for bio-inspired motions [206], decentralized
and bending effects, thereby improving tracking performance
robust control for modular architectures [70], and synergetic
[195]. However, its effectiveness depends heavily on model
control [207], which has recently shown robustness to distur-
accuracy. To address this limitation, [196] proposed a hybrid
bances in continuum robots control.
approach that combines an inner-loop FL controller with
a robust outer-loop strategy such as Sliding Mode Control
(SMC),enablingrobustnessagainstmodeluncertainties[196]. E. Shape/State Estimation
Practical aspects also matter: research shows that the choice
A general MB shape controller requires feedback in terms
of discretization scheme can significantly influence numerical
of configuration vector q and its time derivative q˙ (Figure 5).
robustness, computational cost, and accuracy [52].
Depending on the spatial discretization, the vector q could
An alternative approach is the Energy-Shaping Control
be difficult or impossible to measure. To tackle this issue, a
(ESC). Instead of canceling dynamics, ESC reshapes the
general MB control framework requires an Estimator, which
system’s potential energy such that the desired configuration
maps the measures y to the estimated state qˆ, qˆ˙. For contin-
becomes a stable energetic minimum. By reformulating the
uumandsoftrobots,thisproblemisreferredtoasShape/State
dynamics in a Port–Hamiltonian framework, this method can
Estimation or Shape/State Reconstruction. Shape Estimation
formally guarantee stability and passivity, allowing control of
methods can use geometrical models or Computer Vision
bothunder-actuatedandhyper-redundantsystems[197],[198].
algorithms [209], [210]. However, the following works show
ESC often produces smooth, natural motions that exploit the
that incorporating prior knowledge of rod-based models can
robot’s intrinsic compliance. It was applied even to complex
significantly enhance performance. The pioneering work of
bio-inspired systems such as octopus tentacles, where optimal
[211] suggests three approaches for Shape Estimation, based
controlwasusedtoidentifyshapinglawsforadvancedmodels
onCRT:(i)mountingloadcellsatthebase,(ii)employingca-
that include non-rigid cross-sections [199].
ble encoders, and (iii) mounting an inclinometer at the end of
Discrete-time control is necessary for practical implemen-
eachpiece.Amaximumtippositionerrorof3%Lisobserved
tations, even though most of the ESC literature concentrates
in simulations. All three approaches were then experimentally
on continuous-time models. Structure-preserving numerical
validated on the OctArm VI [212]. Another study by [213]
techniques, such as Lie group variational integrators, are
proposes a real-time shape-estimation method based on the
used to maintain the stability and passivity guarantees in a
force-torquemeasuredatthebasisofthetubesforaconcentric
discretized system [200]. These integrators allow for efficient
tube robot (CTR). It extends a shape estimation algorithm
stabilization of flexible beams while preserving the geometric
for elastic Kirchhoff rods. They modeled a CTR combining
structure of the manipulator’s configuration space.
planar piecewise constant curvature (PCC) segments lying on
different equilibrium planes. The approach is evaluated with
D. Robust and Optimal Control
singleandtwocombinedadditivelymanufacturedtubesathigh
Robust controllers for continuum robots were designed frequency, achieving a mean deviation of 2 − 5 mm along
to mitigate model uncertainties. SMC is a widely adopted the tube. Differently, [214] developed a model for shape and
strategy for ensuring robustness against model uncertainties strain estimation of a continuum cable-driven robot using a

17
TABLEIII
MODEL-BASEDCONTROLLERSUSINGRODMODELS.
|     |                   | Controller |     |     | References  |       | RodModel |      |                   |                 | Task |     | Validation   |     |     |
| --- | ----------------- | ---------- | --- | --- | ----------- | ----- | -------- | ---- | ----------------- | --------------- | ---- | --- | ------------ | --- | --- |
|     |                   |            |     |     | [189],[208] |       |          | EBRT |                   | TipPoseTT       |      |     | Experimental |     |     |
|     |                   |            |     |     |             | [152] |          | CRT  |                   | TipPositionTT   |      |     | Experimental |     |     |
|     | InverseKinematics |            |     |     |             | [191] |          | CRT  | MPOrientationReg. |                 |      |     | Experimental |     |     |
|     |                   |            |     |     |             | [192] |          | CRT  |                   | TipPoseTT       |      |     | Experimental |     |     |
|     |                   |            |     |     |             | [193] | CRT(GVS) |      |                   | MPPoseTT        |      |     | Numerical    |     |     |
|     |                   |            |     |     |             | [109] | EBRT+PH  |      |                   | ShapeRegulation |      |     | Experimental |     |     |
InverseDynamics
|     |     |     |     |     |     | [194] |     | CRT |     | ShapeTT       |     |     | Numerical |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ------------- | --- | --- | --------- | --- | --- |
|     |     |     |     |     |     | [196] |     | KRT |     | TipPositionTT |     |     | Numerical |     |     |
FeedbackLinearization
|     |     |                |     |     |             | [52]  | CRT(GVS)  |     |                   | PickandPlace    |     |     | Numerical    |     |     |
| --- | --- | -------------- | --- | --- | ----------- | ----- | --------- | --- | ----------------- | --------------- | --- | --- | ------------ | --- | --- |
|     |     |                |     |     | [197],[198] |       | CRT(GVS)  |     |                   | TipPositionReg. |     |     | Numerical    |     |     |
|     |     | Energy-Shaping |     |     |             | [199] | CRT(DER)  |     | Reaching,Grasping |                 |     |     | Numerical    |     |     |
|     |     |                |     |     |             | [200] | PlanarCRT |     |                   | ShapeReg.       |     |     | Numerical    |     |     |
|     |     |                |     |     |             | [201] |           | CRT |                   | TipPoseTT       |     |     | Numerical    |     |     |
|     |     | SlidingMode    |     |     |             | [202] |           | CRT |                   | TipPositionTT   |     |     | Experimental |     |     |
|     |     |                |     |     |             | [203] | CRT+Hyst. |     |                   | TipPositionTT   |     |     | Numerical    |     |     |
|     |     |                |     |     |             | [204] | StaticCRT |     |                   | TipPositionTT   |     |     | Experimental |     |     |
ModelPredictiveControl
|     |     |     |     |     |     | [205] |     | EBRT |     | TipPositionTT |     |     | Numerical |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | ---- | --- | ------------- | --- | --- | --------- | --- | --- |
Open-LoopOptimalController [206] CRT(DER) Reaching,Fetching Numerical
|     |     | H   |     |     |     | [70] |     | EBRT |     | ShapeRegulation |     |     | Numerical |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- | --------------- | --- | --- | --------- | --- | --- |
∞
|     | SynergeticControl |     |     |     |     | [207] |     | CRT |     | TipPositionTT |     |     | Numerical |     |     |
| --- | ----------------- | --- | --- | --- | --- | ----- | --- | --- | --- | ------------- | --- | --- | --------- | --- | --- |
GaussianProcessregressiontoestimatecontinuoustrajectories experimentally, with and without knowledge of the contact
in SE(3). The idea involves substituting (i) time t with arc- positions. Recently, [220], [221] proposed the Cosserat the-
length s and (ii) kinematic and dynamic laws based on CRT. oretic boundary observer, a mechanics-based dynamic state
Thismethodefficientlyestimatestherobot’sshapeusingnoisy estimation algorithm to recover the infinite-dimensional robot
measurements from sensors such as strain gauges, tracking states by measuring the tip velocity twist and the tip pose.
coils, and an external camera. The real-world experiments Finally, [222] presents a novel method for estimating the dy-
provide excellent performances, with an average tip pose namicstate(poseandvelocity)oftendon-actuatedCSMs.The
error of 3.3 mm and 0.035◦. In parallel, [215] developed approach uniquely combines a Geometrical Variable Strain
a model-based framework for estimating distributed contact (GVS) Cosserat rod model with a nonlinear State-Dependent
forces directly from shape measurements. The method in- Riccati Equation observer. A key advantage of this technique
volvedfittingaCosseratrodkinetostaticmodelwithGaussian is its ability to estimate the state using only internal sensor
load parameterization and solving it via an Extended Kalman data, such as tendon displacements and actuator forces. The
Filter,enablingreal-time,sensorlessforceestimationwithsub- method was validated both in simulation and on a prototype,
Newton accuracy. State estimation under uncertainty was also achieving an average dynamic tip position error of 1.79 cm.
| addressed | in reconfigurable |     | parallel | continuum |     | systems | [216], |     |     |     |     |     |     |     |     |
| --------- | ----------------- | --- | -------- | --------- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
applying Cosserat rod modeling, multi-point constraints, and VIII. LEARNING-BASEDCONTROLLERSFORROD
| advanced | filtering | to  | improve | tip accuracy |     | and enable | load |     |     |     |     |     |     |     |     |
| -------- | --------- | --- | ------- | ------------ | --- | ---------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
MODELS
| inference.      | [217] | presents | a surgical |               | continuum | manipulator |        |              |          |         |       |         |             |                |      |
| --------------- | ----- | -------- | ---------- | ------------- | --------- | ----------- | ------ | ------------ | -------- | ------- | ----- | ------- | ----------- | -------------- | ---- |
|                 |       |          |            |               |           |             |        | Machine      | Learning |         | (ML)  | methods | for         | controlling    | CSMs |
| with integrated |       | FBG      | sensing    | for real-time | 3D        | shape       | recon- |              |          |         |       |         |             |                |      |
|                 |       |          |            |               |           |             |        | are becoming |          | a trend | [10], | [12],   | [20], [21]. | Learning-based |      |
struction,enablingsub-millimeternavigationwithoutradiation
|            |          |           |       |          |     |               |     | controllers | can | leverage | the | physics | of rod | models | to derive |
| ---------- | -------- | --------- | ----- | -------- | --- | ------------- | --- | ----------- | --- | -------- | --- | ------- | ------ | ------ | --------- |
| in complex | surgical | settings. | [218] | provided | a   | comprehensive |     |             |     |          |     |         |        |        |           |
π(· ; w)
|        |                  |     |            |     |              |           |     | control                                       | policies |     | from | experience. |     | Such | policies es- |
| ------ | ---------------- | --- | ---------- | --- | ------------ | --------- | --- | --------------------------------------------- | -------- | --- | ---- | ----------- | --- | ---- | ------------ |
| review | of shape-sensing |     | modalities |     | for surgical | continuum |     |                                               |          |     |      |             |     |      |              |
|        |                  |     |            |     |              |           |     | tablishend-to-endmappingsbetweendesiredposesg |          |     |      |             |     |      | ,sensor      |
robots, highlighting complementary strengths of electromag- d
|                 |      |     |              |     |          |                |     | measurements |     | y, and | motor | commands | τ:  |     |     |
| --------------- | ---- | --- | ------------ | --- | -------- | -------------- | --- | ------------ | --- | ------ | ----- | -------- | --- | --- | --- |
| netic, optical, | FBG, | and | vision-based |     | methods. | On the control |     |              |     |        |       |          |     |     |     |
side, underactuated discrete rod models were leveraged to τ =π(g ,y; w), (47)
d
| achieve | precise | task-space | trajectory | tracking |     | through FL | and |     |     |     |     |     |     |     |     |
| ------- | ------- | ---------- | ---------- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
wherewrepresentstheweightsofanartificialneuralnetworks
| robust sliding-mode |     | strategies, |     | all while | relying | on minimal |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | ----------- | --- | --------- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(ANNs).Byintegratingphysics-baseddata,thesemethodscan
| sensing       | [196].   | In addition,        | [219]        | propose    | an            | optimization- |         |                     |                |              |                |          |                  |          |            |
| ------------- | -------- | ------------------- | ------------ | ---------- | ------------- | ------------- | ------- | ------------------- | -------------- | ------------ | -------------- | -------- | ---------------- | -------- | ---------- |
|               |          |                     |              |            |               |               |         | improve             | adaptability   |              | and robustness |          | in automation    |          | tasks that |
| based method  |          | that simultaneously |              | estimates  | the           | shape and     | the     |                     |                |              |                |          |                  |          |            |
|               |          |                     |              |            |               |               |         | involve             | compliant      | interactions |                | with     | the environment. |          | Below,     |
| forces acting | on       | a continuum         |              | robot by   | employing     | the           | quasi-  |                     |                |              |                |          |                  |          |            |
|               |          |                     |              |            |               |               |         | we review           | learning-based |              |                | policies | for Supervised   |          | Learning   |
| static CRT.   | Magnetic |                     | localization | determines |               | the position  |         |                     |                |              |                |          |                  |          |            |
|               |          |                     |              |            |               |               |         | (SL) and            | Reinforcement  |              | Learning       |          | (RL).            | We adopt | a chrono-  |
| of multiple   | robot    | points.             | The          | method     | estimates     | the           | robot’s |                     |                |              |                |          |                  |          |            |
|               |          |                     |              |            |               |               |         | logical perspective |                | to           | highlight      | the      | evolution        | of this  | growing    |
| shape and     | force    | in                  | a wide       | range      | of conditions | validated     |         |                     |                |              |                |          |                  |          |            |
|               |          |                     |              |            |               |               |         | field and           | its impact     | on           | robotics       | and      | automation.      |          |            |

18
policy can be stochastic, mapping a state to a distribution
over actions a ∼ π(·|s ). As a result of taking an action,
t t
the environment transitions to a new state s according to
t+1
the rod dynamics. Then, the agent perceives a scalar reward
signal r from the environment, indicating the goodness of
t+1
the current state specifying the control task. The goal of the
agentistomaximizeitsreturn,thecumulativesumofrewards:
∞
(cid:88)
G = γkr , (48)
t t+1+k
k=0
where γ ∈(0,1) is a discount factor. To sum up, RL aims to
Fig.6. SoftrobotcontrolcombingRLandrodmodels.Theagentemploys find an optimal policy π∗ that maximizes the expected return
anANNascontroller,whilerodmodelsgoverntheenvironmentdynamics.
π∗ =argmaxE [G ]. (49)
π 0
π
A. Supervised Learning
Below and in Table IV, we review the state-of-the-art RL
SL in simulation is a viable approach to address simple
policies for CSMs trained on rod models.
taskswithsoftrobots.Itreliesonpseudo-randommotiondata
Survey of RL policies: The earliest contribution was pre-
of actuations τ and corresponding task space g to train an
sented by Satheeshbabu et al. [227], where they applied deep
inverse model (47). For instance, [223] developed dynamic
Q-learning(DQL)withexperiencereplay.DQLcancopewith
models of CSMs using recurrent neural networks (RNNs)
thechallengingstate-actionspaceofsoftrobotsbyemploying
and presented a trajectory optimization method for task space anANNQˆ(s,a;w)toapproximatethevaluefunctionofstate-
control. They validated the controller on a Cosserat rod
action pairs [228], which is defined as
with piecewise constant strain (PCS) parameterization and a
pneumaticCSM.Similarly,[224]developedaclosed-loopcon-
troller for continuum robots using RNNs to approximate for- Q π (s,a):=E π [G t |s,a]. (50)
ward and inverse dynamics. They extended the model in [49]
to account for spine compression and generate motion data Then, a deterministic policy can leverage Qˆ to select the
for training. A non-parametric Gaussian process regression best action in a state as a = π(s) = argmax a Qˆ(s,a;w).
compensates for discrepancies between the real robot and the The work presented an open-loop policy for the quasi-static
RNN, while a hybrid controller alternates between two stand- position control of a pneumatic CSM that can bend and twist.
alone policies. The approach was validated on reaching and The policy π was trained on a static Cosserat rod simulation
tracking tasks with a tendon-driven continuum robot, showing andvalidatedbothinsimulationandonthephysicalplatform,
improved accuracy by combining simulated and experimen- subject to various external loads. The work was extended
tal data. Recently, generative adversarial networks achieved by increasing the dexterity of the CSM and developing a
domain translation of a pose controller across environments closed-loop policy, still for precise quasi-static positioning,
with different medium viscosities, supported by a Cosserat via deep deterministic policy gradient (DDPG) [229]. They
rod model [225]. While combining continuum and generative investigatedtherobustnessofthecontrolpolicytoloadingand
models for adaptive soft robotic automation is promising, the workspacediscontinuity,anddeployedthepolicyonhardware.
domain-translation model required substantial computing, and The DDPG algorithm also derived a closed-loop controller
the policy only solved tracking tasks in simulation. for the quasi-static positioning of a pneumatic CSM modeled
with the Kirchhoff rod theory (KRT) [230]. Interestingly, the
CSM was integrated into a mobile platform including a rigid
B. Reinforcement Learning
arm and a sensorized gripper. The system was teleoperated
Overview: RL is a versatile framework for sequential and validated in the agricultural task of picking berries using
decision-making, adaptive control, and robotic automation different maneuvering strategies.
[226]. The two fundamental objects of an RL problem are The potential of continuum mechanical models is fully
the agent and the environment. In soft robotic control, the exploited in automatic physical interaction tasks. Naughton
agent is a learning-based controller based on ANNs, whereas et al. [65] effectively applied several deep RL algorithms to
the environment is everything outside the agent, comprising train various control policies. They explored point reaching,
the soft robot and other objects. Figure 6 depicts the agent- trajectory tracking, and maneuvering through structured and
environmentinteractionhighlightingtheroleofANNsandrod unstructuredobstacles.Thecontrollerswerelearnedandtested
models. The agent and the environment interact at discrete in simulation using a synthetic CSM based on a dynamic
time steps t. At every step, the agent observes the (possibly CRT. The rod was actuated by applying distributed internal
partial) state s of the environment, including sensor readings torques, modeled via splines characterized by control points
t
and task information. The agent acts according to a policy and vanishing values at the rod ends. The work showcased a
π to select actions a taking the form of low-level controls captivating interaction between the rod and the environment.
t
τ like torques or pressures. A policy can be a deterministic For example, the maneuvering task required the rod free end
mapping from states to actions, a = π(s ). Alternatively, a r(L) to reach a position x behind fixed obstacles. The task
t t d

19
TABLEIV
DEEPREINFORCEMENTLEARNINGCONTROLLERSUSINGRODMODELS.
RodModel Sim-to-real
Controller References Task
(dynamics) (technique)
DeepQ-Learning [227] CRT(✗) TipPositionTT(way-point) ✓(None)
[229] CRT(✗) TipPositionTT(way-point) ✓(None)
DeepDeterministicPolicyGradient [230] KRT(✗) TipPositionTT(way-point) ✓(None)
TrustRegionPolicyOptimization [65] CRT(✓) TipPoseTT,Obstaclemaneuvering ✗
[231] CRT(✓) TipPositionTT,Objectinterception ✗
ProximalPolicyOptimization [27] CRT(✓) Pushing(TipPose/Force) ✓(DR)
was solved with a reward function that only considered the this end, the Kirchhoff–Love theory handles large rotations
distance to the target and a penalty term for numerical errors and displacements but assumes the rod is inextensible and
(cid:40) unshearable. This assumption limits its ability to model ex-
penalty, numerical errors
reward= (51) tensible pneumatic actuators. Finally, the Cosserat-Reissner
||x d −r(L)||, otherwise. model and its extensions are the most general and suited for
continuum soft robots. They can handle large deformations,
Interestingly, the rod learned to navigate and interact with the
shear, torsion, and stretching. However, they require more
obstacles without an explicit reward term.
computationaleffort.Overall,eachrodtheoryhasitsstrengths
The generalization capabilities of learned controllers are
andweaknesses.Thechoicedependsonthesystem’sbehavior
vital for successful real-world deployment. In this regard,
andthelevelofdetailneeded.WesuggestoptingforaCosserat
Alessietal.[231]appliedproximalpolicyoptimization(PPO)
rod model and tuning the space and time discretization to
to train a closed-loop position control policy for dynamic
match the desired tradeoff between efficiency and accuracy.
trajectorytrackingwithapneumaticCSM.Thecontrollerwas
trained leveraging a dynamic Cosserat rod model of the soft
robot [160]. Then, four simulation tests evaluated how the B. On the Deformations
policy generalized to new observations, dynamics, and tasks.
Researchers developed numerous rod-based models by
The experiments included tracking new trajectories subject to
adapting classical rod theories to soft robotics. The reviewed
unknown external forces F (L) or using different material
e models capture different combinations of strain modes, giving
properties (e.g., E). The policy generalized well within some
rise to nine deformation classes.
boundaries and also transferred without retraining to intercept
The most common class in literature is Bend, with about
a moving object. Subsequently, [27] extended the simulation
a third of the examined papers. This popularity is due to
environment to account for the dynamics of a dexterous CSM
the propensity of slender bodies to bend. In fact, due to
and its interaction with objects. The proposed closed-loop
the assumption of L ≫ D, with D cross-section diameter,
pose/force controller enabled dynamic pushing with CSMs
the bending stiffness turns out smaller than the stretching or
in the real world. To mitigate the significant sim-to-real gap
shear ones, easing the bending deformation. In addition, most
in soft robotics, the authors introduced a novel adaptation
used actuator paths are linear, which excite predominantly
of domain randomization (DR) [104] emphasizing the soft
bending modes. These reasons justify the approximation of
material properties. This work demonstrated the first sim-to-
considering only the bending mode. Furthermore, we can
real transfer of a rod-based manipulation policy, paving the
observethatmostmodelsintheBendclassleveragetheEBRT.
wayforsoftroboticautomationandphysicalinteractiontasks.
However,assummarizedinTableII,severalmodelsemployed
the general CRT. While this may constitute a computational
IX. DISCUSSIONANDEMERGINGCHALLENGES
surplus for simple bending structures, the expressive power of
A. On the Rod Theories Cosserat models becomes valuable when the model is used in
Following our mathematical treatment and review of rod physicalinteractionscenarios,forinstance,forpolicylearning
models, we briefly reevaluate the strengths and limitations or model-based control design.
of the various rod theories within soft robotics. The Euler- The next class is All Deformation, with about a quarter
Bernoullimodelissimple,computationallylight,andeffective of the examined papers. As expected, only models based on
forslender,stiffstructuressubjecttosmallbendingdeflections. the CRT achieve all deformations (Table II). This group of
Its nonlinear version makes it suitable for large deformations. models received a deep study in the last decade, thanks to
However, it remains a planar model and neglects shear as the rising interest in physical interaction with unstructured
the cross-sections remain perpendicular to the centerline. This environments where all strain modes are significant. Indeed,
assumptionmakesitunsuitableformodelinginteractionswith thesemodelsareusefultodescribeaccuratelythedeformations
the environment in soft robotics. Nonetheless, some works of slender robots caused by friction (e.g., anisotropic friction
extended its applicability beyond bending by coupling it with for locomotors) or by different mediums (e.g., water). In
other models. The Timoshenko model improves on this by addition, the most common actuation sources (i.e., pneumatic
including shear deformation. However, Timoshenko is less and cables) excite elongation and compression, causing a
suited to nonlinear actuator paths that induce torsion. To significant change in the dimension workspace.

20
The third class accounting for about a fifth of the investi- detailed finite element method (FEM) simulations served a
gated studies is Bend & Twist. These models mainly describe dual purpose: (i) to assess the correctness of the rod model,
robots in which the unshearability and the unstretchability ap- and(ii)toestimatetheunknownparameters.Intheabsenceof
proximations hold (Table II). Including the twisting deforma- preciseFEMmodels,lumped-massmodelswithahighnumber
tionallowstherepresentationofbackboneswithgenericthree- of degrees of freedom (DoFs) were employed. Otherwise,
dimensional (3D) curves. However, the twisting deformation researchers resort to model optimization to match experimen-
can be excited only by specific actuator paths (e.g., helicoidal tal data. In particular, when the robot morphology is not
cables) or asymmetric actuators. uniform, researchers usually estimate geometrical properties
Another significant class is Bend & Stretch thanks to the (e.g., cross-sectional area A(s)) and material characteristics
wide diffusion of linear extensible soft pneumatic actuators (e.g., elastic modulus E, damping coefficient β). The ex-
and tendon-driven robots. Such actuators extend or compress periments conducted typically feature the robot at different
uponsolicitation,whichinducesthecontinuumbodytostretch base orientations subject to external loads F (s) or at the
e
andbendthankstotheirradialdispositiononthecross-section. tip. Most rod models are identified and validated through
The remaining five categories are less explored. While the motion data collected with predefined actuation profiles τ.
Bend, Twist & Stretch is a particular case of the All Deforma- However, rigorous mechanical tests are still needed to yield
tions class, the other classes include fewer works. The lack of more accurate models, especially for unstructured physical
work is due to the difficulty of exciting these specific strain interactions with the environment. Indeed, despite a careful
modes with the current actuation technologies or the small model calibration on motion data, [27], [160] observed real-
number of applications in which the assumptions are valid. worldbucklingduringamanipulationtaskthatwasnotpresent
The fact that fewer studies explored shearing per se could in simulation. Concerning performance metrics, rod models
be due to the tendency to consider shearing an undesirable or predicted experimental tip positions with Euclidean errors in
negligibledeformation.However,shearingcouldbesignificant therange1−10%L.However,onlyafewstudiesassessedthe
whenthereisaprominentenvironmentinteraction,asobserved angular errors, which play a role in dexterous manipulators.
inperistalticlocomotion[172]orcomplexmanipulation[170]. In summary, the increasing use of experimental data reflects
Shearing also becomes important when the aspect ratio of the the demand to bridge the sim-to-real gap for developing more
CSM becomes less slender and thicker. accurate controllers.
C. On the Spatial Discretization
E. On the Impact of Materials and Manufacturing
A characterizing feature of rod models is the spatial dis-
Most of the analyzed rod models employed continuum and
cretization method, which significantly impacts the model’s
soft robots built with diverse materials, including traditional
accuracyandcomplexity.Forsimulationandcontrolpurposes,
elastomers (e.g., silicone, rubber) or other polymers (e.g.,
the discrete model must be computationally efficient and as
shape memory alloys (SMAs), hydrogels). Each material of-
accurate as possible. In the analyzed literature, two primary
fers distinct properties, influencing the robot’s compliance,
discretization approaches are commonly employed: Discrete
flexibility, and functionality. However, effectively modeling
Elastic Rod (DER) and Strain Parameterization.
the nonlinear behavior inherent in soft materials using rod
The DER method discretizes the rod’s length into nodes
theories presents challenges. For instance, some combinations
connected by rigid links, representing the rod CSM as a set
of materials and actuation mechanisms cause notable changes
of discrete poses. The accuracy of the solution relative to the
in cross-section areas or volume, which may render the rod-
continuous rod depends on the number of nodes. In contrast,
like assumption overly restrictive. Nonetheless, an extension
StrainParameterizationdiscretizestherodintheconfiguration
of the CRT considering geometrical rescaling (15) could
space,constrainingtherobot’sbackbonetoasubsetofadmis-
approximate complex dynamics (16).
siblespatialcurves.Thelatterapproachpermitstheneglectof
The viscoelastic constitutive law of the material impacts
specific strain modes without imposing additional constraints
significantly on the accuracy. In the classic rod theories, this
on the EoMs, as required in the DER formulation, thereby
relation is supposed linear, as already shown in (6). However,
enhancing computational efficiency. Furthermore, Strain Pa-
especially in the case of pneumatic actuation, the linear
rameterization naturally allows the forward dynamics to be
constitutive law is no longer valid. To tackle this issue, many
expressed in Lagrangian form, which is particularly advanta-
analyzedworkspresentedmodelswithanonlinearconstitutive
geous for control design. Both approaches were widely used
law, using hyperelastic model such as Odgen.
and integrated into dedicated simulators, such as SoRoSim
Manufacturing techniques provided continuum and soft
[60] for Strain Parameterization and PyElastica [65] for DER.
robots with unprecedented dexterity [232]. However, manu-
Straddling geometric and mechanical models, some exam-
facturing uncertainties may impact model accuracy. Recent
inedworksproposedtofitdiscretepointswithfunctions,such
rodmodelsaddressedmanufacturinguncertaintiesconsidering
as Pythagorean Hodograph (PH) or Euler’s spirals, which is
variations in material [160] and geometric properties [180].
useful, especially for Shape Estimation.
Research gaps persist despite these advancements. First,
capturing hysteresis—a prevalent phenomenon in soft ma-
D. On the Identification and Validation
terials that affects the accuracy and predictability of the
Identification and validation of rod models play a crucial robot’s behavior—remains largely underexplored in rod mod-
role in accurately reproducing the experimental robot behav- els. Second, incorporating self-healing materials can poten-
iors. Despite the high computational cost, it emerged that tiallyenhancethedurabilityandlongevityofsoftrobots[233].

21
However, integrating the dynamic restoring process into rod few studies involving external forces due to interactions with
models should still be investigated. Filling these gaps could the environment, particularly because of the complexity in-
advancethecapabilitiesofcontinuumandsoftrobots,enabling volvedinmodelingandestimatingcontactandfrictionforces.
theirintegrationintodiverseapplicationsandreal-worldtasks. Due to the current lack of maturity of the controllers, the
literature on rod-based planning [171], [203] is still sparse,
F. On the Model-based Controllers although planning algorithms using geometrical approaches
The emergence of computationally efficient and accurate wererecentlyproposed[235].Futuredevelopmentsonmodel-
modelsenablesresearcherstodevelopmodel-basedcontrollers based controllers could benefit from using physics-informed
that can accurately predict and react to nonlinear elastic rods. ANNs to lessen the computational burden of complex ex-
WeobservedthatcontrollersbasedonIKarethemostpopular pressions (e.g., the Coriolis matrix) or use them to compute
choice, as they achieve tip trajectory tracking tasks in real- the EoMs of the elastic rod, as already explored in [236],
world prototypes (Table III). Despite the simplified model, [237]. Another promising future direction is the application
thefeedbackactioncanrejectunmodeledeffects,showingthe of the Collocated Form proposed in [185] to the design of
effectiveness of that strategy. However, we should note that more advanced controllers, particularly those inspired by the
most IK-based controllers treat the system as fully actuated. rigid underactuated robotics literature. This specific change
This limits control to a smaller set of DoFs than the robot is of coordinates can simplify feedback implementation, since
inherently capable of exhibiting. the actuator lengths are directly measurable and easier to
A dynamic model is essential to exploit the properties of estimate,asalsoexploitedby[222].Furthermore,adoptingthis
continuumrobots.Mostoftheproposedcontrollersadoptwell- coordinatetransformationcanenhanceIK-basedcontrollersby
known approaches from the under-actuation literature, such naturally accounting for the system’s under-actuation. Finally,
as FL, ESC, SMC, or MPC. However, only a few proposed differentiablesimulatorsandlibrariesforrodmodelscouldbe
controllers were validated experimentally. The reasons for utilized for optimal control. Recently, analytical derivatives
neglecting the sim-to-real comparison could be the lack of for the GVS model were calculated in [61], facilitating the
robustness or physical limits of the prototypes. While the implementation of model-based optimal controllers.
Inverse Dynamics, FL, and ESC are sensitive to unmodelled
effects and parametric uncertainties, the discontinuous output G. On the Learning-based Controllers
of the SMC is difficult to implement with the most popular Learning-based controllers utilized the physics of rod mod-
actuationtechnologies(e.g.,tendons,pneumatic).Specifically, els with a clear distinction between SL and RL.
theactuators’internaldynamicsmaylimittheeffectivesystem In SL-based methods, rod models were only used as
bandwidth, hence filtering the discontinuous output of the proxies to collect motion data under predefined open-loop
controller. The MPC is a promising but not widely explored policies. The motion data were employed to train ANNs,
controller in the continuum robots literature, which could be which efficiently emulated forward or inverse robot models,
attributed to the relatively high computational cost. and replaced rods to facilitate the preliminary validation of
Two key aspects facilitate the design of controllers for controlhypotheses.AlthoughSLwaswidelyusedinearlysoft
CSMs: (i) the development of advanced discretization tech- robotic controllers, it limits the robot tasks to simple reaching
niques and (ii) the tunability of model accuracy. The former and tracking due to the challenges in collecting supervised
enables the design of controllers with a finite number of state data for physical interaction tasks. For this reason, we believe
variables, allowing for the efficient computation of the robot’s SL for rod models could fade away in the future.
kinematics and dynamics. Choosing appropriate discretization Conversely, the role of rod models is central for developing
techniques is particularly critical for determining the mini- complex deep RL control policies to achieve unstructured
mum control frequency required to ensure numerical stability. physical interaction with CSMs. Deep RL agents exploited
Furthermore, the DER technique captures cross-sectional de- computationally feasible rod models embedded in simulated
formations, which are especially relevant for modeling and environments to learn optimal actions τ iteratively. Herein,
controlling muscle-like structures in bio-inspired robotic sys- RL reduces the burden of collecting labeled datasets offline
tems [199]. This feature was recently integrated within the and unlocks new possibilities that are not fully explored yet.
GVS framework by [234], who proposed an extended CRT The control tasks addressed evolved from position control for
formulationthatmodelsradial(in-plane)deformationsthrough quasi-static tracking to simulated pose control for obstacle
an additional strain variable. Their model also incorporates maneuvering and pose/force control for dynamic pushing
nonlinear hyperelasticand viscouseffects, extending the GVS (Table IV). For instance, initial policies limited the physical
approach to more complex, bio-inspired dynamic scenarios. interaction to static payloads without addressing the sim-to-
Equally important is the ability to tune model accuracy by real gap [229]. Conversely, efforts in developing simulated
neglectingspecificmodesorreducingthenumberofDoFs,as environments [65] combined with careful reward engineering
implemented in the Strain Parameterization. This flexibility and sim-to-real techniques [27] facilitated recent advance-
allows for trade-offs between accuracy and computational ments in physical interaction with CSMs. In summary, we
complexity, enabling the controller to treat unmodeled dy- believethecombinationofrodmodels,deepRLmethods,and
namics as external disturbances. Such a strategy increases the sim-to-realtransfertechniquescouldadvancethemanipulation
control loop frequency by reducing computational load and capabilities of CSMs.
enhances its overall robustness. Alltheseworks,however,reliedonmotioncapturesystems
Regarding research gaps, we observed the lack of experi- to track the robot positions. Indeed, reliable soft robotic pro-
mental validation for MB controllers. Furthermore, there are prioception is an open challenge [238]. Future developments

22
|     |     |     |     |     |     |     |     |     |     |     | (cid:2) |     | (cid:3)⊤ |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | -------- | --- | --- |
couldexploremodel-basedRL,wheremodel-basedhererefers For a vector w = w w w ∈R3, its application
|     |     |     |     |     |     |     |     |     |     |     | x   | y   | z   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
to not only learning a policy but also learning a predictive gives an skew-symmetric matrix
modeloftheenvironmentusedforplanning[239].Alternative
|     |     |     |     |     |     |     |     |     |     |     |    |     |     |    |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
researchlinescanbeborrowedfromrigidroboticsandtailored 0 −w z w y
|                       |     |     |            |     |          |        |        |     |         | w˜       | = w       | 0   | −w  | x . | (B.2) |
| --------------------- | --- | --- | ---------- | --- | -------- | ------ | ------ | --- | ------- | -------- | ---------- | --- | --- | ---- | ----- |
| to the nonlinearities |     | of  | continuum  |     | and soft | robots | [240]. |     |         |          |            | z   |     |      |       |
|                       |     |     |            |     |          |        |        |     |         |          | −w         | w   | 0   |      |       |
|                       |     |     |            |     |          |        |        |     |         |          |            | y   | x   |      |       |
|                       |     | X.  | CONCLUSION |     |          |        |        |     | The Hat | operator | is defined | as  |     |      |       |
•
| This review | paper |     | explored | the | modeling | and | control of |     |     |     |     |     |     |     |     |
| ----------- | ----- | --- | -------- | --- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
ˆ
continuum and soft robots with rod theories. Our vertical ( ·):R6 →se(3). (B.3)
| literature | survey | spanned | mathematical |     | formulations |     | of rod |     |     |            |           |      |     |     |     |
| ---------- | ------ | ------- | ------------ | --- | ------------ | --- | ------ | --- | --- | ---------- | --------- | ---- | --- | --- | --- |
|            |        |         |              |     |              |     |        |     |     | (cid:2) w⊤ | ν⊤(cid:3) | ∈R6. |     |     |     |
theories, rod-based models of continuum and soft robots, and Let be h= The Hat operator gives
control strategies with rod models. The review of the math- (cid:20) (cid:21)
|     |     |     |     |     |     |     |     |     |     |     | hˆ  | w˜ ν |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
ematical background facilitated comparison between different = ∈se(3). (B.4)
|            |          |       |              |     |             |     |          |     |     |     | 0⊤  | 0   |     |     |     |
| ---------- | -------- | ----- | ------------ | --- | ----------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
| rod theory | variants | while | highlighting |     | connections |     | to other |     |     |     |     |     |     |     |     |
models. We uncovered the versatility of rod theories through The Vee operator is the inverse of the Hat operator
•
| a comprehensive |     | review | of  | rod-based | models | that | supported |     |     |     |     |     |     |     |     |
| --------------- | --- | ------ | --- | --------- | ------ | ---- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
various studies, from bioengineering design to experimental (·)∨ :se(3)→R6.
(B.5)
| validation | of continuum |     | and | soft robots. | We  | grouped | the rod- |     |     |     |     |     |     |     |     |
| ---------- | ------------ | --- | --- | ------------ | --- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:16) (cid:17)∨
basedmodelsindeformationclassestooffernewperspectives Consequentially, it is possible to write hˆ =h.
| on the evolution |     | of the  | state | of the       | art, particularly |     | regarding |     |             |                 |     |         |     |           |     |
| ---------------- | --- | ------- | ----- | ------------ | ----------------- | --- | --------- | --- | ----------- | --------------- | --- | ------- | --- | --------- | --- |
| the relationship |     | between | robot | deformations |                   | and | modeling  |     |             |                 |     |         |     |           |     |
|                  |     |         |       |              |                   |     |           | •   | The Adjoint | Representations |     | consist | in  | two maps: | Ad  |
(·)
choices. While advanced model-based control approaches and ad . The former is defined as
(·)
| were effective | for | tracking | tasks, | RL  | coupled | with | sim-to-real |     |     |     |     |     |     |          |          |
| -------------- | --- | -------- | ------ | --- | ------- | ---- | ----------- | --- | --- | --- | --- | --- | --- | -------- | -------- |
|                |     |          |        |     |         |      |             |     |     |     |     |     |     | (cid:20) | (cid:21) |
strategies emerged as a promising approach for manipulation. R 0
|     |     |     |     |     |     |     |     |     | Ad  | :SE(3)→R6×6, |     |     | Ad = | 3×3   | ,   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | ---- | ----- | --- |
|     |     |     |     |     |     |     |     |     | (·) |              |     |     | g    | r˜R R |     |
Despiteremarkableadvancementsinintegratingrodtheories
(B.6)
| within soft | robot | models | and | controllers, |     | limitations | persist. |     |     |     |     |     |     |     |     |
| ----------- | ----- | ------ | --- | ------------ | --- | ----------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
For instance, modeling hysteresis effects of soft materials where g ∈SE(3). The latter is defined as
|     |     |     |     |     |     |     |     |     |     |     |     |     | (cid:20) | (cid:21) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | -------- | --- |
and comprehensive experimental validations in contact-rich w˜ 0
|     |     |     |     |     |     |     |     |     | ad  | :R6×6 | →R6×6, | ad  | =   | 3 ×3 , | (B.7) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------ | --- | --- | ------ | ----- |
scenarios remain challenging. Related to the control, address- (·) h ν˜ w˜
| ing efficient | sim-to-real |     | policy | transfer | remains |     | essential for |     |              |     |                |     |        |                     |     |
| ------------- | ----------- | --- | ------ | -------- | ------- | --- | ------------- | --- | ------------ | --- | -------------- | --- | ------ | ------------------- | --- |
|               |             |     |        |          |         |     |               |     | Furthermore, |     | it is possible | to  | define | also the co-adjoint |     |
robotdeployment.Whilethispaperfocusedonrodmodelsfor
|     |     |     |     |     |     |     |     |     | operator | ad∗ , | that is |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----- | ------- | --- | --- | --- | --- |
continuum and soft robot control, we believe the presented (·)
| insights | can broadly | support |     | future | research | in  | soft robotic |     |     |     |     |        |     |     |       |
| -------- | ----------- | ------- | --- | ------ | -------- | --- | ------------ | --- | --- | --- | --- | ------ | --- | --- | ----- |
|          |             |         |     |        |          |     |              |     |     |     | ad∗ | =−ad⊤. |     |     | (B.8) |
automation, manipulation, and interaction with complex envi- h h
| ronments, | and serve | as  | a reference |     | for developing |     | continuum |     |     |     |     |     |     |     |     |
| --------- | --------- | --- | ----------- | --- | -------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
REFERENCES
| and soft | robotic | systems. |     |     |     |     |     |     |     |     |     |     |     |     |     |
| -------- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
D.Trivedietal.,“Softrobotics:Biologicalinspiration,stateoftheart,
[1]
andfutureresearch,”AppliedBionicsandBiomechanics,vol.5,no.3,
APPENDIXA
pp.99–117,2008.
QUERYFORMODELSANDCONTROLLERS
|     |     |     |     |     |     |     |     | [2] | C.Laschietal.,“Soft |     | robotics: | newperspectivesforrobotbodyware |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --------- | ------------------------------- | --- | --- | --- |
andcontrol,”Polymers,vol.2,p.3,2014.
| The two | Scopus | advanced |     | search | queries | used | for the |     |     |     |     |     |     |     |     |
| ------- | ------ | -------- | --- | ------ | ------- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
[3] ——,“Softrobotics:Technologiesandsystemspushingtheboundaries
models and controllers are respectively: ofrobotabilities,”Sciencerobotics,vol.1,no.1,p.eaah3690,2016.
TITLE-ABS-KEY (“soft” OR “continuum”) AND [4] D.Rusetal.,“Design,fabricationandcontrolofsoftrobots,”Nature,
| •   |     |     |     |     |     |     |     |     | vol.521,no.7553,pp.467–475,2015. |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | --- | --- |
TITLE-ABS-KEY(robot*OR“arm”OR“manipulator”) [5] Y. Wang et al., “Advancements in soft robotics: A comprehensive
AND TITLE-ABS-KEY (“Cosserat” OR “Kirchhoff” review on actuation methods, materials, and applications,” Frontiers
OR “Timoshenko” OR “Euler-Bernoulli” OR “Geomet- inbioengineeringandbiotechnology,vol.16,no.8,p.1087,2024.
|     |     |     |     |     |     |     |     | [6] | G. S. Chirikjian, |     | “A continuum | approach | to  | hyper-redundant | ma- |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | ------------ | -------- | --- | --------------- | --- |
rically exact” OR “rod” OR “beam”) AND (theor* OR nipulator dynamics,” in Proceedings of 1993 IEEE/RSJ International
model*). ConferenceonIntelligentRobotsandSystems(IROS’93),vol.2. IEEE,
1993,pp.1059–1066.
[7] ——,“Hyper-redundantmanipulatordynamics:Acontinuumapprox-
| TITLE-ABS-KEY |     |     | (“soft” | OR  | “continuum”) |     | AND |     |                                                       |     |     |     |     |     |     |
| ------------- | --- | --- | ------- | --- | ------------ | --- | --- | --- | ----------------------------------------------------- | --- | --- | --- | --- | --- | --- |
| •             |     |     |         |     |              |     |     |     | imation,”AdvancedRobotics,vol.9,no.3,pp.217–243,1994. |     |     |     |     |     |     |
TITLE-ABS-KEY(robot*OR“arm”OR“manipulator”)
|     |     |     |     |     |     |     |     | [8] | C. Armanini | et  | al., “Soft robots | modeling: | A   | structured overview,” |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ----------------- | --------- | --- | --------------------- | --- |
IEEETransactionsonRobotics,2023.
| AND     | TITLE-ABS-KEY |     |       | (“Cosserat”       |     | OR  | ”Kirchhoff” |     |                |          |                  |             |          |                       |         |
| ------- | ------------- | --- | ----- | ----------------- | --- | --- | ----------- | --- | -------------- | -------- | ---------------- | ----------- | -------- | --------------------- | ------- |
|         |               |     |       |                   |     |     |             | [9] | H. B. Gilbert, | “On      | the mathematical |             | modeling | of slender biomedical |         |
| OR      | “Timoshenko”  |     | OR    | “Euler-Bernoulli” |     | OR  | “Geomet-    |     |                |          |                  |             |          |                       |         |
|         |               |     |       |                   |     |     |             |     | continuum      | robots,” | Frontiers        | in Robotics | and      | AI, vol. 8, p.        | 732643, |
| rically | exact”        | OR  | “rod” | OR “beam”)        |     | AND | (control*). |     |                |          |                  |             |          |                       |         |
2021.
[10] T.GeorgeThurutheletal.,“Controlstrategiesforsoftroboticmanip-
ulators:Asurvey,”Softrobotics,vol.5,no.2,pp.149–163,2018.
APPENDIXB
[11] C.DellaSantinaetal.,“Model-basedcontrolofsoftrobots:Asurvey
|     |     |     |            |     |     |     |     |     |              |        |         |                   |     | IEEE Control | Systems |
| --- | --- | --- | ---------- | --- | --- | --- | --- | --- | ------------ | ------ | ------- | ----------------- | --- | ------------ | ------- |
|     |     |     | LIEALGEBRA |     |     |     |     |     | of the state | of the | art and | open challenges,” |     |              |         |
Magazine,vol.43,no.3,pp.30–65,2023.
• The Tilde Operator is defined as [12] E.Faloticoetal.,“Learningcontrollersforcontinuumsoftmanipula-
tors:Impactofmodelingandloomingchallenges,”AdvancedIntelligent
Systems,vol.n/a,no.n/a,p.2400344,2024.
|     |     |     | ( ˜ ·):R3 | →so(3). |     |     | (B.1) |     |     |     |     |     |     |     |     |
| --- | --- | --- | --------- | ------- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |

23
[13] R. J. Webster III et al., “Design and kinematic modeling of constant [41] M.S.Xavieretal.,“Finiteelementmodelingofsoftfluidicactuators:
curvature continuum robots: A review,” The International Journal of Overview and recent developments,” Advanced Intelligent Systems,
RoboticsResearch,vol.29,no.13,pp.1661–1683,2010. vol.3,no.2,p.2000187,2021.
[14] P. E. Dupont et al., “Continuum robots for medical interventions,” [42] J.Allardetal.,“Sofa-anopensourceframeworkformedicalsimula-
ProceedingsoftheIEEE,vol.110,no.7,pp.847–870,2022. tion,” in MMVR 15-Medicine Meets Virtual Reality, vol. 125. IOP
[15] J.Burgner-Kahrsetal.,“Continuumrobotsformedicalapplications:A Press,2007,pp.13–18.
survey,”IEEEtransactionsonrobotics,vol.31,no.6,pp.1261–1280, [43] E. Coevoet et al., “Software toolkit for modeling, simulation, and
2015. controlofsoftrobots,”AdvancedRobotics,vol.31,no.22,pp.1208–
[16] J.Zhangetal.,“Asurveyondesign,actuation,modeling,andcontrol 1224,2017.
ofcontinuumrobot,”CyborgandBionicSystems,2022. [44] M.Dubiedetal.,“Sim-to-realforsoftrobotsusingdifferentiablefem:
[17] G. Mengaldo et al., “A concise guide to modelling the physics of Recipes for meshing, damping, and actuation,” IEEE Robotics and
embodiedintelligenceinsoftrobotics,”NatureReviewsPhysics,vol.4, AutomationLetters,vol.7,no.2,pp.5015–5022,2022.
no.9,pp.595–610,2022. [45] C.Agabitietal.,“Whole-armgraspingstrategyforsoftarmstocapture
[18] P.Scheggetal.,“Reviewongenericmethodsformechanicalmodeling, spacedebris,”in2023IEEEInternationalConferenceonSoftRobotics
simulation and control of soft robots,” Plos one, vol. 17, no. 1, p. (RoboSoft). IEEE,2023,pp.1–6.
e0251059,2022. [46] E. Me´nager et al., “Toward the use of proxies for efficient learning
[19] S.Sadatietal.,“Reducedordermodelingandmodelorderreduction manipulationandlocomotionstrategiesonsoftrobots,”IEEERobotics
for continuum manipulators: an overview,” Frontiers in Robotics and andAutomationLetters,2023.
AI,vol.10,2023. [47] F. Renda et al., “Dynamic model of a multibending soft robot arm
[20] X. Wang et al., “A survey for machine learning-based control of drivenbycables,”IEEETransactionsonRobotics,vol.30,no.5,pp.
continuum robots,” Frontiers in Robotics and AI, vol. 8, p. 730330, 1109–1122,2014.
2021. [48] M.Gazzolaetal.,“Forwardandinverseproblemsinthemechanicsof
[21] J. Wang et al., “Control strategies for soft robot systems,” Advanced soft filaments,” Royal Society open science, vol. 5, no. 6, p. 171628,
IntelligentSystems,vol.4,no.5,p.2100165,2022. 2018.
[22] C. Laschi et al., “Learning-based control strategies for soft robots: [49] J. Till et al., “Real-time dynamics of soft and continuum robots
Theory, achievements, and future challenges,” IEEE Control Systems basedoncosseratrodmodels,”TheInternationalJournalofRobotics
Magazine,vol.43,no.3,pp.100–113,2023. Research,vol.38,no.6,pp.723–746,2019.
[23] K.Chinetal.,“Machinelearningforsoftroboticsensingandcontrol,” [50] F.Rendaetal.,“Aunifiedmulti-soft-bodydynamicmodelforunder-
AdvancedIntelligentSystems,vol.2,no.6,p.1900171,2020. water soft robots,” The International Journal of Robotics Research,
[24] A.Centurellietal.,“Closed-loopdynamiccontrolofasoftmanipulator vol.37,no.6,pp.648–666,2018.
using deep reinforcement learning,” IEEE Robotics and Automation [51] X. Zhang et al., “Modeling and simulation of complex dynamic
Letters,vol.7,no.2,pp.4741–4748,2022. musculoskeletalarchitectures,”Naturecommunications,vol.10,no.1,
[25] F.Pique´etal.,“Controllingsoftroboticarmsusingcontinuallearning,” p.4825,2019.
IEEERoboticsandAutomationLetters,vol.7,no.2,pp.5469–5476, [52] D.Caradonnaetal.,“Modelandcontrolofr-softinvertedpendulum,”
2022. IEEERoboticsandAutomationLetters,vol.9,no.6,pp.5102–5109,
[26] D.Bianchietal.,“Softoss:Learningtothrowobjectswithasoftrobot,” 2024.
IEEERobotics&AutomationMagazine,2023. [53] E. Cosserat et al., “Sur la the´orie de l’e´lasticite´. Premier me´moire,”
[27] C.Alessietal.,“Pushingwithsoftroboticarmsviadeepreinforcement Annales de la Faculte´ des sciences de Toulouse pour les sciences
learning,”AdvancedIntelligentSystems,2024. mathe´matiques et les sciences physiques, vol. 1e se´rie, 10, no. 3-4,
[28] T. Mahl et al., “A variable curvature continuum kinematics for kine- pp.I1–I116,1896.
matic control of the bionic handling assistant,” IEEE transactions on [54] F. Boyer et al., “Dynamics of continuum and soft robots: A strain
robotics,vol.30,no.4,pp.935–949,2014. parameterization based approach,” IEEE Transactions on Robotics,
[29] C.DellaSantinaetal.,“Controlorientedmodelingofsoftrobots:the vol.37,no.3,pp.847–863,2020.
polynomial curvature case,” IEEE Robotics and Automation Letters, [55] F. Renda et al., “Discrete cosserat approach for multisection soft
vol.5,no.2,pp.290–298,2019. manipulatordynamics,”IEEETransactionsonRobotics,vol.34,no.6,
[30] O. Fischer et al., “Dynamic task space control enables soft manipu- pp.1518–1533,2018.
lators to perform real-world tasks,” Advanced Intelligent Systems, p. [56] ——,“Ageometricvariable-strainapproachforstaticmodelingofsoft
2200024,2022. manipulators with tendon and fluidic actuation,” IEEE Robotics and
[31] G. Lou et al., “Controlling soft robotic arms using hybrid modelling AutomationLetters,vol.5,no.3,pp.4006–4013,2020.
and reinforcement learning,” IEEE Robotics and Automation Letters, [57] A. T. Mathew et al., “Reduced order modeling of hybrid soft-rigid
2024. robotsusingglobal,local,andstate-dependentstrainparameterization,”
[32] Q.Xieetal.,“Simplifieddynamicalmodelandexperimentalverifica- The International Journal of Robotics Research, vol. 44, no. 1, pp.
tionofanunderwaterhydraulicsoftroboticarm,”SmartMaterialsand 129–154,2025.
Structures,vol.31,no.7,p.075011,2022. [58] E.Haieretal.,GeometricNumericalintegration:structure-preserving
[33] H. Habibi et al., “A lumped-mass model for large deformation con- algorithmsforordinarydifferentialequations. Springer,2006.
tinuum surfaces actuated by continuum robotic arms,” Journal of [59] R.M.Murrayetal.,AMathematicalIntroductiontoRoboticManip-
MechanismsandRobotics,vol.12,no.1,2020. ulation,1sted. USA:CRCPress,Inc.,1994.
[34] M.A.Grauleetal.,“Somo:Fastandaccuratesimulationsofcontinuum [60] A.T.Mathewetal.,“Sorosim:Amatlabtoolboxforhybridrigid–soft
robots in complex environments,” in 2021 IEEE/RSJ International robotsbasedonthegeometricvariable-strainapproach,”IEEERobotics
Conference on Intelligent Robots and Systems (IROS). IEEE, 2021, &AutomationMagazine,vol.30,no.3,pp.106–122,2022.
pp.3934–3941. [61] ——,“Analyticalderivativesofstrain-baseddynamicmodelforhybrid
[35] J.Austinetal.,“Titan:Aparallelasynchronouslibraryformulti-agent soft-rigid robots,” The International Journal of Robotics Research, p.
andsoft-bodyroboticsusingnvidiacuda,”in2020IEEEInternational 02783649251346209,2024.
Conference on Robotics and Automation (ICRA). IEEE, 2020, pp. [62] L. Xun et al., “Cosserat-rod based dynamic modeling of soft slender
7754–7760. robot interacting with environment,” IEEE Transactions on Robotics,
[36] B.Sicilianoetal.,“Robotics:modelling,planningandcontrol,2010,” 2024.
Citedon,vol.1,1994. [63] M. Bergou et al., “Discrete elastic rods,” in ACM SIGGRAPH 2008
[37] V. K. Venkiteswaran et al., “Shape and contact force estimation of papers. Association for Computing Machinery (ACM), 2008, pp.
continuummanipulatorsusingpseudorigidbodymodels,”Mechanism 1–12.
andmachinetheory,vol.139,pp.34–45,2019. [64] R.Courantetal.,“Onthepartialdifferenceequationsofmathematical
[38] R.Morimotoetal.,“Model-freereinforcementlearningwithensemble physics,” IBM journal of Research and Development, vol. 11, no. 2,
for a soft continuum robot arm,” in 2021 IEEE 4th International pp.215–234,1967.
ConferenceonSoftRobotics(RoboSoft). IEEE,2021,pp.141–148. [65] N.Naughtonetal.,“Elastica:Acompliantmechanicsenvironmentfor
[39] ——,“Characterizationofcontinuumrobotarmsunderreinforcement soft robotic control,” IEEE Robotics and Automation Letters, vol. 6,
learning and derived improvements,” Frontiers in Robotics and AI, no.2,pp.3389–3396,2021.
vol.9,p.895388,2022. [66] A. E. H. Love, A treatise on the mathematical theory of elasticity.
[40] E.Todorovetal.,“Mujoco:Aphysicsengineformodel-basedcontrol,” Cambridge,England:CambridgeUniversityPress,1906.
in 2012 IEEE/RSJ international conference on intelligent robots and [67] O. M. O’Reilly, Modeling nonlinear problems in the mechanics of
systems. IEEE,2012,pp.5026–5033. stringsandrods. Springer,2017.

24
[68] B. D. Coleman et al., “On the dynamics of rods in the theory of [94] ——, “Dynamic modeling of soft manipulators actuated by twisted-
kirchhoff and clebsch,” Archive for rational mechanics and analysis, and-coiled actuators,” in 2018 IEEE Conference on Decision and
vol.121,no.4,pp.339–359,1993. Control(CDC). IEEE,2018.
[69] S.Timoshenko,Historyofstrengthofmaterials:withabriefaccount [95] A. Doroudchi et al., “Dynamic modeling of a hydrogel-based con-
ofthehistoryoftheoryofelasticityandtheoryofstructures. Courier tinuum robotic arm with experimental validation,” in 2020 3rd IEEE
Corporation,1983. International Conference on Soft Robotics (RoboSoft). IEEE, 2020,
[70] A.Doroudchietal.,“Decentralizedcontrolofdistributedactuationin pp.695–701.
a segmented soft robot arm,” in 2018 IEEE Conference on Decision [96] J.Maetal.,“Dynamicsmodelingofasoftarmunderthecosseratthe-
andControl(CDC). IEEE,2018,pp.7002–7009. ory,”in2021IEEEInternationalConferenceonReal-timeComputing
[71] M.P.doCarmo,Differentialgeometryofcurvesandsurfaces. Prentice andRobotics(RCAR). IEEE,2021.
Hall,1976. [97] P.Wangetal.,“Generalkinetostaticmodelinganddeformationanalysis
[72] S.Timoshenkoetal.,TheoryofElasticity,2nded. McGraw-HillBook ofatwo-modulerod-drivencontinuumrobotwithfrictionconsidered,”
Company,1951. ChineseJournalofMechanicalEngineering,vol.36,no.1,p.68,2023.
[73] F. Renda et al., “Dynamics and control of soft robots with implicit [98] A.Jalalietal.,“Dynamicmodelingoftendon-drivenco-manipulative
strainparametrization,”IEEERoboticsandAutomationLetters,vol.9, continuum robots,” IEEE Robotics and Automation Letters, vol. 7,
no.3,pp.2782–2789,2024. no.2,pp.1643–1650,2021.
[74] B. He et al., “An analytic method for the kinematics and dynamics [99] M.Dehghanietal.,“Dynamicsmodelingofacontinuumroboticarm
of a multiple-backbone continuum robot,” International Journal of withacontactpointinplanargrasp,”JournalofRobotics,vol.2014,
AdvancedRoboticSystems,vol.10,no.1,p.84,2013. 2014.
[75] L.Lietal.,“Shapemodelingofaparallelsoftpanelcontinuumrobot,” [100] A. Hooshiar et al., “Analytical tip force estimation on tendon-driven
in2018IEEEInternationalConferenceonRoboticsandBiomimetics catheters through inverse solution of cosserat rod model,” in 2021
(ROBIO). IEEE,2018,pp.367–372. IEEE/RSJInternationalConferenceonIntelligentRobotsandSystems
[76] Y. Wenlong et al., “Mechanics-based kinematic modeling of a con- (IROS). IEEE,2021,pp.1829–1834.
tinuum manipulator,” in 2013 IEEE/RSJ International Conference on [101] W. Amehri et al., “Workspace boundary estimation for soft manipu-
IntelligentRobotsandSystems. IEEE,2013. latorsusingacontinuationapproach,”IEEERoboticsandAutomation
[77] K.M.dePayrebruneetal.,“Onconstitutiverelationsforarod-based Letters,vol.6,no.4,pp.7169–7176,2021.
model of a pneu-net bending actuator,” Extreme Mechanics Letters, [102] Q.Xiaoetal.,“Kinematicsandstiffnessmodelingofsoftrobotwith
vol.8,pp.38–46,2016. aconcentricbackbone,”JournalofMechanismsandRobotics,vol.15,
[78] B.JanizadehHajietal.,“Steady-statedynamicanalysisofanonlinear no.5,p.051011,2023.
fluidic soft actuator,” Journal of Vibration and Control, vol. 29, no. [103] P. Molaei et al., “Cable decoupling and cable-based stiffening of
7-8,pp.1606–1625,2023. continuumrobots,”IEEEAccess,vol.10,pp.104852–104862,2022.
[79] G.Wuetal.,“Design,modeling,andworkspaceanalysisofanexten- [104] W.Zhaoetal.,“Sim-to-realtransferindeepreinforcementlearningfor
sible rod-driven parallel continuum robot,” Mechanism and Machine robotics:asurvey,”in2020IEEEsymposiumseriesoncomputational
Theory,vol.172,p.104798,2022. intelligence(SSCI). IEEE,2020,pp.737–744.
[80] H.Sadatietal.,“Reducedordervs.discretizedlumpedsystemmodels [105] Y. Fan et al., “A novel continuum robot with stiffness variation
withabsoluteandrelativestatesforcontinuummanipulators,”inRoyal capability using layer jamming: Design, modeling, and validation,”
StatisticsSocietyInternationalConference2019,2019. IEEEAccess,vol.10,pp.130253–130263,2022.
[81] Y.Lietal.,“Analyticformulationofkinematicsforaplanarcontinuum [106] M. Grube et al., “Simulation of soft robots with nonlinear material
parallelmanipulatorwithlarge-deflectionlinks,”JournalofIntelligent behavior using the cosserat rod theory,” in 8th European Congress
&RoboticSystems,vol.107,no.4,p.58,2023. on Computational Methods in Applied Sciences and Engineering,
[82] A. Gao et al., “Mechanical model of dexterous continuum manipu- ECCOMAS2022. SCIPEDIA,2022.
lators with compliant joints and tendon/external force interactions,” [107] S. S. Nalkenani et al., “Modelling of soft bending actuator using
IEEE/ASME Transactions on Mechatronics, vol. 22, no. 1, pp. 465– cosserat rod pdes,” in 2021 9th RSI International Conference on
475,2016. RoboticsandMechatronics(ICRoM). IEEE,2021.
[83] A.Tariverdietal.,“Dynamicmodelingofsoftcontinuummanipulators [108] K. M. De Payrebrune et al., “On the development of rod-based
using lie group variational integration,” Plos one, vol. 15, no. 7, p. models for pneumatically actuated soft robot arms: A five-parameter
e0236121,2020. constitutive relation,” International Journal of Solids and Structures,
[84] X. Zhou et al., “Flexing into motion: A locomotion mechanism for vol.120,pp.226–235,2017.
softrobots,”InternationalJournalofNon-LinearMechanics,vol.74, [109] S. Mbakop et al., “Inverse dynamics model-based shape control of
pp.7–17,2015. soft continuum finger robot using parametric curve,” IEEE Robotics
[85] G. Cicconofri et al., “A study of snake-like locomotion through the andAutomationLetters,vol.6,no.4,pp.8053–8060,2021.
analysis of a flexible robot model,” Proceedings of the Royal Society [110] W.S.Roneetal.,“Continuumrobotdynamicsutilizingtheprinciple
A: Mathematical, Physical and Engineering Sciences, vol. 471, no. ofvirtualpower,”IEEETransactionsonRobotics,vol.30,no.1,pp.
2184,p.20150054,2015. 275–287,2013.
[86] C. A. Daily-Diamond et al., “Dynamical analysis and development [111] M. Tummers et al., “Cosserat rod modeling of continuum robots
of a biologically inspired sma caterpillar robot,” Bioinspiration & from newtonian and lagrangian perspectives,” IEEE Transactions on
biomimetics,vol.12,no.5,p.056005,2017. Robotics,062023.
[87] H. Xiang et al., “Study on tetherless micro-soft robot based on [112] F.Rendaetal.,“A3dsteady-statemodelofatendon-drivencontinuum
magnetic elastic composite material,” in 2019 IEEE International soft manipulator inspired by the octopus arm,” Bioinspiration &
Conference on Mechatronics and Automation (ICMA). IEEE, 2019, biomimetics,vol.7,no.2,p.025006,2012.
pp.668–673. [113] ——, “Screw-based modeling of soft manipulators with tendon and
[88] B.A.Jonesetal.,“Three-dimensionalstaticsforcontinuumrobotics,” fluidicactuation,”JournalofMechanismsandRobotics,vol.9,no.4,
in2009IEEE/RSJInternationalConferenceonIntelligentRobotsand p.041012,2017.
Systems. IEEE,2009. [114] C. Armanini et al., “Discrete cosserat approach for closed-chain
[89] M. Giorelli et al., “A two dimensional inverse kinetics model of a soft robots: Application to the fin-ray finger,” IEEE Transactions on
cabledrivenmanipulatorinspiredbytheoctopusarm,”in2012IEEE Robotics,vol.37,no.6,pp.2083–2098,2021.
international conference on robotics and automation. IEEE, 2012, [115] M. K. Mishra et al., “Fractional-order bouc-wen hysteresis model
pp.3819–3824. for pneumatically actuated continuum manipulator,” Mechanism and
[90] M.Roshanfaretal.,“Hyperelasticmodelingandvalidationofhybrid- Machinetheory,vol.173,p.104841,2022.
actuated soft robot with pressure-stiffening,” Micromachines, vol. 14, [116] K.Oliver-Butleretal.,“Continuumrobotstiffnessunderexternalloads
2023. andprescribedtendondisplacements,”IEEETransactionsonRobotics,
[91] M. H. Namdar Ghalati et al., “Static modeling of soft reinforced vol.35,no.2,pp.403–419,2019.
bendingactuatorconsideringexternalforceconstraints,”SoftRobotics, [117] D. Trivedi et al., “Geometrically exact dynamic models for soft
vol.9,no.4,pp.776–787,2022. roboticmanipulators,”in2007IEEE/RSJInternationalConferenceon
[92] R. W. Odgen et al., Non-linear elastic deformations. Courier IntelligentRobotsandSystems. IEEE,2007,pp.1497–1502.
corporation,2013. [118] ——, “Geometrically exact models for soft robotic manipulators,”
[93] B. Pawlowski et al., “Modeling of soft manipulators with couplings IEEETransactionsonRobotics,vol.24,no.2,pp.773–780,2008.
betweenactuationsandbodydeformations,”in2018AnnualAmerican [119] M. Roshanfar et al., “Toward semi-autonomous stiffness adaptation
ControlConference(ACC). IEEE,2018. of pneumatic soft robots: Modeling and validation,” in 2021 IEEE
InternationalConferenceonAutonomousSystems(ICAS). IEEE,2021.

25
[120] S. Grazioso et al., “Analytic solutions for the static equilibrium con- [146] N. K. Uppalapati et al., “Parameter estimation and modeling of a
figurationsofexternallyloadedcantileversoftroboticarms,”in2018 pneumatic continuum manipulator with asymmetric building blocks,”
IEEE International Conference on Soft Robotics (RoboSoft). IEEE, in 2018 IEEE International Conference on Soft Robotics (RoboSoft).
2018,pp.140–145. IEEE,2018,pp.528–533.
[121] R. Berthold et al., “A preliminary study of soft material robotic [147] ——,“Designandmodelingofsoftcontinuummanipulatorsusingpar-
modelling: Finite element method and cosserat rod model,” in 2021 allelasymmetriccombinationoffiber-reinforcedelastomers,”Journal
9thinternationalconferenceoncontrol,mechatronicsandautomation ofMechanismsandRobotics,vol.13,no.1,2021.
(ICCMA). IEEE,2021,pp.7–13. [148] M. Ji et al., “Rapid design and analysis of microtube pneumatic
[122] M. Wiese et al., “Towards accurate modeling of modular soft pneu- actuators using line-segment and multi-segment euler–bernoulli beam
matic robots: from volume fem to cosserat rod,” in 2022 IEEE/RSJ models,”Micromachines,vol.10,no.11,p.780,2019.
International Conference on Intelligent Robots and Systems (IROS). [149] G. Gu et al., “Analytical modeling and design of generalized pneu-
IEEE,2022,pp.9371–9378. netsoftactuatorswiththree-dimensionaldeformations,”Softrobotics,
[123] J.Tilletal.,“Elasticstabilityofcosseratrodsandparallelcontinuum vol.8,no.4,pp.462–477,2021.
robots,”IEEETransactionsonRobotics,vol.33,no.3,pp.718–733, [150] F. Renda et al., “A sliding-rod variable-strain model for concentric
2017. tuberobots,”IEEERoboticsandAutomationLetters,vol.6,no.2,pp.
[124] C.B.Blacketal.,“Parallelcontinuumrobots:Modeling,analysis,and 3451–3458,2021.
actuation-basedforcesensing,”IEEETransactionsonRobotics,vol.34, [151] C. Wu et al., “A modeling of twisted and coiled polymer artificial
no.1,pp.29–47,2017. musclesbasedonelasticrodtheory,”inActuators,vol.9,no.2. MDPI,
[125] S. Lilge et al., “Kinetostatic modeling of tendon-driven parallel con- 2020,p.25.
tinuum robots,” IEEE Transactions on Robotics, vol. 39, no. 2, pp. [152] B. Mauze´ et al., “Micrometer positioning accuracy with a planar
1563–1579,2022. parallel continuum robot,” Frontiers in Robotics and AI, vol. 8, p.
[126] F. Boyer et al., “Locomotion dynamics for bio-inspired robots with 706070,2021.
softappendages:Applicationtoflappingflightandpassiveswimming,” [153] M.Forghanietal.,“Controlofuniflagellarsoftrobotsatlowreynolds
JournalofNonlinearScience,vol.27,pp.1121–1154,2017. numberusingbucklinginstability,”JournalofDynamicSystems,Mea-
[127] ——, “Statics and dynamics of continuum robots based on cosserat surement,andControl,vol.143,no.6,p.061004,2021.
rods and optimal control theories,” IEEE Transactions on Robotics, [154] A.A.Siposetal.,“Thelongestsoftroboticarm,”InternationalJournal
vol.39,no.2,pp.1544–1562,2022. ofNon-LinearMechanics,vol.119,p.103354,2020.
[128] A. Y. Alkayas et al., “Soft synergies: Model order reduction of [155] S.Pattanshettietal.,“Onthekinematicmodelofcontinuumrobotswith
hybrid soft-rigid robots via optimal strain parameterization,” IEEE spatiallyvaryingnonlinearstiffness,”in2019InternationalSymposium
TransactionsonRobotics,p.1–20,2024. onMedicalRobotics(ISMR). IEEE,2019,pp.1–7.
[129] ——, “Structure-preserving model order reduction of slender soft [156] Z.Chenetal.,“Modelanalysisofroboticsoftarmsincludingexternal
robots via autoencoder-parameterized strain,” IEEE Robotics and Au- forceeffects,”Micromachines,vol.13,no.3,p.350,2022.
tomationLetters,2025. [157] S. H. Sadati et al., “Control space reduction and real-time accurate
[130] D. C. Rucker et al., “A model for concentric tube continuum robots modelingofcontinuummanipulatorsusingritzandritz–galerkinmeth-
under applied wrenches,” in 2010 IEEE International Conference on ods,”IEEERoboticsandAutomationLetters,vol.3,no.1,pp.328–335,
RoboticsandAutomation. IEEE,2010,pp.1047–1052. 2017.
[131] ——,“Ageometricallyexactmodelforexternallyloadedconcentric- [158] H. B. Gilbert et al., “Validation of an extensible rod model for soft
tubecontinuumrobots,”IEEEtransactionsonrobotics,vol.26,no.5, continuummanipulators,”in20192ndIEEEInternationalConference
pp.769–780,2010. onSoftRobotics(RoboSoft). IEEE,2019,pp.711–716.
[132] J. Till et al., “A dynamic model for concentric tube robots,” IEEE [159] J.Garbulinskietal.,“Bendingpropertiesofanextensilefluidicartificial
TransactionsonRobotics,vol.36,no.6,pp.1704–1718,2020. muscle,”FrontiersinRoboticsandAI,vol.9,2022.
[133] J.Wangetal.,“Steeringamulti-armedroboticsheathusingeccentric [160] C.Alessietal.,“Ablationstudyofadynamicmodelfora3d-printed
precurved tubes,” in 2019 international conference on robotics and pneumaticsoftroboticarm,”IEEEAccess,2023.
automation(ICRA). IEEE,2019,pp.9834–9840. [161] W.Douetal.,“Designandmodelingofahybridsoftroboticmanipula-
[134] L. Wang et al., “Eccentric-tube robot (etr) modeling and validation,” torwithcompliantmechanism,”IeeeRoboticsandAutomationLetters,
in20208thIEEERAS/EMBSInternationalConferenceforBiomedical vol.8,no.4,pp.2301–2308,2023.
RoboticsandBiomechatronics(BioRob). IEEE,2020,pp.866–871. [162] N. N. Goldberg et al., “On planar discrete elastic rod models for the
[135] J.Wangetal.,“Eccentrictuberobotsasmultiarmedsteerablesheaths,” locomotion of soft robots,” Soft robotics, vol. 6, no. 5, pp. 595–610,
IEEETransactionsonRobotics,vol.38,no.1,pp.477–490,2021. 2019.
[136] G. Smoljkic et al., “Compliance computation for continuum types [163] F. Renda et al., “A general mechanical model for tendon-driven
of robots,” in 2014 IEEE/RSJ International Conference on Intelligent continuum manipulators,” in 2012 IEEE International Conference on
RobotsandSystems. IEEE,2014,pp.1066–1073. RoboticsandAutomation. IEEE,2012,pp.3813–3818.
[137] D. C. Rucker et al., “Statics and dynamics of continuum robots with [164] H. Wang et al., “Three-dimensional dynamics for cable-driven soft
general tendon routing and external loading,” IEEE Transactions on manipulator,”IEEE/ASMEtransactionsonmechatronics,vol.22,no.1,
Robotics,vol.27,no.6,pp.1033–1044,2011. pp.18–28,2016.
[138] M.Dehghanietal.,“Modelingofcontinuumrobotswithtwistedtendon [165] Y.Adagolodjoetal.,“Couplingnumericaldeformablemodelsinglobal
actuationsystems,”in2013FirstRSI/ISMInternationalConferenceon andreducedcoordinatesforthesimulationofthedirectandtheinverse
RoboticsandMechatronics(ICRoM). IEEE,2013,pp.14–19. kinematics of soft robots.” IEEE Robotics and Automation Letters,
[139] ——, “Modeling and control of a planar continuum robot,” in 2021.
IEEE/ASME (AIM) International Conference on Advanced Intelligent [166] H.-T. Ryu et al., “Application of cosserat rod theory to configuration
Mechatronics. IEEE,2011. estimationofcoionoscope,”in201815thInternationalConferenceon
[140] ——,“Compactmodelingofspatialcontinuumroboticarmstowards UbiquitousRobots(UR). IEEE,2018,pp.11–13.
real-timecontrol,”AdvancedRobotics,vol.28,no.1,pp.15–26,2014. [167] M. Ghafoori et al., “Modeling and experimental analysis of a multi-
[141] W. S. Rone et al., “Continuum robotic tail loading analysis for rodparallelcontinuumrobotusingthecosserattheory,”Roboticsand
mobile robot stabilization and maneuvering,” in International design AutonomousSystems,vol.134,p.103650,2020.
engineering technical conferences and computers and information in [168] Y. Chen et al., “A variable curvature model for multi-backbone
engineeringconference,vol.46360. AmericanSocietyofMechanical continuum robots to account for inter-segment coupling and external
Engineers,2014,p.V05AT08A009. disturbance,”IEEERoboticsandAutomationLetters,vol.6,no.2,pp.
[142] D.Xuetal.,“Modellingandbendingcontrolofflexiblearmbasedon 1590–1597,2021.
bionicoctopus,”in2017ChineseAutomationCongress(CAC). IEEE, [169] M. Bartholdt et al., “A parameter identification method for static
2017,pp.7162–7167. cosserat rod models: Application to soft material actuators with ex-
[143] L. Niu et al., “Closed-form equations and experimental verification teroceptive sensors,” in 2021 IEEE/RSJ International Conference on
for soft robot arm based on cosserat theory,” in 2019 IEEE/RSJ IntelligentRobotsandSystems(IROS). IEEE,2021,pp.624–631.
International Conference on Intelligent Robots and Systems (IROS). [170] S. Grazioso et al., “A geometrically exact model for soft contin-
IEEE,2019,pp.6630–6635. uum robots: The finite element deformation space formulation,” Soft
[144] M. T. Chikhaoui et al., “Comparison of modeling approaches for a robotics,vol.6,no.6,pp.790–811,2019.
tendonactuatedcontinuumrobotwiththreeextensiblesegments,”IEEE [171] M. Bentley et al., “Safer motion planning of steerable needles via a
RoboticsandAutomationLetters,vol.4,no.2,pp.989–996,2019. shaft-to-tissue force model,” Journal of Medical Robotics Research,
[145] F. Janabi-Sharifi et al., “Cosserat rod-based dynamic modeling of vol.8,no.01n02,2023.
tendon-drivencontinuumrobots:Atutorial,”IEEEAccess,vol.9,pp.
68703–68719,2021.

26
[172] E. G. Hemingway et al., “Continuous models for peristaltic locomo- Conference on Intelligent Robots and Systems (IROS). IEEE, 2022,
tion with application to worms and soft robots,” Biomechanics and pp.10967–10974.
ModelinginMechanobiology,vol.20,no.1,pp.5–30,2021. [197] B. Caasenbrood et al., “Energy-based control for soft manipulators
[173] H. Nguewou-Hyousse et al., “Distributed control of a planar discrete usingcosserat-beammodels.”inICINCO,2021,pp.311–319.
elastic rod model for caterpillar-inspired locomotion,” in ASME 2019 [198] ——,“Energy-shapingcontrollersforsoftrobotmanipulatorsthrough
DynamicSystemsandControlConference. ASME,2019. port-hamiltoniancosseratmodels,”SNComputerScience,vol.3,no.6,
[174] S. H. Sadati et al., “A geometry deformation model for braided p.494,2022.
continuummanipulators,”FrontiersinRoboticsandAI,vol.4,p.22, [199] H.-S.Changetal.,“Energy-shapingcontrolofamuscularoctopusarm
2017. movinginthreedimensions,”ProceedingsoftheRoyalSocietyA,vol.
[175] ——, “Mechanics of continuum manipulators, a comparative study 479,no.2270,p.20220593,2023.
of five methods with experiments,” in Towards Autonomous Robotic [200] D. Tiwari et al., “Discrete geometric control of planar flexible link
Systems: 18th Annual Conference, TAROS 2017, Guildford, UK, July manipulators,” IFAC-PapersOnLine, vol. 56, no. 2, pp. 2865–2870,
19–21,2017,Proceedings18. Springer,2017,pp.686–702. 2023.
[176] X. Wang et al., “Dynamics modeling and verification of parallel [201] A. A. Alqumsan et al., “Robust control of continuum robots using
extensible soft robot based on cosserat rod theory,” in 2022 IEEE cosserat rod theory,” Mechanism and Machine Theory, vol. 131, pp.
International Conference on Automation Science and Engineering 48–61,2019.
(CASE). IEEE,2022. [202] X. Li et al., “Modeling and experimental validation for a large-scale
[177] F.Lampingetal.,“Anovelandpracticableapproachfordetermining and ultralight inflatable robotic arm,” IEEE/ASME Transactions on
thebeamparametersofsoftpneumaticmulti-chamberbendingactua- Mechatronics,vol.27,no.1,pp.418–429,2021.
tors,”AppliedSciences,vol.13,no.5,2023. [203] M. K. Mishra et al., “Trajectory tracking control of a pneumatically
[178] Sachinetal.,“Analyticalmodelingofsoftpneu-netactuatorsubjected actuatedcontinuummanipulatorinthepresenceofobstaclesbyusing
toplanartipcontact,”IEEETransactionsonRobotics,vol.38,no.5, terminalslidingmodecontrol,”ISAtransactions,vol.143,pp.79–93,
pp.2720–2733,2022. 2023.
[179] E.Flores-Mart´ınezetal.,“Softpneumaticactuatorinspiredonflexion- [204] M. K. Soltani et al., “A soft robotics nonlinear hybrid position/force
extension motion trajectory of the human fingers,” in USCToMM controlfortendondrivencatheters,”InternationalJournalofControl,
Symposium on Mechanical Systems and Robotics. Springer, 2022, AutomationandSystems,vol.15,pp.54–63,2017.
pp.168–177. [205] A.S.Barbosaetal.,“Motionplanningofafish-likepiezoelectricactu-
[180] S. R. Eugster et al., “Soft pneumatic actuator model based on a atedrobotusingmodel-basedpredictivecontrol,”JournalofVibration
pressure-dependent spatial nonlinear rod theory,” IEEE robotics and andControl,vol.29,no.1-2,pp.411–427,2023.
automationletters,vol.7,no.2,pp.2471–2478,2022. [206] T.Wangetal.,“Optimalcontrolofasoftcyberoctopusarm,”in2021
[181] C.Sunetal.,“Ahybridcontinuumrobotbasedonpneumaticmuscles AmericanControlConference(ACC). IEEE,2021,pp.4757–4764.
with embedded elastic rods,” Journal of Mechanical Engineering [207] S.H.Hashemietal.,“Robustglobalstabilizationofaerialcontinuum
Science,vol.234,no.1,pp.318–328,2019. manipulationsystemsviahybridfeedback,”ISAtransactions,vol.138,
[182] R.Bertholdetal.,“Investigationoflateralcompressioneffectsinfiber pp.160–167,2023.
reinforcedsoftpneumaticactuators,”in2022InternationalConference [208] A. Ataka et al., “Observer-based control of inflatable robot with
onElectrical,Computer,CommunicationsandMechatronicsEngineer- variable stiffness,” in 2020 IEEE/RSJ International Conference on
ing(ICECCME). IEEE,2022. IntelligentRobotsandSystems(IROS). IEEE,2020,pp.8646–8652.
[183] S. P. Hanza et al., “Mechanics of fiber reinforced soft manipulators [209] H.Bezawadaetal.,“Shapereconstructionofsoftmanipulatorsusing
basedoninhomogeneouscosseratrodtheory,”MechanicsofAdvanced vision and imu feedback,” IEEE Robotics and Automation Letters,
MaterialsandStructures,2023. vol.7,no.4,pp.9589–9596,2022.
[184] S. Liu et al., “Modeling of a soft actuator with a semicircular [210] A.AlBeladietal.,“Vision-basedshapereconstructionofsoftcontin-
cross section under gravity and external load,” IEEE Transactions on uum arms using a geometric strain parametrization,” in 2021 IEEE
IndustrialElectronics,vol.7,no.5,2023. InternationalConferenceonRoboticsandAutomation(ICRA). IEEE,
[185] P.Pustinaetal.,“Inputdecouplingoflagrangiansystemsviacoordinate 2021,pp.11753–11759.
transformation: General characterization and its application to soft [211] D. Trivedi et al., “Model-based shape estimation for soft robotic
robotics,”IEEEtransactionsonrobotics,vol.40,pp.2098–2110,2024. manipulators:Theplanarcase,”JournalofMechanismsandRobotics,
[186] P. Borja et al., “Energy-based shape regulation of soft robots with vol.6,no.2,p.021005,2014.
unactuated dynamics dominated by elasticity,” in 2022 IEEE 5th [212] M.D.Grissometal.,“Designandexperimentaltestingoftheoctarm
international conference on soft robotics (RoboSoft). IEEE, 2022, soft robot manipulator,” in Unmanned systems technology VIII, vol.
pp.396–402. 6230. SPIE,2006,pp.491–500.
[187] ——, “On the role of coupled damping and gyroscopic forces in [213] H. Donat et al., “Real-time shape estimation for concentric tube
the stability and performance of mechanical systems,” IEEE Control continuum robots with a single force/torque sensor,” Frontiers in
SystemsLetters,vol.6,pp.3433–3438,2022. RoboticsandAI,vol.8,p.734033,2021.
[188] P. Pustina et al., “P-sati-d shape regulation of soft robots,” IEEE [214] S. Lilge et al., “Continuum robot state estimation using gaussian
RoboticsandAutomationLetters,vol.8,no.1,pp.1–8,2022. process regression on se (3),” The International Journal of Robotics
[189] A.Atakaetal.,“Model-basedposecontrolofinflatableeversionrobot Research,vol.41,no.13-14,pp.1099–1120,2022.
withvariablestiffness,”IEEERoboticsandAutomationLetters,vol.5, [215] V. Aloi et al., “Estimating forces along continuum robots,” IEEE
no.2,pp.3398–3405,2020. RoboticsandAutomationLetters,vol.7,no.4,pp.8877–8884,2022.
[190] I.A.Gravagneetal.,“Largedeflectiondynamicsandcontrolforplanar [216] P. L. Anderson et al., “Continuum reconfigurable parallel robots for
continuumrobots,”IEEE/ASMEtransactionsonmechatronics,vol.8, surgery: Shape sensing and state estimation with uncertainty,” IEEE
no.2,pp.299–307,2003. roboticsandautomationletters,vol.2,no.3,pp.1617–1624,2017.
[191] M. Richter et al., “Multi-point orientation control of discretely- [217] J.M.Fergusonetal.,“Unifiedshapeandexternalloadstateestimation
magnetizedcontinuummanipulators,”IEEERoboticsandautomation for continuum robots,” IEEE Transactions on Robotics, vol. 40, pp.
letters,vol.6,no.2,pp.3607–3614,2021. 1813–1827,2024.
[192] F.Campisanoetal.,“Closed-loopcontrolofsoftcontinuummanipula- [218] C.Shietal.,“Shapesensingtechniquesforcontinuumrobotsinmin-
torsundertipfolloweractuation,”TheInternationaljournalofrobotics imallyinvasivesurgery:Asurvey,”IEEETransactionsonBiomedical
research,vol.40,no.6-7,pp.923–938,2021. Engineering,vol.64,no.8,pp.1665–1678,2016.
[193] F.Rendaetal.,“Geometrically-exactinversekinematiccontrolofsoft [219] M. Yousefi et al., “Model-aided 3d shape and force estimation of
manipulatorswithgeneralthreadlikeactuators’routing,”IEEERobotics continuum robots based on cosserat rod theory and using a magnetic
andAutomationLetters,vol.7,no.3,pp.7311–7318,2022. localization system,” Intelligent Service Robotics, vol. 16, no. 4, pp.
[194] A.Doroudchietal.,“Configurationtrackingforsoftcontinuumrobotic 471–484,2023.
armsusinginversedynamiccontrolofacosseratrodmodel,”in2021 [220] T. Zheng et al., “Full state estimation of continuum robots from tip
IEEE4thInternationalConferenceonSoftRobotics(RoboSoft). IEEE, velocities:Acosserat-theoreticboundaryobserver,”IEEETransactions
2021,pp.207–214. onAutomaticControl,2024.
[195] V. Falkenhahn et al., “Dynamic control of the bionic handling assis- [221] ——, “Estimating infinite-dimensional continuum robot states from
tant,” IEEE/ASME Transactions on Mechatronics, vol. 22, no. 1, pp. thetip,”in2024IEEE7thInternationalConferenceonSoftRobotics
6–17,2016. (RoboSoft). IEEE,2024,pp.572–578.
[196] C. Rucker et al., “Task-space control of continuum robots using [222] D. Feliu-Talegon et al., “Dynamic shape estimation of tendon-driven
underactuated discrete rod models,” in 2022 IEEE/RSJ International softmanipulatorsviaactuationreadings,”IEEERoboticsandAutoma-
tionLetters,2024.

27
[223] T. G. Thuruthel et al., “Learning dynamic models for open loop IEEE International Conference on Soft Robotics (RoboSoft). IEEE,
predictive control of soft robotic manipulators,” Bioinspiration & 2023,pp.1–7.
biomimetics,vol.12,no.6,p.066003,2017. [232] T.Wallinetal.,“3dprintingofsoftroboticsystems,”NatureReviews
[224] X. Wang et al., “A data-efficient model-based learning framework Materials,vol.3,no.6,pp.84–100,2018.
for the closed-loop control of continuum robots,” in 2022 IEEE 5th [233] S.Terrynetal.,“Self-healingsoftpneumaticrobots,”ScienceRobotics,
International Conference on Soft Robotics (RoboSoft). IEEE, 2022, vol.2,no.9,2017.
pp.247–254. [234] Y. Sun et al., “Real-time dynamics of soft manipulators with cross-
[225] N.Kushawahaetal.,“Domaintranslationofasoftroboticarmusing sectional inflation: application to the octopus muscular hydrostat,”
conditional cycle generative adversarial network,” in 2025 8th Inter- ProceedingsoftheRoyalSocietyA,vol.481,no.2314,p.20240642,
national Conference on Robotic Systems and Applications (ICRSA), 2025.
2025. [235] P.Raoetal.,“Towardscontact-aidedmotionplanningfortendon-driven
[226] R. S. Sutton et al., Reinforcement learning: An introduction. MIT continuum robots,” IEEE Robotics and Automation Letters, vol. 9,
press,2018. no.5,pp.4687–4694,2024.
[227] S. Satheeshbabu et al., “Open loop position control of soft contin- [236] M. Lutter et al., “Combining physics and deep learning to learn
uum arm using deep reinforcement learning,” in 2019 International continuous-time dynamics models,” The International Journal of
Conference on Robotics and Automation (ICRA). IEEE, 2019, pp. RoboticsResearch,vol.42,no.3,pp.83–107,2023.
5133–5139. [237] J. Liu et al., “Physics-informed neural networks to model and con-
[228] V.Mnihetal.,“Playingatariwithdeepreinforcementlearning,”arXiv trol robots: A theoretical and experimental investigation,” Advanced
preprintarXiv:1312.5602,2013. IntelligentSystems,vol.6,no.5,p.2300385,2024.
[229] S. Satheeshbabu et al., “Continuous control of a soft continuum arm [238] N. Pagliarani et al., “Softtex: Soft robotic arm with learning-based
using deep reinforcement learning,” in 2020 3rd IEEE International textileproprioception,”IEEERoboticsandAutomationLetters,vol.10,
ConferenceonSoftRobotics(RoboSoft). IEEE,2020,pp.497–503. no.4,pp.3779–3786,2025.
[230] N.K.Uppalapatietal.,“Aberrypickingrobotwithahybridsoft-rigid [239] T.M.Moerlandetal.,“Model-basedreinforcementlearning:Asurvey,”
arm:Designandtaskspacecontrol.”inRobotics:ScienceandSystems, FoundationsandTrends®inMachineLearning,vol.16,no.1,pp.1–
2020,p.95. 118,2023.
[231] C.Alessietal.,“Learningacontrollerforsoftroboticarmsandtesting [240] J. Ibarz et al., “How to train your robot with deep reinforcement
its generalization to new observations, dynamics, and tasks,” in 2023 learning: lessons we have learned,” The International Journal of
RoboticsResearch,vol.40,no.4-5,pp.698–721,2021.