This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
|            |     |                  |          | IEEE/ASMETRANSACTIONSONMECHATRONICS |     |      |     |              |     |     |       |          |     |     | 1   |
| ---------- | --- | ---------------- | -------- | ----------------------------------- | --- | ---- | --- | ------------ | --- | --- | ----- | -------- | --- | --- | --- |
|            |     |                  | Modeling |                                     |     |      | and | Compensation |     |     |       |          |     |     |     |
|            | of  | Backlash-Induced |          |                                     |     |      |     | Dynamics     |     |     | Error |          | in  |     |     |
| Industrial |     |                  | Robots   |                                     |     | With |     | a PINN-Based |     |     |       | Approach |     |     |     |
Hongbo Hu , Zhongkai Zhang , and Chungang Zhuang , Member, IEEE
Abstract—Roboticdynamicsmodelingandidentification Compared to other error sources, backlash-induced dynamics
methods lay the foundation for higher precision applica- errorexhibitsmoredistinctcharacteristicsandtypicallylarger-
| tions of | robots. | However, |     | challenges | remain | in  | compen- |           |        |             |       |       |      |             |     |
| -------- | ------- | -------- | --- | ---------- | ------ | --- | ------- | --------- | ------ | ----------- | ----- | ----- | ---- | ----------- | --- |
|          |         |          |     |            |        |     |         | magnitude | abrupt | variations, | which | exert | more | significant | im- |
satingfornonlinearcharacteristicssuchasjointbacklash.
pactsonrobotcontrolbasedondynamicsmodel[6].Moreover,
Specifically,theserialkinematicsofmultiaxisserialrobots
amplify the impact of backlash on dynamics. This article thelifecycleofindustrialrobotsissignificantlyaffectedbywear
addressesthebacklashphenomenoninsixdegreesoffree- duetocontinuousandrepetitivejointmovements.Theresulting
dom(DOF)serialrobotsandproposesaphysics-informed increase in backlash can jeopardize task execution, leading to
| neural       | network | (PINN)-based |        | approach |            | for modeling | and       |            |          |     |          |         |         |     |       |
| ------------ | ------- | ------------ | ------ | -------- | ---------- | ------------ | --------- | ---------- | -------- | --- | -------- | ------- | ------- | --- | ----- |
|              |         |              |        |          |            |              |           | unintended | downtime | and | economic | losses. | Despite | the | char- |
| compensating |         | dynamics     | error. | First,   | a temporal |              | detection |            |          |     |          |         |         |     |       |
acteristiclowbacklashofharmonicdrives,bothindustrialand
andclassificationstrategyisdesignedbasedontheforma-
collaborativerobotsinevitablyexperiencebacklasherrors.This
tionmechanismofbacklash.Next,anerrormodelbasedon
Gaussian basis functions is proposed, and a correspond- issueisparticularlypronouncedinmultiaxisserialrobots,where
ing PINN is constructed to implement online compensa- theserialkinematicsamplifythenegativeimpactsoffrictionand
tionforbacklash-induceddynamicserror.Finally,theerror
gearclearances[7].
compensationperformanceoftheproposedmethodisval-
DynamicsidentificationbasedontherecursiveNewton–Euler
| idated experimentally, |     |        | achieving | average   |        | error         | reductions |             |        |            |     |         |          |           |     |
| ---------------------- | --- | ------ | --------- | --------- | ------ | ------------- | ---------- | ----------- | ------ | ---------- | --- | ------- | -------- | --------- | --- |
|                        |     |        |           |           |        |               |            | formulation | is the | mainstream | in  | robotic | dynamics | modeling, |     |
| of 45.93%              | and | 34.19% | on        | two 6-DOF | robots | respectively, |            |             |        |            |     |         |          |           |     |
outperforming other advanced methods. Additionally, the which involves linearizing the dynamics model, extracting the
designed compensation strategy ensures the superior ro- minimal set of inertia parameters, and utilizing least squares
bustnessoftheproposedmethod.
|     |     |     |     |     |     |     |     | regression. | Sousa | and Cortesão | [8] | improved | the | precision | of  |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | ------------ | --- | -------- | --- | --------- | --- |
Index Terms—Backlash error modeling, dynamics com- modelingbyconsideringthephysicalconstraintsofjointmod-
pensation, industrial robot, physics informed neural net- els.Hanetal.[9]developedatriple-loopiterativelearningstrat-
works.
egyforrobotdynamics,whicheffectivelyhandledfrictionand
outlierdata.However,constrainedbythelinearizationrequire-
I. INTRODUCTION mentsoftheleastsquaresregressionmodel,dynamicsparameter
identificationmethodstypicallyunderperforminaddressingthe
HIGHER
|     |     | performance | has | become | a   | prerequisite | for the | nonlinearitiesindynamics. |     |     |     |     |     |     |     |
| --- | --- | ----------- | --- | ------ | --- | ------------ | ------- | ------------------------- | --- | --- | --- | --- | --- | --- | --- |
furtherapplicationsofrobots.Accuratedynamicsmodels
|            |          |             |     |         |       |             |     | In contrast, | learning-based |     | approaches, |     | particularly |     | those |
| ---------- | -------- | ----------- | --- | ------- | ----- | ----------- | --- | ------------ | -------------- | --- | ----------- | --- | ------------ | --- | ----- |
| and torque | feedback | effectively |     | enhance | robot | performance |     | in           |                |     |             |     |              |     |       |
employingphysics-informedneuralnetworks(PINNs),exhibit
| trajectory | tracking | and | force | control | [1], | [2], [3]. | To address |     |     |     |     |     |     |     |     |
| ---------- | -------- | --- | ----- | ------- | ---- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
superiornonlinearlearningcapabilitiesandgeneralizationabil-
thedegradationintheaccuracyofdynamicsmodelscausedby
ities,becomingasignificantresearchtopicinroboticdynamics
nonlinearbehaviors,dynamicserrorcompensationisintroduced modeling[10],[11].Lutteretal.[12]combineddeeplearning
torefineinversedynamicsestimation,withproveneffectiveness
|     |     |     |     |     |     |     |     | methods | with Lagrangian |     | dynamics | to  | propose | the deep | La- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------------- | --- | -------- | --- | ------- | -------- | --- |
inhuman–robotinteraction[4]andcontactforceestimation[5].
grangiannetworkasadynamicsmodelingframeworkforrobots.
Lahoudetal.[13]furtherintegratedtheCoulomb-viscousfric-
|          |          |       |         |     |          |      |             | tion model | to achieve | better         | overall | modeling   |      | performance. |      |
| -------- | -------- | ----- | ------- | --- | -------- | ---- | ----------- | ---------- | ---------- | -------------- | ------- | ---------- | ---- | ------------ | ---- |
|          |          |       |         |     |          |      |             | However,   | current    | learning-based |         | approaches | tend | to treat     | var- |
| Received | 4 August | 2025; | revised | 13  | November | 2025 | and 17 Jan- |            |            |                |         |            |      |              |      |
uary2026;accepted1March2026.RecommendedbyTechnicalEditor
iousnonlineardynamicsfactorsasaunifiedblack-boxmodule,
| R. Meattini | and | Senior Editor | C.  | Clévy | This work | was | sponsored | in           |          |         |     |              |     |                 |     |
| ----------- | --- | ------------- | --- | ----- | --------- | --- | --------- | ------------ | -------- | ------- | --- | ------------ | --- | --------------- | --- |
|             |     |               |     |       |           |     |           | complicating | accurate | capture | of  | the dynamics |     | characteristics |     |
partbytheNationalNaturalScienceFoundationofChinaunderGrant
ofbacklash.
| 52275500, | and in | part by | the Explorers |     | Program | of Shanghai | (Basic |     |     |     |     |     |     |     |     |
| --------- | ------ | ------- | ------------- | --- | ------- | ----------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
ResearchFunding)underGrant24TS1414700. (Correspondingauthor: Inthefieldofcontrolengineering,researchongearbacklashis
ChungangZhuang.)
relativelycomprehensive.Theseparationandcontactingclosure
| The authors |     | are with | the | School | of Mechanical |     | Engineering, |     |     |     |     |     |     |     |     |
| ----------- | --- | -------- | --- | ------ | ------------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Shanghai Jiao Tong University, Shanghai 200240, China (e-mail: ofgearboxteethareconsideredthecausesofbacklash-induced
cgzhuang@sjtu.edu.cn). dynamicserror.Theseverityofbacklashdeterminesthemagni-
Color versions of one or more figures in this article are available at tudeofspikesinmotorcurrent,whichinturncausesdeviations
https://doi.org/10.1109/TMECH.2026.3670322.
DigitalObjectIdentifier10.1109/TMECH.2026.3670322 betweentheactualjointtorqueandthemodel-predictedtorque,
1083-4435©2026IEEE.Allrightsreserved,includingrightsfortextanddatamining,andtrainingofartificialintelligenceandsimilartechnologies.
Personaluseispermitted,butrepublication/redistributionrequiresIEEEpermission.Seehttps://www.ieee.org/publications/rights/index.html
formoreinformation.
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore.  Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
| 2   |     |     |     |     |     |     |     | IEEE/ASMETRANSACTIONSONMECHATRONICS |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- |
resultingincorresponding dynamics error[14].Therefore,the proposes a PINN-based compensation approach for backlash-
change in the direction of joint motion is a prerequisite for induced dynamics errors. Initially, a time-series module is
the generation of backlash. An overview of classic backlash utilized to perform online localization and classification of
compensationmethodsisprovidedin[15].Cobleetal.[16]use backlash-inducederror.Subsequently,anerrormodelisdevel-
piecewiselinearspringforcetoreplacethebacklashmechanism oped,employingGaussianbasisfunctionsandincorporatingan
andinnovativelyemployphysics-informedmachinelearningto analysisofthecausativefactorsofbacklash.Thismodelisthen
investigatethefrictionandbacklashinrotatingstructures. usedwithadesignedPINNtolearnthelatentmappingbetween
Current theoretical research on the compensation of gear the error model parameters and the states of robot joint mo-
backlash in robots remains limited. Ruderman et al. [17] pro- tion.Across-validationexperimentisconductedtoevaluatethe
posedanelasticrobotjointmodelbasedonthePreisachmodel, compensationperformanceoftheproposedmethodforbacklash
which captures the nonlinearities of friction, hysteresis, and errors,comparingitwithotheradvancedmethods.Additionally,
backlash. Ali et al. [7] studied the dynamic behavior of gear a load generalization experiment is performed to verify the
backlashinindustrialrobotsanditsmeasurability.Guidaetal. applicability of this method. The primary contributions are as
| [14]exploredtheeffectsanddetectionmethodsofbacklashin |     |     |     |     |     |     | follows. |     |     |     |
| ----------------------------------------------------- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
the collaborative robot with dual encoders. However, the de- 1) Ageneralcompensationmodelforbacklasherrorbased
pendencyoftheabovemethodsonmodelaccuracyandsensing onGaussianbasisfunctionsisproposed,consideringthe
limitstheirapplicationscenarios. potentialrelationshipbetweenbacklashandtherobotmo-
On the other hand, due to the difficulty of comprehensively tionstatestoavoidcomplexbacklashcontactmodeling.
modelingtheforcecontactprocessinvolvedinbacklash,some 2) Online detection and classification of backlash are
studies have instead focused on the compensation for non- achievedbyleveragingatemporalpredictionmoduleto
linear errors. Yang et al. [18] proposed a continuous friction learnthehistoricalmotioninformationoftherobot.
feedforwardslidingmodecontroller,whichutilizesavelocity- 3) ThedesignedPINNforerrorcompensationisconstructed
dependent function to compute feedforward control terms to byembeddingthebacklasherrormodeltoprovidephys-
addressdiscontinuouserrordisturbances.Zhangetal.[19]used icalpriors.Thecompensationperformanceandgeneral-
afeedforwardcontrolstrategyfromthekinematicperspectiveto izationcapabilityareevaluatedthroughexperiments.
suppressbacklashandfrictionduringjointreversal.Hanetal. The rest of this article is structured as follows. Section II
[20]developedamultipulsecompensationstrategyfornonlinear provides an overview of the necessary theoretical background
errors during joint commutation, exploring the potential rela- andrelatedwork.SectionIIIdetailstheproposedPINN-based
tionship between compensation parameters and joint angular modeling and compensation method for the backlash-induced
acceleration. dynamicserror,includingthedesignoftheerrordetectionand
Methods based on deep learning benefit from the excel- classificationmodule.Theexperimentalvalidationoftheerror
lent nonlinear fitting capabilities, becoming another important compensation performance, along with analysis and compara-
branchforerrorcompensationinrobotics.Tanetal.[21]con- tive evaluation, is presented in Section IV. Finally, Section V
sidered the pose-dependent impact of load on joint tracking concludesthearticle.
errorsandproposedarobottrackingerrorpredictionandcom-
pensation method based on temporal convolutional networks II. PRELIMINARIES
(TCN).Zhuangetal.[6]constructedasemiparametricdynam-
A. RobotDynamicsandFrictionModeling
| ics model | based | on convolutional |     | neural | networks | to  | achieve |     |     |     |
| --------- | ----- | ---------------- | --- | ------ | -------- | --- | ------- | --- | --- | --- |
dynamics compensation. Çallar and Böttger [22] proposed a For an n degrees of freedom (DOF) serial robot, the total
hybrid learning framework for robot dynamics targeted at lo- torqueexertedoneachjointtypicallycomprisesdynamicstorque
∈(cid:3)n×1, ∈(cid:3)n×1,
cally isotropic motion, combining the dynamics model with a τ friction torque τ and torque errors
|     |     |     |     |     |     |     | dyn | fri |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
data-drivenmodelbasedonlongshort-termmemorynetworks. τ ∈(cid:3)n×1attributabletootherdifficult-to-modelstrongnon-
err
| Furthermore, | recent | studies | have       | attempted  | to            | incorporate | the linearfactors |         |      |     |
| ------------ | ------ | ------- | ---------- | ---------- | ------------- | ----------- | ----------------- | ------- | ---- | --- |
| disturbance  | Kalman | filter  | to enhance | the        | dynamic       | estimation  |                   |         |      |     |
|              |        |         |            |            |               |             | τ                 | =τ +τ   | +τ   |     |
|              |        |         |            |            |               |             |                   | dyn fri | err. | (1) |
| performance  | of     | robotic | systems    | with model | uncertainties |             | [5],              |         |      |     |
[23].Despiteadvances, theomissionofthepotentialinterplay Thedynamicstorqueofrobotjointscanbederivedinthesame
| between | backlash | and joint | motion | in these | methods |     | hampers |     |     |     |
| ------- | -------- | --------- | ------ | -------- | ------- | --- | ------- | --- | --- | --- |
formusingeithertheNewton–EulermethodortheLagrangian
| theaccuratecaptureofbacklash-induceddynamicserror. |     |     |     |     |     |     | method |     |     |     |
| -------------------------------------------------- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- |
Investigatingthedynamicsbehaviorofgearbacklashthrough (cid:2) (cid:5)
|     |     |     |     |     |     |     |            |     | (cid:3) (cid:4) T |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ----------------- | --- |
|     |     |     |     |     |     |     | =M(q)q¨+M˙ | 1   | ∂ TM(q)q˙         |     |
the information available on industrial robots presents signifi- τ (q)q˙ − q˙ +G(q)
|     |     |     |     |     |     |     | dyn | 2 ∂q |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
cantchallenges.Thequalityoftherobotsignalsoftenrestricts (cid:6) (cid:7)(cid:8) (cid:9)
| effective | dynamics | compensation. |     | Therefore, | gear | backlash | is  |     |     |     |
| --------- | -------- | ------------- | --- | ---------- | ---- | -------- | --- | --- | --- | --- |
:=C(q,q˙)q˙
typically simplified as a static effect and compensated for (2)
. ..
through calibration techniques, which limits the accuracy and where q ∈(cid:3)n×1 denotes the joint angle, while q ,q ∈(cid:3)n×1
robustnessofthecompensation. representthekinematicstatesoftherobot.M(q)∈(cid:3)n×nisthe
|             |     |              |        |     |          |     | symmetricandpositivedefinitemassmatrix,C(q, |     | q . )∈(cid:3)n×n |     |
| ----------- | --- | ------------ | ------ | --- | -------- | --- | ------------------------------------------- | --- | ---------------- | --- |
| To mitigate |     | the negative | impact | of  | backlash | and | achieve                                     |     |                  |     |
morepreciseinversedynamicsestimationofrobots,thisarticle denotestheCoriolisandcentrifugalmatrix,andG(q)∈(cid:3)n×1
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore.  Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
HUetal.:MODELINGANDCOMPENSATIONOFBACKLASH-INDUCEDDYNAMICSERRORININDUSTRIALROBOTS 3
servesastheinputtothei-thnetworklayer,thusyielding
∂ ∂ h h i− i 1 =diag (cid:3) g (cid:4) (cid:10) WT i h i−1 +b i (cid:11)(cid:4) W i. (8)
Bysubstituting(8)into(6),∂L/∂qcanbeobtainedthrough
achaincalculation,andd(LLT
)/dtcanthenbefurtherderived
based on (5). The procedure for deriving ∂(q
.TLLT
q
.
)/∂q
followsasimilarapproach
(cid:14) (cid:15) (cid:16) (cid:17)
∂ q .TLLT q . =q .T ∂L LT +L ∂LT q . . (9)
∂q ∂q ∂q
Therefore,thedynamicstorquecanbedetermined,witheach
term inferred through PINNs. Notably, the Stribeck effect be-
comespronouncedatlowvelocities,characterizedbyadecrease
infrictionwithincreasingvelocity[25].TakingtheStribeckef-
Fig.1. PINN-basedrobotdynamicsandfrictionmodeling. fectintoaccount,thefrictiontorqueandthecoefficientoffriction
demonstrate a nonlinear relationship, further complicating the
modelingofjointdynamics.Thefrictiontorqueofthekthjoint
signifiesthegravityvector.Themassmatrixcanbedecomposed canbeexpressedas
asfollows: (cid:14) (cid:15)
.
M(q)=L(q)LT (q) (3) τ f k ri =W f q k,v s k ,δ s k ,α k K f
(cid:3) (cid:4)
whereL(q)∈(cid:3)n×n isalowertriangularmatrix.Thisdecom- K f = f c k f v k f b k T (10)
position strictly ensures the physical constraint of the positive where fk, fk, and fk represent the Coulomb coefficient, the
c v b
definitenessofthemassmatrixM(q).
viscous coefficient, and the friction offset of the k-th joint,
ReferencingthePINNframeworkforrobotdynamicsmodel- respectively. W f represents the friction model matrix, which
ing[12],[24]asshowninFig.1,therigidbodydynamicsmodel canbeexpandedas
oftherobotcanbesimplyexpressedas (cid:14) (cid:15) (cid:18) (cid:19) (cid:19) (cid:20)
Θ (cid:10) q, q . ,q .. (cid:11) =LLT q .. + d (cid:10) LLT (cid:11) q . W f =sign q . k · λ k (1−λ k) (cid:19) (cid:19)q . k (cid:19) (cid:19) αk
dt (cid:16) (cid:19) (cid:19) (cid:17)
−
1 (cid:2) ∂ (cid:12)
q
.TLLT
q
. (cid:13)(cid:5) T
+G (4)
λ k =exp − (cid:19) (cid:19)q . k/v s k (cid:19) (cid:19) δ s k (11)
2 ∂q
where sign(·) is the sign function. Empirical parameters vk,
s
where L and G can be computed through a Lagrangian layer δ s k, αk and friction coefficients K f are considered inherent
basedonaReLUnetwork.
Computing the partial derivatives d(LLT )/dt and ∂(q .T parametersofthePINNandareupdatedthroughtraining.
LLT q . )/∂qusingautomaticdifferentiationischallengingsince
B. Backlash-InducedDynamicsError
time t is not an input to the dynamics model. Therefore, the
followingchaindecompositionisadopted: Researchhasbeenconductedtodevelopmathematicalmodels
for backlash-induced dynamics error based on the Sigmoid
d d t (cid:10) LLT (cid:11) =L d d L t T + d d L t LT =L ∂ ∂ L q T q . + ∂ ∂ L q q . LT . (5) function[26].TheSigmoidfu (cid:16) nctionisformul (cid:17) atedas:
1 1
ζ(x)=K − (12)
Owingtothecompositionalstructureanddifferentiabilityof sig 1+e−ax 2
thenetwork,thederivativeofLwithrespecttothenetworkinput
where K represents the overall gain, and a is the parameter
iscomputableviarecursiveapplicationofthechainrule sig
that determines the similarity to the inverse dead-zone model.
∂L = ∂L ∂h N−1 ··· ∂h 1 (6) Thus,asmoot ⎧ hinversedead-zonemodelcanbedesignedas
∂q ∂h
N−1
∂h
N−2
∂q
⎨x+x +ζ(−x ) (x<−x )
1 1 1
where h i denotes the output of the ith network layer, derived ζ (cid:4) (x)= ⎩ ζ(x) (−x 1 ≤x≤x 1 ). (13)
fromanaffinetransformationsucceededbyanonlinearactiva- x−x 1 +ζ(x 1 ) (x>x 1 )
tionfunctiongi(·)
Here, x and −x are points in the Sigmoid function (12)
(cid:10) (cid:11) 1 1
h i =gi WT i h i−1 +b i (7) where the slope is 1, ensuring the smoothness of the backlash
compensation model in (13), which contains two parameters.
where W i and b i represent the network parameters of the ith After adjusting a, K sig is tuned by comparing the intercept of
layer. h i−1 is the output of the (i–1)th network layer and also thetangentlinewiththeidentifieddead-zonewidth.
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore. Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
| 4   |     |     |     |     |     |     |     | IEEE/ASMETRANSACTIONSONMECHATRONICS |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- |
Fig.2. ProposedPINN-basedmodelingandcompensationmethodforbacklash-induceddynamicserror.
III. METHODOLOGY differencesinthemagnitudeanddurationoftheerror.Therefore,
aneffectiveclassificationoferrortypescanimprovemodeling
Thissectionprovidesadetaileddescriptionoftheproposed
andcompensationeffects.
PINN-basedmodelingandcompensationapproach.Asshownin
|     |     |     |     |     | Considering |     | the | correlation | between | backlash-induced |     | dy- |
| --- | --- | --- | --- | --- | ----------- | --- | --- | ----------- | ------- | ---------------- | --- | --- |
Fig.2,afterdataacquisitionanderrorextraction,errorlabelgen-
|     |     |     |     |     | namics | error | and | robot motion | state, | the occurrence |     | of such |
| --- | --- | --- | --- | --- | ------ | ----- | --- | ------------ | ------ | -------------- | --- | ------- |
erationisconductedtoconstructanerrorclassificationdataset.
|     |     |     |     |     | errors | can | be determined | based | on  | the motion | state | criterion. |
| --- | --- | --- | --- | --- | ------ | --- | ------------- | ----- | --- | ---------- | ----- | ---------- |
Then,errordetectionandclassificationareperformedbasedon
|     |     |     |     |     | First, | the characteristic |     | factor | representing |     | the motion | state of |
| --- | --- | --- | --- | --- | ------ | ------------------ | --- | ------ | ------------ | --- | ---------- | -------- |
theTCNmodule.Finally,theproposedPINNisdesignedwith
thekthjointisdefinedasfollows:
anerrormodelbuiltonGaussianbasisfunctions.Theremainder
|     |     |     |     |     |     |          |          | (cid:24) | (cid:14) (cid:15) | (cid:14) | (cid:15) |     |
| --- | --- | --- | --- | --- | --- | -------- | -------- | -------- | ----------------- | -------- | -------- | --- |
|     |     |     |     |     |     | (cid:14) | (cid:15) |          | .                 |          | .        |     |
o f t h i s s e c ti o n w i l l e l a b o r a te o n th e d e te c t i o n a nd c l a s s ifi c at i on ·sign ≤0
|     |     |     |     |     |     | .   |     | 1, ifsign | q i |     | q i+1 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | ----- | --- |
cr it e r i a f o r b a ck l a s h - i n d u c e d d yn a m ic s e r r o r ,a s w e l l a s th e i m - (cid:7)k q i,ti = (15)
|     |     |     |     |     |     |     |     | 0,  |     | else |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
plementationofthedesignedPINNerrorcompensationmethod.
.
|     |     |     |     |     | where | ti and | q i represent |     | the time | and joint | angular | velocity |
| --- | --- | --- | --- | --- | ----- | ------ | ------------- | --- | -------- | --------- | ------- | -------- |
A. ErrorExtractionandLabelGeneration corresponding to the ith motion state sample, respectively. If
.
(cid:7)k(q
By conducting robot excitation experiments to collect real i,ti)equals1,itindicatesthatthemotiondirectionofthe
motiondata,thedynamicsandfrictionmodelsoftherobotcan k-thjointreversesattimeti.
betrained.Thejointdynamicstorqueτ
andfrictiontorque Reversalerroroccurswhenthejointmotiondirectionreverses
dyn
τ friarethencalculatedaccordingto(2)and(10),respectively. with large angular acceleration. In contrast, start-stop error
Themeasuredvalueofthetotaljointtorqueτ occurswhentherobotisjuststartingorabouttostop,typically
canbeobtained
i∈(cid:3)n×1.
by converting the joint current Therefore, the joint withsmallangularaccelerationtoensuresmoothmotion.Thus,
torqueerroroftherobotcanbeexpressedasfollows: based on angular velocity and acceleration, backlash-induced
dynamicserrorcanbeaccuratelyidentified,andtherobotstates
|     | τ =S(cid:6)i−τ |     | −τ      | (14) |                                |     |     |     |     |     |     |     |
| --- | -------------- | --- | ------- | ---- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- |
|     | err            |     | dyn fri |      | canbecategorizedintothreetypes |     |     |     |     |     |     |     |
where(cid:6)representstheHadamardproduct,andS ∈(cid:3)n×1isthe ⎧
⎨0,
|     |     |     |     |     |     | (cid:14) |     | (cid:15) |     | if (cid:7)i =0 |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | -------- | --- | -------------- | --- | --- |
j o i n t d r iv e g a in m a tr ix u se d to c o n v ertm o t o r cu r re nt s i n to m e a - . .. . .
|     |     |     |     |     |     | κi q | i,q i,ti | = 1, | if (cid:7)i | =1andq | ≥σ    | (16) |
| --- | --- | --- | --- | --- | --- | ---- | -------- | ---- | ----------- | ------ | ----- | ---- |
|     |     | τ   |     |     |     |      |          | ⎩    |             |        | . . i |      |
s u r e d t o rq u e . Th e d y na m i cs er r o r err a r i se s fr o m f a c to rs l ik e =1andq
|            |                  |       |                    |         |     |     |     | 2,  | if (cid:7)i |     | i <σ |     |
| ---------- | ---------------- | ----- | ------------------ | ------- | --- | --- | --- | --- | ----------- | --- | ---- | --- |
| mismatched | parameters [27], | joint | backlash [28], and | reducer |     |     |     |     |             |     |      |     |
ripplefriction[29].Givenitsmulticomponentcouplingnature, whereκirepresentstheerroroccurrencemarkerattimeti:when
criteriamustfirstbedesignedtoextracttheseerrorcomponents areversalerroroccurs,κiismarkedas1;whenastart-stoperror
formodelingandcompensation. occurs,κiismarkedas2.κi =0indicatesthatnoerroroccurs.
Torque errors induced by joint backlash can be categorized Each nonzero marker corresponds to an error sample. σ is the
into two types. The first type, referred to as the reversal error accelerationthreshold.
τ , occurs during direction reversals of joint motion and is However, noise in the raw data causes multiple consecutive
| Rev |     |     |     |     |     |     |     |     |     |     |     | .   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sign(q
characterized by a short duration with abrupt, high-magnitude fluctuations in joint angular velocity direction, i.e., i),
variations. The second type, the start-stop error τ , arises evenduringasinglereversalofjointmotion.Thisresultsinmul-
SS
during the initiation or termination of motion and exhibits a tipleerrormarkersbeingrecorded,eventhoughtheyallbelong
relativelylongerdurationwithsmoothervariationsinerrormag- to the same error sample. Therefore, the above classification
nitude.Thesedistinctphysicalmechanismsresultinsignificant method is insufficient to handle real robot motion state data.
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore.  Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
HUetal.:MODELINGANDCOMPENSATIONOFBACKLASH-INDUCEDDYNAMICSERRORININDUSTRIALROBOTS 5
| It is necessary |     | to introduce |     | an additional | continuity |     | criterion |     |     |     |     |     |     |     |     |
| --------------- | --- | ------------ | --- | ------------- | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
toavoidrepeatedmarkingofbacklash-induceddynamicserror.
| Taking | reversal   | error   | as an | example,       | the set | of indices | for all    |     |     |     |     |     |     |     |     |
| ------ | ---------- | ------- | ----- | -------------- | ------- | ---------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
| error  | occurrence | markers | can   | be represented |         | as an      | increasing |     |     |     |     |     |     |     |     |
sequence
|     |     | s ={i|κi | =1,i=1,2,...,N}. |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | -------- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(17)
Rev
| If there | are | adjacent | elements | in the | sequence |     | with a gap |     |     |     |     |     |     |     |     |
| -------- | --- | -------- | -------- | ------ | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
exceeding η , the set s is sliced to obtain multiple sub- Fig.3. Backlash-induceddynamicserror.
|        | Rev       |     | Rev           |     |                        |     |     |     |     |     |     |     |     |     |     |
| ------ | --------- | --- | ------------- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sets{S | ,S ,...,S |     | }.EachsubsetS |     |                        |     |     |     |     |     |     |     |     |     |     |
|        | 1 2       | m   |               |     | j correspondstomarkers |     |     |     |     |     |     |     |     |     |     |
belongingtothesameerrorsample. predicting them is essential for effective error modeling and
|     |     | {S ,S | ,...,S | }=F (s |     |     |     | compensation. |     |     |     |     |     |     |     |
| --- | --- | ----- | ------ | ------ | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
|     |     |       |        | m      | ,η  | )   |     |               |     |     |     |     |     |     |     |
1 2 Rev Rev Directlypredictingwhetherbacklash-induceddynamicserror
Sj =(cid:8)S (cid:9) willoccurinthenextmomentbasedonthecurrentrobotstate
|          |      |            |            |                    | j   |          | (18)     |                |     |             |           |             |       |              |     |
| -------- | ---- | ---------- | ---------- | ------------------ | --- | -------- | -------- | -------------- | --- | ----------- | --------- | ----------- | ----- | ------------ | --- |
|          |      |            |            |                    |     |          |          | is unreliable, |     | as the      | same      | joint state | at a  | given moment | may |
| where    | F(·) | represents | the        | slicing operation, |     | and      | η is     | a              |     |             |           |             |       |              |     |
|          |      |            |            |                    |     |          | Rev      | correspond     |     | to multiple | different | motions.    | Thus, | this article | in- |
| constant | that | can be     | determined | based              | on  | the data | sampling |                |     |             |           |             |       |              |     |
corporateshistoricalinformationofthejointmotiontoimprove
| frequency | and | the error | type. | (cid:8)·(cid:9) denotes | the | floor | operation, |     |     |     |     |     |     |     |     |
| --------- | --- | --------- | ----- | ----------------------- | --- | ----- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
thestabilityofthepredictionmodel.
toreplacethesetS
i.e.,usingSj j toavoidrepeatedmarkingof The error category label κ serves as the target output for
thesameerrorsample.Then,basedonthedurationoftheerror,
temporalprediction.Aslidingwindowoflengthlisappliedto
theerrorcategorylabelsareregenerated,andthecorresponding . ..
|     |     |     |     |     |     |     |     | processthekinematicvariablesq,q |     |     |     |     | andq ,therebygenerating |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | ----------------------- | --- | --- |
errorsignalτ
isseparated:
|     |     | Rev      |     |     |     |     |     | theinputforthetemporalpredictionmodule |     |     |         |     |         |     |     |
| --- | --- | -------- | --- | --- | --- | --- | --- | -------------------------------------- | --- | --- | ------- | --- | ------- | --- | --- |
|     |     | (cid:25) |     |     |     |     |     |                                        |     |     | (cid:3) |     | (cid:4) |     |     |
m
|     | ∀i∈ |     | B(Sj | +δ ,δ | ),  | κi =1 |     |     |     |     | X =      | Q ,...,Q |          |     |     |
| --- | --- | --- | ---- | ----- | --- | ----- | --- | --- | --- | --- | -------- | -------- | -------- | --- | --- |
|     |     | j=1 |      | Rev   | Rev |       |     |     |     |     | t        | t−l+1    | t        |     |     |
|     |     |     |      |       |     |       |     |     |     |     | (cid:12) |          | (cid:13) |     |     |
(cid:2)
|     |     |     | τ     |          |     |     |      |        |                                                  |     |          | . .. | T   |     |      |
| --- | --- | --- | ----- | -------- | --- | --- | ---- | ------ | ------------------------------------------------ | --- | -------- | ---- | --- | --- | ---- |
|     | τ   |     | err , | if κi =1 |     |     |      |        |                                                  |     | Q = qt,q | t,q  |     |     | (20) |
|     |     | =   |       | .        |     |     | (19) |        |                                                  |     | t        | t    |     |     |      |
|     | Rev |     | 0,    | else     |     |     |      |        |                                                  |     |          |      |     |     |      |
|     |     |     |       |          |     |     |      | whereQ | representstherobotstatevectorattimet,andtheinput |     |          |      |     |     |      |
t
Here,B(Sj +δ ,δ )representstheneighborhoodofthe X ∈(cid:3)3×listhecombinationofconsecutivestatevectorsovera
|             |       | Rev                                       | Rev     |            |          |     |           | t                                                       |     |     |     |     |     |     |     |
| ----------- | ----- | ----------------------------------------- | ------- | ---------- | -------- | --- | --------- | ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
| center      | Sj +δ | in                                        | the set | of natural | numbers. | The | neighbor- |                                                         |     |     |     |     |     |     |     |
|             |       | Rev                                       |         |            |          |     |           | pastdurationoflengthl.Thetemporaldependenciesintheinput |     |     |     |     |     |     |     |
| hoodradiusδ |       | characterizesthedurationofasinglereversal |         |            |          |     |           |                                                         |     |     |     |     |     |     |     |
Rev are captured using a stacked one-dimensional convolutional
errorsampleandcanbeautomaticallylearnedduringthetraining
architecturewithdilatedconvolutions.Thedilatedconvolution
| ofthePINNusedforcompensation. |     |     |     |     |     |     |     | canbedescribedas |     |     |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
Theseparationprocessforthestart-stoperrorτ
|     |     |     |     |     |     | SS  | issimilar. |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:26)k−1
Notably,althoughthebacklash-induceddynamicserrorissep-
|        |        |             |     |             |               |     |         |     | y(t)=(x∗ |     | f)(t)= |     | x(t−di)·f(i) |     |      |
| ------ | ------ | ----------- | --- | ----------- | ------------- | --- | ------- | --- | -------- | --- | ------ | --- | ------------ | --- | ---- |
|        |        |             |     |             |               |     |         |     |          |     | d      |     |              |     | (21) |
| arated | in the | time domain |     | rather than | the frequency |     | domain, |     |          |     |        |     |              |     |      |
i=0
| τ   | is  | considered | an  | acceptable | representation |     | due | to  |     |     |     |     |     |     |     |
| --- | --- | ---------- | --- | ---------- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
backlash
its significantly larger magnitude compared to other coupled where∗ isthedilatedconvolutionoperation,x∈(cid:3)n×1 isthe
d
|       |             |               |     |          |        |     |           | inputdata,f |     | ∈(cid:3)k×1denotesthedilatedconvolutionfilter,kis |     |     |     |     |     |
| ----- | ----------- | ------------- | --- | -------- | ------ | --- | --------- | ----------- | --- | ------------------------------------------------- | --- | --- | --- | --- | --- |
| error | components. | Additionally, |     | as these | errors | are | typically |             |     |                                                   |     |     |     |     |     |
time-discontinuousintypicalrobotoperatingconditionswithout thefiltersize,anddrepresentsthedilationfactor.
|     |     |     |     |     |     |     |     | The | TCN | module | consists | of stacked | one-dimensional |     | con- |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | -------- | ---------- | --------------- | --- | ---- |
noticeablevibration,time-domainprocessingismoreeffective
thanfrequencydecomposition. volutionallayerswithdifferentdilationfactorsandfiltersizes,
asshowninFig.2.Paddinglayersandcroppinglayersareused
B. TemporalPredictionandClassificationofErrors tomaintaintheconsistencyofthenumberofchannels,thereby
|     |     |     |     |     |     |     |     | enhancing | the | feature | learning | capability | [21]. | The prediction |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------- | -------- | ---------- | ----- | -------------- | --- |
Accurately predicting the occurrence of backlash-induced oferrorcategoriesκˆcanbeexpressedas
dynamics error in advance is a prerequisite for implementing (cid:10) (cid:11)
. ..
corresponding compensation in real-time robotic motion con- κˆ =TCN q,q,q . (22)
| trol. For | the | error | samples | separated | in Section |     | III-A, each |     |     |     |     |     |     |     |     |
| --------- | --- | ----- | ------- | --------- | ---------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
Whenthepredictedlabelvaluechangesfrom0toanonzero
samplehasacertainduration,asshowninFig.3,whichincludes
|            |           |     |           |                 |                  |       |           | value    | at a certain |           | moment, | it indicates | that          | backlash-induced   |           |
| ---------- | --------- | --- | --------- | --------------- | ---------------- | ----- | --------- | -------- | ------------ | --------- | ------- | ------------ | ------------- | ------------------ | --------- |
| a complete | process   |     | where the | error magnitude |                  | rises | to a peak |          |              |           |         |              |               |                    |           |
|            |           |     |           |                 |                  |       |           | dynamics | error        | will      | occur.  | Therefore,   | by predicting |                    | the error |
| and then   | decreases |     | until it  | vanishes.       | This corresponds |       | to the    |          |              |           |         |              |               |                    |           |
|            |           |     |           |                 |                  |       |           | types,   | real-time    | detection | of      | backlash     | errors        | and classification |           |
gearmeshingstatetransitioncausedbythebacklashwhenthe
oferrorcategoriesareachieved.
| motion | direction | of  | the robotic | joint | reverses. | Therefore, | it  | is  |     |     |     |     |     |     |     |
| ------ | --------- | --- | ----------- | ----- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
necessarytodetecttheoccurrenceoftheerrorattheinitialstage,
|      |               |       |      |               |     |         |           | C. ErrorModelingandCompensationBasedonPINNs |     |     |     |     |     |     |     |
| ---- | ------------- | ----- | ---- | ------------- | --- | ------- | --------- | ------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
| when | a significant | error | peak | has typically |     | not yet | appeared. |                                             |     |     |     |     |     |     |     |
Moreover,sincereversalandstart-stoperrorsarisefromdifferent For the backlash phenomenon present in joint motion, ac-
mechanismsandexhibitdistinctcharacteristics,classifyingand curately modeling the contact process of the reducer gear
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore.  Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
| 6   |     |     |     |     |     |     |     |     |     | IEEE/ASMETRANSACTIONSONMECHATRONICS |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- |
transmission is challenging. In contrast, the dynamics error In addition, backlash-induced dynamics error typically has
characteristicscausedbybacklashexhibitanobviouscorrelation higherpeakvaluesandasparsertime-domaindistributioncom-
withthejointmotionstateinthetimedomain.Therefore,model- paredtodynamicserrorcausedbyotherfactors.Thus,theloss
ingthedynamicserrorcausedbythebacklashwhileconsidering functionofthePINN-basedmodelisdefinedas
thejointmotionstateismorestraightforwardandfeasible.
(cid:26)N
Th is a r ti c le e m p lo y s G au s s i an b a s is f u n c ti on s t o fi t th e d y - 1
|     |     |     |     |     |     |     |     |     | Loss= |     | ωi(τ | −τˆ | )2  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | ---- | --- | --- | --- |
err err
nam ic se r r o r ca u se d b y t he b a c k las h , m o d e l in g in d i vi d ua l er r o r N
i=1
samples.Then,aPINNisdevelopedtoestablishthemappingre-
lationshipbetweentherobotjointmotionstateandthebacklash- ωi =(τ −τˆ )2+σ (28)
err err
| induced         | dynamics error.    | Finally, |     | combined | with   | the real-time |       |         |                                                 |     |     |     |     |     |
| --------------- | ------------------ | -------- | --- | -------- | ------ | ------------- | ----- | ------- | ----------------------------------------------- | --- | --- | --- | --- | --- |
|                 |                    |          |     |          |        |               |       | whereωi | representstheweightingcoefficientofthelossfunc- |     |     |     |     |     |
| error detection | and classification |          | in  | Section  | III-B, | online        | error |         |                                                 |     |     |     |     |     |
tion,whichemphasizestheimpactoferrorswithlargerampli-
predictionandcompensationareachieved.TheGaussianbasis
|     |     |     |     |     |     |     |     | tudes, thereby | achieving | a better | approximation |     | of backlash- |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --------- | -------- | ------------- | --- | ------------ | --- |
functionisdefinedasfollows:
induceddynamicserror.σ
|     |     |     | (cid:27) |     | (cid:28) |     |     |     |     | denotesapositiveconstantcloseto |     |     |     |     |
| --- | --- | --- | -------- | --- | -------- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- |
(t− b j)2 z er o , in troducedtopreventcomputationalerrorswhentheerror
|     | Φj(t)=aj |     | ·exp | −   | .   |     | (23) |             |     |     |     |     |     |     |
| --- | -------- | --- | ---- | --- | --- | --- | ---- | ----------- | --- | --- | --- | --- | --- | --- |
|     |          |     |      |     |     |     |      | is z e ro . |     |     |     |     |     |     |
|     |          |     |      | cj  | 2   |     |      |             |     |     |     |     |     |     |
Foreachtimestepduringroboticcontroltaskexecution,the
Here,aj,bj,andcjareparametersthatdeterminetheshapeof occurrence of backlash-induced dynamics error is predicted
usinghistoricalinformationfromtheprecedingltimesteps.The
theGaussianbasisfunction,whichareupdatedthroughlearning
toensureaccuratefittingoftheerror.Sincethelengthofasingle proposed method predicts the parameters of the error model
error sample in the time domain is finite, the Gaussian basis throughthePINNratherthandirectlypredictingtheerrorval-
functioncanbemodifiedbasedon(19)as ues. This effectively simplifies the complexity of the mapping
|     |     |     |     |     |     |     |     | relationship, | making | the proposed | error | compensation | method |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | ------ | ------------ | ----- | ------------ | ------ | --- |
t∈B(Sj
| Φj(Sj,δRev)=Φj(t), |     |      |            | +δ  | ,δ            | )   | (24)   | morerobustandeasiertolearn. |     |     |     |     |     |     |
| ------------------ | --- | ---- | ---------- | --- | ------------- | --- | ------ | --------------------------- | --- | --- | --- | --- | --- | --- |
|                    |     |      |            |     | Rev           | Rev |        |                             |     |     |     |     |     |     |
| where B(Sj         | +δ  | ,δ ) | represents | the | time interval |     | during |                             |     |     |     |     |     |     |
Rev Rev
whichtheerrorpersists,i.e.,thejthconsecutiveintervalwhen IV. EXPERIMENTS
theerrorcategorylabelκisnonzero. Theproposedmethodisexperimentallyvalidatedontwodif-
TheproposedPINN-basederrormodelingandcompensation
ferent6-DOFserialindustrialrobots:theSIASUNSN7Brobot
methodisshowninFig.2.First,amultilayerperceptron(MLP) and the ROKAE XB7S robot. The proposed error prediction
module is utilized to learn the mapping relationship between andcompensationmodelisfirsttrainedandsavedusingPython
therobotmotionstateandtheparametersoftheGaussianbasis
withPyTorch,thencompiledandintegratedintotheMATLAB
functions Simulink-based robot control framework. Upon detection of
|     | (cid:14) | (cid:15) |     | (cid:14) | (cid:15) |     |     |     |     |     |     |     |     |     |
| --- | -------- | -------- | --- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
..
aˆj,ˆbj,cˆj q,q,κ;ϑ backlash-induced dynamics error, the proposed compensation
|     |     |     | =MLP |     | .   |     | (25) |                  |              |                  |         |             |             |     |
| --- | --- | --- | ---- | --- | --- | --- | ---- | ---------------- | ------------ | ---------------- | ------- | ----------- | ----------- | --- |
|     |     |     |      |     |     |     |      | module           | corrects the | inverse dynamics |         | estimation. | A Beckhoff  |     |
|     |     |     |      |     |     |     |      | C6930 industrial | computer     | is               | used as | the main    | controller, | as  |
ThepredictedvaluesoftheGaussianbasisfunctionparame-
tersaredenotedasaˆj,ˆbj,andcˆj.Thejointangleqandangular showninFig.4,performing real-timecontrolanddataacquisi-
|               | ..                                      |     |     |     |     |     |     | tionatafrequencyof1kHzviatheEtherCATbuswiththerobot. |          |          |          |           |             |     |
| ------------- | --------------------------------------- | --- | --- | --- | --- | --- | --- | ---------------------------------------------------- | -------- | -------- | -------- | --------- | ----------- | --- |
| accelerationq | areusedasinputstothemodel.Thejointangle |     |     |     |     |     |     |                                                      |          |          |          |           |             |     |
|               |                                         |     |     |     |     |     |     | Benefiting                                           | from the | openness | and high | real-time | performance |     |
hasasignificantimpactonthetemporaloffsetoftheerror,while
oftheBeckhoffplatform,themodifieddynamicsmodelcanbe
theangularaccelerationprimarilyaffectsthepeakvalueofthe
deployedinactualrobotcontrolscenariosthroughtheBeckhoff
error.Thisisconsistentwiththephysicalcharacteristicsofthe
TE1400module.
contactprocessingearbacklash.Thelabelκrepresentstheerror
| type. Different | types | of errors | with | distinct | characteristics |     | are |     |     |     |     |     |     |     |
| --------------- | ----- | --------- | ---- | -------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
A. DatasetConstructionofBacklash-InducedDynamics
learnedusingseparateMLPbranches.Thenetworkparameters,
| representedbyϑ,areupdatedduringthemodeltrainingprocess. |     |     |     |     |     |     |     | Error |     |     |     |     |     |     |
| ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
Therefore,thepredictionofasinglereversalerrorsamplecan
|     |     |     |     |     |     |     |     | Periodic | reciprocating | motion | is commonly |     | used as the | test |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------------- | ------ | ----------- | --- | ----------- | ---- |
beexpressedas(26).Thepredictionforstart-stoperrorissimilar trajectory to analyze the backlash dynamics behavior of robot
butusesadifferentMLPbranch
joints[7].However,itscoveredmotionstatesarelimited,making
|            | (cid:14)      |     | (cid:15) |     |     |       |      |              |                  |     |              |         |           |     |
| ---------- | ------------- | --- | -------- | --- | --- | ----- | ---- | ------------ | ---------------- | --- | ------------ | ------- | --------- | --- |
|            |               |     |          |     |     |       |      | it difficult | to fully capture | the | relationship | between | backlash- |     |
| Φˆ j(t)=Φj | t,aˆj,ˆbj,cˆj |     | , t∈B(Sj |     | +δ  | ,δ ). | (26) |              |                  |     |              |         |           |     |
|            |               |     |          |     | Rev | Rev   |      |              |                  |     |              |         |           |     |
induceddynamicserrorandjointmotionstates.
|          |               |        |     |                  |     |          |     | On the   | other hand,  | the fifth-order | Fourier  |     | series trajectory |     |
| -------- | ------------- | ------ | --- | ---------------- | --- | -------- | --- | -------- | ------------ | --------------- | -------- | --- | ----------------- | --- |
| Finally, | the predicted | values | of  | backlash-induced |     | dynamics |     |          |              |                 |          |     |                   |     |
|          |               |        |     |                  |     |          |     | exhibits | more complex | motion          | behavior | and | is widely used    | as  |
erroroveraperiodofmotioncanbeobtainedas
|     |     |     |     |     |     |     |     | the excitation | trajectory | in dynamics | parameter |     | identification. |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | ---------- | ----------- | --------- | --- | --------------- | --- |
(cid:29)(cid:4)
τˆ =Σ m Φˆ j(t)+Σ m (cid:4) Φ j(t) (27) After optimization, this trajectory can cover most of the robot
|     | err | j=i |     | j=  | i   |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
workspace[30],therebypresentingcomprehensivejointmotion
(cid:29)(cid:4)
whereΦ j(t)representsthepredictionofthejthstart-stoperror characteristics.Therefore,asshowninFig.4(b),thefollowing
sample. test trajectories are adopted as the actual robot motions for
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore.  Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
HUetal.:MODELINGANDCOMPENSATIONOFBACKLASH-INDUCEDDYNAMICSERRORININDUSTRIALROBOTS 7
|     |     |     | the joint  | torque | error    | can be   | calculated | by        | (14).     | Then, error |
| --- | --- | --- | ---------- | ------ | -------- | -------- | ---------- | --------- | --------- | ----------- |
|     |     |     | separation | and    | category | labeling | are        | performed | according | to          |
SectionIII-Ausingtheunfilteredrawtorquesignalstopreserve
theoriginalbacklashtransients,producingthebacklash-induced
dynamicserrordataset.Theoriginaldatasetissharedin[32].
|     |     |     | At the | trajectory | level, | the | dataset | is randomly | divided | into |
| --- | --- | --- | ------ | ---------- | ------ | --- | ------- | ----------- | ------- | ---- |
training,validation,andtestsubsets,withproportionsof60%,
|     |     |     | 20%, and  | 20%,    | respectively, |              | ensuring  | that         | joint      | motions in |
| --- | --- | --- | --------- | ------- | ------------- | ------------ | --------- | ------------ | ---------- | ---------- |
|     |     |     | different | subsets | belong        | to different |           | trajectories | to         | avoid data |
|     |     |     | leakage.  | Then,   | a sliding     | window       | operation |              | is applied | to the     |
dataset,takingthejointmotionstateatagivenmomentasinput
|     |     |     | and the      | corresponding |     | error occurrence |     | category | as  | the label,  |
| --- | --- | --- | ------------ | ------------- | --- | ---------------- | --- | -------- | --- | ----------- |
|     |     |     | to construct | a time-series |     | classification   |     | dataset  | for | the robot’s |
backlash-induceddynamicserror.
B. ErrorClassificationandLocalizationResults
|     |     |     | After | constructing |     | the error | classification |     | dataset, | the de- |
| --- | --- | --- | ----- | ------------ | --- | --------- | -------------- | --- | -------- | ------- |
signedTCNmoduleisusedtopredictwhetheranerroroccurs
Fig.4. Robotexperimentplatform.(a)Robotexcitationtrajectories.(b)
|     |     |     | and determine |     | the error | category | based | on  | historical | motion |
| --- | --- | --- | ------------- | --- | --------- | -------- | ----- | --- | ---------- | ------ |
SIASUNSN7Brobot.(c)ROKAEXB7Srobot.(d)Robotcontrolsystem.
information.TheTCNmoduleconsistsoffourlayers,eachwith
twoconvolutionalhiddenlayersof25neuronsandwithdilation
factorssetto[1],[2],[4],[8]toprogressivelyextracthistorical
|     |     |     | features | from the | data. | Finally, | a fully | connected     |     | layer and a |
| --- | --- | --- | -------- | -------- | ----- | -------- | ------- | ------------- | --- | ----------- |
|     |     |     | Softmax  | function | are   | used to  | output  | the predicted |     | labels. The |
cross-entropylossfunctionisusedastheobjectivefunctionand
adaptivemomentestimation(Adam)isselectedastheoptimizer.
|     |     |     | Without | loss | of generality, |     | Fig. | 5 shows | the time-domain |     |
| --- | --- | --- | ------- | ---- | -------------- | --- | ---- | ------- | --------------- | --- |
distributionofbacklash-induceddynamicserror,alongsidepre-
|     |     |     | dictions | of error | categories | by  | the | designed | TCN | module. A |
| --- | --- | --- | -------- | -------- | ---------- | --- | --- | -------- | --- | --------- |
transitionfromzerotoanonzerovalueintheerrorlabelsignifies
theonsetoferrorscausedbybacklash.Thedottedlinerepresents
|     |     |     | the error | category | label | values | determined |     | based on | the robot |
| --- | --- | --- | --------- | -------- | ----- | ------ | ---------- | --- | -------- | --------- |
motionstate,whilethedashedlinerepresentspredictions.Fig.5
indicatesthatthedurationofactualerrorsisfullyencompassed
withinthepredictedinterval,coveringtheerrorpeakanditsrise
andfallphases.Inaddition,thetwolabeledlinesarecloseinthe
Fig.5. Temporalerrorlocalizationandclassification.
timedomain,withthedashedoneevenexhibitinganearliercat-
|     |     |     | egory transition, |     | indicating | that | the | predicted | error | occurrence |
| --- | --- | --- | ----------------- | --- | ---------- | ---- | --- | --------- | ----- | ---------- |
startsearlierthanthelabeledvalue.Thisresultindicatesthatthe
constructingthedynamicserrordataset
proposedmethodcaneffectivelyachieveearlyerrorprediction,
| (cid:16) |     | (cid:17) |     |     |     |     |     |     |     |     |
| -------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:26)5 makingreal-timeerrorcompensationpossible.
|              | a i,k      | b i,k     |     |     |     |     |     |     |     |     |
| ------------ | ---------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
| qi(t)=qi,0 + | sin(kωft)− | cos(kωft) |     |     |     |     |     |     |     |     |
|              | k ω        | k ω       |     |     |     |     |     |     |     |     |
|              | f          | f         |     |     |     |     |     |     |     |     |
k=1 C. VerificationofErrorCompensationBasedonPINNs
(29)
where t is time, ωf the base frequency, ai,k and bi,k the kth Afterobtainingthestartingoccurrencepositionsoftherobot’s
order coefficients for the ith joint, and qi,0 the initial position. backlash-induced dynamics error through the temporal pre-
Thefundamentalfrequencyistypicallysetto0.1Hz,andthetra- diction module, the PINN error prediction method based on
jectorycoefficientsarecalculatedusinganiterativeoptimization Gaussian basis functions, designed in Section III-C, is used
technique[31]. forcompensation.ThedesignedPINNincorporatestwoparallel
Datafrom12differentexcitationtrajectories,includingjoint branchestohandledistincterrortypesandeachbranchconsists
angles,angularvelocities,andjointcurrents,arecollected,with of three fully connected layers with neuron configurations set
eachtrajectorylasting10s.Afifth-orderButterworthlow-pass as [2, 64, 64, 3]. The prediction and compensation results of
filter with a cutoff frequency of 50 Hz is applied bidirection- the proposed method on the backlash-induced dynamics error
ally to the raw data to eliminate high-frequency noise for the of two robots are shown in Fig. 6, illustrating typical error
subsequent dynamics and friction modeling. The joint angular patterns across all joints on the same time scale. The results
accelerationisobtainedbydifferentiatingtheangularvelocity. showthattheproposedmethodeffectivelysuppressestheimpact
After completing the robot dynamics and friction modeling, of backlash-induced dynamics error on the robot dynamics.
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore.  Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
8 IEEE/ASMETRANSACTIONSONMECHATRONICS
Fig.6. Backlash-induceddynamicserrorcompensationresults.(a)SIASUNSN7Brobot.(b)ROKAEXB7Srobot.
TABLEI
COMPARISONOFERRORMODELINGMETHODS
The compensation performance remains stable even for non-
Gaussian backlash-induced errors, indicating that the method
doesnotrelyonastrictGaussiandistributionassumption.
Fig.7. Comparisonexperimentresults.(a)Overallcomparisonofer-
ror compensation effects. (b) Local interval with error spike. (c) Local
D. PerformanceEvaluationandComparison
intervalwithouterrorspikes.
Comparativeexperimentsareconductedtoevaluatetheper-
formance of the proposed method. Table I gives detailed in- structuralsimplicity,butdoesnottakethehistoricalinformation
formation on the advanced existing methods for robot error of joint motion states into account, which affects its accuracy
compensationandthetechniquestheyemploy.Thesettingsof inpredictingabruptbacklash-inducederrors.Methods3–5use
themainhyperparametersforotherlearning-basedmethodsand different techniques to learn the potential error characteristics
theproposedmethodarethesame.TheAdamoptimizerisused, fromhistoricalinformation,improvingerrorcompensationper-
with the learning rate set to 1e−03 and the batch size set to formance.Theproposedmethodlearnsthepotentialcorrelation
512.Thelossfunctionisdefinedas(28).Theinputsforvarious between historical information and error occurrence through
methods include joint angles, angular velocities, and angular a temporal prediction module. It employs the PINN method
accelerations, while the proposed method only requires joint embeddedwithaGaussianbasisfunction-basedmodelforcom-
anglesandangularaccelerations. pensation.Experimentalresultsontworobotsdemonstrateav-
Thedetailedresultsofthecompensationperformanceevalu- eragejointerrorreductionsof45.93%and34.19%,respectively,
ationandcomparisonwithothermethodsacrossallrobotjoints outperformingotheradvancedcomparativemethods.
aregiveninTableII.Therootmeansquarederror(RMSE)[33] Fig.7providesacomparativevisualizationoftheprediction
is selected as the metric to evaluate the effectiveness of error resultsforbacklash-induceddynamicserrorusingvariousmeth-
compensation.Allmethodsaretrainedmultipletimestoobtain ods,takingjoint4asanexample.AsillustratedinFig.7(b),both
theaveragecompensationresults.Method1adoptsatraditional theproposedmethodandmethod5effectivelycompensatefor
errorcompensationmodelbasedonaSigmoidfunction,relying abrupt backlash-induced dynamics error, outperforming other
on accurate prior values of model parameters. Method 2 has methodswithsmallerresidualerrors.
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore. Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
HUetal.:MODELINGANDCOMPENSATIONOFBACKLASH-INDUCEDDYNAMICSERRORININDUSTRIALROBOTS 9
TABLEII
ERRORCOMPENSATIONPERFORMANCECOMPARISONWITHOTHERMETHODSEVALUATEDBYRMSE(N·M)
TABLEIII
COMPARISONOFMODELTRAININGANDINFERENCETIME
Fig.7(c)magnifiesasegmentwithoutabrupterrorchanges,
Fig.8. Loadgeneralizationexperimentplatform.
where the comparative methods exhibit unexpected error pre-
dictions,resultinginlargerresidualerrorsaftercompensation.
Incontrast,theproposedmethodaccuratelydeterminesthatno
E. DiscussiononGeneralization
erroroccurs.This isbecause theproposed approach combines
temporal localization with PINN-based compensation, where Loadgeneralizationexperimentsareconductedtoinvestigate
errorlocalizationisdirectlydeterminedfromtherobot’shistor- theimpactofdifferentpayloadsonbacklash.Theplatformfor
icalmotion.Moreover,theGaussianbasisfunction-basederror the experiments is shown in Fig. 8, where the payload at the
model provides strict physical constraints for the PINN-based end-effectorissettofiveconditions:0kg;1kg;3kg;5kg;and
compensationmodule,furtherensuringthesuperiorrobustness 7kg,coveringtherobot’sratedpayloadrange.
oftheproposedmethod. Keeping all other conditions constant, including the same
An evaluation of the time costs is also conducted. Table III motion path and speed, error compensation experiments are
comparesthetrainingtimeandinferencetimeoftheproposed carried out for each case. Fig. 9(a) and (b) presents measured
methodwithotherlearning-basedmethods.Trainingtimerefers jointtorquevaluesanderrorcompensationresults,respectively,
totheaveragedurationrequiredforthenetworkmodeltocon- underdifferentpayloadconditions.Amongthese,joints1,4,and
vergewhentrainedonthesamecomputerequippedwithasingle 6 only experience inertial torque due to their inherent rotation
NVIDIARTX4060GPU(16GB).Inferencetimereferstothe orientation,showingminimalvariationintorquewithchanging
average duration required for the trained model to predict the end-effector payloads. In contrast, joints 2, 3, and 5 bear the
error at a single time point on the same Beckhoff controller dominant portion of gravitational torque induced by payloads.
equippedwithanIntelCorei7-7700CPU(16GB). Consequently, payload variations directly induce correspond-
Byseparatingthetemporallocalizationoferrorsfrommodel- ing torque changes. The resulting torque errors belong to the
basederrorcompensation,theproposedPINNmodelbasedon modeled dynamics components and can typically be resolved
Gaussian basis functions only needs to learn the relationship throughgravitycompensationtechniques[34].
betweenthemodelparametersandmotionstates.Thissimpler, Notably, the backlash-induced dynamics error with abrupt
robustmappingsignificantlyreducesthetimerequiredformodel characteristicsdemonstratesconsistentbehavioracrossalltested
trainingandimprovesinferencespeed.Duetothis,theproposed payload conditions, exhibiting similar magnitudes of abrupt
method achieves an inference time of 6.69e−07 s per sample, changes and durations. This indicates that changes in end-
superiortoothermethods. effector payload have little impact on backlash-induced errors
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore. Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
| 10  |     |     |     |     |     |     |     |     | IEEE/ASMETRANSACTIONSONMECHATRONICS |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- |
Fig.9. Loadgeneralizationexperimentresults.(a)Measuredjointtorques.(b)Errorcompensationresults.
|     |     |     |     |     |     |     | Fig. | 11. Evaluation | of the generalization |     | experiment |     | by the average |
| --- | --- | --- | --- | --- | --- | --- | ---- | -------------- | --------------------- | --- | ---------- | --- | -------------- |
RMSEacrossalljoints.
|     |     |     |     |     |     |     | predictions |     | at high speed (1000 | Hz) | and | low speed | (500 Hz) |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------------------- | --- | --- | --------- | -------- |
respectively,whileFig.10(c)and(d)presentsthecorresponding
Fig.10. Speedgeneralizationexperimentresults.(a)Jointtorquepre-
|                 |         |        |                  |            |         |        | error | compensation | results.         | At low    | speed,    | the error | amplitude    |
| --------------- | ------- | ------ | ---------------- | ---------- | ------- | ------ | ----- | ------------ | ---------------- | --------- | --------- | --------- | ------------ |
| diction results | at fast | speed. | (b) Joint torque | prediction | results | at low |       |              |                  |           |           |           |              |
|                 |         |        |                  |            |         |        | is    | reduced      | while exhibiting | prolonged | duration. |           | The proposed |
speed.(c)Errorcompensationresultsatfastspeed.(d)Errorcompen-
sationresultsatlowspeed. method learns the correlation between joint motion state and
|     |     |     |     |     |     |     | backlash-induced |     | dynamics | error, | maintaining | effective | com- |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | -------- | ------ | ----------- | --------- | ---- |
pensationacrossdifferentspeeds.
Theloadandspeedgeneralizationexperimentsforthecom-
underthesamemotionstate,enablingtheproposedmethodto
|     |     |     |     |     |     |     | pensation |     | of backlash-induced | errors | are | quantified | using the |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------------------- | ------ | --- | ---------- | --------- |
handlevariouspayloadconditionseffectively.
averageRMSEacrossalljoints,asshowninFig.11.Theresults
| The speed | generalization |     | ability is | also | explored | to further |     |     |     |     |     |     |     |
| --------- | -------------- | --- | ---------- | ---- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
demonstratethatbacklash-induceddynamicserrorisprimarily
| demonstrate   | the          | proposed | method’s                  | robustness. | The             | perfor-  |            |              |                      |         |            |      |             |
| ------------- | ------------ | -------- | ------------------------- | ----------- | --------------- | -------- | ---------- | ------------ | -------------------- | ------- | ---------- | ---- | ----------- |
|               |              |          |                           |             |                 |          | influenced |              | by the motion state, | showing | negligible |      | correlation |
| mance of      | the proposed |          | method is cross-validated |             | on              | multiple |            |              |                      |         |            |      |             |
|               |              |          |                           |             |                 |          | with       | end-effector | payloads.            | This is | consistent | with | impact dy-  |
| trajectories, | as           | shown    | in (29), demonstrating    |             | its applicabil- |          |            |              |                      |         |            |      |             |
t+
ity to different joint motion states, as the trajectories include namics,wherethereengagementimpulsesatisfies ∫ τ(t)dt=
t−
| sufficient | frequency | components | that | excite | various | dynamic |     | .           |     |     |     |     |     |
| ---------- | --------- | ---------- | ---- | ------ | ------- | ------- | --- | ----------- | --- | --- | --- | --- | --- |
|            |           |            |      |        |         |         | J   | Δθ,inwhichJ |     |     |     |     |     |
characteristicsofthesystem.Additionally,testsareconducted eq eq denotesthejoint-sideequivalentinertia
toexecuteidenticalmotionpathsatvaryingspeedsbyadjusting of the drive chain (approximately constant within the tested
.
Δθ
therobot’scontrolfrequency.Fig.10showsthespeedgeneral- payload range) and is the change in angular velocity at
ization results, with Fig. 10(a) and (b) displaying joint torque theinstantofreengagement,suggestingthattheimpactseverity
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore.  Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
HUetal.:MODELINGANDCOMPENSATIONOFBACKLASH-INDUCEDDYNAMICSERRORININDUSTRIALROBOTS 11
| is governed | primarily | by the | relative | velocity | at contact | rather |                 |     |              |          |                   |          |     |
| ----------- | --------- | ------ | -------- | -------- | ---------- | ------ | --------------- | --- | ------------ | -------- | ----------------- | -------- | --- |
|             |           |        |          |          |            |        | [8] C. D. Sousa | and | R. Cortesão, | “Inertia | tensor properties | in robot | dy- |
namicsidentification:Alinearmatrixinequalityapproach,”IEEE/ASME
thanbythesteadyloadlevel.
|          |             |     |                             |     |     |       | Trans. | Mechatron., | vol. | 24, no. 1, | pp.406–411, | Feb. 2019, | doi: |
| -------- | ----------- | --- | --------------------------- | --- | --- | ----- | ------ | ----------- | ---- | ---------- | ----------- | ---------- | ---- |
| Theabove | experiments |     | demonstratetheeffectiveness |     |     | ofthe |        |             |      |            |             |            |      |
10.1109/TMECH.2019.2891177.
proposedmethodundervariousconditions.However,accurate [9] Y.Han,J.Wu,C.Liu,andZ.Xiong,“Aniterativeapproachforaccuratedy-
dynamicsandfrictionmodelingremainsessentialforreliableer- namicmodelidentificationofindustrialrobots,”IEEETrans.Robot.,vol.
36,no.5,pp.1577–1594,Oct.2020,doi:10.1109/TRO.2020.2990368.
rorpredictionandcompensation.Additionally,forrobotmotions
|     |     |     |     |     |     |     | [10] H. Lee, | “Physics-based | cooperative | robotic | digital | twin framework | for |
| --- | --- | --- | --- | --- | --- | --- | ------------ | -------------- | ----------- | ------- | ------- | -------------- | --- |
without trajectory smoothing treatment, nonzero acceleration contactlessdeliverymotionplanning,”Int.J.Adv.Manuf.Technol.,vol.
during initiation/termination phases can adversely affect the 128,no.3,pp.1255–1270,Sep.2023,doi:10.1007/s00170-023-11956-3.
accuracyofmotionstatecriterionasin(16). [11] X.Yang,Z.Zhou,L.Li,andX.Zhang,“Collaborativerobotdynamics
withphysicalhuman-robotinteractionandparameteridentificationwith
Essentially,theproposedmethodconstructsageneralback- PINN,”Mech.Mach.Theory,vol.189,Nov.2023,Art.no.105439,doi:
lash error model based on Gaussian basis functions, provid- 10.1016/j.mechmachtheory.2023.105439.
|                   |     |          |        |              |      |          | [12] M.LutterandC.Ritter,andJ.Peters,“DeepLagrangiannetworks:Using |          |           |                 |          |            |        |
| ----------------- | --- | -------- | ------ | ------------ | ---- | -------- | ------------------------------------------------------------------ | -------- | --------- | --------------- | -------- | ---------- | ------ |
| ing the necessary |     | physical | priors | for the PINN | used | in error |                                                                    |          |           |                 |          |            |        |
|                   |     |          |        |              |      |          | physics                                                            | as model | prior for | deep learning,” | in Proc. | Int. Conf. | Learn. |
compensation, thereby enabling interpretable error prediction. Represent.,May2019,pp.1–17.
Moreover, by establishing a direct mapping between backlash [13] M.Lahoud,G.Marchello,M.D’Imperio,A.Müller,andF.Cannella,“A
deeplearningframeworkfornon-symmetricalCoulombfrictionidenti-
androbotmotionstates,theproposedmethodachievesasimpler
ficationofroboticmanipulators,”inProc.IEEEInt.Conf.Rob.Autom.,
errornetworkstructure,whichfurtherensurestherobustnessof
May2024,pp.10510–10516.
|     |     |     |     |     |     |     | [14] R.Guidaetal.,“Simulationoftheeffectsofbacklashontheperformance |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
theproposedapproach.
ofacollaborativerobot:Apreliminarycasestudy,”inProc.Int.Conf.
Robot.Alpe-Adria-DanubeRegion,Jun.2022,pp.28–35.
|     |     |     |     |     |     |     | [15] M.Nordin,J.Galic’,andP.-O.Gutman,“Newmodelsforbacklashand |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
V. CONCLUSION gearplay,”Int.J.Adapt.ControlSignalProcess.,vol.11,no.1,pp.49–63,
Feb.1997,doi:10.1002/(SICI)1099-1115(199702)11:1.
This article adopts a PINN-based error modeling and com- [16] D.Coble,L.Cao,A.R.Downey,andJ.M.Ricles,“Physics-informed
pensationapproachtoaddressthebacklashinmultijointserial machine learning for dry friction and backlash modeling in structural
controlsystems,”Mech.Syst.SignalProcess.,vol.218,Sep.2024,Art.
robots. A Gaussian basis function-based backlash error model no.111522,doi:10.1016/j.ymssp.2024.111522.
is proposed, enabling online compensation through temporal [17] M. Ruderman, F. Hoffmann, and T. Bertram, “Modeling and iden-
detectionandclassificationoferrors.Experimentsdemonstrate tification of elastic robot joints with hysteresis and backlash,” IEEE
|     |     |     |     |     |     |     | Trans. Ind. | Electron., | vol. | 56, no. 10, | pp.3840–3847, | Oct. 2009, | doi: |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ---------- | ---- | ----------- | ------------- | ---------- | ---- |
thattheproposedmethodoutperformsotheradvancedmethods
10.1109/TIE.2009.2015752.
inerrorcompensationperformanceandsignificantlydecreases [18] X.Yangetal.,“Continuousfrictionfeedforwardslidingmodecontroller
foraTriMulehybridrobot,”IEEE/ASMETrans.Mechatronics.,vol.23,
| inference costs. | Furthermore, |     | the | generalization | performance |     |     |     |     |     |     |     |     |
| ---------------- | ------------ | --- | --- | -------------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
no.4,pp.1673–1683,Aug.2018,doi:10.1109/TMECH.2018.2853764.
| of the proposed | method | is  | also | discussed. Future | work | could |                                                                 |     |     |     |     |     |     |
| --------------- | ------ | --- | ---- | ----------------- | ---- | ----- | --------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
|                 |        |     |      |                   |      |       | [19] R.Zhang,Z.Wang,N.Bailey,andP.Keogh,“Experimentalassessment |     |     |     |     |     |     |
furtherinvestigateothererrorsourcesandextendthebacklash
andfeedforwardcontrolofbacklashandstictioninindustrialserialrobots
forlow-speedoperations,”Int.J.Comput.Integr.Manuf.,vol.36,no.3,
compensationapproachtokinematicapplications.Additionally,
pp.393–410,Mar.2023,doi:10.1080/0951192X.2022.2090609.
| combining | the temporal | detection |     | of error | with model-based |     |                                                                         |     |     |     |     |     |     |
| --------- | ------------ | --------- | --- | -------- | ---------------- | --- | ----------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
|           |              |           |     |          |                  |     | [20] J.Hanetal.,“Anovelmulti-pulsefrictioncompensationstrategyforhybrid |     |     |     |     |     |     |
errorpredictiontoachieveend-to-endcompensationisanother robots,”Mech.Mach.Theory,vol.201,Oct.2024,Art.no.105726,doi:
| promisingdirection. |     |     |     |     |     |     | 10.1016/j.mechmachtheory.2024.105726.                         |     |     |     |     |     |     |
| ------------------- | --- | --- | --- | --- | --- | --- | ------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
|                     |     |     |     |     |     |     | [21] S.Tan,J.Yang,andH.Ding,“Apredictionandcompensationmethod |     |     |     |     |     |     |
ofrobottrackingerrorconsideringpose-dependentloaddecomposition,”
Robot.Comput.Integr.Manuf.,vol.80,Apr.2023,Art.no.102476,doi:
|     |     | REFERENCES |     |     |     |     | 10.1016/j.rcim.2022.102476.                                            |     |     |     |     |     |     |
| --- | --- | ---------- | --- | --- | --- | --- | ---------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
|     |     |            |     |     |     |     | [22] T.-C.ÇallarandS.Böttger,“Hybridlearningoftime-seriesinversedynam- |     |     |     |     |     |     |
[1] S. Ahmad, H. Zhang, and G. Liu, “Multiple working mode control icsmodelsforlocallyisotropicrobotmotion,”IEEERobot.Autom.Lett.,
of door-opening with a mobile modular and reconfigurable robot,” vol.8,no.2,pp.1061–1068,Feb.2023,doi:10.1109/LRA.2022.3222951.
IEEE/ASMETrans.Mechatron.,vol.18,no.3,pp.833–844,Jun.2013, [23] S.Liu,L.Wang,andX.V.Wang,“Sensorlessforceestimationforin-
doi:10.1109/TMECH.2012.2191301. dustrialrobotsusingdisturbanceobserverandneurallearningoffriction
approximation,”Robot.Comput.Integr.Manuf.,vol.71,Oct.2021,Art.
[2] T.Gold,A.Völz,andK.Graichen,“Modelpredictivepositionandforce
trajectory tracking control for robot-environment interaction,” in Proc. no.102168,doi:10.1016/j.rcim.2021.102168.
IEEEInt.Conf.Intell.Robot.Syst.,Oct.2020,pp.7397–7402. [24] H.Hu,Z.Shen,andC.Zhuang,“APINN-basedfriction-inclusivedynam-
[3] E. Spyrakos-Papastavridis and J. S. Dai, “Minimally model-based tra- icsmodelingmethodforindustrialrobots,”IEEETrans.Ind.Electron.,vol.
jectorytrackingandvariableimpedancecontrolofflexible-jointrobots,” 72,no.5,pp.5136–5144,May2025,doi:10.1109/TIE.2024.3476977.
IEEETrans.Ind.Electron.,vol.68,no.7,pp.6031–6041,Jul.2021,doi: [25] N.KammererandP.Garrec,“Dryfrictionmodelingindynamicidenti-
10.1109/TIE.2020.2994886. ficationforrobotmanipulators:Theoryandexperiments,”inProc.IEEE
[4] W.He,C.Xue,X.Yu,Z.Li,andC.Yang,“Admittance-basedcontroller Int.Conf.Mechatron.,Feb.2013,pp.422–429.
designforphysicalhuman–robotinteractionintheconstrainedtaskspace,” [26] S.YamadaandH.Fujimoto,“Precisejointtorquecontrolmethodfortwo-
IEEETrans.Autom.Sci.Eng.,vol.17,no.4,pp.1937–1949,Oct.2020, inertiasystemwithbacklashusingload-sideencoder,”IEEJJ.Ind.Appl.,
doi:10.1109/TASE.2020.2983225. vol.8,no.1,pp.75–83,Mar.2019,doi:10.1541/ieejjia.8.75.
[5] J. Hu and R. Xiong, “Contact force estimation for robot manipula- [27] F. Khadivar, K. Chatzilygeroudis, and A. Billard, “Self-correcting
tor using semiparametric model and disturbance Kalman filter,” IEEE quadratic programming-based robot control,” IEEE Trans. Syst. Man
Trans. Ind. Electron., vol. 65, no. 4, pp.3365–3375, Apr. 2018, doi: Cybern. Syst., vol. 53, no. 8, pp.5236–5247, Aug. 2023, doi:
| 10.1109/TIE.2017.2748056. |     |     |     |     |     |     | 10.1109/TSMC.2023.3262954. |     |     |     |     |     |     |
| ------------------------- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- |
[6] C. Zhuang, Y. Yao, Y. Shen, and Z. Xiong, “A convolution neural [28] K.Li,Y.Tsai,andK.Chan,“Identifyingjointclearanceviarobotmanip-
network based semi-parametric dynamic model for industrial robot,” ulation,”J.Mech.Eng.Sci.,vol.232,no.15,pp.2549–2574,Aug.2018,
J. Mech. Eng. Sci., vol. 236, no. 7, pp.3683–3700, Apr. 2022, doi: doi:10.1177/0954406217721940.
10.1177/09544062211039875. [29] Y.S.Lu,S.M.Lin,M.Hauschild,andG.Hirzinger,“Atorque-ripple
[7] K.Ali,B.Fabian,andV.Alexander,“Measurabilityofthedynamicbehav- compensationschemeforharmonicdrivesystems,”Elect.Eng.,vol.95,
iorofgearbacklashatindustrialrobots,”inProc.Int.Conf.Mechatron. no.4,pp.357–365,Dec.2013,doi:10.1007/s00202-012-0264-4.
Mach.Vis.Pract.,Nov.2018,pp.1–6.
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore.  Restrictions apply.

This article has been accepted for inclusion in a future issue of this journal. Content is final as presented, with the exception of pagination.
| 12  |     |     |     |     |     |     |     | IEEE/ASMETRANSACTIONSONMECHATRONICS |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- |
[30] K.-J.Park,“Fourier-basedoptimalexcitationtrajectoriesforthedynamic Zhongkai Zhang received the B.E degree in
identificationofrobots,”Robotica,vol.24,no.5,pp.625–633,Sep.2006, mechanicalengineeringfromHarbinInstituteof
doi:10.1017/S0263574706002712. Technology, Harbin, China, in 2023. He is cur-
[31] V.Bonnet,P.Fraisse,A.Crosnier,M.Gautier,A.González,andG.Venture, rently working toward the M.S. degree in me-
“Optimalexcitingdanceforidentifyinginertialparametersofananthro- chanical engineering with Shanghai Jiao Tong
pomorphicstructure,”IEEETrans.Robot.,vol.32,no.4,pp.823–836, University,Shanghai,China.
Aug.2016,doi:10.1109/TRO.2016.2583062. Hisresearchinterestsincluderobotmodeling,
[32] C.G.Zhuang,“Robotbacklash-induceddynamicserrordataset,”2025. calibrationandforcecontrol.
| [Online]. | Available: |     | https://drive.google.com/drive/folders/1S8BZc__ |     |     |     |     |     |     |     |
| --------- | ---------- | --- | ----------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
gJeAV8GpH7tZW9d_0RL7xOezY?usp=sharing
| [33] Y. Wei, | S. Lyu,    | W. Li,             | X. Yu,      | Z. Wang, | and L.        | Guo, “Contact | force       |     |     |     |
| ------------ | ---------- | ------------------ | ----------- | -------- | ------------- | ------------- | ----------- | --- | --- | --- |
| estimation   | of         | robot manipulators |             | with     | imperfect     | dynamic       | model: On   |     |     |     |
| Gaussian     | process    | adaptive           | disturbance |          | Kalman        | filter,”      | IEEE Trans. |     |     |     |
| Autom.       | Sci. Eng., | vol.               | 21,         | no. 3,   | pp.3524–3537, | Jul.          | 2024, doi:  |     |     |     |
10.1109/TASE.2023.3280750.
[34] J.Duan,Z.Liu,Y.Bin,K.Cui,andZ.Dai,“Payloadidentificationand
gravity/inertialcompensationforsix-dimensionalforce/torquesensorwith
| a fast | and robust | trajectory | design | approach,” | Sensors, | vol. | 22, no. 2, |     |     |     |
| ------ | ---------- | ---------- | ------ | ---------- | -------- | ---- | ---------- | --- | --- | --- |
Jan.2022,Art.no.439,doi:10.3390/s22020439.
Hongbo Hu received the B.E. degree in me- Chungang Zhuang (Member, IEEE) received
|     |     |          |     |             |      |           |         | the Ph.D. degree | in mechanical | engineer- |
| --- | --- | -------- | --- | ----------- | ---- | --------- | ------- | ---------------- | ------------- | --------- |
|     |     | chanical |     | engineering | from | Chongqing | Univer- |                  |               |           |
sity,Chongqing,China,in2022.Heiscurrently ing from the School of Mechanical Engineer-
workingtowardthePh.D.degreeinmechanical ing, Shanghai Jiao Tong University, Shanghai,
|     |     | engineeringwithShanghaiJiaoTongUniversity, |     |     |     |     |     | China,in2007.   |              |                |
| --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | --------------- | ------------ | -------------- |
|     |     |                                            |     |     |     |     |     | He is currently | an Associate | Professor with |
Shanghai,China.
Hisresearchinterestsincluderobotforcecon- theSchoolofMechanicalEngineering,Shang-
trol,robotdynamicmodelingandcalibration. haiJiaoTongUniversity.Hisresearchinterests
includemachinevision,robotforcecontrol,and
structuraltopologyoptimization.
Authorized licensed use limited to: University of Melbourne. Downloaded on June 02,2026 at 01:47:49 UTC from IEEE Xplore.  Restrictions apply.