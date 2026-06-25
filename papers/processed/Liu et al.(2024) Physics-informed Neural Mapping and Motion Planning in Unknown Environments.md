5202
nuJ
51
]OR.sc[
2v38890.0142:viXra
1
Physics-informed Neural Mapping and Motion
Planning in Unknown Environments
Yuchen Liu *, Ruiqi Ni *, and Ahmed H. Qureshi
Fig. 1: Active NTFields mapping and motion planning in a real-world indoor environment with a differential drive Turtlebot4
robot.Mapping:Thetoprowshowstheonlineexplorationoftheenvironmentwiththecorrespondingdepthimagestream.Our
method incrementally constructs the map with incoming frames and uses the reconstructed arrival time field in the partially
observed environment to reach the next viewpoint for further sensing. Thus, no external motion planner is needed during
mapping. Finally, in this environment, the robot takes 65 seconds to actively explore and reconstruct the arrival time fields.
Motion Planning: The bottom row shows motion planning in the reconstructed environment, where the goal is set behind the
chair, and planning takes only 0.02 seconds.
Abstract—Mappingandmotionplanningaretwoessentialele- I. INTRODUCTION
mentsofrobotintelligencethatareinterdependentingenerating
environmentmapsandnavigatingaroundobstacles.Theexisting MAPPING and motion planning are two fundamental
mapping methods create maps that require computationally components in robotic operations within unknown en-
expensive motion planning tools to find a path solution. In this vironments [12, 29]. Mapping is focused on reconstructing
paper, we propose a new mapping feature called arrival time
environmentalfeatures,suchasobstacleoccupancyordistance
fields, which is a solution to the Eikonal equation. The arrival
to obstacle [12, 59, 65]. Motion planning, on the other hand,
time fields can directly guide the robot in navigating the given
environments. Therefore, this paper introduces a new approach uses these mapped features to find collision-free sequences of
called Active Neural Time Fields (Active NTFields), which is robot movements between the specified start and goal points
a physics-informed neural framework that actively explores the [29]. Despite decades of development in both fields [59], a
unknown environment and maps its arrival time field on the
notablegapstillexistsbetweeneffectivemappingandefficient
fly for robot motion planning. Our method does not require any
motion planning, requiring additional, often computationally
expertdataforlearningandusesneuralnetworkstodirectlysolve
the Eikonal equation for arrival time field mapping and motion intensive, tools to integrate these systems seamlessly.
planning. We benchmark our approach against state-of-the-art Forinstance,avarietyofmotionplanningalgorithms—from
mappingandmotionplanningmethodsanddemonstrateitssupe-
optimization-based to sampling-based planners—rely heavily
riorperformanceinbothsimulatedandreal-worldenvironments
on collision features identified during the mapping phase
withadifferentialdriverobotanda6degrees-of-freedom(DOF)
robot manipulator. The supplementary videos can be found at [27,75].Thesealgorithms,whilepowerful,demandsignificant
https://youtu.be/qTPL5a6pRKk, and the implementation code computational resources and time to deliver viable path solu-
repositoryisavailableathttps://github.com/Rtlyc/antfields-demo. tions. Bridging this gap efficiently has profound implications
for practical robotics applications.
Index Terms—Mapping, motion planning, physics-informed Specifically, robots often need to generate a map of their
neural networks, partial differential equations (PDEs) environmentonlyonceandthenuseitrepeatedlytofindpaths
between arbitrary start and goal points. A vacuum robot, for
The authors are with the Department of Computer Science, Purdue example,maycreateamapofahomeenvironmentonlyonce,
University, West Lafayette, IN 47907, USA (e-mail: liu3853@purdue.edu,
butitwillusemotionplannersoverthatmaptoreacharbitrary
ni117@purdue.edu,ahqureshi@purdue.edu).
*denotesequalcontribution dirty places throughout its lifespan. If the mapping feature

2
requiresadditionalcomputationallyexpensivetoolsformotion arrival time field map for pathfinding in near real-time.
planning,thesetoolswillbeneededrepeatedlythroughoutthe ● Demonstrations of our proposed mapping and motion plan-
robot’s operational lifespan. Thus, a map that eliminates the ning framework in simulated and real-world, complex en-
need for costly motion planning methods would be ideal for vironments with a differential drive robot and 6-DOF robot
| a wide range | of  | real-world | robotics | applications. |     |     | manipulator. |     |     |     |     |     |     |     |
| ------------ | --- | ---------- | -------- | ------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
Therefore,inthispaper,weproposeanovelmappingfeature
|     |     |     |     |     |     |     | Our results | show | that | the Active | NTFields | quickly | map | the |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ---- | ---- | ---------- | -------- | ------- | --- | --- |
called the arrival time fields, which bridges the gap between unknownenvironmentandallowmotionplanningmuchfaster
| mapping    | and motion | planning | without | needing   | any     | compu- |                 |          |           |              |     |                |        |          |
| ---------- | ---------- | -------- | ------- | --------- | ------- | ------ | --------------- | -------- | --------- | ------------ | --- | -------------- | ------ | -------- |
|            |            |          |         |           |         |        | than any        | existing | method.   | Furthermore, |     | it also        | scales | to real- |
| tationally | expensive  | tools.   | We show | that this | new map | can    |                 |          |           |              |     |                |        |          |
|            |            |          |         |           |         |        | world settings, |          | including | kitchen      | and | narrow-passage |        | cabinet- |
be developed online in unknown environments based on local like environments.
| observations. | Once   | the      | arrival time | field map        | is generated, |        |     |     |     |             |     |     |     |     |
| ------------- | ------ | -------- | ------------ | ---------------- | ------------- | ------ | --- | --- | --- | ----------- | --- | --- | --- | --- |
| it can enable | motion | planning | that         | is significantly |               | faster | in  |     |     |             |     |     |     |     |
|               |        |          |              |                  |               |        |     |     | II. | RELATEDWORK |     |     |     |     |
| computation   | times  | than     | any existing | method.          |               |        |     |     |     |             |     |     |     |     |
The arrival time is determined by solving the Eikonal Mapping the environment encodes the basic kinematic con-
equation,asdescribedindetailinSectionIII.Thearrivaltime straints for motion planning. Commonly, these constraints
represents the shortest travel time from a starting point to a are used for collision avoidance, which dominates the com-
destination.Thegradientsofthearrivaltimeguidethegenera- putational cost in motion planning [5]. Map representations
tionofacontinuousshortestpathformotionplanning[41,56]. could be obstacle representations like point clouds. They are
For example, the Fast Marching Method (FMM) solves the surface geometry, which is easily gathered from the sensor’s
Eikonal equation via grid search over discretized space for back-projected rays [45]. However, they are impractical for
path planning [56, 66, 67]. However, these methods do not motion planning due to collision querying with logarithmic
scale to higher-dimensional robot configuration space. Recent computational times of map size [6, 46], especially for raw
methods solve the Eikonal equation via neural networks in real-world data. Signed Distance Field (SDF) and truncated
continuous space and scale to higher dimensional motion SDF provide an alternative map representation for collision
planning problems [33, 40, 41, 42, 57]. Their results show avoidance to compute distance in constant time. They can be
thatthearrivaltimefieldsallowpathplanningmuchfasterthan quickly constructed by fusing depth measurements [38, 39].
any other motion planner. However, these methods require a These methods are grid-based and are limited to a large
known environment and infer arrival time fields through the resolution due to computational and memory costs [21, 44].
offline training of neural networks. Additionally, their process Recently, neural fields have emerged as suitable environ-
to solve the Eikonal equation is either slow or prone to errors ment representations due to their compactness and continuity
in complex environments, making them unsuitable for online property [11, 36, 47]. They use a neural network to map a
applications.FormoredetailsonthesepreviousneuralEikonal coordinate to some signal like occupancy or distance [70],
equation solvers, please refer to Section III. Experimental andtheycanbetrainedfromscratchtoaccuratelyfitaspecific
comparisons with previous methods are provided in Section scene [2, 58, 72]. Besides offline reconstruction tasks, neural
| V.  |     |     |     |     |     |     | fields can | also | be trained | in  | real-time | as part | of a | SLAM |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ---- | ---------- | --- | --------- | ------- | ---- | ---- |
In contrast to these earlier methods that require a known system [45, 54, 60, 74]. For instance, iMAP [60] was the first
environment and a computationally intensive training process, worktoreconstructthemapbyreal-timecontinuallearningof
the solution to the mapping problem demands a fast, efficient, neural radiance fields. Similarly, iSDF [45] reconstructed the
andreliablemethodologyforgeneratingamapofanunknown signed distance field in unknown environments.
| environment. | Therefore, |     | the objective | of this | work is | to solve |     |     |     |     |     |     |     |     |
| ------------ | ---------- | --- | ------------- | ------- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
WhiletheSDFexcelsinperformingefficientbatchcollision
the Eikonal equation using a neural network in unknown queries,findingpathswithintheenvironmentstillrequiresthe
environments based on local observations without relying on incorporation of motion planning methods such as sampling-
costly training strategies and complex loss functions. based methods (SMP) [7, 26, 27] and trajectory optimization
To achieve the above-mentioned objectives, this paper in- (TO) [3, 68]. SMP still suffer from significant computation
troduces a novel approach called Active Neural Time Fields times in high-dimensional space, and they struggle to find
(Active NTFields), which quickly maps the arrival time fields optimal, even valid results due to low sampling efficiency
in unknown environments in an online manner and uses them [20,50,61].Incontrast,iterativeoptimizationinTOrelieson
| for real-time | motion | planning | in  | complex environments. |     | The |                       |     |     |               |     |                |              |     |
| ------------- | ------ | -------- | --- | --------------------- | --- | --- | --------------------- | --- | --- | ------------- | --- | -------------- | ------------ | --- |
|               |        |          |     |                       |     |     | initial trajectories, |     | but | the solutions |     | are not global | trajectories |     |
maincontributionsofourproposedworkarelistedasfollows: andfrequentlyconvergetolocalminima[30,43,55,75].This
A new mapping feature called arrival time fields, which issue persists in neural environment representations, such as
●
| allowsfastmotionplanningandscalestohigherdimensional |     |     |     |     |     |     | neural SDF | [1, | 8]. |     |     |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
robot configuration space. Oneexceptionisroadmap-basedSMPs[7,25],whichshare
● A novel framework that actively explores the unknown the same philosophy of building a map suitable for motion
environment and uses only local perception data to train planning.Forexample,PRMcanbeseenasamappingmethod
neural networks on the fly to map the arrival time field of that maps the collision-free C-Space by graph construction.
the given, unknown environment. Recent work also shows its effectiveness in constructing
A fast motion planning method that does not require any collision-freegraphsinunknownenvironmentsthroughexplo-
●
complex tools and instead directly uses the gradients of the ration [18, 71, 73]. However, the explicit graph representation

3
is discrete, which means that the start and goal positions are The robot configuration space is indicated as Q ∈ Rd with
approximated to the nearest nodes in the graph, and it can dimension d, where Q obs and Q free indicate the obstacle and
be computationally demanding to scale to high-dimensional obstacle-free space. The objective of environment mapping is
configuration spaces. Additionally, motion planning on the for a robot to explore environment X to recover its features
constructed graph relies on graph search algorithms and often F [59, 65]. The traditional mapping methods describe the
requires additional trajectory optimizers to smooth the path. features as maps, indicating obstacles and obstacle-free space
In recent times, Neural Motion Planners (NMP) [19, 23, [59]. The modern approaches also recover the environment’s
28, 48, 49, 51] based on learning have emerged. They prove geometry as the SDF [45, 54]. The SDF provides the signed
efficientinfindingpaths,especiallywithpriorknowledge,and distance of any point in the environment to its obstacle geom-
canscaletohighDOFrobotsystems.Theseplannerstakeraw etry’s surface. These features allow motion planning methods
environmental data, such as point clouds or depth images, as to find a collision-free path connecting a robot’s given start
input and forecast trajectories. However, they are limited by and goal configurations to navigate the mapped environment
theirneedforofflinetrainingbecausetheirtrainingdatarelies [75].Thecollisionavoidanceconstraintsfortherobotpathare
on expert trajectories from traditional planners. Consequently, satisfied by leveraging the environment features F recovered
these methods are unsuitable for real-time mapping scenarios during mapping. However, traditional and modern mapping
where experts are not in the loop. features require an extra computational mechanism to find the
| Perhaps | the closest |     | relevant | mapping | method | is  | the cost- |     |     |     |     |     |     |     |
| ------- | ----------- | --- | -------- | ------- | ------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
robot’smotionpath.Inthispaper,weintroduceanewmapping
to-go map [9, 10, 22, 32, 62]. This map stores the cost-to- feature called the arrival time field, which is the solution to
go function in C-Space coordinates, and the gradients of this the Eikonal equation.
function guide motion planning paths. Traditionally, the cost- TheEikonalequationisafirst-ordernon-linearequationthat
to-go function relies on discrete representations of free space represents a robot moving from a start q to a goal q within
|               |            |     |         |           |     |          |        |         |            |      |         |      | s                     | g   |
| ------------- | ---------- | --- | ------- | --------- | --- | -------- | ------ | ------- | ---------- | ---- | ------- | ---- | --------------------- | --- |
| environments, | calculated |     | through | wavefront |     | [56, 66, | 67] or |         |            |      |         |      |                       |     |
|               |            |     |         |           |     |          |        | a speed | constraint | S(q) | defined | over | robot configurations. |     |
diffusionmethods[10,14,16,17].However,thesemethodsare The speed function outputs a scalar value and is designed so
inefficient and challenging to scale for high DOF conditions. that the robot’s speed is high in the free space and low near
Learning-based approaches have been suggested to learn the the obstacle region. The Eikonal equation relates the speed
cost-to-go function on grid [9, 62] or continuous space [22, constraint to the robot arrival time T between the start q and
s
32].Unfortunately,theynecessitateexpertcost-to-gofunctions
|                                                         |           |     |     |     |     |     |     | goal q | g , i.e., |     |     |         |     |     |
| ------------------------------------------------------- | --------- | --- | --- | --- | --- | --- | --- | ------ | --------- | --- | --- | ------- | --- | --- |
| assupervisiondata,leadingtotime-consumingdatageneration |           |     |     |     |     |     |     |        |           |     | 1   |         |     |     |
|                                                         |           |     |     |     |     |     |     |        |           |     | =∥∇ | T(q     | )∥  |     |
| and offline                                             | training. |     |     |     |     |     |     |        |           |     |     | qg s ,q | g   | (1) |
|                                                         |           |     |     |     |     |     |     |        |           | S(q | )   |         |     |     |
g
| Recently, | physics-informed |     |     | neural | networks | (PINN) | [52] |     |     |     |     |     |     |     |
| --------- | ---------------- | --- | --- | ------ | -------- | ------ | ---- | --- | --- | --- | --- | --- | --- | --- |
have emerged as promising tools for motion planning. They The solution of the above PDE is the shortest arrival time
findpathsolutionsinafractionofasecondanddonotrequire between the given start and goal. The prior methods solved
expensive expert trajectories for learning. NTFields [41] and the above equation using the grid-based FMM to recover the
its variant P-NTFields [40] are the first of these methods that shortestpathbasedonarrivaltimebetweenthegivenstartand
| directly | learn to | solve | the Eikonal | equation |     | without | needing |      |          |               |       |         |        |            |
| -------- | -------- | ----- | ----------- | -------- | --- | ------- | ------- | ---- | -------- | ------------- | ----- | ------- | ------ | ---------- |
|          |          |       |             |          |     |         |         | goal | [56, 66, | 67]. However, | these | methods | lacked | continuity |
expert trajectories. The solution of the Eikonal equation is an and were computationally intractable in higher dimensional
arrival time field between the given start and goal. The arrival spaces. Recent work introduced a Laplacian-based viscosity
timefieldisatypeofcost-to-gofunctionwhosegradientslead termintheEikonalequationandanewfactorizedformulation
to a path solution. The NTFields were limited by the com- of arrival time, which allowed for solving Eq. 1 using neural
| plex loss | landscape   | of       | the Eikonal | equation.     |     | The P-NTFields |            |          |      |          |            |         |         |              |
| --------- | ----------- | -------- | ----------- | ------------- | --- | -------------- | ---------- | -------- | ---- | -------- | ---------- | ------- | ------- | ------------ |
|           |             |          |             |               |     |                |            | networks | [40, | 41]. The | factorized | arrival | time is | described as |
| extended  | the Eikonal | equation |             | via Laplacian |     | and            | introduced | follows: |      |          |            |         |         |              |
progressivespeedschedulingtoguideneuralnetworklearning. ∥q −q ∥
|     |     |     |     |     |     |     |     |     |     |     |       | s   | g   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     |     | T(q | ,q )= |     |     | (2) |
However, these additions significantly increased the training s g τ(q ,q )
s g
| time of | P-NTFields, | making | it  | unsuitable | for | online | mapping |     |     |     |     |     |     |     |
| ------- | ----------- | ------ | --- | ---------- | --- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- |
tasks of unknown environments. The neural network predicts τ for the given start and goal to
In this paper, we propose an innovative framework named parameterize the above equation, which leads to arrival time
Active NTFields, incorporating a new formulation of the T and its gradient. When the target point is in the obstacle
|         |          |           |     |              |              |     |     | space, | the τ | is predicted | to be | 0, making | T very | large, and |
| ------- | -------- | --------- | --- | ------------ | ------------ | --- | --- | ------ | ----- | ------------ | ----- | --------- | ------ | ---------- |
| Eikonal | equation | alongside | a   | novel neural | architecture |     | and | a      |       |              |       |           |        |            |
loss function without the need for Laplacian or curriculum when the target is the same as the start, ∥q −q ∥ is 0, making
|     |     |     |     |     |     |     |     |     |     |     |     |     | s g |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
learning. Our framework facilitates rapid active learning and arrival time T equal to zero. The estimated arrival time T
efficient mapping of neural time fields within unknown envi- and its gradient are then used to predict the speed using the
ronments.Oncelearned,thesetimefieldsallowpathfindingin following viscosity Eikonal equation with a Laplacian [15].
| a negligible | amount | of  | time, much | faster | than | state-of-the-art |     |     |     |     |     |     |     |     |
| ------------ | ------ | --- | ---------- | ------ | ---- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
1
| motion | planners. |     |     |     |     |     |     |     |     | =∥∇ | T(q ,q | )∥+ϵ∆ | T(q ,q | ), (3) |
| ------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | ----- | ------ | ------ |
|        |           |     |     |     |     |     |     |     | S(q | )   | qg s   | g     | qg s   | g      |
g
|     |     | III. | BACKGROUND |     |     |     |     |       |        |                 |     |           |             |          |
| --- | --- | ---- | ---------- | --- | --- | --- | --- | ----- | ------ | --------------- | --- | --------- | ----------- | -------- |
|     |     |      |            |     |     |     |     | where | ϵ is a | hyperparameter. |     | The above | formulation | is semi- |
Let the environment be denoted as X ∈ R3 with its obsta- linear elliptic and has a unique solution around obstacles.
|     |     |     |     | X   | X   |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
cle and obstacle-free space as obs and free , respectively. Finally, the predicted speed is compared against the following

4
SpeedField PosedSensor TimeField convergence to an incorrect solution. The Laplacian is com-
|     |     |     |     |     |     |     | putationally |          | expensive       |         | to calculate | as       | it requires |             | the second |
| --- | --- | --- | --- | --- | --- | --- | ------------ | -------- | --------------- | ------- | ------------ | -------- | ----------- | ----------- | ---------- |
|     |     |     |     |     |     |     | derivation   |          | of the          | neural  | network,     | and      | the         | progressive | speed      |
|     |     |     |     |     |     |     | scheduling   |          | requires        | a large | number       | of       | training    | epochs.     | Both       |
|     |     |     |     |     |     |     | strategies   |          | make P-NTFields |         | unsuitable   |          | when        | aiming      | for a fast |
|     |     |     |     |     |     |     | mapping      | approach |                 | that    | learns       | to infer | the         | arrival     | time field |
1/S=∥∇T∥ of the environment on the fly. Hence, we introduce a new
T
|     |     |     |     |     |     |     | factorization |     | of the | arrival | time | as described |     | in the | following. |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ------ | ------- | ---- | ------------ | --- | ------ | ---------- |
qs
|     |     |      | C-Space |     | TimeField |     |     |     |     |              |     |          |     |      |     |
| --- | --- | ---- | ------- | --- | --------- | --- | --- | --- | --- | ------------ | --- | -------- | --- | ---- | --- |
|     |     | γ(⋅) | Encoder |     | Generator |     |     |     | T(q | ,q )=log(τ(q |     | ,q ))2∥q |     | −q ∥ | (5) |
|     | qg  |      |         |     |           |     |     |     |     | s g          |     | s g      | s   | g    |     |
|     |     |      | f(⋅)    |     | g(⋅)      |     |     |     |     |              |     |          |     |      |     |
∇T
|      |          |                   |                     |       |               |        | It can                                        | be seen | that    | we replace |            | 1/τ in     | Eq. 2    | with log(τ)2. | The         |
| ---- | -------- | ----------------- | ------------------- | ----- | ------------- | ------ | --------------------------------------------- | ------- | ------- | ---------- | ---------- | ---------- | -------- | ------------- | ----------- |
|      |          |                   |                     |       |               |        | latterismoreflattenedandchangeslesssteeplyasτ |         |         |            |            |            |          |               | decreases,  |
| Fig. | 2:       | The process       | begins by capturing |       | the scene     | from   |                                               |         |         |            |            |            |          |               |             |
|      |          |                   |                     |       |               |        | preventing                                    |         | sharp   | features   | near       | obstacles. |          | We show       | in our      |
| the  | camera’s | current viewpoint | and sampling        |       | C-space       | points |                                               |         |         |            |            |            |          |               |             |
|      |          |                   |                     |       |               |        | experiments                                   |         | that    | the new    | definition |            | recovers | accurate      | arrival     |
| q    | and      | q . Each sampled  | point pair          | (q ,q | ) is then     | input  |                                               |         |         |            |            |            |          |               |             |
| s    |          | g                 |                     | s     | g             |        |                                               |         |         |            |            |            |          |               |             |
|      |          |                   |                     |       |               |        | time                                          | fields  | without | needing    | Laplacian  |            | or       | speed         | scheduling. |
| into | the      | neural network,   | as shown in         | Fig.  | 3, to predict | the    |                                               |         |         |            |            |            |          |               |             |
Furthermore,bysolvingtheEikonalequation(Eq.1)viachain
| corresponding |     | arrival times | T. The predicted |     | speed | field | is  |     |     |     |     |     |     |     |     |
| ------------- | --- | ------------- | ---------------- | --- | ----- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
derived using the Eikonal equation, as detailed in Eq. 6. The rule with the new arrival time definition in Eq. 5, the speed S
|     |     |     |     |     |     |     | becomes | as  | follows: |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | -------- | --- | --- | --- | --- | --- | --- |
neuralnetworkistrainedbasedonthelossbetweentheground
| truth     | speed | and the predicted  | speed,              | as outlined | in             | Eq. 12. |     |     |        |     |          |     |       |        |     |
| --------- | ----- | ------------------ | ------------------- | ----------- | -------------- | ------- | --- | --- | ------ | --- | -------- | --- | ----- | ------ | --- |
|           |       |                    |                     |             |                |         |     | S(q | )=1/∥∇ |     | (log(τ(q | ,q  | ))2∥q | −q ∥)∥ | (6) |
|           |       |                    |                     |             |                |         |     |     | g      | qg  |          | s   | g     | s g    |     |
| Finally,  |       | the next viewpoint | is selected         | using       | an exploration |         |     |     |        |     |          |     |       |        |     |
| strategy, |       | and the local      | arrival time fields | guide       | the            | robot   | to  |     |        |     |          |     |       |        |     |
that viewpoint without requiring any external motion planner. B. Neural Model Design
This process repeats until the entire environment is observed Ourneuralarchitectureisinspiredbyspectraldistance(SD)
| and    | its | arrival time fields  | are reconstructed. |     |               |     |             |           |                   |          |             |         |           |         |            |
| ------ | --- | -------------------- | ------------------ | --- | ------------- | --- | ----------- | --------- | ----------------- | -------- | ----------- | ------- | --------- | ------- | ---------- |
|        |     |                      |                    |     |               |     | formulation |           | [13,              | 34]. The | SD          | d (q ,q | ) between |         | two points |
|        |     |                      |                    |     |               |     |             |           |                   |          |             | w s     | g         |         |            |
|        |     |                      |                    |     |               |     | q and       | q         | is an approximate |          | alternative |         | to an     | arrival | time with  |
| ground |     | truth speed function | S∗ via isotropic   |     | loss function |     | to s        | g         |                   |          |             |         |           |         |            |
|        |     |                      |                    |     |               |     | the         | following | form:             |          |             |         |           |         |            |
| train  | the | neural network.      |                    |     |               |     |             |           |                   |          |             |         |           |         |            |
∞
|     |     | s   |     |     |     |     |     |     |     | )2=∑w(λ |     |     |     | ))2, |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | ---- | --- |
S∗(q)= const ×clip(d(q,X ),d ,d ) (4) d w (q s ,q g i )(ϕ i (q s )−ϕ i (q g (7)
|     |     |     | obs | min | max |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | d   |     |     |     |     |     |     |     |     | i=1 |     |     |     |     |
max
The function d provides the minimum distance from robot where ϕ (⋅) and λ are the eigenfunctions and eigenvalues,
|     |     |     |     |     |     |     |     | i   |     | i   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
pointsofC-SpacepointqtotheobstacleX respectively, of the Laplace operator ∆ in the given collision-
obs ,clippedbetween
user-defined thresholds d and d , and scaled by factor freespaceandw(⋅)isaweightfunction.Theeigenfunctionof
min max
s . Note that the output of S∗ is a scalar value and is the Laplace operator in the given collision-free space implies
const
|     |     |     |     |     |     |     | −∆  | ϕ (q) | = λ ϕ | (q) | q   | ∈ Q |     | ∇   | ϕ (q) = 0 |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | --- | --- | --- | --- | --- | --------- |
based on the minimum distance of robot configuration to the q i i i when free , whereas n i
obstacle. Once the neural network is trained, it provides the when q ∈ ∂Q and ∇ denotes the directional derivative
|     |     |     |     |     |     |     |     |     | free |     | n   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
alongtheoutwardnormalofthecollision-freespaceboundary.
| arrival | time | field between | any given start | and | goal, | leading | to  |     |     |     |     |     |     |     |     |
| ------- | ---- | ------------- | --------------- | --- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
a path solution. For further details, refer to [40, 41]. In practice, the spectral distance is computed using the k
|     |     |     |     |     |     |     | smallest | eigenvalues |     | and | their | corresponding |     | eigenfunctions. |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | --- | --- | ----- | ------------- | --- | --------------- | --- |
IV. PROPOSEDMETHOD Although SD does not produce the exact shortest arrival time,
|     |     |     |     |     |     |     | it provides |     | a robust | global | approximation |     | sufficient |     | to retrieve |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | -------- | ------ | ------------- | --- | ---------- | --- | ----------- |
This section presents our proposed framework for actively a path solution, as illustrated in Fig. 4. This attribute of SD to
mappingthearrivaltimefieldoftheenvironmentandutilizing
captureglobalstructureinspiresourneuralarchitecturedesign
itforpathplanning.Thekeycomponentsandtheirintegration to capture the global structure of the time field.
| into | a   | unified Active | NTField framework |     | are described | as  |      |     |             |     |          |            |     |            |         |
| ---- | --- | -------------- | ----------------- | --- | ------------- | --- | ---- | --- | ----------- | --- | -------- | ---------- | --- | ---------- | ------- |
|      |     |                |                   |     |               |     | This | SD  | formulation |     | inspires | our neural |     | time field | network |
follows.
|     |     |     |     |     |     |     | to approximate |                  |     | the shortest | arrival | time.        | To  | further | improve |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ---------------- | --- | ------------ | ------- | ------------ | --- | ------- | ------- |
|     |     |     |     |     |     |     | its            | representational |     | capacity,    |         | we integrate |     | random  | Fourier |
A. New Time Field Factorization positional encoding [63] with the SIREN neural network
|                                         |             |                   |                       |         |                  |           | architecture |       | [58].   |            |     |          |      |          |           |
| --------------------------------------- | ----------- | ----------------- | --------------------- | ------- | ---------------- | --------- | ------------ | ----- | ------- | ---------- | --- | -------- | ---- | -------- | --------- |
|                                         | Although    | the factorization | in Eq. 2              | has the | desirable        | prop-     |              |       |         |            |     |          |      |          |           |
|                                         |             |                   |                       |         |                  |           |              |       |         |            | ∈ Q |          |      | ∈        | Q         |
|                                         |             |                   |                       |         |                  |           | Given        | the   | robot   | start      | q s | free and | goal | q g      | free , we |
| ertiesformotionplanning,thearrivaltimeT |             |                   |                       |         | increasessteeply |           |              |       |         |            |     |          |      |          |           |
|                                         |             |                   |                       |         |                  |           | obtain       | their | Fourier | positional |     | encoding | as   | follows: |           |
| as                                      | τ decreases | to zero.          | Hence, when computing |         | the              | gradients |              |       |         |            |     |          |      |          |           |
of Eq. 1 to train the neural network, the sharp features around γ(q )=[cos(2πcTq ),sin(2πcTq )]
|     |     |     |     |     |     |     |     |     | s   |     |     | s   |     | s   | (8) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
obstaclesoftenleadtoincorrectlocalminima.Therefore,inP-
|                                                     |     |     |     |     |     |     |     |     | γ(q | )=[cos(2πcTq |     | ),sin(2πcTq |     | )], |     |
| --------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ----------- | --- | --- | --- |
| NTFields[40],aLaplacianterminEq.3andaspeedscheduler |     |     |     |     |     |     |     |     | g   |              |     | g           |     | g   |     |
wasintroduced.TheformerleadstoauniqueEikonalequation where c is a fixed latent random code. These encodings
solution, whereas the latter progressively reduces the speed are then passed through the SIREN neural network, denoted
around obstacles as the training epoch increases to prevent as f, which is a multilayer perceptron with sine activation

5
functions. The sine activation function captures the high- q f(γ(qs)),f(γ(qg))
frequency features and allows smooth differentiation for gra-
dient computation in our method. Let the combination of
positional and SIREN be defined as Φ(q) = f(γ(q)). Next, Positionalencodingγ(q) SymmetricOperator⊗
as inspired by Eq. 7, we subtract these features and take a
[cos(2πcTq),sin(2πcTq)] (f(γ(qs))−f(γ(qg)))2
square, i.e.,
Φ(q )⊗Φ(q )=(Φ(q )−Φ(q ))2, where
s g s g
(9)
Φ(q )=f(γ(q )),Φ(q )=f(γ(q ))
s s g g
FC+Sine (FC+Softplus)×3
The above squared subtraction is also relevant to the sym-
256×128 128×128
metric operator introduced in NTFields [41]. This operator
enforces the arrival time field’s symmetric property, i.e., the
arrivaltimefromstarttogoalandfromgoaltostartshouldbe
the same. Specifically, let latent encodings of start and goal (FC+Sine)×3 FC+Sigmoid
configurations be denoted as a and b. The symmetric operator
128×128 128×1
in [41] was defined as the concatenation of min and max,
i.e., [max(a,b),min(a,b)]. The other choice of symmetric
operators could be subtraction, addition, or averaging. Hence,
the squared subtraction operator in Eq. 9, inspired by spectral
C-Spacefeaturef(γ(q)) TimeFieldg(⋅)
distance, also acts as a symmetric operator, ensuring the
(a) C-Space Encoder (b) Time Field Generator
symmetric property of the arrival time field. Furthermore,
we observed that the squared subtraction operator instead of Fig. 3: Our Neural Architecture: The fully connected (FC)
concatenationofminandmaxreducesthefeaturesize,leading layer, with the shape depicted below, forms the core of our
to neural network training efficiency. Finally, the resulting network. We employ several activation functions, including
featuresfromEq.9aregiventoanothermulti-layerperceptron, Sine,Softplus,andSigmoid.In(a),q representsapointinthe
denoted as g, that predicts the τ. In summary, our neural time configuration space, γ(⋅) denotes a positional embedding, and
field network with parameters θ is summarized as follows: f(⋅) (shown in gray) represents a C-space embedding, as also
depicted in Fig. 2. In (b), g(⋅) (shown in brown) represents
τ θ (q s ,q g )=g(Φ(q s )⊗Φ(q g )) (10) the factorized time field, which also appears in Fig. 2.
As highlighted in Eqs. 9-10 and Fig. 2, our model has four
parts,i.e.,thepositionalencoderγ(⋅),configurationspace(C-
goal are then utilized to train the network by comparing them
Space) encoder f(⋅), symmetric operator ⊗, and time field
against the expert speed model, as described in Section III.
generator g(⋅). The positional encoder, γ(q), takes a given
configuration q and outputs the Fourier features, according to
Eq. 8. In our implementation, these features are of size 256
D. Path Inference
units. These features are then passed through function f(⋅),
whichcomprisesfourfullyconnected(FC)layersfollowedby Once the neural time field network is trained, we utilize its
SineactivationtoproduceC-Spacefeatures,i.e.,f(γ(q)).The predictionsandgradientstorecoverthepathsolutionbetween
numberofhiddenunitsofFClayersinfunctionf(⋅)is128,as any start and goal as follows. First, the network predicts
alsoindicatedinFig.3(a).Byfollowingtheabove-mentioned τ(q s ,q g ), and we use it to predict speeds (Section IV-A) and
procedure, we obtain the C-space features of both start and also to parameterize Eq. 5 to determine the arrival time field
goal configurations, i.e., f(γ(q s )) and f(γ(q g )). Next, the T(q s ,q g ).Next,werecoverthepathsolutioninthesameway
SymmetricOperator⊗preservestheinvarianceandsymmetry as in NTFields [41], i.e., we follow gradients bidirectionally
property when switching the start and goal configurations by from start to goal and from goal to start as described below:
subtracting and squaring the C-space encodings (Fig. 3 (b)).
q ←q −αS2(q )∇ T(q ,q )
Finally, the time field function g(⋅) takes the symmetrized s s s qs s g (11)
q ←q −αS2(q )∇ T(q ,q )
latent embedding and processes them through multiple FC g g g qg s g
and Softplus blocks to output a Sigmoid value representing
The α is a user-defined step-size scaling factor. The above
the factorized time field. The number of hidden units of FC
iterative procedure is repeated until the waypoints from the
layers in function g(⋅) is 128 (Fig. 3 (b)).
start and the goal are within the threshold. It should be
emphasizedthatgradientdescentdoesnotensureconvergence,
C. Speed Inference
and the algorithm may terminate unsuccessfully after a prede-
The neural framework mentioned above predicts τ(q ,q ) fined number of iterations. To address this issue, the learned
s g
for the given start and goal pairs. We use the predicted arrival time field maps can also be used more robustly by
τ and its gradients with respect to start ∇ τ(q ,q ) and incorporating them into search [24] or optimization [4, 69]
qs s g
goal ∇ τ(q ,q ) to estimate the speeds S(q ) and S(q ) techniques. These methods will guided by the learned arrival
qg s g s g
according to Eq. 6. These predicted speeds at the start and time field map, yielding effective path solutions fast.

6
E. Active Neural Time Fields sample points q and their expert speed values S∗ .
{n} {n}
2) Online Training: Note that our data arrives in streams.
Thissectiondescribesourapproachtogatheringdataonline Therefore, we maintain a memory buffer, M, that stores all
in unknown environments for training our neural network on
sample points and their ground truth speed gathered over
thefly.Thepriorworkassumestheenvironmenttobeknown,
time. However, training the timefield neural network on the
and therefore, the dataset for training the neural time field
complete memory is computationally expensive. Therefore,
models is gathered offline. The dataset comprises randomly
we randomly sample a batch of points and their ground truth
sampled start and goal points and their ground truth speed speed from the memory. Let the batch be denoted as B⊂M,
values. As described in Section IV-A (Eq. 4), the ground
comprisingsamplepointsandtheirgroundtruthspeedvalues.
truth speed S∗ is computed for each sampled point based on Next,weaugmentthememorybuffer,M=M∪(q ,S∗ ),
its minimum distance from the obstacles. The NTFields [41] and the batch buffer, B = B∪(q ,S∗ ) , with {n n } ew { d n a } ta.
and P-NTFields [40] can directly acquire this distance from {n} {n}
We randomly shuffle the batch buffer and form pairs of
a known environment by calculating the distance between the
consecutive points. These pairs act as start and goal points
point and the nearest obstacle mesh. However, in our setting,
for training our neural model. The neural network trains on
the environment is unknown, and the robot needs to explore,
these pairs for a fixed number of iterations. Note that buffer
obtain data, and determine its ground truth speed values to
B contains samples from new and old perception data, and
train the neural networks. Therefore, this section provides
random shuffling allows start and goal pairs to spread across
procedurestoactivelycreatesuchdataanddefinetheirground
different parts of the observed environment. Hence, it allows
truth speed for online training of our neural networks.
neural networks to learn to generate the arrival time field of a
1) Local Perception Processing: Our local perception pro- fully observed environment over time.
cessingisinspiredbytheiSDFframework[45].Therawinput Wepassthesampledstartandgoalpairsthroughourneural
of data comprises robot odometry and the sensor readings. time field network to obtain the τ. The τ and its gradients
We assume the sensor data to be either lidar-based scanning parametrize Eq. 6 to infer the speed S (Section IV-A). Next,
or depth images. The lidar provides scanning in the form of we compute the loss of predicted speed against ground truth
rays.Iftheperceptionisfromdepthimages,wesamplepixels speedanduseittotrainourneuralnetworksforafixednumber
and convert them to rays using the camera intrinsic matrix. of iterations.
√
Furthermore,wetransformtheseraystoworldcoordinatesand
L(S∗,S)=( S∗(q )/S(q )−1)2+
randomly select N number of rays from the given scan. For √ s s (12)
each ray, we sample m ∈ N stratified points along its range. ( S∗(q g )/S(q g )−1)2
Thismeansthateachrayoflengthl∈Rwillbesplitintol/m
Notethattheabovelossfunctionisdifferentfromtheisotropic
bins, and in each bin, we will select one sample. Hence, we loss function used in prior work [40, 41]. Since we proposed
gather n ∈ N sample points, denoted as x {n} ⊂ X, from N amoreflattenedversionoffactorizedtime,weexpecttheloss
rays. tobealsoflattened.Therefore,ournewlosswithsquaredroot
Next, we need to determine the ground truth speed values and square makes the loss smoother and more flat than MSE
for all sampled points. In our setting, the actual minimum and isotropic loss functions. We observed that our new loss
distance to the nearest obstacle is unknown since the envi- function aids in training our neural network faster than prior
ronment will only be partially observed during exploration. loss functions introduced by NTFields [41] and P-NTFields
This contrasts with prior methods where the environment [40].
mesh is provided, and the nearest distance to obstacles is 3) Next Viewpoint Selection: Upon training the neural net-
readily available. Therefore, in our framework, we revert to work with the given local perception data, the next step is to
approximating the minimum distance of sampled points to select the subsequent viewpoint for acquiring new observa-
the obstacles. We calculate the distance between the point tions. Active exploration involves choosing the next optimal
and the nearest surface point in the given scan. Although viewpoint to collect data using the robot’s onboard sensor. As
using all lidar points or depth points can be more accurate for thisworkdoesnotaimtodevelopnovelexplorationstrategies,
distanceestimation,itiscomputationallyexpensive.Therefore, we utilize a standard approach to maximize scene coverage.
we only use N sampled rays to select the nearest obstacle During exploration, we maintain an occupancy map. Re-
surface. For 3D point robot, workspace sampled points x gions of the map are marked as explored once the robot’s
{n}
aretheC-Spacepointsq .However,inthecaseofahigher- sensor gathers sufficient information, while the remaining
{n}
dimension manipulator, we need a further operation to get areas are labeled as unexplored.
C-Space samples and their expert speed values. Specifically, To determine the next best view for exploration, we ran-
we use x as the manipulator end effect positions and domly sample collision-free points from the frontier of the
{n}
determine their configuration samples q via inverse kine- explored occupancy map, considering these as candidates for
{n}
maticsolution.Next,fortheseC-Spacesamples,wedetermine the next best view. We then compute the arrival time to these
the robot surface points to compute the minimum distance pointsusingourneuralmodelfromtherobot’scurrentlocation
to the obstacle. Once the approximate minimum distance of and select the point with the minimal arrival time. The path
all sampled points from the obstacle is available, we define from the robot’s current location to this next best view is
the expert speed model based on Eq. 4 (Section IV-A). In calculatedusingthearrivaltimefield,followingtheprocedure
summary, this module processes local perception, creating described in Section IV-E.

7
FMM Ours P-NTFields NTFields SD
Fig. 4: We compare our method with NTFields, P-NTFields, FMM, and SD on a maze environment for time field generation.
Our method recovers the correct result within 15 seconds, whereas P-NTFields and NTFields take 18 and 10 minutes,
respectively. Although SD does not recover the exact time field, it provides a smooth global approximation, which inspired
aspects of our architecture design.
Algorithm 1 Active NTFields Online Learning observations from a given viewpoint and processing them to
Require: get sample points q and their expert speed estimates S∗
{n} {n}
1: ● Odom data ▷ Robot odometry data (lines3-7).Thesesamples,alongwithsomepastsamplesfrom
● Lidar or depth images ▷ Sensor readings M,arethenusedtotrainthenetworkonlineforafewepochs
● N ▷ Number of rays (lines 9-15). Once trained, the next best viewpoint (NBV) is
● m ▷ Number of stratified points per ray selected, and the path to NBV is generated using the learn
● M ▷ Memory buffer arrivaltimefieldmap(lines17-18).Theprocedureisrepeated
● B ▷ Batch buffer untiltheunknownenvironmentisexploredanditsarrivaltime
● θ ▷ Model Parameters field map is recovered. In our implementation, we choose
● τ θ (⋅) ▷ Neural network model iterator j to go until 5 steps with the batch size of 2000
● S∗ ▷ Ground truth speed samples. Furthermore, we use AdamW [35] with weight 1e-1
2: for i=1,... do ▷ Unknown Environment Exploration and learning rate 5e-4 as optimizer.
3: Obtain odom and sensor data from a given viewpoint
4: Transform data to world coordinates V. EXPERIMENTS
5: Sample N rays, each with m stratified points
6: Gather n samples q ⊂Q from N rays (IV-E1) This section presents our experiment analysis. We begin by
{n}
7: ComputeexpertspeedS∗ forsampledpoints(IV-E1) comparing the training efficiency of our proposed method
{n}
8: for j =1,... do ▷ Online Training Epochs IV-E2 against prior physics-informed methods, i.e., NTFields [41]
9: Sample B j from M ▷ Batch train data and P-NTFields [40], to demonstrate the effectiveness of our
10: B j =B j ∪(q {n} ,S { ∗ n} ) ▷ Add new data proposed approach in recovering arrival time fields online.
11: ∀(q s ,q g ,S∗(q s ),S∗(q g ))∈B j ∶ Next, we quantitatively compare the inferred maps from our
12: τ θ (q s ,q g ) ▷ Predict factorized time Eq. 10 proposed approach against state-of-the-art mapping methods.
13: S(q s ),S(q g ) ▷ Predict speed by Eq. 6 Lastly, we demonstrate the effectiveness of learned arrival
14: l j =L(S∗,S) ▷ Compute loss by Eq. 12 time field maps in performing fast motion planning. We also
15: θ=θ−∇ θ l j ▷ Update model parameters demonstrateourapproachinreal-worldsettingsforperforming
bothmappingandmotionplanninginahigher-dimensionalC-
16: M=M∪(q ,S∗ ) ▷ Update memory IV-E2
{n} {n} space. All experiments were performed using a system with
17: SelectNextBestViewpointfromlocaltimefieldIV-E3
3090 RTX GPU, Core i7 CPU, and 128GB RAM.
18: Find a path to NBV by Eq. 11
A. Training Efficiency Analysis
It is important to note that our neural time field genera-
This section demonstrates our method performance over
tor can be seamlessly integrated into any other exploration
NTFields [41] and P-NTFields [40]. Fig. 4 shows the speed
strategy. Since the next best viewpoints typically lie at the
and time fields of our method, NTFields, P-NTFields, and
boundaries between explored and unexplored regions, the
SD in comparison to FMM as ground truth. The color shows
locallylearnedtimefieldscanprovideapathwithouttheneed
the speed fields and the contours show the arrival time fields
for an external path planner.
from a start point. From Fig. 4 contours, our approach and
P-NTFields get a similar result as FMM, while NTFields
F. Active NTFields Online Learning Summary
generate incorrect time fields. Although the SD contours
Algorithm1andFig.2providesourActiveNTFieldsonline are not perfectly aligned with those of FMM, they offer a
training pipeline. The procedure begins with obtaining the smooth and globally consistent approximation of the arrival

8
|     | Ours |     |     | iSDF |     |     | KinectFusion | nvblox |     | Ground | Truth |
| --- | ---- | --- | --- | ---- | --- | --- | ------------ | ------ | --- | ------ | ----- |
Fig. 5: Comparison for mapping in Gibson environments. The figures show two indoor environments’ SDF maps and zero-
level-set mesh generated by our method, iSDF [45], KinectFusion [38], and nvblox [37].
time fields, which inspired elements of our feature design for takes 15 seconds, while P-NTFields and NTFields take 18
learning the shortest arrival times. minutes and 10 minutes, respectively. While our method and
To quantitatively compare the results of all PINN methods, P-NTFields have similar results, the latter is about 72 times
|               |        |          |                 |            |       |       | faster than | the former | in terms of | training speed. | Hence, this   |
| ------------- | ------ | -------- | --------------- | ---------- | ----- | ----- | ----------- | ---------- | ----------- | --------------- | ------------- |
| we sample     | points | from     | their predicted | arrival    | time  | and   | com-        |            |             |                 |               |
|               |        |          |                 |            |       |       | performance | comparison | validates   | our method’s    | effectiveness |
| pute absolute |        | error to | the ground      | truth time | field | value | given       |            |             |                 |               |
by the FMM. Our time fields have an error of 0.044±0.050, and its suitability for online continual learning in mapping
tasks.
| P-NTFields | have     | an            | error of | 0.048 ±   | 0.047,      | and NTFields |     |     |     |     |     |
| ---------- | -------- | ------------- | -------- | --------- | ----------- | ------------ | --- | --- | --- | --- | --- |
| have       | an error | of 0.44±0.42. |          | Note that | the NTField | error        | is  |     |     |     |     |
almosttentimeshigher.Regardingtrainingtimes,ourmethod

9
B. Mapping Comparison PerformanceMetrics
Methods
Thissectiondemonstratesourmethodperformanceonmap- Time(sec)↓ Length↓ SR(%)↑
pingtasksoverKinectFusion[38],iSDF[45],andnvblox[37]. Ours(G) 0.01±0.05 0.48±0.43 98.28
WeuseeightGibsonenvironments[31]todemonstratethe3D LazyPRM(C) 0.34±1.54 0.41±0.22 99.28
iSDF+MPOT(G) 1.42±0.52 0.62±0.27 91.43
mappingofindoorscenes.Duetothethreebaselinesrequiring KFusion+MPOT(G) 0.28±0.08 0.55±0.16 93.71
a given trajectory, we first run our active exploration strategy nvblox+MPOT(G) 0.27±0.05 0.58±0.14 96.57
to obtain a series of depth images and camera poses. With iSDF+RRTConnect(G) 1.44±2.13 0.35±0.20 83.85
KFusion+RRTConnect(G) 0.89±1.36 0.38±0.21 91.57
these raw data, all methods reconstruct the maps of all indoor nvblox+RRTConnect(G) 0.51±0.99 0.39±0.21 88.71
scenes. We compared all other methods over SDF quality KFusion+RRTConnect(C) 0.20±0.48 0.40±0.22 94.71
and mapping efficiency, as our speed fields can be seen as nvblox+RRTConnect(C) 0.27±0.46 0.40±0.22 96.29
truncated SDF. In Fig. 5, we present two environments of
TABLE II: Comparison for motion planning in eight Gibson
SDF and their zero-level-set mesh. Our method, iSDF, and
environments. For each environment, 100 randomly sampled
nvblox capture a similar result as the ground truth, while
starts and goals near obstacles are selected for evaluation.
KinectFusion can only reconstruct the SDF very close to
We load grid-based maps in both CPU (C) and GPU (G) for
the obstacles as it cannot support large truncated regions.
RRTConnect-based approaches.
However, from the zero-level-set mesh, KinectFusion and
nvblox can reconstruct high-quality obstacles, whereas our
method and iSDF cannot capture many details. Note that we
arefocusingonthedownstreammotionplanningapplications,
and rough obstacle details are fine for collision avoidance,
as also validated by our motion planning experiments in the
next section. Table I shows the SDF error and reconstruction
time. To compute the SDF error, we sample points within the
truncatedregionandcalculatetheabsoluteerrorofSDFvalue
againstgroundtruthresults.Inthetable,itcanbeseenthatour
SDF error is similar to iSDF. Regarding mapping efficiency,
although our method is slower than the baseline methods as it
gathers informative features, our mapping time is comparable
with baseline methods and suitable for online tasks.
PerformanceMetrics
SDF
SDFError↓ FrameTime(s)↓ MappingTime(s)↓
Ours 0.09±0.10 2.12±0.06 149.74±18.24
iSDF 0.09±0.11 0.94±0.02 69.90±7.57
KFusion 0.47±0.27 1.71±0.01 126.08±16.06
nvblox 0.07±0.07 0.12±0.00 9.16±3.70
TABLE I: Quantitative comparison of our method against
iSDF [45], Kinect Fusion (KFusion) [38], and nvblox [37]
in mapping the Gibson environments.
C. Motion Planning Comparison
This section demonstrates our method performance on
Fig. 6: Comparison for motion planning in Gibson environ-
motion planning tasks over MPOT [30], RRTConnect with
ments. The figures show five paths generated by our method
smoothing [27], and online LazyPRM with smoothing[7].
(orange), LazyPRM (gray), iSDF+MPOT (red), Kinect-
The MPOT is the most recent and best available method
Fusion+MPOT (cyan), iSDF+RRTConnect (green), Kinect-
that outperformed various state-of-the-art motion planning
Fusion+RRTConnect (yellow), nvblox+MPOT (blue), and
methods.Furthermore,weusethereconstructedmapsofeight
nvblox+RRTConnect(pink).Thetableshowsstatisticalresults
Gibson environments [31] from our mapping results (Section
on 8×100 different starts and goals in eight Gibson environ-
V-B). Hence, two planners, MPOT and RRTConnect, use
ments. We load grid-based maps in both CPU and GPU in
the reconstructed map from iSDF, KinectFusion, and nvblox.
RRTConnect to test the performance. The highlighted region
MPOT is a GPU-based method, and we only load the grid
illustrates that MPOT and RRTConnect may discover longer
map to GPU. Additionally, MPOT was run in batches of 100
paths belonging to a different homotopy class.
trajectories which we select to balance the trade-off between
itssuccessrateandcomputationtime.RRTConnectisaCPU- graph search with smoothing to find the path. In contrast,
based method, and we load the grid map on both GPU and our method can directly generate motion planning paths by
CPU. LazyPRM uses its own reconstructed roadmap and uses following Eq. 11, demonstrating the effectiveness of arrival

10
|     | Start |     |     |     |     |     |     | Intermediate |     |     |     |     |     | Goal |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | ---- | --- |
1 esaC
2 esaC
Fig. 7: Real-world cabinet environment: Our method reconstructed the arrival time fields using the in-hand camera. The top
and bottom rows show two cases of our motion planning problems in this confined environment. The first case shows the
manipulator going into the cabinet, and the second case shows the manipulator crossing the cabinet’s middle level to reach the
given target at the top level. We highlight the end effector to show the narrow passage condition of Case 2. In this scenario,
ourmethodtakesonly0.02secondstofindthepath,whereasLazyPRM(CPU)takes3.72seconds,KinectFusion+RRTConnect
| (CPU) takes | 4.15     | seconds, | and | nvblox+MPOT |     | (GPU) | takes | 4.63 | seconds. |     |     |     |                    |     |     |
| ----------- | -------- | -------- | --- | ----------- | --- | ----- | ----- | ---- | -------- | --- | --- | --- | ------------------ | --- | --- |
| time field  | mapping. |          |     |             |     |       |       |      |          |     |     |     | PerformanceMetrics |     |     |
Methods
We randomly choose 100 start and goal points in each Time(sec)↓ Length↓ SR(%)↑
| environment | and | run | the above-mentioned |     |     | motion | planning |     |     |         |           |     |           |     |       |
| ----------- | --- | --- | ------------------- | --- | --- | ------ | -------- | --- | --- | ------- | --------- | --- | --------- | --- | ----- |
|             |     |     |                     |     |     |        |          |     |     | Ours(G) | 0.03±0.01 |     | 2.25±0.72 |     | 91.00 |
methods to get the final paths. We compare the path length, LazyPRM(C) 1.36±0.81 3.05±0.89 87.00
|     |     |     |     |     |     |     |     |     | iSDF+MPOT(G) |     | 3.63±1.29 |     | 4.04±0.77 |     | 89.00 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --------- | --- | --------- | --- | ----- |
computationaltime,andsuccessrate.Thecollisioncheckingis
|     |     |     |     |     |     |     |     |     | KFusion+MPOT(G) |     | 2.18±0.06 |     | 3.99±0.48 |     | 79.00 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --------- | --- | --------- | --- | ----- |
performedusingtheground-truthmaptovalidatethegenerated
|     |     |     |     |     |     |     |     |     | nvblox+MPOT(G) |     | 2.11±0.39 |     | 4.15±0.56 |     | 88.00 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --------- | --- | --------- | --- | ----- |
|     |     |     |     |     |     |     |     |     |                |     | 3.92±8.20 |     | 2.33±1.04 |     |       |
paths and compute the success rate. We also set a time limit iSDF+RRTConnect(G) 89.00
|               |       |                    |     |         |            |            |     |     | KFusion+RRTConnect(G) |     | 2.71±4.56 |     | 2.18±0.83 |     | 85.00 |
| ------------- | ----- | ------------------ | --- | ------- | ---------- | ---------- | --- | --- | --------------------- | --- | --------- | --- | --------- | --- | ----- |
| of 10 seconds |       | for sampling-based |     | methods |            | LazyPRM    | and |     |                       |     |           |     |           |     |       |
|               |       |                    |     |         |            |            |     |     | nvblox+RRTConnect(G)  |     | 3.16±3.53 |     | 2.30±1.09 |     | 84.00 |
| RRTConnect,   | after | which              | the | case is | considered | a failure. |     |     |                       |     |           |     |           |     |       |
|               |       |                    |     |         |            |            |     |     | KFusion+RRTConnect(C) |     | 1.64±1.35 |     | 2.48±1.21 |     | 82.00 |
Fig. 6 shows the paths where our method and Kinect- nvblox+RRTConnect(C) 1.90±5.63 2.32±0.96 82.00
| Fusion+MPOT |     | generate | short | and | smooth | paths, | but |     |     |     |     |     |     |     |     |
| ----------- | --- | -------- | ----- | --- | ------ | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
TABLEIII:ComparisonformotionplanningintheUR5eMa-
| iSDF+MPOT  | and  | nvblox+MPOT |     | generate |                 | damping | results.  |           |     |                        |     |      |     |          |         |
| ---------- | ---- | ----------- | --- | -------- | --------------- | ------- | --------- | --------- | --- | ---------------------- | --- | ---- | --- | -------- | ------- |
|            |      |             |     |          |                 |         |           | nipulator |     | in cabinet environment |     | with | 100 | randomly | sampled |
| RRTConnect | only | considers   | the | SDF      | zero-level-set; |         | thus, all |           |     |                        |     |      |     |          |         |
startandgoalsnearobstacles.Weloadgrid-basedmapsinboth
| RRTConnect | generate |     | similar | results. | Table | II presents | the |     |     |     |     |     |     |     |     |
| ---------- | -------- | --- | ------- | -------- | ----- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
CPU(C)andGPU(G)inRRTConnecttotesttheperformance.
| statistical | results. | Our | method’s | computational |     | time | is about |     |     |     |     |     |     |     |     |
| ----------- | -------- | --- | -------- | ------------- | --- | ---- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
30 times faster than MPOT and achieves 98% success rate. ourmethod,failureswereduetotheinabilitytofindafeasible
|                  |               |           |               |        |           |          |        | path | without | collisions.       |     |     |     |     |     |
| ---------------- | ------------- | --------- | ------------- | ------ | --------- | -------- | ------ | ---- | ------- | ----------------- | --- | --- | --- | --- | --- |
| In addition,     | our           | method    | generates     | smooth | paths     | with     | a safe |      |         |                   |     |     |     |     |     |
| margin           | to obstacles, | while     | RRTConnect    |        | generates | paths    | close  |      |         |                   |     |     |     |     |     |
|                  |               |           |               |        |           |          |        | D.   | Real    | World Experiments |     |     |     |     |     |
| to the obstacle, |               | resulting | in relatively |        | shorter   | lengths. |        |      |         |                   |     |     |     |     |     |
All sampling-based methods failed in some cases primarily This section presents our real-world experiments with dif-
due to exceeding the time limit. These methods rely on ferential drive TurtleBot4 and 6-DOF UR5E robots.
samplingstrategiesthatcanrequiresignificanttimetoexplore 1) TurtleBot4 in indoor environment: In this experiment, a
| complex | environments |     | and find | a global | collision-free |     | path, |            |     |                |      |              |     |        |         |
| ------- | ------------ | --- | -------- | -------- | -------------- | --- | ----- | ---------- | --- | -------------- | ---- | ------------ | --- | ------ | ------- |
|         |              |     |          |          |                |     |       | TurtleBot4 |     | robot equipped | with | a RealSense2 |     | camera | is used |
especially when narrow passages are present. In contrast, to explore an indoor environment with furniture. The camera
MPOT failed primarily because it was unable to find a global poses are from the TurtleBot4 odometry, while depth images
collision-free path, even when sufficient time was available, are from the RealSense2 camera. Fig. 1 shows our method
as it depends on local optimization, which may get trapped in of incrementally constructing the map with incoming frames.
| local minima | without | a   | global | guarantee. |     |     |     |              |     |            |      |     |               |     |              |
| ------------ | ------- | --- | ------ | ---------- | --- | --- | --- | ------------ | --- | ---------- | ---- | --- | ------------- | --- | ------------ |
|              |         |     |        |            |     |     |     | Furthermore, |     | our method | uses | the | reconstructed |     | arrival time |
Our method, like MPOT, also failed in some cases because field in the partially observed environment to reach the next
it could not find a global collision-free path, but it demon- viewpoint for sensing. Thus, it does not require any external
strated higher robustness and faster convergence. To clarify motionplannerduringmapping.InFig.1,thecolorrepresents
the success rate further, failures for sampling-based methods the speed fields, and the contour lines indicate the time fields.
occurredduetoexceedingthetimelimit,whileforMPOTand It takes 65 seconds for the robot to actively explore and

11
reconstruct the arrival time field of the whole environment. camera for mapping and solving motion planning in a real-
These results highlight the capability of our approach in world narrow passage, cabinet-like environment. We compare
mapping a real-world indoor environment. our framework against state-of-the-art mapping and motion
|      |         |                |     |          |           |     | planning | approaches. |     | The | mapping | results | demonstrate |     | that |
| ---- | ------- | -------------- | --- | -------- | --------- | --- | -------- | ----------- | --- | --- | ------- | ------- | ----------- | --- | ---- |
| Once | the map | reconstruction |     | is done, | any start | and | goal     |             |     |     |         |         |             |     |      |
pairinthemapcanbefedintotheneuralnetwork,andapath our approach can map the environments with arrival time
is generated in a bidirectional way using Eq. 11. To evaluate field features that can directly provide robot navigation paths
our method of motion planning performance, we randomly between any start and goal robot configurations. The motion
sampled 100 starts and goals in the real environment. On planning comparison shows at least 40× speed enhancement
|          |            |             |     |       |          |        | over | the best | available | method. |     |     |     |     |     |
| -------- | ---------- | ----------- | --- | ----- | -------- | ------ | ---- | -------- | --------- | ------- | --- | --- | --- | --- | --- |
| average, | our method | computation |     | times | remained | around | 0.02 |          |           |         |     |     |     |     |     |
seconds with a 98% success rate. Finally, the bottom row of Inourfuturework,weplantoinvestigatecontinuallearning
Fig.1depictsanexamplepath.Wepickthestartlocationnear approaches for training our neural network to explore large-
the sofa and the goal location behind a chair. It takes only scale environments. We also aim to explore ensemble-based
0.02 seconds to generate a valid smooth trajectory, avoiding neural approaches to address the spectral bias issue of neural
| collision | with all | the furniture. |     |     |     |     |          |     |              |     |           |          |     |                |     |
| --------- | -------- | -------------- | --- | --- | --- | --- | -------- | --- | ------------ | --- | --------- | -------- | --- | -------------- | --- |
|           |          |                |     |     |     |     | networks |     | that hinders |     | them from | tackling |     | high-frequency |     |
2) UR5e Manipulator in cabinet environment: We use the featuresthatalsoappearfrequentlyinverylargeenvironments.
UR5e robotic arm with a hand-held RealSense2 camera to A parallel development to our method is a new line of
navigate a realistic cabinet setting. Our approach generates an workrelatedtohardware-acceleratedmotionplanningthatalso
arrival time field map in 6 DOF C-Space and completes this aims to expedite motion planning [64], [53]. These methods
|     |     |     |     |     |     |     | leverage | traditional |     | occupancy | maps. | Therefore, |     | in our | future |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | --- | --------- | ----- | ---------- | --- | ------ | ------ |
processin115seconds.Bycomparison,alternativeworkspace
maps reconstruction methods like iSDF, KinectFusion, and work, we also aim to explore integrating our mapping feature
nvblox require significantly less time – 6 seconds, 2.47 with strategies in hardware-accelerated motion planning to
seconds, and 0.55 seconds, respectively. Note that the time investigate if motion planning speed can be further improved
difference is primarily because our method maps the higher- beyond microseconds. Lastly, we also plan to extend our
|     |     |     |     |     |     |     | framework |     | to outdoor | mapping |     | scenarios, | which | we  | believe |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ---------- | ------- | --- | ---------- | ----- | --- | ------- |
dimensional(6D)C-Space,whereasbaselinemethodsmapthe
3D workspace. The baseline SDF methods cannot scale to C- canopennewwaystosolveautonomousdrivingtaskswithout
Space mapping. Furthermore, the LazyPRM constructed from needing expert demonstrations.
| incremental | local      | observations |           | takes 162 | seconds     | to build | the |     |     |     |     |     |     |     |     |
| ----------- | ---------- | ------------ | --------- | --------- | ----------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| roadmap     | in C-Space | and          | is slower | than      | our method. |          |     |     |     |     |     |     |     |     |     |
REFERENCES
| For motion | planning, |     | we used | the reconstructed |     | map | and |     |     |     |     |     |     |     |     |
| ---------- | --------- | --- | ------- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
conducted tests using 100 randomly selected start and goal [1] Michal Adamkiewicz, Timothy Chen, Adam Caccavale,
pairings near obstacles. Our method demonstrated a quick RachelGardner,PrestonCulbertson,JeannetteBohg,and
|         |          |         |      |         |        |             |     | Mac | Schwager. | Vision-only |     | robot | navigation | in  | a neural |
| ------- | -------- | ------- | ---- | ------- | ------ | ----------- | --- | --- | --------- | ----------- | --- | ----- | ---------- | --- | -------- |
| average | planning | time of | 0.03 | seconds | with a | 91% success |     |     |           |             |     |       |            |     |          |
rate, as detailed in Table III, achieving a computational time radiance world. IEEE Robotics and Automation Letters,
|               |     |       |        |           |             |     |      | 7(2):4606–4613, |     | 2022. |     |     |     |     |     |
| ------------- | --- | ----- | ------ | --------- | ----------- | --- | ---- | --------------- | --- | ----- | --- | --- | --- | --- | --- |
| approximately | 40  | times | faster | than that | of LazyPRM. |     | Fig. |                 |     |       |     |     |     |     |     |
7 showcases two instances of motion planning within this [2] Dejan Azinovic´, Ricardo Martin-Brualla, Dan B Gold-
environment. The first scenario illustrates the manipulator man, Matthias Nießner, and Justus Thies. Neural rgb-d
|            |          |      |     |           |     |          |     | surface | reconstruction. |     | In Proceedings |     | of  | the IEEE/CVF |     |
| ---------- | -------- | ---- | --- | --------- | --- | -------- | --- | ------- | --------------- | --- | -------------- | --- | --- | ------------ | --- |
| initiating | movement | from | an  | open area | and | entering | the |         |                 |     |                |     |     |              |     |
cabinet, while the second shows the manipulator navigating ConferenceonComputerVisionandPatternRecognition,
across the cabinet’s levels to reach a specified target. No- pages 6290–6301, 2022.
tably, the manipulator begins from a confined position deep [3] John T Betts and William P Huffman. Path-constrained
within the cabinet in Case 2. Furthermore, in this particular trajectory optimization using sparse sequential quadratic
|          |           |            |     |          |         |            |     | programming. |     | Journal | of  | Guidance, | Control, |     | and Dy- |
| -------- | --------- | ---------- | --- | -------- | ------- | ---------- | --- | ------------ | --- | ------- | --- | --------- | -------- | --- | ------- |
| scenario | (case 2), | our method |     | was able | to find | a solution | in  |              |     |         |     |           |          |     |         |
just 0.02 seconds, whereas LazyPRM (CPU) tool 3.72 sec- namics, 16(1):59–68, 1993.
onds, KinectFusion+RRTConnect (CPU) takes 4.15 seconds, [4] Homanga Bharadhwaj, Kevin Xie, and Florian Shkurti.
and nvblox+MPOT (GPU) takes 4.63 seconds. These exper- Model-predictive control via cross-entropy and gradient-
iments demonstrate the scalability of our approach to high- based optimization. In Learning for Dynamics and
|             |         |     |            |          |               |     |     | Control,                                              | pages | 277–286.      | PMLR, | 2020.   |     |      |         |
| ----------- | ------- | --- | ---------- | -------- | ------------- | --- | --- | ----------------------------------------------------- | ----- | ------------- | ----- | ------- | --- | ---- | ------- |
| dimensional | C-Space | and | real-world | confined | environments. |     |     |                                                       |       |               |       |         |     |      |         |
|             |         |     |            |          |               |     |     | [5] JoshuaBialkowski,SertacKaraman,andEmilioFrazzoli. |       |               |       |         |     |      |         |
|             |         |     |            |          |               |     |     | Massively                                             |       | parallelizing | the   | rrt and | the | rrt. | In 2011 |
VI. CONCLUSIONSANDFUTUREWORK
IEEE/RSJInternationalConferenceonIntelligentRobots
This paper presents Active Neural Time Fields that actively and Systems, pages 3513–3518. IEEE, 2011.
explore and learn arrival time field mapping of unknown [6] Joshua Bialkowski, Michael Otte, Sertac Karaman, and
environments.Thearrivaltimefieldsallowextremelyfastmo- EmilioFrazzoli.Efficientcollisioncheckinginsampling-
tionplanningwithoutrequiringanycomputationallyexpensive based motion planning via safety certificates. The Inter-
tools. We demonstrate the effectiveness of our approach on national Journal of Robotics Research, 35(7):767–796,
| a differential | drive | robot | in mapping |     | and navigating |     | eight | 2016. |     |     |     |     |     |     |     |
| -------------- | ----- | ----- | ---------- | --- | -------------- | --- | ----- | ----- | --- | --- | --- | --- | --- | --- | --- |
Gibson and real-world kitchen environments. We also show- [7] RobertBohlinandLydiaEKavraki. Pathplanningusing
case our approach with a 6-DOF robot arm with a hand-held lazyprm.InProceedings2000ICRA.Millenniumconfer-

12
ence. IEEE international conference on robotics and au- motion planning of aerial robots. In 2019 IEEE/RSJ In-
tomation. Symposia proceedings (Cat. No. 00CH37065), ternationalConferenceonIntelligentRobotsandSystems
volume 1, pages 521–528. IEEE, 2000. (IROS), pages 4423–4430. IEEE, 2019.
[8] Gadiel Sznaier Camps, Robert Dyro, Marco Pavone, [22] Jinwook Huh, Volkan Isler, and Daniel D Lee. Cost-
and Mac Schwager. Learning deep sdf maps online to-go function generating networks for high dimensional
for robot navigation and exploration. arXiv preprint motionplanning. In2021IEEEInternationalConference
arXiv:2207.10782, 2022. on Robotics and Automation (ICRA), pages 8480–8486.
[9] Devendra Singh Chaplot, Deepak Pathak, and Jitendra IEEE, 2021.
Malik.Differentiablespatialplanningusingtransformers. [23] Brian Ichter, James Harrison, and Marco Pavone. Learn-
InInternationalConferenceonMachineLearning,pages ing sampling distributions for robot motion planning. In
1484–1495. PMLR, 2021. 2018 IEEE International Conference on Robotics and
[10] Yu Fan Chen, Shih-Yuan Liu, Miao Liu, Justin Miller, Automation (ICRA), pages 7087–7094. IEEE, 2018.
and Jonathan P How. Motion planning with diffusion [24] Le´onard Jaillet, Juan Corte´s, and Thierry Sime´on.
maps. In 2016 IEEE/RSJ International Conference on Sampling-based path planning on configuration-space
IntelligentRobotsandSystems(IROS),pages1423–1430. costmaps. IEEE Transactions on Robotics, 26(4):635–
IEEE, 2016. 646, 2010.
[11] Zhiqin Chen and Hao Zhang. Learning implicit fields [25] LydiaEKavraki,PetrSvestka,J-CLatombe,andMarkH
for generative shape modeling. In Proceedings of the Overmars. Probabilistic roadmaps for path planning in
IEEE/CVF Conference on Computer Vision and Pattern high-dimensional configuration spaces. IEEE transac-
Recognition, pages 5939–5948, 2019. tionsonRoboticsandAutomation,12(4):566–580,1996.
[12] Howie Choset, Kevin M Lynch, Seth Hutchinson, [26] Lydia E Kavraki, Mihail N Kolountzakis, and J-C
George A Kantor, and Wolfram Burgard. Principles of Latombe. Analysis of probabilistic roadmaps for path
robot motion: theory, algorithms, and implementations. planning. IEEE Transactions on Robotics and automa-
MIT press, 2005. tion, 14(1):166–171, 1998.
[13] RonaldRCoifmanandSte´phaneLafon. Diffusionmaps. [27] James J Kuffner and Steven M LaValle. RRT-connect:
Applied and computational harmonic analysis, 21(1):5– An efficient approach to single-query path planning. In
30, 2006. Proceedings 2000 ICRA. Millennium Conference. IEEE
[14] Christopher I Connolly, J Brian Burns, and Rich Weiss. International Conference on Robotics and Automation.
Path planning using laplace’s equation. In Proceedings., SymposiaProceedings(Cat.No.00CH37065),volume2,
IEEEInternationalConferenceonRoboticsandAutoma- pages 995–1001. IEEE, 2000.
tion, pages 2102–2106. IEEE, 1990. [28] Rahul Kumar, Aditya Mandalika, Sanjiban Choudhury,
[15] Michael G Crandall and Pierre-Louis Lions. Viscosity and Siddhartha Srinivasa. Lego: Leveraging experience
solutions of hamilton-jacobi equations. Transactions of in roadmap generation for sampling-based planning. In
the American mathematical society, 277(1):1–42, 1983. 2019 IEEE/RSJ International Conference on Intelligent
[16] KeenanCrane,ClarisseWeischedel,andMaxWardetzky. Robots and Systems (IROS), pages 1488–1495. IEEE,
Geodesicsinheat:Anewapproachtocomputingdistance 2019.
based on heat flow. ACM Transactions on Graphics [29] SMLaValle. Planningalgorithms. CambridgeUniversity
(TOG), 32(5):1–11, 2013. Press google schola, 2:3671–3678, 2006.
[17] KeenanCrane,MarcoLivesu,EnricoPuppo,andYipeng [30] AnT.Le,GeorgiaChalvatzaki,ArminBiess,andJanPe-
Qin. A survey of algorithms for geodesic paths and ters. Acceleratingmotionplanningviaoptimaltransport.
distances. arXiv preprint arXiv:2007.10430, 2020. In Advances in Neural Information Processing Systems
[18] Tung Dang, Marco Tranzatto, Shehryar Khattak, Frank (NeurIPS), 2023.
Mascarich, Kostas Alexis, and Marco Hutter. Graph- [31] Chengshu Li, Fei Xia, Roberto Mart´ın-Mart´ın, Michael
basedsubterraneanexplorationpathplanningusingaerial Lingelbach, Sanjana Srivastava, Bokui Shen, Kent El-
and legged robots. Journal of Field Robotics, 37(8): liott Vainio, Cem Gokmen, Gokul Dharan, Tanish Jain,
1363–1388, 2020. Andrey Kurenkov, Karen Liu, Hyowon Gweon, Jiajun
[19] Adam Fishman, Adithyavairavan Murali, Clemens Epp- Wu,LiFei-Fei,andSilvioSavarese. igibson2.0:Object-
ner, Bryan Peele, Byron Boots, and Dieter Fox. Motion centric simulation for robot learning of everyday house-
policynetworks.InConferenceonRobotLearning,pages holdtasks. InAleksandraFaust,DavidHsu,andGerhard
967–977. PMLR, 2023. Neumann, editors, Proceedings of the 5th Conference
[20] JonathanDGammell,SiddharthaSSrinivasa,andTimo- on Robot Learning, volume 164 of Proceedings of Ma-
thy D Barfoot. Informed RRT: Optimal sampling-based chineLearningResearch,pages455–465.PMLR,08–11
pathplanningfocusedviadirectsamplingofanadmissi- Nov2022.URLhttps://proceedings.mlr.press/v164/li22b.
bleellipsoidalheuristic. In2014IEEE/RSJInternational html.
Conference on Intelligent Robots and Systems, pages [32] XuetingLi,SifeiLiu,ShaliniDeMello,XiaolongWang,
2997–3004. IEEE, 2014. Ming-Hsuan Yang, and Jan Kautz. Learning continuous
[21] Luxin Han, Fei Gao, Boyu Zhou, and Shaojie Shen. Fi- environmentfieldsviaimplicitfunctions.InInternational
esta:Fastincrementaleuclideandistancefieldsforonline Conference on Learning Representations, 2022. URL

13
https://openreview.net/forum?id=3ILxkQ7yElm. IntelligentRobotsandSystems(IROS),pages1366–1373.
[33] Yiming Li, Jiacheng Qiu, and Sylvain Calinon. A IEEE, 2017.
riemannian take on distance fields and geodesic flows [45] Joseph Ortiz, Alexander Clegg, Jing Dong, Edgar Su-
in robotics. arXiv preprint arXiv:2412.05197, 2024. car, David Novotny, Michael Zollhoefer, and Mustafa
[34] Yaron Lipman, Raif M Rustamov, and Thomas A Mukadam. iSDF: Real-Time Neural Signed Distance
Funkhouser. Biharmonic distance. ACM Transactions FieldsforRobotPerception. InProceedingsofRobotics:
on Graphics (TOG), 29(3):1–11, 2010. Science and Systems, New York City, NY, USA, June
[35] Ilya Loshchilov and Frank Hutter. Decoupled weight 2022. doi: 10.15607/RSS.2022.XVIII.012.
decay regularization. In International Conference on [46] Jia Pan and Dinesh Manocha. Gpu-based parallel colli-
Learning Representations, 2017. URL https://api. siondetectionforreal-timemotionplanning. InAlgorith-
semanticscholar.org/CorpusID:53592270. mic Foundations of Robotics IX: Selected Contributions
[36] Lars Mescheder, Michael Oechsle, Michael Niemeyer, of the Ninth International Workshop on the Algorithmic
Sebastian Nowozin, and Andreas Geiger. Occupancy FoundationsofRobotics,pages211–228.Springer,2010.
networks: Learning 3d reconstruction in function space. [47] Jeong Joon Park, Peter Florence, Julian Straub, Richard
InProceedingsoftheIEEE/CVFconferenceoncomputer Newcombe, and Steven Lovegrove. Deepsdf: Learning
vision and pattern recognition, pages 4460–4470, 2019. continuous signed distance functions for shape represen-
[37] Alexander Millane, Helen Oleynikova, Emilie Wirbel, tation. In Proceedings of the IEEE/CVF conference on
Remo Steiner, Vikram Ramasamy, David Tingdahl, and computervisionandpatternrecognition,pages165–174,
Roland Siegwart. nvblox: Gpu-accelerated incremental 2019.
signed distance field mapping. 2024 IEEE International [48] Ahmed H Qureshi and Michael C Yip. Deeply informed
Conference on Robotics and Automation (ICRA), pages neural sampling for robot motion planning. In 2018
2698–2705, 2023. URL https://api.semanticscholar.org/ IEEE/RSJInternationalConferenceonIntelligentRobots
CorpusID:264832853. and Systems (IROS), pages 6582–6588. IEEE, 2018.
[38] Richard A Newcombe, Shahram Izadi, Otmar Hilliges, [49] Ahmed H Qureshi, Anthony Simeonov, Mayur J Bency,
DavidMolyneaux,DavidKim,AndrewJDavison,Push- and Michael C Yip. Motion planning networks. In 2019
meet Kohi, Jamie Shotton, Steve Hodges, and Andrew International Conference on Robotics and Automation
Fitzgibbon. Kinectfusion: Real-time dense surface map- (ICRA), pages 2118–2124. IEEE, 2019.
ping and tracking. In 2011 10th IEEE international [50] AhmedHussainQureshiandYasarAyaz. Potentialfunc-
symposium on mixed and augmented reality, pages 127– tionsbasedsamplingheuristicforoptimalpathplanning.
136. Ieee, 2011. Autonomous Robots, 40:1079–1093, 2016.
[39] Richard A Newcombe, Dieter Fox, and Steven M Seitz. [51] AhmedHussainQureshi,YinglongMiao,AnthonySime-
Dynamicfusion: Reconstruction and tracking of non- onov, and Michael C Yip. Motion planning networks:
rigid scenes in real-time. In Proceedings of the IEEE Bridging the gap between learning-based and classical
conference on computer vision and pattern recognition, motion planners. IEEE Transactions on Robotics, 37(1):
pages 343–352, 2015. 48–66, 2020.
[40] RuiqiNiandAhmedHQureshi.ProgressiveLearningfor [52] Maziar Raissi, Paris Perdikaris, and George E Karni-
Physics-informed Neural Motion Planning. In Proceed- adakis. Physics-informedneuralnetworks:Adeeplearn-
ings of Robotics: Science and Systems, Daegu, Republic ing framework for solving forward and inverse problems
of Korea, July 2023. doi: 10.15607/RSS.2023.XIX.063. involvingnonlinearpartialdifferentialequations. Journal
[41] Ruiqi Ni and Ahmed H Qureshi. NTFields: Neural time of Computational physics, 378:686–707, 2019.
fields for physics-informed robot motion planning. In [53] Clayton Ramsey, Zachary Kingston, Wil Thomason, and
International Conference on Learning Representations, Lydia E Kavraki. Collision-Affording Point Trees:
2023. URLhttps://openreview.net/forum?id=ApF0dmi1 SIMD-Amenable Nearest Neighbors for Fast Motion
9K. Planning with Pointclouds. In Proceedings of Robotics:
[42] Ruiqi Ni and Ahmed H. Qureshi. Physics-informed Science and Systems, Delft, Netherlands, July 2024. doi:
neural motion planning on constraint manifolds. In 10.15607/RSS.2024.XX.038.
2024 IEEE International Conference on Robotics and [54] Erik Sandstro¨m, Yue Li, Luc Van Gool, and Martin R
Automation (ICRA), pages 12179–12185, 2024. doi: Oswald. Point-slam: Dense neural point cloud-based
10.1109/ICRA57147.2024.10610883. slam. In Proceedings of the IEEE/CVF International
[43] Ruiqi Ni, Zherong Pan, and Xifeng Gao. Robust Conference on Computer Vision, pages 18433–18444,
multi-robot trajectory optimization using alternating di- 2023.
rection method of multiplier. IEEE Robotics and Au- [55] John Schulman, Yan Duan, Jonathan Ho, Alex Lee,
tomation Letters, 7:5950–5957, 2021. URL https://api. Ibrahim Awwal, Henry Bradlow, Jia Pan, Sachin Patil,
semanticscholar.org/CorpusID:246634449. Ken Goldberg, and Pieter Abbeel. Motion planning
[44] Helen Oleynikova, Zachary Taylor, Marius Fehr, Roland with sequential convex optimization and convex colli-
Siegwart, and Juan Nieto. Voxblox: Incremental 3d sion checking. The International Journal of Robotics
euclidean signed distance fields for on-board mav plan- Research, 33(9):1251–1270, 2014.
ning. In 2017 IEEE/RSJ International Conference on [56] James A Sethian. A fast marching level set method

14
for monotonically advancing fronts. Proceedings of the Computer Graphics Forum, volume 41, pages 641–676.
National Academy of Sciences, 93(4):1591–1595, 1996. Wiley Online Library, 2022.
[57] Xujie Shen, Haocheng Peng, Zesong Yang, Juzhan Xu, [71] Zhefan Xu, Di Deng, and Kenji Shimada. Autonomous
HujunBao,RuizhenHu,andZhaopengCui. Pc-planner: uavexplorationofdynamicenvironmentsviaincremental
Physics-constrained self-supervised learning for robust sampling and probabilistic roadmap. IEEE Robotics and
neural motion planning with shape-aware distance func- Automation Letters, 6(2):2729–2736, 2021.
tion. InSIGGRAPHAsia2024ConferencePapers,pages [72] Zike Yan, Yuxin Tian, Xuesong Shi, Ping Guo, Peng
| 1–11, | 2024. |     |     |     |     |     |     |     | Wang, and | Hongbin | Zha. | Continual | neural | mapping: |
| ----- | ----- | --- | --- | --- | --- | --- | --- | --- | --------- | ------- | ---- | --------- | ------ | -------- |
[58] Vincent Sitzmann, Julien N.P. Martel, Alexander W. Learninganimplicitscenerepresentationfromsequential
Bergman, David B. Lindell, and Gordon Wetzstein. observations. In Proceedings of the IEEE/CVF Inter-
Implicit neural representations with periodic activation national Conference on Computer Vision, pages 15782–
| functions. |     | In Proc. | NeurIPS, |     | 2020. |     |     |     | 15792, | 2021. |     |     |     |     |
| ---------- | --- | -------- | -------- | --- | ----- | --- | --- | --- | ------ | ----- | --- | --- | --- | --- |
[59] Cyrill Stachniss. Robotic mapping and exploration, [73] Fan Yang, Chao Cao, Hongbiao Zhu, Jean Oh, and
volume 55. Springer, 2009. Ji Zhang. Far planner: Fast, attemptable route planner
[60] Edgar Sucar, Shikun Liu, Joseph Ortiz, and Andrew J usingdynamicvisibilityupdate. In2022ieee/rsjinterna-
Davison. imap:Implicitmappingandpositioninginreal- tionalconferenceonintelligentrobotsandsystems(iros),
time. In Proceedings of the IEEE/CVF International pages 9–16. IEEE, 2022.
ConferenceonComputerVision,pages6229–6238,2021. [74] Zihan Zhu, Songyou Peng, Viktor Larsson, Weiwei Xu,
[61] Zaid Tahir, Ahmed H Qureshi, Yasar Ayaz, and Raheel Hujun Bao, Zhaopeng Cui, Martin R. Oswald, and
Nawaz. Potentially guided bidirectionalized RRT* for Marc Pollefeys. Nice-slam: Neural implicit scalable
fast optimal path planning in cluttered environments. encoding for slam. 2022 IEEE/CVF Conference on
Robotics and Autonomous Systems, ComputerVisionandPatternRecognition(CVPR),pages
|     |     |     |     |     |     | 108:13–27, | 2018. |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
[62] AvivTamar,YiWu,GarrettThomas,SergeyLevine,and 12776–12786, 2021. URL https://api.semanticscholar.
Pieter Abbeel. Value iteration networks. Advances in org/CorpusID:245385791.
neural information processing systems, 29, 2016. [75] MattZucker,NathanRatliff,AncaDDragan,MihailPiv-
[63] MatthewTancik,PratulSrinivasan,BenMildenhall,Sara toraiko, Matthew Klingensmith, Christopher M Dellin,
Fridovich-Keil, Nithin Raghavan, Utkarsh Singhal, Ravi J Andrew Bagnell, and Siddhartha S Srinivasa. Chomp:
Ramamoorthi,JonathanBarron,andRenNg.Fourierfea- Covariant hamiltonian optimization for motion planning.
tures let networks learn high frequency functions in low The International journal of robotics research, 32(9-10):
| dimensional |           | domains.        |               | Advances      | in         | Neural         | Information |     | 1164–1193, | 2013.  |     |                  |       |              |
| ----------- | --------- | --------------- | ------------- | ------------- | ---------- | -------------- | ----------- | --- | ---------- | ------ | --- | ---------------- | ----- | ------------ |
| Processing  |           | Systems,        | 33:7537–7547, |               |            | 2020.          |             |     |            |        |     |                  |       |              |
| [64] Wil    | Thomason, |                 | Zachary       | Kingston,     | and        | Lydia          | E Kavraki.  |     |            |        |     |                  |       |              |
| Motions     |           | in microseconds |               | via           | vectorized | sampling-based |             |     |            |        |     |                  |       |              |
| planning.   |           | In 2024         | IEEE          | International |            | Conference     |             | on  |            |        |     |                  |       |              |
|             |           |                 |               |               |            |                |             |     |            | Yuchen | Liu | (Student Member, | IEEE) | received his |
Robotics and Automation (ICRA), pages 8749–8756. B.S. and M.S. degrees in computer science from
|                      |       |     |                        |     |     |                |     |     |     | NewYorkUniversity(NYU),NewYork,NY, |          |                     |         | USA,            |
| -------------------- | ----- | --- | ---------------------- | --- | --- | -------------- | --- | --- | --- | ---------------------------------- | -------- | ------------------- | ------- | --------------- |
| IEEE,                | 2024. |     |                        |     |     |                |     |     |     |                                    |          |                     |         |                 |
|                      |       |     |                        |     |     |                |     |     |     | in                                 | 2022 and | 2023, respectively. |         | He is currently |
| [65] SebastianThrun. |       |     | Probabilisticrobotics. |     |     | Communications |     |     |     |                                    |          |                     |         |                 |
|                      |       |     |                        |     |     |                |     |     |     | pursuing                           | a Ph.D.  | in computer         | science | at Purdue       |
of the ACM, 45(3):52–57, 2002. University, West Lafayette, IN, USA, where he is
[66] Eran Treister and Eldad Haber. A fast marching al- affiliated with the Cognitive Robot Autonomy and
|     |     |     |     |     |     |     |     |     |     | Learning | Lab. | His research | interests | span active |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | ---- | ------------ | --------- | ----------- |
gorithm for the factored eikonal equation. Journal of mapping, motion planning, and physics-informed
| Computational |               | physics, |            | 324:210–225, |            | 2016.          |           |       |     | machinelearning. |     |     |     |     |
| ------------- | ------------- | -------- | ---------- | ------------ | ---------- | -------------- | --------- | ----- | --- | ---------------- | --- | --- | --- | --- |
| [67] Alberto  | Valero-Gomez, |          |            | Javier       | V Gomez,   | Santiago       |           | Gar-  |     |                  |     |     |     |     |
| rido,         | and           | Luis     | Moreno.    | The          | path       | to efficiency: |           | Fast  |     |                  |     |     |     |     |
| marching      |               | method   | for safer, | more         | efficient  |                | mobile    | robot |     |                  |     |     |     |     |
|               |               | IEEE     | Robotics   | &            | Automation |                | Magazine, |       |     |                  |     |     |     |     |
| trajectories. |               |          |            |              |            |                |           | 20    |     |                  |     |     |     |     |
RuiqiNi(StudentMember,IEEE)receivedhisB.S.
| (4):111–120, |     | 2013. |     |     |     |     |     |     |     |        |                |     |               |         |
| ------------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- | ------ | -------------- | --- | ------------- | ------- |
|              |     |       |     |     |     |     |     |     |     | degree | in Information | and | Computational | Science |
[68] OskarVonStrykandRolandBulirsch.Directandindirect
|     |     |     |     |     |     |     |     |     |     | from | the University | of Science | and | Technology of |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | -------------- | ---------- | --- | ------------- |
methodsfortrajectoryoptimization.Annalsofoperations China (USTC) in 2018. He later pursued graduate
research, 37:357–373, 1992. studies in Computer Science at Florida State Uni-
versity,FL,USA.Currently,heisaPh.D.studentin
| [69] Grady | Williams, |     | Paul | Drews, | Brian | Goldfain, | James | M   |     |     |     |     |     |     |
| ---------- | --------- | --- | ---- | ------ | ----- | --------- | ----- | --- | --- | --- | --- | --- | --- | --- |
ComputerScienceatPurdueUniversityandamem-
Rehg, and Evangelos A Theodorou. Aggressive driving ber of the Cognitive Robot Autonomy and Learn-
withmodelpredictivepathintegralcontrol.In2016IEEE ing Lab. His research focuses on motion planning
andcontrol,physics-informedmachinelearning,and
International Conference on Robotics and Automation physics-basedsimulation.
| (ICRA),     | pages    | 1433–1440. |         | IEEE,     | 2016. |             |          |        |     |     |     |     |     |     |
| ----------- | -------- | ---------- | ------- | --------- | ----- | ----------- | -------- | ------ | --- | --- | --- | --- | --- | --- |
| [70] Yiheng |          | Xie,       | Towaki  | Takikawa, |       | Shunsuke    |          | Saito, |     |     |     |     |     |     |
| Or          | Litany,  | Shiqin     | Yan,    | Numair    | Khan, | Federico    | Tombari, |        |     |     |     |     |     |     |
| James       | Tompkin, |            | Vincent | Sitzmann, |       | and Srinath | Sridhar. |        |     |     |     |     |     |     |
| Neural      | fields   | in         | visual  | computing |       | and         | beyond.  | In     |     |     |     |     |     |     |

15
AhmedH.Qureshi(Member,IEEE)isanAssistant
Professor in the Department of Computer Science
at Purdue University, where he leads the Cognitive
Robot Autonomy and Learning (CoRAL) Lab. His
research group focuses on both fundamental and
appliedaspectsofrobotplanningandcontrol,aiming
to deploy robots in natural and dynamic human
environments. His work addresses challenges such
asscalableandrapidmotionplanning,activepercep-
tion,human-in-the-looprobotmanipulation,mobile
navigation, and data-driven control. Dr. Qureshi’s
contributions to the field have been recognized through the spotlight and
best paper awards at various academic venues. He currently serves as an
Associate Editor for the IEEE Transactions on Robotics (TRO) and the
IEEE Robotics and Automation Letters (RA-L). In 2024, he received the
Outstanding Associate Editor Award from IEEE RA-L. He has also been
involved in the program committees for prestigious conferences, including
RSS, ICRA, IROS, and CoRL. Before his current position, Dr. Qureshi
earned a B.S. in Electrical Engineering from NUST in Pakistan, an M.S.
in Engineering from Osaka University in Japan, and a Ph.D. in Intelligent
Systems,Robotics,andControlfromtheUniversityofCalifornia,SanDiego.