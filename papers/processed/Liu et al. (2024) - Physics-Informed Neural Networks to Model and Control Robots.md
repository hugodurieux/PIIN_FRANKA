| RESEARCH |     | ARTICLE |     |     |     |     |     |     |     |     |     |     |     |     |     |
| -------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
www.advintellsyst.com
| Physics-Informed |       |               |        | Neural |        | Networks         |         |     | to  | Model         |     | and | Control |     |     |
| ---------------- | ----- | ------------- | ------ | ------ | ------ | ---------------- | ------- | --- | --- | ------------- | --- | --- | ------- | --- | --- |
| Robots:          |       | A Theoretical |        |        |        | and Experimental |         |     |     | Investigation |     |     |         |     |     |
| Jingyue          | Liu,* | Pablo         | Borja, | and    | Cosimo | Della            | Santina |     |     |               |     |     |         |     |     |
specifically
|     |     |     |     |     |     |     |     |     |     | a rising | trend | in  | robotics | to  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----- | --- | -------- | --- | --- |
This work concerns the application of physics-informed neural networks to the incorporate geometric priors into data-
modeling and control of complex robotic systems. Achieving this goal requires driven methods to optimize learning
efficiency.[13–15]Thisapproachprovesespe-
| extending | physics-informed |     | neural | networks | to  | handle nonconservative |     | effects. |     |     |     |     |     |     |     |
| --------- | ---------------- | --- | ------ | -------- | --- | ---------------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
ciallyadvantageousforhigh-leveltasksthat
| These learned |     | models are | proposed | to  | combine | with model-based |     | controllers |     |     |     |     |     |     |     |
| ------------- | --- | ---------- | -------- | --- | ------- | ---------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
neednotengagewiththesystem’sphysics.
originallydevelopedwithfirst-principlemodelsinmind.Bycombiningstandard
|     |     |     |     |     |     |     |     |     |     | Physics-informed |     |     | neural | networks |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | ------ | -------- | --- |
(PINNs),[16–18]infusingfundamentalphys-
andnewtechniques,precisecontrolperformancecanbeachievedwhileproving
theoreticalstabilitybounds.Thesevalidationsincludereal-worldexperimentsof ics knowledge into their architecture and
|     |     |     |     |     |     |     |     |     |     | training, | have | found | success | in  | various |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | ---- | ----- | ------- | --- | ------- |
motionpredictionwithasoftrobotandtrajectorytrackingwithaFrankaEmika
fields
| Panda manipulator. |     |     |     |     |     |     |     |     |     |     | outside | robotics, | from | earth | science |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------- | ---- | ----- | ------- |
tomaterialsscience.[19–22]Inrobotics,inte-
|     |     |     |     |     |     |     |     |     |     | gration | of  | Lagrangian |     | or Hamiltonian |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ---------- | --- | -------------- | --- |
mechanicswithDLhasyieldedmodelslike
Lagrangianneuralnetworks(LNNs)[23]andHamiltonianneural
1. Introduction
(HNN).[24]
|     |     |     |     |     |     |     | networks |     |     | Several | extensions |     | have been | proposed | in  |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | ------- | ---------- | --- | --------- | -------- | --- |
Deep learning (DL) has made significant strides across various the literature, for example, including contact models[25] or pro-
fields,withroboticsbeingasalientexample.DLhasexcelledin posing graph formulations.[26] The potential of LNNs and
|            |     |               |     |                |                    |     | HNNs | in learning |     | the dynamics |     | of basic | physical | systems | has |
| ---------- | --- | ------------- | --- | -------------- | ------------------ | --- | ---- | ----------- | --- | ------------ | --- | -------- | -------- | ------- | --- |
| tasks such | as  | vision-guided |     | navigation,[1] | grasp-planning,[2] |     |      |             |     |              |     |          |          |         |     |
studies.[18,27–29]
human–robot interaction,[3] and even design.[4] Despite this, been demonstrated in various However, the
theapplicationofDLtogeneratemotorintelligenceinphysical exploration of these techniques in modeling intricate robotic
|         |         |          |      |               |           |         | structures, |     | especially | with | real-world | data, | is  | still in its | early |
| ------- | ------- | -------- | ---- | ------------- | --------- | ------- | ----------- | --- | ---------- | ---- | ---------- | ----- | --- | ------------ | ----- |
| systems | remains | limited. | Deep | reinforcement | learning, | in par- |             |     |            |      |            |       |     |              |       |
stages.Notably,[30]appliedthesemethodstoaposition-controlled
| ticular, | has shown | the | potential | to outperform |     | traditional |     |     |     |     |     |     |     |     |     |
| -------- | --------- | --- | --------- | ------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
approachesinsimulations.[5–7]However,itstransfertophysical robotwithfourdegreesoffreedom,whichrepresentsarelatively
applicationshasbeenprimarilyhamperedbytheprerequisiteof less complex system in comparison to contemporary
|             |      |           | environment.[8–10] |     |     |     | manipulators. |           |       |      |     |              |     |             |     |
| ----------- | ---- | --------- | ------------------ | --- | --- | --- | ------------- | --------- | ----- | ---- | --- | ------------ | --- | ----------- | --- |
| pretraining | in a | simulated |                    |     |     |     |               |           |       |      |     |              |     |             |     |
|             |      |           |                    |     |     |     |               | This work | deals | with | the | experimental |     | application | of  |
Thecentraldrawbackofgeneral-purposeDLliesinitssample
|               |              |      |          |          |             |                | PINN              | to rigid | and         | soft continuum |                | robots.[31] |        | Such endeavor |         |
| ------------- | ------------ | ---- | -------- | -------- | ----------- | -------------- | ----------------- | -------- | ----------- | -------------- | -------------- | ----------- | ------ | ------------- | ------- |
| inefficiency, | stemming     | from | the      | need to  | distill     | all aspects of | a                 |          |             |                |                |             |        |               |         |
|               |              |      |          |          |             |                | requiredmodifying |          |             | LNN and        | HNN            | to fix      | three  | issues that   | pre-    |
| task from     | data.[11,12] | In   | response | to these | challenges, | there is       |                   |          |             |                |                |             |        |               |         |
|               |              |      |          |          |             |                | vented            | their    | application | to             | these          | systems:    | 1) the | lack of       | energy  |
|               |              |      |          |          |             |                | dissipation       |          | mechanism;  | 2)             | the assumption |             | that   | control       | actions |
arecollocatedonthemeasuredconfigurations;and3)theneed
J.Liu,C.DellaSantina
fordirectaccelerationmeasurements,whicharenoncausaland
DepartmentofCognitiveRobotics
|     |     |     |     |     |     |     | require | numerical |     | differentiation. |     | For | issue | (3), we borrow | a   |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --- | ---------------- | --- | --- | ----- | -------------- | --- |
DelftUniversityofTechnology
2628CDDelft,TheNetherlands
|     |     |     |     |     |     |     | strategy | proposed |     | in refs. | [32,33], | which | relies | on forward | inte- |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------- | --- | -------- | -------- | ----- | ------ | ---------- | ----- |
E-mail:J.Liu-14@tudelft.nl
gratingthedynamics,whilefor(1)and(2),weproposeinnovative
| P.Borja |     |     |     |     |     |     | solutions. |     |     |     |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
SchoolofEngineering,ComputingandMathematics
|     |     |     |     |     |     |     |     | Furthermore, |     | we exploit | a central | advantage |     | of LNNs | and |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ---------- | --------- | --------- | --- | ------- | --- |
UniversityofPlymouth
|     |     |     |     |     |     |     | HNNs | compared |     | to other | learning | techniques; |     | the fact | that |
| --- | --- | --- | --- | --- | --- | --- | ---- | -------- | --- | -------- | -------- | ----------- | --- | -------- | ---- |
PL48AAPlymouth,UK
C.DellaSantina thelearnedmodelhasthemathematicalstructurethatisusually
InstituteofRoboticsandMechatronicsGermanAerospaceCenter(DLR) assumed in robots and mechanical systems control. By forcing
82234Oberpfaffenhofen,Germany such a representation, we use model-based strategies originally
developedforfirstprinciplemodels[34–36]toobtainprovablysta-
TheORCIDidentificationnumber(s)fortheauthor(s)ofthisarticle
canbefoundunderhttps://doi.org/10.1002/aisy.202300385. ble performance with guarantees of robustness.
|     |     |     |     |     |     |     |     | The use | of PINNs | in control |     | has only | recently | started | to be |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | -------- | ---------- | --- | -------- | -------- | ------- | ----- |
©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-
|           |      |            |        |         |           |              | explored. | Recent |     | investigations[33,37,38] |     |     | focused | on combining |     |
| --------- | ---- | ---------- | ------ | ------- | --------- | ------------ | --------- | ------ | --- | ------------------------ | --- | --- | ------- | ------------ | --- |
| VCH GmbH. | This | is an open | access | article | under the | terms of the |           |        |     |                          |     |     |         |              |     |
Creative Commons Attribution License, which permits use, distribution PINNswithmodelpredictivecontrol(MPC),thusnotexploiting
and reproduction in any medium, provided the original work is themathematicalstructureofthelearnedequations.Indeed,this
properlycited.
|     |     |     |     |     |     |     | strategyispart |     | ofan | increasinglyestablished |     |     | trendseekingthe |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ---- | ----------------------- | --- | --- | --------------- | --- | --- |
DOI: 10.1002/aisy.202300385 combination of (non-PI and nondeep) learned models with
Adv.Intell.Syst.2024,6,2300385 2300385 (1 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     |     |     |     |     |     |     |     |     |     | www.advintellsyst.com |     |     |
| --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- |
MPC.[39,40] Applications to control partial differential equations L ¼MSEððq˙,p˙Þ,ðq ˆ˙,p ˆ˙ÞÞ (2)
HNN
| are | discussed | in refs. | [41–44], | while | an application | to  | robotics |     |     |     |     |     |     |     |     |
| --- | --------- | -------- | -------- | ----- | -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
is investigated in simulation in ref. [45]. Weusefullyconnectedneuralnetworkswithmultiplelayers
Preliminary investigations in other model-based techniques ofneuronswithassociatedweightstolearntheLagrangianorthe
areprovidedinrefs.[30,46],where,however,controllersarepro- Hamiltonian, as shown in Figure 1.
videdwithoutanyguaranteeofstabilityorrobustnessandformu-
specific
| lated | for        | cases. |         |                     |     |          |           |             |            |      |     |      |     |     |     |
| ----- | ---------- | ------ | ------- | ------------------- | --- | -------- | --------- | ----------- | ---------- | ---- | --- | ---- | --- | --- | --- |
|       |            |        |         |                     |     |          |           | 2.3. Limits | of Classic | LNNs | and | HNNs |     |     |     |
| To    | summarize, |        | in this | work, we contribute |     | to state | of art in |             |            |      |     |      |     |     |     |
PINNsandroboticswiththefollowing:1)anapproachtoinclude
Notethatbothlossfunctionsrelyonmeasuringderivativesofthe
dissipationandallowfornon-collocatedcontrolactionsinLNNs
|     |     |     |     |     |     |     |     | stateq¨and | p˙, which—by |     | definition | of state—cannot |     | be  | directly |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------------ | --- | ---------- | --------------- | --- | --- | -------- |
andHNNs,solvingissues(1)and(2);2)controllersforregulation
measured.Thisissueiseasilycircumventedinsimulationbythe
| and | tracking, | grounded | in  | classic nonlinear |     | control that | exploit |     |     |     |     |     |     |     |     |
| --- | --------- | -------- | --- | ----------------- | --- | ------------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
useofanoncausalsensor.Yet,thisisnotafeasiblesolutionwith
| the   | mathematical |     | structure | of the learned | models. | For      | the first   |              |              |              |             |              |     |                |     |
| ----- | ------------ | --- | --------- | -------------- | ------- | -------- | ----------- | ------------ | ------------ | ------------ | ----------- | ------------ | --- | -------------- | --- |
|       |              |     |           |                |         |          |             | physical     | experiments. |              | An unrobust | alternative  |     | is to estimate |     |
| time, | we prove     | the | stability | and robustness |         | of these | strategies; |              |              |              |             |              |     |                |     |
|       |              |     |           |                |         |          |             | these values | from         | measurements |             | of positions |     | and velocities |     |
and3)simulationsandexperimentsonarticulatedandsoftcon-
numerically.Thisrelatestoissue(3)statedintheintroduction.
authors’
| tinuum | robotic | systems. | To  | the | best | knowledge, | these |     |     |     |     |     |     |     | ∈ℝN |
| ------ | ------- | -------- | --- | --- | ---- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
arethefirstvalidationofPINNandPINN-basedcontrolapplied Moreover,existingLNNsandHNNsassumethatF ext is
directlymeasured.Thisisareasonablehypothesisonlyifthesys-
| to complex |     | mechanical | systems. |     |     |     |     |     |     |     |     |     |     |     |     |
| ---------- | --- | ---------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
temisconservative,fullyactuated,andtheactuationiscollocated.
Thefirstcharacteristicisneverfulfilledbyrealsystems,whilethe
|     |     |     |     |     |     |     |     | second and | the | third are | very | restrictive | outside | when | dealing |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --------- | ---- | ----------- | ------- | ---- | ------- |
2. Preliminaries roboticsolutionsassoft[31]orflexiblerobots.[47]
withinnovative
|      |            |     |             |          |     |     |     | Note that | learning-based |     | control | is imposing | itself | as a | central |
| ---- | ---------- | --- | ----------- | -------- | --- | --- | --- | --------- | -------------- | --- | ------- | ----------- | ------ | ---- | ------- |
| 2.1. | Lagrangian | and | Hamiltonian | Dynamics |     |     |     |           |                |     |         |             |        |      |         |
trendinthesenonconventionalroboticsystems.[48]Theseconsid-
|     |     |     |     |     |     |     |     | erations | relate to | issues | (1) and | (2) stated | in the | introduction. |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | --------- | ------ | ------- | ---------- | ------ | ------------- | --- |
Robots’
|             | dynamics    |            | can be      | represented | using | Lagrangian       | or         |             |     |            |     |     |     |     |     |
| ----------- | ----------- | ---------- | ----------- | ----------- | ----- | ---------------- | ---------- | ----------- | --- | ---------- | --- | --- | --- | --- | --- |
| Hamiltonian |             | mechanics. | In          | the former, | the   | state is defined | by         |             |     |            |     |     |     |     |     |
| the         | generalized |            | coordinates | q∈ℝN        | and   | their            | velocities |             |     |            |     |     |     |     |     |
|             |             |            |             |             |       |                  |            | 3. Proposed |     | Algorithms |     |     |     |     |     |
q˙ ∈ℝN,whereNrepresentstheconfigurationspacedimension.
|     | Eul(cid:3)er–Lagrange |     |     |     |     | system’s |     |     |     |     |     |     |     |     |     |
| --- | --------------------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Th(cid:1)e equation dictates the behavior 3.1. A Learnable Model for Nonconservative Forces
| ∂L  | ðq ,q˙Þ   | ∂L ðq ,q˙Þ¼F |     | Lðq,q˙Þ¼Tðq,q˙Þ(cid:2)VðqÞ |     |     |      |     |     |     |     |     |     |     |     |
| --- | --------- | ------------ | --- | -------------------------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
| d   | ∂ (cid:2) | ∂            | ,   | where                      |     |     | with |     |     |     |     |     |     |     |     |
d t q˙ q ext InstandardLNNstheory,nonconservativeforcesareassumedto
|                      |        | VðqÞ∈ℝ |                                         |             |        |      | q˙TMðqÞq˙, |                                                         |     |             |     |         |         |              |     |
| -------------------- | ------ | ------ | --------------------------------------- | ----------- | ------ | ---- | ---------- | ------------------------------------------------------- | --- | ----------- | --- | ------- | ------- | ------------ | --- |
| potential            | energy |        |                                         | and kinetic | energy | T ¼1 |            |                                                         |     |             |     |         |         |              |     |
|                      |        |        |                                         |             |        |      | 2          | befullyknownandtobeequaltoactuationforcesdirectlyacting |     |             |     |         |         |              |     |
| whereMðqÞ∈ℝN(cid:3)N |        |        | isthepositivedefinitemassinertiamatrix. |             |        |      |            |                                                         |     |             |     |         |         |              |     |
|                      |        |        |                                         |             |        |      |            | on the Lagrangian                                       |     | coordinates |     | q. This | is very | restrictive, | as  |
∈ℝN,includecontrolinputsand
Externalforces,denotedasF already discussed in the introduction.
ext
dissipation forces. In this work, we include external forces given by dissipation
In Hamiltonian mechanics, momenta p∈ℝN replace the andactuatorforces,i.e.,F ¼F ðq,q˙ÞþF ðqÞ.Weproposethe
|     |     |     |                    |     |     |     |     |     |     |     | ext | d   | a   |     |     |
| --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | q˙ ¼M(cid:2)1ðqÞp. |     |     |     |     |     |     |     |     |     |     |     |     |
velocities, with The Hamiltonian equations following model for dissipation forces:
| q˙ ¼ | ∂H ð q,pÞ, | p˙ ¼(cid:2) | ∂H ð q,pÞþF | , where |     | Hðq,pÞ¼Tðq,pÞþ |     |                        |     |     |     |     |     |     |     |
| ---- | ---------- | ----------- | ----------- | ------- | --- | -------------- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |
|      | ∂ p        |             | ∂ q         | ext     |     |                |     | F ðq,q˙Þ¼(cid:2)DðqÞq˙ |     |     |     |     |     |     | (3) |
d
VðqÞisthetotalenergy.Thekineticenergyinthiscaseisdefined
Tðq,pÞ¼1pTM(cid:2)1ðqÞp. where DðqÞ∈ℝN(cid:3)N is the positive semi-definite damping
as
2
|      |      |          |     |     |     |     |     | matrix. Besides, |     | we model | the | actuator force | as  |     |     |
| ---- | ---- | -------- | --- | --- | --- | --- | --- | ---------------- | --- | -------- | --- | -------------- | --- | --- | --- |
|      |      |          |     |     |     |     |     | F ðqÞ¼AðqÞu      |     |          |     |                |     |     | (4) |
| 2.2. | LNNs | and HNNs |     |     |     |     |     | a                |     |          |     |                |     |     |     |
LNNsemploytheprincipleofleastactiontolearnaLagrangian
| function | Lðq,q˙Þ | from | trajectory | data, | with the | learned | function |     |     |     |     |     |     |     |     |
| -------- | ------- | ---- | ---------- | ----- | -------- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
generatingdynamicsviastandardEuler–Lagrangemachinery.[34]
ThelossfunctionfortheLNNinref.[23]isgivenbythemean
squarederror(MSE)betweentheactualaccelerationsq¨andthe
| ones | that the   | learned | model | would expect | q¨ ˆ |     |     |     |     |     |     |     |     |     |     |
| ---- | ---------- | ------- | ----- | ------------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L    | ¼MSEðq¨,q¨ | ˆ Þ:    |       |              |      |     | (1) |     |     |     |     |     |     |     |     |
LNN
| HNNs,        |     | conversely,                                | are | designed | to learn | the Hamiltonian |     |     |     |     |     |     |     |     |     |
| ------------ | --- | ------------------------------------------ | --- | -------- | -------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| functionHðp, |     | qÞ.Oncelearned,thisHamiltonianfunctionpro- |     |          |          |                 |     |     |     |     |     |     |     |     |     |
videsdynamicsthroughHamilton’sequations.Thelossfunction
forHNNissimilaranMSEbutbetweenthepredictedandactual
time derivatives of generalized coordinates and momenta: Figure1. Fullyconnectednetwork.
Adv.Intell.Syst.2024,6,2300385 2300385 (2 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     |     |     |     |     |     |     |     |     | www.advintellsyst.com |     |     |
| --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- |
where u∈ℝW is the control input signal to the system, and 3.2. Nonconservative Noncollocated Lagrangian and
| AðqÞ∈ℝN(cid:3)W |     |     |     |     |     |     |     |     | Modified |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
is an input transformation matrix. For example, Hamiltonian NNs with Loss
| A could | be  | the transpose | Jacobian | associated | with the point | of  |     |     |     |     |     |     |     |     |
| ------- | --- | ------------- | -------- | ---------- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
application of an actuation force on the structure. With this Figure2reportstheproposednetworkframework,whichbuilds
model, we take into account that in complex robotic systems, uponLagrangianandHamiltonianNNsdiscussedinSection2.2.
actuatorsare,ingeneral,notcollocatedonthemeasuredconfig-
|     |     |     |     |     |     | Our | work | incorporates | the | damping | matrix | network, |     | input |
| --- | --- | --- | --- | --- | --- | --- | ---- | ------------ | --- | ------- | ------ | -------- | --- | ----- |
modified
urationsq.Notethat,evenifweacceptedtoimposeanopportune matrix network, and a loss function into the original
change of coordinates, for some systems, a representation framework. The damping matrix network is used to account
withoutAisnotevenadmissible.[49]WithEquation(4),wealso for the dissipation forces in the system via Equation (3), while
|           |     |                     |          |     |     | the | input | matrix network |     | corresponds | to  | A(q) in | Equation | (4). |
| --------- | --- | ------------------- | -------- | --- | --- | --- | ----- | -------------- | --- | ----------- | --- | ------- | -------- | ---- |
| seemingly |     | treat underactuated | systems. |     |     |     |       |                |     |             |     |         |          |      |
Notethatref.[46]usesadissipativemodelbutconsidersitina WepredictthenextstatebyintegratingEquation(5)or(7)with
Runge–Kutta
white-box fashion. the aid of the 4 integrator. Clearly, different inte-
Hence, we rewrite the Lagrangian dynamics as follows: gration strategies could be used in its place.
(cid:4) (cid:5) (cid:4) (cid:5) ThedatasetD¼½D ,T jk∈f0,:::,k g(cid:4)containsinforma-
|     |     |     |     |     |     |     |     |     | k k |     | end |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∂2Lðq,q˙Þ (cid:2)1 ∂2Lðq,q˙Þ ∂ Lðq,q˙Þ tion about thestate transitions of the mechanical system. With
| q¨¼ |       | AðqÞu(cid:2) |     | q˙þ    | (cid:2)DðqÞq˙ |     |     |     |     |     |     |     |     |     |
| --- | ----- | ------------ | --- | ------ | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | ∂ q˙2 |              | ∂   | ∂ q˙ ∂ |               |     |     |     |     |     |     |     |     |     |
q q thiscompactnotation,wearenotexclusivelyreferringtoasingle
system’s
|     |     |     |     |     |     | (5) trajectory |        | of the        | behavior, |     | but we     | aggregate | data     | from |
| --- | --- | --- | --- | --- | --- | -------------- | ------ | ------------- | --------- | --- | ---------- | --------- | -------- | ---- |
|     |     |     |     |     |     | multiple       | system | trajectories. |           | The | input data | D is      | composed | of   |
k
|       |     |                  |           |             |     | either½q | ,q˙ | ,u ,Δt(cid:4),forLagrangiandynamics,or½q |     |     |     |     | ,p ,u | ,Δt(cid:4)in |
| ----- | --- | ---------------- | --------- | ----------- | --- | -------- | --- | ---------------------------------------- | --- | --- | --- | --- | ----- | ------------ |
| which | can | be alternatively | expressed | as follows: |     |          | k   | k k                                      |     |     |     |     | k k   | k            |
thecaseofHamilton(cid:8)iandynam(cid:9)ics.Similarly,thecorresponding
q¨¼M(cid:2)1ðqÞðAðqÞu(cid:2)Cðq,q˙Þq˙(cid:2)GðqÞ(cid:2)DðqÞq˙Þ T ,q˙
|            |                    |                 |          |          |     | (6) label |                                                       | is either               | q   | ,         | for the | Lagrangian |     | case, or |
| ---------- | ------------------ | --------------- | -------- | -------- | --- | --------- | ----------------------------------------------------- | ----------------------- | --- | --------- | ------- | ---------- | --- | -------- |
|            |                    |                 |          |          |     |           | k                                                     |                         | kþ1 | kþ1       |         |            |     |          |
|            |                    |                 |          |          |     | ½q        | ,p                                                    | (cid:4) for Hamiltonian |     | dynamics. | Here,   | k and      | kþ1 | refer    |
|            |                    |                 |          |          |     | kþ        | 1 k þ 1                                               |                         |     |           |         |            |     |          |
| where      | Cðq,q˙Þ∈ℝN(cid:3)N | and             | GðqÞ∈ℝN. |          |     |           |                                                       |                         |     |           |         |            |     |          |
|            |                    |                 |          |          |     | to co     | ns e c utivetimestepsinthedataset,wherekprovidesinput |                         |     |           |         |            |     |          |
| Similarly, |                    | the Hamiltonian | takes    | the form |     |           |                                                       |                         |     |           |         |            |     |          |
dataatonetimestep,andkþ1correspondstothelabeldataat
|     |     | 2   | 3           |     |     | the | subsequent | time | step Δt. |     |     |     |     |     |
| --- | --- | --- | ----------- | --- | --- | --- | ---------- | ---- | -------- | --- | --- | --- | --- | --- |
|     |     | ∂ H | ð q , q ˙ Þ |     |     |     |            |      |          |     |     |     |     |     |
(cid:6) (cid:7) (cid:6) (cid:7) (cid:6) (cid:7) T h e v al u e s o f M (q ,θ ) , V ( q, θ ) , D ( q ,θ ) , a n d A ( q, θ ) a re e sti -
| ˙   |     | 6   | ∂ 7 |     |     |     |     |     | 1   | 2   | 3   |     | 4   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
q 0 I 6 q 7 0 ma te d b y f o u r su b ne tw o r ks , n a m e l y, t h e m a s s n et w o r k ( M -N N ) ,
| ˙   | ¼        | 4 ∂            | ˙ 5þ      | u    |     | (7)       |       |                |         |         |         |         |           |         |
| --- | -------- | -------------- | --------- | ---- | --- | --------- | ----- | -------------- | ------- | ------- | ------- | ------- | --------- | ------- |
| p   | (cid:2)I | (cid:2)D ðqÞ H | ð q , q Þ | AðqÞ |     |           |       |                |         |         |         |         |           |         |
|     |          |                |           |      |     | potential |       | energy network |         | (V-NN), | damping | network |           | (D-NN), |
|     |          |                | ∂ p       |      |     |           |       |                |         |         |         |         |           |         |
|     |          |                |           |      |     | and       | input | matrix         | network | (A-NN), | as      | shown   | in Figure | 2.      |
Figure2. TheoverviewofLagrangianandHamiltonianneuralnetworks:theyellowpart—i.e.,D andT —representstheinputandlabeldatausedinthe
|     |     |     |     |     |     |     |     | k   | k   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
network;inred,thedataandcalculationprocessrequiredforLagrangiandynamics;andthegreenpartsrepresentthecorrespondingdataandcalculation
associatedwiththeHamiltoniandynamics.
Adv.Intell.Syst.2024,6,2300385 2300385 (3 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |          |              |     |            |     |         |     |     |     |     |     | www.advintellsyst.com |     |     |
| --------------------------- | --- | -------- | ------------ | --- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --------------------- | --- | --- |
| The parameter               |     | θ, where | i∈{1,2,3,4}, |     | represents | the | subnet- |     |     |     |     |     |                       |     |     |
i
| works’ model | parameter. |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------ | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Thekineticenergycanbecalculatedoncethevaluesofq˙
orp
areobtained.Then,theLagrangianorHamiltonianfunctionscan
bederivedfromthekineticandpotentialenergies.Thederivative
| ofthestatesq¨ˆor½qˆ˙ |     | pˆ˙ |     |     |     |     |     |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:4)Tcanbecomputedusing(5)or(7),respec-
| tively.Thepredictednextstateqˆ˙ |     |     |     | or½qˆ | pˆ(cid:4)T |     |     |     |     |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | ----- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
canbeobtainedusing
| the Runge–Kutta |     | 4 integrator. |     | We thus | employ | the following |     |     |     |     |     |     |     |     |     |
| --------------- | --- | ------------- | --- | ------- | ------ | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
modified losses:[32,33]
|     |     |     |     |     |     |     |     | Figure4. Diagramforactuatormatrix:Thefullyconnectednetworkoutput |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|     | 1 X |     |     |     |     |     |     |                                                                  |     |     |     |     |     |     |     |
(cid:2)qˆ k2þkq˙ ˆ˙ k2Þ is a vector in ℝNW, which isreshaped to a matrix in ℝN(cid:3)W. A sigmoid
| L LNN ¼ #D | ðkq |     |     |     | (cid:2)q |     | (8) |     |     |     |     |     |     |     |     |
| ---------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
kþ1 kþ1 2 kþ1 kþ1 2 activation function can be applied to the matrix elements for value
k∈D
constraint.
| for LNNs, | where | #D is | the cardinality |     | of D, | and |     |     |     |     |     |     |     |     |     |
| --------- | ----- | ----- | --------------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
X
1 positive.Theremaining(N2(cid:2)N)/2valuesareplacedinthelower
|            |     | (cid:2)qˆ | k2þkp |       | (cid:2)pˆ | k2Þ |     |             |        |                  |     |         |     |     |     |
| ---------- | --- | --------- | ----- | ----- | --------- | --- | --- | ----------- | ------ | ---------------- | --- | ------- | --- | --- | --- |
| L HNN ¼ #D | ðkq | kþ1       | kþ1   | 2 kþ1 | kþ1       | 2   | (9) |             |        |                  |     |         |     |     |     |
|            |     |           |       |       |           |     |     | left corner | of the | lower triangular |     | matrix. |     |     |     |
k∈D
|     |     |     |     |     |     |     |     | The calculation |     | of the | potential | energy | is performed |     | using a |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------ | --------- | ------ | ------------ | --- | ------- |
forHNNs.Thus,comparedto(1)and(2),wearecalculatingthe simple, fully connected network with a single output, which is
MSE of a future prediction of the state—simulated via the represented as V(q,θ ). Moreover, A-NN, depicted in Figure 4,
2
learned dynamics—rather than of the current accelerations, calculates A(q,θ ) with dimensions ℝN(cid:3)W.
4
whichcannotbemeasured.Notethatwealsoincludeameasure
ofthepredictionerrorattheconfigurationlevelforL
|     |     |     |     |     |     | HNN | because | 3.3. PINN-Based |     | Controllers |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------------- | --- | ----------- | --- | --- | --- | --- | --- |
∂H
| the information |     | on  | ð q,q˙Þ appears | disentangled |     | from | D and A |     |     |     |     |     |     |     |     |
| --------------- | --- | --- | --------------- | ------------ | --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
∂ p
(whicharealsolearned)inthefirstnequationsofEquation(7). Weprovideinthissectiontwoprovablystablecontrollersbycom-
|     |     |     |     |     |     |     |     | bining | the learned | dynamics |     | with | classic | model-based |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ----------- | -------- | --- | ---- | ------- | ----------- | --- |
approaches.Beforestatingtheseresults,itisimportanttospend
| 3.2.1. Subnetwork |     | Structures |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
afewlinesremarkingonthepotentialrelationshipsbetweenthe
Constraintsbasedonphysicalprinciplescanbeimposedonthe outcomesobtainedthroughproposedLNNandthegroundtruth,
|            |         |     |          |              |     | Specifically, |     | as well as | their | implications | for | controller | design. | Due | to the |
| ---------- | ------- | --- | -------- | ------------ | --- | ------------- | --- | ---------- | ----- | ------------ | --- | ---------- | ------- | --- | ------ |
| parameters | learned | by  | the four | subnetworks. |     |               | the |            |       |              |     |            |         |     |        |
massanddampingmatricesmustbepositivedefiniteandposi- inclusionoftheactuatormatrixandtheinherentnonuniqueness
tivesemidefinite,respectively.Tothisend,thenetworkstructure of the Lagrangian, we assume that the Lagrangian L ðq,q˙Þ
L
|     |     |     |     |     |     |     |     | learned by | LNN | can be represented |     | as  | follows: |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ------------------ | --- | --- | -------- | --- | --- |
ofthedissipationmatrixcanfollowtheprototypeestablishedfor
| themass | matrix | in ref. | [50]. This | structure | can | bedecomposed |     |                     |     |     |     |     |     |     |      |
| ------- | ------ | ------- | ---------- | --------- | --- | ------------ | --- | ------------------- | --- | --- | --- | --- | --- | --- | ---- |
|         |        |         |            |           |     |              |     | L ðq,q˙Þ¼aLðq,q˙Þþb |     |     |     |     |     |     | (10) |
L
| into a lower | triangular |     | matrix | L D with | nonnegative |     | diagonal |     |     |     |     |     |     |     |     |
| ------------ | ---------- | --- | ------ | -------- | ----------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
elements, which is then computed using the Cholesky whereaisanonzeroconstant,andbisanotherconstantterm.In
decomposition[51] as D¼L L T. The representation of D(q) is thissection,wehighlightthecomponentsthathavebeenlearned
D D
illustrated in Figure 3. byaddinganLasasubscripttoprovideaclearerillustration.The
(N2þN)/2,
The output of M-NN and D-NN is calculated as LNN enables us to discover an oridinary differential equation
first
with the N values representing the diagonal entries of the (ODE) with a solution that matches that of the real ODE
lowertriangularmatrix.Toensurenonnegativity,activationfunc-
|     |     |     |     |     |     |     |     | (cid:2) 1 | τ   | ˙ ˙ |     |     | ˙Þ  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
tions such as Softplus or ReLU are utilized as the last layer. M |fflfflffl fflffl fflffl ð fflffl q fflffl Þ fflffl ð fflffl A fflfflffl ð fflffl q fflffl Þ fflffl fflfflffl (cid:2) fflfflfflfflffl C fflfflffl ð fflffl{ q z ,q ffl fflffl Þ ffl q ffl fflfflffl (cid:2) fflfflfflffl G fflfflfflffl ð fflffl q fflffl Þ fflfflffl (cid:2) fflfflfflfflffl D fflfflffl ð fflffl q fflffl Þ fflffl q }
| Furthermore, | the | constant | ε   | is introduced |     | to guarantee | that |     |     |     |     |     |     |     |     |
| ------------ | --- | -------- | --- | ------------- | --- | ------------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
q¨
|     |     |     | definite. |     |     | ε   |     |     |     |     |     |     |     |     | (11) |
| --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
the mass matrix is positive Note that is a hyperpara- ¼M(cid:2)1ðqÞðA ðqÞτ(cid:2)C ðq,q˙Þq˙(cid:2)G ðqÞ(cid:2)D ðqÞq˙Þ
|fflfflfflLfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflLfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflLfflfflfflffl{zfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflLfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflLfflfflfflfflfflfflfflffl}
| meter that | should | be  | selected | to be | small-enough | but | strictly |     |     |     |     |     |     |     |     |
| ---------- | ------ | --- | -------- | ----- | ------------ | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
q¨L
|     |     |     |     |     |     |     |     | Also, by         | construction, |         | M , G  | , A , | and D        | will have | all the |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | ------------- | ------- | ------ | ----- | ------------ | --------- | ------- |
|     |     |     |     |     |     |     |     |                  |               |         | L      | L L   | L            |           |         |
|     |     |     |     |     |     |     |     | usual properties |               | that we | expect | from  | these terms, | like      | M L and |
beingsymmetricandpositivedefinite,andG
|     |     |     |     |     |     |     |     | D L                                   |     |     |     |     |     | L beingapoten- |      |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | -------------- | ---- |
|     |     |     |     |     |     |     |     | tialforce.Yet,thisdoesnotimplythatM=M |     |     |     |     |     | ,G=G           | ,A=A |
,
|     |     |     |     |     |     |     |     |        |                                             |     |     |     | L   | L   | L   |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------------------------------------------- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     | andD=D | .Indeed,therecouldexistaconstantmatrixPsuch |     |     |     |     |     |     |
L
|     |     |     |     |     |     |     |     | that PM(q), | PG(q), | PA(q), | and PD(q) | have | all the | properties | dis- |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ------ | ------ | --------- | ---- | ------- | ---------- | ---- |
fulfilling:
|     |     |     |     |     |     |     |     | cussed above                           | while | simultaneously |     |     |     |     |      |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------- | ----- | -------------- | --- | --- | --- | --- | ---- |
|     |     |     |     |     |     |     |     | Lðq,q˙;PM,PG,PA,PDÞ¼aLðq,q˙;M,G,A,DÞþb |       |                |     |     |     |     | (12) |
So,controllersmustbeformulatedandproofsderivedunder
Figure3. Diagramofthedampingmatrixincludingafeed-forwardneural
network, a nonnegative shift for diagonal entries, and the Cholesky theassumptionofthelearnedtermsbeingclosetotherealones
| decomposition. |     |     |     |     |     |     |     | up to a multiplicative |     | factor. |     |     |     |     |     |
| -------------- | --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | ------- | --- | --- | --- | --- | --- |
Adv.Intell.Syst.2024,6,2300385 2300385 (4 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

www.advancedsciencenews.com www.advintellsyst.com
3.3.1. Regulation Rearranging terms, we get that:
Thegoalofthefollowingcontrolleristostabilizeagivenconfig- Δ I ðqÞ¼A(cid:2) L 1ðqÞ(cid:2)ðPAðqÞÞ(cid:2)1
uration q
X∞
(18)
ref ¼ ð(cid:2)ðPAðqÞÞ(cid:2)1Δ ðqÞÞkðPAðqÞÞ(cid:2)1
A
k¼1
u¼A(cid:2)1ðqÞG ðqÞþA(cid:2)1ðqÞðK ðq (cid:2)qÞ(cid:2)K q˙Þ (13)
L L L P ref D
Therefore, we can bound the norm of ΔðqÞ as follows:
I
where we omit the arguments t and θ to ease the readability. X∞
i
G L (q ref )isthepotentialforcewhichcanbecalculatedbytaking jjΔ I ðqÞjj≤ jjðPAðqÞ(cid:2)1Δ A ðqÞÞjjkjjðPAðqÞÞ(cid:2)1jj
thepartialderivativeofthepotentialenergylearnedbytheLNN; k¼1 (19)
K and K are control gains. jjðPAðqÞÞ(cid:2)1Δ ðqÞjjjjðPAðqÞÞ(cid:2)1jj
P D ¼ A <δ
Forthesakeofconciseness,weintroducethecontroller,and 1(cid:2)jjðPAðqÞÞ(cid:2)1Δ ðqÞjj I
A
we prove its stability for the fully actuated case. However, the
controller and the proof can be extended to the generic under- Hence, the generalized forces produced by the controller
actuated case using arguments in ref. [36, p. 50]. This will be AðqÞu are given by:
the focus of future work.
AðqÞA(cid:2)1ðqÞ½G ðqÞþðK ðq (cid:2)qÞ(cid:2)K q˙Þ(cid:4)
L L P ref D Proposition1:AssumethatW=N,withAandA L bothfullrank, ¼ AðqÞðA(cid:2)1ðqÞP(cid:2)1þΔðqÞÞ½ðPGðqÞþΔ ðqÞÞ and the existence of a constant matrix P∈ℝN(cid:3)N such that I G
jjG ðqÞ(cid:2)PGðqÞjj<δ , for some finite and positive δ . We þK P ðq ref (cid:2)qÞ(cid:2)K D q˙(cid:4)
assu L me that: G G ¼ðP(cid:2)1þAðqÞΔ I ðqÞÞ½ðPGðqÞþΔ G ðqÞÞþK P ðq ref (cid:2)qÞ(cid:2)K D q˙(cid:4)
¼GðqÞþΔ ðqÞþK ˆ ðq (cid:2)qÞ(cid:2)K ˆ q˙
all P ref D
jjA(cid:2)1ðqÞP(cid:2)1½A ðqÞ(cid:2)PAðqÞ(cid:4)jj<1 (14) (20)
L
whereΔ ðqÞ¼P(cid:2)1Δ ðqÞþAðqÞΔðqÞPGðqÞþAðqÞΔðqÞΔ ðqÞþ
all G I I G and that the gains K P , K D are chosen such that: AðqÞΔ K ðq (cid:2)qÞ(cid:2)AðqÞΔ K q˙ isaboundedterm,assumand
I P ref I D
ˆ ˆ productofboundedterms.ThegainsK andK arepositivedef-
P D P(cid:2)1K P ≻0, and; P(cid:2)1K D ≻0 (15) inite matrices, resulting from the products P(cid:2)1K P and P(cid:2)1K D ,
respectively,asindicatedinRemark2.Thus,theclosed-loopsys-
Then,givenamaximumadmittederrorδ ,theclosedloopof(5) tem takes the form: q
and (13) is such that MðqÞq¨þCðq,q˙Þq˙ ¼Δ ðqÞþK ˆ ðq (cid:2)qÞ(cid:2)ðDðqÞþK ˆ Þq˙
all P ref D
(21)
limqðtÞ¼q with jjq (cid:2)q jj<δ (16)
t!∞ ss ss ref q
To conclude, replicating the arguments provided in
ref. [53, Theorem 1] yields the result. In turn, that work was
adapted from the seminal paper.[54] Alternatively, Equation
Remark1:Assumption(14)isarequestonthelearnedmatrixA (q) (21) can be rewritten as:
L
being close enough to A(q) up to a multiplicative factor P, which is MðqÞq¨þCðq,q˙Þq˙þðDðqÞþK ˆ Þq˙þK ˆ ðq(cid:2)q Þ¼Δ ðqÞ
somethingweneedtoensure,asdiscussedinSection3.3.Indeed,if |fflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflffl{zfflfflfflfflfflfflfflfflfflfflDfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflfflPfflfflfflfflfflfflfflfflfflfflfflfflfflfflrfflfflefflffflffl} all
A L ðqÞ≃PAðqÞ, then (14) is fulfilled. nominalsystem
(22)
Remark 2: Note that there always exist K and K that fulfill
assumption (15). Specifically, they can be ex P pressed a D s K ¼PK ˆ Thus, considering the Lyapunov candidate function:
P P
andK ¼PK ˆ ,whereK ˆ andK ˆ denotepositivedefinitematrices.
D D P D Vðq,q˙Þ¼ 1 q˙TMðqÞq˙þ 1 ðq(cid:2)q ÞTK ˆ ðq(cid:2)q Þ (23)
Proof. Let us introduce the matrix Δ ∈ℝN(cid:3)N such that 2 2 ref P ref
A
A ðqÞ¼PAðqÞþΔ ðqÞ.Thismatrixissmallenoughbyassump-
L A asimplestabilityanalysisshowsthatthenominalsystemhasan
tionasdetailedinRemark1.Wenowwanttoboundthediffer-
asymptoticallystableequilibriumpointatthedesiredconfigura-
encebetweentheinverseofA(q)andPA (q).Thegoalistowrite
L tion. Therefore, the closed-loop system can be interpreted as a
A(cid:2) L 1ðqÞ¼ðPAðqÞÞ(cid:2)1þΔ I ðqÞ, with jjΔ I ðqÞjj<δ I . perturbed system, where the perturbation is given by Δ (q). BecauseofEquation(14),wecanusetheNeumannseries— all
Hence, the result can be proven following arguments for per-
see, for instance, in ref. [52, p. 20]—to obtain the following: turbed systems—see, for instance, in ref. [35, Chapter 9].
Note that even if we provided the proof using a Lagrangian
A(cid:2) L 1ðqÞ¼ðPAðqÞþΔ A ðqÞÞ(cid:2)1 formalism, the Hamiltonian version can be derived following
X∞ (17) similarsteps.Also,notethattheboundsonthelearnedmatrices
¼ ð(cid:2)ðPAðqÞÞ(cid:2)1Δ A ðqÞÞkðPAðqÞÞ(cid:2)1 arealwaysverifiedforanychoiceofδ A andδ G atthecostoftrain-
k¼0 ing the model with a large enough training set.
Adv.Intell.Syst.2024,6,2300385 2300385 (5 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH
26404567,
2024,
5,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385
by
National
Health
And Medical
Research
Council,
Wiley
Online
Library
on
[04/05/2026].
See the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use; OA
articles
are
governed
by the
applicable
Creative
Commons
License

www.advancedsciencenews.com www.advintellsyst.com
Weconcludewithacorollarythatdiscussestheperfectlearn- theonesinProposition1wouldleadtosimilarresultsinthetrack-
ing scenario. ing case, with jjPA ðqÞ(cid:2)AðqÞjj<δ , jjPM ðqÞ(cid:2)MðqÞjj<δ ,
L A L M
jjPC ðqÞ(cid:2)CðqÞjj<δ , jjPG ðqÞ(cid:2)GðqÞjj<δ , and jjPD ðqÞ(cid:2)
Corollary1:AssumethatW=NandAisfullrank.Then,theclosed L C L G L
DðqÞjj<δ , for some finite andpositive δ ,δ ,δ ,δ ,δ ∈ℝ.
loop of Equation (5) and (13) is such that: G A M C G D
limqðtÞ¼q (24)
t!∞ ref
4. Methods: Simulation and Experiment Design
if it exists a matrix P∈ℝN(cid:3)N such that M (q)=PM(q),
L
A (q)=PA(q), G (q)=PG(q). ToevaluatetheefficacyoftheproposedPINNsandPINN-based
L L
control,weapplytheminthreedistincttasks:(T1)learningthe
Proof.NotethatΔ =0asthedeltasarenowallzero.So,the
all dynamicmodelofa one-segmentspatialsoft manipulator,(T2)
closedloopofEquation(21)isalwaystheequivalentofamechan-
learningthedynamicmodelofatwo-segmentspatialsoftmanip-
icalsystem,withoutanypotentialforce,controlledbyaPD.Note
ulator,and(T3)learningthedynamicmodeloftheFrankaEmika
that the gains K ˆ and K ˆ are positive definitive. The proof of
P D Pandarobot.Weselected(T1)and(T2)becausetheyhaveanon-
stabilityfollowsstandardLyapunovarguments(see,forexample, trivialA(q),and(T3)becauseithasseveraldegreesoffreedom.
in ref. [34, p. 186]) by using the Lyapunov candidate given in
Furthermore,weemploythelearneddynamicstodesignandtest
Equation (23)).
model-based controllers for T2 and T3.
In a hardware experiment, the LNN is utilized to learn the
3.3.2. Trajectory Tracking dynamic model of the tendon-driven soft manipulator, as
reportedinref.[56],andthePandarobot.Weshowforthefirst
Thegoalofthefollowingcontrolleristotrackagiventrajectoryin time experimental closed-loop control of a robotic system
configurationspaceq ∶ℝ!ℝn.Weassumeq tobebounded (the Panda robot) with a PINN-based algorithm.
ref ref
withboundedderivatives.Wealsoassumethesystemtobefully
actuated—i.e., W=N, det(A)6¼0, det(A )6¼0. Under these
L 4.1. Data Generation
assumptions,weextendEquation(13)withthefollowingcontrol-
ler to follow the desired trajectory:
Training data for T1 and T2 are generated by simulating the
u¼A(cid:2)1ðqÞðM ðq Þq¨ þC ðq ,q˙ Þq˙ þD ðq Þq˙ dynamics of one-segment and two-segment soft manipulators
L L ref ref L ref ref ref L ref ref (25) in MATLAB. For these two cases, a random sampling strategy
þG L ðq ref ÞÞþA(cid:2) L 1ðqÞðK P ðq ref (cid:2)qÞþK D ðq˙ ref (cid:2)q˙ÞÞ is employed in data generation due to the unbounded configu-
whereweomittheargumentstandθ toeasethereadability.We rationspaceinherenttosoftmanipulatormodelsinsimulation.
i
ForT1,tendifferentinitialstatesarecombinedwithtendifferent
highlightthecomponentsthathavebeenlearnedfromtheones
inputsignalstogeneratedatausingtheone-segmentmanipula-
that are not by adding an L as a subscript. We can obtain the
CoriolismatrixC ðq ,q˙ ÞfromthelearnedLagrangianbytak- tor dynamics model. Each combination produces ten-second
L ref ref
trainingdatawithatimestepof0.0002s.ForT2,weuseavari- ingthesecondpartialderivativeoftheLagrangianwithrespectto
the desired joint position q ref and velocity q˙ ref , i.e., ∂2 ∂ L q ð r q e r f e∂f, q˙ q r ˙ e r f efÞ. a m b a le tic s a te l p m s o iz d e el in o S f im a u tw li o n - k se t g o m ge e n n e t r s a o te ft d m ata a s n e i t p s u f l r a o to m r. th W e it m h at t h h e is -
approach, we create twelve different sixty-second trajectories,
which are subsequently resampled at fixed frequencies of
Corollary2:TheclosedloopofEquation(5)and(25)issuchthat,for
some δ ≥0 50, 100, and 1000Hz. Concerning T3, the PyBullet simulation
q
environment is used to generate training data corresponding
t l ! im ∞ jjqðtÞ(cid:2)q ref ðtÞjj<δ q (26) to the Panda robot. Then, different input signals are applied
to the joints to create the data of 70 different trajectories with
If it exists a matrix P∈ℝN(cid:3)N such that A (q)=PA(q), a frequency of 1000Hz. These trajectories are thoughtfully
L
M (q)=PM(q), C (q)=PC(q), G (q)=PG(q), and D (q)= designed to encompass a significant portion of the robot’s
L L L L
PD(q). workspace.
Proof.WecanrewriteEquation(25)bysubstitutingthevalues Regardingexperimentalvalidation,weproposethefollowing
of the learned elements in terms of P. The result is experiments.Forthetendon-drivencontinuumrobot,weprovide
sinusoidal inputs with different frequencies and amplitudes to
AðqÞu¼ðMðq ref Þq¨ ref þCðq ref ,q˙ ref Þq˙ ref þDðq ref Þq˙ ref þGðq ref ÞÞ the actuators—four motors—and record the movement of the
þP(cid:2)1ðK ðq (cid:2)qÞþK ðq˙ (cid:2)q˙ÞÞ robot. An inertial measurement unit (IMU) records the tip ori-
P ref D ref
(27) entation data with a 10Hz sampling frequency. As a result,
122 trajectories are generated, and four more are collected as
Moreover,withtheAssumption(15)inCorollary1,theclosed thetestset.ForthePandarobot,weprovide70setsofsinusoidal
loopisequivalenttotheonediscussedinref.[55].Therefore,the desired joint angles with different amplitudes and frequencies.
proof follows the same steps as discussed there. Wecollectthetorque,jointangle,andangularvelocitydatausing
Finally,notethatweprovidedhereonlyproofofstability for the integrated sensors, considering a sampling frequency of
theperfectlylearnedcase.Similarhypothesesandargumentsto 500Hz.
Adv.Intell.Syst.2024,6,2300385 2300385 (6 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH
26404567,
2024,
5,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385
by
National
Health
And
Medical
Research
Council,
Wiley
Online
Library
on
[04/05/2026].
See
the Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by the
applicable
Creative
Commons
License

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     |     |     | www.advintellsyst.com |     |
| --------------------------- | --- | --- | --- | --- | --- | --------------------- | --- |
4.2. Baseline Model and Model Training and the Hessian within the loss function. The optimization of
|     |     |     |     | the model parameters | is carried | out using AdamW | in the |
| --- | --- | --- | --- | -------------------- | ---------- | --------------- | ------ |
To provide a basis for comparison, baseline models are estab- Optax package, which inherently include regularization terms
lishedforallsimulationsandhardwareexperiments.Thesemod- withintheoptimization process, eliminating theneed for addi-
els, which serve as a control, are constructed using a fully tional explicit regularization terms in the loss function.
| connected network | and trained   | using the same  | datasets as the |     |     |     |     |
| ----------------- | ------------- | --------------- | --------------- | --- | --- | --- | --- |
| proposed models,  | however, with | a larger amount | of data and     |     |     |     |     |
a greater number of training epochs. These baseline models 5. Simulation Results
| aimed to demonstrate | the benefits | of incorporating | physical |     |     |     |     |
| -------------------- | ------------ | ---------------- | -------- | --- | --- | --- | --- |
knowledge into neural networks. 5.1. One-Segment 3D Soft Manipulator
Inthisproject,alltheneuralnetworksutilizedareconstructed
|     |     |     |     | define configuration |     |     |     |
| --- | --- | --- | --- | -------------------- | --- | --- | --- |
usingtheJAXanddm-HaikupackagesinPython.Inparticular, To the space of the soft manipulator, we
the JAX Autodiff system is used to calculate partial derivatives adoptthepiecewiseconstantcurvature(PCC)approximation,[57]
Figure5. PCCapproachillustration:a)two-segmentsoftmanipulatorisshown,whereSistheendframe,thebluepartsaretheorientatedplane,andlis
|     |     |     |     | i   |     |     | i   |
| --- | --- | --- | --- | --- | --- | --- | --- |
theoriginallengthofeachsegment;b)thelengthofthefourarcswhoseendsconnectedtotheframeS.
i
(a)
2
1
0
-1
-2
|     | 0   | 1 2 | 3 4 | 5 6 7 | 8 9 | 10  |     |
| --- | --- | --- | --- | ----- | --- | --- | --- |
(b)
2
1
0
-1
-2
|     | 0   | 1 2 | 3 4 | 5 6 7 | 8 9 | 10  |     |
| --- | --- | --- | --- | ----- | --- | --- | --- |
One-segmentsoftmanipulator-learnedmodelcomparisonresults:a)thepredictionsgeneratedbytheblack-boxmodel(Δ),theLagrangian-
Figure6.
basedlearningmodel(⋯),andtheground-truth((cid:2))arisingfromthedynamicmathematicalequations;b)thepredictionerrorofthesetwolearnedmodels.
Adv.Intell.Syst.2024,6,2300385 2300385 (7 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     |     |     |     |     |     |     |     |     |     | www.advintellsyst.com |     |
| --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- |
asshowninFigure5.Customarily,thisapproximationdescribes sizeandnetworkdimensions,primarilyduetotwokeyfactors.
theconfigurationofeachsegmentasq =[ϕ,θ,δl],whereϕ is First, the nature of the optimization problem favors HNN,
|     |     |     |     | i   | i i i | i   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
theplaneorientation,θ isthecurvatureinthatplane,andδl benefits HNN’s
|     |     | i   |     |     |     | i is | which |     | from a | unique | solution. | Second, |     | input |
| --- | --- | --- | --- | --- | --- | ---- | ----- | --- | ------ | ------ | --------- | ------- | --- | ----- |
thechangeofarclength.Inthiswork,theconfiguration-defined
|     |     |     |     |     |     |     | data, | momentum, | provide | a   | more | comprehensive | description |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --------- | ------- | --- | ---- | ------------- | ----------- | --- |
method reported in ref. [58] is used to avoid the singularity of system dynamics. The detailed information regarding the
problem of PCC. Hence, the configuration of each segment is one-segment soft manipulator simulation is elucidated in
½Δ ,Δ ,Δ Δ Δ Table 1. The MSE shown in Table 1 and Figure 8 over a 5s
| given by | xi yi | li (cid:4), where | xi  | and yi | are the difference | of  |     |     |     |     |     |     |     |     |
| -------- | ----- | ----------------- | --- | ------ | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
arc length. duration reveals substantial performance advantages for both
Figure6 indicatesthatthemodeltrainedbyLNNsexhibitsa the Lagrangian-based and Hamiltonian-based learned models
highdegreeofpredictiveaccuracy,manifestingnear-infinitepre- in comparison to the black-box model. Notably, the
Hamiltonian-basedmodeldemonstratesaremarkablesuperior-
dictioncapabilitieswithover50000consecutivepredictionsteps
|     |     |     |     |     |     |     | ity, yielding |     | an average | prediction | error | of  | 0.0220(cid:5)0.0210 | for |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ---------- | ---------- | ----- | --- | ------------------- | --- |
inthisexample.Whilesomeareasexhibitlessprecisefits,such
the5ssimulationperiod.Thisunderscoresthemodel’sefficacy
| errors do | not accrue | over | time. | These outcomes | suggest | that |     |     |     |     |     |     |     |     |
| --------- | ---------- | ---- | ----- | -------------- | ------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
LNN-basedmodelscaneffectivelycapturetheunderlyingdynam- inadeptlycapturingandpredictingtheintricatedynamicsofthe
system.
icsoftheone-segmentsoftmanipulator(Figure6).Incontrast,
Thematricesobtainedfromthesetwophysics-basedlearning
| the black-box | model | converges | during | the | training process | but |        |     |                |     |        |       |                 |     |
| ------------- | ----- | --------- | ------ | --- | ---------------- | --- | ------ | --- | -------------- | --- | ------ | ----- | --------------- | --- |
|               |       |           |        |     |                  |     | models | are | shown in Table | 2   | and 3, | where | G(q) represents | the |
lacksthegeneralizedpredictiveabilityoutsidethetrainingdata-
∂V
set.Itsperformancerevealsitsinabilitytocaptureandgeneralize potentialforces,i.e., ð qÞ.AsTable3shows,HNNscanlearnthe
∂ q
the underlying dynamics. This system is also learned using physically meaningful matrices, while LNNs only learn one of
Euler–Lagrangian
HNNs by providing momentum data. HNNs yield similar the solutions satisfying the equation.
quality prediction results as LNNs, as shown in Figure 7. Comparing the corresponding matrices in Table 2 and 4, we
The HNN outperforms theLNN with identical training sample can find that the matrices and vectors learned by the LNNs
(a)
4
2
0
-2
-4
|     |     | 0   |     | 5   | 10  |     | 15  |     | 20  | 25  |     | 30  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(b)
0.4
0.2
0
-0.2
-0.4
|     |     | 0   |     | 5   | 10  |     | 15  |     | 20  | 25  |     | 30  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
One-segmentsoftmanipulatorHNNandLNNcomparison:a)theLagrangian-basedlearnedmodelpredictionresults(⋯),Hamiltonian-based
Figure7.
learnedmodelpredictionresults(○),andtheground-truthprediction((cid:2));b)errorofthetwomodelswiththegroundtruth.
Table1. One-segmentsoftmanipulatorsimulationdetailedinformation.
Black-boxmodel Lagrangian-basedlearnedmodel Hamiltonian-basedlearnedmodel
Model(width(cid:3)depth) 128(cid:3)5 32(cid:3)3,5(cid:3)3,16(cid:3)2 32(cid:3)3,5(cid:3)3,16(cid:3)2
| Samplenumber  |     |     |     | 19188 |     |     |     | 8000 |     |     |     |     | 8000 |     |
| ------------- | --- | --- | --- | ----- | --- | --- | --- | ---- | --- | --- | --- | --- | ---- | --- |
| Trainingepoch |     |     |     | 15000 |     |     |     | 6000 |     |     |     |     | 6000 |     |
Trainingerror 6.891(cid:3)10(cid:2)5(cid:5)4.63(cid:3)10(cid:2)4 8.418(cid:3)10(cid:2)7(cid:5)1.77(cid:3)10(cid:2)5 5.374(cid:3)10(cid:2)11(cid:5)7.74(cid:3)10(cid:2)10
Predictionerror[m2] 7.647(cid:5)10.413(5s) 0.171(cid:5)0.272(5s) 0.0220(cid:5)0.0210(5s)
Adv.Intell.Syst.2024,6,2300385 2300385 (8 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     |     |     |     |                      |             |                   |             |             | www.advintellsyst.com |               |          |
| --------------------------- | --- | --- | --- | --- | --- | --- | -------------------- | ----------- | ----------------- | ----------- | ----------- | --------------------- | ------------- | -------- |
|                             |     |     |     |     |     |     | 5.2. Two-Segment     |             | 3D Soft           | Manipulator |             |                       |               |          |
|                             |     |     |     |     |     |     | The two-segment      |             | soft manipulator  |             | model       | is                    | simulated     | in       |
|                             |     |     |     |     |     |     | MATLAB,              | where       | the configuration |             | space       | is also               | defined       | as in    |
|                             |     |     |     |     |     |     | the one-segment      |             | case. The         | training    | and         | testing               | information   |          |
|                             |     |     |     |     |     |     | for this             | task is     | presented         | in Table    | 5. In       | the 100Hz             |               | dataset, |
|                             |     |     |     |     |     |     | the Lagrangian-based |             | learned           | model       | outperforms |                       | the           | black-   |
|                             |     |     |     |     |     |     | box model            | with        | a notably         |             | lower       | prediction            | MSE           | of       |
|                             |     |     |     |     |     |     | 1.690(cid:5)0.673m2  |             | with less         | training    | data.       | Figure                | 9 summarizes  |          |
|                             |     |     |     |     |     |     | the prediction       | results     | of                | the 50,     | 100,        | and 1000Hz            |               | learned  |
|                             |     |     |     |     |     |     | model. From          | the         | simulations,      | we          | conclude    | that                  | the higher    | the      |
|                             |     |     |     |     |     |     | sampling             | frequency   | within            | a           | certain     | range,                | the           | more     |
|                             |     |     |     |     |     |     | accurate             | the learned | model             | is. This    | phenomenon  |                       | is attributed |          |
|                             |     |     |     |     |     |     | to the sensitivity   |             | of the            | integration | algorithm   |                       | to step       | size.    |
Employingmoreaccurateintegrationalgorithmsorshortertime
|     |     |     |     |     |     |     | steps in | future | experiments | is  | expected | to enhance |     | model |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ----------- | --- | -------- | ---------- | --- | ----- |
precision.
| Figure 8. One-segment |     | soft manipulator | LNN-based | and | HNN-based |     |       |        |               |         |     |         |     |          |
| --------------------- | --- | ---------------- | --------- | --- | --------- | --- | ----- | ------ | ------------- | ------- | --- | ------- | --- | -------- |
|                       |     |                  |           |     |           |     | Based | on the | learned model | trained | at  | 1000Hz, | we  | devise a |
learnedmodels’predictionMSEresults.
PINN-basedcontrolloopasinEquation(13).Todemonstratethe
performanceofthedesignedcontroller,weemployittocontrol
are related to the real parameters through a transformation P. thetwo-segmentsoftmanipulatorinMATLAB.Theproportional
Notably, P manifests subtle variations across different states; gains K and derivative gains K are set to 10 and 50, respec-
|     |     |     |     |     |     |     | P   |     |     | D   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
however, in theory, P is anticipated to remain constant. The configurations.
|     |     |     |     |     |     |     | tively, for | all six |     | The | alterations |     | in the | states of |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------- | --- | --- | ----------- | --- | ------ | --------- |
observeddiscrepanciesareattributedtoinherentlearningerrors the two-segment manipulator under control are depicted in
within the network. Figure 10, whereas the performance of the controller is
Table2. Lagrangian-basedlearningmodelmatricesofone-segmentsoftmanipulator.
| q   |     | ML(q) |     |     | DL(q) |     | GL(q) |     |     | AL(q) |     |     | P   |     |
| --- | --- | ----- | --- | --- | ----- | --- | ----- | --- | --- | ----- | --- | --- | --- | --- |
| 2 3 | 2   |       | 3   | 2   |       |     | 3 2   | 3   | 2   |       | 3   | 2   |     | 3   |
1.20 4.23(cid:3)10(cid:2)3 1.20(cid:3)10(cid:2)3 (cid:2)0.03 0.16 (cid:2)0.02 0.0 2.44 0.12 (cid:2)1.72 (cid:2)0.21 0.61 (cid:2)0.02 0.03
4 5 4 1.20(cid:3)10(cid:2)3 5.99(cid:3)10(cid:2)3 5 4 5 4 5 4 5 4 5
(cid:2)0.20 (cid:2)0.02 (cid:2)0.02 0.33 (cid:2)0.01 (cid:2)0.61 3.05 (cid:2)0.19 (cid:2)0.13 (cid:2)0.02 0.28 0.01
0.15 (cid:2)0.03 (cid:2)0.02 0.59 0.0 (cid:2)0.01 0.35 (cid:2)5.25 (cid:2)0.34 1.01 3.40 0.33 0.15 0.25
| 2 3 | 2   |     | 3   | 2   |     |     | 3 2 | 3   | 2   |     | 3   | 2   |     | 3   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.80 6.93(cid:3)10(cid:2)3 1.84(cid:3)10(cid:2)3 (cid:2)0.03 0.17 (cid:2)0.01 (cid:2)0.0 1.62 0.19 (cid:2)1.66 (cid:2)0.20 0.62 (cid:2)0.02 0.03
| 4 5 | 4   |     | 5   | 4   |     |     | 5 4 | 5   | 4   |     | 5   | 4   |     | 5   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.20 1.84(cid:3)10(cid:2)3 0.01 (cid:2)0.02 (cid:2)0.01 0.33 (cid:2)0.01 0.81 2.97 (cid:2)0.25 (cid:2)0.13 (cid:2)0.02 0.31 0.01
0.30 (cid:2)0.03 (cid:2)0.02 0.50 (cid:2)0.0 (cid:2)0.01 0.35 (cid:2)4.67 (cid:2)0.40 1.01 3.43 0.21 0.10 0.26
Table3. Hamiltonian-basedlearningmodelmatricesofone-segmentsoftmanipulator.
| q   |     | M(cid:2) L 1ðqÞ |     |     |     | DL(q) |     |     |     | GL(q) |     |     | AL(q) |     |
| --- | --- | --------------- | --- | --- | --- | ----- | --- | --- | --- | ----- | --- | --- | ----- | --- |
| 2 3 | 2   |                 | 3   | 2   |     |       |     | 3   |     | 2 3   |     | 2   |       | 3   |
1.20 600.32 16.90 15.67 1.02(cid:3)10(cid:2)1 3.44(cid:3)10(cid:2)3 8.12(cid:3)10(cid:2)5 1.33 (cid:2)0.06 (cid:2)0.94 0.05
4 (cid:2)0.20 5 4 16.90 622.92 (cid:2)1.34 5 4 3.44(cid:3)10(cid:2)3 1.05(cid:3)10(cid:2)1 (cid:2)4.39(cid:3)10(cid:2)45 4 (cid:2)0.18 5 4 0.83 0.02 (cid:2)0.04 5
0.15 15.67 (cid:2)1.34 11.61 8.12(cid:3)10(cid:2)5 (cid:2)4.39(cid:3)10(cid:2)4 9.91(cid:3)10(cid:2)2 (cid:2)1.15 0.0 0.01 0.78
| 2 3 | 2   |     | 3   | 2   |     |     |     | 3   |     | 2 3 |     | 2   |     | 3   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.80 285.01 11.08 6.65 1.01(cid:3)10(cid:2)1 3.48(cid:3)10(cid:2)3 6.56(cid:3)10(cid:2)4 0.93 0.03 (cid:2)0.96 0.05
4 0.20 5 4 11.08 292.46 2.06 5 4 3.48(cid:3)10(cid:2)3 1.03(cid:3)10(cid:2)1 (cid:2)7.45(cid:3)10(cid:2)55 4 0.25 5 4 0.92 (cid:2)0.03 (cid:2)0.02 5
0.30 6.65 2.06 10.59 6.56(cid:3)10(cid:2)4 (cid:2)7.45(cid:3)10(cid:2)5 9.87(cid:3)10(cid:2)2 (cid:2)1.10 (cid:2)0.01 0.0 0.89
Table4. Mathematicalmodelmatricesofone-segmentsoftmanipulator.
M(cid:2)1(q)
| q   |     | M(q) |     |     |     |     |     |     | D(q) |     | G(q) |     | A(q) |     |
| --- | --- | ---- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- | ---- | --- |
| 2 3 | 2   |      |     | 3   | 2   |     | 3   | 2   |      | 3 2 | 3    | 2   |      | 3   |
1.20 1.73(cid:3)10(cid:2)3 (cid:2)3.12(cid:3)10(cid:2)5 (cid:2)1.96(cid:3)10(cid:2)3 593.09 9.35 12.47 0.1 0 0 1.29 (cid:2)0.04 (cid:2)1.0 0.07
| 4 5 | 4   |     |     | 5   | 4   |     | 5   | 4   |     | 5 4 | 5   | 4   |     | 5   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:2)0.20 (cid:2)3.12(cid:3)10(cid:2)5 1.55(cid:3)10(cid:2)3 3.26(cid:3)10(cid:2)4 9.35 647.61 (cid:2)2.08 0 0.1 0 (cid:2)0.22 0.78 0.04 (cid:2)0.01
|     |     |     |     |     |     |     |     |     |     |     |     | 0:  | 0:  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.15 (cid:2)1.96(cid:3)10(cid:2)3 3.26(cid:3)10(cid:2)4 9.29(cid:3)10(cid:2)2 12.47 (cid:2)2.08 11.04 0 0 0.1 (cid:2)1.15 0.77
| 2 3  | 2                     |                       |                              | 3   | 2      |             | 3    |     |     | 2   | 3    | 2    |             | 3    |
| ---- | --------------------- | --------------------- | ---------------------------- | --- | ------ | ----------- | ---- | --- | --- | --- | ---- | ---- | ----------- | ---- |
|      | 3.64(cid:3)10(cid:2)3 | 4.52(cid:3)10(cid:2)5 | (cid:2)1.94(cid:3)10(cid:2)3 |     |        |             |      |     |     |     |      |      |             |      |
| 0.80 |                       |                       |                              |     | 277.76 | (cid:2)2.84 | 5.55 |     |     |     | 0.89 | 0.03 | (cid:2)0.99 | 0.06 |
4 0.20 5 4 4.52(cid:3)10(cid:2)5 3.47(cid:3)10(cid:2)3 (cid:2)4.84(cid:3)10(cid:2)45 4 (cid:2)2.84 288.42 1.39 5 4 0.22 5 4 0.90 (cid:2)0.03 0.02 5
0.30 (cid:2)1.94(cid:3)10(cid:2)3 (cid:2)4.84(cid:3)10(cid:2)4 9.67(cid:3)10(cid:2)2 5.55 1.39 10.46 (cid:2)1.09 0: 0: 0.89
Adv.Intell.Syst.2024,6,2300385 2300385 (9 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     |     |     | www.advintellsyst.com |     |
| --------------------------- | --- | --- | --- | --- | --- | --------------------- | --- |
Table5. Two-segmentsimulatedsoftmanipulatortrainingandtestingdetailedinformation.
|     |     | Black-boxmodel |     |      | Lagrangian-basedlearnedmodel |     |        |
| --- | --- | -------------- | --- | ---- | ---------------------------- | --- | ------ |
|     |     | 100Hz          |     | 50Hz | 100Hz                        |     | 1000Hz |
Model(width(cid:3)depth) 152(cid:3)3 42(cid:3)3,5(cid:3)3,42(cid:3)3 42(cid:3)3,5(cid:3)3,42(cid:3)2 42(cid:3)3,5(cid:3)3,42(cid:3)3
| Samplenumber  |     | 59200 |     | 45000 | 45000 |     | 45000 |
| ------------- | --- | ----- | --- | ----- | ----- | --- | ----- |
| Trainingepoch |     | 15000 |     | 5500  | 5500  |     | 5500  |
Trainingerror 3.536(cid:3)10(cid:2)4(cid:5)1.08(cid:3)10(cid:2)3 5.916(cid:3)10(cid:2)4(cid:5)8.61(cid:3)10(cid:2)3 1.652(cid:3)10(cid:2)4(cid:5)2.12(cid:3)10(cid:2)2 1.822(cid:3)10(cid:2)7(cid:5)6.67(cid:3)10(cid:2)6
Predictionerror[m2]
44.683(cid:5)4.518(10s) 2.098(cid:5)1.253(10s) 1.690(cid:5)0.673(10s) 0.089(cid:5)0.278(10s)
|     | (a) |     | (b) |     | (c) |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     | 10  |     | 10  |     | 10  |     |     |
|     | 8   |     | 8   |     | 8   |     |     |
|     | 6   |     | 6   |     | 6   |     |     |
|     | 4   |     | 4   |     | 4   |     |     |
|     | 2   |     | 2   |     | 2   |     |     |
|     |     |     | 0   |     | 0   |     |     |
0
|     | 0   | 5   | 10 0 | 5   | 10 0 | 5   | 10  |
| --- | --- | --- | ---- | --- | ---- | --- | --- |
|     | 4   |     | 4    |     | 4    |     |     |
|     | 3   |     | 3    |     | 3    |     |     |
|     | 2   |     | 2    |     | 2    |     |     |
|     | 1   |     | 1    |     | 1    |     |     |
|     | 0   |     | 0    |     | 0    |     |     |
|     | -1  |     | -1   |     | -1   |     |     |
|     | 0   | 5   | 10 0 | 5   | 10 0 | 5   | 10  |
Figure9. Two-segmentsoftmanipulatorpredictionperformancesunderdifferentsamplingfrequencies:a)50Hz,b)100Hz,andc)1000Hz.
Figure10. Thesequenceofmovementsatthetimes0.0,0.1,0.3,0.6,and1.0sexecutedbythetwo-segmentsoftrobotasaresultoftheimplementation
oftheLNN-model-basedcontroller.Theredlinerepresentsthetip’sposition.
Adv.Intell.Syst.2024,6,2300385 2300385 (10 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     |     |     |     |     |     | www.advintellsyst.com |     |
| --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- |
Figure11. Two-segmentsoftmanipulatormodel-basedcontrollerperformance:a)theevolutionoftheconfigurationvariablesandthedesiredstatewith
dottedlines;b)theerrorbetweenthedesiredstatesandcurrentstates;andc)controleffort.
demonstratedinFigure11.Resultsindicatethatthecontrolleris
|     |     |     |     |     | 5.3. Panda | Robot |     |     |     |     |
| --- | --- | --- | --- | --- | ---------- | ----- | --- | --- | --- | --- |
capableoftrackingastaticsetpointwithin1swhilekeepingthe
rootmeansquareerror(RMSE)lessthan0.23%,andexhibitsa Table6presentsthetrainingandtestingresultsofthesimulated
stableandminimalovershootperformance.Theseperformances PandainPyBullet,whileFigure12displaysthepredictionresults
underscorethereliabilityandefficiencyofthedesignedcontrol- obtainedfromthelearnedmodel.Incomparisontothedynamics
modelsformulatedinMATLAB,thesimulator’sdynamicsmodel
| ler based on the | learned | model. |     |     |     |     |     |     |     |     |
| ---------------- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
influenced
|     |     |     |     |     | is characterized | by       | increased   | complexity, |          | by the    |
| --- | --- | --- | --- | --- | ---------------- | -------- | ----------- | ----------- | -------- | --------- |
|     |     |     |     |     | inherent         | physical | constraints | in robotic  | systems, | including |
Table6. Pandasimulationdetailedinformation(1000Hz,predictionerror restrictions on acceleration and velocity. This heightened com-
inPandacaseisaccumulatederrorfor2s).
|     |     |     |     |     | plexity presents | challenges    |     | in learning        | the dynamics | model.    |
| --- | --- | --- | --- | --- | ---------------- | ------------- | --- | ------------------ | ------------ | --------- |
|     |     |     |     |     | Nevertheless,    | the LNN-based |     | model demonstrates |              | a smaller |
Black-boxmodel Lagrangian-based prediction MSE than the MSE of the black-box model.
|                          |     |             |     | learnedmodel          | Notably, | limitations | emerge | in long-term |     | predictions. |
| ------------------------ | --- | ----------- | --- | --------------------- | -------- | ----------- | ------ | ------------ | --- | ------------ |
| Model(width(cid:3)depth) |     | 120(cid:3)4 |     | 40(cid:3)3,20(cid:3)2 |          |             |        |              |     |              |
Consequently,inFigure12c,weadoptedacontinuousprediction
approach—forecasting
Samplenumber 550000 25000 50 steps consecutively and updating the
|               |     |       |     |       | model state | to effectively | illustrate | its performance. |     |     |
| ------------- | --- | ----- | --- | ----- | ----------- | -------------- | ---------- | ---------------- | --- | --- |
| Trainingepoch |     | 10000 |     | 10000 |             |                |            |                  |     |     |
Basedonthislearnedmodel,webuildthetrackingcontroller
| Trainingerror | 1.476(cid:3)10(cid:2)4(cid:5)2.69(cid:3)10(cid:2)3 |     | 1.424(cid:3)10(cid:2)4(cid:5)2.90(cid:3)10(cid:2)3 |     |     |     |     |     |     |     |
| ------------- | -------------------------------------------------- | --- | -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
discussedinSection3.3.TheresultsaredepictedinFigure13,
Predictionerror[rad2]
|     | 110.610(cid:5)8.809(2s) |     |     | 8.884(cid:5)6.323(2s) |     |     |     |     |     |     |
| --- | ----------------------- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- |
whereweobservethatourcontrollerhasafastresponsetimeand
Figure12. FrankaEmikaPandalearnedmodelpredictionresults:a)1500stepspredictioninarow;b)theangleerrorsofthepredictionconcerningthe
groundtruth;andc)thelongpredictionresultswith50-stepwindowsize.
Adv.Intell.Syst.2024,6,2300385 2300385 (11 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     |     |     |     | www.advintellsyst.com |
| --------------------------- | --- | --- | --- | --- | --- | --- | --------------------- |
Figure13. Performanceofthemodel-basedcontrollerdesignedusingthemodellearnedbytheLNNs.Thedesiredtrajectoriesareplottedwithdotted
lines:a)showsthetrajectorytrackingperformanceandb)visualizesthetorqueinputgeneratedbythecontroller.
canquicklyadapttochangesinthereferencesignal.Itcanmain- Table 7. The tendon-driven soft robot: NECK training and testing
information.
tainhighaccuracyandlowphaselag,whichmakesitwell-suited
| for tracking | fast-changing signals. |     |     |     |     |                |                  |
| ------------ | ---------------------- | --- | --- | --- | --- | -------------- | ---------------- |
|              |                        |     |     |     |     | Black-boxmodel | Lagrangian-based |
learnedmodel
6. Experimental Validation Smoothing Model 60(cid:3)3 21(cid:3)2,25(cid:3)2,10(cid:3)2
|                  |                       |                  |             |     | Samplenumber  | 69426                        | 69426                        |
| ---------------- | --------------------- | ---------------- | ----------- | --- | ------------- | ---------------------------- | ---------------------------- |
| 6.1. One-Segment | Tendon-Driven         | Soft Manipulator | – NECK      |     |               |                              |                              |
|                  |                       |                  |             |     | Trainingepoch | 10000                        | 3000                         |
|                  |                       |                  |             |     | Trainingerror | 1.985(cid:3)10(cid:2)2       | 2.277(cid:3)10(cid:2)2       |
| We validate      | the proposed approach | in the platform  | depicted in |     |               |                              |                              |
|                  |                       |                  |             |     |               | (cid:5)1.85(cid:3)10(cid:2)1 | (cid:5)2.39(cid:3)10(cid:2)1 |
Figure14,whichisconstructedbasedonrefs.[56,59].Weconsider
two different data preprocessing methods: 1) moving average Predictionerror[°2] 13.229(cid:5)60.762(5s) 2.429(cid:5)1.259(5s)
| method:thismethodreducedthe |                              | noise andoutliers | inthe data, |         |              |            |                                  |
| --------------------------- | ---------------------------- | ----------------- | ----------- | ------- | ------------ | ---------- | -------------------------------- |
|                             |                              |                   |             | Fitting | Model        | 60(cid:3)3 | 21(cid:3)2,25(cid:3)2,10(cid:3)2 |
| generating                  | a more stable representation | of underlying     | trends.     |         |              |            |                                  |
|                             |                              |                   |             |         | Samplenumber | 57950      | 48200                            |
However,itmayoverlookintricaterelationshipsbetweenvariables,
|     |     |     |     |     | Trainingepoch | 5000 | 5000 |
| --- | --- | --- | --- | --- | ------------- | ---- | ---- |
resultinginsomeinformationloss;and2)polynomialfitting:this
|     |     |     |     |     |     | 4.431(cid:3)10(cid:2)3 | 2.758(cid:3)10(cid:2)3 |
| --- | --- | --- | --- | --- | --- | ---------------------- | ---------------------- |
methodcapturednonlinearpatternsinthedata.However,itwas Trainingerror
susceptibletotheinfluenceofoutliers,resultinginspuriousinfor-
|     |     |     |     |     |     | (cid:5)3.07(cid:3)10(cid:2)2 | (cid:5)2.84(cid:3)10(cid:2)2 |
| --- | --- | --- | --- | --- | --- | ---------------------------- | ---------------------------- |
mation that may compromisethequalityof thetrainedmodel. Predictionerror[°2]
|              |                         |          |             |     |     | 8.368(cid:5)12.575(5s) | 6.426(cid:5)36.237(5s) |
| ------------ | ----------------------- | -------- | ----------- | --- | --- | ---------------------- | ---------------------- |
| The training | and testing information | is shown | in Table 7. |     |     |                        |                        |
Figure14. Experimentplatform:one-segmenttendon-drivensoftmanipulatorequippedwithIMU.
Adv.Intell.Syst.2024,6,2300385 2300385 (12 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     |     |     |     |     |     | www.advintellsyst.com |
| --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------- |
ThemethodofmovingaverageisimplementedinMATLAB Furthermore, Figure 15c shows that the learning model
through the utilization of the movmean function, with a can realize long-term predictions under the short-term
| prescribed window | size of 50 | points. | The processed |     | data are update. |     |     |     |     |
| ----------------- | ---------- | ------- | ------------- | --- | ---------------- | --- | --- | --- | --- |
ThepolynomialfittingofthedataisdoneinMATLABusing
| used for training | the LNNs. | In Figure | 15, | we compare | the |     |     |     |     |
| ----------------- | --------- | --------- | --- | ---------- | --- | --- | --- | --- | --- |
continuous prediction ability of black-box and Lagrangian- the function polyfit. The prediction results of the model are
based learning models. The prediction performance in this showninFigure16.Thelearnedmodelexhibitsadecentperfor-
figure
indicates that the Lagrangian-based learning model mancewhenthewindowsizeisreduced,asshowninFigure16c.
Incontrasttothepreviousmodel,thismodelexhibitssignificant
| exhibits superior | predictive | accuracy | in  | this | sample. |     |     |     |     |
| ----------------- | ---------- | -------- | --- | ---- | ------- | --- | --- | --- | --- |
|                   | (a)        |          |     |      |         | (b) |     |     |     |
|                   | 5          |          |     |      |         | 2   |     |     |     |
0
0
-2
|     | -5  |     |     |     |     | -4  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 0   | 2   | 4   | 6   | 8   | 0 2 | 4   |     | 6 8 |
(c)
0
-5
-10
-15
|     | 0   | 2   | 4   | 6   | 8   | 10 12 | 14  | 16  | 18  |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
Figure15. Thesmoothingdatablack-boxmodel(Δ)andphysics-basedlearningmodel(--)continuouspredictionresults:a,b)the43predictionstepsina
row;c)depictsthepredictionresultswith5-stepwindowsize.
|     | (a) |     |     |     |     | (b) |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2
0
1.5
-2
1
-4
0.5
-6
0
|     | 0   | 1   | 2   | 3   | 4 5 | 0 1 | 2   | 3   | 4 5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(c)
15
10
5
0
|     | 0   | 2   | 4   | 6   | 8   | 10 12 | 14  | 16  | 18  |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
Thefittingdatablack-boxmodel(Δ)andphysics-basedlearningmodel(⋯)continuouspredictionresults:a,b)25predictionstepsinarow;
Figure16.
c)thepredictionresultswith5-stepwindowsize.
Adv.Intell.Syst.2024,6,2300385 2300385 (13 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     |     |     |     |     |     | www.advintellsyst.com |     |
| --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- |
prediction errors shown in Table 7. This can be caused by the other important factors, we utilize a scaling sigmoid function.
significant noise in the sensors and misinformation caused by This function ensures that the elements in the mass matrix
|     | fit |     |     |     |     | specific |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- |
the approximation used to the data. are scaled within a range. For this particular case, we
|     |     |     |     | have | set the | scaling factor | to 3.50. |     |     |     |
| --- | --- | --- | --- | ---- | ------- | -------------- | -------- | --- | --- | --- |
Robot—Franka Figure 17 illustrates the predictive performance of our
| 6.2. Rigid | Emika | Panda |     |               |     |              |        |             |     |            |
| ---------- | ----- | ----- | --- | ------------- | --- | ------------ | ------ | ----------- | --- | ---------- |
|            |       |       |     | physics-based |     | model, where | Figure | 17b depicts | the | continuous |
ThecollecteddataareprocessedthroughaButterworthfilterin prediction error within 2s or 1000 prediction steps and
Figure17cshowsthatupdatingthemodel’sinputwithreal-time
MATLABtoreducenoise.FurtherdetailsareprovidedinTable8.
In the experiment, we observe small joint acceleration, which state data can help us make a long prediction.
|     |     |     |     | A   | controller | based on | the equation | presented | in  | (25) is pro- |
| --- | --- | --- | --- | --- | ---------- | -------- | ------------ | --------- | --- | ------------ |
resultsinminimalvelocitychange.Topreventthenetworkfrom
|     |     |     |     | posed | for the | actual robot. | The | proportional | gain | matrix, K , |
| --- | --- | --- | --- | ----- | ------- | ------------- | --- | ------------ | ---- | ----------- |
focusing solely on learning a large mass matrix and neglecting P
|                                                    |     |     |     | is set | to a          | diagonal matrix   | with | entries        | 600, 600, | 600, 600,   |
| -------------------------------------------------- | --- | --- | --- | ------ | ------------- | ----------------- | ---- | -------------- | --------- | ----------- |
|                                                    |     |     |     | 250,   | 150, and      | 50, respectively. |      | The derivative | gain      | matrix, K , |
| Table8. Pandaexperimentdetailedinformation(500Hz). |     |     |     |        |               |                   |      |                |           | D           |
|                                                    |     |     |     | is set | to a diagonal | matrix            | with | entries 30,    | 30, 30,   | 30, 10, 10, |
and5,respectively.Figure18illustratesaseriesofphotographs
|                          | Black-boxmodel                                     |     | Lagrangian-based                                  |                                                        |          |              |           |                |           |             |
| ------------------------ | -------------------------------------------------- | --- | ------------------------------------------------- | ------------------------------------------------------ | -------- | ------------ | --------- | -------------- | --------- | ----------- |
|                          |                                                    |     | learnedmodel                                      | depictingtheperiodicmovementusedtotrackasinusoidaltra- |          |              |           |                |           |             |
|                          |                                                    |     |                                                   | jectory                                                | within   | a time frame | of        | 10s. The whole | tracking  | perfor-     |
| Model(width(cid:3)depth) | 120(cid:3)5                                        |     | 40(cid:3)3,20(cid:3)2                             |                                                        |          |              |           |                |           |             |
|                          |                                                    |     |                                                   | mance                                                  | is shown | in Figure    | 19.       |                |           |             |
| Samplenumber             | 550000                                             |     | 25000                                             |                                                        |          |              |           |                |           |             |
|                          |                                                    |     |                                                   | Furthermore,                                           |          | we have      | presented | the trajectory |           | of the end- |
| Trainingepoch            | 10000                                              |     | 3000                                              |                                                        |          |              |           |                |           |             |
|                          |                                                    |     |                                                   | effector,                                              | which    | is a helical | motion    | shown          | in Figure | 20, and its |
|                          | 1.371(cid:3)10(cid:2)5(cid:5)2.03(cid:3)10(cid:2)5 |     | 1.68(cid:3)10(cid:2)7(cid:5)6.64(cid:3)10(cid:2)6 |                                                        |          |              |           |                |           |             |
Trainingerror resultant control effect has been visually demonstrated in
| Predictionerror[rad] | 182.495(cid:5)64.645(2s) |     | 2.681(cid:5)1.383(2s) | Figure | 19.  |     |     |     |     |     |
| -------------------- | ------------------------ | --- | --------------------- | ------ | ---- | --- | --- | --- | --- | --- |
|                      | (a)                      |     |                       | (b)    |      |     |     |     |     |     |
|                      | 2                        |     |                       |        | 0.05 |     |     |     |     |     |
1
0
0
-1
-0.05
-2
-0.1
|     | 0 0.5 | 1   | 1.5 2 |     | 0   | 0.5 | 1 1.5 | 2   |     |     |
| --- | ----- | --- | ----- | --- | --- | --- | ----- | --- | --- | --- |
(c)
2
1
0
-1
-2
|     | 0 1 | 2   | 3 4 5 | 6   | 7   | 8   |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
Figure17. Pandaphysics-basedlearningmodelpredictionresults:a,b)thepredictionofabout800stepsinarow;c)thepredictionresultswitha5-step
windowsize.
Figure18. PhotosequenceofoneperiodicmovementresultingfromtheapplicationoftheLNN-model-basedcontrollertrackingtrajectory.
Adv.Intell.Syst.2024,6,2300385 2300385 (14 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |     |     |     | www.advintellsyst.com |
| --------------------------- | --- | --- | --- | --------------------- |
Figure19. Performance ofthe model-based controller thatisdesignedusingthelearnedmodel:a) showsthe trajectory trackingperformanceand
b)visualizesthetorqueinputgeneratedbythecontroller.
Figure20. Photosequenceofhelicalmotionoftheend-effectorbyusingLNN-model-basedcontroller.
| (a) |     | (b) | (c) |     |
| --- | --- | --- | --- | --- |
|     |     | 2   | 30  |     |
0.4
1.5
| 0.35 |     |     | 20  |     |
| ---- | --- | --- | --- | --- |
1
0.3
| 0 10 | 20 30 | 0.5 |     |     |
| ---- | ----- | --- | --- | --- |
10
0
0
-0.5
|      |     | -1   | -10 |     |
| ---- | --- | ---- | --- | --- |
| 0.56 |     | -1.5 |     |     |
-20
| 0.51 |       | -2         |      |       |
| ---- | ----- | ---------- | ---- | ----- |
| 0.46 |       | -2.5       | -30  |       |
|      |       | 0 10 20 30 |      |       |
| 0 10 | 20 30 |            | 0 10 | 20 30 |
Figure21. Performanceofthemodel-basedcontrollerthatisdesignedusingthelearnedmodel:a)thedesiredend-effectortrajectory;b)thecorre-
spondingjoints’angleandthecontrolresults;andc)thecontroller’sinputtorquesforsuchmotion.
Adv.Intell.Syst.2024,6,2300385 2300385 (15 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

 26404567, 2024, 5, Downloaded from https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385 by National Health And Medical Research Council, Wiley Online Library on [04/05/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
| www.advancedsciencenews.com |                                               |     |     |     |     |          |     |     |     |     |     | www.advintellsyst.com |     |
| --------------------------- | --------------------------------------------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --------------------- | --- |
| Inthese                     | figures,wecanobservethatthedesignedcontroller |     |     |     |     | Keywords |     |     |     |     |     |                       |     |
hassatisfactoryperformance,asevidencedbyitsabilitytotracka
|                     |        |            |        |                |          | dissipation, | Euler–Lagrange |           | equations, |             | Hamiltonian | neural           | networks, |
| ------------------- | ------ | ---------- | ------ | -------------- | -------- | ------------ | -------------- | --------- | ---------- | ----------- | ----------- | ---------------- | --------- |
| desired trajectory. | The    | tracking   | error, | while presents | in some  |              |                |           |            |             |             |                  |           |
|                     |        |            |        |                | signifi- | Lagrangian   | neural         | networks, |            | model-based | control,    | physics-informed |           |
| joints, remains     | within | acceptable | bounds | and does       | not      |              |                |           |            |             |             |                  |           |
neuralnetworks,port-Hamiltoniansystems
cantlyimpairtheoverallperformanceofthecontrollerinpracti-
calapplications.Anexaminationofthecontroller’sperformance Received:July7,2023
reveals that, while generally effective, its performance exhibits Revised:November16,2023
Publishedonline:February23,2024
somedegreeofvariabilityacrossdifferentjoints.Theoverallper-
formanceofthecontrollerremainswithinacceptablelevelsand
suggestsitspotentialforeffectiveuseinreal-worldapplications
(Figure 21). [1] A.I.Chen,M.L.Balter,T.J.Maguire,M.L.Yarmush,Nat.Mach.
Intell.2020,2,104.
|     |     |     |     |     |     | [2] J. | Ichnowski, | Y. Avigal, | V.  | Satish, | K. Goldberg, | Sci. | Rob. 2020, 5, |
| --- | --- | --- | --- | --- | --- | ------ | ---------- | ---------- | --- | ------- | ------------ | ---- | ------------- |
eabd7710.
7. Conclusion
|     |     |     |     |     |     | [3] D. | Mukherjee, | K.  | Gupta, L. | H. Chang, | H. Najjaran, |     | Rob. Comput. |
| --- | --- | --- | --- | --- | --- | ------ | ---------- | --- | --------- | --------- | ------------ | --- | ------------ |
Integr.Manuf.2022,73,102231.
Thisarticlepresentedanapproachtoconsiderdampingandthe
[4] F.Stella,C.DellaSantina,J.Hughes,Nat.Mach.Intell.2023,5,561.
interactionbetweenrobotsandactuatorsinPINNs—specifically,
|     |     |     |     |     |     | [5] L. | Buşoniu, | T. De | Bruin, D. | Tolic´, | J. Kober, | I. Palunko, | Annu. Rev. |
| --- | --- | --- | --- | --- | --- | ------ | -------- | ----- | --------- | ------- | --------- | ----------- | ---------- |
HNNs—improving
| LNNs and |     |     | the applicability |     | of these neural | Control2018,46,8. |     |     |     |     |     |     |     |
| -------- | --- | --- | ----------------- | --- | --------------- | ----------------- | --- | --- | --- | --- | --- | --- | --- |
networks for learning dynamic models. Moreover, we used [6] P. R. Wurman, S. Barrett, K. Kawamoto, J. MacGlashan,
theRunge—Kutta4methodtoavoidaccelerationmeasurements, K. Subramanian, T. J. Walsh, R. Capobianco, A. Devlic, F. Eckert,
whichareoftenunavailable.ThemodifiedPINNsprovedsuitable
|     |     |     |     |     |     | F.  | Fuchs, | L. Gilpin, | P.  | Khandelwal, | V.  | Kompella, | H. Lin, |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---------- | --- | ----------- | --- | --------- | ------- |
forlearningthedynamicmodelofrigidandsoftmanipulators.
|     |     |     |     |     |     | P.  | MacAlpine, | D.  | Oller, T. | Seno, | C. Sherstan, | M.  | D. Thomure, |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --------- | ----- | ------------ | --- | ----------- |
Forthelatter,weconsideredthePCCapproximationtoobtaina H. Aghabozorgi, L. Barrett, R. Douglas, D. Whitehead, P. Dürr,
simplified
model of the system. P.Stone,M.Spranger,H.Kitano,Nature2022,602,223.
The modified PINN approach exploits the knowledge of the [7] N. Rudin, D. Hoeller, P. Reist, M. Hutter, in Conf. Robot Learning,
underlying physics of the system, which results in a largely PMLR,Auckland,NewZealand,December2022,pp.91–100.
|          |             |             |        |          |          | [8] I. | Akkaya, | M. Andrychowicz, |     | M. Chociej, | M.  | Litwin, | B. McGrew, |
| -------- | ----------- | ----------- | ------ | -------- | -------- | ------ | ------- | ---------------- | --- | ----------- | --- | ------- | ---------- |
| improved | accuracy in | the learned | models | compared | with the |        |         |                  |     |             |     |         |            |
A.Petron,A.Paino,M.Plappert,G.Powell,R.Ribas,J.Schneider,
baselinemodels,whichweretrainedusingafullyconnectednet-
|     |     |     |     |     |     | N.  | Tezak, | J. Tworek, | P. Welinder, | L.  | Weng, | Q. Yuan, | W. Zaremba, |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---------- | ------------ | --- | ----- | -------- | ----------- |
work.TheresultsshowthatPINNsexhibitamoreinstructiveand
L.Zhang(Preprint),arXiv:1910.07113,v1,submitted:Oct.2019.
| directional | learning process |     | because | of the prior | knowledge |     |     |     |     |     |     |     |     |
| ----------- | ---------------- | --- | ------- | ------------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
[9] W.Zhao,J.P.Queralta,T.Westerlund,in2020IEEESymp.Serieson
| embedded | into the approach. |     | Notably, | physics-based | learning |     |     |     |     |     |     |     |     |
| -------- | ------------------ | --- | -------- | ------------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
ComputationalIntelligence(SSCI),IEEE2020,pp.737–744.
modelstrainedwithfewerdataaremoregeneralandrobustthan [10] P.Kulkarni,J.Kober,R.Babuška,C.DellaSantina,Adv.Intell.Syst.
| thetraditional | black-boxones.Therefore, |     |     | continuouslong-term |     |     |     |     |     |     |     |     |     |
| -------------- | ------------------------ | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2022,4,2100095.
andvariablestep-sizepredictionscanbeachieved.Furthermore,
[11] N.Sünderhauf,O.Brock,W.Scheirer,R.Hadsell,D.Fox,J.Leitner,
| the learned | model enables | decent | anticipatory | control, | where | a   |     |     |     |     |     |     |     |
| ----------- | ------------- | ------ | ------------ | -------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
B.Upcroft,P.Abbeel,W.Burgard,M.Milford,P.Corke,Int.J.Rob.
naivePDcanbeintegratedforagoodperformance,asillustrated
Res.2018,37,405.
in the experiments performed with the Panda robot. [12] G. Antonelli, S. Chiaverini, P. Di Lillo, Nonlinear Dyn. 2023, 111,
6487.
|     |     |     |     |     |     | [13] H. | Beik-Mohammadi, |     | S.  | Hauberg, | G. Arvanitidis, |     | G. Neumann, |
| --- | --- | --- | --- | --- | --- | ------- | --------------- | --- | --- | -------- | --------------- | --- | ----------- |
Acknowledgements L.Rozo(Preprint),arXiv:2106.04315,v2,submitted:Jul.2021.
[14] A.Simeonov,Y.Du,A.Tagliasacchi,J.B.Tenenbaum,A.Rodriguez,
This work is supported by the EU EIC project EMERGE (grant no. P. Agrawal, V. Sitzmann, in 2022 Int. Conf. on Robotics and
101070918).TheauthorsaregratefultoBastianDeutschmann,theinven- Automation (ICRA), IEEE, Philadelphia, USA, December 2022,
| toroftheNECKexperimentalplatform,whichgreatlyfacilitatedthework. |     |     |     |     |     | pp.6394–6400. |     |     |     |     |     |     |     |
| ---------------------------------------------------------------- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
TheauthorswouldalsoliketoexpresstheirdeepestgratitudetoFrancesco
|     |     |     |     |     |     | [15] J. | Urain, | N. Funk, | G. Chalvatzaki, |     | J. Peters, | in 2023 | Int. Conf. on |
| --- | --- | --- | --- | --- | --- | ------- | ------ | -------- | --------------- | --- | ---------- | ------- | ------------- |
StellaandTomásColemanfortheirinvaluableguidanceandhelpinthe
|                              |                      |                 |              |              |               | Robotics      | and | Automation |     | (ICRA), | IEEE, London, | UK, | May 2023, |
| ---------------------------- | -------------------- | --------------- | ------------ | ------------ | ------------- | ------------- | --- | ---------- | --- | ------- | ------------- | --- | --------- |
| experiments.                 | Finally, the authors |                 | extend their | appreciation | to their col- | pp.5923–5930. |     |            |     |         |               |     |           |
| leaguesforinsightfulfeedback |                      | andconstructive |              | criticism,   | whichhelped   |               |     |            |     |         |               |     |           |
refinetheideasandmethods.[Correctionaddedon24March2024after [16] A. Daw, A. Karpatne, W. Watkins, J. Read, V. Kumar (Preprint),
onlinepublication:TyposinTitlewereupdatedinthisversion.] arXiv:1710.11431,v1,submitted:Oct.2017.
|     |     |     |     |     |     | [17] G. | E. Karniadakis, |     | I. G. Kevrekidis, |     | L. Lu, P. | Perdikaris, | S. Wang, |
| --- | --- | --- | --- | --- | --- | ------- | --------------- | --- | ----------------- | --- | --------- | ----------- | -------- |
L.Yang,Nat.Rev.Phys.2021,3,422.
Conflict [18] F.Djeumou,C.Neary,E.Goubault,S.Putot,U.Topcu,inLearningfor
of Interest
DynamicsandControlConf.,PMLR,StanfordUniversity,Stanford,CA,
| Theauthorsdeclarenoconflictofinterest. |     |     |     |     |     | June2022,pp.263–277. |     |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- |
[19] M.Chen,R.Lupoiu,C.Mao,D.-H.Huang,J.Jiang,P.Lalanne,J.Fan
(Preprint),v1,submitted:Aug.2021,https://doi.org/10.21203/rs.3.
| Data Availability | Statement |     |     |     |     | rs-807786/v1. |     |     |     |     |     |     |     |
| ----------------- | --------- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
[20] B.Huang,J.Wang,IEEETrans.PowerSyst.2022,38,572.
Thedatathatsupportthefindingsofthisstudyareavailablefromthecor- [21] Z.Mao,A.D.Jagtap,G.E.Karniadakis,Comput.MethodsAppl.Mech.
| respondingauthoruponreasonablerequest. |     |     |     |     |     | Eng.2020,360,112789. |     |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- |
Adv.Intell.Syst.2024,6,2300385 2300385 (16 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH

www.advancedsciencenews.com www.advintellsyst.com
[22] S. A. Niaki, E. Haghighat, T. Campbell, A. Poursartip, R. Vaziri, [41] S. S.-E. Plaza, R. Reyes-Baez, B. Jayawardhana, in Learning for
Comput.MethodsAppl.Mech.Eng.2021,384,113959. Dynamics and Control Conf., PMLR, Stanford University, Stanford,
[23] M.Cranmer,S.Greydanus,S.Hoyer,P.Battaglia,D.Spergel,S.Ho CA,June2022,pp.520–531.
(Preprint),arXiv:2003.04630,v2,submitted:Jul.2020. [42] S.Sánchez-Escalonilla,R.Reyes-Báez,B.Jayawardhana,in2022IEEE
[24] S.Greydanus,M.Dzamba,J.Yosinski,Adv.NeuralInf.Process.Syst. 61st Conf. on Decision and Control (CDC), IEEE, Cancun, Mexico,
2019,32. December2022,pp.2463–2468.
[25] Y. D.Zhong, B. Dey, A. Chakraborty, Adv. NeuralInf. Process. Syst. [43] F.Arnold,R.King,Eng.Appl.Artif.Intell.2021,101,104195.
2021,34,21910. [44] S.Mowlavi,S.Nabi,J.Comput.Phys.2023,473,111731.
[26] R.Bhattoo,S.Ranu,N.A.Krishnan,Mach.Learn.:Sci.Technol.2023, [45] J.Nicodemus,J.Kneifl,J.Fehr,B.Unger,IFAC-PapersOnLine2022,
4,015003. 55,331.
[27] M.A.Roehrl,T.A.Runkler,V.Brandtstetter,M.Tokic,S.Obermayer, [46] M. Lutter, K. Listmann, J. Peters, in 2019 IEEE/RSJ Int. Conf. on
IFAC-PapersOnLine2020,53,9195. Intelligent Robots and Systems (IROS), IEEE, The Venetian Macao,
[28] Y. D. Zhong, B. Dey, A. Chakraborty, Learning for Dynamics and Macau,November2019,pp.7718–7725.
Control,PMLR2021,pp.1218–1229. [47] C. Della Santina, Encyclopedia of Robotics, Vol. 20, Springer Berlin
[29] R.Bhattoo,S.Ranu,N.Krishnan,Adv.NeuralInf.Process.Syst.2022, Heidelberg,Berlin,Germany2021.
35,29789. [48] C. Laschi, T. G. Thuruthel, F. Lida, R. Merzouki, E. Falotico, IEEE
[30] M.Lutter,J.Peters,Int.J.Rob.Res.2023,42,83. ControlSyst.Mag.2023,43,100.
[31] C. Della Santina, M. G. Catalano, A. Bicchi, M. Ang, O. Khatib, [49] P.Pustina,C.DellaSantina,F.Boyer,A.DeLuca,F.Renda(Preprint),
B. Siciliano, Encyclopedia of Robotics, Vol. 489, Springer Berlin arXiv:2306.07258,v1,submitted:Jun.2023.
Heidelberg,Berlin,Germany2020. [50] M.Lutter,C.Ritter,J.Peters(Preprint),arXiv:1907.04490,v1,submit-
[32] J.K.Gupta,K.Menda,Z.Manchester,M.J.Kochenderfer(Preprint), ted:Jul.2019.
arXiv:1902.08705,v2,submitted:Mar.2019. [51] L. N. Trefethen, D. Bau, Numerical Linear Algebra, Vol. 181, Siam,
[33] J.K.Gupta,K.Menda,Z.Manchester,M.Kochenderfer,Learningfor Trefethen,Philadelphia,USA2022.
DynamicsandControl,PMLR2020,pp.328–337. [52] K. B. Petersen, M. S. Pedersen, The Matrix Cookbook, Technical
[34] R. M. Murray, Z. Li, S. S. Sastry, S. S. Sastry, A Mathematical UniversityofDenmark,Copenhagen,Denmark2008.
Introduction to Robotic Manipulation, CRC Press, Boca Raton, FL [53] M. Montagna,P. Pustina, A. De Luca, in I-RIM Conf., Rome, Italy,
1994. October2023.
[35] H.K.Khalil,NonlinearControl,Pearson,NewYork,NY2015. [54] P.Tomei,IEEETrans.Autom.Control1991,36,1208.
[36] C.DellaSantina,C.Duriez,D.Rus,IEEEControlSyst.Mag.2023,43, [55] R.Kelly,R.Salgado,IEEETrans.Rob.Autom.1994,10,566.
30. [56] B.Deutschmann,J.Reinecke,A.Dietrich,in2022IEEE5thInt.Conf.
[37] Y.Zheng,C.Hu,X.Wang,Z.Wu,J.ProcessControl2023,128,103005. on Soft Robotics (RoboSoft), Edinburgh, Scotland, UK, April 2022,
[38] S. Sanyal, K. Roy, in 2023 Int. Conf. on Robotics and Automation pp.54–61.
(ICRA),IEEE2023,pp.1019–1025. [57] M.W.Hannan,I.D.Walker,J.Rob.Syst.2003,20,45.
[39] L. Hewing, J. Kabzan, M. N. Zeilinger, IEEE Trans. Control Syst. [58] C.DellaSantina,A.Bicchi,D.Rus,IEEERob.Autom.Lett.2020,5,
Technol.2019,28,2736. 1001.
[40] I.Mitsioni,P.Tajvar,D.Kragic,J.Tumova,C.Pek,IEEETrans.Rob. [59] B. Deutschmann, https://github.com/DLR-RM/TendonDriven
2023,39,3242. Continuum(accessed:August2022).
Adv.Intell.Syst.2024,6,2300385 2300385 (17 of 17) ©2024TheAuthors.AdvancedIntelligentSystemspublishedbyWiley-VCHGmbH
26404567,
2024,
5,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300385
by
National
Health
And
Medical
Research
Council,
Wiley
Online
Library
on
[04/05/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License