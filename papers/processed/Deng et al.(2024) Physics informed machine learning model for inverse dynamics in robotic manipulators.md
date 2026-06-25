Version of Record: https://www.sciencedirect.com/science/article/pii/S1568494624006513
Manuscript_7ec5e9858c2554104eddcb481503e939
Physics informed machine learning model for inverse
dynamics in robotic manipulators
WeikunDenga,,FabioArdianib,KhanhT.P.Nguyena,MouradBenoussaada,
KamalMedjahera
aLaboratoireGéniedeProduction,LGP,UniversitédeToulouse,INP-ENIT,47Av.d’Azereix,65016,
Tarbes,France.
bNimbleOne,8rueduCanard,31000,Toulouse,France.
Abstract
In the field of robotic modelling, the challenge of parameter estimation using
limited joint monitoring data presents a substantial hurdle for both traditional
physics-based methods (PBMs) and machine learning (ML) techniques. PBMs
grapplewithmodellinguncertainties,variableworkingconditions,diverserobotic
configurations,andincompleteparameterinformation.MLmethodsfacehurdles
inmaintainingphysicalconsistency,interpretability,andtheneedforextensive
training data. In response to these challenges, this paper proposes a novel ap-
proach, the Equation Embedded Neural Network (E2NN), enhanced by an in-
novativeLiquidmechanism,whicheffectivelyblendsthestrengthsofPBMsand
MLtosurmounttheirinherentlimitations.Itsprimarycontributionsencompass:
1) a pioneering review and synthesis of hybrid frameworks integrating physi-
calprincipleswithML,2)thedevelopmentandrigorousvalidationoftheE2NN
framework, and 3) the introduction of a novel physics regulator and dynamic
Liquid mechanism. Particularly, the proposed E2NN leverages inverse dynam-
ics equations to construct specialized neural network layers, featuring activa-
tion functions and interconnections expressed as composition operators, thus
explicitly encoding physical knowledge. This architectural choice proves espe-
ciallywell-suitedfortasksinvolvinginversedynamicsanddynamicplanningof
roboticmanipulators.TheaccompanyingLiquidmechanismallowsfordynamic
adaptationofinterlayerconnectionsinresponsetoinputdata,enablingreal-time
Emailaddress:weikun.deng@enit.fr(WeikunDeng)
PreprintsubmittedtoAppliedSoftComputing May22,2024
© 2024 published by Elsevier. This manuscript is made available under the Elsevier user license
https://www.elsevier.com/open-access/userlicense/1.0/

adjustmentstochanginginputsandequationsofmotion,ultimatelyenhancing
flexibility and performance. Quantitative assessments of E2NN reveal its com-
pellingperformance, yieldingaMeanAbsoluteError(MAE)of0.10716, closely
alignedwiththeBenchmarkDeepResidualShrinkageNetwork’s(DRSN)MAE
of 0.10415, showcasing its competitive efficacy while achieving higher compu-
tationalefficiencyandamorecompactmodelsize. Robustnessevaluationsfur-
ther confirm E2NN’s adaptability, as it attains a Mean Squared Error (MSE) of
0.3,outperformingDRSN’s1.1undervaryingworkingconditions. E2NNexcels
intorquetrajectoryfitting,achievinganimpressiveaccuracyrateof97.1%,un-
derscoring its practical effectiveness. Furthermore, E2NN excels in torque pre-
diction and parameter identification for inverse dynamics models, particularly
whenconfrontedwithlimitedjointdataandvariablefrictionconditions. Itsub-
stantiallyimprovingthediscernmentofrobotdynamicsandenhancingitsappli-
cabilityinreal-worldtrajectoryfitting.
Keywords: Physics-informedmachinelearning,Roboticmanipulators,
Parameteridentification,Equationembeddedneuralnetwork,Liquid
mechanism.
1. Introduction
In the field of robotics, the best approach for control is the use of model-based
techniques[1]. Themoreprecisethemodelis, thebetterandfastertheperfor-
manceofthecontrollerwillbe. Thefoundationofthesemodelsliesintheintri-
cate mathematical interplay of physical quantities governed by Newton’s laws
whichconsidertherelatestates,asposition,velocity,accelerationandforcesto
abignumberofparametersincludingmasses,inertiatensors,distancesbetween
bodies,andmore[2].
Unluckily, obtaining precise real numerical values for the aforementioned pa-
rameters is not a straightforward task, and numerous robot manufacturers opt
toconcealthisinformationforlogicalsafetyandcopyrightreasons. Analterna-
tiveformeasuringthesevaluesinvolvesanalyzingandconductingexperiments
onindividualcomponentsoftherobotseparately[3].However,thisrequiresthe
risky and time-consuming disassembly of the robot, with the added complica-
tionthattheassemblyprocessitselfmayintroducesignificantchanges.Another
viable approach is to use a Computer-Aided Design (CAD) model of the robot.
Nevertheless, suchmodelsmaybeincompleteandmaynotaccountforcertain
factors,suchasfriction,flexibilityandparametervariationsduetoexternalfac-
2

torsastemperatureandforces.
Thethirdapproach,andmostlyusedinrobotics,istocarryoutaparameteriden-
tificationprocess(alsocalledgray-boxmodeling).Itobviatesthenecessitytodis-
assembletherobotandhasproventobemoreaccuratethantheothermethods.
Itreliesonthestatisticalmatchingbetweenrealsampleddatafromtherobotand
themathematicalformulationofthemodel[4].Itconsistsofaniterativeprocess,
involving multiple stages, each with its distinct challenges and design options,
aswhichphysicalphenomenashouldbeincludedonthemodelandhow,which
trajectoryshouldbechosen,andwhichmathematicaltechniqueshouldbeused
toobtaintheresult,manyofwhichwereaddressedin[5]. Somecomprehensive
surveysofparameteridentificationinroboticscanbefoundin[5,6].
Severalstatisticalmethodshavebeenproposedandtestedinliteraturebasedon
theclassicaldynamicequationoftherobots[7].Someofthesolutionsarebased
onthewell-knownLeast-Squarestechnique[8,9],whichhasbeenproventobe
thebestlinearunbiasedestimatoriftheerrortermshavezeromean.Theyareho-
moscedastic(constantfinitevariance),donotpresentmulti-collinearityandare
not autocorrelated between them. As these assumptions are most of the times
difficulttoensure,othertechniqueshavebeenused,suchasthosebasedonthe
InstrumentalVariable[10,11], theso-calledOutputErrormethods[12,13]and
the Input Error methods [14]. Furthermore, for control techniques as adaptive
control [2], the tracking of the parameters on real-time is important. For this
reason,therecursivevariantsofthesemethodshavebeenproposed[15,5]. Ad-
ditionally, the mathematical approach may produce physically implausible re-
sults, such as negative mass values, because of noise and certain assumptions.
Therefore, alternative methods have been suggested to ensure physical valid-
ity[16,17],includingtheutilizationofthewidelyrecognizedExtendedKalman
Filter algorithm [18]. These mathematical methods mentioned possess various
meritsanddrawbacksconcerningcomputationalcost, speed, complexity, noise
robustness,sensitivitytoinitialconditions,resistancetoperturbationsandmod-
ellinginaccuracies,real-timesuitability,physicalcoherence,aswellasaccuracy
andprecision.Nonetheless,theyshareacommonrelianceontherepresentation
oftherobot’sdynamicmodel.Mostofthemexploitthefactthatthemodel(espe-
ciallytheinversedynamicmodel)canbewritteninthelinearformofy =Ax+ρ,
where y are the torques needed to generate a specific movement, x are the set
ofparameterstobeidentified,ρisthenoise,perturbationsandnotmodeledef-
fects,andAiscalledtheobservationmatrix,whichincludesthemeasurements
ofposition,velocityandaccelerationofthedifferentparts.
Thisraisesseveralchallenges.First,theincreasingcomplexityofrobotsmakesit
3

hardertosymbolicallyderiveobservationmatrices. Second,incorporatingnon-
linear effects such as flexibility [19], friction [20], and environmental factors
liketemperatureandload[21]limitstheapplicabilityofmanyexistingmethods.
Third,thetemporaryinsignificanceofcertainparametersduetosub-excitation
[22],andtheinfluenceofdisturbancesandunaccountedfactorsrequireadaptive
methods.Specifically,inroboticarmjoints,constructingafrictionmodellikeLu-
Gre [23, 24] with dynamic parameters is often essential to accurately estimate
frictionundervaryingworkingconditions,inconjunctionwiththestandarddy-
namicsmodel.
Inthiscontext,MachineLearning(ML)-baseddata-drivenmethods,suchasneu-
ral networks (NNs), offer alternative approaches from a physics-agnostic per-
spective(alsoincludedinthesocalledblack-boxmodelingmethods). Themain
advantages lie in the adaptability to cope with the robotic model variations in
real-time[25]. MLmethodsfocusonfittingtherelationsandtimedependencies
between system parameters and motion data by stacking multiple ML models
[26],allowingforthecaptureofcomplexrelationsandaccuratepredictionswith-
out the need for detailed mechanism analysis or physics-based induction [27].
Although these methods seem attractive, it is crucial to acknowledge their in-
herentlimitations. First,thetrainingprocessnecessitatesasubstantialquantity
oflabeleddataandcomputationalresources.Second,over-fittingthenetworkin
thetrainingdatawillmakeitfailtogeneralizeeffectivelytounseendata.Thirdly
and most importantly, the absence of physics consistency and interpretability
within the generated models, make it complicated to use the results for other
purposes(i.e. controlandidentification)thansimulation.
Recognizingtheinherentlimitationsinbothtraditionalstatisticalmethodsand
ML-basedapproaches,thefocushasshiftedtowardsdevelopinghybridmethods
that combine the strengths of both, aligned with the concept of dark-grey box
modellingintroducedbyLjungin[28].Therefore,ourpapercommencesbythor-
oughlyreviewingadvancedhybridmethodsinSection2,pinpointingtheirshort-
comings. Thiscomprehensiveanalysisconstitutesourfirstsignificantcontri-
bution. Building upon the principles of Physical informed Machine Learning
(PIML) as delineated in [29], we then develop the Equation Embedded Neural
Network(E2NN).Thisnovelparadigm,detailedinSection3,isoursecondand
majorcontribution.Theframeworkcapturestheunderstandingofroboticarm
dynamicswithinaphysicsoperatorembeddednetworkstructure. Thisnetwork
featuresinter-layerconnectionsthatadapttoinputdata,allowingittoaccount
forchangesdynamicallyandautonomouslyinknowledgeacrossvariousrobotic
armstates. OurthirdcontributionistheempiricalvalidationofE2NN’seffi-
4

cacy.DetailedinSection4,thisvalidationprocessemploysbothsimulationdata
and real-world scenarios across varying conditions, utilizing a novel metric to
measuretheperformance. Thisstepunderscoresthepracticalapplicabilityand
effectiveness of the E2NN framework in real-world settings. Finally, in Section
5,weconcludewithasummaryandoutlineperspectivesforfutureresearch.
2. Relatedworks
Ahybridframeworkinthecontextofroboticdynamicsiscommonlyunderstood
as the development of a semi-parametric model, representing a confluence of
gray-box (partially physics-based) and black-box (data-driven) methodologies.
This study delineates a novel threefold classification of state-of-the-art (SOTA)
hybrid frameworks, categorizing them based on the specific functions of ML
| withinthesesystems. |     | Theclassificationencompassesthreedistinctroles: |     |     |     |     |
| ------------------- | --- | ----------------------------------------------- | --- | --- | --- | --- |
1. Physicsassistedsystemsurrogate(PAS):MLsignifiesanunknowntermin
| a physical | equation, | thereby contributing |     | to the final | system | model in a |
| ---------- | --------- | -------------------- | --- | ------------ | ------ | ---------- |
hybridML-equationform.
2. Physicsaugmentedestimation(PAE):MLestimatessystemparametersthat
facilitatetheresolutionofkineticequationsandvalidatetheadherenceto
analyticallaws.
3. Physicsassistedmatching(PAM):MLidentifiessuitabledynamicsolutions
| bymatchingsystemmodelsand |     |     | parametersacrosstheentireworkspace, |     |     |     |
| ------------------------- | --- | --- | ----------------------------------- | --- | --- | --- |
withinaknownselectionscope.
| Withinthatperspective,Table. |     | 1summarizestherelatedresearches. |     |     |     |     |
| ---------------------------- | --- | -------------------------------- | --- | --- | --- | --- |
Table1:Summaryofhybridmethodsforroboticmanipulatoridentification.(Ta-Taxonomy)
| Application | Hybridmethod |     | Advantages |     | Futurework | Ta. |
| ----------- | ------------ | --- | ---------- | --- | ---------- | --- |
UR5manip- Combines imitation learn- Without re- Learn a gen- PAS
| ulators. | ing and                 | reinforcement      | quiring          | demon-   | eralized   | con- |
| -------- | ----------------------- | ------------------ | ---------------- | -------- | ---------- | ---- |
|          | learning                | (RL). ML           | is strator       | action   | troller    | from |
|          | initialized             | by solving a su-   | information,     |          | numerous   |      |
|          | pervised                | learning problem   | learningdirectly |          | demonstra- |      |
|          | that uses               | the expert’s state | from             | a single | tions.     |      |
|          | and action              | pairs to learn     | demonstration    |          |            |      |
|          | theinversedynamics[30]. |                    | trajectory.      |          |            |      |
5

Barrett Lagrangian induction Guaranteephys- Only simulate PAS
| WAM,     | semi-parametric          | for         | esti- ically | plausible | articulatedrigid |         |     |
| -------- | ------------------------ | ----------- | ------------ | --------- | ---------------- | ------- | --- |
| Kuka-LWR | matingroboticparameters, |             | dynamics.    |           | bodies           | without |     |
| robot.   | and equation             | consistency |              |           | contact          | and re- |     |
|          | [31,32].                 |             |              |           | liesonknowing    |         |     |
and observing
the generalized
coordinates.
| A bench-    | Physics-based | side            | infor- Improves      | data | Use      | the    | PAS |
| ----------- | ------------- | --------------- | -------------------- | ---- | -------- | ------ | --- |
| mark suite  | mation        | shapes network  | efficiency           | and  | physics- |        |     |
| of robotics | structure     | and constraints | generalization       |      | informed |        |     |
| environ-    | output values | and             | internal ofthemodel. |      | dynamics | mod-   |     |
| ments.      | states[33].   |                 |                      |      | els to   | design |     |
controllaws.
Soft pneu- Embedding physical mod- Enhanced pre- Apply PIRNN PAS
| matic      | els into          | RNN recursive | dictionaccuracy |            | to more         | practi- |     |
| ---------- | ----------------- | ------------- | --------------- | ---------- | --------------- | ------- | --- |
| actuators. | computations[34]. |               | and             | effective- | cal engineering |         |     |
|            |                   |               | ness            | across     | problems        |         | in  |
|            |                   |               | diverse         | types      | softrobotics.   |         |     |
|            |                   |               | of              | RNNs and   |                 |         |     |
|            |                   |               | soft            | robotics   |                 |         |     |
platforms.
MICO Using Generative Adver- More data ef- Reduce the re- PAS
| and Fetch   | sarialNetworkstocompen- |         | ficiency,        | better | dundancy      | and |     |
| ----------- | ----------------------- | ------- | ---------------- | ------ | ------------- | --- | --- |
| robotic ma- | sate analytical         | models’ | ap- performance, |        | computational |     |     |
| nipulator.  | proximationerrors[35].  |         | andaccuracy.     |        | cost.         | Try | to  |
adapt to sparse
data.
Da Vinci Design each joint’s NN The identifi- The necessary PAE
| surgical | that receives | input          | mea- cation         | method   | force            | infor- |     |
| -------- | ------------- | -------------- | ------------------- | -------- | ---------------- | ------ | --- |
| robot.   | surements     | from           | every canbeimproved |          | mation           | may    |     |
|          | robot joint   | and            | outputs with        | more     | not always       |        | be  |
|          | torque/force  | estimation,    | data                | sets and | available        | in     | a   |
|          | using the     | identification | er- training.       |          | surgicalsetting. |        |     |
rorfortrainingsupervision
[36].
6

Dielectric Differentiable model com- 5% simulation Improvecontrol PAE
≤
| elastomer | biningamaterialproperties |                   | error compared  | and         | inference |
| --------- | ------------------------- | ----------------- | --------------- | ----------- | --------- |
| actuators | neural                    | network for PBM   | tofiniteelement | algorithms  |           |
| control.  | parameter                 | estimations       | models          | and low for | real and  |
|           | and an                    | analytical dynam- | timecost.       | multi-DOF   | soft      |
|           | ics model                 | for responses     |                 | robot.      |           |
calculation[37].
Multi-link Thederivativesoftheresid- Efficient Enhance PINNs PAE
| robotic ma- | uals at                 | a finite number  | gradient-based | to handle              | more        |
| ----------- | ----------------------- | ---------------- | -------------- | ---------------------- | ----------- |
| nipulators. | of matched              | points were      | algorithms     | for complex            | con-        |
|             | designed                | as physical loss | the underlying | trol                   | actions and |
|             | functionstoguidethePINN |                  | optimal        | control initialvalues. |             |
|             | toapproximatethetruere- |                  | problem.       |                        |             |
sponses[38].
KUKA ma- Use meta-learning to learn Quick adapta- Investigate PAE
| nipulators. | structured,state-dependent |              | tion to     | changes the | state-  |
| ----------- | -------------------------- | ------------ | ----------- | ----------- | ------- |
|             | loss functions             | for updating | indynamics. | dependent   |         |
|             | themodelparameters[39].    |              |             | loss.       | Explore |
|             |                            |              |             | its         | perfor- |
|             |                            |              |             | mance       | in more |
parameters’
estimation.
Simulated Two novel physics- Superior perfor- Extending to PAE
| 7-dof ma-  | informed             | loss functions | mance         | to using multi-body  |           |
| ---------- | -------------------- | -------------- | ------------- | -------------------- | --------- |
| nipulator. | about the            | space velocity | normal        | deep contact,explore |           |
|            | controlerror[40,41]. |                | modelsandeasy | the                  | effect of |
|            |                      |                | todesign.     | adaptively           |           |
|            |                      |                |               | tuning               | the       |
|            |                      |                |               | trade-off            | loss      |
weight.
Simulated Optimizing end-effector Low computa- Testing on PAM
| multi-DOF | position                 | with wave func- | tion cost       | and various        | robotic   |
| --------- | ------------------------ | --------------- | --------------- | ------------------ | --------- |
| manipula- | tion and                 | Monte Carlo     | acceptable      | per- manipulators, |           |
| tors.     | method                   | to satisfy the  | formanceonthe   | exploring          | dif-      |
|           | Euclid fitness           | through the     | simulationdata. | ferent             | fitness   |
|           | particle                 | swmanipulators  |                 | functions,         | and       |
|           | optimization             | [42, 43]        | or              | evaluating         |           |
|           | artificialbeecolony[44]. |                 |                 | its                | practical |
performance.
7

Different Artificial Neural Networks Easy to design, Explore the PAM
| multi-joint | [45], Multi-layer       | percep-        | high              | precision | model’s          | flexi-    |
| ----------- | ----------------------- | -------------- | ----------------- | --------- | ---------------- | --------- |
| robotic     | tron, Long              | Short-Term     | and               | model     | bility           | and the   |
| manipula-   | Memory,                 | Gated          | Recur- the        | uncertain | identificationof |           |
| tors, such  | rent Unit               | [46], Fuzzy    | NN factors.       |           | key influencing  |           |
| as ABB      | [47] nonlinearly        | fits           | and               |           | parameters       |           |
| Industrial  | matches end-effector    |                | pose              |           | in the           | model,    |
| Robot.      | to joint configurations |                | in                |           | and expand       | its       |
|             | theentireworkingspace.  |                |                   |           | application.     |           |
| ICub hu-    | Semiparametric          | models         | Better            | gen-      | Compare          | with PAM  |
| manoid      | that combine            | rigid          | body eralization, |           | parametric       |           |
| robot       | dynamics                | (parametric    | derivative-free   |           | method,          | en-       |
| inverse     | model) with             | Gaussian       |                   |           | hance            | physical, |
| dynamics    | processes               | (nonparametric |                   |           | design           | for       |
| model-      | model).                 | Two versions   |                   |           | predictive       |           |
| ing [48]    | proposed:               | withRBDinthe   |                   |           | Control          |           |
meanfunctionorwithRBD
inthekernel.
Theseinvestigationsconsistentlyhighlightamyriadofadvantages,encompassingim-
provedperformance,augmenteddataefficiency,andincreasedphysicalconsistency.No-
tably,emphasishasbeenplacedontheintegrationofdynamicalequationsintoNNstruc-
tures[31],andtheconstructionofNNssubjecttophysicalconstraints[32].Particularly,
inthefieldofsoft-bodiedrobots[34],theamalgamationoftraditionalincompleteana-
lyticalmodelswithmachinelearning(ML)hasshowcasedpositiveeffects.Nonetheless,
theenvisionedfuturetrajectoryoftheseworksnecessitatesamorein-depthexploration
ofmodelflexibility,acomprehensiveexaminationofthemethodologiesemployedtoem-
bedphysicsknowledgeintodiverseMLstructures,andpracticalvalidation.
The Physics assisted systemsurrogate (PAS) methodology has found successful appli-
cationsinvariousfields,includingtheUniversalRobotsfor5kgweights(UR5)manip-
ulator [30] and soft pneumatic actuators [34]. These models offer advantages such as
enhanceddataefficiencyandadaptability.However,theyencounterchallengeswhenit
comestogeneralizationfromlimiteddemonstrationsandcomputationalefficiency.One
significantlimitationistheirinabilitytoadapttodiversescenariosanddifferentoper-
atingconditions.Thislimitationarisesbecause,whenmachinelearningisemployedto
approximateunknowntermswithinphysicalequations,allconnectionsoftheapproxi-
mationoperatorsanddataflowbecomefixed,hardtolearnandmodify.
Ontheotherhand, PAEmethodshavebeenimplementedinsystemsliketheDaVinci
surgical robot [36] and multi-link robotic manipulators [45]. These methods excel in
8

estimatingsystemparameters,boastinghighsimulationaccuracyandefficientcontrol
algorithms.However,theyoftenstruggletomaintainphysicalconsistency,particularly
inthepresenceofnon-modeleffectslikefrictionandtemperaturevariations. Ensuring
therealismandphysicalaccuracyofthesemodelsacrossvariousconditionsremainsa
significantchallenge.
PAM strategies, which involve machine learning to match dynamic solutions across a
widerangeofworkspaces,canbeobservedinapplicationssuchastheICubhumanoid
robot [48]. Whileproficientatmatchingdynamicsolutionsindiversesituations,they
grapplewiththecomplexityandcomputationaldemandsassociatedwithhandlingin-
tricateroboticsystems.Thesechallengesencompassprocessingandmanagingthecom-
putationalloadofadvancedroboticsystemsinreal-time,whilealsorequiringimproved
physicalconsistencyandcomparativeanalyseswithparametricapproaches.
Furthermore,thesestudiesprimarilyfocusonimprovingcontrolperformancesthrough
ML-basednonlineardatafitting, ratherthanfindingfixedpatternsandestimatingthe
systemparameters.WhilehybridPBM-MLmethodsareadvancing,thereisasig-
nificantgapinachievinganoptimalbalancebetweenphysicalconsistencyand
real-timeadaptabilityundertheMLframeworkwherephysicalmodelscanbe
expressed. Thisgaphighlightstheneedformoresensitiveinputsandknowl-
edgeflexiblearchitecturalapproachesinhybridmodelling. Consequently,the
primaryobjectiveofthispaperistointroduceaversatileandinterpretablePIML
frameworktailoredforroboticmanipulatormodellingandparameteridentifi-
cation. Thisframeworkconsistsofaphysics-informedstructuremethodwith
theabilitytogeneralizeonnewdatafromunknownworkingconditions.Hereby,
in the validation process, this study will demonstrate the effectiveness of the
proposeddesignbycomparingtheperformancebeforeandafterusingthepro-
posedframeworktomodifyanexistingalgorithm.
3. Proposedframework
Motivatedbytheresearchpublishedin[49]whichproposesimplementingtheflux–tendency
relationsdirectlyintoestablishingNNstructuretoinherentlyrespecttheconservation
laws, this research develops the penultimate hidden layer and interlayer connections
enforcingrobotdynamicsintheproposedE2NN.Inaddition,foradaptingtothediffer-
entworkingmodes,aliquidinter-layerconnectionparadigmisexplored.Theproposed
frameworkisshowninFig.1.
The implementation process involves building an inverse dynamics model using ana-
lyticderivationfirst,tostudytheindividualtermsofposition,velocityandacceleration
that are repeated over and over. Next, the NN’s neurons are designed based on basic
computationalfunctionsintheanalyticalrelationsincompletemodel,suchassineand
cosine. These neurons form layers that express sub-term transformation relations for
9

Figure1:ImplementationframeworkforE2NN
the inverse dynamics model. Then inter-layer connections are designed based on the
relationsbetweensub-terms. Finally,afullyconnectedlayerrepresentsthesummation
operationrelations. Eachstepofthecomputationisimplementedthroughsubstitution
usingtheNN.Adetaileddescriptionoftheproposedframeworkisshowninthefollow-
ingsections,especiallytheinnovativepartsaregiveninthesubsection3.2.
3.1. Robotinversedynamicmodel
Theinversedynamicsmodelofamdegreesoffreedomroboticmanipulatorcanbewrit-
ten,asexplainedinSection1,inalinearwaywithrespecttoitsparameteras:
τ =W(q,q˙,q¨)β+ρ (1)
whereW(q,q˙,q¨) R r × nbistheobservationmatrixinEq.(2)obtainedfromevaluating
∈
f i (q,q˙,q¨)mtimes,withr = n m,andntheamountofmeasurements;ρ R r are
× ∈
the unmodelled effects; τ R r is the torque vector of the robotic manipulator; q, q˙,
∈
andq¨ arejointpositions,velocities,andaccelerationsmeasurements,respectively;and
β R nb isthevectorofthen b baseparametersdescribingthemanipulator.
∈
f (q ,q˙ ,q¨)
1 1 1 1
f (q ,q˙ ,q¨)
2 2 2 2
W(q,q˙,q¨)= .  (2)
.
.
 
  f m (q m ,q˙ m ),q¨ m ) 
 
Theparametersetβisselectedtominimizemodelcomplexitywhileensuringthatthere
isnomulticollinearitywithintherowsoftheobservationmatrix.Thisparticularparam-
etersetisreferredtoasthebaseparameterusedinthefieldofrobotics.Itconstitutesa
lineartransformationoftheconventionaldynamicparameters,whichincludethecen-
10

tresofmass,inertialproperties,andmassesoftheroboticlinks,giventhatthekinematic
parameters(therelativedistancesandanglesbetweenjoints)arepresumedtobeknown
[50,51].Thederivationofthisbaseparametersetcanbeapproachedthroughanalytical
methods[50],aswellasthroughnumericalstrategies[52,53]. Thepremiseoftreating
thekinematicparametersasknownisaprevalentassumptioninrobotics. Thisisdue
totheeaseofaccuratelymeasuringlinkdimensionswithcontemporarymeasurement
technologies. Ininstanceswherethesekinematicparametersareunavailableorwhere
increasedprecisionisrequired,kinematiccalibrationtechniquescanbeemployedtore-
finethesevalues[54].
AsalsosaidinSection1,thetrajectoryselectionisanimportanttaskonparameteriden-
tification. Itwilldetermineifparametersarewell-excitedornot,thusitwilldetermine
theconfidenceontheestimationofthem[55,56].Formanipulatorsthatarecommanded
through position, velocity and/or acceleration, the well-known finite Fourier series is
themostpopularwaytodesignthereferencetrajectorytoexciteasmanyparametersas
possible[57,58]:
Ni
|     |       |             | a l,i |     | b l,i      |     |     |
| --- | ----- | ----------- | ----- | --- | ---------- | --- | --- |
|     | q(t)= |             | sin(ω | lt) | cos(ω lt)  | +q  |     |
|     | i     |             | ω l   | f − | ω l f      | i0  |     |
|     |       | l=1(cid:18) | f     |     | f (cid:19) |     |     |
X
Ni
|     | q˙(t)= i |     | (a l cos(ω | f lt)+b l | sin(ω f lt)) |     | (3) |
| --- | -------- | --- | ---------- | --------- | ------------ | --- | --- |
l=1
X
Ni
|     | q¨(t)= i |     | ( aω l f lsin(ω | f lt)+bω | l f lcos(ω f | lt)) |     |
| --- | -------- | --- | --------------- | -------- | ------------ | ---- | --- |
−
l=1
X
whereω representsthefundamentalpulsationoftheFourierseries,andN
| f   |     |     |     |     |     | i   | indicates |
| --- | --- | --- | --- | --- | --- | --- | --------- |
theorderoftheharmonic.Theparametersa andb correspondtotheamplitudesofthe
|     |     |     |     | l   | l   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
sineandcosinefunctions,whileq denotestheinitialpositionaroundwhichthejoint
0
oscillates.
Moreover,frictionneedstobeaddedtothebasicdynamicmodel.Manymodelsexistin
literature[20,59,60].Oneofthemostusedinroboticsis:
|     |     | τ fj | =f vj q˙ j | +f cj sign(q˙ | j )+τ offj |     | (4) |
| --- | --- | ---- | ---------- | ------------- | ---------- | --- | --- |
whereτ representsthejointfrictiontorque;f istheviscousfrictioncoefficient;f is
| fj  |     |     |     |     | vj  |     | cj  |
| --- | --- | --- | --- | --- | --- | --- | --- |
theCoulombfrictioncoefficient;andτ isusedtocombinetheasymmetricalCoulomb
offj
frictioncoefficientandotheroffsetscausedbysensorsandamplifiers[61].
Bycarefulstudyofthedynamicequation,foreachjoint,wecanrewriteEq.(1)inorder
tobuildinformed-NNas:
11

P
τ = β f w cos(q),w sin(q),w sign(q),w q,w q˙,w q¨...
i p ip 1pi 2pi 3pi 4pi 5pi 6pi
(5)
p=1
P (cid:0) +β q˙ +β sign(q˙)+β (cid:1)
P+1 i P+2 i P+3
whereP aretheamountofparametersrelatedtoτ.Thedetailedmathematicalexpres-
i
sions for the overall nonlinear mapping function f and the coefficients β and w are
ip
tobelearnedfrommonitoringdata. Thismodelis,ofcourse,asimplificationofreality,
andthatiswhywesayinthispaperthatitisincomplete. Severalphenomenamaybe
missingand/ormodeleddifferently.
3.2. Proposedmethodology
TheprocessofMLmodelingistolearnparametersβ .Theseparametersarecombined
p
withdifferenttransformations.Additionally,thelearnedrelationsneedtobeflexibleto
accommodatevariationsinworkingconditionsandadapttodifferentinputdata.Tosat-
isfytheserequirements,aspecificNNstructureisdesignedaccordingtoEq.(5).Thede-
tailsareshowninFig.2andsubsection.3.2.1.Thearchitecture’scoreisunderpinnedby
Figure2:ArchitectureoftheEquation-EmbeddedNeuralNetwork(E2NN)foroneroboticjoint.
(Thebluecomponentsrepresentthephysics-informedpartsofthetraditionalneuralnetwork.
The circular nodes represent individual neurons, while the rectangular nodes denote custom
layers.Theinterconnectedcirculargroupwithintheliquidlayersignifiestheirdynamicconnec-
tions. IntheLiquidlayers,theconnectionisindeterminateandisthereforerepresentedbythe
stackingpatternoftheneuronpool.TherelationshipbetweenthephysicalequationandtheNN
structureisgivenbythedarkbluearrow.)
theimplementationofcustomdesign.Withinthe“MimeticNonlinearTransformsLay-
ers”,thefoundationalphysicalrelationsaresimulatedforeachinputtoeffectivelycreate
12

asymbolicrepresentationofthephysicsinvolved. Subsequenttothistransformation,
the“CombinationLayers”amalgamatethissymbolicrelationintoanoutputthataligns
with the prescribed dynamic formulation. In the “Combination Layers”, the weights,
symbolizing the parameters of the robotic manipulators, are subject to automated ad-
justmentthroughaniterativelearningprocess.
3.2.1. NNlayerswithembeddeddomainequations
E2NNusesthecustomerlayerstosimulatethebasicnonlineartransformationterms,as
showninFig.4.
q
1
nb
q 2 CustomLayer h i (ω i q i )+b g 1 n
−
i=1
P
q n
n h ( ωq +b)
u i i
i=1
P
Figure3:Customlayerstorepresentbasicarithmeticunits.
Whereh representsaseriesofpartiallyknownphysicsnonlinearelementsf inEq.(5).
i
n isthetypenumberofthebasicitemsinvolved. h consistsofthebasicsmathemat-
b i
icaltermssuchascos(q),sin(q),sign(q˙),andlineartransformationrelationsofq,q˙,q¨.
FortheunknownelementsinEq. (5),E2NNusesthetraditionalMLlayerh tofitthe
u
potentialtransformation. Thusfar, E2NNhasperformedthepolynomialfittingofthe
independentvariablescontainedinf forEq.(5).Inparticular,thebiastermbofthelast
i
hiddenlayercorrespondstoτ .
offj
Inthedeeperhiddenlayers,E2NNdesignscustomlayerstosimulatethebasicmathe-
maticalcombinationsoftheabovebasicelements,asillustratedinFig.4.
13

g
1
nk
g 2 CustomLayer k i ( ω i q i +b) y 1 n
−
i=1
P
g
n
Figure4:Customlayerstorepresentanalyticcombinationrelationsforpolynomials
Where k represents a series of known mathematical relations consisting of squares,
i
radicals,varioustypesofquadraticoperations,etc. n isthetypenumberofthebasic
k
combinationrelationsinvolvedinEq.(5).
3.2.2. NNinterlayerconnection
Tofitapolynomialfunctionofdegreen toasetofdatapointsinEq.(5),n+1coeffi-
j
cientsareneededtodefinethepolynomial.Thesependingcoefficientsβ,whereiranges
i
from1ton ,canberepresentedbytheweightsandbiasesofasinglehiddenlayerwith
j
n neurons. Theinputofthesehiddenneuronsisresponsibleforprovidingthevalues
j
off inEq.(5),andtheoutputneuronproducesthefinalpredictedtorquevalueτ.
3.2.3. Liquidmechanismtoenhancethemodelgeneralizationperformance
The structure presented in Fig. 5 incorporates the dynamics equation as a hard con-
straint, resulting in a model with strong physical consistency. However, the existing
PIML works have fi‘xed node and connectivity configurations after training. This re-
stricts the model’s potential for adapting to novel working conditions, particularly in
caseswheretheunderlyingequationsdifferacrossdiverseoperatingconditions. When
itcomestoastraightforwardpredictiontask,trainingacomplexneuralnetworkfora
mobilemanipulatorrobotisnotanoptimalchoiceintermsoftimeefficiency[62]sothat
theconnectivitybetweennodesoftheproposedmodelinE2NNmustbeabletochange
dynamically. Therefore, the liquid mechanism is proposed to build custom dynamics
inter-layer connection based on the current input and previous state of the network.
Inspiredbythe“Liquidtime-constantneuralnetwork”researchpublishedin[63],this
paper introduces the “Liquid mechanism” to address the robust performance issue. A
gatingunithasbeenincorporatedbetweenthephysics-informedlayers. Itcomprisesa
gatingcontrollerandanonlineartransformerwhichregulatetheinformationflowand
14

| Mimeticnonlinear | Combinatorics |     |     |     |
| ---------------- | ------------- | --- | --- | --- |
Inputlayer
|     | transforms | bymimesis |     |     |
| --- | ---------- | --------- | --- | --- |
| q¨  | h          | k         |     |     |
|     | 1          | 1         |     |     |
β
1st
| q˙  | h   | k β   | Outputlayer |     |
| --- | --- | ----- | ----------- | --- |
|     | 2   | 2 2st |             |     |
τ
|     |     | β   | i   |     |
| --- | --- | --- | --- | --- |
3st
| q   | h   | k   |     |     |
| --- | --- | --- | --- | --- |
|     | 3   | 3   |     |     |
β nst
|     | h n | k n |     |     |
| --- | --- | --- | --- | --- |
h
u
Figure5:Thestructureofthecustominter-layerconnectionintheE2NNlayers(thedashedline
inthefigureindicatesthatthehiddenlayerinthemiddleisomitted).
Mimeticnonlinear
Liquidlayer
transforms
| h   | l   |     |     |     |
| --- | --- | --- | --- | --- |
| 1   | 1   |     |     |     |
Combinatorics
| h 2 | l 2 | bymimesis |               |     |
| --- | --- | --------- | ------------- | --- |
| h   | l   | Output:   | k(t)=Wouth(t) |     |
| n   | 3   |           | i             | i   |
l 4
l
n
| Updaterule: | Eq. 6 |     |     |     |
| ----------- | ----- | --- | --- | --- |
Figure6:E2NNlayerwithvariantinputdependentconnectionsandhiddenstateupdaterule.
15

transformationbetweenthelayers,asshowninFig.6.Thecolorsrepresentthedifferent
connectivitypatternswhentheE2NNlayerprocessesdifferentinputs.Theseconnectiv-
itypatternsrefertothenumberofconnections,betweeneachneuronandotherneurons,
andtheEq.(6)basedgatingcontrolconnectionweights.
|     | z =σ(W | h+U l) |     |     |     |
| --- | ------ | ------ | --- | --- | --- |
z z
|     | g=tanh(W | g h+U g (α | h)) |     | (6) |
| --- | -------- | ---------- | --- | --- | --- |
⊙
|     | k′ =(1 | z) k+z | g   |     |     |
| --- | ------ | ------ | --- | --- | --- |
|     |        | − ⊙ ⊙  |     |     |     |
In the formula (6), h is the input vector of the current layer, k is the output vector of
thecurrentlayer,z isthegatingunit,g isthenon-lineartransformer,W ,U ,W ,U
|     |     |     |     | z z | g g |
| --- | --- | --- | --- | --- | --- |
aremodelparameters,σ,andtanhareactivationfunctions,and denoteselement-wise
⊙
multiplication.Thethirdequationintheformulaindicatesthatthenewoutputk iscal-
′
culatedbyanon-lineartransformationgcontrolledbythegatingunitz,incombination
withthepreviouslayeroutput.
Itisnotedthattheleakagerateαplaysakeyroleincontrollingthescaleoftheoutput
hoftheupperlevelinthenonlineartransformationg.Typically,αisrelatedtothetime
constant τ, to which is assigned a pre-determined value. However, to achieve input-
related dynamics leakage rate and consider the dynamic physics constraints inside, α
canbecalculatedusingα=sigmoid(h).
3.2.4. Interpretableparameters
The parameter β of Eq. (5) in the E2NN represents the weights of polynomial terms
thatcorrespondtochannelweightsinthehiddenlayerofaneuralnetwork,asshown
in Fig. 5. To enhance the performance of the E2NN, a customized loss function that
takesintoaccountboththelayerparametersandtheunderlyingphysicsequationshas
beendevelopedandincorporatedintothelosscalculation. ThisensuresthattheE2NN
canachieveoptimalvaluesforboththeNNstructuralparametersandthepolynomial
weights during training. In Fig. 7. The loss function is composed of two parts: the
meansquarederror(MSE)betweenthepredicted(τ )andtrue(τ)values,andaphysical
′
formula term that accounts for the dynamics of the robotic manipulators movements.
Thephysicalformulatermisdefinedas:
|       | nk       | nk    | nj         |         |     |
| ----- | -------- | ----- | ---------- | ------- | --- |
| 1     |          | 1     |            |         |     |
| loss= | (τ τ′)2+ | (τ    | β f (q ,q˙ | ,q¨ ))2 | (7) |
| n     | −        | n −   | inn i it   | it it   |     |
| k     |          | k     |            |         |     |
|       | X i=1    | X i=1 | X i=1      |         |     |
16

q w
1,
(
1
1)
. w ( 2 1 , ) 1 l 1
q τ Loss
w (1 3 ) ,2 l n
..
q
Figure7:Dynamicsequationembeddedlossfunction.Thebluedashedlineindicatestheparam-
eterusedtocalculatethefinalloss,andtheblackdashedlinerepresentstheintermediatehidden
layerthatpassesfrominputqtooutputτ.
4. Verificationoftheproposedmethodologyinlimiteddataconditions
TheefficacyoftheE2NNisaffirmedthroughsimulationandexperimentalprocedures
conductedonaroboticmanipulator,aswillbedetailedinSubSection4.1.Thearchitec-
turalchoiceforthispaperistheResidualBlock-E2NN,whichemploysaresidualneural
networkasacriticalcomponentoftheE2NNframeworkthatisintroducedinSubSec-
tion 4.2. The evaluation metrics employed to assess the performance of the proposed
methodsareexplainedinSubSection4.3. Validationresultsareshownandanalyzedin
Subsections4.4and4.4.2.
4.1. Applicationcases
Forourexperimentation,weutilizedthe7-degree-of-freedom(DOF)collaborativema-
nipulatorKUKAiiwa,asdepictedinFig. 8,alongwithitsDenavit-Hartenbergparam-
eters. Thismanipulatorischaracterizedbyabaselineof43baseparameters,whichex-
tends to64 whenincorporating the21 parametersrelated tothe frictionmodel as de-
scribedbyEq. (4)inresearch[15]. Inanefforttostreamlineourstudyandfocusona
subsystem,wenarrowedouranalysistoonlythelastlinkoftherobot.Thedynamicsof
17

Figure8:ParametersandlinkframesoftheKUKALBRiiwa14R820[9].
thislinkaredescribedinEq.(4).
|     |     |     | 0.06cos(q) |     | 0.22sin(q) |     |     |     |
| --- | --- | --- | ---------- | --- | ---------- | --- | --- | --- |
−
|    |     |     | (0.22cos(q)+0.06sin(q)) |     |     |     |     |    |
| --- | --- | --- | ----------------------- | --- | --- | --- | --- | --- |
0.04q¨
−
|                    | ( 0              | . 0 6 c o s (q ) | 0 . 2 2 s i      | n ( q ) ) 2 | ( 0 . 2 2 c o s ( q ) +   | 0 .0 6 s i n ( q ) | ) 2                      |            |
| ------------------- | ---------------- | ---------------- | ---------------- | ----------- | ------------------------- | ------------------ | ------------------------ | ----------- |
|                    |                  |                  | −                | −           |                           |                    |                          |  β 1       |
|  q˙ ( 0 . 22 c o s | ( q )+ 0 . 0 6 s | in ( q ) ) 0     | . 0 06 s i n ( q | ) ( q ˙ +   | 0 . 4 9 ) ( 0 . 2 2 c o s | ( q ) + 0 . 0 6 s  | i n (q ) ) 0 .1 0 98 c o | s ( q )  β |
|                   |                  | −                |                  | −           |                           |                    | −                        |    2    |
τ=  0 . 1 1 si n ( q ) 0. 0 0 6 2 c o s ( q ) ( q ˙ + 0 . 4 9 ) ( 0 . 0 6 c o s( q ) 0 . 2 2 s i n ( q ) ) + q ˙ ( 0 . 0 6 c o s( q ) 0 .2 2 si n ( q ) )  ...
|    | −   | −   | 4 . 9 0 | s i n ( q )   | 0 . 0 2 − 6 c o s ( q ) |     | −   |            |
| --- | --- | --- | ------- | ------------- | ----------------------- | --- | --- | ----------- |
|    |     |     |         | −             |                         |     |     |          |
|    |     |     | 4 . 9 0 | c o s ( q ) + | 0 . 0 2 6 s i n ( q )   |     |     |   β 1 0  |
|   |     |     |         |               |                         |     |     |         |
|    |     |     |         | sign(q˙)      |                         |     |     |          |
|    |     |     |         |               |                         |     |     |            |
|    |     |     |         | q˙            |                         |     |     |            |
|    |     |     |         |               |                         |     |     |            |
|    |     |     |         | 1.0           |                         |     |     |            |
|    |     |     |         |               |                         |     |     |  (8)       |
|    |     |     |         |               |                         |     |     |            |
whereq,q˙,q¨,τ refertovaluesofthe7thjoint,andthenumericalvaluesariseforcom-
binationofthekinematicparameters,whichareconsideredtobeprovidedandknown.
Noticethefundamentalmathematicaloperationsonthemeasurementsignalsmentioned
inSection3.2.1. Inthisstudy,wemadeastrategicdecisiontofocusexclusivelyonthe
lastlinkofthe7-DOFKUKAiiwamanipulator,primarilytosimplifytheinherentcom-
plexityofafullroboticarmsystem. Thistargetedapproachenablesustodelvedeeply
intothedynamicsandcontrolalgorithmsofaspecific,yetrepresentative,segmentofthe
manipulator. However,itinherentlylimitsthebreadthofourfindings. Specifically,the
18

resultsmaynotfullyencapsulatethedynamicinteractionsamongthemultiplelinksof
afullroboticmanipulatorbecausetheembeddedoperatorsinEq.(4)arelimited.There-
fore,whenextrapolatingtomorecomplex,multi-linkmanipulatorsystems,theextend
oftheNNstructureandscalearerequired.
Regarding the kinematic parameters of the robotic system, we operated under the as-
sumptionthattheseparametersareknownandaccuratelyprovided.Thisassumptionis
groundedinthefactthatroboticsystems,liketheKUKAiiwa,usuallyhavewell-defined
kinematicparameters,eitherfromprecisemanufacturingspecificationsorthroughcal-
ibrationprocesses. However,thisassumptionmaynotfullycapturethechallengesen-
counteredinreal-worldscenarios,wheremanufacturingvariancesandoperationalwear-
and-tearcanleadtodeviationsintheseparameters.Consequently,whilethisassumption
facilitatedamorestreamlinedanalysis,itpotentiallyoverlooksthenuancesofparameter
identificationandadjustmentinpracticalsettings.Theperformanceandaccuracyofour
model,therefore,mightneedadjustmentsorrecalibrationswhenappliedinoperational
environments where these parameters could differ from their initially defined values.
Buttheresultingbiascanbeattributedtoarobustnessproblem,whichisexpectedtobe
compensatedbytheMLpartofE2NN.
4.1.1. Simulationtest
Togeneratethesimulationenvironmentofthemanipulator,thefollowingsteps
areconsidered:
1. Definetherobot’sdynamicequations.
2. Specify the robot’s physical parameters, obtained from previous identifi-
cationprocessesastheonein[15].
3. Design the trajectories to be used. In this work several trajectories were
used, some of them that excite predominantly the phenomena of friction
(called "Friction"), others that excite the mainly the inertial parameters
(called "Inertial"), and others that excite both (called "Direct-Servo") with
trajectoriesdesignedasmentionedinEq. (3).
4. Usetheprovidedequationsandinputstoemulatetherobot’smotionover
aspecifieddurationusingnumericalintegrationmethodsliketheEuleror
Runge-Kutta.
Thetrainingdataconsistof26988measurementsmadeonseveraldifferenttra-
jectories, mainly exciting inertia parameters. The testing data include 53976
movement recording points from trajectories mainly exciting friction parame-
19

ters,toanalyzethegeneralizationabilityoftheproposedapproach. Fortesting
robustness, additional data is used as a second training dataset, but the E2NN
avoidsretrainingonit.
4.1.2. Experimentaltest
Intheexperimentalvalidation, theKUKASunriseOSisusedtointerpolatethe
trajectorypointsandcreatethedisplacement,velocity,andaccelerationprofiles
withtheSplineandPTPmotiontypes[15]. TheFastRobotInterface(FRI)[64]
library provided by KUKA is used to continuously exchange data in real time
betweentherobotcontrollerandaC++clientapplicationonanexternalsystem.
The client application recorded data from the robot at its highest possible rate
of 1000 Hz. For the commanded signals, the data are first down-sampled to 50
Hz, and then velocities and accelerations are calculated from the commanded
position.Asecond-orderdigitalButterworthfilterwithacutofffrequencyof3.5
Hz in both directions is applied before the down-sampling process. A total of
42977robotmanipulatorposedatapointsfrom10randomtasktrajectorieswere
collected,ofwhich3taskstotalling11894datapointswererandomlyselectedas
thetrainingset,andtheremaining7taskstotalling31103datapointswereused
asthetestsettosimulaterealsmall-sampleconditions.
4.2. E2NNwithresidualblocks
The E2NN framework enhances a deep residual shrinkage network (DRSN) ar-
chitecture, as illustrated in Fig. 10, forming the E2NN-ResNet model. This is
contrasted with a conventional ResNet model, depicted in Fig. 9. Our compar-
ative analysis centres on the structural differences between standard artificial
neural networks (ANNs) based on residual blocks and an advanced version in-
tegrating a Physics-Informed (PI) module. The conventional ResNet lacks this
PI module, whereas the E2NN-ResNet incorporates it, notably adding links be-
tween the PI module and the corresponding PI layer. This addition in E2NN-
ResNetintroducesauniqueresidualblockemployingtrigonometricoperations
(sine and cosine functions) to compute sums and differences of inputs, a func-
tionalityabsentsinthestandardResNetstructure. Thisstructuralenhancement
inE2NN-ResNetispivotalforunderstandingthedistinctionsandimprovements
brought about by incorporating PI principles in ANN architectures. In this pa-
per,deepresidualshrinkagenetwork(DRSN)hasthreeinputs,allofwhichyield
a(batchsize, 1)inputforthesubsequentlayers. Itconsistsof6residualblocks
withafullyconnectedlayer. Theoutputoftheblockissummedwithashortcut
connectionbyaddingaresidualconnectionwiththeReLUactivationfunction.
20

Figure9:Theframeworkofthedeepresidualshrinkagenetwork(DRSN).
Thismodelusesthemeansquareerroroftorquepredictionasthelossfunction
andistrainedusingtheAdamoptimizer.
The E2NN is innovatively implemented to refine the DRSN model by modify-
ing the activation function and the interconnections within the residual block,
therebyhighlightingthedistinctivenessofE2NNinFig. 10. TheE2NNdemon-
strates considerable prowess in mimicking the inverse dynamics process sub-
jected to physical constraints, thus offering a notable improvement to existing
methods. The structure of the model comprises Residual Shrinkage Blocks and
a Liquid Layer. The first of the Residual Shrinkage Blocks, "RDB1", calculates
thecosineofq (shortcut=tf.cos(q))andmapsittothefiltersviaadenselayer.
The second block "RDB2" processes q˙ and q¨. The "Concat" layer then merges
thethreeoutputsprocessedbytheresidualshrinkageblock. Additionally,their
products (R1 R1,R1 R2) are concatenated. The "Liquid" layer assimilates
× ×
21

Figure10:E2NN:DeepResidualShrinkageNetworkwithanembeddedequationproposal.
22

thesecomponentsandfitsthemtoτ inanapproximatemathematicalform.This
methodicalandsystematicapproachtoequationrepresentationandassimilation
formstheessenceoftheE2NN’ssuperiorfunctionality.
4.3. Evaluationmetrics
To quantify the performance of the proposed method regarding the adaptation
degreeoftherobotmanipulatorstrajectory,meansquareerror(MSE),theFréchet
distance[65],andthePolygonAreadifference[66])areusedasmetric.
4.3.1. PolygonAreaDifference
| PolygonareaiscalculatedbyusingShoelace’sformulaEq. |     |     |     |     |     | (9): |     |
| -------------------------------------------------- | --- | --- | --- | --- | --- | ---- | --- |
n 2
−
| Area=0.5 |               | (q  | y q     | y)+(q | y     | q y )        | (9) |
| -------- | ------------- | --- | ------- | ----- | ----- | ------------ | --- |
|          |               | i   | i+1 i+1 | i     | n 1 0 | 0 n 1        |     |
|          | ·(cid:12)     | ·   | −       | ·     | − · − | · − (cid:12) |     |
|          | (cid:12)X i=0 |     |         |       |       | (cid:12)     |     |
|          | (cid:12)      |     |         |       |       | (cid:12)     |     |
|          | (cid:12)      |     |         |       |       | (cid:12)     |     |
where (q i ,y i ), i = 0,(cid:12)1,...,n 1, characterize the polygon vertices. (cid:12)Next, the
−
absolutedifferencebetweentheareasofthepredictedandobservedtrajectories
isshowninEq. (10).
|     |     | D=  | Area      | Area |        |     | (10) |
| --- | --- | --- | --------- | ---- | ------ | --- | ---- |
|     |     |     | predicted |      | actual |     |      |
−
|     |     | (cid:12) |     |     | (cid:12) |     |     |
| --- | --- | -------- | --- | --- | -------- | --- | --- |
A smaller value of D indicate(cid:12)s a better match betwe(cid:12)en the predicted and the
actualtrajectories.
4.3.2. FréchetDistance
This metric measures the similarity between two curves, taking into account
the location and arrangement of points. It is particularly useful for comparing
robotmanipulators’trajectoriesasittakesintoaccounttheirspatialandtemporal
aspects. Given two curves P and Q represented by sequences of points, the
Discrete Fréchet Distance (DFD) can be calculated by dynamic programming.
TheequationfortheDFDisrecursivelydefinedasfollows:
|     |     | DFD(P,Q)=c(P |     | ,   | Q)  |     | (11) |
| --- | --- | ------------ | --- | --- | --- | --- | ---- |
|     |     |              |     | | | | | | |     |      |
23

Wherec(i,j)isafunctiondefinedas:
d(P,Q ) ifi=1andj =1
i j
max(d(P,Q ), min(c(i 1,j),c(i 1,j 1),c(i,j 1)))
c(i,j)= i j − − − − (12)
  ifi>1andj >1


otherwise
∞




Where d(P,Q ) is the Euclidean distance between points P and Q , and P
i j i j
| |
and Q arethelengthsofthetrajectoriesP andQrespectively. Asmallervalue
| |
meansabetterfit.
4.3.3. Timecost
Apartfromprecision,computationalefficiencyisalsoacriticalfactorthatdeter-
minesthesuitabilityofadynamicsalgorithmforreal-timeapplications. There-
fore, theevaluationtakesintoaccounttheexpectedcomputationtimeforeach
point,andthefinalassessmentwillincludetheaveragepredictiontimeforasin-
glepoint.
Whenassessingthedynamicsofroboticarmmodels,traditionalmetricslikeMSE
maynotfullycapturethenuancesofperformance. Instead,theAreaDifference
metricismoreinformative,offeringaholisticviewbymeasuringthecumulative
deviation over the entire motion range, which is crucial for systems requiring
sustained, smooth operation. Similarly, the Fréchet Distance provides a com-
prehensivemeasureofthemodel’saccuracyinfollowingthedesiredtrajectory,
byconsideringthesequenceandtimingofthearm’smotion. Thesemetricsare
particularly suited to robotics, where the precision of movement patterns and
adherencetotheintendedpathareparamountforpracticalapplications.
4.4. ValidationoftheE2NNperformance
4.4.1. Performanceevaluationthroughsimulateddata
The model is initially configured for 5000 training iterations. However, imple-
menting an early stop mechanism enabled efficient convergence at 822 itera-
tionepochs,witheachsteptakingbetween5-8ms. Thisisachievedbytraining
the model in TensorFlow, incorporating early stopping triggered after 60 itera-
tion epochs without improvement, and using a checkpoint system to save the
modelparametersatthepointofminimumtrainingloss. Thisrevisedapproach
ensures a balance between sufficient training and computational efficiency. At
trainingconvergence,thetorquepredictionMAEoftheBenchmarkDRSNmodel
24

is0.10415andtheMAEofE2NNis0.10716. UsingthemetricsproposedinSec-
tion.4.3,thetestresultsonthe53976movementrecordingpointsareshownin
Table. 2 and Fig. 13. Moreover, the E2NN has a smaller model size and faster
responsespeedthanthebenchmarkDRSN,whichmakesitamoreefficientand
practical solution for robot trajectory fitting tasks. The results also show that
whilethebenchmarkmodelandtheproposedmethodhavesimilarerrormetrics
values,thebenchmarkmodel’sperformanceisachievedthroughover-fittingto
localpoints,resultinginagroupoflargeanddiscretepredictionpointsaround
theangularvelocityscopein(-5,5).Theerrors’maximumvalueisequalto44.431
Nm, which reflects ML’s violation of physical facts. In contrast, the proposed
·
E2NNarchitectureexhibitedanoveralltrendthatisclosertothegroundtruth.
Table2:Comparisonofdifferentmethodsonvariousmetrics.
Metrics
Method Responsetime Parameters
MSE AreaDifference FréchetDistance
ANN 0.6 42.9 56.7 3.3 10 4 66753
−
×
E2NN 0.5 8.3 14.3 1.1 10 4 56223
−
×
ThetrajectoryfittingresultsrevealedthattheE2NNisabletomoreaccuratelyfit
therobottrajectorytothegroundtruthcomparedtothebenchmarkDRSN.The
difference in performance between conventional DRSN and E2NN when tested
illustratestheexistenceofover-fittinginDRSN,especiallyastheyperformsim-
ilarlyintraining.
25

Figure11:ComparisonoftheperformanceoftheDRSN(above)andE2NN(below).
The difference between the training and final test results can be attributed to
thefactthatthetrainingandtestdataaregeneratedfromdifferentsimulations.
Specifically, the training data are generated from “direct-servo” and “inertia”,
whilethetestdataaregeneratedfrom“friction”,whichcoversawiderrangeof
workingconditionsandhasdifferentactualtorquefunctions.However,E2NNis
abletocompensateforsomeofthemissinginformationfrom“simulatedtraining
data”byembeddingitscorrespondingequations.
4.4.2. TestE2NNperformanceonrealdata
Inthecurrentinvestigation,ourobjectiveistometiculouslyevaluateandcom-
pareaspectrumofMLmethodologiesintherealmofrobotmanipulatortorque
estimation. Thisevaluationencompassesastrategicallyselectedarrayofmeth-
ods, tailored to the context of small sample sizes and complex data structures
typical in robotic applications. These include classical machine learning algo-
rithmssuchasK-NearestNeighbors(KNN)andSupportVectorMachine(SVM),
26

whicharerenownedfortheirefficacyinsmallerdatasets.Additionally,wedelve
intothedomainofdeeplearning,employingDeepMultilayerPerceptron(MLP)
and DRSN, both recognized for their profound capabilities in handling high-
dimensional data. The XGBRegressor, a gradient-boosted model, is also incor-
porated due to its proficiency in regression tasks. Furthermore, we explore the
applicationofNonlinearRegressionwithLassoRegularization,whereeachsub
termofthetorqueequation(referencedasEq.(8))functionsasanindividualop-
erator in physics-based model. Finally, the E2NN-enhanced DRSN, as depicted
inFig.10,standsasatestamenttotheintegrationofPIMLintothismultifaceted
| comparativestudy. | TheirperformanceisshowninTable. |     |     | 3andFig. 15to20. |     |
| ----------------- | ------------------------------- | --- | --- | ---------------- | --- |
Table3:Validationonreal-worlddata.
Metric
| Method            |         |                |                 | Maximumerror(Nm) |     |
| ----------------- | ------- | -------------- | --------------- | ---------------- | --- |
|                   | MSE     | AreaDifference | FréchetDistance |                  | ·   |
| DeepMLP           | 0.00272 | 3.998          | 0.249           | 0.510            |     |
| SVM               | 0.575   | 9.791          | 1.513           | 2.263            |     |
| XGBRegressor      | 0.00247 | 3.703          | 0.223           | 0.391            |     |
| KNN               | 0.00442 | 4.029          | 0.209           | 0.528            |     |
| DRSN              | 0.00314 | 4.835          | 0.160           | 0.374            |     |
| Physicsestimation | 0.00542 | 6.519          | 0.256           | 0.572            |     |
| E2NN              | 0.00103 | 1.248          | 0.173           | 0.172            |     |
According to Table. 3, it appears that KNN, with an MSE of 0.00442, Area Dif-
ferenceof4.029, andFréchetDistanceof0.209, wouldbeastrongcontenderin
this application. However, a deeper analysis reveals that while KNN does out-
performSVM(whichhasasignificantlyhigherMSEof0.575andAreaDifference
of9.791),itfallsshortwhencomparedtomoreadvancedmethodslikeDeepMLP
andDRSN.Theperformancegapisparticularlynoticeableinthecontextofcom-
plexdynamicsmodellingforroboticarms, whereDeepMLPsandDRSNsexcel
duetotheirmulti-leveldatarepresentationcapabilities.Thesemodels,withtheir
advancedfeatureextractionandnoisetoleranceabilities,areespeciallyadeptat
handlingtheintricateinterplaybetweenvariousinputandoutputvariables,such
asangulardisplacementandtorque.
27

Figure12:Predictionresultsonrealrobotmanipulators.
CombiningFig.12toFig.20,whicharescatterplotscomparingpredictedtorque
torealtorqueagainstmovementangularvelocity,weconcludethatE2NNemerges
asthemostnotablemodel,outperformingallothersasithasMSEof0.00103. It
fits the whole trajectory better. Its joint torque predictions have small and few
severedeviationsfromasinglelargeerror.
4.5. Discussionofmeasureddatatorquepredictionresults
Building on the discussion of different models’ torque prediction results, this
paperalsoinvestigatestheidentificationofinversedynamicsparametersusing
the E2NN model, assessing the torque prediction robustness of E2NN in real-
worldunseenfrictionscenarios.
4.5.1. Discussionofmeasureddatatorquepredictionresults
Inthecontextoffittingangulardisplacement,angularvelocity,andangularac-
celerationtoroboticarmjointtorque,thispaperfocusesontheperformanceof
differentmodelsonsuchmeasuredsmallsampledata. DRSNstandsoutamong
these models due to its balanced approach, offering a low maximum error of
0.374 and the lowest Fréchet Distance of 0.160 among the compared methods.
Itsarchitecturaladvantages,likeresidualconcatenationandcontractionopera-
tions, contribute significantly to this performance, enhancing feature selection
andreducingnoise,whichiscrucialforaccuratemodelling.
Inscenarioswithlimiteddata,theXGBRegressordemonstratesitsstrength.With
anMSEof0.00247andAreaDifferenceof3.703,itsurpassestheDeepMLPmodel.
Thishighlightstheeffectivenessofensemblemethods,particularlyinsmalldata
28

contexts. The XGBRegressor, through its boosting process, incrementally cor-
rects previous errors, thereby constructing a robust model that is less prone to
overfitting – a common concern in small datasets. Its ability to adapt and im-
provegraduallywitheachadditionalmodelintheensembleisakeyfactorinits
superiorperformance.
E2NNoutperformspreviousmodelslikeSVM,KNN,DeepMLP,andDRSN.The
combination of the Physics-Informed module, trigonometric functions in the
residual blocks, and the equation-based structure of the “Liquid” layer enables
theE2NNtoeffectivelymimictheinversedynamicsprocessoftheroboticarm
under physical constraints. It leads to notable improvements in predictive ac-
curacyandgeneralizationcapabilitiesovermodelsthatdonotincorporatesuch
domainknowledge.OnecanseethatE2NNcanaccuratelyfitthetrajectorywith
highprecisionandcomputationalefficiencyunderrealfrictionconditions,while
also exhibiting a good fit to the robot manipulator’s motion. The model’s per-
formance is better than the simulation data, which suggests that the impact of
frictionontherobotmanipulatorsduringsingle-jointmotionislesspronounced
inthereal-worldscenariothaninthesimulation.
4.5.2. Identificationofinversedynamicsparameters
Inthispaper,E2NNoutputsjointtorque,anditsembeddedphysicaloperatorcan
also serve to estimate the joint parameter β. To evaluate the E2NN’s learning
mechanism and its grasp of robot motion dynamics, we extracted the weights
corresponding to the embedded operator’s NN layer and compared them with
theβ valuesfromthegeneratedsimulationdata. Thiscomparisonallowedusto
assesswhetherE2NNhaseffectivelylearnedtherobotmotiondynamics.
Table4:Resultsofβestimationfortheroboticmanipulatorstorquemodel
βi 1 2 3 4 5 6 7 8 9 10
Real 0 0.600 0 0 0 0.010 0.015 0.200 0.100 0.300
Prosedmethods -0.0132 0.617 0.146 0.023 0.0987 0.0134 0.126 0.303 0.116 0.312
TheaverageweightsoftheE2NNdenselayerareusedasβvaluesfortherecon-
structedrobotmanipulator’storquetrajectory.Thefittingperformanceisevalu-
atedbycomparingthereconstructedtrajectorywiththegroundtruthtrajectory.
The obtained results are shown in Table. 4 and Fig. 13. The average accuracy
of the proposed methods, measured as the MAE, for the parameter estimation
in the robotic manipulators torque model is approximately 0.05433. This value
representstheaveragedeviationoftheestimatedvaluesfromtheactualvalues
29

acrossallparameters.ThereconstructedtrajectoriesusingE2NN’sweightshave
a high torque fitting accuracy reaching 97.1% (as its trajectory is shown in Fig.
14).
Figure13:ReconstructedtorquebyusingMatlab.
TheseresultsindicatethattheE2NNcanapproximatelysimulatetheactualbe-
haviouroftherobotmanipulator. Thisaccuracyiscriticalinapplicationswhere
fine motion control and subtle manipulation capabilities are required. The re-
sultssuccessfullydemonstratethecapabilityoftheE2NNinpredictingthejoint
torquesandestimatingthejointparametersβ ofaroboticmanipulator. Thekey
innovation of the E2NN lies in its embedded physical operator, which bridges
thegapbetweentheoreticalmodellingofroboticsandpracticalapplications.
4.5.3. InvestigationontheE2NN’srobustness
This paper employs data generated under the "Friction" working condition to
evaluatetherobustnessoftheE2NN.Thisprocessinvolvesapplyingthebench-
markmodelandtheE2NN,whichhavebeentrainedonthesamedataset,directly
to the new test without any additional training. The size of the new test set is
8996samples.ThepredictionresultsofthetwomodelsarepresentedinTable.5.
Duringthesteady-statemotionoftherobotmanipulatorsintheangularvelocity
range of -2 to 2, it can be observed that the benchmark DRSN model produces
largeoutlierpointsandextremelyunstablepredictedcurves. Themaximumer-
rorofDRSNmodelis5.3,whichishigherthanthatoftheE2NN,andthereare
significantoutliersintheslewingprocessaround-3and3.Inaddition,thebench-
markmodelshowsthatthepredictionresultsdeviatesignificantlyfromtheob-
servation in the enlarged view of the entire steady-state movement formation.
30

Figure14:ComparisonbetweentherobustnessperformanceoftheE2NN(below)modelandthe
benchmarkDRSN(above).
31

Table5:Comparisonoftherobustnessofdifferentmethodsacrossvariousmetricswhenapplied
tonewdata.
Metrics
Method Responsetime Parameters
MSE AreaDifference FréchetDistance
DRSN 1.1 14.4 8.2 1.2 10 4 66753
−
×
E2NN 0.3 1.6 1.6 8.8 10 5 56223
−
×
Besides, the E2NN is still able to fit the actual trajectory with promised trend
tracking.
5. Conclusionandfutureworks
ThisstudypresentstheEquationEmbeddedNeuralNetwork(E2NN),aninnova-
tivePhysics-informedmachinelearningapproachtailoredforaddressingrobotic
inverse dynamics challenges. E2NN showcases notable precision in predicting
torqueanddemonstratesrapidcomputationcapabilities,evenwithlimitedjoint
data. Its effectiveness is corroborated through both simulated and real-world
experiments on a 7-degree-of-freedom robotic manipulator. Key contributions
of this study include a comprehensive examination of existing hybrid models
thatmergephysicalprincipleswithmachinelearning,thedevelopmentandas-
sessment of the E2NN framework, the incorporation of a physics regulator to
enhanceparameterlearning, andthecreationofadynamic’liquid’mechanism
forcontinuousmodeladaptation.
It is founded and explored that at the heart of E2NN is a unique design that
utilizes inverse dynamics equations to form specialized neural network layers.
These layers are equipped with tailored activation functions and interconnec-
tionsthatmimicphysicsoperators,thusembeddingphysicalknowledgedirectly
intothenetworkarchitecture.AstandoutfeatureofE2NNisitsabilitytodynam-
ically adjust the connections between layers through gating units. This allows
thenetworktospontaneouslygeneratevariouscombinationsofphysicaloper-
ators in response to the input data. This dynamic, fluid-like structure is key to
E2NN’s adaptability. It allows the network to seamlessly adjust to varying in-
putsandequationsofmotion,therebymaintainingadynamicrepresentationof
physicsknowledge. Thisinnovativeapproachmarksasignificantadvancement
in the field of Physics-informed machine learning and opens new avenues for
roboticcontrolandsimulation.
Forthefuturedevelopmentoftheproposedmethodology,E2NNframeworkhas
32

complexityinitsmodeldesign.Itfeaturescustomlayersformathematicalcombi-
nations,aphysicalinformationlayer,aliquidmechanismforinter-layerconnec-
tions, and a loss function with neural network structural parameters and poly-
nomialweights. Somemoreeasyestablishmentmethodsareneeded. Architec-
turally,E2NNonthisconditioncanbegeneralizedbysharingparametersacross
multiple sub-networks. It also exhibits imprecision in estimating inverse dy-
namicsparameters,includingnon-zeroestimatesforexpectedzeroparameters,
suggesting potential over-parameterization. Incorporating prior knowledge of
thenumberandstatesofpendingparametersmaybenecessary. Fromtheper-
spective of applicationFuture work could focus on testing the method on more
complexsystems,ascouldbetheentire7-dofmanipulatorandcollaborativeap-
plicationswherehumansandexternalforcesareappliedontherobot.
References
[1] S. Moberg, Modeling and control of flexible manipulators, Ph.D. thesis,
LinköpingUniversityElectronicPress(2010).
[2] B.Siciliano,L.Sciavicco,L.Villani,G.Oriolo,Robotics:modelling,planning
andcontrol,SpringerScience&BusinessMedia,2010.
[3] B.Armstrong,O.Khatib,J.Burdick,Theexplicitdynamicmodelandiner-
tial parameters of the puma 560 arm, in: IEEE Proceedings. International
conferenceonroboticsandautomation,Vol.3,1986,pp.510–518.
[4] A.K.Tangirala,Principlesofsystemidentification:theoryandpractice,Crc
Press,2018.
[5] F.Ardiani,Contributiontotheparametricidentificationofdynamicmodels:
applicationtocollaborativerobotics,Ph.D.thesis,Toulouse,ISAE(2023).
[6] Q. Leboutet, J. Roux, A. Janot, J. R. Guadarrama-Olvera, G. Cheng, Iner-
tialparameteridentificationinrobotics: Asurvey,AppliedSciences11(9)
(2021)4303.
[7] W. Khalil, E. Dombre, Modeling identification and control of robots, CRC
Press,2002.
[8] S.Briot,M.Gautier,Globalidentificationofjointdrivegainsanddynamic
parametersofparallelrobots,MultibodySystemDynamics33(1)(2015)3–
26.
33

[9] A. Fabio, B. Mourad, A. Janet, On the dynamic parameter identification
of collaborative manipulators: Application to a kuka iiwa, in: 2022 17th
International Conference on Control, Automation, Robotics and Vision
(ICARCV),IEEE,2022,pp.468–473.
[10] A.Janot,P.-O.Vandanjon,M.Gautier,Agenericinstrumentalvariableap-
proach for industrial robot identification, IEEE Transactions on Control
SystemsTechnology22(1)(2013)132–145.
[11] F. Ardiani, M. Benoussaad, A. Janot, Comparison of least-squares and in-
strumentalvariablesforparametersestimationondifferentialdrivemobile
robots,IFAC-PapersOnLine54(7)(2021)310–315.
[12] M. Gautier, A. Janot, P.-O. Vandanjon, A new closed-loop output error
methodforparameteridentificationofrobotdynamics,IEEETransactions
onControlSystemsTechnology21(2)(2012)428–444.
[13] M. Brunot, A. Janot, F. Carrillo, H. Garnier, Comparison between the
idim-iv method and the didim method for industrial robots identification,
in: IEEE International Conference on Advanced Intelligent Mechatronics
(AIM),2017,pp.571–576.
[14] M.Brunot,A.Janot,F.Carrillo,J.Cheong,J.-P.Noël,Outputerrormethods
for robot identification, Journal of Dynamic Systems, Measurement, and
Control142(3)(2020)031002.
[15] F.Ardiani,M.Benoussaad,A.Janot,Improvingrecursivedynamicparame-
terestimationofmanipulatorsbyknowingrobot’smodelintegratedinthe
controller,IFAC-PapersOnLine55(20)(2022)223–228.
[16] A. Bahloul, S. Tliba, Y. Chitour, Dynamic parameters identification of an
industrialrobotwithandwithoutpayload,Ifac-Papersonline51(15)(2018)
443–448.
[17] A.Fabio,A.Janot,B.Mourad,Industrialrobotparameteridentificationus-
ingaconstrainedinstrumentalvariablemethod,in:2022IEEE/RSJInterna-
tionalConferenceonIntelligentRobotsandSystems(IROS),IEEE,2022,pp.
6250–6255.
34

[18] C.A.Lightcap,S.A.Banks,Anextendedkalmanfilterforreal-timeestima-
tionandcontrolofarigid-linkflexible-jointmanipulator,IEEETransactions
onControlSystemsTechnology18(1)(2009)91–103.
[19] M.Ruderman,Modelingofelasticrobotjointswithnonlineardampingand
hysteresis,RobotSystControlProgram(2012)293–312.
[20] M.Indri,S.Trapani,Frameworkforstaticanddynamicfrictionidentifica-
tionforindustrialmanipulators,ASMETransactionsonMechatronics25(3)
(2020)1589–1599.
[21] S.Surati,S.Hedaoo,T.Rotti,V.Ahuja,N.Patel,Pickandplaceroboticarm:
areviewpaper,Int.Res.J.Eng.Technol8(2)(2021)2121–2129.
[22] A.Mousaei,M.Gheisarnejad,M.H.Khooban,Robustslidingmodecontrol
fortwo-wheelrobotwithoutkinematicequations(2023).
[23] P. Moradi, M. H. Korayem, N. Y. Lademakhi, Online identification and ro-
bust compensation of extended nonlinear time-varying friction model in
robotic arms, Journal of Mechanical Science and Technology 37 (1) (2023)
367–373.
[24] J. A. Luz Junior, J. M. Balthazar, M. A. Ribeiro, F. C. Janzen, A. M. Tusset,
Dynamicmodelofaroboticmanipulatorwithonedegreeoffreedomwith
friction component., International Journal of Robotics & Control Systems
3(2)(2023).
[25] R.Mukhopadhyay,R.Chaki,A.Sutradhar,P.Chattopadhyay,Modellearn-
ingforroboticmanipulatorsusingrecurrentneuralnetworks,in:TENCON
2019 - 2019 IEEE Region 10 Conference (TENCON), 2019, pp. 2251–2256.
doi:10.1109/TENCON.2019.8929622.
[26] F. Semeraro, A. Griffiths, A. Cangelosi, Human-robot collaboration and
machine learning: A systematic review of recent research, Robotics and
Computer-IntegratedManufacturing79(2022).
[27] L.Jin,S.Li,B.Hu,M.Liu,Asurveyonprojectionneuralnetworksandtheir
applications,AppliedSoftComputing76(2019)533–544.
[28] L. Ljung, Q. Zhang, P. Lindskog, A. Juditski, Estimation of grey box and
black box models for non-linear circuit data, IFAC Proceedings Volumes
37(13)(2004)399–404.
35

[29] G. E. Karniadakis, I. G. Kevrekidis, L. Lu, P. Perdikaris, S. Wang, L. Yang,
Physics-informed machine learning, Nature Reviews Physics 3 (6) (2021)
422–440.
[30] B.S.Pavse,F.Torabi,J.Hanna, G.Warnell,P.Stone,Ridm: Reinforcedin-
verse dynamics modeling for learning from a single observed demonstra-
tion,IEEERoboticsandAutomationLetters5(4)(2020)6262–6269.
[31] M. Lutter, J. Peters, Combining physics and deep learning to learn
continuous-time dynamics models, The International Journal of Robotics
Research42(3)(2023)83–107.
[32] X. Wang, X. Liu, L. Chen, H. Hu, Deep-learning damped least squares
method for inverse kinematics of redundant robots, Measurement 171
(2021)108821.
[33] F. Djeumou, C. Neary, E. Goubault, S. Putot, U. Topcu, Neural networks
withphysics-informedarchitecturesandconstraintsfordynamicalsystems
modeling,in:LearningforDynamicsandControlConference,PMLR,2022,
pp.263–277.
[34] W.Sun,N.Akashi,Y.Kuniyoshi,K.Nakajima,Physics-informedrecurrent
neuralnetworksforsoftpneumaticactuators,IEEERoboticsandAutoma-
tionLetters7(3)(2022)6862–6869.
[35] H. Ren, P. Ben-Tzvi, Learning inverse kinematics and dynamics of a
robotic manipulator using generative adversarial networks, Robotics and
AutonomousSystems124(2020)103386.
[36] N.Yilmaz,J.Y.Wu,P.Kazanzides,U.Tumerdem,Neuralnetworkbasedin-
versedynamicsidentificationandexternalforceestimationonthedavinci
research kit, in: 2020 IEEE International Conference on Robotics and Au-
tomation (ICRA), 2020, pp. 1387–1393. doi:10.1109/ICRA40945.2020.
9197445.
[37] M. Lahariya, C. Innes, C. Develder, S. Ramamoorthy, Learning physics-
informed simulation models for soft robotic manipulation: A case study
with dielectric elastomer actuators, in: 2022 IEEE/RSJ International Con-
ference on Intelligent Robots and Systems (IROS), IEEE, 2022, pp. 11031–
11038.
36

[38] C. Rodwell, P. Tallapragada, Physics-informed reinforcement learning for
motioncontrolofafish-likeswimmingrobot(2022).
[39] K. Morse, N. Das, Y. Lin, A. S. Wang, A. Rai, F. Meier, Learning state-
| dependent | losses for | inverse dynamics |     | learning, | in: 2020 | IEEE/RSJ | Inter- |
| --------- | ---------- | ---------------- | --- | --------- | -------- | -------- | ------ |
nationalConferenceonIntelligentRobotsandSystems(IROS),IEEE,2020,
pp.5261–5268.
[40] F.Cursi,D.Chappell,P.Kormushev,Augmentinglossfunctionsoffeedfor-
| ward neural | networks      | with differential |     | relationships |     | for robot | kinematic |
| ----------- | ------------- | ----------------- | --- | ------------- | --- | --------- | --------- |
| modelling,  | in: 2021 20th | International     |     | Conference    | on  | Advanced  | Robotics  |
(ICAR),IEEE,2021,pp.201–207.
[41] G.Pizzuto,M.Mistry,Physics-penalisedregularisationforlearningdynam-
| ics models | with contact, | in: Learning |     | for Dynamics |     | and Control, | PMLR, |
| ---------- | ------------- | ------------ | --- | ------------ | --- | ------------ | ----- |
2021,pp.611–622.
[42] S.Dereli,R.Köker,Ameta-heuristicproposalforinversekinematicssolu-
| tionof7-dofserialroboticmanipulator: |     |     |     | quantumbehavedparticleswarm |     |     |     |
| ------------------------------------ | --- | --- | --- | --------------------------- | --- | --- | --- |
algorithm,ArtificialIntelligenceReview53(2020)949–964.
[43] R. Ram, P. M. Pathak, S. Junco, Inverse kinematics of mobile manipulator
usingbidirectionalparticleswarmoptimizationbymanipulatordecoupling,
MechanismandMachineTheory131(2019)385–405.
[44] S.Dereli, R.Köker, Simulationbasedcalculationoftheinversekinematics
| solution | of 7-dof robot | manipulator | using | artificial | bee | colony | algorithm, |
| -------- | -------------- | ----------- | ----- | ---------- | --- | ------ | ---------- |
SNAppliedSciences2(2020)1–11.
[45] M. Alebooyeh, R. J. Urbanic, Neural network model for identifying
| workspace, | forward | and inverse | kinematics |     | of the 7-dof | yumi | 14000 abb |
| ---------- | ------- | ----------- | ---------- | --- | ------------ | ---- | --------- |
collaborativerobot,IFAC-PapersOnLine52(10)(2019)176–181.
[46] J.S.Toquica,P.S.Oliveira,W.S.Souza,J.M.S.Motta,D.L.Borges,Anan-
alyticalandadeeplearningmodelforsolvingtheinversekinematicprob-
lemofanindustrialparallelrobot,Computers&IndustrialEngineering151
(2021)106682.
[47] J. Demby’s, Y. Gao, G. N. DeSouza, A study on solving the inverse kine-
| matics | of serial robots | using artificial |     | neural | network | and | fuzzy neural |
| ------ | ---------------- | ---------------- | --- | ------ | ------- | --- | ------------ |
37

network,in: 2019IEEEinternationalconferenceonfuzzysystems(FUZZ-
IEEE),IEEE,2019,pp.1–6.
[48] D.Romeres,M.Zorzi,R.Camoriano,S.Traversaro,A.Chiuso,Derivative-
freeonlinelearningofinversedynamicsmodels,IEEETransactionsonCon-
trolSystemsTechnology28(3)(2019)816–830.
[49] P.O.Sturm,A.S.Wexler,Conservationlawsinaneuralnetworkarchitec-
ture:enforcingtheatombalanceofajulia-basedphotochemicalmodel(v0.
2.0),GeoscientificModelDevelopment15(8)(2022)3417–3431.
[50] M.Gautier,W.Khalil,Directcalculationofminimumsetofinertialparam-
etersofserialrobots, IEEETransactionsonroboticsandAutomation6(3)
(1990)368–373.
[51] W. Khalil, F. Bennis, Comments on" direct calculation of minimum set of
inertialparametersofserialrobots",IEEEtransactionsonroboticsandau-
tomation10(1)(1994)78–79.
[52] M.Gautier,Numericalcalculationofthebaseinertialparametersofrobots,
Journalofroboticsystems8(4)(1991)485–506.
[53] G.H.Golub,C.F.VanLoan,Matrixcomputations,JHUpress,2013.
[54] J.Santolaria,M.GinéS,Uncertaintyestimationinrobotkinematiccalibra-
tion, Robotics and Computer-Integrated Manufacturing 29 (2) (2013) 370–
384.
[55] L. Ljung, System Identification: Theory for the User, Pearson Education,
1998.
[56] F.Pukelsheim,Optimaldesignofexperiments,SIAM,2006.
[57] J. Swevers, W. Verdonck, J. De Schutter, Dynamic model identification for
industrialrobots,IEEEControlsystemsmagazine27(5)(2007)58–71.
[58] J. Jia, M. Zhang, X. Zang, H. Zhang, J. Zhao, Dynamic parameter identifi-
cation for a manipulator with joint torque sensors based on an improved
experimentaldesign,Sensors19(10)(2019)2248.
38

[59] L.Simoni,M.Beschi,G.Legnani,A.Visioli,Frictionmodelingwithtemper-
| ature effects | for industrial | robot | manipulators, | in: IEEE/RSJ | international |     |
| ------------- | -------------- | ----- | ------------- | ------------ | ------------- | --- |
conferenceonintelligentrobotsandsystems(IROS),2015,pp.3524–3529.
[60] A.Raviola,R.Guida,A.DeMartin,S.Pastorelli,S.Mauro,M.Sorli,Effectsof
temperatureandmountingconfigurationonthedynamicparametersiden-
tificationofindustrialrobots,Robotics10(3)(2021)83.
[61] P.Hamon,M.Gautier,P.Garrec,A.Janot,Dynamicidentificationofrobot
| with a load-dependent |     | joint friction | model, | in: 2010 IEEE | Conference | on  |
| --------------------- | --- | -------------- | ------ | ------------- | ---------- | --- |
Robotics,AutomationandMechatronics,IEEE,2010,pp.129–135.
[62] Y.Dai,J.Wang,J.Li,Dynamicenvironmentpredictiononunmannedmobile
| manipulator | robot | via ensemble | convolutional | randomization | networks, |     |
| ----------- | ----- | ------------ | ------------- | ------------- | --------- | --- |
AppliedSoftComputing125(2022)109136.
[63] R.Hasani,M.Lechner,A.Amini,D.Rus,R.Grosu,Liquidtime-constantnet-
| works, in: | Proceedings | of the | AAAI Conference | on Artificial | Intelligence, |     |
| ---------- | ----------- | ------ | --------------- | ------------- | ------------- | --- |
Vol.35,2021,pp.7657–7666.
[64] G. Schreiber, A. Stemmer, R. Bischoff, The fast research interface for the
| kukalightweightrobot,in: |               | IEEEworkshoponinnovativerobotcontrolar- |              |        |            |     |
| ------------------------ | ------------- | --------------------------------------- | ------------ | ------ | ---------- | --- |
| chitectures              | for demanding | (Research)                              | applications | how to | modify and | en- |
hancecommercialcontrollers(ICRA),2010,pp.15–21.
[65] L.Tonin,F.C.Bauer,J.d.R.Millán,Theroleofthecontrolframeworkfor
continuousteleoperationofabrain–machineinterface-drivenmobilerobot,
IEEETransactionsonRobotics36(1)(2019)78–91.
[66] H. Shen, L. Pan, J. Qian, Research on large-scale additive manufacturing
basedonmulti-robotcollaborationtechnology,AdditiveManufacturing30
(2019)100906.
6. Annex
39

Figure15:TorquetrajectorypredictedbyMLP
Figure16:TorquetrajectorypredictedbySVM
40

Figure17:TorquetrajectorypredictedbyKNN
41

Figure18:TorquetrajectorypredictedbyXGBRegressor
42

Figure19:TorquetrajectorypredictedbyDRSN
43

Figure20:TorquetrajectorypredictedbyPhysicsmodel
44

Highlights
 Comprehensive review and summarization of hybrid framework in robot modeling.
 Physics-informed machine learning framework for robot parameter identification and
torque prediction.
 Dynamic "liquid" mechanism for enhancing the flexibility and performance of the
proposed framework in different working modes.
 Validation of the proposed framework through simulation and real operational
conditions.

Declaration of interests
☒ The authors declare that they have no known competing financial interests or personal relationships
that could have appeared to influence the work reported in this paper.