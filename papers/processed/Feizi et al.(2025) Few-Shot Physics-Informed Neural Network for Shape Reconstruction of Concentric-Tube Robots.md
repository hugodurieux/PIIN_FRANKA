Few-Shot Physics-Informed Neural Network for Shape Reconstruction
of Concentric-Tube Robots
Navid Feizi*, Filipe C. Pedrosa*, Rajni V. Patel**, and Jagadeesan Jayender**
Abstract—Modeling concentric tube robots (CTRs) involves SafenavigationofaCTRinmedicalapplicationsrequires
complex nonlinear continuum mechanics, and despite recent accuratemotionplanning,notonlyforthedistalend,butalso
progress,physics-basedmodelsoftenlackanaccuraterepresen-
for the entire body of the robot to avoid collisions with the
tationoftheexperimentalsetups.Toovercometheselimitations,
surrounding anatomy [9]. This demands a precise kinematic
deep neural network-based models have been explored as al-
ternativeswithsuperioraccuracy;however,theyoftenoverlook modelcapableofestimatingtheshapeoftherobotforagiven
knownmechanics,requirelargetrainingdatasets,andtypically set of actuation inputs while being computationally efficient
discard shape estimation of the robot. We present a physics- for real-time control/planning applications.
informed neural network (PINN) for kinematic modeling of
a 6-DoF CTR with three pre-curved tubes that embeds the A. Related Work
Cosserat rod differential equations and learns from few-shot
observational data, balancing physics priors with data-driven Physics-basedmodelingofCTRsiscommonlyfoundedon
fitting.PINNenablesfull-stateestimationofshape,twistangle, the well-established Cosserat rod theory, in which the tubes
torsionalstrain,bendingmoment,andorientation.Benchmark are considered inextensible and without transverse shear
tests show a mean shape error below 1% of the robot length strain [10]–[14]. Using this, the kinematics are formulated
andaccuratelyrecoveredotherkinematicstates,outperforming
into a boundary value problem (BVP) that reconstructs the
a purely physics-based Cosserat rod model baseline while
using a minimal training set. The resulting model is also full backbone shape of the robot. The BVP can be solved
computationally efficient and robust, making it well-suited for using optimization-based numerical methods [15] to obtain
real-time control applications. the states. However, optimization-based iterative solvers are
computationallydemandingandhighlysensitivetoactuation
I. INTRODUCTION inputs and initial conditions. This leads to inconsistent com-
putationtime,makingthisapproachinadequateforreal-time
Concentric tube robots (CTRs), are a subclass of contin-
path planning applications, specifically with sampling-based
uum robots that consist of two or more pre-curved flexible
techniques such as rapidly-exploring random tree, where
tubes[1],[2].Axialtranslationandrotationofthesetubesal-
the model is evaluated frequently [16]. Furthermore, despite
lowactivemanipulationofthebackbonecurvatures,enabling
substantialprogress,physics-basedmodelsremainlimitedin
the robot to generate complex three-dimensional shapes [3].
accuracy due to unmodeled effects, including friction, tube
Due to their slender, needle-like structure and dexterity,
clearance, and nonlinear constitutive laws.
CTRs have been widely investigated for applications requir-
Deepneuralnetwork(DNN)areknownfortheircapability
ingnavigationthroughtortuouspathways,particularlyinthe
to serve as universal function approximators. They have
minimally invasive surgery domain, including skull base,
been used to learn the kinematics or dynamics of various
abdominal, thoracic, and cardiac [4]–[8].
systems [17]. If a collection of solution-labeled pairs is
provided, a DNN can be trained to estimate the solution
*N.FeiziandF.C.Pedrosacontributedequallytothiswork.
mapping through supervised learning. In [18], a multilayer
**R.V.PatelandJ.Jayenderareco-seniorauthors.
ThisworkwassupportedbytheNationalInstituteofDiabetesandDiges- perceptron (MLP) was trained on 80K data points to learn
tiveandKidneyDiseasesoftheNationalInstitutesofHealth(NIH)through theforwardkinematicsofa6-DoFCTR,predictingthedistal
awardnumberR01DK119269andNationalInstituteofBiomedicalImaging
endpositionandorientationfromjointconfigurations.In[19]
andBioengineeringoftheNIHunderawardnumberR01EB028278(JJ)and
by the Natural Sciences and Engineering Research Council (NSERC) of an MLP was trained on 94K data points, showing that using
CanadagrantRGPIN1345(RVP),andtheCanadaResearchChairsProgram quaternion/vector-pairs outperforms other representations in
(RVP).
learning the forward kinematics. Their experimental dataset,
Navid Feizi is with the Department of Radiology at Brigham and
Women’sHospital,andHarvardMedicalSchool,Boston,MA02115,USA consisting of 100K configurations, was published in [20],
(e-mail:nfeizi@bwh.harvard.edu). which we have used in this paper. In [21], an MLP was
FilipeC.PedrosaiswithCanadianSurgicalTechnologiesandAdvanced
trained on a 100K dataset, consisting of the shape of the
Robotics(CSTAR),LondonHealthSciencesCentre(LHSC),andwiththe
Department of Electrical and Computer Engineering, Western University, CTRdetectedbycameras,toreconstructtheentirebackbone
London,Ontario,Canada.(e-mail:fpedrosa@uwo.ca). of a three-tube CTR, demonstrating a two-fold reduction
Rajni V. Patel is with CSTAR, and with the Department of Electrical
in average error and nearly six-fold reduction in maximum
andComputerEngineering,theDepartmentofSurgery,theDepartmentof
ClinicalNeurologicalSciences,andtheSchoolofBiomedicalEngineering, error compared to the physics-based model. In [22], an
WesternUniversity.(e-mail:rvpatel@uwo.ca). inverse kinematics was learned from robot shapes captured
Jagadeesan Jayender is with the Department of Radiology at Brigham
bycamerasusing100Kdatapoints.In[23],theforwardand
and Women’s Hospital, and Harvard Medical School, Boston, MA 02115,
USA(e-mail:jayender@bwh.harvard.edu). inverse kinematics of a 4-DoF CTR were learned employing
6202
yaM
21
]OR.sc[
1v09721.5062:viXra

an LSTM-MLP network structure that is able to capture the • Recovery of the entire 3D backbone shape of the CTR
snapping behavior, where the network was trained on 200K without the need for a shape-sensing modality.
data points recorded in 21 hours. • Estimation of the latent states of the CTR, including
DNN-basedmodelingapproachesoftenyieldamoreaccu- twist angle, torsional strain, and orientation.
|                     |     |     |              |     |            |               |     | Comprehensive |     |     | evaluation | in  | simulation | and with | the |
| ------------------- | --- | --- | ------------ | --- | ---------- | ------------- | --- | ------------- | --- | --- | ---------- | --- | ---------- | -------- | --- |
| rate representation |     | of  | the physical |     | robot than | physics-based |     | •             |     |     |            |     |            |          |     |
methods, as they can capture uncertainties and unmodeled open-source experimental dataset in [20].
| behaviors, | which | are | typically | neglected |     | in physics-based |     |     |     |     |     |     |     |     |     |
| ---------- | ----- | --- | --------- | --------- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
C. Outline
| formulations | but | are | implicitly | learned | from | experimental |     |     |     |     |     |     |     |     |     |
| ------------ | --- | --- | ---------- | ------- | ---- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
data [19]–[21]. Since DNN prediction requires only a for- The remainder of this paper is organized as follows. In
ward pass through the network [24], [25], rather than an Section II, we introduce some preliminaries, including the
iterative optimization based solver to solve the Cosserat rod CosseratrodtheoryformodelingCTRsandthefoundational
| BVP, these | approaches |     | are | computationally |     | less | demanding |     |     |     |     |     |     |     |     |
| ---------- | ---------- | --- | --- | --------------- | --- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
conceptsofPINNs.SectionIIIdescribestheproposedPINNs
and more stable, However, standard DNN is data-hungry framework and training strategy. In Section IV, we present
which often requires tens of thousands of training samples simulation and experimental results. Finally, Section V pro-
| as it learns | solely | from | observation |     | data, | neglecting | the |                  |     |          |     |     |     |     |     |
| ------------ | ------ | ---- | ----------- | --- | ----- | ---------- | --- | ---------------- | --- | -------- | --- | --- | --- | --- | --- |
|              |        |      |             |     |       |            |     | vides concluding |     | remarks. |     |     |     |     |     |
underlyingphysics.Ingeneral,collectingalargedatasetfrom
an experimental setup is challenging and may cause wear II. PRELIMINARIES
| of the setup. | More      | importantly, |     | despite       | the | backbone | being       |             |     |        |     |     |     |     |     |
| ------------- | --------- | ------------ | --- | ------------- | --- | -------- | ----------- | ----------- | --- | ------ | --- | --- | --- | --- | --- |
|               |           |              |     |               |     |          |             | A. Cosserat | Rod | Theory |     |     |     |     |     |
| essential     | for tasks | such         | as  | path planning |     | and      | follow-the- |             |     |        |     |     |     |     |     |
leader implementations, in most conventional DNN-based a) Kinematics: Using Cosserat rod theory [10], [13],
|             |        |       |     |       |             |     |           | [14], the | shape | of a | rod (tube) | of  | length | ℓ is represented |     |
| ----------- | ------ | ----- | --- | ----- | ----------- | --- | --------- | --------- | ----- | ---- | ---------- | --- | ------ | ---------------- | --- |
| approaches, | except | [21], | the | shape | estimation, |     | which de- |           |       |      |            |     |        |                  |     |
mands a shape-sensing modality, increasing the difficulty by a continuous homogeneous transformation g(s) SE(3)
∈
alongthecenterlineoftherod,whereg(s)consistsofaposi-
| of generating                                       |              | the dataset, | is           | disregarded, |               | and only | the end    |             |      |               |              |                |        |                 |        |
| --------------------------------------------------- | ------------ | ------------ | ------------ | ------------ | ------------- | -------- | ---------- | ----------- | ---- | ------------- | ------------ | -------------- | ------ | --------------- | ------ |
|                                                     |              |              |              |              |               |          |            | tion vector | p(s) | R3            | and a        | rotation       | matrix | R(s)            | SO(3), |
| effector                                            | of continuum |              | robots       | is modeled   | [18],         | [23],    | [24].      |             |      |               |              |                |        |                 |        |
|                                                     |              |              |              |              |               |          |            |             |      | ∈             |              |                |        | ∈               |        |
|                                                     |              |              |              |              |               |          |            | where       | s    | [0,ℓ] denotes |              | the arc-length |        | (for notational |        |
| Physics-informedneuralnetworks(PINNs)incorporatethe |              |              |              |              |               |          |            |             | ∈    |               |              |                |        |                 |        |
|                                                     |              |              |              |              |               |          |            | simplicity, | we   | omit          | the explicit | dependence     |        | on s            | in the |
| governing                                           | physics      | into         | the training |              | loss function |          | along with |             |      |               |              |                |        |                 |        |
the observation dataset [26]. By embedding the physics into following equations). Accordingly, the spatial derivatives of
|              |             |     |               |     |                |     |            | R and p | are given | by  |      |        |     |     |     |
| ------------ | ----------- | --- | ------------- | --- | -------------- | --- | ---------- | ------- | --------- | --- | ---- | ------ | --- | --- | --- |
| the training | process,    |     | PINNs         | can | significantly  |     | reduce the |         |           |     |      |        |     |     |     |
| amount       | of required |     | observational |     | data, creating |     | a balance  |         |           |     |      |        |     |     |     |
|              |             |     |               |     |                |     |            |         |           | R˙  | =Ru, | p˙ =Rv |     |     | (1) |
between data and physics-based information, or even elimi- (cid:98)
natingitinfullyphysics-basedformulationsasin[26].PINN wherevanduarethelinearandangularstrains,respectively.
| has been | recently | adapted | for | various | robotic | applications. |     |          |        |             |     |         |          |       |       |
| -------- | -------- | ------- | --- | ------- | ------- | ------------- | --- | -------- | ------ | ----------- | --- | ------- | -------- | ----- | ----- |
|          |          |         |     |         |         |               |     | In other | words, | the vectors |     | v and u | describe | how p | and R |
It has been used to solve time domain ordinary differential vary with respect to the arc-length of the rod. The operator
equations (ODEs) with variable initial conditions to model () denotes the Lie algebra of SO(3), 3 3 skew-symmetric
(cid:98)
the dynamics of a robotic arm [27], as well as to learn · R3 ×
|     |     |     |     |     |     |     |     | m atrices | mapping | vectors | from |     | to so (3). |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ------- | ------- | ---- | --- | ---------- | --- | --- |
the dynamics of the end effector of a tendon-driven robot b) Constitutive Law: Based on the linear constitutive
| [28]. Bensch |     | et al. | [25] demonstrated |     |     | that incorporating |     |          |              |     |        |         |        |                |     |
| ------------ | --- | ------ | ----------------- | --- | --- | ------------------ | --- | -------- | ------------ | --- | ------ | ------- | ------ | -------------- | --- |
|              |     |        |                   |     |     |                    |     | law, the | relationship |     | of the | strains | to the | internal force | n   |
Cosserat rod differential equations into the training loss and moment m at s is described as follows:
| facilitated | complete |     | shape | estimation | of  | a tendon-driven |     |     |     |     |     |     |     |     |     |
| ----------- | -------- | --- | ----- | ---------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
continuumrobotwithhighaccuracyinsimulation,whilesub- n=RK (v v∗) (2a)
se
−
stantially reducing computational costs compared to solving m=RK (u u∗) (2b)
bt
| the Cosserat | BVP. |     |     |     |     |     |     |       |             |     |     | −   |        |                 |     |
| ------------ | ---- | --- | --- | --- | --- | --- | --- | ----- | ----------- | --- | --- | --- | ------ | --------------- | --- |
|              |      |     |     |     |     |     |     | where | K =diag(GA, |     | GA, | EA) | is the | shear-extension |     |
se
B. Contributions stiffness matrix, K bt =diag(EI xx , EI yy , GI zz ) is the
|     |     |     |     |     |     |     |     | bending-torsion |     | stiffness | matrix, | A   | is the | cross-sectional |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --------- | ------- | --- | ------ | --------------- | --- |
In this work, we propose, to the best of our knowledge, area,E istheYoung’smodulus,Gistheshearmodulus,and
| the first | PINN | for the | real-time | forward |     | kinematics | of a 6- |      |         |        |         |     |            |               |     |
| --------- | ---- | ------- | --------- | ------- | --- | ---------- | ------- | ---- | ------- | ------ | ------- | --- | ---------- | ------------- | --- |
|           |      |         |           |         |     |            |         | I ,I | are the | second | moments | of  | area about | the principal |     |
xx yy
DoF CTR in free space. The model incorporates Cosserat axes of the cross-section, and I is the polar moment of
zz
| rod equations,effectively |     |          | balancingphysics-based |               |     |         | principles |          |                                               |     |        |        |        |              |     |
| ------------------------- | --- | -------- | ---------------------- | ------------- | --- | ------- | ---------- | -------- | --------------------------------------------- | --- | ------ | ------ | ------ | ------------ | --- |
|                           |     |          |                        |               |     |         |            | inertia. | The unloaded                                  |     | linear | strain | of the | rod is given | by  |
| with data-driven          |     | fitting, | which                  | significantly |     | reduces | the size   |          |                                               |     |        |        |        |              |     |
|                           |     |          |                        |               |     |         |            | v∗ =[0,  | 0, 1]⊤,andtheunloadedcurvature(pre-curvature) |     |        |        |        |              |     |
of the required observation dataset while enabling the es- oftherodisu∗ =[κ , 0, 0]⊤,sinceweonlyassumeplanar
i
| timation  | of entire | shapes,           | without |      | using | any shape-sensing |     |          |                       |       |     |                           |     |     |     |
| --------- | --------- | ----------------- | ------- | ---- | ----- | ----------------- | --- | -------- | --------------------- | ----- | --- | ------------------------- | --- | --- | --- |
|           |           |                   |         |      |       |                   |     | unloaded | curvature             | about | the | x-axis.                   |     |     |     |
| modality. | Our       | key contributions |         | are: |       |                   |     |          |                       |       |     |                           |     |     |     |
|           |           |                   |         |      |       |                   |     | c)       | EquilibriumEquations: |       |     | Thestaticequilibriumequa- |     |     |     |
• Formulation of a PINN that incorporates the Cosserat tions of a rod subject to a distributed external force f and
rodequationsforCTR,reducingthenumberofrequired moment l per unit length are obtained by integrating the
experimental measurements from tens of thousands to free-body diagram of a cantilever beam extending from s to
a few hundred. ℓ [10]. Differentiating the mechanical equilibrium equation

with respect to the arc-length s yields the classical equilib-
rium equations for a Cosserat rod:
n˙ +f =0 (3a)
m˙ +p(cid:98)˙ n+l=0 (3b)
Differentiating (2b) and using (1), we can write (3b) in
terms of u, f, and l as follows:
(cid:16) (cid:90) ℓ (cid:17)
u˙ =u˙∗ K−1 u (cid:98) K(u u∗)+ (cid:98) e 3 R⊤ f(σ)dσ+R⊤l Fig.1. Athree-tubeCTRdemonstratingsixsegmentsalongitsbackbone
− − s aswellastransitionpointswherecontinuitymustbemaintained.
(4)
where e =[0, 0, 1]⊤. Equation (4) along with (1) forms a
3
system of differential equations with boundary conditions at
and the torsional curvature for the innermost tube is com-
s=0 and s=ℓ that can be solved to reconstruct the shape
puted as
of a rod under external loads.
d) StaticModelofaCollectionofTubes: Consideringa (cid:16) (cid:17)(cid:12)
u =K−1 mb+K u∗+R K u∗+R K u∗ (cid:12) (9)
CTR composed of n tubes, the static equilibrium condition 1,x,y 1 1 1 2 2 2 3 3 3 (cid:12) x,y
is obtained by summing the contributions from all tubes.
e) Boundary Conditions: Inputs to the model are de-
Accordingly,theinternalforceandmomentatacross-section
scribed by linear β and angular α actuation values applied
atarc-lengthsaregivenbythesumofthecontributionsfrom i i
attheproximalendoftheith tube,asshowninFig.1.Thus,
each tube as follows:
the differential equations in (7) are subject to the following
n
(cid:88) n˙ +f =0 (5a) boundary conditions at the base (s=0):
i i
i=1  
0
n
(cid:88) m˙ i +p(cid:98)˙n i +l i =0 (5b) θ(0)=α 2 − β 2 u 2,z (0) − (α 1 − β 1 u 1,z (0)) (10)
α β u (0) (α β u (0))
i=1 3 − 3 3,z − 1 − 1 1,z
Assuming that the tubes are concentric, they share the
samecenterlinecurvepandtangentp˙,whileremainingfree p(0)=[0,0,0]⊤ (11)
to twist independently. Accordingly, the rotation matrix of
the ith tube can be expressed in terms of the rotation of R(0)=Rot (α β u (0)) (12)
z 1 1 1,z
−
the innermost tube and its relative twist angle, with respect
to tube 1, θ , as R =R R (θ ), where the matrix R (θ ) The known distal boundary condition at s=ℓ for a CTR
i i 1 z i z i i
denotes the rotation about the z-axis by θ . in free space is given by:
i
u i =R⊤ z,i u 1 +θ˙ i e 3 , θ˙ i =u i,z − u 1,z (6) mb 1,x,y (ℓ 1 )=0 (13)
This implies that only the z-components of the tube G J u (ℓ )=0, i=1,...,n
i i i,z i
curvatures are independent variables. Using this, (4) can be
where ℓ is the arc-length at the distal termination point of
rewrittenforeachtube.Sincethexandy componentsofthe i
tube i, as shown in Fig. 1.
tube curvatures are identical across all tubes, we only retain
the individual torsional component u in the equations. f) Implementations: A challenge in solving the BVP
i,z
For the sake of notational simplicity, we use the x and defined by (7) and (10) - (13) arises from the discontinuities
y components of the body-frame bending moment of the in stiffness and pre-curvature of the tubes at transition
innermost tube (i = 1), mb , instead of u , leading points. We divide the spatial domaininto multiple segments,
1,x,y 1,x,y
to the following system of ODEs for an n-tube CTR under as show in Fig. 1, and ensure continuity of the position,
external loads: orientation, and bending moments at the interfaces between
m˙ b 1,x,y = (cid:0) − u (cid:98)1 mb 1 − (cid:98) e 3 R⊤ 1 (cid:1)(cid:12) (cid:12) x,y these segments.
u˙ =u˙∗ + E i I i(cid:0) u u∗ u u∗ (cid:1) g i (s−)=g i (s+), m i (s−)=m i (s+) (14)
i,z i,z G J i,x i,y− i,y i,x
i i
θ˙ =u u (7) The BVP in (7) is non-trivial because the constraints are
i i,z 1,z
− split between the proximal and distal ends of the tubes. In
p˙ =R e
1 1 3 practice, one can employ a shooting method: (i) guess the
R˙ 1 =R 1 u (cid:98)1 unknown proximal boundary conditions, (ii) integrate the
where ODE forward, and (iii) iteratively update the guess so that
the distal boundary conditions are satisfied [15]. This can
N
mb = (cid:2) mb ,mb ,mb (cid:3)⊤ , mb = (cid:88) G J u . (8) be computationally expensive and highly sensitive to initial
1 1,x 1,y 1,z 1,z i i i,z
guesses.
i=1

TABLEI
B. Physics-Informed Neural Networks
CTRTUBEKINEMATICPARAMETERS
DNN relies solely on observational data, neglecting the
underlying physics of the system, which necessitates a large Parameter TubeI TubeII TubeIII
trainingdatasettogeneralizeeffectively.Inmanyengineering
Innerdiameter[mm] 0.40 0.70 1.20
scenarios, including robotics, the underlying physics of the Outerdiameter[mm] 0.50 0.90 1.50
system is well investigated and can be included in training Straightlength[mm] 169.00 65.00 10.00
Curvedlength[mm] 41.00 100.00 100.00
DNNs. By incorporating physics, the DNN is essentially Curvature(κ)[m − 1] 28 12.4 4.37
restrictedtoalowerdimension,whichallowsittobetrained Young’sModulus(E)[GPa] 50.00 50.00 50.00
using a limited amount of data [29]. ShearModulus(G)[GPa] 19.23 19.23 19.23
In the seminal work by Raissi et al. [26] PINN was
proposed for learning the solution of a partial differential
equation (PDE) by incorporating the differential equation,
boundary, and initial functions into the training loss. This
spatio-temporal function approximation is an alternative for
solving nonlinear PDEs, eliminating the need for sampled
solutions for training, as well as avoiding linearization or
time-stepping.
By discarding the temporal domain, PINN can also be
used to solve BVPs. Assume a differential equation defined
by x˙ = (x,s) with boundary function g(x,s )=0,
bound
N
PINN approximates x for s [0,ℓ]. The parameters of the
∈
neural network are trained by minimizing the following loss
function:
=λ +λ Fig. 2. Block diagram of the PINN including the structure and training
ode ode bc bc
L L L lossterms.
1 N (cid:88)ode
= (x ) (x ,s )
N ode ∥∇ s i −N i i ∥2 (15)
i=1 also from the experimental observation dataset. The physics
1 (cid:88) Nbc loss enforces the PINN to learns the evolution/dynamics
+ g(x ,s )
N bc i=1 ∥ i i ∥2 o w f it t h he re s s y p s e t c e t m to ( s 7 , ), fo s l u l c o h ws th t a h t e ∇ sy s s xˆ te , m th d e y d n e a r m iv i a c t s iv x e ˙, o w f h P il I e N t N he s
where x is the PINN output at s and is the derivative boundary and observation loss terms anchor the solution to
i i s
∇
operator with respect to s that can be computed by applying the specified region of the state space. Fig 2 illustrates the
the chain rule using automatic differentiation, and N and block diagram of the proposed PINN and the loss terms.
ode
N bc are the number of collocation points for the ODE and The ODE loss is defined as follows:
boundary conditions, respectively. The terms λ and λ
ode bc
are weights that balance the contributions of loss terms. 1 (cid:88)
Node
(cid:88) (cid:13) (cid:13)
L ode = N λo g de(cid:13)e g,i(cid:13) 2 (16)
ode
III. METHODS i=1g∈{mb,u,θ,p,h}
Weconsiderathree-tubeCTRwithindependentlyactuated where
translations and rotations of each tube with the design
eode =[eode,eode,eode,eode,eode]= xˆ (xˆ ,s ,τ )
parameters mentioned in Table I, which is the same as i mb u θ p h ∇ s i −N i i i
the CTR used in [20]. The actuation input is defined as (17)
τ =[β 1 , β 2 , β 3 , α 1 , α 2 , α 3 ]⊤ R6, where repre- where λo g de is a weighting vector for each state group,
sents the allowable actuation s ∈ pa B ce ⊆ . The system B state is balancing the loss terms to ensure equal loss scales. N ode
represented by x=[mb , u , θ , p , h ]⊤ R15, as is the number of collocation points sampled in the domain
described in (7). 1,x,y i,z i 1 1 ⊆ [0,ℓ 1 ] , which will be described in the next section. It
×B
should be noted that is described by (7), and the system
N
A. Implementation parameters E, G, I, J, and u∗ vary depending on the
The PINN approximates the mapping φ:R7 R15, segment of the robot in which s i lies.
where the inputs are arc-length and joints ac → tuation The boundary loss is defined as follows:
[s,τ] [0,ℓ ] R6,andtheoutputisthestatexˆ(s) R15.
T 10 h 0 eP n I o ∈ N de N s a p r 1 e c r h × i l t a e y c e tu r, re a i n s d an th M e L ta P n w h i a th ct s iv ix at h io id n de fu n n l c a t y io e ⊆ n rs w an a d s L bc = N 1 bc (cid:88) Nbc (cid:88) λb g c (cid:13) (cid:13)e g,i (cid:13) (cid:13) 2 (18)
i=1g∈{mb,u,θ,p,h}
used for all layers except the output layer.
We extend the loss function (15) adding observation loss where λode is a weighting vector. To compute e ,
g i
to not only learn from the physics of the system but four forward calls to the PINN are required at
obs
L

TABLEII
Collocation Observation Boundary
200 200
TRAININGDATAPOINTS
150 m] 150 m]
collocation boundary obs(model) obs([20])
100s [ 100s [
#samples 20,000 1,000 1,000 500
50 50
0 0
0 20
− 60 β 1 − [m 40 ] − 20 − 6 − 0 4
−
0 β
2
2
0
[
m]
− 60 − β 2 40 [m] − 20 − 20
0
β3 [
m]
− (β 10.0 5 ≤ 5. β 0) 3 ≤ β 0.0 m β m, m th m e , p a ro n x d im th a e l p tr r a o n x s i l m at a io l n tra o n f s t l u a b ti e on 2 o to f
3 2 3
− ≤ ≤
tube 1 to (β 15.0) β β mm. The rotational inputs
Fig. 3. Linear actuation βi and arc-length s of the training data points.
of all tubes w
2 −
ere cons
≤
train
1
ed
≤
to
2
π α π.
Collocation, boundary, and observation samples are shown in blue, red, i
− ≤ ≤
andblack,respectively.Allsamplesliewithintheboundarydefinedbythe
We train the PINN in two stages. (a) Simulation-based
inequalities for βi. The gray regions indicate the planes at the base and
distalendsofthetubes. training: We generate synthetic observations with a Cosserat
rod model; each observation is a set of distal-tip positions
of the three tubes. Samples are drawn over the actuation
s = 0,ℓ ,ℓ ,ℓ with the actuation inputs τ ,
an i d e { bc = 3, [ i ebc 2, , i eb 1 c , , i e } bc,ebc,ebc]. i space τ ∈B and at s= { ℓ 1 ,ℓ 2 ,ℓ 3 } . (b): Experiment-based
i mb u θ p h training:Wecontinuetrainingbyincorporatingexperimental
ebc =x(ℓ ,τ ) tip-position measurements for tubes 1–3 from the dataset
mb 1,i i mx,y
published in [20] into the observation loss . Note
eb u c =x(ℓ j,i ,τ i ) uz , for j ∈{ 1,2,3 } that [20] spans a broader range for β ; howev L er o , bs because
i
eb θ c =x(0,τ i ) θ − θ(0,τ i ) (19) α i are constrained to ± π/3, the actuation space is snap
ebc =x(0,τ ) p(0,τ ) free. The collocation, boundary, and observation sets for the
p i p − i
simulation-basedcaseareillustratedinFig.3,andthesample
ebc =x(0,τ ) h(0,τ )
h i h − i counts are listed in Table II.
Inafreespacecase,ebcandebcarezeroattheboundaries,
u m PINNs require a larger number of epochs to train com-
as in (13) and θ, p, and h are as described in (10)-(12).
pared to conventional DNNs. This is due to three reasons:
The observation loss is defined as follows:
(a)Multi-objectivelossterms,whichmayinvolvestateterms
L obs = N 1 obs (cid:88) N i= ob 1 s λo p bs (cid:13) (cid:13)x(s i ,τ i ) p − p¯(s i ,τ i ) (cid:13) (cid:13) 2 (20) a th n a d t L ar o e bs sc o a f l t e e d n c v o e n ry ve d rg if e fe q re u n ic tl k y l , y s a o t m fi e r t s im t, e th s e c n on th fl e ic o ti p n t g im . i L ze bc r
needstensofthousandsofstepstominimizethe .While
ode
where p¯ is a few-shot position observation data, that can be L
using adjusted loss weights, as described in Section III-A,
obtained from experimental measurement or the solution of
provides some balance, it is insufficient, leading to gradient
the Cosserat rod model in simulation. All weighting terms
pathologies [32]. (b) Ill-conditioned ODE loss: Higher-order
λodr, λbc, and λobs are tuned empirically to balance the loss
g g p derivatives from autograd make the loss landscape poorly
terms.
conditioned, so the optimizer takes many steps to balance
The PINN and the Cosserat rod equations were imple-
terms[32].(c)Thespectralbiasofthenetwork:PINNstend
mented in Python using PyTorch tensors, enabling using
to capture the low-frequency components of the solution
Autograd to compute the spatial derivative xˆ and also
s first, while higher-frequency components require substan-
∇
backpropagation through the Cosserat residuals for training.
tially more training epochs to be learned [33]. All these
B. Training together make training to require multiple steps, and highly
sensitive to the optimizer.
The collocation points for the ODE loss were sampled
using a uniform random sampler in [0,ℓ ] , where For training, we used the L-BFGS [34] optimizer, which
1
×B B
is primarily constrained by the physical joint limits of the approximates second-order curvature for optimization, mak-
robot. The boundary points were also sampled similarly for ing it robust to the loss landscapes conditions. In our ex-
τ. However, the arc-length was set to the boundary points periments, L-BFGS significantly outperformed Adam [35],
of the three tubes s= 0,ℓ ,ℓ ,ℓ . which aligns with recent findings in [36] where it was
3 2 1
{ }
Remark: Due to the mechanical design of CTRs, specif- observed that L-BFGS can reduce the PINN loss by several
ically certain joint configurations, and particularly those orders of magnitude more than Adam, attributed to the
involving high torsion, there may exist multiple solu- ill-conditioning of the loss landscape, which a first-order
tions to the BVP [30], [31]. This phenomenon, known as gradient-based method cannot address. We initialized the
snapping, causes the robot to abruptly transition between network weights using Xavier [37] and trained the network
equilibrium configurations. Since PINNs are not designed with learning rate 2.0, tolerance 1×10-10, a “strong-Wolfe”
to handle such multi-modal behaviors [26], we restrict line search method. The training was performed on a work-
the actuation domain to avoid these scenarios. Specifi- station with an NVIDIA RTX 3080 GPU for enough epochs
cally, the proximal translation of tube 3 was limited to 300,000 until the error reduced to an acceptable level.
≥

Base
PINN
Cosserat
40
20
0 m]
m
20 [
− y
40
−
60
−
80
−
40 80
60 z[m
m ]
80
120 40− 20 0
2
x
0
[m
40
m]
−
Fig. 4. Shape estimation of the PINN trained on simulated observation
datasetandCosseratrodmodelforrandomactuations.
2
1
0
0.0 0.2 0.4 0.6 0.8 1.0
s/‘1
s%
100
0
Normalized Error
avg
min-maxbound
std
Fig. 5. Average backbone error with standard deviation and minimum-
maximum bounds. The Euclidean distance error was normalized by the
corresponding arc-length along the backbone. The horizontal axis is nor-
malizedbyℓ1.
IV. RESULTSANDDISCUSSION
A. Trained using Synthesized Observations Dataset
Fig. 4 shows the three-dimensional shape of the CTR as
estimated by the PINN, in comparison to the Cosserat rod
model, which serves as the ground truth, using 12 randomly
selectedunseenactuationinputs.Fig.5showsthedistribution
oftheerrornormalizedwithrespecttothearc-lengthfor100
randomly selected unseen actuation inputs. The Euclidean
distance error for each point along the backbone was nor-
malized by the arc-length s. Since the length of the CTR,
ℓ ,variesbasedonβ ,thearc-lengthaxiswasnormalizedby
1 1
ℓ . The results indicate that the PINN estimated the shape
1
with an error margin of less than 1% along the body of
the robot, and a maximum error of less than 2.5%, closely
matching the Cosserat rod model.
Fig. 6 shows the states predicted by the
trained PINN and the solution of the Cosserat
rod model for an unseen actuation input
τ =[ 0.032, 0.023, 0.005, 2.49, 0.32, 1.52]. The
− − − − − −
results demonstrate that the PINN accurately predicts the
]mm[
P
States
x z
y
2
0
2
−
]m.N[
bm
×
10− 7
x y
2.5
0.0
2.5
−
]m/1[
zU
tube1 tube2 tube3
2
1
0
]dar[
θ tube1 tube2 tube3
0
1
−
0 25 50 75 100 125 150 175
s[mm]
noinretauQ
x z
y w
Fig. 6. States estimations of the PINN (dashed lines) and the Cosserat
rodmodel(solidlines-notmentionedinthelegends)vs.arc-lengthfora
randomactuationinput.
states of the CTR along its backbone. Since the modeling
assumes free space, mb , representing the bending moment
x,y
of the composite tubes, is expected to be zero, which is
accurately estimated by the PINN. Therefore, for the sake
of brevity in the free-motion case, mb could be removed
x,y
fromthestatevector.Additionally,θ ,representingthetwist
1
oftube1withrespecttoitself,isalwayszeroandcouldalso
be removed from the state vector. However, in this work,
we retain the full state representation for completeness.
B. Trained using Experimental Observations Dataset
Fig. 7 shows the backbone shapes for six randomly se-
lected actuation inputs estimated by the pretrained PINN as
describedinIV-Aandadditionallytrainedusing500random
experimental observation data points from [20]. The colored
scatter points represent the experimental position measure-
ments of the terminal points of the three tubes. Fig. 8 shows
the distribution of position errors and normalized position
errors at the terminal points for the PINN and Cosserat
models across 2000 unseen randomly selected samples from
[20]. As can be seen in Fig. 7, the shape reconstruction
using the Cosserat rod exhibits slight deviations from the
experimental measurements due to mismatches in the cal-
ibrated Cosserat rod model and the physical CTR setup.

|     |     |     |     |     |      |        |     |     | PINN |     |     |     | Cosserat |     |     |
| --- | --- | --- | --- | --- | ---- | ------ | --- | --- | ---- | --- | --- | --- | -------- | --- | --- |
|     |     |     |     |     | Base | Expt‘3 | 3.0 |     |      |     |     |     |          |     |     |
1000
|     |     |     |     |     | PINN | Expt‘2 |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2.0
|     |     |     |     |     | Cosserat | Expt‘1 |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
]sm[emit
10
0
1.0
|     |     |     |     |     |     | 20  | 0.6 |     |     |     | 0.1 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
−
0.4
|     |     |     |     |     |     | 40 m] |     | 30  | 60  | 90 150 |     | 30  | 60  | 90  | 150 |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
− m
|     |     |     |     |     |     |     |     | #backbonepoints |     |     |     | #backbonepoints |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --------------- | --- | --- | --- |
[
y
60
|     |     |     |     |     |     | −   | Fig. 9. | Runtime | of the | PINN and | Cosserat | rod model | for | 5,000 | random |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | ------ | -------- | -------- | --------- | --- | ----- | ------ |
actuations.
|     | 0   |     |     |     |     | 80  |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
−
40
|     |     |     |     |     |     |     | mode      | with | GCC 13.3.0 | using         | -O3 | optimizations, |        | and   | ex- |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---- | ---------- | ------------- | --- | -------------- | ------ | ----- | --- |
| z   | 80  |     |     |     | 40  |     |           |      |            |               |     |                |        |       |     |
|     | [m  |     |     |     | 20  |     |           |      |            |               |     |                | Intel® |       |     |
|     |     | 120 |     | 0   |     |     | periments | were | run on     | a workstation |     | with           | an     | Core™ |     |
|     | m   |     | 20  |     |     |     |           |      |            |               |     |                |        |       |     |
] − x[mm] i9-10940X CPU and 256 GB RAM with isolated cores and
|     |     |     |     |     |     |     | CPU | affinity | (via isolcpus |     | and | taskset). |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------------- | --- | --- | --------- | --- | --- | --- |
Fig. 7. Shape estimation of the PINN, the Cosserat rod model, and Simulations were performed for four backbone discretiza-
experimentalmeasurementsoftheterminalpointsofthetubes.ThePINN tions. While the median runtimes of the PINN and the
wastrainedusing500experimentalobservationdatapoints.
|     |     |            |     |     |       |     | Cosserat  | rod       | model               | do not | show     | a remarkable |         | difference, |      |
| --- | --- | ---------- | --- | --- | ----- | --- | --------- | --------- | ------------------- | ------ | -------- | ------------ | ------- | ----------- | ---- |
|     |     |            |     |     |       |     | their     | variation | significantly       |        | differs. | PINN         | shows   | negligible  |      |
|     |     | Error [mm] |     |     | Error | %s  |           |           |                     |        |          |              |         |             |      |
|     |     |            |     |     |       |     | variation | across    | all configurations, |        |          | whereas      | the     | Cosserat    | rod  |
|     |     |            |     | 10  |       |     | model     | shows     | a substantial       |        | increase | in           | spread. | The         | PINN |
10 runtime is almost insensitive to the actuation and arc-length,
sinceeachevaluationisaforwardpassoftheMLP.However,
1
| 1   |     |     |     |     |     |     | the       | Cosserat | solver         | employs | a           | shooting | method | that         | is  |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------- | -------------- | ------- | ----------- | -------- | ------ | ------------ | --- |
|     |     |     |     |     |     |     | sensitive | to       | both actuation |         | and initial | guess    | at     | the proximal |     |
0.1
|     |      |     |     |     |      |     | boundary. | The | number | of  | iterations | required |     | to converge |     |
| --- | ---- | --- | --- | --- | ---- | --- | --------- | --- | ------ | --- | ---------- | -------- | --- | ----------- | --- |
| 0.1 | PINN |     |     |     | PINN |     |           |     |        |     |            |          |     |             |     |
Cosserat Cosserat can vary widely, resulting in a broad range of computation
times,sometimesexceedingtheupperboundobservedforthe
|     | ‘3  | ‘2  | ‘1  |     | ‘3  | ‘2 ‘1 |         |        |              |       |                   |     |         |           |       |
| --- | --- | --- | --- | --- | --- | ----- | ------- | ------ | ------------ | ----- | ----------------- | --- | ------- | --------- | ----- |
|     |     |     |     |     |     |       | PINN    | (e.g., | high torsion | or    | large actuations) |     | and     | sometimes |       |
|     |     |     |     |     |     |       | falling | below  | its lower    | bound | (e.g.,            | low | torsion | or        | small |
Fig.8. Errordistributionsatthedistalterminalpointsofthetubes.Left:
Euclidean distance error. Right: Euclidean error normalized by tube arc- actuations). Consequently, PINN provides more consistent
length.BothpanelscomparePINNandCosseratestimations. runtime, which is essential for real-time applications.
D. Limitations
In contrast, estimations of the PINN at the terminal points The proposed approach demonstrates superior perfor-
aligncloselywiththeexperimentaldatawhileestimatingthe
manceintermsofbothaccuracyandruntimewhencompared
overall shape. This results in an average position estimation to the Cosserat rod model. However, it is limited to con-
error of less than 1% of the arc-length. figurations that yield unique solutions, making it unsuitable
It is important to note that among the 2,000 randomly for capturing snapping behavior. Future work will aim to
selected datapoints from [20], five samples exhibiting re- address this limitation by implementing a multi-agent PINN
| markably | high | errors | at the | tip positions, | both | for the PINN |               |     |                |     |        |         |         |     |        |
| -------- | ---- | ------ | ------ | -------------- | ---- | ------------ | ------------- | --- | -------------- | --- | ------ | ------- | ------- | --- | ------ |
|          |      |        |        |                |      |              | architecture. |     | Also, although |     | a very | limited | dataset | is  | suffi- |
andCosseratmodels,wereexcludedfromtheerrorplot.Itis cientfortraining,thistrainingprocessistime-consumingand
believedthatthesesampleswereoutliersintheexperimental must be conducted for each specific CTR parameter design.
dataset,likelyduetomeasurementerrorsorunexpectedrobot
|     |     |     |     |     |     |     | Future | work | will address |     | this limitation |     | by  | developing | a   |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---- | ------------ | --- | --------------- | --- | --- | ---------- | --- |
behavior, such as snapping. foundational model that can adapt to a variety of CTR
|            |     |      |     |     |     |     | designs | rather | than just | one. |     |     |     |     |     |
| ---------- | --- | ---- | --- | --- | --- | --- | ------- | ------ | --------- | ---- | --- | --- | --- | --- | --- |
| C. Runtime |     | Time |     |     |     |     |         |        |           |      |     |     |     |     |     |
Fig. 9 shows the runtimes of the PINN and the Cosserat V. CONCLUSIONS
rod model over 5,000 random actuation inputs. The PINN In this work, we propose a PINN to model the kinematic
wasimplementedinC++usingLibTorch,andtheCosserat of a three-tube CTR in free space. The PINN integrates the
model was implemented in C++ with a Shooting-based Cosserat rod differential equations and boundary conditions,
BVPsolverthatusesan8th orderAdams-Bashforth-Moulton together with a very small dataset of only 500 experimental
integrator from the Boost library coupled with a modified observations of the distal tip of the CTR, to learn the
Newton-Raphson method. All code was built in Release mapping from actuation to the full latent state, including

the backbone shape. Simulation results showed an average [19] R. Grassmann and J. Burgner-Kahrs, “On the merits of joint space
shape error of less than 1% along the backbone, and the and orientation representations in learning the forward kinematics in
se(3).,”inRobotics:ScienceandSystems,2019.
experimental results using the dataset in [20] showed that
[20] R. M. Grassmann, R. Z. Chen, N. Liang, and J. Burgner-Kahrs, “A
the mean position error is below 1% at the terminal points datasetandbenchmarkforlearningthekinematicsofconcentrictube
of the three tubes. Furthermore, the proposed approach continuum robots,” in 2022 IEEE/RSJ International Conference on
IntelligentRobotsandSystems,pp.9550–9557,IEEE,2022.
couldenhanceruntimeefficiencycomparedtothetraditional
[21] A. Kuntz, A. Sethi, R. J. Webster, and R. Alterovitz, “Learning the
Cosserat rod model, making it more suitable for real-time complete shape of concentric tube robots,” IEEE Transactions on
control and planning. MedicalRoboticsandBionics,vol.2,no.2,pp.140–147,2020.
[22] N. Liang, R. M. Grassmann, S. Lilge, and J. Burgner-Kahrs,
“Learning-basedinversekinematicsfromshapeasinputforconcentric
REFERENCES
tube continuum robots,” in 2021 IEEE International Conference on
RoboticsandAutomation,pp.1387–1393,IEEE,2021.
[1] P. E. Dupont, N. Simaan, H. Choset, and C. Rucker, “Continuum
[23] G.JeongandS.Y.Ko,“Learning-basedkinematicmodelingforcon-
robotsformedicalinterventions,”ProceedingsoftheIEEE,vol.110,
centrictuberobot:Addressingitsnonlinearityandsnappingbehavior,”
no.7,2022.
IEEERoboticsandAutomationLetters,2025.
[2] J. Burgner-Kahrs, D. C. Rucker, and H. Choset, “Continuum robots
[24] N. Feizi, F. C. Pedrosa, J. Jayender, and R. V. Patel, “Deep Koop-
formedicalapplications:Asurvey,”IEEETransactionsonRobotics,
man approach for nonlinear dynamics and control of tendon-driven
vol.31,no.6,2015.
continuumrobots,”IEEERoboticsandAutomationLetters,2025.
[3] C. J. Nwafor, C. Girerd, G. J. Laurent, T. K. Morimoto, and
[25] M. Bensch, T.-D. Job, T.-L. Habich, T. Seel, and M. Schappler,
K. Rabenorosoa, “Design and fabrication of concentric tube robots:
“Physics-informed neural networks for continuum robots: Towards
Asurvey,”IEEETransactionsonRobotics,vol.39,no.4,pp.2510–
fast approximation of static Cosserat rod theory,” in 2024 IEEE
2528,2023.
International Conference on Robotics and Automation, pp. 17293–
[4] Z. Mitros, S. H. Sadati, R. Henry, L. Da Cruz, and C. Bergeles,
17299,IEEE,2024.
“Fromtheoreticalworktoclinicaltranslation:Progressinconcentric
[26] M. Raissi, P. Perdikaris, and G. E. Karniadakis, “Physics-informed
tube robots,” Annual Review of Control, Robotics, and Autonomous
neuralnetworks:Adeeplearningframeworkforsolvingforwardand
Systems,vol.5,no.1,pp.335–359,2022.
inverse problems involving nonlinear partial differential equations,”
[5] K.Price,J.Peine,M.Mencattelli,Y.Chitalia,D.Pu,T.Looi,S.Stone,
JournalofComputationalPhysics,vol.378,pp.686–707,2019.
J.Drake,andP.E.Dupont,“Usingroboticstomoveaneurosurgeon’s
[27] J. Nicodemus, J. Kneifl, J. Fehr, and B. Unger, “Physics-informed
handstothetipoftheirendoscope,”ScienceRobotics,vol.8,no.82,
neuralnetworks-basedmodelpredictivecontrolformulti-linkmanip-
p.eadg6042,2023.
ulators,”IFAC-PapersOnline,vol.55,no.20,pp.331–336,2022.
[6] J. Burgner, D. C. Rucker, H. B. Gilbert, P. J. Swaney, P. T. Russell,
[28] J. Liu, P. Borja, and C. Della Santina, “Physics-informed neural
K.D.Weaver,andR.J.Webster,“Ateleroboticsystemfortransnasal
networkstomodelandcontrolrobots:Atheoreticalandexperimental
surgery,” IEEE/ASME Transactions on Mechatronics, vol. 19, no. 3,
investigation,”AdvancedIntelligentSystems,vol.6,no.5,p.2300385,
pp.996–1006,2014.
2024.
[7] N. Feizi, F. C. Pedrosa, R. Zhang, D. Sacco, R. V. Patel, and
[29] G. E. Karniadakis, I. G. Kevrekidis, L. Lu, P. Perdikaris, S. Wang,
J.Jayender,“Designandvalidationofacompactconcentric-tuberobot
and L. Yang, “Physics-informed machine learning,” Nature Reviews
forpercutaneousnephrolithotomy,”AuthoreaPreprints,2025.
Physics,vol.3,no.6,pp.422–440,2021.
[8] J. B. Gafford, S. Webster, N. Dillon, E. Blum, R. Hendrick, F. Mal-
[30] R. Xu, S. F. Atashzar, and R. V. Patel, “Kinematic instability
donado, E. A. Gillaspie, O. B. Rickman, S. D. Herrell, and R. J.
in concentric-tube robots: Modeling and analysis,” in 5th IEEE
WebsterIII,“Aconcentrictuberobotsystemforrigidbronchoscopy:
RAS/EMBS International Conference on Biomedical Robotics and
a feasibility study on central airway obstruction removal,” Annals of
Biomechatronics,pp.163–168,IEEE,2014.
BiomedicalEngineering,vol.48,no.1,pp.181–191,2020.
[31] H.B.Gilbert,R.J.Hendrick,andR.J.WebsterIII,“Elasticstability
[9] F. C. Pedrosa, N. Feizi, R. Zhang, R. Delaunay, D. Sacco, J. Ja-
ofconcentrictuberobots:Astabilitymeasureanddesigntest,”IEEE
gadeesan, and R. Patel, “On surgical planning of percutaneous
TransactionsonRobotics,vol.32,no.1,pp.20–35,2015.
nephrolithotomy with patient-specific CTRs,” in International Con-
[32] S. Wang, Y. Teng, and P. Perdikaris, “Understanding and mitigating
ference on Medical Image Computing and Computer-Assisted Inter-
gradientflowpathologiesinphysics-informedneuralnetworks,”SIAM
vention,pp.626–635,Springer,2022.
Journal on Scientific Computing, vol. 43, no. 5, pp. A3055–A3081,
[10] S.S.Antman,NonlinearProblemsofElasticity. Springer,2005.
2021.
[11] D. C. Rucker, B. A. Jones, and R. J. Webster III, “A geometrically
[33] N.Rahaman,A.Baratin,D.Arpit,F.Draxler,M.Lin,F.Hamprecht,
exactmodelforexternallyloadedconcentric-tubecontinuumrobots,”
Y.Bengio,andA.Courville,“Onthespectralbiasofneuralnetworks,”
IEEETransactionsonRobotics,vol.26,no.5,pp.769–780,2010.
in International Conference on Machine Learning, pp. 5301–5310,
[12] D. C. Rucker, R. J. Webster III, G. S. Chirikjian, and N. J. Cowan,
PMLR,2019.
“Equilibriumconformationsofconcentric-tubecontinuumrobots,”The
[34] D. C. Liu and J. Nocedal, “On the limited memory bfgs method for
InternationalJournalofRoboticsResearch,vol.29,no.10,pp.1263–
largescaleoptimization,”MathematicalProgramming,vol.45,no.1,
1280,2010.
pp.503–528,1989.
[13] P.E.Dupont,J.Lock,B.Itkowitz,andE.Butler,“Designandcontrol
[35] D. P. Kingma and J. Ba, “Adam: A method for stochastic opti-
of concentric-tube robots,” IEEE Transactions on Robotics, vol. 26,
mization,” in International Conference on Learning Representations
no.2,pp.209–225,2010.
(ICLR),2014.
[14] D. C. Rucker, B. A. Jones, and R. J. Webster III, “A geometrically
[36] J.F.Urba´n,P.Stefanou,andJ.A.Pons,“Unveilingtheoptimization
exactmodelforexternallyloadedconcentric-tubecontinuumrobots,”
processofphysicsinformedneuralnetworks:Howaccurateandcom-
IEEETransactionsonRobotics,vol.26,no.5,pp.769–780,2010.
petitivecanPINNsbe?,”JournalofComputationalPhysics,vol.523,
[15] H. B. Keller, Numerical Methods for Two-Point Boundary-Value
p.113656,2025.
Problems. CourierDoverPublications,2018.
[37] X.GlorotandY.Bengio,“Understandingthedifficultyoftrainingdeep
[16] G. Niu, Y. Zhang, and W. Li, “Path planning of continuum robot
feedforwardneuralnetworks,”inProceedingsoftheThirteenthInter-
based on path fitting,” Journal of Control Science and Engineering,
nationalConferenceonArtificialIntelligenceandStatistics,pp.249–
vol.2020,no.1,p.8826749,2020.
256,JMLRWorkshopandConferenceProceedings,2010.
[17] C.Legaard,T.Schranz,G.Schweiger,J.Drgonˇa,B.Falay,C.Gomes,
A. Iosifidis, M. Abkar, and P. Larsen, “Constructing neural network
based models for simulating dynamical systems,” ACM Computing
Surveys,vol.55,no.11,pp.1–34,2023.
[18] R.Grassmann,V.Modes,andJ.Burgner-Kahrs,“Learningtheforward
andinversekinematicsofa6-dofconcentrictubecontinuumrobotin
se (3),” in IEEE/RSJ International Conference on Intelligent Robots
andSystems,pp.5125–5132,IEEE,2018.