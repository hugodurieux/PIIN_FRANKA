|             | One Model | to        | Drift | Them  | All: | Physics-Informed |               |
| ----------- | --------- | --------- | ----- | ----- | ---- | ---------------- | ------------- |
| Conditional |           | Diffusion |       | Model | for  | Driving          | at the Limits |
FranckDjeumou1,2,ThomasLew1,NanDing1,MichaelThompson1,
MakotoSuminaka1,MarcusGreiff1,andJohnSubosits1
|     | 1Toyota   | Research                                                     | Institute,2Rensselaer |     |     | Polytechnic | Institute |
| --- | --------- | ------------------------------------------------------------ | --------------------- | --- | --- | ----------- | --------- |
|     | Abstract: | Enablingautonomousvehiclestoreliablyoperateatthelimitsofhan- |                       |     |     |             |           |
dling—wheretireforcesaresaturated—wouldimprovetheirsafety,particularly
|     | in scenarios | like emergency |     | obstacle avoidance |     | or adverse weather | conditions. |
| --- | ------------ | -------------- | --- | ------------------ | --- | ------------------ | ----------- |
However,unlockingthiscapabilityischallengingduetothetask’sdynamicna-
tureandthehighsensitivitytouncertainpropertiesoftheroad,vehicle,andtheir
|     | dynamicinteractions. |     | Motivatedbythesechallenges,weproposeaframeworkto |     |     |     |     |
| --- | -------------------- | --- | ------------------------------------------------ | --- | --- | --- | --- |
learnaconditionaldiffusionmodelforhigh-performancevehiclecontrolusingan
unlabelleddatasetcontainingtrajectoriesfromdistinctvehiclesindifferentenviron-
|     | ments. Wedesignthediffusionmodeltocapturethecomplexdataset’strajectory |     |     |     |     |     |     |
| --- | ---------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
distributionthroughamultimodaldistributionofparametersofaphysics-informed
|     | data-drivendynamicsmodel. |     |     | Byconditioningthegenerationprocessononline |     |     |     |
| --- | ------------------------- | --- | --- | ------------------------------------------ | --- | --- | --- |
measurements,weintegratethediffusionmodelintoareal-timemodelpredictive
controlframeworkfordrivingatthelimits,andshowthatitcanadaptontheflyto
|     | agivenvehicleandenvironment. |     |     | ExtensiveexperimentsonaToyotaSupraand |     |     |     |
| --- | ---------------------------- | --- | --- | ------------------------------------- | --- | --- | --- |
aLexusLC500showthatasinglediffusionmodelenablesreliableautonomous
driftingonbothvehicleswhenoperatingwithdifferenttiresinvaryingroadcondi-
|     | tions. Themodelmatchestheperformanceoftask-specificexpertmodelswhile |     |     |     |     |     |     |
| --- | -------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
outperformingthemingeneralizationtounseenconditions,pavingthewaytowards
ageneral,reliablemethodforautonomousdrivingatthelimitsofhandling.
|     | Keywords: | DiffusionModels,LearningforControl,AutonomousDrifting. |     |     |     |     |     |
| --- | --------- | ------------------------------------------------------ | --- | --- | --- | --- | --- |
Figure1: Left: Examplesoftheconditionaldiffusionmodelperformingdriftingtrajectoriesontwo
vehicles. Right: Overview of the controller architecture and online model parameter generation
Thevideosoftheexperimentscanbefoundathttps://tinyurl.com/diff-drift.
process.
1 Introduction
Existingautonomousvehiclesareconstrainedtooperateatafractionoftheirfullhandlingpotential.
Designingalgorithmstoreliablycontrolvehiclesbeyondtheseengineeredlimitswouldunlockfaster
8thConferenceonRobotLearning(CoRL2024),Munich,Germany.

and more reliable responses to diverse safety-critical situations [1, 2] such as driving on ice and
avoidingsuddenobstacles,scenarioswherethevehiclemayusealloftheavailabletire-roadfriction,
causingittoslideacrosstheroad[3,4,5]. However,drivingatthelimitsofhandlingischallenging
duetothetask’sdynamicnature,thehighsensitivitytomodelmismatch,andtheuncertainproperties
of the road, the vehicle, and their dynamic interactions. In addition, the high cost of collecting
a dataset for driving at the limits, the complex vehicle dynamics, and the safety considerations
complicatetheuseofimitationlearningandreinforcementlearningstrategies. Thesechallenges
motivatethedevelopmentofamodelcapableofexploitingphysicsknowledgeandcapturingcomplex
formsofuncertaintieswhilebeingamenabletoreal-timeautonomousvehiclecontrol.
Diffusion models [6, 7, 8, 9] have shown to be highly capable of representing complex, high-
dimensional,andmultimodaldistributionsfromdata. However,theirdirectusefordrivingatthe
limitsisnotstraightforward. Thelimitationsofclassicaldiffusionmodelsincludethequestionof
how to leverage prior physics knowledge to improve data efficiency and interpretability, and the
considerablemodelinferencetime,whichcanbeabottleneckforhigh-bandwidthcontrol.
Contribution. Weproposeaconditionaldiffusionvehiclemodelforcontrol-orientedmodelingof
driving at the limits of handling under uncertainties. By predicting the parameters of a physics-
informedneuralstochasticdifferentialequationdynamicsmodel,themodelhasfourkeyproperties.
Byencodingpriorphysicsknowledgeasaninductivebias,theproposeddiffusion-basedvehicle
•
modelisinterpretableandgeneralizestonewenvironmentsfromsmallamountsofdata.
Themodelcancapturecomplexmultimodaldistributionsoverthevehiclemodel’sparameters.
•
Themodelcanadaptontheflytovarioustest-timevehiclesandroadconditionsbyconditioning
•
onmeasurementsofthevehicle’sinteractionwiththeworld.
Bypredictingtheparametersofaphysics-basedmodel,asopposedtodirectlypredictingstate
•
trajectories,themodelinferenceandcontrolloopsaredecoupled. Thishierarchicalapproach
unlocksdiffusionsamplingatlowratesandhigh-frequencypredictivecontrol.
Weintegratethediffusionmodelinareal-timenonlinearmodelpredictivecontrolframeworkfor
autonomousdrivingatthefrictionlimits,andextensivelyvalidateitonaToyotaSupraandaLexus
LC500. Ourresultsshowcasethatasinglediffusionmodelcanreliablycontrolbothvehicleson
challengingdriftingtasksinvolvingdifferentroadconditionsandvehicleproperties,seeFigure1.
2 Relatedwork
Several works have explored autonomous driving at the limits of handling, both in the context
ofracing [10, 11, 12, 13]and drifting[14, 5, 4, 15]. Thesemethodsidentifythe parametersofa
physics-basedvehicledynamicsmodel[16,17,4,18,19]ortrainaneuralnetworkmodel[15,20],
andsubsequentlyuseitformodel-basedoptimalcontrol. Nonlinearmodelpredictivecontrol(MPC)
isthego-tocontrolstrategyinsuchsettingsandhasdemonstratedhigh-performancetrackingability
inchallengingracinganddriftingtasks[12,11,4,15]. However,theperformanceofMPCislimited
bythefidelityofthevehiclemodel,designedtocaptureasinglevehiclewithgiventiresoperatingin
specificroadconditions.Incontrast,usinganunlabeledtrajectorydataset,wetrainasinglegenerative
vehiclemodelwithonlineadaptationcapabilitiesthatenableautonomousdrivingatthelimitsof
handlingondifferentvehiclesinvaryingroadconditions.
Diffusionmodelshaveemergedasapowerfultoolforgeneratingcomplexandmultimodaldistri-
butionsincontinuousdomainssuchasimages[21,22],3Dcontents[23,24],planningandcontrol
[25,26,27,28,29,30,31],timeseries[32,33],andphysicsprocesses[34,35,36]. However,all
theseworkslearntorepresent,inablack-boxmanner,distributionsforwhichsamplesaredirectly
availableinthetrainingdata. Incontrast, wetrainadiffusionmodeltogeneratesamplesfroma
latentspaceofvehicledynamicsparametersthatarenotinthetrainingdata. Ourapproachrelates
to research in latent diffusion models [23, 37]. But instead of learning encoder and decoder net-
workstomapbetweenthedataandlatentspaces,weimposeastructureonthelatentspacethrough
physics-informedneuralstochasticdifferentialequations.
Neuralordinarydifferentialequations[38,39,40,41,42],Koopmanoperators[43,44,45,46,47,48],
classicalsystemidentification[49,50,51,52,53],Gaussianprocesses[54,55,56,57,58],andneural
stochasticdifferentialequations(SDEs)[59,60,61,62,63]havebeenwidelystudiedformodeling
uncertaindynamicalsystemsfromdata. Thesemodelsareeitherdeterministicorcancaptureonlya
2

singlemodeofthetrainingdataset’sdistribution,alongwiththeuncertaintyaroundthemode. Onthe
otherhand,Bayesianinferenceontheparametersofsomeofthesemodelscan,intheory,capturethe
multimodaldistributionofthemodelparameters. However,classicalMonteCarlo-basedmethods
[64,65,66,67]donotscalewellwithlargemodelsanddatasets,whilevariationalinference-based
methods[68,69,70]arelimitedbythechoiceofvariationalfamilyusedtoapproximatemultimodal
posteriors. Toaddresstheselimitations,recentworks[71,72,73,36]havehighlightedthescalability
and expressivity of diffusion models when approximating the posterior distribution in Bayesian
inference. Weleveragesuchexpressivitytocaptureamultimodaldistributionovertheparametersof
avehiclemodelexpressedasaneuralSDE:Amodelshownin[63]toimprovelong-termprediction
accuracyanduncertaintyestimatecomparedtodeepGaussian-basedmodels[74,75].
Ourmodelingapproachissimilartometa-learningmethods[76,77,78]sincethediffusionmodel
learnsofflinetopredicttheparametersofaneuralSDEmodelwhileadaptingonlinetodifferent
vehiclesandenvironmentconditions.However,incontrasttoexistingmeta-learningapproacheswhere
thedatasethastask-specificlabels,wetrainourmodelfromanunlabeleddatasetofvehicletrajectories.
Inaddition, whileconditioningtheoffline-traineddiffusionmodelenablesonlineadaptation, we
emphasizethatnogradientupdatesoranysortofregressiononthemodelparametersareperformed
onlineforadaptation,asistypicallydoneinmeta-learningoronlinelearning[79,80,81,82,83].
3 Method
Weassumeaccesstoadataset = τ ,...,τ ofvehicletra-
1 |T|
T { }
jectories τ = (x ,u ),...,(x ,u ) , where each (x ,u )
{
t0 t0 t|τ| t|τ|
}
t t
denotesastate-controlpair. Wedenotebyx =[x ,...,x ]
t:Tf t t+Tf
andu = [u ,...,u ]thefuturestateandcontrolsequence
t:Tf t t+Tf
fromtimettotimet+T ,andbyx andu thepastsequence
f Tp:t Tp:t
fromt T tot. Wealsouseτ ,τ ,andτ todenote
− p t:Tf Tp:t Tp:t:Tf Figure2: Trajectoriesin .
thefuture, past, andfullsequenceofstate-controlpairsattimet, T
respectively. Weconsiderthatthedataset’strajectoriesmaybecollectedfromvehicleswithdifferent
physicalandtirespecifications,andoperatingonvariousroadconditionswhileperformingdifferent
tasks. Thus,thedistributionoveritstrajectoriesiscomplexandchallengingtomodel. Thedataset
is also characterized as unlabelled since no information (per trajectories) about the vehicles and
environmentsisprovidedformodelidentificationotherthanthestate-controlpairs.
Wepresentourapproachtolearningphysics-constrainedgenerativemodelsforautonomousdriving
atthelimits. Themainideaistointegratethestructureandtheexistingphysicsknowledgeofdriving
atthelimitsintothedesignofaneuralSDEmodelparametrizedbyθ. Then,wetrainastate-control
historyconditioneddiffusionmodel,parameterizedbyψ,tooutputadistributionp (θ x ,u )
ψ
|
Tp:t Tp:t
over the neural SDE parameters θ, which is then used to generate the future state trajectories or
modelstousebyanMPCcontroller. However, existingapproachestotrainingdiffusionmodels
cannotbedirectlyappliedhereastheywouldrequireunavailableaccesstoadatasetofneuralSDE
parameters. Theproposedapproach(Section3.1)generatessuchadatasetandconsistentlyimproves
itsparameterswithrespecttothetrajectoriesin whilesimultaneouslytrainingthediffusionmodel.
T
Neural SDEs for modeling. Neural SDEs [84, 85, 59, 60, 63] offer a principled approach for
modelinguncertaindynamicalsystemsduetotheirabilitytoencodepriorphysicsknowledgefrom
firstprinciples,theircalibrateduncertainties,andtheirexpressivenessfromusingneuralnetworks:
dx=fθ(x,u)dt+Σθ(x,u)dW, (1)
where x Rnx is the state, u Rnu is the control input, t is the time, W is the
n
x
-thdim ∈ en X sion ⊆ alWienerprocess,and ∈ fθU : ⊆
X ×U →
Rnx andΣθ :
X ×U →
Rn
+
x×nx arethe
parametrizeddriftanddiffusionterms,respectively,andtheequationisinterpretedasanSDEinthe
Itôsense. Undersmoothnessassumptions[86,87]onfθ,Σθ,wecanefficientlysampleadistribution
ofpredictedtrajectoriesvianumericalintegrationoftheneuralSDE[88,89]. Assumingapproximate
GaussiantransitionsbetweendiscretetimesofanumericalSDEintegrator,thenegativelog-likelihood
(NLL)lossofastatesequencex giventhecontrolsu canbeestimatedby
t:Tf t:Tf
(cid:20) (cid:21)
(θ,τ ):=E (cid:88)t+Tf x x˜θ 2 +log (cid:0) det (cid:0) Σθ(cid:1)(cid:1) , (2)
J nll t:Tf x˜θ t:Tf s=t (cid:107) s − s(cid:107)(Σθ s )−1 s
with
(cid:107)
z
(cid:107)
2
A
:=z(cid:62)Azforz
∈
Rnx,A
∈
Rnx×nx,andwhereΣθ
s
:=Σθ(x˜θ
s
,u
s
)andx˜θ
t:Tf
isasample
sequenceobtainedfromtheSDEintegrationforafixedθandtheinitialconditionsx andu .
t t:Tf
3

Algorithm2OnlineMPCModelSampling
Algorithm1TrainingoftheDiffusionModelψ
2 1 : : C In o it m ia p li u z t e e D θlo = cb ∅ y . solving(3)usingSGD. 1 2 : : I I n n i i t t i i a a l l i i z z e e h b i e s s t t o p ry ar d a a m ta e s te e r t s T θ h 1 is , t . = .., ∅ θ . nbest.
3: whilenotterminateddo
3: whilenotconvergeddo
6 4 5 : : : S S if a a R m m e p p fi l l n e e e τ { T t τ h T p e : p t n : : t T k f :T f f ro } m k a T ro . undτ Tp:t:Tf . 4 5 : : sub A T s g p e e t p n s e ← o n f d T l { a h τ t i e T st s p t :t ( k x } t k , , u T t v ) a t l o ← T hi { s τ t . tj:Tf} j are
1 1 7 8 9 0 1 : : : : : e O A U n p p p d U t p d i e a p m if n t d e i d a z ψ t e ( e τ f u θ T o s l r p o i : n c θ t g , t w θ u ( i t 5 t s ) h ) in t o p o g n ψ D ( ( b 4 · . a ) | h t a c ( n h τ d e T s θ p f : l t o r ) o c ) . m . . 6 7 8 9 : : : : { θ t E { U S k θ e v p } t n a d k k d l a } u ∪ θ t k a e b t { e ∼ e Θ s θ t p = s p : } = c ψ n p a o = ( b r r { · e g e 1 | s θ { m s t p . τ } i T J n n p p t = b r : a t e 1 t j k s r ( t a } θ j ( w k , θ ) T i , t v u h a v s l a b i ) n l e ) g s f t t o o ( s 7 r M c ) o . θ P re C s ∈ . .
12: endwhile D θ∈Θ J T
10: endwhile
3.1 Conditioneddiffusionmodelinparameterspace
WeprovidethemainstepsofthetrainingprocessbelowandsummarizetheminAlgorithm1.
Initial estimate of the neural SDE parameters. First, we compute the maximum a posteriori
estimateoftheneuralSDEparametersθovertheentiredataset . Thetrainingproblemisgivenby
T
θloc ← argmin θJ traj (θ, T ),with J traj (θ, T ):= E (τt:Tf ∼T) (cid:2) J nll (θ,τ t:Tf ) (cid:3) +λ traj R (θ), (3)
where isthenegativelog-likelihooddefinedin(2),andτ isasampledtrajectoryfromthe
nll
J ∼T
dataset. Thetermλ controlstheregularizationterm (θ)thatenforcesavailablepriorknowledge
traj
R
ontheneuralSDEparameters;seeAppendixA.4fordetailsonthedesignchoicesinthissection.
Parameterdatasetgenerationvialocaloptimization. Next,weusetheestimateθloctoiteratively
generateadataset = (τ ,θ ),... ofshortstate-controltrajectoriesτ andmodelparameters
D {
Tp:t t
}
Tp:t
θ thatareconsistentwith(a)thedatasequenceτ ,(b)theimmediatefuturesequenceτ ,and(c)
t Tp:t t:Tf
additionalsequencesτ inaneighborhoodoftheinitialdatasequenceτ . Thetimesteps
t aresampledfromau T n p i : f t o k r :T m f distributionUoffixedwidthcenteredatt.Thelo T c p a : l t: o T p f timalparameter
k
θ thatisaddedtotheparametersdataset isgivenbyθ =argmin (τ ,θ,θloc)with
t D t θJ loc Tp:t
J loc (τ Tp:t ,θ,θloc):= J nll (θ,τ t:Tf )+E tk∼U (t−W,t+W) (cid:2) J nll (θ,τ Tp:tk:Tf ) (cid:3) +λ loc (cid:107) θ − θloc (cid:107) 2, (4)
where the term in λ regularizes θ to be close to the estimate θloc. The additional sequences
loc
τ help refine the uncertainty estimates of the neural SDE model. Using short sequences
τ
Tp:tk:Tf
,witht inasmalltimewindowW R aroundt,helpsensurethattheycanbeexplained
Tp:tk:Tf k
∈
+
byasingleparametervectorθ ,sincepropertiesofthesystemmayotherwisevaryoveratrajectory
t
τ ifτ istoolong. Weoptimizeforθ usinggradientdescenton(4)startingfroman
Tp:t:Tf Tp:t:Tf t
initialguesssampledfromaGaussiandistributioncenteredatθloc. Wefoundthatregularizingtothe
estimateθlocintheobjective(4)stabilizestheoptimizationprocess.
Training the diffusion model. Given the generated neural SDE parameters in , we update the
D
parametersψofourconditionaldenoisingdiffusionmodelwithgradientdescentasin[7],onaloss
J DM (ψ)=E (θt,τTp:t)∼D,(cid:15)∼N(0,I),k∼U (1,K) (cid:2) (cid:107) (cid:15) ψ (√γ k θ t + (cid:112) 1 − γ k (cid:15),k,h(τ Tp:t )) − (cid:15) (cid:107) 2(cid:3) , (5)
whereγ :=
(cid:81)k
(1 β )withβ (0,1)beingalinearnoisescheduletograduallydistortthe
k i=1 − i i ∈
parametersdataset , (0,I)isthestandardnormaldistribution,K isthenumberofdiffusionsteps,
D N
and(cid:15) isthedenoisingneuralnetworkpredictingthenoise(cid:15)addedduringthenoisingprocess. Here,
ψ
hisafunctionthatmapsthehistoryτ toafeaturespaceforconditioningthediffusionmodel:
Tp:t
h(τ )=[∆x ∆t−1 ,u ], with∆x =[x x ,...,x x ], (6)
Tp:t Tp:t Tp:t Tp:t Tp:t Tp+1 − Tp t − t−1
and∆t−1 =[(t t )−1,...,(t t )−1]. WeuseK =1000noisingstepsasin[7].
Tp:t Tp+1 − Tp t − t−1
Iterativelyrefiningtheparameterdataset. Asthediffusionmodeltrainingprogresses,itspredic-
tionsofthelocalparametersθ becomemoreaccuratewhiletheinitialestimateθloccomputedin(3)
t
4

maybecomeasuboptimalinitialguessforθ . Thus,aftersomenumberofdiffusiontrainingsteps,
t
weusethegenerativemodeltorefinethedataset bysamplinganeuralSDEparameterthatwould
D
serveasaninitialestimateθlocandaregularizer forthelocaloptimizationproblem(4).
Onlinediffusionmodelinference.
Algorithm2outlinesasimpleonlinestrategyforsamplingthe
neuralSDEparametersconditionedononlinemeasurements. Thealgorithmmaintainsthehistory
ofstate-controlpairsandusesitasasourceforgenerating,validating,andscoringtheneuralSDE
parameters. Ateachtimestepofthealgorithm,aset ofstate-actionsequencesissampledfrom
T gen
thehistorydataset togenerateasetofparametersθ conditionedoneachτ . Thisis
|     |     | h is t |     |     |     |     | t   |     |     | T p :t g e n |     |
| --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | ------------ | --- |
|     |     | T      | ¯   |     |     |     | ¯   |     | ¯   | ∈ T          |     |
doneinK steps,by sa m plingθ K (0,I)andrefining θ k−1 (µ ψ (θ k ,k,h ( τ Tp:t ) ) , σ k I)with
|     |      |     |       | ∼N          |     |     |         | ∼N  |             |           |     |
| --- | ---- | --- | ----- | ----------- | --- | --- | ------- | --- | ----------- | --------- | --- |
|     |      | 1 γ | k−1   |             |     | 1   | (cid:0) | β   | k           | (cid:1)   |     |
|     | σ =β | −   | ,andµ | (θ ¯ ,k,z)= |     |     | θ ¯     |     | (cid:15) (θ | ¯ ,k,z) , | (7) |
|     | k    | k 1 |       | ψ k         |     | √1  | k       | √1  | ψ           | k         |     |
|     |      |     | γ k   |             |     |     | β k     | −   | γ k         |           |     |
|     |      | −   |       |             |     | −   |         | −   |             |           |     |
=θ ¯
beforelettingθ t 0 . Finally,aset val hist issampledandusedtovalidatethegeneratedparam-
|     |     |     |     | T ⊆T |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
etersandcomputetheirscores,definedastheloss (θ, val )in(3)plusa2-normregularization
|     |     |     |     |     |     | J traj | T   |     |     | nbest. |     |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | ------ | --- |
termthatpenalizesthedistancetothen =5bes tprevio uslygeneratedparameters θp We
|     |     |     |     | best |     |     |     |     |     | { }p=1 |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | ------ | --- |
foundthatthislasttermhelpsensureconsistentupdatesduringtheonlineinferenceprocess.
3.2 Applicationtoautonomousdrivingatthelimitsofhandling
Physics-constrained neural SDE model. We now introduce the uncertainty-aware and physics-
constrainedneuralSDEmodelfordrivingatthelimitsofhandling. Weemploythecommonlyused
single-trackmodel[90,16,91,18,17]asafoundationtodescribethenonlineardynamicsofthe
vehicle. Thevehiclepositionisexpressedinacurvilinearcoordinatesystemrelativetoareference
trajectory [14,19,12]. Specifically,thepositioncoordinateisdescribedbythedistancesalongthe
referencetrajectory,therelativeheading∆φwithrespecttoareferenceheadingφ ,andthelateral
ref
| deviationefromthepath. |     |     | TheproposedneuralSDEmodelisgivenby |     |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | ---------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|                        |     |     | dx=Mθ(x,u)Fθ(x,u)dt+Σθ(x,u)dW,     |     |     |     |     |     |     |     | (8) |
wherepriorknowledgecomesfromthematrixMθ(, )thatdependsonvehicleparameterssuchas
· ·
themassmθ,yawmomentofinertiaIθ,rotationalinertiaofthedrivetrainIθ,tireradiusRθ,and
|     |     |     |     | z   |     |     |     |     | w   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
distancesfromthecenterofgravitytothefrontandrearaxlesaθandbθ. Thecontrolinputu=[δ,τe]
|                                                 |     |     |     |     |     | Thestatex=[r,V,β,ω |     |     | ,e,∆φ,s]includesthe |     |     |
| ----------------------------------------------- | --- | --- | --- | --- | --- | ------------------ | --- | --- | ------------------- | --- | --- |
| isthesteeringangleandenginetorque,respectively. |     |     |     |     |     |                    |     |     | r                   |     |     |
yawrater,velocityV,sideslipangleβ,rearwheelspeedω r ,lateralerrore,andangulardeviation
∆φ. Lastly,Fθ =[Fθ ,Fθ ,Fθ ,Fθ ]representsthetireforcesbetweenthevehicleandtheroad.
|     |     | xf  | yf  | xr yr |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
TheseunknowntireforcesFθ
arelearnedasfunctionsofthestateandcontrolinputs.
Modeling the dynamic interaction between the tires and the uncertain road surface is crucial for
accuratelycontrollingavehicleatthelimitsofhandling. Todoso,weincorporateintoourneural
SDEmodelaversionoftheneural-ExpTanhtiremodel[15],aphysics-informedneuraltiremodel
that captures the nonlinearities and saturation effects of tire forces, and that has shown to better
predict tire forces than previous models used in the literature. We refer to Appendix A.1 for the
derivationsofMθ(,
)andtheneuraltireforcemodelsusedintheexperiments.
|     |     | · · |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Modelpredictivecontrol(MPC)forautonomousdrifting. TheMPCtracksareferencetrajectory
underactuatorandactuatorrateconstraintsbysolvingateachtimettheoptimizationproblem
|     |        | (cid:104)(cid:88)H |     |          |       |     |        | 2       | 2    | e2 (cid:105) |      |
| --- | ------ | ------------------ | --- | -------- | ----- | --- | ------ | ------- | ---- | ------------ | ---- |
| min | im ize | E                  |     | Q (β ¯ β | )2+Q  |     | e¯2 +Q | ∆¯ φ +Q | δ ˙  | +Q τ˙        | (9a) |
|     |        | x¯1:H+1            |     | β k      | ref,k | e   | k      | φ k     | δ˙ k | τ˙ k         |      |
| u¯0 | :H     |                    | k=1 | −        |       |     |        |         |      |              |      |
subjectto x¯ =SDESolve(x¯ ,u¯ ;θ ) k =0,...,H,x¯ =x , u¯ ,u¯˙ ¯ (9b)
|     |     | k+1 |     | k k | best |     |     | 0 t | 0:H | 0:H |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | ∀    |     |     |     | ∈U  | ∈U  |     |
wherex isthestateattimestepk,x¯ denotesthestatetrajectoryoverthepredictionhorizon
|     | k   |     |     | 1:H+1 |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
oflengthH +1,andu¯ arethecorrespondingcontrolsignals. SDESolveisanydifferentiable
0:H
SDEintegrationscheme,inourcaseasimpleEuler–Maruyamamethod,parameterizedusingthe
Thestatesx¯
bestparametersθ best foundbyAlgorithm2. 1:H+1 arethusrandomvariables,andthe
expectation in (9a) is evaluated using Monte Carlo. We use 2 particles in our experiments. The
systemisactuatedbyu =u¯(cid:63),whereu¯(cid:63)istheoptimalsolutionto(9)constrainedwithx¯ =x .
|     |     | t   | 0   | 0   |     |     |     |     |     | 0   | t   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
4 Results
Wevalidatetheproposedframeworkontwovehiclesinscenarioswithdifferenttires,operatinggears,
androadconditions. First,weverifythecapabilitiesoftheconditionaldiffusionmodeltocapturethe
5

complexityoftheunlabelleddatasetandadaptitspredictionsonline(Section4.1). Second,weshow
thatthemodelcanadapttodifferenttires(Section4.2). Third,wedemonstratethehighperformance
ofthemethodindiversescenarios(Section4.3). Finally,usingasmallamountofdatacollectedon
wetsurfaces,weshowthattheframeworkenablesdriftingatthelimitsofhandlinginheavyrain
| (Section4.4). | WeprovidefurtherdetailsontheexperimentsinAppendixA. |     |     |     |     |     |
| ------------- | --------------------------------------------------- | --- | --- | --- | --- | --- |
Experimentalvehicles. WedeploytheapproachonaToyotaSupraandaLexusLC500,asshownin
Figure1. TheSupraismodifiedwithamorepowerfulengineandmoreresponsiveactuators,whereas
theLexusiskeptwithfactorysettings,makingitaparticularlychallengingplatformforautonomous
drifting. Thetwovehicles’largedifferencesindynamicsresponsesmakethemidealplatformsfor
evaluatingtherobustnessandgeneralizationcapabilitiesofourapproach. Forbothvehicles,weuse
onboardvehiclestateestimationusingaGPSandIMU,andweusetheCPUofaruggedizedPCto
runthediffusionmodelinferenceat2HzandcomputecontrolinputsusingMPCat200Hz.
| Training | dataset. | We train | the diffusion | model on a |     |     |
| -------- | -------- | -------- | ------------- | ---------- | --- | --- |
totalof84manualandautonomousdrivinganddrifting
| trajectoriesfromthetwovehicles. |            |        | Thedurationofeach |             |     |     |
| ------------------------------- | ---------- | ------ | ----------------- | ----------- | --- | --- |
| trajectory                      | is between | 10 and | 90 seconds.       | It consists |     |     |
of5manualdrivingtrajectoriespushingthecartothe
limitsofhandling,whereastheremainingtrajectoriesare
autonomousdriftingexperimentscomprisingoffailed
and successful attempts. The dataset includes driving Figure3: Datasetformodeltraining.
dataindifferentgears(affectingtheeffectivenessofthe
throttleinput)andusingtireswithdifferentphysicalproperties(affectingthevehicle’sdynamicsand
steeringinputeffectiveness). ThecompositionofthedatasetissummarizedinFigure3.
Baselines. We compare with neural SDE dynamics models (referred to as BaseSDE or Expert
dependingoncontext)trainedonspecificvehicle-tire-gearsubsetsofthedatasetinFigure3. Each
baseline is trained with the loss function in (3) and a regularization term (θ) encoding prior
R
knowledgeabouttheparameters(m,a,b,I ,I ,R). TheresultingmodelsareExpertsincetheyare
|     |     |     |     | z w |     |     |
| --- | --- | --- | --- | --- | --- | --- |
optimizedforspecificscenarios,buttheymayperformpoorlywhendeployedindifferentconditions.
4.1 Multimodalityandconditioningcapabilitiesofthediffusionmodel
Weconditionthemodelontwotrajectoriesfromthe
|     | Grip  |     |     | Lexusvehicledataset(seeFigure3),wherethevehi-    |     |     |
| --- | ----- | --- | --- | ------------------------------------------------ | --- | --- |
| 3   | Slide | 1.5 |     | cleiseitheracceleratinginastraightline(gripping) |     |     |
ytisneD
| 2   |     | 1.0 |     | ordrifting(sliding). | InFigure4,wereporttwopre- |     |
| --- | --- | --- | --- | -------------------- | ------------------------- | --- |
dictedparameters(Iθ,cθ)correspondingtotherear
w 1
| 1   |     | 0.5 |     | wheelinertiaandthemaximumtotalforcethatcan |     |     |
| --- | --- | --- | --- | ------------------------------------------ | --- | --- |
begeneratedbythereartires;seeAppendixA.1. By
| 0   |     | 0.0 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
2 0 2 0 1 2 3 conditioningonthestraight-line(grip)trajectory,the
| −   | ∝logIw | ∝logmaxrearforce |     |     |     |     |
| --- | ------ | ---------------- | --- | --- | --- | --- |
modelreturnsamultimodalparameterdistribution
Figure4: Parameterdistributionpredictedby duetothelackofinformationabouttirefrictionprop-
thediffusionmodel,whenconditionedongrip- erties,astireforcesarenotsaturated. Interestingly,
pingandslidingtrajectories. byconditioningonatrajectorywherethevehicleis
slidingandtireforcesaresaturated,themodelpre-
dictsatightunimodaldistributionoftheparameters. Theleftmodeofthetwoparametersfromthe
grippingphasehascollapsedduetosufficientinformationtoinfervehicleproperties. Thisexample
showsthattheproposedconditionaldiffusionmodelcapturesmultimodalparameterdistributionsand
adaptsitspredictionsbasedontheinformationcontainedinthetrajectory.
4.2 Onlineadaptationtodifferenttires
Wefurtherhighlightthegeneralizationcapa- Table1: Trackingerror: Lexuswithtirestype2.
bilityoftheproposedmethodbystudyingthe
|     |     |     |     |     | Donut | Figure-8 |
| --- | --- | --- | --- | --- | ----- | -------- |
closed-looptrackingperformanceoftheLexus RMSE e(m) β(deg) e(m) β(deg)
whenoperatingwithvarioustires. Wereport Expert(Tires2) 0.35 4.08 0.32 5.17
BaseSDE(Tires3)
| trackingperformanceontworeferencetrajec- |          |                |       |                     | spin spin | spin spin  |
| ---------------------------------------- | -------- | -------------- | ----- | ------------------- | --------- | ---------- |
|                                          |          |                |       | BaseSDE(Tires2&3)   | 0.51 4.52 | 1.39 13.63 |
| tories in                                | Table 1. | The controller | using | the                 |           |            |
|                                          |          |                |       | Diffusion(Tires2&3) | 0.31 4.19 | 0.56 5.38  |
Expertmodelaccuratelytracksthereference
trajectory. Incontrast,usingthebaselinetrainedonlyontype3tiredataisinsufficienttotrackthe
6

| 40  |     |     |     | 20  |     |     | 40  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
30
| ]m[tsaE 20 |     |     |     | ]m[tsaE |     | ]m[tsaE |     |     |     |     |
| ---------- | --- | --- | --- | ------- | --- | ------- | --- | --- | --- | --- |
|            |     |     |     | 10      |     |         | 20  |     |     |     |
| 0          |     |     |     |         |     |         | 10  |     |     |     |
Start
|              |     |                 |     | 0        |       |     | 0   |       |     |          |
| ------------ | --- | --------------- | --- | -------- | ----- | --- | --- | ----- | --- | -------- |
| −20 North[m] |     |                 |     | North[m] | Start |     |     | Start |     | North[m] |
| −20          | 0   | 20 40 60 80 100 |     | −20 −10  | 0     |     |     | −20   | 0   | 20 40    |
14
| ]s/m[V 16 |     |     |     | Reference | Diffusion |     | 16  |     |     |     |
| --------- | --- | --- | --- | --------- | --------- | --- | --- | --- | --- | --- |
| 14        |     |     | 12  | Expert    |           |     | 14  |     |     |     |
10
| 12     |     |     |     |     |     |     | 12  |     |     |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 50     |     |     | 0   |     |     |     | 50  |     |     |     |
| 25     |     |     |     |     |     |     | 25  |     |     |     |
| ]ged[β |     |     | −15 |     |     |     |     |     |     |     |
| 0      |     |     |     |     |     |     | 0   |     |     |     |
−30
| −25 |     |     |     |     |     |     | −25 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| −50 |     |     | −45 |     |     |     | −50 |     |     |     |
1.0
| 2    |     |     |     |     |     |     | 1   |     |     |     |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ]m[e |     |     | 0.5 |     |     |     |     |     |     |     |
| 1    |     |     |     |     |     |     | 0   |     |     |     |
0.0
| 0   |     |     |     |     |     |     | −1  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
−0.5
150 200 250 300 350 400 450 150 200 250 300 350 200 300 400 500 600
|     | Distancealongpath[m] |     |     | Distancealongpath[m] |     |     |     | Distancealongpath[m] |     |     |
| --- | -------------------- | --- | --- | -------------------- | --- | --- | --- | -------------------- | --- | --- |
Figure5: DriftingtheSupra: performancecomparisonbetweentheExpertandDiffusionmodels.
reference,andleadstospinningout. Thisbaselinefailstoinitiatethedrift,duetodifferencesinthe
corneringstiffnessbetweenthetwotiresleadingtoapoorpredictionofhowfastthevehiclewill
saturatethereartires. TheBaseSDEmodeltrainedondatawithtype2andtype3tirescandriftwith
ahighertrackingerror. Onthedonuttrajectory,thisbaselinedriftsonacirclewithalargerradius
duetoatireforcemodelingmismatch. Finally,thediffusionmodelquicklyinfersthetireproperties,
whichresultsinadaptivetrackingperformancethatmatchesExpertperformance.
4.3 Driftingperformanceindifferentscenarios
Weevaluatetheframeworkonarangeofscenarios,includingreferencetrajectoriesthatarenotinthe
dataset,andcompareitsperformancewithanExperttrainedontherelevantsubsetofthedataset.
| Drifting | results | on the Toyota           | Supra. |         |                                |     |              |     |                 |     |
| -------- | ------- | ----------------------- | ------ | ------- | ------------------------------ | --- | ------------ | --- | --------------- | --- |
|          |         |                         |        | Table2: | TrackingerrorontheToyotaSupra. |     |              |     |                 |     |
| We       | report  | performance in tracking |        | dif-    |                                |     |              |     |                 |     |
|          |         |                         |        |         | Slalom(gear2)                  |     | Donut(gear1) |     | Figure-8(gear2) |     |
ferent reference trajectories in Figure 5 RMSE e(m) β(deg) e(m) β(deg) e(m) β(deg)
|            |     |                          |     | Expert    | 0.74 | 5.03 | 0.31 | 3.32 | 0.32 | 3.40 |
| ---------- | --- | ------------------------ | --- | --------- | ---- | ---- | ---- | ---- | ---- | ---- |
| andTable2. |     | Thediffusionmodelenables |     |           |      |      |      |      |      |      |
|            |     |                          |     | Diffusion | 0.72 | 6.52 | 0.19 | 2.26 | 0.57 | 4.34 |
driftingmaneuverswithtrackingperfor-
mancethatiscomparabletoexpertmodels, whilesimultaneouslyhavingtheadvantageofbeing
trained on an unstructured dataset. This demonstrates the model’s ability to adapt at test time to
thespecificvehiclesettingandroadconditionbasedontheonlineobservation. Interestingly,the
frameworksucceedsinaccuratelytrackingtheSlalomtrajectory(firstcolumnofFigure5),which
isnotpartofanymaneuversinthetrainingdataset. Trackingthistrajectoryrequiresthevehicleto
operateoutsideofthetrainingdatadistribution,giventherapidchangesbetweencirclesofdifferent
radiiwhileacceleratingduringthelasttransitionofthetrajectory. Wespeculatethatthisabilityto
generalizeresultsfromthepriorphysicsknowledgeencodedintheneuralSDEvehiclemodel.
| Drifting | results | on the Lexus | LC500. |         |                |     |                      |     |     |     |
| -------- | ------- | ------------ | ------ | ------- | -------------- | --- | -------------------- | --- | --- | --- |
|          |         |              |        | Table3: | Trackingerror: |     | Lexuswithtype3tires. |     |     |     |
TrackingresultsinFigure6andTable3 Donut(gear2) Donut(gear1) Figure-8(gear1)
show that using the diffusion model en- RMSE e(m) β(deg) e(m) β(deg) e(m) β(deg)
|     |     |     |     | Expert | 0.48 | 3.44 | 0.38 | 6.39 | 0.32 | 3.27 |
| --- | --- | --- | --- | ------ | ---- | ---- | ---- | ---- | ---- | ---- |
ablesaccuratetrackingwithperformance
|                           |     |     |           | Diffusion | 0.82 | 4.70 | 0.29 | 4.48 | 0.34 | 3.79 |
| ------------------------- | --- | --- | --------- | --------- | ---- | ---- | ---- | ---- | ---- | ---- |
| comparabletoexpertmodels. |     |     | Again,the |           |      |      |      |      |      |      |
proposedmethodiscapableofperformingadonuttrajectoryinsecondgear,althoughnosecond-gear
trajectoryfromtheLexusisinthedataset. Moreover,onlyunsuccessfulFigure-8trajectoriesonthe
Lexusareinthedataset,yetbothmethodsusingtheexpertanddiffusionmodelssucceedintracking
thistrajectory,thankstothephysicsstructureencodedintheneuralSDEmodel.
4.4 Driftinginlow-frictionconditionsusinglimiteddata
7

15
|     | 30      |     |     |         |     |     |         | 15  |     |     |
| --- | ------- | --- | --- | ------- | --- | --- | ------- | --- | --- | --- |
|     | ]m[tsaE |     |     | ]m[tsaE |     |     | ]m[tsaE |     |     |     |
|     |         |     |     | 10      |     |     |         | 10  |     |     |
20
|     |     |     |     | 5   |     |     |     | 5   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
10
|     | 0North[m]   |       |     | 0        |     |       |     | 0     |     |          |
| --- | ----------- | ----- | --- | -------- | --- | ----- | --- | ----- | --- | -------- |
|     |             | Start |     | North[m] |     | Start |     | Start |     | North[m] |
|     | −40 −30 −20 | −10 0 |     |          | −10 | 0     |     | 0     | 10  | 20 30    |
14
| ]s/m[V |     |     | 8   |     |     |     |     | 10  |     |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
12
|     |     |     | 7   |     |     |     |     | 8   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
10
50
0
| ]ged[β −10 |     |     | 0   |     | Reference | Diffusion |     | 25  |     |     |
| ---------- | --- | --- | --- | --- | --------- | --------- | --- | --- | --- | --- |
| −20        |     |     | −15 |     | Expert    |           |     | 0   |     |     |
| −30        |     |     | −30 |     |           |           | −25 |     |     |     |
−40
|     |     |     | −45 |     |     |     | −50 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1
1
]m[e
|     | 0   |     | 0   |     |     |     |     | 0   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
−1
|     |     |     | −1  |     |     |     |     | −1  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
100 200 300 400 20 40 60 80 100 120 140 160 100 150 200 250 300
|     | Distancealongpath[m] |     |     | Distancealongpath[m] |     |     |     | Distancealongpath[m] |     |     |
| --- | -------------------- | --- | --- | -------------------- | --- | --- | --- | -------------------- | --- | --- |
Figure6: DriftingtheLexus: performancecomparisonbetweentheExpertandDiffusionmodels.
Lastly, we augment the dataset with 3 manual drifting trajectories collected in the rain and 4 au-
tonomousdriftingdonuttrajectoriesonawetsurfacewithfailedandsuccessfulattemptsontheLexus
vehicle. Then,weretrainthediffusionmodelandreporttheperformanceoftheresultingcontroller
deployedinheavyraininFigure7. Theproposedapproachiscapableofdriftingwithonly1.47mas
thelateralRMSerror(e)and4.79degastheRMSslipangle(β)error.
Driftinginsuchrainyconditionsisparticularlychal-
| lenging.Indeed,accuratefrictionmodelingiscritical |     |     |     |     |     | ]s/m[V 8 |     |     |     |     |
| ------------------------------------------------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- |
| tosuccessfullyinitiatingthedriftwithoutspinning   |     |     |     |     |     | 7        |     |     |     |     |
| out,especiallyusingacommercialvehiclesuchas       |     |     |     |     |     | 6        |     |     |     |     |
45
| theLexus. | Stabilizingthevehicleinrainyconditions |     |     |     |     | ]ged[β 30 |     |     |     |     |
| --------- | -------------------------------------- | --- | --- | --- | --- | --------- | --- | --- | --- | --- |
isparticularlydifficultduetotheincreasedeffectof 15 Reference Diffusion
0
smallfrictionvariationsonthehandlingcharacteris-
| ticsofthevehicle,andbecausefrictionparameters |     |     |     |     |     | 4   |     |     |     |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
]m[e
| varyoverspaceduetotheterraindryingunevenly |                                       |     |     |     |     | 2   |     |     |     |     |
| ------------------------------------------ | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overtime.                                  | Theseresultsindicatethatasinglegener- |     |     |     |     |     |     |     |     |     |
0
|     |     |     |     |     |     | 25  | 50  | 75 100 125 | 150 175 | 200 225 |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | ------- |
ativemodel,trainedonamajorityofdatacollected
Distancealongpath[m]
onhigh-frictionsurfaces,hasthepotentialtoenable
reliableautonomousdrivingatthelimitsinbothhigh Figure7: Trackingperformanceinheavyrain
andlow-frictionconditions. onadonuttrajectorywhendriftingtheLexus.
5 Conclusions
Weproposeaphysics-informedgenerativevehiclemodelforautonomousdrivingatthelimitsof
handling. By decoupling model inference and control, this hierarchical approach combines the
expressivenessofadiffusionmodelwiththehigh-ratereplanningandreliabilityofmodelpredictive
control. ThroughextensiveautonomousdriftingexperimentsonaToyotaSupraandLexusLC500,
wedemonstratethatasingleconditionaldiffusionmodel, trainedonunlabelledtrajectoriesfrom
bothvehiclesoperatinginvariousconditions,canenableadaptive,robust,andreal-timeautonomous
drivingatthelimitsofhandling.
Limitationsandfuturework. Althoughthediffusionmodelpredictsamultimodaldistributionof
parametersoftheneuralSDEvehicledynamicsmodel,thecurrentmodelpredictivecontrolleronly
usesonepredictedparametersetforcontrolatatime. Fullyreasoningoverpredicteddistribution
using risk-sensitive algorithms would potentially lead to additional robustness and inform data
collectionviaactiveexplorationtobestreduceuncertaintiesonline. Finally,whileonlyvalidatedon
driftingtasks,thegeneralityoftheproposedhierarchicalmethodandtheexperimentsindicatethat
theapproachcouldpotentiallybeusedinotherautonomousdrivingandroboticsapplications.
8

Acknowledgments
WewouldliketothanktheplatformresearchteamatToyotaResearchInstitutefortheirsupport
with the test platforms and experiments. Special acknowledgment to Phung Nguyen and Steven
Goldine for facilitating the experiments and making it possible to validate our framework under
variousconditions,andJennaLeeforfacilitatingdataloggingandprocessing. Wewouldalsolike
tothankYuseiSakamotoatToyotaMotorCorporationforthetremendousassistanceinsettingup
ourframeworkontheirtestplatform,andcreatinganenvironmenttovalidateourapproachonwet
surfacesandrainyconditions.
References
[1] A. Gray, Y. Gao, T. Lin, J. K. Hedrick, H. E. Tseng, and F. Borrelli. Predictive control for
agilesemi-autonomousgroundvehiclesusingmotionprimitives. In2012AmericanControl
Conference(ACC),pages4239–4244,2012.
[2] T.Zhao,E.Yurtsever,andG.Rizzoni. Justifyingemergencydriftcontrolforautomatedvehicles.
IFAC-PapersOnLine,55(24):141–148,2022.
[3] T.GordonandM.Lidberg. Automateddrivingandautonomousfunctionsonroadvehicles.
VehicleSystemDynamics,53(7):958–994,2015.
[4] J.Y.Goh,M.Thompson,J.Dallas,andA.Balachandran. Nonlinearmodelpredictivecontrol
forhighlytransientautonomousdrifting. 15thInternationalSymposiumonAdvancedVehicle
Control,2022.
[5] T.P.WeberandJ.C.Gerdes. Modelingandcontrolfordynamicdriftingtrajectories. IEEE
TransactionsonIntelligentVehicles,2023.
[6] J.Sohl-Dickstein,E.Weiss,N.Maheswaranathan,andS.Ganguli. Deepunsupervisedlearning
usingnonequilibriumthermodynamics. InInternationalconferenceonmachinelearning,pages
2256–2265,2015.
[7] J.Ho,A.Jain,andP.Abbeel. Denoisingdiffusionprobabilisticmodels. Advancesinneural
informationprocessingsystems,33:6840–6851,2020.
[8] Y.SongandS.Ermon. Generativemodelingbyestimatinggradientsofthedatadistribution.
Advancesinneuralinformationprocessingsystems,32,2019.
[9] Y.Song,J.Sohl-Dickstein,D.P.Kingma,A.Kumar,S.Ermon,andB.Poole. Score-based
generativemodelingthroughstochasticdifferentialequations. InInternationalConferenceon
LearningRepresentations,2020.
[10] G.Williams,P.Drews,B.Goldfain,J.M.Rehg,andE.A.Theodorou. Aggressivedrivingwith
modelpredictivepathintegralcontrol. In2016IEEEInternationalConferenceonRoboticsand
Automation(ICRA),pages1433–1440,2016.
[11] J.Dallas,M.Thompson,J.Goh,andA.Balachandran. Ahierarchicaladaptivenonlinearmodel
predictive control approach for maximizing tire force usage in autonomous vehicles. Field
Robotics,3(1):222–242,2023.
[12] J. K. Subosits and J. C. Gerdes. Impacts of model fidelity on trajectory optimization for
autonomous vehicles in extreme maneuvers. IEEE Transactions on Intelligent Vehicles, 6:
546–558,2021.
[13] J. Dallas, M. P. Cole, P. Jayakumar, and T. Ersal. Terrain adaptive trajectory planning and
trackingondeformableterrains. IEEETransactionsonVehicularTechnology,70(11):11255–
11268,2021.
[14] J. Y. Goh, T. Goel, and J. C. Gerdes. Toward automated vehicle control beyond the sta-
bility limits: Drifting along a general path. Journal of Dynamic Systems Measurement and
Control-transactionsofTheAsme,142,2019.
9

[15] F.Djeumou,J.Y.Goh,U.Topcu,andA.Balachandran. Autonomousdriftingwith3minutes
of data via learned tire models. In 2023 IEEE International Conference on Robotics and
Automation(ICRA),pages968–974,2023.
[16] R.Rajamani. Vehicledynamicsandcontrol. SpringerScience&BusinessMedia,2011.
[17] P.Polack,F.Altché,B.d’AndréaNovel,andA.deLaFortelle. Thekinematicbicyclemodel:
Aconsistentmodelforplanningfeasibletrajectoriesforautonomousvehicles? 2017IEEE
IntelligentVehiclesSymposium(IV),pages812–818,2017.
[18] J.Kong,M.Pfeiffer,G.Schildbach,andF.Borrelli. Kinematicanddynamicvehiclemodelsfor
autonomousdrivingcontroldesign. 2015IEEEIntelligentVehiclesSymposium(IV),pages
1094–1099,2015.
[19] J.Y.GohandJ.C.Gerdes. Simultaneousstabilizationandtrackingofbasicautomobiledrifting
trajectories. 2016IEEEIntelligentVehiclesSymposium(IV),pages597–602,2016.
[20] N.A.Spielberg,M.Brown,andJ.C.Gerdes. Neuralnetworkmodelpredictivemotioncontrol
appliedtoautomateddrivingwithunknownfriction. IEEETransactionsonControlSystems
Technology,30(5):1934–1945,2021.
[21] A. Ramesh, M. Pavlov, G. Goh, S. Gray, C. Voss, A. Radford, M. Chen, and I. Sutskever.
Zero-shot text-to-image generation. In International conference on machine learning, pages
8821–8831,2021.
[22] C. Saharia, W. Chan, S. Saxena, L. Li, J. Whang, E. L. Denton, K. Ghasemipour, R. Gon-
tijoLopes,B.KaragolAyan,T.Salimans,etal. Photorealistictext-to-imagediffusionmodels
with deep language understanding. Advances in neural information processing systems, 35:
36479–36494,2022.
[23] A. Vahdat, F. Williams, Z. Gojcic, O. Litany, S. Fidler, K. Kreis, et al. Lion: Latent point
diffusionmodelsfor3dshapegeneration.AdvancesinNeuralInformationProcessingSystems,
35:10021–10039,2022.
[24] L.Zhou,Y.Du,andJ.Wu.3dshapegenerationandcompletionthroughpoint-voxeldiffusion.In
ProceedingsoftheIEEE/CVFinternationalconferenceoncomputervision,pages5826–5835,
2021.
[25] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song. Diffusion policy:
Visuomotor policy learning via action diffusion. In Proceedings of Robotics: Science and
Systems(RSS),2023.
[26] A. Ajay, Y. Du, A. Gupta, J. Tenenbaum, T. Jaakkola, and P. Agrawal. Is conditional gen-
erative modeling all you need for decision-making? International Conference on Learning
Representations,11,2023.
[27] B.Kang,X.Ma,C.Du,T.Pang,andS.Yan.Efficientdiffusionpoliciesforofflinereinforcement
learning. AdvancesinNeuralInformationProcessingSystems,36,2024.
[28] T.Pearce,T.Rashid,A.Kanervisto,D.Bignell,M.Sun,R.Georgescu,S.V.Macua,S.Z.Tan,
I.Momennejad,K.Hofmann,etal. Imitatinghumanbehaviourwithdiffusionmodels. arXiv
preprintarXiv:2301.10677,2023.
[29] T.Gu,G.Chen,J.Li,C.Lin,Y.Rao,J.Zhou,andJ.Lu. Stochastictrajectorypredictionvia
motionindeterminacydiffusion. InProceedingsoftheIEEE/CVFConferenceonComputer
VisionandPatternRecognition,pages17113–17122,2022.
[30] C.Jiang,A.Cornman,C.Park,B.Sapp,Y.Zhou,D.Anguelov,etal. Motiondiffuser: Con-
trollable multi-agent motion prediction using diffusion. In Proceedings of the IEEE/CVF
ConferenceonComputerVisionandPatternRecognition,pages9644–9653,2023.
[31] D.Rempe,Z.Luo,X.BinPeng,Y.Yuan,K.Kitani,K.Kreis,S.Fidler,andO.Litany. Trace
andpace: Controllablepedestriananimationviaguidedtrajectorydiffusion. InProceedingsof
theIEEE/CVFConferenceonComputerVisionandPatternRecognition,pages13756–13766,
2023.
10

[32] J.M.L.AlcarazandN.Strodthoff. Diffusion-basedtimeseriesimputationandforecastingwith
structuredstatespacemodels. arXivpreprintarXiv:2208.09399,2022.
[33] Y.Tashiro,J.Song,Y.Song,andS.Ermon. Csdi: Conditionalscore-baseddiffusionmodelsfor
probabilistictimeseriesimputation. AdvancesinNeuralInformationProcessingSystems,34:
24804–24816,2021.
[34] B.Holzschuh,S.Vegetti,andN.Thuerey.Solvinginversephysicsproblemswithscorematching.
AdvancesinNeuralInformationProcessingSystems,36,2023.
[35] G.Kohl,L.-W.Chen,andN.Thuerey. Turbulentflowsimulationusingautoregressivecondi-
tionaldiffusionmodels. arXivpreprintarXiv:2309.01745,2023.
[36] Q.LiuandN.Thuerey. Uncertainty-awaresurrogatemodelsforairfoilflowsimulationswith
denoisingdiffusionprobabilisticmodels. AmericanInstituteofAeronauticsandAstronautics,
pages1–22,2024.
[37] R.Rombach,A.Blattmann,D.Lorenz,P.Esser,andB.Ommer.High-resolutionimagesynthesis
withlatentdiffusionmodels. InProceedingsoftheIEEE/CVFconferenceoncomputervision
andpatternrecognition,pages10684–10695,2022.
[38] R.T.Chen,Y.Rubanova,J.Bettencourt,andD.Duvenaud. Neuralordinarydifferentialequa-
tions. InProceedingsofthe32ndInternationalConferenceonNeuralInformationProcessing
Systems,pages6572–6583,2018.
[39] C.Rackauckas,Y.Ma,J.Martensen,C.Warner,K.Zubov,R.Supekar,D.Skinner,A.Ramadhan,
andA.Edelman. Universaldifferentialequationsforscientificmachinelearning. arXivpreprint
arXiv:2001.04385,2020.
[40] F.Djeumou,C.Neary,E.Goubault,S.Putot,andU.Topcu. Neuralnetworkswithphysics-
informedarchitecturesandconstraintsfordynamicalsystemsmodeling. InProceedingsofThe
4thAnnualLearningforDynamicsandControlConference,volume168,2022.
[41] M.Cranmer, S.Greydanus, S.Hoyer, P.Battaglia, D.Spergel, andS.Ho. Lagrangianneu-
ral networks. In International Conference on Learning Representations, 2020 Workshop on
IntegrationofDeepNeuralModelsandDifferentialEquations,2020.
[42] S. Greydanus, M. Dzamba, and J. Yosinski. Hamiltonian neural networks. In Advances in
NeuralInformationProcessingSystems,2019.
[43] B.O.Koopman. Hamiltoniansystemsandtransformationinhilbertspace. Proceedingsofthe
NationalAcademyofSciences,17(5):315–318,1931.
[44] I. Mezic´. Spectral properties of dynamical systems, model reduction and decompositions.
NonlinearDynamics,41:309–325,2005.
[45] I.Mezic´. Analysisoffluidflowsviaspectralpropertiesofthekoopmanoperator. Annualreview
offluidmechanics,45:357–378,2013.
[46] C.W.Rowley,I.Mezic´,S.Bagheri,P.Schlatter,andD.S.Henningson. Spectralanalysisof
nonlinearflows. Journaloffluidmechanics,641:115–127,2009.
[47] J.L.Proctor,S.L.Brunton,andJ.N.Kutz. Generalizingkoopmantheorytoallowforinputs
andcontrol. SIAMJournalonAppliedDynamicalSystems,17(1):909–930,2018.
[48] S.L.Brunton,M.Budišic´,E.Kaiser,andJ.N.Kutz. Modernkoopmantheoryfordynamical
systems. arXivpreprintarXiv:2102.12086,2021.
[49] J.L.Proctor,S.L.Brunton,andJ.N.Kutz. Dynamicmodedecompositionwithcontrol. SIAM
JournalonAppliedDynamicalSystems,15(1):142–161,2016.
[50] E. Kaiser, J. N. Kutz, and S. L. Brunton. Sparse identification of nonlinear dynamics for
modelpredictivecontrolinthelow-datalimit. ProceedingsoftheRoyalSocietyA,474(2219):
20180335,2018.
11

[51] M.KordaandI.Mezic´. Linearpredictorsfornonlineardynamicalsystems: Koopmanoperator
meetsmodelpredictivecontrol. Automatica,93:149–160,2018.
[52] J.Coulson,J.Lygeros,andF.Dörfler. Data-enabledpredictivecontrol: Intheshallowsofthe
deepc. In201918thEuropeanControlConference(ECC),pages307–312,2019.
[53] H.J.vanWaarde,M.K.Camlibel,andM.Mesbahi. Fromnoisydatatofeedbackcontrollers:
Nonconservativedesignviaamatrixs-lemma. IEEETransactionsonAutomaticControl,67
(1):162–175,2020.
[54] C.E.Rasmussen. Gaussianprocessesinmachinelearning. Springer,2003.
[55] C.K.WilliamsandC.E.Rasmussen. Gaussianprocessesformachinelearning. MITpress
Cambridge,2006.
[56] L. Song, J. Huang, A. Smola, and K. Fukumizu. Hilbert space embeddings of conditional
distributions with applications to dynamical systems. In Proceedings of the 26th Annual
InternationalConferenceonMachineLearning,pages961–968,2009.
[57] J.Snoek,O.Rippel,K.Swersky,R.Kiros,N.Satish,N.Sundaram,M.Patwary,M.Prabhat,
andR.Adams. Scalablebayesianoptimizationusingdeepneuralnetworks. InInternational
conferenceonmachinelearning,pages2171–2180,2015.
[58] A. J. Thorpe, C. Neary, F. Djeumou, M. M. Oishi, and U. Topcu. Physics-informed kernel
embeddings: Integrating prior system knowledge with data-driven control. arXiv preprint
arXiv:2301.03565,2023.
[59] B.TzenandM.Raginsky. Neuralstochasticdifferentialequations: Deeplatentgaussianmodels
inthediffusionlimit. arXivpreprintarXiv:1905.09883,2019.
[60] P.Kidger. Onneuraldifferentialequations. PhDthesis,UniversityofOxford,2021.
[61] X.Li, T.-K.L.Wong, R.T.Chen, andD.K.Duvenaud. Scalablegradientsandvariational
inference for stochastic differential equations. In Symposium on Advances in Approximate
BayesianInference,2020.
[62] T.Lew,S.Singh,M.Prats,J.Bingham,J.Weisz,B.Holson,X.Zhang,V.Sindhwani,Y.Lu,
F. Xia, et al. Robotic table wiping via reinforcement learning and whole-body trajectory
optimization. In 2023 IEEE International Conference on Robotics and Automation (ICRA),
pages7184–7190,2023.
[63] F. Djeumou, C. Neary, and U. Topcu. How to learn and generalize from three minutes of
data: Physics-constrainedanduncertainty-awareneuralstochasticdifferentialequations. In
ConferenceonRobotLearning,pages577–601,2023.
[64] W.K.Hastings. Montecarlosamplingmethodsusingmarkovchainsandtheirapplications.
Biometrika,57:97–109,1970.
[65] S.ChibandE.Greenberg. Understandingthemetropolis-hastingsalgorithm. Theamerican
statistician,49(4):327–335,1995.
[66] R.M.Nealetal. Mcmcusinghamiltoniandynamics. Handbookofmarkovchainmontecarlo,
2(11):2,2011.
[67] M.D.Hoffman,A.Gelman,etal. Theno-u-turnsampler: adaptivelysettingpathlengthsin
hamiltonianmontecarlo. JournalofMachineLearningResearch,15(1):1593–1623,2014.
[68] M.D.Hoffman,D.M.Blei,C.Wang,andJ.Paisley. Stochasticvariationalinference. Journal
ofMachineLearningResearch,2013.
[69] A.Graves. Practicalvariationalinferenceforneuralnetworks. Advancesinneuralinformation
processingsystems,24,2011.
[70] D.M.Blei,A.Kucukelbir,andJ.D.McAuliffe. Variationalinference:Areviewforstatisticians.
JournaloftheAmericanstatisticalAssociation,112(518):859–877,2017.
12

[71] L.Baldassari,A.Siahkoohi,J.Garnier,K.Solna,andM.V.deHoop. Conditionalscore-based
diffusionmodelsforbayesianinferenceininfinitedimensions. AdvancesinNeuralInformation
ProcessingSystems,36,2024.
[72] B.Kawar,G.Vaksman,andM.Elad. Snips: Solvingnoisyinverseproblemsstochastically.
AdvancesinNeuralInformationProcessingSystems,34:21757–21769,2021.
[73] Y.Song,L.Shen,L.Xing,andS.Ermon. Solvinginverseproblemsinmedicalimagingwith
score-basedgenerativemodels. arXivpreprintarXiv:2111.08005,2021.
[74] B.Lakshminarayanan,A.Pritzel,andC.Blundell. Simpleandscalablepredictiveuncertainty
estimation using deep ensembles. Advances in neural information processing systems, 30,
2017.
[75] K.Chua,R.Calandra,R.McAllister,andS.Levine.Deepreinforcementlearninginahandfulof
trialsusingprobabilisticdynamicsmodels.Advancesinneuralinformationprocessingsystems,
31,2018.
[76] J. Schmidhuber. Evolutionary principles in self-referential learning, or on learning how to
learn: themeta-meta-...hook. PhDthesis,TechnischeUniversitätMünchen,1987.
[77] A. Santoro, S. Bartunov, M. Botvinick, D. Wierstra, and T. Lillicrap. Meta-learning with
memory-augmentedneuralnetworks. InInternationalconferenceonmachinelearning,pages
1842–1850,2016.
[78] C.Finn,P.Abbeel,andS.Levine. Model-agnosticmeta-learningforfastadaptationofdeep
networks. InInternationalConferenceonMachineLearning,2017.
[79] L.Bottou. Onlinelearningandstochasticapproximations. Onlinelearninginneuralnetworks,
17(9):142,1998.
[80] M. McCloskey and N. J. Cohen. Catastrophic interference in connectionist networks: The
sequentiallearningproblem. PsychologyofLearningandMotivation,24:109–165,1989.
[81] J.Kivinen,A.Smola,andR.C.Williamson. Onlinelearningwithkernels. IEEETransactions
onSignalProcessing,52:2165–2176,2001.
[82] T.Lew,A.Sharma,J.Harrison,A.Bylard,andM.Pavone. Safeactivedynamicslearningand
control: Asequentialexploration exploitationframework. IEEETransactionsonRobotics,38:
2888–2907,2020.
[83] M.P.Deisenroth,D.Fox,andC.E.Rasmussen. Gaussianprocessesfordata-efficientlearning
inroboticsandcontrol. IEEETransactionsonPatternAnalysisandMachineIntelligence,37:
408–423,2015.
[84] R.L.Stratonovich. Anewrepresentationforstochasticintegralsandequations. SiamJournal
onControl,4:362–371,1966.
[85] K.Itô. Onstochasticdifferentialequations. AmericanMathematicalSociety,1951.
[86] B.Øksendal. Stochasticdifferentialequations. SpringerBerlinHeidelberg,2003.
[87] H.Kunita. Stochasticflowsandstochasticdifferentialequations. Cambridgeuniversitypress,
1997.
[88] G.N.Milstein. Numericalintegrationofstochasticdifferentialequations. SpringerScience&
BusinessMedia,1994.
[89] P. E. Kloeden, E. Platen, and H. Schurz. Numerical solution of SDE through computer
experiments. SpringerScience&BusinessMedia,2002.
[90] B.Paden,M.Cáp,S.Z.Yong,D.S.Yershov,andE.Frazzoli. Asurveyofmotionplanningand
controltechniquesforself-drivingurbanvehicles. IEEETransactionsonIntelligentVehicles,
1:33–55,2016.
13

[91] P. Falcone, F. Borrelli, J. Asgari, H. E. Tseng, and D. Hrovat. Predictive active steering
controlforautonomousvehiclesystems. IEEETransactionsonControlSystemsTechnology,
15:566–580,2007.
[92] J.Bradbury,R.Frostig,P.Hawkins,M.J.Johnson,C.Leary,D.Maclaurin,G.Necula,A.Paszke,
J. VanderPlas, S. Wanderman-Milne, and Q. Zhang. JAX: composable transformations of
Python+NumPyprograms,2018. URLhttp://github.com/google/jax.
[93] D.KingmaandJ.Ba. Adam: Amethodforstochasticoptimization. InternationalConference
onLearningRepresentations,2014.
[94] Q.Li,Y.Zhou,Y.Liang,andP.K.Varshney. Convergenceanalysisofproximalgradientwith
momentum for nonconvex optimization. In International Conference on Machine Learning,
pages2111–2119,2017.
14

A Appendix
ThissectionprovidesadditionaldetailsontheneuralSDEvehiclemodel,theexperimentalvehicles
andtrainingdataset,theexpertmodelsusedasbaselines,thediffusionmodeltraining,andthemodel
predictivecontrolformulation.
We implement all the numerical experiments (training the models and the gradient-based model
predictive control solver) using the Python library JAX [92] to take advantage of its automatic
differentiationandjust-in-timecompilationfeatures. WeusePython3.8.5fortheexperimentsand
trainallourmodelsonalaptopcomputerwithanIntelR Xeon(R)W-11855MCPU(basefrequency
(cid:13)
3.30GHz),12cores,32GBofRAM,andaGeForceRTX2060,TU10.
A.1 Physics-inspiredneuralSDEvehiclemodel
| We  | employ | the commonly |     | used | single-track |     |     |     |     |
| --- | ------ | ------------ | --- | ---- | ------------ | --- | --- | --- | --- |
model[90,16,91,18,17]asafoundationtodescribe
| thenonlineardynamicsofthevehicle. |     |     |     |     | Thevehicle |     |     |     |     |
| --------------------------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- |
positionisexpressedinacurvilinearcoordinatesys-
| temrelativetoareferencetrajectory |     |                                 |     |     | [14,19,12],as |     |     |     |     |
| --------------------------------- | --- | ------------------------------- | --- | --- | ------------- | --- | --- | --- | --- |
| showninFigure8.                   |     | Specifically,thepositioncoordi- |     |     |               |     |     |     |     |
nateisdescribedbythedistancesalongthepath,the
relativeheading∆φwithrespecttoaplannedcourse
| φ ref ,andthelateraldeviationefromthepath. |     |     |     |     |     |     | For |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
simplicity,weassumeonlythesteeringandthrottle
areusedforautonomousdriftinganddonotinclude
| brakesinthecontrolinputsanddynamics. |     |     |     |     |     | Thepro- |          |                                |     |
| ------------------------------------ | --- | --- | --- | --- | --- | ------- | -------- | ------------------------------ | --- |
|                                      |     |     |     |     |     |         | Figure8: | Single-trackmodelofavehicleona |     |
posedneuralSDEmodelisgivenby
referencepath.
|     |    |    |                  |             |              |             |              |             |      |
| --- | --- | --- | ----------------- | ----------- | ------------ | ----------- | ------------ | ------------ | ---- |
|     |     |     |                   | aθF         | θ cos(δ)+aθF |             | θ sin(δ)−bθF | θ            |      |
|     | r  |    |                  |             | y f          |             | x f y        | r           |      |
|     |    |    |                  |             |              | Iθ          |              |             |      |
|     |    |    |                  |             |              | z           |              |             |      |
|     |    |    |                  |             |              |             |              |             |      |
|     |    |    |                  |             |              |             |              |             |      |
|     |     |     | −Fθ              | sin(δ−β)+Fθ |              | cos(δ−β)+Fθ | sin(β)+Fθ    |              |      |
|     |    |    | yf                |             | xf           |             | yr           | xr cos(β)   |      |
|     | V  |    |                  |             |              |             |              |             |      |
|     |    |    |                  |             |              | mθ          |              |             |      |
|     | d  | =  |                  |             |              |             |              | +Σθ(x,u)dW, | (10) |
|     |    |    |                  |             |              |             |              |             |      |
|     |    |    |  F θ cos(δ−β)+F |             | θ sin(δ−β)+F |             | θ cosβ−F     | θ sinβ      |      |
|     | β  |    | y f               |             | x f          |             | y r          | x r r       |      |
|     |    |    |                  |             |              | mθV         |              |             |      |
|     |    |    |                  |             |              |             |              | −           |      |
|     |    |    |                  |             |              |             |              |             |      |
|     |    |    |                  |             |              |             |              |             |      |
|     |    |    |                  |             | GEθ(τe)−Fθ   |             | Rθ           |             |      |
|     | ω   | r   |                   |             |              |             | xr           |              |      |
Iθ w
|     |     |     |     |     |     |     | mθ, | Iθ, |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
where vehicle-specific parameters such as the mass yaw moment of inertia rotational
z
inertiaofthedrivetrainIθ, thetireradiusRθ, andthedistancesfromthecenterofgravitytothe
w
| frontandrearaxlesaθ |     |     | andbθ | areincludedintheneuralSDEparametersθ |     |     |     |     |     |
| ------------------- | --- | --- | ----- | ------------------------------------ | --- | --- | --- | --- | --- |
tolearn. Thecontrol
[δ,τe]isthesteeringangleandenginetorque,respectively. Eθ(τe)isaparameterized
inputu =
polynomialfunctionthatmapstheenginetorquetothewheeltorquethroughthegearratioG. The
statex=[r,V,β,ω ,e,∆φ,s]includestheyawrater,velocityV,sideslipangleβ,rearwheelspeed
r
ω ,lateralerrore,andangulardeviation∆φ. Theevolutionofthepath-dependentvariablese,∆φ,
r
andsarewelldescribedbybasickinematics
|     |     |     |     |     | de=V | sin(∆φ)dt, |     |     | (11) |
| --- | --- | --- | --- | --- | ---- | ---------- | --- | --- | ---- |
V cos(∆φ)
|     |     |     |     |     | ds= |     | dt, |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(12)
|     |     |     |     |     |     | 1   | eκ (s) |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
|     |     |     |     |     |     | −   | ref    |     |     |
˙
|     |     |     |     | d(∆φ)=(β |     | +r  | κ (s)s˙)dt, |     | (13) |
| --- | --- | --- | --- | -------- | --- | --- | ----------- | --- | ---- |
− ref
whereκ (s)isthecurvatureofthereferencepath,andweuseβ ˙ ands˙asanabuseofnotationfor
ref
Lastly,theunknownlateralandlongitudinaltireforcesFθ
| thedrifttermsofβ |     | ands,respectively. |     |     |     |     |     |     | ,   |
| ---------------- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- |
xf
Fθ ,Fθ ,andFθ
yf xr yr areparametrizedandlearnedasfunctionsofthestateandcontrolinputs.
15

We propose to incorporate into our neural SDE model a version of the recently proposed neural-
ExpTanh[15]tiremodeparameterizedby
|     | Fθ =ExpTanhθ(tan(α  |            | ); feat   | ), Fθ | =ExpTanhθ(tan2(α |     | )+cθσ2; | feat ), |      |
| --- | ------------------- | ---------- | --------- | ----- | ---------------- | --- | ------- | ------- | ---- |
|     | yf                  |            | f         | 1 tot |                  |     | r       | 0 r 2   |      |
|     | (cid:20) θ (cid:21) | NNθ (α     | ,σ )      | Rθω   | V cosβ           |     |         |         |      |
|     | F y r               | 0 r        | r Fθ      |       | r                |     |         |         |      |
|     | =                   |            | , σ       | r =   | − ,              |     |         |         |      |
|     | F θ                 | NNθ (α     | ,σ ) tot  |       | V cosβ           |     |         |         | (14) |
|     | x r                 | 0 r        | r         |       |                  |     |         |         |      |
|     |                     | (cid:107)  | (cid:107) |       |                  |     |         |         |      |
|     |                     | V sinβ+aθr |           |       | V sinβ bθr       |     |         |         |      |
|     | α f =atan           |            | δ, α r    | =atan | −                | ,   |         |         |      |
|     |                     | V cosβ     | −         |       | V cosβ           |     |         |         |      |
|     |                     |            |           |       | (cid:0) (cid:1)  |     |         |         |      |
whereExpTanhθ(z;feat):=cθ +cθ e−cθ |z|tanh cθ (z cθ ) issuchthat(cθ )5 =NNθ(feat)is
|                                                          |     |     | 1 2 | 3   | 4 5 |     |     | i i=1 |     |
| -------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ----- | --- |
| theoutputofaneuralnetworkwithinputfeatandsatisfyingcθ,cθ |     |     |     |     | −   |     |     |       |     |
0(enforcedviaanexponential
|     |     |     |     |     | 3   | 4 ≥ |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
functiononthelasttwooutputsoftheneuralnetwork). Besides,σ istheslipratio,α andα are
|     |     |     |     |     |     | r   |     | f   | r   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
theslipanglesforthefrontandreartires,feat =[r,V,β]andfeat =[r,V,β,ω ]arefeaturesfor
|     |     |     |       | 1      |     | 2   |     | r   |     |
| --- | --- | --- | ----- | ------ | --- | --- | --- | --- | --- |
|     |     |     | andcθ | andNNθ |     |     |     |     |     |
thetwoneural-ExpTanhmodels, arelearnedtoapproximatethecoupledeffect
|     |     |     |     | 0   | 0   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
betweenthelongitudinalandlateraltiredynamicswhenthevehicleisslidingandacceleratingat
thesametime. Wenotethatourmodelhasfourneuralnetworks: NNθ forthecoupledeffect,NNθ
|     |     |     |     |     |     |     | 0   |     | 1   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
andNNθ
forfrontandrearneural-ExpTanhtiremodels,andΣθ forthediffusionterm. Lastly,we
2
emphasize thatalthough the proposedneural model assumes rear-wheel drive vehicles, itcan be
straightforwardlyextendedtootherdriveconfigurations.
Modelingdetails. WeuseadiagonalmatrixtorepresentthenoisescaleΣθ. Thisdesignchoice
greatlyreducesthecomputationofthelosses(2), (3), and(4)atthecostofpossiblylimitingthe
expressivityofthemodelbyneglectingcorrelationsbetweenstates. However,theexperimentsshow
thatthemodelcanstillcapturethecomplexdynamicsofthevehicleandenablereliableperformance
Thevehicleparametersmθ,Iθ,Iθ,Rθ,aθ,andbθarelearnablescalar
ondiversedriftingmaneuvers.
|     |     |     |     |     | z   | w   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
valuesoptimizedduringtraining. WerefertoAppendixA.3forpriorknowledgeenforcedonthese
vehicleparametersduringthetrainingofexpertmodels,butnotduringthediffusionmodeltraining.
TheenginetorquefunctionEθ(τe)isalinearfunctionwithlearnableparameters. Theparameter
cθ isalearnablescalarvalue,andtheneuralnetworksNNθ,NNθ,andNNθ
arefeedforwardneural
| 0   |     |     |     |     | 0   | 1   | 2   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
networkswithtwohiddenlayersof6neuronseachandtanhactivationfunctions. Wedonotperform
anypreprocessingonthetrainingdatasetandlearnfromrawandnoisyvehicletrajectories.
A.2 Experimentalvehiclesandtrainingdataset
Figure9: Experimentalvehiclesusedinthestudy. Left: ToyotaSupra. Right: LexusLC500.
Experimental vehicles. We deployed our framework on a Toyota Supra and a Lexus LC500,
illustratedinFigure9. TheSupraisaprototypevehiclethathasbeenheavilymodifiedtobecome
anautonomousdriftingplatform,whiletheLexusisacommercial2019LC500withitspowertrain,
drivetrain, and suspension unmodified from the dealership. The Supra has been modified with a
3Linline-sixenginecapableofoutputting380hp. Theenginehasbeenoutfittedwithanupgraded
turbocharger that can provide an additional 300hp, for a total of 680hp. The steering system is
outfittedwithbothhydraulicassistandelectricpower-assistedsteering,providinghigh-performance
steer-by-wireabilitieswithupto56.7Nmoftorque.
Thevehiclehasalsobeenmodifiedtoprovide
16

brake-by-wireandthrottle-by-wirecapabilities. Thesemodificationsmaketheplatformextremely
suitablefor(autonomous)Formuladrift,astheyallowforpreciseandfastcontrolofthevehicle’s
dynamics. TheLexus,ontheotherhand,haslower-performanceactuatorsandisnotdesignedto
beusedasadriftingvehicle. Ultimately,thesetwoplatformshavecompletelydifferentdynamics,
whichmakesthemidealforevaluatingtherobustnessandgeneralizationcapabilitiesofourapproach.
WeuseanOxfordTechnicalSystems(OxTS)RT4003v2RTK-GPS/IMUsystemforlocalization
andvehiclestateestimationforbothvehicles. TheMPCcontrollerisimplementedonanIntelXeon
E-2278GE(basefrequency3.30GHz)CPULinuxcomputermountedonboardthevehicles. The
computercommunicateswithalow-levelPIDcontrollerimplementedonadSpaceMicroAutoBoxII
τe.
(DS1401) to track desired steering angle δ and engine torque The MicroAutoBoxII receives
commandsfromtheMPCcontrollerviaUDPandsendsactuatorcommandstotheoriginalequipment
manufacturer’ssteeringandengineelectroniccontrolunits. Alldataaresynchronizedandrecorded
atafrequencyof62.5HzontheLexusand100HzontheSupra.
Trainingdataset. Webuildadatasetofmanualandautonomousdrivinganddriftingtrajectories
onaclosedcircuitfrombothvehicles. Thedatasetcontainsatotalof84trajectories,eachtrajectory
withadurationbetween10and90seconds. Ithas5trajectoriescollectedfrommanualdrivingwith
theintentofpushingthecartothelimitsofhandlingwithoutanyspecificpath-trackingmaneuvers
Theremainingtrajectoriesarefromautonomousdriftingexperimentswith28fromthe
planned.
Supra and the rest from the Lexus. The supra dataset contains failed and successful attempts at
performingdonutmaneuversinfirstgearandFigure-8maneuversinsecondgear. TheLexusdataset
containsattemptsatperformingdonutmaneuversinfirstgearandverylimited(allfailed)attemptsat
performing"Figure-8"maneuversinfirstgear. Nosecond-geardriftingtrajectorieswereprovidedin
thetrainingdatasetfortheLexus. Additionally,7%ofthetrajectoriesfromtheLexuswerecollected
withTire2,asopposedtoTire3usedintherestofthedataset. Anotabledifferencebetweenthe
twosetsoftiresistheircorneringstiffness,whichmakesdriftinitiationstrategiesandtiredynamics
differentbetweenthetwosetsoftires.
| Training | dataset | for | drifting | on  | heavy | rain. |              |     |                |              | 7   |
| -------- | ------- | --- | -------- | --- | ----- | ----- | ------------ | --- | -------------- | ------------ | --- |
|          |         |     |          |     |       |       | We augmented | the | above training | dataset with |     |
additionaldriftingtrajectoriescollectedonawettrackwithavehicleidenticaltotheLexusLC500.
3ofthetrajectoriesweremanuallycollected,whiletheremaining4werecollectedautonomously.
Theautonomoustrajectorieswerecollectedusingsecond-geardriftingmaneuversonlyonadonut
trajectory. Despitethelimitednumberoftrajectoriesandrestrictiontosecond-geardrifting,weshow
inSection4.4thatthediffusionmodeltrainedonthisdatasetgeneralizestodriftinginheavyrainon
afirst-geardonuttrajectory.
A.3 Expertmodelstraining
|     |             |         | Table4: |       | Priorparametersfortheexpertmodels. |     |          |       |       |       |     |
| --- | ----------- | ------- | ------- | ----- | ---------------------------------- | --- | -------- | ----- | ----- | ----- | --- |
|     |             | Vehicle |         | m(kg) | I (kgm2)                           |     | I (kgm2) | R(m)  | a(m)  | b(m)  |     |
|     |             |         |         |       | z                                  | ·   | w ·      |       |       |       |     |
|     | ToyotaSupra |         |         | 2048  | 3675                               |     | 6        | 0.368 | 1.345 | 1.522 |     |
|     |             |         |         | 1476  | 2241                               |     | 6        | 0.323 | 1.239 | 1.209 |     |
LexusLC500
We recall that the expert models in the experiments are neural SDE models trained on specific
vehicle-tiresubsetsofthedataset. Givenasubset exp ofthetrainingdataset ,wetraintheexpert
|     |     |     |     |     |     |     | T   |     | T   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
modelsbyminimizingthenegativelog-likelihood (θ, exp )definedin(3)withrespecttothe
|     |     |     |     |     |     |     | J traj T |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- |
neuralSDEparametersθdefinedinAppendixA.1. Theregularizationterm (θ)encodesaGaussian
R
prioronthevehicleparametersmθ,Iθ,Iθ,Rθ,aθ,andbθ. Foreachparameter,weuseaGaussian
|     |     |     |     |     | z   | w   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
prior with a mean equal to the known (estimated) parameter value for the specific vehicle and a
| standarddeviationof1. |     |     | Theresulting |     | (θ)isgivenby |     |     |     |     |     |     |
| --------------------- | --- | --- | ------------ | --- | ------------ | --- | --- | --- | --- | --- | --- |
R
| (θ)=(mθ |     | m)2+(Iθ |     | I   | )2+(Iθ | I )2+(Rθ | R)2+(aθ |     | a)2+(bθ | b)2, | (15) |
| ------- | --- | ------- | --- | --- | ------ | -------- | ------- | --- | ------- | ---- | ---- |
|         |     |         |     | z z |        | w− w     |         |     |         |      |      |
| R       |     | −       |     | −   |        |          | −       |     | −       | −    |      |
wheretheparametersvaluesm,I z ,I w ,R,a,andbforeachvehicleareprovidedinTable4. The
expertmodelsaretrainedusingAdamoptimizer[93]withalearningrateof10−3andabatchsize
of64. Weuseλ =10−4fortheregularizationterminthelossfunction(3). Duringtraining,we
traj
discretizethesumintheexpressionof (see(2)fortheexpressionand(3)forthelossfunction)into
nll
|         |     | =20discretetimestepst |     |     | J        |            | =t,T | =t  |             | =t +∆t |     |
| ------- | --- | --------------------- | --- | --- | -------- | ---------- | ---- | --- | ----------- | ------ | --- |
| asumofN | f   |                       |     |     | 0 ,...,t | Nf ,wheret | 0    | f   | N t 0 ,andt | i i−1  | i   |
−
17

=U
fori=1,...,N . Weset∆t ∆twhere∆tistypically0.01fortrajectoriesontheSupra
|     | f   | i   | (1,6) |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- |
and0.016fortrajectoriesontheLexus. Werandomizethetimesteps∆t duringtrainingtoimprove
i
themodel’sgeneralizationwhenevaluatedwithanintegrationschemethatusesstepsizesotherthan
thetrainingstepsizes.Thisistypicallythecasewhenusingthemodelinamodelpredictivecontroller;
see Appendix A.5. We note that the model learns to predict state-action sequences with varying
lengthsT f between0.4secondsand1.96seconds. Lastly,weuse5particlesoftheneuralSDEto
| computetheexpectationintheexpressionof |     |     | .   |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
J nll
A.4 Diffusionmodeltrainingandonlinesampling
InitialestimateoftheneuralSDEparameters. Wetraintheinitialestimateθloc oftheneural
SDEparametersinasimilarmannertotheexpertmodelsinAppendixA.3. Themaindifferenceis
thatweusethefulltrainingdataset insteadofthevehicle-specificsubset ,andthuswedonot
exp
| enforceanypriorknowledgeonthevehicleparametersasin(15). |     |     | T   |     | Specifically,theregularization T |     |     |
| ------------------------------------------------------- | --- | --- | --- | --- | -------------------------------- | --- | --- |
(θ)isnowenforcinganuninformativeGaussianpriorwithmean0andstandarddeviation1
term
R
onalltheneuralSDEparametersθasfollows
(cid:88)Nθ
|     |     |     | (θ)= | (θ )2, |     |     | (16) |
| --- | --- | --- | ---- | ------ | --- | --- | ---- |
i
|                                                                 |     |     | R   | i=1 |     |     |     |
| --------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
| whereN isthenumberofparametersinθ,andθindefinedasinAppendixA.3. |     |     |     |     |     |     |     |
θ
Parameterdatasetgenerationvialocaloptimization. Thehyperparametersthatdefinethisstep
ofthediffusionmodeltrainingaretheregularizationparameterλ ,thetimewindowW,thehistory
loc
lengthT ,thefuturetrajectorylengthT ,andthenumberofsequencesτ usedtocomputethe
| p   |     |     | f   |     | Tp:tk:Tf |     |     |
| --- | --- | --- | --- | --- | -------- | --- | --- |
=10−3,W=10seconds,andthenumberofsequencesτ
| expectationin(4). | Wesetλ |     |     |     |     |          | to5. |
| ----------------- | ------ | --- | --- | --- | --- | -------- | ---- |
|                   |        | loc |     |     |     | Tp:tk:Tf |      |
Inasimilarmannertohowwechosethetimestepsinthetrainingoftheexpertmodels(seeAppendix
A.3),wediscretizeτ andτ intoN =10discretetimestepswiththesamerandomization
|     | Tp:t | Tp:tk | p   |     |     |     |     |
| --- | ---- | ----- | --- | --- | --- | --- | --- |
∆t
of the step size i as in Appendix A.3. Thus, the maximum length of the history sequence is
T p =0.96seconds. Besides,wekeepthefuturetrajectorylengthT f tobethesameasinthetraining
oftheexpertmodels,i.e.,withN =20discretetimestepsandamaximumlengthof1.96seconds.
f
Weuse5particlesoftheneuralSDEtocomputetheexpectationintheexpressionof .
J nll
WeoptimizetheneuralSDEparametersθofthelossfunction(4)usinggradientdescentwithNesterov
accelerationandanadaptivelearningratethroughArmijolinesearch. Wesetthemaximumnumber
of iterations to 1000 and the initial guess for the learning rate and neural SDE parameters to be
respectively0.01andθloc.
| Diffusion model | training. |           |               |           |                 |         |           |
| --------------- | --------- | --------- | ------------- | --------- | --------------- | ------- | --------- |
|                 |           | We follow | the procedure | described | in [7] to train | all our | diffusion |
models. Themodel(cid:15) ψ definingthegenerativeprocessisrepresentedasastandardfeedforwardneural
network with three hidden layers of 256 neurons each. We use a sinusoidal positional encoding
ofthediffusionstepk (see(5))asaninputtotheneuralnetworkdefining(cid:15) , insteadofusingk
ψ
directlyastheinput. Theencodingisdonebyscalingthediffusionstepandconcatenatingitssine
andcosinetotheinputofafeedforwardneuralnetworkwithtwohiddenlayersof32and16neurons
| eachandswishastheactivationfunction. |     |     |        | = 1000denoisingsteps, |     |                 |     |
| ------------------------------------ | --- | --- | ------ | --------------------- | --- | --------------- | --- |
|                                      |     |     | WeuseK |                       |     | andalinearnoise |     |
scheduleβ i (0,1),whereβ i =0.0001+0.02i/K fori=0,...,K. WeuseAdamoptimizerwith
∈
alearningra teof10−4andabatchsizeof32totrainthediffusionmodel. Additionally,weperform
| 50gradientupdatesof(cid:15) |     | foreachstepofAlgorithm1. |     |     |     |     |     |
| --------------------------- | --- | ------------------------ | --- | --- | --- | --- | --- |
ψ
Iterativelyrefiningtheparameterdataset. Giventhehistorysequenceτ Tp:t ,weusethediffusion
generationprocessdefinedin(7)toobtainasetofparameters θp 100 conditionedonτ . Then,
|                         |     |                                                            |     |     | t}p=0 | Tp:t |     |
| ----------------------- | --- | ---------------------------------------------------------- | --- | --- | ----- | ---- | --- |
| weusethefuturesequenceτ |     | toselectthebestparameterintermsofthenegativelog-likelihood |     |     | {     |      |     |
t : T
| (θp,τ | )with5parti | f   |     |     |     |     |     |
| ----- | ----------- | --- | --- | --- | --- | --- | --- |
nll t Tp:t:Tf c l e softheneuralSDEtocomputetheexpectationinitsexpression. The
J
obtainedbestparameteristhenusedtoupdateθlocforbetterinitializationandregularizationofthe
localoptimizationproblem(4). Inourexperiments,werefineθlocateverystepofAlgorithm1only
aftertheinitial20000stepsofthemaintrainingloop.
Online diffusion model inference. In Algorithm 2, we use a sliding window to deal with the
growingsizeofthedataset andtoaccountforchangingvehicle-roadpropertiesorenvironment
hist
|                                              |     | T   |     | istypicallysetto30secondsworthof |     |     |     |
| -------------------------------------------- | --- | --- | --- | -------------------------------- | --- | --- | --- |
| conditions. Themaximumsizeoftheslidingwindow |     |     |     | hist                             |     |     |     |
T
18

driving data. During online sampling for model predictive control, we randomly sample the set
tocontain5historysequencesτ andtheset tocontain30sequencesτ of
| T gen |     |     | Tp:tj |     | T val ⊆T | hist |     | tl:Tf |
| ----- | --- | --- | ----- | --- | -------- | ---- | --- | ----- |
thecurrenthistorydataset . Specifically,byindexingeachstate-actionpairx ,u withthe
|                                                                              |     | hist |     |     |     |     | tk  | tk        |
| ---------------------------------------------------------------------------- | --- | ---- | --- | --- | --- | --- | --- | --------- |
| correspondingdiscretetime,wecandefineadiscretedistributiontosamplesequencesτ |     | T    |     |     |     |     |     |           |
|                                                                              |     |      |     |     |     |     |     | Tp:tk ,by |
samplingtimeindexest k andusingthecorrespondingstate-actionastheendpointofthesequence
of length T p . In our experiments, we use an exponential distribution with a higher mass on the
latesttimeindexesin togenerate . Then,togenerate ,wepickthefuturesequences
|     |     | T hist | T   | gen |     | T val |     |     |
| --- | --- | ------ | --- | --- | --- | ----- | --- | --- |
τ correspondingtothesequencesof andsampletheremainingvalidationsequencesτ
| tj:Tf             |     |                                                              |     | gen |     |     |     | tl:Tf |
| ----------------- | --- | ------------------------------------------------------------ | --- | --- | --- | --- | --- | ----- |
| inthesamemanneras |     | . Thesequencesinthevalidationdatasetareselectedtobeascloseas |     | T   |     |     |     |       |
gen
|     |     | T   |     | Weusethediffusionmodeltogenerateatotalof100 |     |     |     |     |
| --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- |
possibletothelatesttimeinthehistorydataset.
parameters θ tk} k conditionedonthesequencesin gen ,andselectthebestparameteraccordingto
| {   |     |     |     |     | T   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Algorithm2.
A.5 Modelpredictivecontrolformulation
Weuseacustomproximalgradient-basedsolverwithNesterovaccelerationandArmijolinesearch,
inspired by the approach in [94], to optimize the MPC problem 9a–9b. The state constraints, if
any,andcontrolrateconstraintsareenforcedusingslackvariables,andtheproximaloperatorfor
projectingtheslackvariablesontothefeasibleset. Weuseafirst-orderapproximationtocomputethe
controlrateasinu¯˙ =(u¯ u¯ )/∆t . Ontheotherhand,theboxconstraintsonthecontrolinput
|     | k   | k+1 | k k |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
−
aresimplyenforcedbyprojectionontothesetateachiterationoftheproximalgradient-basedsolver.
Referencetrajectories. Thereferencetrajectoriesforthemapsaregeneratedofflineviathequasi-
equilibriumstrategyproposedin[19]. Westartwithafewwaypointsintermsofthedesiredcurvature
κ andsideslipangleβ asafunctionofpathdistances. Then,foreachpointonthepath,an
| ref |     | ref |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
=
equilibrium point is computed using the single-track bicycle model and the conditions κ κ ref ,
| ˙   |     | ˙   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
β = β ,φ = κ V,andV = r˙ = 0,yieldingthefine-grainedreferencevehiclestatex . We
| ref | ref |     |     |     |     |     |     | ref |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
emphasizethatthemodelusedtogeneratethereferencetrajectoriesdifferssignificantlyfromthe
neuralSDEmodelusedintheMPCcontroller. Wereducetheover-relianceonpossiblyinfeasible
referencetrajectorybyusingacostfunctionthatpenalizesthedeviationfromonlyinthesideslip
| angleβ andwheelspeedω |     | r ,see(9a)-(9b). |     |     |     |     |     |     |
| --------------------- | --- | ---------------- | --- | --- | --- | --- | --- | --- |
Lexus LC500. We use Q = 120, Q = 2.0, Q = 60.0, Q = 5, and Q = 10−6. The
|     |     | β   |     | e   | φ   | δ˙  | τ˙  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
¯
control set is given by = [ 0.52,0.52] [ 1,400] while the control rate set is given by =
|     |     | U − |     | × − |     |     |     | U   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
[ 0.9,0.9] [ 3000,400]. TheproblemisoptimizedoverahorizonH = 30with25shorttime
| − × | −   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
stepsof0.05sand5longtimestepsof0.15s. Thus,thetotallookaheadhorizonamountsto2s.
| Toyota Supra. |     | Q =   | 70, Q | = 3.0, | Q = 30.0, | Q = 1, | Q = | 10−7. |
| ------------- | --- | ----- | ----- | ------ | --------- | ------ | --- | ----- |
|               | We  | use β | e     |        | φ         | δ˙ and | τ˙  | The   |
control set is given by = [ 0.75,0.75] [ 50,350] while the control rate set is given by
| ¯   |     | U − |     | ×   | −   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
=[ 2,2] [ 3000,2 000]. T heproblemis op timizedoverahorizonH =30with25shorttime
| U − × | −   |     |     |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- |
stepsof0.05sand5longtimestepsof0.15s. Thus,thetotallookaheadhorizonamountsto2s.
A.6 Detailsonthedriftingexperiments
Inthissection,weprovideadditionaldetailsonthedriftingexperimentsconductedwiththeToyota
SupraandLexusLC500vehicles. Weshowthefullvehiclestateandcontrolevolutionwhendrifting
onthevarioustrajectoriesandroadconditions,andwhenequippedwithdifferenttires:
Figure10showstheLexusLC500driftingonafirst-geardonuttrajectorywithTire3.
•
Figure11showstheLexusLC500driftingonafirst-gearFigure-8trajectorywithTire3.
•
Figure12showstheLexusLC500driftingonasecond-geardonuttrajectorywithTire3.
•
Figure13showstheToyotaSupradriftingonafirst-geardonuttrajectory.
•
Figure14showstheToyotaSupradriftingonasecond-gearFigure-8trajectory.
•
Figure15showstheToyotaSupradriftingonasecond-gearslalom-liketrajectory.
•
Figure16showstheLexusLC500driftingonafirst-geardonuttrajectorywithTire2.
•
Figure17showstheLexusLC500driftingonafirst-gearFigure-8trajectorywithTire2.
•
Figure18showstheLexusLC500driftingonafirst-geardonuttrajectoryonheavyrain.
•
19

|          |     | Reference | Expert Diffusion |     |     |
| -------- | --- | --------- | ---------------- | --- | --- |
| ]s/m[V 8 |     |           | ]s/dar[r         |     |     |
1
7
0
| 0      |     |        | 20  |     |     |
| ------ | --- | ------ | --- | --- | --- |
| ]ged[β |     | ]ged[δ |     |     |     |
0
20
−
20
| 40  |     |     | −   |     |     |
| --- | --- | --- | --- | --- | --- |
−
1
0.1
]dar[φ∆
]m[e 0
0.0
| 1   |     |     | 0.1 |     |     |
| --- | --- | --- | --- | --- | --- |
| −   |     |     | −   |     |     |
300
]s/m[rω 12
]mN[eτ
200
10
| · 8 |     |     | 100 |     |     |
| --- | --- | --- | --- | --- | --- |
R
| 6         |                                                     |         | 0        |                      |         |
| --------- | --------------------------------------------------- | ------- | -------- | -------------------- | ------- |
| 20 40 60  | 80 100 120                                          | 140 160 | 20 40 60 | 80 100 120           | 140 160 |
|           | Distancealongpath[m]                                |         |          | Distancealongpath[m] |         |
| Figure10: | Lexusdriftingonafirst-geardonuttrajectorywithTire3. |         |          |                      |         |
20

|        |     | Reference Expert | Diffusion |     |     |
| ------ | --- | ---------------- | --------- | --- | --- |
| 10     |     |                  | 1         |     |     |
| ]s/m[V |     | ]s/dar[r         |           |     |     |
0
8
|     |     | −   | 1   |     |     |
| --- | --- | --- | --- | --- | --- |
20
25
| ]ged[β |     | ]ged[δ |     |     |     |
| ------ | --- | ------ | --- | --- | --- |
| 0      |     |        | 0   |     |     |
25
| −   |     |     | 20  |     |     |
| --- | --- | --- | --- | --- | --- |
−
0.1
]dar[φ∆
]m[e 0
0.0
0.1
| 1   |     | −   |     |     |     |
| --- | --- | --- | --- | --- | --- |
−
300
14
]s/m[rω
]mN[eτ 200
12
| ·   |     | 100 |     |     |     |
| --- | --- | --- | --- | --- | --- |
R 10
0
| 100 150              | 200 250                                                | 300 | 100 150              | 200 250 | 300 |
| -------------------- | ------------------------------------------------------ | --- | -------------------- | ------- | --- |
| Distancealongpath[m] |                                                        |     | Distancealongpath[m] |         |     |
| Figure11:            | Lexusdriftingonafirst-gearFigure-8trajectorywithTire3. |     |                      |         |     |
21

14
12
10
]s/m[V
Reference Expert Diffusion
1.0
0.5
0.0
]s/dar[r
0
20
−
40
−
]ged[β
20
0
20
−
]ged[δ
1
0
1 −
]m[e
0.1
0.0
0.1 −
]dar[φ∆
15
10
100 200 300 400
Distancealongpath[m]
]s/m[rω
R
·
400
200
0
100 200 300 400
Distancealongpath[m]
]mN[eτ
Figure12: Lexusdriftingonasecond-geardonuttrajectorywithTire3.
22

|     |     | Reference Expert | Diffusion |     |     |
| --- | --- | ---------------- | --------- | --- | --- |
1.5
14
| ]s/m[V |     | ]s/dar[r |     |     |     |
| ------ | --- | -------- | --- | --- | --- |
1.0
12
0.5
10
0.0
0
| ]ged[β |     | ]ged[δ | 0   |     |     |
| ------ | --- | ------ | --- | --- | --- |
20
−
20
−
40
−
1.0
0.1
| 0.5 |     | ]dar[φ∆ |     |     |     |
| --- | --- | ------- | --- | --- | --- |
]m[e
0.0
0.0
0.1
| − 0.5 |     |     | −   |     |     |
| ----- | --- | --- | --- | --- | --- |
20
200
]s/m[rω
]mN[eτ
0
10
·
| R   |     |     | 200 |     |     |
| --- | --- | --- | --- | --- | --- |
−
0
| 150 200              | 250 300                                          | 350 | 150 200              | 250 300 | 350 |
| -------------------- | ------------------------------------------------ | --- | -------------------- | ------- | --- |
| Distancealongpath[m] |                                                  |     | Distancealongpath[m] |         |     |
| Figure13:            | ToyotaSupradriftingonafirst-geardonuttrajectory. |     |                      |         |     |
23

|     |     | Reference Expert | Diffusion |     |     |
| --- | --- | ---------------- | --------- | --- | --- |
2
| 16     |     | 1        |     |     |     |
| ------ | --- | -------- | --- | --- | --- |
| ]s/m[V |     | ]s/dar[r |     |     |     |
| 14     |     | 0        |     |     |     |
| 12     |     | 1        |     |     |     |
−
50
25
]ged[β ]ged[δ
| 0   |     | 0   |     |     |     |
| --- | --- | --- | --- | --- | --- |
25
| 50  |     | −   |     |     |     |
| --- | --- | --- | --- | --- | --- |
−
0.1
1
]dar[φ∆
]m[e
0
0.0
1
| −   |     | 0.1 |     |     |     |
| --- | --- | --- | --- | --- | --- |
−
| ]s/m[rω 20 |     | 200 |     |     |     |
| ---------- | --- | --- | --- | --- | --- |
]mN[eτ
0
10
| ·   |     | − 200 |     |     |     |
| --- | --- | ----- | --- | --- | --- |
R
0
− 400
| 200 300              | 400 500                                              | 600 | 200 300              | 400 500 | 600 |
| -------------------- | ---------------------------------------------------- | --- | -------------------- | ------- | --- |
| Distancealongpath[m] |                                                      |     | Distancealongpath[m] |         |     |
| Figure14:            | ToyotaSupradriftingonasecond-gearFigure-8trajectory. |     |                      |         |     |
24

|        |     | Reference | Expert Diffusion |     |     |
| ------ | --- | --------- | ---------------- | --- | --- |
| 16     |     |           | 1                |     |     |
| ]s/m[V |     | ]s/dar[r  |                  |     |     |
0
14
1
| 12     |     |        | −   |     |     |
| ------ | --- | ------ | --- | --- | --- |
| 25     |     |        | 25  |     |     |
| ]ged[β |     | ]ged[δ |     |     |     |
| 0      |     |        | 0   |     |     |
| − 25   |     |        | 25  |     |     |
−
50
−
0.1
2
]dar[φ∆
]m[e
| 1   |     |     | 0.0 |     |     |
| --- | --- | --- | --- | --- | --- |
0
0.1
−
200
]s/m[rω 20
]mN[eτ
0
10
| ·   |     |     | 200 |     |     |
| --- | --- | --- | --- | --- | --- |
| R   |     |     | −   |     |     |
0
| 150 200 250          | 300 350 400                                             | 450 | 150 200 250          | 300 350 400 | 450 |
| -------------------- | ------------------------------------------------------- | --- | -------------------- | ----------- | --- |
| Distancealongpath[m] |                                                         |     | Distancealongpath[m] |             |     |
| Figure15:            | ToyotaSupradriftingonasecond-gearslalom-liketrajectory. |     |                      |             |     |
25

|     | Reference Expert(Tires2) |     | Diffusion(Tires2,3) |     | BaseSDE(Tires2,3) |     |
| --- | ------------------------ | --- | ------------------- | --- | ----------------- | --- |
8
| ]s/m[V |     |     | ]s/dar[r |     |     |     |
| ------ | --- | --- | -------- | --- | --- | --- |
1
7
0
| 0      |     |     |        | 20  |     |     |
| ------ | --- | --- | ------ | --- | --- | --- |
| ]ged[β |     |     | ]ged[δ |     |     |     |
| 20     |     |     |        | 0   |     |     |
−
| 40  |     |     |     | 20  |     |     |
| --- | --- | --- | --- | --- | --- | --- |
| −   |     |     |     | −   |     |     |
0.5
|     |     |     | ]dar[φ∆ | 0.1 |     |     |
| --- | --- | --- | ------- | --- | --- | --- |
]m[e 0.0
0.0
− 0.5
0.1
−
300
]s/m[rω 12.5
]mN[eτ 200
10.0
100
·
R 7.5
0
| 25  | 50 75 100 125                                                 | 150 175 | 200                 | 25 50 | 75 100 125           | 150 175 200 |
| --- | ------------------------------------------------------------- | ------- | ------------------- | ----- | -------------------- | ----------- |
|     | Distancealongpath[m]                                          |         |                     |       | Distancealongpath[m] |             |
|     | Figure16: Lexusdriftingonafirst-geardonuttrajectorywithTire2. |         |                     |       |                      |             |
|     | Reference Expert(Tires2)                                      |         | Diffusion(Tires2,3) |       | BaseSDE(Tires2,3)    |             |
10
| ]s/m[V |     |     | ]s/dar[r | 1   |     |     |
| ------ | --- | --- | -------- | --- | --- | --- |
0
8
− 1
| 25  |     |     |     | 20  |     |     |
| --- | --- | --- | --- | --- | --- | --- |
]ged[β ]ged[δ
| 0   |     |     |     | 0   |     |     |
| --- | --- | --- | --- | --- | --- | --- |
25
| −   |     |     |     | − 20 |     |     |
| --- | --- | --- | --- | ---- | --- | --- |
0.2
0
]dar[φ∆
]m[e
0.0
− 2
4
| −   |     |     |     | 0.2 |     |     |
| --- | --- | --- | --- | --- | --- | --- |
−
300
14
]s/m[rω
| 12  |     |     | ]mN[eτ | 200 |     |     |
| --- | --- | --- | ------ | --- | --- | --- |
| 10  |     |     |        | 100 |     |     |
·
R
8
0
| 50        | 100 150 200                                            | 250 | 300 | 50  | 100 150              | 200 250 300 |
| --------- | ------------------------------------------------------ | --- | --- | --- | -------------------- | ----------- |
|           | Distancealongpath[m]                                   |     |     |     | Distancealongpath[m] |             |
| Figure17: | Lexusdriftingonafirst-gearFIgure-8trajectorywithTire2. |     |     |     |                      |             |
26

Reference Diffusion
0.0
8
]s/m[V ]s/dar[r 0.5
−
| 7   | 1.0 |     |     |
| --- | --- | --- | --- |
−
1.5
| 6   | −   |     |     |
| --- | --- | --- | --- |
| 40  | 20  |     |     |
]ged[β ]ged[δ
| 20  | 0   |     |     |
| --- | --- | --- | --- |
0
20
−
0.2
4
]dar[φ∆
]m[e
0.0
2
− 0.2
0
| ]s/m[rω 12.5 | 150 |     |     |
| ------------ | --- | --- | --- |
]mN[eτ
100
10.0
· 50
R 7.5
0
| 50 100                                                          | 150 200 | 50 100               | 150 200 |
| --------------------------------------------------------------- | ------- | -------------------- | ------- |
| Distancealongpath[m]                                            |         | Distancealongpath[m] |         |
| Figure18: Lexusdriftingonafirst-geardonuttrajectoryonheavyrain. |         |                      |         |
27