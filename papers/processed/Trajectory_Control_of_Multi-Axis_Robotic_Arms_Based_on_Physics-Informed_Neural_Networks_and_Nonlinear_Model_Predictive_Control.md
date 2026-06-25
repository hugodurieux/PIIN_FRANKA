Trajectory Control of Multi-Axis Robotic Arms
Based on Physics-Informed Neural Networks and
Nonlinear Model Predictive Control
1st Yiqing Wang 2nd Changqing Xia
School of Automation and Electrical Engineering State Key Laboratory of Robotics
Shenyang Ligong University Shenyang Institute of Automation
Shenyang, China Chinese Academy of Sciences
State Key Laboratory of Robotics Shenyang, China
Shenyang Institute of Automation Key Laboratory of Networked Control Systems
Chinese Academy of Sciences Chinese Academy of Sciences
Shenyang, China Shenyang, China
Key Laboratory of Networked Control Systems xiachangqing@sia.cn
Chinese Academy of Sciences
Shenyang, China
wyq1597762375@163.com
3rd Xi Jin 4th Chi Xu 5th Yanzhu Zhang
State Key Laboratory of Robotics State Key Laboratory of Robotics School of Automation
Shenyang Institute of Automation Shenyang Institute of Automation and Electrical Engineering
Chinese Academy of Sciences Chinese Academy of Sciences Shenyang Ligong University
Shenyang, China Shenyang, China Shenyang, China
Key Laboratory of Networked Control Systems Key Laboratory of Networked Control Systems syzd710471@163.com
Chinese Academy of Sciences Chinese Academy of Sciences
Shenyang, China Shenyang, China
jinxi@sia.cn xuchi@sia.cn
Abstract—Multi-axis robotic arms are extensively utilized in [1] play an increasingly important role in modern industry.
intelligent manufacturing scenarios, with trajectory control in In such applications,the trajectory control [2] ofrobotic arms
flexible scenarios constituting a primary challenge. Physics- directlyaffectstheprecision,speed,andstabilityofoperations.
InformedNeuralNetworks(PINNs)representadvancedmethods
Traditional Proportional-Integral-Derivative (PID) [3] control
thatintegratephysicallawswithdata-drivenapproaches.Despite
their outstanding performance in integrating theory and data, methods are simple and easy to implement, and they were
research on their application for controlling robotic arms in widelyusedinearlyindustrialapplications.However,astasks
complex scenarios remains limited. This paper establishes a becomemorecomplex,PIDcontrolmethodsshowlimitations
nonlinear dynamic model based on the physical relationships
in handling nonlinear dynamic characteristics, model uncer-
between the axes of robotic arms. In the absence of prior data,
tainties, and local disturbances. Therefore, researchers have
Sobol sequence random sampling is employed to generate data,
whicharesubsequentlytrainedusingPINNs.Consideringsystem exploredintelligentcontrolmethods[4][5],whichcanhandle
noise,theExtendedKalmanFilter(EKF)isutilizedtopredictthe thecomplexitiesofnonlineardynamicsystems.Amongthese,
nextstateinnoisyenvironments,andNonlinearModelPredictive Model Predictive Control (MPC) [6] [7] has been extensively
Control (NMPC) is implemented to control the robotic arm
studied for its ability to optimize control inputs in real-
for trajectory tracking, achieving real-time control. Simulation
time, providing a significant advantage for complex dynamic
resultsdemonstratethattheproposedDiscretePhysics-Informed
PredictiveControl(DPIPC)methodexhibitssmallerpositionand system control. Nonlinear Model Predictive Control (NMPC)
velocity errors with less fluctuation compared to the method in [8] is an extension of MPC that can handle nonlinearities and
the reference, indicating superior control capabilities. system uncertainties, making it suitable for improving control
Index Terms—Robotic arm, PINNs, EKF, NMPC accuracy and stability. The Extended Kalman Filter (EKF) is
awidelyusedestimationalgorithminNMPCtoimprovestate
I. INTRODUCTION
estimation accuracy and system stability. However, NMPC
With the rapid development of industrial automation and faces significant challenges in obtaining accurate models and
intelligent manufacturing technology, multi-axis robotic arms real-time computational efficiency. Inaccurate models may
979-8-3503-6860-4/24/$31.00 ©2024 IEEE 4618
37646801.4202.29836CAC/9011.01
:IOD
|
EEEI
4202©
00.13$/42/4-0686-3053-8-979
|
)CAC(
ssergnoC
noitamotuA
anihC
4202
Authorized licensed use limited to: University of Melbourne. Downloaded on May 04,2026 at 23:19:16 UTC from IEEE Xplore. Restrictions apply.

degrade control performance and potentially cause system Rewriting the dynamic equations, it can be stated that:
instability.UsingneuralnetworkstogenerateNMPCdataisan (cid:6) (cid:7)
q˙
importantapproachtoaddressmodelinaccuracies[9].Physics- x˙ = M(q)−1(Bu−C(q,q˙)q˙ −g(q)+Γω) (2)
| Informed | Neural | Networks |     | (PINNs) | [10] | combine | physical |     |     |     |     |     |     |     |     |
| -------- | ------ | -------- | --- | ------- | ---- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
models and data-driven methods, offering significant advan- x˙ = f(x,u),
|     |     |     |     |     |     |     |     | Define |     |     | the original | dynamic | equation |     | trans- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | ------------ | ------- | -------- | --- | ------ |
tages over traditional neural networks. PINNs incorporate forms into a set of ordinary differential equations (ODEs).
physical laws into the loss function, improving training effi- However, after establishing the state-space equations, it is
ciencyandmodelaccuracy,andeffectivelyhandlingboundary
|     |     |     |     |     |     |     |     | necessary | to make | some | reasonable |     | assumptions | about | the |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ------- | ---- | ---------- | --- | ----------- | ----- | --- |
conditions and other physical constraints [11]. variables to ensure that the model conforms more closely to
This paper combines PINNs, EKF, and NMPC to propose mathematical and physical logic.
a new solution for multi-axis robotic arm trajectory control, This section has established the model for the robotic arm.
namedDiscretePhysics-InformedPredictiveControl(DPIPC). Inthenextsection,thispaperwillpresentspecificmethodsto
Basedonexperimentalresults,thisintegratedmethodnotonly address the trajectory tracking control problem for multi-axis
|              |             |           |                |            |        |         |             | robotic arms. |                                    |     |     |     |     |     |     |
| ------------ | ----------- | --------- | -------------- | ---------- | ------ | ------- | ----------- | ------------- | ---------------------------------- | --- | --- | --- | --- | --- | --- |
| enhances     | the         | accuracy  | and            | stability  | of the | control | system      |               |                                    |     |     |     |     |     |     |
| but also     | strengthens | the       | system’s       | robustness |        | against | unknown     |               |                                    |     |     |     |     |     |     |
|              |             |           |                |            |        |         |             | III.          | DISCRETEPHYSICS-INFORMEDPREDICTIVE |     |     |     |     |     |     |
| disturbances |             | and model | uncertainties. |            | It has | broad   | application |               |                                    |     |     |     |     |     |     |
CONTROL
| prospects | and | research | value. |     |     |     |     |     |     |     |     |     |     |     |     |
| --------- | --- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The remaining sections of this paper are organized as To achieve precise trajectory control of multi-axis robotic
follows:SectionIIestablishesthemodelandcontrolobjectives arms in intelligent manufacturing environments, this sec-
|         |         |           |     |         |            |     |             | tion proposes | an  | integrated | method |     | under the | premise | of  |
| ------- | ------- | --------- | --- | ------- | ---------- | --- | ----------- | ------------- | --- | ---------- | ------ | --- | --------- | ------- | --- |
| for the | robotic | arm based | on  | dynamic | equations. |     | Section III |               |     |            |        |     |           |         |     |
introduces the guidance and control design of DPIPC, com- data scarcity and the presence of noise, combining Discrete
bining PINNs, EKF, and NMPC. Section IV sets parameters Physics-Informed Neural Networks (Discrete PINNs) and
|     |     |     |     |     |     |     |     | Nonlinear | Model | Predictive | Control | (NMPC), |     | referred | to as |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ----- | ---------- | ------- | ------- | --- | -------- | ----- |
andconductsexperimentsaccordingtothedesignedalgorithm,
comparing the results with those obtained using the method DiscretePhysics-InformedPredictiveControl(DPIPC).PINNs
described in the literature [12]. Finally, Section V provides areutilizedformodelingthedynamicequationsandgenerating
|             |     |               |     |     |     |     |     | control strategies, |           | while       | the Extended | Kalman   | Filter | (EKF)     | is  |
| ----------- | --- | ------------- | --- | --- | --- | --- | --- | ------------------- | --------- | ----------- | ------------ | -------- | ------ | --------- | --- |
| conclusions |     | and analysis. |     |     |     |     |     |                     |           |             |              |          |        |           |     |
|             |     |               |     |     |     |     |     | employed            | for state | estimation. |              | Finally, | NMPC   | processes | the |
II. MODELESTABLISHMENT generated states, achieving accurate trajectory tracking.
| With | the continuous |     | advancement |     | of industrial |     | automation, | A. Discrete | PINNs |     |     |     |     |     |     |
| ---- | -------------- | --- | ----------- | --- | ------------- | --- | ----------- | ----------- | ----- | --- | --- | --- | --- | --- | --- |
multi-axisroboticarmsarerequiredtooperateinenvironments In scenarios lacking prior data, traditional neural networks
with significant noise and external disturbances. Ensuring the may not provide sufficient accuracy and robustness, whereas
| speed | control | performance | and | stability |     | of robotic | arms | in  |     |     |     |     |     |     |     |
| ----- | ------- | ----------- | --- | --------- | --- | ---------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
theapplicationofPINNscanfacilitateprecisedynamicmodel-
suchcomplexenvironmentshasbecomeakeyfocusofcurrent ingandcontrol.However,duetotherelativelyslowmovement
research. This section focuses on the trajectory control of speed of robotic arms, using conventional PINNs may lead
multi-axis robotic arms in noisy environments, establishing a to insufficient computational accuracy. The Discrete PINNs
modelfortheroboticarmbasedonmodificationstothemodel can effectively meet the needs for modeling the dynamic
presented in the literature [12]. equations of robotic arms, generating control strategies, and
Consider the state-space equations of a general control ensuringstateestimationaccuracy.Thismethodfocusesonthe
system: discretizedphysicalsystem,applyingphysicallawstodiscrete
|     |     |     |     |     |     |     |     | time steps, | making | it more | suitable | for | handling | discrete-time |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ------ | ------- | -------- | --- | -------- | ------------- | --- |
M(q)q¨+C(q,q˙)q˙ +g(q)=Bu+Γω (1) dynamic systems. It not only maintains the continuity of sys-
temdynamicsbutalsomanagescomplexsystemdynamicsand
| Where | M(q) | is the | inertia | matrix | (n×n), | C(q,q˙) | is the |     |     |     |     |     |     |     |     |
| ----- | ---- | ------ | ------- | ------ | ------ | ------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
constraints,providingrobustandefficientcontrolperformance.
(n×n),
Coriolis force matrix g(q) is the gravitational vector Before using Discrete PINNs to handle the dynamic equa-
| (n×1), |                |              |               |     |             |        | (n×        |              |              |         |           |            |          |         |        |
| ------ | -------------- | ------------ | ------------- | --- | ----------- | ------ | ---------- | ------------ | ------------ | ------- | --------- | ---------- | -------- | ------- | ------ |
|        | B              | is the input | matrix        | of  | the control | system |            |              |              |         |           |            |          |         |        |
|        |                |              |               |     |             |        |            | tions, it    | is necessary | to      | determine | the        | solution | methods | for    |
| m),    | u is typically | the          | joint torques |     | (m×1),      | Γ is   | the matrix |              |              |         |           |            |          |         |        |
|        |                |              |               |     |             |        |            | the matrices | and          | vectors | in the    | equations. | The      | values  | of the |
(n×n),
representing the effect of nonlinear friction ω is the inertia matrix M(q), the Coriolis matrix C(q,q˙), and the
vectorofnonlineardisturbances(n×1),q
isthejointposition
|        |        |           |       |          |        |        |           | gravitational | vector | g(q) | are | determined | by  | the mass | and |
| ------ | ------ | --------- | ----- | -------- | ------ | ------ | --------- | ------------- | ------ | ---- | --- | ---------- | --- | -------- | --- |
| vector | (n×1), | q˙ is the | joint | velocity | vector | (n×1), | q¨ is the |               |        |      |     |            |     |          |     |
lengthofeachlink.Assumethelinksareuniformrods.Denote
|     |     |     | (n×1). |     | n   |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
joint acceleration vector Here, is the number of m asthemassofthei-thlink,l asthelengthofthei-thlink,
|        |              |            |           |        |         |          |          | i                              |     |     |     | i                           |     |     |     |
| ------ | ------------ | ---------- | --------- | ------ | ------- | -------- | -------- | ------------------------------ | --- | --- | --- | --------------------------- | --- | --- | --- |
| joints | or degrees   | of freedom |           | of the | robotic | arm, and | m is the |                                |     |     |     |                             |     |     |     |
|        |              |            |           |        |         |          |          | q i astheangleofthei-thjoint,q |     |     |     | j astheangleofthej-thjoint, |     |     |     |
| number | of actuators |            | or inputs | to the | system. |          |          |                                |     |     |     |                             |     |     |     |
(cid:15) (cid:16) (cid:15) (cid:16) q˙ as the angular velocity of the i-th joint, q˙ as the angular
|     |     |     |     |     | (cid:2) |     | (cid:2) | i   |     |     |     |     | j   |     |     |
| --- | --- | --- | --- | --- | ------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
Definethesta tevariablex= q q˙ ,thenx˙ = q˙ q¨ . velocity of the j-th joint, and g as the gravitational constant
|     |     | (cid:15) |     | (cid:16) |     |     |     |     |            |     |     |     |     |     |     |
| --- | --- | -------- | --- | -------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
|     |     |          | ··· | (cid:2)  |     |     |     |     | 9.81m/s2). |     |     |     |     |     |     |
Consider q = q 1 q 2 q n , and assume the matrix (approximately The specific calculation formulas
M(q) is positive semi-definite. are as follows (where n is the number of robotic arm axes):
4619
Authorized licensed use limited to: University of Melbourne. Downloaded on May 04,2026 at 23:19:16 UTC from IEEE Xplore.  Restrictions apply.

The inertia matrix M(q): The physical loss is defined as follows:
(cid:31) +
M(q)=diag m
n
1 l 1 2 ,..., m
n
n l n 2 (3) L
phys
=
N
1 N(cid:21)phys+ + +M(q∗(i))q¨∗ (i)+C(q∗(i),q˙∗ (i))q˙∗ (i)
phys i=1 +
The Coriolis force matrix C(q,q˙): +2
(cid:11) +g(q∗(i))−Γω−Bu(t i ) + +
C (q,q˙)= −0.5m i l i l j (q˙ i +q˙ j )·sin(q i −q j ), i(cid:7)=j 2 (9)
ij
0, i=j
Here, i represents the i-th data point in the sample dataset,
(4) N represents the number of samples, and (cid:8)·(cid:8)2 denotes the
2
The gravitational vector g(q):
Euclidean norm squared.
(cid:2) Therefore, the total loss function is:
g(q)=(m gl cos(q ),...,m gl cos(q )) (5)
1 1 1 n n n
L=αL +βL (10)
To discretize Equation (1), various numerical methods are data phys
commonly used for solving the dynamic equations of robotic Here, α and β are weighting factors used to balance the
arms, including the Euler Method, Runge-Kutta Methods, influence of data loss and physical loss, respectively, and are
Finite Element Method (FEM), and Trapezoidal Method. In set according to different scenarios.
ordertoeffectivelyhandlethedynamicchangesofthesystem After initializing the neural network model, the optimizer
in actual robotic arm control and ensure the stability of the is determined. This paper chooses the Adam optimizer for
control process, this study chooses the Trapezoidal Method. trainingandfine-tuningthe(cid:15)networ(cid:16)k.Foreachtrainingperiod,
(cid:2)
The Trapezoidal Method is a second-order numerical integra- the state variable x = q q˙ needs to be predicted
tion method that provides more accurate numerical solutions first, and then all variables are determined. Next, L and
data
compared to the improved Euler Method. L are calculated, and the neural network loss function
phys
Assume the sampling period (step size) is Δt, the to- is propagated backward to update the network parameters.
(cid:15)tal number (cid:16)of step(cid:15)s is n,(cid:16)and the initial state is x(0) = According to the calculated gradient, the optimizer updates
(cid:2) (cid:2)
q(0) q˙(0) = q q˙ . Using the trapezoidal method themodelparametersiterativelytominimizethelossfunction.
0 0
to solve the system, the predicted values q∗ and q˙∗ are The supervised tra(cid:15)ining process(cid:16)of the loss function outputs
n+1 n+1 (cid:2)
calculated as follows: the state x n+1 = q n+1 q˙ n+1 .
q∗ =q +Δt·q˙ , B. Extended Kalman Filter and Nonlinear Model Predictive
n+1 n (cid:22)n
q˙∗ =q˙ +Δt· M(q )−1(Bu −C(q ,q˙ )q˙ (6) Control
n+1 n n n n n n
−g(q )+Γω )) After establishing the PINNs model and performing initial
n n
stateprediction,tofurtherimprovetheaccuracyandrobustness
Using the trapezoidal method to correct the predicted val-
of the model, this section employs EKF for state estima-
ues and update the original state, the following equation is
tion and designs the NMPC algorithm to perform trajectory
obtained:
(cid:22) (cid:23) tracking for the given references. To simplify notation and
Δt
q˙ =q˙ + q˙ +q˙∗ (7) distinguishdifferenttimesteps,thevariablenisreplacedwith
n+1 n 2 n n+1
(cid:15) (cid:16) ktorepresentthetimestepintheKalmanfilter.Thisapproach
(cid:2)
The new state x = q q˙ . Thus, the dy- helps avoid confusion since n is typically used to denote the
n+1 n+1 n+1
namics equation has been discretized using the trapezoidal number of samples or total steps, while k directly indicates
method to obtain the predicted position and velocity. For this the current time step in the filtering process. Specifically,
robotic arm, the physical model is relatively accurate, but k represents the current time step used for predicting and
there is limited known data. Therefore, PINNs can be used updating state estimates.
for training. Using the known data from the literature, initial 1) Extended Kalman Filter: The design of the Kalman
dataforpositionq,velocityq˙,timet,andcontrolinputucan filter primarily involves two processes: prediction and update.
be obtained. After obtaining the initial data, a PINNs model Introducing the measurement equation z k = h(x k ) + v k ,
is established. A multi-layer perceptron (MLP) network is where z k is the observation, h is the measurement function,
designed,consistingofseveralhiddenlayers,eachwithseveral and v k is the measurement noise, which follows a Gaussian
neurons. The loss function of the model is defined from two distribution with zero mean.
aspects: data loss and physical loss. Data loss is mainly used Prediction process:
to balance the difference between the predicted values and Usingthestateequationtopredictthestateatthenexttime
actual measured data. In this paper, the data loss is defined as step:
follows: xˆ k+1|k =f(xˆ k ,u k )+ν k , ν k ∼N(0,Q) (11)
L = 1
N(cid:21)
data
(cid:27)
(cid:8)q∗(i)−q (i)(cid:8)2+(cid:8)q˙∗ (i)−q˙ (i)(cid:8)2
(cid:28)
where ν k is the process noise in the prediction process, Q is
data N data i=1 data 2 data 2 the process noise covariance matrix, and f is the system state
(8) update function.
4620
Authorized licensed use limited to: University of Melbourne. Downloaded on May 04,2026 at 23:19:16 UTC from IEEE Xplore. Restrictions apply.

Since the dynamic equations are nonlinear, a linearized have upper and lower bounds. Combining EKF and NMPC,
Kalman filter cannot be directly used. It is necessary to apply the EKF provides the predicted state xˆ for the next time
k+1|k
a Jacobian matrix to facilitate state est2imation in the EKF. step, while NMPC solves the optimization problem to find
f2
Calculate the Jacobian matrix F = ∂ , then the next theoptimalcontrolinputsequenceu∗ ={u ,u ,...,u }.
|     |     |     |     |     | ∂ x | xˆk,uk |     |     |     |     |     |     | 0   | 1   | L−1 |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
step of the covariance matrix is: The control input used as the system input is the one that
(cid:2) mostcloselymatchesthereferencetrajectorypredictedbythe
|     |     |     | P =FP |     | F +Q |     | (12) |     |     |     |     |     |     |     |     |
| --- | --- | --- | ----- | --- | ---- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
k+1|k k PINNs, compared to the first value in the optimal sequence
u∗(0).ThisapproachensuresthattheEKFismoreaccurately
| where | P is | the state | covariance |     | matrix | at the | current time |     |     |     |     |     |     |     |     |
| ----- | ---- | --------- | ---------- | --- | ------ | ------ | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
k
| step.  |          |     |     |     |     |     |     | utilized | for         | the subsequent |        | state estimation. |     |            |     |
| ------ | -------- | --- | --- | --- | --- | --- | --- | -------- | ----------- | -------------- | ------ | ----------------- | --- | ---------- | --- |
|        |          |     |     |     |     |     |     |          | The overall | control        | system | architecture      | of  | this paper | is  |
| Update | process: |     |     |     |     |     |     |          |             |                |        |                   |     |            |     |
showninFigure1,comprisingthreemaincomponents:PINNs,
Usingthemeasurementequationtopredictthemeasurement
| value: |         |            |             |           |     |              |              | EKF, | and NMPC. |     |     |     |     |     |     |
| ------ | ------- | ---------- | ----------- | --------- | --- | ------------ | ------------ | ---- | --------- | --- | --- | --- | --- | --- | --- |
|        | z =h(xˆ | k+1|k      | )+v         | ,         | v   | ∼N(0,R)      | (13)         |      |           |     |     |     |     |     |     |
|        | k+1     |            |             | k+1       | k+1 |              |              |      |           |     |     |     |     |     |     |
| where  | v k+1   | is the     | measurement | noise     | and | R is         | the measure- |      |           |     |     |     |     |     |     |
| ment   | noi2se  | covariance | matrix.     | Calculate |     | the Jacobian | matrix       |      |           |     |     |     |     |     |     |
∂h2
| H = |     | , then | the Kalman |     | gain can | be obtained | as: |     |     |     |     |     |     |     |     |
| --- | --- | ------ | ---------- | --- | -------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∂x xˆk+1|k
|     |     |          | (cid:2) |           |     | (cid:2) +R)−1 |      |     |     |      |     |     |     |      |     |
| --- | --- | -------- | ------- | --------- | --- | ------------- | ---- | --- | --- | ---- | --- | --- | --- | ---- | --- |
|     | K   | =P k+1|k | H       | (HP k+1|k | H   |               | (14) |     |     | PINN |     |     | EKF | NMPC |     |
xˆ
| According   | to  | the              | Kalman | gain, the | state | estimate | k+1 and     |     |     |        |                            |     |     |     |     |
| ----------- | --- | ---------------- | ------ | --------- | ----- | -------- | ----------- | --- | --- | ------ | -------------------------- | --- | --- | --- | --- |
|             |     |                  |        |           |       |          |             |     |     | Fig.1. | ControlSystemArchitecture. |     |     |     |     |
| the updated |     | state covariance |        | matrix    | P     | can be   | updated as: |     |     |        |                            |     |     |     |     |
k+1
|     |     | xˆ  | =xˆ   | +K(z |     | −zˆ ), |     |     |     |     |                       |     |     |     |     |
| --- | --- | --- | ----- | ---- | --- | ------ | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- |
|     |     | k+1 | k+1|k |      | k+1 | k+1    |     |     |     | IV. | EXPERIMENTSANDRESULTS |     |     |     |     |
(15)
P =(I−KH)P
k+1 k+1|k To verify the reliability of the proposed algorithm, this
2) Nonlinear Model Predictive Control Design: In indus- subsection conducted experiments on the established robotic
trial applications of multi-axis robotic arms, precise trajectory arm model, set parameters for PINNs and NMPC, and ran
planning is crucial for executing complex tasks. For example, both the algorithm from the literature [12] and the proposed
in welding, painting, and assembly tasks, the robotic arm algorithm in this environment. Through a detailed analysis of
must follow the predetermined trajectory accurately to ensure the experimental results, conclusions were derived.
| the consistency |       | of            | the processing |          | quality   | and | accuracy. To |     |              |     |           |          |     |     |     |
| --------------- | ----- | ------------- | -------------- | -------- | --------- | --- | ------------ | --- | ------------ | --- | --------- | -------- | --- | --- | --- |
|                 |       |               |                |          |           |     |              | A.  | Experimental |     | Parameter | Settings |     |     |     |
| meet            | these | requirements, | it             | is often | necessary | to  | use complex  |     |              |     |           |          |     |     |     |
trajectoryplanningmethodstodescribethemotionpathsofthe 1) Robotic Arm Parameters: The study considers a 3-DOF
robotic arms. This paper adopts a three-dimensional periodic roboticarmwiththreelinks.Consideringpracticaloperations,
|            |           |     |       |             |     |         |             | the | parameters | are | set as | follows: | the bottom | link | has a |
| ---------- | --------- | --- | ----- | ----------- | --- | ------- | ----------- | --- | ---------- | --- | ------ | -------- | ---------- | ---- | ----- |
| trajectory | approach, |     | which | can achieve |     | complex | and precise |     |            |     |        |          |            |      |       |
motionpathsandissuitableforvariousindustrialapplications. relatively large length and mass, supporting and moving; the
The trajectory is set as follows: middlelinkhasamoderatelengthandmass,usedforauxiliary
⎡ ⎤ movement; and the top link has a smaller length and mass,
cos(θ[kΔt])
⎣ ⎦ mainly for precise operations. Thus, the parameters for the
|     |     | xr ef =p+r |     | sin(θ[kΔt]) |     | +η  | (16) |     |     |     |     |     |     |     |     |
| --- | --- | ---------- | --- | ----------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
k k three links are set as: m 1 = 2, m 2 = 1.5, m 3 = 1, l 1 = 1,
sin(2θ[kΔt])
|       |         |               |     |             |     |                |          | l             | = 0.8, | l = | 0.6. Determining            |     | the range | of generated |     |
| ----- | ------- | ------------- | --- | ----------- | --- | -------------- | -------- | ------------- | ------ | --- | --------------------------- | --- | --------- | ------------ | --- |
|       |         |               |     |             |     |                |          | 2             |        | 3   |                             |     |           |              |     |
|       |         |               |     |             |     |                |          | parameters:−π |        | ≤q  | ≤π,−0.1≤q˙≤0.1,−0.01≤u≤0.01 |     |           |              |     |
| where | xref is | the reference |     | trajectory, | p   | is the initial | position |               |        |     |                             |     |           |              |     |
k
vectoroftheroboticarm,r istheradius,θ istheangleofthe Theparametersfordisturbancearesetas:Γ =diag(1,1,1),
|               |          |                    |          |     |                     |     |     | ω    | =[ω ,ω | ,ω ](cid:2) | ∼N([0,0,0](cid:2),0.012I).Thesamplingtime |          |         |             |     |
| ------------- | -------- | ------------------ | -------- | --- | ------------------- | --- | --- | ---- | ------ | ----------- | ----------------------------------------- | -------- | ------- | ----------- | --- |
| circulararc,k |          | isthetimestep,andη |          |     | isthenoiseterminthe |     |     |      | 1      | 2 3         |                                           |          |         |             |     |
|               |          |                    |          |     | k                   |     |     | step | Δt =   | 0.05s.      | The Sobol                                 | sequence | is used | to generate |     |
| trajectory    | planning |                    | process. |     |                     |     |     |      |        |             |                                           |          |         |             |     |
The cost function is defined as: all motion data of the robotic arm, processed through the
trapezoidalmethod.Eachsamplegeneratesaninitialstateand
|     | L(cid:21)−1(cid:22) |     |     |     |     |     | (cid:23) |     |     |     |     |     |     |     |     |
| --- | ------------------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
aseriesofcontrolinputs,simulatingtheroboticarm’smotion.
| J   | =   | (x −xref)(cid:2)V(x |     | −xref)+u(cid:2)Wu |     |     |      |             |     |                                            |     |     |     |     |     |
| --- | --- | ------------------- | --- | ----------------- | --- | --- | ---- | ----------- | --- | ------------------------------------------ | --- | --- | --- | --- | --- |
|     |     | k                   | k   | k                 | k   | k   | k    | Finally,e−3 |     |                                            |     |     |     |     |     |
|     |     |                     |     |                   |     |     | (17) |             |     | ischosenastheboundarythreshold.Dataonjoint |     |     |     |     |     |
k=0
|     |     |                  |     |        |     |     |     | angles | and | velocities | near the | boundary | values | are filtered | to  |
| --- | --- | ---------------- | --- | ------ | --- | --- | --- | ------ | --- | ---------- | -------- | -------- | ------ | ------------ | --- |
|     | +(x | −xref)(cid:2)U(x |     | −xref) |     |     |     |        |     |            |          |          |        |              |     |
L L L L ensuredatavalidity.Finally,thisexperimentgenerated103,993
| where | V is | the state | error | weight | matrix, | W is | the control | sets | of valid | data. |     |     |     |     |     |
| ----- | ---- | --------- | ----- | ------ | ------- | ---- | ----------- | ---- | -------- | ----- | --- | --- | --- | --- | --- |
input weight matrix, U is the terminal state error weight 2) Parameters for PINNs: Since there is no prior data
matrix, and L is the prediction horizon length. This problem in this scenario, sampling is needed to generate data in the
216
can be transformed into determining the optimal control input space. By generating (65536) evenly distributed high-
u∗
sequence that minimizes J given xref, where x and u dimensional samples using the Sobol sequence and scaling
|     |     |     |     |     | k   |     | k   | k   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
4621
Authorized licensed use limited to: University of Melbourne. Downloaded on May 04,2026 at 23:19:16 UTC from IEEE Xplore.  Restrictions apply.

themtotherequiredrange,initialstatesandcontrolinputsfor
| the robotic | arm simulation |     | can be | created. | The | PINNs | consist |     |     |     |     |     |     |     |
| ----------- | -------------- | --- | ------ | -------- | --- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- |
ofthreefullyconnectedlayers,eachwith128neurons,andan
| output layer    | with        | 3 neurons | for predicting |                     | the      | control    | inputs. |     |     |     |     |     |     |     |
| --------------- | ----------- | --------- | -------------- | ------------------- | -------- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| Forward         | propagation | uses      | the ReLU       | activation          |          | function,  | and     |     |     |     |     |     |     |     |
| acceleration    | is computed |           | using          | finite differences. |          | Given      | the     |     |     |     |     |     |     |     |
| sufficient      | data and    | accurate  | dynamic        | equations,          |          | the loss   | func-   |     |     |     |     |     |     |     |
| tion parameters | are         | set       | to α = β       | = 1.                | The Adam | optimizer, |         |     |     |     |     |     |     |     |
withalearningrateof0.0001,isusedfor200trainingepochs,
| recording | the loss | value | for each | epoch, | and saving | predicted |     |     |     |     |     |     |     |     |
| --------- | -------- | ----- | -------- | ------ | ---------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
valuesintoatable.Thetraininglossovertheepochsisshown
| in Figure | 2. From | the | figure, it | can be | seen that | due | to the |     |        |                                        |     |     |     |     |
| --------- | ------- | --- | ---------- | ------ | --------- | --- | ------ | --- | ------ | -------------------------------------- | --- | --- | --- | --- |
|           |         |     |            |        |           |     |        |     | Fig.3. | ActualandReferenceStateSimulationPlot. |     |     |     |     |
complexityofthedynamicmodel,theinitiallossofthePINNs
| is relatively | high. | However, | after | several | rounds | of learning, |     |     |     |     |     |     |     |     |
| ------------- | ----- | -------- | ----- | ------- | ------ | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
the loss gradually converges to a value close to zero and of the robotic arm has a significant tracking error in posi-
remains around this value. This demonstrates that the training tion. Within one second, it gradually adjusts to approach the
of the PINNs is successful. reference trajectory. This initial deviation is due to the initial
statesoftheroboticarmandthereferencetrajectorynotbeing
|     |     |     |     |     |     |     |     | completely | aligned. | Compared |     | to the brown | trajectory, | the |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | -------- | -------- | --- | ------------ | ----------- | --- |
greentrajectorytracksthereferencetrajectorymoreaccurately
|     |     |     |     |     |     |     |     | and with   | less     | fluctuation. | This      | improvement | stems        | from the  |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | -------- | ------------ | --------- | ----------- | ------------ | --------- |
|     |     |     |     |     |     |     |     | fact that, | compared | to the       | algorithm | in the      | literature   | [12], the |
|     |     |     |     |     |     |     |     | algorithm  | proposed | in this      | paper     | considers   | the terminal | state     |
errorandusesEKFtoadjustcontrolperformanceateachstep,
|     |     |     |     |     |     |     |     | making    | it more | suitable for | complex | nonlinear      | systems. |              |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ------- | ------------ | ------- | -------------- | -------- | ------------ |
|     |     |     |     |     |     |     |     | The three | charts  | on the       | right   | side of Figure | 3        | show the ve- |
locitytrackingsimulationresults.Itcanbeseenthatunderthe
|     |     |     |     |     |     |     |     | influence           | of noise, | the brown | trajectory  | deviates   |          | significantly |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --------- | --------- | ----------- | ---------- | -------- | ------------- |
|     |     |     |     |     |     |     |     | from the            | reference | velocity  | trajectory, | with       | a larger | range of      |
|     |     |     |     |     |     |     |     | speed fluctuations, |           | greatly   | affecting   | the safety | of       | the robotic   |
arm’smovement.Incontrast,thegreentrajectoryderivedfrom
theproposedalgorithmtracksthereferencevelocitytrajectory
Fig.2. Physics-InformedNeuralNetworks(PINNs)TrainingPlot. well, maintaining the stability of the system.
| 3) Parameter |        | Settings | for EKF   | and   | NMPC:     | In the | EKF,    |     |     |     |     |     |     |     |
| ------------ | ------ | -------- | --------- | ----- | --------- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- |
| Q            | 2I     | R        |           | 0.1I. |           |        |         |     |     |     |     |     |     |     |
| is set       | to and |          | is set to | In    | the NMPC, |        | set the |     |     |     |     |     |     |     |
predictionhorizonto10timesteps.Duetotheheaviermassof
| the bottom                 | link, which |         | makes it less               | sensitive | to    | disturbances, |     |     |     |     |     |     |     |     |
| -------------------------- | ----------- | ------- | --------------------------- | --------- | ----- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|                            |             |         |                             | q         | q     |               |     |     |     |     |     |     |     |     |
| the position               | error       | weights | for                         | 2 and     | 3 are | slightly      | in- |     |     |     |     |     |     |     |
| creased,whiletheweightforq |             |         | isreducedaccordingly.Denote |           |       |               |     |     |     |     |     |     |     |     |
1
| V = diag(5,10,10,1,1,1), |     |     | W   | = diag(0.1,0.1,0.1), |     |     | and |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
U =diag(5,10,10,1,1,1).Thereferencetrajectorytimestep
| is set to        | 0.05s, with | a total | time        | domain       | length    | of 100s. | The       |     |     |     |     |     |     |     |
| ---------------- | ----------- | ------- | ----------- | ------------ | --------- | -------- | --------- | --- | --- | --- | --- | --- | --- | --- |
| initial position | vector      | of      | the robotic | arm          | is p=[0.5 |          | 0.5 0.5], |     |     |     |     |     |     |     |
| r =[0.4          | 0.3 0.2],   | θ=0.6,  | and η       | ∼N(0,0.012). |           |          |           |     |     |     |     |     |     |     |
k
B. Experimental Results and Analysis Fig.4. TheRootMeanSquareError(RMSE)ofTrajectoryTracking.
Conduct the experiment as described, compare the results Figure 4 shows the Root Mean Square Error (RMSE) of
with those in the literature [12], and summarize as follows: the actual trajectories compared to the reference trajectory.
In Figure 3, the red dashed line with stars represents the The top row shows the position errors, and the bottom row
referencetrajectory,thegreensolidlinewithcirclesrepresents shows the velocity errors. The horizontal axis labels q , q ,
|     |     |     |     |     |     |     |     |     |     |     |     |     |     | 1 2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
theresultsoftheDPIPCalgorithmproposedinthispaper,and and q 3 correspond to the three axes of the robotic arm using
theDPIPCalgorithmproposedinthispaper,whileq(cid:6),q(cid:6),and
| the brown | solid line | with | squares | represents | the | results | of the |     |     |     |     |     |     |     |
| --------- | ---------- | ---- | ------- | ---------- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- |
1 2
algorithm from the literature [12] in the same environment. q(cid:6) correspond to the three axes of the robotic arm using the
3
ThethreechartsontheleftsideofFigure3showtheposition algorithm from the literature [12] in the same environment.
tracking simulation results. It can be seen that the initial state Theblueboxesinthefigurerepresentthedatadistribution,the
4622
Authorized licensed use limited to: University of Melbourne. Downloaded on May 04,2026 at 23:19:16 UTC from IEEE Xplore.  Restrictions apply.

green lines represent the median, and the black lines indicate data and the presence of noise. Experimental results demon-
the range of the RMSE. From the position error plots, it can strate that, compared with the method presented in the liter-
be seen that the RMSE between the simulation curves of the ature [12], the DPIPC method controls most of the position
DPIPCalgorithmandthereferencetrajectoryismostlyaround trackingerrorswithin0.05radandthevelocitytrackingerrors
0.05rad,withasmallerrangeoferrorfluctuations.Incontrast, within 0.02 rad/s, indicating superior experimental perfor-
the RMSE between the curves generated by the algorithm in mancewithreducedfluctuation.Thisunderscoresthemethod’s
[12] and the reference trajectory is larger, exceeding 0.05 rad, broadapplicationprospectsandresearchsignificance.Overall,
and the range of error fluctuations is greater. the DPIPC-based multi-axis robotic arm trajectory control
Fromthevelocityerrorplots,itcanbeseenthattheRMSE method provides a new solution for controlling complex
betweenthesimulationcurvesoftheDPIPCalgorithmandthe dynamic systems in intelligent manufacturing scenarios.
referencetrajectoryismostlyaround0.02rad/s,withasmaller
VI. ACKNOWLEDGMENT
rangeoferrorfluctuations.Incontrast,theRMSEbetweenthe
curves generated by the algorithm in [12] and the reference This work was supported in part by the National Key
trajectory is larger, exceeding 0.05 rad/s, and the range of Research and Development Program of China under Grant
error fluctuations is greater. Therefore, in this experimental 2022YFB3304000, the Independent Subject of the State Key
environment, from the perspective of the RMSE of position Laboratory of Robotics under Grant 2024-Z12, the National
and velocity, the DPIPC algorithm proposed in this paper is Natural Science Foundation of Liaoning province 2024-
superior to the algorithm from [12]. MSBA-85,theNationalNaturalScienceFoundationofChina(
62133014, 92267108, 62173322), the Science and Tech-
nology Program of Liaoning Province (2023JH3/10200004,
2023JH3/10200006, 2022JH25/10100005) and Youth Inno-
vation Promotion Association of the Chinese Academy of
Sciences, Y2021062.
REFERENCES
[1] M.MatulisandC.Harvey,“Arobotarmdigitaltwinutilisingreinforce-
mentlearning,”Computers&Graphics,vol.95,pp.106–114,2021.
[2] C. Yang, D. Huang, W. He, and L. Cheng, “Neural control of robot
manipulatorswithtrajectorytrackingconstraintsandinputsaturation,”
IEEETransactionsonNeuralNetworksandLearningSystems,vol.32,
no.9,pp.4231–4242,2020.
[3] M.Bi,“Controlofrobotarmmotionusingtrapezoidfuzzytwo-degree-
of-freedompidalgorithm,”Symmetry,vol.12,no.4,p.665,2020.
[4] D. Shang, X. Li, M. Yin, and F. Li, “Dynamic modeling and fuzzy
adaptivecontrolstrategyforspaceflexibleroboticarmconsideringjoint
Fig.5. 3DTrajectoryTrackingPerformanceChart. flexibility based on improved sliding mode controller,” Advances in
SpaceResearch,vol.70,no.11,pp.3520–3539,2022.
Thefinal3Dtrajectorytrackinggraphofthispaperisshown [5] M.Bikova,V.O.Latkoska,B.Hristov,andD.Stavrov,“Pathplanning
using fuzzy logic control of a 2-dof robotic arm,” in 2022 IEEE 17th
in Figure 5. Due to the initial error of the robotic arm, the
International Conference on Control & Automation (ICCA). IEEE,
graphstartsat1second.Inthefigure,thereddashedlinewith 2022,pp.998–1003.
stars represents the reference trajectory, the green solid line [6] J. Yan, L. Jin, and B. Hu, “Data-driven model predictive control for
redundant manipulators with unknown model,” IEEE Transactions on
with circles represents the trajectory generated by the DPIPC
Cybernetics,2024.
algorithmproposedinthispaper,andthebrownsolidlinewith [7] J.Nubert,J.Ko¨hler,V.Berenz,F.Allgo¨wer,andS.Trimpe,“Safeand
squares represents the trajectory obtained by the algorithm fast tracking on a robot manipulator: Robust mpc and neural network
control,”IEEERoboticsandAutomationLetters,vol.5,no.2,pp.3050–
from the literature [12] in the same environment. It can be
3057,2020.
seen from the figure that both algorithms successfully track [8] A. Astudillo, J. Carpentier, J. Gillis, G. Pipeleers, and J. Swevers,
the reference trajectory, but the green trajectory is closer to “Mixeduseofanalyticalderivativesandalgorithmicdifferentiationfor
nmpcofrobotmanipulators,”IFAC-PapersOnLine,vol.54,no.20,pp.
the reference trajectory and does not generate extraneous seg-
78–83,2021.
ments. The brown solid line deviates more from the reference [9] A. Liu, H. Zhao, T. Song, Z. Liu, H. Wang, and D. Sun, “Adaptive
trajectory and has some extraneous segments, indicating that control of manipulator based on neural network,” Neural Computing
andApplications,vol.33,pp.4077–4085,2021.
thecontrolsystemislessstableduringtracking.Fromthis3D
[10] F.Heldmann,S.Berkhahn,M.Ehrhardt,andK.Klamroth,“Pinntraining
trajectorygraph,itcanbeconcludedthattheDPIPCalgorithm using biobjective optimization: The trade-off between data loss and
proposedinthispaperhasbettertrackingperformancethanthe residualloss,”JournalofComputationalPhysics,vol.488,p.112211,
2023.
algorithm from the literature [12] in this problem.
[11] A.Carron,E.Arcari,M.Wermelinger,L.Hewing,M.Hutter,andM.N.
Zeilinger,“Data-drivenmodelpredictivecontrolfortrajectorytracking
V. CONCLUSION witharoboticarm,”IEEERoboticsandAutomationLetters,vol.4,no.4,
pp.3758–3765,2019.
For the trajectory tracking problem of multi-axis robotic [12] J.Nicodemus,J.Kneifl,J.Fehr,andB.Unger,“Physics-informedneural
arms, this paper proposes a DPIPC control method. This networks-based model predictive control for multi-link manipulators,”
IFAC-PapersOnLine,vol.55,no.20,pp.331–336,2022.
method achieves precise control despite the absence of prior
4623
Authorized licensed use limited to: University of Melbourne. Downloaded on May 04,2026 at 23:19:16 UTC from IEEE Xplore. Restrictions apply.