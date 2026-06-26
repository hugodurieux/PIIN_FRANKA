TYPEOriginalResearch
PUBLISHED31March2026
DOI10.3389/fagro.2026.1764002
|     | Hybrid       |     | LSTM-edge |     |     | correction       |     |     |     |     |
| --- | ------------ | --- | --------- | --- | --- | ---------------- | --- | --- | --- | --- |
|     | architecture |     |           |     | for | physics-informed |     |     |     |     |
OPENACCESS
|     | crop | health |     | monitoring |     |     |     | in  |     |     |
| --- | ---- | ------ | --- | ---------- | --- | --- | --- | --- | --- | --- |
EDITEDBY
MarcoSozzi,
| UniversityofPadua,Italy | distributed |     |     | agricultural |     |     |     | robotics |     |     |
| ----------------------- | ----------- | --- | --- | ------------ | --- | --- | --- | -------- | --- | --- |
REVIEWEDBY
TianrongZhang,
ZhejiangShurenUniversity,China
AbdulrahmanM.Abdulghani, Rongchuan Yu1, Yongsheng Xie2*, Rifeng Wang1* and Wenxin Li3
PutraMalaysiaUniversity,Malaysia
1SchoolofArtificialIntelligence,GuangxiScience&TechnologyUniversity,Laibin,Guangxi,China,
*CORRESPONDENCE
2SchoolofArtificialIntelligenceandCenterforNetworkandEducationalTechnology,GuangxiScience
YongshengXie
xieyongsheng@gxstnu.edu.cn &TechnologyUniversity,Laibin,Guangxi,China,3SmartAgricultureCollege(IoTEngineeringCollege),
RifengWang GuangxiScience&TechnologyUniversity,Laibin,Guangxi,China
023505@163.com
RECEIVED09December2025 Agricultural robotics-enabled crop health monitoring faces critical trade-offs:
REVISED15February2026
sacrifice
ACCEPTED02March2026 standalone on-device models accuracy for real-time responsiveness,
PUBLISHED31March2026
whilecloud-dependentapproachessufferfromhighlatencyandcommunication
CITATION overhead. Additionally, data-driven models often lack biophysical plausibility,
YuR,XieY,WangRandLiW(2026)
|     | leading | to unreliable |     | predictions |     | for agronomic |     | decision-making |     | under |
| --- | ------- | ------------- | --- | ----------- | --- | ------------- | --- | --------------- | --- | ----- |
HybridLSTM-edgecorrection
architectureforphysics-informedcrop resource constraints. We propose a hybrid LSTM-edge correction architecture
healthmonitoringindistributed that hierarchically integrates lightweight Long Short-Term Memory (LSTM)
agriculturalrobotics.
field
Front.Agron.8:1764002. networks on robots with physics-informed neural networks (PINNs) at the
doi:10.3389/fagro.2026.1764002 edge. On-device LSTMs process localized sensor data (soil moisture, spectral
reflectance)
COPYRIGHT to generate initial crop stress probability estimates with minimal
©2026Yu,Xie,WangandLi.Thisisan latency. Edge-based PINNs refine these predictions by embedding biophysical
| open-accessarticledistributedunderthe | dynamics—modeled |     |     |     |     |     |     |     |     |     |
| ------------------------------------- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
termsoftheCreativeCommons via coupled partial differential equations (PDEs) governing
AttributionLicense(CCBY).Theuse, the soil-plant-atmosphere continuum (SPAC)—to ensure agronomic validity,
distributionorreproductioninother
|     | mitigate | sensor | noise, | and account |     | for spatial | variability. | The | framework | is  |
| --- | -------- | ------ | ------ | ----------- | --- | ----------- | ------------ | --- | --------- | --- |
forumsispermitted,providedthe
|     | deployed | on  | NVIDIA | Jetson | Nano (local | inference) |     | and AMD | EPYC | servers |
| --- | -------- | --- | ------ | ------ | ----------- | ---------- | --- | ------- | ---- | ------- |
originalauthor(s)andthecopyright
owner(s)arecreditedandthatthe
(edgeprocessing),seamlesslyintegratingwithexistingfarminginfrastructuresto
originalpublicationinthisjournalis
|     | replace | rule-based |     | thresholds | with | adaptive, | physics-grounded |     |     | control |
| --- | ------- | ---------- | --- | ---------- | ---- | --------- | ---------------- | --- | --- | ------- |
cited,inaccordancewithaccepted
PINN’s
academicpractice.Nouse,distribution commands. A Fourier Neural Operator (FNO) optimizes the edge
orreproductionispermittedwhichdoes computational efficiency for high-dimensional PDE solving. Experimental
notcomplywiththeseterms.
|     | evaluations       | on       | two real-world |             | datasets   | (soybean    | and      | citrus) demonstrate |          | that        |
| --- | ----------------- | -------- | -------------- | ----------- | ---------- | ----------- | -------- | ------------------- | -------- | ----------- |
|     | the hybrid        | approach |                | improves    | prediction |             | accuracy | by 18%              | compared | to          |
|     | standalone        | LSTMs    | (F1-score:     |             | 0.89±0.02  | for         | soybean, | 0.83±0.03           |          | for citrus) |
|     | while maintaining |          | real-time      | performance |            | (end-to-end |          | latency:            | 210 ms,  | energy      |
consumption:5.1J/prediction).Fielddeploymentona50-hectaresoybeanfarm
yieldstangibleagronomicbenefits:22%reductioninirrigationwaterusage,18%
fewerpesticideapplications,and95%systemuptimeunderfieldconditions.The
frameworkexhibitsrobustperformanceagainstsensornoise(≥80%accuracyat
|     | 30% noise-to-signal |              | ratio)      | and                 | outperforms  |          | cloud-based | PINNs          | (72.8%      | lower      |
| --- | ------------------- | ------------ | ----------- | ------------------- | ------------ | -------- | ----------- | -------------- | ----------- | ---------- |
|     | energy              | consumption) |             | and threshold-based |              | methods  |             | (28–33% higher |             | F1-score). |
|     | This work           | advances     | distributed |                     | agricultural |          | robotics    | by bridging    | data-driven |            |
|     | machine             | learning     | and         | domain-specific     |              | physics, |             | delivering     | a           | scalable,  |
resource-efficient
|                     | interpretable, |                       | and |     |          | solution | for | precision | agriculture.    | The |
| ------------------- | -------------- | --------------------- | --- | --- | -------- | -------- | --- | --------- | --------------- | --- |
|                     | hierarchical   | prediction-correction |     |     | pipeline | balances |     | real-time | responsiveness  |     |
| FrontiersinAgronomy |                |                       | 01  |     |          |          |     |           | frontiersin.org |     |

Yuetal. 10.3389/fagro.2026.1764002
with biological plausibility, making it suitable for resource-constrained field
robots. By integrating legacy sensors and adaptive actuation control, the
architecture offers a practical pathway to upgrade existing farming systems,
enablingdata-informedinterventionswhilereducingenvironmentalimpact.
KEYWORDS
hybridLSTM-edgearchitecture,physics-informedcorrection,crophealthmonitoring,
distributedagriculturalrobotics,Fourierneuraloperator
1 Introduction attheedgelayer,whichintegratedomainexpertisebymeansofpartial
differential equations that model soil-plant-atmosphere continuum
Agriculturalproductivityfacesincreasingpressurefromclimate processes (Lewandowski et al., 1999). The physics-informed neural
variability, resource scarcity, and the need for sustainable networksadjustforinaccuraciesinsensordata,spatialvariability,and
intensification. Traditional crop monitoring relies on manual simplifications in the model while guaranteeing that predictions
scouting or satellite imagery, which often lacks the temporal complywithestablishedbiophysicalprinciples.Thislayeredstructure
resolution or spatial granularity required for precise interventions supports immediate functionality while preserving the clarity and
(Khadatkar, 2024). Recent progress in agricultural robotics and reliabilitynecessaryforfarming-relatedchoices.
edge computing has made possible the autonomous gathering of The primary innovation stems from the active interplay
databynetworkedsensorsandunmannedgroundvehicles,which between the data-driven LSTM attributes and the correction
yields high-frequency time-series information on soil conditions, mechanisms grounded in physics. In contrast to previous
microclimate, and plant physiology (Abedalrhman and Alzaydi, methods that either impose physical constraints after training or
2025). Nevertheless, the conversion of this data into practical employdistinctphysicalmodels(Lançonetal.,2007),ourmethod
knowledgeisdifficultbecauseoftheintricaterelationshipbetween firstpre-trainstheLSTMonhistoricaldata,thenjointlyoptimizes
environmentalconditionsandcropbehavior. thePINNparameters and physical equation weightsduring edge-
Long Short-Term Memory (LSTM) networks have proven basedfine-tuning.Theon-deviceLSTMremainsfixedduringedge
especially effective in capturing time-based patterns in agricultural PINN updates, with periodic synchronization of improved
data, establishing machine learning as a robust approach for parameters when network conditions permit. The edge nodes
forecastingcrophealth(Siami-Naminietal.,2018).Althoughthese dynamically adjust the correction weights in response to
models attain satisfactory accuracy, their implementation on incoming data streams, which establishes a feedback loop that
resource-limited field robots presents notable trade-offs between progressively refines both the on-device and edge models. This
latency and energy expenditure. Moreover, approaches relying adaptive capability proves particularly valuable in agriculture,
solely on data frequently do not account for core biophysical where field conditions change rapidly due to weather events, pest
mechanisms that regulate plant development, which results outbreaks,ormanagementpractices.
inpredictionsthatlackbiologicalplausibilityinnewscenarios(Cai Theproposedmethodpresentsthreeclearbenefitscomparedto
etal.,2021).Thislimitationbecomescriticalwhenmakingirrigation current techniques. Initially, it preserves real-time responsiveness
or pesticide application decisions, where errors can have cascading bysituatingthecomputationallydemandingphysicssimulationsat
effectsoncropyieldandenvironmentalsustainability. the edge instead of on robots with limited resources. Second, it
Existing solutions typically adopt one of two suboptimal yieldsbiologicallycredibleforecastseveninunfamiliarscenariosby
approaches: either running simplified models directly on edge imposing physical conservation laws during the adjustment stage.
devices with limited computational capacity or offloading all Third,thearchitectureoperatesefficientlyacrossdiversehardware,
processing to cloud servers with high communication overhead (Yi ranging from low-power microcontroller units on field robots to
etal.,2015).Thefirstapproachcompromisesaccuracyinforecastingto GPU-accelerated edge servers, which renders it suitable for
achieve immediate processing, whereas the second method creates extensiveagriculturaloperations.
delaysthatareunsuitableforurgentactionssuchaspreventingfrost Theremainderofthispaperisorganizedasfollows:Section2
damage or controlling pests (Abdulghani et al., 2022). Neither reviewsrelatedworkinagriculturalrobotics,edgeAI,andphysics-
approach adequately addresses the need for both computational informed machine learning. Section 3 introduces the biophysical
efficiencyandagronomicvalidityindistributedagriculturalsystems. foundations and neural network architectures underlying our
We present a hybrid architecture integrating the advantages of approach. Section 4 describes the hybrid LSTM-edge correction
embeddedmachinelearningwithphysics-awarecorrectionassistedby framework,whichcoversthedistributedtrainingprotocolandreal-
edge computing. The system applies lightweight LSTM networks on time inference pipeline. Section 5 presents experimental results
fieldrobotstohandlelocalsensorstreams,whichproducesinitialstress comparing the system against baseline methods across multiple
probability estimates with minimal delay. These forecasts are crop types and growing seasons. Finally, Sections 6 and 7 discuss
subsequentlyadjustedbyphysics-informedneuralnetworks(PINNs) broaderimplicationsandfutureresearchdirections.
FrontiersinAgronomy 02 frontiersin.org

Yuetal. 10.3389/fagro.2026.1764002
2 Related work tackle the distinct obstacles in crop health surveillance, including
managing inconsistent sensor sampling frequencies or merging
diverseenvironmentaldatatypes.
Recent progress in agricultural robotics and edge computing
The proposed hybrid LSTM-edge correction architecture
has created novel frameworks for decentralized crop observation
progresses beyond these current methods by integrating three
and control. Existing approaches can be broadly categorized into
principal novel elements: (1) a hierarchical prediction-correction
three research directions: (1) edge-cloud collaborative systems for
system preserving real-time responsiveness alongside physical
agricultural analytics, (2) physics-aware machine learning in
plausibility, (2) close interconnection between data-driven
precision agriculture,and(3)distributed intelligence architectures
forfieldrobotics. features and physics-based constraints via differentiable PDE
solversattheedge,and(3)flexiblemodelpartitioningtailoredfor
2.1 Edge-cloud collaborative systems agricultural time-series data with varying spatial granularity. In
contrast to previous edge-cloud systems that merely transfer
Edgecomputinghasemergedasacriticalenablerforreal-time computational tasks (Liu et al., 2025), our approach creates a
agricultural analytics by reducing latency and bandwidth feedback mechanism where edge-based corrections inform
requirements compared to cloud-only solutions. A number of periodic updates to on-device models. Future work will explore
investigations have examined mixed frameworks in which full parameter distillation from edge to device. This differs from
peripheral devices initially process detector information prior to independentphysics-basedmodels(Songetal.,2023)bypermitting
sendingcompressedattributestoremoteservers(Liuetal.,2025). effective implementation on varied hardware without losing the
For example, irrigation setups employing LoRaWAN and edge
clarityadvantagesofembeddingexpertinsights.Thearchitecture’s
computing show decreased water usage by making decisions at distinct blend of temporal analysis (LSTM), spatial adjustment
thelocallevel(Zhangetal.,2025).Nevertheless,suchsystemsoften (PINN), and decentralized processing yields a more thorough
depend on heuristic thresholds or statistical models incapable of approach for monitoring crop health relative to current edge AI
grasping intricate crop-environment relationships. While the (Sureshetal.,2025)ordecentralizedcomputational(Lietal.,2023)
adaptive polling methods in ESP32-driven soil monitoring setups methodsinagriculturalapplications.
(Chantimaetal.,2025)markadvancementinoptimizingedgedata
acquisition,theyfailtotacklethecoreissueofembeddingphysical
limitationswithinforecastingframeworks.
3 Background and preliminaries
2.2 Physics-informed learning in
agriculture To build the theoretical basis for our hybrid architecture, we
initiallyexaminethecoreideasinbiophysicalmodelingandneural
Incorporatingdomainknowledgeintomachinelearningmodels network design which form the basis of our method. This part
hasbecomeincreasinglypopularasamethodtoboostgeneralization outlinestheessentialcontextforgraspinghowphysicallimitations
in agricultural applications. Physics-informed neural networks can be merged with learning based on data in decentralized
(PINNs) have shown promise in modeling soil moisture dynamics agriculturalsetups.
andcropgrowthpatterns(Songetal.,2023).Thesemethodsembed
physical laws directly into the loss function, guaranteeing that 3.1 Biophysical models in agriculture
predictions comply with established biological and environmental
constraints. Current implementations frequently depend on Crop growth dynamics are governed by complex interactions
centralizedprocessing,whichrendersthemunsuitableforreal-time betweenplantsandtheirenvironment,typicallydescribedthrough
application inthe field. TheCNN-TemporalAttentionMechanism coupled partial differential equations (PDEs). The soil-plant-
for soil monitoring (Suresh et al., 2025) shows the promise of atmosphere continuum (SPAC) model serves as a structure for
combined architectures but does not include direct physical examining these interactions by depicting mass and energy fluxes
limitationsorrefinementmethodsbasedonedges. viaasystemofconservationlaws(PenuelasandSardans,2021).The
governing PDE for water transport in the soil-plant system is
2.3 Distributed intelligence architectures (Penuelas and Sardans, 2021). The water transport equation
formsthecoreofSPACmodeling:
Distributed computing frameworks have been proposed to
∂q
balancecomputationalloadacrossedgedevicesandservers.Some =∇·(K(q)∇y)−S(q) (1)
∂t
systemsemploymodelpartitioningstrategieswheredifferentlayers
of a neural network execute across hierarchical nodes (Li et al., where q represents soil water content (m³/m³), K(q) the
2023). Although these methods are suitable for broad IoT hydraulic conductivity (m/s), y the water potential (kPa), S the
applications, they fail to address the distinct temporal-spatial plantwater uptake rate(1/s), z the soildepth (m), and t time(s).
relationships inherent in agricultural data streams. Recent Boundary conditions: no-flux at the bottom (z = -1m, ∂q/∂z = 0)
research on hybrid edge-P2P frameworks (Serena et al., 2021) andatmosphericforcingatthesurface(z=0,-K(q)∂y/∂z=E-P,
yieldsunderstandingofadaptableresourcedistributionyetfailsto where E is evaporation and P is precipitation). Initial conditions
FrontiersinAgronomy 03 frontiersin.org

Yuetal. 10.3389/fagro.2026.1764002
fromfieldmeasurementsatt=0.K(q)thehydraulicconductivity, 3.4 Edge computing paradigms
y thewaterpotential,andS(q)theplantwateruptakerate.Similar
equationsdelineatenutrienttransport,photosynthesis,andbiomass Contemporary edge computing systems allocate processing
accumulation, which form an interconnected system governing duties across tiered levels, ranging from devices with limited
crop health parameters such as leaf area index and stomatal resources to higher-capacity edge servers. The key metrics for
conductance(SargunandMohan,2020). agricultural applications include latency (L), energy consumption
(E), and communication cost (C), which form a multi-objective
3.2 Long short-term memory networks
optimizationproblem(Equation6):
LSTMs have become the de facto standard for modeling min½L(x),E(x),C(x)(cid:2) (6)
x∈X
sequential data in agricultural applications due to their ability to
wherexrepresentstheallocationofcomputationaltasksacross
capturelong-rangedependenciesintime-seriesmeasurements.The
the network (Zhang et al., 2020). Recent progress in model
primary innovation is found in their gating mechanism, which
compression and quantization has made it possible for
controls the movement of information within the network
(Equations2–4). sophisticated neural networks to operate effectively on embedded
hardware without compromising accuracy required for practical
f t =s(W f ·½h t−1 ,x t (cid:2)+b f ) (2) applications(Kimetal.,2023).
Our hybrid architecture is built upon the union of these
i t =s(W i ·½h t−1 ,x t (cid:2)+b i ) (3) elements: biophysical models, temporal neural networks, physics-
awarelearning,anddistributedcomputing.Thejointapplicationof
o t =s(W o ·½h t−1 ,x t (cid:2)+b o ) (4) theirdistinctcapabilitiestacklesthecoreobstaclesofreal-timecrop
health assessment under limited resources, guaranteeing that
where f, i, and o represent forget, input, and output gates
t t t predictionsalignwithestablishedbiologicallaws.
respectively, s denotes the sigmoid function, and W matrices
contain learnable parameters (Yang et al., 2024). This structural
design is notably efficient for handling irregularly sampled sensor
dataobtainedfromfieldrobots,givenitscapacitytoretainpertinent 4 Hybrid edge-AI framework for crop
statedetailsoverdifferingtemporalspans. health prediction
3.3 Physics-informed neural networks
The proposed framework creates a layered computational
structure connecting on-device machine learning to physical
Physics-informed neural networks establish a method for
correctionatthe edge. As showninFigure 1, the system processes
embedding domain expertise within deep learning architectures
agriculturalsensordatathroughsequentialstagesoftemporalfeature
by directly embedding physical principles into the objective
extraction and physics-informed refinement. This design addresses
function. The standard method focuses on reducing both the
the dual challenges of real-time responsiveness and biological
mismatch in data and the errors in the partial differential
plausibilityindistributedcropmonitoringsystems.
equationterms(Equation5).
4.1 Hybrid on-device LSTM and edge
L=l jju −u jj2+l jjF(u )jj2 (5)
data NN obs PDE NN physics-informed correction mechanism
where u represents the neural network prediction, u the
NN obs
observed data, and F the PDE operator (Farea et al., 2025). The The primary innovation of our architecture is found in its
weightingfactorsl
data
andl
PDE
controlthetrade-offbetweenfitting
hierarchical prediction-correction pipeline, where lightweight
measurementsandsatisfyingphysicalconstraints.Infarmingcontexts, LSTMs implemented on field robots produce preliminary crop
thismodelguaranteesthatforecastsstaywithinbiologicallyreasonable stress estimates that are later improved by physics-aware edge
boundsdespitelimitedorimprecisetrainingdata. models. The on-device LSTM processes time-series sensor inputs
FIGURE1
HierarchicalarchitectureofhybridLSTM-edgecorrectionsystem.
FrontiersinAgronomy 04 frontiersin.org

Yuetal. 10.3389/fagro.2026.1764002
X t =½x t−k ,…,x t (cid:2) from soil moisture probes, spectral reflectance where D x and D y represent anisotropic diffusion coefficients
sensors, and microclimate monitors, where x ∈Rd represents a learned from historical soil maps. This model accounts for the
t
d-dimensional measurement vector at time t. The network anisotropic nature of hydraulic conductivity typically observed in
architecture employs a pruned LSTM cell with reduced hidden agricultural settings. The source term f incorporates crop-specific
state dimensionality h ∈Rm (where m≪n compared to responsestoenvironmentalconditions:
t
standard implementations) to minimize computational overhead
f(u^,E)=R(u^)·G(E) (11)
(Equation7): t t
Here,R(u^)representstherootwateruptakefunctiondependent
h
t
=LSTMq(X
t
) (7)
onsoilmoisture,andG(E)modelstheenvironmentalmodulation
t
where q denotes the trainable parameters optimized for factor based on solar radiation and vapor pressure deficit. The
embedded deployment. The hidden state h t projects to an initial multiplicativestructureguaranteesbiologicallyrealisticinteractions
stress probability distribution p t ∈½0,1(cid:2)c through a compressed amongsoilandatmosphericfactors.
fully-connectedlayer,withcrepresentingthenumberofcropstress TheedgeserverperiodicallyretrainsthePINNusingaggregated
classes(e.g.,waterdeficit,nutrientdeficiency,pestinfestation). data from multiple field robots, updating the parameters f while
These on-device predictions serve as inputs to the edge keeping the on-device LSTM fixed. This decentralized learning
correction module, which solves a coupled system of PDEs method permits the adjustment system to conform to local
describing crop-environment interactions. The correction circumstances while avoiding the need for regular modifications
procedure reduces a combined loss function, penalizing both totheintegratedmodels.Thetrainingprocessemploysanadaptive
divergence from the LSTM outputs and infringement of physical weighting scheme for a and b based on the spatial density of
constraints(Equation8). sensorsandtheconfidencescoresfromtheLSTMpredictions.
(cid:1) (cid:1)
L =a∥y −p ∥2+b
(cid:1)
(cid:1) (cid:1)
∂u^
−∇·(D∇u^)−f(u^,E)
(cid:1)
(cid:1) (cid:1)
2
(8) 4.3 Dynamic integration of legacy sensors
corr t t 2 ∂t t
2 with learned models
Here,y representsthecorrectedprediction,u^ thecontinuous
t
fieldvariable(e.g.,soilmoisturecontent),Dthediffusioncoefficient Theproposedframeworkintegrateslegacyagriculturalsensors
tensor, and E environmental forcing terms (radiation, by means of an adaptive fusion layer which translates raw
t
precipitation).Theweightingfactorsa andb balancedatafidelity measurements into features compatible with LSTM. Let s(
t
i)∈R
against physical consistency, adaptively adjusted based on sensor denote the scalar output from the i-th legacy sensor (e.g.,
reliabilitymetrics. capacitance-based soil moisture probe) at time t. The system
transforms these readings into normalized feature vectors z(i)∈
t
Rk throughalearnedaffinetransformation(Equations12–14):
4.2 Physics-informed neural networks for
edge-based agronomic correction z(i)=W(i)s(i)+b(i) (12)
t s t s
where W(i)∈Rk(cid:3)1 and b(i)∈Rk are trainable parameters
The edge-based correction module employs physics-informed s s
neuralnetworks(PINNs)torefinetheon-deviceLSTMpredictions specific to each sensor type. The dimension k matches the input
whileenforcingdomain-specificconstraints.ThePINNframework size of the LSTM’s first layer, enabling seamless integration
with modern multi-modal sensors. This method substitutes
employs a multi-layer perceptron (MLP) to approximate the
conventional calibration techniques dependent on thresholds,
solutionofthegoverningPDEsystem.GiventheLSTMoutputp
t
which necessitate manual tuning for varying soil types and
and environmental inputs E, the network predicts the corrected
t
stressstatey andthecontinuousfieldvariablesu^(Equations9–11): environmentalconditions.
t
Thefusionproceduremergestraditionalsensorattributeswith
½y
t
,u^(cid:2)=MLPf(p
t
,E
t
) (9) data obtained from digital imaging detectors and spectral
reflectance assessments. For N legacy sensors and M modern
where f denotes the PINN parameters. The network
sensors,thecompleteinputvectorx totheLSTMbecomes:
architecture differs from conventional MLPs through its dual t
output structure and physics-constrained loss formulation. The x =½⊕N z(i)(cid:2)⊕½⊕M d(j)(cid:2) (13)
first term in Equation 8 ensures the corrected prediction y does t i=1 t j=1 t
t
notdeviateexcessivelyfromtheLSTMestimatep t ,preservingthe where d t (j) represents digital sensor readings and ⊕ denotes
temporalpatternslearnedbytheon-devicemodel.Thesecondterm vector concatenation. The transformation weights W s (i) are
enforces the PDE constraints, where f(u^,E) represents the initialized using historical calibration data and fine-tuned during
t
source/sink terms accounting for plant water uptake and the LSTM training phase, allowing the model to learn optimal
environmentalforcing.
scalingfactorsforeachsensorundervaryingfieldconditions.
The diffusion term ∇·(D∇u^) models spatial heterogeneity in Theedgecorrectionmodulerefinesthesemergedattributesby
soilproperties,withthediffusiontensorDparameterizedas: embedding physical limitations on sensor operation. For soil
moisture sensors, the PINN enforces mass conservation between
D=diag(D x (x,y),D y (x,y)) (10) successivemeasurements:
FrontiersinAgronomy 05 frontiersin.org

Yuetal. 10.3389/fagro.2026.1764002
∂q^ q −q variablesu^(x):
= t+1 t −∇·(K(q)∇y)+S(q)≈0 (14)
∂t Dt
½y(x),u^(x)(cid:2)=Q(h (x)) (18)
whereq representsthesensor-derivedmoisturecontent,q^ the L
physics-con
t
sistent estimate, and Dt the sampling interval. This
whereQisaprojectionnetworkthatmapsthefinalhiddenstate
tothedesiredoutputs.Thephysicalconstraintsareimposedbyan
limitation adjusts for typical sensor anomalies such as time-based
adjustedlossfunctionwhichpenalizesdiscrepanciesfromboththe
deviations and area-wide averaging impacts. The system
dynamically adjusts the fusion weights W(i) based on the residual governing partial differential equations and the predictions of the
s
longshort-termmemorynetwork.
between raw sensor values and physics-corrected estimates,
effectivelylearningreliabilityfactorsforeachsensorchannel. L =l ∥y(x)−p(x)∥2+l ∥F(u^,E)∥2+l ∥B(u^)∥2 (19)
FNO 1 2 3
4.4 Fourier neural operator for edge PINNs The first term maintains consistency with the on-device
predictions, the second term enforces the PDE residuals F
To address the computational challenges of solving high- (from Equation 1), and the third term incorporates boundary
dimensional PDEs at the edge, we implement the physics- conditions B (e.g., no-flux conditions at field edges). The FNO’s
informedcorrectionmoduleasaFourierNeuralOperator(FNO). capacity to acquire knowledge of the solution operator instead
The FNO framework models the solution operator for the of specific solutions permits it to generalize across diverse
governing PDE system by means of spectral transformations, field arrangements and environmental contexts with little
achieving a substantial reduction in computational expense additionaltraining.
relative to conventional PINNs without compromising accuracy TheedgedeploymentoftheFNOemploysmodelparallelismto
(Lietal.,2021). allocate computations among accessible hardware resources. The
The FNO transforms the input function space, consisting of FouriertransformsexecuteonGPU-acceleratededgeservers,while
sensor data and LSTM results, into the solution space of adjusted the pointwise neural network operations can run on lower-power
forecasts by applying Fourier transforms and neural network coprocessors. This division approach preserves the model’s
operations. Given the input function Our FNO implementation precision while satisfying the delay constraints for immediate
uses4Fourierlayerswith32hiddenchannels,16Fouriermodesper agricultural decision processes. The parameter efficiency of the
dimension,andGELUactivationfunctions.Thenetworkistrained FNO also permits periodic updates across limited rural networks,
with Adam optimizer (learning rate 1e-3, batch size 16) for 500 which guarantees that the correction module adjusts to seasonal
epochs.Computationalcost:45MFLOPsperforwardpass,12MB variationsincropconditions.
modelsize,achieving15xspeedupoverconventionalPINNsolvers
while maintaining comparable accuracy (<2% relative error). v(x) 4.5 Distributed actuation guided by
defined over spatial domain x∈D, the FNO first lifts v(x) to a corrected predictions
higher-dimensionalrepresentation(Equations15–19):
The final component of our framework translates the edge-
h (x)=P(v(x)) (15)
0 corrected predictions into precise control signals for agricultural
wherePisashallowfully-connectednetwork.Themodelthen actuators. Let y t * ∈Rc denote the physics-informed stress
applies L iterative Fourier layers that mix information in both probabilities after edge correction at time t. These forecasts
physicalandfrequencydomains: operate a decentralized control mechanism coordinating various
field devices, including irrigation valves, sprayers, and fertigation
h l+1 (x)=s(W l h l (x)+F −1(R l ·F(h l ))(x)) (16) systems. For each actuator a i located at spatial coordinate x i , we
Here,F andF
−1denotetheFouriertransformanditsinverse, computethecontrolsignalu
i
(t)asEquations20–26:
Z
R is a learnable weight tensor in Fourier space, W is a linear
l l t de(t)
transformation in physical space, and s is an activation function. u i (t)=K p e i (t)+K i 0 e i (t)dt+K d d i t (20)
The Fourier-domain multiplication R ·F(h) enables global
convolution operations with O(nlogn) l comp l lexity, making it where e i (t)=y t * ,i −y target represents the error between the
particularlyefficientforlargeagriculturalfields. predicted stress level and desired threshold for actuator i. The
PID gains K , K, and K aredynamically adjusted basedon crop
For the crop health adjustment task, we adapt the FNO p i d
growthstageandenvironmentalconditions:
framework to manage the interconnected soil-plant-atmosphere
dynamics specified in Equation 1. The input function v(x)
K =f (E,GDD), K =f(E,GDD), K =f (E,GDD) (21)
p p t i i t d d t
combines:
Here, GDD denotes growing degree days, and f , f, f are
p i d
v(x)=½p(x),E(x),S(x)(cid:2) (17)
nonlinearfunctionslearnedfromhistoricaloptimalcontrolpatterns.
where p(x) represents the on-device LSTM predictions, E(x) This adaptive tuning ensures appropriate responsiveness to stress
environmental variables (temperature, radiation), and S(x) soil signalswhilepreventingover-actuationundertransientconditions.
properties (texture, organic matter). The FNO outputs the The control signals travel across a ROS 2 middleware layer
corrected stress predictions y(x) and the continuous field responsible for handling real-time communication between edge
FrontiersinAgronomy 06 frontiersin.org

Yuetal. 10.3389/fagro.2026.1764002
nodes and fieldactuators. Each actuator subscribes to adedicated 5 Experimental evaluation
topic containing its control parameters, with quality-of-service
settings configured for reliable delivery over 5G/LoRaWAN
To assess the performance of our hybrid LSTM-edge correction
hybrid networks. The message format encodes both the
framework,wecarriedoutextensiveexperimentsindiverseagricultural
immediatecontrolvalueu(t)andashort-termforecast:
i settingsandwithvariouscropspecies.Theevaluationfocusesonthree
m(t)=hu(t),fu^(t+Dt),…,u^(t+kDt)gi (22) key aspects: (1) prediction accuracy compared to standalone
i i i i approaches, (2) computational efficiency under resource constraints,
whereu^
i
(t+jDt)representsj-stepaheadpredictionsgenerated
and(3)robustnesstosensornoiseandenvironmentalvariability.
bytheedgePINN.Thisforecastingmechanismpermitsactuatorsto
proactively modify their function in response to predicted stress 5.1 Experimental setup
progression, thereby diminishing reaction delay under swift
environmentalshifts. Datasets: Our system was assessed with two farming datasets
Thespatialcoordinationofmultipleactuatorsincorporatesthe gatheredfromoperationalagriculturalsites,withdetailedprotocols
corrected field-scale predictions u^(x) from the FNO module. For for data collection, labeling, and quality assurance. The initial
managing irrigation, the system addresses a resource-limited dataset (Soybean2023) contains high-frequency (5-minute
optimization problem aimed at reducing water consumption interval) measurements from 32 sensor nodes distributed over a
whilekeepingsoilmoisturewithindesiredlevels. 50-hectaresoybeanfield(latitude23.5°N,longitude109.2°E),with
dataonsoilmoistureatthreedepths(0-10cm,10-20cm,20-40cm
min
oN
u2s:t:u^(x)+au ∈½q ,q (cid:2)∀ i (23) using capacitance-based probes), canopy temperature (infrared
i i i i min max
fuigi=1 thermometers), and multispectral reflectance (NDVI, GNDVI,
where a represents the irrigation effectiveness coefficient for RVI indices). The second dataset (CitrusUAT-Extended) contains
i
zone i, and q , q define the agronomically optimal moisture hourlyobservationsfrom12weatherstationsand48soilprobesina
min max
25-hectaremixedcitrusorchard,withadditionalmanualcropstress
range. The quadratic objective function emphasizes even
water allocation, and the constraints guarantee sufficient assessments conducted weekly by agronomists using standardized
hydration for the entire field. This optimization runs periodically visual scoring protocols. Our system was assessed with two
farming datasets gathered from operational agricultural sites. The
onedgeservers,withresultsdisseminatedtoactuatorsthroughthe
initial dataset contains high-frequency (5-minute interval)
ROS2network.
measurementsfrom32sensornodesdistributedovera50-hectare
Forpestcontrolpurposes,thesystemappliessprayingstrategies
soybean field, with data on soil moisture (0-40cm depth), canopy
based on thresholds, integrating both present stress forecasts and
temperature, and multispectral reflectance (Lou et al., 2023). The
diseasespreadmodels.
second dataset contains hourly observations from 12 weather
(
1 if y * >t (GDD) stations and 48 soil probes in a mixed citrus orchard, with
us i pray(t)= t,i pest (24) additional manual crop stress assessments conducted weekly
0 otherwise
(Gómez-Floresetal.,2024).
The dynamic threshold t (GDD) accounts for pest Baselines: We compared against three state-of-the-
pest
developmental rates modeled as a function of growing degree artapproaches:
days.Inscenarioswherevariousstressorsareanticipated(suchas
water shortage and pest infestation), the edge node calculates a 1. Standalone LSTM: A conventional LSTM network with 2
unified actuation signal by balancing conflicting demands with layers, 64 hidden units, running entirely on edge devices
multi-objectiveoptimization. (Basecaetal.,2025).Modelsize:850KB,trainedwithAdam
optimizer(lr=0.001)for100epochs.AconventionalLSTM
uopt =argmin½∥y ∗−ytarget∥2+l∥u∥ (cid:2) (25) network running entirely on edge devices (Baseca
i t 2 1
u
etal.,2025)
TheL1regularizationterm ∥u∥ promotessparseinterventions, 2. Cloud PINN: A physics-informed neural network with 6-
1
reducing chemical usage while maintaining crop health. The layer MLP (128 units/layer) offloaded to cloud servers via
optimization weights l are adaptively tuned based on HTTPS/REST API (Abhishek and Ramesh, 2024). Round-
environmentalimpactassessmentsandinputcostfactors. trip communication latency (980ms) includes network
Theactuationsubsystemcontinuouslymonitorsimplementation transmission (650ms), cloud processing (280ms), and
fidelitythroughsensorfeedbackloops.Eachactuatorreportsitsactual response return (50ms). Model size: 12 MB. A physics-
state(e.g.,flowrate,pressure)backtotheedgenode,whichcompares informed neural network offloaded to cloud servers
againstcommandedvaluestodetectmalfunctionsorcalibrationdrift. (AbhishekandRamesh,2024)
Discrepancies activate either automatic recalibration procedures or 3. Threshold-Based:Conventionaldecision-makingapproaches
notificationsforhumanreview,guaranteeingthatthephysicalactions basedonpredeterminedsoilmoisturelevels(Guetal.,2020).
preciselyalignwiththecomputationalsuggestions.Thisclosed-loop Thresholds tuned per dataset using ROC analysis on
operation is essential for preserving system dependability during validation set: soybean (field capacity 35%, wilting point
prolongeddeploymentindemandingagriculturalsettings. 15%), citrus (field capacity 40%, wilting point 18%).
FrontiersinAgronomy 07 frontiersin.org

| Yuetal. |     |     |     |     |     |     |     |     |     |     | 10.3389/fagro.2026.1764002 |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- |
Conventional decision-making approaches based on TABLE1 Cropstresspredictionperformance(F1-score).
predeterminedsoilmoisturelevels(Guetal.,2020)
|     |     |     |     |     |     |     |        |     |         |        | Energy |     | Latency |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | ------- | ------ | ------ | --- | ------- |
|     |     |     |     |     |     |     | Method |     | Soybean | Citrus |        |     |         |
|     |     |     |     |     |     |     |        |     |         |        | (J)    |     | (ms)    |
Metrics:Theaccuracyofpredictionswasevaluatedby:
|                                                  |     |     |     |     |     |     | Standalone |     | 0.72 | 0.68 | 3.2 |     | 120 |
| ------------------------------------------------ | --- | --- | --- | --- | --- | --- | ---------- | --- | ---- | ---- | --- | --- | --- |
| (cid:129) Stressclassificationaccuracy(F1-score) |     |     |     |     |     |     | LSTM       |     |      |      |     |     |     |
(cid:129) Meanabsoluteerror(MAE)forcontinuousvariables CloudPINN 0.85 0.79 18.7 980
(cid:129)
| Energyconsumption(Joulesperprediction)                  |     |     |     |     |     |     | Threshold- |     |      |      |     |     |     |
| ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | ---------- | --- | ---- | ---- | --- | --- | --- |
|                                                         |     |     |     |     |     |     |            |     | 0.61 | 0.55 | 0.8 |     | 50  |
| (cid:129) Latency(msfromsensorreadingtoactuationsignal) |     |     |     |     |     |     | Based      |     |      |      |     |     |     |
Proposed
|                                                    |     |     |     |     |     |     |        |     | 0.89±0.02 | 0.83±0.03 | 5.1 |     | 210 |
| -------------------------------------------------- | --- | --- | --- | --- | --- | --- | ------ | --- | --------- | --------- | --- | --- | --- |
| Implementation:Theon-deviceLSTMwasdeployedonNVIDIA |     |     |     |     |     |     | Hybrid |     |           |           |     |     |     |
JetsonNano(4GBRAM,128-coreMaxwellGPU,Quad-coreARM
| A57 CPU | @1.43 | GHz, 10W | TDP mode), | running | JetPack | 4.6 with |             |      |      |           |        |        |              |
| ------- | ----- | -------- | ---------- | ------- | ------- | -------- | ----------- | ---- | ---- | --------- | ------ | ------ | ------------ |
|         |       |          |            |         |         |          | independent | runs | with | different | random | seeds. | The combined |
CUDA 10.2 and TensorRT 8.0. The edge correction module ran on method attained higher precision without exceeding the
| AMD EPYC | 7B12 | servers (64 | cores | @ 2.25 | GHz, 256 | GB RAM, |     |     |     |     |     |     |     |
| -------- | ---- | ----------- | ----- | ------ | -------- | ------- | --- | --- | --- | --- | --- | --- | --- |
boundariesofinstantaneousprocessingrequirements.
A100–40
NVIDIA GB GPU, 280W TDP). The system employed The physics-informed adjustment yielded F1-score
| LoRaWAN | (868 | MHz, 125 | kHz bandwidth, |     | SF7) for connections |     |              |     |           |          |        |      |                 |
| ------- | ---- | -------- | -------------- | --- | -------------------- | --- | ------------ | --- | --------- | -------- | ------ | ---- | --------------- |
|         |      |          |                |     |                      |     | improvements |     | of 17-23% | relative | to the | LSTM | baseline, which |
betweendevicesandtheedge(average2.3KBpayload),while5GNR underscorestheimportanceofembeddingdomain-specificinsights.
(sub-6GHz)wasadoptedforlinksbetweentheedgeandthecloud.All refines
|     |     |     |     |     |     |     | Figure 2 | illustrates | how | the edge | correction |     | initial LSTM |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | --- | -------- | ---------- | --- | ------------ |
models were trained with PyTorch 1.12 employing mixed-precision predictionsforarepresentativedroughtstressevent.
(FP16)quantizationtosupportdeploymentonembeddedsystems.The
configured
| Jetson Nano | was |     | in 10W | power | mode (nvpmodel | -m 0) |                   |     |     | efficiency |     |     |     |
| ----------- | --- | --- | ------ | ----- | -------------- | ----- | ----------------- | --- | --- | ---------- | --- | --- | --- |
|             |     |     |        |       |                |       | 5.3 Computational |     |     |            |     |     |     |
withjetson_clocksenabledformaximumperformance.Theon-device
LSTMwasdeployedonNVIDIAJetsonNano(10WTDP),whilethe
|                       |     |       |     |          |            |        | The | layered | structure | attained | accuracy | comparable | to cloud- |
| --------------------- | --- | ----- | --- | -------- | ---------- | ------ | --- | ------- | --------- | -------- | -------- | ---------- | --------- |
| edge correctionmodule |     | ranon | AMD | EPYC7B12 | servers(64 | cores, |     |         |           |          |          |            |           |
efficiency
|            |     |        |          |         |                 |     | based systems |     | while retaining | the |     | of  | edge computing. |
| ---------- | --- | ------ | -------- | ------- | --------------- | --- | ------------- | --- | --------------- | --- | --- | --- | --------------- |
| 280W TDP). | The | system | employed | LoRaWAN | for connections |     |               |     |                 |     |     |     |                 |
Energymeasurementsrevealed:
| between | devices | and the edge, | while | 5G  | was adopted | for links |     |     |     |     |     |     |     |
| ------- | ------- | ------------- | ----- | --- | ----------- | --------- | --- | --- | --- | --- | --- | --- | --- |
between the edge and the cloud. All models were trained with E =E +E +E =3:2+0:9+1:0=5:1J (26)
|         |           |                 |     |              |     |         | hybrid | LSTM        | comm    | corr     |          |     |                  |
| ------- | --------- | --------------- | --- | ------------ | --- | ------- | ------ | ----------- | ------- | -------- | -------- | --- | ---------------- |
| PyTorch | employing | mixed-precision |     | quantization | to  | support |        |             |         |          |          |     |                  |
|         |           |                 |     |              |     |         | This   | constitutes | a 72.8% | decrease | relative | to  | cloud offloading |
deploymentonembeddedsystems.
|     |     |     |     |     |     |     | (18.7J) while | preserving |     | similar | accuracy. | The | communication |
| --- | --- | --- | --- | --- | --- | --- | ------------- | ---------- | --- | ------- | --------- | --- | ------------- |
5.2 Prediction accuracy overhead E was minimized through compressed feature
comm
transmission(average2.3KBperprediction).
Table 1 compares the stress detection performance across Latency measurements showed our system operated within the
methods, reported as mean ± standard deviation over 5 250ms window required for real-time irrigation control (based on
FIGURE2
TemporalevolutionofdroughtstressprobabilitiesshowingLSTMpredictions(dashedblueline)andPINN-correctedoutputs(solidredline)fora
representativedroughtstresseventinsoybean(Dataset:Soybean2023,NodeID:SB-17,July15-25,2023).X-axis:Time(days),Y-axis:Stress
probability(0-1,unitless).Shadedregionindicates±1standarddeviationacross5modelruns.Thecorrectionreducesfalsepositivesduringtransient
moisturefluctuationswhilemaintainingsensitivitytoactualstressonset.
| FrontiersinAgronomy |     |     |     |     |     |     | 08  |     |     |     |     |     | frontiersin.org |
| ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- |

| Yuetal. |     |     |     |     |     |     |     |     |     |     | 10.3389/fagro.2026.1764002 |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- |
(cid:129)
actuatordynamics:valveresponsetime100ms,safetymargin50ms, 22%reductioninirrigationwaterusage
samplinginterval60s).End-to-endlatencybreakdown(median/p95/ (cid:129) 18%fewerpesticideapplications
(cid:129) 95%systemuptimeinfieldconditions
p99):total210/245/320ms,LSTMinference45/52/68ms,LoRaWAN
| transmission | 110/125/150 | ms, edge | correction |     | 55/68/102 | ms. |     |     |     |     |     |     |
| ------------ | ----------- | -------- | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
Comparedto980/1250/1580msforcloud-basedapproaches. Theedgecorrectionsuccessfullyadaptedtolocalsoilvariations,
asshowninFigure4’sspatialhealthmaps.
| 5.4 Robustness |             | analysis |         |          |         |     |              |       |              |     |             |           |
| -------------- | ----------- | -------- | ------- | -------- | ------- | --- | ------------ | ----- | ------------ | --- | ----------- | --------- |
|                |             |          |         |          |         |     | 5.6 Ablation | study |              |     |             |           |
| We evaluated   | performance | under    | varying | sensor   | quality | and |              |       |              |     |             |           |
|                |             |          |         | system’s |         |     | We analyzed  | the   | contribution | of  | each system | component |
| environmental  | conditions. | Figure   | 3 shows | the      | ability | to  |              |       |              |     |             |           |
withstandhighersensornoiselevels,achievingover80%accuracy throughcontrolledremovals(Table2):
|     |     |     |     |     |     |     | The physics | constraints |     | delivered | the greatest | singular |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ----------- | --- | --------- | ------------ | -------- |
evenwhenthenoise-to-signalratioreaches30%.
The physics constraints proved particularly valuable during improvement (+8 points), which substantiated our hybrid
|               |         |                |     |      |                |     | learning method. |     | The energy | overhead | from | additional |
| ------------- | ------- | -------------- | --- | ---- | -------------- | --- | ---------------- | --- | ---------- | -------- | ---- | ---------- |
| novel weather | events. | When evaluated |     | on a | novel heatwave |     |                  |     |            |          |      |            |
scenario (ambient temperature +8 °C beyond the training range), componentsremainedbelow8%ofbaseline.
thehybridmodelachieved82%accuracy,comparedto54%forthe
LSTMalone.
|           |            |         |     |     |     |     | 6 Discussion    |          | and future |        | work      |     |
| --------- | ---------- | ------- | --- | --- | --- | --- | --------------- | -------- | ---------- | ------ | --------- | --- |
| 5.5 Field | deployment | results |     |     |     |     |                 |          |            |        |           |     |
|           |            |         |     |     |     |     | 6.1 Limitations |          | of the     | hybrid | LSTM-edge |     |
|           |            |         |     |     |     |     | correction      | approach |            |        |           |     |
Ahalf-yeardeployment(May-October2023)onanoperational
| 50-hectare | soybean farm | in Guangxi, | China | (23.5°N, | 109.2°E) |     |     |     |     |     |     |     |
| ---------- | ------------ | ----------- | ----- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- |
showed tangible advantages. The study employed a randomized Although the suggested framework shows notable progress
complete block design with 4 replicate plots per treatment: (1) compared to current approaches, a number of constraints merit
HybridLSTM-Edgesystem,(2)Threshold-basedcontrol(farmers’ efficacy
|     |     |     |     |     |     |     | examination. The |     | of the | system | is determined | primarily by |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ------ | ------ | ------------- | ------------ |
standardpractice),(3)StandaloneLSTM.Eachplotwas2hectares. thecaliberofthephysicalmodelsintegratedwithintheedgeadjustment
Weather normalization was performed using reference component.Inregionswheresoil-plant-atmospheredynamicsdeviate
evapotranspiration (ETo) calculations. Baseline year (2022) data substantially from the assumed PDE formulations, such as highly
fields
was collected for comparison. These results represent preliminary heterogeneous or novel crop varieties, the correction
observations with the following limitations: single-location study, mechanism may introduce biases rather than reduce errors.
one growing season, potential confounding from spatial Moreover, the existing approach necessitates repeated retraining of
soilvariability. the PINN elements as they are applied to different agricultural
FIGURE3
Predictionaccuracy(F1-score)underdifferentlevelsofsensornoise.X-axis:Noise-to-signalratio(%),rangingfrom0%(cleandata)to50%(highnoise).
Y-axis:F1-score(0-1).Resultsaveragedover100MonteCarlosimulationswithGaussiannoiseaddedtosensorreadings.Errorbarsrepresent95%
confidenceintervals.
| FrontiersinAgronomy |     |     |     |     |     | 09  |     |     |     |     |     | frontiersin.org |
| ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- |

Yuetal. 10.3389/fagro.2026.1764002
6.3 Scalability considerations for large-
scale agricultural operations
Scaling the system to thousands of field robots presents both
technical and algorithmic challenges. On the technical side, the
LoRaWAN communication backbone may become a bottleneck
when coordinating dense sensor networks across thousands of
hectares. Subsequent research may investigate mixed mesh
networking configurations, balancing proximate robot interactions
with extended-distance connections to edge servers. From an
algorithmicperspective,thefederatedlearningmethodforupdating
edge models requires improvement to address non-IID data
distributions arising from diverse soil types, management Data
Availability: The Soybean2023 and CitrusUAT-Extended datasets
FIGURE4
Spatialdistributionofcorrectedcrophealthmetrics(stress used in this study are available upon reasonable request from the
probability,0–1scale)acrossthe50-hectareproductionfieldon
correspondingauthors.Datapreprocessingscripts(Python3.9)and
August10,2023.Themapshowskriging-interpolatedvaluesfrom
32sensornodes(markedasblackdots).Colorscale:green(low model configuration files (YAML format) are provided in the
stress,<0.3),yellow(moderatestress,0.3-0.6),red(highstress,>0.6). Supplementary Materials. Due to privacy agreements with
Thespatialpatterncorrelateswithsoiltexturevariations(higher
participating farms, raw sensor location data is anonymized. Code
stressinsandyareas,lowerstressinclay-richzones).
repository: github.com/gxstnu/hybrid-lstm-edge (available upon
paper acceptance).practices, and crop rotations across different
settings,whichposespracticalobstaclesforbroadimplementation.The fields. A promising approach employs meta-learning methods
energy data further indicate an unavoidable compromise: while our thattraincorrection modelsonvaried agricultural settings,which
hybridapproachuses72.8%lesspowercomparedtocloudoffloading,it
supports quicker adjustment to novel regions. The spatial Fourier
demands 6.4 times more energy than basic threshold-based neural operator shows particular potential here, as its spectral
mechanisms. This trade-off may limit deployment in solar-powered approach naturally handles multi-scale field variability.
fieldroboticsoperatingunderstrictenergybudgets.
Nevertheless, the implementation of these models necessitates the
6.2 Potential application scenarios for the joint development of the network architecture alongside edge
proposed system hardwarecapacitiestoupholdreal-timeperformance.
The framework shows particular promise in three agricultural
contextswheretraditionalmethodsstruggle.Initially,perennialcrops 7 Conclusion
with high economic value, such as vineyards and orchards, gain
advantages from the system’s capacity to simulate prolonged stress
The hybrid LSTM-edge correction architecture presents a
accumulation and spatially diverse microclimates. Second, in areas
notable progress in distributed agricultural robotics by achieving
withlimitedwaterresources,precisionirrigationcanapplyphysics-
an optimal equilibrium between computational performance and
basedadjustmentstoimprovewaterefficiencywithoutreducingcrop
biological accuracy. The system attains real-time crop health
production. Third, in organic farming systems, where chemical
monitoring by hierarchically merging lightweight on-device
treatments must be carefully timed, early pest identification could
LSTMs and physics-informed neural networks at the edge,
employ the hybrid predictions to reduce unnecessary preventive preserving the interpretability and robustness necessary for field
spraying. The modular structure of the architecture also permits deployment. The experimental findings show steady progress
adjustments extending past crop health surveillance, for instance,
compared to individual methods, especially in addressing sensor
connecting with models forecasting harvests or systems managing
noise, spatial variability, and unfamiliar environmental scenarios.
greenhouse atmospheric conditions. These applications would The framework’s capacity to assimilate older sensors while
necessitate expanding the PDE frameworks to encompass imposing physical limitations presents tangible benefits for
supplementary biophysical phenomena while preserving the
currentagriculturalpracticesadoptingprecisionmethods.
computationalperformanceoftheexistingapproach.
The achievement of the architecture arises from its methodical
blendingofdata-drivenandphysics-basedmodelingapproaches.The
TABLE2 Ablationstudy(soybeanF1-score). LSTM elements identify intricate time-based relationships in sensor
data, whereas the edge-deployed physics-informed neural networks
Configuration Accuracy Energy guarantee that predictions comply with core biophysical laws. This
combination proves especially valuable in agriculture, where purely
FullSystem 0.89 5.1J
data-driven models often fail under changing field conditions or
w/oPhysicsLoss 0.81 4.9J
limitedtrainingdata.Thedecentralizedexecutionpreservesthequick
w/oLSTMPretrain 0.83 5.3J
reaction necessary for urgent actions, with power usage patterns
w/oDynamicWeighting 0.85 5.0J appropriateforroboticsinsolar-poweredoutdoorsettings.
FrontiersinAgronomy 10 frontiersin.org

| Yuetal. |     |     |     |     |     |     |     |     |     |     | 10.3389/fagro.2026.1764002 |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | --- |
Apartfromdirectfarminguses,themixedmethodservesasa Demonstration of Tower and Mast Intelligent Operation and
modelforadditionalfieldsneedingcontinuousobservationwithin Maintenance Technology in Mountainous and Hilly Areas Based
onBeidouSatelliteBasedEnhancement”(No.GuikeAB25069262).
| material | limitations. | The | overarching |     | structure | of  | on-device |     |     |     |     |     |     |     |
| -------- | ------------ | --- | ----------- | --- | --------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
attributederivationsucceededbyedge-assistedphysics-informed
| adjustment    | can | be applied |             | to ecological |                       | surveillance, |     |     |     |     |     |     |     |     |
| ------------- | --- | ---------- | ----------- | ------------- | --------------------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| manufacturing |     | operation  | regulation, |               | or biological-medical |               |     |     |     |     |     |     |     |     |
Conflict
of interest
| setups.  | Subsequent   | developments |          | may           | investigate |          | advanced |               |          |      |           |               |     |        |
| -------- | ------------ | ------------ | -------- | ------------- | ----------- | -------- | -------- | ------------- | -------- | ---- | --------- | ------------- | --- | ------ |
| physical | frameworks,  |              | flexible | communication |             | methods, | and      |               |          |      |           |               |     |        |
|          |              |              |          |               |             |          |          | The author(s) | declared | that | this work | was conducted |     | in the |
| deeper   | coordination | with         | robotic  | control       | mechanisms. |          | The      |               |          |      |           |               |     |        |
absenceofanycommercialorfinancialrelationshipsthatcouldbe
currentlimitationsinmodelgeneralizationandenergyefficiency
construedasapotentialconflictofinterest.
| point to | promising | research |     | directions | in meta-learning |     | and |     |     |     |     |     |     |     |
| -------- | --------- | -------- | --- | ---------- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
hardware-softwareco-design.
|      |              |     |                    |     |     |          |         | Generative    | AI statement        |      |            |        |             |        |
| ---- | ------------ | --- | ------------------ | --- | --- | -------- | ------- | ------------- | ------------------- | ---- | ---------- | ------ | ----------- | ------ |
| Data | availability |     | statement          |     |     |          |         |               |                     |      |            |        |             |        |
|      |              |     |                    |     |     |          |         | The author(s) | declared            | that | generative | AI was | used        | in the |
|      |              |     |                    |     |     |          |         | creation      | of this manuscript. | AIGC | played     | a role | in language |        |
| The  | Soybean2023  | and | CitrusUAT-Extended |     |     | datasets | used in |               |                     |      |            |        |             |        |
this study are available upon reasonable request from the polishing and logical analysis during the writing process of
thisarticle.
| corresponding | authors. |     | Data preprocessing |     | scripts | (Python | 3.9) |     |     |     |     |     |     |     |
| ------------- | -------- | --- | ------------------ | --- | ------- | ------- | ---- | --- | --- | --- | --- | --- | --- | --- |
Anyalternativetext(alttext)providedalongsidefiguresinthis
andmodelconfigurationfiles(YAMLformat)areprovidedinthe
articlehasbeengeneratedbyFrontierswiththesupportofartificial
| Supplementary |     | Materials. | Due | to privacy |     | agreements | with |     |     |     |     |     |     |     |
| ------------- | --- | ---------- | --- | ---------- | --- | ---------- | ---- | --- | --- | --- | --- | --- | --- | --- |
participatingfarms,rawsensorlocationdataisanonymized.Code intelligence and reasonable efforts have been made to ensure
|     |     |     |     |     |     |     |     | accuracy, | including review | by  | the authors | wherever | possible. | If  |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ---------------- | --- | ----------- | -------- | --------- | --- |
repository:https://github.com/gxstnu/hybrid-lstm-edge.
youidentifyanyissues,pleasecontactus.
| Author | contributions |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ------ | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Publisher’s
note
| RY: | Formal analysis, |     | Methodology, | Writing |     | – review | & editing. |     |     |     |     |     |     |     |
| --- | ---------------- | --- | ------------ | ------- | --- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
–
| YX: Project | administration, |     | Data | curation, | Writing | original | draft, |     |     |     |     |     |     |     |
| ----------- | --------------- | --- | ---- | --------- | ------- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- |
Allclaimsexpressedinthisarticlearesolelythoseoftheauthors
| Conceptualization.RW: |     | Conceptualization,Methodology, |     |     |     |     | Writing | –      |                 |           |       |          |            |     |
| --------------------- | --- | ------------------------------ | --- | --- | --- | --- | ------- | ------ | --------------- | --------- | ----- | -------- | ---------- | --- |
|                       |     |                                |     |     |     |     |         | and do | not necessarily | represent | those | of their | affiliated |     |
review&editing,Formalanalysis.WL:Conceptualization,Writing–
|     |     |     |     |     |     |     |     | organizations, | or those | of the | publisher, | the editors | and | the |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | -------- | ------ | ---------- | ----------- | --- | --- |
review&editing,Validation,Formalanalysis,Investigation.
|     |     |     |     |     |     |     |     | reviewers. | Any product | that may | be evaluated | in  | this article, | or  |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ----------- | -------- | ------------ | --- | ------------- | --- |
claimthatmaybemadebyitsmanufacturer,isnotguaranteedor
endorsedbythepublisher.
Funding
| Theauthor(s) |         | declared         | thatfinancialsupport |           |         | wasreceivedfor |        |               |     |          |     |     |     |     |
| ------------ | ------- | ---------------- | -------------------- | --------- | ------- | -------------- | ------ | ------------- | --- | -------- | --- | --- | --- | --- |
|              |         |                  |                      |           |         |                |        | Supplementary |     | material |     |     |     |     |
| this work    | and/or  | its publication. |                      | This work | was     | supported      | by the |               |     |          |     |     |     |     |
| Guangxi      | Science | and Technology   |                      | Plan      | Project | “Research      | and    |               |     |          |     |     |     |     |
Application of Machine Vision for Rapid Multi-Target TheSupplementaryMaterialforthisarticlecanbefoundonline
Differential Detection” (No.GuiKe AD23026282) and Key R&D at: https://www.frontiersin.org/articles/10.3389/fagro.2026.1764002/
“Research
Program Project in Guangxi and Application full#supplementary-material
References
Abdulghani, A. M., Abdulghani, M. M., Walters, W. L., and Abed, K. H. (2022). Chantima,P.,Yarnguy,T.,Sarawan,K.,Chanthan,P.,Wongkhan,S.,andPhromsorn,
“Cyber-physical N..(2025).“Hybridintelligenceforfield-scalesoilanalysisandcropadvisoryusing
|     | system | based | data mining | and | processing | toward | autonomous |     |     |     |     |     |     |     |
| --- | ------ | ----- | ----------- | --- | ---------- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- |
agricultural systems,” in 2022 International Conference on Computational Science embeddedsensorsandmachinelearning,”inIEEEGlobalConferenceOnArtificial
andComputationalIntelligence(CSCI),LasVegas,NV,USA:IEEE. IntelligenceAndComputing.IEEE.
Abedalrhman,K.,andAlzaydi,A.(2025).Agriculture4.0:integratingadvancedIoT, Farea,A.,Yli-Harja,O.,andEmmert-Streib,F.(2025).Usingphysics-informedneural
AI, and robotics solutions for enhanced yield, sustainability, and resource networksformodelingbiologicalandepidemiologicaldynamicalsystems.Mathematics
optimization-evidencefromagricultural….Agric.Pract.Syria.
13,1664.doi:10.3390/math13101664
Abhishek,P.,andRamesh,V.(2024).Farminginthedigitalsky:cloud-basedapproaches Gómez-Flores,W.,Garza-Saldaña,J.J.,Flores-Perez,A.,Gomez-Garcia,M.A.,and
forsustainableagriculture.J.CloudComput.13,45–62.doi:10.46727/c.17-18-05-2024
Duarte-Galvan,C..(2024).CitrusUAT:AdatasetoforangeCitrussinensisleavesfor
|     |     |     |     |     |     |     |     | abnormality | detection using image | analysis | techniques. | Data | Brief 52, | 109908. |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --------------------- | -------- | ----------- | ---- | --------- | ------- |
Baseca,C.C.,Dionıśio,R.,Ribeiro,F.,andMetrôlho,J.(2025).Edge-computingsmart
|            |            |               |     |          |                |            | deficit | doi:10.1016/j.dib.2023.109908 |     |     |     |     |     |     |
| ---------- | ---------- | ------------- | --- | -------- | -------------- | ---------- | ------- | ----------------------------- | --- | --- | --- | --- | --- | --- |
| irrigation | controller | using LoRaWAN |     | and LSTM | for predictive | controlled |         |                               |     |     |     |     |     |     |
irrigation.Sensors25,7079.doi:10.3390/s25227079
|     |     |     |     |     |     |     |     | Gu, Z., Qi, | Z., Burghate, R., Yuan, | S., | Jiao, X., and | Zhang, Y.. | (2020). | Irrigation |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ----------------------- | --- | ------------- | ---------- | ------- | ---------- |
schedulingapproachesandapplications:Areview.JournalofIrrigationandDrainage
Cai,S.,Mao,Z.,Wang,Z.,Yin,M.,andKarniadakis,G.E.(2021).Physics-informedneuralnetworks
(PINNs)forfluidmechanics:Areview.ActaMech.Sin.37,1–20.doi:10.1007/s10409-021-01148-1 Engineering146,04020066.doi:10.1061/(ASCE)IR.1943-4774.0001464
| FrontiersinAgronomy |     |     |     |     |     |     |     | 11  |     |     |     |     | frontiersin.org |     |
| ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- |

Yuetal. 10.3389/fagro.2026.1764002
Khadatkar, D. R. (2024). “Optimizing resource allocation in precision agriculture Sargun,K.,andMohan,S.(2020).Modelingthecropgrowth-areview.Mausam71,1–
through the application of K-means clustering,” in Smart Agriculture: Harnessing 14.doi:10.54302/mausam-v71i1.10
MachineLearning(BocaRaton,FL,USA:CRCPress/Taylor&FrancisGroup). Serena,L.,Zichichi,M.,D’Angelo,G.,andFerretti,S..(2021).“Simulationofhybrid
Kim,K.,Jang,S.J.,Park,J.,Lee,E.,andLee,S.S.(2023).Lightweightandenergy- edgecomputingarchitectures,”in2021IEEE/ACM25thInternationalSymposiumOn
efficient deep learning accelerator for real-time object detection on edge devices. DistributedSimulationAndRealTimeApplications.IEEE/ACM
Sensors,23,1185.doi:10.3390/s23031185 Siami-Namini,S.,Tavakoli,N.,Mirzaei,A.,andNamin,A..(2018).“Acomparisonof
Lançon,J.,Wery,J.,Rapidel,B.,Angokaye,M.,Goze,M.,Scopel,E.,etal.(2007).An ARIMA and LSTM in forecasting time series,” in 2018 17th IEEE International
improvedmethodologyforintegratedcropmanagementsystems.Agron.Sustain.Dev. ConferenceOnMachineLearningAndApplications(ICMLA).Orlando,FL,USA:IEEE.
27,161–173.doi:10.1051/agro:2006037
Song,T.,Si,Y.,Gao,J.,Wang,W.,Nie,C.,andKlemes,̌ J.J.(2023).Predictionand
Lewandowski, I., Härdtlein, M., and Kaltschmitt, M. (1999). Sustainable crop monitoringmodelforfarmlandenvironmentalsystemusingsoilsensorandneural
production:definitionandmethodologicalapproachforassessingandimplementing networkalgorithm.OpenPhys.21,20220224.doi:10.1515/phys-2022-0224
sustainability.CropSci.39,25–38.doi:10.2135/cropsci1999.0011183X003900010029x
Suresh,M.L.,Rao,T.K.,Gokilamani,S.,Muthukumar,P.,andKoteeswaran,S..(2025).
Li,Z.,Kovachki,N.,Azizzadenesheli,K.,Liu,B.,Bhattacharya,K.,andStuart,A..(2021). Ahybridconvolutionalneuralnetwork-temporalattentionmechanismapproachfor
“Fourier neural operator for parametric partial differential equations,” in International real-timepredictionofsoilmoistureandtemperatureinprecisionagriculture.Agric.
ConferenceonLearningRepresentations(ICLR2021).VirtualConference:OpenReview. WaterManage.295,109182.doi:10.14569/IJACSA.2025.0160556
Li,P.,Koyuncu,E.,andSeferoglu,H.(2023).Adaptiveandresilientmodel-distributed Yang,F.,Fu,X.,Yang,Q.,andChu,Z.(2024).Decompositionstrategyandattention-
inferenceinedgecomputingsystems.IEEEOpenJ.Comput.Soc.4,1–15.doi:10.1109/ basedlongshort-termmemorynetworkformulti-stepultra-short-termagricultural
OJCOMS.2023.3280174 powerloadforecasting.ExpertSyst.Appl.238,121831.doi:10.1016/j.eswa.2023.122226
Liu,J.,Du,Y.,Yang,K.,Wu,J.,Wang,Y.,Hu,X.,etal.(2025).Edge-cloudcollaborative Yi,S.,Li,C.,andLi,Q.(2015).“Asurveyoffogcomputing:concepts,applicationsand
computingondistributedintelligenceandmodeloptimization:Asurvey.IEEEInternetThingsJ. issues,”inProceedingsofthe2015workshoponmobilebigdata.Hangzhou,China:ACM
Lou,Z.,Wang,F.,Peng,D.,Zhang,X.,Xu,J.,Zhu,X.,etal.(2023).Combiningshape Zhang, X., Cao, Z., and Dong, W. (2020). Overview of edge computing in the
andcropmodelstodetectsoybeangrowthstages.RemoteSens.Environ.295,113827. agriculturalinternetofthings:Keytechnologies,applications,challenges.IEEEAccess
doi:10.1016/j.rse.2023.113827 8,175946–175958.doi:10.1109/ACCESS.2020.3013005
Penuelas,J.,andSardans,J.(2021).Developingholisticmodelsofthestructureand Zhang, Y., Wang, X., Jin, L., Ni, J., Zhu, Y., Cao, W., et al. (2025). Research and
functionofthesoil/plant/atmospherecontinuum.PlantSoil460,5–17.doi:10.1007/ developmentofanIoTsmartirrigationsystemforfarmlandbasedonLoRaandedge
s11104-020-04641-x computing.Comput.Electron.Agric.225,109182.doi:10.3390/agronomy15020366
FrontiersinAgronomy 12 frontiersin.org