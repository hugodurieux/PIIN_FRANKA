MachineLearningforComputationalScienceandEngineering(2025)1:15
https://doi.org/10.1007/s44379-025-00015-1
RESEARCH
From PINNs to PIKANs: recent advances in physics-informed machine
learning
JuanDiego Toscano1·Vivek Oommen2·AlanJohn Varghese2·Zongren Zou1·Nazanin AhmadiDaryakenari2,3·
Chenxi Wu2·GeorgeEm Karniadakis1
Received:18October2024/Accepted:26February2025/Publishedonline:11March2025
©TheAuthor(s),underexclusivelicencetoSpringerNatureSwitzerlandAG 2025
Abstract
Physics-InformedNeuralNetworks(PINNs)haveemergedasakeytoolinScientificMachineLearningsincetheirintroduc-
tionin2017,enablingtheefficientsolutionofordinaryandpartialdifferentialequationsusingsparsemeasurements.Over
the past few years, significant advancements have been made in the training and optimization of PINNs, covering aspects
such as network architectures, adaptive refinement, domain decomposition, and the use of adaptive weights and activation
functions.AnotablerecentdevelopmentisthePhysics-InformedKolmogorov-ArnoldNetworks(PIKANS),whichleverage
arepresentationmodeloriginallyproposedbyKolmogorovin1957,offeringapromisingalternativetotraditionalPINNs.In
thisreview,weprovideacomprehensiveoverviewofthelatestadvancementsinPINNs,focusingonimprovementsinnetwork
design,featureexpansion,optimizationtechniques,uncertaintyquantification,andtheoreticalinsights.Wealsosurveykey
applicationsacrossarangeoffields,includingbiomedicine,fluidandsolidmechanics,geophysics,dynamicalsystems,heat
transfer,chemicalengineering,andbeyond.Finally,wereviewcomputationalframeworksandsoftwaretoolsdevelopedby
bothacademiaandindustrytosupportPINNresearchandapplications.
Keywords Physics-informedneuralnetworks·Kolmogorov-Arnoldnetworks·Optimizationalgorithms·SeparablePINNs·
Self-adaptiveweights·Uncertaintyquantification
1 Introduction large-scalecomputationsprohibitivelyexpensive.FEMand
otherconventionalnumericalmethodsareeffectiveinsolv-
Thefiniteelementmethod(FEM)hasbeenthecornerstone ingwell-posedproblemwithfullknowledgeoftheboundary
ofComputationalScienceandEngineering(CSE)inthelast and initial conditions as well as all material parameters.
few decades but it was viewed with skepticism when the Unfortunately,inpracticalapplications,therearealwaysgaps
first published works appeared in the early 1960s. Despite insuchasettingandarbitraryassumptionshavetobemade,
their success in academic research and industrial applica- e.g.toassumethethermalboundaryconditionsatthewalls
tions, FEM cannot easily assimilate measured data unless inpowerelectronicscoolingapplications.Thismayleadto
elaboratedataassimilationmethodsareemployedthatrender erroneousresultsasinsuchaproblemofinterestisthehighest
temperatureorthehighestheatfluxthatistypicallylocated
at the surface where erroneous assumptions are employed.
Juan Diego Toscano, Vivek Oommen, and Alan John Varghese con-
Whatmaybeavailableinsteadareafewsparsethermocou-
tributedequallytothiswork.
plemeasurementseitheronthesurfaceorinsidethedomain
B
GeorgeEmKarniadakis of interest. Unfortunately, current numerical methods like
george_karniadakis@brown.edu
FEMcannotutilizesuchmeasurementseffectivelyandhence
1 DivisionofAppliedMathematics,BrownUniversity, importantexperimentalinformationforthesystemislost.On
Providence02912,RI,USA theotherhand,neuralnetworksaretrainedbasedondataof
2 SchoolofEngineering,BrownUniversity,Providence02912, anyfidelityoranymodalitysodataassimilationisanatural
RI,USA processinsuchsettings.
3 CenterforBiomedicalEngineering,BrownUniversity, Physics-InformedNeuralNetworks(PINNs)weredevel-
Providence02912,RI,USA oped to address precisely this need, considering different
123

15 Page 2 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
simulationscenarioswherethereissomeknowledgeofthe systems.Incontrast,[11]conductedabibliometricanalysis
governing physical laws but not complete knowledge, and of120researcharticles,highlightingkeypublicationtrends,
thereexistsomesparsemeasurementsforsomeofthestate highlycitedauthorsandleadingcountriesinPINNresearch.
variablesbutnotforall.Hence,PINNsprovideaframework The structure of the paper is shown schematically in
toencodephysicallawsinneuralnetworks[1]andresolvethe Fig. 1. In Section 2 we outline the general framework of
disconnect between traditional physically grounded math- Physics-Informed Machine Learning. Section 3 provides a
ematical models and modern purely data-driven methods. comprehensive summary of the major techniques aimed at
Specifically,PINNsincorporatethegoverninglawsbyhav- improvingPINNs.InSection4weprovideanoverviewofthe
inganadditional‘residual’losstermintheobjectivefunction diverseapplicationsofPINNs.Section5focusesonuncer-
thatenforcestheunderlyingPDEasasoftconstraint.They tainty quantification methods in PINNs. In Section 6, we
are effective in solving both forward and inverse problems summarize the developments in the theory behind PINNs.
acrossallscientificdomains.PINNscanincorporatesparse Section7reviewsthevariouscomputationalframeworksand
and noisy data, making them effective in scenarios where software.Finally,inSection8,weprovideadiscussionand
acquiringaccuratemeasurementscanbedifficultorexpen- futureoutlook.
sive. A key innovation in PINNs is the use of automatic
differentiation based on computational graphs that leads to
accuratetreatmentofthedifferentialoperatorsemployedin 2 Physics-informedmachinelearning(PIML)
conservationlawsbutmostimportantlyremovesthetyranny
ofelaboratemeshgenerationthatistimeconsumingandlim- Physics-Informed Machine Learning (PIML) has emerged
itssolutionaccuracy. as a powerful alternative to traditional numerical methods
Since the original two papers appeared on the arXiv in forsolvingpartialdifferentialequations(PDEs)inbothfor-
2017 [2, 3] and the subsequent publication of a combined wardandinverseproblems.PIMLwasfirstintroducedina
paperin2019[1],therehasbeengreatexcitementintheCSE seriesofpapersbyRaissi,Perdikaris,andKarniadakis[12]
community and very important advances on many aspects basedonGaussianprocessesregression(GPR);seealsothe
ofthemethodhavebeenproposedbyresearchgroupsfrom patentbythesameauthors[13].Inthispaper,however,we
around the world and across all scientific domains. At the willreviewthesubsequentdevelopmentofPIMLusingneu-
timeofthiswriting,therehavealreadybeenover11000cita- ralnetworksandautomaticdifferentiation,startingwiththe
tionsof[1],withmanystudiesinvestigatingtheapplicability twopapersfrom2017onthearXiv[2,3],whichwerecom-
ofPINNsacrossdifferentscientificdomainswhileotherstud- binedintoasinglepaperlaterin[1].Itisworthnotingthat
iesproposingalgorithmicimprovementsaimedataddressing earlierpapersby[14,15]attemptedtosolvePDEs(forward
the limitations of the original formulation. In the current problems) but without any data fusion or automatic differ-
reviewpaper,weprovideacompilationofmostofthemajor entiation. The PIML we present in this paper employs a
algorithmicdevelopmentsandpresentanon-exhaustivelist representationmodel,namelyamultilayerperceptron(MLP)
ofapplicationsofPINNsacrossdifferentdisciplines.Acom- oraKolmogorov-ArnoldNetwork(KAN)[62],toapproxi-
prehensive timeline of some of the important papers about matethesolutionofordinaryorpartialdifferentialequations
PINNsispresentedintheAppendix. (ODEs/PDEs)andmatchanygivendataandconstraintsby
Whileexistingreviews,suchasthoseby[4–7]summarize minimizingalossfunctioncomprisedofmultipleterms.In
keyaspectsofPINNs,ourpaperdifferentiatesitselfbypro- particular,thislossfunctionisdesignedtofitobservabledata
viding a more extensive overview of the latest algorithmic orotherphysicalormathematicalconstraintswhileenforcing
developments and by covering a broader range of applica- theunderlyingphysics,e.g.,conservationlaws[1,16].
tionsofPINNsacrossscientificdisciplines.Reviewsby[4] Unliketraditionalnumericalmethods,mostPIMLmodels
and [5] focus primarily on the methodology and applica- donotrelyonpredefinedgridsormeshes,allowingthemto
tions of PINNs in various domains, with less emphasis on handlecomplexgeometriesandhigh-dimensionalproblems
recent algorithmic improvements. The review by [7] pro- efficiently. By leveraging automatic differentiation, PIML
videsaconciseoverviewofPINNsandtheirextensions,with models compute derivatives accurately without discretiza-
anexampleondata-drivendiscoveryofequations,butdoes tion, seamlessly integrating governing physical laws with
notdivedeepintoapplicationsofPINNs.Thereviewin[6] data. This flexibility allows PIML models to approximate
includesadiscussionofalgorithmicdevelopments,butlim- solutionsfrompartialinformation,makingthemoptimalfor
its the scope of their discussion on applications to thermal uncovering hidden parameters [1], as well as reconstruct-
management and computational fluid dynamics. Addition- ing[17]orinferringhiddenfields[18]fromreal-worlddata.
ally,severalreviewsfocusonspecificdomainsofapplication. Moreover,PIMLmodelsarewell-suitedforhandlinghigh-
For example, [8] and [9] review the use of PINNs in fluid dimensionalPDEs[19],coupledsystems[20,21],stochastic
dynamics,while[10]focusesonapplicationswithinpower differential equations [22], and fractional PDEs [23], all
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 3 of 43 15
Fig.1 Overviewofthepaper:
Taxonomyofalgorithmic
developments(Section3),
applications(Section4),
uncertaintyquantification
(Section5),andtheoryof
PINNs(Section6)isillustrated
here
whilemaintainingscalabilitythroughparallelizationonmod- tionmodel,denotedas:
ernhardwaresuchasGPUs[24].ThisenablesPIMLmodels
toefficientlytacklemulti-physicsproblemsandlarge-scale
|                                                     |     |     | uˆ(x)≈u(θ,x),x | ∈(cid:3)∪(cid:3) | ,   |     |
| --------------------------------------------------- | --- | --- | -------------- | ---------------- | --- | --- |
| simulationswithreducedcomputationaloverheadcompared |     |     |                |                  | B   | (2) |
totraditionalmethods.
PIMLisagnostictospecificgoverninglaws,soherewe
istherepresentationmodel,andθ
|     |     |     | whereu |     |     | areitslearnable |
| --- | --- | --- | ------ | --- | --- | --------------- |
considerthefollowingnonlinearODE/PDE:
parameters.Sinceuiscontinuousanddifferentiable,itallows
|              |         |           | forthecomputationofthesourceandboundaryterms |     |     | f and |
| ------------ | ------- | --------- | -------------------------------------------- | --- | --- | ----- |
| F τ [uˆ](x)= | f(x), x | ∈(cid:3), | (1a)                                         |     |     |       |
bthroughautomaticdifferentiation[25],expressedasF [u]
τ
| B [uˆ](x)=b(x), | x   | ∈(cid:3) , | (1b) andB | [u][1].          |                     |                    |
| --------------- | --- | ---------- | --------- | ---------------- | ------------------- | ------------------ |
| τ               |     | B          |           | τ                |                     |                    |
|                 |     |            |           | The goal of PIML | training is to find | the optimal learn- |
representsthespatial-temporalcoordinate,uˆ
where x isthe ableparametersthatminimizethecumulativeerrorbetween
solutiontotheODE/PDE,τ aretheparametersoftheequa- theapproximatedsolutionandtheknowncomponentsofthe
isthesourceterm,bistheboundaryterm,andF
tion, f and truesolution,suchasthegoverningequation,boundarycon-
Baregeneralnonlineardifferentialandboundaryoperators, ditions,ordataresiduals.Thisframeworkcanalsobeeasily
respectively. The PIML approach aims to approximate the extended to ODE/PDE systems by stacking constraints for
solutiontotheproblemdefinedbyEq.1usingarepresenta- eachapproximatedsolution[18].
123

15 Page 4 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
|     |     |     |     | τ   |     |     |     |     |     |     | =   | {u ,...,u | })  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- |
In general, when the equation parameters are known functions. The approximated solution (u 1 p
and the boundary conditions are prescribed, the problem is usingMLPscanbemathematicallyexpressedas:
referredtoasaforwardproblem,wherenoobservationaldata
withinthedomainarerequired[1,26].Conversely,whenpar- u(θ,x)=MLP(θ,x) (3)
|     |     | τ,  |     |     |     |     | (cid:2) | (cid:2) | (cid:2) |     | (cid:3) | (cid:3) | (cid:3) |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | ------- | --- | ------- | ------- | ------- |
tial information, such as boundary conditions, or hidden W(L)σ W(L−1)...σ W(1)x+b(1) ...+b(L−1) +b(L)
=σ
fieldsintheODE/PDEsystem,isunknown,thentheproblem
(4)
isreferredtoasaninverseproblem,wheretheobjectiveisto
infersimultaneouslytheunknowninformationandthesolu-
|     |     |     |     |     |     |         | =   | {x ,...,x | }))areinputsandθ |     |     | = {W | (l),b (l)} |
| --- | --- | --- | --- | --- | --- | ------- | --- | --------- | ---------------- | --- | --- | ---- | ---------- |
|     |     |     |     |     |     | where(x |     | 1         | n                |     |     |      |            |
tionfromavailabledataorobservations[18].Aschematicof
|     |     |     |     |     |     | are the | trainable | parameters |     | of the | network; | W (l) | and b (l) |
| --- | --- | --- | --- | --- | --- | ------- | --------- | ---------- | --- | ------ | -------- | ----- | --------- |
theoverallPIMLframeworkisshowninFig.2.
denotetheweightsandbiasesofthel-thlayer,respectively.
|     |     |     |     |     |     | The        | network   | consists | of L       | layers, and | σ denotes | a      | suitable |
| --- | --- | --- | --- | --- | --- | ---------- | --------- | -------- | ---------- | ----------- | --------- | ------ | -------- |
|     |     |     |     |     |     | activation | function. |          | The output | of each     | layer     | serves | as the   |
3 AlgorithmicdevelopmentsofPIML
inputforthesubsequentlayer,culminatinginthefinaloutput
u.
| From the | PIML framework        |     | outlined | in Section       | 2, we can |         |          |         |         |             |           |           |      |
| -------- | --------------------- | --- | -------- | ---------------- | --------- | ------- | -------- | ------- | ------- | ----------- | --------- | --------- | ---- |
|          |                       |     |          |                  |           | The     | ability  | of MLPs | to      | approximate | virtually | any       | con- |
| identify | three key components: |     | (1)      | a representation | model     |         |          |         |         |             | Rn        |           |      |
|          |                       |     |          |                  |           | tinuous | function | on      | compact | subsets     | of is     | supported | by   |
toapproximatethesolution,(2)agoverningequation(such
|           |          |         |                 |     |              | the Universal |     | Approximation |     | Theorem | [27]. | This | theorem |
| --------- | -------- | ------- | --------------- | --- | ------------ | ------------- | --- | ------------- | --- | ------- | ----- | ---- | ------- |
| as an ODE | or PDE), | and (3) | an optimization |     | process that |               |     |               |     |         |       |      |         |
underpinstheeffectivenessofneuralnetworksinmodeling
| minimizes | a multi-objective |     | loss function | to find | the opti- |     |     |     |     |     |     |     |     |
| --------- | ----------------- | --- | ------------- | ------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
complexnonlinearrelationships.
| mal learnable | parameters, |     | see Fig. | 2. Ongoing | research |          |     |        |              |      |         |      |         |
| ------------- | ----------- | --- | -------- | ---------- | -------- | -------- | --- | ------ | ------------ | ---- | ------- | ---- | ------- |
|               |             |     |          |            |          | Building |     | on the | foundational | work | in [1], | many | studies |
hasgreatlyenhancedPIML’sbaselineperformancethrough
haveexploredenhancingtheexpressivenessofrepresentation
| various    | methods targeting     | these | three  | areas, namely, | mod-   |        |          |         |         |             |     |       |         |
| ---------- | --------------------- | ----- | ------ | -------------- | ------ | ------ | -------- | ------- | ------- | ----------- | --- | ----- | ------- |
|            |                       |       |        |                |        | models | in PINNs | through | various | strategies. |     | These | include |
| ifications | to the representation |       | model, | advancements   | in the |        |          |         |         |             |     |       |         |
inputandoutputnormalization,featureexpansions,hardcon-
| treatment | of the governing |     | equation, | and optimization | pro- |         |           |       |                 |     |     |               |     |
| --------- | ---------------- | --- | --------- | ---------------- | ---- | ------- | --------- | ----- | --------------- | --- | --- | ------------- | --- |
|           |                  |     |           |                  |      | straint | encoding, | model | decompositions, |     | and | architectural |     |
cessimprovements.
modifications.Eachofthesestrategiesaimstoimprovethe
|     |     |     |     |     |     | network’s | ability | to  | capture | the underlying |     | physics | of the |
| --- | --- | --- | --- | --- | --- | --------- | ------- | --- | ------- | -------------- | --- | ------- | ------ |
3.1 Representationmodelmodifications problemmoreaccuratelyandefficiently.
WhentherepresentationmodelisdefinedusinganMLP,the 3.1.1 Input/Outputtransformations
PIMLformulationisreferredtoasphysics-informedneural
networks(PINNs) [1].PINNsutilizeMLPstoapproximate Oneofthemoststraightforwardwaystoimprovethestability
thesolutionsofanODE/PDEsystem(uˆ ={uˆ ,...,uˆ })by andaccuracyofarepresentationmodelMisbytransforming
|     |     |     |     | 1   | p   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
leveragingthenetwork’sabilitytomodelcomplexnonlinear themodelinputs x ∈ Rn oroutputs u ∈ Rp usingsuitable
I(·)and (cid:6)(·)
|     |     |     |     |     |     | mappings, |     |     | (see | Fig. 3). | Under | this reformula- |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | ---- | -------- | ----- | --------------- | --- |
tion,thesolutionsofanODE/PDE(uˆ)canbeapproximated
as:
|     |     |     |     |     |     | uˆ(x)≈ | u(θ,x)=(cid:6)(M(θ,I(x))), |           |       |         |              |           | (5)  |
| --- | --- | --- | --- | --- | --- | ------ | -------------------------- | --------- | ----- | ------- | ------------ | --------- | ---- |
|     |     |     |     |     |     | where  | u =                        | {u ,...,u | })    | are the | approximated | solutions |      |
|     |     |     |     |     |     |        |                            | 1         | p     |         |              |           |      |
|     |     |     |     |     |     |        |                            |           |       | M,      | :            | Rn →      | Rm   |
|     |     |     |     |     |     | from   | the representation         |           | model |         | and I        |           | is a |
mappingthattransformsthemultivariateinputsandenhances
|     |     |     |     |     |     | themodel’sexpressivity.Thechoiceof |     |     |     |     | I oftendependson |     |     |
| --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --- | --- | ---------------- | --- | --- |
theactivationfunctionσ,asdifferentactivationfunctionsare
moreeffectiveoverspecificinputdomains.Forexample,Cai
etal.[37]proposednormalizinginputstotherange[−1,1]
Fig.2 PIMLTrainingcomponents.Arepresentationmodelprovides
whenusingsin(·)ortanh(·)activationfunctions.Similarly,
anapproximationuoftheODE/PDEsolutionuˆ.Themismatch(resid-
uals)betweentheapproximatedsolutionandtheknowncomponents Raissietal.[18]recommendednormalizinginputsbasedon
of the true solution, such as physical laws and boundary conditions, theirmeanandstandarddeviationwhenusingtheswish(·)
iscalculated.Thesegoverningequationsdefineasetofrequirements
activationfunction.
thatgenerateanoptimizationproblem.Thisproblemisreformulated
|     |     |     |     |     |     |     |     |     |     |     | (cid:6) : | Rp → | Rq  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | ---- | --- |
asalossfunctionandthensenttoanoptimizerthatupdatesthemodel On the other hand, the function is
parameters selected based on the specific characteristics of the prob-
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 5 of 43 15
Fig.3 RepresentationModelEnhancements:Inputtransformations whereeachcanbeaperceptron(PINNs)oraKAN(PIKAN)[16,62].
improve the model’s ability to impose periodic boundary condi- PINN performance is further enhanced by modifications like weight
tions[28],enhanceexpressioncapabilities[29],andmitigatespectral normalization [32, 33] or adaptive activation functions [34]. Output
biasthroughfeatureexpansions[30].Residualconnectionsboostper- transformationsenforcesolutionconstraints,suchasDirichletbound-
formanceandaccuracyforhigh-orderderivativesrequiredtoenforce aryconditions[35]ordivergence-freeconstraints[36]
| the PDE | [31]. The model architecture | typically | consists | of layers, |     |     |     |     |     |     |     |
| ------- | ---------------------------- | --------- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
lem.Forinstance,Anagnostopoulosetal.[38]usedscalars
HardConstraints
| ,...,a | ∈ R |     |     |     |     |     |     |     |     |     |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
a p to create different linear maps to handle Training in PIML involves minimizing an objective func-
1
| various   | scales in the model | outputs, represented |     | as u = |           |                |     |          |              |     |               |
| --------- | ------------------- | -------------------- | --- | ------ | --------- | -------------- | --- | -------- | ------------ | --- | ------------- |
|           |                     |                      |     |        | tion that | often combines |     | multiple | constraints, |     | significantly |
| {a ,...,a | },                  |                      |     |        |           |                |     |          |              |     |               |
1 u 1 p u p which aids in improving convergence. complicating the optimization process [49]. Research has
| Similarly,(cid:6) | canbeusedtoconstraintherangeofpredicted |            |     |     |            |          |             |     |             |     |            |
| ----------------- | --------------------------------------- | ---------- | --- | --- | ---------- | -------- | ----------- | --- | ----------- | --- | ---------- |
|                   |                                         |            |     |     | shown that | improper | enforcement |     | of boundary |     | conditions |
|                   |                                         | (cid:6)(u) | =   | |u| |            |          |             |     |             |     |            |
outputs. For example, absolute value or expo- can degrade both the performance and stability of neural
| nential(cid:6)(u) | = eu functionscanenforcethenon-negativity |     |     |     |         |          |          |            |            |     |          |
| ----------------- | ----------------------------------------- | --- | --- | --- | ------- | -------- | -------- | ---------- | ---------- | --- | -------- |
|                   |                                           |     |     |     | network | training | [28, 36, | 50]. Thus, | accurately |     | imposing |
requiredforthedensityfieldinhigh-speedflows[39].Like- boundary conditions is crucial for improving model reli-
wise,Zapfetal.[40]usedthesigmoidfunctiontoconstrain
|     |     |     |     |     | ability and | efficiency. | In  | particular, | Zeinhofer |     | et al. [51] |
| --- | --- | --- | --- | --- | ----------- | ----------- | --- | ----------- | --------- | --- | ----------- |
therangeofthepredicteddiffusivity. theoretically demonstrated that hard constraints can lead
FeatureExpansions to lower error estimates in linear problems. One practical
|     |     |     |     |     | way to address | these | challenges |     | is by | embedding | bound- |
| --- | --- | --- | --- | --- | -------------- | ----- | ---------- | --- | ----- | --------- | ------ |
Thesemodificationsaimtoaddresssomefundamentalweak-
nesses in the conventional PIML formulation, particularly ary conditions directly into the model’s structure, either
throughinput/outputtransformationsorspecializedarchitec-
| in learning | high-frequency | functions, | known | as spectral |     |     |     |     |     |     |     |
| ----------- | -------------- | ---------- | ----- | ----------- | --- | --- | --- | --- | --- | --- | --- |
tures,therebysimplifyingtheoptimizationandenhancingthe
bias[41,42],andcapturingothercomplexrelations[30].To
overallperformance.
mitigatetheseissues,researchershavemodifiedthebaseline
| modelformulationbytransformingitsinputx |     |     |     | ∈Rn intoan |     |     |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
DirichletBoundaryConditions
I(x)∈Rm,whichisthenfedintotherepre-
expandedinput Several methods have been developed to enforce Dirichlet
sentationmodelasshowninFig.3.Severalexpansionmaps
|     |     |     |     |     | boundary | conditions | exactly | in  | PIML | problems. | Berrone |
| --- | --- | --- | --- | --- | -------- | ---------- | ------- | --- | ---- | --------- | ------- |
have been explored, with their selection typically based on et al. [52] introduced the Nitsche’s method, which applies
thespecificproblem.Forexample,Wangetal.[30]proposed
avariationalapproachtoenforcetheseconditions.Another
using random Fourier features and demonstrated that this systematic technique is the Theory of Functional Connec-
| modification | helps to mitigate | spectral bias. | Other | types of |              |         |             |     |         |            |      |
| ------------ | ----------------- | -------------- | ----- | -------- | ------------ | ------- | ----------- | --- | ------- | ---------- | ---- |
|              |                   |                |       |          | tions, which | imposes | constraints |     | through | functional | con- |
expansions, such as polynomials, exponentials, Chebyshev nections, as detailed by Leake et al. [53]. On the other
polynomials,andevengatedrecurrentunits(GRU),havealso
|     |     |     |     |     | hand, hPINNs | utilize | penalty | methods |     | and the | augmented |
| --- | --- | --- | --- | --- | ------------ | ------- | ------- | ------- | --- | ------- | --------- |
beenexploredorproposedinpreviousstudies[43–48]. Lagrangianapproachtoimposehardconstraints,providing
123

15 Page 6 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
a flexible framework for handling various boundary condi- data, which preserves the symplectic structure through dif-
tions[54].Notably,Sukumaretal.[35]introducedApprox- ferentJacobianmatrixfactorizationtechniques[58].Finally
imate Distance Functions (ADF), which impose boundary [59] proposed a method that uses the theory of functional
conditions through output transformations. Under the ADF connectionstoexactlyenforcethedataconstraintsininverse
framework,theconstrainedexpressionforDirichletbound- problems.
aryconditionsisrepresentedas:
3.1.2 Architectures
uˆ(x)≈ u(θ,x)=(cid:6)(M(θ,I(x)))
= g(x)+φ(x)M(θ,I(x)), (6) PerceptronModifications
The original PIML formulation uses an MLP as the rep-
where (cid:6)(·) transform the network output in terms of a resentation model [1]. The building blocks of an MLP are
function that satisfies the solution uˆ along the boundaries perceptrons, which define a layer l and can be defined as
g(·) and a composite distance function φ(·) that equals follows:
zero when evaluated on the boundaries. If the boundary is
composedofMpartitions,denotedas[S
1
,...,S
M
],thecom-
z
(l) =σ(l)(W (l)
z
(l−1)+b (l)),
(7)
posite distance function for Dirichlet boun(cid:4)dary conditions
can be expressed as φ(φ 1 ,φ 2 ,...,φ M ) = i M =1 φ i , where where z (l) = {z (l),··· ,z (l)}aretheoutputsoflayerl,σ(l)
[φ 1 ,...,φ M ] are the individual distance functions. Notice isanon-lineara 0 ctivationf H unction(e.g.,sigmoid(·),tanh(·),
that if x ∈ S i , then φ(x) = 0, ensuring that the neural sin(·),etc.),andW (l) andb (l) aretrainableparametersthat
network approximation exactly satisfies the boundary con- linearly transform the inputs z (l−1) = {z (l−1),...,z (l−1)}.
ditions,i.e.,u(x)= g(x). 0 H
Severalapproacheshavebeenproposedtoimprovetheper-
ceptron’scapabilities.Forinstance,Jagtapetal.[34,60,61]
PeriodicBoundaryConditions p(cid:5)roposed modifying the activation function in as σ(l)(·) =
On the other hand, this type of boundary conditions can
a
(l)σ(f (l)·),
where a
(l)
and f
(l)
are trainable parame-
i i i i i
be strictly enforced as hard constraints by selecting a suit-
ters.Theauthorsshowedboththeoreticallyandempirically
able input transformation I(x) (see Fig. 3). For instance,
thatthesemodificationssignificantlyimprovemodelperfor-
theperiodicnatureofasmoothunivariatefunctionu(x)can
mance.
be encoded into a model using a one-dimensional Fourier
featureembedding,I(x)=[1,cos(ω x),sin(ω x),...,cos
x x Otherapproachesproposedmodifyingtheweightmatrix
(mω
x
x),sin(mω
x
x)].Dongetal.[28]demonstratedthatany
W (l) ;forinstance,[18,32]proposeddecomposingW (l) into
representation model, such as u(θ,I(x)), is periodic along
its magnitude and its direction via weight normalization
the x coordinate when using this Fourier feature embed- described as W (l) = g(l) v (l) . This re-parameterization
ding.Similarexpansionmapshavebeenexploredforhigher (cid:6)v(l)(cid:6) 2
speeds up the model convergence with minimal compu-
dimensionsbyWangetal.[55].
tational overhead [32]. Similarly, [33] proposed weight
Other methods to impose hard constraints for periodic
factorizationW (l) =diag(s (l))·V (l) ,wheres (l) aretrainable
boundary conditions include using hPINNs, which employ
parameters. The authors experimentally and theoretically
the penalty and augmented Lagrangian methods to enforce
showed that this reparameterization significantly improves
such constraints [54]. Additionally, hybrid approaches that
themodelperformance[33].
combinevarioustechniquesfortheexactimpositionofperi-
odicboundaryconditionshavebeeninvestigated[56]. OtherRepresentationModels
Onenaturalextensiontootherrepresentationmodels,given
ComplexConstraints their similarity to MLPs, is Kolmogorov-Arnold Networks
Complex constraints can be addressed through specialized (KANs) [62], which were introduced as PIKANs in [16].
architectures that incorporate domain-specific knowledge EachPIKANlayercanbedescribedasfollows:
into the learning process. One such approach is the use of
Divergence-FreeNetworks,whichapplyanappropriateout- ⎛ ⎞
put transformation to ensure that the learned vector fields (cid:6)H (cid:6)H
satisfy divergence-free conditions (see Fig. 3), as required z (l) = (cid:9) i ⎝ φ i,j (z ( j l−1))⎠, (8)
in certain fluid dynamics applications [36, 49, 57]. Zein- i=1 j=1
hofer et al. [51] theoretically demonstrated that enforcing
divergence-freeconstraintsleadstoimprovederrorestimates wherez (l−1) ={z (l−1),··· ,z (l−1)}isthemultivariateinput,
0 H
inlinearproblems.AnotherexampleisSympNets,aspecial- H denotes the number of neurons and (cid:9) i,j are the outer
ized architecture for identifying Hamiltonian systems from andφ i,j aretheinnerunivariatefunctions.Thespecificform
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 7 of 43 15
Fig.4 GoverningEquations.(a)Derivativesarerequiredtoenforce usingvariousoperators,includingfractional[23],stochastic[75],and
theODE/PDE,boundaryconditions(BCs),andpossiblydata.Themost eventhoseallowingmultiplesolutions[96].Modelperformancecanbe
commonmethodtoobtainderivativesisthroughautomaticdifferenti- enhancedthroughnon-dimensionalization[97],reformulations[20],or
ation[25].However,othermethodshavebeenproposed,suchasfinite approximations[90].(c)Residualscanbeenforcedeitherintheirstrong
differences [94], estimating derivatives as outputs [95], or stochastic form[98]orweakform[99].Intheweakform,severaltypesoftest
dimension gradient descent [19]. (b) The physical laws are imposed functionshavebeenexplored
Fig. 5 Optimization Process Enhancements. The PIML problem plingmethod[125],andatransformationfunction.(c)Theoptimizer
involvessatisfyingmultipleconstraintsinagivendomain.Forcom- updatestheparametersusingalinesearchmethod[126].Thechoiceof
plexconstraints,theproblemcanbesimplifiedusingsequentialtraining thesymmetricmatrixdefinestheoptimizationmethod,suchasgradient
orstackedtraining[123].Whendealingwithcomplexdomains(e.g., descent,Adam,L-BFGS,orNewton’smethod.Severalapproacheshave
large,irregular),domaindecompositioncanbeemployed[124].(b)The improvedbaseperformance,ensuringconflict-freeupdates[127],orby
lossfunctionmeasuresthecumulativeerrorinthedomainand,once usingalternativemethodslikenon-dominatedgeneticalgorithms[128],
discretized,comprisesglobalweights[36],localweights[38],asam- orparticleswarmoptimization[129]
123

15 Page 8 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
| φ(·) | (cid:9)(·) |     |     |     |     |     |     |     |     |
| ---- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
of and defines the types of KAN architectures. 80], information-botleneck inspired architectures [81] and
Among these variations, [16] introduced cPIKANs, which reinforcementlearningmodels[82–84].
| use Chebyshev | polynomials | as  | in(cid:5)ner and | outer univariate |     |     |     |     |     |
| ------------- | ----------- | --- | ---------------- | ---------------- | --- | --- | --- | --- | --- |
ResidualConnections
| functionsdefinedasφ(ζ,θ)=w |     |                                  | dc T    | (tanh(ζ)),where |     |                                                    |     |     |     |
| -------------------------- | --- | -------------------------------- | ------- | --------------- | --- | -------------------------------------------------- | --- | --- | --- |
|                            |     |                                  | n n n n |                 |     | AnotherapproachtoimprovethePIMLarchitectureperfor- |     |     |     |
| ζ aretheinputs,θ           |     | =(w ,c )aretrainableparameters,d |         |                 |     |                                                    |     |     |     |
|                            |     | n n                              |         |                 | is  |                                                    |     |     |     |
manceisbyaddingresidualconnections(seeFig.3),which
| thedegree            | and T | isthen-thorder | Chebyshev | polynomial, |          |                 |             |                            |     |
| -------------------- | ----- | -------------- | --------- | ----------- | -------- | --------------- | ----------- | -------------------------- | --- |
|                      | n     |                |           |             |          | enable accurate | calculation | of high-order derivatives. | The |
|                      |       | (ζ) =          | 2ζT (ζ)+T |             | (ζ)[63]. |                 |             |                            |     |
| definedrecursivelyas |       | T n            | n−1       | n−2         |          |                 |             |                            |     |
generalformulationforasingleadditiveskipconnectionis
| The authors | found | that this stable | representation |     | is more |     |     |     |     |
| ----------- | ----- | ---------------- | -------------- | --- | ------- | --- | --- | --- | --- |
definedasfollows:
| robust to  | noise [16] | and can lead      | to improved | performance |     |                       |            |        |     |
| ---------- | ---------- | ----------------- | ----------- | ----------- | --- | --------------------- | ---------- | ------ | --- |
| with fewer | parameters | [16, 49]          | than MLPs.  | Subsequent  |     |                       |            |        |     |
|            |            |                   |             |             |     | (l)(z (l−1),θ)=M(l)(z | (l−1),θ)+z | (l−1), |     |
|            |            |                   |             |             |     | z                     |            |        | (9) |
| studies    | extended   | the KAN framework | and         | developed   | new |                       |            |        |     |
architecturesforPIMLproblems[48,49,64–72].
|       |                |        |           |                |     | (l) =   | {z (l),...,z (l)}aretheoutputsoflayerl,M(l) |     |     |
| ----- | -------------- | ------ | --------- | -------------- | --- | ------- | ------------------------------------------- | --- | --- |
| Other | representation | models | have also | been explored, |     | where z |                                             |     |     |
0 H
includingconvolutionalneuralnetworks(CNNs)[73],Her- isalayeroftherepresentationmodel(e.g.,MLPlayer,KAN
|     |     |     |     |     |     |     | (l−1) = {z (l−1),...,z | (l−1)} |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | ------ | --- |
mite spline CNNs [74], generative adversarial neural net- layer), and z are the inputs to
|     |     |     |     |     |     |     | 0   | H   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
works(GANs)[75,76],spikingneuralnetworks[77],trans- layer l. Several studies have explored the advantages of
formers[78],longshort-termmemory(LSTM)networks[79, incorporating skip connections via addition or multiplica-
Fig.6 ApplicationsofPINNs.AnillustrationofthediverseapplicationswherePINNshavebeenemployedbyincorporatingtheunderlying
physicallaws.(TheindividuallogoswerecreatedusingDALL.E[200])
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 9 of 43 15
tion.Wangetal.[36]pioneeredthisapproachbyintroducing duced to the deep learning community as tensor neural
amethodreferredtoasmodifiedMLP,wheretwosingle-layer networksin[87].While[87]focusedonimprovingaccuracy
MLPsprojectthemodelinputs(x)intoahigh-dimensional through enhanced numerical integration methods, [86] pri-
feature space, which is then used to update the remaining oritized computational efficiency, achieving up to 60-times
hidden layers via element-wise multiplication and addi- speedups for high-dimensional problems, such as the 3D
tion.Otherapproachesintroducemultiplicativeconnections Helmholtz Equation and the 4D Navier-Stokes Equation.
between every layer [85]. Finally, the modified MLP was This formulation has been further explored and improved
further improved by incorporating adaptive residual con- insubsequentstudies[19,88,89].
nections that incorporate a new learnable parameter that Other types of decompositions have also been explored
controls the contribution of the deeper layers with respect for inverse problems [59, 90]. For instance, [90] extended
totheinput[31].Thisimprovedarchitectureenablestheuse the negative log-likelihood (NLL) framework [91] for lin-
of deeper networks without compromising the accuracy of ear PDEs in PIML, enabling the quantification of aleatoric
PIMLproblems. uncertaintyandimprovingmodelperformance.Theauthors
assumed that the observed data was corrupted by noise, so
ModelDecomposition they decomposed the desired solution into mean fields and
Furtherimprovementscanbeachievedbysplittingthenet- fluctuations as u = u¯ + u (cid:7) . Then they used independent
workintoseveralcomponents.Choetal.[86]proposedsep- modelstolearnthedata-drivenmeanfieldsu¯ andtheircor-
arablePINNs(sPINNs),whichutilizeseparatesub-networks respondingfluctuations,standarddeviationsu (cid:7) byusingthe
toapproximatethedesiredsolution.Underthisformulation, NLLcriterion[91–93].Ontheotherhand,[59,417]proposed
t(cid:5)he sol(cid:4)ution of a PDE is approximated as uˆ(x 1 ,··· ,x d ) = amethodtosimultaneouslyreconstructflowstatesanddeter-
p j=1 i d =1 M j (x i ,θ i ) , where {M j (x i ,θ i )}p j=1 are the mine particle properties from Lagrangian particle tracking
outputs univariate representation models that encodes each (LPT) using a neural network as a flow model and a data-
dimension x i into a p-dimensional space. This decomposi- constrainedpolynomialasaparticlemodel(Figs.4,5,6,7
tion addressed the curse-of-dimensionality and was intro- and8).
Fig.7 ApplicationsinMedicine.PINNsarehighlyeffectiveatrecon- innovative approach to intraventricular vector flow mapping (iVFM)
structing displacement fields, mapping intraventricular vector flows, byreplacingthetraditionaloptimizationmethodwithacombinationof
anduncoveringcellheterogeneityinsignaltransductionfromsparse PINNsandaphysics-guidednnU-Netmodel,enhancingcolorDoppler
data. a) [224] introduce a novel method that combines PINNs with analysisincardiacimaging.c)[203]proposedDensity-PINNstoinfer
3Dnonlinearbiomechanicalmodelsofsofttissue,enablingtherecon- transduction time distribution from observed final stress responses,
structionofdisplacementfieldsandtheestimationofpatient-specific providing insights into signal pathway dynamics such as speed and
biophysicalproperties,includingstressandstrain.b)[228]proposean accuracy
123

15 Page 10 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
Fig.8 ApplicationsinFluids.PINNseffectivelyreconstructvelocity, PINNsisusedtoreconstructthetemperatureandpressurefieldsaround
pressure,andtemperaturefieldsfromsparseobservations.a)[239]use anespressocupandaswimmingfish,respectively.Ind)[49]PIKANs
PINNstoreconstructthevelocityfieldfromsparsevelocityobservations areusedtoreconstructthevelocityandtemperaturefieldsinRayleigh-
fromPIV/PTVofaturbulentjet.Theiso-surfacesofthevorticitymag- Bernardconvectionfromsparseobservations
nitudereconstructedbyPINNsareshownhere.Inb)[17]andc)[252],
| 3.2 Governingequations |     |     |     | usingadataresidualr | (x,θ),definedas: |     |
| ---------------------- | --- | --- | --- | ------------------- | ---------------- | --- |
D
PIMLaimstoobtainarepresentationmodelu thatadheres (x,θ)=u(x,θ)−uˆ(x), ∈(cid:3) ,
|                  |            |                 |               | r D | x D | (12) |
| ---------------- | ---------- | --------------- | ------------- | --- | --- | ---- |
| to the governing | equations. | In the original | study by [1], |     |     |      |
theODE/PDEandboundaryconditions(BCs)areenforced
where(cid:3) ⊆(cid:3)isthedatadomain.TheobjectiveofPIMLis
D
by iteratively minimizing the strong-form residuals from tofindasolutionthatadherestoboththephysicallawsand
| the governing | equations. | The ODE/PDE | residualsr (u,θ) |                       |     |     |
| ------------- | ---------- | ----------- | ---------------- | --------------------- | --- | --- |
|               |            |             | E                | theobservationaldata. |     |     |
(u,θ)are
| andboundaryconditions(orinitialconditions)r |     |     | B   |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | --- | --- |
definedas:
3.2.1 Derivativecalculation
(x,θ)=F [u](x,θ)− f(x), ∈(cid:3) , To enforce governing laws, it is necessary to compute the
| r E | τ   | x   | E (10) |     |     |     |
| --- | --- | --- | ------ | --- | --- | --- |
(x,θ)=B [u](x,θ)−b(x), ∈(cid:3) . spatial and temporal derivatives of the approximated solu-
| r B | τ   | x B | (11) |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- |
tioninordertoconstructandpenalizePDEresiduals.Inthe
originalformulationby[1],thesederivativeswerecomputed
These residuals quantify the extent to which the approxi- exactlyusingautomaticdifferentiation(AD).ADleverages
mation u satisfies the ODE/PDE and boundary constraints thefactthatallnumericalcomputationsareultimatelycom-
specifiedinEq.1.Ifr = 0andr = 0,theapproximated positionsofafinitesetofelementaryoperations,forwhich
|     | E   | B   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
solutionsatisfiesthePDEandBCsexactly. derivativesareknown[25,100].However,ADsignificantly
Forinverseproblems,itisnecessarytoincorporateaddi- increasescomputationalcostduetotheneedforcalculating
tional observations within the domain. The disagreement and multiplying gradients at each layer, which can become
between theobservations andpredictions canbequantified inaccurateforhigher-orderderivatives[31]andinfeasiblefor
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 11 of 43 15
fractional operators or high-dimensional problems [19]. To lenging in such cases since the requirements for derivative
addressthesechallenges,severalstudieshaveexploredalter- calculationincreasewiththenumberofdimensions.Alterna-
nativestoorenhancementsofbackpropagation(Figs.9,10, tiveapproachestoADhavebeenproposed,particularlyfor
11,12and13). high-dimensional problems. For instance, [108] introduced
aGaussian-smoothedmodelwithStein’sidentitytoparam-
| AlternativeDifferentiationMethods |     |     | Limetal.[94]proposed |     |     |     |     |     |     |     |
| --------------------------------- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- |
eterizePINNs,bypassingbackpropagationandaccelerating
| approximating | derivatives | using | finite differences, |     | which |     |     |     |     |     |
| ------------- | ----------- | ----- | ------------------- | --- | ----- | --- | --- | --- | --- | --- |
convergence.Additionally,[19]proposedStochasticDimen-
| speeds up | computation; | however, | this method | relies | on a |     |     |     |     |     |
| --------- | ------------ | -------- | ----------- | ------ | ---- | --- | --- | --- | --- | --- |
sionGradientDescent(SDGD),amethodthatdecomposes
| predefined | grid, limiting | its | broader applicability. |     | Other |              |         |                    |                 |     |
| ---------- | -------------- | --- | ---------------------- | --- | ----- | ------------ | ------- | ------------------ | --------------- | --- |
|            |                |     |                        |     |       | the gradient | of PDEs | and PINN residuals | into components |     |
approaches[95,101]involvepredictingderivativesasaddi-
correspondingtodifferentdimensions.Duringeachtraining
tionalnetworkoutputsandlearningtherelationshipthrough
|              |                |     |                   |              |     | iteration, | a subset of these | dimensional | components | is ran- |
| ------------ | -------------- | --- | ----------------- | ------------ | --- | ---------- | ----------------- | ----------- | ---------- | ------- |
| an auxiliary | loss function. | To  | handle fractional | derivatives, |     |            |                   |             |            |         |
domlysampled,resultinginahighlyefficientapproachthat
| several | studies have | employed | Monte Carlo | methods | [23, |     |     |     |     |     |
| ------- | ------------ | -------- | ----------- | ------- | ---- | --- | --- | --- | --- | --- |
enablessolvingPDEswithupto100,000dimensions.
102–106].
High-Dimensions
|     |     |     |     |     |     | 3.2.2 ODE/PDEreformulations |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | --- |
OneofthemainadvantagesofPIMLmethodsistheirability
tohandlehigh-dimensionalproblems[100,107].However,
ToenhancetheperformanceofPIMLmodels,severalstudies
computing derivatives with AD becomes particularly chal- haveproposedreformulationsoftheODE/PDEs.
Fig.9 Applicationsinmechanicsandmaterialsscience.a)Compar- toestimatethedeformationinafullyclampedhyperbolicparaboloid
ingtheplasticzonesaroundadefectinmaterialestimatedbyPINNsand subjecttogravitationalloading.c)Materialidentification[262]byinfer-
FEM[256].b)[258]usesPINNsbasedonstrongandweakformulations ringthenon-homogeneousshearmodulusfromthedeformations
123

15 Page 12 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
Fig.10 Applicationsin
Geophysics.a)Comparingthe
plasticzonesaroundadefectin
materialestimatedbyPINNs
andFEM[256].b)The
earthquakehypocentresare
estimatedusingHypoSVIthat
blendsPINNswithStein
VariationalInference[265]
Fig.11 Applicationsin
dynamicalsystems,control,
andautonomy:(a)
Flower-shapedTuringpattern
obtainedbysolvingthe2D
Gray-Scottsystemusing
PINNs[277].(b)Thereference
trajectoryandthePINN-based
modelpredictivecontrol
trajectoryforthetracking
probleminamulti-link
manipulator[278].(c)The
imageontheleftshowsa
pictureoftheDeepseaWarriors
Uboat(DW-Uboat)intheQin
HuaiRiver,China,fromthe
experimentsconductedby[279].
Theinsetshowsaprofileofthe
DW-Uboat.APINNisusedto
predictthesurge,sway,and
rotationvelocitiesofthe
unmannedsurfacevehicleusing
thedatacollectedfromzig-zag
trajectories(redcurveinthe
imageontheright).
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 13 of 43 15
Fig.12 Applicationsin
physics:(a)Input2D
wide-anglescatteringpattern,
thereconstructed&groundtruth
nanoscalestructureandthe
simulatedscatteringpattern
usingthepredicted
structure[296].(b)Aschematic
from[303],whereaPINNis
usedtotrackthetrajectoryof
spacedebrisafterinelastic
collisionwithasatellite.(c)A
schematicofananocylinder
withconstantpermittivity
coatedwithacloakingmaterial
tozerooutthescattering[304].
Thecorrespondingelectricfield
distributionwiththecoating
layerpermittivitypredicted
usingaPINNisalsoshown
Fig.13 Applications in chemical engineering: (a) Applications of bedgranularadsorptionreactor[339].(d)Concentrationprofileofthe
PINNsinChemicalEngineering.(b)PredictionresultsofPINNsfor speciesalongtheradiusandlengthofthereactoraspredictedbyPINNs
cyclicvoltammetry[298].Temporalspatialconcentrationprofile(top) (right)andFDM(left)attemperature370K[329].(e)PINNsprediction
andthevoltammogrampredictedbyPINNs(blueline)comparedwith (upperhalf)andtheDNSresults(bottomhalf)in2Dlaminarpremixed
thevoltammogramgenerated(bottom).(c)PredictionofPINNsinfixed- combustion[335]
123

15 Page 14 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
Non-dimensionalization residuals by projecting them onto a suitable space of test
As discussed in [109], one of the simplest and most effec- functions V [99]. In the variational form, the residuals are
| tive ways                                             | to improve | model |     | performance | is  | through non- | representedas: |          |     |     |     |     |
| ----------------------------------------------------- | ---------- | ----- | --- | ----------- | --- | ------------ | -------------- | -------- | --- | --- | --- | --- |
| dimensionalizingthegoverningequations.Inthisapproach, |            |       |     |             |     |              |                | (cid:11) |     |     |     |     |
theinputsandpredictedoutputsarescaledusingcharacter- R (u)= (x,θ)v dx,
|              |         |     |          |           |                 |     | e,j | r e             |     | j   |     |     |
| ------------ | ------- | --- | -------- | --------- | --------------- | --- | --- | --------------- | --- | --- | --- | --- |
| istic units, | helping | to  | identify | important | non-dimensional |     |     | (cid:11)(cid:3) |     |     |     |     |
numbers (e.g., Reynolds, Peclet, Prandtl, Rayleigh) that R (u)= (x,θ)v dx,
|     |     |     |     |     |     |     | b,j | r   | b   | j   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
characterizethesolution’sbehavior.Additionally,choosing
(cid:3) B
appropriatecharacteristicunitscancontrolthemagnitudeof
the inputs and outputs, which is crucial for stabilizing the where v represents a chosen test function. Ideally, the
j
exactsolutionisobtainedwhenallresidualsareidentically
trainingprocess.Severalstudieshavesuccessfullyapproxi-
matedsolutionstoPDEsintheirnon-dimensionalform[17, zero[99].Varioustypesoftestfunctionshavebeenproposed,
|     |     |     |     |     |     |     | including | Dirac-delta | functions | [98], | global | [112], piece- |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----------- | --------- | ----- | ------ | ------------- |
18,20,36,37,49,90,110].
wise[114]polynomials,andnon-overlappingfunctions[99].
|     |     |     |     |     |     |     | ThevPINNformulationhas |     |     | alsobeen | explored | inthecon- |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | -------- | -------- | --------- |
EquivalentandAuxiliaryFormulations
Anotherapproachtoimprovingmodelperformanceinvolves textofmesh-freemethods[115],variablecoefficients[116],
volume-weightedmethods[117],andhasbeenoptimizedfor
| transforming | the | governing |     | equations | into | an equivalent |     |     |     |     |     |     |
| ------------ | --- | --------- | --- | --------- | ---- | ------------- | --- | --- | --- | --- | --- | --- |
form that simplifies the optimization problem. For exam- computationalefficiency[118,119].
ple,Wangetal.[36]andsubsequentstudies[57]solvedthe
Navier-Stokes equations using the streamfunction formula- FractionalDifferentialEquations
tion, which inherently satisfies the conservation of mass, Anotherextensioninvolvesfractionaloperators,givingrise
thereby reducing the number of constraints to optimize. tothefractionalPINNs(fPINNs)framework,firstintroduced
Similarly, Jin et al. [20] reformulated the Navier-Stokes by [23]. Several studies have explored and expanded upon
equations into their vorticity formulation, achieving better thefPINNformulation[102–106,120].Forexample,[104]
performance.Basiretal.[111]introducedanauxiliaryvortic- proposed a Monte Carlo-based method to solve fractional
ityvariable,whichloweredtheorderoftheStokesequations, partialdifferentialequationsonirregulardomains.Further-
furthersimplifyingtheproblem.Insomecases,theserefor- more, [105] provided a theoretical analysis to estimate the
trainingandgeneralizationerrorsfortheψ-Caputotypefrac-
| mulations | are necessary |     | to achieve |     | an acceptable | solution. |     |     |     |     |     |     |
| --------- | ------------- | --- | ---------- | --- | ------------- | --------- | --- | --- | --- | --- | --- | --- |
Forinstance,Toscanoetal.[49]reformulatedtheRayleigh- tionalPDE.Lastly,[106]extendedthefPINNframeworkto
Bénardequationsusingthevorticityformulation,eliminating overcomethecurseofdimensionalityinfractionalandtem-
thepressuredependenceandenablingtheinferenceoftem- peredfractionalPDEs.
peraturefromsparseturbulentvelocitydata.Similarly,Wang
etal.[110]reformulatedtheNavier-Stokesequationswithan StochasticDifferentialEquations
entropy-viscositymethod,allowingfortheapproximationof Stochastic Differential Equations (SDEs) have also been
solutionsathighReynoldsnumbers. explored within the PIML framework. For instance, [75]
|     |     |     |     |     |     |     | utilized | GANs as | a representation |     | model and | applied auto- |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------- | ---------------- | --- | --------- | ------------- |
maticdifferentiationtoencodethegoverninglawsforsolv-
3.2.3 DifferentialOperatorVariations
|     |     |     |     |     |     |     | ing SDEs. | Similarly, | [121] | combined | spectral | dynamically |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---------- | ----- | -------- | -------- | ----------- |
orthogonal(DO)anddynamicallybiorthogonal(BO)meth-
| The PIML | approach | is  | flexible | enough | to  | solve several |          |         |         |           |      |                |
| -------- | -------- | --- | -------- | ------ | --- | ------------- | -------- | ------- | ------- | --------- | ---- | -------------- |
|          |          |     |          |        |     |               | ods with | PIML to | develop | two novel | PINN | approaches for |
typesofproblemsevenwithmultiplesolutions;forinstance,
solvingtime-dependentSDEs.Furthermore,[100]extended
Huangetal.[96]proposedhomotopyphysics-informedneu-
|                 |            |              |          |            |          |             | the PIML    | formulation   |      | to solve    | high-dimensional        | SDEs;     |
| --------------- | ---------- | ------------ | -------- | ---------- | -------- | ----------- | ----------- | ------------- | ---- | ----------- | ----------------------- | --------- |
| ral networks    | (HomPINNs) |              | for      | solving    | multiple | solutions   |             |               |      |             |                         |           |
|                 |            |              |          |            |          |             | see also    | [122] for     | more | recent PINN | algorithms              | for high- |
| of nonlinear    | elliptic   | differential |          | equations. | This     | flexibility |             |               |      |             |                         |           |
|                 |            |              |          |            |          |             | dimensional | Fokker-Planck |      | and         | Hamilton-Jacobi-Bellman |           |
| allows handling |            | residuals    | in their | strong     | or weak  | form and    |             |               |      |             |                         |           |
equations.
obtainingapproximatesolutionsfromdifferenttypesofoper-
ators,leadingtovariousPIMLextensions.
| VariationalMethods |     |               |     |        |           |         | 3.3 Optimizationprocess |     |     |     |     |     |
| ------------------ | --- | ------------- | --- | ------ | --------- | ------- | ----------------------- | --- | --- | --- | --- | --- |
| Several studies    |     | have proposed |     | weakly | enforcing | the PDE |                         |     |     |     |     |     |
andboundaryconstraintsbysolvingtheprobleminitsvari- Training a PIML model involves solving an optimization
ational form. This approach, known as variational PINNs problemthatenablesarepresentationmodeltoapproximate
(vPINNs),wasintroducedby[112].SimilartotheDeepRitz the solution of a governing equation. The model parame-
Method [113], vPINNs compute weighted integrals of the tersarelearnedbyoptimizingalossfunction(i.e.,objective
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 15 of 43 15
function), which minimizes the residuals (i.e., Eqs. 10, 11, chosen to capture the spikes observed in the system. For
and12)ofthegoverningequations,boundaryconditions,and example,intheCMINNsmethod,thetumorgrowthmodel
dataobservations.Thislossfunctionisminimizedusingan following drug administration exhibits spikes that cannot
optimizationalgorithm,oftenreferredtoasan“optimizer.” be effectively represented without decomposition. Further-
Basedonthisdescription,theoptimizationprocessinPIML more,domaindecompositionisnecessaryfortheinferenceof
canbebrokendownintothreemainsubcomponents:theopti- piecewise-constant parameter values over continuous inter-
mizationproblem,theloss(i.e.,objective)function,andthe vals, enhancing the ability to capture variations in drug
optimizer. efficacyandprovidinginsightsintotolerancephenomenain
multi-doseadministration.
3.3.1 Optimizationproblem
TimeDecomposition
Fortime-dependentproblems,severalstudieshaveproposed
| The optimization |     | problem | in  | PIML | can be summarized |     | as  |     |     |     |     |     |     |
| ---------------- | --- | ------- | --- | ---- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
trainingthemodeloverashorttimeintervalbeforegradually
| minimizing | a multi-objective |     |     | loss function | that | encourages |     |     |     |     |     |     |     |
| ---------- | ----------------- | --- | --- | ------------- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- |
expandingthetrainingwindowuntiltheentiretimedomain
| the model | to        | satisfy constraints |     | related         | to      | boundary      | con-   |              |                |           |             |          |              |
| --------- | --------- | ------------------- | --- | --------------- | ------- | ------------- | ------ | ------------ | -------------- | --------- | ----------- | -------- | ------------ |
|           |           |                     |     |                 |         |               |        | is covered   | [55, 141–145]. | A unified | approach    |          | of the vari- |
| ditions,  | governing | equations,          |     | and potentially |         | observational |        |              |                |           |             |          |              |
|           |           |                     |     |                 |         |               |        | ous proposed | methods        | for wave  | propagation | problems | was          |
| data. To  | simplify  | this problem,       |     | several         | studies | have          | sought |              |                |           |             |          |              |
presentedin[146].
toreducethenumberofconstraints.Forinstance,insystems
| of PDEs,[21]proposed |     |     | using | numerical | solvers | toprovide |     |     |     |     |     |     |     |
| -------------------- | --- | --- | ----- | --------- | ------- | --------- | --- | --- | --- | --- | --- | --- | --- |
TransferLearningandCurriculumTraining
| easily accessible |     | high-fidelity |     | data, using | the | PIML | model |                  |         |              |     |       |            |
| ----------------- | --- | ------------- | --- | ----------- | --- | ---- | ----- | ---------------- | ------- | ------------ | --- | ----- | ---------- |
|                   |     |               |     |             |     |      |       | These strategies | involve | initializing | the | model | parameters |
primarilytouncoverhiddenfieldsthataredifficulttorecover
bypretrainingonasimplerproblemandthenretrainingon
withtraditionalmethods.Otherapproachesaimtosimplify
|             |         |        |     |                |     |          |      | the target | problem. Once | the model | is pre-trained, |     | transfer |
| ----------- | ------- | ------ | --- | -------------- | --- | -------- | ---- | ---------- | ------------- | --------- | --------------- | --- | -------- |
| the problem | through | domain |     | decomposition, |     | learning | from |            |               |           |                 |     |          |
learningapproaches[147–151]demonstratethatfine-tuning
low-fidelitydata,andsequentialtrainingstrategies.
|     |     |     |     |     |     |     |     | only the | final layers can | significantly | improve |     | model per- |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ---------------- | ------------- | ------- | --- | ---------- |
DomainDecomposition formance. Curriculum training, by contrast, progressively
Thebaselineapproachfordomaindecompositionwasintro- increasestheproblemcomplexityandhasprovenusefulfor
duced in the extended PINNs (XPINNs) framework [130] systemsofPDEs[31,109,142,152]aswellasinverseprob-
andcanbesummarizedasfollows.First,thetrainingdomain lems [47, 49, 90, 140]. For instance, [109] solved the 2D
(cid:3)isdividedinto N smallersubdomains(cid:3) ⊂ (cid:3).Then, N Navier-StokesequationsathighReynoldsnumbers(Re)by
i
PIMLsubmodelsaretrainedtoapproximatethesolutionon gradually increasing the Reynolds number during training.
eachsubdomain(cid:3) .Variousstudieshaveexploredmethods Notably,[31]proposedinitializingthelastlayer(i.e.,linear)
i
(cid:3)
for optimally partitioning and ensuring communication using least squares and then employing an adaptive resid-
i
between the submodels. For example, [130–132] proposed ual connection that progressively includes deeper layers as
incorporatinganadditionallosstermforinterfaceconditions necessary. Other curriculum training methods include pre-
toensurethatsubmodelpredictionsandresidualsalignatthe trainingonsimulateddataortheoreticalmodels,alternating
subdomainboundaries.ConservativePINNs(cPINNs)[133] betweenlearnedfields[152],oradjustingthelossfunctionto
followasimilarapproach,ensuringthecontinuityoffluxes focusonrefiningthesolution[49,90].Forinverseproblems
across subdomains, akin to traditional numerical methods. thatrequireinferringhiddenfields,[49]suggestedfirstfitting
Additionally,[134]introducedasoftdomaindecomposition thedataandboundaryconditions,thenlearningatheoretical
method using a shared subnetwork to route inputs into dif- representationofthehiddenfield,andfinallyincorporating
ferentsubmodels.Similarmethodshavealsobeenpublished thefullphysics.Usingthisapproach,theauthorssuccessfully
in [26, 99, 124, 135–139], achieving accelerated training, inferredhiddentemperaturefieldsfromsparseexperimental
easyparallelization,andimprovedaccuracy. turbulentvelocitydata.
| SequentialTraining |     |     |     |     |     |     |     | MultiFidelityandstackedtraining |     |     |     |     |     |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | --- |
Multifidelityandstackedtrainingmethodshavebeenemplo-
| Sequential | training | can | be viewed | as  | a form | of “problem |     |     |     |     |     |     |     |
| ---------- | -------- | --- | --------- | --- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- |
decomposition,” where the model learns or satisfies objec- yed to improve the prediction accuracy of PINNs. Mutli-
|                     |     |        |     |           |          |     |       | fidelity PINNs | proposed | in [153] | provide | a framework | for |
| ------------------- | --- | ------ | --- | --------- | -------- | --- | ----- | -------------- | -------- | -------- | ------- | ----------- | --- |
| tives sequentially. |     | Ahmadi | et  | al. [140] | proposed | a   | novel |                |          |          |         |             |     |
method for addressing specific challenges in inverse prob- integratinglow-andhigh-fidelitydata.Thismodelinvolves
fourneuralnetworks:thefirstapproximateslow-fidelitydata,
| lems, where | the | values | of constant |     | parameters | change | at  |     |     |     |     |     |     |
| ----------- | --- | ------ | ----------- | --- | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- |
specifictimesandthesystemexperiencesabruptspikesdue thesecondandthirdlearnlinearandnonlinearcorrelations
betweenthelow-andhigh-fidelitydata,andthefinalnetwork
tosuddeninputchanges.Inthiscase,itisessentialtotrain
the model on sequential intervals, which are strategically encodestheunderlyingPDEs.Themultifidelityapproachhas
123

15 Page 16 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
beenextendedtoBayesiannetworks,quantifyinguncertain- where Nβ,α is the batch size, representing the number of
ties in the prediction [154]. Another approach to learning points x
i
in the subset Xβ,α, sampled from a probabil-
frommulti-fidelitydatahasbeenproposedin[155],involving ity density function pα over the domain (cid:3) α. Similar to
aNNtoapproximatethelow-fidelitydataandasubsequent weightedMonteCarlomethods[159],thediscreteresiduals
NNtolearnthecorrectiontermusingthehigh-fidelitydata f(rα (x
i
,θ))arescaledusingpointwisemultipliers,referred
and aphysics-informed loss.Multifidelity approaches have toaslocalweightsλ α,i .
been successfully applied to solve the inverse-water wave DefiningasuitableLiscrucialtoensurethatmodelpredic-
problem governed by Serre-Green-Naghdi equations [34]. tionsalignwiththePDEsolution,andongoingresearchhas
Stacked training techniques, presented in [123, 156], is focusedonrefiningfourkeycomponents:theglobalweights
another approach to improve the prediction accuracy in (mα), the local weights (λ α,i ), the choice of function (fα),
PINN. By stacking networks sequentially, the output from and the sampling strategy, which is indirectly based on the
eachstepservesaslow-fidelityinputforsubsequentstages, probability density function (pα) and the number of points
allowingthemodeltorefinepredictionsprogressively.This (Nα).
approachhasbeenfurtherimprovedin[157]bycombining
GlobalWeights
multi-fidelitystackingwithdomaindecompositionmethods,
The global weights (mα) balance the contribution of each
makingitpracticalformultiscaletime-dependentproblems.
loss subterm and ensure that all constraints are satisfied.
A multi-stage neural network was introduced in [156] to
These weights can be either fixed, as in the original PIML
tacklespectralbiasbydividingthetrainingintostages,where
framework [1, 18], or dynamic, adjusting their magnitude
eachstageinvolvestraininganewNNtofittheresiduefrom
during training. In particular, Wang et al. [36] proposed a
the previous stage. Also, [158] presented an approach to
learning rate annealing algorithm that dynamically adjusts
combine different neural networks of varying fidelities by
the global weights based on back-propagated gradients.
exploitingtheirlow-rankstructure.
Thisapproachimprovedperformanceandwassuccessfully
appliedindiverseapplications[20,37,160].Similarly,self-
3.3.2 Lossfunctionmodifications adaptive loss balancing methods, such as those proposed
by [161], also dynamically adjust global weights during
The loss function (L) quantifies the disagreement between training. Liu et al. [162] developed a dual-dimer method
theapproximationprovidedbytherepresentationmodeland fortrainingPINNswithaminimaxarchitecture,optimizing
known information from the PDE solution, such as bound- theglobalweightstomanagecomplexmulti-objectiveprob-
ary conditions, ODE/PDE residuals, and data. Training in lems.Additionally,Basiretal.[111]exploredfailuremodes
PIML involves iteratively minimizing the loss subcompo- in PINNs and refined global weight strategies to enhance
nents(L α)overtheirrespectivedomains(cid:3) α.Ingeneral,L
modelrobustness.Finally,specificformsofsequentialtrain-
canberoughlyrepresentedas: ingcanbeseenasiteration-basedweightadjustments,where
(cid:11) themodel’slearningprocessevolves.Forexample,Wanget
(cid:6)
al. [55] introduced a causal parameter for time-dependent
L(θ)= mα fα (rα (x,θ))dx, (13)
α∈C
(cid:3)α problems, which forces the model to learn sequentially,
adjustingtheweightsbasedontimestepstocapturecausality.
Overall,globalweights-whetherstatic,dynamic,oriteration-
where C = {D,B,E,...} is an index specifying the loss
based-play a critical role in ensuring the effectiveness of
groups,e.g.,data(L ),boundary(L ),andequation(L ).
D B E
Thefunction fα
:R→R+
isapositive,preferableconvex,
PIMLmodels,andongoingresearchcontinuestorefinethese
weightstoimproveperformance.Inparticular[97]extended
function applied to the residuals rα of each subcomponent
the Neural Tangent Kernel(NTK) to PIML and proposed a
(i.e., Eqs. 11, 10, and 12), and mα are scalar weights that
novel adaptive global weighting training strategy that sig-
balance the contributions of each term, often referred to as
nificantlyenhancethetrainablityandpredictiveaccuracyof
globalweights.
PIMLmodels.
To enable computation, this expression is typically dis-
cretized and computed iteratively over finite subdomains
LocalWeights
Xβ,α ⊂(cid:3) α asfollows:
One of the main challenges in PIML is that residuals at
key points can be underrepresented in the overall summa-
(cid:6) N(cid:6)β,α
tion of the objective function (Eq. 14). As a result, despite
L(θ,Xα,β )= mα λ α,i f(rα (x i ,θ)), a decrease in total loss during training, certain spatial or
α∈C i=1
temporal characteristics might not be fully captured. This
wherex
i
∈ Xα,β , (14)
issue becomes particularly pronounced in multiscale prob-
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 17 of 43 15
lems,whereregionsofinterestmaylackdetail,andimportant HypercubeSampling(LHS),Halton,Hammersley,andSobol
| information | from | the initial | and | boundary | conditions |     | may | sequences. |     |     |     |     |     |     |
| ----------- | ---- | ----------- | --- | -------- | ---------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
not propagate effectively through the domain, thereby hin- However,recentstudieshavedemonstratedthatuniform
dering convergence [38]. To address this issue, researchers samplingmethodsareofteninsufficient,particularlyforsolv-
λ
have proposed assigning local weights α,i to balance the ing PDEs with sharp gradients [125]. This has led to the
contributionofeachresidualpoint,thusincreasingfocuson developmentofadaptivesamplingmethods,whichdynami-
thechallengingregionsinbothspaceandtimedimensions. callyadjustthesamplingofresidualpointsbasedoncertain
McClenny et al. [163] introduced a self-adaptive (SA) criteria. Broadly, adaptive sampling can be classified into
approach,whereindividuallossweightsareadjustedthrough two main strategies: (1) Resampling (adaptive pα), where
adversarialtraining.Buildingonthisidea,Zhangetal.[164] allresidualpointsareresampledafterafixednumberofitera-
proposed a differentiable adversarial self-adaptive (DASA) tionsaccordingtothespecifiedcriteria,and(2)Incremental
weighting scheme, which uses a subnetwork to optimize sampling (adaptive Nα), where an initial set of residual
the local multipliers. Basir et al. [165] developed the points is sampled, and additional points are incrementally
physics and quality-constrained artificial neural network addedduringtraining,guidedbyeitherthesameordifferent
| (PECANN), | which | calculates |     | local weights |     | based | on the | criteria. |     |     |     |     |     |     |
| --------- | ----- | ---------- | --- | ------------- | --- | ----- | ------ | --------- | --- | --- | --- | --- | --- | --- |
residualsofconstraints,suchasinitialandboundarycondi- Adaptivesamplingmethodsemployvariousselectioncri-
tions, using the augmented Lagrangian method. PECANN teria. While uniform sampling methods may serve as a
has since been expanded with adaptive versions, such as baseline,non-uniformcriteriaaremorecommonlyused.The
|            |     |                   |     |        |          |     |        | mostprevalentapproachdefines |     |     | pα  | tobeproportionaltothe |     |     |
| ---------- | --- | ----------------- | --- | ------ | -------- | --- | ------ | ---------------------------- | --- | --- | --- | --------------------- | --- | --- |
| PECANN-AL, |     | which incorporate |     | global | Lagrange |     | multi- |                              |     |     |     |                       |     |     |
pliers [111, 166]. Similarly, Son et al. [167] introduced an PDE residual, concentrating the sampling in regions where
|           |            |            |     |        |     |       |      | the residual | is  | large [40, 49, | 125, | 173–181]. | This | strategy |
| --------- | ---------- | ---------- | --- | ------ | --- | ----- | ---- | ------------ | --- | -------------- | ---- | --------- | ---- | -------- |
| augmented | Lagrangian | relaxation |     | method | for | PINNs | (AL- |              |     |                |      |           |      |          |
PINNs), where the initial and boundary conditions act as enhances the distribution of residual points by focusing on
areasthatcontributemostsignificantlytothePDEloss.Alter-
constraintstooptimizethePDEresidual.
Anagnostopoulos et al. [168] introduced residual-based natively,othermethodsprioritizehigh-errorregionswithout
attention(RBA)weights,whereλ directly relying on the PDE residual. For example, [49]
α,i iscomputedusingthe
λ
exponentially weighted moving average of the residuals. proposed using pre-computed local multipliers α,i , which
|     |     |     |     |     |     |     |     | encode | historical | information | about | high-error |     | regions, to |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ---------- | ----------- | ----- | ---------- | --- | ----------- |
Sinceresidualscontaininformationaboutregionswithhigh
error,thismethodprovedtobehighlyeffective,outperform- update pα ateverytrainingiterationwithnegligiblecompu-
ing previous approaches with minimal computational cost. tational cost. Another approach, failure-informed adaptive
Thesetechniqueshavebeenfurtherdevelopedandrefinedin sampling [182, 183], defines a failure probability function
subsequentstudies[16,169–171].Notably,Chenetal.[171] andaddsnewresidualpoints(i.e.,increases Nα)inregions
extendedbothSAandRBAmethodsusingtheNeuralTan- wherethisprobabilityexceedsapredefinedthreshold.
| gent Kernel | [97] | and analogies |     | to traditional |     | numerical |     |     |     |     |     |     |     |     |
| ----------- | ---- | ------------- | --- | -------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
FunctionSelection
| methods,     | resulting | in a | robust | and improved |     | algorithm | for |                 |     |        | R+  |                        |     |     |
| ------------ | --------- | ---- | ------ | ------------ | --- | --------- | --- | --------------- | --- | ------ | --- | ---------------------- | --- | --- |
|              |           |      |        |              |     |           |     | AsshowninEq.13, |     | fα : R | →   | isapositive,preferable |     |     |
| calculatingλ |           | .    |        |              |     |           |     |                 |     |        |     |                        |     |     |
α,i
convexfunctionappliedtotheresidualsrα(i.e.,Eqns.11,10,
Sampling and 12). This function aims to transform the residuals and
L
AsshowninEq.14,PIMLmodelsareiterativelyoptimized give the required characteristics to be optimizable. The
onNαpointsfromadiscretesubdomainXβ,α,whichissam- most prevalent choice of this function is fα (z,p) = |z|p,
(cid:3) whichtransformsLintothethesumofLp (cid:5)normoftheresid-
| pled from | α   | using a suitable |     | probability | density | function |     |     |     |     |     |     |     |     |
| --------- | --- | ---------------- | --- | ----------- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
(x)(cid:6)p
pα.Inthiscontext,thesamplingmethodreferstothespecific uals for each lossC subcomponent,(L = (cid:6)rα ).
|          |        |                                     |     |     |     |     |     |                                         |     |     |     |     | α∈C | p         |
| -------- | ------ | ----------------------------------- | --- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- | --------- |
|          |        |                                     |     |     |     |     |     | Noticethat,asdescribedin[107],bysetting |     |     |     |     | p   | =2anddis- |
| choiceof | Nα and | pα,whichdefinethenumberanddistribu- |     |     |     |     |     |                                         |     |     |     |     |     |           |
tionofthetrainingpoints. cretizingwithλ α,i = (1/N),werecoverthemean-squared
|     |     |     |     |     |     |     |     | error as | introduced | in the | first PINN | study | [1] | and broadly |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ---------- | ------ | ---------- | ----- | --- | ----------- |
SamplingmethodsinPIMLcanbecategorizedbasedon
uniformity, adaptability, and selection criteria. In terms of adopted in the PIML community. However, the L2 norm
|     |     |     |     |     |     |     |     | tends to | be sensitive | to outliers |     | and diminish |     | small val- |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------------ | ----------- | --- | ------------ | --- | ---------- |
uniformity,thesemethodsaredividedintouniformandnon-
uniform sampling techniques. Early approaches employed ues, so it struggles capturing small details; thus, several
|     |     |     |     |     |     |     |     | studies | propose | training by | a combination |     | of  | L1 and L2 |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------- | ----------- | ------------- | --- | --- | --------- |
simplemethodslikeequispacedgridsanduniformlyrandom
sampling[125,172].Later,moresophisticatednon-adaptive usingasequentialapproach[49]oradaptivelyviatheHuber
Loss[76,150].Ontheotherhand,Wangetal.,[107]inves-
uniformsamplingtechniqueswereintroduced,suchasLatin
123

15 Page 18 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
tigated the relationship between the loss function and the from a plateau. Also, [194] proposed augmenting the stan-
approximationqualityofthelearnedsolutionandprovedthat dardgradientdescentdirectionbyincludingsearchvectors,
forgeneralLploss,severaltypesofequationsarestableonly
whicharechosentoexplicitlyadjusttheactivationpatterns
if pissufficientlylargeanddevelopedanoblealgorithmto of the neurons, which improved the performance of two-
∞
minimize the L loss. Other types of functions have also layer rectified neural networks. On the other hand, [188]
been explored. For instance, [126] ex√perimentally showed proposedusingNon-dominatedSortingGeneticAlgorithms
|     | (z)=log(z)or |     | (z)= | |z|cansignificantly |     |     |     |     |     |     |     |
| --- | ------------ | --- | ---- | ------------------- | --- | --- | --- | --- | --- | --- | --- |
thatusing fα fα (NSGA)tohelptraditionalstochasticgradientoptimization
improvethebaselinemodelperformance.Otherstudies[90] algorithms escape local minima. Similarly [128] analyzed
proposed using the negative-log-likelihood (NLL), intro- the Pareto front, highlighted the most common pitfalls for
duced in [91–93], for inverse problems in PIML enabling multi-objectiveproblems,andcomparedthestandardmeth-
obtainingthealeatoricuncertaintyandimprovingthemodel odswithNSGA-II.
performance. Similarly, [184] proposed the stochastic par- Other studies have focused on improving gradients in
ticle advection velocimetry method, which introduces a multi-task learning [127, 189, 190]. For example, [127]
statistical data loss that improves the accuracy of inverse introducedaconflict-freeupdatealgorithmtohandlemulti-
problems in fluid dynamics. This method is based on an objective optimization, ensuring a positive dot product
explicitparticleadvectionmodelthatpredictsparticleposi- between the final update and each loss-specific gradient.
tionsovertimeasafunctionoftheestimatedvelocityfield. Conversely,[129]proposedreplacinggradientdescentwith
particleswarmoptimization,whichnotonlyimprovesperfor-
mancebutalsoallowsforthecomputationofrelateduncer-
3.3.3 Optimizer
|     |     |     |     |     |     | tainties. | Finally, | [195] | propose | Gauss-Newton’s | method in |
| --- | --- | --- | --- | --- | --- | --------- | -------- | ----- | ------- | -------------- | --------- |
Thegoaloftheoptimizeristofindtheoptimalparametersθ function space for the solution of the Navier-Stokes equa-
sothattheapproximatedsolutionmatchesascloseaspossible tions. Upon discretization, this yields a natural gradient
tothetruesolution.Thisprocessisperformediterativelyby methodthatmimicsthefunctionspacedynamicsandallows
graduallyminimizingLuntiladesiredaccuracyisreached.
|     |     |     |     |     |     | theauthors | toachieve |     | close | tosingle-precision | accuracy in |
| --- | --- | --- | --- | --- | --- | ---------- | --------- | --- | ----- | ------------------ | ----------- |
Asdescribedin[126],themostcommonoptimizersinPIML therelative L2 norm[195].
fallunderthegeneralfamilyofLineSearchMethods[185], In some applications, quasi-Newton methods such as
whereθ areupdatedasfollows: BFGSorL-BFGS[187]canbeusedtoachievebetterperfor-
mancewithfeweriterations,thoughtheyaremoreproneto
| θk+1 =θk | +αkpk, |     |     |     |      |                                                       |     |     |     |     |     |
| -------- | ------ | --- | --- | --- | ---- | ----------------------------------------------------- | --- | --- | --- | --- | --- |
|          |        |     |     |     | (15) | gettingtrappedatsaddlepoints[126].Tomitigatethis,some |     |     |     |     |     |
pk =−H ∇ L(θk). (16) studiesrecommendusingAdamduringtheinitialstagesof
k θ
|     |     |     |     |     |     | training, | followed | by  | L-BFGS | for fine-tuning | [1, 20, 126]. |
| --- | --- | --- | --- | --- | --- | --------- | -------- | --- | ------ | --------------- | ------------- |
Here,αk isthestepsizeatiterationk,and pk isthestep Given the effectiveness of quasi-Newton methods, recent
direction,whichdependsonthelossgradient∇ L(θk)anda research has aimed atfurtherenhancing theirperformance.
θ
symmetricmatrix Hk.Underthisformulation,linearmeth- For instance, [126] proposed a modified BFGS algorithm,
|     |     |     |     |     |     | demonstrating |     | that by | selecting | an improved | optimization |
| --- | --- | --- | --- | --- | --- | ------------- | --- | ------- | --------- | ----------- | ------------ |
odssuchasgradientdescentorADAM[186]arerecovered
bysetting H = I.Ontheotherhand,quasi-Newtonmeth- method and incorporating modifications to the loss func-
k
ods,suchasL-BFGS[187],canberecoveredbysettingHkto tion,theaccuracyofsolutionscomparabletofinite-difference
anapproximationoftheHessianmatrixofL,whichrequires schemescanbeachievedinspecificexamples.Ontheother
|     |     |     |     |     |     | hand, [196] | theoretically |     | analyzed | PIML | ill-conditioning |
| --- | --- | --- | --- | --- | --- | ----------- | ------------- | --- | -------- | ---- | ---------------- |
onlyfirst-orderderivativesandhelpsachievesuperlinearcon-
vergence[126]. and introduced a novel second-order optimizer that sig-
|     |          |               |            |     |                | nificantly | improves | PIML |     | performance. | Similarly [197] |
| --- | -------- | ------------- | ---------- | --- | -------------- | ---------- | -------- | ---- | --- | ------------ | --------------- |
| Due | to their | computational | efficiency |     | and mini-batch |            |          |      |     |              |                 |
flexibility, linear methods are widely used in the PIML proposed energy natural gradient descent with respect to
|            |     |         |              |         |            | a Hessian-induced |     | Riemannian |     | metric | as an optimization |
| ---------- | --- | ------- | ------------ | ------- | ---------- | ----------------- | --- | ---------- | --- | ------ | ------------------ |
| community, | and | several | studies have | focused | on improv- |                   |     |            |     |        |                    |
ing their performance [127, 188–191]. For instance, [192] algorithm for PINNs yielding highly accurate solutions for
shallownetworks,outperformingADAMandLBFGs.This
| proposed | adopting | an  | adaptive basis | viewpoint | of neural |     |     |     |     |     |     |
| -------- | -------- | --- | -------------- | --------- | --------- | --- | --- | --- | --- | --- | --- |
networks, which led to novel initialization and a hybrid studywasextendedtodeepernetworksandfurtherimproved
|                        |     |     |                    |     |                  | in[198]. | Finally, | [199] | introduced | a two-level | overlapping |
| ---------------------- | --- | --- | ------------------ | --- | ---------------- | -------- | -------- | ----- | ---------- | ----------- | ----------- |
| least squares/gradient |     |     | descent optimizer. |     | Similarly, [193] |          |          |       |            |             |             |
proposed an iterative training method, the Active Neuron additive Schartz preconditioner strategy that can be com-
binedwithanyoptimizertoacceleratethetrainingofPIML
LeastSquares,characterizedbyexplicitlyadjustingtheacti-
| vation pattern | at  | each step, | designed | to enable | a quick exit | problems. |     |     |     |     |     |
| -------------- | --- | ---------- | -------- | --------- | ------------ | --------- | --- | --- | --- | --- | --- |
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 19 of 43 15
4 ApplicationsofPIML sparse datasets, paving the way for better treatment out-
comes.
Numerous studies have demonstrated the success of PIML Applications in cardiovascular engineering are also pro-
across a wide range of fields. Here, we provide a selec- found, as evidenced by studies on intraventricular flow
tive yet comprehensive review of PIML applications in mapping[228],cufflessbloodpressureestimation[229],and
biomedicine, mechanics, geophysics, dynamical systems, modelingaorticbloodflow[230]usingPINNs.[231]demon-
controlandautonomy,heattransfer,physics,chemicalengi- strated the utilization of PINNs in modeling active cooling
neering,andothermiscellaneousareas. withinvascularsystems,indicatingthebroadutilityofPINNs
inthermoregulationstudieswithinbiologicalcontexts.Over-
all,PINNsaresettingnewstandardsinmedicaldiagnostics
4.1 Applicationsinbiomedicine andpersonalizedmedicinebyprovidingarobustframework
thatintegratescomputationalmodelswithreal-worldmedi-
ThepotentialofPINNshavebeendemonstratedacrossawide caldata[18,37,73,205,209,214–216,218,219].
rangeofbiomedicalapplications,includingsystemsbiology, In the field of systems pharmacology, PINNs solve the
systems pharmacology, biomechanics, and epidemiology. compartment model to predict the assimilation of drugs
By integrating biophysical laws with data-driven learning, in the human body, enhancing the understanding of phar-
PINNsofferapowerfulframeworkforsolvingcomplexprob- macokinetics for better therapeutic outcomes [47, 209]. In
lemsinthesefields. thisstudy[210],PINNsareemployedtouncoverunknown
In systems biology, for example, PINNs have been components in differential equations modeling chemother-
employedtomodeldynamicbiologicalprocesses.Notably, apy pharmacodynamics. Additionally, a pharmacodynamic
theworkby[201]and[202]successfullyappliedPINNsto study [211] explores the effectiveness of the Verhulst and
modelcomplexbiochemicalreactionsandconductparameter Montroll models in simulating tumor cell growth through
identification for system-level biological processes. Build- the application of PINNs. In a recent work [140], Com-
ing on this, the AI-Aristotle framework [47] has further partmentModelInformedNeuralNetworks(CMINNs)was
demonstratedtheadaptabilityofPINNsinbothsystemsbiol- proposedasameansoftransformingcompartmentalmodel-
ogyandsystemspharmacologygray-boxdiscovery,showing ing, with the objective of enhancing pharmacokinetic (PK)
how these models can handle the intricate dynamics of andintegratedpharmacokinetic-pharmacodynamic(PK-PD)
biological systems [47]. Beyond these applications, PINNs modeling. This approach incorporates fractional calculus
havealsobeenleveragedtoexplorecellularsignalingpath- and time-varying parameters, combined with constant or
ways.Forinstance,[203]introducedDensity-PINNstoinfer piecewise-constantparameters,providinginsightsintodrug
transduction-timedistributionsincellularsignaling,provid- dynamicsincancerandrevealingthedynamicsofcancercell
inginsightsintohowresponsetimescontributetocell-to-cell deathinmulti-doseadministrations,whichmayexhibitresis-
heterogeneity.Thisunderstandinghasthepotentialtoinform tance, persistence, and tolerance. Recent research demon-
moreeffectivediseasetreatmentstrategies. stratesthatusingPINNsenablescomprehensivemathemat-
Transitioning to cardiac health, PINNs have made sig- ical modeling in systems toxicology, providing a deeper
nificant stridesindiagnosingandtreatingatrialfibrillation. understanding of the effects of pharmaceutical substances
They have been used to create detailed activation maps oncardiachealth[212].Thecharacterizationofdrugeffects
for diagnosis and estimate cardiac fiber orientation from oncardiacelectrophysiologyby[213]usingPINNsmarksa
electroanatomical data,bothofwhichareessentialforper- pivotaldevelopmentinpredictivehealthcare,enablingbetter
sonalized treatment and procedural planning [204, 205]. managementofarrhythmicdisorders.
Additionally,intheareaofbloodcoagulation-acriticalpro- In the field of biomechanics, PINNs are revolutionizing
cess in hemostasis-PINNs address challenges in parameter diagnosticsandtreatmentplanningbyseamlesslyintegrating
estimationduetothedifficultyofmeasuringreactionrates. physical laws with clinical data. PINNs have proven par-
The introduction of Coagulo-Net [206] demonstrated how ticularly effective in inferring blood flow dynamics from
PINNs can infer unknown parameters and dynamics from non-invasive imaging techniques, such as 4D flow MRI,
sparse and noisy data, offering a robust solution to model- enablingdetailedanalysesofcardiovascularconditionslike
ing blood clotting. Similarly, TGM-Net has been proposed intracranial aneurysms and stenosis [18, 214–217]. These
in [207] to facilitate tumor growth forecasting. Finally, in networks are adept at handling noisy, sparse data, facilitat-
electrophysiology,theprecisesimulationofactionpotentials ing the calibration of conventional models, and predicting
and the estimation of electrophysiological tissue properties flow fields without extensive simulation data, thus enhanc-
are essential for diagnosing and treating arrhythmias such ingdiagnosticaccuracyandefficiency[214–216].Moreover,
asatrialfibrillation.[208]presentedEP-PINNs,whichoffer PINNscontributetothenon-invasiveinferenceofthrombus
highly accurate simulations and parameter estimation from materialproperties,facilitatingtheestimationofpermeabil-
123

15 Page 20 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
ity and viscoelastic moduli, which are vital for assessing parameters across several compartmental models, illustrat-
treatmentoptions[218].Thistechnologyalsoenhancesthe ing their potential in refining epidemiological predictions
quality of medical imaging through super-resolution and and parameter discovery [237]. This study [238] explores
denoising of 4D flow MRI, making it more reliable for multiple epidemiological models using PINNs to identify
clinical applications [73, 219]. Liu et al. [220] extended time-varying parameters and fractional differential opera-
PINNs to model the mechanical behavior of soft biologi- tors.VariousextensionsoftheclassicSIRmodel,including
caltissues,providingcrucialinsightsintotissuemechanics, fractional-order and time-dependent parameters, are exam-
which are essential for medical simulations and prosthetic ined. By applying these methods to COVID-19 data from
design. Similarly, [221] utilized these networks to derive New York, Rhode Island, Michigan, and Italy, the work
mechanisticinsightsfromsparseexperimentaldata,enhanc- simultaneously infers both unknown parameters and unob-
ingthemodelingofbiologicalphenomena.Anovelmethod serveddynamics.Theresearchhighlightstheidentifiability
proposed in another study [222] employed PINNs to fit ofmodelparametersanduncertaintiesrelatedtoneuralnet-
DCE-MRIdata,incorporatingcontrastagentdiffusionwhile worksandcontrolmeasures,offeringinsightsintopandemic
ensuringcompliancewithmassconservationequationsfrom forecasting.Theseapplicationsdemonstratethecapabilityof
thepharmacokineticmodel,resultinginenhancedpredictive PINNstoprovideadeeperunderstandingofdiseasedynam-
accuracy. Recent research has demonstrated the versatility ics,makingtheminvaluableintheongoingeffortstomanage
of PINNs in modeling various aspects of tissue behavior, publichealthcrises.
includingthermalproperties,biomechanicalresponses,and
elasticity[223–225].Notably,[226]appliedPINNstotackle
theinverseproblemoftissueelasticityreconstructioninMag- 4.2 Applicationsinmechanics
netic Resonance Elastography, showcasing the potential of
thesemethodsforunderstandingandengineeringbiological 4.2.1 Fluidmechanics
tissues. Additionally, [227] introduced a hybrid PINN that
reconstructs3Dtissuedynamicsfromsparse2Dimagesby PINNshavemadesignificantstridesacrossawidearrayof
integratingfluiddynamicswithsofttissuemodelingforclin- applicationsinfluidmechanics,showcasingtheirversatility
icaldiagnostics. androbustcapabilitytosolvecomplexproblemsbyintegrat-
PINNs have been adapted to address a range of epi- ingphysicallawswithmachinelearning.
demiological models, including the susceptibles-infected- Inimagingandflowvisualization,PINNshavebeenpiv-
recoveredframeworksandtheirextensions.Forinstance,bi- otal in inferring complex fluid dynamics such as the 3D
objectiveoptimizationhasbeenemployedtotrainPINNson velocityandpressurefieldsfromtemperaturedataintomo-
theSusceptible-Vaccinated-Infected-Hospitalized-Recovered graphicbackgroundorientedSchlierenimaging,exemplified
(SVIHR) model, which includes compartments for leaky- by studies like the flow over an espresso cup [17]. Cai
vaccinated and hospitalized populations, demonstrating a et al. [239] reconstructs the velocity field in a turbulent jet
sophisticated approach to managing the trade-off between from sparse observations available from Particle Tracking
data fit and model fidelity [232]. In a practical applica- Velocimetry (PTV). This technique also extends to bio-
tion, PINNs were used to model COVID-19 infection and logicalflows,wherePINNsaccuratelyreconstructpressure
hospitalizationscenariosbasedondatafromGermany,prov- fieldsaroundswimmingfishfromParticleImageVelocime-
ing their effectiveness in comparison to traditional finite try (PIV) data, providing insights that surpass traditional
difference methods [233]. A recent work [234] devel- methods[240].
oped a PINNs model for estimating temporal changes in Forturbulentandhigh-speedflows,PINNsaddressboth
the SIR model to analyze transmission dynamics during forwardandinverseproblems.Theyhandlehigh-speedflows
outbreaks. Furthermore, the concept of Disease-Informed by approximating the Euler equations, solving problems
Neural Networks (DINNs) extends PINNs to predict the involving moving discontinuities and oblique waves, and
spread of various infectious diseases, showcasing the flex- inferringflowpropertiesfromsparsedatainsupersonicenvi-
ibilityofPINNsinhandlingepidemiologicaldata[235].The ronments[39,241].Intwo-dimensionalturbulence,PINNs
Susceptible-Exposed-Infected-Recovered(SEIR)modelhas aid in predicting flow quantities and improving the under-
beenaugmentedtoincorporateenvironmentalpathogencon- standingofsmall-scaleturbulence[242].
centrations.PINNshavebeenemployedtoaddressbothfor- PINNs also explore complex fluid behavior in non-
ward and inverse problems, thereby improving the model’s Newtonianfluids,learningtheviscosityfromvelocitymea-
effectivenessinanalyzingCOVID-19dynamicsthatinvolve surements,whichhelpsinmodelingtheflowbetweenparallel
intricateinteractionsbetweenhumansandpathogens[236]. plates-a challenging scenario for traditional models [243].
Lastly,PINNshavebeenintegratedwiththeExtremeTheory Similarly,inthecontextofvortexdynamicsandscalarmix-
ofFunctionalConnections(X-TFC)todynamicallyestimate ing, they provide new approaches to inferring lift and drag
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 21 of 43 15
forces on bluff bodies and enhancing the understanding of The modeling of elastic plates using PINNs showcases
scalarmixinginturbulentflows[98,244]. acomparisonbetweendata-driven,PDE-based,andenergy-
Further,PINNshavebeeninstrumentalinsolvinginverse basedapproaches,emphasizingtheefficacyofPINNsincap-
problems such as reconstructing Rayleigh-Bernard flows turing finite deformations governed by complex equations
fromtemperaturedataandmodelingrarefied-gasdynamics like the Föppl-von Kármán equations [257]. Additionally,
under the Bhatnagar-Gross-Krook approximation, showing inthecontextofshellstructures,PINNssolveforthesmall-
potentialinregimeswheredataissparseorincomplete[245, strainresponseofcurvedshells,showinghighaccuracywhen
246]. Their application extends to modeling viscoelastic PDElossisenforcedintheweakform[258].
materials, where the ViscoelasticNet framework aids in PINNsalsoenhancethephase-fieldmodelingoffracture,
understandingthecomplexstressandpressurefieldsinflu- where they predict crack paths in materials by minimizing
ids[247]. the variational energy of the system. Transfer learning is
In structural applications, PINNs facilitate the design employedtoimproveefficiency,avoidingtheneedtoretrain
of offshore structures by solving the Serre-Green-Naghdi thenetworkfromscratchforeachloadstep[259].Moreover,
equationsforwaterwaves,predictingfuturestatesofwater inthedigitalrealm,PINNspredictthedeformationofdigi-
surfaces and velocities crucial for engineering applica- talmaterialsunderload,applyingenergy-basedformulations
tions [34]. They also enhance large-eddy simulations of andinnovativelossfunctionstopreventerroneouslearning
fluidflowsbyincorporatingphysicalpriorsintothemodel- ofdeformationgradients[260].
ingprocess,improvingpredictionsacrossvaryingReynolds Forcomplexnonlinearproblemsincomputationalmecha-
numbers[248]. nics, the Integrated Finite Element Neural Network (I-
Moreover, in acoustics, PINNs solve frequency-domain FENN) combines PINNs with finite element methods to
equations for isotropic media, avoiding the high com- accelerate nonlinear solutions, showcasing the integration
putational costs associated with traditional methods and ofmachinelearningwithtraditionalnumericalmethodsfor
eliminatingnumericaldispersion[249].Theirutilityinpre- enhanced computational performance [261]. Additionally,
dicting fluid flow behaviors in complex geometries is also in elasticity imaging, PINNs are used for inverse identi-
demonstrated in the modeling of thermal creep flows and fication of nonhomogeneous mechanical properties from
vortex-inducedvibrations[250,251]. displacement measurements under loading, demonstrating
theirutilityinbiomechanicalapplications[262].
4.2.2 Solidmechanicsandmaterialscience Lastly,Physics-informedmulti-LSTMnetworksareintro-
duced for the metamodeling of nonlinear structures. These
PINNsaddressadiverserangeofcomplexproblemsacross networks incorporate physical laws into LSTM models to
different material behaviors and structural forms. In the learn dynamics from limited data, significantly enhancing
domain of nondestructive testing and evaluation, PINNs theirlearningefficiencyandextrapolationcapabilities[263].
areeffectively utilizedtoidentifyandcharacterize surface- Overall, these applications underscore the broad and
breakingcracksinmetalplates.Byestimatingthespeedof impactfulroleofPINNsinadvancingmechanicsandmaterial
sound, which varies due to the presence of cracks, PINNs sciences,offeringrobustsolutionstotraditionallychalleng-
facilitateprecisecrackdetectionfromultrasonicdata,high- ingproblemsacrossvariousmaterialbehaviorsandstructural
lightingtheirpotentialinstructuralhealthmonitoring[253]. analyses.
Similarly, PINNs are deployed to quantify microstructural
propertiesinpolycrystallinenickel,solvinginverseproblems 4.3 Applicationsingeophysics
toinfermaterialpropertieslikecompressibilityandstiffness
fromultrasonicdata,demonstratingtheircapabilityinmate- PINNs are demonstrating significant advancements in geo-
rialcharacterization[254]. physics. PINNs effectively solve the eikonal equation for
For complex fluid behavior in materials, PINNs extend seismicwavetraveltimes,enhancingapplicationslikesource
theirapplicationtomodelnon-Newtonianfluids,accurately localization and seismic inversion [264]. This flexibility
simulatingfluidswithtimeanddeformation-dependentprop- allowsthemtoincorporatecomplexconstraintslikemedium
erties. This includes generalized Newtonian, viscoelastic, anisotropyandfree-surfacetopography,whicharechalleng-
and thixotropic fluids, where PINNs recover velocity and ingfortraditionalmethods[265].Additionally,inearthquake
stressfieldseffectivelyfromsparsemeasurements[255].In hypocentre inversion, PINNs, combined with Stein Varia-
the realm of solid mechanics, PINNs are applied to infer tionalInference,rapidlyapproximateposteriordistributions,
internal structures and defects in materials, accurately pre- showingeffectivenesswithrealseismicdata[265].
dicting the size, shape, and mechanical properties of voids In compositional modeling, PINNs perform flash cal-
or inclusions from stress-displacement data, demonstrating culations to determine phase composition, achieving sig-
versatilityacrossdifferentmaterialtypes[256]. nificantly lower error rates than traditional deep neural
123

15 Page 22 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
networks by adhering to thermodynamic constraints [266]. within porous materials under various physical conditions.
For hydrological modeling, PINNs act as surrogate models Their ability to integrate and solve multiphysics problems
forwaterflowsinriverchannels,efficientlyhandlinginverse through a unified framework highlights their potential to
parameterestimationandoutperformingconventionalmod- reshapetraditionalapproachesingeosciencesandengineer-
els[267].Moreover,theytacklecomplexwavepropagation ing[276].
and full waveform inversion problems, automatically satis-
fyingabsorbingboundaryconditionsandprovidingefficient 4.4 Applicationsindynamicalsystems,controland
solutionscomparedtoconventionalsolvers[268]. autonomy
In geostatistical modeling, a physics-informed semantic
inpaintingapproachusingPINNsincorporatesindirectmea- PINNs are making impactful advancements in the fields of
surementsintogroundwaterflowmodels,demonstratinghow dynamicalsystems,control,andautonomy,providinginno-
PINNs can enhance the understanding of subsurface phe- vativesolutionstocomplexmodelingandcontrolchallenges
nomena[269].Thesediverseapplicationshighlightthebroad acrossvariousapplications.
potential of PINNs to advance geophysical investigations, In dynamical systems, PINNs are effectively used to
offeringmoreaccurate,flexible,andefficientmethodologies solve and understand the behavior of complex models like
forunderstandingandpredictinggeologicalandhydrological the1Dand2DGray-Scottsystems,overcomingchallenges
processes. related to local minima in the loss function by integrating
PINNs have proven to be highly effective in addressing datafromfiniteelementmethods[277].Forcontrolapplica-
complextransportproblemsinporousmedia,bringingsignif- tions,PINNshavebeenextendedtohandlecontrolvariables
icantadvancesacrossvariousapplications.PINNsareadept and enhance extrapolation capabilities, as demonstrated in
atsolvingpartialPDEsrelatedtohyperbolictransportprob- controllingVanderPolandfour-tanksystems,showingsig-
lems such as the Buckley-Leverett and Burgers equations, nificantimprovementsovertraditionalPINNs[280].PINNs
demonstratingaccuracycomparabletotraditionalnumerical areappliedtopredictandcontrolunmannedsurfacevehicle
methodslikeLagrangian-EulerianandLax-Friedrichs[270]. dynamics,integratingrealtrajectorydatatoenhancemodel
Inmodelingmultiphaseflowthroughporousmedia,suchas generalizationandperformance[279].Furthermore,PINNs
thedrainageofgasinwater-saturatedmedia,PINNsnotonly areintegratedintorobustadaptivemodelspredictivecontrol
estimate water saturation effectively but also solve inverse frameworks,suchasRAMP-Net,whichsignificantlyreduces
problemstoinferflowparameters,showingsuperiorperfor- trackingerrorsinquadrotorflightbyencodingbothknown
manceovertraditionaldata-drivenmethods.especiallywhen physicsanddata-driveninsights[281].PINNshavealsobeen
dataissparse[271]. used to learn the dynamics in quadrotors, demonstrating a
Further expanding their application, PINNs have been bettergeneralizationcapacitycomparedtolinearizedmath-
employed to infer key hydraulic properties and transport ematicalmodels[282]
phenomena in subsurface transport scenarios. They out- PINNshavealsobeeneffectivelyusedforcontrolappli-
perform classical neural networks by accurately predicting cations. For example, [283] combines a dynamics model
hydraulic conductivity and concentration fields using cou- learned using PINNs with model-predictive control for
pledequationslikeDarcy’slawandtheadvection-dispersion motion prediction and trajectory tracking for rigid and soft
equation [272, 273]. These networks handle both saturated continuum robots. Additionally, PINNs are used for non-
andunsaturatedflowconditionsefficiently,oftensurpassing linear model predictive control in multi-link manipulators,
state-of-the-artmethodsinparameterestimationfromnoisy wheretheyefficientlyapproximatenonlineardynamics,out-
data. performingtraditionalnumericalmethodsintermsofspeed
PINNs also address the coupled flow and deformation andaccuracy[278].Theworkby[284]usesPINNstomodel
in porous media, solving complex poroelastic problems complex deformation in a soft robotic gripper with data
using stress-split sequential training methods. They effi- assimilation, achieving better accuracy when compared to
cientlytacklebenchmarkproblemsinporoelasticity,proving FEM. Furthermore, the paper by [285] introduces a PINN-
their robustness in simulations involving both single-phase basedframeworkthatprogressivelyimprovestheefficiency
and multiphase flows [274]. In non-isothermal multiphase of motion planning in dynamic environments, enhancing
poromechanics, PINNs facilitate inverse modeling, iden- both adaptability and computational performance in real-
tifying parameters in thermo-hydro-mechanical processes, timeapplications.Incar-followingmodels,PINNsleverage
andapplyingthesecapabilitiestoclassicconsolidationand existing physics-based models to enhance prediction accu-
injection-productionproblems[275]. racy,outperformingtraditionaldata-drivenmethods,partic-
Overall,PINNsrepresentatransformativeapproachinthe ularly in sparse data scenarios [286]. Lastly, in risk-aware
study of porous media transport, offering a powerful tool autonomous driving, PINNs model complex wheel-ground
for simulating and understanding the complex interactions interactions and utilize latent features to develop advanced
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 23 of 43 15
controlframeworks,improvingperformanceundervariable used to model plasma dynamics in magnetic confinement
conditions[287]. fusion devices, revealing electric potentials and fields from
These applications highlight the versatility of PINNs in sparseelectrondatabysolvingthedrift-reducedBraginskii
adapting to and solving multifaceted problems in dynam- equations[295].Anotherapplicationinvolvesreconstructing
ical systems, control, and autonomy. They showcase their 3D structures from 2D diffraction patterns, demonstrating
potentialtotransformtraditionalapproacheswithenhanced real-time capabilities that outperform traditional numeri-
predictiveandcontrolcapabilitiesacrossvariousengineering cal methods [296]. In magnetostatics and micromagnetics,
andtechnologicaldomains. PINNssolvebothforwardandinverseproblems,enhancing
ourunderstandingandcontrolovermagneticmaterials[297].
4.5 Applicationsinheattransfer PINNshavealsobeenemployedinthestudyofelectrochem-
istry for predicting voltammetry across various configura-
PINNs are proving to be transformative in handling heat tions,solvingbothforwardandinverseproblemsincycling
transfer problems across diverse applications, demonstrat- voltammetry[298].
ing their effectiveness inboth simulation and optimization. Furthermore, PINNs are adept at solving the time-
NVIDIA’s SimNet framework exemplifies this by solving dependent Schrödinger equation, providing insights into
variousmultiphysicsproblems,suchasoptimizingheatsink quantumdynamics[299].Theyarealsoutilizedinsolvingthe
designsforelectroniccomponentsandmodelingbloodflow nonlinearSchrödingerequation,accuratelypredictingrogue
dynamics in medical applications [288]. In traditional heat waves, and parameter discovery [300]. One notable study
transfer contexts, PINNs solve forced and mixed convec- employedanimprovedPINNmethodtotacklethederivative
tion problems, even when thermal boundary conditions are nonlinear Schrödinger equation, showcasing the versatility
unknown, which is crucial for real-world applications like ofPINNsinobtainingdetailedwavesolutions[301].Lastly,
electronicchipcoolingandheatsinkefficiency[9]. PINNsareusedinmultiscalemode-resolvedphonontrans-
Inmetaladditivemanufacturing,PINNsareutilizedtopre- port,optimizingthermalmanagementinmicroelectronicsby
dictthetemperatureandmeltpooldynamics,enhancingthe solvingthephononBoltzmanntransportequationefficiently
understandingandcontrolofmanufacturingprocessesunder andaccurately[302].
limited data conditions [289].Moreover, in advanced man- PINNs enable the reconstruction of electric permittivity
ufacturing scenarios involving convective heating, PINNs distributions from synthetic scattering data in nano-optics
offer solutions that integrate convection boundary condi- and metamaterials, effectively addressing challenges such
tions,outperformingconventionalfiniteelementmethodsin as cloaking in nanocylinders [304]. In fiber optics, PINNs
bothspeedandadaptability[290].Additionally,PINNsare successfullymodelnonlineardynamicsgovernedbythenon-
showntobeeffectiveinmodelingmicroscaleheatconduc- linearSchrödingerequation,enhancingcapabilitiesinoptical
tionindouble-layeredthinfilmsexposedtoultrashort-pulsed fiber communications through precise modeling of disper-
lasers[291,292],extensivelyusedinthermalprocessingof sion and nonlinear effects [305]. Additionally, PINNs are
materials,structuralmonitoringofthinmetalfilmsandlaser usedtopredictdynamicprocessesandparametersforvector
processinginthin-filmdeposition. opticalsolitonsinbirefringentfibers,showcasingtheirabil-
PINNsalsoaddressthethermochemicalcuringprocesses itytoperforminverseestimationsofdispersioncoefficients
incomposite-toolsystems,modelingtheintricatedynamics and nonlinearity coefficients with resilience to noise [306].
oftemperatureandchemicaltransformationsduringmanu- Inthecontextoffiber-opticcommunicationsystems,PINNs
facturing, which are critical for optimizing product quality improvedigitalbackpropagation byincorporatingtrainable
and material properties [293]. These applications highlight filters,reducingcomputationalcomplexitywhileenhancing
theextensivepotentialofPINNstorevolutionizeheattrans- performance,thusaligningwellwithpracticaldigitalsignal
fermodeling,providingrobust,efficient,andhighlyaccurate processingapplications[307].Theseexampleshighlightthe
solutions that integrate seamlessly with engineering work- transformative impact of PINNs in advancing fundamental
flowsandleadtoimproveddesignsandprocessesinavariety researchinphysics,providinginnovativesolutionsthatinte-
ofindustrialcontexts. gratephysicallawswithmachinelearningtechniques.
In the study of Earth’s radiation belts, PINNs have been
4.6 Applicationsinphysics adeptly used to solve the inverse problem associated with
theFokker-Planckequation,usingdatafromtheVanAllen
PINNsarefacilitatingadvancementsinfundamentalphysics. Probes to enhance our understanding of electron transport
Inaerodynamics-thermodynamics,PINNshandlehyperbolic mechanisms[308].Additionally,PINNsplayacriticalrole
systems with shocks better through a new space-time con- in optimizing planar orbit transfers by learning optimal
trol volume scheme, addressing traditional challenges in control actions, adhering to the conditions set by the Pon-
shock-relatedproblems[294].PINNshavebeeneffectively tryaginminimumprinciple,thusofferingapromisingavenue
123

15 Page 24 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
forspacenavigation[309].Furtherapplicationsincludethe construction,anddesignoptimization.Zhuetal.[317]review
development of closed-loop optimal guidance and control the current use of machine learning in chemical engineer-
policies in aerospace systems, where PINNs integrate with ing and categorize PINNs as domain knowledge-informed
the Hamilton-Jacobi-Bellman equation and the theory of machinelearningmodels,emphasizingtheiruniquecapabil-
functional connections to tackle complex control problems ity to integrate prior knowledge of physics, mathematical
inNewtonianmechanics[310].Similarly,PINNshavebeen laws, chemical mechanisms, and boundary conditions as
used alongside the Extreme Theory of Functional Connec- constraints. Since previous sections have covered PINNs
tions(X-TFC)tosolveconstrainedoptimalcontrolproblems, in transport and heat transfer, this section focuses on their
provingeffectiveinscenariosliketheconstrainedminimum applicationsinmasstransfer,chemicalreactionsandreactor
time-energyoptimalHalo-Haloorbittransferandfuelopti- design,separationandunitoperations,andsurrogatemodel
mallandingproblems[311].Furthermore,PINNshavebeen developmentwithinchemicalengineering.
usedtopredictthetrajectoryofuntrackedspacedebrisafter Mass transfer is central to many separation and reac-
inelasticcollisionwithasatellite[303]. tion processes. Chen et al. [298] applied PINNs to model
Reinforcementlearningapplicationsinspacemissionsare 1Dand2Dcyclicvoltammetryinelectrochemicalsystems,
enhanced by PINN-based gravity models, which simulate incorporating mass diffusion equations and electrochem-
environmentaldynamicsmorerapidlythantraditionalmeth- ically consistent boundary conditions. Batuwatta-Gamage
ods,aidinginthedevelopmentofsaferspacecraftbehaviors etal.[318]proposedphysics-informedneuralnetworksfor
aroundirregularlyshapedbodiesandfacilitatingthediscov- masstransfer(PINN-MT)toeffectivelypredictcellular-level
ery of periodic orbits [312]. This approach is extended in mass loss and subsequent moisture variations during low-
gravity field modeling, where PINNs tackle challenges in temperaturedrying.Additionally,Xuanetal.[319]combined
modelinggravityfieldsofsmallcelestialbodies,significantly physics-informed learning with an optimization method to
improvingrobustnesstonoiseandmodelingaccuracy[313]. predictmassflowrate,pressure,andvelocityinrefrigerant
Thediscoveryofperiodicorbitsisfurtheroptimizedthrough filling,further demonstrating the effectiveness of PINNs in
PINNs,whichreducesearchtimesdramaticallybyintegrat- masstransfermodeling.
ing with orbital element space computations, a shift from PINNs have been used to address various challenges in
conventional Cartesian space methods [314]. Lastly, in the chemical reactions and reactor design, focusing on sev-
fieldofradiativetransfer,PINNsareemployedtosolveboth eralkeyaspects.Oneimportantapplicationishandlingstiff
forward and inverse problems, enabling the estimation of chemical kinetics, as demonstrated by Ji et al. [320], De et
absorptioncoefficientsandradiativeintensitywithenhanced al. [321], and Weng et al. [322]. Additionally, PINNs are
accuracy, also providing insights into the generalization appliedtoidentifymissingorunknownkineticinformation
error associated with such models [315]. These applica- in complex reaction models. For instance, Ngo et al. [323]
tions demonstrate the transformative potential of PINNs used inverse PINN methods to determine the effectiveness
inastronomyandaerospaceengineering,providingsophis- factor in a nonlinear reaction rate model for catalytic CO
2
ticated tools for navigating, modeling, and understanding methanationinanisothermalfixed-bedreactor,whileCohen
spacephenomenaandengineeringchallenges. et al. [324] applied symbolic regression with PINNs to
derivekineticmodelsindynamicplugflowreactors.Bibeau
4.7 Applicationsinchemicalengineering et al. [325] also employed PINNs to predict the kinetics
of biodiesel production in microwave reactors. Moreover,
Chemical engineering applications involve a broad range PINNshavealsobeenappliedtomodelcomplexconvection-
of subjects, including transport phenomena, heat transfer, diffusion-reaction systems. Hou et al. [326] used PINNs
optimalcontrol,speciesseparation,unitoperations,thermo- to solve a variety of cases, such as gas-solid adsorption,
dynamics,andreactionkinetics.Theunderstandingofthese forward-reactingflowsunderdifferentPécletnumbers,and
areas is grounded in the fundamental conservation laws of inverse problems with missing chemical information. Sun
momentum, energy, and mass, as well as reaction kinet- et al. [327] introduced PINNs to solve two-dimensional
ics, such as the Arrhenius equation and rate laws, which convection-diffusion-reactionequationsfornonlinearreact-
quantifyreactantconsumptionandproductformationrates. ingflows.PINNshavebeenappliedtoawiderangeofreactor
The most precise representation of these conservation laws typesandapplications.Forcontinuousflowreactors,suchas
and reaction kinetics is achieved through PDEs. As multi- plugflowreactors(PFRs)andcontinuousstirred-tankreac-
plestudiesdemonstratedthesuccessofPINNsinmodeling tors (CSTRs), Choi et al. [328] assessed the feasibility of
multiphysicssystems,PINNshavebecomevaluabletoolsin usingPINNstomodelaCSTRwithavandeVussereaction,
dealingwithchemicalengineeringproblems.Wuetal.[316] whilePateletal.[329]utilizedPINNstooptimizetempera-
provideacomprehensiveoverviewofPINNs’applicationsin turetrajectoriesinPFRs.Ngoetal.[330]developedforward
chemicalengineering,includingprocessmodeling,surrogate PINNs based on the one-dimensional design equations for
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 25 of 43 15
PFRs. Furthermore, PINNs have been applied to nuclear PINNs are crucial for sectors ranging from pharmaceu-
reactordesign,asdemonstratedbyElhareefetal.[331]and ticals to nanotechnology. The power systems sector also
Schiassietal.[332]. benefitsfromPINNs,whichfacilitatethemodelingofcom-
Modeling multiphysics problems in chemical engineer- plex grid dynamics, allowing for faster and more accurate
ing using PDEs often leads to high degrees of nonlinearity prediction of states such as rotor angles and system fre-
and nonconvexity, which increases the complexity of the quencies[343].Inrenewableenergy,specificallywindpower
optimizationprocess.Toaddressthis,surrogatemodelsare estimation,PINNsprovideamethodtooptimizeturbinelay-
used to balance model accuracy with computational effi- outandperformanceprediction,contributingsignificantlyto
ciency. Many studies have made initial attempts to apply theefficiencyofwindfarms[344].Environmentalengineer-
PINNstoconstructsurrogatesofcomplexsystemsinchem- ing applications, particularly in managing natural disasters
ical engineering. For example, Liu et al. [333] proposed a suchaswildfires,benefitfromPINNsthroughenhanceddata
multi-fidelity surrogate modeling method based on PINNs, assimilation and modeling capabilities, which improve the
combining high-fidelity simulation data with low-fidelity accuracy of predictions and the effectiveness of response
governing equations described by differential equations. strategies[345].PINNsalsoaddresschallengesinphysical
This approach was applied to simulate the startup phase of domains with irregular geometries, solving complex PDEs
a CSTR, demonstrating strong extrapolation performance. infieldsasvariedasheattransfer,fluiddynamics,andelec-
Antonelloetal.[334]presentedtheuseofPINNsassurrogate tromagnetism,whicharecrucialforadvancing engineering
modelsforaccidentalscenariossimulationinNuclearPower solutions[346].
Plants (NPPs). Liu et al. [335] developed a field-resolving Furthermore,theabilityofPINNstomodeldiscontinuities
surrogate modeling framework using PINNs for a parame- andhigh-gradientphenomenaalsoopensnewpossibilitiesin
terizedtwo-dimensionalmethane-airjetcombustionsystem. aerospaceengineering,seismology,andmeteorology,where
PINNshavealsobeenusedinspeciesseparationandunit accurate modeling of such phenomena is essential [347].
operations. For example, they have been applied to model Additionally,cusp-capturingPINNs[348]introduceacusp-
chromatography columns [336–338]. Li et al. [339] exam- enforcedlevelsetfunctiontosolvediscontinuous-coefficient
inedthepredictivecapabilitiesandgeneralizabilityofPINNs ellipticinterfaceproblemswhosesolutioniscontinuousbut
inmodelingunitoperationprocesses(UOPs)forurbanwater hasdiscontinuousfirstderivativesontheinterface.
treatment, including continuous stirred-tank reactors, acti- PINNsalsocontributetotheunderstandingandprediction
vated sludge reactors, and fixed-bed granular adsorption ofbehaviorsinsystemsgovernedbynonlineardiffusivityand
reactors. Biot’sequations,impactingfieldssuchasgeotechnicalengi-
neering,biomedicalapplications,andenergysystems[349].
4.8 Miscellaneousapplications
Inadditiontotheapplicationsmentionedabove,PINNshave 5 Uncertaintyquantification
alsobeenutilizedindiversefieldssuchasfinance,topology
optimization,porousmediaandenvironmentalengineering, Uncertaintyquantification(UQ)isessentialforthereliable
amongothers.ThefinanceindustryutilizesimprovedPINNs andtrustworthydeploymentofPINNsinsolvingdifferential
for more stable and accurate modeling of complex finan- equations for forward and inverse problems. Convention-
cialinstrumentslikeoptionsundertheBlack-Scholesmodel, ally, in machine learning and data science, uncertainty is
showcasingthepotentialofthesenetworkstorevolutionize categorized into aleatoric uncertainty and epistemic uncer-
financialanalyticsandriskmanagement[340].Inthedomain tainty[350,351].Aleatoricuncertainty(ordatauncertainty)
of optimization and design, PINNs facilitate the design of arisesfrominherentvariabilityinthedataitself.Thistypeof
electromagnetic metamaterials by solving Maxwell’s equa- uncertaintyisduetorandomnoiseorvariabilityinthedata
tions and determining material properties like permeability distribution and is considered irreducible because it is not
and permittivity and are therefore crucial for the design of related to any lack of knowledge or flaws in the model but
devices such as cylindrical cloaks and rotators [341]. They insteadisanintrinsicpropertyofthedata.Epistemicuncer-
alsofacilitatetopologyoptimizationinholographyandfluid tainty(orknowledge/modeluncertainty)isduetoalackof
dynamics, where hard constraints are effectively managed knowledgeabouttheunderlyingprocessormodel.
through advanced methodologies like the penalty and aug- This uncertainty occurs when the model lacks sufficient
mentedLagrangianmethods[54]. data or knowledge to make accurate predictions. Aleatoric
In molecular simulations, PINNs enable the prediction uncertaintycanonlybereducedbyenhancing dataquality,
ofmaterialpropertiesfrommoleculardynamicssimulations whereasepistemicuncertaintycanbereducedbygathering
and, therefore, provide insights into nanoscale phenom- moredata,refiningthemodel,orimprovingdataquality[350,
ena[342].Theinsightsintomaterialbehaviorgainedthrough 351].
123

15 Page 26 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
5.1 Noisyand/orgappydata tiallydiffersfromtheepistemicuncertaintystemmingfrom
imposing a noisy model. The former is caused by the ran-
One common yet crucial source of uncertainty in solving domness of the data and is irreducible even if more data
differential equations is noisy data, which refers to uncer- are available, while the latter can be decreased given more
taintyovertheexactvalueofthesoughtsolution,themodel availabledata.Itwasshownin[351,353,363]thatthetotal
parameter, the source term, and/or the boundary term of uncertainty could be decomposed into separable aleatoric
the PDE. For example, in solving a forward problem, the uncertaintyandepistemicuncertaintieswhenthenoisemodel
source term f in Eq. 1 can only be resolved by noisy mea- isadditiveandknownbyadoptingtheBayesianframework.
surements/observations at some discrete points rather than Figure 14(c) shows an illustrative example regarding total
beingpreciselyknown.Anotherimportantsourceofuncer- uncertainty.
taintyisgappydata,whichreferstoincompleteinformation Although the PINNs method can solve complex sys-
of aforementioned quantities, e.g., data of the source term temswithsufficientdata,itoftenstruggleswithsparsedata.
are not available for a subdomain when solving a forward In[354],theauthorsshowedthatthisissuecouldberesolved
problemordataofthesolutionarenotsufficientenoughto byleveraginganinformative,functionalpriormodeltrained
makeconfidentprediction/inferenceoverthePDEparameter beforehand from historical or simulated data using genera-
in an inverse problem. Figure 14(b) displays an illustrative tiveadversarialnetworks.Whenanewtaskisconsidered,this
exampleregardingthenoisyandgappydata. functionalpriormodelisemployedtosolvethePDEproblem
Tackling noisy and/or gappy data and quantifying asso- withUQ,givenverylittlenoisydata.Anexampleispresented
ciated uncertainty is often challenging in conventional inFig.14(d)forillustration.Similarly,in[367],theauthors
numerical methods. Many PINN-based methods have been employed the multi-head architecture and the normalizing
proposedtoaddresssuchproblems.Onenotablemethodis flow [368] to learn a functional prior model to tackle the
theBayesianPINNs(B-PINNs),introducedin[352],which challenges of physics-informed learning with PINNs when
addressesforwardandinversePDEproblemsbasedonnoisy dataaresparse.Thefunctionalpriormodelhasproventobe
andgappydatawhilequantifyingtheassociateduncertainty veryeffective,particularlywhendataaresparse,andextrap-
through a Bayesian framework, estimating the correspond- olationisneeded[351,353,369,370].
ing posterior distributions. We note that the uncertainty While numerous UQ methods have been proposed to
quantified in [352] is epistemic, which can be interpreted addressnoisydatainsolvingPDEsinPINNs,mostofthem
as the uncertainty arising from gappy data and the noise assumethattheinputofdata,i.e.,thespatial-temporalcoor-
modelinobservingthedata.BesidesB-PINNs,theDropout dinatex inEq.1,iscertainandthereforefailtoconsiderthe
method,whichhasbeenshowntoeffectivelycapturetheepis- uncertainty caused by the noisy inputs. Recently, in [371],
temicuncertaintyofneuralnetworks[356],wasincorporated the authors investigated the impact of noisy inputs in solv-
into PINNs for solving differential equations [357]. In [22, ing forward and inverse PDE problems and employed a
358, 359], generative adversarial networks were employed Bayesianapproachtoquantifytheuncertaintyarisingfrom
to quantify uncertainty stemming from uncertain data in noisyinputs-outputsinPINNs.Specifically,theyconsidered
solving PDE problems. In [351, 353, 360, 361], the deep twoindependentnoisemodels,onefortheinputandonefor
ensemble PINNs method was developed as a practical UQ theoutput,andestablishedlikelihooddistributionsforboth
method to handle noisy and/or gappy data in both forward intheBayesianframework.
andinverseproblems.Incontrast,in[362,363],adataper-
turbationtechniquewasusedtoimprovetheperformanceof 5.2 Physicalmodeluncertainty
deep-ensemble-basedUQmethodsfurther.Amulti-variance
replicaexchangemethodwasintroducedin[364]toenhance Physicalmodeluncertaintyisonesignificantsourceofuncer-
the performance of B-PINNs in tackling the challenges tainty,oftenoverlookedinconventionalnumericalmethods
posed by multimodal posterior distributions. In [365], the and refers to a lack of knowledge over the precise form of
polynomialchaosexpansionwasintegratedintothePINNs specifictermsinPDE,e.g.,thelocalproductionmodelofthe
frameworkforpropagationofparameteruncertainty.Acon- reaction-diffusionsystemusedtodescribethespatiotemporal
tinuallearningperspectiveofsolvingPDEswithUQunder propagation of misfolded tau protein [372] and the resis-
thePINNframeworkwasdiscussedin[366].In[351],arange tancemodelinthepulmonarycompartmentoftheCVSim-6
of modern UQ methods for neural networks, such as snap- cardiovascularODEsystem[363].Ignoringthisuncertainty
shotensembleandstochasticweightaverageGaussian,were results in physical model misspecifications, leading to sig-
alsointegratedintothePINNsframeworkforUQ. nificant discrepancies between data and physics, as well as
Anotherimportantsourceofuncertaintywhenconsider- inaccurate predictions in both forward and inverse prob-
ing noisy data in PINNs is data (aleatoric) uncertainty. We lems[355,373–376].AnexampleofwhenPINNsencounter
notethatinthenoisydataregime,thedatauncertaintyessen- modelmisspecification,whereaNewtonianflowisassumed,
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 27 of 43 15
Fig.14 (a)Abreakdownofcommonsourcesofuncertaintyinsolving inginformativefunctionalpriorinsolvingPDEswithnoisyandgappy
differentialequationswithPINNs(adaptedfrom[351]).(b)Anexample data(adaptedfrom[354]).(e)Anexampleofphysicalmodeluncer-
ofnoisyandgappydatainfunctionapproximation(adaptedfrom[352]). taintyinPINNsisassumingaNewtonianflowwhilethedatacomes
(c)Anillustrationofdecomposingtotaluncertaintyintoaleatoricand fromanon-Newtonianflow(adaptedfrom[355])
epistemicuncertaintiesinsolvingPDEs(adaptedfrom[353]).(d)Utiliz-
but the underlying physics that generates the data is non- betweenphysicsanddata,whichiscausedbythemodelmis-
Newtonian,isillustratedinFig.14(e). specification, is corrected by adding this additional neural
In[355],theissueofphysicalmodelmisspecificationsin network,and(2)bysuccessfultraining,thevalueofthisneu-
PINNswasdiscussed.Theauthorsproposedtouseanother ralnetworkrepresentsthediscrepancywhileitsuncertainty
neural network to model the discrepancy in the differential representsthemodeluncertainty.Similarlytogappydata,this
equation,whichleadstotwobenefits:(1)thedisagreement uncertaintycouldbecategorizedasepistemicuncertainty.
123

15 Page 28 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
5.3 Someapplications ity of the representation model to capture the true solution
|uˆ −u ∗|.
Recently developed UQ methods for PINNs have been uti- Severalstudieshaveaddressedconvergenceanderroresti-
lizedtotacklemanyreal-worldproblems.Forexample,[365] mates in PIML [51, 321, 380–384], and a comprehensive
employedPINNsforuncertaintypropagationofparameters reviewofthesestudiescanbefoundin[4].Shinetal.[380]
in ocean modeling; the PINNs [238] and B-PINNs [377] pioneeredthisfieldbyprovidingconvergenceestimatesfor
methodswereusedforUQinepidemiologyproblemsgiven linearsecond-orderellipticandparabolicPDEs.Subsequent
real-worldCOVID-19data;[378]appliedPINNstoestimate studies [385] extended these results to all linear problems,
bloodalcoholconcentrationwithquantifieduncertainty;traf- including hyperbolic equations. Zeinhofer et al. [51] pro-
ficstateestimationwithUQisaccomplishedbyleveraging videdsharpgeneralizationerrorestimatesforlinearelliptic,
the PINN framework, generative adversarial networks and parabolic,andhyperbolicPDEs,showingthattheL2penalty
normalizingflowsin[379]. approach for initial and boundary conditions weakens the
errordecayrate.Ontheotherhand,[315]estimatedgener-
alization error in terms of the training error and number of
6 TheoreticaladvancesinPIML trainingpoints,whichwasfurtherextendedtoinverseprob-
lems in [386]. Another line of work focuses on variational
6.1 ErrorestimatesandconvergenceinPIML
formulationsofellipticPDEs[113,387].
ThegoalofPIMListofindarepresentation modelu ∗ that OtherstudieshavefocusedonspecifictypesofPDEs.For
approximatesthesolutiontoaPDE/ODE,uˆ,byminimizing example,[132]providedrigorouserrorboundsfortheincom-
alossfunction(Eq.13)thataccountsfortheresidualsfrom pressible Navier-Stokes equations using X-PINNs [130],
the governing equations, boundary conditions, and data in showingthattheunderlyingPDEresidualcanbemadearbi-
thecontinuousdomain.AsdescribedinSection3.3.2,dueto trarily small with tanh neural networks. Similarly, [388]
computational constraints,Eq.13 isestimated inadiscrete proposedanexpliciterrorestimateandstabilityanalysisfor
form(Eq.14),withaminimizeru ∗ .However,asdiscussed the incompressible Navier-Stokes equations. On the other
d
in [380], this function is minimized using a gradient-based hand,[321]focusedonKolmogorov-typeequations,deriving
optimization method which, due to the high non-convexity
boundsontheexpectationoftheL2errorundertheassump-
ofL,doesnotfullyrecoveru ∗ ,leadingtoasuboptimalsolu- tion that the weights of the neural network are bounded.
d
tionu.Undertheseassumptions,andasproposedby[380], Similarly,[315]analyzedtheradiativetransferequationand
thetotalerrorinaPIMLmodel(seeFig.15)canbedecom- provedthatthegeneralizationerrorisboundedbythetraining
posed into three parts: (1) an optimization error resulting error,providinganestimatethatdependsonlyonthenumber
fromtheoptimizer’sinabilitytofullyminimizethelossfunc- oftrainingpoints.
tion |u −u ∗|; (2) an estimation or quadrature error due to Finally,[389]providedacomprehensivetheoreticalanal-
d
thediscretizationofthelossfunction|u ∗−u ∗|;and(3)an ysisofthemathematicalfoundationsdrivingPIMLinboth
d
approximationerror,whichreflectstheexpressivityorcapac- thehybridmodelingandPDEsolversettings,showingthat
Fig.15 Decompositionoftotalerror.ThetotalerrorinaPIMLmodel approximationerror,whichreflectstheexpressivityorcapacityofthe
can be decomposed into three parts [380]: (1) an optimization error representationmodeltocapturethetruesolution|uˆ−u∗|.Hereu∗isthe
resultingfromtheoptimizer’sinabilitytofullyminimizethelossfunc- minimizerofthelosswithfiniteamountofdata,andu∗isthemin d imizer
tion|u−u∗|;(2)anestimationorquadratureerrorduetodiscretizing ofthelosswithinfinitelymanydata
thelossfun d ctionoverafinitenumberofpoints|u∗−u∗|;and(3)an
d
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 29 of 43 15
anadditionallevelofregularizationissufficienttoguarantee embeddings [30], weight factorization [33], adaptive resid-
strongconvergence. ualconnections[31],globalweights[391],causality[55]and
localweights[171].
6.2Trainingdynamics
6.2.1 NeuraltangentkernelperspectiveinPINNs
|     |     |     |     |     |     |     |     | 6.2.2 Informationbottlenecktheory |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- |
TheNeuralTangentKernel(NTK)offersatheoreticalframe-
TheInformationBottleneck(IB)theoryprovidesaninforma-
worktounderstandthetrainingdynamicsoffullyconnected
tion-theoreticperspectiveonthetrainingandperformanceof
neuralnetworks,particularlyintheinfinite-widthlimit.Jacot
neuralnetworks.Itpresentsaframeworkforformingacon-
| et al. [390] | introduced |     | the | NTK theory, |     | which | provides |     |     |     |     |     |     |     |
| ------------ | ---------- | --- | --- | ----------- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
T,
|     |     |     |     |     |     |     |     | densed representation |     | of  | layer activations, |     | with | respect |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | ------------------ | --- | ---- | ------- |
insightsintohownetworkparametersevolveduringtraining
|            |      |           |             |     |            |     |         | to an input | variable | x ∈       | X, retaining | as  | much information |         |
| ---------- | ---- | --------- | ----------- | --- | ---------- | --- | ------- | ----------- | -------- | --------- | ------------ | --- | ---------------- | ------- |
| by linking | them | to kernel | regression. |     | For PINNs, |     | the NTK |             |          |           |              |     |                  |         |
|            |      |           |             |     |            |     |         |             |          |           |              | y ∈ | Y                |         |
|            |      |           |             |     |            |     |         | as possible | about    | an output | variable     |     | [392,            | 393]. A |
describesthebehaviorofboththedata-drivenandphysics-
|                  |     |     |          |           |      |     |           | keyconceptinthistheoryisthemutualinformation |     |     |     |     |     | I(x,y), |
| ---------------- | --- | --- | -------- | --------- | ---- | --- | --------- | -------------------------------------------- | --- | --- | --- | --- | --- | ------- |
| based components |     | of  | the loss | function. | Wang | et  | al. [391] |                                              |     |     |     |     |     |         |
whichsuggeststhatoptimalmodelrepresentationspreserve
| derived        | the NTK  | of PINNs |           | and demonstrated |                 | that,  | in the |              |                    |     |           |          |                  |     |
| -------------- | -------- | -------- | --------- | ---------------- | --------------- | ------ | ------ | ------------ | ------------------ | --- | --------- | -------- | ---------------- | --- |
|                |          |          |           |                  |                 |        |        | all relevant | information        |     | about the | output   | while discarding |     |
| infinite-width | limit,   | it       | converges | to               | a deterministic |        | kernel |              |                    |     |           |          |                  |     |
|                |          |          |           |                  |                 |        |        | irrelevant   | input information, |     | thus      | creating | an “information  |     |
| that remains   | constant |          | during    | training.        | This            | kernel | allows |              |                    |     |           |          |                  |     |
bottleneck”.IBtheoryidentifiestwodistinctphasesoflearn-
forananalysisofthetrainingprocessintermsofeigenval-
|                  |              |            |        |             |             |       |         | ing: fitting    | and diffusion,      |          | separated | by     | a phase transition |         |
| ---------------- | ------------ | ---------- | ------ | ----------- | ----------- | ----- | ------- | --------------- | ------------------- | -------- | --------- | ------ | ------------------ | ------- |
| ues, revealing   |              | that PINNs | suffer | from        | spectral    | bias, | where   |                 |                     |          |           |        |                    |         |
|                  |              |            |        |             |             |       |         | driven by       | the signal-to-noise |          | ratio     | (SNR)  | of the             | gradi-  |
| higher frequency |              | components |        | of the      | solution    | are   | learned |                 |                     |          |           |        |                    |         |
|                  |              |            |        |             |             |       |         | ents [394–396]. | Anagnostopoulos     |          |           | et al. | [57] extended      | this    |
| more slowly.     | Furthermore, |            | a      | significant | discrepancy |       | in the  |                 |                     |          |           |        |                    |         |
|                  |              |            |        |             |             |       |         | framework       | to study            | learning | dynamics  |        | in PINNs,          | propos- |
convergenceratesofthedifferentlosscomponents-1)PDE
ingtheexistenceofathirdphasecalledtotaldiffusion(see
residuallossand2)dataloss,canleadtostifftrainingdynam-
Fig.16(a)).Subsequentstudies[16]demonstratedthatthese
| ics and poor | accuracy. |     | To mitigate | this, | [391] | proposed | an  |     |     |     |     |     |     |     |
| ------------ | --------- | --- | ----------- | ----- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
threephasesarealsoobservableinotherrepresentationmod-
| adaptive | trainingalgorithmthatusestheeigenvalues |     |     |     |     |     | ofthe |     |     |     |     |     |     |     |
| -------- | --------------------------------------- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
els,suchasKANs.
NTKtobalancethecontributionsoftheselosscomponents.
The NTK framework has been extended and used as a Signal-to-NoiseRatio(SNR)
theoretical framework to develop and justify several algo- As described in [16, 57, 395, 396], the batch-wise signal-
rithmic enhancements of PIML, such as Fourier feature to-noise ratio (SNR) is a key metric for understanding the
Fig.16 StagesofLearning.(a)Thestagesoflearningcanbeidentified andresidualdistributionsatdifferentstagesoflearninginforHelmholtz
usingthesignal-to-noiseratio(SNR)ofthegradients.Highlydetermin- equation[16].Thefittingphaseishighlydeterministic,sotheresiduals
isticregimesarecharacterizedbyahighSNR,whilehighlystochastic displayanorderedpattern.AstheSNRdecreasesandthemodeltran-
regimes are characterized by a low SNR [57]. During fitting, PIML sitionstoastochasticstage,diffusion,theresidualsgraduallybecome
model’sSNRgofromhightolow.Thissuggestsaninitialphasewhere disordered.Finally,intotaldiffusion,themodelreachesanequilibrium
themodelcloselyfitsthetrainingdata.Thediffusionphaseisconsid- state,simplifiesinternalrepresentations,andreducestheircomplexity,
eredanexploratorystagecharacterizedbyafluctuatinglowSNR.In makingitmuchmoreefficientandgeneralizable.Noticethatduringthis
the last stage, total diffusion, the SNR suddenly increases and con- stage,thepredictionscloselymatchtheanalyticalsolution.Thisphase
vergestoacriticalvalue,andthegeneralization(i.e.,relativeL2)error ischaracterizedbyhighlystochastic(i.e.,noisy)residuals[57]
decreasesfaster,suggestinganoptimalconvergence[57].(b)Prediction
123

15 Page 30 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
trainingdynamicsofneuralnetworks.Itisdefinedas: deredresiduals.However,asobservedin[16,57],oncethe
optimal direction (i.e., signal) is found and total diffusion
SNR= (cid:6)μ(cid:6) 2 = (cid:6)E[∇ θ L B ](cid:6) 2 , begins, the generalization error (i.e., relative L2) decreases
(cid:6)σ(cid:6) 2 (cid:6)std[∇ θ L B ](cid:6) 2 rapidly,indicatingoptimalconvergence.Unsurprisingly,the
best-performingmodelstransitiontototaldiffusionfirst[16,
where θ represents the network parameters, and (cid:6)μ(cid:6) and 57].
2
(cid:6)σ(cid:6) aretheL2-normsofthebatch-wisemeanandstandard
2
deviationofthegradientsofthetotalloss∇ θ L B.According One of the main advantages of this approach is that it
to[16],the“signal”referstoanidealizedgradientthatdrives providesameasureofconvergencethatcanbeusedtoeval-
theoptimizertoreduceerrorsacrossallsubdomains,while uateamodel’sperformance.Previousstudies[16,57]have
“noise”representsperturbationsfromthisidealgradientdue shown that the best-performing models typically reach the
tothefinitenumberofobservations. totaldiffusionphaseearlierthanothers.Conversely,models
that fail to converge often remain trapped in the diffusion
StagesofLearning
stage,unabletoprogressfurther.Additionally,thistheoret-
Thestagesoflearningcanbeviewedasaprocesswherethe
ical framework reflects the underlying training dynamics,
modelinitiallyfitsthedata(capturingrelevantinformation)
which could potentially be leveraged to develop new algo-
and then compresses it (discarding irrelevant information),
rithmsorarchitecturesthatoptimizelearningefficiencyand
thereby enhancing generalization capabilities [57]. Each
enhancemodelgeneralization.
phaseisdefinedbythedominanttermintheSNR.Determin-
isticregimesexhibithighSNR,characterizedbyadominant
signal,whilestochasticstagesaremarkedbylowSNR,where 7 Computationalframeworksandsoftware
noisedominates(seeFig.16(a)).
AsthePINNsmethodemergesasarevolutionaryapproachto
Fitting
solvingPDEproblems,manysoftwarepackageshavebeen
At the start of training, both the loss and its gradients are
developed for fast and reliable implementations of PINNs
highacrossallsubdomains.Thisagreementresultsinanini-
basedondifferentcomputationalframeworks.Mostofthese
tially high SNR, where a clear signal (i.e., direction) helps
weredevelopedinPythontoleveragemodernmachinelearn-
reducethetrainingerroracrossthesubdomains.However,as
ingcomputingtools,whilesomeareinotherprogramming
thelossandgradientsdecrease,disagreementbetweensub-
languages, e.g., the NeuralPDE.jl [397], and the ADCME
domains (i.e., noise) increases, leading to a decline in the
libraries were developed in Julia. We note that in this sec-
SNR. Therefore, the fitting stage is a deterministic phase,
tion, we provide a brief review of these libraries only for
transitioningfromhightolowSNRastheresidualsdisplay
PINNs,whilesomehavebeendevelopedfurthertoaddress
anorderedpattern[57](seeFig.16(b)).
broaderapplicationsinscientificmachinelearning,suchas
Diffusion neuraloperators,whicharebeyondthescopeofthispaper.
After the model has adequately fitted the data, it enters an A notable library is DeepXDE [172], which was ini-
explorationphase,searchingforasignal(i.e.,direction)that tiallydevelopedbasedontheTensorFlowplatformandnow
reducesthetrainingerroracrossallsubdomains.Duringthis supports multiple backends, including PyTorch, JAX, and
phase, the network weights diffuse, enhancing the model’s PaddlePaddle.TheDeepXDElibraryalsosupportscomplex
generalization capabilities by disrupting the initial order of domain geometries, various boundary conditions, different
parameters.Thediffusionstageischaracterizedbyafluctu- automatic differentiation methods, and many more in solv-
ating, low SNR [57]. In this stochastic stage, the residuals ing differential equations using PINNs. On the other hand,
becomedisordered(seeFig.16(b)),andtheSNRbeginsto NVIDIA’sModulus[398]supportsonlythePyTorch back-
oscillate. end but specializes in scalable training with the power
of NVIDIA GPUs maximized for training PINNs. The
TotalDiffusion NeuroDiffEq [399] and TorchPhysics [400] libraries are
Inthefinalphase,afterthemodelidentifiesanoptimalsig- PyTorch-based: the former provides additional toolsets for
nal, the SNR increases rapidly, reaching equilibrium as the transfer learning and conveniently obtaining solution bun-
modelexploitsaconsistentdirectiontominimizegeneraliza- dle for inverse problems, while the latter features complex
tionerroracrosssubdomains.Duringthisphase,themodel domaingenerations.SciANN[401]isahigh-levelwrapper
simplifies its internal representation by retaining essential based on TensorFlow and Keras. PyDENs [402] (PyTorch-
featuresanddiscardingirrelevantones,effectivelyreducing based)focusesmoreonsolvingparametricfamiliesofPDEs,
its complexity and breaking the order of the residuals. As such as heat and wave equations. NeuralPDE.jl [397] and
shown in Fig. 16(b), this phase is marked by highly disor- ADCME[403]aretwolibrariesinJulia:theformerismore
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 31 of 43 15
comprehensive for PINNs while the latter specializes more importantandwillcontinuetodriveresearchbutitisimpor-
intacklinginverseproblemsandwasdevelopedbasedonthe tant to put it in the right context and also define the proper
JuliaversionofTensorFlow.TheTensorDiffEqlibrary[404] benchmarks.Forexample,forsolvingPDEsin1Dand2D,
is based on the TensorFlow platform and supports multi- FEM performs better both in terms of accuracy and speed
GPU distributed training for large systems. The NeuralUQ but in higher dimensions PINNs will outperform not only
library [353] (Tensorflow-based) specializes in uncertainty FEM but any method. For example, recent work on high-
quantification.Someotherpackagesforsolvingdifferential dimensional PDEs, such as the Hamilton-Jacobi-Bellman
equationswithPINNscanbefoundin[405–407]. and Fokker-Planck equations demonstrated thatproper for-
mulationsofPINNscantackleeven100,000dimensionsat
thecostofonlyanhouronasingleGPU,ataskthatnoother
8 Discussionandoutlook methodcanhandle[19].
A recognized difficulty with PINNs is the inference
Physics-informedmachinelearningandPINNs,inparticular, of dynamical systems that exhibit chaotic and turbulent
have disrupted scientific computing in a fundamental way, responses, especially for long-time integration. This is pri-
enabling a seamless integration of data and physics, unlike marily due to the limited accuracy of the vanilla PINNs in
conventionalnumericalmethodsthatrequireexpensiveand forwardproblemswithnodataavailableduetotheoptimiza-
ofteninaccuratedataassimilationschemes.Thisnewcapa- tion error that dominates the overall error. However, recent
bilityhasbeenappliedindiverseapplications,wellbeyond proposalsformulti-stagedtrainingandstackedarchitectures
theintentionintheoriginalpaper.Despitethenumerouslim- havedemonstratedtheabilityofthesemodifiedversionsof
itationsofthevanillaPINNs,thecomputationalcommunity PINNstoreachaccuracydowntomachineprecision,whichis
has embraced this new capability and attempted to further importantforresolvingchaotictrajectoriesinchaoticdynam-
tailorPINNsandenhanceboththeirefficiencyandaccuracy icalsystems[123,411].
invarioussettings,frommechanicstogeophysicsandeven The question of the high computational cost currently
toquantitativepharmacology. under debate for general neural networks also pertains to
In the Appendix, we provide a table of the evolution of PINNs. The introduction of deep neural operators in 2019,
the algorithmic variants and enhancements so far, which suchasDeepOnet,byourgrouphaspavedthewayforsignif-
addressed the early limitations of PINNs. The first key icantprogressinalleviatingthiscost[412].Moreover,new
development was the introduction of self-adaptive weights representationmodelslikeKANs[62]andPIKANs[16]that
based on adversarial (min-max) training, which is partic- wereviewedhereleadtosmallermodelsandmayalsocon-
ularly important for multiscale problems [408]. Similarly, tributetoloweringthecomputationalcostwhilemaintaining
introducingfeatureexpansionlayerstodealwiththespectral goodaccuracy.Anotherdirectionistofurtheradvancespik-
biasofneuralnetworkswasanessentialdevelopmentintack- ing neural networks [77] that will be working on specially
lingproblemswithhighfrequenciesandwavenumbers[43]. designed neuromorphic chips, like Intel’s Loihi 2, but at
Thedevelopmentofthejaxframeworkhasbeeninstrumen- the moment, the demonstrated accuracy is below the one
tal in computing high-order derivatives fast and accurately, obtainedwithNNsandKANs.Yetanotherpossibleresearch
inadditiontooverallspeedingupPINNcomputations[409]. directionistodevelophybridmethodsthatblendPINNsand
Tothisend,domaindecompositionforconservationlawsbut conventionalnumericalmethodsviadomaindecomposition
alsoforotherPDEshasbeenintroducedtoscaleupPINNsto techniques. For example, PINNs or PIKANs can be used
largespatio-temporaldomainsand,moreover,totakeadvan- only where data is available and interfaced with FEM or
tageofmulti-GPUcomputing[130].Inthissetting,aseparate othermethodsviaproperboundaryconditions.Inadditionto
PINNwithdifferenthyperparameterscanbeassignedineach algorithmicdevelopments,newsoftwareisrequiredtohan-
subdomain,whichalsohelpswithaccuracyenhancementfor dlethetypicallyheterogeneousprogrammingenvironments
multiphysicsproblems.Inadditiontoadaptiveweights,the ofclassicalmethodswithdeeplearningmethods.
introductionofadaptiveactivationfunctionsaffectsboththe In summary, PINNs and PIKANs have significantly
accuracy but also convergence as, under some conditions, advanced in a very short time. They can outperform con-
therearetheoreticalguaranteesofavoidingbadminima[61]. ventional methods for inverse problems, e.g., parameter
A significant advance was the introduction of separable estimationanddiscoveringmissingphysicsingray-boxtype
PINNsandtensornetworksthatdemonstratedaspeed-upof scenarios. Future work should focus on speeding up the
almosttwoordersofmagnitude[410].However,evenwith optimization process, increasing the overall accuracy, and
suchacomputationalspeed-up,thereiscurrentlyadebateif automating hyperparameter tuning so that these methods
PINNs can compete with FEM for forward problems since become robust and competitive with FEM and other clas-
forinverseproblemsPINNsisaclearwinner.Thisquestionis sicalmethods,evenforforward-typesimulationproblems.
123

15 Page 32 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
AppendixAChronologicaloverviewofkey
advancementsinPIML
In Table 1, we present a chronological overview of key
advancementsinPIML.
Table1 Evolutionofthealgorithmicvariants
Publication Contribution Year
PhysicsInformedDeepLearning(PartI):Data-drivensolutionsofnon- PINNframeworkforsolvingPDEs 2017
linearPartialDifferentialEquations[2]
Physics Informed Deep Learning (Part II): Data-driven discovery of PINNframeworkforPDEdiscovery 2017
nonlinearPartialDifferentialEquations[3]
Hidden Fluid Mechanics: A Navier-Stokes informed deep learning Uncovershiddenfields,usesweightnormalization 2018
frameworkforassimilatingflowvisualizationData[413]
fPINNs:FractionalPhysics-InformedNeuralNetworks [23] ExtendsPINNstofractionalPDEs 2018
Quantifyingtotaluncertaintyinphysics-informedneuralnetworksfor IntroducesUQforPINNs 2018
solvingforwardandinversestochasticproblems[357]
Physics-informedneuralnetworks:Adeeplearningframeworkforsolv- JournalpaperformalizingPINNs 2019
ingforwardandinverseproblemsinvolvingnonlinearpartialdifferential
equations[1]
Multi-scale Deep Neural Networks for Solving High-Dimensional Introducesmulti-scalefeatureexpansions 2019
PDEs[43]
VariationalPhysics-InformedNeuralNetworksForSolvingPartialDif- ExtendsPINNsusingvariationalapproaches 2019
ferentialEquations[414]
DeepOnet: Learning nonlinear operators for identifying differential IntroducesDeepONets 2019
equationsbasedontheuniversalapproximationtheoremofoperators
[412]
DeepXDE: A deep learning library for solving differential equations FirstPIMLlibraryandintroductiontoresampling 2019
[172]
On the convergence of physics-informed neural networks for linear ConvergenceanderrorboundsforPINNs 2020
second-orderellipticandparabolictypePDEs[380]
WhenandwhyPINNsfailtotrain:Aneuraltangentkernelperspec- NTKanalysisforPINN 2020
tive[415]
Extendedphysics-informedneuralnetworks(XPINNs):Ageneralized DomaindecompositionforPINNs 2020
space-timedomaindecomposition-baseddeeplearningframeworkfor
nonlinearpartialdifferentialequations[130]
Locallyadaptiveactivationfunctionswithsloperecoveryfordeepand Introducesadaptiveactivationfunctions 2020
physics-informedneuralnetworks[61]
B-PINNs:BayesianPhysics-InformedNeuralNetworksforforwardand BayesianPINNsfornoisydata 2020
inversePDEproblemswithnoisyData[352]
Self-adaptivephysics-informedneuralnetworksusingasoftattention Introduceslocalweightsanattentionmechanisms 2020
mechanism[408]
OntheeigenvectorbiasofFourierfeaturenetworks:Fromregressionto Fourierfeaturesformulti-scalePDEs 2020
solvingmulti-scalePDEswithphysics-informedneuralnetworks[416]
SeparablePhysics-InformedNeuralNetworks[410] Speedsuptrainingupto100times 2023
ArtificialtoSpikingNeuralNetworksConversionforScientificMachine ExtendsPIMLtoSpikingNNs 2023
Learning[77]
Residual-basedattentionandconnectiontoinformationbottleneckthe- Connectiontoinformationbottlenecktheory 2023
oryinPINNs[168]
Stackednetworks improve physics-informed training: applicationsto Stackedtrainingimprovesperformance 2023
neuralnetworksanddeepoperatornetworks[123]
Multi-stageNeuralNetworks:Functionapproximatorofmachinepre- Multi-stagetrainingforbetterperformance 2023
cision[411]
TacklingthecurseofdimensionalitywithPhysics-InformedNeuralNet- SolvesPDEswithupto100,000dimensions 2023
works[19]
KAN:Kolmogorov-Arnoldnetworks[62] ExtensiontoKANs 2024
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 33 of 43 15
Acknowledgements We acknowledge the support of the NIH grant 9. CaiS,MaoZ,WangZ,YinM,KarniadakisGE.Physics-informed
R01AT012312,MURI/AFOSRFA9550-20-1-0358project,theDOE- neural networks (PINNs) for fluid mechanics: A review. Acta
MMICSSEA-CROGSDE-SC0023191award,andtheONRVannevar MechSinica.2021;37(12):1727–1738.
BushFacultyFellowship(N00014-22-1-2795). 10. Huang B, Wang J. Applications of physics-informed neural
|     |     |     |     | networks | in power | systems-a | review. | IEEE | Trans | Power Syst. |
| --- | --- | --- | --- | -------- | -------- | --------- | ------- | ---- | ----- | ----------- |
AuthorContributions J.D.T.Literaturereview,analysis,visualization, 2022;38(1):572–88.
andwriting.V.O.Literaturereview,analysis,visualization,andwrit- 11. LawalZK,YassinH,LaiDTC,CheIdrisA.Physics-informed
ing,A.J.V.Literaturereview,analysis,visualization,andwriting.Z.Z. neuralnetwork(PINN)evolutionandbeyond:Asystematicliter-
Literature review, analysis, visualization, and writing. N.A.D. litera- aturereviewandbibliometricanalysis.BigDataCognitComput.
| turereview,analysis,visualization,andwriting.C.W.literaturereview, |     |     |     | 2022;6(4):140. |     |     |     |     |     |     |
| ------------------------------------------------------------------ | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- |
analysis,visualization,andwritingG.K.Researchsupervision,analy- 12. RaissiM,PerdikarisP,KarniadakisGE.Machinelearningoflin-
sis,writing. ear differential equations using Gaussian processes. J Comput
Phys.2017;348:683–693.
Funding NIH grant R01AT012312, MURI/AFOSR FA9550-20-1- 13. RaissiM,PerdikarisP,KarniadakisGE.Physicsinformedlearn-
0358project,theDOE-MMICSSEA-CROGSDE-SC0023191award, ingmachine.GooglePatents.USPatent.2021;10,963,540.
andtheONRVannevarBushFacultyFellowship(N00014-22-1-2795). 14. DissanayakeMG,Phan-ThienN.Neural-network-basedapproxi-
mationsforsolvingpartialdifferentialequations.CommunNumer
DataAvailability No datasets were generated or analysed during the MethodsEng.1994;10(3):195–201.
currentstudy. 15. LagarisIE,LikasA,FotiadisDI.Artificialneuralnetworksfor
|     |     |     |     | solving | ordinary | and partial | differential | equations. |     | IEEE Trans |
| --- | --- | --- | --- | ------- | -------- | ----------- | ------------ | ---------- | --- | ---------- |
Materialsavailability Notapplicable. NeuralNetw.1998;9(5):987–1000.
|     |     |     |     | 16. Shukla | K, Toscano | JD, | Wang Z, | Zou Z, | Karniadakis | GE. A |
| --- | --- | --- | --- | ---------- | ---------- | --- | ------- | ------ | ----------- | ----- |
Codeavailability Notapplicable. comprehensive and FAIR comparison between MLP and KAN
representationsfordifferentialequationsandoperatornetworks.
| Declarations |     |     |     | ComputMethodsApplMechEng.2024;431,117290. |     |     |     |     |     |     |
| ------------ | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | --- |
17. CaiS,WangZ,FuestF,JeonYJ,GrayC,KarniadakisGE.Flow
overanespressocup:inferring3-Dvelocityandpressurefields
|                    |                                        |     |     | from | tomographic | background | oriented | Schlieren |     | via physics- |
| ------------------ | -------------------------------------- | --- | --- | ---- | ----------- | ---------- | -------- | --------- | --- | ------------ |
| Competinginterests | Theauthorsdeclarenocompetinginterests. |     |     |      |             |            |          |           |     |              |
informedneuralnetworks.JFluidMech.2021;915.
18. RaissiM,YazdaniA,KarniadakisGE.Hiddenfluidmechanics:
| Ethicsapprovalandconsenttoparticipate |     |     | Weconsenttoparticipate. |          |          |     |                 |      |                      |     |
| ------------------------------------- | --- | --- | ----------------------- | -------- | -------- | --- | --------------- | ---- | -------------------- | --- |
|                                       |     |     |                         | Learning | velocity | and | pressure fields | from | flow visualizations. |     |
Science.2020;367(6481):1026–1030.
| Consentforpublication | Weconsenttopublication. |     |     |           |        |                |     |           |     |              |
| --------------------- | ----------------------- | --- | --- | --------- | ------ | -------------- | --- | --------- | --- | ------------ |
|                       |                         |     |     | 19. Hu Z, | Shukla | K, Karniadakis | GE, | Kawaguchi | K.  | Tackling the |
curseofdimensionalitywithphysics-informedneuralnetworks.
NeuralNetw.2024;176:106369.
20. JinX,CaiS,LiH,KarniadakisGE.NSFnets(Navier-Stokesflow
nets):Physics-informedneuralnetworksfortheincompressible
References
Navier-Stokesequations.JComputPhys.2021;426:109951
|     |     |     |     | 21. Shukla | K, Zou | Z, Chan | CH, Pandey | A, Wang | Z,  | Karniadakis |
| --- | --- | --- | --- | ---------- | ------ | ------- | ---------- | ------- | --- | ----------- |
1. RaissiM,PerdikarisP,KarniadakisGE.Physics-informedneural GE.NeuroSEM:Ahybridframeworkforsimulatingmultiphysics
networks: A deep learning framework for solving forward and problems by coupling PINNs and spectral elements. Comput
inverse problems involving nonlinear partial differential equa- MethodsApplMechEng.2025;433:117498.
tions.JComputPhys.2019;378:686–707. 22. Yang Y, Perdikaris P. Adversarial uncertainty quantifica-
2. RaissiM,PerdikarisP,KarniadakisGE.PhysicsInformedDeep tion in physics-informed neural networks. J Comput Phys.
| Learning(PartI):Data-drivenSolutionsofNonlinearPartialDif- |     |     |     | 2019;394:136–52. |     |     |     |     |     |     |
| ---------------------------------------------------------- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- |
ferentialEquations.2017.arXiv:1711.10561. 23. Pang G, Lu L, Karniadakis GE. fPINNs: Fractional
3. RaissiM,PerdikarisP,KarniadakisGE.PhysicsInformedDeep physics-informed neural networks. SIAM J Sci Comput.
Learning (Part II): Data-driven Discovery of Nonlinear Partial 2019;41(4):2603–2626.
DifferentialEquations.2017.arXiv:1711.10566. 24. Karniadakis GE, Kevrekidis IG, Lu L, Perdikaris P, Wang S,
4. CuomoS,DiColaVS,GiampaoloF,RozzaG,RaissiM,Pic- Yang L. Physics-informed machine learning. Nat Rev Phys.
| cialli F. | Scientific machine | learning | through physics-informed | 2021;3(6):422–40. |     |     |     |     |     |     |
| --------- | ------------------ | -------- | ------------------------ | ----------------- | --- | --- | --- | --- | --- | --- |
neuralnetworks:Whereweareandwhat’snext.JSciComput. 25. BaydinAG,PearlmutterBA,RadulAA,SiskindJM.Automatic
differentiationinmachinelearning:asurvey.JMachLearnRes.
2022;92(3):88.
2018;18(153):1–43.
5. FareaA,Yli-HarjaO,Emmert-StreibF.UnderstandingPhysics-
|          |                  |             |                       | 26. Meng | X, Li | Z, Zhang | D, Karniadakis | GE. | PPINN: | Parareal |
| -------- | ---------------- | ----------- | --------------------- | -------- | ----- | -------- | -------------- | --- | ------ | -------- |
| Informed | Neural Networks: | Techniques, | Applications, Trends, |          |       |          |                |     |        |          |
physics-informedneuralnetworkfortime-dependentPDEs.Com-
andChallenges.AI2024;5(3):1534–1557.
putMethodsApplMechEng2020;370:113250
6. GangaS,UddinZ.ExploringPhysics-InformedNeuralNetworks:
FromFundamentalstoApplicationsinComplexSystems.2024. 27. HornikK,StinchcombeM,WhiteH.Multilayerfeedforwardnet-
arXiv:2410.00422[cs.CE]. worksareuniversalapproximators.NeuralNetw.1989;2(5):359–
| 7. Raissi | M, Perdikaris | P, Ahmadi | N, Karniadakis GE. | 66. |     |     |     |     |     |     |
| --------- | ------------- | --------- | ------------------ | --- | --- | --- | --- | --- | --- | --- |
Physics-informed neural networks and extensions. 2024. 28. DongS,NiN.Amethodforrepresentingperiodicfunctionsand
arXiv:2408.16806. enforcingexactlyperiodicboundaryconditionswithdeepneural
8. Zhao C, Zhang F, Lou W, Wang X, Yang J. A comprehen- networks.JComputPhys.2021;435:110242.
sive review of advances in physics-informed neural networks 29. Guan W, Yang K, Chen Y, Liao S, Guan Z. A dimension-
and their applications in complex fluid dynamics. Phys Fluids. augmentedphysics-informedneuralnetwork(DaPINN)withhigh
2024;36(10):101301. levelaccuracyandefficiency.JComputPhys.2023;491:112360.
123

15 Page 34 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
30. WangS,WangH,PerdikarisP.OntheeigenvectorbiasofFourier 50. ChenJ,DuR,WuK.AcomparisonstudyofdeepGalerkinmethod
featurenetworks:Fromregressiontosolvingmulti-scalePDEs anddeepRitzmethodforellipticproblemswithdifferentbound-
withphysics-informedneuralnetworks.ComputeMethodsAppl aryconditions.2020.arXiv:2005.04554
MechEng.2021;384:113938. 51. Zeinhofer M, Masri R, Mardal K-A. A unified framework for
31. Wang S, Li B, Chen Y, Perdikaris P. PirateNets: Physics- the error analysis of physics-informed neural networks. 2023
informedDeepLearningwithResidualAdaptiveNetworks.2024. arXiv:2311.00529.
arXiv:2402.00326. 52. BerroneS,CanutoC,PintoreM,SukumarN.EnforcingDirich-
32. SalimansT,KingmaDP.Weightnormalization:Asimplerepa- let boundary conditions in physics-informed neural networks
rameterizationtoacceleratetrainingofdeepneuralnetworks.Adv and variational physics-informed neural networks. Heliyon.
NeuralInfProcessSyst.2016;29 2023;9(8).
33. Wang S, Wang H, Seidman JH, Perdikaris P. Random weight 53. LeakeC,MortariD.Deeptheoryoffunctionalconnections:A
factorization improves the training of continuous neural repre- new method for estimating the solutions of partial differential
sentations.2022.arXiv:2210.01274. equations.MachLearnKnowlExtraction.2020;2(1):37–55.
34. Jagtap AD, Mitsotakis D, Karniadakis GE. Deep learning 54. Lu L, Pestourie R, Yao W, Wang Z, Verdugo F, Johnson SG.
of inverse water waves problems using multi-fidelity data: Physics-informed neural networks with hard constraints for
Application to Serre–Green–Naghdi equations. Ocean Eng. inversedesign.SIAMJSciComput.2021;43(6):1105–32.
2022;248:110775 55. Wang S, Sankaran S, Perdikaris P. Respecting causality is all
35. Sukumar N, Srivastava A. Exact imposition of boundary con- you need for training physics-informed neural networks. 2022.
ditionswithdistancefunctionsinphysics-informeddeepneural arXiv:2203.07404.
networks.ComputMethodsApplMechEng.2022;389:114333. 56. Barschkis S. Exact and soft boundary conditions in Physics-
36. WangS,TengY,PerdikarisP.Understandingandmitigatinggradi- InformedNeuralNetworksfortheVariableCoefficientPoisson
entflowpathologiesinphysics-informedneuralnetworks.SIAM equation.2023.arXiv:2310.02548.
JSciComput.2021;43(5):3055–81. 57. Anagnostopoulos SJ,ToscanoJD,StergiopulosN,Karniadakis
37. CaiS,LiH,ZhengF,KongF,DaoM,KarniadakisGE,SureshS. GE.LearninginPINNs:Phasetransition,totaldiffusion,andgen-
Artificialintelligencevelocimetryandmicroaneurysm-on-a-chip eralization.2024.arXiv:2403.18494.
forthree-dimensionalanalysisofbloodflowinphysiologyand 58. Jin P, Zhang Z, Zhu A, Tang Y, Karniadakis GE. SympNets:
disease.ProceedNationalAcadSci.2021;118(13) Intrinsic structure-preserving symplectic networks for identify-
38. Anagnostopoulos SJ,ToscanoJD,Stergiopulos N,Karniadakis ingHamiltoniansystems.NeuralNetw.2020;132:166–179
GE. Residual-based attention in physics-informed neural net- 59. ZhouK,GrauerSJ.Flowreconstructionandparticlecharacteri-
works.ComputMethodsApplMechEng.2024;421:116805 zationfrominertialLagrangiantracks.2023.arXiv:2311.09076.
39. MaoZ,JagtapAD,KarniadakisGE.Physics-informedneuralnet- 60. JagtapAD,KawaguchiK,KarniadakisGE.Adaptiveactivation
worksforhigh-speedflows.ComputMethodsApplMechEng. functionsaccelerateconvergenceindeepandphysics-informed
2020;360:112789 neuralnetworks.JComputPhys.2020;404:109136
40. Zapf B, Haubner J, Kuchta M, Ringstad G, Eide PK, Mardal 61. Jagtap AD, Kawaguchi K, Em Karniadakis G. Locally adap-
K-A. Investigating molecular transport in the human brain tive activation functions with slope recovery for deep and
from MRI with physics-informed neural networks. Sci Report. physics-informed neural networks. Proceed Royal Soc A.
2022;12(1):15475 2020;476(2239):20200334.
41. RahamanN,BaratinA,ArpitD,DraxlerF,LinM,HamprechtF, 62. LiuZ,WangY,VaidyaS,RuehleF,HalversonJ,Soljacˇic´M,Hou
BengioY,CourvilleA.Onthespectralbiasofneuralnetworks. TY, Tegmark M. KAN: Kolmogorov-Arnold Networks. 2024.
In:Internationalconferenceonmachinelearning.PMLR;2019. arXiv:2404.19756.
p.5301–5310. 63. Karniadakis G, Sherwin SJ. Spectral/hp Element Methods for
42. CaoY,FangZ,WuY,ZhouD-X,GuQ.Towardsunderstanding ComputationalFluidDynamics.OxfordUniversityPress,USA,
thespectralbiasofdeeplearning.2019.arXiv:1912.01198. 2005.
43. CaiW,XuZ-QJ.Multi-scaledeepneuralnetworksforsolving 64. Howard AA, Jacob B, Murphy SH, Heinlein A, Stinis P.
highdimensionalPDEs.2019.arXiv:1910.11710. Finite basis Kolmogorov-Arnold networks: domain decompo-
44. Liu Z, Cai W, Xu Z-QJ. Multi-scale deep neural network sition for data-driven and physics-informed problems. 2024.
(MscaleDNN)forsolvingPoisson-Boltzmannequationincom- arXiv:2406.19662.
plexdomains.2020.arXiv:2007.11207. 65. RigasS,PapachristouM,PapadopoulosT,AnagnostopoulosF,
45. Wang B, Zhang W, Cai W. Multi-scale deep neural network Alexandridis G. Adaptive training of grid-dependent physics-
(MscaleDNN) methods for oscillatory stokes flows in complex informedkolmogorov-arnoldnetworks.2024.arXiv:2407.17611.
domains.2020.arXiv:2009.12729 66. ShuaiH,LiF.Physics-InformedKolmogorov-ArnoldNetworks
46. LiuL,CaiW,etal.Linearizedlearningwithmultiscaledeepneural forPowerSystemDynamics.2024.arXiv:2408.06650.
networksforstationaryNavier-Stokesequationswithoscillatory 67. Wang Y, Sun J, Bai J, Anitescu C, Eshaghi MS, Zhuang X,
solutions.EastAsianJApplMath.2022;13(3). RabczukT,LiuY.KolmogorovArnoldInformedneuralnetwork:
47. Ahmadi Daryakenari N, De Florio M, Shukla K, Karni- Aphysics-informeddeeplearningframeworkforsolvingforward
adakis GE. AI-Aristotle: A physics-informed framework for and inverse problems based on Kolmogorov Arnold Networks.
systems biology gray-box identification. PLOS Comput Biol. 2024.arXiv:2406.11045[cs.LG].
2024;20(3):1011916. 68. Guilhoto L.F, Perdikaris P. Deep Learning Alternatives of the
48. Zhang Z, Shen T, Zhang Y,Zhang W, Wang Q. AL-PKAN: A Kolmogorov superposition theorem. 2024. arXiv:2410.01990
HybridGRU-KANNetworkwithAugmentedLagrangianFunc- [cs.LG].
tionforSolvingPDEs.AvailableatSSRN.2024;4957859 69. Koenig BC, Kim S, Deng S. Kan-odes: Kolmogorov-arnold
49. Toscano JD, Käufer T, Maxey M, Cierpka C, Karni- network ordinary differential equations for learning dynamical
adakis GE. Inferring turbulent velocity and temperature fields systemsandhiddenphysics.ComputMethodsApplMechEng.
and their statistics from Lagrangian velocity measurements 2024;432:117397.
using physics-informed Kolmogorov-Arnold Networks. 2024 70. Patra S, Panda S, Parida BK, Arya M, Jacobs K, Bondar DI,
arXiv:2407.15727. Sen A. Physics informed kolmogorov-arnold neural networks
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 35 of 43 15
for dynamical analysis via efficent-kan and wav-kan. 2024. 91. LakshminarayananB,PritzelA,BlundellC.Simpleandscalable
arXiv:2407.18373. predictiveuncertaintyestimationusingdeepensembles.AdvNeu-
71. WangY,SiegelJW,LiuZ,HouTY.Ontheexpressivenessand ralInfProcessSyst.2017;30.
spectralbiasofkans.2024.arXiv:2410.01803. 92. Quiñonero-Candela J, Dagan I, Magnini B, D’Alché-Buc F.
72. Liu Z, Ma P, Wang Y, Matusik W, Tegmark M. Kan MachineLearningChallenges:EvaluatingPredictiveUncertainty,
2.0: Kolmogorov-arnold networks meet science. 2024. Visual Object Classification, and Recognizing Textual Entail-
arXiv:2408.10205. ment, First Pascal Machine Learning Challenges Workshop,
73. Gao H, Sun L, Wang J-X. Super-resolution and denoising of MLCW 2005, Southampton, UK, April 11-13, 2005, Revised
fluid flow using physics-informed convolutional neural net- SelectedPapersvol.3944.Springer,2006
works without high-resolution labels. Phys Fluids. 2021;33(7): 93. CawleyGC,TalbotNL,ChapelleO.Estimatingpredictivevari-
073603. anceswithkernelridgeregression.In:MachineLearningChal-
74. Wandel N, Weinmann M, Neidlin M, Klein R. Spline-PINN: lengesWorkshop,Springer.2005;p.56–77.
Approaching PDEs without data using fast, physics-informed 94. LimK.L,DuttaR,RotaruM.Physicsinformedneuralnetwork
hermite-splineCNNs.In:ProceedingsoftheAAAIConference usingfinitedifferencemethod.In:2022IEEEInternationalCon-
onArtificialIntelligence,2022;vol.36,p.8529–8538. ferenceonSystems,Man,andCybernetics(SMC),IEEE.2022.
75. YangL,ZhangD,KarniadakisGE.Physics-informedgenerative p.1828–1833.
adversarialnetworksforstochasticdifferentialequations.SIAM 95. Gladstone RJ, Nabian MA, Meidani H. FO-PINNs: A first-
JSciComput.2020;42(1):292–317 order formulation for physics informed neural networks. 2022
76. Bullwinkel B, Randle D, Protopapas P, Sondak D. DEQGAN: arXiv:2210.14320.
learningthelossfunctionforPINNswithgenerativeadversarial 96. Huang Y, Hao W, Lin G. HomPINNs: Homotopy physics-
networks.2022.arXiv:2209.07081. informed neural networks for learning multiple solutions of
77. ZhangQ,WuC,KahanaA,KimY,LiY,KarniadakisGE,Panda nonlinear elliptic differential equations. Comput Math Appl.
P.ArtificialtoSpikingNeuralNetworksConversionforScientific 2022;121:62–73.
MachineLearning.2023arXiv:2308.16372. 97. Wang S, Yu X, Perdikaris P. When and why PINNs fail to
78. Zhao Z, Ding X, Prakash BA. Pinnsformer: A transformer- train: A neural tangent kernel perspective. J Comput Phys.
based framework for physics-informed neural networks. 2023. 2022;449:110768.
arXiv:2307.11833. 98. Raissi M, Babaee H, Givi P. Deep learning of turbulent scalar
79. ChoG,ZhuD,CampbellJJ,WangM.AnLSTM-PINNhybrid mixing.PhysRevFluids.2019;4(12):124501.
methodtoestimatelithium-ionbatterypacktemperature.IEEE 99. KharazmiE,ZhangZ,KarniadakisGE.hp-VPINNs:Variational
Access.2022;10:100594–604. physics-informed neuralnetworkswithdomaindecomposition.
80. NathasarmaR,RoyBK.Physics-informedlong-short-termmem- ComputMethodsApplMechEng.2021;374:113547
oryneuralnetworkforparametersestimationofnonlinearsys- 100. Raissi M. Forward–backward stochastic neural networks: deep
tems.IEEETransIndustryAppl.2023;59(5):5376–5384. learning of high-dimensional partial differential equations. In:
81. Guo L, Wu H, Wang Y, Zhou W, Zhou T. IB-UQ: Infor- Peter Carr Gedenkschrift: Research Advances in Mathematical
mation bottleneck based uncertainty quantification for neural Finance,pp.637–655.WorldScientific,2024
functionregressionandneuraloperatorlearning.JComputPhys. 101. BuzaevF,GaoJ,ChuprovI,KazakovE.Hybridaccelerationtech-
2024;113089. niquesforthephysics-informedneuralnetworks:acomparative
82. BanerjeeC,NguyenK,FookesC,RaissiM.Asurveyonphysics analysis.MachLearn.2024;113(6):3675–92.
informed reinforcement learning: Review and open problems. 102. MehtaPP,PangG,SongF,KarniadakisGE.Discoveringauni-
2023.arXiv:2309.01909. versalvariable-orderfractionalmodelforturbulentCouetteflow
83. Ramesh A, Ravindran B. Physics-informed model-based rein- using a physics-informed neural network. Fractional Calculus
forcement learning. In: Learning for Dynamics and Control ApplAnal2019;22(6):1675–1688.
Conference,PMLR.2023.p.26–37. 103. RenH,MengX,LiuR,HouJ,YuY.Aclassofimprovedfractional
84. RadaidehMI,WolvertonI,JosephJ,TusarJJ,OtgonbaatarU,Roy physicsinformedneuralnetworks.Neurocomputing.2023;562:
N,ForgetB,ShirvanK.Physics-informedreinforcementlearn- 126890.
ingoptimizationofnuclearassemblydesign.NuclearEngDes. 104. Wang S, Karniadakis GE. GMC-PINNs: A new general monte
2021;372:110966. carlo PINNs method for solving fractional partial differential
85. Jiang F, Hou X, Xia M. Densely Multiplied Physics Informed equationsonirregulardomains.2024.arXiv:2405.00217.
NeuralNetwork.2024.arXiv:2402.04390. 105. Sivalingam S, Govindaraj V. Physics informed neural network
86. Cho J, Nam S, Yang H, Yun S-B, Hong Y, Park E. Separable basedschemeanditserroranalysisforψ-Caputotypefractional
physics-informedneuralnetworks.AdvNeuralInfProcessSyst. differentialequations.PhysScripta.2024;99(9):096002.
2024;36. 106. Hu Z, Kawaguchi K, Zhang Z, Karniadakis GE. Tackling the
87. WangY,JinP,XieH.Tensorneuralnetworkanditsnumerical Curse of Dimensionality in Fractional and Tempered Frac-
integration.2022.arXiv:2207.02754. tional PDEs with Physics-Informed Neural Networks. 2024.
88. WangT,HuZ,KawaguchiK,ZhangZ,KarniadakisGE.Tensor arXiv:2406.11708.
neuralnetworksforhigh-dimensionalFokker-Planckequations. 107. WangC,LiS,HeD,WangL.IsL2PhysicsInformedLossAlways
2024.arXiv:2404.05615. Suitable for Training Physics Informed Neural Network? Adv
89. VemuriS.K,BüchnerT,NieblingJ,DenzlerJ.FunctionalTensor NeuralInfProcessSyst.2022;35:8278–90.
Decompositions for Physics-Informed Neural Networks. 2024. 108. He D, Li S, Shi W, Gao X, Zhang J, Bian J, Wang L, Liu T-
arXiv:2408.13101. Y. Learning physics-informed neural networks without stacked
90. ToscanoJD,WuC,Ladron-de-GuevaraA,DuT,NedergaardM, back-propagation.In:InternationalConferenceonArtificialIntel-
KelleyDH,KarniadakisGE,BosterK.Inferringinvivomurine ligenceandStatistics,PMLR.2023.p.3034–3047.
cerebrospinal fluid flow using artificial intelligence velocime- 109. Wang S, Sankaran S, Wang H, Perdikaris P. An expert’s
try with moving boundaries and uncertainty quantification. guide to training physics-informed neural networks. 2023.
2024;bioRxiv,2024–08 arXiv:2308.08468.
123

15 Page 36 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
110. WangZ,MengX,JiangX,XiangH,KarniadakisGE.Solution 130. JagtapAD,KarniadakisGE.Extendedphysics-informedneural
multiplicity and effects of data and eddy viscosity on Navier- networks(XPINNs): Ageneralizedspace-timedomaindecom-
Stokessolutionsinferredbyphysics-informedneuralnetworks. position based deep learning framework for nonlinear partial
2023.arXiv:2309.06010. differentialequations.CommunComputPhys.2020;28(5).
111. BasirS.InvestigatingandMitigatingFailureModesinPhysics- 131. Hu Z, Jagtap AD, Karniadakis GE, Kawaguchi K. When do
informedNeuralNetworks(PINNs).2022.arXiv:2209.09988. extendedphysics-informedneuralnetworks(XPINNs)improve
112. Kharazmi E, Zhang Z, Karniadakis GE. Variational physics- generalization?2021.arXiv:2109.09444.
informed neural networks for solving partial differential equa- 132. De Ryck T, Jagtap AD, Mishra S. Error estimatesfor physics-
tions.2019arXiv:1912.00873. informedneuralnetworksapproximatingtheNavier-Stokesequa-
113. YuB,etal.ThedeepRitzmethod:adeeplearning-basednumer- tions.IMAJNumerAnal.2024;44(1):83–119.
icalalgorithmforsolvingvariationalproblems.CommunMath 133. JagtapAD,KharazmiE,KarniadakisGE.Conservativephysics-
Stat.2018;6(1):1–12. informedneuralnetworksondiscretedomainsforconservation
114. Khodayi-Mehr R, Zavlanos M. VarNet: Variational neural net- laws: Applications to forward and inverse problems. Comput
worksforthesolutionofpartialdifferentialequations.In:Learn- MethodsApplMechEng.2020;365:113028.
ingforDynamicsandControl,PMLR.2020.p.298–307. 134. Hu Z, Jagtap AD, Karniadakis GE, Kawaguchi K. Augmented
115. Berrone S, Pintore M. Meshfree Variational Physics Informed Physics-InformedNeuralNetworks(APINNs):Agatingnetwork-
Neural Networks (MF-VPINN): an adaptive training strategy. basedsoftdomaindecompositionmethodology.EngApplArtif
2024.arXiv:2406.19831. Intell.2023;126:107183.
116. MiaoZ,ChenY.VC-PINN:Variablecoefficientphysics-informed 135. MoseleyB,MarkhamA,Nissen-MeyerT.FiniteBasisPhysics-
neural network for forward and inverse problems of pdes with Informed Neural Networks (FBPINNs): a scalable domain
variablecoefficient.PhysicaD:NonlinearPhenomena.2023;456: decompositionapproachforsolvingdifferentialequations.Adv
133945. ComputMath.2023;49(4):62.
117. SongJ,CaoW,LiaoF,ZhangW.VW-PINNs:Avolumeweighting 136. DoleanV,HeinleinA,MishraS,MoseleyB.Multileveldomain
methodforPDEresidualsinphysics-informedneuralnetworks. decomposition-based architectures for physics-informed neural
2024.arXiv:2401.06196. networks.ComputMethodsApplMechEng.2024;429:117116.
118. Ghose D, Anandh T, Ganesan S. FastVPINNs: A fast, ver- 137. LiuC,WuH.cv-PINN:Efficientlearningofvariationalphysics-
satile and robust Variational PINNs framework for forward informedneuralnetworkwithdomaindecomposition.Extreme
and inverse problems in science. In: ICLR 2024 Workshop on MechLett.2023;63:102051.
AI4DifferentialEquationsInScience 138. NguyenL,RaissiM,SeshaiyerP.Efficientphysicsinformedneu-
119. Anandh T, Ghose D, Tyagi A, Gupta A, Sarkar S, Ganesan S. ral networks coupled with domain decomposition methods for
Anefficienthp-VariationalPINNsframeworkforincompressible solvingcoupledmulti-physicsproblems.In:AdvancesinCom-
Navier-Stokesequations.2024.arXiv:2409.04143. putationalModelingandSimulation,pp.41–53.Springer,2022.
120. GuoL,WuH,YuX,ZhouT.MonteCarlofPINNs:Deeplearning 139. KopanicˇákováA,KothariH,KarniadakisG.E,KrauseR.Enhanc-
methodforforwardandinverseproblemsinvolvinghighdimen- ingtrainingofphysics-informedneuralnetworksusingdomain
sionalfractionalpartialdifferentialequations.ComputMethods decomposition–based preconditioning strategies. SIAM J Sci
ApplMechEng.2022;400:115523. Comput.2024;46–67.
121. Zhang D, Guo L, Karniadakis GE. Learning in modal space: 140. Daryakenari NA, Wang S, Karniadakis G. Cminns: Compart-
Solvingtime-dependentstochasticPDEsusingphysics-informed mentmodelinformedneuralnetworks–unlockingdrugdynamics.
neuralnetworks.SIAMJSciComput.2020;42(2):639–665. 2024.arXiv:2409.12998.
122. Hu Z, Zhang Z, Karniadakis GE, Kawaguchi K. Score- 141. WightCL,ZhaoJ.SolvingAllen-CahnandCahn-Hilliardequa-
fPINN: Fractional Score-Based Physics-Informed Neural Net- tionsusingtheadaptivephysicsinformedneuralnetworks.2020.
works for High-Dimensional Fokker-Planck-Levy Equations. arXiv:2007.04542.
2024.arXiv:2406.11676. 142. Krishnapriyan A, Gholami A, Zhe S, Kirby R, Mahoney
123. HowardAA,MurphySH,AhmedSE,StinisP.Stackednetworks MW.Characterizingpossiblefailuremodesinphysics-informed
improve physics-informed training: applications to neural net- neuralnetworks.AdvNeuralInfProcessSyst.2021;34:26548–
worksanddeepoperatornetworks.2023.arXiv:2311.06483. 26560.
124. ShuklaK,JagtapAD,KarniadakisGE.Parallelphysics-informed 143. MatteyR,GhoshS.Anovelsequentialmethodtotrainphysics
neural networks via domain decomposition. J Comput Phys. informedneuralnetworksforAllenCahnandCahnHilliardequa-
2021;447:110683 tions.ComputMethodsApplMechEng.2022;390:114474.
125. Wu C, Zhu M, Tan Q, Kartha Y, Lu L. A comprehensive 144. HaitsiukevichK,IlinA.Improvedtrainingofphysics-informed
studyofnon-adaptiveandresidual-basedadaptivesamplingfor neural networks with model ensembles. In: 2023 International
physics-informed neural networks. Comput Meth Appl Mech JointConferenceonNeuralNetworks(IJCNN),IEEE.2023.p.
Eng.2023;403:115671. 1–8(2023).
126. UrbánJF,StefanouP,PonsJA.Unveilingtheoptimizationpro- 145. Chen P, Meng T, Zou Z, Darbon J, Karniadakis GE. Leverag-
cess of Physics Informed Neural Networks: How accurate and ingHamilton-JacobiPDEswithtime-dependentHamiltoniansfor
competitivecanPINNsbe?2024arXiv:2405.04230. continualscientificmachinelearning.In:6thAnnualLearningfor
127. Liu Q, Chu M, Thuerey N. ConFIG: Towards Conflict- Dynamics&ControlConference,PMLR.2024.p.1–12.
free Training of Physics Informed Neural Networks. 2024. 146. PenwardenM,JagtapAD,ZheS,KarniadakisGE,KirbyRM.
arXiv:2408.11104. Aunifiedscalableframeworkforcausalsweepingstrategiesfor
128. AkhterJ,FährmannP.D,SonntagK,PeitzS.Commonpitfallsto physics-informed neural networks (PINNs) and their temporal
avoidwhileusingmultiobjectiveoptimizationinmachinelearn- decompositions.JComputPhys.2023;493:112464.
ing.2024.arXiv:2405.01480. 147. Desai S, Mattheakis M, Joy H, Protopapas P, Roberts S. One-
129. Davi C, Braga-Neto U. PSO-PINN: Physics-informed neu- shottransferlearningofphysics-informedneuralnetworks.2021.
ral networks trained with particle swarm optimization. 2022. arXiv:2110.11286.
arXiv:2202.01943.
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 37 of 43 15
148. LiuY,LiuW,YanX,GuoS,ZhangC-a.Adaptivetransferlearning 169. Song Y, Wang H, Yang H, Taccari ML, Chen X. Loss-
forPINN.JComputPhys.2023;490:112291. attentional physics-informed neural networks. J Comput Phys.
149. Xu C, Cao BT, Yuan Y, Meschke G. Transfer learning based 2024;501:112781.
physics-informedneuralnetworksforsolvinginverseproblems 170. RamirezI,PinoJ,PardoD,SanzM,RioL,OrtizA,Morozovska
inengineeringstructuresunderdifferentloadingscenarios.Com- K,AizpuruaJI.Residual-basedAttentionPhysics-informedNeu-
putMethodsApplMechEng.2023;405:115852. ralNetworksforEfficientSpatio-TemporalLifetimeAssessment
150. ChenY,XiaoH,TengX,LiuW,LanL.Enhancingaccuracyof of Transformers Operated in Renewable Power Plants. 2024.
physicallyinformedneuralnetworksfornonlinearSchrödinger arXiv:2405.06443.
equations through multi-view transfer learning. Inf Fusion. 171. ChenW,HowardAA,StinisP.Self-adaptiveweightsbasedonbal-
2024;102:102041. ancedresidualdecayrateforphysics-informedneuralnetworks
151. ChenP,MengT,ZouZ,DarbonJ,KarniadakisGE.Leveraging anddeepoperatornetworks.2024.arXiv:2407.01613.
multitimeHamilton–JacobiPDEsforcertainscientificmachine 172. Lu L, Meng X, Mao Z, Karniadakis GE. DeepXDE: A deep
learningproblems.SIAMJSciComput.2024;46(2):216–248. learning library for solving differential equations. SIAM Rev.
152. ZhangH,ChanRH,TaiX-C.AMeshlessSolverforBloodFlow 2021;63(1):208–228.
SimulationsinElasticVesselsUsingaPhysics-InformedNeural 173. Daw A, Bu J, Wang S, Perdikaris P, Karpatne A. Rethinking
Network.SIAMJSciComput.2024;46(4):479–507. theimportanceofsamplinginphysics-informedneuralnetworks.
153. MengX,KarniadakisGE.Acompositeneuralnetworkthatlearns 2022.arXiv:2207.02338.
frommulti-fidelitydata:Applicationtofunctionapproximation 174. Gao W, Wang C. Active learning based sampling for high-
andinversePDEproblems.JComputPhys.2020;401:109020. dimensional nonlinear partial differential equations. J Comput
154. Meng X, Babaee H, Karniadakis GE. Multi-fidelity Bayesian Phys.2023;475:111848.
neural networks: Algorithms and applications. J Comput Phys. 175. TangK,WanX,YangC.DAS:Adeepadaptivesamplingmethod
2021;438:110361. forsolvingpartialdifferentialequations.2021.arXiv:2112.14038.
155. RegazzoniF,PaganiS,CosenzaA,LombardiA,QuarteroniA.A 176. PengW,ZhouW,ZhangX,YaoW,LiuZ.Rang:Aresidual-based
physics-informedmulti-fidelityapproachfortheestimationofdif- adaptivenodegenerationmethodforphysics-informedneuralnet-
ferentialequationsparametersinlow-dataorlarge-noiseregimes. works.2022arXiv:2205.01051.
RendicontiLincei.2021;32(3):437–70. 177. ZengS,ZhangZ,ZouQ.Adaptivedeepneuralnetworksmeth-
156. WangY,LaiC.-Y.Multi-stageneuralnetworks:Functionapprox- odsforhigh-dimensionalpartialdifferentialequations.JComput
imatorofmachineprecision.JComputPhys.2024;504:112865. Phys.2022;463:111232.
157. Heinlein A, Howard AA, Beecroft D, Stinis P. Multifidelity 178. HannaJM,AguadoJV,Comas-CardonaS,AskriR,Borzacchiello
domaindecomposition-basedphysics-informedneuralnetworks D. Residual-based adaptivity for two-phase flow simulation in
fortime-dependentproblems.2024.arXiv:2401.07888. porousmediausingphysics-informedneuralnetworks.Comput
158. PenwardenM,ZheS,NarayanA,KirbyRM.Multifidelitymod- MethodsApplMechEng.2022;396:115100.
elingforphysics-informedneuralnetworks(PINNs).JComput 179. SubramanianS,KirbyRM,MahoneyMW,GholamiA.Adaptive
Phys.2022;451:110844. self-supervision algorithms for physics-informed neural net-
159. LiuJ.S,LiuJS.MonteCarloStrategiesinScientificComputing works.In:ECAI2023,IOSPress,2023.p.2234–2241.
vol.10.Springer,2001. 180. Nabian MA, Gladstone RJ, Meidani H. Efficient training of
160. BosterKA,CaiS,Ladrón-de-GuevaraA,SunJ,ZhengX,DuT, physics-informed neural networks via importance sampling.
ThomasJH,NedergaardM,KarniadakisGE,KelleyDH.Artifi- Computer-AidedCivilInfrastructEng.2021;36(8):962–77.
cialintelligencevelocimetryrevealsinvivoflowrates,pressure 181. Daw A, Bu J, Wang S, Perdikaris P, Karpatne A. Mitigating
gradients,andshearstressesinmurineperivascularflows.Proceed propagationfailuresinphysics-informedneuralnetworksusing
NationalAcadSci.2023;120(14):2217744120. retain-resample-release(r3)sampling.2022.arXiv:2207.02338.
161. Xiang Z, Peng W, Liu X, Yao W. Self-adaptive loss bal- 182. GaoZ,YanL,ZhouT.Failure-informedadaptivesamplingfor
anced Physics-informed neural networks. Neurocomputing. PINNs.SIAMJSciComput.2023;45(4):1971–94.
2022;496:11–34. 183. GaoZ,TangT,YanL,ZhouT.Failure-informedadaptivesam-
162. Liu D, Wang Y. A Dual-Dimer method for training physics- plingforPINNs,partii:combiningwithre-samplingandsubset
constrainedneuralnetworkswithminimaxarchitecture.Neural simulation.CommunApplMathComput.2023;1–22.
Netw.2021;136:112–25. 184. ZhouK,LiJ,HongJ,GrauerS.J.Stochasticparticleadvection
163. McClennyLD,Braga-NetoUM.Self-adaptivephysics-informed velocimetry (SPAV): theory, simulations, and proof-of-concept
neuralnetworks.JComputPhys.2023;474:111722. experiments.MeasSciTechnol.2023;34(6):065302.
164. ZhangG,YangH,ZhuF,ChenY,etal.DASA-PINNs:Differ- 185. NocedalJ,WrightSJ.NumericalOptimization.Springer,1999.
entiableAdversarialSelf-AdaptivePointwiseWeightingScheme 186. KingmaDP,BaJ.Adam:Amethodforstochasticoptimization.
forPhysics-InformedNeuralNetworks.SSRN2023 2014.arXiv:1412.6980.
165. Basir S, Senocak I. Physics and equality constrained artificial 187. Liu DC, Nocedal J. On the limitedmemory BFGS method for
neural networks: Application to forward and inverse problems largescaleoptimization.MathProgram.1989;45(1):503–28.
withmulti-fidelitydatafusion.JComputPhys.2022;463:111301. 188. Lu B, Moya C, Lin G. NSGA-PINN: a multi-objective opti-
166. BasirS,SenocakI.AnadaptiveaugmentedLagrangianmethod mizationmethodforphysics-informedneuralnetworktraining.
fortrainingphysicsandequalityconstrainedartificialneuralnet- Algorithms.2023;16(4):194.
works.2023.arXiv:2306.04904. 189. Zhou T, Zhang X, Droguett EL, Mosleh A. A generic
167. SonH,ChoSW,HwangHJ.EnhancedPhysics-InformedNeural physics-informed neural network-based framework for reliabil-
NetworkswithAugmentedLagrangianRelaxationMethod(AL- ity assessment of multi-state systems. Reliab Eng Syst Saf.
PINNs).Neurocomputing.2023;126424. 2023;229:108835.
168. Anagnostopoulos SJ,ToscanoJD,Stergiopulos N,Karniadakis 190. Yao J, Su C, Hao Z, Liu S, Su H, Zhu J. Multiadam:
GE.Residual-basedattentionandconnectiontoinformationbot- Parameter-wisescale-invariantoptimizerformultiscaletraining
tlenecktheoryinPINNs.2023.arXiv:2307.00379.
123

15 Page 38 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
of physics-informed neural networks. In: International Confer- 211. RodriguesJA.UsingPhysics-InformedNeuralNetworks(PINNs)
enceonMachineLearning,PMLR.2023,p.39702–39721. fortumorcellgrowthmodeling.Mathematics.2024;12(8).
191. Fang Z, Wang S, Perdikaris P. Ensemble learning for physics 212. SoukariehI,HesslerG,MinouxH,MohrM,SchmidtF,Wen-
informedneuralnetworks:Agradientboostingapproach.2023. zel J, Barbillon P, Gangloff H, Gloaguen P. HyperSBINN:
arXiv:2302.13143. A Hypernetwork-Enhanced Systems Biology-Informed Neural
192. CyrEC,GulianMA,PatelRG,PeregoM,TraskNA.Robusttrain- Network for Efficient Drug Cardiosafety Assessment. 2024.
ingandinitializationofdeepneuralnetworks:Anadaptivebasis arXiv:2408.14266.
viewpoint. In: Mathematical and Scientific Machine Learning, 213. Chiu C-E, Pinto AL, Chowdhury RA, Christensen K, Varela
PMLR,2020.p.512–536. M. Characterisation of Anti-Arrhythmic Drug Effects on Car-
193. AinsworthM,ShinY.Plateauphenomenoningradientdescent diacElectrophysiologyusingPhysics-InformedNeuralNetworks.
trainingofrelunetworks:Explanation,quantification,andavoid- 2024.arXiv:2403.08439.
ance.SIAMJSciComput.2021;43(5):3438–68. 214. KissasG,YangY,HwuangE,WitscheyWR,DetreJA,Perdikaris
194. Ainsworth M, Shin Y. Active neuron least squares: A training P.Machinelearningincardiovascularflowsmodeling:Predicting
method for multivariate rectified neural networks. SIAM J Sci arterialbloodpressurefromnon-invasive4DflowMRIdatausing
Comput.2022;44(4):2253–75. physics-informedneuralnetworks.ComputMethodsApplMech
195. JniniA,VellaF,ZeinhoferM.Gauss-NewtonNaturalGradient Eng.2020;358:112623.
Descent for Physics-Informed Computational Fluid Dynamics. 215. Sun L, Gao H, Pan S, Wang J-X. Surrogate modeling for
2024.arXiv:2402.10680. fluidflowsbasedonphysics-constraineddeeplearningwithout
196. Rathore P, Lei W, Frangella Z, Lu L, Udell M. Chal- simulation data. Comput Methods Appl Mech Eng. 2020;361:
lenges in training PINNs: A loss landscape perspective. 2024. 112732.
arXiv:2402.01868. 216. ArzaniA,WangJ-X,D’SouzaRM.Uncoveringnear-wallblood
197. MüllerJ,ZeinhoferM.Achievinghighaccuracywithpinnsvia flow from sparse data with physics-informed neural networks.
energynaturalgradientdescent.In:InternationalConferenceon PhysFluids.2021;33(7):071905.
MachineLearning,PMLR,2023,p.25471–25485. 217. DanekerM,CaiS,QianY,MyzelevE,KumbhatA,LiH,LuL.
198. Dangel F, Müller J, Zeinhofer M. Kronecker-factored approx- Transferlearningonphysics-informedneuralnetworksfortrack-
imate curvature for physics-informed neural networks. 2024. ingthehemodynamicsintheevolvingfalselumenofdissected
arXiv:2405.15603. aorta.Nexus.2024;1(2).
199. LeeY,KopanicˇákováA,KarniadakisGE.Two-leveloverlapping 218. Yin M, Zheng X, Humphrey JD, Karniadakis GE. Non-
additiveSchwarzpreconditionerfortrainingscientificmachine invasiveinferenceofthrombusmaterialpropertieswithphysics-
learningapplications.2024.arXiv:2406.10997. informed neural networks. Comput Methods Appl Mech Eng.
200. OpenAI.DALL·E3.https://openai.com/dall-e2024. 2021;375:113603.
201. Yazdani A, Lu L, Raissi M, Karniadakis GE. Systems biol- 219. FathiMF,Perez-RayaI,BaghaieA,BergP,JanigaG,ArzaniA,
ogyinformeddeeplearningforinferringparametersandhidden D’Souza RM. Super-resolution and denoising of 4D-flow MRI
dynamics.PLOSComputBiol.2020;16(11). usingphysics-informeddeepneuralnets.ComputMethodsPro-
202. DanekerM,ZhangZ,KarniadakisGE,LuL.SystemsBiology: gramsBiomed.2020;197:105729.
Identifiabilityanalysisandparameteridentificationviasystems- 220. Liu M, Liang L, Sun W. A generic physics-informed neural
biologyinformedneuralnetworks.2022.arXiv:2202.01723. network-based constitutive model for soft biological tissues.
203. JoH,HongH,HwangHJ,ChangW,KimJK.Densityphysics- ComputMethodsApplMechEng.2020;372:113402.
informedneuralnetworksrevealsourcesofcellheterogeneityin 221. Lagergren JH, Nardini JT, Baker RE, Simpson MJ, Flores
signaltransduction.Patterns.2024;5(2). KB. Biologically-informed neural networks guide mechanistic
204. Sahli Costabal F, Yang Y, Perdikaris P, Hurtado DE, Kuhl E. modeling from sparse experimental data. PLOS Comput Biol.
Physics-informedneuralnetworksforcardiacactivationmapping. 2020;16(12):1008462.
FrontPhys.2020;8:42. 222. Sainz-DeMenaD,PérezM.A,García-AznarJM.Exploringthe
205. RuizHerreraC,GranditsT,PlankG,PerdikarisP,SahliCostabal potentialofPhysics-InformedNeuralNetworkstoextractvascu-
F,PezzutoS.Physics-informedneuralnetworkstolearncardiac larizationdatafromDCE-MRIinthepresenceofdiffusion.Med
fiberorientationfrommultipleelectroanatomicalmaps.EngCom- EngPhys.2024;123:104092.
put.2022;38(5):3957–73. 223. Awojoyogbe BO, Dada MO. Simulation of Temperature Dis-
206. QianY,ZhuG,ZhangZ,ModepalliS,ZhengY,ZhengX,Fryd- tribution in Biological Tissues Using Physics-Informed Neural
manG,LiH.Coagulo-Net:Enhancingthemathematicalmodeling Networks.In:DigitalMolecularMagneticResonanceImaging,
of blood coagulation using physics-informed neural networks. pp.217–228.Springer,2024.
NeuralNetw.2024;180:106732. 224. Caforio F, Regazzoni F, Pagani S, Karabelas E, Augustin C,
207. Chen Q, Ye Q, Zhang W, Li H, Zheng X. TGM-Nets: A deep HaaseG,PlankG,QuarteroniA.Physics-informedneuralnet-
learning framework for enhanced forecasting of tumor growth work estimation of material properties in soft tissue nonlinear
by integrating imaging and modeling. Eng Appl Artif Intell. biomechanicalmodels.ComputMech.2024;1–27.
2023;126:106867. 225. Wu W, Daneker M, Turner KT, Jolley MA, Lu L. Identifying
208. HerreroMartinC,OvedA,ChowdhuryRA,UllmannE,Peters heterogeneousmicromechanicalpropertiesofbiologicaltissues
NS, Bharath AA, Varela M. EP-PINNs: Cardiac electrophysi- viaphysics-informedneuralnetworks.2024.arXiv:2402.10741.
ologycharacterisationusingphysics-informedneuralnetworks. 226. RagozaM,BatmanghelichK.Physics-InformedNeuralNetworks
FrontCardiovascMed.2022;8:768419. for Tissue Elasticity Reconstruction in Magnetic Resonance
209. Goswami K, Sharma A, Pruthi M, Gupta R. Study of Drug Elastography.MedImageComputComput-AssistedInterv(MIC-
AssimilationinHumanSystemusingPhysicsInformedNeural CAI).2023;14229:333–43.
Networks.2021.arXiv:2110.05531. 227. Movahhedi M, Liu X-Y, Geng B, Elemans C, Xue Q, Wang
210. PodinaL,GhodsiA,KohandelM.LearningChemotherapyDrug J-X, Zheng X. Predicting 3D soft tissue dynamics from 2D
ActionviaUniversalPhysics-InformedNeuralNetworks.2024. imagingusingphysicsinformedneuralnetworks.CommunBiol.
arXiv:2404.08019. 2023;6(1):541.
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 39 of 43 15
228. LingHJ,BruS,PuigJ,VixègeF,MendezS,NicoudF,Courand 248. Yang X, Zafar S, Wang J-X, Xiao H. Predictive large-eddy-
P-Y, Bernard O, Garcia D. Physics-Guided Neural Networks simulationwallmodelingviaphysics-informedneuralnetworks.
forIntraventricularVectorFlowMapping.IEEETransactionson PhysRevFluids.2019;4(3):034602.
Ultrasonics,Ferroelectrics,andFrequencyControl.2024. 249. SongC,AlkhalifahT,WaheedUB.Solvingthefrequency-domain
229. SelK,MohammadiA,PettigrewRI,JafariR.Physics-informed acousticVTIwaveequationusingphysics-informedneuralnet-
neuralnetworksformodelingphysiologicaltimeseriesforcuff- works.GeophysJInt.2021;225(2):846–859.
lessbloodpressureestimation.npjDigitalMed.2023;6(1):110. 250. Lou Q, Meng X, Karniadakis GE. Physics-informed neural
230. DuToitJF,LaubscherR.EvaluationofPhysics-InformedNeural networks for solving forward and inverse flow problems via
NetworkSolutionAccuracyandEfficiencyforModelingAortic the Boltzmann-BGK formulation. J Comput Phys. 2021;447:
TransvalvularBloodFlow.MathComputAppl.2023;28(2):62. 110676.
231. Jagtap NV, Mudunuru MK, Nakshatrala KB. CoolPINNs: A 251. ErichsonN.B,MuehlebachM,MahoneyMW.Physics-informed
physics-informedneuralnetworkmodelingofactivecoolingin autoencoders for Lyapunov-stable fluid flow prediction. 2019.
vascularsystems.ApplMathModell.2023;122:265–87. arXiv:1905.10866.
232. HeldmannF,BerkhahnS,EhrhardtM,KlamrothK.Pinntraining 252. CalicchiaMA,MittalR,SeoJ-H,NiR.Reconstructingthepres-
usingbiobjectiveoptimization:Thetrade-offbetweendataloss surefieldaroundswimmingfishusingaphysics-informedneural
andresidualloss.JComputPhys.2023;488:112211. network.JExperBiol.2023;226(8).
233. TreibertS,EhrhardtM.APhysics-InformedNeuralNetworkto 253. ShuklaK,DiLeoniPC,BlackshireJ,SparkmanD,Karniadakis
ModelCOVID-19InfectionandHospitalizationScenarios2022. GE.Physics-informedneuralnetworkforultrasoundnondestruc-
234. MillevoiC,PasettoD,FerronatoM.APhysics-InformedNeural tivequantificationofsurfacebreakingcracks.JNondestructEval.
Network approach for compartmental epidemiological models. 2020;39:1–20.
PLOSComputBiol.2024;20:1–29. 254. ShuklaK,JagtapAD,BlackshireJL,SparkmanD,Karniadakis
235. ShaierS,RaissiM,SeshaiyerP.Data-drivenapproachesforpre- GE. A physics-informed neural network for quantifying the
dicting spread of infectious diseases through DINNs: Disease microstructural properties of polycrystalline nickel using ultra-
InformedNeuralNetworks.LettBiomath.2022;9(1):71–105. sounddata:Apromisingapproachforsolvinginverseproblems.
236. NguyenL,RaissiM,SeshaiyerP.Modeling,AnalysisandPhysics IEEESignalProcessMag.2021;39(1):68–77.
Informed Neural Network approaches for studying the dynam- 255. Mahmoudabadbozchelou M, Karniadakis GE, Jamali S. nn-
icsofCOVID-19involvinghuman-humanandhuman-pathogen PINNs: Non-newtonian physics-informed neural networks for
interaction.ComputMathBiophys.2022;10(1):1–17. complexfluidmodeling.SoftMatter.2022;18(1):172–85.
237. SchiassiE,DeFlorioM,D’ambrosioA,MortariD,FurfaroR. 256. ZhangE,DaoM,KarniadakisGE,SureshS.Analysesofinternal
Physics-informed neural networks and functional interpolation structuresanddefectsinmaterialsusingphysics-informedneural
fordata-drivenparametersdiscoveryofepidemiologicalcompart- networks.SciAdv.2022;8(7).
mentalmodels.Mathematics.2021;9(17):2069. 257. LiW,BazantMZ,ZhuJ.Aphysics-guidedneuralnetworkframe-
238. KharazmiE,CaiM,ZhengX,ZhangZ,LinG,KarniadakisGE. workforelasticplates:Comparisonofgoverningequations-based
Identifiability and predictability of integer-and fractional-order andenergy-basedapproaches.ComputMethodsApplMechEng.
epidemiologicalmodelsusingphysics-informedneuralnetworks. 2021;383:113933.
NatComputSci.2021;1(11):744–753. 258. BastekJ-H,KochmannDM.Physics-InformedNeuralNetworks
239. CaiS,GrayC,KarniadakisGE.Physics-InformedNeuralNet- forShellStructures.2022.arXiv:2207.14291.
worksEnhancedParticleTrackingVelocimetry:AnExamplefor 259. Goswami S, Anitescu C, Chakraborty S, Rabczuk T. Trans-
TurbulentJetFlow.IEEETransInstrumMeas.2024. fer learning enhanced physics informed neural network for
240. CalicchiaM,NiR,MittalR,SeoJ-H.Reconstructingthepressure phase-field modeling of fracture. Theor Appl Fract Mech.
fieldaroundanundulatingbodyusingaphysics-informedneural 2020;106:102447.
network.BulletAmPhysSoc.2022. 260. ZhangZ,GuGX.Physics-informeddeeplearningfordigitalmate-
241. JagtapAD,MaoZ,AdamsN,KarniadakisGE.Physics-informed rials.TheorApplMechLett.2021;11(1):100220.
neuralnetworksforinverseproblemsinsupersonicflows.2022 261. PantidisP,MobasherME.IntegratedFiniteElementNeuralNet-
arXiv:2202.11821. work (I-FENN) for non-local continuum damage mechanics.
242. KagV,SeshasayananK,GopinathV.Physics-informeddatabased 2022.arXiv:2207.09908.
neural networks for two-dimensional turbulence. Phys Fluids. 262. ZhangE,YinM,KarniadakisGE.Physics-informedneuralnet-
2022;34(5):055130. works for nonhomogeneous material identification in elasticity
243. Reyes B, Howard AA, Perdikaris P, Tartakovsky AM. Learn- imaging.2020.arXiv:2009.04525.
ingunknownphysicsofnon-Newtonianfluids.PhysRevFluids. 263. ZhangR,LiuY,SunH.Physics-informedmulti-LSTMnetworks
2021;6(7):073301. formetamodelingofnonlinearstructures.ComputMethodsAppl
244. RaissiM,WangZ,TriantafyllouMS,KarniadakisGE.Deeplearn- MechEng.2020;369:113226.
ingofvortex-inducedvibrations.JFluidMech.2019;861:119– 264. WaheedU,HaghighatE,AlkhalifahT,SongC,HaoQ.PINNeik:
137. Eikonalsolutionusingphysics-informedneuralnetworks.Com-
245. Di Leoni PC, Agasthya L, Buzzicotti M, Biferale L. Recon- putGeosci.2021;155:104833.
structing Rayleigh-Benard flows out of temperature-only mea- 265. RossZ,SmithJ,AzizzadenesheliK,MuirJ.HypoSVI:Hypocen-
surements using Physics-Informed Neural Networks. 2023. terinversionwithsteinvariationalinferenceandphysicsinformed
arXiv:2301.07769. neuralnetworks.In:AGUFallMeetingAbstracts,2021;vol.2021,
246. De Florio M, Schiassi E, Ganapol BD, Furfaro R. Physics- p.33–08.
informed neural networks for rarefied-gas dynamics: Thermal 266. Ihunde TA, Olorode O. Application of physics informed neu-
creep flow in the Bhatnagar-Gross-Krook approximation. Phys ral networks to compositional modeling. J Petroleum Sci Eng.
Fluids.2021;33(4):047110. 2022;211:110175.
247. ThakurS,RaissiM,ArdekaniAM.ViscoelasticNet:Aphysics 267. NazariLF,CamponogaraE,SemanLO.Physics-InformedNeural
informed neural network framework for stress discovery and NetworksforModelingWaterFlowsinaRiverChannel.IEEE
modelselection.2022.arXiv:2209.06972. TransArtifIntell.2022.
123

15 Page 40 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
268. Rasht-BeheshtM,HuberC,ShuklaK,KarniadakisGE.Physics- 288. HennighO,NarasimhanS,NabianMA,SubramaniamA,Tangsali
InformedNeuralNetworks(PINNs)forwavepropagationandfull K,FangZ,RietmannM,ByeonW,ChoudhryS.NVIDIASim-
waveforminversions.JGeophysRes:SolidEarth.2022;127(5). Net™:AnAI-acceleratedmulti-physicssimulationframework.
269. Zheng Q, Zeng L, Karniadakis GE. Physics-informed seman- In:InternationalConferenceonComputationalScience,Springer,
ticinpainting:Applicationtogeostatisticalmodeling.JComput 2021;p.447–461.
Phys.2020;419:109676. 289. Zhu Q, Liu Z, Yan J. Machine learning for metal additive
270. AbreuE,FlorindoJB.Astudyonafeedforwardneuralnetworkto manufacturing:predictingtemperatureandmeltpoolfluiddynam-
solvepartialdifferentialequationsinhyperbolic-transportprob- ics using physics-informed neural networks. Comput Mech.
lems. In: International Conference on Computational Science, 2021;67(2):619–35.
Springer,2021;p.398–411. 290. ZobeiryN,HumfeldKD.Aphysics-informedmachinelearning
271. AlmajidMM,Abu-Al-SaudMO.Predictionofporousmediafluid approach for solving heat transfer equation in advanced man-
flowusingphysicsinformedneuralnetworks.JPetrolSciEng. ufacturing and engineering applications. Eng Appl Artif Intell.
2022;208:109205. 2021;101:104232.
272. He Q, Barajas-Solano D, Tartakovsky G, Tartakovsky AM. 291. BoraA,DaiW,WilsonJP,BoytJC.Neuralnetworkmethodfor
Physics-informedneuralnetworksformultiphysicsdataassimila- solvingparabolictwo-temperaturemicroscaleheatconductionin
tionwithapplicationtosubsurfacetransport.AdvWaterResour. double-layeredthinfilmsexposedtoultrashort-pulsedlasers.Int
2020;141:103610. JHeatMassTransfer.2021;178:121616.
273. Tartakovsky AM, Marrero CO, Perdikaris P, Tartakovsky GD, 292. BoraA,DaiW,WilsonJ.P,BoytJ.C,SobolevS.L.Neuralnet-
Barajas-Solano D. Physics-informed deep neural networks for workmethodforsolvingnonlocaltwo-temperaturenanoscaleheat
learningparametersandconstitutiverelationshipsinsubsurface conductioningoldfilmsexposedtoultrashort-pulsedlasers.IntJ
flowproblems.WaterResourRes.2020;56(5):2019–026731. HeatMassTransfer.2022;190:122791.
274. Haghighat E, Amini D, Juanes R. Physics-informed neural 293. Niaki SA, Haghighat E, Campbell T, Poursartip A, Vaziri R.
network simulation of multiphase poroelasticity using stress- Physics-informedneuralnetworkformodellingthethermochemi-
split sequential training. Comput Methods Appl Mech Eng. calcuringprocessofcomposite-toolsystemsduringmanufacture.
2022;397:115141. ComputMethodsApplMechEng.2021;384:113959.
275. AminiD,HaghighatE,JuanesR.Inversemodelingofnonisother- 294. PatelRG,ManickamI,TraskNA,WoodMA,LeeM,TomasI,Cyr
mal multiphase poromechanics using physics-informed neural EC.Thermodynamicallyconsistentphysics-informedneuralnet-
networks.2022.arXiv:2209.03276. worksforhyperbolicsystems.JComputPhys.2022;449:110754.
276. AminiD,HaghighatE,JuanesR.Physics-informedneuralnet- 295. Mathews A, Francisquez M, Hughes JW, Hatch DR, Zhu
worksolutionofthermo-hydro-mechanical(THM)processesin B, Rogers BN. Uncovering turbulent plasma dynamics
porousmedia.2022.arXiv:2203.01514. via deep learning from partial observations. Phys Rev E.
277. Giampaolo F, De Rosa M, Qi P, Izzo S, Cuomo S. Physics- 2021;104(2):025205.
informed neural networks approach for 1D and 2D Gray-Scott 296. Stielow T, Scheel S. Reconstruction of nanoscale particles
systems.AdvModelSimulEngSci.2022;9(1):1–17. from single-shot wide-angle free-electron-laser diffraction pat-
278. NicodemusJ,KneiflJ,FehrJ,UngerB.Physics-informedneural terns with physics-informed neural networks. Phys Rev E.
networks-basedmodelpredictivecontrolformulti-linkmanipu- 2021;103(5):053312.
lators.IFAC-PapersOnLine.2022;55(20):331–6. 297. KovacsA,ExlL,KornellA,FischbacherJ,HovorkaM,Gusen-
279. XuP-F,HanC-B,ChengH-X,ChengC,GeT.Aphysics-informed bauer M, Breth L, Oezelt H, Praetorius D, Suess D, et al.
neural network for the prediction of unmanned surface vehicle Magnetostaticsandmicromagneticswithphysicsinformedneural
dynamics.JMarineSciEng.2022;10(2):148. networks.JMagnMagnMater.2022;548:168951.
280. AntoneloEA,CamponogaraE,SemanLO,SouzaER,Jordanou 298. Chen H, Katelhon E, Compton RG. Predicting voltammetry
JP,HubnerJF.Physics-informedneuralnetsforcontrolofdynam- using physics-informed neural networks. J Phys Chem Lett.
icalsystems.2021.arXiv:2104.02556. 2022;13(2):536–543.
281. Sanyal S, Roy K. RAMP-Net: A Robust Adaptive MPC 299. ShahK,StillerP,HoffmannN,CangiA.Physics-InformedNeural
for Quadrotors via Physics-informed Neural Network. 2022. NetworksasSolversfortheTime-DependentSchrödingerEqua-
arXiv:2209.09025. tion.2022.arXiv:2210.12522.
282. Gu W, Primatesta S, Rizzo A. Physics-informed Neural Net- 300. WangL,YanZ.Data-drivenroguewavesandparameterdiscovery
work for Quadrotor Dynamical Modeling. Robot Auton Syst. inthedefocusingnonlinearSchrödingerequationwithapotential
2024;171:104569. usingthePINNdeeplearning.PhysLettA.2021;404:127408.
283. Liu J, BorjaP, DellaSantinaC. Physics-Informed Neural Net- 301. PuJ,LiJ,ChenY.Solvinglocalizedwavesolutionsofthederiva-
workstoModelandControlRobots:ATheoreticalandExperi- tive nonlinear Schrödinger equation using an improved PINN
mentalInvestigation.AdvIntellSyst.2024;6(5):2300385. method.NonlinearDyn.2021;105(2):1723–39.
284. WangX,DabrowskiJJ,PinskierJ,LiowL,ViswanathanV,Scalzo 302. LiR,LeeE,LuoT.Physics-informedneuralnetworksforsolving
R,HowardD.PINN-Ray:APhysics-InformedNeuralNetwork multiscalemode-resolvedphononBoltzmanntransportequation.
toModelSoftRoboticFinRayFingers.2024.arXiv:2407.08222. MaterTodayPhys.2021;19:100429.
285. Progressive Learning for Physics-informed Neural Motion 303. Singh G, Kumar V, Buduru AB, Biswas S.K. Tracking an
Planning, author=Ni, Ruiqi and Qureshi, Ahmed H. 2023. untrackedspacedebrisafteraninelasticcollisionusingphysics
arXiv:2306.00616. informedneuralnetwork.SciReport.2024;14(1):3350.
286. MoZ,ShiR,DiX.Aphysics-informeddeeplearningparadigm 304. ChenY,LuL,KarniadakisGE,DalNegroL.Physics-informed
forcar-followingmodels.TranspRespartC:EmergingTechnol. neuralnetworksforinverseproblemsinnano-opticsandmetama-
2021;130:103240. terials.OpticsExpress.2020;28(8):11618–33.
287. KimT,LeeH,LeeW.PhysicsEmbeddedNeuralNetworkVehi- 305. Jiang X, Wang D, Fan Q, Zhang M, Lu C, Lau APT. Physics-
cleModelandApplicationsinRisk-AwareAutonomousDriving Informed Neural Network for Nonlinear Dynamics in Fiber
UsingLatentFeatures.In:2022IEEE/RSJInternationalConfer- Optics.LaserPhotonicsRev.2022;16(9):2100483.
enceonIntelligentRobotsandSystems(IROS),IEEE.2022;p. 306. WuG-Z,FangY,WangY-Y,WuG-C,DaiC-Q.Predictingthe
4182–4189. dynamicprocessandmodelparametersofthevectoropticalsoli-
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 41 of 43 15
tonsinbirefringentfibersviathemodifiedPINN.Chaos,Solitons 326. HouQ,DuH,SunZ,WangJ,WangX,WeiJ.PINN-CDR:A
Fractals.2021;152:111393. neural network-based simulation tool for convection-diffusion-
307. Häger C, Pfister HD. Physics-based deep learning for fiber- reactionsystems.IntJIntellSyst.2023;2023(1):2973249.
opticcommunicationsystems.IEEEJSelectedAreasCommun. 327. SunZ,DuH,MiaoC,HouQ.Aphysics-informedneuralnetwork
2020;39(1):280–294. basedsimulationtoolforreactingflowwithmulticomponentreac-
308. CamporealeE,WilkieGJ,DrozdovAY,BortnikJ.Data-driven tants.AdvEngSoftw.2023;185:103525.
discoveryofFokker-PlanckequationfortheEarth’sradiationbelts 328. Choi S, Jung I, Kim H, Na J, Lee JM. Physics-informed deep
electronsusingPhysics-InformedNeuralNetworks2022. learningfordata-drivensolutionsofcomputationalfluiddynam-
309. SchiassiE,D’AmbrosioA,DrozdK,CurtiF,FurfaroR.Physics- ics.KoreanJChemEng.2022;39(3):515–528.
informed neural networks for optimal planar orbit transfers. J 329. PatelR,BhartiyaS,GudiR.Optimaltemperaturetrajectoryfor
SpacecraftRockets.2022;59(3):834–49. tubularreactorusingphysicsinformedneuralnetworks.JProcess
310. Furfaro R, D’Ambrosio A, Schiassi E, Scorsoglio A. Physics- Control.2023;128:103003.
InformedNeuralNetworksforClosed-LoopGuidanceandCon- 330. Ngo SI, Lim Y-I. Forward Physics-Informed Neural Net-
trol in Aerospace Systems. In: AIAA SCITECH 2022 Forum, works Suitable for Multiple Operating Conditions of Catalytic
2022;p.0361. CO2 Methanation Isothermal Fixed-Bed. IFAC-PapersOnLine.
311. D’AmbrosioA,SchiassiE,CurtiF,FurfaroR.Physics-Informed 2022;55(7):429–34.
NeuralNetworksAppliedtoaSeriesofConstrainedSpaceGuid- 331. Elhareef MH, Wu Z. Physics-informed neural network method
ance Problems. In: 31st AAS/AIAA Space Flight Mechanics and application to nuclear reactor calculations: A pilot study.
Meeting2021. NuclearSciEng.2023;197(4):601–22.
312. MartinJ,SchaubH.Reinforcementlearningandorbit-discovery 332. Schiassi E, De Florio M, Ganapol BD, Picca P, Furfaro
enhancedbysmall-bodyphysics-informedneuralnetworkgravity R. Physics-informed neural networks for the point kinetics
models.In:AIAASCITECH2022Forum,2022;p.2272. equations for nuclear reactor dynamics. Ann Nuclear Energy.
313. MartinJ,SchaubH.Physics-informedneuralnetworksforgravity 2022;167:108833.
fieldmodelingoftheEarthandMoon.CelestMechDynAstron. 333. Liu Y-T, Wu C-Y, Chen T, Yao Y. Multi-fidelity surrogate
2022;134(2):1–28. modeling for chemical processes with physics-informed neural
314. Martin JR, Schaub H. Periodic Orbit Discovery Enhanced by networks.In:ComputerAidedChemicalEngineering,Elsevier,
Physics-Informed Neural Networks. In: 2022 Astrodynamics 2023,vol.52,p.57–63.
Specialist Conference, Charlotte, North Carolina, 2022; p. 7– 334. AntonelloF,BuongiornoJ,ZioE.Physicsinformedneuralnet-
11. worksforsurrogatemodelingofaccidentalscenariosinnuclear
315. MishraS,MolinaroR.Physicsinformedneuralnetworksforsim- powerplants.NuclearEngTechnol.2023;55(9):3409–16.
ulatingradiativetransfer.JQuantSpectroscRadiativeTransfer. 335. Liu K, Luo K, Cheng Y, Liu A, Li H, Fan J, Balachan-
2021;270:107705. dar S. Surrogate modeling of parameterized multi-dimensional
316. Wu Z, Wang H, He C, Zhang B, Xu T, Chen Q. The appli- premixed combustion with physics-informed neural networks
cation of physics-informed machine learning in multiphysics for rapid exploration of design space. Combustion Flame.
modeling in chemical engineering. Industrial Eng Chem Res. 2023;258:113094.
2023;62(44):18178–204. 336. ZouT,YajimaT,KawajiriY.Aparameterestimationmethodfor
317. ZhuL-T,ChenX-Z,OuyangB,YanW-C,LeiH,ChenZ,LuoZ- chromatographicseparationprocessbasedonphysics-informed
H.Reviewofmachinelearningforhydrodynamics,transport,and neuralnetwork.JChromatographyA.2024;465077.
reactionsinmultiphaseflowsandreactors.IndustrialEngChem 337. Söderström P. Physics-Informed Neural Networks for Liquid
Res.2022;61(28):9901–9949. Chromatography2022.
318. Batuwatta-Gamage CP, Rathnayaka C, Karunasena HC, Jeong 338. Tang S-Y, Yuan Y-H, Chen Y-C, Yao S-J, Wang Y, Lin D-
H,KarimA,GuYT.Anovelphysics-informedneuralnetworks Q. Physics-informed neural networks to solve lumped kinetic
approach(PINN-MT)tosolvemasstransferinplantcellsduring model for chromatography process. J Chromatography A.
drying.BiosystEng.2023;230:219–241. 2023;1708:464346.
319. XuanW,LouH,FuS,ZhangZ,DingN.Physics-informeddeep 339. LiH,SpelmanD,SansaloneJ.UnitOperationandProcessMod-
learning method for the refrigerant filling mass flow metering. elingwithPhysics-InformedMachineLearning.JEnvironEng.
FlowMeasInstrum.2023;93:102418. 2024;150(4):04024002.
320. JiW,QiuW,ShiZ,PanS,DengS.Stiff-pinn:Physics-informed 340. BaiY,ChaoluT,BiligeS.Theapplicationofimprovedphysics-
neural network for stiff chemical kinetics. J Phys Chem A. informedneuralnetwork(IPINN)methodinfinance.Nonlinear
2021;125(36):8098–106. Dyn.2022;107(4):3655–67.
321. De Florio M, Schiassi E, Furfaro R. Physics-informed neural 341. FangZ,ZhanJ.Deepphysicalinformedneuralnetworksformeta-
networksandfunctionalinterpolationforstiffchemicalkinetics. materialdesign.IEEEAccess.2019;8:24506–13.
Chaos:AnInterdisciplinaryJNonlinearSci.2022;32(6):063107. 342. Islam M, Thakur MSH, Mojumder S, Hasan MN. Extrac-
322. WengY,ZhouD.Multiscalephysics-informedneuralnetworks tion of material properties through multi-fidelity deep learn-
forstiffchemicalkinetics.JPhysChemA.2022;126(45):8534– ing from molecular dynamics simulation. Comput Mater Sci.
43. 2021;188:110187.
323. NgoSI,LimY-I.Solutionandparameteridentificationofafixed- 343. Misyris GS, Venzke A, Chatzivasileiadis S. Physics-informed
bedreactormodelforcatalyticCO2methanationusingphysics- neural networks for power systems. In: 2020 IEEE Power &
informedneuralnetworks.Catalysts.2021;11(11):1304. EnergySocietyGeneralMeeting(PESGM),IEEE,2020;p.1–
324. CohenB,BeykalB,BollasGM.Data-drivenDiscoveryofReac- 5.
tion Kinetic Models in Dynamic Plug Flow Reactors using 344. ParkJ,ParkJ.Physics-inducedgraphneuralnetwork:Anapplica-
SymbolicRegression.In:ComputerAidedChemicalEngineer- tiontowind-farmpowerestimation.Energy.2019;187:115883.
ingvol.53,pp.2947–2952.Elsevier,2024. 345. Dabrowski JJ,PagendamDE,HiltonJ,SandersonC,MacKin-
325. BibeauV,BoffitoDC,BlaisB.Physics-informedNeuralNetwork layD,HustonC,BoltA,KuhnertP.BayesianPhysicsInformed
topredictkineticsofbiodieselproductioninmicrowavereactors. Neural Networks for Data Assimilation and Spatio-Temporal
ChemEngProcess-ProcessIntensif.2024;196:109652. ModellingofWildfires.2022.arXiv:2212.00970.
123

15 Page 42 of 43 MachineLearningforComputationalScienceandEngineering(2025)1: 15
346. Gao H, Sun L, Wang J-X. PhyGeoNet: Physics-informed 366. ZouZ,MengT,ChenP,DarbonJ,KarniadakisGE.Leveraging
geometry-adaptive convolutional neural networks for solving ViscousHamilton-JacobiPDEsforUncertaintyQuantificationin
parameterizedsteady-statePDEsonirregulardomain.JComput ScientificMachineLearning.SIAM/ASAJUncertaintyQuantif.
Phys.2021;428:110079. 2024;12(4):1165–1191.
347. LiuL,LiuS,YongH,XiongF,YuT.DiscontinuityComputing 367. Zou Z, Karniadakis GE. L-HYDRA: multi-head physics-
withPhysics-InformedNeuralNetwork.2022.arXiv:2206.03864. informedneuralnetworks.2023.arXiv:2301.02152.
348. TsengY-H,LinT-S,HuW-F,LaiM-C.Acusp-capturingpinnfor 368. RezendeD,MohamedS.Variationalinferencewithnormalizing
ellipticinterfaceproblems.JComputPhys.2023;491:112359. flows.In:InternationalConferenceonMachineLearning,PMLR.
349. KadeethumT,JørgensenTM,NickHM.Physics-informedneural 2015;p.1530–1538.
networksforsolvingnonlineardiffusivityandBiot’sequations. 369. Meng X. Variational inference in neural functional prior using
PLOSOne.2020;15(5):0232683. normalizingflows:applicationtodifferentialequationandoper-
350. Abdar M, Pourpanah F, Hussain S, Rezazadegan D, Liu L, atorlearningproblems.ApplMathMech.2023;44(7):1111–24.
GhavamzadehM,FieguthP,CaoX,KhosraviA,AcharyaUR, 370. YinM,ZouZ,ZhangE,CavinatoC,HumphreyJD,Karniadakis
etal.Areviewofuncertaintyquantificationindeeplearning:Tech- GE.Agenerativemodelingframeworkforinferringfamiliesof
niques, applications and challenges. Inf Fusion. 2021;76:243– biomechanicalconstitutivelawsindata-sparseregimes.JMech
97. PhysSolids.2023;181:105424.
351. PsarosAF,MengX,ZouZ,GuoL,KarniadakisGE.Uncertainty 371. Zou Z, Meng X, Karniadakis GE. Uncertainty quantifica-
quantificationinscientificmachinelearning:Methods,metrics, tion for noisy inputs-outputs in physics-informed neural net-
andcomparisons.JComputPhys.2023;477:111902. worksandneuraloperators.ComputMethodsApplMechEng.
352. YangL,MengX,KarniadakisGE.B-PINNs:Bayesianphysics- 2025;433:117479.
informedneuralnetworksforforwardandinversePDEproblems 372. ZhangZ,ZouZ,KuhlE,KarniadakisGE.Discoveringareaction–
withnoisydata.JComputPhys.2021;425:109913. diffusion model for Alzheimer’s disease by combining PINNs
353. Zou Z, Meng X, Psaros AF, Karniadakis GE. NeuralUQ: A with symbolic regression. Comput Methods Appl Mech Eng.
comprehensive library for uncertainty quantification in neural 2024;419:116647.
differentialequationsandoperators.SIAMRev.2024;66(1):161– 373. ChenZ,LiuY,SunH.Physics-informedlearningofgoverning
190. equationsfromscarcedata.NatCommun.2021;12(1):6136.
354. MengX,YangL,MaoZ,ÁguilaFerrandisJ,KarniadakisGE. 374. Chen Z, Xiu D. On generalized residual network for deep
Learningfunctionalpriorsandposteriorsfromdataandphysics. learning of unknown dynamical systems. J Comput Phys.
JComputPhys.2022;457:111073. 2021;438:110362.
355. ZouZ,MengX,KarniadakisGE.Correctingmodelmisspecifi- 375. EbersMR,SteeleKM,KutzJN.DiscrepancyModelingFrame-
cationinphysics-informedneuralnetworks(PINNs).JComput work:LearningMissingPhysics,ModelingSystematicResiduals,
Phys.2024;505:112918. andDisambiguatingbetweenDeterministicandRandomEffects.
356. GalY,GhahramaniZ.DropoutasaBayesianapproximation:Rep- SIAMJApplDynSyst.2024;23(1):440–69.
resenting model uncertainty in deep learning. In: International 376. Meng T, Zou Z, Darbon J, Karniadakis GE. HJ-sampler: A
ConferenceonMachineLearning,PMLR,2016;p.1050–1059. Bayesian sampler for inverse problems of a stochastic process
357. Zhang D, Lu L, Guo L, Karniadakis GE. Quantifying total byleveragingHamilton-JacobiPDEsandscore-basedgenerative
uncertainty in physics-informed neural networks for solving models.2024.arXiv:2409.09614.
forward and inverse stochastic problems. J Comput Phys. 377. Linka K, Schäfer A, Meng X, Zou Z, Karniadakis GE, Kuhl
2019;397:108850. E. Bayesian Physics Informed Neural Networks for real-world
358. Gao Y, Ng MK. Wassersteingenerative adversarial uncertainty nonlineardynamicalsystems.ComputMethodsApplMechEng.
quantification in physics-informed neural networks. J Comput 2022;402:115346.
Phys.2022;463:111270. 378. Oszkinat C, Luczak SE, Rosen I. Uncertainty quantification in
359. DawA,MarufM,KarpatneA.PID-GAN:AGANFramework estimatingbloodalcoholconcentrationfromtransdermalalcohol
basedonaPhysics-informedDiscriminatorforUncertaintyQuan- levelwithphysics-informedneuralnetworks.IEEETransNeural
tificationwithPhysics.In:Proceedingsofthe27thACMSIGKDD NetwLearnSyst.2022;34(10):8094–101.
ConferenceonKnowledgeDiscovery&DataMining,2021;p. 379. MoZ,FuY,XuD,DiX.TrafficFlowGAN:Physics-informedflow
237–247. basedgenerativeadversarialnetworkforuncertaintyquantifica-
360. JiangX,WangX,WenZ,LiE,WangH.Practicaluncertainty tion. In: Joint European Conference on Machine Learning and
quantificationforspace-dependentinverseheatconductionprob- KnowledgeDiscoveryinDatabases,Springer,2022;p.323–339.
lemviaensemblephysics-informedneuralnetworks.IntCommun 380. ShinY,DarbonJ,KarniadakisGE.Ontheconvergenceofphysics
HeatMassTransfer.2023;147:106940. informed neural networks for linear second-order elliptic and
361. SoibamJ,AslanidouI,KyprianidisK,FdhilaRB.Inverseflow parabolictypePDEs.2020.arXiv:2004.01806.
predictionusingensemblePINNsanduncertaintyquantification. 381. MishraS,MolinaroR.Estimatesonthegeneralizationerrorof
IntJHeatMassTransfer.2024;226:125480. physics-informedneuralnetworksforapproximatingPDEs.IMA
362. Yang M, Foster JT. Multi-output physics-informed neural net- JNumerAnal.2023;43(1):1–43.
worksforforwardandinversePDEproblemswithuncertainties. 382. WuS,ZhuA,TangY,LuB.Convergenceofphysics-informed
ComputMethodsApplMechEng.2022;402:115041. neuralnetworksappliedtolinearsecond-orderellipticinterface
363. DeFlorioM,ZouZ,SchiavazziDE,KarniadakisGE.Quantifi- problems.2022.arXiv:2203.03407.
cationoftotaluncertaintyinthephysics-informedreconstruction 383. QianY,ZhangY,HuangY,DongS.Erroranalysisofphysics-
ofCVSim-6physiology.2024.arXiv:2408.07201. informedneuralnetworksforapproximatingdynamicPDEsof
364. LinG,WangY,ZhangZ.Multi-variancereplicaexchangeSGM- secondorderintime.2023.arXiv:2303.12245.
CMC for inverse and forward problems via Bayesian PINN. J 384. HuR,LinQ,RaydanA,TangS.Higher-ordererrorestimatesfor
ComputPhys.2022;460:111173. physics-informed neural networks approximating the primitive
365. LütjensB,CrawfordCH,VeilletteM,NewmanD.PCE-PINNs: equations.PartialDifferEquAppl.2023;4(4):34.
Physics-informedneuralnetworksforuncertaintypropagationin
oceanmodeling.2021.arXiv:2105.02939.
123

MachineLearningforComputationalScienceandEngineering(2025)1: 15 Page 43 of 43 15
385. ShinY,ZhangZ,KarniadakisGE.Errorestimatesofresidualmin- 403. Xu K, Darve E. ADCME: Learning spatially-varying physical
imizationusingneuralnetworksforlinearPDEs.JMachLearn fieldsusingdeepneuralnetworks.2020.arXiv:2011.11955.
ModelComput.2023;4(4). 404. McClenny LD, Haile MA, Braga-Neto UM. TensorDiffEq:
386. MishraS,MolinaroR.Estimatesonthegeneralizationerrorof Scalable Multi-GPU Forward and Inverse Solvers for Physics
physics-informedneuralnetworksforapproximatingaclassof InformedNeuralNetworks.2021.arXiv:2103.16034.
inverseproblemsforPDEs.IMAJNumerAnal.2022;42(2):981– 405. Araz JY, Criado JC, Spannowsky M. Elvet–a neural network-
1022. baseddifferentialequationandvariationalproblemsolver.2021.
387. MüllerJ,ZeinhoferM.ErrorestimatesforthedeepRitzmethod arXiv:2103.14575.
withboundarypenalty.In:MathematicalandScientificMachine 406. Peng W, Zhang J, Zhou W, Zhao X, Yao W, Chen X.
Learning,PMLR,2022;p.215–230. IDRLnet: A physics-informed neural network library. 2021.
388. Biswas A, Tian J, Ulusoy S. Error estimates for deep learn- arXiv:2107.04320.
ing methods in fluid dynamics. Numerische Mathematik. 407. PedroJB,MaroñasJ,ParedesR.Solvingpartialdifferentialequa-
2022;151(3):753–77. tionswithneuralnetworks.2019.arXiv:1912.04737.
389. DoumècheN,BiauG,BoyerC.Convergenceanderroranalysis 408. McClenny L, Braga-Neto U. Self-adaptive physics-informed
ofPINNs.2023.arXiv:2305.01240. neural networks using a soft attention mechanism. 2020.
390. Jacot A, Gabriel F, Hongler C. Neural Tangent Kernel: Con- arXiv:2009.04544.
vergenceandgeneralizationinneuralnetworks.AdvNeuralInf 409. Frostig R, Johnson MJ, Leary C. Compiling machine learning
ProcessSyst.2018;31. programsviahigh-leveltracing.SystMachLearn.2018;4(9).
391. Wang S, Yu X, Perdikaris P. When and why PINNs fail to 410. Cho J, Nam S, Yang H, Yun S-B, Hong Y, Park E. Separa-
train: A neural tangent kernel perspective. J Comput Phys. blePhysics-InformedNeuralNetworks.2023.arXiv:2306.15969
2022;449:110768. [cs.LG].
392. Tishby N, Pereira FC, Bialek W. The information bottleneck 411. Wang Y, Lai C-Y. Multi-stage Neural Networks: Function
method.2000.arXiv:0004057. Approximator of Machine Precision. 2023. arXiv:2307.08934
393. TishbyN,ZaslavskyN.Deeplearningandtheinformationbot- [cs.LG].
tleneckprinciple.In:2015IEEEInformationTheoryWorkshop 412. LuL,JinP,KarniadakisG.E.DeepOnet:Learningnonlinearoper-
(ITW),IEEE,2015;p.1–5. atorsforidentifyingdifferentialequationsbasedontheuniversal
394. Shwartz-ZivR,TishbyN.Openingtheblackboxofdeepneural approximationtheoremofoperators.2019arXiv:1910.03193.
networksviainformation.2017.arXiv:1703.00810. 413. RaissiM,YazdaniA,KarniadakisGE.HiddenFluidMechanics:
395. GoldfeldZ,PolyanskiyY.Theinformationbottleneckproblem ANavier-StokesInformedDeepLearningFrameworkforAssim-
anditsapplicationsinmachinelearning.IEEEJSelectedAreas ilatingFlowVisualizationData.2018.arXiv:1808.04327[cs.CE].
InfTheory.2020;1(1):19–38. 414. Kharazmi E, Zhang Z, Karniadakis GE. Variational Physics-
396. Shwartz-ZivR.Informationflowindeepneuralnetworks.2022. InformedNeuralNetworksForSolvingPartialDifferentialEqua-
arXiv:2202.06749. tions.2019.arXiv:1912.00873[cs.NE].
397. ZubovK,McCarthyZ,MaY,CalistoF,PagliarinoV,Azeglio 415. WangS,YuX,PerdikarisP.WhenandwhyPINNsfailtotrain:
S, Bottero L, Luján E, Sulzer V, Bharambe A, et al. Neu- A neural tangent kernel perspective. 2020. arXiv:2007.14527
ralPDE:Automatingphysics-informedneuralnetworks(PINNs) [cs.LG].
witherrorapproximations.2021.arXiv:2107.09443. 416. WangS,WangH,PerdikarisP.OntheeigenvectorbiasofFourier
398. Modulus Contributors: NVIDIA Modulus: An Open-source featurenetworks:Fromregressiontosolvingmulti-scalePDEs
FrameworkforPhysics-basedDeepLearninginScienceandEngi- withphysics-informedneuralnetworks.2020.arXiv:2012.10047.
neering.https://github.com/NVIDIA/modulus 417. MojganiR,BalajewiczM,HassanzadehP.Kolmogorovn–width
399. ChenF,SondakD,ProtopapasP,MattheakisM,LiuS,Agarwal andLagrangianphysics-informedneuralnetworks:Acausality-
D,DiGiovanniM.NeuroDiffEq:APythonpackageforsolving conformingmanifoldforconvection-dominatedPDEs.Computer
differentialequationswithneuralnetworks.JOpenSourceSoftw. MethodsinAppliedMechanicsandEngineering[Internet].2023
2020;5(46):1931. Feb;404:115810. Available from: https://dx.doi.org/10.1016/j.
400. TanyuDN,NingJ,FreudenbergT,HeilenkötterN,Rademacher cma.2022.115810.
A,IbenU,MaassP.Deeplearningmethodsforpartialdifferential
equationsandrelatedparameteridentificationproblems.Inverse
Probl.2023;39(10):103001.
Publisher’sNote SpringerNatureremainsneutralwithregardtojuris-
401. HaghighatE,JuanesR.SciANN:AKeras/Tensorflowwrapper
dictionalclaimsinpublishedmapsandinstitutionalaffiliations.
forscientificcomputationsandphysics-informeddeeplearning
using artificial neural networks. Comput Methods Appl Mech
SpringerNatureoritslicensor(e.g.asocietyorotherpartner)holds
Eng.2021;373:113552.
exclusiverightstothisarticleunderapublishingagreementwiththe
402. Koryagin A, Khudorozkov R, Tsimfer S. PyDEns: A Python
author(s)orotherrightsholder(s);authorself-archivingoftheaccepted
framework for solving differential equations with neural net-
manuscriptversionofthisarticleissolelygovernedbythetermsofsuch
works.2019.arXiv:1909.11544.
publishingagreementandapplicablelaw.
123