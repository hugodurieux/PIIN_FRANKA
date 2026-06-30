How to Train Your Robots?
The Impact of Demonstration Modality on Imitation Learning
Haozhuo Li;, Yuchen Cui§, Dorsa Sadigh;
Abstract—Imitation learning is a promising approach for
learning robot policies with user-provided data. The way demon-
strationsareprovided,i.e.,demonstrationmodality,influencesthe
qualityofthedata.Whileexistingresearchshowsthatkinesthetic
teaching (physically guiding the robot) is preferred by users
for the intuitiveness and ease of use, the majority of existing
manipulation datasets were collected through teleoperation via
a VR controller or spacemouse. In this work, we investigate
how different demonstration modalities impact downstream
learning performance as well as user experience. Specifically, we
compare low-cost demonstration modalities including kinesthetic
teaching, teleoperation with a VR controller, and teleoperation
with a spacemouse controller. We experiment with three table-
top manipulation tasks with different motion constraints. We Figure 1: Demonstration modalities under study. Kinesthetic teaching
evaluate and compare imitation learning performance using controls precise joint poses; and teleoperation controls the delta pose of
data from different demonstration modalities, and collected therobot’send-effector:VRprovidesadirectspatialmappingofthetrajectory,
subjective feedback on user experience. Our results show that whilespacemouseallowstheusertocommandvelocitythroughbuttons.
kinesthetic teaching is rated the most intuitive for controlling the
robot and provides cleanest data for best downstream learning that kinesthetic teaching is shown to be more intuitive for
performance. However, it is not preferred as the way for large- people to use compared to teleoperation methods [16, 17].
scale data collection due to the physical load. Based on such Kinesthetic teaching refers to the demonstrator physically
insight, we propose a simple data collection scheme that relies
moving a passive robot arm to complete a given task. The
on a small number of kinesthetic demonstrations mixed with
demonstrator can control the precise position of each joint of
data collected through teleoperation to achieve the best overall
learningperformancewhilemaintaininglowdata-collectioneffort. the robotic arm. Since the robot’s controller is not engaged
during data collection, replaying the recorded trajectory is
necessarytodeterminetheactionsneededtoreplicateeachpose.
I. INTRODUCTION
Replaying also yields clean visual observations unimpeded by
Imitation learning has shown to be a promising approach the demonstrator’s hand. While kinesthetic teaching is often
for scaling up learning end-to-end robot policies for diverse more intuitive, it also comes with additional costs in time
tasks through collecting ad-hoc demonstrations from end-users. and physical effort. By contrast, teleoperation modalities (e.g.,
However, the performance of imitation-based policies depends VR or spacemouse) allow the demonstrator to directly control
in large part on the quality of the demonstrated data [1–3], the end-effector’s motion. However, these two modalities also
which can be influenced by a number of design factors during have some nuanced differences. With VR teleoperation, the
the data collection process. In particular, the way of providing demonstrator only needs to have a rough estimate of how
demonstrations, which we refer to as demonstration modality, their motion scales to the robot’s motion and their hand
isanimportantfactorthatcanaffectdataqualitybyinfluencing trajectory can then directly translate to robot trajectory. The
how users control the robot [4]. demonstrator hence has a direct spatial control of the motion.
Therearevariouswaystoprovideademonstration,including Withspacemouseorjoystick-stylecontrollers,thedemonstrator
physically guiding the robot through kinesthetic teaching [5–7] directly controls the magnitude and direction of the end-
or puppeteering via a leader robot [8, 9], and teleoperating the effector’s motion using combinations of button presses.
robot with different control devices such as 3D spacemouse Despite the wide range of demonstration modalities, their
controllers[10,11]orvirtualreality(VR)interfaces[1,12–14]. relative effects on policy performance, data quality, and
These modalities, shown in Fig. 2, often compose the majority user experience remain insufficiently explored. In this work,
of existing robot datasets such as the OpenXE dataset [15]. we investigate how these distinct demonstration modalities
While there are many different ways of providing robot influence imitation learning for manipulation tasks through
demonstrations, teleoperation with a VR controller or a thesethreelenses.Wefocusonstudyingcommonlow-costdata
spacemouse is currently the dominant data collection modality collection modalities (shown in Fig. 1) for robotic arms used
for training visuomotor policies. This is despite the fact by practitioners, including kinesthetic teaching, teleoperation
through VR controller, and teleoperation through spacemouse.
; ComputerScienceDepartment,StanfordUniversity.
We evaluate the effect of these three demonstration modal-
§ ComputerScienceDepartment,UniversityofCalifornia,LosAngeles.
CorrespondingEmail:yuchencui@cs.ucla.edu ities via different manipulation tasks with varying motion
5202
raM
01
]OR.sc[
1v71070.3052:viXra

arm[1,13,14].Kinestheticteachinginvolvesthedemonstrator
physically moving the robot and requires replaying to recover
the commanded actions, especially in the presence of contact
forces; and hence it is a shadowing approach that does not
directly record the robot’s actions.
The main benefit of kinesthetic teaching over teleoperation
is that the demonstrator can physically feel the joint limits
and contact forces through the robotic arm. In an effort to
Figure 2: Popular demonstration modalities. Composition of human reproduce similar feedback in teleoperation methods, an active
demonstrationmodalitiespresentintheOpenXEdataset[15]. body of research develops specialized devices for effective
teleoperation such as haptic controllers [21]. Puppeteering,
constraints as our testbed. Additionally, we propose a data
where the demonstrator kinesthetically moves one robot to
collectionparadigmthatleveragesthebenefitsofthesedifferent
control an identical twin, is a special case along this direction
modalities.Wefirstcollectdemonstrationsfromasingleexpert
where a passive robot is used as the controller to provide
across three different modalities for all the tasks and train
feedback of joint limits mechanically [8, 9]. Puppeteering
diffusion-based imitation policies [18]. We then conduct a
sharesmanycharacteristicsofkinestheticteachingbutbypasses
user study where participants provide demonstrations for the
the challenges of replay by recording the commanded poses
manipulation tasks using all three modalities and compare the
on the leader robot. Pushing the idea of wearing the robot,
modalities in terms of subjective and objective metrics. Our
a line of research proposes to make the human demonstrator
key findings are:
hold a robot gripper to provide data and then use the in-hand
‚ Kinesthetic teaching produces data that leads to higher camera observation to align states across data collection and
policy performance and is preferred by users for the ease
deployment[22,23].Recentresearchhasalsomadesignificant
of use when controlling robots.
progress towards vision-based teleoperation systems, especially
‚ However, kinesthetic teaching is not preferred by users for mapping human hand motions to robot actions [16, 24, 25].
large-scale data collection due to its physical demand and
added time to replay. User experience of demonstration modality. The influence
‚ Data from kinesthetic teaching exhibits high action con- of demonstration interface design has been studied in a
sistency, while teleoperation via VR or spacemouse offer number of prior works. For example, Akgun et al. [6] show
higher state diversity, where both metrics of action consis- that different types of kinesthetic teaching (keyframe versus
tency and state diversity correlate with high quality data. trajectory) can have different implications on data quality and
Basedontheseinsights,weproposeahybriddatacollection user experience. Wrede et al. [26] and Sakr et al. [27] study
scheme that combines a small amount of data from kinesthetic how to train or aid non-expert users to better program the
teaching with additional data from VR teleoperation. This robot with kinesthetic teaching. Rakita et al. [12] studies user
simple approach results in an average of 20% higher perfor- experience of a VR-based remote teleoperation system. Duan
mance than using data from individual modalities alone, while et al. [16] demonstrate an augmented reality-based modality
maintaining a low physical burden on the demonstrator. with matching performance with kinesthetic teaching in simple
pick-and-place tasks. Closely related to our work, Jiang et al.
II. RELATEDWORK
[17] studies the effect of data collection modalities on user
Our work is broadly related to research that designs control
experience and performance in terms of how successful they
interfacesanddatacollectionmethodsforimitationlearning,as
were able to perform assigned tasks.
wellasworkinhuman-robotinteractionthataimstounderstand
Our contributions differ from prior work in the following
interface design implications on user experience. We also
aspects:1)whileinpriorworkperformanceisevaluatedashow
borrow tools from recent research on data quality in imitation
successful the user is able to provide demonstrations through a
learning to analyze data from different modalities.
modality, we close the evaluation loop by training downstream
Demonstration modalities for imitation learning. Demon- imitation policies with the collected data and evaluating the
stration modalities are generally categorized into teleoperation learning performance; and 2) unlike prior work that heavily
versus shadowing, depending on whether there is a direct focuses on the experience of novice users, we are interested in
recording mapping of actions [19, 20]. Teleoperation via a VR the experience of expert users of robots, especially those who
controller or spacemouse has become the dominant modality want to collect large-scale data for training effective policies.
in the era of end-to-end visuomotor policy learning due to the Results from our user study align with findings in prior work
accessibility of these low-cost devices. Spacemouse is similar that most users find kinesthetic teaching more intuitive than
to traditional joystick controllers where the user is effectively teleoperation methods and further confirm that kinesthetic data
pressing buttons to control each axis of motion, but it requires provides the best performing models except when contact
only one hand to control all 6 degrees of freedom [10, 11]. forces are present. Our user study suggests that most users
VR controller tracks hand motion with an IMU sensor and would choose teleoperation over kinesthetic teaching for large-
thereforecanbeusedtocommandthedeltamotionoftherobot scale data collection, despite the fact that they rate kinesthetic

teaching more favorable in terms of subjective measures. We
further propose a simple yet effective data collection scheme
that mixes data from multiple demonstration modalities to
balance the trade-off between performance and cost.
Data quality. Scaling real-world robot data for imitation
learning is expensive. Therefore, an increasing line of research Figure3:Actiondiscrepancy.Replayingrecordedend-effectorposemaynot
studies how to formalize, evaluate, and control data quality [2– recoverthedesiredaction,especiallywhencontactforceispresent.
4,28,29].Specifically,Hejnaetal.[3]usesrobustoptimization
consistency and state diversity in the dataset. Instead of
tofindtheoptimalweightsformixingexistingdatasetsinlarge-
clustering states with a fixed distance, we approximate action
scale imitation learning. Other works guide data collection by
variance (opposite of action consistency) among K nearest-
querying for trajectories with more consistent actions [28] or
neighbor states in proprioceptive state space:
trajectories that are guided by compositional generalization
ÿ ÿ
1 1
capabiliteis of imitation policies [29]. By contrast, our work ActionVariancepDq“ pa´ aˆq2
focuses on studying the effect of demonstration modality on |D| K
ps,aqPD psˆ,aˆqPNNps,D,Kq
collectingtask-specificdataforimitationlearning.Ourfindings (4)
are complementary to prior work and can add additional Weestimatestatediversitywiththesamemethodbycomputing
guidance for future large-scale data collection design. state variance instead. While these metrics do not take into
account visual states, the initial state distribution is the same
III. PRELIMINARIES
across modalities, therefore the same estimation bias equally
Problem formulation. Imitation learning assumes access to a exists in all datasets under comparison.
demonstration dataset D “tτ ,...,τ u of N demonstrations.
1 N
Each demonstration τ consists of a sequence of continuous
IV. EXPERIMENTALDESIGN
i
state-action pairs of length T , τ “tps ,a q,...,ps ,a qu, Inthissection,weoutlineourexperimentalsetupanddesign
i i 1 1 Ti Ti
with states s P S and actions a P A. Demonstrations are choices for evaluating the impact of demonstration modalities.
generated by expert policy π psq under environment dynamics We begin by presenting our environment setup and task design,
E
ρps1|s,aq. The objective of imitation learning is to learn a followedbyadetaileddescriptionofthedatacollectionpipeline
policy π :S ÑA that maps states to actions similar to π . for each modality. We then provide an overview of the policy
θ E
In practice, human demonstrators do not have direct access training process and describe the user study that assesses user
to the robot’s action space and therefore human’s internal experiences across the three demonstration modalities.
policy π has to go through control modality modifier ϕ .
H x Setup. We use a 7-DoF Franka Emika Panda robotic arm as
The observed dataset hence contains actions from a modality-
the hardware. We use the Cartesian impedance controller in
specific policy:
Polymetis to control desired end-effector pose of the arm. We
ps,aq„ϕ pπ psq,ρq (1) process the user input from different demonstration modalities
x H
to compute delta end-effector pose as action commands, such
ϕ captures the biases introduced by different demonstration
x that the collected data from different modalities shares the
modality design. For example, joystick-style controllers allow
same state and action representation.
users to easily move in straight lines.
Tasks. We select three manipulation tasks with different types
Policy model. We follow the work of Chi et al. [18] to
of motion constraints as our testbed, including one requiring
formulatethebehavioralcloningpoliciesasdenoisingdiffusion
high contact force. Fig. 4 shows the three tasks we study.
probabilistic models that optimize the following loss over D :
N Open Drawer consists of a free-space reaching motion, a
Lpθq“MSEpϵk,ϵ ps ,a0`ϵk,kqq, (2) precise alignment motion for grasping the knob, and a final
θ i i
constrained linear motion to pull out the drawer. Flip Glass
where aK i is sampled from Gaussian noise and the process consists of a free-space reaching motion followed by a pick up
takes K steps of denoising iteration to a0 i : motion, a 180-degree rotation to turn the glass upside down,
ak´1 “αpak´γϵ ps ,ak,kq`Np0,σ2Iqq (3) and finally a transfer to the desired placement location. To
i i θ i i perform this task, the robot arm needs to operate near its joint
The state s consists of RGB observations that are encoded limits.PushSanitizer involvestherobotaimingatthecenterof
with ResNet [30] and then concatenated with proprioception the sanitizer top and pressing down to dispense sanitizer. The
data. We use high-dimensional temporal action sequence as pushing motion requires pressing force towards the sanitizer.
the output space for the diffusion policy models, where one
Data collection interfaces. For kinesthetic teaching, we
action consists of the desired delta pose of end-effector and a
first record the end-effector poses and gripper actions
binary indicator for controlling the gripper.
tppdemo,gdemoqu in gravity compensated mode as the demon-
t t
Data quality. We follow the work of Belkhale et al. [2] to strator physically moves the robot arm to complete the task.
approximate quality of a dataset through measuring action We record at the same frequency as the active robot controller

mapped to robot end-effector delta pose with a scaling factor.
Training data. To control confounding factors, including
demonstrator style and experience, we use data from a
single demonstrator who is similarly experienced in using
all modalities for training policies. The demonstrator was
previously unexposed to any modality and practiced using
each equally prior to data collection. Upon data collection, the
demonstrator provided a total of 100 trajectories per modality
for each task, switching modality every 10 trajectories and
marking initial states to ensure the data collected are under
conditions as similar as possible.
Policy learning. Data quality is a function of the downstream
learning algorithm [2], therefore we fix it to be diffusion
policy[18].Specifically,themodeltakestwoRGBobservations
(one wrist camera view and one external camera view) and the
robot’s proprioception state as input and outputs a sequence of
actions.Wetrainthemodelwithsupervisedlossassepcifiedin
Eq. (2). The model is trained to predict 16 consecutive actions,
Figure4:Taskswithvaryingmotionconstraints.Thethreeselectedtasks
eachhasadifferenttypeofmotionconstraint(e.g.constrainedlinear,large but we only execute the first 8 per inference during evaluation.
rotation,andexertingcontactforce)torepresentabroadrangeoftasks. We train each model for 800K gradient steps and probe the
performance of the last 5 checkpoints (10K steps apart) with
uses.Wethenresetthetaskandreplaythedemonstrationusing a set of in-distribution tests, and select the model with highest
the timestamped end-effector poses as targets and compute the performance for full evaluation. The full evaluation includes
deltaposefromtherobot’scurrentposeastheactioncommand: half in-distribution and half out-of-distribution tests. We report
the success rate out of 20 total trials.
a0 “pdemo´p0 (5)
t t t
User study. We conducted a user study to evaluate how user
where pi is the pose in i-th iteration of replay at timestamp t.
t experience is influenced by different demonstration modalities:
Corresponding states and commanded actions are recorded as
‚ Participants.Werecruited12universitystudents(4female,
thedataset.However,thecomputedactionsmaynotrecoverthe
8 male, aged 19–29) majoring in computer science or
demonstrated trajectory, especially in the presence of contact
engineering. 6 participants identified as Expert in training
forces. As illustrated in Fig. 3, while the action is equivalent
robot policies, while the rest had little to no experience.
to the delta pose for free space motions, it is nontrivial to
‚ IndependentVariables.Participantsengagedwith3demon-
recover the action when contact forces are present and the
stration modalities: kinesthetic, VR, and spacemouse. Our
robot may fail to reach the commanded pose. The principled
resultsshowsnostatisticallysignificantdifferencesbetween
way to resolve this issue is to record the end-effector force
VRandspacemouse.HenceweclassifyVRandspacemouse
profile during demonstration and replay accordingly [31, 32].
as teleoperation methods in our subsequent analysis.
However, we do not have access to a force sensor and can
‚ Dependent Variables. We collected both objective and
only account for such control error in hindsight using a trick
subjective measures from the user study. We recorded the
to compensate actions with errors in the previous iteration of
time participants spent on the practice task before they
replay. In our data collection, if the replay fails to complete
feel confident to collect successful demonstrations. We also
the task in the first try, we will replay with additional error
collected subjective feedback through likert-scale questions
term added to the action to accommodate force-induced error:
in the NASA-TLX survey [34] for each modality and a
a1 “pdemo´p1 `λppdemo´p0 q (6) comprehensive questionnaire comparing all modalities.
t t t`1 t`1 t`1
‚ Hypotheses. We have the the following hypotheses:
This heuristic results in doubling the replay time for tasks that H1. (intuitiveness) kinesthetic teaching requires shorter
require strong contact forces such as Push Sanitizer. practice time than teleoperation methods;
For VR teleoperation, we use Oculus Quest’s controller H2. (perceived effectiveness) kinesthetic teaching is pre-
and access the controller’s pose change for controlling the ferred by users for controlling robot while teleoperation
robot [33]. Pressing a button on the VR controller activates methods are preferred for large-scale data collection.
teleoperation, recording the controller’s pose as a reference. ‚ Procedure.Participantsfirstpracticedatesttaskundereach
Therobot’send-effectormovesbasedonthecontroller’smotion modality until they were confident to perform study tasks.
relative to this reference. Releasing the button stops the robot, Then they are asked to provide 5 successful demonstrations
allowing the user to reset the reference pose for full rotational per modality across two assigned tasks—Open Drawer or
control. With spacemouse teleoperation, the input is directly Push Sanitizer, and Flip Glass. The order of modalities is

Figure7:Usersubjectivefeedbackresults.Average7-pointlikertscalerating
fordifferentdemonstrationmodalityisplottedforeachquestion.
| Figure 5: | Policy performance. |     | Success | rates | of policies | learned | for each |     |     |     |     |     |     |     |     |
| --------- | ------------------- | --- | ------- | ----- | ----------- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
taskunderdifferentdemonstrationmodality.Kinestheticdataleadstobest-
performingmodelsinOpenDrawerandFlipGlassbutunderperformsinPush
Sanitizerwherestrongcontactforceisrequiredtocompletethetask.
|     |     |     |     |     |     |     |     | Figure 8: | Survey   | question     | response.    | Composition |        | of user     | responses to |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | -------- | ------------ | ------------ | ----------- | ------ | ----------- | ------------ |
|     |     |     |     |     |     |     |     | questions | in final | survey. Most | participants |             | prefer | kinesthetic | teaching as  |
themodalityforcontrollingarobotarmtocompleteaspecifictask.However,
mostparticipantschooseteleoperationmethodsoverkinestheticteachingwhen
askedtoperformlarge-scaledatacollection.
Practice time. User experience (H2). The subjective feedback for each
| Figure 6: |     | Candle | chart | for the | time participants |     | spent on |     |     |     |     |     |     |     |     |
| --------- | --- | ------ | ----- | ------- | ----------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
thepracticetaskundereachmodalityuntilconfident.Usersspentlesstime modality from 7-scale likert questions is shown in Fig. 7.
practicingkinestheticteachingthanteleoperationmethods(p-value=0.038).
|     |     |     |     |     |     |     |     | Kinesthetic | teaching | is  | consistently | rated | to  | require | less mental |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | --- | ------------ | ----- | --- | ------- | ----------- |
demand(p!0.01)andfrustrationlevel(p!0.01)andprovide
randomized within a task. After each modality, participants highestperceivedperformance(p!0.01).Itisratedtorequire
filled out a NASA-TLX survey. A final comprehensive the highest level of physical demand (p“0.016). We do not
questionnairewasusedtocomparemodalities,askingabout observe a different trend for the Push Sanitizer task in the
preferences for robot control and large-scale data collection. relative ratings for kinesthetic teaching, despite the fact that it
requiresdoubletheamountoftimetoreplay.However,although
V. RESULTS
|                  |           |             |               |                  |         |          |            | users rate       | kinesthetic | teaching    |            | to require          | the      | least               | amount of |
| ---------------- | --------- | ----------- | ------------- | ---------------- | ------- | -------- | ---------- | ---------------- | ----------- | ----------- | ---------- | ------------------- | -------- | ------------------- | --------- |
|                  |           |             |               |                  |         |          |            | total demand,    | when        | asked       | about      | which               | modality | they                | would     |
| In this          | section,  | we          | first present | the              | impact  | of       | different  |                  |             |             |            |                     |          |                     |           |
|                  |           |             |               |                  |         |          |            | use for          | large-scale | data        | collection |                     | at the   | end of the          | session,  |
| modalities       | on policy | learning,   |               | then discuss     | the     | results  | of user    |                  |             |             |            |                     |          |                     |           |
|                  |           |             |               |                  |         |          |            | the majority     | of          | the users   | choose     | teleoperation-based |          |                     | modality  |
| study, and       | provide   | an analysis |               | of the collected |         | data     | using data |                  |             |             |            |                     |          |                     |           |
|                  |           |             |               |                  |         |          |            | over kinesthetic |             | teaching    | (see       | Fig.                | 8). This | result              | supports  |
| quality metrics. |           | Finally,    | we present    | and              | discuss | a novel  | data       |                  |             |             |            |                     |          |                     |           |
|                  |           |             |               |                  |         |          |            | H2 and           | correlates  | with        | the        | status              | quo that | the majority        | of        |
| collection       | scheme    | based       | on the        | insights         | from    | our data | analysis.  |                  |             |             |            |                     |          |                     |           |
|                  |           |             |               |                  |         |          |            | large-scale      | datasets    | are         | collected  | through             |          | teleoperation-based |           |
|                  |           |             |               |                  |         |          |            | methods          | (Fig.       | 2). Despite | the        | popularity          |          | of VR in            | practical |
Policylearning.Weevaluatetheperformanceofpolicylearning
through task success rates. The success rates of the best- adoption for collecting demonstration data, most participants
performing checkpoint of each learned policy under different find it to require high mental demand and lead to high level
|            |                     |     |         |        |                  |      |          | of frustration | in  | comparison |     | to the other | two | modalities. |     |
| ---------- | ------------------- | --- | ------- | ------ | ---------------- | ---- | -------- | -------------- | --- | ---------- | --- | ------------ | --- | ----------- | --- |
| modalities | is plotted          | in  | Fig. 5. | We see | that kinesthetic |      | teaching |                |     |            |     |              |     |             |     |
| leads to   | the best-performing |     |         | models | for both         | Open | Drawer   |                |     |            |     |              |     |             |     |
and Flip Glass, with a large margin in Open Drawer. However, Dataquality.Wevisualizetheend-effectortrajectoriesthrough
|               |             |            |           |              |              |             |            | plotting         | its position | in            | 3D and   | compute    | corresponding  |         | action     |
| ------------- | ----------- | ---------- | --------- | ------------ | ------------ | ----------- | ---------- | ---------------- | ------------ | ------------- | -------- | ---------- | -------------- | ------- | ---------- |
| in Push       | Sanitizer   | (requiring |           | high contact | force),      | kinesthetic |            |                  |              |               |          |            |                |         |            |
|               |             |            |           |              |              |             |            | statistics       | for each     | task          | using    | prescribed | data           | quality | metrics    |
| teaching      | falls short | since      | replaying | recorded     | end-effector |             | poses      |                  |              |               |          |            |                |         |            |
|               |             |            |           |              |              |             |            | from Section     | III          | (see          | Fig. 9). | Due        | to high        | noise   | and cross- |
| did not       | succeed     | at this    | task      | in the first | try.         | The error   | term       |                  |              |               |          |            |                |         |            |
|               |             |            |           |              |              |             |            | subject variance |              | in non-expert |          | data (6    | participants), |         | we discard |
| we introduced |             | in Section | IV        | induces high | jerkiness    |             | in actions |                  |              |               |          |            |                |         |            |
despitesuccessfullycompletingthetaskontheseconditeration. them for this analysis. We plot both the data from the single
|     |     |     |     |     |     |     |     | expert demonstrator |     | and | aggregated |     | data | from | user study |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | ---------- | --- | ---- | ---- | ---------- |
Intuitiveness (H1). Fig. 6 shows that participants on average participants who rated themselves as Expert in controlling
spent considerably less time practicing with kinesthetic teach- robots. In general, data collected through teleoperation spreads
ing, supporting H1 with a p-value of 0.038 (<0.05). This result out in space and covers more diverse states than kinesthetic
aligns with prior research showing that users find kinesthetic teaching. To estimate action consistency, we compute the
teaching more intuitive for controlling the robot [16, 17]. We average action variance (Eq. (4)) for the top K nearest
observe that users find controlling rotation motions with VR neighbors in proprioceptive state space (K “200 for expert
unintuitive as they need to constantly reset the reference pose. data, K “50 for user data), and plot positional and rotational

Figure9:Data analysis.Weshowvisualizationsof3Dend-effectorpositionaltrajectoriesandcorrespondingactionstatisticsacrosstasksforboth(single)
expert data and aggregated user study data. We observe that kinesthetic provides data exhibits lower action variance and lower maximum-jerkiness than
teleoperationmethods,exceptforthePushSanitizertaskwhichrequiresstrongcontactforce.
|     |     |     |     | paradigm | that mixes | data from | different | demonstration |     | modali- |
| --- | --- | --- | --- | -------- | ---------- | --------- | --------- | ------------- | --- | ------- |
tiestoachievehighqualitywhilemaintaininglowhumaneffort.
|     |     |     |     | Specifically,   | we can     | leverage    | a small     | amount      | of               | kinesthetic |
| --- | --- | --- | --- | --------------- | ---------- | ----------- | ----------- | ----------- | ---------------- | ----------- |
|     |     |     |     | data and        | augment it | with larger | amounts     |             | of teleoperation | data.       |
|     |     |     |     | We experimented | with       | mixing      | kinesthetic |             | data with        | VR data     |
|     |     |     |     | in Open         | Drawer and | Flip        | Glass       | tasks. Push | Sanitizer        | is not      |
Figure10:Dataquality.MixingdatafromkinestheticandVRcanimprove
statediversityoractionconsistencyofthedemonstrationdataset(lightercolor included since kinesthetic data has low quality due to contact
isrotationalvarianceanddarkercolorispositionalvariance). force. Fig. 10 show that the mixed datasets display higher state
|     |     |     |     | diversity       | than datasets   | from    | any single      | modality,   |                | and slightly |
| --- | --- | --- | --- | --------------- | --------------- | ------- | --------------- | ----------- | -------------- | ------------ |
|     |     |     |     | higher action   | consistency     |         | than VR         | data        | in Flip        | Glass case.  |
|     |     |     |     | Fig. 11 shows   | the success     | rates   | of              | models      | with mixed     | data and     |
|     |     |     |     | corresponding   | baselines       | using   | single-modality |             | data.          | We see       |
|     |     |     |     | that the        | best-performing | models  | with            | mixed       | data           | outperform   |
|     |     |     |     | single-modality | baseline        | by      | 20%             | on average. | In             | Flip Glass,  |
|     |     |     |     | the model       | trained with    | a total | of              | 100 mixed   | demonstrations |              |
achieves75%successrate,outperforming(+5%)thebestmodel
|                                     |     |                               |     | using all | 100 kinesthetic | demonstrations |     |     | (Fig. 5). |     |
| ----------------------------------- | --- | ----------------------------- | --- | --------- | --------------- | -------------- | --- | --- | --------- | --- |
| Figure11:Performanceofpoliciesusing |     | mixed data.Stagedsuccessrates |     |           |                 |                |     |     |           |     |
|                                     |     |                               |     |           |                 | VI. CONCLUSION |     |     |           |     |
forthebestperformingmodelsareplotted.Modelswithmix-modalitydata
(cyan)outperformmodelslearningfromsingle-modalitydata. In this work, we investigate the impact of demonstration
modalityonimitationlearning,focusingonpolicyperformance,
action variance separately. We also compute the jerkiness as data quality, and user experience. Our results indicate that
the second derivative of recorded actions. We observe that users find kinesthetic teaching more intuitive, and the data
kinesthetic teaching leads to data with relatively low action collected through kinesthetic teaching leads to better learning
variance in the two tasks without contact force, but high action performance in tasks that do not involve strong contact forces.
variance and jerkiness in the Push Sanitizer task. We further However, due to the physical effort and time required, users
visualize the recorded actions of Push Sanitizer (red arrows prefer teleoperation modalities for large-scale data collection.
insideredcircles)andobservethattheactionsfromkinesthetic Toaddressthis,weproposedasimpledatacollectionparadigm
teaching replay are highly jerky and do not align well with the thatcombinesasmallamountofkinestheticdatawithadditional
trajectory.IntheFlipGlasstask,theoptimaltrajectoryoperates teleoperation data. We show that this approach yields policies
near the joint limits of the robot and therefore the trajectories with20%highersuccessrateonaveragecomparedtousingdata
overlap a lot in kinesthetic teaching mode, especially with from individual modalities alone. An interesting direction for
data from the single expert demonstrator. However, recruited futureworkistodevelopmethodsforautomaticallydetermining
participants seem to struggle to effectively solve this task the optimal ratio of data to collect from different modalities.
| through teleoperation | modalities, | as indicated | by the wide |     |     |     |     |     |     |     |
| --------------------- | ----------- | ------------ | ----------- | --- | --- | --- | --- | --- | --- | --- |
spreading trajectories in the plots. Acknowledgement This work was supported in part by
|     |     |     |     | NSF #2132847 | &   | #2218760, |     | ONR | N00014-21-1-2298, |     |
| --- | --- | --- | --- | ------------ | --- | --------- | --- | --- | ----------------- | --- |
Learning from mixed modality data. With the insights from AFOSR YIP, Cooperative AI Foundation, and DARPA project
our data analysis, we propose a simple hybrid data collection #W911NF2210214. Views and conclusions are of the authors.

REFERENCES man, D. Kalashnikov, D. Sadigh, E. Johns, E. Foster, F. Liu,
F. Ceola, F. Xia, F. Zhao, F. V. Frujeri, F. Stulp, G. Zhou,
[1] A.Mandlekar,D.Xu,J.Wong,S.Nasiriany,C.Wang,R.Kulka- G. S. Sukhatme, G. Salhotra, G. Yan, G. Feng, G. Schiavi,
rni, L. Fei-Fei, S. Savarese, Y. Zhu, and R. Mart’in-Mart’in, G. Berseth, G. Kahn, G. Yang, G. Wang, H. Su, H.-S. Fang,
“What matters in learning from offline human demonstrations H. Shi, H. Bao, H. B. Amor, H. I. Christensen, H. Furuta,
for robot manipulation,” ArXiv, vol. abs/2108.03298, 2021. H. Walke, H. Fang, H. Ha, I. Mordatch, I. Radosavovic, I. Leal,
[2] S. Belkhale, Y. Cui, and D. Sadigh, “Data quality in imitation J.Liang,J.Abou-Chakra,J.Kim,J.Drake,J.Peters,J.Schneider,
learning,” Advances in Neural Information Processing Systems, J.Hsu,J.Bohg,J.Bingham,J.Wu,J.Gao,J.Hu,J.Wu,J.Wu,
vol. 36, 2024. J. Sun, J. Luo, J. Gu, J. Tan, J. Oh, J. Wu, J. Lu, J. Yang,
[3] J. Hejna, C. A. Bhateja, Y. Jiang, K. Pertsch, and D. Sadigh, J. Malik, J. Silvério, J. Hejna, J. Booher, J. Tompson, J. Yang,
“Remix: Optimizing data mixtures for large scale imitation J. Salvador, J. J. Lim, J. Han, K. Wang, K. Rao, K. Pertsch,
learning,” in 8th Annual Conference on Robot Learning, 2024. K.Hausman,K.Go,K.Gopalakrishnan,K.Goldberg,K.Byrne,
[4] Y. Cui, P. Koppol, H. Admoni, S. Niekum, R. Simmons, K. Oslund, K. Kawaharazuka, K. Black, K. Lin, K. Zhang,
A. Steinfeld, and T. Fitzgerald, “Understanding the relation- K.Ehsani,K.Lekkala,K.Ellis,K.Rana,K.Srinivasan,K.Fang,
ship between interactions and outcomes in human-in-the-loop K. P. Singh, K.-H. Zeng, K. Hatch, K. Hsu, L. Itti, L. Y.
machinelearning,”inInternationalJointConferenceonArtificial Chen, L. Pinto, L. Fei-Fei, L. Tan, L. J. Fan, L. Ott, L. Lee,
Intelligence, 2021. L. Weihs, M. Chen, M. Lepert, M. Memmel, M. Tomizuka,
[5] A. Billard, S. Calinon, R. Dillmann, and S. Schaal, “Survey: M. Itkina, M. G. Castro, M. Spero, M. Du, M. Ahn, M. C.
Robot programming by demonstration,” Springer handbook of Yip, M. Zhang, M. Ding, M. Heo, M. K. Srirama, M. Sharma,
robotics, pp. 1371–1394, 2008. M. J. Kim, N. Kanazawa, N. Hansen, N. Heess, N. J. Joshi,
[6] B. Akgun, M. Cakmak, J. W. Yoo, and A. L. Thomaz, “Tra- N. Suenderhauf, N. Liu, N. D. Palo, N. M. M. Shafiullah,
jectories and keyframes for kinesthetic teaching: A human- O. Mees, O. Kroemer, O. Bastani, P. R. Sanketi, P. T. Miller,
robot interaction perspective,” in Proceedings of the seventh P.Yin,P.Wohlhart,P.Xu,P.D.Fagan,P.Mitrano,P.Sermanet,
annual ACM/IEEE international conference on Human-Robot P. Abbeel, P. Sundaresan, Q. Chen, Q. Vuong, R. Rafailov,
Interaction, 2012, pp. 391–398. R. Tian, R. Doshi, R. Mart’in-Mart’in, R. Baijal, R. Scalise,
[7] P. Sharma, L. Mohan, L. Pinto, and A. Gupta, “Multiple R. Hendrix, R. Lin, R. Qian, R. Zhang, R. Mendonca, R. Shah,
interactionsmadeeasy(mime):Largescaledemonstrationsdata R. Hoque, R. Julian, S. Bustamante, S. Kirmani, S. Levine,
for imitation,” in Conference on robot learning. PMLR, 2018, S.Lin,S.Moore,S.Bahl,S.Dass,S.Sonawani,S.Song,S.Xu,
pp. 906–915. S. Haldar, S. Karamcheti, S. Adebola, S. Guist, S. Nasiriany,
[8] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine- S. Schaal, S. Welker, S. Tian, S. Ramamoorthy, S. Dasari,
grained bimanual manipulation with low-cost hardware,” arXiv S. Belkhale, S. Park, S. Nair, S. Mirchandani, T. Osa, T. Gupta,
preprint arXiv:2304.13705, 2023. T. Harada, T. Matsushima, T. Xiao, T. Kollar, T. Yu, T. Ding,
[9] S. Yang, M. Liu, Y. Qin, D. Runyu, L. Jialong, X. Cheng, T. Davchev, T. Z. Zhao, T. Armstrong, T. Darrell, T. Chung,
R. Yang, S. Yi, and X. Wang, “Ace: A cross-platfrom V.Jain,V.Vanhoucke,W.Zhan,W.Zhou,W.Burgard,X.Chen,
visual-exoskeletons for low-cost dexterous teleoperation,” arXiv X.Chen,X.Wang,X.Zhu,X.Geng,X.Liu,X.Liangwei,X.Li,
preprint arXiv:240, 2024. Y.Pang,Y.Lu,Y.J.Ma,Y.Kim,Y.Chebotar,Y.Zhou,Y.Zhu,
[10] Y. Zhu, P. Stone, and Y. Zhu, “Bottom-up skill discovery from Y.Wu,Y.Xu,Y.Wang,Y.Bisk,Y.Dou,Y.Cho,Y.Lee,Y.Cui,
unsegmented demonstrations for long-horizon robot manipula- Y. Cao, Y.-H. Wu, Y. Tang, Y. Zhu, Y. Zhang, Y. Jiang, Y. Li,
tion,” IEEE Robotics and Automation Letters, vol. 7, no. 2, pp. Y.Li,Y.Iwasawa,Y.Matsuo,Z.Ma,Z.Xu,Z.J.Cui,Z.Zhang,
4126–4133, 2022. Z. Fu, and Z. Lin, “Open X-Embodiment: Robotic learning
[11] H. Liu, S. Nasiriany, L. Zhang, Z. Bao, and Y. Zhu, “Robot datasets and RT-X models,” https://arxiv.org/abs/2310.08864,
learning on the job: Human-in-the-loop autonomy and learning 2023.
during deployment,” Robotics: Science and Systems XIX, 2023. [16] J. Duan, Y. R. Wang, M. Shridhar, D. Fox, and R. Krishna,
[12] D. Rakita, B. Mutlu, and M. Gleicher, “An autonomous dy- “Ar2-d2: Training a robot without a robot,” in Conference on
namic camera method for effective remote teleoperation,” in Robot Learning. PMLR, 2023, pp. 2838–2848.
Proceedings of the 2018 ACM/IEEE International Conference [17] X. Jiang, P. Mattes, X. Jia, N. Schreiber, G. Neumann, and
on Human-Robot Interaction, 2018, pp. 325–333. R. Lioutikov, “A comprehensive user study on augmented
[13] P. Stotko, S. Krumpen, M. Schwarz, C. Lenz, S. Behnke, reality-based data collection interfaces for robot learning,” in
R. Klein, and M. Weinmann, “A vr system for immersive Proceedings of the 2024 ACM/IEEE International Conference
teleoperation and live exploration with a mobile robot,” in 2019 on Human-Robot Interaction, 2024, pp. 333–342.
IEEE/RSJ International Conference on Intelligent Robots and [18] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel,
Systems (IROS). IEEE, 2019, pp. 3630–3637. and S. Song, “Diffusion policy: Visuomotor policy learning
[14] A. Mandlekar, Y. Zhu, A. Garg, J. Booher, M. Spero, A. Tung, via action diffusion,” in Proceedings of Robotics: Science and
J. Gao, J. Emmons, A. Gupta, E. Orbay et al., “Roboturk: Systems (RSS), 2023.
A crowdsourcing platform for robotic skill learning through [19] B. D. Argall, S. Chernova, M. Veloso, and B. Browning, “A
imitation,” in Conference on Robot Learning. PMLR, 2018, survey of robot learning from demonstration,” Robotics and
pp. 879–893. autonomous systems, vol. 57, no. 5, pp. 469–483, 2009.
[15] O. X.-E. Collaboration, A. O’Neill, A. Rehman, A. Maddukuri, [20] H. Ravichandar, A. S. Polydoros, S. Chernova, and A. Billard,
A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Man- “Recentadvancesinrobotlearningfromdemonstration,”Annual
dlekar, A. Jain, A. Tung, A. Bewley, A. Herzog, A. Irpan, review of control, robotics, and autonomous systems, vol. 3,
A.Khazatsky,A.Rai,A.Gupta,A.Wang,A.Kolobov,A.Singh, no. 1, pp. 297–330, 2020.
A.Garg,A.Kembhavi,A.Xie,A.Brohan,A.Raffin,A.Sharma, [21] I. El Rassi and J.-M. El Rassi, “A review of haptic feedback in
A. Yavary, A. Jain, A. Balakrishna, A. Wahid, B. Burgess- tele-operated robotic surgery,” Journal of medical engineering
Limerick, B. Kim, B. Schölkopf, B. Wulfe, B. Ichter, C. Lu, & technology, vol. 44, no. 5, pp. 247–254, 2020.
C. Xu, C. Le, C. Finn, C. Wang, C. Xu, C. Chi, C. Huang, [22] S. Young, D. Gandhi, S. Tulsiani, A. Gupta, P. Abbeel, and
C. Chan, C. Agia, C. Pan, C. Fu, C. Devin, D. Xu, D. Morton, L. Pinto, “Visual imitation made easy,” in Conference on Robot
D. Driess, D. Chen, D. Pathak, D. Shah, D. Büchler, D. Jayara- Learning. PMLR, 2021, pp. 1992–2005.

[23] C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng,
R. Tedrake, and S. Song, “Universal manipulation interface:
In-the-wild robot teaching without in-the-wild robots,” in Pro-
ceedings of Robotics: Science and Systems (RSS), 2024.
[24] Y. Qin, W. Yang, B. Huang, K. Van Wyk, H. Su, X. Wang,
Y.-W. Chao, and D. Fox, “Anyteleop: A general vision-based
dexterous robot arm-hand teleoperation system,” in Robotics:
Science and Systems, 2023.
[25] R. Ding, Y. Qin, J. Zhu, C. Jia, S. Yang, R. Yang, X. Qi,
and X. Wang, “Bunny-visionpro: Real-time bimanual dexterous
teleoperation for imitation learning,” 2024.
[26] S. Wrede, C. Emmerich, R. Grünberg, A. Nordmann,
A. Swadzba, and J. Steil, “A user study on kinesthetic teaching
of redundant robots in task and configuration space,” Journal of
Human-Robot Interaction, vol. 2, no. 1, pp. 56–81, 2013.
[27] M. Sakr, M. Freeman, H. M. Van der Loos, and E. Croft,
“Traininghumanteachertoimproverobotlearningfromdemon-
stration: A pilot study on kinesthetic teaching,” in 2020 29th
IEEEInternationalConferenceonRobotandHumanInteractive
Communication (RO-MAN). IEEE, 2020, pp. 800–806.
[28] K. Gandhi, S. Karamcheti, M. Liao, and D. Sadigh, “Eliciting
compatible demonstrations for multi-human imitation learning,”
inProceedingsofthe6thConferenceonRobotLearning(CoRL),
2022.
[29] J. Gao, A. Xie, T. Xiao, C. Finn, and D. Sadigh, “Efficient
data collection for robotic manipulation via compositional
generalization,”inProceedingsofRobotics:ScienceandSystems
(RSS), 2024.
[30] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning
for image recognition,” in Proceedings of the IEEE conference
on computer vision and pattern recognition, 2016, pp. 770–778.
[31] P. Kormushev, S. Calinon, and D. G. Caldwell, “Imitation learn-
ing of positional and force skills demonstrated via kinesthetic
teaching and haptic input,” Advanced Robotics, vol. 25, no. 5,
pp. 581–603, 2011.
[32] A.Montebelli,F.Steinmetz,andV.Kyrki,“Onhandingdownour
tools to robots: Single-phase kinesthetic teaching for dynamic
in-contact tasks,” in 2015 IEEE International Conference on
Robotics and Automation (ICRA). IEEE, 2015, pp. 5628–5634.
[33] F. E. Jedrzej Orbik, “Oculus reader: Robotic teleoperation
interface,”2021,accessed:YYYY-MM-DD.[Online].Available:
https://github.com/rail-berkeley/oculus_reader
[34] F. M. Calisto and J. C. Nascimento, “Nasa-tlx survey,”
2018. [Online]. Available: http://rgdoi.net/10.13140/RG.2.2.
26978.79044