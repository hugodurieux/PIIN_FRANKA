PublishedasaconferencepaperatICLR2019
| Deep  | Lagrangian |     | Networks: |       |     |     |      |          |     |
| ----- | ---------- | --- | --------- | ----- | --- | --- | ---- | -------- | --- |
| Using | Physics    | as  | Model     | Prior |     | for | Deep | Learning |     |
MichaelLutter,ChristianRitter&JanPeters∗
DepartmentofComputerScience
TechnischeUniversitätDarmstadt
| Hochschulstr. | 10,64289Darmstadt,Germany   |     |     |     |     |     |     |     |     |
| ------------- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| {Lutter,      | Peters}@ias.tu-darmstadt.de |     |     |     |     |     |     |     |     |
Abstract
9102 luJ 01  ]GL.sc[  1v09440.7091:viXra
Deeplearninghasachievedastonishingresultsonmanytaskswithlargeamountsof
|     | dataandgeneralizationwithintheproximityoftrainingdata. |               |         |              |             |            | Formanyimportant |            |        |
| --- | ------------------------------------------------------ | ------------- | ------- | ------------ | ----------- | ---------- | ---------------- | ---------- | ------ |
|     | real-world                                             | applications, | these   | requirements | are         | unfeasible | and              | additional | prior  |
|     | knowledge                                              | on the task   | domain  | is required  | to overcome |            | the resulting    | problems.  |        |
|     | In particular,                                         | learning      | physics | models for   | model-based |            | control          | requires   | robust |
extrapolationfromfewersamples–oftencollectedonlineinreal-time–andmodel
errorsmayleadtodrasticdamagesofthesystem.
Directlyincorporatingphysicalinsighthasenabledustoobtainanoveldeepmodel
|     | learningapproachthatextrapolateswellwhilerequiringfewersamples. |            |            |            |          |         |          |        | Asafirst |
| --- | --------------------------------------------------------------- | ---------- | ---------- | ---------- | -------- | ------- | -------- | ------ | -------- |
|     | example,                                                        | we propose | Deep       | Lagrangian | Networks | (DeLaN) | as       | a deep | network  |
|     | structure                                                       | upon which | Lagrangian | Mechanics  | have     | been    | imposed. | DeLaN  | can      |
learntheequationsofmotionofamechanicalsystem(i.e.,systemdynamics)with
adeepnetworkefficientlywhileensuringphysicalplausibility.
|     | TheresultingDeLaNnetworkperformsverywellatrobottrackingcontrol. |     |     |     |     |     |     |     | The |
| --- | --------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
proposedmethoddidnotonlyoutperformpreviousmodellearningapproachesat
learningspeedbutexhibitssubstantiallyimprovedandmorerobustextrapolation
tonoveltrajectoriesandlearnsonlineinreal-time.
1 Introduction
In the last five years, deep learning has propelled most areas of learning forward at an impressive
pace(Krizhevskyetal.,2012;Mnihetal.,2015;Silveretal.,2017)–withtheexceptionofphysically
embodied systems. This lag in comparison to other application areas is somewhat surprising as
learning physical models is critical for applications that control embodied systems, reason about
prior actions or plan future actions (e.g., service robotics, industrial automation). Instead, most
engineers prefer classical off-the-shelf modeling as it ensures physical plausibility – at a high cost
of precise measurements1 and engineering effort. These plausible representations are preferred as
these models guarantee to extrapolate to new samples, while learned models only achieve good
performanceinthevicinityofthetrainingdata.
Tolearnamodelthatobtainsphysicallyplausiblerepresentations,weproposetousetheinsightsfrom
physicsasamodelpriorfordeeplearning. Inparticular,thecombinationofdeeplearningandphysics
seemsnaturalasthecompositionalstructureofdeepnetworksenablestheefficientcomputationof
thederivativesatmachineprecision(Raissi&Karniadakis,2018)and,thus,canencodeadifferential
equationdescribingphysicalprocesses. Therefore,wesuggesttoencodethephysicspriorintheform
of a differential in the network topology. This adapted topology amplifies the information content
ofthetrainingsamples,regularizestheend-to-endtraining,andemphasizesrobustmodelscapable
of extrapolating to new samples while simultaneously ensuring physical plausibility. Hereby, we
concentrateonlearningmodelsofmechanicalsystemsusingtheEuler-Lagrange-Equation,asecond
orderordinarydifferentialequation(ODE)originatingfromLagrangianMechanics,asphysicsprior.
| ∗MaxPlanckInstituteforIntelligentSystems,Spemannstr. |     |     |     |     |     | 41,72076Tübingen,Germany |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | --- |
1Highlyprecisemodelsusuallyrequiretakingthephysicalsystemapartandmeasuringtheseparatedpieces
(Albu-Schäffer,2002).
1

PublishedasaconferencepaperatICLR2019
We focus on learning models of mechanical systems as this problem is one of the fundamental
challengesofrobotics(deWitetal.,2012;Schaaletal.,2002).
Contribution
Thecontributionofthisworkistwofold. First,wederiveanetworktopologycalledDeepLagrangian
Networks(DeLaN)encodingtheEuler-LagrangeequationoriginatingfromLagrangianMechanics.
Thistopologycanbetrainedusingstandardend-to-endoptimizationtechniqueswhilemaintaining
physical plausibility. Therefore, the obtained model must comply with physics. Unlike previous
approachestolearningphysics(Atkesonetal.,1986;Ledezma&Haddadin,2017),whichengineered
fixedfeaturesfromphysicalassumptionsrequiringknowledgeofthespecificphysicalembodiment,
weare‘only’enforcingphysicsuponagenericdeepnetwork. ForDeLaNonlythesystemstateand
thecontrolsignalarespecifictothephysicalsystembutneithertheproposednetworkstructurenor
thetrainingprocedure. Second,weextensivelyevaluatetheproposedapproachbyusingthemodel
tocontrolasimulated2degreesoffreedom(dof)robotandthephysical7-dofrobotBarrettWAMin
realtime. WedemonstrateDeLaN’scontrolperformancewhereDeLaNlearnsthedynamicsmodel
online starting from random initialization. In comparison to analytic- and other learned models,
DeLaN yields a better control performance while at the same time extrapolates to new desired
trajectories.
In the following we provide an overview about related work (Section 2) and briefly summarize
LagrangianMechanics(Section3). Subsequently,wederiveourproposedapproachDeLaNandthe
necessarycharacteristicsforend-to-endtrainingareshown(Section4). Finally,theexperimentsin
Section 5 evaluate the model learning performance for both simulated and physical robots. Here,
DeLaNoutperformsexistingapproaches.
2 RelatedWork
Models describing system dynamics, i.e. the coupling of control input τττ and system state q, are
essential for model-based control approaches (Ioannou & Sun, 1996). Depending on the control
approach, the control law relies either on the forward model f, mapping from control input to the
changeofsystemstate,orontheinversemodel f−1,mappingfromsystemchangetocontrolinput,
i.e.,
f(q,q(cid:219),τττ)=q(cid:220), f−1(q,q(cid:219),q(cid:220))=τττ. (1)
Examplesforapplicationofthesemodelsareinversedynamicscontrol(deWitetal.,2012),which
usestheinversemodeltocompensatesystemdynamics,whilemodel-predictivecontrol(Camacho&
Alba,2013)andoptimalcontrol(Zhouetal.,1996)usetheforwardmodeltoplanthecontrolinput.
These models can be either derived from physics or learned from data. The physics models must
be derived for the individual system embodiment and requires precise knowledge of the physical
properties (Albu-Schäffer, 2002). When learning the model2, mostly standard machine learning
techniquesareappliedtofiteithertheforward-orinverse-modeltothetrainingdata. E.g.,authors
used Linear Regression (Schaal et al., 2002; Haruno et al., 2001), Gaussian Mixture Regression
(Calinon et al., 2010; Khansari-Zadeh & Billard, 2011), Gaussian Process Regression (Kocijan
etal.,2004;Nguyen-Tuongetal.,2009;Nguyen-Tuong&Peters,2010),SupportVectorRegression
(Choietal.,2007;Ferreiraetal.,2007),feedforward-(Jansen,1994;Lenzetal.,2015;Ledezma&
Haddadin,2017;Sanchez-Gonzalezetal.,2018)orrecurrentneuralnetworks(Rueckertetal.,2017)
tofitthemodeltotheobservedmeasurements.
Only few approaches incorporate prior knowledge into the learning problem. Sanchez-Gonzalez
et al. (2018) use the graph representation of the kinematic structure as input. While the work
of Atkeson et al. (1986), commonly referenced as the standard system identification technique for
robotmanipulators(Siciliano&Khatib,2016),usestheNewton-Eulerformalismtoderivephysics
features using the kinematic structure and the joint measurements such that the learning of the
dynamicsmodelsimplifiestolinearregression. Similarly,Ledezma&Haddadin(2017)hard-code
these physics features within a neural network and learn the dynamics parameters using gradient
descentratherthanlinearregression. Eventhoughthesephysicsfeaturesarederivedfromphysics,the
2FurtherinformationcanbefoundinthemodellearningsurveybyNguyen-Tuong&Peters(2011).
2

PublishedasaconferencepaperatICLR2019
learnedparametersformass,centerofgravityandinertiamustnotnecessarilycomplywithphysics
as the learned parameters may violate the positive definiteness of the inertia matrix or the parallel
axistheorem(Tingetal.,2006). Furthermore,thelinearregressioniscommonlyunderdetermined
and only allows to infer linear combinations of the dynamics parameters and cannot be applied to
close-loopkinematics(Siciliano&Khatib,2016).
DeLaN follows the line of structured learning problems but in contrast to previous approaches
guaranteesphysicalplausibilityandprovidesamoregeneralformulation. Thisgeneralformulation
enables DeLaN to learn the dynamics for any kinematic structure, including kinematic trees and
closed-loopkinematics,andinadditiondoesnotrequireanyknowledgeaboutthekinematicstructure.
Therefore,DeLaNisidenticalforallmechanicalsystems,whichisinstrongcontrasttotheNewton-
Eulerapproaches, wherethefeaturesarespecifictothekinematicstructure. Onlythesystemstate
andinputisspecifictothesystembutneitherthenetworktopologynortheoptimizationprocedure.
ThecombinationofdifferentialequationsandNeuralNetworkshaspreviouslybeeninvestigatedin
literature. EarlyonLagarisetal.(1998;2000)proposedtolearnthesolutionofpartialdifferential
equations (PDE) using neural networks and currently this topic is being rediscovered by Raissi &
Karniadakis(2018);Sirignano&Spiliopoulos(2017);Longetal.(2017). Mostresearchfocuseson
usingmachinelearningtoovercomethelimitationsofPDEsolvers. E.g.,Sirignano&Spiliopoulos
(2017) proposed the Deep Galerkin method to solve a high-dimensional PDE from scattered data.
OnlytheworkofRaissietal.(2017)tooktheoppositestandpointofusingtheknowledgeofthespecific
differentialequationtostructurethelearningproblemandachievelowersamplecomplexity. Inthis
paper, we follow the same motivation as Raissi et al. (2017) but take a different approach. Rather
than explicitly solving the differential equation, DeLaN only uses the structure of the differential
equationtoguidethelearningproblemofinferringtheequationsofmotion. Therebythedifferential
equation is only implicitly solved. In addition, the proposed approach uses different encoding of
thepartialderivatives, whichachievestheefficientcomputationwithinasinglefeed-forwardpass,
enablingtheapplicationwithincontrolloops.
3 Preliminaries: LagrangianMechanics
Describingtheequationsofmotionformechanicalsystemshasbeenextensivelystudiedandvarious
formalisms to derive these equations exist. The most prominent are Newtonian-, Hamiltonian-
andLagrangian-Mechanics. WithinthisworkLagrangianMechanicsisused,morespecificallythe
Euler-Lagrangeformulationwithnon-conservativeforcesandgeneralizedcoordinates.3 Generalized
coordinates are coordinates that uniquely define the system configuration. This formalism defines
the Lagrangian L as a function of generalized coordinates q describing the complete dynamics of
a given system. The Lagrangian is not unique and every L which yields the correct equations of
motionisvalid. TheLagrangianisgenerallychosentobe
L=T−V (2)
whereT isthekineticenergyandV isthepotentialenergy. ThekineticenergyT canbecomputed
for all choices of generalized coordinates using T = 1 q(cid:219)TH(q)q(cid:219), whereas H(q) is the symmetric
2
and positive definite inertia matrix (de Wit et al., 2012). The positive definiteness ensures that all
non-zero velocities lead to positive kinetic energy. Applying the calculus of variations yields the
Euler-Lagrangeequationwithnon-conservativeforcesdescribedby
d ∂L ∂L
− =τττ (3)
dt ∂q(cid:219) ∂q i
i i
whereτττaregeneralizedforces. SubstitutingL anddV/dq=g(q)intoEquation3yieldsthesecond
orderordinarydifferentialequation(ODE)describedby
1 (cid:18) ∂ (cid:16) (cid:17) (cid:19)T
H(q)q(cid:220)+H(cid:219)(q)q(cid:219)− q(cid:219)TH(q)q(cid:219) +g(q)=τττ (4)
2 ∂q
(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32) (cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)
(cid:124) (cid:123)(cid:122) (cid:125)
(cid:66)c(q,q(cid:219))
3More information can be found in the textbooks (Greenwood, 2006; de Wit et al., 2012; Featherstone,
2007)
3

PublishedasaconferencepaperatICLR2019
wherecdescribestheforcesgeneratedbytheCentripetalandCoriolisforces(Featherstone,2007).
UsingthisODEanymulti-particlemechanicalsystemwithholonomicconstraintscanbedescribed.
ForexamplevariousauthorsusedthisODEtomanuallyderivedtheequationsofmotionforcoupled
pendulums(Greenwood,2006),roboticmanipulatorswithflexiblejoints(Book,1984;Spong,1987),
parallelrobots(Miller,1992;Gengetal.,1992;Liuetal.,1993)orleggedrobots(Hemami&Wyman,
1979;Golliday&Hemami,1977).
4 IncorporatingLagrangianMechanicsintoDeepLearning
StartingfromtheEuler-Lagrangeequation(Equation4), traditionalengineeringapproacheswould
estimateH(q)andg(q)fromtheapproximatedormeasuredmasses,lengthsandmomentsofinertia.
Onthecontrarymosttraditionalmodellearningapproacheswouldignorethestructureandlearnthe
inversedynamicsmodeldirectlyfromdata. DeLaNbridgesthisgapbyincorporatingthestructure
introducedbytheODEintothelearningproblemandlearnstheparametersinanend-to-endfashion.
Moreconcretely,DeLaNapproximatestheinversemodelbyrepresentingtheunknownfunctionsg(q)
andH(q)asafeed-forwardnetworks. RatherthanrepresentingH(q)directly, thelower-triangular
matrixL(q)isrepresentedasdeepnetwork. Therefore,g(q)andH(q)aredescribedby
|     |     |     | Hˆ(q)=Lˆ | (q;θ)Lˆ (q;θ)T |     | gˆ(q)=gˆ(q;ψ) |     |     |     |
| --- | --- | --- | -------- | -------------- | --- | ------------- | --- | --- | --- |
whereˆ.referstoanapproximationandθandψaretherespectivenetworkparameters. Theparameters
θ and ψ can be obtained by minimizing the violation of the physical law described by Lagrangian
| Mechanics. | Therefore,theoptimizationproblemisdescribedby |     |                |     |                                   |     |          |     |     |
| ---------- | --------------------------------------------- | --- | -------------- | --- | --------------------------------- | --- | -------- | --- | --- |
|            |                                               |     |                |     | (cid:16)                          |     | (cid:17) |     |     |
|            |                                               |     | (θ∗,ψ∗)=argmin |     | ˆ−1(q,q(cid:219),q(cid:220);θ,ψ), |     |          |     | (5) |
|            |                                               |     |                |     | (cid:96) f                        |     | τττ      |     |     |
θ,ψ
|     |     |                                     |     |     |                        | 1   | (cid:18)   | (cid:19)T    |     |
| --- | --- | ----------------------------------- | --- | --- | ---------------------- | --- | ---------- | ------------ | --- |
|     |     | ˆ−1(q,q(cid:219),q(cid:220);θ,ψ)=Lˆ |     | LˆT | d (cid:16) LˆT(cid:17) |     | ∂ (cid:16) | LˆT (cid:17) |     |
with f q(cid:220)+ Lˆ q(cid:219)− q(cid:219)TLˆ q(cid:219) +gˆ (6)
|     |     |     |           |        | dt    | 2   | ∂q  |     |     |
| --- | --- | --- | --------- | ------ | ----- | --- | --- | --- | --- |
|     |     |     | s.t. 0<xT | Lˆ LˆT | ∀x∈Rn |     |     |     | (7) |
x
0
where ˆ−1 is the inverse model and can be any differentiable loss function. The computational
| f   |     |     |     | (cid:96) |     |     |     |     |     |
| --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
ˆ−1isshowninFigure1.
graphof f
Using this formulation one can conclude further properties of the learned model. Neither Lˆ nor
gˆ are functions of q(cid:219) or q(cid:220) and, hence, the obtained parameters should, within limits, generalize to
arbitraryvelocitiesandaccelerations. Inaddition,theobtainedmodelcanbereformulatedandused
| asaforwardmodel. |     | SolvingEquation6forq(cid:220) |               | yieldstheforwardmodeldescribedby |                        |            |          |              |     |
| ---------------- | --- | ----------------------------- | ------------- | -------------------------------- | ---------------------- | ---------- | -------- | ------------ | --- |
|                  |     |                               |               | (cid:32)                         |                        |            |          | (cid:33)     |     |
|                  |     |                               | LˆT(cid:17)−1 |                                  |                        | 1 (cid:18) |          | (cid:19)T    |     |
|                  | ˆ   |                               | (cid:16)      |                                  | d (cid:16) LˆT(cid:17) | ∂          | (cid:16) | LˆT (cid:17) |     |
f (q,q(cid:219),τττ;θ,ψ)= Lˆ τττ− Lˆ q(cid:219)+ q(cid:219)TLˆ q(cid:219) −gˆ (8)
|     |     |     |     | dt  |     | 2 ∂q |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
LˆTisguaranteedtobeinvertibleduetothepositivedefiniteconstraint(Equation7).
| whereLˆ |     |     |     |     |     |     |     | However, |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | -------- | --- |
solvingtheoptimizationproblemofEquation5directlyisnotpossibleduetotheill-posednessofthe
Lagrangian notbeingunique. TheEuler-Lagrangeequationisinvarianttolineartransformation
L
and, hence, the Lagrangian L(cid:48)=αL+β solves the Euler-Lagrange equation if is non-zero and
α
L is a valid Lagrangian. This problem can be mitigated by adding an additional penalty term to
Equation5describedby
|     |     |                |     | (cid:16)                                     |     | (cid:17) |          |     |     |
| --- | --- | -------------- | --- | -------------------------------------------- | --- | -------- | -------- | --- | --- |
|     |     | (θ∗,ψ∗)=argmin |     | (cid:96) f ˆ−1(q,q(cid:219),q(cid:220);θ,ψ), |     | τττ      | +λΩ(θ,ψ) |     | (9) |
θ,ψ
| whereΩistheL2 |     | -normofthenetworkweights. |     |     |     |     |     |     |     |
| ------------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- |
SolvingtheoptimizationproblemofEquation9withagradientbasedend-to-endlearningapproach
isnon-trivialduetothepositivedefiniteconstraint(Equation7)andthederivativescontainedin f ˆ−1.
Inparticular,d(LLT)/dt and∂ (cid:0) q(cid:219)TLLTq(cid:219)(cid:1) /∂q cannotbecomputedusingautomaticdifferentiation
i
astisnotaninputofthenetworkandmostimplementationsofautomaticdifferentiationdonotallow
the backpropagation of the gradient through the computed derivatives. Therefore, the derivatives
containedin f ˆ−1 mustbecomputedanalyticallytoexploitthefullgradientinformationfortraining
4

PublishedasaconferencepaperatICLR2019
oftheparameters. Inthefollowingweintroduceanetworkstructurethatfulfillsthepositive-definite
(cid:0) q(cid:219)TLLTq(cid:219)(cid:1)
constraintforallparameters(Section4.1),provethatthederivativesd(LLT)/dtand∂ /∂q
i
canbecomputedanalytically(Section4.2)andshowanefficientimplementationforcomputingthe
derivativesusingasinglefeed-forwardpass(Section4.3). Usingthesethreepropertiestheresulting
networkarchitecturecanbeusedwithinareal-timecontrolloopandtrainedusingstandardend-to-end
optimizationtechniques.
|     |     | 0   |     |     | +   | +   | +   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
*
b
|     |     |      | ∗ 0 0 |         |        |       |     |     |
| --- | --- | ---- | ----- | ------- | ------ | ----- | --- | --- |
| %   |     | 12 + | 0 ∗ 0 |         | ! $'"$ | ! " $ | H$  |     |
|     |     |      |       |         | ! %&   | ! #   |     |     |
|     |     |      | 0 0 ∗ |         |        |       |     |     |
|     |     |      | 0 0 0 |         |        |       |     |     |
|     |     | 13   | ∗ 0 0 | + -.-=" |        |       |     |     |
| %̇  |     |      | ∗ ∗ 0 |         |        |       |     |     |
%̈
|     | ReLuNetwork | Linear Network |     | Physics Transformations |     |     |     |     |
| --- | ----------- | -------------- | --- | ----------------------- | --- | --- | --- | --- |
Figure1: ThecomputationalgraphoftheDeepLagrangianNetwork(DeLaN).Showninblueand
greenistheneuralnetworkwiththethreeseparateheadscomputingg(q),l (q),l (q). Theorange
|     |     |     |     |     |     |     | d o |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
boxes correspond to the reshaping operations and the derivatives contained in the Euler-Lagrange
equation. Fortrainingthegradientsarebackpropagatedthroughallverticeshighlightedinorange.
4.1 SymmetryandPositiveDefinitenessofH
EnsuringthesymmetryandpositivedefinitenessofHisessentialasthisconstraintenforcespositive
kinetic energy for all non-zero velocities. In addition, the positive definiteness ensures that is
H
invertibleandtheobtainedmodelcanbeusedasforwardmodel. ByrepresentingthematrixHas
theproductofalower-triangularmatrixthesymmetryandthepositivesemi-definitenessisensured
whilesimultaneouslyreducingthenumberofparameters. Thepositivedefinitenessisobtainedifthe
diagonalofLispositive. ThispositivediagonalalsoguaranteesthatLisinvertible. Usingadeep
networkwithdifferentheadsandalteringtheactivationoftheoutputlayeronecanobtainapositive
diagonal. Theoff-diagonalelementsL usealinearactivationwhilethediagonalelementsL usea
|     |     |     | o   |     |     |     |     | d   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
non-negativeactivation,e.g.,ReLuorSoftplus. Inaddition,apositivescalarbisaddedtodiagonal
elements. Thereby,ensuringapositivediagonalofLandthepositiveeigenvaluesofH. Inaddition,
wechosetoshareparametersbetweenLandgasbothrelyonthesamephysicalembodiment. The
networkarchitecture,withthree-headsrepresentingthediagonall andoff-diagonall entriesofL
|     |     |     |     |     |     | d   | o   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
andg,isshowninFigure1.
4.2 Derivingthederivatives
Thederivatives d (cid:0) LLT(cid:1) /dt and ∂ (cid:0) q(cid:219)TLLTq(cid:219)(cid:1) /∂q arerequiredforcomputingthecontrolsignal τττ
i
using the inverse model and, hence, must be available within the forward pass. In addition, the
second order derivatives, used within the backpropagation of the gradients, must exist to train the
networkusingend-to-endtraining. Toenablethecomputationofthesecondorderderivativesusing
automaticdifferentiationtheforwardcomputationmustbeperformedanalytically. Bothderivatives,
d (cid:0) LLT(cid:1) /dtand∂ (cid:0) q(cid:219)TLLTq(cid:219)(cid:1) /∂q ,haveclosedformsolutionsandcanbederivedbyfirstcomputing
i
therespectivederivativeofLandsecondsubstitutingthereshapedderivativeofthevectorizedform
| l. Forthetemporalderivatived |     | (cid:0) LLT(cid:1) | thisyields |     |     |     |     |     |
| ---------------------------- | --- | ------------------ | ---------- | --- | --- | --- | --- | --- |
/dt
|     |     | d     | d (cid:16) | (cid:17) | dLT | dL  |     |      |
| --- | --- | ----- | ---------- | -------- | --- | --- | --- | ---- |
|     |     | H(q)= | LLT        | =L       | +   | LT  |     | (10) |
|     |     | dt    | dt         |          | dt  | dt  |     |      |
whereasdL/dt canbesubstitutedwiththereshapedformof
|     |     | d ∂l ∂q  | N           | ∂l ∂W | N             | ∂l ∂b |     |      |
| --- | --- | -------- | ----------- | ----- | ------------- | ----- | --- | ---- |
|     |     | l=       | + (cid:213) |       | i + (cid:213) |       | i   | (11) |
|     |     | dt ∂q ∂t |             | ∂W ∂t |               | ∂b ∂t |     |      |
|     |     |          | i=1         | i     | i=1           | i     |     |      |
5

PublishedasaconferencepaperatICLR2019
,-./ MatMul Add
ai
gi ,-
Wi bi g‘i diag(ai) MatMul + + , , -. - /
% ∗ 0 0 '
(a) a0 a1 # ∗ ∗ ∗ ∗ 0 ∗
('
W0 b0 W1 b1 0 0 ∗ ∗ 0 0 ∗ ∗ 0 ∗ 0 0 (%)
0 ∗ 0 ∗ ∗ ∗
$'
$
$
%
#
$
$
%
#%̇ ∗
∗ ∗
0
∗ ∗
0
0 ∗
$*
%̇
(b)
Figure2: (a)ComputationalgraphoftheLagrangianlayer. Theorangeboxeshighlightthelearnable
parameters. The upper computational sub-graph corresponds to the standard network layer while
thelowersub-graphistheextensionoftheLagrangianlayertosimultaneouslycompute∂h i /∂h i−1 .
(b)ComputationalgraphofthechainedLagrangianlayertocomputeL,dL/dt and∂L/∂q usinga
i
singlefeed-forwardpass.
whereireferstothei-thnetworklayerconsistingofanaffinetransformationandthenon-linearityg,
i.e.,h i =g i (cid:0) WT i h i−1 +b i (cid:1). Equation11canbesimplifiedasthenetworkweightsW i andbiasesb i
aretime-invariant,i.e.,dW /dt=0anddb /dt=0. Therefore,dl/dt isdescribedby
i i
d ∂l
l= q(cid:219). (12)
dt ∂q
Duetothecompositionalstructureofthenetworkandthedifferentiabilityofthenon-linearity, the
derivativewithrespecttothenetworkinputdl/dqcanbecomputedbyrecursivelyapplyingthechain
rule,i.e.,
∂ ∂ q l = ∂h ∂ N l −1 ∂ ∂ h h N N − − 2 1 ··· ∂ ∂ h q 1 ∂ ∂ h h i− i 1 =diag (cid:16) g(cid:48)(WT i h i−1 +b i ) (cid:17) W i (13)
where g(cid:48) is the derivative of the non-linearity. Similarly to the previous derivation, the partial
derivativeofthequadratictermcanbecomputedusingthechainrule,whichyields
∂ (cid:2) q(cid:219)THq(cid:219) (cid:3) =tr
(cid:20)
(cid:16) q(cid:219)q(cid:219)T (cid:17)T ∂H
(cid:21)
=q(cid:219)T
(cid:18)
∂L LT+L
∂LT(cid:19)
q(cid:219) (14)
∂q ∂q ∂q ∂q
i i i i
whereas∂L/∂q canbeconstructedusingthecolumnsofpreviouslyderived∂l/∂q. Therefore,all
i
derivativesincludedwithin f ˆcanbecomputedinclosedform.
4.3 ComputingtheDerivatives
The derivatives of Section 4.2 must be computed within a real-time control loop and only add
minimal computational complexity in order to not break the real-time constraint. l and ∂l/∂q,
required within Equation 10 and Equation 14, can be simultaneously computed using an extended
standardlayer. Extendingtheaffinetransformationandnon-linearityofthestandardlayerwithan
additionalsub-graphforcomputing∂h i /∂h i−1 yieldstheLagrangianlayerdescribedby
∂h
a i =W i h i−1 +b i h1 =g i (a i ) ∂h i− i 1 =diag(cid:0) g i (cid:48)(a i ) (cid:1) W i .
ThecomputationalgraphoftheLagrangianlayerisshowninFigure2a. ChainingtheLagrangian
layeryieldsthecompositionalstructureof∂l/∂q(Equation13)andenablestheefficientcomputation
of∂l/∂q. AdditionalreshapingoperationscomputedL/dt and∂L/∂q .
i
5 ExperimentalEvaluation: LearninganInverseDynamicsModelfor
RobotControl
To demonstrate the applicability and extrapolation of DeLaN, the proposed network topology is
appliedtomodel-basedcontrolforasimulated2-dofrobot(Figure3b)andthephysical7-dofrobot
6

PublishedasaconferencepaperatICLR2019
| Control Loop |     |     | Training Process |     |           |     |     |     |     |
| ------------ | --- | --- | ---------------- | --- | --------- | --- | --- | --- | --- |
|              |     | ∇+2 |                  | 1.5 | Cos0 Cos1 |     |     |     |     |
1.0
!-,!̇-, !̈- Inverse Model
| %$&'(!,!̇,!̈;+) |     | Loss  | Inverse Model   | 0.5 |     |     |     |     |     |
| --------------- | --- | ----- | --------------- | --- | --- | --- | --- | --- | --- |
|                 |     | L.0,. | %$&'(!,!̇,!̈;+) |     |     |     |     |     |     |
0.0
]m[y
 0.5
.
| - PD-Controller |     |      | Robot |  1.0 |     |     |     |     |     |
| --------------- | --- | ---- | ----- | ---- | --- | --- | --- | --- | --- |
|                 |     | !,!̇ |       |  1.5 |     |     |     |     |     |
 2.0
|     |     |     |     |     |  0.5 0.0 0.5 | 1.0 1.5 | 2.0 |     |     |
| --- | --- | --- | --- | --- | ------------ | ------- | --- | --- | --- |
|     | (a) |     |     |     | (b) x[m]     |         |     | (c) | (d) |
Figure3: (a)Real-timecontrolloopusingaPD-Controllerwithafeed-forwardtorqueτττ ,compen-
FF
satingthesystemdynamics,tocontrolthejointtorquesτττ. Thetrainingprocessreadsthejointstates
andappliestorquestolearnthesystemdynamicsonline. Onceanewmodelbecomesavailablethe
ˆ−1
inversemodel f inthecontrolloopisupdated. (b)Thesimulated2-dofrobotdrawingthecosine
trajectories. (c) The simulated Barrett WAM drawing the 3d cosine 0 trajectory. (d) The physical
BarrettWAM.
BarrettWAM(Figure3d). TheperformanceofDeLaNisevaluatedusingthetrackingerrorontrain
andtesttrajectoriesandcomparedtoalearnedandanalyticmodel. Thisevaluationschemefollows
existing work (Nguyen-Tuong et al., 2009; Sanchez-Gonzalez et al., 2018) as the tracking error is
the relevant performance indicator while the mean squared error (MSE)4 obtained using sample
basedoptimizationexaggeratesmodelperformance(Hobbs&Hepenstal,1989). Inadditiontomost
previouswork,westrictlylimitallmodelpredictionstoreal-timeandperformthelearningonline,
i.e.,themodelsarerandomlyinitializedandmustlearnthemodelduringtheexperiment.
ExperimentalSetup
Withintheexperimenttherobotexecutesmultipledesiredtrajectorieswithspecifiedjointpositions,
velocities and accelerations. The control signal, consisting of motor torques, is generated using
a non-linear feedforward controller, i.e., a low gain PD-Controller augmented with a feed-forward
| torqueτττ tocompensatesystemdynamics. |     |     |     | Thecontrollawisdescribedby |     |     |     |     |     |
| ------------------------------------- | --- | --- | --- | -------------------------- | --- | --- | --- | --- | --- |
ff
|     | τττ=K | −q)+K |             | −q(cid:219))+τττ | with |     | = ˆ−1(q |                           |     |
| --- | ----- | ----- | ----------- | ---------------- | ---- | --- | ------- | ------------------------- | --- |
|     |       | (q    | (q(cid:219) |                  |      | τττ | f       | ,q(cid:219) ,q(cid:220) ) |     |
|     | p     | d     | d d         |                  | ff   | ff  |         | d d d                     |     |
where K , K are the controller gains and q , q(cid:219) , q(cid:220) the desired joint positions, velocities and
| p d |     |     |     | d   | d d |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
accelerations. The control-loop is shown in Figure 3a. For all experiments the control frequency
is set to 500Hz while the desired joint state and respectively is updated with a frequency of
|     |     |     |     |     |     |     | τττ ff |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
f =200Hz. All feed-forward torques are computed online and, hence, the computation time is
d
strictlylimitedtoT ≤1/200s. ThetrackingperformanceisdefinedasthesumoftheMSEevaluated
atthesamplingpointsofthereferencetrajectory.
Forthedesiredtrajectoriestwodifferentdatasetsareused. Thefirstdatasetcontainsallsinglestroke
characters5whiletheseconddatasetusescosinecurvesinjointspace(Figure3c). The20characters
are spatially and temporally re-scaled to comply with the robot kinematics. The joint references
arecomputedusingtheinversekinematics. Duetothedifferentcharacters,thedesiredtrajectories
containsmoothandsharpturnsandcoverawidevarietyofdifferentshapesbutarelimitedtoasmall
taskspaceregion. Incontrast,thecosinetrajectoriesaresmoothbutcoveralargetaskspaceregion.
Baselines
The performance of DeLaN is compared to an analytic inverse dynamics model, a standard feed-
forwardneuralnetwork(FF-NN)andaPD-Controller. Fortheanalyticmodelsthetorqueiscomputed
using the Recursive Newton-Euler algorithm (RNE) (Luh et al., 1980), which computes the feed-
forwardtorqueusingestimatedphysicalpropertiesofthesystem, i.e. thelinkdimensions, masses
and moments of inertia. For implementations the open-source library PyBullet (Coumans & Bai,
2016–2018)isused.
Both deep networks use the same dimensionality, ReLu nonlinearities and must learn the system
dynamics online starting from random initialization. The training samples containing joint states
and applied torques (q,q(cid:219),q(cid:220),τττ) are directly read from the control loop as shown in Figure 3a.
0,...T
4AnofflinecomparisonsevaluatingtheMSEondatasetscanbefoundintheAppendixA.
5ThedatasetwascreatedbyWilliamsetal.(2008)andisavailableatDheeru&KarraTaniskidou(2017))
7

PublishedasaconferencepaperatICLR2019
|                   | τ             |            | H(q)q¨ |            | c(q,q˙) |                | g(q) |                   | 100 OfflineTestingError |       |
| ----------------- | ------------- | ---------- | ------ | ---------- | ------- | -------------- | ---- | ----------------- | ----------------------- | ----- |
|                   | DeLaN         |            | 2      | 0.3        |         | 2.5            |      |                   |                         | DeLaN |
|                   | 3 GroundTruth |            |        |            |         | 2.0            |      | rorrrEderauqSnaeM |                         | FF-NN |
|                   |               |            | 1      | 0.2        |         |                |      |                   |                         |       |
| 0tnioJ ]mN[euqroT |               | ]mN[euqroT |        | ]mN[euqroT |         | ]mN[euqroT 1.5 |      | 10−1              |                         |       |
|                   | 2             |            |        | 0.1        |         |                |      |                   |                         |       |
|                   |               |            | 0      |            |         | 1.0            |      |                   |                         |       |
|                   | 1             |            |        |            |         |                |      | 10−2              |                         |       |
|                   |               |            |        | 0.0        |         | 0.5            |      |                   |                         |       |
−1
|     | 0   |     |     | −0.1 |     | 0.0 |     | 10−3 |          |              |
| --- | --- | --- | --- | ---- | --- | --- | --- | ---- | -------- | ------------ |
|     | d a | e   | d a | e    | d a | e   | d a | e    | 12 4 6 8 | 101214161820 |
100
|            |      |            | 0.25 | 0.3        |     |                |     |                  |     |     |
| ---------- | ---- | ---------- | ---- | ---------- | --- | -------------- | --- | ---------------- | --- | --- |
|            | 0.5  |            |      |            |     | 0.4            |     | rorrEderauqSnaeM |     |     |
| ]mN[euqroT |      | ]mN[euqroT | 0.00 | ]mN[euqroT |     | ]mN[euqroT 0.2 |     | 10−1             |     |     |
| 1tnioJ     | 0.0  |            |      | 0.2        |     |                |     |                  |     |     |
|            |      | −0.25      |      |            |     | 0.0            |     |                  |     |     |
|            | −0.5 | −0.50      |      | 0.1        |     |                |     | 10−2             |     |     |
−0.2
−0.75
|     | −1.0 |     |     | 0.0 |     | −0.4 |     | 10−3 |          |              |
| --- | ---- | --- | --- | --- | --- | ---- | --- | ---- | -------- | ------------ |
|     | d a  | e   | d a | e   | d a | e    | d a | e    | 12 4 6 8 | 101214161820 |
TrainCharacters
|     | (a) |     | (b) |     | (c) |     | (d) |     |     | (e) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure4: (a)Thetorqueτττ requiredtogeneratethecharacters’a’,’d’and’e’inblack. Usingthese
samples DeLaN was trained offline and learns the red trajectory. DeLaN can not only learn the
desired torques but also disambiguate the individual torque components even though DeLaN was
trainedonthesuper-imposedtorques. UsingEquation6DeLaNcanrepresenttheinertialforceHq(cid:220)
(b),theCoriolisandCentrifugalforcesc(q,q(cid:219))(c)andthegravitationalforceg(q)(d). Allcomponents
matchcloselythegroundtruthdata. (e)showstheofflineMSEofthefeed-forwardneuralnetwork
andDeLaNforeachjoint.
The training runs in a separate process on the same machine and solves the optimization problem
ˆ−1ofthecontrolloop
| online. | Oncethetrainingprocesscomputedanewmodel,theinversemodel |     |     |     |     |     |     | f   |     |     |
| ------- | ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
isupdated.
5.1 SimulatedRobotExperiments
The 2-dof robot shown in Figure 3b is simulated using PyBullet and executes the character and
cosinetrajectories. Figure4showsthegroundtruthtorquesofthecharacters’a’,’d’,’e’,thetorque
groundtruthcomponentsandthelearneddecompositionusingDeLaN(Figure4a-d). Eventhough
DeLaN is trained on the super-imposed torques, DeLaN learns to disambiguate the inertial force
Hq(cid:220) , the Coriolis and Centrifugal force c(q,q(cid:219)) and the gravitational force g(q) as the respective
curves overlap closely. Hence, DeLaN is capable of learning the underlying physical model using
the proposed network topology trained with standard end-to-end optimization. Figure 4d shows
the offline MSE on the test set averaged over multiple seeds for the FF-NN and DeLaN w.r.t. to
differenttrainingsetsizes. Thedifferenttrainingsetsizescorrespondtothecombinationofnrandom
characters, i.e., atrainingsetsizeof1correspondstotrainingthemodelonasinglecharacterand
evaluatingtheperformanceontheremaining19characters. DeLaNclearlyobtainsalowertestMSE
compared to the FF-NN. Especially the difference in performance increases when the training set
is reduced. This increasing difference on the test MSE highlights the reduced sample complexity
and the good extrapolation to unseen samples. This difference in performance is amplified on
thereal-timecontrol-taskwherethemodelsarelearnedonlinestartingfromrandominitialization.
Figure 5a and b shows the accumulated tracking error per testing character and the testing error
averaged over all test characters while Figure 5c shows the qualitative comparison of the control
performance6. Itisimportanttopointoutthatallshownresultsareaveragedovermultipleseedsand
onlyincorporatecharactersnotusedfortrainingand,hence,focustheevaluationontheextrapolation
tonewtrajectories. ThequalitativecomparisonshowsthatDeLaNisabletoexecuteall20characters
when trained on 8 random characters. The obtained tracking error is comparable to the analytic
model,whichinthiscasecontainsthesimulationparametersandisoptimal. Incontrast,theFF-NN
showssignificantdeviationfromthedesiredtrajectorieswhentrainedon8randomcharacters. The
quantitativecomparisonoftheaccumulatedtrackingerroroverseeds(Figure5b)showsthatDeLaN
obtainslowertrackingerroronalltrainingsetsizescomparedtotheFF-NN.Thisgoodperformance
using only few training characters shows that DeLaN has a lower sample complexity and better
extrapolationtounseentrajectoriescomparedtotheFF-NN.
Figure 6a and b show the performance on the cosine trajectories. For this experiment the models
are only trained online on two trajectories with a velocity scale of 1x. To assess the extrapolation
w.r.t. velocitiesandaccelerationsthelearnedmodelsaretestedonthesametrajectorieswithscaled
velocities (gray area of Figure 6). On the training trajectories DeLaN and the FF-NN perform
6ThefullresultscontainingallcharactersareprovidedintheAppendixB.
8

PublishedasaconferencepaperatICLR2019
FF-NN FF-NN FF-NN FF-NN DeLaN DeLaN DeLaN DeLaN RNE PD-Controller n=1 n=6 n=8 n=10 n=1 n=6 n=8 n=10
103
102
101
100
10−1
1 2 4 6 8 10 12 14 16 18 20
TrainCharacters (c)
rorrEgnikcarTdetalumuccA
103
102
101
100
10−1
10−2
a b c d e g h l m n o p q r s u v w y z
TrackingError
FF-NN
DeLaN
RNE
PD-Controller
(b)
rorrEgnikcarT
MLP Lagrangian RNE PD-Controller
(a)
Figure 5: (a) The average performance of DeLaN and the feed forward neural network for each
character. The 4 columns of the boxplots correspond to different numbers of training characters,
i.e., n=1, 6, 8, 10. (b) The median performance of DeLaN, the feed forward neural network and
the analytic baselines averaged over multiple seeds. The shaded areas highlight the 5th and the
95thpercentile. (c)Thequalitativeperformancefortheanalyticbaselines,thefeedforwardneural
networkandDeLaN.Thedesiredtrajectoriesareshowninred.
comparable. WhenthevelocitiesareincreasedtheperformanceofFF-NNdeterioratesbecausethe
newtrajectoriesdonotliewithinthevicinityofthetrainingdistributionasthedomainoftheFF-NN
is defined as (q,q(cid:219),q(cid:220)). Therefore, FF-NN cannot extrapolate to the testing data. In contrast, the
domain of the networks Lˆ and gˆ composing DeLaN only consist of q, rather than (q,q(cid:219),q(cid:220)). This
reduceddomainenablesDeLaN,withinlimit,toextrapolatetothetesttrajectories. Theincreasein
trackingerroriscausedbythestructureof f ˆ−1,wheremodelerrorstoscalequadraticwithvelocities.
However, the obtained tracking error on the testing trajectories is significantly lower compared to
FF-NN.
5.2 PhysicalRobotExperiments
For physical experiments the desired trajectories are executed on the Barrett WAM, a robot with
direct cable drives. The direct cable drives produce high torques generating fast and dexterous
movementsbutyieldcomplexdynamics,whichcannotbemodelledusingrigid-bodydynamicsdue
tothevariablestiffnessandlengthsofthecables7. Therefore,theBarrettWAMisidealfortesting
the applicability of model learning and analytic models8 on complex dynamics. For the physical
experiments we focus on the cosine trajectories as these trajectories produce dynamic movements
whilecharactertrajectoriesaremainlydominatedbythegravitationalforces. Inaddition, onlythe
dynamics of the four lower joints are learned because these joints dominate the dynamics and the
upperjointscannotbesufficientlyexcitedtoretrievethedynamicsparameters.
Figure 6c and d show the tracking error on the cosine trajectories using the the simulated Barrett
WAM while Figure 6e and f show the tracking error of the physical Barrett WAM. It is important
tonote, thatthesimulationonlysimulatestherigid-bodydynamicsnotincludingthedirectcables
drives and the simulation parameters are inconsistent with the parameters of the analytic model.
Therefore, the analytic model is not optimal. On the training trajectories executed on the physical
system the FF-NN performs better compared to DeLaN and the analytic model. DeLaN achieves
slightlybettertrackingerrorthantheanalyticmodel, whichusesthesamerigid-bodyassumptions
asDeLaN.ThatshowsDeLaNcanlearnadynamicsmodeloftheWAMbutislimitedbythemodel
assumptions of Lagrangian Mechanics. These assumptions cannot represent the dynamics of the
7Thecabledrivesandcablescouldbemodelledsimplisticallyusingtwojointsconnectedbymasslessspring.
8TheanalyticmodeloftheBarrettWAMisobtainedusingapubliclyavailableURDF(JHULCSR,2018)
9

PublishedasaconferencepaperatICLR2019
104
103
102
101
100
10−1
1 1.251.51.75 2 2.252.5
VelocityScale
rorrEgnikcarTnaeM
2DoFRobot-Cosine0 2DoFRobot-Cosine1 SimWAM-Cosine0 SimWAM-Cosine1 BarrettWAM-Cosine2 BarrettWAM-Cosine3
104 104 104 104 104 DeLaN
FF-NN
103 103 103 103 103 RNE
102 102 102 102 102
101 101 101 101 101
100 100 100 100 100
TestData 10−1
1 1.251.51.75 2
T
2
e
.
s
2
t
5
Da
2
t
.
a
5
10−1
1 1.25 1.5 1.75
Te
2
stD
2
a
.
t
2
a
5
10−1
1 1.25 1.5 1.75
Te
2
stD
2
a
.
t
2
a
5
10−1
1 1.25 1.5 1.
T
75
estDa
2
ta 10−1
1 1.25 1.5 1.
T
75
estDa
2
ta
VelocityScale VelocityScale VelocityScale VelocityScale VelocityScale
(a) (b) (c) (d) (e) (f)
Figure 6: The tracking error of the cosine trajectories for the simulated 2-dof robot (a & b), the
simulated (c & d) and the physical Barrett WAM (e & f). The feed-forward neural network and
DeLaNaretrainedonlyonthetrajectoriesatavelocityscaleof1×. Afterwardsthemodelsaretested
onthesametrajectorieswithincreasedvelocitiestoevaluatetheextrapolationtonewvelocities.
cabledrives. Whencomparingtothesimulatedresults,DeLaNandtheFF-NNperformcomparable
butsignificantlybetterthantheanalyticmodel. ThesesimulationresultsshowthatDeLaNcanlearn
an accurate model of the WAM, when the underlying assumptions of the physics prior hold. The
tracking performance on the physical system and the simulation indicate that DeLaN can learn a
model within the model class of the physics prior but also inherits the limitations of the physics
prior. ForthisspecificexperimenttheFF-NNcanlocallylearncorrelationsofthetorquesw.r.t. q,q(cid:219)
andq(cid:220) whilesuchcorrelationcannotberepresentedbythenetworktopologyofDeLaNbecausesuch
correlationshould,bydefinitionofthephysicsprior,notexist.
When extrapolating to the identical trajectories with higher velocities (gray area of Figure 6) the
trackingerroroftheFF-NNdeterioratesmuchfastercomparedtoDeLaN,becausetheFF-NNoverfits
to the training data. The tracking error of the analytic model remains constant and demonstrates
the guaranteed extrapolation of the analytic models. When comparing the simulated results, the
FF-NN cannot extrapolate to the new velocities and the tracking error deteriorates similarly to the
performanceonthephysicalrobot. IncontrasttotheFF-NN,DeLaNcanextrapolatetothehigher
velocitiesandmaintainsagoodtrackingerror. Evenfurther,DeLaNobtainsabettertrackingerror
compared the analytic model on all velocity scales. This low tracking error on all test trajectories
highlightstheimprovedextrapolationofDeLaNcomparedtoothermodellearningapproaches.
6 Conclusion
We introduced the concept of incorporating a physics prior within the deep learning framework
to achieve lower sample complexity and better extrapolation. In particular, we proposed Deep
LagrangianNetworks(DeLaN),adeepnetworkonwhichLagrangianMechanicsisimposed. This
specificnetworktopologyenabledustolearnthesystemdynamicsusingend-to-endtrainingwhile
maintaining physical plausibility. We showed that DeLaN is able to learn the underlying physics
from a super-imposed signal, as DeLaN can recover the contribution of the inertial-, gravitational
andcentripetalforcesfromsensordata. Thequantitativeevaluationwithinareal-timecontrolloop
assessingthetrackingerrorshowedthatDeLaNcanlearnthesystemdynamicsonline,obtainslower
samplecomplexityandbettergeneralizationcomparedtoafeed-forwardneuralnetwork. DeLaNcan
extrapolatetonewtrajectoriesaswellastoincreasedvelocities,wheretheperformanceofthefeed-
forwardnetworkdeterioratesduetotheoverfittingtothetrainingdata. Whenappliedtoaphysical
systems with complex dynamics the bounded representational power of the physics prior can be
limiting. However,thislimitedrepresentationalpowerenforcesthephysicalplausibilityandobtains
thelowersamplecomplexityandsubstantiallybettergeneralization. Infutureworkthephysicsprior
should be extended to represent a wider system class by introducing additional non-conservative
forceswithintheLagrangian.
Acknowledgments
ThisprojecthasreceivedfundingfromtheEuropeanUnion’sHorizon2020researchandinnovation
programundergrantagreementNo#640554(SKILLS4ROBOTS).Furthermore,thisresearchwas
alsosupportedbygrantsfromABB,NVIDIAandtheNVIDIADGXStation.
10

PublishedasaconferencepaperatICLR2019
References
Alin Albu-Schäffer. Regelung von Robotern mit elastischen Gelenken am Beispiel der DLR-
Leichtbauarme. PhDthesis,TechnischeUniversitätMünchen,2002.
ChristopherGAtkeson, ChaeHAn, andJohnMHollerbach. Estimationofinertialparametersof
manipulator loads and links. The International Journal of Robotics Research, 5(3):101–119,
1986.
Wayne J Book. Recursive lagrangian dynamics of flexible manipulator arms. The International
JournalofRoboticsResearch,3(3):87–101,1984.
SylvainCalinon,FlorentD’halluin,EricLSauser,DarwinGCaldwell,andAudeGBillard.Learning
andreproductionofgesturesbyimitation.IEEERobotics&AutomationMagazine,17(2):44–54,
2010.
Eduardo F Camacho and Carlos Bordons Alba. Model predictive control. Springer Science &
BusinessMedia,Berlin,Heidelberg,2013.
Younggeun Choi, Shin-Young Cheong, and Nicolas Schweighofer. Local online support vector
regressionforlearningcontrol. InInternationalSymposiumonComputationalIntelligencein
RoboticsandAutomation,pp.13–18.IEEE,2007.
ErwinCoumansandYunfeiBai.Pybullet,apythonmoduleforphysicssimulationforgames,robotics
andmachinelearning. http://pybullet.org,2016–2018.
Carlos Canudas de Wit, Bruno Siciliano, and Georges Bastin. Theory of robot control. Springer
Science&BusinessMedia,2012.
Dua Dheeru and Efi Karra Taniskidou. UCI machine learning repository, 2017. URL http:
//archive.ics.uci.edu/ml.
Roy Featherstone. Rigid Body Dynamics Algorithms. Springer-Verlag, Berlin, Heidelberg, 2007.
ISBN0387743146.
JoaoPFerreira,ManuelCrisostomo,APauloCoimbra,andBernardeteRibeiro. Simulationcontrol
ofabipedrobotwithsupportvectorregression.InIEEEInternationalSymposiumonIntelligent
SignalProcessing,pp.1–6.IEEE,2007.
ZhengGeng, LeonardSHaynes, JamesDLee, andRobertLCarroll. Onthedynamicmodeland
kinematic analysis of a class of stewart platforms. Robotics and autonomous systems, 9(4):
237–254,1992.
C.LeslieGollidayandHooshangHemami. Anapproachtoanalyzingbipedlocomotiondynamics
and designing robot locomotion controls. IEEE Transactions on Automatic Control, 22(6):
963–972,December1977. ISSN0018-9286. doi: 10.1109/TAC.1977.1101650.
DonaldTGreenwood. Advanceddynamics. CambridgeUniversityPress,2006.
MasahikoHaruno,DanielMWolpert,andMitsuoKawato. Mosaicmodelforsensorimotorlearning
andcontrol. Neuralcomputation,13(10):2201–2220,2001.
Hooshang Hemami and Bostwick Wyman. Modeling and control of constrained dynamic systems
with application to biped locomotion in the frontal plane. IEEE Transactions on Automatic
Control,24(4):526–535,August1979. ISSN0018-9286. doi: 10.1109/TAC.1979.1102105.
Benjamin F Hobbs and Ann Hepenstal. Is optimization optimistically biased? Water Resources
Research,25(2):152–160,1989.
PetrosAIoannouandJingSun. Robustadaptivecontrol,volume1. Prentice-Hall,1996.
M Jansen. Learning an accurate neural model of the dynamics of a typical industrial robot. In
InternationalConferenceonArtificialNeuralNetworks,pp.1257–1260,1994.
11

PublishedasaconferencepaperatICLR2019
JHULCSRJHULCSR. Barrettmodelcontainingthe7-dofurdf, 2018. URLhttps://github.
com/jhu-lcsr/barrett_model.
SMohammadKhansari-ZadehandAudeBillard. Learningstablenonlineardynamicalsystemswith
gaussianmixturemodels. IEEETransactionsonRobotics,27(5):943–957,2011.
JušKocijan,RoderickMurray-Smith,CarlEdwardRasmussen,andAgatheGirard.Gaussianprocess
model based predictive control. In American Control Conference, volume 3, pp. 2214–2219.
IEEE,2004.
AlexKrizhevsky,IlyaSutskever,andGeoffreyEHinton. Imagenetclassificationwithdeepconvolu-
tionalneuralnetworks. InAdvancesinNeuralInformationProcessingSystems,pp.1097–1105,
2012.
Isaac E Lagaris, Aristidis Likas, and Dimitrios I Fotiadis. Artificial neural networks for solving
ordinary and partial differential equations. IEEE Transactions on Neural Networks, 9(5):987–
1000,1998.
Isaac E Lagaris, Aristidis C Likas, and Dimitris G Papageorgiou. Neural-network methods for
boundaryvalueproblemswithirregularboundaries. IEEETransactionsonNeuralNetworks,11
(5):1041–1049,2000.
Fernando Díaz Ledezma and Sami Haddadin. First-order-principles-based constructive network
topologies: Anapplicationtorobotinversedynamics. InIEEE-RASInternationalConference
onHumanoidRobotics,2017,pp.438–445.IEEE,2017.
IanLenz,RossAKnepper,andAshutoshSaxena.Deepmpc: Learningdeeplatentfeaturesformodel
predictivecontrol. InRobotics: ScienceandSystems,2015.
KaiLiu, FrankLewis, GuyLebret, andDavidTaylor. Thesingularitiesanddynamicsofastewart
platformmanipulator. JournalofIntelligentandRoboticSystems,8(3):287–308,1993.
ZichaoLong,YipingLu,XianzhongMa,andBinDong. Pde-net: Learningpdesfromdata. arXiv
preprintarXiv:1710.09668,2017.
JohnYSLuh,MichaelWWalker,andRichardPCPaul.On-linecomputationalschemeformechanical
manipulators. JournalofDynamicSystems,Measurement,andControl,102(2):69–76,1980.
KMiller. Thelagrange-basedmodelofdelta-4robotdynamics. Robotersysteme,8:49–54,1992.
VolodymyrMnih,KorayKavukcuoglu,DavidSilver,AndreiARusu,JoelVeness,MarcGBellemare,
AlexGraves,MartinRiedmiller,AndreasKFidjeland,GeorgOstrovski,etal.Human-levelcontrol
throughdeepreinforcementlearning. Nature,518(7540):529,2015.
Duy Nguyen-Tuong and Jan Peters. Using model knowledge for learning inverse dynamics. In
InternationalConferenceonRoboticsandAutomation,pp.2677–2682,2010.
DuyNguyen-TuongandJanPeters.Modellearningforrobotcontrol: asurvey.CognitiveProcessing,
12(4):319–340,2011.
Duy Nguyen-Tuong, Matthias Seeger, and Jan Peters. Model learning with local gaussian process
regression. AdvancedRobotics,23(15):2015–2034,2009.
MaziarRaissiandGeorgeEmKarniadakis. Hiddenphysicsmodels: Machinelearningofnonlinear
partialdifferentialequations. JournalofComputationalPhysics,357:125–141,2018.
MaziarRaissi,ParisPerdikaris,andGeorgeEmKarniadakis.Physicsinformeddeeplearning(parti):
Data-drivensolutionsofnonlinearpartialdifferentialequations.arXivpreprintarXiv:1711.10561,
2017.
Elmar Rueckert, Moritz Nakatenus, Samuele Tosatto, and Jan Peters. Learning inverse dynamics
modelsino(n)timewithlstmnetworks. InIEEE-RASInternationalConferenceonHumanoid
Robotics,pp.811–816.IEEE,2017.
12

PublishedasaconferencepaperatICLR2019
AlvaroSanchez-Gonzalez,NicolasHeess,JostTobiasSpringenberg,JoshMerel,MartinRiedmiller,
RaiaHadsell,andPeterBattaglia. Graphnetworksaslearnablephysicsenginesforinferenceand
control. arXivpreprintarXiv:1806.01242,2018.
StefanSchaal,ChristopherGAtkeson,andSethuVijayakumar. Scalabletechniquesfromnonpara-
metricstatisticsforrealtimerobotlearning. AppliedIntelligence,17(1):49–60,2002.
BrunoSicilianoandOussamaKhatib. Springerhandbookofrobotics. Springer,2016.
DavidSilver,JulianSchrittwieser,KarenSimonyan,IoannisAntonoglou,AjaHuang,ArthurGuez,
Thomas Hubert, Lucas Baker, Matthew Lai, Adrian Bolton, et al. Mastering the game of go
withouthumanknowledge. Nature,550(7676):354,2017.
JustinSirignanoandKonstantinosSpiliopoulos. Dgm: Adeeplearningalgorithmforsolvingpartial
differentialequations. arXivpreprintarXiv:1708.07469,2017.
Mark W Spong. Modeling and control of elastic joint robots. Journal of dynamic systems, mea-
surement,andcontrol,109(4):310–318,1987.
Jo-AnneTing,MichaelMistry,JanPeters,StefanSchaal,andJunNakanishi. Abayesianapproach
tononlinearparameteridentificationforrigidbodydynamics. InRobotics: ScienceandSystems,
pp.32–39,2006.
BenWilliams,MarcToussaint,andAmosJStorkey. Modellingmotionprimitivesandtheirtiming
inbiologicallyexecutedmovements. InAdvancesinNeuralInformationProcessingSystems20,
pp.1609–1616.2008.
KeminZhou, JohnComstockDoyle, KeithGlover, etal. Robustandoptimalcontrol, volume40.
PrenticeHall,NewJersey,1996.
13

PublishedasaconferencepaperatICLR2019
AppendixA:OfflineBenchmarks
10−1
10−2
1 2 4 6 8 10 12 14 16 18 20
TrainCharacters
ESM
OfflineTrainingError
10−1
DeLaN
SI 10−2
FF-NN
1 2 4 6 8 10 12 14 16 18 20
TrainCharacters
(a)
ESM
OfflineTestingError
(b)
Figure 7: The mean squared error averaged of 20 seeds on the training- (a) and test-set (b) of the
charactertrajectoriesforthetwojointrobot. Themodelsaretrainedofflineusingncharactersand
testedusingtheremaining20−ncharacters. Thetrainingsamplesarecorruptedwithwhitenoise,
whiletheperformanceistestedonnoise-freetrajectories.
ToevaluatetheperformanceofDeLaNwithoutthecontroltask,DeLaNwastrainedofflineonprevi-
ouslycollecteddataandevaluatedusingthemeansquarederror(MSE)onthetestandtrainingset.
Forcomparison,DeLaNiscomparedtothesystemidentificationapproach(SI)describedbyAtkeson
et al. (1986), a feed-forward neural network (FF-NN) and the Recursive Newton Euler algorithm
(RNE)usingananalyticmodel. Forthiscomparison,onemustpointoutthatthesystemidentification
approachreliesontheavailabilityofthekinematics,astheJacobiansandtransformationsw.r.t. to
every link must be known to compute the necessary features. In contrast, neither DeLaN nor the
FF-NNrequirethisknowledgeandmustimplicitlyalsolearnthekinematics.
Figure7showstheMSEaveragedover20seedsonthecharacterdatasetexecutedonthetwo-joint
robot. Forthisdataset,themodelsaretrainedusingnoisysamplesandevaluatedonthenoise-free
and previously unseen characters. The FF-NN performs the best on the training set, but overfits
to the training data. Therefore, the FF-NN does not generalize to unseen characters. In contrast,
the SI approach does not overfit to the noise and extrapolates to previously unseen characters. In
comparison, the structure of DeLaN regularizes the training and prevents the overfitting to the
corruptedtrainingdata. Therefore,DeLaNextrapolatesbetterthantheFF-NNbutnotasgoodasthe
SIapproach. SimilarresultscanbeobservedonthecosinedatasetusingtheBarrettWAMsimulated
in SL (Figure 8 a, b). The FF-NN performs best on the training trajectory but the performance
deteriorateswhenthisnetworkextrapolatestohighervelocities. SIperformsworseonthetraining
trajectorybutextrapolatestohighervelocities. Incomparison,DeLaNperformscomparabletothe
SIapproachonthetrainingtrajectory,extrapolatessignificantlybetterthantheFF-NNbutdoesnot
extrapolateasgoodastheSIapproach. Forthephysicalsystem(Figure8c,d),theresultsdifferfrom
theresultsinsimulation. OnthephysicalsystemtheSIapproachonlyachievesthesameperformance
asRNE,whichissignificantlyworsecomparedtotheperformanceofDeLaNandtheFF-NN.When
evaluatingtheextrapolationtohighervelocities,theanalyticmodelandtheSIapproachextrapolate
tohighervelocities, whiletheMSEfortheFF-NNsignificantlyincreases. Incomparison, DeLaN
extrapolatesbettercomparedtotheFF-NNbutnotasgoodastheanalyticmodelortheSIapproach.
This performance difference between the simulation and physical system can be explained by the
underlying model assumptions and the robustness to noise. While DeLaN only assumes rigid-
bodydynamics,theSIapproachalsoassumestheexactknowledgeofthekinematicstructure. For
simulationbothassumptionsarevalid. However, forthephysicalsystem, theexactkinematicsare
unknown due to production imperfections and the direct cable drives applying torques to flexible
joints violate the rigid-body assumption. Therefore, the SI approach performs significantly worse
onthephysicalsystem. Furthermore,thenoiserobustnessbecomesmoreimportantforthephysical
system due to the inherent sensor noise. While the linear regression of the SI approach is easily
corrupted by noise or outliers, the gradient based optimization of the networks is more robust to
noise. ThisrobustnesscanbeobservedinFigure9,whichshowsthecorrelationbetweenthevariance
ofGaussiannoisecorruptingthetrainingdataandtheMSEofthesimulatedandnoise-freecosine
14

PublishedasaconferencepaperatICLR2019
SLBarrettWAM-Cosine0 SLBarrettWAM-Cosine1 BarrettWAM-Cosine0 BarrettWAM-Cosine1
| 103 |     | 103 |     | 103 |     | 103 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
SI
DeLaN
| 102 |     | 102 |     | 102 |     | 102 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
FF-NN
| 101  |          | 101  |          | 101  |          | 101  |          | RNE |
| ---- | -------- | ---- | -------- | ---- | -------- | ---- | -------- | --- |
| ESM  |          | ESM  |          | ESM  |          | ESM  |          |     |
| 100  |          | 100  |          | 100  |          | 100  |          |     |
| 10−1 |          | 10−1 |          | 10−1 |          | 10−1 |          |     |
| 10−2 |          | 10−2 |          | 10−2 |          | 10−2 |          |     |
|      | TestData |      | TestData |      | TestData |      | TestData |     |
| 10−3 |          | 10−3 |          | 10−3 |          | 10−3 |          |     |
1 1.25 1.5 1.75 2 1 1.25 1.5 1.75 2 1 1.25 1.5 1.75 2 1 1.25 1.5 1.75 2
|     | VelocityScale |     | VelocityScale |     | VelocityScale |     | VelocityScale |     |
| --- | ------------- | --- | ------------- | --- | ------------- | --- | ------------- | --- |
|     | (a)           |     | (b)           |     | (c)           |     | (d)           |     |
Figure8: Themeansquarederrorofthecosinetrajectoriesforthesimulated(a,b)andthephysical
Barrett WAM (c and d). The system identification approach, feed-forward neural network and
DeLaNaretrainedofflineusingonlythetrajectoriesatavelocityscaleof1×.Afterwardsthemodels
are tested on the same trajectories with increased velocities to evaluate the extrapolation to new
velocities.
trajectories. Withincreasingnoiselevels,theMSEoftheSIapproachincreasessignificantlyfaster
comparedtothemodelslearnedusinggradientdescent.
Concluding,theextrapolationofDeLaNtounseentrajectoriesandhighervelocitiesisnotasgood
as the SI approach but significantly better than the generic FF-NN. This increased extrapolation
compared to the generic network is achieved by the Lagrangian Mechanics prior of DeLaN. Even
though this prior promotes extrapolation, the prior also hinders the performance on the physical
robot,becausethepriorcannotrepresentthedynamicsofthedirectcabledrives. Therefore,DeLaN
performs worse than the FF-NN, which does not assume any model structure. However, DeLaN
outperformstheSIapproachonthephysicalsystem,whichalsoassumesrigid-bodydynamicsand
requirestheexactknowledgeofthekinematics.
NoiseRobustness
|     |     |     | 101 |     | RNE |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
DeLaN
FF-NN
SI
100
ESM
10−1
10−2
|     |     |     | 10−3 | 10−2 | 10−1 |     |     |     |
| --- | --- | --- | ---- | ---- | ---- | --- | --- | --- |
NoiseVarianceσ2
Figure9: Themeansquarederroronthesimulatedandnoise-freecosinetrajectorieswithvelocity
scale of 1x. For offline training the samples are corrupted using i.i.d. noise sampled from a
multivariateNormaldistributionwiththevarianceofσ2I.
15

PublishedasaconferencepaperatICLR2019
AppendixB:CompleteOnlineResults
PD-Controller
a
RNE
b
c
d
e
g
h
l
m
n
o
p
q
r
s
u
v
w
y
z
FF-NN FF-NN FF-NN FF-NN FF-NN FF-NN FF-NN DeLaN DeLaN DeLaN DeLaN DeLaN DeLaN DeLaN
n = 12 n = 10 n = 8 n = 6 n = 4 n = 2 n = 1 n = 12 n = 10 n = 8 n = 6 n = 4 n = 2 n = 1
Figure10: Thequalitativeperformancefortheanalyticbaselines,thefeedforwardneuralnetwork
andDeLaNfordifferentnumberofrandomtrainingcharacters. Thedesiredtrajectoriesareshown
inred.
16

PublishedasaconferencepaperatICLR2019
Character
a
b
c
d
e
g
h
l
m
n
o
p
q
r
s
u
v
w
y
z
102 101 100 101 102 103
Tracking Error
DeLaN
FF-NN
PD-Controller
RNE
Figure 11: The average performance of DeLaN and the feed forward neural network for each
character. Thecolumnsoftheboxplotscorrespondtodifferentnumbersoftrainingcharacters,i.e.,
n=1,2,4,6,8,10,12.
17