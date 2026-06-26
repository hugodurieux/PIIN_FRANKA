TYPE Original Research
PUBLISHED 13 January 2026
DOI 10.3389/frobt.2025.1752595
Automating PINN-based
kinematic resolution of robotic
OPEN ACCESS
EDITED BY joints using robotic process
Pei-Wei Tsai,
Swinburne University of Technology, Australia
automation frameworks
REVIEWED BY
Manar Lashin,
Benha University, Egypt
Abdalla Elgammal,
British University in Egypt, Egypt
ParthAgrawal, PavithraSekar* and KushKumarKushwaha
*CORRESPONDENCE School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, Tamil Nadu,
Pavithra Sekar, India
pavithra.sekar@vit.ac.in
RECEIVED 23 November 2025
REVISED 18 December 2025
ACCEPTED 22 December 2025 This paper explores the integration of Physics-Informed Neural Networks
PUBLISHED 13 January 2026 (PINNs) and Robot Process Automation (RPA) tools in modeling and controlling
CITATION rigid robotic joint motion. PINNs, which integrate physical laws with neural
Agrawal P, Sekar P and Kushwaha KK (2026)
networks, offer a promising solution for solving both forward and inverse
Automating PINN-based kinematic resolution
of robotic joints using robotic process problems in robotics, while RPA tools provide the means to automate and
automation frameworks. streamline these processes. The study discusses various PINN techniques,
Front. Robot. AI 12:1752595.
including Extended PINNs, Hybrid PINNs, and Minimized Loss techniques,
doi: 10.3389/frobt.2025.1752595
developed to address issues such as high training costs and slow convergence
COPYRIGHT rates. By combining these advanced PINN approaches with RPA tools, the
© 2026 Agrawal, Sekar and Kushwaha. This is
an open-access article distributed under the research aims to enhance the precision and efficiency of robot control, motion
terms of the Creative Commons Attribution planning, and process automation, particularly in non-linear and dynamic
License (CC BY). The use, distribution or
coupling situations. We also examine PDE-Inspired PINNs for motion planning
reproduction in other forums is permitted,
provided the original author(s) and the in robot navigation and manipulation by integrating it with ROS using the RPA
copyright owner(s) are credited and that the tool itself for coordinating joints and angle movements, and exploring how RPA
original publication in this journal is cited, in
can facilitate the implementation of these models in real-world scenarios.
accordance with accepted academic practice.
No use, distribution or reproduction is
permitted which does not comply with KEYWORDS
these terms.
motion planning, physics-informed neural networks, rigid robotic joint motion, robot
Operating system (ROS), RPA, robot navigation
1 Introduction
Robotic technology is today expanding due to the demand for higher level control
and optimization methods that would allow the robot to work and move with high
precision within a given environment. This paper revolves around Robotics and Automation
with substantial attention to the use of Physics-Informed Neural Networks (PINNs) for
modeling and controlling rigid robotic joint motion using environmental data. Since
newly developed robotic systems become more sophisticated, it is essential to provide
methods for analyzing those multi-joint systems more precisely, especially in situations
where external effects strongly affect the systems. One promising solution to this challenge
is the use of PINNs, which incorporates physical laws with neural networks for modeling
and solving forward and inverse problems in robotics. As it has been mentioned before,
PINNs draw much attention in recent years because of their effectiveness in solving
complicated differential equations, which widely exist in many engineering and science
fields. These neural networks find the most use in solving forward problems, where
the given factors determine the behavior of the given system, as well as for solving
inverse problems, where the parameters of the given system are determined from the
Frontiers in Robotics and AI 01 frontiersin.org

Agrawal et al. 10.3389/frobt.2025.1752595
observed behavior. PINNs have been applied in various to realistic modeling and control of multiplex robotic systems.
areas including fluid dynamics, heat transfer, and These non-conservative effects are hard to simulate employing
material science (Cuomo et al., 2022) and have proven their ability to conventional methods (Liu et al., 2024), which has rendered
capture complex physical phenomena with great accuracy. In these PINNs a useful instrument in the development of robotic control
applications, PINNs have been used in modeling fluid dynamics, methods.
predicting temperature fields, and analyzing material behavior,
among others. The multiple uses of PINNs in the solution of PDEs
suggest that it could be useful in addressing complexities in the
2 Related work
behavior of joint dynamics in robots.
Nonetheless, some common critical issues such as high training
Physics-Informed Neural Networks (PINNs) have emerged as
costs and slow convergence rate, are somewhat regarded as
a promising paradigm for embedding physical knowledge into
the drawbacks of PINNs. To address these issues, researchers
machine learning frameworks. Early surveys and bibliometric
have developed various PINN techniques, which can be broadly
analyses (Son et al., 2024) provide a comprehensive overview of
categorized into three types: Extended PINNs, Hybrid PINNs,
the development of PINNs, highlighting their ability to integrate
and Minimized Loss techniques (Lawal et al., 2022). The basic
governing equations with data-driven learning while identifying
framework of PINNs can be extended in the form of Extended
challenges such as high training costs, stiffness in dynamics,
PINNs where modification is made to the neural network structure
and scalability issues (Wang et al., 2022; Terven et al., 2023;
for a better capture of the dynamics or Hybrid PINNs which use
Ji et al., 2021; Miao and Chen, 2023).
a combination of traditional numerical methods and the neural
Loss function innovations like LSWR and differential
network methodologies. The Techniques under Minimized Loss
algebraic systems (Davi and Braga-Neto, 2022; Lu and Mei, 2022;
usually aim to improve the convergence or the rate and frequency
Zhang et al., 2024) offer dimensionless and efficient alternatives for
at which the loss function is computed. Some of this progress made
solid mechanics problems (Zhou et al., 2022). Recent frameworks
in the methodologies of PINN have been vital in enhancing the
such as PINNs-TF2 (Bafghi and Raissi, 2023) and expert training
applicability of the approach in real-time, or in any field where
guides (Wang et al., 2023) improve usability, reproducibility, and
computational power may be a constraint.
computational efficiency.PINNs have been reviewed as effective
However, a significant barrier remains in the operationalization
tools for forward and inverse kinematics problems (Cai et al., 2021).
of these advanced models within real-world robotic systems. The
transition from a simulated PINN model to a physically deployed, In fiber optics, Zang et al. (2022), Ma et al. (2022), Lee et al. (2019)
automated workflow is often hampered by a ‘deployment gap,’ where applied PINNs to nonlinear Schrödinger equations, capturing
significant manual intervention is required to interface the model pulse propagation and birefringence dynamics. Similarly, Bai et al.
with robot control frameworks like ROS and manage the data (Zhang et al., 2024) extended PINNs to 2D/3D solid mechanics, and
pipeline. This research addresses this gap by proposing a novel Li et al. (Bai et al., 2023) applied them to friction-induced vibration
methodological framework where Robotic Process Automation problems core for the robotic joints. PIRNN (Deng et al., 2024)
(RPA) is not simply used for task automation, but is architecturally integrated physics-informed modeling into recurrent architectures
positioned as an intelligent orchestration layer. This framework’s for soft pneumatic actuators (Sun et al., 2022) used in various
core innovation is its ability to create a seamless, bidirectional robotic architectures. PINN-Ray (Li et al., 2024) combined energy
communication bridge between the physics-informed model principles with experimental data for soft robotic fingers, reducing
and the robotic hardware, enabling an automated, closed-loop the reality gap.
system for control and inference that has not been previously Robotics has emerged as a key field for PINN applications.
demonstrated. By doing so, we move beyond a simple proof- Yang et al. (2023) proposed a PINN for identifying collaborative
of-concept integration and establish a scalable template for robot joint dynamics with harmonic drives, outperforming gray-
deploying complex machine learning models in dynamic physical box state-space methods. Liu et al. (2024) expanded PINNs
environments. to model and control soft robots and manipulators, validating
PINNs are applied to a wide range of robotic applications effectiveness through experiments. Ni and Qureshi (2024)
to improve modeling, control, and interaction. By incorporating applied physics-informed motion planning with the Eikonal
physical laws in the architecture of the neural network, the PINNs equation, demonstrating improved efficiency in navigation and
provide more reliable results that help in predicting the performance manipulation tasks. (Nicodemus et al., 2022; Wang et al., 2024)
of the robot under different circumstances. Use of PINNs grows further integrated PINNs into model predictive control for multi-
rapidly to simulate the behavior of the robot joints especially in link manipulators. The Recent studies have emphasized integrating
non-linear and dynamic coupling situations (Yang et al., 2023). PINNs with advanced optimization strategies and multi-scale
These factors are common in the systems of robots because of the learning. Zhou et al. (2022), explored hyperparameter optimization
interactions between several joints and impacts of loads. Having in object detection models using novel fractal and metaheuristic-
control over the physical laws involved in predicting the behavior based loss functions, showing how such strategies could inform
of a joint or a chain of joints will allow improving the precision of PINN training. Similarly, Zhou et al. (Davi and Braga-Neto, 2022)
possible control and motion planning with the help of PINNs. In and Davi et al. highlighted the role of PSO-PINN for convergence
addition, there is increasing appreciation of the need to incorporate and uncertainty quantification. Reviews on machine learning in
the versatile PINNs in applications inclusive of non-conservative soft matter and solid mechanics (Zhang et al., 2024) underline the
force influences like friction and energy loss, which are very vital potential of PINNs to generalize across disciplines.
Frontiers in Robotics and AI 02 frontiersin.org

| Agrawal et al. |     |     |     |     |     |     |     | 10.3389/frobt.2025.1752595 |     |     |
| -------------- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- |
3 Research gap process, we demonstrate a scalable and reproducible template for
deploying. The proposed system architecture which consists the
Existing  PINN  approaches  struggle  with  stiff  dynamics  model, the RPA Tool and ROS along with object locator model
(Ji et al., 2021), computational efficiency (Bafghi and Raissi, 2023),
which provides the loss values to efficiently communicate between
and real-time deployment challenges in robotics (Yang et al., 2023;  the model and the robot for maximum accuracy of results. The RPA
Liu et al., 2024; Wang et al., 2024). Few studies integrate PINNs into  tool acts as the intermediary between the model and ROS. This is
automated robotic pipelines with deployment tools such as ROS2 or  visualized and depicted in Figure 1.
Robotic Process Automation (RPA) but never fully solve the issue of  The following equations establish the mathematical foundation
compatibility with RPA and joints. for each component of this integrated system, from control theory
The integration of Physics-Informed Neural Networks (PINNs)  principles to the specific kinematic derivations and loss functions
and  Robotic  Process  Automation  (RPA)  tools  in  analyzing  that define our model.
rigid body joint movements represents a novel approach that  Object Locator Model: For object detection, we might use
addresses  a  significant  gap  in  current  research.  PINNs  have  a  convolutional  neural  network  (CNN)  with  a  loss  function
| demonstrated  | their  | potential  | in  | modeling  complex  | physical  | (Equation 1). |     |     |     |     |
| ------------- | ------ | ---------- | --- | ------------------ | --------- | ------------- | --- | --- | --- | --- |
systems by incorporating known physical laws into neural network
architectures  (Son et al., 2024).  However,  their  application  to  L=αL cls +βL loc (1)
| rigid  body  | dynamics,  | particularly  |     | joint  movements,  | remains  |             |                                   |     |                           |     |
| ------------ | ---------- | ------------- | --- | ------------------ | -------- | ----------- | --------------------------------- | --- | ------------------------- | --- |
|              |            |               |     |                    |          | where L cls |  is the classification loss and L |     | loc  is the localization  |     |
underexplored (Bafghi and Raissi, 2023). Meanwhile, RPA tools
loss (Wang et al., 2022). PINN Model is governed by solving the
have significantly improved process efficiency across various fields
differential equations of form Equation 2.
but have seen limited use in scientific modeling and simulation
| (Cai et al., 2021).  |     | The  | combination  | of  these  | two  advanced  |     |                |     |     |     |
| -------------------- | --- | ---- | ------------ | ---------- | -------------- | --- | -------------- | --- | --- | --- |
|                      |     |      |              |            |                |     | (∂u/∂t)+N[u]=0 |     |     | (2) |
technologies with PINNs providing a data-driven, physics-based
modeling framework and RPA offering streamlined, automated  where N is a nonlinear differential operator (Terven et al., 2023).
processes for data handling and analysis presents untapped potential  The PINN loss function typically includes both data and physics
components represented in Equation 3.
in the field of kinematics (Wang et al., 2023).
| Recent            | developments  |             | in  PDE-Inspired  | PINNs                  | allow   | the  |        |                        |     |     |
| ----------------- | ------------- | ----------- | ----------------- | ---------------------- | ------- | ---- | ------ | ---------------------- | --- | --- |
|                   |               |             |                   |                        |         |      | L PINN | =MSE data +MSE physics |     | (3) |
| formulation       | of  novel     | techniques  |                   | for  physics-informed  | neural  |      |        |                        |     |     |
| motion  planning  |               | in  robot   | navigation        | and  manipulation (Ni  |         |      |        |                        |     |     |
For inverse kinematics, we might use Joint Servo Values and the
and Qureshi, 2024). These advancements have vast potential of
Jacobian matrix represented in Equation 4.
| enhancing  | the  precision  |     | and  functionality  | of  robotic  | systems  |     |     |     |     |     |
| ---------- | --------------- | --- | ------------------- | ------------ | -------- | --- | --- | --- | --- | --- |
especially in scenarios that are laden with dominant force dynamics.  Δθ=J+Δx (4)
In this way, with the help of PINNs, researchers are able to create
|     |     |     |     |     |     | where  J+  | is  the  pseudo  | inverse  of  | the  Jacobian,  | Δθ  is  |
| --- | --- | --- | --- | --- | --- | ---------- | ---------------- | ------------ | --------------- | ------- |
more complex models as well as control algorithms that will make
robots perform even better in various tasks applicable in industries,  the  change  in  joint  angles,  and  Δx  is  the  desired  end-
effector movement (Zhou et al., 2022).
space exploration and many other sectors. In this paper, we provide
a detailed discussion of PINNs applied to modeling rigid robot joint  For forward kinematics of an n-joint robot arm, it is represented
| movements, along with the results of simulation experiments on the  |     |     |     |     |     | as T in Equation 5. |     |     |     |     |
| ------------------------------------------------------------------- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- | --- |
application of the proposed approaches.
|     |     |     |     |     |     |     | T=A | ×A ···×A |     | (5) |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- |
|     |     |     |     |     |     |     |     | 1 2 n    |     |     |
where T is the transformation matrix and A are individual joint
| 4 Methodology |     |     |     |     |     |     |     |     | I   |     |
| ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
transformations. For control systems we use a PID controller for
smooth motion and is represented in Equation 6.
| The  | methodology  | presented  |     | herein  integrates  | several  |     |     |     |     |     |
| ---- | ------------ | ---------- | --- | ------------------- | -------- | --- | --- | --- | --- | --- |
de(t)
computational components to achieve automated, physics-informed
|     |     |     |     |     |     |     | u(t)=K p e(t)+K | i ∫e(t)dt+K | d   | (6) |
| --- | --- | --- | --- | --- | --- | --- | --------------- | ----------- | --- | --- |
dt
control of a robotic arm. The core objective is to solve the inverse
kinematics problem of determining the necessary joint angles to  where u(t) is the control signal, e(t) is the error, and K , K, K  are
|     |     |     |     |     |     |     |     |     | p   | i d |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
position the robot’s end-effector at a desired location by leveraging  gains. To calculate error and performance evaluation we use Root
a Physics-Informed Neural Network (PINN). Our approach begins  Mean Square Error (RMSE) as referred in Equation 7.
by identifying an object’s position using a standard object locator
∑(ŷ−y)2
model. This position data then serves as the input for a custom  √
|     |     |     |     |     |     |     | RMSE= |     |     | (7) |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
PINN, which is designed not only to learn from training data  n
but also to adhere to the governing kinematic equations of the
where y ̂are predicted values and y are actual values. Similarly, loss is
robot. The RPA tool orchestrates this workflow, managing data
defined in Equation 8.
flow between the perception model, the PINN, and the Robot
|     |     |     |     |     |     |     |     | 1   | 2   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Operating System, which executes the final joint movements. This  Loss= ∑(θ −θ ) (8)
n pred true
architectural choice represents a key contribution, as it abstracts the
complexities of both the ROS interface and the PINN model into  While the preceding Equations 1–8 represent a comprehensive
a single, manageable workflow. By establishing this orchestrated  toolkit for advanced robotic systems, our study focuses specifically
| Frontiers in Robotics and AI |     |     |     |     |     | 03  |     |     | frontiersin.org |     |
| ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- |

Agrawal et al. 10.3389/frobt.2025.1752595
FIGURE 1
Architecture of the physics-informed neural network (PINN) integrated with Robotic Process Automation (RPA) and ROS.
on applying a subset of these principles to the core challenge of
rigid joint motion. The central task is to derive a robust model
for the inverse kinematics of a 2R planar robot. Therefore, the
primary components we will develop in detail are the forward and
inverse kinematic models specific to our robot’s geometry, and the
formulation of a novel loss function for the PINN. This loss function
will incorporate the analytical gradients of the inverse kinematics
solution as a physical constraint, ensuring the network’s predictions
are not only data-driven but also physically consistent. The PID
controller is mentioned as standard components in the broader
control loop that our system would integrate into, but the novel
contribution of this work lies in the formulation and automated
training of the PINN itself.
We further need to follow and assert a few assumptions. All the
results and experimentation are being done on a 2RP robot where
the Prismatic joint, being perpendicular to the plane of the rotation FIGURE 2
2R robot structure.
joints can be ignored in our calculations. The robot is represented
with the structure shown in Figure 2.
The prismatic joint being ignored gives a 2R robot on a 2D
plane with the two rotation joints being parallel to each other and
The general flow of the working of the system is
the values of z-axis are being ignored too. All calculations in the
represented in Figure 4, which describes it in brief. The PINN model
methodology and the results are made only considering the x and
and the Object locator model used in the flow are pre-trained. The
y-axis. The end effect or of the robot has a camera attached to it, and
PINN model will be trained using the RPA tool and will act as the
the images taken from it are assumed to have the camera at origin of inference point of the angles of rotations. The inferred angles will
the frame. This ensures that any object placed inside the frame is at be communicated to the servos/motors via ROS2 and logs will be
exactly (x,y) coordinate in the relative frame as shown in Figure 3. generated on both ends.
The following notations will be used henceforth in the paper To calculate any future angles, the global coordinates of the
relating to all equations: object are required in the x-y plane and are calculated using (9)
and (10). To train the PINN and calculate the required joint angle
1. θ forAngleofBaseJoint(Joint1)
1
corrections, it is first necessary to establish the forward kinematics
2. θ forAngleofJoint2(relativetothefirstlink)
2 of the 2R robot. This involves calculating the global coordinates of
3. l forLengthofLink1
1 an object detected by the end-effector camera. The end-effector itself
4. l forLengthofLink2
2 is located at global coordinates (x ,y ), determined by the standard
e e
Also Joint2 signifies the joint nearest to end effector. kinematic chain equations given before. The camera, mounted on
Frontiers in Robotics and AI 04 frontiersin.org

| Agrawal et al. |     |     |     | 10.3389/frobt.2025.1752595 |     |     |     |
| -------------- | --- | --- | --- | -------------------------- | --- | --- | --- |
FIGURE 3
Representation of relative frame of camera and object.
basis for our kinematic calculations.
|     |     |     | xw  | =l cosθ +l cos(θ | +θ ) |     | (9)  |
| --- | --- | --- | --- | ---------------- | ---- | --- | ---- |
|     |     |     | 1   | 1 1 2            | 1 2  |     |      |
|     |     |     | yw  | =l sinθ +l sin(θ | +θ ) |     | (10) |
|     |     |     | 1   | 1 1 2            | 1 2  |     |      |
Now, the new angle to reach (x,y) for the angle nearest to the
|     | end effector θ |     |  is calculated using substitution of values calculated in  |     |     |     |     |
| --- | -------------- | --- | ---------------------------------------------------------- | --- | --- | --- | --- |
2
Equations 9 and 10 into (Equation 11) and finally into (Equation 12).
|     |     |                                                      |     | ‖xw‖2=xw2+yw2 |     |     | (11)   |
| --- | --- | ---------------------------------------------------- | --- | ------------- | --- | --- | ------ |
|     |     |                                                      |     | 1             | 1   |     |        |
|     |     | With the global coordinates of the target object, (x |     |               |     |     | ,y ),  |
w1 w1
established, we can now address the inverse kinematics problem:
|     | determining the new joint angles, θ |     |     |  and θ | , required to move  |     |     |
| --- | ----------------------------------- | --- | --- | ------ | ------------------- | --- | --- |
|     |                                     |     |     | 1      | 2                   |     |     |
the end-effector to this target location. For a 2R manipulator, this
can be solved geometrically. Consider the triangle formed by the
|     | robot’s base (origin), the first joint, and the target point (x |     |     |     |     |     | ,y ).  |
| --- | --------------------------------------------------------------- | --- | --- | --- | --- | --- | ------ |
w1 w1
|     | The sides of this triangle have lengths l |     |     | , l | , and a resultant length  |     |     |
| --- | ----------------------------------------- | --- | --- | --- | ------------------------- | --- | --- |
1 2
|     | from the origin to the target, which we define as x |     |     |     |     |  as shown in  |     |
| --- | --------------------------------------------------- | --- | --- | --- | --- | ------------- | --- |
w2
Equation 11. By applying the Law of Cosines to this triangle, we can
|     | solve for the angle of the second joint, θ |     |     | 2 . The Law of Cosines states  |     |     |     |
| --- | ------------------------------------------ | --- | --- | ------------------------------ | --- | --- | --- |
=l2+l2−2l
|     | that x2                                            |      | l    | cos(π−θ ). Since cos (π−θ |     | ) = − cos (θ       | ),  |
| --- | -------------------------------------------------- | ---- | ---- | ------------------------- | --- | ------------------ | --- |
|     |                                                    | w2 1 | 2 12 | 2                         |     | 2                  | 2   |
|     | this can be rearranged to solve directly for cos(θ |      |      |                           |     | ), leading to the  |     |
2
formulation for the new joint angle θ′ as presented in Equation 12.
2
FIGURE 4
Proposed working flowchart of system.
‖xw‖2−l2−l2
|     |     |     | =cos−1( | 1   | 2)  |     |      |
| --- | --- | --- | ------- | --- | --- | --- | ---- |
|     |     |     | θ 2     |     |     |     | (12) |
2l l
12
|     |     | To  keep  | the  representation  | of  the  | gradients  | clear  | while  |
| --- | --- | --------- | -------------------- | -------- | ---------- | ------ | ------ |
calculating, we are representing the RHS of the equation to calculate
the end-effector, identifies an object at relative coordinates (x,y)  the angle value as a function f stated in Equation 13.
within its own frame. To find the object’s global coordinates,
(x ,y ), we must translate the object’s relative position to the
| w1 w1 |     |     |     | θ 2 = f(x,y) |     |     | (13) |
| ----- | --- | --- | --- | ------------ | --- | --- | ---- |
end-effector’s position and rotate it according to the end-effector’s
orientation, which is (θ +θ ). This coordinate transformation yields  After the calculation of θ , the base rotation is calculated with
1 2 2
the expressions presented in the following equations, which form the  respect to the calculated angle in Equation 14, thus making θ  the
2
| Frontiers in Robotics and AI | 05  |     |     |     |     | frontiersin.org |     |
| ---------------------------- | --- | --- | --- | --- | --- | --------------- | --- |

Agrawal et al. 10.3389/frobt.2025.1752595
equations (Equations 9, 10). The Physics Loss is then calculated
as the Euclidean distance between the resulting coordinates and
the target coordinates (x,y). This forces the network to discover
the correct inverse mapping by adhering to the geometric laws of
the robot structure. By minimizing this physics loss, we compel
the network to learn not just a set of points, but the fundamental
geometric relationship between the target’s position and the robot’s
joint configuration, thereby improving its accuracy and ability to
generalize.
Following model creation, we calculate the primary Loss as
referred in Equation 15 in the form of Mean Squared Loss.
1 2
Loss= ∑(θ −θ ) (15)
n pred true
The Physics Loss necessary for the creation of the PINN is
calculated as Loss2 and is the deciding loss for the equations. To get
the loss function, we need to minimize the LHS of the Equation 16.
L =‖FK(θ )−x ‖ 2 (16)
physics pred target
Finally, the Total loss for the model is thus calculated by taking
FIGURE 5 a weighted sum of the primary loss and Loss with the mathematical
Flow of data and calculations across the model. 2
equation referred in Equation 17.
TotalLoss=Loss +weights.L (17)
primary physics
deciding factor for our model, since it is the only rotation depending
To successfully minimize errors and perform complex
on the values of x and y directly.
calculations, the Autograd function of the PyTorch gradient
function calculators was used to automatically apply the complex
y l sinθ
θ 1 =tan−1( x w)−tan−1( l + 2 l cos 2 θ ) (14) differentiations that need to be calculated for the Physics Loss.
w 1 2 2
After the completion of the model, the model files are linked to the
The flow of the calculations is simplified and depicted as given RPA tool Robot Framework which provides an assistant function
in Figure 5. They show the general manipulation of values starting to simplify the training methods to automate the complete training
from the relative values to the final values of output from the process based on simple inputs from the user. The tasks are created
model. After the calculation of the values, the model is created as in python to assure uniformity of model created and the overall
represented in Figure 1, which shows the system architecture. The ease of access and updating. UIPath is a robust alternative, which is
model created is a custom PyTorch model in which the forward primarily coded in.NET and C#, with support for running python
function is updated to convert each local value to global values of scripts, but is not being used in this study due to our need for
the coordinates automatically, preserving extensive mathematical connection to the ROS2 framework, for which python will be used.
calculations. The tool is then bridged to the ROS2 subscriber using a publisher
The losses are then added to the model and are represented as to publish the values being calculated based on the inputs of the
the primary loss and the physics loss. The primary loss provides object location calculated from the camera sent to the model via the
the base loss function for the model and the physics loss provides RPA ROS bridge.
the correct physical quantity needed to be calculated as derivatives The calculated value is then used to calculate the base
of the appropriate losses. The foundation of our PINN model angle and then the angle of rotation is calculated for the
is a loss function composed of two distinct parts: a data-driven motor/servo movement.
primary loss and a physics-based loss. The neural network is
trained to learn the function f from Equation 13, which maps
5 Experimental results
the relative object coordinates (x,y) to the required joint angle θ .
2
The primary loss, formulated as a Mean Squared Error (MSE),
ensures that the network’s predicted angle, θ , accurately To train the model, a straight line was taken with link lengths
predicted
matches the true angle, θ , for the given training data points. More l =6cm and l =5cm. θ and θ are taken as 0deg each. All
true 1 2 1 2
importantly, the physics loss component embeds the governing length measurements are defined in centimeters (cm).To validate
kinematic principles directly into the training process. Instead of the model’s trajectory tracking capabilities, a linear path defined
only penalizing errors in the output value, we penalize any violation by 1.7x−2y=4 was selected as the primary test bench. While
of the underlying physical laws. This is achieved by using the robot’s the initial training utilized a dataset of 30 equidistant points
Forward Kinematics as the physics-based constraint. Instead of along this trajectory to demonstrate rapid convergence, the model’s
training the network on a known inverse solution, we input the robustness was further validated against a broader set of random
network’s predicted joint angles (θ ,θ ). into the forward kinematic points within the robot’s reachable workspace to ensure it had not
1 2
Frontiers in Robotics and AI 06 frontiersin.org

Agrawal et al. 10.3389/frobt.2025.1752595
FIGURE 8
Predicted values and actual values.
FIGURE 6
Relation between θ and Y values.
2
of 0.85°, the standard FNN trained on the same dataset only
reached an accuracy of 91.5% with a significantly higher RMSE
of 2.1°, indicating that it struggled to generalize to the untrained
portion of the trajectory. Crucially, while the analytical inverse
kinematics solution (Equation 12) provides exact values, it is
susceptible to computational instability near kinematic singularities
(where the Jacobian determinant approaches zero). In such
configurations, the analytical method often results in infinite
velocities or undefined values. The PINN approach, constrained by
the physics loss, demonstrates superior stability in these regions,
providing smooth and continuous joint angle predictions even when
the analytical solver fails or requires complex exception handling.
The Jacobian-based method provided high accuracy (≈99%) for
points within its well-conditioned workspace but suffered from
convergence issues near singular configurations and had a variable,
FIGURE 7 often slower, computation time. Our proposed model provides a
Log Loss vs. Epoch graph.
more balanced and reliable performance, avoiding the pitfalls of
singularities while outperforming the purely data-driven FNN.
Furthermore, a robustness analysis was conducted to assess the
model’s performance under noisy conditions, simulating real-world
overfitted to a single line. The results presented below focus on the sensor inaccuracies. We introduced zero-mean Gaussian noise with
trajectory tracking performance, which is critical for continuous a standard deviation of 0.5 units to the input coordinates of the
path applications. The points taken in total are 100 and both the test data. Under these conditions, the performance of our PINN
training data and the 100 points are equidistant to each other model degraded gracefully, with the RMSE increasing to only 1.5°.
on the x-axis of the graph representing relation between y and In contrast, the standard FNN proved to be more brittle, as its
θ 2 in Figure 6. RMSE escalated to 4.5°. This demonstrates that the physics-informed
The model is trained with the physics loss for 10,000 epochs with constraint acts as a powerful regulariser, preventing the model from
a learning rate of 10−4 with the Loss weights as 0.6, which gives a overfitting to the training data and enabling it to maintain reliable
2
loss graph represented in Figure 7 with final loss at 0.6243 for the predictions even when inputs are corrupted by noise.
complete extended line. The model was then used to predict all the To ensure the statistical significance of our findings, the
values on the initial line of 100 points and the accuracy of the model entire training and evaluation process for the PINN model was
was calculated. The model provided an accuracy of around 96% for repeated 10 times with different random initializations. The model
the remaining line not trained on, as represented in Figure 8. demonstrated high stability, yielding a final accuracy of 96.2% with
To provide a more comprehensive evaluation, the performance a low standard deviation of ±0.4%. In terms of computational
of our PINN model was benchmarked against two alternative performance, our model’s average inference time was measured
approaches: a standard Feedforward Neural Network (FNN) at approximately 2 ms on an NVIDIA RTX 3060 GPU. While a
without the physics-informed loss term, and a classical iterative single iteration of the Jacobian-based method was faster at 0.5 ms, it
Jacobian-based method. While our PINN model achieved an required an average of five to six iterations to converge, resulting in
accuracy of 96.2% with a Root Mean Square Error (RMSE) a total computation time of around 3 ms. The direct, non-iterative
Frontiers in Robotics and AI 07 frontiersin.org

| Agrawal et al. |     |     |     |     |     |     |     |     | 10.3389/frobt.2025.1752595 |     |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- |
TABLE 1  System latency.
|     |     |     |     |     |     |     | Component        | Description                   |     | Time (ms) |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | ----------------------------- | --- | --------- |
|     |     |     |     |     |     |     | Object detection | CNN inference                 |     | 25        |
|     |     |     |     |     |     |     | RPA bridge       | Data transfer (python to ROS) |     | 12        |
|     |     |     |     |     |     |     | PINN inference   | Joint angle prediction        |     | 2         |
|     |     |     |     |     |     |     | Control signal   | ROS publication to servo      |     | 1.5       |
|     |     |     |     |     |     |     | Total loop       | End-to-end latency            |     | ∼40.5     |
FIGURE 9
Robot framework architectural framework. Using the conda environment, created by the RPA tool, the
environment could be tweaked to successfully create the proper
utilities for running a bridge between ROS2 and the tool. The system
performance metrics are detailed in Table 1.
6 Conclusion
This study represents an advancement in applying RPA tools
and PINN technologies to practical robot control problems. RPA
has been evident in its applications across the industry for software
automation, but this study hopes to bring that level of automation
to the creation of physical robots. By using RPA for both PINN
FIGURE 10 training and ROS2 integration, we have demonstrated a novel
Remote architectural framework for robot framework.
and effective approach to solving inverse kinematics with high
accuracy. The primary contribution of this work is the establishment
of a novel, RPA-centric framework that fundamentally addresses
the deployment gap between theoretical PINN models and their
nature of our PINN model’s predictions makes it highly suitable
practical application on physical robots. It is important to note
for real-time control applications where consistent and low-latency
performance is critical. that while this study validates the architectural framework and
data pipeline in a high-fidelity simulation environment, future
| This  | successful  | extension  | confirms  | that  | the  | RPA-centric  |     |     |     |     |
| ----- | ----------- | ---------- | --------- | ----- | ---- | ------------ | --- | --- | --- | --- |
orchestration  pipeline  is  not  limited  to  simple  planar  work will focus on deployment and latency testing on physical
robotic hardware to further quantify the real-world performance
| robots  and  | can            | be  effectively  |     | applied  | to  more          | complex  |                   |              |                     |                  |
| ------------ | -------------- | ---------------- | --- | -------- | ----------------- | -------- | ----------------- | ------------ | ------------------- | ---------------- |
|              |                |                  |     |          |                   |          | gains.  We  have  | shown  that  | by  elevating  RPA  | from  a  simple  |
| spatial      | manipulators,  | showcasing       |     | the      | generalizability  |          | of                |              |                     |                  |
our approach. automation script to an intelligent orchestration layer, it is possible
|     |     |     |     |     |     |     | to  create  a  | fully  autonomous,  | closed-loop  | pipeline  for  robot  |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ------------------- | ------------ | --------------------- |
After the model is trained, an RPA process was started which
first takes in the values of l , l , θ  and θ  using the assistant created. control that seamlessly handles data ingestion, model inference,
|     |     | 1   | 2 1 | 2   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
and hardware communication. This contribution extends beyond
| The  | architecture  | used  | by  the  | tool  “Robot  | Framework”  |     | is  |     |     |     |
| ---- | ------------- | ----- | -------- | ------------- | ----------- | --- | --- | --- | --- | --- |
mere system integration by providing a methodological blueprint
represented as depicted in Figure 9, where the testing data, in
conjunction  with  the  robot  framework  and  working  with  the  for in-the-loop model execution, tackling a persistent challenge
in the operationalization of complex machine learning models in
underlying test libraries and APIs contains the tasks to be performed
on the lowest layer, the system under test, thus automating tasks  robotics. Our framework offers a robust and scalable solution that
reduces manual oversight and enhances the responsiveness of the
efficiently.
robotic system. As the fields of robotics and automation continue
| Also,  | to  organically  | cater  | to  | the  remote  | capabilities  |     | for  |     |     |     |
| ------ | ---------------- | ------ | --- | ------------ | ------------- | --- | ---- | --- | --- | --- |
ROS  integration,  the  tool  employs  its  remote  architecture  to evolve, we believe that this integrated approach will play a
crucial role in developing more intelligent, accurate, and responsive
as shown in Figure 10.
| The robot, on the other hand, started sending the processed  |      |                          |      |            |           |                 | robotic systems. |     |     |     |
| ------------------------------------------------------------ | ---- | ------------------------ | ---- | ---------- | --------- | --------------- | ---------------- | --- | --- | --- |
| coordinates                                                  | to   | the  RPA  tool           | and  | logged     | all  the  | values          | on               |     |     |     |
| the  shell.                                                  | The  | RPA  tool  successfully  |      | connected  |           | to  the  robot  |                  |     |     |     |
and  calculated  the  angle  θ   using  the  model  and  the  angle  Data availability statement
1
| θ   using  | the  equation  | dependent  |     | on  the  | previous  | angle.  | The  |     |     |     |
| ---------- | -------------- | ---------- | --- | -------- | --------- | ------- | ---- | --- | --- | --- |
2
angle  was  then  published  to  the  robot  using  the  same  node The raw data supporting the conclusions of this article will be
on the RPA. made available by the authors, without undue reservation.
| Frontiers in Robotics and AI |     |     |     |     |     |     | 08  |     |     | frontiersin.org |
| ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- |

Agrawal et al. 10.3389/frobt.2025.1752595
Author contributions Generative AI statement
PA: Data curation, Conceptualisation, Writing – original The author(s) declared that generative AI was not used in the
draft, Formal analysis, Methodology, Resources. PS: Supervision, creation of this manuscript.
Writing – review and editing. KK: Software, Investigation, Any alternative text (alt text) provided alongside figures in
Writing – original draft, Resources, Visualization, Project this article has been generated by Frontiers with the support of
administration, Methodology. artificial intelligence and reasonable efforts have been made to
ensure accuracy, including review by the authors wherever possible.
If you identify any issues, please contact us.
Funding
The author(s) declared that financial support was not received
Publisher’s note
for this work and/or its publication.
All claims expressed in this article are solely those of the
Conflict of interest authors and do not necessarily represent those of their affiliated
organizations, or those of the publisher, the editors and the
The author(s) declared that this work was conducted in the reviewers. Any product that may be evaluated in this article, or claim
absence of any commercial or financial relationships that could be that may be made by its manufacturer, is not guaranteed or endorsed
construed as a potential conflict of interest. by the publisher.
References
Bafghi, R. A., and Raissi, M. (2023). “PINNs-TF2: fast and user-friendly physics- Miao, Z., and Chen, Y. (2023). VC-PINN: variable coefficient physics-informed
informed neural networks in TensorFlow V2,” arXiv:2311.03626. neural network for forward and inverse problems of PDEs with variable coefficient.
Phys. D. Nonlinear Phenom. 456, 133945. doi:10.1016/j.physd.2023.133945
Bai, J., Chen, J. S., Zhang, H., Zhuang, X., and Gu, Y. (2023). A physics-informed
neural network technique based on a modified loss function for computational 2D Ni, R., and Qureshi, A. H. (2024). “Physics-informed neural networks for robot
and 3D solid mechanics. Comput. Mech. 71 (3), 543–562. doi:10.1007/s00466-022- motion under constraints,” in Proc. 1st workshop neural fields robotics (RoboNerF) at
02252-0 ICRA.
Cai, S., Mao, Z., Wang, Z., Yin, M., and Karniadakis, G. E. (2021). Physics-informed Nicodemus, J., Jerez, J. L., De la Cruz, J. M. Z. J. M., and Sava, S. M. (2022). Physics-
neural networks (PINNs) for fluid mechanics: a review. Acta Mech. Sin. 37 (12), informed neural networks-based model predictive control for multi-link manipulators.
1727–1738. doi:10.1007/s10409-021-01148-1 IFAC-PapersOnLine 55 (20), 331–336. doi:10.1016/j.ifacol.2022.09.117
Cuomo, S., Di Cola, V. S., Giampaolo, F., Rozza, G., Raissi, M., and Piccialli, F. (2022). Son, S., Jeong, J., Jeong, D., Sun, K. H., and Oh, K.-Y. (2024). “Physics-informed
Scientific machine learning through physics-informed neural networks: where we are neural network: principles and applications,” in Recent advances in neuromorphic
and what’s next. J. Sci. Comput. 92 (3), 88. doi:10.1007/s10915-022-01939-z computing (IntechOpen).
Davi, C., and Braga-Neto, U. (2022). “Pso-pinn: physics-informed neural networks Sun, W., Akashi, N., Kuniyoshi, Y., and Nakajima, K. (2022). Physics-informed
trained with particle swarm optimization,” arXiv:2202.01943. recurrent neural networks for soft pneumatic actuators. IEEE Robotics Automation Lett.
7 (3), 6862–6869. doi:10.1109/lra.2022.3178496
Deng, W., He, H., Liu, Z., Wang, Y., and Medjaher, K. (2024). Physics informed
machine learning model for inverse dynamics in robotic manipulators. Appl. Soft Terven, J., Cordova-Esparza, D. M., Ramirez-Pedraza, A., Chavez-Urbiola, E. A.,
Comput. 163, 111877. doi:10.1016/j.asoc.2024.111877 and Romero-Gonzalez, J. A. (2023). “Loss functions and metrics in deep learning,”
arXiv:2307.02694.
Ji, W., Qiu, W., Shi, Z., Pan, S., and Wang, S. (2021). Stiff-pinn: physics-informed
neural network for stiff chemical kinetics. J. Phys. Chem. A 125 (36), 8098–8106. Wang, Q., Ma, Y., Zhao, K., and Tian, Y. (2022). A comprehensive survey of loss
doi:10.1021/acs.jpca.1c05102 functions in machine learning. Ann. Data Sci. 9, 187–212. doi:10.1007/s40745-020-
00253-5
Lawal, Z. K., Rahman, M. A. A., Othman, M. M., and Taujuddin, N. S. A. M.
(2022). Physics-informed neural network (PINN) evolution and beyond: a systematic Wang, S., Sankaran, S., Wang, H., and Perdikaris, P. (2023). “An expert’s guide to
literature review and bibliometric analysis. Big Data Cognitive Comput. 6 (4), 140. training physics-informed neural networks,” arXiv:2308.08468.
doi:10.3390/bdcc6040140
Wang, X., Zhang, C., Wang, D., Chen, F., Viswanathan, V., Scalzo, R., et al. (2024).
Lee, M., Kim, H., Joe, H., and Kim, H.-G. (2019). Multi-channel PINN: investigating “PINN-Ray: a physics-informed neural network to model soft robotic fin ray fingers,”
scalable and transferable neural networks for drug discovery. J. Cheminform. 11, 46. 247, 254. doi:10.1109/iros58592.2024.10802217
doi:10.1186/s13321-019-0368-1
Yang, X., Du, Y., Li, L., Zhou, Z., and Zhang, X. (2023). Physics-informed
Li, Z., Zhang, W., Liu, Z., Chen, Y., Tang, M., Yang, Y., et al. (2024). Physics-informed neural network for model prediction and dynamics parameter identification of
neural networks for friction-involved nonsmooth dynamics problems. Nonlinear Dyn. collaborative robot joints. IEEE Robotics Automation Lett. 8 (12), 8462–8469.
112 (9), 7159–7183. doi:10.1007/s11071-024-09350-z doi:10.1109/lra.2023.3329620
Liu, J., Borja, P., and Della Santina, C. (2024). Physics-informed neural networks to Zang, Y., Yu, Z., Xu, K., Lan, X., Chen, M., Yang, S., et al. (2022). Principle-driven fiber
model and control robots: a theoretical and experimental investigation. Adv. Intell. Syst. transmission model based on PINN neural network. J. Light. Technol. 40 (2), 404–414.
6 (5), 2300385. doi:10.1002/aisy.202300385 doi:10.1109/JLT.2021.3139377
Lu, Y., and Mei, G. (2022). A deep learning approach for predicting two-dimensional Zhang, K., Gong, X., and Jiang, Y. (2024). Machine learning in soft
soil consolidation using physics-informed neural networks (PINN). Mathematics 10 matter: from simulations to experiments. Adv. Funct. Mater. 34, 2315177.
(16), 2949. doi:10.3390/math10162949 doi:10.1002/adfm.202315177
Ma, Y., Li, C., Zhu, J., and He, X. (2022). A preliminary study on the resolution Zhou, M., Li, B., and Wang, J. (2022). Optimization of hyperparameters in
of electro-thermal multi-physics coupling problem using physics-informed neural object detection models based on fractal loss function. Fractal Fract. 6 (12), 706.
network (PINN). Algorithms 15 (2), 53. doi:10.3390/a15020053 doi:10.3390/fractalfract6120706
Frontiers in Robotics and AI 09 frontiersin.org