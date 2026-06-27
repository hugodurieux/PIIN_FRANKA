Applied Energy 381 (2025) 125169
ContentslistsavailableatScienceDirect
Applied Energy
journalhomepage:www.elsevier.com/locate/apenergy
A review of physics-informed machine learning for building
energy modeling
Zhihao Maa, Gang Jianga, Yuqing Hub, Jianli Chenc,*
aDepartmentofCivilandEnvironmentalEngineering,TheUniversityofUtah,SaltLakeCity,UT84102,USA
bDepartmentofArchitecturalEngineering,ThePennsylvaniaStateUniversity,UniversityPark,PA16802,USA
cCollegeofCivilEngineering,TongjiUniversity,Shanghai,China
H I G H L I G H T S
•AcomprehensivereviewofPhysics-InformedMachineLearning(PIML)methodsforBuildingEnergyModeling(BEM).
•PresentanddiscussdifferentmethodologiesofPIMLapplicationonBEM.
•DiscussthechallengesandpotentialsolutionsofPIMLapplicationinBEM.
A R T I C L E I N F O A B S T R A C T
Keywords: Buildingenergymodeling(BEM)referstocomputationalmodelingofbuildingenergyuseandindoordynamics.
Physics-informedmachinelearning Asacriticalcomponentinsustainableandresilientbuildingdevelopment,BEMisfundamentaltosupporta
Buildingenergymodeling diverse spectrum of applications, including but not limited to sustainable building design and retrofitting,
Physics-constraintlearning
buildingresilienceanalysis,smartbuildingcontrol.Currently,twomainapproaches,i.e.,physics-basedanddata-
Physics-embeddedalgorithmstructure
driven modeling, exist within BEM. Despite significant advancements of machine learning (ML) and deep
learning(DL)algorithmsinrecentyears,severalchallengesremaintoapplythesedata-drivenapproachesin
BEM,includingthenecessityofobtainingsufficientandhigh-qualitytrainingdatainalgorithmdevelopment,
unreliableandphysicallyinfeasiblepredictions,andlimitedalgorithminterpretabilityandgeneralityinappli-
cations.ThesecontributetodistrustandimpedethewidespreadadoptionofthesealgorithmsinBEMpractices.
To overcome these challenges, this work provides a comprehensive overview of Physics-Informed Machine
Learning(PIML),anovelmodelingapproachthatencodesphysicsprinciplesandusefulphysicalinformationinto
cutting-edgeMLalgorithms.Thisapproachisdesignedforadvancedbuildingenergymodelingwithenhanced
robustnessandinterpretability.Specifically,existingPIMLmethodsforBEMaresummarizedandcategorized
into different paradigms to integrate physics into ML models, including physics-informed inputs, physics-
informed loss functions, physics-informed architectural design, and physics-informed ensemble models. The
challenges,includingtheeffectiveintegrationofpriorphysicalknowledgeinmodelingandtheevaluationof
developedPIMLmethods,inthedevelopmentofPIMLforBEMarethendiscussed.Thisreviewoutlinesextensive
existingresearchworksandfuturepotentialresearchdirectionstoshedlightonthebroaderapplicationofPIML
tosupportBEMpractice.
variousphysicsdomains,includingbutnotlimitedtoheattransfer[3],
fluiddynamics[4],thermaldynamics[5],electricalandcontrolengi-
1. Introduction neering [6–8]. Modeling and forecasting the dynamics of such multi-
physics systems, governed by complex physical laws, remain an open
Building Energy Modeling (BEM) is fundamental to support sus- scientific challenge to the computational modeling and simulation
tainable and resilient building development and counteract emerging community[9].Toaddressthis,thepioneeringcomputationalprogram
globalclimatechange[1,2].However,accuratemodelingofbuildingsis BIRS for modeling building dynamics was developed in the 1960s to
non-trivial,consideringtheirnatureasmultiphysicssystemsspanning
* Correspondingauthor.
E-mailaddress:jianlichen@tongji.edu.cn(J.Chen).
https://doi.org/10.1016/j.apenergy.2024.125169
Received26August2024;Receivedinrevisedform6November2024;Accepted14December2024
Available online 21 December 2024
0306-2619/© 2024 Elsevier Ltd. All rights are reserved, including those for text and data mining, AI training, and similar technologies.

Z.Maetal. Applied Energy 381 (2025) 125169
Nomenclature KNR K-NeighborsRegression
LLM LargeLanguageModel
ACR AirChangeRate LR LinearRegression
AI ArtificialIntelligence LSTM LongShort-TermMemory
ANN ArtificialNeuralNetwork MAE MeanAbsoluteError
ARIMA AutoregressiveIntegratedMovingAverage MAPE MeanAbsolutePercentageError
ARMAX Autoregressive-Moving-AveragewithExogenousInputs ML MachineLearning
ASHRAE AmericanSocietyofHeating,RefrigeratingandAir- MLR MultipleLinearRegression
ConditioningEngineers MMD MaximumMeanDifference
BEM BuildingEnergyModeling MSE MeanSquareError
CDE ControlledDifferentialEquations NODE NeuralOrdinaryDifferentialEquations
CFD ComputationalFluidDynamics PDE PartialDifferentialEquation
CV-RMSE CoefficientofVariationofRootMeanSquareError PIML Physics-InformedMachineLearning
DOE DepartmentofEnergy PINN Physics-InformedNeuralNetwork
DL DeepLearning R2 Thecoefficientofdetermination
GAN GenerativeAdversarialNetwork ResNet ResidualNetworks
GAT GraphAttentionNetwork RC Resistance-Capacitance
GCN GraphConvolutionalNetwork RMSE RootMeanSquareError
GMM GaussianMixtureModel RNN RecurrentNeuralNetwork
GNN GraphNeuralNetwork SAC SoftActor-Critic
GPR GaussianProcessRegression SDA Sub-space-basedDomainAdaptation
GRU GatedRecurrentUnit SSS Sub-keywordSynonymSearch
HVAC Heating,Ventilation,andAirConditioning ST-GCN Spatio-TemporalGraphConvolutionalNetwork
IDA-ICE IndoorClimateandEnergySimulationSoftware SVM SupportVectorMachine
IoT InternetofThings TOWT Time-of-WeekandTemperatureModel
ISO InternationalOrganizationforStandardization TR TreeRegression
KAN Kolmogorov-ArnoldNetwork
facilitatedesignofHeating,Ventilation,andAir-conditioning(HVAC) ML models are not a panacea, particularly in multiphysics-related or
systems.Inthepastthreedecades,severalwell-developedopen-source sophisticated engineering fields[42] considering its limitations in (1)
or commercial building energy simulation programs [10–12], such as thedemandingrequirementsformassiveandhigh-qualitytrainingdata
DOE-2,[13]BLAST[14],EnergyPlus[15],Dymola[16],andTRNSYS in effectivemodel development; (2) the black-boxnature ofML algo-
[17],havebeenextensivelyusedforbuildingenergyprediction,retro- rithms,associatedwithunreliablyorphysicallyinconsistentpredictions
fitting,andbuilding-renewableenergyintegration,etc.[18].However, inpractice;(3)thelackofpredictabilityinout-of-sample(extrapolation)
allthesetoolsrequiredetailedinputsofbuildingparametersandsolving scenarios, especially when training and testing data originate from
complex physics governing equations, which is both time-consuming heterogeneous hypothesis spaces. Thus, while arising as a promising
and labor-intensive, especially considering many required model in- alternative to physics-based modeling, data-driven modeling of build-
puts are not easily available in building modeling practice or the ingsalsocomeswithitsownsignificantchallenges.
computationalresourcesarelimited.Inadditiontobuildingparameters, Thisdilemmabetweenusingphysics-basedmodelsanddata-driven
obtainingaccurateoperationalconditionsisalsochallenging.Although models for modeling multiphysics systems has not been addressed
certain physics-basedmodelsarevalidatedaccordingtoASHRAE140 until the emergence of theory-guided data science paradigm, as
[19] and ISO 52016-1 [20] standards, the pre-designed operational conceptualizedbyKarpatneetal.[42]in2017.In2019,Raissietal.[43]
conditionswithinthesestandardsareoftennotfullyrepresentativeof published another pioneering work that introduced neural networks
real-worldscenarios.Therefore,thecriticalquestionarises:isitpossible designedtosolvesupervisedlearningtaskswhileadheringtophysical
to bypass these sophisticated physics rules and practical constraints, laws described by general nonlinear Partial Differential Equations
while still reliably and accurately model buildings as complex multi- (PDEs).ThesenetworkswerenamedPhysics-informedNeuralNetworks
physicssystems? (PINNs)or,morebroadly,Physics-informedMachineLearning(PIML).
The answer to this question has emerged with the dramatic ad- In his 1997 textbook Machine Learning, computer scientist Tom M.
vancements in Machine Learning (ML) and Artificial Intelligence (AI) Mitchell provided a widely quoted and formal definition of ML: “A
algorithmsoverthelasttwodecades[21,22].MLreliesonmathematical computer program is said to learn from experience E with respect to
models to directly capture complex relationships between inputs and someclassoftasksTandperformancemeasurePifitsperformanceat
outputs.TheadoptionofMLalgorithmsforBEMbeganinthelate1990s tasks in T, as measured by P, improves with experience E" [44]. The
and has become increasingly prevalent due to the extensive data distinctiveaspectofPIMListhattheexperienceElearnedbythecom-
generatedbybuildingautomationsystemsandInternetofThings(IoT) puter program comes not only from data, but also from additional
infrastructuresinbuildings[12,23,24],alongwiththeadvancementsof knowledge described by physical laws. Moreover, the scope of PIML
computingalgorithms.NumerouslinearandnonlinearMLalgorithms, extends beyond merely integrating neural networks with PDEs. It en-
including autoregressivemethods [25,26], Multiple LinearRegression compassesabroaderrangeofapplicationsbyintegratingdiversephysics
(MLR)[27,28],SupportVectorMachine(SVM)[29,30],havedemon- principlesintovariousMLalgorithms.ThisexpansionallowsdiverseML
stratedsignificantpotentialinaccuratelymodelingbuildingenergyuse. techniquestobeinformedbyrelevantphysicallawsintheirapplication.
Othermethodssuchasdeeplearningnetworks[31,32],tree-basedal- PIML has been developed as a novel solution to further empower ML
gorithms[33–35],Bayesiannetworks[36,37],LargeLanguageModels applicationsinscientificandengineeringdomains,particularlywhere
(LLM)[38,39],andensemblelearning[40,41]alsoshowconsiderable understandingandadherencetophysicallawsarecrucial.
promise.However,despitethestrongcapabilitiesofthesealgorithms, In recent years, PIML has been rapidly explored and has found
2

Z.Maetal. Applied Energy 381 (2025) 125169
fruitful applications in a variety of engineering scenarios, including Observationalbiasesinvolveusingphysics-basedsimulateddataordata
systemreliabilityanalysis[45],civilengineering[46],fatiguelifepre- augmentationtechniquesthatmodifyparametersinphysicalequations
diction[47],metaladditivemanufacturing[48],powersystems[49], asinputs,allowingnetworkstolearnfunctionsandoperatorsthatreflect
structuralhealthmonitoring[50],tribology[51],fluiddynamics[52], the physical principles inherent in data. Inductive biases incorporate
heattransfer[53],andclimateprediction[54].PIMLhasemergedasa priorknowledgethroughcustomizedmodelarchitectures,ensuringthat
powerfulalternativemodelingmethodforimprovingbothaccuracyand predictions implicitly satisfy physical laws, which are typically
interpretability of model predictions in engineering applications. Kar- expressed as mathematical constraints. Learning biases involve the
niadakisetal.[55]providedacomprehensivereviewofPIML,catego- introductionofregulatedlossfunctionstoguidethetrainingphaseofan
rizing methods into observational, inductive, and learning biases to ML model towards physics-consistent solutions. In addition to the
guide the learning process towards physically consistent solutions. aforementioned methods, Meng et al. [56] highlighted the fusion of
Fig.1. ClassificationofPIMLapplicationonBEM.
3

Z.Maetal. Applied Energy 381 (2025) 125169
deeplearningwithphysics-basedmodulesasanotherPIMLapproach,i. summarizesthefindingsandhighlightsfuturedirectionsandchallenges.
e., constructing physics-based and data-driven models independently Finally,Section8concludesthisreview.
andthencombiningthemtocapturecharacteristicofdifferentcompo-
nents in a complex system. This ensemble learning framework, also 2. Methodology
discussed by Huang et al. [49], facilitates joint prediction efforts,
showcasing the diverse strategies within PIML to develop robust and TocomprehensivelyexploretheliteratureonPIMLforBEMappli-
physicallyconsistentMLmodels. cations,weemployedtheSub-keywordSynonymSearch(SSS)[23,59],
AlthoughPIMLhasbeenextensivelyexploredwithincomputersci- whichincorporatessynonymsforkeytermsduringthesearchprocessto
ence,fromtaxonomy[57]toexperimentaldesign[58],itsapplicationin ensurenorelevantstudyisoverlooked.Thismethodisvitalforaholistic
thefieldofBEMisstillnascent.ExistingliteraturereviewsofBEMpri- review,asitreducestheriskofmissingcriticalpapersduetotheabsence
marilyfocusonphysics-basedmodelingand/ordata-drivenmodelingas of synonymous search terms or different expression of keywords. For
major modeling approaches [5,8,12,23,41]. A review of the PIML instance,termslike“physics-informedmachinelearning”and“physics-
applicationinBEMisstilllacking.ConsideringtheadvantagesofPIML constraint machine learning” might be used interchangeably by
compared to traditional data-driven and physics-based modeling, it scholars,thoughtheyrepresentsimilarmethodologieswithinPIMLfor
holds great potential for enhancing the performance of BEM by inte- BEM.Neglectingtoincludebothinthesearchcouldleadtoanincom-
grating building physics dynamics into ML models. Therefore, a pletecollectionofresearch.Inourapproach,weselectedonesynonym
comprehensive review in this field is necessary. This review aims to fromapredefinedlist(outlinedinTable1)foroursearches.Addition-
address this gap by providing the following contributions. First, we ally,weadoptedthe‘Snow-ball’technique,reviewingreferenceswithin
systematically review and discuss existing studies on PIML in BEM, the gathered papers to further ensure the comprehensiveness of our
identifyingkeytrends,challenges,andgapsinthecurrentresearch.This search.Inthisreview,wefocusedonkeywordscomposedofthreesub-
analysisnotonlysummarizesthecurrentstateofPIMLinBEMbutalso keywords to narrow the scope of publications on building and urban
highlights key areas for further investigation. Next, we discuss the systems. The first sub-keyword focuses on the research topic that in-
mechanismsofPIML,demonstratinghowitcanenhanceBEMbyinte- cludes “urban” and “building”. The second sub-keyword specifies the
gratingdetailed building physics dynamicsintoML models.Although target for prediction, with the options: “energy modeling”, “load pre-
BEM encompasses various aspects such as air-conditioning systems, diction”, “demand response", and “thermal comfort evaluation”. The
lighting,ventilation,andotherenergyconsumptionareas,thisreview third sub-keyword outlines the prediction methodologies, including
focuses specifically on building energy systems related to thermal “physics-informed machine learning”, “physics-constrained machine
environmentbecausethecurrentresearchontheapplicationofPIMLto learning”, “hybrid model”, and “physics and data-driven”. We used
BEMpredominantlyhighlightsenergyuse(buildingthermalloadpre- GoogleScholarastheprimarysearchenginetoimplementthismeth-
diction),indoortemperature,andthermalcomfortevaluation. odology. The search involved combining these sub-keywords compre-
Throughacomprehensiveliteraturereview,thisworkclassifiesPIML hensively,resultingin32uniquekeywordcombinations.Giventhatthe
applicationsinBEMintofourcategoriesinthiswork(Fig.1),including conceptofPIMLwasintroducedin2018,ourreviewprimarilyfocuses
(1) physics-informed inputs; (2) physics-informed loss functions; (3) onpublicationsfrom2018to2024.Thesesearches,conductedusinga
physics-informed architectural design; (4) physics-informed ensemble Pythonmoduleasreferencedin[23],enabledustocollect202related
models.Specifically,physics-informedinputsemphasizethemanipula- journalandconferencepapersusingtheSSSmethod.Additionally,we
tionofinputdatainMLmodels,leveraginginherentphysicsknowledge identified 31 publications as representing the most cutting-edge
containedwithinphysics-basedsimulationdatatoenhancetheperfor- researchinthisfieldandclassifiedthemintofourcategories(listedin
mance of data-driven building modeling. Physics-informed loss func- Table2).Thecriteriaforselectionwere(1)studiespublishedinprom-
tionsinvolveintegratingphysicsknowledgeintobuildingmodelingby inentjournals(impactfactorin2023>5)orconferences;(2)studies
manipulatingoutputs,i.e.,introducingadditionalregularizationterms that synthesized physical knowledge and data-driven models for pre-
as physics constraints into the loss function to ensure model outputs diction,excludingsurrogatemodeling.Theseworksshowcaseasignif-
adheretophysicallaws.Physics-informedarchitecturaldesigninvolves icantupwardtrendinPIMLforBEMresearchoverrecentyears.
reconstructingthedata-drivenmodelstructuretoincorporatephysical
rulesandprinciples.Physics-informedensemblemodelsexploresjoint 3. Physics-informedinputs
prediction by assembling physics-based and data-driven models to
handle different components in prediction systems. The reasoning TrainingdatasetsserveasthefoundationofMLmodels,containing
behindthiscategorizationisthatMLmodelsareessentiallycomposedof theunderlyingrelationshipsbetweeninputfeaturesandtargetedvari-
threeparts:inputs,architectures(e.g.,hiddenlayersinneuralnetworks), ables. Traditional ML models in BEM focus on elucidating hidden
and outputs.The firstthreecategoriesreflecthowphysics knowledge nonlinear mathematical relationships among variables in the training
can be integratedinto ML modelsfrom different perspectives (i.e.,by dataset,whichtypicallyconsistofobserveddatasuchashistoricalen-
manipulating inputs, model structures, and outputs). The fourth cate- ergyuse(aspredictiontargets),weatherdata,andindoortemperatures
gory, physics-informed ensemble model, refers to scenarios where (asinputfeatures).PhysicsinformedinputsdifferfromtraditionalML
physics-basedanddata-drivenmodelsarecombinedforjointprediction methodsbydirectlyusingsimulationoutcomesofphysics-basedmodels
taskswithoutalteringinputsorarchitectureofthedata-drivenmodels. (e.g., energy use, which is originally a prediction target in pure data-
In ensemble models, each type of model plays a distinct and comple- driven models) as inputs to propagate physics information into data-
mentary role in the integrated model to improve overall predictive driven models. Physics-based models incorporate numerous physical
performance.Accordingly,thisworkisorganizedasfollows.First,the
methodology of this review is shown in Section 2. Second, Section 3
introducesphysics-informedinputs,includingthedirectuseofsimula- Table1
tion results from physics-based modeling as inputs and domain adap- Keywordsearchlist.
tation for mapping simulation data to observations. Third, Section 4 List1-Researchtopic “urban”,“building”
presents physics-informed loss functions, followed by the physics-
List2–Targetfor “energymodeling”,“loadprediction”,“demandresponse",
informedarchitecturaldesigninSection5,whichincludesdata-driven prediction “thermalcomfortevaluation”.
models informed by physical knowledge and physics-based models “physics-informedmachinelearning”,“physics-
empowered with data-driven components. Subsequently, physics- List3-Methodology constrainedmachinelearning”,“hybridmodel”,“physics
anddata-driven”
informed ensemble models are introduced in Section 6. Section 7
4

Z.Maetal. Applied Energy 381 (2025) 125169
Table2
PIMLapproachesintheapplicationforBEM.
Methods Physicalinformation Data-drivenmodel Targetofprediction Reference
|     | Simulationresultsfrommodel |     |     |                   | Brøggeretal. |
| --- | -------------------------- | --- | --- | ----------------- | ------------ |
|     | basedonEuropeanstandardISO |     | MLR | Energyconsumption |              |
[61]
13970[60]
|     | SimulationresultsfromEnergyPlus |                                |     |                   | Nutkiewicz |
| --- | ------------------------------- | ------------------------------ | --- | ----------------- | ---------- |
|     |                                 | ArtificialNeuralNetworks(ANNs) |     | Energyconsumption |            |
model etal.[62,63]
SimulationresultsfromIDA-ICE
Physics-informed LongShort-TermMemory(LSTM) Energyconsumption Ohetal.[65]
[64]
input
K-neighborsclassifier;decisiontreeclassifier;
SimulationresultsfromVirtual randomforestclassifier;logisticregression;gradient Thermalcomfort Tardiolietal.
|     | Environment[66] |     |     |     | [67] |
| --- | --------------- | --- | --- | --- | ---- |
boostingclassifier
SimulationresultsfromRCmodels Sub-space-basedDomainAdaptation(SDA) Walltemperature Contietal.[68]
SimulationresultsfromEnergyPlus GenerativeAdversarialNetworks(GANs) Energyconsumption Tianetal.[69]
model
PhysicalconstraintofRCmodel ANNs Indoortemperature Chenetal.[70]
|     |     |     |     | Indoortemperature;energy | Gokhaleetal. |
| --- | --- | --- | --- | ------------------------ | ------------ |
Physics-informed PhysicalconstraintofRCmodel ANNs;fittedQ-iteration consumption [71,72]
| outputs |     |     |     |     | Paviranietal. |
| ------- | --- | --- | --- | --- | ------------- |
PhysicalconstraintofRCmodel ANNs; Energyconsumption;thermalcomfort
[73]
Fourier’slaw
|     |     |     | ANNs | Thermalconductivity | Liuetal.[74] |
| --- | --- | --- | ---- | ------------------- | ------------ |
PhysicalconstraintofRCmodel DeepDyna-Q Indoortemperature Saeedetal.[75]
|     | Co-variationofindoortemperature |                               |      |                          | Nataleetal.   |
| --- | ------------------------------- | ----------------------------- | ---- | ------------------------ | ------------- |
|     |                                 |                               | LSTM | Indoortemperature        |               |
|     | andHVACenergypower              |                               |      |                          | [76,77]       |
|     | Co-variationofindoortemperature |                               |      |                          | Xiaoetal.     |
|     |                                 | RecurrentNeuralNetworks(RNNs) |      | Indoortemperature        |               |
|     | andHVACenergypower              |                               |      |                          | [78,79]       |
|     | Statespaceequationofindoor      |                               |      | Indoortemperature;energy |               |
|     |                                 |                               | ANNs |                          | Wangetal.[80] |
|     | temperature                     |                               |      | consumption              |               |
Loadprediction,indoorenvironment,
Heatbalanceequations ANNsandRNNs modeling,buildingretrofitting,and Jiangetal.[81]
energyoptimization
|     | Statespaceequationofindoor |                             |     | Indoortemperature;energy |               |
| --- | -------------------------- | --------------------------- | --- | ------------------------ | ------------- |
|     |                            | ANNsandSoftActorCritic(SAC) |     |                          | Wangetal.[82] |
|     | temperature                |                             |     | consumption              |               |
ANNs;SVM;GaussianProcessRegression(GPR);
RCmodel GaussianMixtureModel(GMM);ordinaryleast Energyconsumption Dongetal.[83]
squares
Physics-informed
|     | Statespaceequationofindoor |     |     |     | Drgonˇaetal. |
| --- | -------------------------- | --- | --- | --- | ------------ |
architectural
|        | temperature;boundaryof |     | ANNs | Indoortemperature |      |
| ------ | ---------------------- | --- | ---- | ----------------- | ---- |
| design | parameters             |     |      |                   | [84] |
Statespaceequationofindoor Autoregressive–Moving-AveragewithExogenous Bünningetal.
Indoortemperature
|     | temperature               |     | Inputs(ARMAX) |     | [85]        |
| --- | ------------------------- | --- | ------------- | --- | ----------- |
|     | Buildingorientationandthe |     |               |     | Mirfinetal. |
oppositeimpactofsolargainon Time-Of-WeekandTemperature(TOWT)model Energyconsumption
[86]
heatingandcooling.
|     |     | NeuralOrdinaryDifferentialEquations(NODE)and |     |     | Tabogaetal. |
| --- | --- | -------------------------------------------- | --- | --- | ----------- |
Energyconservationlaw ControlledDifferentialEquations(CDE) Indoortemperature [87]
Heartransferandthermal
|     |     | GraphAttentionNetworks(GATs) |     | Energyconsumption | Jiaetal.[88] |
| --- | --- | ---------------------------- | --- | ----------------- | ------------ |
dynamicsinmulti-zones
Interrelationsbetweenurban GATs Outdoorthermalcomfort Zhengetal.
|     | spatialelements |     |     |     | [89] |
| --- | --------------- | --- | --- | --- | ---- |
Spatio-temporalshadows GraphConvolutionalNetworks(GCNs) Energyconsumption Huetal.[90]
Indoorairdynamics ANNs Indoorcarbondioxideconcentration Sonetal.[91]
LSTM;AutoregressiveIntegratedMovingAverage
|     | EnergyPlusandRCmodels |     |     | Thermalload | Maetal.[92] |
| --- | --------------------- | --- | --- | ----------- | ----------- |
(ARIMA)
Indoortemperature;energy
|                  | RCmodel | ANNs;MLR |     |             | Yueetal.[93] |
| ---------------- | ------- | -------- | --- | ----------- | ------------ |
| Physics-informed |         |          |     | consumption |              |
K-NeighborsRegression(KNR);SVM;TreeRegression
| ensemblemodels | Fanger’smodel |     |     | Thermalcomfort | Zhouetal.[94] |
| -------------- | ------------- | --- | --- | -------------- | ------------- |
(TR);LinearRegression(LR).
Zhangetal.
|     | Grey-boxinfiltrationmodel | Decisiontree |     | Infiltration      | [95]        |
| --- | ------------------------- | ------------ | --- | ----------------- | ----------- |
|     | EnegryPlusmodel           | ANNs         |     | Energyconsumption | Xuetal.[96] |
rules and constraints to describe the dynamics of building operation. 3.1. Directuseofsimulationresultsfromphysics-basedmodelingasinputs
Thus,incorporatingmodelingoutcomesintothetrainingofdata-driven
modelsembedsawealthofphysicalknowledgeintothesemodels.This Actualbuildingenergyusemeasurementsareexpectedtoencompass
sectionexplorestheconceptofusingphysics-informedinputstodirectly threedistinctcomponents[97](Fig.2a):(1)energyconsumptiongov-
leveragephysics-basedsimulationresultsintrainingMLmodels.Section ernedbythephysicsprinciples;(2)stochasticenergyusedrivenbyoc-
cupant’sschedulesandinteractionswithbuildings;and(3)whitenoise
3.1discussestheeffectofdirectlyinputtingphysicsmodelsimulation
results into data-driven models. However, due to the heterogeneous errors stemming from data measurement inaccuracies, such as those
hypothesisdistributionsbetweensimulatedandobserveddata,directly from energy meters or other sensors. Physics-based models rely on
usingthesimulationresultsmightleadtopredictionfailure.Therefore, physics principles (e.g., heat transfer) to simulate building operation
Section3.2exploresdomainadaptationmethodstofacilitatemappingof dynamics, such as interaction with the ambient environment and the
simulationdatatoobserveddata. influence of indoor activities. These models produce simulation out-
comesthatencodethephysicsknowledgewithinthem(component1).
5

| Z.Maetal. |     |     |     |     |     |     | Applied Energy 381 (2025) 125169  |     |
| --------- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- |
Fig.2. (a)Physicalinsightsintheobservedbuildingenergyconsumptiondata.(b)Physics-informedinputthroughusingsimulationresultsandobservedhistorical
dataasinput[62].
Chen et al. [97] highlighted that using simulation data from physics- reductioninCV-RMSEcomparedtopurelyphysics-basedmodels.
basedmodelsasanadditionalinputfeaturecansignificantlyimprove InadditiontoANNs,GANs[98],whicharecomposedofagenerator
thepredictiveaccuracyofMLmodels.Thecoefficientofdetermination GandadiscriminatorD(bothofthemareneuralnetworks),werealso
(R2) for load prediction improved from 0.8 to 0.98 in one test com- fed with simulation data for large scale BEM (Fig. 3). The role of
mercialbuilding.Anothercommonmethodistoinputbothsimulation generatoristoproducesamplesthatmimicrealdata,aimingtodeceive
and experimental data into a neural network, enhancing the model’s thediscriminator,whilethediscriminatorstrivestodistinguishbetween
learning capacity [65,67]. For example, Nutkiewicz et al. [62] intro- thesamplesproducedbythegeneratorandtherealsamples.Thisdy-
ducedaData-drivenUrbanEnergySimulation(DUE–S)frameworkthat namic is encapsulated in the evaluation feedback function V(D,G),
combines physics-based simulation results with residual networks whichservestorefinetheperformanceofgeneratoranddiscriminator.
(ResNet)tocaptureboththethermaldynamicswithinbuildingsandthe TheGANoperatesthroughanadversarialprocess,wherethegenerator
endeavorstominimizethevaluefunctionV(D,G),whilethediscrimi-
| complex nonlinear | interactions | of urban | environments. As | shown in |     |     |     |     |
| ----------------- | ------------ | -------- | ---------------- | -------- | --- | --- | --- | --- |
Fig.2b,periodictimeseriesdatafromEnergyPlusmodelingisusedas natorseekstomaximizeit.Theprocessismathematicallyrepresented
| inputstotheResNet,whichlearnstherelationshipbetweenthesimu- |                 |              |                    |     | as:                     |                    |                          |     |
| ----------------------------------------------------------- | --------------- | ------------ | ------------------ | --- | ----------------------- | ------------------ | ------------------------ | --- |
| lated energy                                                | data and actual | measurements | for each building. | The |                         |                    |                          |     |
|                                                             |                 |              |                    |     | m inm axV(D,G)=Et∼pt(t) | [logD(t)]+Es∼ps(s) | [log(1(cid:0) D(G(s)))], | (1) |
| combinedmodeliscapableofpredictingenergyusageatbothbuilding |                 |              |                    |     | G D                     |                    |                          |     |
andurbanscales,demonstratingaCoefficientofVariationofRootMean
(t)isthedistributionoft;
SquareError(CV-RMSE)of0.460forhourlybuilding-scaleprediction wheretisthetargetdomaindata(realdata);pt
(s)isthepriorontheinput
and0.256forurban-scaleprediction.Moreover,theDUE-Smodelwas ps simulationresults; DandGare thedif-
extended to predict the energy consumption after retrofits (such as ferentialfunctionsusuallyrepresentedasmulti-layerneuralnetworks;
G(s)istheoutputofgenerator;andD(x)representsthepossibilitythatx
window-to-wallratiochangesandconstructionupgrades)bypretrain-
|     |     |     |     |     | is thereal data.GAN | can be effectively | usedforlarge-scale | BEMsce- |
| --- | --- | --- | --- | --- | ------------------- | ------------------ | ------------------ | ------- |
inganANNwithbuildingenergysimulationdata[63].Theirfindings
nario,wherecollectingdetailedphysicalparametersistime-consuming
| suggest that considering | the | urban context | can amplify | the overall |                      |              |                       |            |
| ------------------------ | --- | ------------- | ----------- | ----------- | -------------------- | ------------ | --------------------- | ---------- |
|                          |     |               |             |             | and labor-intensive. | For example, | developing EnergyPlus | models re- |
energy-savingeffectsofretrofitsonindividualbuildingsbyupto7.4%.
|     |     |     |     |     | quires a large | amount of weather | data and physical | parameters |
| --- | --- | --- | --- | --- | -------------- | ----------------- | ----------------- | ---------- |
AnotherexampleisBrøggeretal.[61],whoinputthecalculatedenergy
demandbasedontheEuropeanstandardISO13970andobservedusage (includingbuildingprototype,plugloaddensity,lightingpowerdensity,
data(e.g.,observedenergydemand,heatedfloorarea,andownership) U-value of window, etc.) for each building. To enhance the computa-
intotheMLRmodeltopredicttheheatingenergy,achievinga13.3% tional efficiency of large-scale building modeling, Tian et al. [69]
6

Z.Maetal. Applied Energy 381 (2025) 125169
Fig.3. StructureofGANanditsapplicationonthelarge-scaleBEM[69].
proposedanEnergyPlus-GAN(E-GAN)model,leveragingaGANtrained predictionsevenwhenavailabledataislimitedinthetargetedbuildings.
withthesimulateddailypowerdemandofasmallsetoftypicalbuild- In PIML scenarios, the source domain X S refers to simulation data,
ingstoforecastthepowerdemandsofalargenumberofbuildings.The whilethetargetdomainX T usuallyreferstoobserveddata.However,
processinvolvescategorizingbuildingsbasedontheirenergydemand the data distribution in the source and target domains could be
profiles,selectingarepresentativesubsetfromeachcategoryastypical considerablydifferent,requiringspecificdomainadaptationstrategies.
buildings (around 4 % of total samples), using EnergyPlus to predict This section introduces the subspace-based domain adaptation (SDA)
power demand of these typical buildings, and then applying GAN to method [104,105], which bridges the gap between simulation and
forecastpowerdemandonalargescale.Comparedtotraditionaldata- observeddata,facilitatingeffectivedomainadaptationandenhancing
driven models such as SVM, the E-GAN reduces the Mean Absolute predictionaccuracyinBEM.
PercentageError(MAPE)byapproximately70%.Theaforementioned SDAisatransferlearningstrategythatmapssourceandtargetdata
research highlights the importance of incorporating physics-based into lower-dimensional spaces, known as subspaces, and then aligns
modeling outcomes as inputs to data-driven models to encode valu- these subspacesto createa shared mutualsubspace [106]. Procrustes
ablephysicalinformation.However,whenphysics-basedmodelshave analysisistypicallyusedforthisalignmentprocess,identifyingthebest
lowfidelityandlackaccuracyinmodelingreal-worlddynamics,simu- matchingtranslation,reflection,androtationtransformationsbetween
lationdatamayneedtobeadjustedbasedonobserveddatabeforebeing datastructures(e.g.,shape,image,andscatterplot)(Fig.4).Contietal.
fedintodata-drivenmodels.Thisadjustmentrequiresdomainadapta- [68]introducedanSDAframeworkaimedatpredictingwalltempera-
tiontechniquestoensureaccurateandreliablemappingofsimulation tures using simulation datafrom a3R2C model represented bylinear
datatoactualmeasurements. state-space equations. Applying the SDA strategy has been shown to
reducetheCV-RMSEbyapproximately20–30%comparedtothe3R2C
model.Remarkably,whenthereisamismatchinwallthicknessbetween
3.2. Domainadaptationformappingsimulationdatatoobservations the3R2Cmodelandthegroundtruth,theCV-RMSEreductionachieved
throughSDAcanbeashighas70%,underscoringtheeffectivenessof
Tomoreeffectivelyutilizephysicalinformationinsimulationdata,a thisapproachinenhancingpredictionaccuracythroughdomainadap-
promising solution is to use domain adaptation techniques to map tation techniques. The physics-informed input scheme is particularly
simulation outcomes to the observed data. Mainstream domain adap- usefulinsituationswherethetrainingdatafromactualmeasurementsis
tation approaches for BEM include fine-tuning [99,100], Maximum scarceordataacquisitioncostsarehigh.
MeanDifference(MMD)[101],andensemblelearning[102,103].These
methodstypicallyapplytheknowledgelearnedfromthehistoricaldata
ofsourcebuildings(sourcedomainX S)tofacilitateenergyprediction
for target buildings (target domain X T), enabling more accurate
Fig.4. Physics-informedinputsthroughdomainadaptationstrategies[68].
7

| Z.Maetal. |     |     |     |     |     |     |     |     |     |     |     |     | Applied Energy 381 (2025) 125169  |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- |
4. Physics-informedlossfunctions building control models using fitted Q-iteration [71], the authors re-
portedcostsavingsofaround9%comparedtoconventionalcontrollers.
Inadditiontousingphysics-basedmodelingoutcomesasdirectin- Similarly,Chenetal.[70]developedanphysics-informedNNmodelfor
putsforPIML,anothereffectiveapproachtoencodingphysicsknowl- building demand response control, demonstrating improved accuracy
withaMeanAbsoluteError(MAE)of0.25◦CandaCV-RMSEof1.2%
| edge | into data-driven |     | models | (e.g., | neural networks) | is  | the design | of  |     |     |     |     |     |     |     |
| ---- | ---------------- | --- | ------ | ------ | ---------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
physics-informed loss functions, which integrate additional physics- forroomtemperature,andanMAEof110WandCV-RMSEof17.1%for
constrained regularization terms into the loss function during ML cooling load demand prediction, outperforming conventional neural
modeltraining(Fig.5).UnliketheconventionallossfunctionL(̂y,y)in
networkmodels.Inadditiontoincorporatingphysicalconstraintsfrom
neural networks, which measures the discrepancy between predicted RCmodels,Fourier’slawofheattransfercanalsobeintegratedintothe
outputs ̂yand the actual outputs y, the modified loss function in- lossfunction.Liuetal.[74]proposedaphysics-informedlossfunctionto
corporatesaregularizationtermthatpenalizesdeviationsofpredictions predict the temperature distribution in building envelopes, incorpo-
fromknownphysicalprinciples.Thiscanbeexpressedas: ratingthepenaltiesfordeviationsfromFourier’slawandcorresponding
|     |              |     |     |     |     |     |     |     | boundaryconditions.AnR2 |     | valuegreaterthan0.99demonstratesthe |     |     |     |     |
| --- | ------------ | --- | --- | --- | --- | --- | --- | --- | ----------------------- | --- | ----------------------------------- | --- | --- | --- | --- |
| L   | =L(̂y,y)+λLp | (DΩ | )   |     |     |     |     |     |                         |     |                                     |     |     |     |     |
(2)
|       |     |                    |     |                |     |                 |     |     | effectiveness | of the               | model   | in predicting |            | the uniform     | thermal               |
| ----- | --- | ------------------ | --- | -------------- | --- | --------------- | --- | --- | ------------- | -------------------- | ------- | ------------- | ---------- | --------------- | --------------------- |
|       | λis |                    |     |                |     |                 |     |     | conductivity. |                      |         |               |            |                 |                       |
| where |     | the regularization |     | hyperparameter |     | that determines |     | the |               |                      |         |               |            |                 |                       |
|       |     |                    |     |                |     |                 |     |     | T h e L       | p t er m c a n a l s | o b e u | s e d to p e  | na l i z e | p r e d i ct io | n s t ha t e xc e e d |
strengthofthepenalty;DΩrepresentsthephysicalrulesorconstraints; nˇa
|     |     |     |     |     |     |     |     |     | bou n d ar y | li m i ts. F o r e x | a m p le , | D r go e | t a l . [ 8 | 4 ] u s e d | p a ra m e tr ic r e g - |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | -------------------- | ---------- | -------- | ----------- | ----------- | ------------------------ |
andLpistheregularizationtermthatenforcesthesephysicalconstraints.
|                |     |                                                   |     |     |     |     |     |     | ularization | terms to impose | inequality |     | constraints | that | enforce physi- |
| -------------- | --- | ------------------------------------------------- | --- | --- | --- | --- | --- | --- | ----------- | --------------- | ---------- | --- | ----------- | ---- | -------------- |
| Regularization |     | addressesshortcomingsoftraditionallossfunctionsby |     |     |     |     |     |     |             |                 |            |     |             |      |                |
callymeaningfulboundariesonthetargetvariables.Certainvariablesin
imposingadditionalpenaltiesthatguidethemodeltoproduceoutputs
BEMprocessmustbeconstrainedwithinphysicallyplausibleranges.For
consistentwithestablishedphysicallaws.Thisisparticularlyimportant
|     |     |     |     |     |     |     |     |     | instance, | it is not physically | consistent |     | for a | 1 K change | in ambient |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | -------------------- | ---------- | --- | ----- | ---------- | ---------- |
inscenarioswheredata-drivenmodelsmightotherwiseproducephysi-
temperaturetocausea2Kchangeinindoortemperatureinasingletime
callyimplausibleresults.Byminimizingtheintegratedlossfunction,the
step.Thisconceptcanbeenforcedbyapplyinginequalityconstraintsvia
| model | is encouraged |     | to not | only fit | the data | well but | also adhere | to  |     |     |     |     |     |     |     |
| ----- | ------------- | --- | ------ | -------- | -------- | -------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
penaltyfunctionsateachtimestept:
| predefined |     | physics | rules, | thereby | improving | its generalization |     | and |     |     |     |     |     |     |     |
| ---------- | --- | ------- | ------ | ------- | --------- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|            |     |         |        |         |           |                    |     |     | ̂   | ̂   | ̂   |     |     | ̂   |     |
robustness. Detailed mathematical proofs are available in reference p(T ,Tt )=max(0,T (cid:0) Tt ),p(T ,T )=max(0,T (cid:0) T ) (5)
|                 |     |     |                                                |     |     |     |     |     | t   | t   | t   | t   | t   | t   |     |
| --------------- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [107].ThetermLp |     |     | correspondstospecificphysicalrulesorequations, |     |     |     |     |     |     |     |     |     |     |     |     |
whereDΩ =0,typicallyderivedfromRCmodelsorstatespaceequa- whereTtandT aretheupperandlowerboundsofthepredictedindoor
t
| tions.Forexample,thethermalmasstemperatureTm,tcanbecalculated |     |     |     |     |     |     |     |     |              | ̂                                      |     |     |     |     |     |
| ------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | -------------------------------------- | --- | --- | --- | --- | --- |
|                                                               |     |     |     |     |     |     |     |     | temperatureT | t.Thelossfunctioncanthenbeexpressedas: |     |     |     |     |     |
usinganRCmodelasfollows[70]:
∑
|     | (   |     | )   |     |     |     |     |     | 1   | n ̂ ‖2 | ̂   | )‖2 | ̂   | )‖2 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
Tr,t+1 (cid:0) Tr,t L = ‖Tt (cid:0) T +λ ‖p(T ,Tt +λ ‖p(T ,T (6)
| Tm,t | =α  |     | ,+βT ̂ | +γTa,t | +δQt |     |     | (3) | n   | t 2 | 1 t | 2   | 2 t | t 2 |     |
| ---- | --- | --- | ------ | ------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|      |     | Δ   |        | r,t    |      |     |     |     | t=  | 1   |     |     |     |     |     |
t
|     |     |     |     |     |     |     |     |     | By including | these | two regularization |     | terms, | the | loss function |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ----- | ------------------ | --- | ------ | --- | ------------- |
̂
whereTr,t and Tr,t aretheobservedandestimatedroomtemperature; effectivelypenalizesoutputsthatexceedtheboundarylimits.Overall,
Ta,t istheambienttemperature;Qt istheheatsource;α,β,γ,δarepa- integrating physical constraint terms into the loss function not only
rametersintheRCmodel.Thelossfunctioncanbewrittenas: enhancespredictionaccuracybutalsoensuresthatpredictionsremain
|     |      |     |     |      |     |     |     |     | p h ys i ca l l | y p l a us ib l e . H o | w e ve r , | u si n g so f | t p e n a l ty | c o n st r | a i n ts m eansthat |
| --- | ---- | --- | --- | ---- | --- | --- | --- | --- | --------------- | ----------------------- | ---------- | ------------- | -------------- | ---------- | ------------------- |
|     | 1 ∑n |     | 1   | ∑n ⃦ | ⃦   |     |     |     |                 |                         |            |               |                |            |                     |
L = ‖Tt (cid:0) ̂ ‖2 +λ ⃦ (cid:0) ̂ ⃦2 th e u n d e r ly i n g p h y s ic a l la w s a r e o n ly a p p r o x i m a te l y s a t i sfi e d.
|     |       | T t | 2   | Tm,t | T m,t 2 |     |     | (4) |     |     |     |     |     |     |     |
| --- | ----- | --- | --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | n t=1 |     | n   | t=1  |         |     |     |     |     |     |     |     |     |     |     |
5. Physics-informedarchitecturaldesign
|     | By integrating | the | discrepancies |     | between | predicted | and measured |     |     |     |     |     |     |     |     |
| --- | -------------- | --- | ------------- | --- | ------- | --------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
indoortemperatures,aswellsasthosebetweenpredictedandsimulated
thermalmasstemperatures(viaRCmodels),thelossfunctionensures Data-driven models are typically unreliable in out-of-sample pre-
adherencetothephysicalconstraintsgoverningthethermaldynamicsof dictions(extrapolation).Transformingthestructureofhiddenlayersto
bephysics-informediscrucialforenablingmodelstoleveragephysics
indoorair.Gokhaleetal.[72]demonstratedtheapplicationofanANN-
|       |                  |     |      |          |     |                  |         |     | knowledge | in predictions | that | require | extrapolation. |     | This trans- |
| ----- | ---------------- | --- | ---- | -------- | --- | ---------------- | ------- | --- | --------- | -------------- | ---- | ------- | -------------- | --- | ----------- |
| based | physics-informed |     | loss | function | for | control-oriented | thermal |     |           |                |      |         |                |     |             |
formationsignificantlyenhancestheapplicabilityofdata-drivenmodels
| modeling | of  | buildings, | achieving |     | low prediction | errors | (less | than |     |     |     |     |     |     |     |
| -------- | --- | ---------- | --------- | --- | -------------- | ------ | ----- | ---- | --- | --- | --- | --- | --- | --- | --- |
0.25◦C)forroomtemperature.Inanotherstudyfocusedonresidential inpractice,includingbothinsertingextraneuronsandalteringthelogic
|     |     |     |     |     | Fig.5. | IntegrationofphysicalinformationintothelossfunctionofMLmodels. |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | -------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
8

| Z.Maetal. |     |     |     |     |     |     | Applied Energy 381 (2025) 125169  |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- |
gatesinmodelsaccordingtopriorphysicalknowledge.Byfundamen- outcomes(e.g.,energyuse)areonlyrelevanttohistoricalandcurrent
tallychangingthealgorithmarchitecture,physicallawsandprinciples control/disturbancevariables,notfutureinformation.Recognizingthis,
canbedeeplyanddirectlyincorporatedintocomputationalalgorithms, Wangetal.[80,82]proposedapartiallyconnectedneuralnetworkby
therebyenhancingtheirpredictiveaccuracy,generalizability,andcon- directly modifying neuron connections to predict indoor temperature
sistencywithphysicallaws.Thissectionwillreviewexistingarchitec- thermaldynamics.Inthisdesign,neuronswithineachlayerareorga-
turechangesinMLmodelsthatmakethemphysicsinformed.Section nized intodifferent blocks,soonlycurrent andhistorical information
5.1 willfirst discuss how data-driven models, including ANNs, RNNs, areconsideredwhenpredictingfuturetimesteps(Fig.6a).Takingthe
Graph Neural Networks (GNNs), NODE, and linear models, can be jth hidden layer as an example, the function of this layer can be
| enhanced | with additional | physical knowledge | through architectural |     | expressedas: |     |     |     |     |
| -------- | --------------- | ------------------ | --------------------- | --- | ------------ | --- | --- | --- | --- |
design.Inadditiontohiddenlayerdesign,data-drivenmodelscanalso ⎡ ⎤ ⎛ ⎡ ⎤⎞
|     |     |     |     |     | z ( t) |     | z j(cid:0) ( t) |     |     |
| --- | --- | --- | --- | --- | ------ | --- | --------------- | --- | --- |
serve as nonlinear components in physics-based models to enhance ⎢ j ⎥ ⎜ ⎢ 1 ⎥ ⎟
|     |     |     |     |     | ⎢ zj ( t + | 1) ⎥ ⎜ ⎢ | zj(cid:0) (t + 1) ⎥ ⎟ |     |     |
| --- | --- | --- | --- | --- | ---------- | -------- | --------------------- | --- | --- |
predictionperformance,whichwillbeexploredinSection5.2. ⎢ ⎥ ⎜ ⎢ 1 ⎥ ⎟
|     |     |     |     |     | ⎢ zj (t +2) | ⎥ =gj ⎜ wj ⎢ | zj(cid:0)1 (t +2) ⎥ ⎟ |     | (7) |
| --- | --- | --- | --- | --- | ----------- | ------------ | --------------------- | --- | --- |
|     |     |     |     |     | ⎣           | ⎦ ⎝ ⎣        | ⎦ ⎠                   |     |     |
|     |     |     |     |     | ⋮           |              | ⋮                     |     |     |
|     |     |     |     |     | (t+h(cid:0) | 1)           | (t+h(cid:0) 1)        |     |     |
5.1. Data-drivenmodelsinformedbyphysicalknowledge zj zj(cid:0)1
(i)istheoutputofthejthlayerthatcontainsnofutureinfor-
wherezj
Traditionaldata-drivenmodelsusecellsandconnectionstodevelop
mation;andgjistheactivatedfunction.wjisthemodifiedweightmatrix,
hiddenrelationshipsbetweeninputsandoutputs,whichisknownasthe
whichisexpressedas:
| hidden layers. | The concept | of architectural design | involves | reshaping |     |     |     |     |     |
| -------------- | ----------- | ----------------------- | -------- | --------- | --- | --- | --- | --- | --- |
|                |             |                         |          |           | ⎡   |     |     |     | ⎤   |
t h e h i d d e n l a y e r a r c h i t e c t u r e s u s i n g p r i o r k n o w l e d g e f r o m t h e b u i l d i n g w 0 0 ⋯ 0
|     |     |     |     |     |     | t, z t ,j(cid:0) 1 , j |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- |
p h y s i c s d o m a in . O n e w a y t o l e v e r a g e t h e p h y s i c s i n f o r m a t i o n in d a t a - ⎢ w w 0 ⋯ 0 ⎥
|     |     |     |     |     | ⎢   | t + 1 , z t , j (cid:0) 1 , j t + 1 , z t + | 1 , j (cid:0) 1 , j |     | ⎥   |
| --- | --- | --- | --- | --- | --- | ------------------------------------------- | ------------------- | --- | --- |
d r i v e n m o d e l s i s t o m o d i f y n o d e c o n n e c t i o n s a n d r e o r g a n i z e i n fo r m a - wj = ⎢ w w wt+2,z ⋯ 0 ⎥
|     |     |     |     |     | ⎢ ⎣ | t + 2 , z t , j (cid:0) 1 , j t + 1 , z t + | 2 , j (cid:0) 1 , j t+2,j(cid:0)1,j |     | ⎥ ⎦ |
| --- | --- | --- | --- | --- | --- | ------------------------------------------- | ----------------------------------- | --- | --- |
t i o n fl o w w i t h i n t r a d i t i o n a l n e u r a l n e t w o r k s . D o m a i n k n o w le d g e c a n ⋮ ⋮ ⋮ ⋱ ⋮
alsobeusedtoassignphysicalmeaningstocertainneuronsinthehidden wt+h(cid:0)1,zt,j(cid:0)1 ,j wt+h(cid:0)1,zt+1,j(cid:0)1 ,j wt+h(cid:0)1,zt+2,j(cid:0)1 ,j ⋯ wt+h(cid:0)1,zt+h(cid:0)1,j(cid:0)1 ,j
| layers. This | section will review | the design of | physics-informed | ANNs, |     |     |     |     |     |
| ------------ | ------------------- | ------------- | ---------------- | ----- | --- | --- | --- | --- | --- |
(8)
RNNs,GNNs,NODE,andlinearmodels.
wherewi, ,jistheweightconnectedtotheithblockofthejthlayer.This
ANNs.InatypicalANNstructure,eachneuroninafullyconnected
|     |     |     |     |     | configuration | ensures that | future controls | and disturbances | do not |
| --- | --- | --- | --- | --- | ------------- | ------------ | --------------- | ---------------- | ------ |
layerisconnectedtoeveryneuroninthesubsequentlayer.However,
whenitcomestotaskssuchasbuildingenergyprediction,themodeling impactthecurrentoutput,therebyembeddingphysicalconstraintsinto
Fig.6. Physics-informedarchitecturaldesignforANNsandRNNs.(a)Structureofthepartialconnectedneuralnetworks[80].(b)StructureofthehybridRNNcell,
whichisatwo-layercellconsistingofoneRNNcell(top)andoneLSTMcell(bottom)[78].(c)Theneuralnetworkmodulelibraryandencoder-decoderGRUmodule
model,whereeachmoduleisdesignedtoestimateoneheattransferterm[81].
9

| Z.Maetal. |     |     |     |     |     |     |     |     |     |     |     |     | Applied Energy 381 (2025) 125169  |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- |
thestructureofthenetwork.Implementingthiscontrol-orientedmodel into nodes and connections is the GNNs [108–110]. GNNs efficiently
hasachievedsubstantialenergysavingsofover35%whilemaintaining propagateinformationbasedongraphstructures,minimizingredundant
thermalcomfortandairqualitystandards.Thisapproachdemonstrates computationsandincorporatingthegraphstructureasmodelfeatures.
the importance of integrating physical principles into neural network In GNNs, node labels are updated by considering the states of neigh-
architecturetoenhanceapplicabilityofdata-drivenmodels. boringnodesthroughamessage-passingprocess,asfollows:
|                                                               |                          |              |              |             |             |             |              |                       | (cid:0)                                                |     | (cid:0)     | ))    |          |               |      |
| ------------------------------------------------------------- | ------------------------ | ------------ | ------------ | ----------- | ----------- | ----------- | ------------ | --------------------- | ------------------------------------------------------ | --- | ----------- | ----- | -------- | ------------- | ---- |
| R N N s                                                       | . T h e lo o p -b a s ed | s t r u c    | t u re o fR  | N N s m     | a k e s t h | em m o re   | a d v a n -  | ʹ                     |                                                        |     |             |       |          |               |      |
|                                                               |                          |              |              |             |             |             |              | h =Update             | hi ,Aggregate                                          |     | hj |∀j∈N(i) |       |          |               | (12) |
| tage o u s t                                                  | h a n A N N s f o r      | ca p t u r i | n g th e     | te m p o ra | l d y n a   | m ics o f   | m o d e le d | i                     |                                                        |     |             |       |          |               |      |
| systems.Asaresult,theadoptionofRNNsinbuildingenergyprediction |                          |              |              |             |             |             |              | ʹ                     |                                                        |     |             |       |          |               |      |
|                                                               |                          |              |              |             |             |             |              | whereh                | andhiaretheupdatedandpreviousrepresentationsofnodei;hj |     |             |       |          |               |      |
| hasbeengrowinginrecentyears.Xiaoetal.[78,79]proposedanovel    |                          |              |              |             |             |             |              | i                     |                                                        |     |             |       |          |               |      |
|                                                               |                          |              |              |             |             |             |              | is the representation |                                                        | of  | neighboring | nodes | in N(i). | The operation | of   |
| physics-informed                                              | RNN                      | structure,   | enhancedfrom |             | the         | traditional | LSTM         |                       |                                                        |     |             |       |          |               |      |
GNNsinvolvestwoprimarysteps:aggregationandupdate.First,nodei
withadditionalRNNcells,toenforcephysicallyconsistentdynamicsin
gathersinformationfromitsneighborsN(i)usinganaggregatefunction.
modeling(Fig.6b).Physicalconstraintsareincorporatedthroughpar-
tialderivativesofindoortemperatureTkandrelativehumidityRHkwith Then,itupdatesitsfeaturesviaanupdatefunction.Differentvariations
respecttovariousinputs.Forexample,heatingpowershouldlogically ofGNNsuseuniqueupdateandaggregatefunctions.Thestructureand
(∂Tk /∂Uheat,k(cid:0)i >0), information propagation mechanism in different GNNs align with the
| increase | indoor temperature |     |     |     | while | cooling | power |     |     |     |     |     |     |     |     |
| -------- | ------------------ | --- | --- | --- | ----- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
shoulddecreaseit(∂Tk /∂Ucool,k(cid:0)i <0).TheoutputZk,whichcontainsthe requirements for predicting energy consumption in buildings with
multiplethermalzonesorwithinanurbancontext.Inthesecases,the
| predictedindoortemperatureTk |     |     | andrelativehumidity,haspartialde- |     |     |     |     |     |     |     |     |     |     |     |     |
| ---------------------------- | --- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
topologicstructuresinGNNscanbeconstructedbasedonphysicalin-
rivativesrepresentedasfollows:
teractionsbetweentargetthermalzonesorbuildings.Attheindividual
∂ Z b u il d in g lev e l , t h e g ra p h c an b e f o r m u lat e d w it h n o d e s r e p r e s e n t i n g
| k =TD⋅W | i ⋅Wih >0 |     |     |     |     |     | (9) |     |     |     |     |     |     |     |     |
| ------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∂ ̃x h h ea c h t h erm a l z o n e (d e fi n ed b ya r ea , v o lu m e , oc cu p an c y , t yp e s , e t c . ) a n d
k(cid:0) i
edgesrepresentingtheconnectionsbetweenthesezones,suchasopen-
∂Zk =TD⋅Wi+1>0 ings, walls, or doors (defined by area, thickness, material, thermal
(10)
| ∂Zk(cid:0)i | hh  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
transmittance,etc.),asdemonstratedinFig.7a.Jiaetal.[88]proposeda
hybridGNNmodelforpredictingthermalloadsinmulti-zonebuildings.
whereTDistheproductofi+1derivativesofthetanhfunction,which
|     |     |     |     |     |     |     |     | Their model | integrates |     | two main | modules: | GATs for | spatial | represen- |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ---------- | --- | -------- | -------- | -------- | ------- | --------- |
isalwayspositive.Therefore,theenforcementofphysicalconstraintsis
|          |                      |     |              |     |              |     |          | tation and | GRUs | for time | series | analysis. The | predicted | heating | loads |
| -------- | -------------------- | --- | ------------ | --- | ------------ | --- | -------- | ---------- | ---- | -------- | ------ | ------------- | --------- | ------- | ----- |
| achieved | through the positive |     | definiteness | of  | the weighted |     | matrices |            |      |          |        |               |           |         |       |
haveaMeanSquareError(MSE)of0.00124,whichis34%lowerthan
| (Whh >0,Wih | >0),ensuringthephysicallyplausiblevariationsinpre- |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ----------- | -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
thatofapureGRUmodel,indicatingtheefficacyofcombiningspatial
dictedtemperature.Inapplication,thecontrollerbasedonthehybrid
attentivenesswithtemporaldynamicsinpredictingheatingloads.Inter-
RNN-basedmodeloutperformsothercontrollers,suchastraditionalOn/
buildingeffects(e.g.,radiativeheattransfer)withinurbanenvironments
Off controllers, state-space model-based controllers, and LSTM-based canalsoberepresentedbyagraphstructure.Forexample,Zhengetal.
controllers, with energy savings of 5.8 %, 4.5 %, and 8.9 %, and im- [89]proposedaGATmodelthattreatsbuildingclustersasgraphnodes
provementsinthermalcomfortof55%,59%,and64%,respectively. andstreetsasedgestocapturetheinterrelationsbetweenurbanspatial
| Beyond | modifying the | internal | structure | of  | RNNs, | physics-based |     |     |     |     |     |     |     |     |     |
| ------ | ------------- | -------- | --------- | --- | ----- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
elementsandmodelthestreetUniversalThermalClimateIndex(UTCI)
| knowledge | can also be  | integrated     | into | RNNs          | through | an ensemble |         |            |                 |     |     |                 |     |       |          |
| --------- | ------------ | -------------- | ---- | ------------- | ------- | ----------- | ------- | ---------- | --------------- | --- | --- | --------------- | --- | ----- | -------- |
|           |              |                |      |               |         |             |         | (Fig. 7b). | The constructed |     | GAT | model comprises | six | nodes | and nine |
| approach. | Jiang et al. | [81] developed |      | a modularized |         | neural      | network |            |                 |     |     |                 |     |       |          |
edges,withnodedataobtainedfromBIMandBEM,andedgedatafrom
| incorporating | physical | priors | (ModNN), | based | on  | heat | balance |     |     |     |     |     |     |     |     |
| ------------- | -------- | ------ | -------- | ----- | --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
ComputationalFluidDynamics(CFD)simulation.Comparedtoatradi-
equations:
|     |     |     |     |     |     |     |     | tional ANN | model, | the | proposed | GAT model | significantly |     | enhances |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | --- | -------- | --------- | ------------- | --- | -------- |
∑N p r e d ic t io n a cc ur a cy b y 3 7 .5 % i n M A E a n d 36 . 0 7 % i n R o o t M ea n S qu a re
| dT  | air= ʹ ʹ | +q˙ | +q˙ | +q˙ |     |     |     |     |     |     |     |     |     |     |     |
| --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
maircair Ajq onv,in,j,θ inf,θ sys,θ int.conv,θ (11) E r ro r ( R M S E ). H u e t a l. [ 90 ] d e ve lo p e d a S p a t io- T e m p o r al G C N (S T -
| dt  | c   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
j=1 GCN) model to forecast urban energy demand, focusing on the inter-
|            |                   |               |            |            |              |               |             | connected | effects | of building | shadows | and | solar radiation |     | on energy |
| ---------- | ----------------- | ------------- | ---------- | ---------- | ------------ | ------------- | ----------- | --------- | ------- | ----------- | ------- | --- | --------------- | --- | --------- |
| w h er e m | is t h e m as s o | f s p a c e a | i r , c is | th e s p e | c ifi c h ea | t o f s p a c | e a i r , A |           |         |             |         |     |                 |     |           |
a ir a ir j c o n s u m p t io n p a t t e r n s ( F i g. 7 c) . I n t h is m o d e l, n o d es re p r e se nt b u il d in g s,
|     | jth | ʹ ʹ |     |     |     |     | q˙  |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
i s th e a re a o f t h e s u rf a c e , q ,i n, j, θ is th e c o n v e ct iv e h e a t fl u x , in f , θ is a n d e d g e s re p r e s e n t t h e i r c on n e c ti o n s, d e fi n e d b y th e a n g le o f sh a d o w ,
c o n v
| theheattransferduetoinfiltration,q˙ |     |     | sys,θistheheattransferduetothe |     |     |     |     |     |     |     |     |     |     |     |     |
| ----------------------------------- | --- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
therelativedirectionofshading,andthedistancebetweenbuildings.By
q˙
heating/cooling system, and int.conv,θ is the convective portion of the encodingphysicalinteractionsamongtheelementsofanurbanenergy
internal heat gains due to people, lights or equipment. First, they systemintotheST-GCN,themodeleffectivelypredictsbuildingenergy
developed distinct neural network modules to estimate each specific consumptionwithaMAPEofapproximately5%.Thisapproachhigh-
heattransfertermwithinthedynamicbuildingsystembydecomposing lightsthepotentialofusingspatiotemporalgraphmodelstocaptureand
the heat transfer processes. Then, they adopted a sequence-sequence analyze the complex interactions of buildings, further promoting sus-
encoder-decoder model structure, where the encoder and current tainabledevelopmentintheurbanscale.
Gated Recurrent Unit (GRU) cells act as feature extractors to capture NODEsContinuousOrdinaryDifferentialEquations(ODEs)naturally
pastandcurrentinformation,whilethedecoderGRUcellsrepresentthe represent physical systems that evolve continuously over time, accu-
|     |     |     |     |     |     |     |     | rately capturing |     | their underlying |     | dynamics. | The continuous-time |     | rep- |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ---------------- | --- | --------- | ------------------- | --- | ---- |
predictedsystemdynamics(Fig.6c).TheModNNpredictionresultsfor
resentationofODEsismathematicallydescribedas:
| indoor temperature | closely | align | with | the measured |     | values, | with an |     |     |     |     |     |     |     |     |
| ------------------ | ------- | ----- | ---- | ------------ | --- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
◦C
| av e r ag e M | A E o f 0 .4 3 | a n d a | n M A P E | o f 1 .9 | 3 % . I t | o ut pe r fo | r m s t he | dy(t)        |     |     |     |     |     |     |     |
| ------------- | -------------- | ------- | --------- | -------- | --------- | ------------ | ---------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
|               |                |         |           |          | ◦C        |              |            | =f(y(t),t,θ) |     |     |     |     |     |     |     |
3 R 2 C m o de l, w h ic h h as an a v er a ge M A E o f 0 .9 4 a n d a M A P E o f 3 .9 % . (13)
dt
| Additionally, | the ModNN | model | demonstrates |     | greater | robustness |     |     |     |     |     |     |     |     |     |
| ------------- | --------- | ----- | ------------ | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
compared to the LSTM model. The MAPE of the ModNN model for where t is time; y is the target variable; θ is the parameter matrix
temperaturepredictionis1.7%withboth60-dayand30-daytraining determined by the characteristic of the systems. Common numerical
data,whiletheMAPEfortheLSTMmodelis1.9%with60-daytraining
methodsforsolvingODEsincludetheEulerandRunge-Kuttamethods.
| data and | 2.2 % with 30-day | training |     | data. By | incorporating |     | physical |     |     |     |     |     |     |     |     |
| -------- | ----------------- | -------- | --- | -------- | ------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Interpretingresidualnetworks(ResNets)asEulerdiscretizationofODEs,
knowledge,theproposedModNNmodelexhibitssuperiorperformance
Chenetal.proposeddata-drivencontinuous-timemodelscalledNeural
| inpredictingindoorairthermaldynamics. |     |     |     |     |     |     |     |               |     | [111–113] |       |            |     |         |          |
| ------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --------- | ----- | ---------- | --- | ------- | -------- |
|                                       |     |     |     |     |     |     |     | ODEs (NODEs). |     |           | (Fig. | 8a). NODEs | aim | to find | a neural |
GNNsAnothertypicalparadigmforintegratingphysicsknowledge networkthatapproximatesfinODEs(Fig.8b).IntheNODEframework,
10

Z.Maetal. Applied Energy 381 (2025) 125169
Fig.7. Physics-informedarchitecturaldesignforGNNs.(a)Thermalzonesoftargetbuildinganditsgraphicrepresentation[88].(b)Establishedurbannetworkwith
knownnodeandedgefeaturevectors.[89](c)MethodologyframeworkofapplicationoftheST-GCNmodel[90].
Fig.8. NeuralODEsinphysics-informedarchitecturaldesign.(a)StructuralillustrationoftheResNet.Bysubstitutingtheactivatedfunctionwithaparticularf,the
propagationofResNetcanberegardedasanODEsolver.(b)Reverse-modedifferentiationofanODEsolutionforoptimizingthelossfunction.[113].(c)Performance
ofdifferentmodelsforpredictingindoortemperaturewithmissingdataprobabilityof25%,50%,and75%[87].LNODE:latentNODE;SSM:state-spacemodel;CE:
modelwithcontinuousencoder.
11

Z.Maetal. Applied Energy 381 (2025) 125169
neuronsrepresentthephysicaldynamicsateachtimestep,embedding buildings.Inthismodel,thesolarheatgainofabuildingisdetermined
specific physical information into the network. Zakwan et al. [114] by solar irradiance obtainedfrom weather data. However, physically,
proposed a potential application of NODE for modeling the thermal thesolargainofabuildingdependsnotonlyonweatherdata(e.g.,direct
dynamics of buildings.Theyconceptualized a buildingas a systemof anddiffuseirradiance[115]),butalsoonbuildingparameterssuchas
interconnected thermal zones exchanging energy both internally and windowareaandbuildingorientation[116–118].Additionally,thein-
withtheexternalenvironment,influencedbyheating,cooling,andsolar fluence of solar heat gain on heating and cooling energy is opposite:
radiation.However,thisconceptispresentedasahigh-leveloverview, solar gain reduces heating demand but increases cooling demand. To
indicating fertile ground for future research into the application of addresstheselimitations,Mirfinetal.[86]addedasolargaintermtothe
NODEsinBEM.Tabogaetal.[87]developedcontinuous-timemodels traditionallinearregressionTime-Of-WeekTemperature(TOWT)model
based on NODE for predicting and controlling HVAC operations and and proposed the Time-Of-Week, Solar, and Temperature (TOWST)
indoorenvironment.Theresultsshowthatthecontinuous-timemodels modelforbuildingenergyconsumptionmodeling:
outperformdiscretemodelswhentrainedonsmalldatasets.Theyalso ⎧
incorporatedaphysics-informedstructureintotheNODE: ⎪⎪⎨ch +αTxt (cid:0) βTT t c(cid:0) γTRt (θ)+ϵ t , ϕ t =(cid:0) 1,
[ z z T ϵ ( ( t t ) ) ] = ⎡ ⎢ ⎣ 1 (Qθ (x(t),u(t P ), θ ( d x ( ( t) t) ) , + u( η t) (t , ) d P ( θ t ( ) x ) (t),u(t),d(t))) ⎤ ⎥ ⎦dt (14) Et = ⎪⎪⎩ c c c 0 + + α α T T x x t t + + β ϵ T t , T t c+γTRt (θ)+ϵ t , ϕ ϕ t t = = + 0, 1, (17)
Cp
whereEtistheenergyconsumption;cistheconstantterm;αTxtisatime-
where zϵ (t) is the HVAC energy consumption term; zT (t) is the zone related piecewise constant function; βTT t c is a temperature-related
temperatureterm.Pθ andQθ aretwodimensionlessfunctions.Pθ rep- piecewise linear function; γTRt is the solar gain term, determined by
resentsHVACenergypowerconsumption;Qθisheatexchangeswiththe thewindowareamatrixγT andbuildingorientationmatrixRt;θisthe
outdoorandheatemittedbyappliance;η(t)istheefficiencyofHVAC buildingorientationangleinmatrixRt;ϕ
t
representstheHVACstates,
systems.Thisstructurereflectstheenergyconservationlaw:tempera- with (cid:0) 1 indicating heating, +1 indicating cooling, and 0 indicating
turefluctuationswithinathermalzone(Cp d
d
T
t
)resultfromHVACenergy neither heating nor cooling; ϵ t is the white noise; In this model, pa-
consumption(η(t)P(t))andinternal/externaldisturbance(Q(t)).How- rametersthatneedtobefittedincludeαT,βT,γT,θ,andϕ
t
iftheHVAC
ever,thisstructuredmodeldidnotresultinbetterpredictionaccuracy.A
systemstatesareunknown.ThisTOWSTmodeldemonstratesa30%–72
possiblereasonforthecompromisedpredictionaccuracyisthatNODEs %reductioninMSE,illustratingtheeffectiveincorporationofsolarheat
aredesignedtocapturethephysicaldynamicsofsystemsgovernedby gain into a data-driven model for predicting building energy
unique ODEs. However, the thermal dynamics in buildings are influ- consumption.
enced by time-related external and internal disturbances, such as
weather conditions and stochastic occupant schedules, leading to 5.2. Physics-basedmodelsempoweredwithdata-drivencomponents
varying ODEs. Nevertheless, the physics-informed structure improves
themodelperformanceinextrapolationscenarioswhere50%and75% Inadditiontomodifyingthearchitecturaldesignofhiddenlayersin
ofdataismissing(Fig.8c),demonstratingenhancedrobustnessthrough data-driven models to integrate physics knowledge, physics-based
theincorporationofphysicalknowledge,suchastheenergyconserva- models can also be enhanced by incorporating data-driven compo-
tionlaw,intoarchitecturaldesign. nents.Forexample,incurrentstate-spacemodelsusedasphysics-based
LinearmodelsInadditiontoneuralnetwork-basedmodels,physical models of buildings, the relationships between state parameters are
knowledgecanalsobeintegratedintolinearmodels,wherelinearterms usually simplified to be linear, which can compromise prediction ac-
canbeassignedspecificphysicalmeanings.Bünningetal.[85]proposed curacy.A potentialsolutionis toincorporatedata-driven components
aphysics-informedARMAXmodelthatfitsindoortemperatureusinga intophysics-basedmodelstocapturenonlinearbehaviorsthatarenot
linearfunctionofhistoricaldata.Thismodelbeginswiththeevolution capturedbytraditionalphysics-basedmodels.
ofindoortemperatureandderivesastate-spacefunctionasfollows: Inphysics-basedmodelsofBEM,certainsimplificationsofphysical
( )
∑τ (cid:0) ) rules(e.g.,thelinearassumptioninstatespaceequations)aretypically
Tk+1 =̃θ autoTk +̃θ ambTamb,k +̃θ nTn,k + ̃θ sol,ti Ivert,ti +̃θ actb Tsup (cid:0) T
k
applied,butthesesimplificationscancompromisetheaccuracyofthese
ti=t1 models in realistically reflecting the real-world dynamics of building
(15) operation. Atypical exampleis thelinear ODEsor partial differential
equations (PDEs) to model the dynamics of air temperature, building
whereTk istheindoortemperatureattimestepk;Tamb istheambient envelope,andHVACsystemenergyconsumption[119,120],suchasRC
temperature;Tnisthetemperatureofneighboringzones;Ivertisthesolar modelsforbuildingmodeling.Theseassumptionscanleadtoinaccur-
irradiationonaverticalsurface;Tsupisthesupplyairtemperature;Tis aciesandmayoversimplifythecomplexthermaldynamicsofbuilding
the approximate zone temperature, obtained from the last measured operations. By integrating data-driven components into ODEs, it is
roomtemperature;bisthevalveopeningnumber;
̃θ
auto,
̃θ
amb,
̃θ
n,
̃θ
sol,and possibletomoreeffectivelycapturethesenonlinearbehaviors,resulting
̃θ act are coefficients. These coefficients represent the influence of inmoreaccuratemodels.Incontrol-orientedBEM,ODEsusuallyneedto
different factors on room temperature and should be positive, as be converted into a finite difference form to facilitate model training
demonstratedbyapplyingEq.17recursively(i.e.,inam(cid:0) ulti-step)state- using measured data [5,8]. This process, known as discretization,
spacemodel)[76,77].Next,thetermsofTk andTn,k,b Tsup (cid:0) T
k
,and transforms the state-space representation into a discretized format. A
typicaldiscretizedstate-spacerepresentationisexpressedas:
terms of Tamb,k and Ivert,ti can be rearranged into vectors representing
state (x), input (u), and disturbance (d), respectively, resulting in the xt+1 =Axt +Buut +fd (dt ),
correspondingARMAXmodel:
yk+1 =Θ[yk ⋯yk(cid:0)δuk ⋯uk(cid:0)δdk ⋯dk(cid:0)δ ] (16)
yt =Cxt ,
However,therelationshipbetweenthepredictedstatext+1 andthe
whereΘisthevectorofregressioncoefficientsofeachthermalzoneand terms at time t (i.e., statext and input ut) does not need to be linear.
δ is the time lag. The predictive controller based on this physics- Drgonˇa et al. [84] supposed that the function in state-space could be
informed ARMAX model achieves 26 % to 49 % heating and cooling representedbyanANN(Fig.9).TheyproposedadiscretizedODEmodel
energy savings compared to the baseline hysteresis controller in test asfollows:
12

| Z.Maetal. |     |     |     |     |     |     |     |     |     | Applied Energy 381 (2025) 125169  |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- |
Fig.9. Discretizedstate-spacerepresentationofODEs.(a)State,input,anddisturbancevectorsinbuildingenergymodel[84].(b)Fittingthestate-spacefunction
withANN[84].
| xt+1 =fx (xt                            | )+fu (ut         | )+fd (dt      | )           |                        |            |                 | (18)    |     |     |     |     |
| --------------------------------------- | ---------------- | ------------- | ----------- | ---------------------- | ---------- | --------------- | ------- | --- | --- | --- | --- |
| yt =fy (xt                              | )                |               |             |                        |            |                 | (19)    |     |     |     |     |
| (cid:0)[                                |                  | ])            |             |                        |            |                 |         |     |     |     |     |
| x0 =f0                                  | y1(cid:0)N ;⋯;y0 |               |             |                        |            |                 | (20)    |     |     |     |     |
| where fx,                               | fu, and          | fd represent  | the neural  | network                | components |                 | of the  |     |     |     |     |
| overall system                          | model,           | corresponding | to          | state,                 | input,     | and disturbance |         |     |     |     |     |
| dynamics,respectively.Theinitialvaluex0 |                  |               |             | ismappedfromhistorical |            |                 |         |     |     |     |     |
| data by                                 | f0. Compared     | to linear     | state-space | equations,             |            | the MSE         | of the  |     |     |     |     |
| predicted                               | zone temperature |               | is reduced  | by approximately       |            | 10              | %, from |     |     |     |     |
0.5266Kto0.4720K.
Inadditiontostate-spacemodels,data-drivenapproachescanalso
serveasintegralcomponentsinmodelingindoorairdynamics.Sonetal.
| [91] developed | a   | PIML model | that integrates |     | data-driven |     | modeling |     |     |     |     |
| -------------- | --- | ---------- | --------------- | --- | ----------- | --- | -------- | --- | --- | --- | --- |
withinaphysics-basedframeworktoassessthesensitivityandcontri-
| butions of | various | factors | on the air | change | rate (ACR). | The | rate of |     |     |     |     |
| ---------- | ------- | ------- | ---------- | ------ | ----------- | --- | ------- | --- | --- | --- | --- |
changeinindoorcarbondioxide(CO2)concentrationcanberepresented
as:
| d C in=ACR•(Cout |     | (cid:0) )+S | ˙   |     |     |     |      |     |     |     |     |
| ---------------- | --- | ----------- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
|                  |     | Cin         |     |     |     |     | (21) |     |     |     |     |
d t
| whereCin | isindoorCO2concentration;Cout |     |     | isoutdoorCO2concentra- |     |     |     |     |     |     |     |
| -------- | ----------------------------- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |
˙=nm˙/VistheCO2emissionrate
tion;ACRistheairchangerate[1/h];S
m˙
due to respiration per unit time; n is number of occupants; is CO2 Fig.10. Modelintegrationtopredicttherateofchangeinindoorcarbondi-
emissionrateperoccupant;Vistheeffectivevolumeofthebuilding.As oxideconcentration.NR:thenumberofoccupants;AP:operationalstatusofthe
showninFig.10,ANNspredictthetime-dependentACRusinginputs airpurifier;AC:operationalstatusoftheairconditioner,WS:windspeed;WD:
| like occupant  | count | and wind | speed.          | By integrating |         | Eq. 19    | with the | winddirection. |     |     |     |
| -------------- | ----- | -------- | --------------- | -------------- | ------- | --------- | -------- | -------------- | --- | --- | --- |
| time-dependent | ACR,  | the      | model generates | a              | history | of indoor | CO2      |                |     |     |     |
concentration,whichcanbecomparedwithmeasuredindoorCO2levels
|     |     |     |     |     |     |     |     | 6. Physics-informedensemblemodels |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- |
toiterativelyadjusttheweightsandbiasesofneuralnetwork.ThisPIML
| model offers | essential    | capabilities | for                    | predicting | ACR,       | enabling | the    |                        |                  |                    |               |
| ------------ | ------------ | ------------ | ---------------------- | ---------- | ---------- | -------- | ------ | ---------------------- | ---------------- | ------------------ | ------------- |
|              |              |              |                        |            |            |          |        | Physics-informed       | ensemble models, | which combine      | physics-based |
| preparation  | of optimized |              | ventilation schedules, |            | evaluating | new      | venti- |                        |                  |                    |               |
|              |              |              |                        |            |            |          |        | models and data-driven | models in        | joint predictions, | are a pivotal |
lationsystems,andcomparingventilationperformanceacrossdifferent
approachinPIML.Therationalebehindthismethodisthattraditional
spaces. physicalmodelsexcelatsimulatinglong-termphysics-drivenprocess(e.
13

Z.Maetal. Applied Energy 381 (2025) 125169
g.,heattransfer),whereasthedata-drivenmodelsarebetteratcapturing observation [122–124]. These discrepancies are partly attributable to
the hidden and stochastic dynamics over shorter periods (e.g., indoor model deficiencies, unexpected system operation conditions, and sto-
activities and associated implications on building energy use) [49]. chastic occupant activities and internal heat gains during building
These stochastic interactions are present across multiple scales of operation [92], such as the occupant and appliance usage schedule,
buildingenergyprediction,fromsub-systemscaletoindividualbuilding posing challenges for physical governing equations to capture effec-
scaleandurbanscale.Therefore,physics-informedensemblemodelsare tively. Ma et al. [92] demonstrated the successful decomposition of
promisingastheyharnessthestrengthsofbothphysics-basedanddata- whole building energy use into physics-driven component, occupant-
drivenmodels,ultimatelyimprovingtheaccuracyandinterpretabilityof driven component, and white noise based on correlation and white
buildingenergyconsumptionpredictions. noiseanalysis(Fig.11).Theresidualsbetweenphysics-basedsimulated
Sub-system level Building subsystems include elements such as and observed data are identified as composed of occupant-driven
buildingenvelopes,HVACsystems,andlighting.Thebehaviorofthese componentandwhitenoise.Data-driventimeseriesmodelswerethen
systems can be challenging to fully capture using physical equations appliedtocapturetheseresidualsandintegratedwiththephysics-based
alone. For example, developing physics-based models for refrigerant model to predict building thermal load. Compared to traditional
flow in HVAC systems is difficult due to the unavailability of online physics-basedmodels,theproposedensemblemodelachievedaccuracy
operationalparameters.Yueetal.[93]exploredanensemblemodelto improvement of 40–90 % in both MAE and CV-RMSE compared to
predict the energy consumption of variable refrigerant flow systems. purely physics-based models. Additionally, the ensemble model
TheysimulatedthecoolingloadofabuildingusingtheRCmodeland demonstratedenhancedrobustnessoverpuredata-drivenmodels;with
estimated operational parameters of building systems, such as high only10%oftheannualdatasetfortraining,ityieldedCV-RMSEvalues
pressure,lowpressure,andcompressorfrequency,usingMLRandANN of0.300forcoolingand0.172forheatingpredictions,whereastheCV-
models.ThismodelachievedaCV(RMSE)of24.65%andanR2of0.9. RMSEofLSTMmodelwas1.231forcoolingand0.412forheating.This
Individual-buildinglevelInbuilding-scaleenergyprediction,physics- robustness suggests that the physics-informed ensemble model holds
based models are widely used, though significant discrepancies of up significantpotentialforextrapolationscenarios.
to175%havebeenobservedbetweensimulatedandobservedenergy Dong et al. [83] combined five data-driven models (e.g. ANN and
data[121].Evenwithelaboratebuildingenergycalibration,thereare SVM) with the 2R1C model to enhance the prediction of energy con-
always performance gaps exist between calibrated models and sumption in residential buildings. The workflow, shown in Fig. 12,
Fig.11. Physics-basedensemblemodelbasedonresidualmodelingforbuildingthermalloadprediction.
14

| Z.Maetal. |     |     |     |     |     |     |     |     |     |     |     |     | Applied Energy 381 (2025) 125169  |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- |
Fig.12. Theworkflowanditerationofthephysics-informedensemblemodelforbuildingenergyconsumptionprediction[83].
beginswiththe2R1Cthermalnetworktomodelthethermaldynamicsof showninFig.13.Theoccupantconditionsaredividedintotwostages:
indoortemperatureasfollows: stageArepresentsthe“justentered”phase,characterizedbymetabolic
( ) rate,andstageBrepresentsthe“alreadyentered”phase,characterized
|     |     | ∑ n |     |     | ∑ n |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
d T Z=(cid:0) 1 + 1 + 1 + 1 + T i + T o+ T o + Tg +Qint +Qac b y sk i n te m p e r atu re . F ir s t , a c t u al the r m a l c o m f o rt v o t e s a re c ol l e ct e d ,
| CZ  |     |        |       |         | TZ  |       |          |     |     |     |     |     |     |     |     |
| --- | --- | ------ | ----- | ------- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | d t | i= R i | R w R | inf R f | i=  | R i R | w R in f | R f |     |     |     | ̃   |     | ̃   |     |
1 in 1 i n an d t h e la b e le d m e ta b o l i c r a t e M a n d s k i n t e m pe r a t u r e T s k f o r t h e
|     |     |     |     |     |     |     |     | (22) | regressionmodelareobtainedbyminimizingtheerrorbetweenactual |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | ----------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
andpredictedcomfortvotes:
| whereCZ        |     | istheheatcapacityofairinthetargetzone;TZ          |     |     |     |     |     | isthezone |                           |      |          |     |     |     |      |
| -------------- | --- | ------------------------------------------------- | --- | --- | --- | --- | --- | --------- | ------------------------- | ---- | -------- | --- | --- | --- | ---- |
| temperature;Ri |     |                                                   |     |     |     |     |     |           | M ̃(k)=argmin(V(k)(cid:0) |      | V ̂(k))2 |     |     |     | (24) |
|                |     | in isthehalfoftheconductivethermalresistanceofthe |     |     |     |     |     |           |                           | M(k) |          |     |     |     |      |
ithwall;Rwisthetotalthermalresistanceofwindows;Rinfisthethermal
re s i st a n ce o f in fi l t ra t io n ; R i s h a l f o f t h e t h e r m a l r e s is t a n c e o f t h e ̃ (k)=arg (V(k)(cid:0) ̂(k))2,
|       |             |             |              | f          |              |            |              |                        | T sk | m i n     | V   |     |     |     | (25) |
| ----- | ----------- | ----------- | ------------ | ---------- | ------------ | ---------- | ------------ | ---------------------- | ---- | --------- | --- | --- | --- | --- | ---- |
| g r o | u n d fl oo | r ;T ii s t | h e c e n te | r te m p e | r a tu r e o | f th e i t | h w a ll ; T | i s t h e o u ts i d e |      | T sk ( k) |     |     |     |     |      |
o
| te m | p e ra tu | r e ;T is | t h e t e m | p e r a t ur | e o f g r o | u n d fl o | o r ; Q | i s th e in t e r n a l |     |     |     |     |     |     |        |
| ---- | --------- | --------- | ----------- | ------------ | ----------- | ---------- | ------- | ----------------------- | --- | --- | --- | --- | --- | --- | ------ |
|      |           | g         |             |              |             |            | i n t   |                         |     |     |     |     |     |     | ̂(k)is |
wherekisthetimestep;V(k)istheactualthermalcomfortvote;V
| h e | at g a in d | u e to o cc | u p a n c | y ( b o d y h | ea t , a p | p li a nc e | u s a g e s , | a n d li gh t , e t c. ) , |               |         |         |            |             |       |        |
| --- | ----------- | ----------- | --------- | ------------- | ---------- | ----------- | ------------- | -------------------------- | ------------- | ------- | ------- | ---------- | ----------- | ----- | ------ |
|     |             |             |           |               |            |             |               |                            | the predicted | thermal | comfort | vote based | on Fanger’s | model | [127], |
Qac istheHVACcoolingload.Withinthemodel,thestochasticpartof
|     |     |     |     |     |     |     |     |     | whichisafunctionofM(k)andTsk |     |     | (k).Theselabeledparameters,along |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------------------------- | --- | --- | -------------------------------- | --- | --- | --- |
buildingenergyusageQintiscapturedbydata-drivenmodels,whileQac
withotherinputfeaturessuchasoutdoortemperatureandrelativehu-
| is  | fitted using | ordinary |     | least squares | as  | described | by  | the following |     |     |     |     |     |     |     |
| --- | ------------ | -------- | --- | ------------- | --- | --------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
̃ ̃
equation: midity,arethenfedintotheregressionmodeltopredictMandTsk for
̂
(cid:0) ʹ ʹ ʹ ) (cid:0) ) t h en ex t t i m e ste p . F in a ll y , t h e p r ed i c te d t he r m a l c o m f o r t vo t e s V ( k + 1 )
| Qac | = a+bTo | +cT | 2+dT | +eT 2+fTOT |     | ⋅ g+hFr | +iF 2 | (23) |     |     |     |     |     |     |     |
| --- | ------- | --- | ---- | ---------- | --- | ------- | ----- | ---- | --- | --- | --- | --- | --- | --- | --- |
o Z Z Z r a re ca lc u l a te d u si n g F a n g e r ’ s m o d e l w it h t h e p r e d ic t e d m e t a b ol i c ra te
|     | ʹ   |     |     |     |     |     |     |     | ̂(k+1) |     |     | ̂ (k+1). |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | -------- | --- | --- | --- |
whereT isthechangeofreturnzoneairtemperature;Fristheratioof M and skin temperature T sk If an occupant provides a
Z
actualflowcomparingtofullloadflow;a∼iaretheparametersneeded thermalcomfortvoteafterprediction,thisnewvoteisusedtoupdatethe
trainingdatasetandrefinethemodel.Comparedtothethermalcomfort
tobeestimated.AsshowninFig.12,eachiterationwithintheextended
|     |     |     |     |     |     |     |     |     | level predicted | by  | Fanger’s | model and data-driven | models | alone, | this |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | -------- | --------------------- | ------ | ------ | ---- |
Kalmanfilterprocess[125]involvescalculatingQacusingthepredicted
hybridmodeldemonstratesareductioninRMSEbyapproximately40%
zonetemperatureTZfromthepreviousiteration.ThisQacisthenusedas
and10%,respectively,indicatingsignificantimprovementsinpredic-
| input        | to the | ODE  | to update  | the   | zone          | temperature | TZ.         | The results |                |       |         |           |               |                |     |
| ------------ | ------ | ---- | ---------- | ----- | ------------- | ----------- | ----------- | ----------- | -------------- | ----- | ------- | --------- | ------------- | -------------- | --- |
|              |        |      |            |       |               |             |             |             | tion accuracy. | These | results | highlight | the potential | of integrating |     |
| demonstrated |        | that | the hybrid | model | significantly |             | outperforms | purely      |                |       |         |           |               |                |     |
physicalinsightswithMLtechniquestoprovidearobustandaccurate
data-drivenmodels,withthecoefficientofvarianceby6–10%forhour-
thermalcomfortprediction.
aheadforecastingand2–15%forday-aheadforecasting.
Another challenge at the individual building level is accurately Additionally, building infiltration is another critical component to
predictingoccupantthermalcomfort,whichisdeterminednotonlyby modelaccuratelyinindividualbuildings.Zhangetal.[95]developeda
heat balance of the human body, but also by implicit psychological hybrid methodology that combines ML-based classification algorithm
factors [126]. This complexity presents an opportunity for physics- withgrey-boxsub-modelingtoenhancetheaccuracyandgeneralization
ofcommonlyusedgrey-boxinfiltrationmodels.Theinfiltrationmodelis
| informed |     | ensemble | models | to enhance | prediction |     | performance. | Zhou |     |     |     |     |     |     |     |
| -------- | --- | -------- | ------ | ---------- | ---------- | --- | ------------ | ---- | --- | --- | --- | --- | --- | --- | --- |
expressedasfollows:
| et      | al. [94] | developed | a   | model to        | dynamically |                | predict | the personal |     |     |     |     |     |     |     |
| ------- | -------- | --------- | --- | --------------- | ----------- | -------------- | ------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
| thermal | comfort  | through   |     | online learning |             | and regression |         | modeling, as |     |     |     |     |     |     |     |
15

| Z.Maetal. |     |     |     |     |     |     | Applied Energy 381 (2025) 125169  |     |
| --------- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- |
Fig.13. Theframeworkofthephysics-informedensemblemodelforpersonalthermalcomfortprediction[94].
Infiltration=A+B(Tzone (cid:0) )+CVwind +DV 2 the traditional grey-box model and the pure random-forest model in
|             |                  | Toutdoor     | w ind                   | (26)          |                 |                      |           |                |
| ----------- | ---------------- | ------------ | ----------------------- | ------------- | --------------- | -------------------- | --------- | -------------- |
|             |                  |              |                         | extrapolation | scenarios.      | This is particularly | important | for real-world |
|             |                  |              |                         | applications  | of infiltration | models, where        | it may be | impractical to |
| where Tzone | is zone dry-bulb | temperature, | Toutdoor is environment | dry-          |                 |                      |           |                |
bulbtemperature,Vwind iswindspeed,andcoefficientsA,B,C,andD collectinfiltrationdataacrossallpossibleweatherconditions.
aredeterminedviaexperiment.Thishybridmethodologyfirstemploys UrbanlevelUrbanenergypredictioniscomplexduetointeractions
decision-treeclassificationtosplitthedataspaceintoanoptimalnum- amongadjacentbuildings,includingshadingeffects,ventilationinter-
berofsub-spacesbasedonvariousvariablessuchasaveragewindspeed, ference,andsocialnetworks.Xuetal.[96]developedahybridmodel
average indoor dry-bulb air temperature, and average indoor relative that combines the simulation capabilities of EnergyPlus for physics-
humidity. Subsequently, sub-models using the grey-box infiltration based building modeling with an ANN to account for the occupants
equationstructureareconstructedforeachsub-space,withdifferentsets social networks and neighborhood facilities. (Fig. 15). In the hybrid
ofcoefficientscalculatedforeachsub-space(Fig.14).Whilethishybrid model,theinitialstepinvolvescalculatingtheenergyconsumptionof
modeldoesnotshowanadvantageoverthepurerandom-forestmodel buildingsbyEnergyPlus,representingthephysics-basedcomponentof
whenthetrainingdatasetspansnearlyafullyear,itoutperformsboth themodel.Subsequently,themodelincorporatesasocialdimensionby
Fig.14. Diagramofthedevelopedphysics-informedensemblemodelappliedtoasampledatasetforbuildinginfiltrationprediction[95].
16

| Z.Maetal. |     |     |     |     |     |     |     |     | Applied Energy 381 (2025) 125169  |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- |
Fig.15. Theworkflowofthephysics-informedensemblemodelforurbanenergyconsumptionprediction[96].
considering theenergy savings attributedto theclosenessofrelation- onlyconsiderenergydynamicsofindividualbuildings.
| ships among               | neighbors | [128], resulting | in  | a modified | energy |                         |     |     |     |     |
| ------------------------- | --------- | ---------------- | --- | ---------- | ------ | ----------------------- | --- | --- | --- | --- |
| consumption:              |           |                  |     |            |        | 7. Summaryanddiscussion |     |     |     |     |
| E=E(EnergyPlus)⋅(1(cid:0) | CI⋅3.45%) |                  |     |            | (27)   |                         |     |     |     |     |
Integratingphysicsknowledgeintothedevelopmentofdata-driven
|     |     |     |     |     |     | models represents | a pivotal | advancement | in enhancing | model accu- |
| --- | --- | --- | --- | --- | --- | ----------------- | --------- | ----------- | ------------ | ----------- |
whereCIistheclosenessindex,rangingfrom0to2,representing“no
racyandreliability.Thisintegrationcanbeachievedthroughvarious
| relationship”, | “acquaintance”, | and “friend”, | respectively. |     | The model |     |     |     |     |     |
| -------------- | --------------- | ------------- | ------------- | --- | --------- | --- | --- | --- | --- | --- |
approaches,includingtheincorporationofphysics-basedmodelingin-
assumesanenergysavingsof3.45%foreachunitincreaseinCI.Then,
|     |     |     |     |     |     | puts, regularization | in loss | functions, | transformations | in model archi- |
| --- | --- | --- | --- | --- | --- | -------------------- | ------- | ---------- | --------------- | --------------- |
thetotalCImatrixofhouseholdsiscalculatedbasedonsocialnetworks
andurbancharacteristics,particularlyfocusingonaffiliationsstemming tecture,andfusionofphysics-basedmodelswithdata-drivenapproaches
from demographic data and connections to community hubs such as throughensemblelearning,assummarizedinthisreview.Theprosand
consofeachmethodaregiveninTable3.AsillustratedinFig.16,the
church,elementaryschool,andhighschool.Finally,anANNisapplied
|          |                       |              |     |            |           | types of physics             | information | that                | can be encoded | into data-driven |
| -------- | --------------------- | ------------ | --- | ---------- | --------- | ---------------------------- | ----------- | ------------------- | -------------- | ---------------- |
| to model | theenergy consumption | withfeatures |     | suchas the | operative |                              |             |                     |                |                  |
|          |                       |              |     |            |           | models forimprovementinclude |             | simulationoutcomes, |                | physics princi-  |
temperatureTop,outdoortemperatureTout,solarheatgainQs,andheat
|     |     |     |     |     |     | ples, and physics | constraints | or rules. | The adaptation | of data-driven |
| --- | --- | --- | --- | --- | --- | ----------------- | ----------- | --------- | -------------- | -------------- |
gainfromoccupantsQo:
(cid:0) ) models, predominantly through ANNs, RNNs, and GNNs, leverages
E=f Top ,Tout ,Qs ,Qo ,CI (28) this physics information to enhance prediction accuracy. Ensemble
learningprovidesadditionalflexibility,allowingresearcherstoexplore
| The results | reveal that | acknowledging | the influence | of  | residents’ |                       |     |              |           |                    |
| ----------- | ----------- | ------------- | ------------- | --- | ---------- | --------------------- | --- | ------------ | --------- | ------------------ |
|             |             |               |               |     |            | various methodologies | for | representing | different | physical and data- |
socialinteractionsonenergyconsumptionpatternscanunlockpotential drivencomponentswithinamodel.Thissectionoffersdiscussionsand
%–30
| energy savings | of 20 | % compared | to baseline | assessments | that |     |     |     |     |     |
| -------------- | ----- | ---------- | ----------- | ----------- | ---- | --- | --- | --- | --- | --- |
17

| Z.Maetal. |     |     |     | Applied Energy 381 (2025) 125169  |
| --------- | --- | --- | --- | --------------------------------- |
Table3
SummaryofPIMLapproachesintheapplicationforBEM.
| Methods | Physicalinformation | Data-drivenmodel | Pros | Cons |
| ------- | ------------------- | ---------------- | ---- | ---- |
Usefulwhenmeasurementdatais
Physics-informedinput Simulationdata MLR;ANNs;LSTM;DT;GAN scarceorcostly Featureredundancy
|                         |             |                 | Maintainsphysicallyplausible | Physicallawsareonlyapproximately |
| ----------------------- | ----------- | --------------- | ---------------------------- | -------------------------------- |
| Physics-informedoutputs | Physicrules | ANNs;Q-learning |                              |                                  |
|                         |             |                 | predictions                  | satisfied.                       |
Physics-informed PhysicsKnowledgeand LSTM;ANNs;SVM;GPR;GMM; Strictlyenforcesphysicsrulesor Simplicityofcurrentphysicsrules
| architecturaldesign | physicsrules   | ARMAX;CDE;GAT;GCN   | knowledge            |                              |
| ------------------- | -------------- | ------------------- | -------------------- | ---------------------------- |
| Physics-informed    |                |                     |                      | Challengesinunderstandingthe |
|                     | Simulationdata | ANNs;MLR;KNR;SVM;DR | Highinterpretability |                              |
| ensemblemodels      |                |                     |                      | contributionofeachcomponent  |
Fig.16. Physicsinformationanddata-drivenmodelsinthePIMLforBEM.
Fig.17. PhysicalknowledgeandhiddenrelationshipsinPIML.
18

Z.Maetal. Applied Energy 381 (2025) 125169
insightsonPIMLapplicationsinBEM.First,ahigh-levelunderstanding advantageofPIMLfromtheperspectiveofdata-drivenmodeling.Asa
ofPIMLmodelsispresentedfromamodelingperspective.Then,chal- result, PIML holds promise as an important convergent modeling
lengesandfutureresearchdirectionsareexploredfordifferentmethods, approach in BEM, leveraging the strengths of both physics-based and
categorizedbytheinformationinvolvedinphysics-informedinputs,the data-driven models. By complementing each other, these approaches
integrationofphysicalrulesinlossfunctionsandstructuraldesign,and canachievemoreaccurateandreliablemodelingofbuildings.
the identification of stochastic components within ensemble frame-
works.Finally,theevaluationofPIMLmodelsisdiscussed,withafocus • Informationinvolvedinphysics-informedinputs
ontheselectionofpriorphysicsknowledge,aswellasrobustnessand
uncertaintyassessment. Physics-informedinputsareparticularlyvaluablewhendataavail-
ability is limited. To predict observed building energy consumption,
• PIMLinbuildingenergymodeling simulatedenergyuseiscommonlyemployedasadditionalfeaturesin
data-drivenmodels.Theseinputs,derivedfromphysics-basedmodels,
As shown in Fig. 17, physical phenomena inherently contain so- areexpectedtohelpthetrainedPIMLmodelbetterapproximatesystem
phisticatedphysicsrules,yetnomodelcanperfectlyreplicatethesedue behavior by learning from simulation data. However, it has been re-
to either complexity of these principles (which may not be fully un- portedthatincreasingthenumberoffeatureswithsimulationresultscan
derstood)ortheexcessivecomputationaldemandsrequiredforaccurate possiblyleadtoadecreaseinmodelaccuracy[97].Oneprimaryreason
modeling.Forexample,althoughthehigh-fidelityphysics-basedEner- forthisobservationisthatinaccuratebuildinginformation(e.g.,build-
gyPlusmodelsarewell-developedintermsofheattransferandthermal ingenvelopeoroperationsettings)maybeusedtogeneratethesimu-
dynamicsofbuildings,theystillstruggletoaccuratelydescribeoccupant lationdata,leadingtobiasedinformationthatcanresultinadeclinein
behaviorandnon-uniformdistributionofindoorair(bothtemperature accuracy. Another possible reason for the compromised accuracy is
andvelocity).InEnergyPlus,occupantbehaviorisdeterminedbypre- overfittingcausedbyinformationredundancy.Simulateddataishighly
designed schedules, which cannot fully capture dynamic real-world dependent on weather conditions and building physics parameters,
conditions. Furthermore, calculating the distribution of indoor air whicharetypicallyalreadyincludedasinputsintheoriginaldata-driven
temperature and velocity relies on the CFD module. While there are models. As a result, using simulated data as additional features in-
severalco-simulationplatformsforEnergyPlusandCFD[4,129],they troducesduplicateinformation.Apotentialsolutiontothisissueisto
are associated with heavy computational loads. In physics-based betteranalyzeandunderstandtherelationshipbetweensimulateddata
modeling, certain levels of simplifications are typically necessary to and the features used in traditional data-driven models. By excluding
managesystemcomplexity,leadingtoatrade-offbetweenaccuracyand redundantfeatures(thosehighlycorrelatedwithsimulateddata)while
computationalefficiency.However,suchsimplificationcancompromise retaininguseful,independentones,thepredictionperformancecouldbe
thefidelityofmodelsinrealisticallyreflectingthereal-worlddynamics enhanced.
of physical systems (e.g., RC models). Data-driven models offer a
promisingsolutionbydirectlycorrelatingdrivingfactorswithdesired • Physicalrulesinphysics-informedlossfunctionsandstructural
outcomes through mathematical relationships between model inputs design
andoutputs.Thisapproachisparticularlyusefulforcapturingcomplex
orunknownphysicalphenomena,helpingtobridgethegapsbetween Integratingphysicalconstrainttermsintothelossfunctionenhances
insufficient physics-based modeling and actual ground truth. This prediction accuracy and helps ensure predictions adhere to physical
perspectiveexplainstheroleofPIMLineffectivelycomplementingand laws. By adding loss terms that penalize the violation of PDEs using
enhancing physics-based modeling, especially when physical mecha- derivatives obtained from auto-differentiation of the neural network
nisms are either not fully understood or too complex to model outcomes,themodelremainsmorephysicallyplausible.However,these
accurately. soft penalty constraints only make predictions closer to physical laws
Ontheotherhand,data-drivenmodelingofaphysicalsystemcan instead of strictly following them, as the loss function tends to be
easilyyieldphysicallyinconsistentpredictionresults,especiallywhen minimized rather than eliminated during training [134]. Despite this
thetrainingdataisincomplete,inaccurate,orlimited,togetherwitha limitation, physics-informed outputs can effectively constrain the
lackofmodelinterpretability.Suchpredictionsfrompuredata-driven boundariesoftargetvariables,improvingtheextrapolationbehaviorof
modelsmayfailtoaccuratelyreflectthedynamicsofphysicalsystems models [72]. Conversely, physics-informed architectural designs use
byviolatingfundamentalphysicsrules,therebyseverelycompromising constrainedweights,cells,andconnectionstostrictlyenforceadherence
their performance in specific applications, e.g., system control. To tospecificphysicsrules,resultinginmorerobusttrainingandenhanced
address this limitation, incorporating physics knowledge, either as interpretability. Currently, the physics rules used in such designs are
additionalconstraintsorinformation,intoMLmodelscanenhancethe relativelysimple,focusingmainlyonthesigncontrolofthestructured
robustnessandinterpretabilityofdata-drivenmodeling.Interpretability output, leavingroomforresearchtodevelopmore comprehensiveal-
inBEMisessentialforbuildingtrustofmodels,ensuringmodelaccu- gorithms to describe specific physics systems. Algorithms designed to
racy, and enabling large-scale application [130–133]. It allows stake- capture the dynamics of building systems would be particularly
holders to understand the reasoning of model predictions, making beneficial.
complex black-box machine learning models more transparent and
reliable. ML models vary in interpretability, ranging from inherently • Identifyingthestochasticcomponentsinensembleframework
interpretablemethods(ante-hoc),suchasMLR,decisiontrees,andrule-
basedmodels,toblack-boxmodelslikeANNandSVMthatrelyonpost- Physics-informed ensemble models emphasize the joint predictive
hocinterpretabilitytechniques.Incorporatingphysicsknowledgeoffers capabilitiesofbothphysics-basedanddata-drivenmodels.Therefore,it
an alternative approach to enhancing interpretability. For instance, iscrucialtoclarifytherolesofthesetwomodelsinapredictiontask.In
decomposing building thermal load data into physics-driven and BEM,physics-basedmodelsproviderobustandaccuratepredictionsfor
occupant-driven components allows an ensemble model to effectively components governed by physics laws. Examples include the cooling
incorporate both physical principles and the stochastic occupant be- loadofcoilsinHVACsystems[93],thethermaldynamicsofbuilding
haviors[92].Suchanapproachenhancesinterpretabilitybyclarifying relatedtotheenvelope[83],andhumanbodyheatbalanceinthermal
the contribution of each component to the predictions, thereby comfortevaluation[94].However,theintroductionofstochasticcom-
improving the model accuracy and robustness while maintaining a ponents in a prediction task is inevitable and poses a challenge for
strong foundation for interpretive analysis. This highlights the physics-based models to capture accurately. These stochastic
19

Z.Maetal. Applied Energy 381 (2025) 125169
components, such as occupant behavior, thermal preference, and demonstratethepotentialrobustnessofPIMLmodels,itisimportantto
experiment-dependent coefficients in empirical equations, are better testthesemodelsinscenarioswithlimiteddatasetsandduringextrap-
suited to be modeled by data-driven approaches. Incorporating addi- olation. Another promising direction is the uncertainty evaluations.
tionalphysicsinformationintothesestochasticcomponentswouldun- Manydecision-makingscenariosrequiremoreinformationthanapoint
necessarilyincreasethecomplexityofdata-drivenmodels.Toeffectively forecastingmodel,whichonlyprovidestheconditionalmean.Instead,a
leveragethedata-drivenmodelswhileavoidingoverlycomplexstruc- probabilisticforecastingmodelthatreturnsthefullconditionaldistri-
tures,itisimportanttodistinguishbetweenstochasticcomponentsand butionismoreuseful[138].PIMLhasthepotentialtointuitivelyreduce
physical ones. Nevertheless, a systematic method for effectively dis- predictionuncertaintybyincorporatingphysicsinformation,whichcan
tinguishing these components within an ensemble framework is still be particularly beneficial in limited data and extrapolation scenarios.
lacking,callingforfutureinvestigation. However,mostexistingstudieshavefocusedonpointforecastswithout
consideringuncertainty.Onlyalimitednumberofstudiesinthebuild-
• PriorphysicsknowledgeselectiontointegrateintoPIML ingmodelingdomainhaveexploredprobabilisticforecasts[139,140].
ThephysicsknowledgeandinformationintegratedintoMLmodels 8. Conclusion
will significantly impact the performance of PIML. For example, the
physicsknowledgeembeddedinsimulationresultsmayhaveadifferent Physics-basedmodelsinBEMbuildondetailedbuildingparameters
hypothesisdistributionfromobserveddata,possiblyduetounrealistic and predefined operational conditions that often fail to fully capture
assumptions in the simulation. Without applying domain adaptation real-world dynamics. Conversely, pure data-driven models, while
methods to mitigate this mismatch, directly utilizing such physics in- effective for certain predictions, face challenges with interpretability
formationmightresultinpredictionfailure[68].Anotherchallengelies andmayyieldphysicallyinconsistentoutputs,hinderingtheiradoption.
inthearchitectural designofneuralnetworks toincorporatephysical This review categorizes PIML approaches for BEM, detailing physics-
constraints.Onecanconsiderconstrainingthevariationoftemperature, informed inputs, loss functions, architectural designs, and ensemble
i.e.,risingorfalling,accordingtotheprovidedHVACcooling/heating models.Simulationdatacanenhanceinputsbutrequirescarefulfeature
powerbyconstructingapositivedefiniteweightedmatrix[76,78].Be- analysis to avoid redundancy and overfitting. Physics-informed loss
sides the constraints on weighted matrix, encoding physics principles functionssoftlypenalizedeviationsfromphysicalprinciples,maintain-
intoneuronsofANNorRNNnetworksisalsopromisingtocoupleneural ing model consistency. Additionally, PIML model structure trans-
networkwithPDEorODE,whosetermsandoperatorscanbetreatedas formationhelpsalignpredictionswithphysicallaws,thoughthescope
functional neurons [135]. In addition, Kolmogorov-Arnold Networks ofincorporatedphysicsknowledgeremainslimited.Ensemblemodeling
(KAN) [136,137] represent another promising step towards interpret- offerabalancebyintegratingdeterministicphysicalcomponentswith
abledeepneuralnetworksbydecomposingcomplexfunctionsintosums stochasticelements,highlightingtheneedforasystematicapproachto
ofsimplerfunctionsforPIMLinBEM.However,determiningthemost distinguishthesecomponentseffectively.Futureresearchshouldfocus
significant prior physics knowledge tobe integrated into the network on deepening the integration of physics laws, refining PIML model
structureremainsanopenquestion.Forexample,modelingresultsofRC evaluation in extrapolation and uncertainty contexts, and optimizing
models can be used as prior physics knowledge in PIML models to prior knowledge selection for enhanced PIML performance in BEM.
approximate building energy balance [70,72]. Depending on the StrengtheningtheseareaswillsolidifyPIMLasafoundationalmethod-
complexity of RC models, in the whole building level, these models ology,fosteringmodelstobeaccurate,generalizable,andinterpretable
generally account for interactions among multiple building systems inBEMapplications.
(HVACs,buildingenvelope,etc.)andexternalenvironment.Thiscould
be challenging for pure data-driven models to capture, as it requires CRediTauthorshipcontributionstatement
accurately and interpretably representing inter-system dependencies
anddynamicenergyflows.Thus,incorporatingsuchphysicsknowledge Zhihao Ma: Writing – review & editing, Writing – original draft,
into data-driven building energy modeling is crucial. However, inte- Methodology, Investigation. Gang Jiang:Writing– review &editing,
grating RC models often becomes unnecessary for specific building Investigation. Yuqing Hu: Writing – review & editing. Jianli Chen:
subsystems,suchaslighting,orsolarpanels,consideringtherelatively Writing–review&editing,Supervision,Conceptualization.
well-understood physical behaviors, simpler boundaries, and minimal
interactionsofthesesystemswithothersystems.Therefore,identifying Declarationofcompetinginterest
the appropriate physics knowledge inclusion to support PIML model
developmentisofsignificancetobefurtherexploredbytheautomated The authors declare that they have noknown competing financial
design of neural networks, such as neural architecture search and interestsorpersonalrelationshipsthatcouldhaveappearedtoinfluence
automaticmodularizationofnetworkarchitectures[56]. theworkreportedinthispaper.
• RobustnessanduncertaintyevaluationofPIMLmethods Dataavailability
ExistingevaluationmethodsforPIMLmodelsinBEMaresimilarto Datawillbemadeavailableonrequest.
thoseusedforassessingpuredata-drivenmodels,typicallyrelyingon
evaluation metrics such as MAE, MSE, MAPE, RMSE, and CV(RMSE). Acknowledgement
While it is reasonable to use these metrics to compare different data-
driven models, considering the importance of prediction accuracy as TheresearchisfundedbytheUSNationalScienceFoundation(NSF).
onedimensionofmodelperformance,theyareinsufficienttocompre- Award title: Elements: A Convergent Physics-based and Data-driven
hensively describe the performance or potential advantages of PIML ComputingPlatformforBuildingModeling(#2311685).
algorithms.PIMLaimstoenhancenotonlypredictionaccuracybutalso
theinterpretability,robustness,andphysicalconsistencyofprediction References
outcomes. For example, Taboga et al. [87] found that while incorpo-
ratingphysics-informedstructuredmodelsintoNODEdidnotimprove [1] Gonz´alez-TorresM,etal.Areviewonbuildingsenergyinformation:trends,end-
uses,fuelsanddrivers.EnergyRep2022;8:626–37.
predictionaccuracyinnormalcases,itdidenhancerobustnesswhenthe [2] P´erez-LombardL,OrtizJ,PoutC.Areviewonbuildingsenergyconsumption
probability of missing training data exceeded 50 %. Therefore, to information.EnergBuild2008;40(3):394–8.
20

Z.Maetal. Applied Energy 381 (2025) 125169
[3] WangY,ShuklaA,LiuS.Astateofartreviewonmethodologiesforheattransfer [41] WangZ,SrinivasanRS.Areviewofartificialintelligencebasedbuildingenergy
andenergyflowcharacteristicsoftheactivebuildingenvelopes.RenewSust useprediction:contrastingthecapabilitiesofsingleandensembleprediction
EnergRev2017;78:1102–16. models.RenewSustEnergRev2017;75:796–808.
[4] TianW,etal.BuildingenergysimulationcoupledwithCFDforindoor [42] KarpatneA,etal.Theory-guideddatascience:anewparadigmforscientific
environment:acriticalreviewandrecentapplications.EnergBuild2018;165: discoveryfromdata.IEEETransKnowlDataEng2017;29(10):2318–31.
184–99. [43] RaissiM,PerdikarisP,KarniadakisGE.Physics-informedneuralnetworks:adeep
[5] WangZ,ChenY.Data-drivenmodelingofbuildingthermaldynamics: learningframeworkforsolvingforwardandinverseproblemsinvolvingnonlinear
methodologyandstateoftheart.EnergBuild2019;203:109405. partialdifferentialequations.JComputPhys2019;378:686–707.
[6] SeddikiM,BennadjiA.Multi-criteriaevaluationofrenewableenergyalternatives [44] MitchellTM.Machinelearning.McGraw-hill;1997.
forelectricitygenerationinaresidentialbuilding.RenewSustEnergRev2019; [45] XuY,etal.Physics-informedmachinelearningforreliabilityandsystemssafety
110:101–17. applications:stateoftheartandchallenges.ReliabEngSystSaf2023;230.
[7] SianoP.Demandresponseandsmartgrids—asurvey.RenewSustEnergRev [46] VadyalaSR,etal.Areviewofphysics-basedmachinelearningincivil
2014;30:461–78. engineering.ResEngDes2022:13.
[8] LiX,WenJ.Reviewofbuildingenergymodelingforcontrolandoperation. [47] WangH,etal.Machinelearning-basedfatiguelifepredictionofmetalmaterials:
RenewSustEnergRev2014;37:517–37. perspectivesofphysics-informedanddata-drivenhybridmethods.EngFract
[9] KeyesDE,etal.Multiphysicssimulations:challengesandopportunities.IntJ Mech2023;284.
HighPerformComputAppl2013;27(1):4–83. [48] GuoS,etal.Machinelearningformetaladditivemanufacturing:towardsa
[10] FerrandoM,etal.Urbanbuildingenergymodeling(UBEM)tools:astate-of-the- physics-informeddata-drivenparadigm.JManufSyst2022;62:145–63.
artreviewofbottom-upphysics-basedapproaches.SustainCitiesSoc2020;62: [49] HuangB,WangJ.Applicationsofphysics-informedneuralnetworksinpower
102408. systems-areview.IEEETransPowerSyst2023;38(1):572–88.
[11] PanY,etal.Buildingenergysimulationanditsapplicationforbuilding [50] RizviSHM,AbbasM.Fromdatatoinsight,enhancingstructuralhealth
performanceoptimization:areviewofmethods,tools,andcasestudies.AdvAppl monitoringusingphysics-informedmachinelearningandadvanceddata
Energy2023;10:100135. collectionmethods.EngResExpress2023;5(3).
[12] ChenY,etal.Physicalenergyanddata-drivenmodelsinbuildingenergy [51] MarianM,TremmelS.Physics-informedmachinelearning—Anemergingtrendin
prediction:areview.EnergyRep2022;8:2656–71. tribology.Lubricants2023;11(11).
[13] WinkelmannF,etal.DOE-2supplement:version2.1E.Berkeley,CA(United [52] CaiS,etal.Physics-informedneuralnetworks(PINNs)forfluidmechanics:a
States):LawrenceBerkeleyNationalLab.(LBNL);1993.Hirsch. review.ActaMechSinica2021;37(12):1727–38.
[14] HerronD,etal.Buildingloadsanlaysisandsystemthermodynamics(BLAST) [53] CaiS,etal.Physics-informedneuralnetworksforheattransferproblems.JHeat
programusersmanual.Volumeone.Supplement(Version3.0).Illinois,IL:US Transf2021;143(6).
ArmyConstructionEngineeringResearchLaboratory(CERL);1981. [54] KashinathK,etal.Physics-informedmachinelearning:casestudiesforweather
[15] CrawleyDB,etal.EnergyPlus:creatinganew-generationbuildingenergy andclimatemodelling.PhilosTransAMathPhysEngSci2021;379(2194):
simulationprogram.EnergBuild2001;33(4):319–31. 20200093.
[16] BrückD.,etal.Dymolaformulti-engineeringmodelingandsimulation.In [55] KarniadakisGE,etal.Physics-informedmachinelearning.NatRevPhys2021;3
proceedingsofmodelica.Citeseer,2002;55-1(cid:0) 55-8. (6):422–40.
[17] ShrivastavaR,KumarV,UntawaleS.Modelingandsimulationofsolarwater [56] MengC,etal.Whenphysicsmeetsmachinelearning:Asurveyofphysics-
heater:aTRNSYSperspective.RenewSustEnergRev2017;67:126–43. informedmachinelearning.arXivpreprint;2022.arXiv:2203.16797.
[18] HarishVSKV,KumarA.Areviewonmodelingandsimulationofbuildingenergy [57] vonRuedenL,etal.Informedmachinelearning-ataxonomyandsurveyof
systems.RenewSustEnergRev2016;56:1272–92. integratingpriorknowledgeintolearningsystems.IEEETransKnowlDataEng
[19] ASHRAE.Standard140–2017:Standardmethodoftestfortheevaluationof 2021;1-1.
buildingenergyanalysiscomputerprograms.2017. [58] DasS,TesfamariamS.State-of-the-artreviewofdesignofexperimentsfor
[20] ISO.52016–1:2017:Energyperformanceofbuildings—Energyneedsforheating physics-informeddeeplearning.arXivpreprint;2022.arXiv:2202.06416.
andcooling,internaltemperaturesandsensibleandlatentheatloads.2017. [59] ChenJ,etal.Areviewofcomputing-basedautomatedfaultdetectionand
[21] JordanMI,MitchellTM.Machinelearning:trends,perspectives,andprospects. diagnosisofheating,ventilationandairconditioningsystems.RenewSustEnerg
Science2015;349(6245):255–60. Rev2022;161.
[22] MaheshB.Machinelearningalgorithms-areview.IntJSciRes(IJSR)[Internet] [60] EnergyPerformanceofBuildings—CalculationofEnergyUseforSpaceHeating
2020;9(1):381–6. andCooling(ENISO13790:2008).2008.
[23] ZhangL,etal.Areviewofmachinelearninginbuildingloadprediction.Appl [61] BrøggerM,BacherP,WittchenKB.Ahybridmodellingmethodforimproving
Energy2021;285. estimatesoftheaverageenergy-savingpotentialofabuildingstock.EnergBuild
[24] MinoliD,SohrabyK,OcchiogrossoB.IoTconsiderations,requirements,and 2019;199:287–96.
architecturesforsmartbuildings—energyoptimizationandnext-generation [62] NutkiewiczA,YangZ,JainRK.Data-drivenurbanenergysimulation(DUE-S):a
buildingmanagementsystems.IEEEInternetThingsJ2017;4(1):269–83. frameworkforintegratingengineeringsimulationandmachinelearningmethods
[25] NepalB,etal.ElectricityloadforecastingusingclusteringandARIMAmodelfor inamulti-scaleurbanenergymodelingworkflow.ApplEnergy2018;225:
energymanagementinbuildings.JpnArchitRev2020;3(1):62–76. 1176–89.
[26] LiY,SuY,ShuL.AnARMAXmodelforforecastingthepoweroutputofagrid [63] NutkiewiczA,ChoiB,JainRK.Exploringtheinfluenceofurbancontexton
connectedphotovoltaicsystem.RenewEnergy2014;66:78–89. buildingenergyretrofitperformance:ahybridsimulationanddata-driven
[27] CatalinaT,IordacheV,CaracaleanuB.Multipleregressionmodelforfast approach.AdvApplEnergy2021:3.
predictionoftheheatingenergydemand.EnergBuild2013;57:302–12. [64] IDAICE.Availablefrom:https://www.equa.se/en/ida-ice;2024.
[28] CiullaG,D’AmicoA.Buildingenergyperformanceforecasting:amultiplelinear [65] OhK,KimE-J,ParkC-Y.Aphysicalmodel-baseddata-drivenapproachto
regressionapproach.ApplEnergy2019;253:113500. overcomedatascarcityandpredictbuildingenergyconsumption.Sustainability
[29] AhmadAS,etal.AreviewonapplicationsofANNandSVMforbuildingelectrical 2022;14(15).
energyconsumptionforecasting.RenewSustEnergRev2014;33:102–9. [66] VirtualEnvironment.Availablefrom:https://www.iesve.com/software/
[30] DongB,CaoC,LeeSE.Applyingsupportvectormachinestopredictbuilding virtual-environment;2024.
energyconsumptionintropicalregion.EnergBuild2005;37(5):545–53. [67] TardioliG,etal.Aninnovativemodellingapproachbasedonbuildingphysics
[31] FanC,etal.Assessmentofdeeprecurrentneuralnetwork-basedstrategiesfor andmachinelearningforthepredictionofindoorthermalcomfortinanoffice
short-termbuildingenergypredictions.ApplEnergy2019;236:700–10. building.Buildings2022;12(4).
[32] MocanuE,etal.Deeplearningforestimatingbuildingenergyconsumption. [68] XuerebContiZ,ChoudharyR,MagriL.Aphysics-baseddomainadaptation
SustainEnergyGridsNetworks2016;6:91–9. frameworkformodelingandforecastingbuildingenergysystems.Data-Centric
[33] AhmadMW,MourshedM,RezguiY.Treesvsneurons:comparisonbetween Eng2023:4.
randomforestandANNforhigh-resolutionpredictionofbuildingenergy [69] TianC,etal.Dailypowerdemandpredictionforbuildingsatalargescaleusinga
consumption.EnergBuild2017;147:77–89. hybridofphysics-basedmodelandgenerativeadversarialnetwork.BuildSimul
[34] YuZ,etal.Adecisiontreemethodforbuildingenergydemandmodeling.Energ 2022;15(9):1685–701.
Build2010;42(10):1637–46. [70] ChenY,etal.Physics-informedneuralnetworksforbuildingthermalmodeling
[35] KuangB,etal.Data-drivenanalysisofinfluentialfactorsonresidentialenergy anddemandresponsecontrol.BuildEnviron2023;234.
end-useintheUS.JBuildEng2023;75:106947. [71] GokhaleG,ClaessensB,DevelderC.PhysQ:APhysicsInformedReinforcement
[36] ChongA,MenbergK.GuidelinesfortheBayesiancalibrationofbuildingenergy LearningFrameworkforBuildingControl.arXivpreprint;2022.arXiv:
models.EnergBuild2018;174:527–47. 2211.11830.
[37] HouD,HassanI,WangL.Reviewonbuildingenergymodelcalibrationby [72] GokhaleG,ClaessensB,DevelderC.Physicsinformedneuralnetworksforcontrol
Bayesianinference.RenewSustEnergRev2021;143:110930. orientedthermalmodelingofbuildings.ApplEnergy2022;314.
[38] JiangG,etal.EPlus-LLM:alargelanguagemodel-basedcomputingplatformfor [73] PaviraniF,etal.Demandresponseforresidentialbuildingheating:effective
automatedbuildingenergymodeling.ApplEnergy2024;367:123431. MonteCarlotreesearchcontrolbasedonphysics-informedneuralnetworks.
[39] ZhangL,ChenZ.Largelanguagemodel-basedinterpretablemachinelearning EnergBuild2024;311:114161.
controlinbuildingenergysystems.EnergBuild2024;313:114278. [74] LiuB,etal.Multi-scalemodelinginthermalconductivityofpolyurethane
[40] ArayaDB,etal.Anensemblelearningframeworkforanomalydetectionin incorporatedwithphasechangematerialsusingphysics-informedneural
buildingenergyconsumption.EnergBuild2017;144:191–206. networks.RenewEnergy2024;220.
21

Z.Maetal. Applied Energy 381 (2025) 125169
[75] SaeedMH,KazmiH,DeconinckG.Dyna-PINN:physics-informeddeepdyna-q [107] vanderMeerR,OosterleeCW,BorovykhA.Optimallyweightedlossfunctionsfor
reinforcementlearningforintelligentcontrolofbuildingheatingsysteminlow- solvingPDEswithneuralnetworks.JComputApplMath2022;405.
diversitytrainingdataregimes.EnergBuild2024;324:114879. [108] ScarselliF,etal.Thegraphneuralnetworkmodel.IEEETransNeuralNetw2008;
[76] DiNataleL,etal.Physicallyconsistentneuralnetworksforbuildingthermal 20(1):61–80.
modeling:theoryandanalysis.ApplEnergy2022;325. [109] VelickovicP,etal.Graphattentionnetworks.Stat2017;1050(20):10–48550.
[77] DiNataleL,etal.Towardsscalablephysicallyconsistentneuralnetworks:An [110] ChenM,etal.Simpleanddeepgraphconvolutionalnetworks.In:International
applicationtodata-drivenmulti-zonethermalbuildingmodels.ApplEnergy conferenceonmachinelearning.PMLR;2020.
2023;340. [111] HeK,etal.Identitymappingsindeepresidualnetworks.In:Computer
[78] XiaoT,YouF.Buildingthermalmodelingandmodelpredictivecontrolwith vision–ECCV2016:14thEuropeanconference,Amsterdam,theNetherlands,
physicallyconsistentdeeplearningfordecarbonizationandenergyoptimization. October11–14,2016,proceedings,partIV14.Springer;2016.
ApplEnergy2023;342. [112] ZagoruykoS,KomodakisN.Wideresidualnetworks.arXivpreprint;2016.arXiv:
[79] XiaoT,YouF.Physicallyconsistentdeeplearning-basedday-aheadenergy 1605.07146.
dispatchingandthermalcomfortcontrolforgrid-interactivecommunities.Appl [113] ChenRT,etal.Neuralordinarydifferentialequations.AdvNeuralInfProcesSyst
Energy2024;353. 2018;31.
[80] WangX,DongB.Physics-informedhierarchicaldata-drivenpredictivecontrolfor [114] ZakwanM,etal.PhysicallyconsistentneuralODEsforlearningmulti-physics
buildingHVACsystemstoachieveenergyandhealthnexus.EnergBuild2023; systems.arXivpreprint;2022.arXiv:2211.06130.
291. [115] SeyedzadehS,etal.Tuningmachinelearningmodelsforpredictionofbuilding
[81] JiangZ,DongB.Modularizedneuralnetworkincorporatingphysicalpriorsfor energyloads.SustainCitiesSoc2019;47:101484.
futurebuildingenergymodeling.Patterns2024;5:101029. [116] AbandaFH,ByersL.Aninvestigationoftheimpactofbuildingorientationon
[82] WangX,DongB.Long-termexperimentalevaluationandcomparisonofadvanced energyconsumptioninadomesticbuildingusingemergingBIM(building
controlsforHVACsystems.ApplEnergy2024;371. informationmodelling).Energy2016;97:517–27.
[83] DongB,etal.Ahybridmodelapproachforforecastingfutureresidential [117] MorrisseyJ,MooreT,HorneRE.Affordablepassivesolardesigninatemperate
electricityconsumption.EnergBuild2016;117:341–51. climate:Anexperimentinresidentialbuildingorientation.RenewEnergy2011;
[84] DrgonˇaJ,etal.Physics-constraineddeeplearningofmulti-zonebuildingthermal 36(2):568–77.
dynamics.EnergBuild2021;243. [118] PachecoR,Ordo´n˜ezJ,MartínezG.Energyefficientdesignofbuilding:areview.
[85] BünningF,etal.Physics-informedlinearregressioniscompetitivewithtwo RenewSustEnergRev2012;16(6):3559–73.
machinelearningmethodsinresidentialbuildingMPC.ApplEnergy2022;310. [119] AnL,etal.AninversePDE-ODEmodelforstudyingbuildingenergydemand.In
[86] MirfinA,XiaoX,JackMW.TOWST:aphysics-informedstatisticalmodelfor 2013wintersimulationsconference(WSC).IEEE2013:1869–80.
buildingenergyconsumptionwithsolargain.ApplEnergy2024;369. [120] PourarianS,etal.Efficientandrobustoptimizationforbuildingenergy
[87] TabogaV,etal.Neuraldifferentialequationsfortemperaturecontrolinbuildings simulation.EnergBuild2016;122:53–62.
underdemandresponseprograms.ApplEnergy2024;368. [121] TurnerC,FrankelM,U.Council.EnergyperformanceofLEEDfornew
[88] JiaY,etal.Temporalgraphattentionnetworkforbuildingthermalload constructionbuildings.NewBuildInstitute2008;4(4):1–42.
prediction.EnergBuild2023;321:113507. [122] DeWildeP.Thegapbetweenpredictedandmeasuredenergyperformanceof
[89] ZhengL,LuW.Urbanmicro-scalestreetthermalcomfortpredictionusinga buildings:aframeworkforinvestigation.AutomConstr2014;41:40–9.
‘graphattentionnetwork’model.BuildEnviron2024;111780. [123] JiangG,etal.Adeeplearning-basedBayesianframeworkforhigh-resolution
[90] HuY,etal.Timesseriesforecastingforurbanbuildingenergyconsumptionbased calibrationofbuildingenergymodels.EnergBuild2024;323:114755.
ongraphconvolutionalnetwork.ApplEnergy2022;307. [124] ChongA,GuY,JiaH.Calibratingbuildingenergysimulationmodels:areviewof
[91] Son,J.,J.Kim,AndJ.Koo,AnalysisofVentilationandInfiltrationRatesUsing thebasicstoguidefuturework.EnergBuild2021;253:111533.
Physics-InformedNeuralNetworks:ImpactofSpaceOperationand [125] HouW,etal.StateofchargeestimationforLithium-ionbatteriesatvarious
MeteorologicalFactors.BuildEnviron2024:112249. temperaturesbyextremegradientboostingandadaptivecubatureKalmanfilter.
[92] MaZ,JiangG,ChenJ.Physics-informedensemblelearningwithresidual IEEETransInstrumMeas2024;73:1–11.
modelingforenhancedbuildingenergyprediction.EnergBuild2024;323: [126] MaZ,etal.Personalthermalmanagementtechniquesforthermalcomfortand
114853. buildingenergysaving.MaterTodayPhys2021;20:100465.
[93] YueB,etal.Powerconsumptionpredictionofvariablerefrigerantflowsystem [127] FangerPO.Thermalcomfort.Analysisandapplicationsinenvironmental
throughdata-physicshybridapproach:Anonlinepredictiontestinoffice engineering.ThermalcomfortAnalysisandapplicationsinenvironmental
building.Energy2023;278. engineering.1970.
[94] ZhouY,etal.Ahybridphysics-based/data-drivenmodelforpersonalized [128] PeschieraG,TaylorJE.Theimpactofpeernetworkpositiononelectricity
dynamicthermalcomfortinordinaryofficeenvironment.EnergBuild2021;238. consumptioninbuildingoccupantnetworksutilizingenergyfeedbacksystems.
[95] ZhangL,KaufmanZ,LeachM.Physics-informedhybridmodelingmethodology EnergBuild2012;49:584–90.
forbuildinginfiltration.EnergBuild2024;320. [129] ZhangR,etal.CoupledEnergyPlusandcomputationalfluiddynamicssimulation
[96] XuX,etal.Theimpactofplace-basedaffiliationnetworksonenergy fornaturalventilation.BuildEnviron2013;68:100–13.
conservation:Anholisticmodelthatintegratestheinfluenceofbuildings, [130] ChenZ,etal.Interpretablemachinelearningforbuildingenergymanagement:a
residentsandtheneighborhoodcontext.EnergBuild2012;55:637–46. state-of-the-artreview.AdvApplEnergy2023;9:100123.
[97] ChenX,etal.Ahybrid-modelforecastingframeworkforreducingthebuilding [131] FanC,etal.Anovelmethodologytoexplainandevaluatedata-drivenbuilding
energyperformancegap.AdvEngInform2022;52. energyperformancemodelsbasedoninterpretablemachinelearning.Appl
[98] FangX,etal.Ahybriddeeptransferlearningstrategyforshorttermcross- Energy2019;235:1551–60.
buildingenergyprediction.Energy2021;215. [132] GaoY,RuanY.Interpretabledeeplearningmodelforbuildingenergy
[99] GaoY,etal.Deeplearningandtransferlearningmodelsofenergyconsumption consumptionpredictionbasedonattentionmechanism.EnergBuild2021;252:
forecastingforabuildingwithpoorinformationdata.EnergBuild2020;223. 111379.
[100] AhnY,KimBS.Predictionofbuildingpowerconsumptionusingtransferlearning- [133] ManfrenM,JamesPAB,TronchinL.Data-drivenbuildingenergymodelling–An
basedreferencebuildingandsimulationdataset.EnergBuild2022;258. analysisofthepotentialforgeneralisationthroughinterpretablemachine
[101] LuH,etal.Amulti-sourcetransferlearningmodelbasedonLSTManddomain learning.RenewSustEnergRev2022;167:112686.
adaptationforbuildingenergyprediction.IntJElectrPowerEnergySyst2023; [134] LiXA,etal.Physicalinformedneuralnetworkswithsoftandhardboundary
149. constraintsforsolvingadvection-diffusionequationsusingFourierexpansions.
[102] ParkH,etal.Stackingdeeptransferlearningforshort-termcrossbuildingenergy ComputMathAppl2024;159:60–75.
predictionwithdifferentseasonalityandoccupantschedule.BuildEnviron2022; [135] SunJ,etal.Atheory-guideddeep-learningformulationandoptimizationof
218. seismicwaveforminversion.Geophysics2020;85(2):R87–99.
[103] FangX,etal.Ageneralmulti-sourceensembletransferlearningframework [136] LiuZ,etal.Kan:Kolmogorov-arnoldnetworks.arXivpreprint;2024.arXiv:
integrateofLSTM-DANNandsimilaritymetricforbuildingenergyprediction. 2404.19756.
EnergBuild2021;252. [137] ToscanoJD,etal.FromPINNstoPIKANs:RecentAdvancesinPhysics-Informed
[104] ChenS,etal.Subspacedistributionadaptationframeworksfordomain MachineLearning.arXivpreprint;2024.arXiv:2410.13228.
adaptation.IEEETransNeuralNetworksLearnSyst2020;31(12):5204–18. [138] WenR,etal.Amulti-horizonquantilerecurrentforecaster.arXivpreprint;2017.
[105] FernandoB,etal.Unsupervisedvisualdomainadaptationusingsubspace arXiv:1711.11053.
alignment.inProceedingsoftheIEEEinternationalconferenceoncomputer [139] NiZ,etal.Astudyofdeeplearning-basedmulti-horizonbuildingenergy
vision.2013. forecasting.EnergBuild2024;303:113810.
[106] PanSJ,etal.Domainadaptationviatransfercomponentanalysis.IEEETrans [140] O’NeillZ,O’NeillC.Developmentofaprobabilisticgraphicalmodelfor
NeuralNetw2011;22(2):199–210. predictingbuildingenergyperformance.ApplEnergy2016;164:650–8.
22