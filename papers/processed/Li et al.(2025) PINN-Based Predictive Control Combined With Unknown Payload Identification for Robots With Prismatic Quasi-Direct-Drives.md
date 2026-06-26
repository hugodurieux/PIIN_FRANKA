IEEEROBOTICSANDAUTOMATIONLETTERS,VOL.10,NO.11,NOVEMBER2025 11275
|     | PINN-Based |         |      |     | Predictive |     |     | Control             |     | Combined |     |        |     | With |     |
| --- | ---------- | ------- | ---- | --- | ---------- | --- | --- | ------------------- | --- | -------- | --- | ------ | --- | ---- | --- |
|     |            | Unknown |      |     | Payload    |     |     | Identification      |     |          | for | Robots |     |      |     |
|     |            |         | With |     | Prismatic  |     |     | Quasi-Direct-Drives |     |          |     |        |     |      |     |
HaolinLi ,HaotangChen,YikangChai,HangZhao ,YeZhao ,YuHan ,andJianwenLuo
Abstract—This study introduces a unified control framework particularly in the realm of robotic systems [1], [2], [3], [4].
thataddressesthechallengeofpreciserobotswithQuasi-Direct-
|                      |       |     |                  |           |        |           |            | Robotic      | systems | such    | as robotic | manipulators |              | or  | quadruped  |
| -------------------- | ----- | --- | ---------------- | --------- | ------ | --------- | ---------- | ------------ | ------- | ------- | ---------- | ------------ | ------------ | --- | ---------- |
| Drives               | under |     | unknown          | payloads, | named  | as online | payload    |              |         |         |            |              |              |     |            |
|                      |       |     |                  |           |        |           |            | robots, with | their   | complex | dynamics   |              | and multiple |     | degrees of |
| identification-based |       |     | physics-informed |           | neural | network   | predictive |              |         |         |            |              |              |     |            |
control(OPI-PINNPC).Byintegratingonlinepayloadidentifica- freedom, present unique challenges for motion control. Tradi-
tionwithphysics-informedneuralnetworks(PINNs),ourapproach tional control methods often struggle to meet these demands
embedsidentifiedpayloadparametersdirectlyintotheneuralnet- duetothehighlynonlinearandcoupleddynamics[5],[6],[7].
work’slossfunction,ensuringphysicalconsistencywhileadapting
|     |     |     |     |     |     |     |     | NMPC addresses |     | these | challenges | by  | leveraging | a   | predictive |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ----- | ---------- | --- | ---------- | --- | ---------- |
tochangingloadconditions.Thephysics-constrainedneuralrep-
|     |     |     |     |     |     |     |     | model of | the system | to  | optimize | control | inputs | over | a finite |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ---------- | --- | -------- | ------- | ------ | ---- | -------- |
resentationservesasanefficientsurrogatemodelwithinournon-
linearmodelpredictivecontroller,enablingreal-timeoptimization horizon[8],[9].Unlikelinearcontrolapproaches[10],NMPC
despitethecomplexdynamicsofrobotswithQuasi-Direct-Drives. fullyembracesthenonlinearitiesinherentinsystemdynamics,
Experimentalvalidationonourrobotplatformdemonstrates35% leadingtomoreaccurateandeffectivecontrolstrategies[11].It
improvementinpositionandorientationtrackingaccuracyacross
considersthefuturestatesandconstraintsoftherobot,enabling
diversepayloadconditions,withsubstantiallyfasterconvergence
ittoanticipateandreacttochangesinterrain,disturbances,or
comparedtopreviousadaptivecontrolmethods.Ourframework
desiredtrajectoriesinreal-time[12].Thispredictivecapabilityis
| provides |     | an adaptive | solution | for | maintaining | tracking | perfor- |     |     |     |     |     |     |     |     |
| -------- | --- | ----------- | -------- | --- | ----------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
manceundervariablepayloadconditionswithoutsacrificingcom- crucialfortaskssuchasdynamicwalking,running,andjumping,
putationalefficiency. where the robot must adapt rapidly to maintain stability and
|     |       |                        |     |     |        |          |           | achieve | its objectives |     | [13]. Compared |     | with | analytical | meth- |
| --- | ----- | ---------------------- | --- | --- | ------ | -------- | --------- | ------- | -------------- | --- | -------------- | --- | ---- | ---------- | ----- |
|     | Index | Terms—Physics-informed |     |     | neural | network, | nonlinear |         |                |     |                |     |      |            |       |
ods[14],[15],NMPCincorporatesconstraintslikejointlimits,
modelpredictivecontrol,quadrupedlocomotion,identification.
friction,andcontactforcesintooptimization,ensuringcontrol
|     |     |     | I.  | INTRODUCTION |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
inputsarebothoptimalandsafeforrobot’shardware[16],[17].
NONLINEAR Model Predictive Control (NMPC) has NMPC’sflexibilityenablesadaptationtodifferentrobotdesigns
emerged as a powerful and versatile control strategy, andoperationalscenarios[18],[19].Recentadvancesincomput-
ingandoptimizationhavemadeNMPCpracticalforreal-time
Received 31 March 2025; accepted 10 August 2025. Date of publication controls.However,accuratelymodelingnonlineardynamicsin
| 4   | September | 2025; | date of current | version | 22 September | 2025. | This | article          |     |         |             |     |       |               |     |
| --- | --------- | ----- | --------------- | ------- | ------------ | ----- | ---- | ---------------- | --- | ------- | ----------- | --- | ----- | ------------- | --- |
|     |           |       |                 |         |              |       |      | NMPC constraints |     | remains | challenging |     | under | uncertainties | or  |
wasrecommendedforpublicationbyAssociateEditorK.Chatzilygeroudisand
|     |     |     |     |     |     |     |     | disturbances, | especially |     | with | the unknown |     | parameters | of the |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | ---------- | --- | ---- | ----------- | --- | ---------- | ------ |
EditorO.Stasseuponevaluationofthereviewers’comments.Thisworkwas
supportedinpartbytheNationalNaturalScienceFoundationofChinaunder locomotionmodelundervaryingpayloads[20],[21].Therefore,
Grant51905251,inpartbyShenzhenMajorScienceandTechnologyProgram
|       |       |            |     |         |                  |            |     | it is common       |     | in traditional | methods |        | to incorporate |                | parame- |
| ----- | ----- | ---------- | --- | ------- | ---------------- | ---------- | --- | ------------------ | --- | -------------- | ------- | ------ | -------------- | -------------- | ------- |
| under | Grant | 202402004, | and | in part | by the Guangdong | Provincial |     | Special            |     |                |         |        |                |                |         |
|       |       |            |     |         |                  |            |     | ter identification |     | modules        | to      | handle | model          | uncertainties. | For     |
FundsforPromotingHighQualityEconomicDevelopment(MarineEconomic
Development)inSixMajorMarineIndustriesunderGrantGDNRC[2024]52. example,theRisk-SensitiveExtendedKalmanFilterproposed
(Correspondingauthor:JianwenLuo.) in [22] effectively adapts to dynamically changing inertial pa-
|     | Haolin Li, | Haotang | Chen, Yu | Han, | and Jianwen | Luo are | with the | School |     |     |     |     |     |     |     |
| --- | ---------- | ------- | -------- | ---- | ----------- | ------- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- |
of Intelligent Systems Engineering, Shenzhen Campus of Sun Yat-sen Uni- rameters.[23]proposesanestimationmethodforthecenterof
versity, Shenzhen 518100, China, also with the Guangdong Provincial Key massandfullmomentumofhumanoidrobotsforcontrollingthe
LaboratoryofFireScienceandIntelligentEmergencyTechnology,Guangzhou momentumofhumanoidrobots.
| 510006, | China, | and | also with | General | Embodied | AI Center | of Sun | Yat-sen |     |     |     |     |     |     |     |
| ------- | ------ | --- | --------- | ------- | -------- | --------- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- |
University,Guangzhou510006,China(e-mail:haolin.li.2000@gmail.com;lu- Asroboticsystemshavegrownincreasinglycomplex,tradi-
ojw76@mail.sysu.edu.cn). tional machine learning models and purely physics-based ap-
YikangChaiiswithGeneralEmbodiedAICenter,SunYat-senUniversity, proachesfacedistinctlimitations:theformertypicallysacrifice
China(e-mail:kang.yi622@gmail.com).
physicalinterpretabilityandconsistency,whilethelatterstrug-
HangZhaoiswithRoboticsandAutonomousSystemsThrust,TheHong
KongUniversityofScienceandTechnology(Guangzhou),Guangzhou511458, gletoadapttoreal-timevariationsanduncertainties[24],[25],
China(e-mail:hangzhao@hkust-gz.edu.cn).
[26].Physics-informedNeuralNetworks(PINNs)haveemerged
YeZhaoiswiththeGeorgeW.WoodruffSchoolofMechanicalEngineer-
|     |     |     |     |     |     |     |     | as a groundbreaking |     | methodology |     | in  | robot modeling |     | and con- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | ----------- | --- | --- | -------------- | --- | -------- |
ing,GeorgiaInstituteofTechnology,Atlanta,GA30332-0530USA(e-mail:
ye.zhao@me.gatech.edu). trol,effectivelybridgingthegapbetweenconventionalphysics-
|     | This article | has | supplementary |     | downloadable | material | available | at               |     |     |              |     |         |          |       |
| --- | ------------ | --- | ------------- | --- | ------------ | -------- | --------- | ---------------- | --- | --- | ------------ | --- | ------- | -------- | ----- |
|     |              |     |               |     |              |          |           | based techniques |     | and | contemporary |     | machine | learning | [27], |
https://doi.org/10.1109/LRA.2025.3606361,providedbytheauthors.
[28],[29].
DigitalObjectIdentifier10.1109/LRA.2025.3606361
2377-3766©2025IEEE.Allrightsreserved,includingrightsfortextanddatamining,andtrainingofartificialintelligenceandsimilartechnologies.
Personaluseispermitted,butrepublication/redistributionrequiresIEEEpermission.Seehttps://www.ieee.org/publications/rights/index.htmlformoreinformation.
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:55:26 UTC from IEEE Xplore.  Restrictions apply.

11276 IEEEROBOTICSANDAUTOMATIONLETTERS,VOL.10,NO.11,NOVEMBER2025
PINNsovercometheselimitationsbyembeddingfundamen- NMPCtoaddressthechallengesoftrajectorytrackinginquadro-
tal physical laws into the architecture and training process of torsunderdynamicuncertainties.
neural networks. This integration enables PINNs to leverage PriorresearchhassuccessfullyintegratedPINNswithNMPC
priorknowledgeofphysics,reducingthedependencyonlarge frameworks,demonstratingefficacyincomplexnonlinearsys-
datasetsandimprovingmodelgeneralizability[24],[30].Byem- tems,buttheirapplicationtoreal-timeparameteridentification
beddingroboticsystemdynamicsintotheirstructure,PINNscan andcontrolfornonlinearsystemsremainslimited.
accuratelyidentifydynamicparameters.Moreover,PINNsshow
great potential in control applications. Recent research has in- III. BACKGROUND
troducedframeworkssuchasPhysics-informedNeuralNetsfor
This section introduces the research background, including
Control(PINC)[31],whichextendPINNsbyintegratingwith
thenonlineardynamicsofsinglerigidbodysystems,theNMPC
NMPC and other control techniques. The framework enables
formulation,andthecorrespondingPINNs.
real-time simulation and control of complex robotic systems,
outperformingtraditionalnumericalmethodsincomputational
A. SingleRigidBodyDynamics
efficiencyandpredictionaccuracy.
This study proposes a method to approximate the nonlinear Consider a class of robotic systems characterized by single
dynamics of robots driven by Quasi-Direct-Drives (QDD) via rigid body dynamics, whose dynamic equations are given as
a physics-informed neural network with an unknown payload follows:
(cid:2) (cid:3) (cid:3)
i b d e e lo n w tifi : cation algorithm. Three contributions are highlighted I m θ ¨ r¨ = = (cid:3) r F c c i i × − Fci F + ki(cid:3) − r m ki p × g Fki +rp ×mpg , (1)
1) Weproposeonlinepayloadidentification-basedphysics-
informed neural network predictive control (OPI- wherem∈RandI∈R3×3denotethemassandtherotational
PINNPC),anovelcontrolarchitecturethatintegrateson- inertiamatrixoftherigidbody,respectively.r ∈R3andθ ∈R3
line payload identification, PINNs, and NMPC for the denotethepositionandtheangularpositionoftherigidbody’s
QDD-driven robots tracking control in the presence of Center of Mass (CoM), respectively. Fci ∈R3 denotes the ith
unknownpayloads. control force. Fki ∈R3 denotes the ith known external force.
2) Weincorporatetheidentifiedpayloadmassandorientation mp ∈Rdenotesthemassofthepayload.g ∈R3denotesgrav-
parametersascriticalinputstothephysics-informedloss itational acceleration. rci ∈R3, rki ∈R3 and rp ∈R3 denote
functionofPINNs,enablingaccuratepredictionofsingle thepositionvectorfromtheforcesFci,Fciandmpgwithrespect
rigidbodydynamicswithunknownpayload. tothepositionoftherigidbody’sCoM,respectively.
3) Through the experiment validation on the hardware, the Toillustratetheadaptabilityof(1),weemploytworepresen-
proposedOPI-PINNPCdemonstratesfasterconvergence tativeroboticssystemsasresearchcasesforfurtherstudiesand
rateandhighertrackingaccuracy,comparedwithourpre- experimentsinthisletter:
vious work on adaptive control algorithm for quadruped 1) 3-DoFRoboticManipulatorDynamics: Asillustratedin
locomotion (ACQL) [21], while maintaining superior Fig.1,thedynamicsoftheQDD-drivenmanipulatorwithtwo
adaptationacrosspayloadvariations. rotationalDoFandonetranslationalDoFisgivenasfollows:
(cid:2) (cid:3)
II. RELATEDWORK m Iθ ¨ r¨ = = (cid:3) F rc c i i × − F m ci pg +rp ×mpg , (2)
TraditionalNMPCreliesonprecisemodelsofsystemdynam-
where r and θ are the position and the angular position of the
ics,whichareoftendifficulttoformulateforhigh-dimensional
CoM, notice that due to the negligible mass (0.15kg) of the
or uncertain robotic platforms such as legged locomotion or
linearguiderelativetothepayloadappliedatthemanipulator’s
soft robotics. On the other hand, PINNs have demonstrated
end-effector,theCoMofthesystemcanbeapproximatedatthe
remarkable potential in approximating nonlinear physical sys-
tems by embedding governing equations into neural network
end-effector(seeFig.1).Fciistheithcontrolforceprovidedby
theithmotor.
training[27].
2) Quadruped Locomotion Dynamics: We also use Kirin,
RecentadvancementsinintegratingPINNswithNMPChave
a specifically designed quadruped robot featuring electrically
shown promise in addressing the limitations of traditional
actuated prismatic knee joints [33], as the platform for the
NMPC for nonlinear systems with uncertainties. [32] applies
demonstrationofourproposedmethod,asshowninFig.1.The
PINNs to adaptive MPC for autonomous underwater vehicles
nonlineardynamicfunctionisdescribedasfollows:
(AUVs), achieving energy-efficient tracking with actuator dy- (cid:2) (cid:3) (cid:3)
n im am pr i o c v s e a s n d d y d n is a t m ur i b cs an p c a e ra r m eje e c te ti r o i n d . e T n h ti e fi H ca - t P io IN n N an p d ro m p o o d s e e l d p in re [ d 2 i 6 c ] - m Iθ ¨ r¨ = = (cid:3) F rc c i i × − Fci m + i(cid:3) g− ri m × pg mig+rp ×mpg , (3)
tion for collaborative robot joints, outperforming conventional
PINNs and the non-linear grey-box state-space identification wherer denotesthepositionofthequadrupedrobot’sCoM.θ
method (NLGR) in accuracy and training efficiency. [24] pro- denotesthepostureofrobot’smainbody.Fcidenotesthecontact
poses a hybrid control framework that integrates PINNs with force of ith leg, which is related to the actual actuator control
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:55:26 UTC from IEEE Xplore. Restrictions apply.

LIetal.:PINN-BASEDPREDICTIVECONTROLCOMBINEDWITHUNKNOWNPAYLOADIDENTIFICATIONFORROBOTS 11277
TheoverallframeworkofOPI-PINNPCandthecoordinationdefinitionoftherobot.(i)Trainingphase(switchS¯
| Fig.1. |     |     |     |     |     |     |     |     |     |     |     | closed):OPImoduleestimatesthe |     |     |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------------------- | --- | --- | --- |
unknownpayloadparametersviatheinputdata.Theidentifiedparameterssubsequentlyconstructthephysics-informedloss,whichiscombinedwiththedataloss
computedbylabeleddatatooptimizethenetworkweightsthroughbackpropagation.(ii)Predictionphase(switchSclosed):OPIsynthesizespayloadparameters
usingreal-timerobotstates,followedbythePINNsstatepredictionfulfillingNMPCintegrationrequirements,ultimatelygeneratingcompositecontrolinputs
consistingoftheoptimalcontrolviaNMPCoptimizationandthefeedbackcontrol.
√
forcethroughaJacobiantransformation,asdetailedin[33].mi where(cid:3)∗(cid:3) = ∗TM∗.AndΔukrepresentsthecontrolinput
| denotesthemassofith |     |     |     |     |     |     |     |     | M   |     |     |     |     |     |     |
| ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
leg.Thesymbolnotationsarethesame increment at time instant k, Q and R are diagonal matrices
asthosein[33].
thatweightthepenalizationoftrackingerrorandcontrolinput
| Infact,theQDD-drivenmanipulatorinFig.1canberegarded |     |     |     |     |     |     |     | increments. |     |     |     |     |     |     |     |
| --------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
ashalfpartofthequadrupedrobot,sincebothoftheirprismatic
AprimarychallengeinsolvingtheaboveNMPCproblemis
jointsaredrivenbyQDD. thecomputationalcomplexityandnumericalprecisioninherent
|     |     |     |     |     |     |     |     | in numerical | integration |     | processes. | To  | mitigate | this | compu- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ----------- | --- | ---------- | --- | -------- | ---- | ------ |
B. NonlinearModelPredictiveControl
|     |     |     |     |     |     |     |     | tational | burden, | this study | employs | the | PINNs | framework | to  |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------- | ---------- | ------- | --- | ----- | --------- | --- |
capturetheunderlyingnonlineardynamicsandenablerapidstate
Nonlineardynamicsin(1)istypicallyexpressedinthegeneral
| controlsystemformasbelow: |     |     |     |          |     |     |     | prediction. |     |     |     |     |     |     |     |
| ------------------------- | --- | --- | --- | -------- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
|                           |     |     | x˙  | =f(x,u), |     |     |     |             |     |     |     |     |     |     |     |
(4) C. Physics-InformedNeuralNetworks
| where | x=x(t) | denotes | the | state variables, |     | u=u(t) | denotes |       |            |      |          |           |     |      |          |
| ----- | ------ | ------- | --- | ---------------- | --- | ------ | ------- | ----- | ---------- | ---- | -------- | --------- | --- | ---- | -------- |
|       |        |         |     |                  |     |        |         | PINNs | is a novel | deep | learning | framework |     | that | combines |
thecontrolinput.Thedynamicsfunctionf(x,u)isassumedto
|                          |     |     |     |                |            |     |          | data-driven | approaches  |         | with fundamental |         | physical |     | principles. |
| ------------------------ | --- | --- | --- | -------------- | ---------- | --- | -------- | ----------- | ----------- | ------- | ---------------- | ------- | -------- | --- | ----------- |
| be Lipschitz-continuous. |     |     | Eq  | (4) is usually | formulated |     | into the |             |             |         |                  |         |          |     |             |
|                          |     |     |     |                |            |     |          | It excels   | at modeling | dynamic |                  | systems | governed | by  | ordinary    |
discreteformasrewrittenbelow: differentialequations(ODE)andpredictingsystemstates.Con-
|     |     |     |                 |     |     |     |     | s id e r t h | e O D E | in ( 5 ) | , t he p r | i m a ry o | b jec t i v | e o f P | IN N s l ie s |
| --- | --- | --- | --------------- | --- | --- | --- | --- | ------------ | ------- | -------- | ---------- | ---------- | ----------- | ------- | ------------- |
|     |     |     | xk+1 =h(T,xk,uk |     | ),  |     | (5) |              |         |          |            |            |             |         |               |
Φ
|     |     |     |     |     |     |     |     | in c o n s t | ruc ti ng | a fu n c t | io n ( | t y p ic all y | a n e u | r al n e tw | or k ) t h a t |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --------- | ---------- | ------ | -------------- | ------- | ----------- | -------------- |
wherexk anduk denotethestatevariablesandcontrolinputat approximatesthedynamicsof(5),thatis,
| timeinstantk,andT |      |              | isthesamplingtimeinterval. |        |           |            |     |     |     |      |     |            |     |     |     |
| ----------------- | ---- | ------------ | -------------------------- | ------ | --------- | ---------- | --- | --- | --- | ---- | --- | ---------- | --- | --- | --- |
|                   |      |              |                            |        |           |            |     |     |     | ≈xˆ  |     | =Φ(T,xk,uk | ).  |     |     |
|                   | xref | ,i=1,2,...,N |                            |        |           |            |     |     |     | xk+1 | k+1 |            |     |     | (8) |
| Given             | k+i  |              |                            | as the | reference | trajectory | se- |     |     |      |     |            |     |     |     |
quenceofsystem(5)attimeinstantkwithapredictionhorizon ThelossfunctionofPINNstypicallyconsistsoftwocompo-
N.TheNMPCcanbeformulatedas:
nents,whicharegivenbymeansquarederror(MSE):
|     |     | (cid:4)N    |     |                | N(cid:4)−1     |          |     |     |     |          |     |          |     |     |     |
| --- | --- | ----------- | --- | -------------- | -------------- | -------- | --- | --- | --- | -------- | --- | -------- | --- | --- | --- |
|     |     |             |     |                |                |          |     |     | MSE | =MSEdata |     | +MSEphy, |     |     | (9) |
|     | min | (cid:3)xk+i | −x  | r e f (cid:3)2 | + (cid:3)Δuk+j | (cid:3)2 |     |     |     |          |     |          |     |     |     |
|     |     |             |     | k + i Q        |                | R        | (6) |     |     |          |     |          |     |     |     |
Δu
k+j i=1 j=0 where the first component MSEdata represents the data loss
⎧
|     |      |                 |       |                |          |     |     | function   | that evaluates |          | the deviation | between    |       | the output | from |
| --- | ---- | --------------- | ----- | -------------- | -------- | --- | --- | ---------- | -------------- | -------- | ------------- | ---------- | ----- | ---------- | ---- |
|     |      | ⎪⎪⎪⎪⎪⎪⎨u        | =     | (T             | )        |     |     |            |                |          |               |            |       |            |      |
|     |      | xk + i +        | 1 h   | ,x (cid:3)k+ i | , u k+ i |     |     |            |                |          |               |            |       |            |      |
|     |      |                 |       |                |          |     |     | P IN N s   | a n d l a b el | e d data | as the        | supervised | part. | MSEdata    | is   |
|     |      |                 | =     | + i            | Δ        |     |     |            |                |          |               |            |       |            |      |
|     |      | k + i +         | 1 uk  | j =            | 0 u k +j |     |     | de fin e d | a s fo l lo w  | s :      |               |            |       |            |      |
|     | s.t. |                 | ≤     | ≤              |          |     |     |            |                |          |               |            |       |            |      |
|     |      | ⎪⎪⎪⎪⎪⎪⎩ u m i n | uk +i | u m ax         |          |     |     |            |                | 1        | N(cid:4)data  |            |       |            |      |
Δ u ≤ Δ u ≤ Δumax MSEdata = (cid:3)xˆ (T,xk,uk )−xi (cid:3)2 , (10)
|     |     | m i | n   | k+ i |     |     |     |     |     |     |     | i   |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Nd ata
|     |     | xmin       | ≤xk+i | ≤xmax |     |     |     |        |            |      | i=1  |          |            |         |        |
| --- | --- | ---------- | ----- | ----- | --- | --- | --- | ------ | ---------- | ---- | ---- | -------- | ---------- | ------- | ------ |
|     |     |            |       |       |     |     |     | where  | xi denotes | the  | true | state of | the        | dynamic | system |
|     |     | ∀i=0,...,N |       | −1,   |     |     | (7) | ith    |            |      |      |          | {({T,xk,uk | },xi    | ):i=   |
|     |     |            |       |       |     |     |     | of the | labeled    | data | from | dataset  |            |         |        |
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:55:26 UTC from IEEE Xplore.  Restrictions apply.

11278 IEEEROBOTICSANDAUTOMATIONLETTERS,VOL.10,NO.11,NOVEMBER2025
1,2,...,Ndata }withthenumberoflabeleddatasamplesNdata. where we define x1 = [xT
11
,xT
12
]T =[rT,θT]T, x2 =
xˆ
i
(T,xk,uk )denotestheoutputfromPINNswith{T,xk,uk } [xT
21
,xT
22
]T =[r˙T,θ ˙T]T andx=[xT
1
,xT
2
]T,(12)canberewrit-
astheinput. teninthefollowingstandardstate-spaceform:
Thesecondcomponentofthelossfunction(9)isthephysics- (cid:9) (cid:10) (cid:9) (cid:10) (cid:9) (cid:10)
O I O O
informedlossfunctionMSEphy: x˙ = O 6 6 × × 6 6 O 6 6 ×6 x+ A 1f 6 ¯ 1 + A 1f 6 ˆ 1 , (13)
1 N(cid:4)phy (cid:9) (cid:10)
MSEphy =
Nphy k=1
(cid:3)Φ˙(T,xk,uk )−f(xk,uk )(cid:3)2 , (11)
whereA 1,f ¯ 1andf ˆ 1aregivenby:A 1 = O m
1I
3
O
I− 3× 1 3 ,f ¯ 1 =
(cid:9) (cid:3) (cid:3) (cid:10) (cid:9) 3×3 (cid:10)
whereNphy denotesthenumberofunlabeleddata.{T,xk,uk } (cid:3) Fci − (cid:3) Fki ,f ˆ 1 = −mpg .
is the unlabeled data points that do not have a corresponding rci ×Fci + rki ×Fki rp ×mpg
known output, which is gathered through random sampling of ˆ
Duetothepresenceofunknownpayload,thetermf1of(13)
the collocation points, a method similar to those described in
is to be identified. Building upon our previous investigations
previousstudies[24],[31].Thisapproachallowsustoincorpo-
in adaptive control for quadruped locomotion [21], this study
ratephysicalinformationintothenetworktraining.
extractstheonlinepayloadidentificationalgorithmofACQLto
identifytheunknowntermsmp andrp ×mpgin(1).
IV. METHODS Due to the QDD featuring a lower reduction ratio, enabling
directutilizationofjointcurrentsignalsforpayloadestimation.
This study primarily investigates the robot control problem
under unknown payload conditions. It is well-known that the
Therefore,theidentificationofmpisgivenasfollows,whichis
thesameasthe(7)in[21].
NMPC formulation requires an accurate dynamic model for
numericalintegration,andobtaininganaccuratedynamicmodel 1(cid:4) 1(cid:4) mr¨
mˆ p = Fci − Fki − , (14)
forroboticsystemischallenginginthepresenceofanunknown g g g
payload. To address the challenges, this study proposes OPI-
Toestimaterp ×mpg,thesecondrowformulationof(12)is
PINNPCforroboticsystemswithpayloadvariation.
rewrittenasfollows:
⎧
⎨x˙
12
=x22
A. ArchitectureofOPI-PINNPC x˙
22
=u+l+k
, (15)
AsillustratedinFig.1,OPI-PINNPCincorporatesfourcom- ⎩ ˆ l ˙ =ψ
ponents:(i)anonlinepayloadidentification(OPI)modulethat (cid:3)
estimatespayloadproperties,(ii)aPINNsarchitecturethatgen- whereu(cid:3) =I−1 rci ×Fcidenotestheauxiliarycontrolinput,
eratesstatepredictionsthroughlearnedsystemdynamics,(iii)a k =I−1 ri ×mig, l=I−1rp ×mpg denotes the unknown
ˆ
modifiedNMPCprocedurethatreplacesnumericalintegration parametertobeidentified.ldenotestheestimatedvalueofl,ψ
implementation with PINNs inference, and (iv) a composite denotestheadaptiveupdatelaw.
controllercombiningthefeedbackandfeedforwardcontrolthat For the given reference tracking signal of orientation xref,
12
deployedforroboticsystems. let x˜ 1 =x12 −xr 1 e 2 f, we have x˜˙ 1 =x˙ 12 =x22. Introduce the
Notably,theobjectiveofthisworkistoestablishamapping auxiliaryerrorvariables¯=x˜˙ 1 +Wx˜ 1 whereW isapositive
between payload variations and the robot’s dynamics through definitematrix,wehave:
the PINNs architecture. To achieve this, the OPI module is
embeddedintothePINNsframework,wheretheidentifiedpay-
s¯˙ =u+k+l+Wx22. (16)
loadparametersformulatethephysics-informedloss,enabling Then,thecontrollawandadaptiveupdatelawareproposed:
the PINNs to learn the intrinsic relationship between payload
parametersandrobotdynamicsinsteadofrelyingontheprecise u=−k−ˆ l−Wx22 +Vr, (17)
(cid:11)
measurementofthesystemstates.Thisdesignensuresaccurate ψ =−K(u+ˆ l+Ψ(x12,x22 )+k)
predictionoftherobot’sstatevariablesunderarbitrarypayload , (18)
z˙ =−Kz
conditions.
where V is a positive definite matrix, K denotes the gain
B. FormulationandAlgorithmofOPI-PINNPC
diagonal matrix, Ψ(x12,x22 ) is chosen as Kx22, z =ˆ l−l+
Ψ(x12,x22 ).
Consideranunknownpayload,(1)isreformulatedasfollows: It has been proven that with the action of auxiliary control
ˆ
(cid:9) (cid:10) (cid:9) (cid:10)(cid:9) (cid:3) (cid:3) (cid:10) law (17) and update law (18), the estimated value l is able to
r¨ = m 1I 3 O 3×3 (cid:3) Fci − (cid:3) Fki converge to the true value l, and the auxiliary error variable s¯
θ ¨ O 3×3 I−1 rci ×Fci + rki ×Fki convergestozeroaswell[21].
(cid:9) (cid:10)(cid:9) (cid:10) With the identified mˆ p and ˆ l, define ωˆ =[mˆ p, ˆ lT]T and the
+ m 1I 3 O 3×3 −mpg . (12) identifieddynamicsofsystem(13)canbedescribedasfollows:
O 3×3 I−1 rp ×mpg x˙ =f ˜(x,u,ωˆ)=f ¯(x,u)+f ˆ(ωˆ), (19)
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:55:26 UTC from IEEE Xplore. Restrictions apply.

LIetal.:PINN-BASEDPREDICTIVECONTROLCOMBINEDWITHUNKNOWNPAYLOADIDENTIFICATIONFORROBOTS 11279
¯(x,u)isgivenby:
| wheref |         |     |         |     |          |         |          |      | Algorithm1:OPI-PINNPCAlgorithm. |     |     |     |     |     |
| ------ | ------- | --- | ------- | --- | -------- | ------- | -------- | ---- | ------------------------------- | --- | --- | --- | --- | --- |
|        |         |     | (cid:9) |     | (cid:10) | (cid:9) | (cid:10) |      |                                 |     |     |     |     |     |
|        |         |     | O       | I   |          | O       |          |      |                                 |     |     |     |     |     |
|        | ¯(x,u)= |     | 6 ×     | 6   | 6 x+     |         | 6        |      |                                 |     |     |     |     |     |
|        | f       |     |         |     |          |         | ¯ ,      | (20) |                                 |     |     |     |     |     |
|        |         |     | O       | O   |          | A 1f    |          |      |                                 |     |     |     |     |     |
|        |         |     | 6 ×     | 6   | 6 ×6     |         | 1        |      |                                 |     |     |     |     |     |
ˆ(ωˆ)isgivenby:
andf
|     |     |     |     | (cid:9) | (cid:10) |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
O
|            |                                               |     | ˆ(ωˆ)= |     | 6    |     |     |      |     |     |     |     |     |     |
| ---------- | --------------------------------------------- | --- | ------ | --- | ---- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
|            |                                               |     | f      |     |      | .   |     | (21) |     |     |     |     |     |     |
|            |                                               |     |        | A   | ˆ    |     |     |      |     |     |     |     |     |     |
|            |                                               |     |        |     | 1f 1 |     |     |      |     |     |     |     |     |     |
| ¯(x,u)andf | ˆ(ωˆ)denotethenominaldynamicsandtheidentified |     |        |     |      |     |     |      |     |     |     |     |     |     |
f
dynamicsofthesystem,respectively.
Discretizethesystem(19)tothediscrete-timemodel:
|             |                                    |      | =h ¯(T,xk,uk  |     | )+h  | ˆ(ωˆ).      |             |      |     |     |     |     |     |     |
| ----------- | ---------------------------------- | ---- | ------------- | --- | ---- | ----------- | ----------- | ---- | --- | --- | --- | --- | --- | --- |
|             |                                    | xk+1 |               |     |      |             |             | (22) |     |     |     |     |     |     |
| In summary, |                                    | the  | true dynamics |     | of a | single      | rigid body  | sys- |     |     |     |     |     |     |
| tem consist | of                                 | two  | components:   |     | (i)  | the nominal | dynamics    |      |     |     |     |     |     |     |
| ¯(T,xk,uk   |                                    |      |               |     |      |             | ˆ(ωˆ)w.r.t. |      |     |     |     |     |     |     |
| h           | )and(ii)theunknownpayloaddynamicsh |      |               |     |      |             |             |      |     |     |     |     |     |     |
ωˆ.
| the unknown |     | payload | parameters |     | In  | this study, | the | PINNs |     |     |     |     |     |     |
| ----------- | --- | ------- | ---------- | --- | --- | ----------- | --- | ----- | --- | --- | --- | --- | --- | --- |
methodologyisemployedtoconstructanaccurateapproxima-
tionofthetruesystemdynamics,formulatedas:
|     |                 |     |     | ¯(T,xk,uk |     | ˆ(ωˆ), |     |      |     |            |     |     |     |     |
| --- | --------------- | --- | --- | --------- | --- | ------ | --- | ---- | --- | ---------- | --- | --- | --- | --- |
|     | Φ(xk,uk,T,ωˆ)≈h |     |     |           |     | )+h    |     | (23) |     | ∀i=0,...,N |     | −1. |     |     |
(27)
ωˆ
where is the identified payload information. The data loss The NMPC above is numerically solved through the OSQP
| functionisdefinedas: |     |     |     |     |     |     |     |     |                                              |     |     |     |     | opt    |
| -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- | ------ |
|                      |     |     |     |     |     |     |     |     | solver[34],andthentheoptimalcontrolsolutionu |     |     |     |     | ofNMPC |
k
|         |     |     | N(cid:4)data |                           |     |     |          |      |                                |      |     |           | pid                        |          |
| ------- | --- | --- | ------------ | ------------------------- | --- | --- | -------- | ---- | ------------------------------ | ---- | --- | --------- | -------------------------- | -------- |
|         |     | 1   |              |                           |     |     |          |      | is combined                    | with | PID | control u | k that synthesizes         | the com- |
| MSEdata | =   |     |              | (cid:3)Φ(xk,uk,T,ωˆ)−xk+1 |     |     | (cid:3)2 | .    |                                |      |     |           |                            |          |
|         |     |     |              |                           |     |     |          | (24) | positecontroller(asin[21])addr |      |     |           | essingthetrackingcontrolof |          |
Ndata
|     |     |     | i=1 |     |     |     |     |     | quadrupedlocomotion. |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- |
The labeled dataset is the input-output pairs Algorithm1providesthepseudo-codeofastep-by-stepreal-
({xk,uk,T,ωˆ},xk+1 ) (see Section V-B). The inputs are izationofthecompleteOPI-PINNPCprocess,detailingsequen-
associated with measurable state variables xk, control inputs tial operations across its identification, prediction, and control
uk andsamplingtimeT.Theoutputisthecorrespondingstate phasesaspreviouslyformulated.
| variables | of  | the next | instant | xk+1. | Note | that | the identified |     |     |     |     |     |     |     |
| --------- | --- | -------- | ------- | ----- | ---- | ---- | -------------- | --- | --- | --- | --- | --- | --- | --- |
payloadparametersωˆisalsointegratedasinputstoenhancethe
V. EXPERIMENT
generalizationofPINNs.
Inthissection,hardwareexperimentsareconductedtoverify
Theidentifiedpayloadinformationωˆ
issubsequentlyincor-
theefficacyoftheproposedmethodonourrobotplatforms.
poratedintothephysics-informedlossfunctiontoderivethetrue
dynamicsofsinglerigidbodysystem.Thephysicslossfunction
|     |     |     |     |     |     |     |     |     | A. ExperimentSetup |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- |
isdefinedasfollows:
|     |     |     |     |     |     |     |     |     | Tovalidatetheperformance |     |     | ofOPI-PINNPC,testsarecon- |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | ------------------------- | --- | --- |
1 N(cid:4)phy
|     |     |     | (cid:3)Φ˙(xk,uk,T,ωˆ)−f |     |     | ˜(xk,uk,ωˆ)(cid:3)2 |     |     |     |     |     |     |     |     |
| --- | --- | --- | ----------------------- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
MSEphy = . ducted on a real manipulator and quadruped robot with QDD.
Nphy The manipulator possesses 3 DoFs with two rotational joints
k=1
(25)
|     |     |     |     |     |     |     |     |     | and one | prismatic | joint. | Each joint | is driven | by QDD with a |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------- | ------ | ---------- | --------- | ------------- |
BasedonthetwolossfunctionsMSEdataandMSEphy,the 20:1 gear ratio. Such design makes the robotic manipulator
PINNsistrainedtocapturethetruedynamicsofsinglerigidbody sufficiently lightweight relative to the applied payloads while
system. The learned predictive model subsequently replaces maintainingstructuralintegrityforsupportinglarge-massloads.
conventional numerical integration in the NMPC framework, Similarly,thequadruped robothas12degrees-of-freedom and
whichisreformulatedasfollows: weighs around 50 kg without payload and can be loaded with
(cid:4)N N(cid:4)−1 uptoamaximumof225kgpayloadduetotheprismaticknee
min (cid:3)xk+i −x r e f (cid:3)2 + (cid:3)Δuk+j (cid:3)2 joints driven by QDD. Prismatic QDD is a trade-off solution
|     |     |     |     | k + i Q |     |     | R   | (26) |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
Δu
k+j i=1 j=0 tobalancebetweentheproprioceptivejoints,impactmitigation,
⎧
andhigh-bandwidthphysicalinteraction.
|     | ⎪⎪⎪⎪⎪⎪⎨u |           | = Φ (x |               |          | ωˆ )  |     |     |                  |            |          |               |                    |                        |
| --- | -------- | --------- | ------ | ------------- | -------- | ----- | --- | --- | ---------------- | ---------- | -------- | ------------- | ------------------ | ---------------------- |
|     | xk       | + i + 1   |        | k+(cid:3)i, u | k + i, T | ,     |     |     |                  |            |          |               |                    |                        |
|     |          |           | =      | + i           | Δ        |       |     |     |                  |            |          |               |                    |                        |
|     |          | k + i + 1 | uk     | j             | = 0 u    | k + j |     |     | B. PINNsTraining |            |          |               |                    |                        |
|     | s.t. u   | ≤         | uk     | ≤ u           |          | ,     |     |     |                  |            |          |               |                    |                        |
|     | ⎪⎪⎪⎪⎪⎪⎩  | m i n     | +i     | m ax          |          |       |     |     |                  |            |          |               |                    |                        |
|     |          |           |        |               |          |       |     |     | T h e            | p r op o s | e d P IN | N s a r c hit | ec t ure co n s is | t s of a 4 - l a y e r |
|     | Δ        | u         | ≤ Δ u  | ≤             | Δumax    |       |     |     |                  |            |          |               |                    |                        |
m i n k+ i mu lt i lay e r p e r c ept ro n ( M L P ) w it h 96 n e u r o ns pe r h i d d e n
xmin ≤xk+i ≤xmax layer, activated by ReLU functions, chosen to balance model
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:55:26 UTC from IEEE Xplore.  Restrictions apply.

11280 IEEEROBOTICSANDAUTOMATIONLETTERS,VOL.10,NO.11,NOVEMBER2025
|     |     |     |     |     |     |     | Fig.3. | RMSEofpositionwithOPI-PINNPCanddata-onlymodelacrosswater |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | -------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
fillingcapacityfrom25%to100%.(a)theRMSEofpositionundervaryingwater
fillingcapacity.(b)theRMSEofangularpositionundervaryingwaterfilling
capacity.
sequencesgeneratedinGazebosimulation,encompassingsys-
temstates,controlinputs,andpayloadconditions.Thelabeled
|     |     |     |     |     |     |     | dataset | is collected | from | real | robot | with | ACQL. | The | ratio of |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------ | ---- | ---- | ----- | ---- | ----- | --- | -------- |
labeleddatapointstocollocationpointsisapproximately1:10.
Theselectionofadjustableparametersisgivenas:W=0.6I
3,
|     |     |     |     |     |     |     | V=0.8I   | 3,   | K=1.7I    | 3. The | training | performance |     | of        | PINNs |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---- | --------- | ------ | -------- | ----------- | --- | --------- | ----- |
|     |     |     |     |     |     |     | exhibits | that | the total | loss   | function | eventually  |     | converges | to    |
1×10−4
|     |     |     |     |     |     |     |     | .   | Beyond | the training |     | process, | the | trained | PINNs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------------ | --- | -------- | --- | ------- | ----- |
modeldemonstratesanaveragepredictionlatencyof2.3ms,and
|     |     |     |     |     |     |     | the OSQP   | solver | completes |      | the optimization |      | within4.8ms |               | per |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | --------- | ---- | ---------------- | ---- | ----------- | ------------- | --- |
|     |     |     |     |     |     |     | iteration, | which  | results   | in a | total cycle      | time | of          | approximately |     |
7.1msensuringcompatibilitywiththe100Hzcontrolloop.
|     |     |     |     |     |     |     | C. AblationStudy |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Fig.2. Experimentforvalidationoftheproposedmethodformanipulationand ThebaselinemodelillustratedinSectionIIIincorporatestwo
quadrupedlocomotion.(a)presentsthereferencetrajectoryandtheexperiment corelossterms:thephysics-informedlossMSEphyandthedata
scenariowiththewaterbottleasanunknownpayloadfillinglevelsrangingfrom
lossMSEdata.Duetothesignificanceofthephysics-informed
25%to100%ofthemanipulationexperiment.(b)showstheexperimentscenario
showingpayloadsofvaryingmassesfrom25kgto100kgandthetrottingtest loss in PINNs, we investigate the following ablation scenario:
with50kgpayloadofquadrupedrobot. thephysics-informedlossMSEphytermisremoved,forcingthe
modeltorelyentirelyonsamplingdata.Thisablationstudyis
implementedintheQDD-drivenmanipulatortrajectorytracking
experimentundervaryingpayloadconditions(25%-100%water
| expressiveness | and | computational | efficiency |     | for | real-time |     |     |     |     |     |     |     |     |     |
| -------------- | --- | ------------- | ---------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
filling).
deployment.Thenetworkistrainedusingahybridoptimization
|                |            |            |           |         |             |      | The   | experiment | results  |            | in Fig. | 3 show   | that       | the data-only |          |
| -------------- | ---------- | ---------- | --------- | ------- | ----------- | ---- | ----- | ---------- | -------- | ---------- | ------- | -------- | ---------- | ------------- | -------- |
| strategy,      | similar to | the method | in [24].  | Initial | convergence |      |       |            |          |            |         |          |            |               |          |
|                |            |            |           |         |             |      | model | (with      | 100 data | sequences) |         | produces | a relative |               | error of |
| is accelerated | via the    | Adam       | optimizer | with    | a learning  | rate |       |            |          |            |         |          |            |               |          |
25.2%comparedtotheOPI-PINNPCframework,demonstrating
| of 1×10−3 | for 5000 | epochs, | after | observing | that | smaller |     |     |     |     |     |     |     |     |     |
| --------- | -------- | ------- | ----- | --------- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
values(1×10−4)ledtoslowconvergence,whilelargervalues significant overfitting to noisy measurements and the sparse
|     |     |     |     |     |     |     | data. | Specifically, | the | tracking | error | of  | the data-only |     | model |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------------- | --- | -------- | ----- | --- | ------------- | --- | ----- |
(1×10−2)causedinstability,followedbyfine-tuningusingthe
demonstratesamarkedincreasewiththeescalationofpayload
L-BFGSquasi-Newtonmethodforenhancedprecision.
mass.Thisphenomenonisprimarilyattributedtoitspoorgen-
| A Gazebo | simulation | platform | is adopted |     | to generate | the |     |     |     |     |     |     |     |     |     |
| -------- | ---------- | -------- | ---------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
eralizationtounmodeledpayloaddynamics.
| unlabeled | data for the | manipulator | and | the | quadruped | robot |     |     |     |     |     |     |     |     |     |
| --------- | ------------ | ----------- | --- | --- | --------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
undervaryingpayloadconditions.Payloadsrangingfrom2kg
|          |           |        |                |     |                 |     | D. OPI-PINNPCforManipulationTrackingTest |     |     |     |     |     |     |     |     |
| -------- | --------- | ------ | -------------- | --- | --------------- | --- | ---------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| to 10 kg | and 25 kg | to 100 | kg are applied | to  | the manipulator |     |                                          |     |     |     |     |     |     |     |     |
andthequadrupedrobot’storso,respectively.Atotalof100dis- In this subsection, a manipulation tracking test is first con-
tinct10-secondmotionsequencescontainingjointangles,joint ducted to verify the trajectory tracking accuracy with OPI-
torques,linear/angularpositionofCoMandpayloadinformation PINNPC for manipulation. As shown in Fig. 2(a), a 2000 ml
arerecordedatasamplingrateof100Hzduringsimulationtasks. waterbottlerepresentingtheunknownpayloadisattachedtothe
Following the methodology outlined in [31], the unlabeled end-effectorofthemanipulatorwithwaterfillinglevelsadjusted
({xi,ui,T,ωˆi},xi)
dataset 0 are randomly selected (following from25%to100%.Thereferencetrajectoryisgeneratedthrough
a uniform distribution across the time sequence) from motion cubic spline interpolation of 4 spatial coordinates defined in
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:55:26 UTC from IEEE Xplore.  Restrictions apply.

LIetal.:PINN-BASEDPREDICTIVECONTROLCOMBINEDWITHUNKNOWNPAYLOADIDENTIFICATIONFORROBOTS 11281
Fig.4. Trackingperformanceoftheroboticmanipulatorundervaryingpay-
| load conditions | (25%-100% |     | water filling). | (a) the | RMSE | of position | under |     |     |     |     |     |     |
| --------------- | --------- | --- | --------------- | ------- | ---- | ----------- | ----- | --- | --- | --- | --- | --- | --- |
varyingwaterfillingcapacity.(b)theRMSEofangularpositionundervarying
waterfillingcapacity.(c)thepositiontrackingerrornormcurvesunder50%
waterfillingwithexternaldisturbanceatt=1s.(d)theangularpositiontracking
errornormcurvesunder50%waterfillingwithexternaldisturbanceatt=1s.
|     |     |     |     |     |     |     |     | Fig.5.        | Positionandorientationtrackingerrorcurvesoftrottingtestunder |           |                  |     |              |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | ------------------------------------------------------------ | --------- | ---------------- | --- | ------------ |
|     |     |     |     |     |     |     |     | 50 kg payload | with OPI-PINNPC                                              | and ACQL. | (a) demonstrates |     | the position |
trackingerrorsalongthex-,y-,andz-axes,respectively.(b)showstheorientation
|     |     |     |     |     |     |     |     | tracking errors | in yaw, pitch, | and roll angles, | respectively. | (c) | presents the |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | -------------- | ---------------- | ------------- | --- | ------------ |
thexozplane.Also,comparativeexperimentsareimplemented
|         |              |     |            |        |     |         |      | comparison | position tracking | error norm curves. | (d) | shows the | comparison |
| ------- | ------------ | --- | ---------- | ------ | --- | ------- | ---- | ---------- | ----------------- | ------------------ | --- | --------- | ---------- |
| between | the proposed |     | OPI-PINNPC | method |     | and the | ACQL |            |                   |                    |     |           |            |
orientationtrackingerrornormcurves.
methodreportedin[21].
Fig.4(a)and4(b)presentthepositionandorientationtracking
errorcurvesforOPI-PINNPCandACQLundervaryingpayload
| conditions | (25%-100% |     | water filling). |     | Notably, | OPI-PINNPC |     |     |     |     |     |     |     |
| ---------- | --------- | --- | --------------- | --- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
maintainsstableperformanceregardlessofpayloadvariations,
| whereas  | the tracking | error       | of ACQL    | increases |               | proportionally |           |     |     |     |     |     |     |
| -------- | ------------ | ----------- | ---------- | --------- | ------------- | -------------- | --------- | --- | --- | --- | --- | --- | --- |
| with the | augmentation |             | of payload | mass.     | Additionally, |                | ACQL      |     |     |     |     |     |     |
| exhibits | pronounced   | oscillatory | behavior   |           | compared      |                | with OPI- |     |     |     |     |     |     |
PINNPC.
| To further | validate |         | the robustness | of  | OPI-PINNPC |     | under   |     |     |     |     |     |     |
| ---------- | -------- | ------- | -------------- | --- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- |
| payload    | dynamic  | change, | an robustness  |     | experiment |     | that an |     |     |     |     |     |     |
externalforceasdisturbanceisintentionallyappliedtothe50%
|     |     |     |     |     |     |     |     | Fig.6. RMSEofpositionandorientationwithOPI-PINNPCandACQLacross |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------------------------------- | --- | --- | --- | --- | --- |
filling water bottle at t=1s. As illustrated in Fig. 4(c) and payloadmassvariations(25-100kg).(a)demonstratesthecomparisonRMSE
ofposition.(b)presentsthecomparisonRMSEoforientation.
| 4(d), the | tracking | error     | curves              | reveal | that the  | OPI-PINNPC |          |     |     |     |     |     |     |
| --------- | -------- | --------- | ------------------- | ------ | --------- | ---------- | -------- | --- | --- | --- | --- | --- | --- |
| exhibits  | only     | transient | error amplification |        | following |            | the dis- |     |     |     |     |     |     |
turbanceintroduced,withrapiderrorrecoveryobservedwithin
Fig.5(a)includesthreesubfigurescorrespondingtotheposition
| the subsequent |     | time. In | contrast, | ACQL | method | demonstrates |     |          |                  |             |        |        |              |
| -------------- | --- | -------- | --------- | ---- | ------ | ------------ | --- | -------- | ---------------- | ----------- | ------ | ------ | ------------ |
|                |     |          |           |      |        |              |     | tracking | errors along the | x-, y-, and | z-axes | during | the trotting |
significantlylargerandprolongedtrackingerrorafterencounter-
|     |     |     |     |     |     |     |     | test, while | Fig. 5(b) presents | three | subfigures | depicting | the |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ------------------ | ----- | ---------- | --------- | --- |
ingthesamedisturbance.Thisperformancedifferenceindicates
orientationtrackingerrorsinyaw,pitch,androllanglesrespec-
| that OPI-PINNPC |     | exhibits | superior | adaptability |     | to  | real-time |     |     |     |     |     |     |
| --------------- | --- | -------- | -------- | ------------ | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
tively.Theexperimentalresultsdemonstratethat,comparedwith
dynamicchangesinpayload.
ACQL,theproposedOPI-PINNPCisabletoguaranteehigher
|     |     |     |     |     |     |     |     | accuracy | in each dimension | of position | and | orientation | errors. |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----------------- | ----------- | --- | ----------- | ------- |
E. OPI-PINNPCforQuadrupedLocomotionTrottingTest
Foracleardifferentiationbetweenthetwoalgorithms,Fig.5(c)
Next,tofurtherevaluatetheeffectivenessofOPI-PINNPC,a andFig.5(d)illustratethepositionandorientationtrackingerror
trotting test is performed on the quadruped robot, with ACQL normcurvesduringthetrottingtest,respectively.Thecompar-
proposed in [21] as the baseline. The robot is configured to ative results demonstrate that OPI-PINNPC achieves superior
executeaforwardtrottingtestataconstantspeedwitha50kg performancerelativetoACQL,exhibitinghighertrackingaccu-
payload.TheexperimentscenariosareshowninFig.2(b)with racyandafasterconvergenceratethroughouttheexperiments.
a time interval of 0.25 s. Specifically, the position tracking Meanwhile,asevidencedbytheexperimentalresultsinFig.6,
referencetargetissetto(0.2t,0,0.38)(m),whiletheorientation theproposedOPI-PINNPCdemonstratesadaptivecontrolaccu-
trackingreferenceisdefinedas(−0.05,2.95,0)(rad).
racyacrossthepayloadmassesfrom25to100kg,achievingon
TohighlighttheadvantagesoftheproposedOPI-PINNPCal- averageabout35%higherprecisionthanACQLinpositionand
gorithm,webenchmarktheperformanceofthebaselineACQL. orientationtrackingperformance.
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:55:26 UTC from IEEE Xplore.  Restrictions apply.

11282 IEEEROBOTICSANDAUTOMATIONLETTERS,VOL.10,NO.11,NOVEMBER2025
VI. CONCLUSIONANDFUTUREWORK [14] J.Luoetal.,“Modelingandbalancecontrolofsupernumeraryrobotic
|              |     |            |           |     |             |         | limb | for overhead | tasks,” | IEEE Robot. | Automat. | Lett., | vol. 6, no. 2, |
| ------------ | --- | ---------- | --------- | --- | ----------- | ------- | ---- | ------------ | ------- | ----------- | -------- | ------ | -------------- |
| The proposed |     | OPI-PINNPC | framework |     | establishes | a novel |      |              |         |             |          |        |                |
pp.4125–4132,Apr.2021.
controlparadigmofrobotswithQDDunderunknownpayload [15] J.Luo,Y.Zhao,L.Ruan,S.Mao,andC.Fu,“EstimationofCoMandCoP
conditions by integrating online payload identification with trajectoriesduringhumanwalkingbasedonawearablevisualodometry
|                  |     |           |     |        |           |            | device,”  | IEEE | Trans. | Automat. Sci. | Eng., vol. 19, | no. 1, | pp.396–409, |
| ---------------- | --- | --------- | --- | ------ | --------- | ---------- | --------- | ---- | ------ | ------------- | -------------- | ------ | ----------- |
| physics-informed |     | learning. | Due | to the | embedding | of the OPI | Jan.2022. |      |        |               |                |        |             |
module that formulates the physics-informed loss functions [16] A.Rigo,Y.Chen,S.K.Gupta,andQ.Nguyen,“Contactoptimization
through identified payload parameters in the training process, for non-prehensile loco-manipulation via hierarchical model predictive
control,”inProc.2023IEEEInt.Conf.Robot.Automat.,2023,pp.9945–
| the composite | loss | function | is  | ensured | to rapidly | converge, | 9951. |     |     |     |     |     |     |
| ------------- | ---- | -------- | --- | ------- | ---------- | --------- | ----- | --- | --- | --- | --- | --- | --- |
enabling accurate prediction for QDD-driven robots dynam- [17] B. Liu, F. Meng, S. Gu, X. Chen, Z. Yu, and Q. Huang, “Variational-
|                   |     |          |               |     |             |         | based  | geometric    | nonlinear | model         | predictive control | for        | robust loco- |
| ----------------- | --- | -------- | ------------- | --- | ----------- | ------- | ------ | ------------ | --------- | ------------- | ------------------ | ---------- | ------------ |
| ics. Furthermore, |     | a series | of comparison |     | experiments | between |        |              |           |               |                    |            |              |
|                   |     |          |               |     |             |         | motion | of quadruped |           | robots,” IEEE | Trans. Autom.      | Sci. Eng., | vol. 22,     |
OPI-PINNPC and ACQL reveal a 35% improvement in tra- pp.12975–12985,2025.
jectory tracking precision under payload conditions spanning [18] D.Kim,S.J.Jorgensen,J.Lee,J.Ahn,J.Luo,andL.Sentis,“Dynamic
locomotionforpassive-anklebipedrobotsandhumanoidsusingwhole-
| 25–100 kg. | We note | that | the performance |     | of the | PINN-based |     |     |     |     |     |     |     |
| ---------- | ------- | ---- | --------------- | --- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- |
bodylocomotioncontrol,”Int.J.Robot.Res.,vol.39,no.8,pp.936–956,
| model relies | heavily | on  | the accuracy | of  | the physics-informed |     |     |     |     |     |     |     |     |
| ------------ | ------- | --- | ------------ | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
2020.
loss.Whenthenominalmodelinthephysics-informedlossdevi- [19] H.Zhuetal.,“Terrain-perception-freequadrupedalspinninglocomotion
|     |     |     |     |     |     |     | on versatile | terrains: | Modeling, | analysis, | and experimental |     | validation,” |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --------- | --------- | --------- | ---------------- | --- | ------------ |
atesfromthetruephysicalsystem,thepredictionaccuracyofthe
Front.Robot.AI,vol.8,2021,Art.no.724138.
PINNsmaydegradeduringreal-worlddeployment.Ourfuture
|     |     |     |     |     |     |     | [20] L. Amanzadeh, |     | T. Chunawala, | R. T. | Fawcett, A. | Leonessa, | and K. A. |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | ------------- | ----- | ----------- | --------- | --------- |
workwillincludetheverificationonversatilerobotplatforms, Hamed,“Predictivecontrolwithindirectadaptivelawsforpayloadtrans-
|     |     |     |     |     |     |     | portation | by quadrupedal |     | robots,” IEEE | Robot. | Automat. | Lett., vol. 9, |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------------- | --- | ------------- | ------ | -------- | -------------- |
suchasdexteroushands.
no.11,pp.10359–10366,Nov.2024.
|     |     |     |     |     |     |     | [21] B. Jin, | S. Ye, | J. Su, and | J. Luo, “Unknown | payload | adaptive | control |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ------ | ---------- | ---------------- | ------- | -------- | ------- |
forquadrupedlocomotionwithproprioceptivelinearlegs,”IEEE/ASME
REFERENCES Trans.Mechatron.,vol.27,no.4,pp.1891–1899,Aug.2022.
[22] A.Jordana,A.Meduri,E.Arlaud,J.Carpentier,andL.Righetti,“Risk-
[1] P.M.Wensing,M.Posa,Y.Hu,A.Escande,N.Mansard,andA.D.Prete, sensitiveextendedKalmanfilter,”inProc.2024IEEEInt.Conf.Robot.
“Optimization-based control for dynamic legged robots,” IEEE Trans. Automat.,2024,pp.10450–10456.
Robot.,vol.40,pp.43–63,2024. [23] N. Rotella, A. Herzog, S. Schaal, and L. Righetti, “Humanoid mo-
Proc. IEEE-
[2] C. Khazoom, S. Hong, M. Chignoli, E. Stanger-Jones, and S. Kim, mentum estimation using sensed contact wrenches,” in
RAS15thInt.Conf.HumanoidRobots(Humanoids),2015,pp.556–563,
“Tailoringsolutionaccuracyforfastwhole-bodymodelpredictivecon-
trol of legged robots,” IEEE Robot. Automat. Lett., vol. 9, no. 12, doi:10.1109/HUMANOIDS.
pp.11074–11081,Dec.2024. [24] S.SanyalandK.Roy,“Ramp-Net:ArobustadaptiveMPCforquadrotors
[3] R.Grandia,F.Jenelten,S.Yang,F.Farshidian,andM.Hutter,“Perceptive via physics-informed neural network,” in Proc. 2023 IEEE Int. Conf.
Robot.Automat.,2023,pp.1019–1025.
| locomotion | through | nonlinear | model-predictive |     | control,” | IEEE Trans. |     |     |     |     |     |     |     |
| ---------- | ------- | --------- | ---------------- | --- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
[25] S.Sanyal,R.K.Manna,andK.Roy,“EV-planner:Energy-efficientrobot
Robot.,vol.39,no.5,pp.3402–3421,Oct.2023.
[4] S.Ye,J.Luo,C.Sun,B.Jin,J.Su,andA.Zhang,“Designofalarge- navigationviaevent-basedphysics-guidedneuromorphicplanner,”IEEE
scaleelectrically-actuatedquadrupedrobotandlocomotioncontrolforthe Robot.Automat.Lett.,vol.9,no.3,pp.2080–2087,Mar.2024.
narrowpassage,”inProc.2021IEEE/RSJInt.Conf.Intell.RobotsSyst., [26] X.Yang,Y.Du,L.Li,Z.Zhou,andX.Zhang,“Physics-informedneural
networkformodelpredictionanddynamicsparameteridentificationof
2021,pp.7424–7431.
[5] G.Garcıá,R.Griffin,andJ.Pratt,“Time-varyingmodelpredictivecontrol collaborative robot joints,” IEEE Robot. Automat. Lett., vol. 8, no. 12,
forhighlydynamicmotionsofquadrupedalrobots,”inProc.2021IEEE pp.8462–8469,Dec.023.
Int.Conf.Robot.Automat.,2021,pp.7344–7349. [27] M.Raissi,P.Perdikaris,andG.E.Karniadakis,“Physics-informedneural
[6] Y. Ding, A. Pandala, C. Li, Y.-H. Shin, and H.-W. Park, networks: A deep learning framework for solving forward and inverse
problemsinvolvingnonlinearpartialdifferentialequations,”J.Comput.
| “Representation-free |     | model | predictive | control | for | dynamic motions |     |     |     |     |     |     |     |
| -------------------- | --- | ----- | ---------- | ------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- |
in quadrupeds,” IEEE Trans. Robot., vol. 37, no. 4, pp.1154–1171, Phys.,vol.378,pp.686–707,2019.
Aug.2021. [28] J.Nicodemus,J.Kneifl,J.Fehr,andB.Unger,“Physics-informedneural
[7] W.Chi,X.Jiang,andY.Zheng,“Alinearizationofcentroidaldynamics networks-based model predictive control for multi-link manipulators,”
forthemodel-predictivecontrolofquadrupedrobots,”inProc.2022Int. IFAC-PapersOnLine,vol.55,no.20,pp.331–336,2022.
[29] M.Bensch,T.-D.Job,T.-L.Habich,T.Seel,andM.Schappler,“Physics-
Conf.Robot.Automat.,2022,pp.4656–4663.
[8] T.Corbèresetal.,“Comparisonofpredictivecontrollersforlocomotion informedneuralnetworksforcontinuumrobots:Towardsfastapproxima-
andbalancerecoveryofquadrupedrobots,”inProc.2021IEEEInt.Conf. tionofstaticCosseratrodtheory,”inProc.2024IEEEInt.Conf.Robot.
Robot.Automat.,2021,pp.5021–5027. Automat.,2024,pp.17293–17299.
[9] K.A.Hamed,J.Kim,andA.Pandala,“Quadrupedallocomotionviaevent- [30] D.Luo,Z.Cai,D.Jiang,andH.Peng,“Researchonparameteridentifica-
tionmethodforroboticmanipulatorsjointfrictionmodelbasedonPINN,”
basedpredictivecontrolandQP-basedvirtualconstraints,”IEEERobot.
Automat.Lett.,vol.5,no.3,pp.4463–4470,Jul.2020. inProc.2024IEEEInt.Conf.Adv.Intell.Mechatron.,2024,pp.948–953.
[10] J.Luoetal.,“Robustbipedallocomotionbasedonahierarchicalcontrol [31] E.A.Antonelo,E.Camponogara,L.O.Seman,J.P.Jordanou,E.R.de
structure,”Robotica,vol.37,no.10,pp.1750–1767,2019. Souza, and J. F. Hübner, “Physics-informed neural nets for control of
dynamicalsystems,”Neurocomputing,vol.579,2024Art.no.127419.
[11] H.Li,R.J.Frei,andP.M.Wensing,“Modelhierarchypredictivecontrolof
|     |     |     |     |     |     |     | [32] T. Liu, | J. Zhao, | J. Huang, | Z. Li, | L. Xu, and B. | Zhao, | “Research on |
| --- | --- | --- | --- | --- | --- | --- | ------------ | -------- | --------- | ------ | ------------- | ----- | ------------ |
roboticsystems,”IEEERobot.Automat.Lett.,vol.6,no.2,pp.3373–3380,
Apr.2021. model predictive control of autonomous underwater vehicle based on
[12] A.Meduri,P.Shah,J.Viereck,M.Khadiv,I.Havoutis,andL.Righetti, physicsinformedneuralnetworkmodeling,”OceanEng.,vol.304,2024
| “BiConMP:Anonlinearmodelpredictivecontrolframeworkforwhole |     |     |     |     |     |     | Art.no.117844. |     |     |     |     |     |     |
| ---------------------------------------------------------- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- |
[33] J.Luo,S.Ye,J.Su,andB.Jin,“Prismaticquasi-direct-drivesfordynamic
bodymotionplanning,”IEEETrans.Robot.,vol.39,no.2,pp.905–922,
|     |     |     |     |     |     |     | quadruped | locomotion |     | with high payload | capacity,” | Int. | J. Mech. Sci., |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---------- | --- | ----------------- | ---------- | ---- | -------------- |
Apr.2023.
[13] L. Amatucci, G. Turrisi, A. Bratta, V. Barasuol, and C. Semini, “Ac- vol.235,2022,Art.no.107698.
celeratingmodelpredictivecontrolforleggedrobotsthroughdistributed [34] B.Stellato,G.Banjac,P.Goulart,A.Bemporad,andS.Boyd,“OSQP:An
optimization,”inProc.2024IEEE/RSJInt.Conf.Intell.RobotsSyst.,2024, operatorsplittingsolverforquadraticprograms,”inProc.UKACC12th
Int.Conf.Control,2018,pp.339–339.
pp.12734–12741.
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:55:26 UTC from IEEE Xplore.  Restrictions apply.