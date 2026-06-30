ProceedingsofMachineLearningResearchvol120:1–10,2020 2ndAnnualConferenceonLearningforDynamicsandControl
Encoding Physical Constraints in
Differentiable Newton-Euler Algorithm
GiovanniSutanto* GSUTANTO@USC.EDU
DepartmentofComputerScience,UniversityofSouthernCalifornia
AustinS.Wang WANGAUSTIN@FB.COM
YixinLin YIXINLIN@FB.COM
MustafaMukadam MUKADAM@FB.COM
FacebookArtificialIntelligenceResearch
GauravS.Sukhatme GAURAV@USC.EDU
DepartmentofComputerScience,UniversityofSouthernCalifornia
AksharaRai AKSHARARAI@FB.COM
FranziskaMeier FMEIER@FB.COM
FacebookArtificialIntelligenceResearch
Editors:A.Bayen,A.Jadbabaie,G.J.Pappas,P.Parrilo,B.Recht,C.Tomlin,M.Zeilinger
Abstract
TherecursiveNewton-EulerAlgorithm(RNEA)isapopulartechniqueforcomputingthedynam-
icsofrobots. RNEAcanbeframedasadifferentiablecomputationalgraph,enablingthedynamics
parameters of the robot to be learned from data via modern auto-differentiation toolboxes. How-
ever,thedynamicsparameterslearnedinthismannercanbephysicallyimplausible. Inthiswork,
weincorporatephysicalconstraintsinthelearningbyaddingstructuretothelearnedparameters.
Thisresultsinaframeworkthatcanlearnphysicallyplausibledynamicsviagradientdescent,im-
provingthetrainingspeedaswellasgeneralizationofthelearneddynamicsmodels. Weevaluate
ourmethodonreal-timeinversedynamicscontroltasksona7degreeoffreedomrobotarm,both
insimulationandontherealrobot. Ourexperimentsstudyaspectrumofstructureaddedtothepa-
rametersofthedifferentiableRNEAalgorithm,andcomparetheirperformanceandgeneralization.
Thecodeisavailableathttps://github.com/facebookresearch/differentiable-robot-model.
Keywords: learning, structure, rigid body parameters, differentiable, recursive Newton-Euler al-
gorithm,inversedynamics
1. Introduction
Anaccuratedynamicsmodeliskeytocompliantforcecontrolofrobots,andthereisarichhistory
oflearningofsuchmodelsforrobotics(Anetal.,1988;Murrayetal.,1994;Atkesonetal.,1986).
With an accurate dynamics model, inverse dynamics can be used as a policy to predict the torques
requiredtoachieveadesiredjointacceleration,giventhestateoftherobot(Murrayetal.,1994).
Due to their widespread utility, robot dynamics have been learned in many ways. One way is
to use a purely data-driven approach with parametric models (Hitzler et al., 2019), non-parametric
models (Nguyen-Tuong et al., 2008), and learning error-models (Kappler et al., 2017), in a su-
pervised or self-supervised fashion. However, these purely data-driven approaches typically suffer
*ThisworkwasdonewhenGiovanniSutantowasaninternatFacebookArtificialIntelligenceResearch.
©2020G.Sutanto,A.S.Wang,Y.Lin,M.Mukadam,G.S.Sukhatme,A.Rai&F.Meier.
0202
tcO
8
]OR.sc[
4v16880.1002:viXra

ENCODINGPHYSICALCONSTRAINTSINDIFFERENTIABLENEWTON-EULERALGORITHM
fromalackofgeneralizationtopreviouslyunexploredpartsofthestatespace. Alternatively,Atke-
son et al. (1986) recast the dynamics equations such that inertial parameters are a linear function
of state-dependent quantities, given the joint torques. While inferior to unstructured approaches in
terms of flexibility to fit data, this approach typically provides superior generalization capabilities.
Recently, Lutter et al. (2019); Gupta et al. (2019) learn the parameters of Lagrangian dynamics,
incorporating benefits of flexible function approximation into structured models. However, these
approaches ignore some of the physical relationships and constraints on the learned parameters,
whichcanleadtophysicallyimplausibledynamics.
In this work, we combine the modern approach of parameter learning with the structured ap-
proachtoinversedynamicslearning, similartoLedezmaandHaddadin(2017). Weimplementthe
Recursive Newton-Euler algorithm in PyTorch (Paszke et al., 2017), allowing the inertial param-
eters to be learned using gradient descent and automatic-differentiation for gradient computation.
The benefit, over traditional least-squares implementations, is that we can easily explore various
re-parameterizationsoftheinertialparametersandadditionalconstraintsthatencodephysicalcon-
sistency,suchasWensingetal.(2018),withouttheneedforlinearity.
Inthatcontext,thecontributionofthispaperisthreefold: first,wepresentseveralre-parameteri-
zations of the inertial parameters, which allow us to learn physically plausible parameters using a
differentiable recursive Newton-Euler algorithm. Second, we show that these re-parameterizations
help in improving training speed as well as generalization capability of the model to unseen situ-
ations. Third, we evaluate a spectrum of structured dynamics learning approaches on a simulated
andreal7degree-of-freedomrobotmanipulator.
Our results show that adding such structure to the learning can improve the learning speed as
wellasgeneralizationabilitiesofthedynamicsmodel. Ourmodelscangeneralizewithmuchlesser
data,andneedmuchfewertrainingepochstoconverge. Withourlearneddynamics,weseereduced
contributionsoffeedbacktermsincontrol,resultinginmorecompliantmotions.
2. BackgroundandRelatedWork
The dynamics of a robot manipulator are a function of the joint torque τ, joint acceleration q¨ and
jointpositionandvelocityq,q˙:
τ = f (q,q˙,q¨) = H(q)q¨ +C(q,q˙)q˙ +g(q) (1)
ID
withH(q),C(q,q˙),g(q)arethesysteminertiamatrix,Coriolismatrix,andgravityforce,respec-
tively. f (q,q˙,q¨)istheinversedynamicsmodelthatreturnsthetorquesthatcanachieveadesired
ID
jointacceleration,giventhecurrentjointpositionsandvelocities.
The Recursive Newton-Euler Algorithm (RNEA) (Luh et al., 1980; Featherstone, 2007) is a
computationally efficient method of computing the inverse dynamics, which scales linearly with
respecttothenumberofthedegrees-of-freedomoftherobot.
2.1. Learningmodelsformodel-basedcontrol
Accurate inverse dynamics models are crucial for compliant force controlled robots, and hence
widely studied in robotics. Previously, researchers have used unstructured multi-layer perceptron
(MLP) to learn the complete inverse dynamics (Jansen, 1994; Hitzler et al., 2019) or a residual
component of the inverse dynamics (Kappler et al., 2017). Nguyen-Tuong et al. (2008) compare
2

ENCODINGPHYSICALCONSTRAINTSINDIFFERENTIABLENEWTON-EULERALGORITHM
non-parametricmethodslikelocallyweightedprojectionregression(LWPR),supportvectorregres-
sion(SVR)andGaussianprocessesregression(GPR)forlearninginversedynamicsmodels.
Recently Lutter et al. (2019) and concurrently Gupta et al. (2019, 2020), proposed a semi-
structuredlearningmethodfortheLagrangiandynamicsofamanipulator,calledDeepLagrangian
Networks(DeLaN).InDeLaN,someofthephysicalconstraintsofLagrangiandynamicsareobeyed.
Forexample,theinertiamatrixisparametrizedtobesymmetricpositivedefinite. Moreover,there-
lationshipbetweencoriolisandcentrifugaltermsandtheinertiamatrixandjointvelocities(Murray
et al., 1994) is satisfied via automatic differentiation. Similarly, the gravity term is derived from
a neural network which takes generalized coordinates as input, representing the potential energy.
However,otherconstraintsinthedynamics,suchasthetriangleinequalityintheprincipalmoments
(Traversaro et al., 2016) of the inertia matrix are not considered. Moreover, neural networks can
be sensitive to the chosen architecture and need variations in input data to generalize to new situa-
tions. SimilartoDeLaN,HamiltonianNeuralNetworks(HNN)(Greydanusetal.,2019)predictthe
Hamiltonian(insteadofLagrangian)ofadynamicalsystem.
Many previous works in parameter identification boil down to setting up a least square prob-
lem with some (hard) constraints (Wensing et al., 2018; Mistry et al., 2009; Kozlowski, 2012),
followed by solving a convex optimization problem. On the other hand, our method incorporates
hardconstraintsasstructureinlearningrepresentationsoftheparameters,andthenperformsback-
propagation on the computational graph for optimization. As a result, it is not limited to learning
linear parameters, and can generalize to a larger range of problems. Moreover, our approach can
be applied to an online learning setup: for example when the robot carries an additional mass
(an object) on one of its links, our approach can adapt the dynamics parameters online, as the
robot continues to operate and the data is collected in batches. Traditionally, online learning ap-
proaches–includingadaptivecontrol(SlotineandLi,1987)–donotguaranteephysicalplausibility
of the learned dynamics parameters. On the other hand, more modern system identification meth-
odswhichincorporatehardconstraintsonphysicalparameters(Wensingetal.,2018;Mistryetal.,
2009; Kozlowski, 2012) require collecting data in the new setting before optimizing the new dy-
namicsparameters.
Our work is closely related to the work by Ledezma and Haddadin (2017), in the sense that
ourworkisalsoderivedfromtheNewton-Eulerformulationofinversedynamics. However,inour
work, we emphasize more on how incorporating structure in learning dynamics parameters helps
with improving the training speed and generalization capability of the model. Moreover, we also
compareourmethodwiththestate-of-the-artsemi-structuredDeLaNandanunstructuredMLP.
3. EncodingPhysicalConsistencyinNewton-EulerEquations
TheNewton-Eulerequationscanbeimplementedasadifferentiablecomputationalgraph,e.g. with
PyTorch (Paszke et al., 2017), which we call differentiable NEA (DiffNEA). The parameters of
DiffNEA, e.g. the inertial parameters θ, can now be optimized via gradient descent utilizing auto-
maticdifferentiationtocomputethegradients. Althoughbothkinematicsanddynamicsparameters
areinvolvedinNewton-Euleralgorithm,inthispaperwestudytheoptimizationofonlythedynam-
icsparameters,assumingthekinematicsspecificationoftherobotiscorrectandfixed.
3

ENCODINGPHYSICALCONSTRAINTSINDIFFERENTIABLENEWTON-EULERALGORITHM
Specifically, we aim to optimize parameters θ of the Newton-Euler equations, such that the
inversedynamicslossisminimized
T
|     |     |     |     | (cid:88)   |      |        | ;θ)(cid:107)2. |     |     |     |     |
| --- | --- | --- | --- | ---------- | ---- | ------ | -------------- | --- | --- | --- | --- |
|     |     | L   | =   | (cid:107)τ | −f   | (q ,q˙ | ,q¨            |     |     |     | (2) |
|     |     |     | ID  |            | t NE | t      | t t            | 2   |     |     |     |
t=1
Typically, θ is a collection of inertial parameters θ = [m,θ ,I ,I ,I ,I ,I ,I ]T ∈ R10
|     |     |     |     |     |     | i   | h   | xx xy | xz  | yy yz zz |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | -------- | --- |
per link, where m is the link mass, θ = [h ,h ,h ] = mc with c being the CoM, and the last 6
|     |     |     |     | h   | x y | z   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
parametersrepresentingtherotationalinertiamatrixI C (Atkesonetal.,1986). Whenoptimizingθ
physicalconsistencyoftheestimatedparametersisnotguaranteed. Enforcingphysicalconstraints
ontheparameterscanbedonethroughexplicitconstraints(Traversaroetal.,2016;Wensingetal.,
2018), which requires constrained optimization algorithms to find a solution. In the following, we
discussandproposeseveralpossibleparameterrepresentationsθ,whichencodeincreasinglymore
physicalconsistencyimplicitlyandallowsustoperformunconstrainedgradientdescent.
3.1. UnstructuredMassandRotationalInertiaMatrix(DiffNEANoStr)
We start out with the simplest representation, with an unconstrained mass value θ m and 9 uncon-
strained parametersfortherotationalinertiamatrix:
|       | (cid:2) |     |     |     |     |     |         |     |     | (cid:3) |     |
| ----- | ------- | --- | --- | --- | --- | --- | ------- | --- | --- | ------- | --- |
| θ     | =       | θ θ | θ   | θ   | θ   | θ θ | θ       | θ   | θ   | θ       | (3) |
| NoStr |         | m h | IC1 | IC2 | IC3 | IC4 | IC5 IC6 | IC7 | IC8 | IC9     |     |
Thisparametrizationdoesnotencodeanyphysicalconstraintsandonlyservesasbaseline.
3.2. SymmetricRotationalInertiaMatrix(DiffNEASymm)
In this parametrization, we explicitly construct the rotational matrix as a symmetric matrix, with
only6learnableparameters. Furthermore,werepresentthelinkmassas: m = (θ√ )2 +b,where
m
b > 0isa(non-learnable)smallpositiveconstanttoensurem > 0. Thusthelearnableparameters
ofthisrepresentationare
|     |      | (cid:2) |     |     |     |     |     |     |     | (cid:3) |     |
| --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | ------- | --- |
|     | θ    | = θ√    | θ   | θ   | θ   | θ   | θ   | θ   | θ   |         | (4) |
|     | Symm |         | m h | IC1 | IC2 | IC3 | IC4 | IC5 | IC6 |         |     |
Thisparameterrepresentationenforcespositivemassestimatesandsymmetric–butnotnecessarily
positivedefinite–rotationalinertiamatrices.
3.3. SymmetricPositiveDefiniteRotationalInertiaMatrix(DiffNEASPD)
Next, we introduce a change of variables, to enforce positive definiteness of the rotational inertia
matrix. Weconstructthelowertriangularmatrix:
|     |     |     |     |    | θ   | 0   | 0  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
LI1
|     |     |     |     | L = θ |     | θ   | 0   |     |     |     | (5) |
| --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |        | LI4 | LI2 |    |     |     |     |     |
|     |     |     |     |        | θ   | θ θ |     |     |     |     |     |
|     |     |     |     |        | LI5 | LI6 | LI3 |     |     |     |     |
andconstructtherotationalinertiamatrixI viaCholeskydecompositionplusasmallpositivebias
C
LLT+bI
onthediagonal: I = . I isa3×3identitymatrixandb > 0isa(non-learnable)
|     | C   |     | 3×3 | 3×3 |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
smallpositiveconstanttoensurepositivedefinitenessofI . Thelearnableparametersare:
C
|     |     | (cid:2) |     |     |         |     |     |     | (cid:3) |     |     |
| --- | --- | ------- | --- | --- | ------- | --- | --- | --- | ------- | --- | --- |
|     | θ   | = θ√    |     | θ θ | θ       | θ   | θ   | θ   | θ       |     | (6) |
|     | SPD |         | m   | h   | LI1 LI2 | LI3 | LI4 | LI5 | LI6     |     |     |
4

ENCODINGPHYSICALCONSTRAINTSINDIFFERENTIABLENEWTON-EULERALGORITHM
Whilethisrepresentationenforcespositivemassandpositivedefiniteinertiamatrices,itcouldstill
lead to inertia estimates that are not physically plausible, as discussed in Traversaro et al. (2016).
Toachievefullconsistency,theestimatedinertiamatrixalsoneedstofulfillthetriangularinequality
oftheprincipalmomentsofinertiaofthe3Dinertiamatrices(Traversaroetal.,2016).
3.4. TriangularParameterizedRotationalInertiaMatrix(DiffNEATri)
Toencodethetriangularinequalityconstraints,wefirstdecomposetherotationalinertiamatrixas:
|     |     |     |     |     | I = RJRT |     |     |     |     |     | (7) |
| --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
C
whereR ∈ SO(3)isarotationmatrix,andJ isadiagonalmatrixcontainingtheprincipalmoments
| J ,J | ,J  |     |     |     |     |     |     | (J  | > 0, | J > 0, | J > 0) |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ------ | ------ |
of inertia 1 2 3 . The principal moments of inertia are all positive 1 2 3
suchthatI ispositivedefinite. Inadditiontothepositivenessoftheprincipalmomentsofinertia,
C
a physically realizable rotational inertia matrix I needs to have J that satisfies the triangular
C
inequalities(Wensingetal.,2018;Traversaroetal.,2016):
|     |     | J +J | ≥   | J   | J +J | ≥ J | J   | +J ≥ J |     |     |     |
| --- | --- | ---- | --- | --- | ---- | --- | --- | ------ | --- | --- | --- |
|     |     | 1    | 2   | 3 , | 2    | 3 1 | , 1 | 3 2    |     |     | (8) |
In Wensing et al. (2018); Traversaro et al. (2016) the triangular inequality and R ∈ SO(3) con-
straints were encoded explicitly, here we propose a change of variables such that these constraints
are encoded implicitly allowing us to utilize the standard gradient based optimizers of toolboxes
suchasPyTorch(Paszkeetal.,2017).
|     |     |     |     |     |     |     |     | (cid:2) |     |     | (cid:3)T |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | -------- |
Westartoutbyintroducingasetofunconstrainedparametersθ RAA = θ RAA1 θ RAA2 θ RAA3
that represent an axis-angle orientation from which the rotation matrix R can be recovered by ap-
plyingtheexponentialmaptotheskew-symmetricmatrixrecoveredfromθ .
RAA
|     |     |     |       |         |      |      |     |         |     |     |     |
| --- | --- | --- | ----- | -------- | ---- | ---- | --- | -------- | --- | --- | --- |
|     |     |     |       | (cid:32) | 0    | −θ   | θ   | (cid:33) |     |     |     |
|     |     |     |       |          |      | RAA3 |     | RAA2     |     |     |     |
|     |     | R   | = exp | θ        |      | 0    | −θ  |          |     |     | (9) |
|     |     |     |       |  RAA3   |      |      |     | RAA1    |     |     |     |
|     |     |     |       | −θ       |      | θ    |     | 0        |     |     |     |
|     |     |     |       |          | RAA2 | RAA1 |     |          |     |     |     |
whereexp(.)istheexponentialmappingthatmapsθ ,amemberofso(3)group,toR,amember
RAA
oftheSO(3)group(Murrayetal.,1994).
Second,tosatisfytriangularinequalityconstraintsinEq. 8above,wecanparameterizeJ ,J ,and
1 2
J asthelengthofthesidesofatriangle. Thelengthofthefirst2sidesofthetriangleareencoded
3
byJ andJ ,andthelengthofthe3rdsideiscomputedas
1 2
(cid:113)
|     |     |     | J   | = J2+J2−2J |     |     | J cosα |     |     |     | (10) |
| --- | --- | --- | --- | ---------- | --- | --- | ------ | --- | --- | --- | ---- |
|     |     |     | 3   |            |     |     | 1 2    |     |     |     |      |
1 2
with0 < α < π. ToencodethatJ ,J > 0,and0 < α < π wechoosethefollowingparametriza-
1 2
tion:
|     |     |       | )2+b, |     |       | )2+b, |     |              |     |     |      |
| --- | --- | ----- | ----- | --- | ----- | ----- | --- | ------------ | --- | --- | ---- |
|     | J   | = (θ√ |       | J   | = (θ√ |       | α   | = πsigmoid(θ | )   |     | (11) |
|     | 1   | J1    |       | 2   |       | J2    |     |              | a   |     |      |
Thus,thelearnableparametersofthisparametrizationare:
|     |     | (cid:2) |     |      |      |     |      |       |      | (cid:3) |      |
| --- | --- | ------- | --- | ---- | ---- | --- | ---- | ----- | ---- | ------- | ---- |
|     | θ   | = θ√    | θ   | θ    | θ    | θ   |      | θ√ θ√ | θ    |         | (12) |
|     | TRI |         | m h | RAA1 | RAA2 |     | RAA3 | J1    | J2 a |         |      |
Note,eventhoughtheunderlyinglearnableparametervectorθ inEq. 12isunconstrainedduring
TRI
the parameter optimization via gradient descent, the intermediate parameters J 1 ,J 2 ,J 3 ,R always
satisfy the hard constraints for physical consistency, i.e. that J , J , and J are all positive and
|     |     |     |     |     |     |     |     | 1 2 | 3   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
satisfythetriangleinequalityconstraintsinEq. 8,aswellasR ∈ SO(3). Inotherwords,italways
lieswithintheconstraintmanifoldduringoptimization.
5

ENCODINGPHYSICALCONSTRAINTSINDIFFERENTIABLENEWTON-EULERALGORITHM
3.5. CovarianceParameterizedRotationalInertiaMatrix(DiffNEACov)
Alternatively,thetriangularinequalityconstraintinEq. 8canberewrittenas(Wensingetal.,2018):
1
|     |     | Σ = Tr(I | )I    | −I (cid:31) | 0   |     | (13) |
| --- | --- | -------- | ----- | ----------- | --- | --- | ---- |
|     |     | C        | C 3×3 | C           |     |     |      |
2
which provides a somewhat easier and more intuitive representation. Again, in Wensing et al.
(2018) this constraint was imposed explicitly, through linear matrix inequalities. Here, we encode
theconstraintΣ (cid:31) 0implicitlybyenforcingaCholeskydecompositionplusasmallpositivebias
C
LLT+bI
bonthediagonal: Σ C = 3×3 . WeparametrizethislowertriangularmatrixL:
|     |     |    |     |    |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | θ   | 0   | 0   |     |     |     |
LΣ1
|     |     | L = θ | θ       | 0  |     |     | (14) |
| --- | --- | ------ | ------- | --- | --- | --- | ---- |
|     |     |        | LΣ4 LΣ2 |     |     |     |      |
|     |     | θ      | θ       | θ   |     |     |      |
|     |     |        | LΣ5 LΣ6 | LΣ3 |     |     |      |
andrecovertherotationalinertiamatrixas:
|     |     | I = Tr(Σ | )I    | −Σ  |     |     | (15) |
| --- | --- | -------- | ----- | --- | --- | --- | ---- |
|     |     | C        | C 3×3 | C   |     |     |      |
withTr()isthematrixtraceoperation,andI isa3×3identitymatrix. Thelearnableparameters
3×3
ofthisparametrizationare:
|       | (cid:2) θ√ | θ θ   | θ θ | θ       | θ   | θ (cid:3) |      |
| ----- | ---------- | ----- | --- | ------- | --- | --------- | ---- |
| θ COV | = m        | h LΣ1 | LΣ2 | LΣ3 LΣ4 | LΣ5 | LΣ6       | (16) |
This parametrization also generates fully consistent inertial parameter estimates, like the previous
parametrization,howeveritislesscomplextoimplement.
4. Experiments
In this Section, we evaluate our Torch implementation of the Newton-Euler algorithm, with the
parametrizations introduced in Section 3. We study how the parametrizations affect convergence
speed when training the parameters, and how well the dynamics generalize to unseen scenarios.
Furthermore,wecompareaspectrumofstructureddynamicslearningapproaches,startingfroman
unstructuredMLP,andsemi-structuredmodelslikeDeLaN,toourhighlystructuredapproach. We
startoutwithsimulationexperimentsandthenproviderealsystemresultsonKukaiiwa7robot.
4.1. Simulation
Insimulation,wecollecttrainingdataonasimulatedKUKAIIWAenvironmentinPyBullet
(CoumansandBai,2016–2018),bytrackingsinewavesineachjointwiththeground-truthinverse
dynamics model. The sine waves have time periods of [23.0,19.0,17.0,13.0,11.0,7.0,5.0] sec-
onds in each joint, and amplitudes [0.7,0.5,0.5,0.5,0.65,0.65,0.7] times the maximum absolute
movement in each joint. All dynamics models are trained with this sine wave motion dataset. All
feed-forward neural networks involved in MLP and DeLaN models have [32,64,32] nodes in the
hiddenlayerwithtanh()activationfunctions.
Weperformeachexperimentwith5differentrandomseeds—whichaffectstherandominitial-
izationaswellastherandomend-effectorgoalpositiontobetrackedduringgeneralizationtests—
andthencomputetheperformancestatisticswithmeanandstandarddeviationacrossthese.
6

ENCODINGPHYSICALCONSTRAINTSINDIFFERENTIABLENEWTON-EULERALGORITHM
Table 1: ComparisonbetweenmodelstrainedtooptimizeL onthesinemotiondatasetfromsimulation,
ID
intermsoftrainingspeed,jointposition(q)andvelocity(q˙)tracking,andgeneralizationperformance: end-
effectorposition(x)andvelocity(x˙)trackingunseenend-effectorreachingtasks.
|     |     |     |     |     | SineTracking(NSME) |     |     | End-EffectorTracking(NSME) |     |
| --- | --- | --- | --- | --- | ------------------ | --- | --- | -------------------------- | --- |
Model #TrainingEpochs qTracking q˙ Tracking xTracking x˙ Tracking
|     | GroundTruth  |       |     | N/A   |     | 0.000 | 0.000       | 0.005±0.006 | 0.008±0.010 |
| --- | ------------ | ----- | --- | ----- | --- | ----- | ----------- | ----------- | ----------- |
|     |              | MLP   |     | 23±3  |     | 0.000 | 0.001       | 0.256±0.405 | 5.542±6.980 |
|     |              | DeLaN |     | 58±19 |     | 0.000 | 0.001       | 0.016±0.008 | 0.254±0.278 |
|     | DiffNEANoStr |       |     | 61±53 |     | 0.000 | 0.005±0.006 | 0.005±0.006 | 0.037±0.057 |
|     | DiffNEASymm  |       |     | 8±4   |     | 0.000 | 0.000       | 0.005±0.006 | 0.011±0.011 |
|     | DiffNEASPD   |       |     | 2±1   |     | 0.000 | 0.000       | 0.005±0.006 | 0.008±0.010 |
|     | DiffNEATri   |       |     | 2±1   |     | 0.000 | 0.000       | 0.005±0.006 | 0.008±0.010 |
|     | DiffNEACov   |       |     | 2±1   |     | 0.000 | 0.000       | 0.005±0.006 | 0.008±0.010 |
4.1.1. TRAINING SPEED, GENERALIZATION PERFORMANCE, AND EFFECTIVENESS OF
|     | INVERSE |     | DYNAMICS | LEARNING |     |     |     |     |     |
| --- | ------- | --- | -------- | -------- | --- | --- | --- | --- | --- |
0.1
We train each model until it achieves at most a normalized mean squared error (NMSE) of
for all joints. We record total epochs of training required to reach that level of accuracy and store
the model once this accuracy has been achieved. Next, we evaluate model on tracking a) the sine
motionitself(whichtheparameterswerefittedfor),andb)onaseriesof5operationalspacecontrol
tasks. For the second task, we use a velocity-based operational space controller as described in
(Nakanishi et al., 2008), and use the learned inverse dynamics model within that controller. The
resultsforconvergencespeedandtrackingperformanceareaveragedacrossthe5randomseedsand
summarized in Table 1. We measure the tracking performance through NMSE, which is the mean
squared tracking error normalized by the variance of the target trajectory. The better the tracking,
the less the controller relies on the feedback component, and more on the inverse dynamics model
prediction. Thebehaviorbecomesmorecompliantasthecontributionoflinearfeedbackgoesdown.
Table 1, shows that the parametrizations of θ ,θ ,θ outperform the less constrained
|     |     |     |     |     |     | SPD | TRI | COV |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
learning, by training faster as well as low NMSE. Moreover, we see that DiffNEA performs close
to ground-truth in performance, and generalizes better than the unstructured MLP as well as the
DeLaN model: MLP model oscillates significantly in the end-effector velocity (x˙) tracking, while
| DeLaNalsooscillatesmildlyinx˙ |     |     |     |     | tracking. |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | --------- | --- | --- | --- | --- |
4.1.2. ONLINE LEARNING SPEED Figure1: Onlinelearning,withNMSEinlogscale.
| Next, | we      | measure      | how       | fast each  | model     | can      |     |     |     |
| ----- | ------- | ------------ | --------- | ---------- | --------- | -------- | --- | --- | --- |
| learn | in      | an online    | learning  | setup.     |           | We train |     |     |     |
| each  | model   | sequentially |           | without    | shuffling | on       |     |     |     |
| the   | sine    | motion       | data,     | where each | batch     | is of    |     |     |     |
| size  | of 256. | As           | the model | trains     | with      | the se-  |     |     |     |
quentialdata,wemeasureitspredictionperfor-
mancethroughtheNMSEontheentiredataset.
|      | In Fig.    | 1 we | see that | the DiffNEA     |     | model |     |     |     |
| ---- | ---------- | ---- | -------- | --------------- | --- | ----- | --- | --- | --- |
| with | rotational |      | inertia  | I parameterized |     | with  |     |     |     |
C
symmetricpositivedefinite(SPD)matrix,trian-
gularparameterization,andcovarianceparame-
terizationlearnsthefastest,butalsogeneralizes
7

ENCODINGPHYSICALCONSTRAINTSINDIFFERENTIABLENEWTON-EULERALGORITHM
thebesttotheyetunseentrainingdata, outperformingothermodelsintheonlinelearningsetupin
simulation.
4.2. RealRobotExperiments
FortherealKUKAIIWArobot,wecollectsinewavetrackingdataforabout240secondsat250Hz
using the default URDF (Unified Robot Description Format) parameters, and the Pinocchio C++
library (Carpentier et al., 2015–2019) for dynamics and kinematics of the robot. We noticed un-
modeled friction dynamics not present in simulation, and added a joint viscous friction/damping
modeltobothDeLaNandDiffNEAmodels,whoseparametersarealsolearnedfromdata. Weuse
onepositiveconstantperjointdampingwithparameterizationsimilartoJ ,J inEq. 11, butwith
|     |     |     |     | 1   | 2   |
| --- | --- | --- | --- | --- | --- |
b = 0becauseeachjointdampingconstantcanbe0.
4.2.1. EVALUATION
Table2:
ComparisonbetweenmodelstrainedtooptimizeL ID onthesinemotiondatasetontherealrobot,
in terms of the number of training epochs required to reach convergence, sine motion joint position (q)
tracking, sinemotion jointvelocity(q˙)tracking, and generalizationperformance: end-effectorposition(x)
andvelocity(x˙)trackingNMSEonanend-effectortrackingtask(unseentask/situationduringtraining).
|     | SineTracking(NMSE) |     |     | End-EffectorTracking(NMSE) |     |
| --- | ------------------ | --- | --- | -------------------------- | --- |
Model #TrainingEpochs qTracking q˙ Tracking xTracking x˙ Tracking
| DefaultModel | N/A | 0.001 | 0.009 | 0.000    | 0.016    |
| ------------ | --- | ----- | ----- | -------- | -------- |
| MLP          | 2   | 0.000 | 0.011 | 0.003    | 0.513    |
| DeLaN        | 4   | 0.001 | 0.013 | Unstable | Unstable |
| DiffNEASymm  | 3   | 0.001 | 0.012 | 0.000    | 0.013    |
| DiffNEASPD   | 3   | 0.001 | 0.013 | 0.000    | 0.014    |
| DiffNEATri   | 2   | 0.001 | 0.013 | 0.000    | 0.012    |
| DiffNEACov   | 2   | 0.001 | 0.012 | 0.000    | 0.015    |
Both MLP and DeLaN models converge to average training NMSE less than 0.1, while the
DiffNEA models converge to average training NMSE 0.35, down from the default model with av-
erageNMSE0.74. However,ascanbeseeninTable2,thetrainedDeLaNmodelisunstableduring
the end-effector tracking task, while the trained MLP model has a large end-effector velocity (x˙)
tracking NMSE due to oscillations. On the other hand, trained DiffNEA models still perform rea-
sonably,showingitsbettergeneralizationcapability. WeattributetheimperfecttrainingofDiffNEA
modelstounmodelleddynamicsoftherealsystem,suchasstaticfriction.
5. ConclusionandFutureWork
In this paper, we incorporate physical constraints in learned dynamics by adding structure to the
learnedparameters. Thisenablesustolearnthedynamicsofarobotmanipulatorinacomputational
graphwithautomaticdifferentiation,whilekeepingthelearneddynamicsphysicallyplausible. We
evaluate our approach on both simulated and real 7 degrees-of-freedom KUKA IIWA arm. Our
resultsshowthattheresultingdynamicsmodeltrainsfaster,andgeneralizetonewsituationsbetter
thanotherstate-of-the-artapproaches.
Wealsoobservethatmovingtotherealrobotcreatesnewsourcesofdiscrepanciesbetweenthe
rigidbodydynamicsandthetruedynamicsofthesystem. Factorssuchasstaticfrictioncannotbe
sufficientlycapturedbyourmodel,andpointtointerestingfuturedirections.
8

ENCODINGPHYSICALCONSTRAINTSINDIFFERENTIABLENEWTON-EULERALGORITHM
References
Chae H. An, Christopher G. Atkeson, and John M. Hollerbach. Model-based Control of a Robot
Manipulator. MITPress,Cambridge,MA,USA,1988. ISBN0-262-01102-6.
Christopher G. Atkeson, Chae H. An, and John M. Hollerbach. Estimation of inertial parameters
of manipulator loads and links. The International Journal of Robotics Research, 5(3):101–119,
1986. doi: 10.1177/027836498600500306.
Justin Carpentier, Florian Valenza, Nicolas Mansard, et al. Pinocchio: fast forward and in-
verse dynamics for poly-articulated systems. https://stack-of-tasks.github.io/
pinocchio,2015–2019.
Erwin Coumans and Yunfei Bai. Pybullet, a python module for physics simulation for games,
roboticsandmachinelearning. http://pybullet.org,2016–2018.
Roy Featherstone. Rigid Body Dynamics Algorithms. Springer-Verlag, Berlin, Heidelberg, 2007.
ISBN0387743146.
Sam Greydanus, Misko Dzamba, and Jason Yosinski. Hamiltonian neural networks. CoRR,
abs/1906.01563,2019. URLhttp://arxiv.org/abs/1906.01563.
Jayesh K. Gupta, Kunal Menda, Zachary Manchester, and Mykel J. Kochenderfer. A general
framework for structured learning of mechanical systems. CoRR, abs/1902.08705, 2019. URL
http://arxiv.org/abs/1902.08705.
Jayesh K. Gupta, Kunal Menda, Zachary Manchester, and Mykel J. Kochenderfer. Structured me-
chanical models for robot learning and control. CoRR, abs/2004.10301, 2020. URL http:
//arxiv.org/abs/2004.10301.
K. Hitzler, F. Meier, S. Schaal, and T. Asfour. Learning and adaptation of inverse dynamics mod-
els: A comparison. In 2019 IEEE-RAS 19th International Conference on Humanoid Robots
(Humanoids),pages491–498,2019.
M. Jansen. Learning an accurate neural model of the dynamics of a typical industrial robot. In
InternationalConferenceonArtificialNeuralNetworks,page1257–1260,1994.
D. Kappler, F. Meier, N. Ratliff, and S. Schaal. A new data source for inverse dynamics learning.
In 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages
4723–4730,Sep.2017. doi: 10.1109/IROS.2017.8206345.
Krzysztof R. Kozlowski. Modelling and identification in robotics. Springer Science & Business
Media,2012.
F.D.LedezmaandS.Haddadin. First-order-principles-basedconstructivenetworktopologies: An
application to robot inverse dynamics. In 2017 IEEE-RAS 17th International Conference on
Humanoid Robotics (Humanoids), pages 438–445, Nov 2017. doi: 10.1109/HUMANOIDS.
2017.8246910.
9

ENCODINGPHYSICALCONSTRAINTSINDIFFERENTIABLENEWTON-EULERALGORITHM
J. Y. S. Luh, M. W. Walker, and R. P. C. Paul. On-Line Computational Scheme for Mechani-
cal Manipulators. Journal of Dynamic Systems, Measurement, and Control, 102(2):69–76, 06
1980. ISSN 0022-0434. doi: 10.1115/1.3149599. URL https://doi.org/10.1115/1.
3149599.
M.Lutter,C.Ritter,andJ.Peters. Deeplagrangiannetworks: Usingphysicsasmodelpriorfordeep
learning. In7thInternationalConferenceonLearningRepresentations(ICLR),May2019. URL
https://openreview.net/pdf?id=BklHpjCqKm.
M.Mistry,S.Schaal,andK.Yamane. Inertialparameterestimationoffloatingbasehumanoidsys-
temsusingpartialforcesensing. In20099thIEEE-RASInternationalConferenceonHumanoid
Robots,pages492–497,Dec2009. doi: 10.1109/ICHR.2009.5379531.
Richard M. Murray, S. Shankar Sastry, and Li Zexiang. A Mathematical Introduction to Robotic
Manipulation. CRCPress,Inc.,BocaRaton,FL,USA,1stedition,1994. ISBN0849379814.
JunNakanishi,RickCory,MichaelMistry,JanPeters,andStefanSchaal.Operationalspacecontrol:
Atheoreticalandempiricalcomparison. TheInternationalJournalofRoboticsResearch,27(6):
737–757, 2008. doi: 10.1177/0278364908091463. URL https://doi.org/10.1177/
0278364908091463.
D. Nguyen-Tuong, J. Peters, M. Seeger, and B. Scho¨lkopf. Learning inverse dynamics: A com-
parison. In Advances in Computational Intelligence and Learning: Proceedings of the Euro-
peanSymposiumonArtificialNeuralNetworks,pages13–18,Evere,Belgium,April2008.Max-
Planck-Gesellschaft,d-side.
Adam Paszke, Sam Gross, Soumith Chintala, Gregory Chanan, Edward Yang, Zachary DeVito,
Zeming Lin, Alban Desmaison, Luca Antiga, and Adam Lerer. Automatic differentiation in
pytorch. InNIPS-W,2017.
Jean-JacquesE.SlotineandWeipingLi. Ontheadaptivecontrolofrobotmanipulators. TheInter-
national Journal of Robotics Research, 6(3):49–59, 1987. doi: 10.1177/027836498700600303.
URLhttps://doi.org/10.1177/027836498700600303.
S. Traversaro, S. Brossette, A. Escande, and F. Nori. Identification of fully physical consistent
inertialparametersusingoptimizationonmanifolds. In2016IEEE/RSJInternationalConference
onIntelligentRobotsandSystems(IROS),pages5446–5451,Oct2016. doi: 10.1109/IROS.2016.
7759801.
P.M.Wensing,S.Kim,andJ.E.Slotine. Linearmatrixinequalitiesforphysicallyconsistentinertial
parameter identification: A statistical perspective on the mass distribution. IEEE Robotics and
AutomationLetters,3(1):60–67,Jan2018. ISSN2377-3774. doi: 10.1109/LRA.2017.2729659.
10