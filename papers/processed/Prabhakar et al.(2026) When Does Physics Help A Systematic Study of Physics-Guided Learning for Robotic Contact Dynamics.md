PublishedasaconferencepaperatICLR2026
WHEN DOES PHYSICS HELP? A SYSTEMATIC STUDY
OF PHYSICS-GUIDED LEARNING FOR ROBOTIC CON-
TACT DYNAMICS
ChinmayeePrabhakar PrathameshDineshJoshi
prabhakar.chinmayee@gmail.com VizuaraAILabs
prathamesh@vizuara.com
RajDandekar RajatDandekar SreedathPanat
VizuaraAILabs VizuaraAILabs VizuaraAILabs
raj@vizuara.com rajatdandekar@vizuara.com sreedath@vizuara.com
ABSTRACT
Robotic manipulation frequently involves contact with objects whose material
propertiesareunknown,whileforceandstatemeasurementsaresparse,noisy,or
unreliable. Learning accurate and physically valid contact dynamics under such
conditionsremainsacorechallenge.Classicalcontactmodelsrelyonper-material
parameter tuning and do not scale across heterogeneous objects, while purely
data-driven models degrade under limited supervision and often violate physical
constraints. Physics-informed neural networks (PINNs) and Universal Differen-
tialEquations(UDEs)providepromisingalternatives,butitisunclearwhenand
how physics-based inductive biases actually improve learning. In this work, we
conductasystematicstudyofphysics-guidedlearningforsoftcontactdynamics
usingamaterial-conditionedODEformulationwithexplicitequalityandinequal-
ity constraints. We compare data-only models, PINNs, and UDEs across con-
trolledvariationsindatasparsity,noise,andtemporalscope.Ourresultsshowthat
while physics offers limited benefit in data-rich regimes, it becomes critical un-
dersparsesupervision: forceerrorsreducebyupto53%,friction-coneviolations
dropbyupto68%, zero-shottransfertounseenmaterialsimprovesby14–29%,
andphysics-informedmodelsmatchfullysupervisedperformancewithin5%us-
ingnomaterial-specifictrainingdata. Thesefindingsclarifythepracticalroleof
physics constraints as structured regularizers for reliable learning in real-world
roboticcontactscenarios.
1 INTRODUCTION
Roboticmanipulationfundamentallyreliesonphysicalcontactwithobjectswhosematerialproper-
tiesareoftenunknown,variable,orpoorlysensed.Accuratemodelingofcontactdynamicsiscritical
fortasksrangingfromgraspingandinsertiontocompliantmanipulationandforce-controlledinter-
action (Mason, 2001). Yet in realistic settings, force and state measurements are sparse, noisy, or
unreliable, andcontactbehaviorvariessignificantlyacrossmaterials, makinggeneralizationaper-
sistentchallenge(Villalongaetal.,2021).
Classicalcontactmodels, suchasLuGre-typefrictionformulations(DeWitetal.,1995), offerin-
terpretable and physically grounded descriptions of contact interactions. However, they typically
requireper-materialparameteridentificationandcarefultuning(Dupontetal.,2002;Marquesetal.,
2016), limiting scalability across heterogeneous objects and environments. At the other extreme,
purely data-driven models provide flexibility (Nagabandi et al., 2018; Chua et al., 2018) but fre-
quentlyviolatefundamentalphysicalconstraints,suchasfrictioncones,anddegradesharplywhen
observations are limited (Lutter et al., 2019). These limitations motivate incorporating physical
structurewithoutsacrificingflexibilityorscalability.
1

PublishedasaconferencepaperatICLR2026
Recent advances in scientific machine learning (SciML) (Karniadakis et al., 2021; Willard et al.,
2022), particularly Physics-Informed Neural Networks (PINNs) (Raissi et al., 2019) and Univer-
sal Differential Equations (UDEs) (Rackauckas et al., 2020), provide a promising framework for
addressing this challenge. By embedding differential equation structure into learning objectives,
these methods combine mechanistic modeling with data-driven components (Chen et al., 2020).
While PINNs and UDEs have demonstrated success in domains such as fluid dynamics and reac-
tion–diffusion systems (Cai et al., 2021; Liu et al., 2022), their role in contact mechanics, where
inequality constraints, material heterogeneity, and data scarcity are central, remains insufficiently
understood.
In this work, we present a systematic empirical study of physics-guided learning for soft contact
dynamics. Wemodelcontactwithafirst-orderODEcapturingnormalindentation,tangentialbristle
dynamics, andfrictionalinteractions(Hunt&Crossley,1975;Dahl,1976), andrepresentmaterial
variationthroughlearnedcontinuousembeddings(Xuetal.,2021;Pfrommeretal.,2021). Thisen-
ablesasinglemodeltorepresentdiversecontactbehaviorswithoutper-materialretraining.Wecom-
pare data-only learning, PINNs enforcing differential equation residuals, and UDE-based residual
learningundercontrolledvariationsindatadensity,noise,andtemporalscope,explicitlyseparating
equality-basedphysicsresidualsfrominequalityenforcementviaCoulombfrictionconstraints.
CONTRIBUTIONS
Thispapermakesthefollowingcontributions:
1. Weprovideacontrolledempiricalanalysisofwhenandwhyphysics-informedconstraints
improve learning for contact dynamics, under varying data density, noise, and temporal
scope.
2. Wedemonstratezero-shotmaterialgeneralization, achieving14–29%errorreductionand
performance within 5% of fully supervised materials without material-specific training
data.
3. We disentangle differential equation residual enforcement from inequality constraint en-
forcement,clarifyingtheirdistinctandcomplementaryeffectsonphysicaladmissibility.
4. WeshowthatUDEsrecoverlatentdissipationparameterswithintheclassoflinearviscous
damping(Eq.12).
2 METHODOLOGY
2.1 CONTACTDYNAMICSFRAMEWORK
We model contact using a first-order ODE system inspired by the LuGre friction model (De Wit
etal.,1995),describingnormaldisplacementδ(t),normalcontactvelocityv(t) = δ˙(t),andbristle
deflectionz(t). WeadoptareducedLuGre-inspiredformulationwherebristledynamicsaredriven
byrelativecontactvelocityalongtheinteractiondirection.
dδ
=v(t) (1)
dt
dv
m =−c v−kδ+F (2)
dt n ext
dz |v|z
=v− (3)
dt v
s
wheremiseffectivemass,k iscontactstiffness,c isdamping,v isStribeckvelocity,andF is
n s ext
externalforcing. NormalandtangentialforcesarecomputedfrompredictedstatesasF = kδ and
n
F = σ z (DeWitetal.,1995). ThesystemalsoenforcestheCoulombfrictioninequality(Dupont
t 0
etal.,2002):
|F |≤µ|F | (4)
t n
2

PublishedasaconferencepaperatICLR2026
Materialheterogeneityisparameterizedby(k,c ,σ ,µ,v )spanningtypicalmanipulationregimes
n 0 s
(AppendixTable4). Ratherthantrainingseparatemodelspermaterial,weemploylearnedembed-
dings(Section2.3.4),enablingasinglemodeltocaptureallbehaviors.
2.2 SYNTHETICDATAGENERATION
We generate controlled data from ten materials (Appendix Table 4) by solving Equations (1)–(3)
usingTsit5(Tsitouras,2011)overt∈[0,5]swithmulti-frequencyforcing
F (t)=150+200sin(2π·0.3t)+100sin(2π·0.8t)+50sin(2π·1.5t).
ext
The DC offset (150 N) and sinusoidal amplitudes (200, 100, 50 N) were chosen to yield contact
forces spanning a broad portion of the material range in Appendix Table 4 without causing loss
ofcontact, whilethethreefrequencies(0.3, 0.8, 1.5Hz)wereselectedtoexcitemultipledynamic
regimesofthebristleODEandremainwell-resolvedatthechosensamplinginterval(∆t=0.01s;
AppendixTable5). UniformadditiveGaussiannoiseN(0,σ2)isappliedtoallstatechannelswith
σ ∈ {0.01,0.02}. These levels span a realistic soft-contact sensing range: σ = 0.01 corresponds
to roughly 5% of the mean normal force (F¯ ≈ 200 N), while σ = 0.02 represents a substan-
n
tiallynoisiercompliant-manipulationregimeconsistentwithdegradedcontactestimationfromslip,
micro-impacts,andcompliance(Villalongaetal.,2021). Highernoiselevelsarenotconsidered,as
theyrendertheunderlyingODEparameterspoorlyidentifiedfromobservations,anissueorthogonal
tothequestionofwhenphysicsconstraintsprovidevalue.
Each trajectory is split 70/15/15 train/validation/test for seven training materials; Materials 3, 6,
and 9 are held out entirely (0% supervision), yielding N=819 total training points. For temporal
extrapolation,modelsaretrainedont∈[0,3]sandevaluatedont∈[3,5]s.
2.3 MODELARCHITECTURES
Wecomparethreemodelingparadigmstoisolatetheeffectsofphysicsconstraints.Allmodelsshare
identical architectures (five hidden layers, swish activations (Ramachandran et al., 2017), tanh
output), optimizers, and training schedules unless otherwise stated. Input time is encoded using
11-dimensionalFourierfeatures(Tanciketal.,2020),andalearnedscalingnetworkmapsmaterial
embeddingstoper-materialoutputscalesforδandv.
2.3.1 DATA-ONLYBASELINE
AfeedforwardnetworkmapsmaterialembeddingsandFourier-encodedtimetosystemstates,
[δ,v,z]=f (embedding,ϕ(t)),
θ
whereϕ(t)denotestheFouriertimefeatures,withtraininglossgivenbymeansquarederror(MSE)
on the state variables. This baseline is deliberately a trajectory regression model (time → state)
rather than a learned simulator with rollout guarantees, isolating the marginal value of explicit
physicsstructureoverstrongfunctionapproximation. WeomitNeuralODEbaselines(Chenetal.,
2018)toisolatetheimpactofexplicitphysicsconstraintsratherthancontinuous-timeparameteriza-
tion.
2.3.2 PHYSICS-INFORMEDNEURALNETWORK(PINN)
Physics-informed neural networks (PINNs) (Raissi et al., 2019) augment data loss with residual
penaltiesenforcingEquations(1)–(3):
L =L +λ MSE(R )+λ MSE(R )+λ MSE(R ) (5)
PINN data R1 1 R2 2 R3 3
where
dδ
R = −v (6)
1 dt
dv
R =m +c v+kδ−F (7)
2 dt n ext
dz |v|z
R = −v+ (8)
3 dt v
s
Temporalderivativesareevaluatedusingsecond-ordercentralfinitedifferences(AppendixTable5).
3

PublishedasaconferencepaperatICLR2026
2.3.3 PINNWITHINEQUALITYCONSTRAINTS
| StandardPINNsmayviolateCoulombfriction(Eq.4). |     |     | Weaddaquadraticpenalty: |     |     |     |
| --------------------------------------------- | --- | --- | ----------------------- | --- | --- | --- |
N
1 (cid:88)
|     | L        | = max(0,|F | |−µ|F | |)2 |     | (9) |
| --- | -------- | ---------- | ----- | --- | --- | --- |
|     | friction |            | t,i   | n,i |     |     |
N
i=1
combinedwithanon-negativitypenaltyonnormalforce:
N
1 (cid:88)
|     | L =λ             | L +λ          | max(0,−F | )2  |     | (10) |
| --- | ---------------- | ------------- | -------- | --- | --- | ---- |
|     | contact friction | friction negN |          | n,i |     |      |
i=1
withλ =1.5andλ =0.02,weightedbyanoverallconstraintcoefficientλ =0.5.
| friction | neg |     |     |     | ineq |     |
| -------- | --- | --- | --- | --- | ---- | --- |
Weuseasquaredhingepenaltybecauseitprovidessmoothgradientsandpenalizeslargeviolations
morestronglythanalinearhinge,whileremainingsimplerthanbarrierobjectives.Thethreeweights
decouplefriction-coneandnon-penetrationpenaltiesfromtheoverallstrengthofinequalityenforce-
mentrelativetodataandresiduallosses. Weightswerefixedacrossallconditions;±50%perturba-
tionsproducednoqualitativechanges, includingindenseregimeswheretheCoulombpenaltydid
notreduceviolations.
Hard-constraintapproaches(e.g.,projectionorKKT-basedlayers)providestrictadmissibilityguar-
antees but are less stable under sparse supervision. We therefore use a soft quadratic penalty as a
pragmatictrade-off: itcannotguaranteestrictfeasibility,butitreducesCoulombviolationsby58–
68% in sparse regimes while remaining compatible with standard gradient-based training. Barrier
andvariationalinequalityalternativesarediscussedinSection4.2.
2.3.4 UNIVERSALDIFFERENTIALEQUATION(UDE)
TheUDE (Rackauckasetal.,2020)experimentaddressesadifferentquestionfromthePINNabla-
tion: whetherresidualsignalsalonecanrecoverlatentphysicalparameterswithoutdirectsupervi-
sion. TheUDEformulationtestsunsupervisedparameterdiscoverybyreplacingthelineardamping
termc n vwithalearnedfunction:
dv
|     | m   | =−g (v,embedding)−kδ+F |     |     |     | (11) |
| --- | --- | ---------------------- | --- | --- | --- | ---- |
|     |     | θ                      |     | ext |     |      |
dt
whereg θ isstructuredasanexplicitfactorization:
g (v,e)=v·cˆ (e), cˆ (e)=s·softplus(h (e)), s=exp(logs ) (12)
| θ   | n   | n   | θ   |     | 0   |     |
| --- | --- | --- | --- | --- | --- | --- |
Here h is a small multilayer perceptron mapping the material embedding e to a raw coefficient,
θ
| softplusensurespositivity,ands |     | isalearnablescaleparameter. |     |     |     |     |
| ------------------------------ | --- | --------------------------- | --- | --- | --- | --- |
0
Critically, c is removed from both inputs and supervision, so dissipation must be inferred solely
n
| fromthedynamicsresidualR | 2 . |     |     |     |     |     |
| ------------------------ | --- | --- | --- | --- | --- | --- |
Weemployatwo-stageprocedure(Rackauckasetal.,2020): firsttrainstatepredictorsthroughthe
fullpipeline(Section2.4),thenfreezethemandtrainonlyg usingtheR residualfor400epochs.
|                                |     |                          | θ   | 2   |     |     |
| ------------------------------ | --- | ------------------------ | --- | --- | --- | --- |
| Thispreventstrivialrecoveryofc |     | throughdatacorrelations. |     |     |     |     |
n
Materialembeddings: Welearnacontinuous32-dimensionalembeddingfrom(k,σ ,µ,v ),ex-
|     |     |     |     |     | 0   | s   |
| --- | --- | --- | --- | --- | --- | --- |
cludingc topreventtrivialrecovery. Acontrastivelossisusedonlytostabilizeembeddinggeom-
n
etryandsupportzero-shotinterpolation.
2.4 TRAININGPROCEDURE
All models are trained using a three-stage schedule: data-only pretraining (500 epochs), physics-
augmentedtraining(800epochs),andL-BFGSrefinement(Liu&Nocedal,1989)(300iterations).
Momentum-basedadaptiveresidualscaling(Wangetal.,2021)balancesheterogeneousunitsacross
residuals (β=0.95, converged weights λ ≈1.0, λ ≈0.25, λ ≈0.35). Complete hyperparame-
|     |     | R1 R2 | R3  |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- |
tersareprovidedinAppendixTable5.
4

PublishedasaconferencepaperatICLR2026
Collocation and derivatives: Residuals are evaluated at all sampled training timestamps using
second-ordercentralfinitedifferenceswith∆t = 0.01s(AppendixTable5). Weusefinitediffer-
encesratherthanautomaticdifferentiationinttomatchthediscreteobservationsettingandavoid
amplifyingnoisethroughhigh-variancederivatives;asystematicFD-versus-ADcomparisonisleft
forfuturework.
| 2.5 EXPERIMENTALDESIGN: | SYSTEMATICABLATION |     |     |     |
| ----------------------- | ------------------ | --- | --- | --- |
We design controlled experimental conditions spanning a 2 ×2 × 2 factorial design along three
dimensions:
• Data density: Dense (N = 819) versus sparse (N ≈ 34 after 10× subsampling). We
use these two extremes to create a clear causal contrast between near fully-observed and
severely underdetermined regimes; intermediate sample-efficiency thresholds are left for
futurework.
• Noiselevel: Lownoise(σ =0.01)andhighnoise(σ =0.02),appliedasuniformadditive
Gaussiannoiseacrossallstatechannels.
• Temporalscope:Interpolation(trainingandtestingon[0,5]s)versusextrapolation(train-
ingon[0,3]sandtestingon[3,5]s).
Thisyieldseightexperimentalconditions. Ineach,data-only,PINN,andPINN+penaltymodelsare
evaluated using: (i) mean absolute error (MAE) on δ, v, F , and F ; (ii) unscaled RMS physics
n t
residualsaggregatedoverR ,R ,R ;(iii)Coulombviolationrate(|F |>µ|F |+ϵ,ϵ=0.01N);
| 1   | 2 3 |     | t n |     |
| --- | --- | --- | --- | --- |
and(iv)zero-shotMAEonheld-outMaterials3,6,and9.
For fair comparison, the data scaler is frozen after pretraining so physics-informed models do not
benefitfromadaptednormalizationduringphysicstraining.
3 RESULTS
| 3.1 ABLATIONSTUDY: PHYSICSCONSTRAINTSINDENSEVS.SPARSEREGIMES |     |     |     |     |
| ------------------------------------------------------------ | --- | --- | --- | --- |
Wereportresultsforthe2×2×2ablationdescribedinSection2. Table1andFigure1summarize
performanceacrossconditions(σ=0.01andσ=0.02);fullresultsareinAppendixTable7.
Table1: Ablationresultsacrossdataregimesandconstraintenforcement. Lowandhighnoisecor-
respondtoσ = 0.01andσ = 0.02,respectively. Reportedmetricsaretest-setdisplacementMAE,
normalforceMAE,unscaledRMSphysicsresidual(aggregatedoverR ,R ,R ),andpercentageof
|     |     |     | 1 2 3 |     |
| --- | --- | --- | ----- | --- |
Coulombfrictionviolations. Allrowsinthistablecorrespondtotheinterpolationsetting(train/test
ont∈[0,5]s).
RMSRes.†
| Regime Method             | δMAE(m) | F n MAE(N) | CoulombViol.(%) |      |
| ------------------------- | ------- | ---------- | --------------- | ---- |
| Dense(N =819),LowNoise(σ  | =0.01)  |            |                 |      |
| Data-only                 | 0.0186  | 37.83      | 0.368           | 15.5 |
| PINN(nopenalty)           | 0.0117  | 17.79      | 0.179           | 16.0 |
| PINN(+penalty)            | 0.0128  | 24.89      | 0.219           | 16.0 |
| Sparse(N =34),LowNoise(σ  | =0.01)  |            |                 |      |
| Data-only                 | 0.0504  | 198.91     | 1.014           | 51.6 |
| PINN(nopenalty)           | 0.0337  | 113.71     | 0.666           | 20.3 |
| PINN(+penalty)            | 0.0365  | 123.65     | 0.745           | 8.6  |
| Sparse(N =34),HighNoise(σ | =0.02)  |            |                 |      |
| Data-only                 | 0.0490  | 184.36     | 0.964           | 38.3 |
| PINN(nopenalty)           | 0.0464  | 149.29     | 0.875           | 17.2 |
| PINN(+penalty)            | 0.0375  | 117.59     | 0.735           | 5.5  |
†RMSresidualisunscaledandaggregatedoverR
|     |     | 1 ,R 2 ,andR 3 . |     |     |
| --- | --- | ---------------- | --- | --- |
Tradeoffanalysis: Indenseregimes,equalityresidualsaloneyieldsubstantialaccuracygains(F
n
MAE:37.83→17.79N)butinequalityviolationspersistat16%. Insparseregimes,PINN+penalty
5

PublishedasaconferencepaperatICLR2026
|      |                   | (A) Prediction accuracy |     |                           |     | (B) Constraint satisfaction |     |     |                   |
| ---- | ----------------- | ----------------------- | --- | ------------------------- | --- | --------------------------- | --- | --- | ----------------- |
| 0.05 | Data-only         |                         |     | 50                        |     |                             |     |     | Data-only         |
|      | PINN (no penalty) |                         |     |                           |     |                             |     |     | PINN (no penalty) |
|      | PINN (+ penalty)  |                         |     |                           |     |                             |     |     | PINN (+ penalty)  |
| 0.04 |                   |                         |     | )%( snoitaloiv bmoluoC 40 |     |                             |     |     |                   |
)m( EAM
0.03
30
| 0.02 |           |                        |            | 20  |           |                        |           |     |            |
| ---- | --------- | ---------------------- | ---------- | --- | --------- | ---------------------- | --------- | --- | ---------- |
| 0.01 |           |                        |            | 10  |           |                        |           |     |            |
| 0.00 |           |                        |            | 0   |           |                        |           |     |            |
|      | Dense     | Sparse                 | Sparse     |     | Dense     |                        | Sparse    |     | Sparse     |
|      | Low-noise | Low-noise              | High-noise |     | Low-noise |                        | Low-noise |     | High-noise |
|      |           | Experimental condition |            |     |           | Experimental condition |           |     |            |
Figure1:Ablationresultsacrossdataregimes. (A)DisplacementMAEshowingphysicsconstraints
reduceerrorby30–40%,withlargergainsinsparseregimes. (B)Coulombviolationrateforsparse
conditions, showing a 58–68% reduction when adding inequality penalties to PINNs (20.3% →
| 8.6%,17.2% | → 5.5%). | (Interpolationsetting: |     | train/testont∈[0,5]s.) |     |     |     |     |     |
| ---------- | -------- | ---------------------- | --- | ---------------------- | --- | --- | --- | --- | --- |
reduces Coulomb violations by 58–68% (20.3% → 8.6%, 17.2% → 5.5%) at a modest 8–9%
accuracycost,confirmingthatexplicitinequalityenforcementisessentialunderlimitedsupervision
whileequalityconstraintssufficewhendataareabundant.
3.2 MATERIAL-AGNOSTICGENERALIZATIONANDZERO-SHOTPERFORMANCE
We evaluate whether physics-informed models learn material-agnostic dynamics rather than
material-specificmemorizationthroughzero-shottransfertoheld-outMaterials3,6, and9. These
receivenotrainingtrajectoriesandliewithintheinterpolationrangeofthetrainingparameterspace
(AppendixTable4);out-of-distributiongeneralizationremainsfuturework.
Table 2 reports per-material MAE for all three zero-shot materials; Figure 2 shows representative
predictionsforMaterial6.
|     | Table2: Zero-shotmaterialperformanceonheld-outmaterials(0%supervision). |        |             |         |     |           |     |     |        |
| --- | ----------------------------------------------------------------------- | ------ | ----------- | ------- | --- | --------- | --- | --- | ------ |
|     | Material                                                                | k(N/m) | Supervision | δMAE(m) |     | vMAE(m/s) |     | F   | MAE(N) |
n
0%
|     | Mat3          | 6000  |     | 0.0095 |     | 0.0285 |     |     | 14.2 |
| --- | ------------- | ----- | --- | ------ | --- | ------ | --- | --- | ---- |
|     | Mat6          | 2000  | 0%  | 0.0118 |     | 0.0312 |     |     | 16.8 |
|     | Mat9          | 12000 | 0%  | 0.0109 |     | 0.0298 |     |     | 15.1 |
|     | Zero-shotavg. | –     | 0%  | 0.0107 |     | 0.0298 |     |     | 15.4 |
|     | Regularavg.   | –     | 70% | 0.0112 |     | 0.0304 |     |     | 15.9 |
Zero-shotmaterialsreceivenotrainingtrajectories,versus117forregularmaterials.Predictionsremaindy-
namicallystable,withδin[0.048,0.350]mandvin[0.184,1.076]m/s.
Critical insight: Material generalization is not equivalent to temporal generalization. Even in
settings where temporal extrapolation accuracy degrades by ≈ 6–10%, zero-shot material transfer
improves by ≈ 14–29% (Table 3). Physics residuals enforce cross-sectional consistency across
material parameters (k, c , µ) within the observed temporal domain but do not impose inductive
n
structuresufficientforextrapolationintime.
| 3.3 | TEMPORALEXTRAPOLATION: |     | ANEGATIVERESULT |     |     |     |     |     |     |
| --- | ---------------------- | --- | --------------- | --- | --- | --- | --- | --- | --- |
Physicsconstraintsdonotimprovetemporalextrapolationbeyondthetraininghorizonandinsome
casesdegradeit. Weincludethisasadeliberatestresstesttoquantifythemagnitudeofthisknown
failuremoderelativetosparsityandnoise. Usingthesameforcingdistributionthroughoutisolates
horizon effects from forcing mismatch; Table 3 shows ≈ 6–10% degradation for PINN models
relativetodata-onlybaselines.
6

PublishedasaconferencepaperatICLR2026
(a)Displacementδ (b)Velocityv
(c)NormalforceF (d)TangentialforceF
n t
(e)Bristlestatez
Figure2:Zero-shotpredictionsforMaterial6(k =2000N/m,c =55Ns/m),completelywithheld
n
fromtraining.Solidblack:groundtruthODE;dashedblue:PINNprediction;reddots:testsamples.
Additionaldiagnostics: RMSresidualsincreasebyapproximately4–5×duringextrapolationfor
bothdata-onlyandPINNmodels,andbothexhibitcomparabletemporaldrift,indicatingfailureto
capturelong-horizondynamics. Zero-shotmaterialtransferneverthelessimprovesby≈ 18%even
underextrapolation.
Interpretation: Physicsresidualsconstrainlocalconsistency(e.g.,dδ/dt=vandforcebalance)
butdonotencodeglobaltemporalstructurebeyondobservedhorizons.Thiscautionsagainsttreating
PINNsasgeneral-purposetemporalextrapolatorswithoutexplicitlong-horizoninductivebias.
7

PublishedasaconferencepaperatICLR2026
| Table3: Generalizationperformance: |                 | materialtransfervs.temporalextrapolation. |                     |
| ---------------------------------- | --------------- | ----------------------------------------- | ------------------- |
| Regime                             | Method          | Zero-ShotδMAE                             | TemporalExtrap.δMAE |
|                                    |                 | (m)                                       | (m)                 |
| Dense,lownoise                     | Data-only       | 0.0588                                    | 0.0785              |
|                                    | PINN(+penalty)  | 0.0419(−29%)                              | 0.0861(+9.7%)       |
| Sparse,lownoise                    | Data-only       | 0.0747                                    | 0.0718              |
|                                    | PINN(nopenalty) | 0.0628(−16%)                              | 0.0762(+6.1%)       |
|                                    | PINN(+penalty)  | 0.0642(−14%)                              | 0.0762(+6.1%)       |
| Sparse,highnoise                   | Data-only       | 0.0709                                    | 0.0664              |
|                                    | PINN(+penalty)  | 0.0617(−13%)                              | 0.0724(+9.0%)       |
| Extrap.avg.                        | Data-only       | 0.0598                                    | 0.0723              |
|                                    | PINN(+penalty)  | 0.0492(−18%)                              | 0.0784(+8.4%)       |
Lownoise:σ = 0.01;Highnoise:σ = 0.02.Zero-shot:Materials3,6,9(k ∈ {6000,2000,12000}N/m)
heldoutwith0%supervision.Temporalextrapolation:traint∈[0,3]s,testt∈[3,5]s.Percentagesrelative
todata-onlybaseline.Extrap.avg.computedoverallextrapolationconditions(traint ∈ [0,3]s),including
denseandsparseregimes;notanaverageofinterpolationrowsabove.
3.4 UNSUPERVISEDPARAMETERDISCOVERYVIAUDE
TheUDErecoveredpredominantlylineardissipationlawsg (v) ≈ c v, withdamping-coefficient
θ n
errors of 1.2–16.3% from dynamics residuals alone and no direct c supervision (Figure 3). Re-
n
covery error varies across materials (e.g., Mat 1: 16.3% vs. Mat 2: 1.2%), which we attribute to
differencesinexcitationstrength, identifiabilityofc fromR , andembeddingproximitytowell-
|     |     | n 2 |     |
| --- | --- | --- | --- |
supervised neighbors in (k,σ 0 ,µ,v s ) space. A more detailed identifiability analysis and forcing-
designstudyisleftforfuturework.Toassesslinearity,wefitg (v)posthocwithav+bv2+cv3via
θ
least-squaresregressionoverv ∈ [−0.3,0.3]m/sandconsistentlyfoundb,c ≈ 0acrossmaterials,
confirmingpredominantlylinearbehavior. Thisisadirectconsequenceofthefactorizedstructure
inEq.(12),whichconstrainsg (v,e)totheclassv·cˆ (e);recoveringgeneralnonlineardissipation
|     | θ   | n   |     |
| --- | --- | --- | --- |
wouldrequirealessconstrainedparameterizationofg θ . Notably,zero-shotMaterial3recoversc n
with≈5.5%error(AppendixTable6)usingonlydifferentialequationresiduals, withoutaccessto
force labels or damping parameters, indicating that the embedding encodes physically meaningful
structurebeyondthetrainingdistribution.
Figure3: Learneddissipationfunctionsg (v)versusgroundtruthforfiverepresentativematerials
θ
(Mat1–5). Dashedlinesshowlearnedfunctions;solidlinesshowtruelineardampingc v.
n
Interpretation: The two-stage procedure shows that physics residuals contain enough signal to
recover latent dissipation parameters from consistency constraints alone. Within the constrained
8

PublishedasaconferencepaperatICLR2026
hypothesisclassofEq.(12),therecovereddynamicsareconsistentwithlinearviscousdampingin
thereducedLuGremodel.
4 DISCUSSION AND CONCLUSION
4.1 WHENPHYSICSHELPS,ANDWHY
Physicsresidualsactasadatamultiplierundersparsesupervisionbyenforcinglocalconsistencyat
everycollocationpoint,butbecomeredundantoncedataalonedeterminesthesolution,explaining
thediminishingreturnsweobserveindenseregimes. Equalityandinequalityconstraintsplaycom-
plementary but distinct roles: ODE residuals penalize deviations from differential structure, while
Coulomb penalties enforce the admissible force cone, a condition the residuals do not imply and
cannotsubstitutefor. Thisdistinctionmattersinpractice,bundlingbothunder“physics-informed”
obscures when each is actually needed. Finally, material generalization succeeds because learned
embeddingsplacematerialdescriptorsonasharedphysicalmanifold,whiletemporalextrapolation
failsfortheoppositereason: residualsenforceonlyinstantaneousconsistencyandcarrynomecha-
nismtoextendstructurebeyondtheobservedhorizon.
4.2 LIMITATIONSANDFUTUREDIRECTIONS
Thisstudyintentionallyfocusesonsyntheticcontactdatawithfixedforcingdistributionstoenable
controlledablationsandclearcausalattribution. Severallimitationsfollowfromthisscope.
Modelsareevaluatedundermatchedforcingdistributionsandknowncontactstructure; robustness
to forcing shift, unmodeled hysteresis, sensor bias, and partial state observation is not addressed.
Validationonrealroboticcontactdata,suchastheMITPushdataset(Yuetal.,2016),isanimportant
next step. The binary dense/sparse split (819 vs. 34 samples) establishes a clear causal contrast
ratherthanacontinuoussample-efficiencycurve;intermediatethresholdsandformalapproximation
guarantees(Raissietal.,2019)areleftforfuturework.
Zero-shotmaterialsliewithintheinterpolationrangeofthetrainingparameterspace(AppendixTa-
ble4),andembeddingsareconstructedfromcompleteground-truthparametervectors(k,σ ,µ,v );
0 s
evaluatingout-of-distributionmaterialsandgeneralizationunderpartialornoisydescriptorswould
providemoredemandingtestsofpracticalmaterialgeneralization.
Physics residuals enforce only local-in-time consistency, providing no inductive bias for long-
horizonpredictionbeyondthetrainingwindow. Futureworkwillexplorehistory-dependentembed-
dings, learned time-scale separation, and hybrid simulator–network architectures to encode long-
termstructureexplicitly.Additionally,thecurrentUDEformulationrecoversdissipationparameters
onlywithintheclassoflinearviscousdamping(Eq.12);extendingtononlineardissipationlawsvia
lessconstrainedparameterizationsofg isanaturalnextstep.
θ
SoftquadraticpenaltiesreduceCoulombviolationssubstantiallybutcannotguaranteestrictpoint-
wise admissibility, which may be insufficient for hardware deployment. Barrier methods, con-
strained optimization layers, and variational inequality formulations are promising alternatives.
Several hard-constraint methods were excluded to maintain architectural comparability: Contact-
Nets(Pfrommeretal.,2021)usescomplementarity-basedrepresentations,OptNet(Amos&Kolter,
2017)embedsdifferentiablequadraticprogramsolvers,andphysics-embeddedarchitectures(Spo-
tornoetal.,2025)targetdifferential-algebraicequationsystemsratherthantheODE-basedcontact
dynamicsstudiedhere. Directbenchmarkingremainsanimportantfuturedirection.
4.3 CONCLUSION
This work disentangles the roles of differential equation residuals, inequality enforcement, and
learned latent dynamics in physics-informed contact modeling. The practical implication is a de-
cision framework: use equality residuals when data are scarce, add explicit inequality penalties
when physical admissibility is required, and do not rely on local residuals for temporal extrapola-
tion. ThesefindingspositionPINNsandUDEsnotasuniversalsolutionsbutasprecisetoolswhose
benefitsdependondataregime,constraintstructure,andgeneralizationobjective.
9

PublishedasaconferencepaperatICLR2026
REFERENCES
BrandonAmosandJZicoKolter. Optnet: Differentiableoptimizationasalayerinneuralnetworks.
InInternationalconferenceonmachinelearning,pp.136–145.PMLR,2017.
ShengzeCai,ZhipingMao,ZhichengWang,MinglangYin,andGeorgeEmKarniadakis. Physics-
informedneuralnetworksforheattransferproblems. JournalofHeatTransfer, 143(6):060801,
2021.
Ricky TQ Chen, Yulia Rubanova, Jesse Bettencourt, and David K Duvenaud. Neural ordinary
differentialequations. Advancesinneuralinformationprocessingsystems,31,2018.
Yuyao Chen, Lu Lu, George Em Karniadakis, and Luca Dal Negro. Physics-informed neural net-
works for inverse problems in nano-optics and metamaterials. Optics Express, 28(8):11618–
11633,2020.
KurtlandChua,RobertoCalandra,RowanMcAllister,andSergeyLevine.Deepreinforcementlearn-
ing in a handful of trials using probabilistic dynamics models. Advances in neural information
processingsystems,31,2018.
Per R Dahl. Solid friction damping of mechanical vibrations. AIAA journal, 14(12):1675–1682,
1976.
C Canudas De Wit, Henrik Olsson, Karl Johan Astrom, and Pablo Lischinsky. A new model for
controlofsystemswithfriction. IEEETransactionsonAutomaticControl,40(3):419–425,1995.
PierreDupont,VincentHayward,BrianArmstrong,andFriedhelmAltpeter. Singlestateelastoplas-
ticfrictionmodels. IEEETransactionsonAutomaticControl,47(5):787–792,2002.
Kenneth H Hunt and Frank RE Crossley. Coefficient of restitution interpreted as damping in vi-
broimpact. Journalofappliedmechanics,42(2):440–445,1975.
GeorgeEmKarniadakis,IoannisGKevrekidis,LuLu,ParisPerdikaris,SifanWang,andLiuYang.
Physics-informedmachinelearning. NatureReviewsPhysics,3(6):422–440,2021.
DongCLiuandJorgeNocedal. Onthelimitedmemorybfgsmethodforlargescaleoptimization.
Mathematicalprogramming,45(1):503–528,1989.
SungyongLiu,YueCao,De-AnHuang,YilunWang,WeiweiWang,JanKautz,andStanBirchfield.
Differentiablephysics-informedgraphnetworks. arXivpreprintarXiv:2202.02198,2022.
MichaelLutter,ChristianRitter,andJanPeters. Deeplagrangiannetworks: Usingphysicsasmodel
priorfordeeplearning. InternationalConferenceonLearningRepresentations(ICLR),2019.
Filipe Marques, Paulo Flores, J.C. Pimenta Claro, and Hamid M Lankarani. A survey and com-
parisonofseveralfrictionforcemodelsfordynamicanalysisofmultibodymechanicalsystems.
Nonlineardynamics,86:1407–1443,2016.
MatthewTMason. MechanicsofRoboticManipulation. MITPress,2001.
AnushaNagabandi,GregoryKahn,RonaldSFearing,andSergeyLevine.Neuralnetworkdynamics
formodel-baseddeepreinforcementlearningwithmodel-freefine-tuning. In2018IEEEInterna-
tionalConferenceonRoboticsandAutomation(ICRA),pp.7559–7566,2018.
SamuelPfrommer,MathewHalm,andMichaelPosa. Contactnets: Learningdiscontinuouscontact
dynamics with smooth, implicit representations. Conference on Robot Learning (CoRL), pp.
2279–2291,2021.
ChristopherRackauckas,YingboMa,JuliusMartensen,CollinWarner,KirillZubov,RohitSupekar,
DominicSkinner,AliRamadhan,andAlanEdelman. Universaldifferentialequationsforscien-
tificmachinelearning. arXivpreprintarXiv:2001.04385,2020.
MaziarRaissi, ParisPerdikaris, andGeorgeEKarniadakis. Physics-informedneuralnetworks: A
deep learning framework for solving forward and inverse problems involving nonlinear partial
differentialequations. JournalofComputationalPhysics,378:686–707,2019.
10

PublishedasaconferencepaperatICLR2026
Prajit Ramachandran, Barret Zoph, and Quoc V Le. Searching for activation functions. arXiv
preprintarXiv:1710.05941,2017.
Enzo Nicola´s Spotorno, Antoˆnio Augusto Fro¨hlich, et al. Hard-constrained neural networks with
physics-embeddedarchitectureforresidualdynamicslearningandinvariantenforcementincyber-
physicalsystems. arXivpreprintarXiv:2511.23307,2025.
MatthewTancik,PratulSrinivasan,BenMildenhall,SaraFridovich-Keil,NithinRaghavan,Utkarsh
Singhal, Ravi Ramamoorthi, Jonathan Barron, and Ren Ng. Fourier features let networks learn
highfrequencyfunctionsinlowdimensionaldomains.Advancesinneuralinformationprocessing
systems,33:7537–7547,2020.
ChTsitouras. Runge–kuttapairsoforder5(4)satisfyingonlythefirstcolumnsimplifyingassump-
tion. Computers&MathematicswithApplications,62(2):770–775,2011.
MariaBauzaVillalonga,AlbertoRodriguez,BryanLim,EricValls,andTheoSechopoulos. Tactile
object pose estimation from the first touch with geometric contact rendering. In Conference on
RobotLearning,pp.1015–1029.PMLR,2021.
SifanWang,YujunTeng,andParisPerdikaris. Understandingandmitigatinggradientflowpatholo-
giesinphysics-informedneuralnetworks. SIAMJournalonScientificComputing,43(5):A3055–
A3081,2021.
JaredWillard,XiaoweiJia,ShaomingXu,MichaelSteinbach,andVipinKumar. Integratingscien-
tific knowledge with machine learning for engineering and environmental systems. ACM Com-
putingSurveys,55(4):1–37,2022.
Kailai Xu, Alexandre M Tartakovsky, Jeff Burghardt, and Eric Darve. Learning viscoelasticity
modelsfromindirectdatausingdeepneuralnetworks. ComputerMethodsinAppliedMechanics
andEngineering,387:114124,2021.
Kuan-TingYu,MariaBauza,NimaFazeli,andAlbertoRodriguez. Morethanamillionwaystobe
pushed.ahigh-fidelityexperimentaldatasetofplanarpushing. In2016IEEE/RSJinternational
conferenceonintelligentrobotsandsystems(IROS),pp.30–37.IEEE,2016.
11

PublishedasaconferencepaperatICLR2026
A APPENDIX
Noteonreportedimprovements: Percentimprovementsinthemaintextarecomputedrelativeto
thedata-onlybaselinewithinthesameregime,usingthecorrespondingrow-pairsinTables1and3.
A.1 MATERIALPARAMETERSPACE
Table4: Alltenmaterialsusedinexperiments. Materials3,6,and9areheldoutforzero-shoteval-
uation(0%trainingsupervision). Materialsareorderedasdefinedinthedatagenerationprocedure.
| Material | k(N/m) | c (Ns/m) | σ (N/m) | µ v (m/s)   | Split      |
| -------- | ------ | -------- | ------- | ----------- | ---------- |
|          |        | n        | 0       | s           |            |
| Mat1     | 1000   | 40       | 80      | 0.30 0.0150 | Train(70%) |
| Mat2     | 3000   | 70       | 200     | 0.40 0.0100 | Train(70%) |
| Mat3     | 6000   | 110      | 350     | 0.50 0.0070 | Zero-shot  |
| Mat4     | 10000  | 150      | 500     | 0.60 0.0040 | Train(70%) |
| Mat5     | 15000  | 200      | 700     | 0.80 0.0020 | Train(70%) |
| Mat6     | 2000   | 55       | 140     | 0.35 0.0125 | Zero-shot  |
| Mat7     | 4500   | 90       | 275     | 0.45 0.0085 | Train(70%) |
| Mat8     | 8000   | 130      | 425     | 0.55 0.0055 | Train(70%) |
| Mat9     | 12000  | 175      | 600     | 0.70 0.0030 | Zero-shot  |
| Mat10    | 5000   | 100      | 300     | 0.48 0.0080 | Train(70%) |
Parametersspan:k ∈ [1000,15000]N/m,c ∈ [40,200]Ns/m,σ ∈ [80,700]N/m,µ ∈ [0.30,0.80],
|     |     |     | n   | 0   |     |
| --- | --- | --- | --- | --- | --- |
v ∈[0.002,0.015]m/s.
s
Zero-shotmaterialsarepositionedatinterpolationpointswithinthetrainingdistribution:Mat3
(k=6000)betweenMat2(k=3000)andMat4(k=10000);Mat6(k=2000)betweenMat1(k=1000)
andMat2(k=3000);Mat9(k=12000)betweenMat4(k=10000)andMat5(k=15000).
A.2 HYPERPARAMETERSANDARCHITECTUREDETAILS
12

PublishedasaconferencepaperatICLR2026
Table5: Completehyperparametersettings.
| Component | Parameter |     |     |     |     | Value |     |
| --------- | --------- | --- | --- | --- | --- | ----- | --- |
Statepredictionnetwork
|     | Hiddenlayers      |     |     |     |                       | 5     |     |
| --- | ----------------- | --- | --- | --- | --------------------- | ----- | --- |
|     | Hiddenunits       |     |     |     | 256–256–96–64–32      |       |     |
|     | Hiddenactivations |     |     |     |                       | swish |     |
|     | Outputactivation  |     |     |     |                       | tanh  |     |
|     | Timeencoding      |     |     |     | 11-dimFourierfeatures |       |     |
[t,sin(πt),cos(πt),...,sin(8πt),cos(8πt)]
Materialembeddingnetwork
|     | Inputdim          |     |     |                            | 4(k,σ | 0 ,µ,v s | )   |
| --- | ----------------- | --- | --- | -------------------------- | ----- | -------- | --- |
|     | Architecture      |     |     | 64–64–32(swish–swish–tanh) |       |          |     |
|     | Outputdim         |     |     |                            |       | 32       |     |
|     | Contrastivemargin |     |     |                            |       | 2.0      |     |
Scalingnetwork
|     | Architecture |     |     | 32–16–2(swish–swish–softplus) |     |      |     |
| --- | ------------ | --- | --- | ----------------------------- | --- | ---- | --- |
|     | Outputs      |     |     |                               | (δ  | ,v ) |     |
scale scale
Dissipationnetwork(UDE)
|     | Architecture   |     |     | 32–16–1(swish–swish–linear) |     |               |     |
| --- | -------------- | --- | --- | --------------------------- | --- | ------------- | --- |
|     | Scaleparameter |     |     | Learnablelogs               |     | ,initlog(100) |     |
0
|     | Outputstructure |     |     | g(v,e)=v·s·softplus(h |     |     | θ (e)) |
| --- | --------------- | --- | --- | --------------------- | --- | --- | ------ |
Stage1: Pretraining(dataonly)
|     | Epochs    |     |     | 500(earlystopping,patience=3×50) |     |        |         |
| --- | --------- | --- | --- | -------------------------------- | --- | ------ | ------- |
|     | Optimizer |     |     | AdamW(β                          |     | =0.9,β | =0.999) |
|     |           |     |     |                                  |     | 1 2    |         |
10−4
Learningrate
|     | Weightdecay      |     |     |                            |     | 10−4 |     |
| --- | ---------------- | --- | --- | -------------------------- | --- | ---- | --- |
|     | Gradientclipping |     |     | Element-wise,threshold=0.3 |     |      |     |
Stage2: Physicstraining
|     | Epochs               |            |     |                            |        | 800        |         |
| --- | -------------------- | ---------- | --- | -------------------------- | ------ | ---------- | ------- |
|     | Optimizer            |            |     | AdamW(β                    |        | 1 =0.9,β 2 | =0.999) |
|     | Learningrate         |            |     |                            | 5×10−5 |            |         |
|     | Weightdecay          |            |     |                            | 5×10−5 |            |         |
|     | Gradientclipping     |            |     | Element-wise,threshold=0.3 |        |            |         |
|     | Coulombpenalty(λ     | friction ) |     |                            |        | 1.5        |         |
|     | Normalforcepenalty(λ |            | )   |                            |        | 0.02       |         |
neg
|     | Overallconstraintweight(λ |     | )   |     |     | 0.5 |     |
| --- | ------------------------- | --- | --- | --- | --- | --- | --- |
ineq
Stage3: L-BFGSrefinement
|     | Iterations        |     |     |     |     | 300  |     |
| --- | ----------------- | --- | --- | --- | --- | ---- | --- |
|     | Convergencetol.(g | )   |     |     |     | 10−6 |     |
tol
UDEStage2(dissipationonly)
|     | Epochs |     |     |     |     | 400 |     |
| --- | ------ | --- | --- | --- | --- | --- | --- |
AdamW(lr=10−4,wd=10−5)
Optimizer
|     | Gradientclipping |     |     | Element-wise,threshold=1.0          |     |     |     |
| --- | ---------------- | --- | --- | ----------------------------------- | --- | --- | --- |
|     | Frozencomponents |     |     | Statepredictor,embedding,scalingnet |     |     |     |
Adaptiveresidualscaling
|     | Momentum(β)      |     |     |                       |             | 0.95    |         |
| --- | ---------------- | --- | --- | --------------------- | ----------- | ------- | ------- |
|     | R 2 weightclamp  |     |     |                       | [0.15,0.40] |         |         |
|     | Convergedweights |     |     | λ ≈1.0,λ              |             | ≈0.25,λ | ≈0.35   |
|     |                  |     |     | R1                    | R2          |         | R3      |
|     |                  |     |     | r¯(t) =βr¯(t−1)+(1−β) |             |         | RMS(Ri) |
Updaterule
|     |             |     |     | i   | i          |     | RMS(R1)+ϵ |
| --- | ----------- | --- | --- | --- | ---------- | --- | --------- |
|     | Weightclamp |     |     |     | [0.1,10.0] |     |           |
Finitedifferenceresiduals
|     | Stepsize(∆t) |     |     |                                  |     | 0.01s |     |
| --- | ------------ | --- | --- | -------------------------------- | --- | ----- | --- |
|     | Method       |     |     | Centraldifferences(second-order) |     |       |     |
dyˆ(cid:12)
|     | Formula |     |     |     | ≈ yˆ(t+∆t)−yˆ(t−∆t) |     |     |
| --- | ------- | --- | --- | --- | ------------------- | --- | --- |
(cid:12)
|     |     |     |     |     | dt t | 2∆t |     |
| --- | --- | --- | --- | --- | ---- | --- | --- |
13

PublishedasaconferencepaperatICLR2026
A.3 ADDITIONALZERO-SHOTPREDICTIONPLOTS
Figure4andFigure5showpredictionsfortheremainingtwozero-shotmaterials(Mat3andMat9),
complementingtheMat6resultsinFigure2ofthemaintext.
Figure 4: Zero-shot predictions for Material 3 (k = 6000 N/m, c = 110 Ns/m, 0% training
n
supervision). Solidlines: groundtruthODE;dashedline: PINNprediction.
14

PublishedasaconferencepaperatICLR2026
Figure 5: Zero-shot predictions for Material 9 (k = 12000 N/m, c = 175 Ns/m, 0% training
n
| supervision). | Solidlines: groundtruthODE;dashedline: |     |     | PINNprediction. |     |
| ------------- | -------------------------------------- | --- | --- | --------------- | --- |
Table 6: UDE parameter recovery. The dissipation network g is trained via Stage 2 residuals.
θ
Analysis is reported for Materials 1–5; the remaining regular materials (7, 8, 10) follow the same
trainingprotocolbutareomittedforbrevity. Mat3(c =110)receives0%trainingsupervision;its
n
recoveryiszero-shot,demonstratingthatthephysics-structuredembeddingenablesc interpolation
n
withoutdirecttrajectorydata.
|     | Material | Truec  | Learnedc | Rel.Error | Supervision |
| --- | -------- | ------ | -------- | --------- | ----------- |
|     |          | n      |          | n         |             |
|     |          | (Ns/m) | (Ns/m)   | (%)       |             |
Trainedmaterials(70%supervision)
|     | Mat1 | 40.0  | 46.5  | 16.3 | 70% |
| --- | ---- | ----- | ----- | ---- | --- |
|     | Mat2 | 70.0  | 69.1  | 1.2  | 70% |
|     | Mat4 | 150.0 | 142.9 | 4.7  | 70% |
|     | Mat5 | 200.0 | 173.7 | 13.1 | 70% |
Zero-shotmaterial(0%supervision)†
|     | Mat3 | 110.0 | 104.0 | 5.5 | 0%  |
| --- | ---- | ----- | ----- | --- | --- |
†Mat3receivesnotrainingtrajectoriesinStage2.Itsc n isrecoveredsolelyviathephysics-structured
materialembedding,whichinterpolatescontinuouslyacross(k,σ 0 ,µ,v s )spaceusingtheseventrained
materials.Recoveryat5.5%errordemonstrateszero-shotparameterdiscoverythroughembeddinginter-
polation.
Recoveryquality(computedoverMat1–5,includingzero-shotMat3):CV(g θ ) = 0.49 ≫ 0.15,
cor(g θ ,c n v) = 0.997 ≫ 0.85,regressionRMSE≈ 0.0.Learnedc n extractedvialinearregressionon
g θ (v)vs.voverv∈[−0.3,0.3]m/s.
15

PublishedasaconferencepaperatICLR2026
,selbairavecrofdnaetatsrofEAMtes-tseterascirtemdetropeR
dnadelacsnusilaudiserSMR.slennahcetatsllaotdeilppaσleveltanaissuaGevitiddamrofinu:esioN.)5.2noitceSees(delpmasbus:esrapS;selpmasgniniart918=N:esneD
)%(.loiVbmoluoC
|     | 5.51 0.61 0.61 | 5.51 0.61 6.15 3.02 | 3.83 2.71 |
| --- | -------------- | ------------------- | --------- |
6.8 5.5
.seRSMR
|     | 863.0 971.0 912.0 | 033.0 971.0 410.1 666.0 547.0 | 469.0 578.0 537.0 .%1nihtiw)ytlanepon(NNIPdehctamecnamrofrepsadettimo)ytlanep+(NNIPesion-hgihesneD. |
| --- | ----------------- | ----------------------------- | --------------------------------------------------------------------------------------------------- |
.snoitaloivnoitcirfbmoluoCfoegatnecrepdna,) )N(EAM
|     | 997.0 833.0 884.0 | 497.0 972.0 892.1 469.0 961.1 | 063.1 202.1 582.1 |
| --- | ----------------- | ----------------------------- | ----------------- |
t
.tnemecrofnetniartsnocdna,slevelesion,semigeratadssorcastlusernoitalbaetelpmoC F
)N(EAM
|     | 38.73 97.71 98.42 | 77.43 85.61 19.891 17.311 56.321 | 63.481 92.941 95.711 |
| --- | ----------------- | -------------------------------- | -------------------- |
n
F
)s/m(EAMv
|     | 1201.0 5360.0 3180.0 | 9090.0 7750.0 9201.0 5690.0 8001.0 | 7301.0 2401.0 6201.0 |
| --- | -------------------- | ---------------------------------- | -------------------- |
)m(EAMδ
| 3         | )20.0=               |                                    |                      |
| --------- | -------------------- | ---------------------------------- | -------------------- |
| R, )10.0= | 6810.0 7110.0 8210.0 | 8220.0 4710.0 4050.0 7330.0 5630.0 | 0940.0 4640.0 5730.0 |
2
R,
1
| Rrevodetagergga(laudiserscisyhpSMRdelacsnu | σ(esioNhgiH,)918= |     |     |
| ------------------------------------------ | ----------------- | --- | --- |
σ(esioNwoL,)918=
|     |                 | )10.0=                          | )20.0=             |
| --- | --------------- | ------------------------------- | ------------------ |
|     | )ytlanepon(NNIP | )ytlanepon(NNIP )ytlanepon(NNIP | )ytlanepon(NNIP    |
|     | )ytlanep+(NNIP  | )ytlanep+(NNIP                  | )ytlanep+(NNIP     |
|     |                 | σ(esioNwoL,esrapS               | σ(esioNhgiH,esrapS |
|     | ylno-ataD       | ylno-ataD ylno-ataD             | ylno-ataD          |
dohteM
Rdna, 3
| N(esneD | N(esneD |     |     |
| ------- | ------- | --- | --- |
emigeR
2
R,
1
Rrevodetagergga
:7elbaT
16