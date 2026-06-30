Article
TheInternationalJournalof
RoboticsResearch
| How | to train |     | your | robot |     | with | deep |     |     |     |     |     |     |     |
| --- | -------- | --- | ---- | ----- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
2021,Vol.40(4-5)698–721
(cid:2)TheAuthor(s)2021
| reinforcement |     |     | learning: |     |     | lessons | we  | have |     |     |     |     |     |     |
| ------------- | --- | --- | --------- | --- | --- | ------- | --- | ---- | --- | --- | --- | --- | --- | --- |
Articlereuseguidelines:
| learned |     |     |     |     |     |     |     |     |     |     | sagepub.com/journals-permissions |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- |
DOI:10.1177/0278364920987859
journals.sagepub.com/home/ijr
Julian Ibarz1 , Jie Tan1, Chelsea Finn1,2, Mrinal Kalakrishnan3 ,
| Peter Pastor3 |     | and | Sergey | Levine1,4 |     |     |     |     |     |     |     |     |     |     |
| ------------- | --- | --- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Abstract
Deep reinforcement learning (RL)hasemergedasa promisingapproach forautonomouslyacquiring complex behaviors
from low-level sensor observations. Although a large portion of deep RL research has focused on applications in video
games and simulated control, which does not connect with theconstraints of learning in real environments, deep RL has
also demonstrated promise in enabling physical robots to learn complex skills in the real world. At the same time, real-
worldroboticsprovidesanappealingdomainforevaluatingsuchalgorithms,asitconnectsdirectlytohowhumanslearn:
as an embodied agentin the real world. Learning to perceive and move in the real world presents numerouschallenges,
someofwhichareeasiertoaddressthanothers,andsomeofwhichareoftennotconsideredinRLresearchthatfocuses
only on simulated domains. In this review article, we present a number of case studies involving robotic deep RL.
Building off of these case studies, we discuss commonly perceived challenges in deep RL and how they have been
addressedin theseworks.We also provide anoverview ofotheroutstandingchallenges,many of whichare uniquetothe
real-worldroboticssettingandarenotoftenthefocusofmainstreamRLresearch.Ourgoalistoprovidearesourceboth
for roboticists and machine learning researchers who are interested in furthering the progress of deep RL in the real
world.
Keywords
Robotics,reinforcementlearning,deeplearning
1. Introduction unknown objects, and to learn a state representation suit-
ableformultipletasks.
| Robotic         | learning   | lies at | the intersection |              | of machine    |          | learn- |                          |            |                |             |               |             |          |
| --------------- | ---------- | ------- | ---------------- | ------------ | ------------- | -------- | ------ | ------------------------ | ---------- | -------------- | ----------- | ------------- | ----------- | -------- |
|                 |            |         |                  |              |               |          |        | Despite                  | being      | an interesting | medium,     | there         | is a        | signifi- |
| ing and         | robotics.  | From    | the perspective  |              | of a machine  |          | learn- |                          |            |                |             |               |             |          |
|                 |            |         |                  |              |               |          |        | cant barrier             | for        | a machine      | learning    | researcher    |             | to enter |
| ing researcher  | interested |         | in studying      |              | intelligence, | robotics |        |                          |            |                |             |               |             |          |
|                 |            |         |                  |              |               |          |        | robotics                 | and vice   | versa.         | Beyond      | the cost      | of a robot, | there    |
| is an appealing | medium     |         | to study         | as it        | provides      | a lens   | into   |                          |            |                |             |               |             |          |
|                 |            |         |                  |              |               |          |        | are many                 | design     | choices        | in choosing | how           | to set-up   | the      |
| the constraints | that       | humans  | and              | animals      | encounter     |          | when   |                          |            |                |             |               |             |          |
|                 |            |         |                  |              |               |          |        | algorithmandtherobot.For |            |                | example,    | reinforcement |             | learn-   |
| learning,       | uncovering | aspects | of               | intelligence | that          | might    | not    |                          |            |                |             |               |             |          |
|                 |            |         |                  |              |               |          |        | ing (RL)                 | algorithms | require        | learning    | from          | experience  | that     |
otherwise be apparent to study when we restrict ourselves the robot autonomously collects itself, opening up many
| to simulated   | environments.  |        | For           | example,  | robots           |           | receive |                  |         |              |                 |     |            |         |
| -------------- | -------------- | ------ | ------------- | --------- | ---------------- | --------- | ------- | ---------------- | ------- | ------------ | --------------- | --- | ---------- | ------- |
|                |                |        |               |           |                  |           |         | choices          | in how  | the learning | is initialized, |     | how to     | prevent |
| streams        | of raw sensory |        | observations  |           | as a consequence |           | of      |                  |         |              |                 |     |            |         |
|                |                |        |               |           |                  |           |         | unsafe behavior, |         | and how      | to define       | the | goal or    | reward. |
| their actions, | and            | cannot | practically   | obtain    | large            | amounts   |         |                  |         |              |                 |     |            |         |
|                |                |        |               |           |                  |           |         | Likewise,        | machine | learning     | and             | RL  | algorithms | also    |
| of detailed    | supervision    |        | beyond        | observing |                  | these     | sensor  |                  |         |              |                 |     |            |         |
| readings.      | This makes     | for    | a challenging |           | but highly       | realistic |         |                  |         |              |                 |     |            |         |
1RoboticsatGoogle,MountainView,CA,USA
| learning | problem. | Further, | unlike | agents | in video |     | games, |     |     |     |     |     |     |     |
| -------- | -------- | -------- | ------ | ------ | -------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
2StanfordUniversity,Stanford,CA,USA
robotsdonotreadilyreceiveascoreorrewardfunctionthat 3EverydayRobots,X,TheMoonshotFactory,MountainView,CA,USA
isshapedfor their needs,andinsteadneedtodeveloptheir 4UniversityofCaliforniaBerkeley,Berkeley,CA,USA
| own internal | representation |     |     | of progress | towards |     | goals. |     |     |     |     |     |     |     |
| ------------ | -------------- | --- | --- | ----------- | ------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
Correspondingauthor:
| From the | perspective | of  | robotics | research, | using | learning- |     |     |     |     |     |     |     |     |
| -------- | ----------- | --- | -------- | --------- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
JulianIbarz,Google,Inc.,1600AmphitheatreParkway,MountainView,
| based techniques |     | is appealing |     | because | it can | enable | robots |     |     |     |     |     |     |     |
| ---------------- | --- | ------------ | --- | ------- | ------ | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
CA94043,USA.
to move towards less-structured environments, to handle Email:julianibarz@google.com

Ibarzetal. 699
provide a number of important design choices and hyper-
parametersthatcanbetrickytoselect.
Motivated by these challenges for the researchers in the
respective fields, our goal in this article is to provide a
high-level overviewof how deep RL can be approached in
a robotics context, summarize theways in which key chal-
lengesinRLhavebeenaddressedinsomeofourownpre-
viouswork, and provide a perspective on major challenges
that remain to be solved, many of which are not yet the
subjectofactiveresearchintheRLcommunity.
There have been high-quality survey articles about
applying machine learning to robotics. Deisenroth et al.
(2013) focused on policy search techniques for robotics,
whereasKoberetal.(2013)focusedonRL.Morerecently,
Kroemer et al. (2019) reviewed the learning algorithms for
manipulationtasks.Su¨nderhaufetal.(2018)identifiedcur-
rentareasofresearchindeeplearningthatwererelevantto
robotics, and described a few challenges in applying deep
learningtechniquestorobotics.
Instead of writing another comprehensive literature
review, we first center our discussion around three case
Fig.1. APR2learnstoplacearedtrapezoidblockintoashape-
studies from our own prior work. We then provide an in- sortingcube.WithLevineetal.(2016),itlearnslocalpoliciesfor
depthdiscussionofafewtopicsthatweconsiderespecially eachinitialpositionofthecube,whichcanberesetautomatically
important given our experience. This article naturally using the robot’s left arm. The local policies are distilled into a
includes numerous opinions. When sharing our opinions, global policy that takes images as input, rather than the cube’s
we do our best to ground our recommendations in empiri- location.
cal evidence, while also discussing alternative options. We
hope that,bydocumentingtheseexperiences andour prac-
tices, we can provide a useful resource both for roboticists falls into the realm of RL (Sutton and Barto 2018). In the
interested in using deep RL and for machine learning paradigm of RL, samples of state-action sequences (trajec-
researchersinterestedinworkingwithrobots. tories) are required in order to learn how to control the
robot and maximize the reward. In model-based RL, the
samplesareusedtolearnadynamicsmodeloftheenviron-
2. Background ment,whichinturnisusedinaplanningoroptimalcontrol
algorithm to produce a policy or the sequence of controls.
In this section,we provide a brief,informal introductionto
Inmodel-freeRL,thedynamicsarenotexplicitlymodeled,
RL,by contrasting it with classical techniques of program-
but instead the optimal policy or value function is learned
ming robot behavior. A robotics problem is formalized by
directly by interaction with the environment. Both model-
defining a state and action space, and the dynamics which
based and model-free RL have their own strengths and
describehowactions influencethestateofthesystem.The
weaknesses, and the choice of algorithm depends heavily
state space includes internal states of the robot as well as
on the properties required. These considerations are dis-
the state of the world that is intended to be controlled.
cussedfurtherinSections3and4.
Quite often, the state is not directly observable–instead, the
robot is equipped with sensors, which provide observations
thatcanbeusedtoinfer thestate.Thegoalmaybedefined
3. Case studies in robotic deep RL
either as a target state to be achieved, or as a reward func-
tiontobemaximized.Wewanttofindacontroller,(known In this section, we present a few case studies of applica-
as a policyinRLparlance),that mapsstates toactions ina tionsofdeepRLtovariousrobotictasksthatwehavestud-
waythatmaximizestherewardwhenexecuted. ied. The applications span manipulation, grasping, and
Ifthestatescanbedirectlyorindirectlyobserved,anda legged locomotion. The sensory inputs used range from
model of the system dynamics is known, the problem can low-dimensional proprioceptive state information to high-
be solved with classical methods such as planning or opti- dimensional camera pixels, and the action spaces include
mal control. These methods use the knowledge of the bothcontinuousanddiscreteactions.
dynamics model to search for sequences of actions that By consolidating our experiences from those case stud-
when applied from the start state, take the system to the ies,weseektoderiveacommonunderstandingofthekinds
desired goal state or maximize the achieved reward. of robotic tasks that are tractable to solve with deep RL
However, if the dynamics model is unknown, the problem today. Using these case studies as a backdrop, we point

| 700 |     |     |     |     |     |     | TheInternationalJournalofRoboticsResearch40(4-5) |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- |
Fig.2. Examplesofmodel-free-basedalgorithmslearningskillsinafewhoursfromlow-dimensionalstateobservations:(a)learning
tostackLegoblockswithHaarnojaetal.(2018a);(b)learningdooropeningwithGuetal.(2017).
readers to outstanding challenges that remain to be solved shapeintotheholeataspecificposition.Inthecaseofthe
andarecommonlyencounteredinSection4. experiment illustrated in Figure 1, nine local policies were
trainedforninedifferentcubepositions,andasingleglobal
|               |     |              |     |        |     |     | policy was | then | trained | to perform | the | task from | images. |
| ------------- | --- | ------------ | --- | ------ | --- | --- | ---------- | ---- | ------- | ---------- | --- | --------- | ------- |
| 3.1. Learning |     | manipulation |     | skills |     |     |            |      |         |            |     |           |         |
Typically,thelocalpoliciesdonotusedeepRL,anddonot
Reinforcement learning of individual robotic skills has a useimageinputs.Theyinsteaduseobservationsthatreflect
| long history | (Daniel | et  | al., 2013; | Ijspeert | et  | al., 2002; |     |     |     |     |     |     |     |
| ------------ | ------- | --- | ---------- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
thelow-dimensional,‘‘true’’stateofthesystem,suchasthe
Koberetal.,2013;Konidarisetal.,2012;Manschitzetal., positionoftheshape-sortingcubeinthepreviousexample,
2014; Peters et al., 2010; Peters and Schaal, 2008). Deep in order to learn more efficiently. Local policies can be
| RL provides | some | appealing | capabilities |     | in this | regard: |         |                  |     |         |     |         |         |
| ----------- | ---- | --------- | ------------ | --- | ------- | ------- | ------- | ---------------- | --- | ------- | --- | ------- | ------- |
|             |      |           |              |     |         |         | trained | with model-based |     | methods |     | such as | LQR-FLM |
deep neural network policies can alleviate the need to (LevineandAbbeel,2014;Levineetal.,2016),whichuses
manuallydesignpolicyclasses,provideamoderateamount
|     |     |     |     |     |     |     | linear quadratic |     | regulator | (LQR) | with | fitted time-varying |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --------- | ----- | ---- | ------------------- | --- |
of generalization tovariable initial conditions and, perhaps linear models, or model-free techniques such as PI2
most importantly, allow for end-to-end joint training for (Chebotaretal.,2017a,b).
| both perceptionand |     | control, | learning | to directly |     | map high- |        |             |           |     |        |               |        |
| ------------------ | --- | -------- | -------- | ----------- | --- | --------- | ------ | ----------- | --------- | --- | ------ | ------------- | ------ |
|                    |     |          |          |             |     |           | A full | theoretical | treatment |     | of the | guided policy | search |
dimensionalsensoryinputs,suchasimages,tocontrolout- algorithm is outside the scope of this article, and we refer
| puts. Of | course, | such end-to-end |     | training | itself | presents | a          |          |      |         |       |         |             |
| -------- | ------- | --------------- | --- | -------- | ------ | -------- | ---------- | -------- | ---- | ------- | ----- | ------- | ----------- |
|          |         |                 |     |          |        |          | the reader | to prior | work | on this | topic | (Levine | and Abbeel, |
number of challenges, which we will also discuss. We dis- 2014;Levineetal.,2016;LevineandKoltun,2013).
cussafewcasestudiesonsingle-taskdeeproboticlearning
|               |     |           |          |           |             |     | An important |         | point          | of discussion |            | for this article, | how-   |
| ------------- | --- | --------- | -------- | --------- | ----------- | --- | ------------ | ------- | -------------- | ------------- | ---------- | ----------------- | ------ |
| with avariety | of  | different | methods, | including | model-based |     |              |         |                |               |            |                   |        |
|               |     |           |          |           |             |     | ever, is     | the set | of assumptions |               | underlying | guided            | policy |
and model-free algorithms, and with different starting search methods. Typically, such methods assume that the
assumptions.
|     |     |     |     |     |     |     | local policies | can  | be  | optimized | with    | simple, | ‘‘shallow’’ |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ---- | --- | --------- | ------- | ------- | ----------- |
|     |     |     |     |     |     |     | RL methods,    | such | as  | LQR-FLM   | or PI2. | This    | assumption  |
3.1.1. Guided policy search. Guided policy search meth- is reasonable for robotic manipulation tasks trained in
ods (Levine et al., 2016) were among the first deep RL laboratory settings, but can prove difficult in (1) open-
|         |            |              |         |     |       |            | world environments |     | where | the | low-level | state | of the sys- |
| ------- | ---------- | ------------ | ------- | --- | ----- | ---------- | ------------------ | --- | ----- | --- | --------- | ----- | ----------- |
| methods | that could | be tractably | applied | to  | learn | individual |                    |     |       |     |           |       |             |
neural network skills for image-based manipulation tasks. temcannotbeeffectivelymeasuredandin(2)settingswhere
|          |           |                          |     |     |     |           | resetting | the environment |     | poses | a challenge. | For | example, |
| -------- | --------- | ------------------------ | --- | --- | --- | --------- | --------- | --------------- | --- | ----- | ------------ | --- | -------- |
| Thebasic | principle | behindthesemethodsisthat |     |     |     | theneural |           |                 |     |       |              |     |          |
network policy is ‘‘guided’’ by another RL method, typi- intheexperiment inFigure 1,therobot isholdingthe cube
callyamodel-basedRLalgorithm.Theneuralnetworkpol- in its left arm during training, so that the position of the
icy is referred to as a global policy, and is trained to cube can be provided to the low-level policies and so that
perform the task successfully from raw sensory observa- therobotcanautomaticallyrepositionthecubeintodifferent
|           |       |          |             |     |             |        | positions | deterministically. |     | We  | discuss | these challenges | in  |
| --------- | ----- | -------- | ----------- | --- | ----------- | ------ | --------- | ------------------ | --- | --- | ------- | ---------------- | --- |
| tions and | under | moderate | variability | in  | the initial | condi- |           |                    |     |     |         |                  |     |
tions.Forexample,asshowninFigure1,theglobalpolicy moredetailinSections4.12and4.2.3.
might be required to put the red shape into the shape sort- Nonetheless, for learning individual robotic skills,
ing cube at different positions. This requires the policy to guided policy search methods have been applied widely
implicitlydeterminethepositionofthehole.However,this and to a broad range of behaviors, ranging from inserting
is not supervised directly, but instead the perception objects into containers and putting caps on bottles (Levine
mechanism is learned end-to-end together with control. et al., 2016), opening doors (Chebotar et al., 2017b), and
Supervision is provided from multiple individual model- shooting hockey pucks (Chebotar et al., 2017a). In most
basedlearnersthatlearnseparatelocalpoliciestoinsertthe cases, guided policy search methods are very efficient in

Ibarzetal. 701
terms of the number of samples, particularly as compared learning (Gu et al., 2017; Haarnoja et al., 2018a) or actor–
to model-free RL algorithms, since the model-based local criticdesigns(Haarnojaetal.,2018b),on-policypolicygra-
policy learners can acquire the local solutions quickly and dient algorithms have also been used. Although standard
efficiently. Image-based tasks can typically be learned in a configurations of these methods can require around 10
few hundred trials, corresponding to 2–3 hours of real- times the number of samples as off-policy algorithms, on-
world training, including all resets and network training policy methods such as TRPO (Schulman et al., 2015),
time(Chebotaretal.,2017a;Levineetal.,2016). NPG(Kakade,2002),andPPO(Schulmanetal.,2017)can
be tuned to only be two or three times less efficient than
off-policy algorithms in some tasks (Peng et al., 2019). In
3.1.2.Model-freeskilllearning. Model-freeRLalgorithms
somecases,thisincreasedsamplerequirementmaybejusti-
liftsomeofthelimitationsofguidedpolicysearch,suchas
fiedbyeaseofuse,betterstability,andbetterrobustnessto
the need to decompose a task into multiple distinct and
suboptimal hyperparameter settings. On-policy policy gra-
repeatable initial states or the need for a model-basedopti-
dient algorithms have been used to learn tasks such as peg
mizer that typically operates on a low-dimensional state
insertion (Lee et al., 2019), targeted throwing Ghadirzadeh
representation, but at the cost of a substantial increase in
etal.(2017),anddexterousmanipulation(Zhuetal.,2019)
the required number of samples. For example, the Lego
directlyonreal-worldhardware,andcanbefurtheracceler-
block stacking experiment reported by Haarnoja et al.
atedwithexampledemonstrations(Zhuetal.,2019).
(2018a)requiredalittleover2hoursofinteraction,whereas
Although, in principle, model-free deep RL algorithms
comparable Lego block stacking experiments reported by
should excel at learning directly from raw image observa-
Levine et al. (2015) required about 10 minutes of training.
tions, in practice this is a particularly difficult training
Thegap in training time tends to close a bit when we con-
regime, and good real-world results with model-free deep
sidertaskswithmorevariability:guidedpolicysearchgen-
RL learning directly from raw image observations have
erally requires a linear increase in the number of samples
only been obtained recently, with accompanying improve-
withmoreinitialstates,whereasmodel-freealgorithmscan
ments in the efficiency and stability of off-policy model-
better integrate experience from multiple initial states and
free RL methods (Fujimoto et al., 2018; Haarnoja et al.,
goals, typically with sub-linear increase in sample require-
2019, 2018b). The SAC algorithm can learn tasks in the
ments. As model-free methods generally do not require a
real world directly from images (Haarnoja et al., 2019;
lower-dimensional state for model-based trajectory optimi-
Singh et al., 2019), and several other recent works have
zation, they can also be applied to tasks that can only be
studied real-world learning from images (Schoettler et al.,
definedonimages,withoutanexplicitrepresentationlearn-
2019;Schwabetal.,2019).
ingphase.
Alloftheseexperimentswereconductedinrelativelycon-
Although there is a long history of model-free RL in
strained laboratory environments, and although the learned
robotics (Daniel et al., 2013; Ijspeert et al., 2002; Kober
skillsuserawimageobservations,theygenerallyhavelimited
et al., 2013; Konidaris et al., 2012; Manschitz et al., 2014;
robustness to realistic visual perturbations andcan only han-
Peters et al., 2010; Peters and Schaal, 2008), modern
dlethespecificobjectsonwhichtheyaretrained.Wediscuss
model-free deep RL algorithms have been used more
inSection3.2howimage-baseddeepRLcanbescaledupto
recently for tasks such as door opening (Gu et al., 2017)
enablemeaningfulgeneralization.Furthermore,amajorchal-
and assembly and stacking of objects (Haarnoja et al.,
lenge in learning from raw image observations in the real
2018a) with low-dimensional state observations. These
world is the problem of reward specification: if the robot
methods were generally based on off-policy actor–critic
needs to learn from raw image observations, it also needs to
designs, such as DDPG or NAF (Gu et al., 2016; Lillicrap
evaluate the reward function from raw image observations,
etal.,2015),softQ-learning(Haarnojaetal.,2018a,b),and
which itself can require a hand-designed perception system,
soft actor–critic (SAC; Haarnoja et al., 2019). An illustra-
partly defeating the purpose of learning from images in the
tionof some ofthesetasksisshowninFigure2.Fromour
first place, or otherwise require extensive instrumentation of
experiences, we generally found that simple manipulation
theenvironment(Zhuetal.,2019).Wediscussthischallenge
tasks, such as opening doors and stacking Lego blocks,
furtherinSection4.9.
either with a single position or some variation in position,
can be learned in 2–4 hours of interaction, with either tor-
que control or end-effector position control. Incorporating 3.1.3. Learning predictive models for multiple skills with
demonstration data and other sources of supervision can visualforesight. Althoughtherearesituationswhereasin-
furtheracceleratesomeofthesemethods(Riedmilleretal., gle skill is all a robot will need to perform, it is not suffi-
2018; Vecˇcer´ık et al., 2017). Section 4.2 describes other cient for general-purpose robots where learning each skill
techniques to make those approaches more sample from scratch is impractical. In such cases, there is a great
efficient. deal of knowledgethat canbeshared across tasksto speed
Althoughmostmodel-freedeepRLalgorithmsthathave up learning. In this section, we discuss one particular case
beenappliedtolearnmanipulationskillsdirectlyfromreal- study of scalable multi-task learning of vision-based
world data have used off-policy algorithms based on Q- manipulation skills, with a focus on tasks that require

| 702 |     |     |     |     |     |     |     | TheInternationalJournalofRoboticsResearch40(4-5) |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- |
pushingorpickingandplacingobjects.Unlikeintheprevi-
| ous section,               | if             | our goal    | is to        | learn many              | tasks       | with    | many    |     |     |     |     |
| -------------------------- | -------------- | ----------- | ------------ | ----------------------- | ----------- | ------- | ------- | --- | --- | --- | --- |
| objects,                   | a challenge    | discussed   |              | in detail               | in          | Section | 4.5,    | it  |     |     |     |
| will be                    | most practical |             | to learn     | from                    | data that   | can     | be col- |     |     |     |     |
| lected at                  | scale,         | without     | human        | supervision             |             | or      | even    | a   |     |     |     |
| humanattendingtherobot.Asa |                |             |              | result,itbecomesimpera- |             |         |         |     |     |     |     |
| tive to remove             |                | assumptions |              | such as                 | regular     | resets  | of the  |     |     |     |     |
| environment                | or             | a carefully | instrumented |                         | environment |         | for     |     |     |     |     |
measuringreward.
| Motivated         |        | by these | challenges,    |                    | the visual   |         | foresight |     |     |     |     |
| ----------------- | ------ | -------- | -------------- | ------------------ | ------------ | ------- | --------- | --- | --- | --- | --- |
| approach          | (Ebert | et al.,  | 2018;          | Finn               | and          | Levine, | 2017)     |     |     |     |     |
| leverages         | large  | batches  | of off-policy, |                    | autonomously |         | col-      |     |     |     |     |
| lected experience |        | to train | an             | action-conditioned |              | video   | pre-      |     |     |     |     |
| diction           | model, | and      | then uses      | this               | model        | to      | plan to   |     |     |     |     |
accomplishtasks.Thekeyintuitionofthisapproachisthat
| knowledge | learned | about | physics | and | dynamics |     | can be |     |     |     |     |
| --------- | ------- | ----- | ------- | --- | -------- | --- | ------ | --- | --- | --- | --- |
sharedacrosstasksandlargelydecoupledfromgoal-centric
| knowledge. | These | models | are | trained | using | streams | of  |                  |              |          |                         |
| ---------- | ----- | ------ | --- | ------- | ----- | ------- | --- | ---------------- | ------------ | -------- | ----------------------- |
|            |       |        |     |         |       |         |     | Fig. 3. Close-up | of our robot | grasping | set-up (left) and about |
robotexperience,consistingoftheobservedcameraimages 1,000 visually and physically diverse training objects (right).
andactionstaken,withoutassumptionsaboutrewardinfor- Each robot consists of a KUKA LBR IIWA arm with a two-
mation.Aftertraining,ahumanprovidesagoal,byprovid- fingergripperandanover-the-shoulderRGBcamera.
| ing an image  |           | of the goal    | or        | by indicating |     | that an         | object |               |            |             |                       |
| ------------- | --------- | -------------- | --------- | ------------- | --- | --------------- | ------ | ------------- | ---------- | ----------- | --------------------- |
| corresponding |           | to a specified |           | pixel should  |     | be moved        | to     | a             |            |             |                       |
|               |           |                |           |               |     |                 |        | discuss these | challenges | in Sections | 4.6 and 4.9. Finally, |
| desired       | position. | Then,          | the robot | performs      |     | an optimization |        |               |            |             |                       |
over actionsequences in aneffort to minimize thedistance findingplansfor complextasks posea challengingoptimi-
betweenthepredictedfutureandthedesiredgoal. zation problem for the planner, which can be addressed to
This algorithm has been used to complete object rear- some degree using demonstrations (for details, see Section
rangement tasks such as grasping an apple and putting it 4.4). This has enabled the models to be used for tool use
taskssuchassweepingtrashintoadustpan,wipingobjects
| on a plate, | reorienting |     | a stapler, | and | pushing | other | objects |     |     |     |     |
| ----------- | ----------- | --- | ---------- | --- | ------- | ----- | ------- | --- | --- | --- | --- |
into configurations (Ebert et al., 2018; Finn and Levine, offaplatewithasponge,andhookingout-of-reachobjects
2017). Further, it has been used for visual reaching tasks withahook(Xieetal.,2019).
| (Byravan                            | et al., | 2018), | object | pushing | and        | trajectory | fol-     |               |         |           |     |
| ----------------------------------- | ------- | ------ | ------ | ------- | ---------- | ---------- | -------- | ------------- | ------- | --------- | --- |
| lowingtasks(Yen-Chenetal.,2020),for |         |        |        |         | satisfying |            | relative |               |         |           |     |
|                                     |         |        |        |         |            |            |          | 3.2. Learning | tograsp | with deep | RL  |
| object positioning                  |         | tasks  | (Xie   | et al., | 2018),     | and for    | cloth    |               |         |           |     |
manipulation tasks such as folding shorts, covering an Learningtograspremainsoneofthemostsignificantopen
object with a towel, and rearranging a sleeve of a shirt problems in robotics, requiring complex interaction with
(Ebert et al., 2018). Importantly, each collection of tasks previouslyunseenobjects,closed-loopvision-basedcontrol
can be performed using a single learned model and plan- toreacttounforeseendynamicsorsituations.Indeed,most
ning approach, rather than having to retrain a policy for object interaction behaviors require grasping the object as
eachindividualtaskorobject.Thisgeneralizationprecisely the first step. Prior work typically tackles grasping as the
resultsfromthealgorithmsabilitytoleveragebroad,auton- problem of identifying suitable grasp locations (Mahler
omously collected datasets with hundreds of objects, and et al., 2018; Morrison et al., 2018b; ten Pas et al., 2017;
the ability to train reusable,task-agnostic models from this Zeng et al., 2018), rather than as an explicit control prob-
data. lem. The motivation for this problem definition is to allow
Despite these successes, there are a number of limita- the visual problem to be completely separated from the
tions and challenges that we highlight here. First, although control problem, which becomes an open-loop control
thedatacollectionprocessdoesnotrequirehumaninvolve- problem. This separation significantly simplifies the prob-
ment, it uses a specialized set-upwith the robot in front of lem. The drawback is that this approach cannot adapt to
a bin with tilted edges that ensure that objects not fall out, dynamic environments or refine its strategy while execut-
along with an action space that is constrained within the ing the grasp. Can deep RL provide us with a mechanism
bin. This allows continuous, unattended data collection, tolearntograspdirectlyfromexperience,andasadynami-
discussed further in Section 4.7. Outside of laboratory set- calandinteractiveprocess?
tings, however, collecting data in unconstrained, open- A number of works have studied closed-loop grasping
worldenvironmentsintroducesanumberof importantchal- (Hausman et al., 2017; Levine et al., 2018; Viereck et al.,
lenges,whichwediscussinSection4.12.Second,inaccura- 2017; Yu and Rodriguez, 2018). In contrast to these
cies in the model and reward function can be exploited by methods, which frame closed-loop grasping as a servoing
the planner, leading to inconsistencies in performance. We problem, QT-Opt Kalashnikov et al. (2018) uses a general-

Ibarzetal. 703
Fig. 4. Eight grasps from the QT-Opt policy, illustrating some of the strategies discovered by our method: (a), (b) pregrasp
manipulation;(c),(d)graspreadjustment;(e),(f)graspingdynamicobjectsandrecoveryfromperturbations;and(g),(h)graspingin
clutter.
purpose RL algorithm to solve the grasping task, which can achieve excellent grasp success rates even with this
enables multi-step reasoning, in other words, the policy rudimentarysensingset-up.
can be optimized across the entire trajectory. In practice, In this work, we focus on evaluating the success rate of
this enables this method to autonomously acquire thepolicyingraspingneverseenduringtrainingobjectsin
complexgraspingstrategies,someofwhichweillustratein abinusingatop-downgrasping(fourdegreesoffreedom).
Figure4.Thismethodisalsoentirelyself-supervised,using This task definition simplifies some robot safety chal-
only grasp outcome labels that are obtained automatically lenges,whicharediscussedmoreinSection4.11.However,
by the robot. Several works have proposed self-supervised this problem retains the challenging aspects that have been
grasping systems (Levine et al., 2018; Pinto and Gupta, hard to deal with: unknown object dynamics, geometry,
2016), but to the best of the authors’ knowledge, this vision-based closed-loop control, self-supervised approach
methodisthefirsttoincorporate amulti-stepoptimization as well as hand–eye coordination by removing the need to
via RL into a generalizablevision-based system trained on calibratetheentiresystem(cameraandgripperlocationsas
self-supervisedreal-worlddata. wellasworkspaceboundsarenotgiventothepolicy).
Related to this work, Zeng et al. (2018) recently pro- For thisspecifictask,QT-Optcanreach86%graspsuc-
poseda Q-learningframeworkforcombininggraspingand cess when learning completely from data collected from
pushing.QT-Optutilizesamuchmoreflexibleactionspace, previousexperimentswhichwerefertoasofflinedata,and
directly commanding gripper motionin alldegrees offree- can quickly reach 96% success with an additional online
dom in three dimensions, and exhibits substantially better data of 28,000 grasps collected during a joint fine-tuning
performanceandgeneralization.Finally,incontrasttomany training phase. Those results show that RL can be scalable
currentgraspingsystemsthatutilizedepthsensing(Mahler andpracticalonarealroboticapplicationbyeitherallowing
etal.,2018;Morrisonetal.,2018a)orwrist-mountedcam- toreusepastcollectedexperiences(offlinedata),andpoten-
eras (Morrison et al., 2018a; Viereck et al., 2017), QT-Opt tiallytrainingpurelyoffline(noadditionalrobotinteraction
operates on raw monocular RGB observations from an required)oracombinationofofflineandonlineapproaches
over-the-shouldercamerathatdoesn’tneedtobecalibrated. (called joint fine-tuning). Leveraging offline data makes
TheperformanceofQT-Optindicatesthateffectivelearning deep RL a practical approach for robotics as it allows to

704 TheInternationalJournalofRoboticsResearch40(4-5)
3.3. Learning legged locomotion
Although walking and running seems effortless activities
for us, designing locomotion controllers for legged robots
is a long-standing challenge (Raibert, 1986). RL holds the
promisetoautomaticallydesignhigh-performancelocomo-
tion controllers (Ha et al., 2018; Hwangbo et al., 2019;
Kohl and Stone, 2004; Lee et al., 2020; Tedrake et al.,
2015). In this case study, we apply deep RL techniques on
the Minitaur robot (Figure 5), a mechanically simple and
low-cost quadruped platform (De, 2017). We have over-
come significant challenges and developed various
learning-based approaches, with which agile and stable
locomotiongaitsemergeautomatically.
Simulationisanimportantprototypingtoolfor robotics,
Fig. 5. The Minitaur robot learns to walk from scratch using which can help to bypass many challenges of learning on
deepRL. real systems, such as data efficiency and safety. In fact,
most of the prior work used simulation (Brockman et al.,
2016; Coumans andBai,2016) toevaluateandbenchmark
scale the training dataset to a large enough size to allow the learning algorithms (Ha¨ma¨la¨inen et al., 2015; Heess
generalizationtohappen,withasmallroboticfleetofseven et al., 2017; Peng et al., 2018a; Yu et al., 2018). Using
robotsandovera periodofafewmonths,orbyleveraging general-purpose RL algorithms and a simple reward for
simulation, to generalize with a collection effort of just a walking fast and efficiently, we can train the quadruped
fewdays(Jamesetal.,2019;Raoetal.,2020)(seeSection robot to walk in simulation within 2–3 hours. However, a
4.3formoreexamplesofsim-to-realtechniques). policy learnedin simulation usually does notwork wellon
Because the policy is learned by optimizing the reward therealrobot.Thisperformancegapisknownasthereality
across the entire trajectory (optimizing for long-term gap. Our researchhasidentified thekey causes of this gap
reward using Bellman backup), and is constantly replan- anddevelopedvarioussolutions.PleaserefertoSection4.3
ning its next move with vision as an input, the policy can formoredetails.Withthesesim-to-realtransfertechniques,
learn complex behaviors in a self-supervised manner that wecansuccessfullydeploythecontrollers learnedinsimu-
would have been hard to program, such as singulation, lation on the robots with zero or only a handful of real-
pregrasp manipulation, dealing with a cluttered scene, world experiments (Tan et al., 2018; Yu et al., 2019).
learning retrial behaviors as well as handling environment Without much prior knowledge and manual tuning, the
disturbance and dynamic objects (Figure 4). Retrial beha- learning algorithm automatically finds policies that are
viorscanbelearnedbecausethepolicycanquicklyreactto more agile and energy efficient than the controllers devel-
thevisualinput,ateverystep,whichmayshowinonestep opedwiththetraditionalapproaches.
that the object dropped after the gripper lifted it from the Given the initial policies learned in simulation, it is
bin,andthusdecidingtoreattemptagraspinthenewloca- importantthattherobotscancontinuetheirlearningprocess
tiontheobjectfellto. in the real-world in a life-long fashion to adapt their poli-
Section 4.2 describes some of the design principles we cies to the changing dynamics and operation conditions.
used to obtain good data efficiency. Section 4.5 discusses There are three main challenges for real-world learning of
strategies that allowed us to generalize properly to unseen locomotion skills. The first is sample efficiency. Deep RL
objects.Section4.7describeswayswemanagedtoscaleto oftenneedstensofmillionsofdatasamplestolearnmean-
sevenrobotswithonehumanoperatoraswellasenable24 ingfullocomotiongaits,whichcantakemonthsofdatacol-
h/7 day operations. Section 4.4 discusses how we side- lectionontherobot.Thisisfurtherexacerbatedbytheneed
stepped exploration challenges by leveraging scripted of extensive hyperparameter tuning. We have developed
policies. novel solutions that have significantly reduced the sample
The lessons from this work have been that: (1) a lot of complexity (Section 4.2) and the need for hyperparameter
varied data was required to learn generalizable grasping, tuning(Section4.1).
whichmeansthatweneedunattendeddatacollectionanda Robot safety is another bottleneck for real-world train-
scalable RL pipeline; (2) the need for large and varied data ing. During the exploration stage of learning, the robot
meansthatweneedtoleverageallofthepreviouslycollected oftentriesnoisyactuationpatternsthatcausejerkymotions
data so far (offline data) and need a framework that makes andseverewear-and-tearofthemotors.Inaddition,because
this easy is crucial; (3) to achieve maximal performance, the robot has yet to master balancing skills, the repeated
combining offline data with a small amount of online data falling quickly damages the hardware. We discuss in
allowsustogofrom86%to96%graspsuccess. Section4.11 several techniques that we employ to mitigate

Ibarzetal. 705
the safety concerns for learning locomotion with real methods (Chiang et al., 2019). However, such methods
robots. typicallyrequirerunningRLalgorithmsmanytimes,which
The last challenge is asynchronous control. On a physi- is impractical outside of simulated domains. A potentially
cal robot, sensor measurements, neural network inference, promising alternative available for off-policy RL methods
and action execution usually happen simultaneously and is to run multiple learning processes with different hyper-
asynchronously. The observation that the agent receives parameters on the same off-policy data buffer, effectively
may not be the latest owing to computation and communi- using one run’s worth of data for multiple independent
cation delays. However, this asynchrony breaks the funda- learning processes. Recent work has explored this idea in
mental assumption of the markovian decision process simple simulated domains (Khadka et al., 2019), though it
(MDP). Consequently, the performance of many deep RL remainstobeseenifsuchanapproachcanbescaledupto
algorithms drop dramatically in the presence of asynchro- real-worldroboticlearningsettings.Anotherapproachisto
nous control. In locomotion tasks, asynchronous control is developalgorithmsthatautomaticallytunetheirownhyper-
essentialtoachieve highcontrolfrequency.Inotherwords, parameters,asinthecaseofSACwithautomatedtempera-
to learn towalk, the robot has to think and act at the same turetuning,whichhasbeendemonstratedtogreatlyreduce
time. We discuss our solutions to this challenge in Section the need for hyperparameter tuning across domains, thus
4.8, for both model-free and model-based learning enabling much easier deployment on real-world robotic
algorithms. systems (Haarnoja et al., 2019). Lastly, we can aim to
Withtheprogresstoovercomethesechallenges,wehave developmethodsthatare,throughtheirdesign,morerobust
developed an efficient and autonomous on-robot training to hyperparameter settings. This option, although the most
system(Haarnojaetal.,2019),inwhichtherobotcanlearn desirable, is also the toughest, because it likely requires an
walking and turning, from scratch in the real world, with in-depthunderstandingfor thereal reasons behind thesen-
only 5 min of data (Yang et al., 2020) and little human sitivity of current RL algorithms, which has so far proven
supervision. elusive.
The second challenge to reliable and stable learning is
local optima and delayed rewards. In contrastto supervised
4. Outstanding challenges in deep RL and
learningproblems,whichputa convexlossfunctionontop
strategies to mitigate them
of a nonlinear neural network function approximator, the
Intheprevioussection,weshowedafewexamplesofappli- RL objective itself can present a challenging optimization
cations of deep RL on robotic tasks that enabled progress landscape independently of the policy or value function
over previous approaches in terms of generalization to a parameterization, which means that the usual benefits of
large variety of environments, objects, or more complex over-parameterized networks do not fully resolve issues
behaviors. Those applications required to solve or at least relating to local optima. This is indeed part of the reason
mitigate a few challenges specific to applying deep RL on whydifferentrunsofthesamealgorithmcanproducedrasti-
real robots that have been identified over the years. In this cally different solutions, and it presents a major challenge
section, we describe those challenges and provide, when- for real-world deployment, where even a single run can be
ever available, our current best mitigation strategies that exceptionally time-consuming. Some methods might pro-
enabled us to apply deep RL to the applications we dis- videbetterresiliencetolocaloptimabypreferringstochastic
cussedinSection3. policies that can explore multiple strategies simultaneously
(Foxetal.,2016;Haarnojaetal.,2017,2018c;Rawliketal.,
2013; Toussaint, 2009; Ziebart et al., 2008). More sophisti-
4.1. Reliable and stable learning
cated exploration strategies might further alleviate these
DeepRLalgorithmsarenotoriouslydifficulttouseinprac- issues (Fu et al., 2017; Pathak et al., 2017), and parameter-
tice(Irpan,2018).TheperformanceofcommonlyusedRL space exploration strategies might offer a particularly pro-
methods depends on careful settings of the hyperpara- mising approach to combating this issue (Burda et al.,
meters,andoftenvariessubstantiallybetweenruns(i.e.,for 2019).Indeed,wehaveobservedinsomeofourownexperi-
different ‘‘random seeds’’ in simulation). Off-policy algo- mentsthatwhencollectinglargeamountofon-policydatais
rithms, which are particularly desirable in robotics owing not an issue, direct parameter search methods such as aug-
to their improved sample efficiency, can suffer even more mented random search (Mania et al., 2018) can often be
from these issues than on-policy policy gradient methods. substantiallyeasiertodeploythanmoreclassicRLmethods,
We can broadly classify the challenges of reliable and sta- likely to their ability to avoid local optima by exploring
ble learning into two groups: (1) reducing sensitivity to directlyintheparameterspace.Itmaythereforeprovefruit-
hyperparameters; and (2) reducing issues owing to local ful to investigate methods that combine entropy maximiza-
optimaanddelayedrewards. tion and parameter space exploration as a way to avoid the
One approach to reducing the burden of tuning hyper- localoptimaanddelayedrewardissuesthatmakereal-world
parameters is to use automated hyperparameter tuning deploymentchallenging.

706 TheInternationalJournalofRoboticsResearch40(4-5)
4.2. Sample efficiency ofsteps.Traininganon-policymodelmaythusrequiresev-
eralmillionsandsometimesbillionsofactionexecutionsin
Many popular RL algorithms require millions of stochastic
therealworld,whichisoftenprohibitive.
gradient descent (SGD) steps to train policies that can
Off-policy methods do not assume that the samples are
accomplish complex tasks (Mnih et al., 2013; Schulman
coming from the current trained policy. In practice, this
et al., 2017). This often means that millions of interaction
means the samples can be reused multiple times across
withtherealworldwillberequiredforrobotictasks,which
back-propagations, potentially hundreds or thousands of
is quite prohibitive in practice. Without any improvement
times, without any over-fitting in complex visual tasks. In
in sample efficiency to those algorithms, the number of
Kalashnikov et al. (2018), up to 15 training steps of batch
trainingstepswillonlyincreaseasthemodelsizeincreases
size 32 were done per collect step on real robots during a
totacklemoreandmorecomplexrobotictasks.
fine-tuningphase, which isequivalent to 480gradient des-
We have found that some classes of RL algorithms are
cents per collect step. Recently, SAC (Haarnoja et al.,
muchmoresampleefficientthanothers.RLalgorithmscan
2019),anoff-policymethod,wasabletolearntowalkona
be categorized into model-based versus model-free meth-
quadruped robot, from scratch, with just 2 hours of real
ods. Among the model-free methods, they are often cate-
robot data coming from a single robot. Note that further
gorized into on-policy and off-policy methods. Generally
increasing the ratio between the number of training steps
speaking, among model-free techniques, off-policy meth-
and the number of collected samples may decrease the
ods are about an order of magnitude more data efficient
training performance owing to overfitting. The optimal
than on-policy methods. Model-based methods could be
ratio is often task dependent, policy dependent, or algo-
another order of magnitude more data efficient than their
rithm dependent, which is an important hyperparameter to
model-free counterparts. In the following sections we dis-
tune.
cussourexperienceswiththesemethods.
4.2.2. Model-based algorithms. Model-based algorithms
4.2.1.Off-policyalgorithms. On-policyalgorithmssuchas such as Draeger et al. (1995) choose the optimal action by
policy gradient methods (Peters and Schaal, 2006; leveraging a model of the environment. The agent may
Schulman et al., 2015) have recently become popular learn from the experience generated using this model
owingtotheirstabilityandtheirabilitytolearnpoliciesfor instead of collected in the real environment. Thus, the
awidevarietyoftasks.Unfortunately,on-policyalgorithms amount of data required for model-based methods is usu-
have the constraint to only use a sample coming from the ally much less than their model-free counterparts. For
latest policy that is being trained. This has the unfortunate example,weleveragedsuchatechniquetoeffectivelylearn
consequence that the number of required data samples is towalk,fromscratch,withonlyafewminutesofrealrobot
equal and often larger to the number of training steps data(Nagabandietal.,2018;Yangetal.,2020).Thedown-
neededtotrainamodel,which,inpractice,canbemillions side is that these methods require to have access to such a
Fig.6. PR2learningtoscoopabagofriceintoabowlwithaspatula(left)usingalearnedvisualstaterepresentation (right),using
(Finnetal.,2016b).Thefeaturepointsvisualizedontherightimageswerelearnedwithoutsupervisionwithanautoencoder.

| Ibarzetal. |     |     |     |     |     |     |     |     |     |     |     |     |     | 707 |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
model, which is often challenging to acquire in practice. policies,andthus,potentiallyscaletobillionsofrealworld
| Wecovermodel-basedtechniquesinmoredetailinSection |       |           |     |     |                  |     | samples.                                          |        |         |              |                  |         |     |         |
| ------------------------------------------------- | ----- | --------- | --- | --- | ---------------- | --- | ------------------------------------------------- | ------ | ------- | ------------ | ---------------- | ------- | --- | ------- |
| 4.6.                                              |       |           |     |     |                  |     | Off-policymethodscanleverageallthedatacollectedin |        |         |              |                  |         |     |         |
|                                                   |       |           |     |     |                  |     | the past,                                         | across | many    | experiments. |                  | In most | RL  | bench-  |
|                                                   |       |           |     |     |                  |     | marks, off-policy                                 |        | methods | are          | still collecting |         | new | data as |
| 4.2.3.                                            | Input | remapping |     | for | high-dimensional |     |                                                   |        |         |              |                  |         |     |         |
thetraininghappens.However,off-policymethodscanalso
| observations. |     | When | learning | from | high-dimensional |     |     |     |     |     |     |     |     |     |
| ------------- | --- | ---- | -------- | ---- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
betrainedwithoutcollectinganynewdataduringthetrain-
observations, e.g., image observations, learning visual ingphase;similartosupervisedlearningproblems.Wecall
| representations |     | can occupy | substantial |     | amount | of training |              |           |         |       |      |     |      |          |
| --------------- | --- | ---------- | ----------- | --- | ------ | ----------- | ------------ | --------- | ------- | ----- | ---- | --- | ---- | -------- |
|                 |     |            |             |     |        |             | this offline | training, | whereas | other | work | may | call | it batch |
and sample complexity. One trick for addressing this chal- RL.InSection3.2,we have shownthatthismode oftrain-
| lenge is | via input | remapping. |     | In particular, | when | policies |             |     |               |          |     |          |     |        |
| -------- | --------- | ---------- | --- | -------------- | ---- | -------- | ----------- | --- | ------------- | -------- | --- | -------- | --- | ------ |
|          |           |            |     |                |      |          | ing allowed | us  | to generalize | grasping |     | policies | to  | unseen |
aretrainedinalaboratoryenvironment,thetrueunderlying
|     |     |     |     |     |     |     | objects with | just | 500,000 | trials. | If we | compare | this | dataset |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ---- | ------- | ------- | ----- | ------- | ---- | ------- |
stateofthesystemmaybeobservableduringtraining,even
totheImageNetdataset,whichhasabout1millionimages,
whenthepolicytobelearnedmustusevision.Intheseset-
|     |     |     |     |     |     |     | we can | see that | the amount | of  | data | to learn | this complex |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | -------- | ---------- | --- | ---- | -------- | ------------ | --- |
tings, one policy or multiple local policies can be effi- robotic task from vision sensor, using RL, is in the same
| ciently | learned | without | vision | using | privileged | state |          |           |     |          |             |     |             |     |
| ------- | ------- | ------- | ------ | ----- | ---------- | ----- | -------- | --------- | --- | -------- | ----------- | --- | ----------- | --- |
|         |         |         |        |       |            |       | order of | magnitude | as  | learning | to classify |     | 1,000 types | of  |
information, and these policies can be distilled into a final objects. In both cases, the learned models have shown the
policythattakesrawobservationsasinputandistrainedto
|          |            |     |                |     |           |            | ability to | generalize | to             | a wide | variety      | of      | unseen    | object |
| -------- | ---------- | --- | -------------- | --- | --------- | ---------- | ---------- | ---------- | -------------- | ------ | ------------ | ------- | --------- | ------ |
| produce  | the output | of  | the non-vision |     | policies. | This trick |            |            |                |        |              |         |           |        |
|          |            |     |                |     |           |            | instances. | There      | are challenges |        | to stabilize | offline | training. |        |
| has been | successful | in  | a number       | of  | settings  | including  |            |            |                |        |              |         |           |        |
Theofflinetrainingcanbecomeunstableifthestate–action
| robotic | manipulation |     | from | image pixels | (Levine | et al. |              |      |     |               |         |     |      |      |
| ------- | ------------ | --- | ---- | ------------ | ------- | ------ | ------------ | ---- | --- | ------------- | ------- | --- | ---- | ---- |
|         |              |     |      |              |         |        | distribution | from | the | latest policy | differs | too | much | from |
2016; Pinto et al. 2018), autonomous driving (Chen et al. the one that was used to collect the training data. Recent
| 2020), and | robotic | locomotion |     | from a | history | of proprio- |     |     |     |     |     |     |     |     |
| ---------- | ------- | ---------- | --- | ------ | ------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
workjuststartedtoidentifyandaddresstosomeextentthis
ceptivesensormeasurements(Leeetal.2020b).
|      |         |          |         |        |            |     | specific | problem | (Agarwal | et  | al., 2020; | Fujimoto |     | et al., |
| ---- | ------- | -------- | ------- | ------ | ---------- | --- | -------- | ------- | -------- | --- | ---------- | -------- | --- | ------- |
| When | thetrue | statesof | objects | cannot | bemeasured | and |          |         |          |     |            |          |     |         |
2019;Kumaretal.,2019).
| the local   | policies        | must  | themselves | handle               | image | observa-  |              |           |             |        |            |              |            |           |
| ----------- | --------------- | ----- | ---------- | -------------------- | ----- | --------- | ------------ | --------- | ----------- | ------ | ---------- | ------------ | ---------- | --------- |
|             |                 |       |            |                      |       |           | An important |           | techniqueto | bypass |            | thesample    | efficiency |           |
| tions,these | observationscan |       |            | be first encodedinto |       | a lower-  |              |           |             |        |            |              |            |           |
|             |                 |       |            |                      |       |           | problem      | is to use | simulators, |        | which      | can generate |            | realistic |
| dimensional | state           | space | via an     | autoencoder,         | such  | as a spa- |              |           |             |        |            |              |            |           |
|             |                 |       |            |                      |       |           | experience   | much      | faster      | than   | real time. | Combining    |            | with      |
tial autoencoder that summarizes the image with a set of sim-to-realtransfertechniques,simulatorsallowustolearn
featurepointsinimagespace(Finnetal.,2016b):anexam-
policiesthatcanbedeployedintherealworldwithamini-
| ple of       | such | features         | are | illustrated | in   | Figure 6.    |            |     |            |              |     |        |      |          |
| ------------ | ---- | ---------------- | --- | ----------- | ---- | ------------ | ---------- | --- | ---------- | ------------ | --- | ------ | ---- | -------- |
|              |      |                  |     |             |      |              | mal amount | of  | real-world | interaction. |     | In the | next | section, |
| Unsupervised |      | feature learning |     | methods     | such | as autoenco- |            |     |            |              |     |        |      |          |
wediscusstheuseofsimulation.
ders(Finnetal.,2016b;Ghadirzadehetal.,2017),contras-
| tive losses | (Sermanet |        | et al. | 2018), and     | correspondence |              |          |               |     |     |     |     |     |     |
| ----------- | --------- | ------ | ------ | -------------- | -------------- | ------------ | -------- | ------------- | --- | --- | --- | --- | --- | --- |
| learning    | (Florence | et al. | 2018,  | 2019), provide |                | a reasonable |          |               |     |     |     |     |     |     |
|             |           |        |        |                |                |              | 4.3. Use | of simulation |     |     |     |     |     |     |
solutionincaseswheretheinductivebiasesoftheunsuper-
|                 |     |             |       |     |       |              | Simulation | is becoming |     | increasingly |     | accurate | over | the |
| --------------- | --- | ----------- | ----- | --- | ----- | ------------ | ---------- | ----------- | --- | ------------ | --- | -------- | ---- | --- |
| vised algorithm |     | effectively | match | the | needs | of the state |            |             |     |              |     |          |      |     |
representation. years,whichmakesitagoodproxytorealrobots.Onebot-
|     |     |     |     |     |     |     | tleneck | of robotic | learning | is to | collect | a large | amount | of  |
| --- | --- | --- | --- | --- | --- | --- | ------- | ---------- | -------- | ----- | ------- | ------- | ------ | --- |
dataautonomouslyandsafely.Whilecollectingenoughreal
4.2.4. Offline training. Image classifiers used by compa- data on the physical systemis slowandexpensive, simula-
nies, such Facebook or Google, are trained on tens of mil- tion can run orders of magnitude faster than real time, and
lion of labeled images (Kuznetsova et al., 2020), or can start many instances simultaneously. In addition, data
pretrainedonbillionsof images(Mahajanetal.,2018;Xie can be collected continuously without human intervention.
etal.,2020),toreachthelevelofqualityrequiredbycertain On the real robot, human supervision is always needed for
products. Natural language processing (NLP) systems for resetting experiments, monitoring hardware status and
machine translation, or speech recognition systems such as ensuring safety. In contrast, experiments can be reset auto-
BERT(Devlinetal.,2019),alsorequirebillionsofsamples matically, and safety is not a problem in simulation. Thus,
to generalize and have descent performance for real appli- prototyping in simulation is faster, cheaper, and safer than
cations.Inaway,supervisedlearningsystemsarealsoinef- experimentingontherealrobot.Theseenablefastiteration
ficient,butinmanyapplications,thegainsingeneralization ofdevelopingandtuninglearningalgorithms.Thefastpace
and performance that deep learning provides compensates of experiments allow us to efficiently shape the reward
for the cost of collecting such large amounts of data. function, sweep the hyperparameters, fine-tune the algo-
Similarly, a general-purpose robot may also require a large rithm,and testwhether a given task fallswithin therobot’s
volumeofdatatotrainon,unlesssignificantimprovements hardware capability. From our own experience, we have
havebeenmadeinourlearningalgorithms.Offlinetraining benefited tremendously from prototyping in simulation
| enable us | to use | all the | data | collected | so far | to train our | (Tanetal.,2018). |     |     |     |     |     |     |     |
| --------- | ------ | ------- | ---- | --------- | ------ | ------------ | ---------------- | --- | --- | --- | --- | --- | --- | --- |

708 TheInternationalJournalofRoboticsResearch40(4-5)
In addition to prototyping, can we directly use the poli- physical parameters, unmodeled dynamics, and stochastic
cies trained in simulation on real robots? Unfortunately, real environment. However, there is no general consensus
deploying these policies can fail catastrophically owing to about which of these sources plays a more important role.
therealitygap.Modelingerrorscause amismatchinrobot After a large number of experiments with legged robots,
dynamics,andrenderedimagesoftendonotlookliketheir both in simulation and on real robots, we found that the
real-worldcounterparts.Therealitygapisamajorobstacle actuatordynamicsandthelackoflatencymodelingarethe
that prevents the application of learning to robotics. In main causes of the model error. Developing accurate mod-
simulations, the robots can learn to backflip (Peng et al., els for the actuator and latency significantly narrow the
2018a) bicycle stunts (Tan et al., 2014), and even put on reality gap (Tan et al., 2018). We successfully deployed
clothes(Cleggetal.,2018).Incontrast,itisstillverychal- agile locomotion gaits that are learned in simulation to the
lengingtoteachrobotstoperformbasictaskssuchaswalk- real robot without the need for any data collected on the
ing in the real world. Bridging the reality gap will allow robot.
robotics to fully tap into the power of learning. More
importantly, bridging the reality gap is important to push
4.3.3. Domain randomization. The idea behind domain
the advancement of machine learning for robotics towards
randomization is to randomly sample different simulation
the right direction. In the last few years, the OpenAI Gym
parameters while training the RL policy. This can include
benchmark(Brockmanetal.,2016)isthekeydrivingforce
various dynamics parameters (Peng et al., 2018b; Tan
behind the development of deep RL and its application to
et al., 2018) of the robot and the environment, as well as
robotics. However, these simulation benchmarks are con-
visual and rendering parameters such as textures and light-
siderablyeasierthantheirreal-worldequivalent.Itdoesnot
ing(SadeghiandLevine,2017;Tobinetal.,2017).Similar
takeintoconsiderationthedetaileddynamics,partialobser-
to data augmentation methodsin supervised learning, poli-
vability, latency, and safety aspects of robotics. Thus, the
cies trained under such diverse conditions tend to be more
scores which researchers optimize their algorithms for can
robust to such variations, and can thus perform better in
bemisleading:thelearningalgorithmsthatperform wellin
therealworld.
thegymenvironmentsmaynotworkwellonrealrobots.If
we can bridge this reality gap, we would have a far better
simulation benchmark for robotics, which can focus the 4.3.4. Domain adaptation. The success of adversarial
research efforts to the most pressing challenges in robot training methods such as generative adversarial networks
learning, such as non-Markovian assumption (asynchro- (Goodfellowet al., 2014) have resulted in their application
nous control), partial observability, and safe exploration to several other problems, including sim-to-real transfer.
and actuation. In the following, we outline a few methods Adapter networks have been trained that convert simulated
that have been employed successfully for sim-to-real images to look like their real-world counterparts, which
transfer. canthen be used to train policies in simulation (Bousmalis
et al., 2018, 2017; James et al., 2017; Rao et al., 2020;
Shrivastava et al., 2017). An alternative approach is that of
4.3.1. Better simulation. Addressing Partial
James et al. (2019), which trains an adapter network to
ObservationsInsimulation,wecanaccesstheground-truth
convert real-world images to canonical simulation images,
state of the robot, which can significantly simplify the
allowing a policy trained only in simulation to be applied
learning of tasks. In contrast, in the real-world, we are
in the real world. Training of the real-to-sim adapter was
restricted to partial observations that are usually noisy and
achieved by using domain-randomized simulation images
delayed, due to the limitation of onboard sensors. For
as a proxy for real-world images, removing the need for
example,itisdifficulttopreciselymeasuretheroottransla-
real-world data altogether. The resulting policy achieved
tion of a leggedrobot. To eliminate this difference, we can
70%graspsuccess in therealworldwith theQT-Opt algo-
remove the inaccessible states during training (Tan et al.
rithm, with no real-world data, and reaches a success rate
2018), apply state estimation, add more sensors (e.g.
of 91% after fine-tuning on just 5,000 real-world grasps: a
MotionCapture)(Haarnojaetal.2019)orlearntoinferthe
result which previously took over 500,000 grasps to
missing information (e.g. reward) (Yang et al. 2019). On
achieve.
the other hand, if used properly, the groundtruth states in
simulationcansignificantlyspeeduplearning.Learningby
cheating(Chenetal.2020)firstleveragedtheground-truth 4.4. Side-stepping exploration challenges
states to learn a privileged agent, and in the second stage,
In RL, ‘‘exploration’’refers most generally to the problem
imitatedthis agenttoremove therelianceontheprivileged
of choosing a policy that allows an agent to discover high-
information.
reward regions of the state space. Such a policy may not
itselfhaveveryhighaveragereward:typically,goodexplo-
4.3.2. Better simulation. The reality gap is caused by the ration strategies are risk-seeking (Bellemare et al., 2016),
discrepancybetweenthesimulationandthereal-worldphy- highly stochastic (Fox et al., 2016; Haarnoja et al., 2017;
sics. This error has many sources, including incorrect Osband et al., 2016; Rawlik et al., 2013; Toussaint, 2009;

| Ibarzetal. |     |     |     |     |     |     |     |     |     |     |     |     |     | 709 |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Fig.7. Usingbothunsupervisedinteractionandteleoperateddemonstrationdata,therobotlearnsavisualdynamicsmodelandaction
proposalmodelthatenablesittoperformnewtaskswithnovel,previouslyunseentools(usingXieetal.,2019).Thetaskspecification
isshownontheleftandtherobotperformingthetaskisshownontheright.
Ziebartetal.,2008),andprioritizenoveltyoverexploitation incorporate the demonstrations into the learning process,
(Bellemareetal.,2016;Fuetal.,2017;Pathaketal.,2017). whicharediscussedinthefollowing.
| In practice, | effective | exploration |     | is particularly |     | challenging |     |     |     |     |     |     |     |     |
| ------------ | --------- | ----------- | --- | --------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
intaskswithsparsereward.Inthemostextremeversionof
|     |     |     |     |     |     |     | 4.4.1. Initialization. |     | A   | simple | way to | incorporate | demon- |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | ------ | ------ | ----------- | ------ | --- |
this problem, the agent must essentially find a (high- strationstomitigatetheexplorationchallengeistopretrain
| reward)  | needle  | in a (zero-reward) |     | haystack. | Unfortunately, |          |                   |     |          |                |     |              |        |       |
| -------- | ------- | ------------------ | --- | --------- | -------------- | -------- | ----------------- | --- | -------- | -------------- | --- | ------------ | ------ | ----- |
|          |         |                    |     |           |                |          | a policy network  |     | with     | demonstrations |     | via learning |        | (also |
| the most | natural | formulation        |     | of many   | practical      | robotics |                   |     |          |                |     |              |        |       |
|          |         |                    |     |           |                |          | called behavioral |     | cloning) | (Bojarski      |     | et al.,      | 2016). | This  |
taskshasthisproperty.Formanytasks,itismostnaturalto
approachhasbeenusedinavarietyofpriorroboticlearning
| formulate | them | as binary | reward | tasks | (Irpan, | 2018): | a             |     |            |          |         |       |           |     |
| --------- | ---- | --------- | ------ | ----- | ------- | ------ | ------------- | --- | ---------- | -------- | ------- | ----- | --------- | --- |
|           |      |           |        |       |         |        | works (Daniel | et  | al., 2013; | Ijspeert | et al., | 2002; | Manschitz |     |
grasping robot can either succeed or fail at grasping an etal.,2014;PetersandSchaal,2008)
| object, a | pouring | robot | can pour | water into | a glass | or not, |          |      |          |           |     |       |            |     |
| --------- | ------- | ----- | -------- | ---------- | ------- | ------- | -------- | ---- | -------- | --------- | --- | ----- | ---------- | --- |
|           |         |       |          |            |         |         | Although | this | approach | is simple | and | often | effective, | it  |
and a mobile robot can reach the destination or not. One suffers from twomajor challenges. First,imitationlearning
| can reasonably |     | regard these     | as  | the most | basic task | specifi-    |                      |     |             |             |               |           |          |     |
| -------------- | --- | ---------------- | --- | -------- | ---------- | ----------- | -------------------- | --- | ----------- | ----------- | ------------- | --------- | -------- | --- |
|                |     |                  |     |          |            |             | effective guarantees |     | on          | performance | both          | in theory | and      | in  |
| cation, with   | any | more informative |     | reward   | (e.g.,     | distance to |                      |     |             |             |               |           |          |     |
|                |     |                  |     |          |            |             | practice (Ross       | et  | al., 2011), | and         | the resulting |           | policies | can |
thegoal)asadditionalengineer-providedshaping. suffer from ‘‘compounding errors,’’ where a small mistake
| For this | reason, | a number |     | of prior works | have | focused |            |        |      |               |        |       |     |       |
| -------- | ------- | -------- | --- | -------------- | ---- | ------- | ---------- | ------ | ---- | ------------- | ------ | ----- | --- | ----- |
|          |         |          |     |                |      |         | throws the | policy | into | an unexpected | state, | where | it  | makes |
on studying exploration for sparse-reward robotic tasks a bigger mistake. Second, the learned initialization can be
| (Andrychowicz |     | et al., | 2017; | Schoettler | et  | al., 2019). |                  |     |        |        |              |     |          |     |
| ------------- | --- | ------- | ----- | ---------- | --- | ----------- | ---------------- | --- | ------ | ------ | ------------ | --- | -------- | --- |
|               |     |         |       |            |     |             | easily forgotten |     | by the | RL. As | it is common |     | practice | to  |
Numerous methods for improving exploration have been begin RL with a high random exploration factor, RL can
| proposedintheliterature |     |     | (Foxetal.,2016;Haarnoja |     |     | etal., |     |     |     |     |     |     |     |     |
| ----------------------- | --- | --- | ----------------------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
quicklydecimatethepretrainedpolicy,andendupinastate
| 2017; Osband |     | et al., 2016; | Pathak | et  | al., 2017; | Rawlik |            |        |             |                 |     |      |      |      |
| ------------ | --- | ------------- | ------ | --- | ---------- | ------ | ---------- | ------ | ----------- | --------------- | --- | ---- | ---- | ---- |
|              |     |               |        |     |            |        | that is no | better | than random | initialization. |     | Note | that | some |
et al., 2013; Toussaint, 2009; Ziebart et al., 2008), and algorithmsandpolicyrepresentationsareparticularlyamen-
| many of | these | can be applied |     | directly to | real-world | robotic |                        |     |      |                 |     |     |          |     |
| ------- | ----- | -------------- | --- | ----------- | ---------- | ------- | ---------------------- | --- | ---- | --------------- | --- | --- | -------- | --- |
|         |       |                |     |             |            |         | able to initialization |     | from | demonstrations. |     | For | example, |     |
RL. However, for certain real-world robotic tasks, this dynamic movement primitives (DMPs) can be initialized
| problem | can often | be side-stepped |     | using | a combination | of  |                     |     |     |       |           |     |        |      |
| ------- | --------- | --------------- | --- | ----- | ------------- | --- | ------------------- | --- | --- | ----- | --------- | --- | ------ | ---- |
|         |           |                 |     |       |               |     | from demonstrations |     | in  | a way | that does | not | suffer | from |
relatively simple manual engineering and demonstration compoundingerrors(Schaal,2006),whereasguidedpolicy
data, and this provides a very powerful mechanism for searchcanbeinitializedfromdemonstrationbypretraining
| avoiding | a major | challenge | and | instead | focusing | on other |     |     |     |     |     |     |     |     |
| -------- | ------- | --------- | --- | ------- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
thelocalpolicies,which,inpractice,tendstobealotmore
issues, such as efficiency and generalization. The use of stable than demonstration pretraining for standard policy
| demonstrations |     | to mitigate | exploration |     | challenges | has | a   |     |     |     |     |     |     |     |
| -------------- | --- | ----------- | ----------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
gradientoractor–criticmethods(Levineetal.,2015).
| long history | in  | robotics | (Daniel | et al., 2013; | Ijspeert | et al., |     |     |     |     |     |     |     |     |
| ------------ | --- | -------- | ------- | ------------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
2002;Manschitzetal.,2014;PetersandSchaal,2008),and 4.4.2. Data aggregation. Another technique for incorpor-
has been used in a number of recent works (Jain et al., ating demonstrations in off-policy model-free RL is to add
2019; Nair et al., 2018). There are various ways to demonstration data to the data buffer for the off-policy

| 710 |     |     |     |     |     |     | TheInternationalJournalofRoboticsResearch40(4-5) |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
algorithm. This method is often used with Q-learning or around 15–30%. Although this success rate is much lower
actor–criticstylealgorithms(Vecˇer´ıketal.,2017;Wuetal., than the final policy, which succeeds 96% of the time, it
2019).Thiscan,inprinciple,mitigatetheexplorationchal- was sufficient to bootstrap an effectivevision-based grasp-
| lenge, because |     | the algorithm |     | is exposed | to high-reward |     | ingskill. |     |     |     |     |     |     |     |
| -------------- | --- | ------------- | --- | ---------- | -------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
behavior, but tends to be problematic in practice, because Another reason why we pre-populate the replay buffer
commonly used approximate dynamic programming meth- only with a scripted policy is to help keep a ratio of suc-
ods (i.e., value function estimation) need to see both good cessful and unsuccessful episodes close to 50%. This is
and bad experience to learn which actions are desirable. motivated by techniques trying to re-balance equally each
Therefore, when the demonstrations are much better than class when training a multi-class classifier as in Chawla et
theagent’sownexperience,thevaluefunctionwilltypically al.(2002).Apoorperformingpolicydoesntgenerategood
|            |                  |     |        |             |     |            | data to | train a | Q-function | since | it requires | both | good | and |
| ---------- | ---------------- | --- | ------ | ----------- | --- | ---------- | ------- | ------- | ---------- | ----- | ----------- | ---- | ---- | --- |
| learn that | the demonstrated |     | states | are better, | but | might fail |         |         |            |       |             |      |      |     |
to learn which actions must be taken to reach those states. bad attempts to be able to learn a good ranking of what a
Therefore,thistendstobemuchmoreeffectivewhencom- good or bad actionis.At the beginning of the training,the
binedwiththenextmethod. policy is bad because the Q-function being learned hasn t
|                      |     |                                   |     |     |     |     | converged | yet.  | Such a | policy  | only generates |        | unsuccessful |     |
| -------------------- | --- | --------------------------------- | --- | --- | --- | --- | --------- | ----- | ------ | ------- | -------------- | ------ | ------------ | --- |
|                      |     |                                   |     |     |     |     | episodes  | which | can t  | be used | to train       | a good | Q-function.  |     |
| 4.4.3.Jointtraining. |     | Insteadofsimplypretrainingthepol- |     |     |     |     |           |       |        |         |                |        |              |     |
Thisiswhythepolicyisonlyusedtogeneratedataonceit
| icy with supervisedlearning,we |     |     |     | cantrain | itjointly,adding |     |         |           |        |     |              |     |     |         |
| ------------------------------ | --- | --- | --- | -------- | ---------------- | --- | ------- | --------- | ------ | --- | ------------ | --- | --- | ------- |
|                                |     |     |     |          |                  |     | reached | a certain | amount | of  | performance. |     | Our | rule of |
togetherthelossfromthepolicygradientobjectivewiththe
|                     |     |         |         |         |       |           | thumb is | to only | start | using the | trained | policy | for data | col- |
| ------------------- | --- | ------- | ------- | ------- | ----- | --------- | -------- | ------- | ----- | --------- | ------- | ------ | -------- | ---- |
| loss for behavioral |     | cloning | (Hester | et al., | 2018; | Johannink |          |         |       |           |         |        |          |      |
lectiononceithasreached20+%success.
et al., 2019; Wu et al., 2019). This simple approach pro- Scripted policies can also be used in a ‘‘residual’’ RL
| vides a much | stronger |     | signal to | the learner, | generally | suc- |     |     |     |     |     |     |     |     |
| ------------ | -------- | --- | --------- | ------------ | --------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
framework,whichservesasimilarpurposeasjointtraining
| ceeding in      | staying | close  | to the    | demonstrations,       |     | but at the |                      |     |     |             |     |            |     |         |
| --------------- | ------- | ------ | --------- | --------------------- | --- | ---------- | -------------------- | --- | --- | ----------- | --- | ---------- | --- | ------- |
|                 |         |        |           |                       |     |            | with demonstrations. |     |     | In residual | RL  | (Johannink |     | et al., |
| cost of biasing |         | policy | learning: | if the demonstrations |     | are        |                      |     |     |             |     |            |     |         |
2019;Silveretal.,2018;Tanetal.,2018,thereinforcement
suboptimal,thebehavioralcloninglossmaypreventtheRL
|     |     |     |     |     |     |     | learner learns | a   | policy | that is | additively | combined |     | with the |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------ | ------- | ---------- | -------- | --- | -------- |
algorithmfromdiscoveringabetterpolicy. scripted policy, i.e., p (s)=p (s)+ p (s).
|                                      |     |     |     |     |               |     |                |          |             | final   | scripted |                 | learned    |     |
| ------------------------------------ | --- | --- | --- | --- | ------------- | --- | -------------- | -------- | ----------- | ------- | -------- | --------------- | ---------- | --- |
|                                      |     |     |     |     |               |     | The motivation |          | is similar: | unlike  | pure     | initialization, |            | the |
|                                      |     |     |     |     |               |     | residual       | approach | always      | retains | the      | scripted        | component. |     |
| 4.4.4.Demonstrationsinmodel-basedRL. |     |     |     |     | Inmodel-based |     |                |          |             |         |          |                 |            |     |
RL, demonstration data can also be aggregated with the However, unlike joint training with demonstrations, resi-
|                    |     |            |     |                |          |     | dual RL  | can overcome |     | the bias | in the        | scripted | policy | by      |
| ------------------ | --- | ---------- | --- | -------------- | -------- | --- | -------- | ------------ | --- | -------- | ------------- | -------- | ------ | ------- |
| agent’s experience |     | to produce |     | better models. | However, | in  |          |              |     |          |               |          |        |         |
|                    |     |            |     |                |          |     | learning | to ‘‘undo’’p |     | (s),     | and therefore |          | can in | princi- |
contrast to the model-free setting, for model-based RL this scripted
plestillconvergetotheoptimalpolicy.
| approach | can be | quite | effective, | because | it would | enable |     |     |     |     |     |     |     |     |
| -------- | ------ | ----- | ---------- | ------- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
thelearnedmodeltocapturecorrectdynamicsinimportant
partsofthestatespace.Whencombinedwithagoodplan- 4.4.6. Reward shaping. Shaping the reward function can
|               |                |         |           |                    |       |            | also side-step | exploration |            | challenges |         | by providing     |          | the RL |
| ------------- | -------------- | ------- | --------- | ------------------ | ----- | ---------- | -------------- | ----------- | ---------- | ---------- | ------- | ---------------- | -------- | ------ |
| ning method,  | which          | can     | also use  | the demonstrations |       | (e.g.,     |                |             |            |            |         |                  |          |        |
|               |                |         |           |                    |       |            | algorithm      | with        | additional | guidance   |         | for exploration. |          | For    |
| as a proposal | distribution), |         | including | demonstrations     |       | into       |                |             |            |            |         |                  |          |        |
|               |                |         |           |                    |       |            | example,       | for a       | reaching   | task,      | one can | use the          | distance | of     |
| the model     | training       | dataset | can       | enable a           | robot | to perform |                |             |            |            |         |                  |          |        |
theagenttothegoalasanegativerewardwhichwillsignif-
| complex | behaviors, | such | as using | tools | (Figure | 7), which |     |     |     |     |     |     |     |     |
| ------- | ---------- | ---- | -------- | ----- | ------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
wouldbeextremelydifficulttodiscoverautomatically(Xie icantly speed uptheexploration.Weve used this approach
|     |     |     |     |     |     |     | in several | works | for learning |     | manipulation |     | skills, | such as |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ----- | ------------ | --- | ------------ | --- | ------- | ------- |
etal.,2019).
|     |     |     |     |     |     |     | door opening |     | and peg   | insertion, | where    | object |        | location |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --------- | ---------- | -------- | ------ | ------ | -------- |
|     |     |     |     |     |     |     | information  | is  | available | during     | training | (Gu    | et al. | 2017;    |
4.4.5. Scripted policies. In addition to demonstrations, we Levine etal.2016).Thisapproachisveryeffectiveforany
canalsoovercometheexplorationchallengewithamoder-
taskswheretheagenthastogotoaspecificknowlocation,
ateamountofmanualengineering,bydesigning‘‘scripted’’ such as in navigation tasks Francis et al. (2020). However,
policies that can serve as initialization. Scripted policies wevefoundinpracticethatsuchanapproachcanbediffi-
can be incorporated into the learning process in much the cult to scale to many diverse manipulation tasks. This is
sameway as demonstrations, and can provide considerable due to two factors. First, it can be very difficult to weight
benefit.IntheQT-Optgraspingsystem(Figure3),scripted the shaping terms properly to avoid any greedy and unin-
policies are used to prepopulate the data buffer with a tentional sub-optimal behaviors. For example, to open the
higher proportion of successful grasps than would be door, one may want to get close to the handle, but may
obtainedwithpurelyrandomactions.Althoughaggregating require to take some distance from it to take a different
such data from a small number of demonstrations would approach with the gripper if the handle can t be moved
have limited effectiveness, the advantage of a scripted pol- with the current orientation. Such behavior would go
icy is that it can be used to collect very large datasets. In against the shaping of the reward, and thus the reward
the final QT-Opt experiment, the scripted policy was used shaping may make it impossible to discover such a beha-
to collect 200,000 grasp attempts, with a success rate vior if its weight is too high. Second, and perhaps more

| Ibarzetal. |     |     |     |     |     |     |     |     |     |     |     |     |     | 711 |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
importantly in real-world environments, such shaped 4.5.2. Proper evaluation. To get good generalization, the
reward functions require knowledge of the precise state of entire system, including its hyperparameters, has to be
the environment, such as object locations relative to the tuned to optimize for it. This means that when we define
robot. This is feasible in simulation but can be very chal- the evaluation protocol, we have to be thoughtful to have
lenging on real robots, where the only input may be an two Markov decision processes (MDPs): one for training
andaseparateoneforevaluation.
| image. | Once | one wants | to  | tackle | multiple | manipulation |     |     |     |     |     |     |     |     |
| ------ | ---- | --------- | --- | ------ | -------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
tasks,dealingwiththosevariationsmaybedifficulttopro- This separation of MDP has to be done based on what
gram even in simulation, since the state configuration one we care to generalize against: if we want a policy that can
has to deal with can grow exponentially. While we have graspnewobjects,weshouldhavethetrainingMDPwitha
discussed how the challenge of exploration can be side- different setof objects than thetestingMDP,both insimu-
|         |              |     |                 |     |     |                    |     | lation and | the real setup. | If  | we care | about | generalizing | to  |
| ------- | ------------ | --- | --------------- | --- | --- | ------------------ | --- | ---------- | --------------- | --- | ------- | ----- | ------------ | --- |
| stepped | by employing |     | demonstrations, |     |     | scripted policies, |     |            |                 |     |         |       |              |     |
and reward shaping, the study of exploration and curiosity new robot dynamics, we should make sure to define our
in roboticlearning still plays an important role. Indeed, we training MDP with different dynamics than our testing
| can regard | those | approaches |     | as  | a means | to parallelize |     | MDP. |     |     |     |     |     |     |
| ---------- | ----- | ---------- | --- | --- | ------- | -------------- | --- | ---- | --- | --- | --- | --- | --- | --- |
researchonroboticlearning:ifweaimtostudyperception,
generalization,andcomplextasks,wecanavoidneedingto 4.6. Avoiding model exploitation
solveexplorationasaprerequisite.
|     |     |     |     |     |     |     |     | There have  | been notable  | success |      | stories in | robotics | with   |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ------------- | ------- | ---- | ---------- | -------- | ------ |
|     |     |     |     |     |     |     |     | model-based | RL approaches |         | that | learn a    | model    | of the |
4.5. Generalization
dynamicsandusethatmodeltochooseactions(Deisenroth
Generalization to any new skills, environments, or tasks et al., 2013; Finn and Levine, 2017; Kurutach et al., 2018;
still remains an unsolved problem. Solving this problem is Lenz et al., 2015; Levine et al., 2016; Nagabandi et al.,
required to allow robots to operate in awidevarietyof real- 2018;Xieetal.,2019;Yangetal.,2020).Here,weusethe
worldscenarios.However,thereareafewrestrictedsituations term ‘‘model-based’’ to describe algorithms that learn a
wherewehaveseengoodgeneralization.Inthenextsection, modelofthedynamicsfromdata,nottorefertothesetting
wecovertwoimportantaspects:(1)gooddatadiversityguar- where a model is known a priori. Empirically, these meth-
anteeingtocoverthespacewewanttogeneralizeand(2)hav- ods have enjoyed superior sample complexity in compari-
inga correct trainandtest evaluationprotocolthat allowsus son with model-free approaches (Deisenroth et al., 2013;
tooptimizeoursystemtowardsbettergeneralization. Nagabandi et al., 2018; Yang et al., 2020), have scaled to
|             |            |     |      |      |           |             |     | vision-based  | tasks (Finn | and    | Levine,          | 2017; | Finn        | et al., |
| ----------- | ---------- | --- | ---- | ---- | --------- | ----------- | --- | ------------- | ----------- | ------ | ---------------- | ----- | ----------- | ------- |
|             |            |     |      |      |           |             |     | 2016b; Levine | et al.,     | 2016), | and demonstrated |       | generaliza- |         |
| 4.5.1. Data | diversity. |     | Good | data | diversity | that covers | the |               |             |        |                  |       |             |         |
tioncapabilitiestomanyobjectsandtaskswhenthemodel
space of generalization we care about is critical to have is trained on large, diverse datasets (Finn and Levine,
| good performance |     | with | deep | learning. |     | Deep RL | is no |            |                |       |                |     |              |     |
| ---------------- | --- | ---- | ---- | --------- | --- | ------- | ----- | ---------- | -------------- | ----- | -------------- | --- | ------------ | --- |
|                  |     |      |      |           |     |         |       | 2017; Yang | et al., 2020). | These | generalization |     | capabilities |     |
exception. In QT-Opt, we cared about generalization to the are a natural byproduct of being able to train on off-policy
| objects   | that were | never  | seen | during      | training. | Thus,       | we  | datasets. |                |             |     |     |          |        |
| --------- | --------- | ------ | ---- | ----------- | --------- | ----------- | --- | --------- | -------------- | ----------- | --- | --- | -------- | ------ |
| made sure | that      | during | data | collection, | the       | agent would | see |           |                |             |     |     |          |        |
|           |           |        |      |             |           |             |     | Despite   | the benefitsof | model-based |     | RL  | methods, | a pri- |
more than 1,000 different object types. If we had only col- mary, well-known challenge faced by such model-based
| lecteddatawith |     | a smallset |     | of objects,we |     | may notachieve |     |               |          |               |     |            |     |       |
| -------------- | --- | ---------- | --- | ------------- | --- | -------------- | --- | ------------- | -------- | ------------- | --- | ---------- | --- | ----- |
|                |     |            |     |               |     |                |     | RL approaches | is model | exploitation, |     | i.e., when | the | model |
the generalization capability that we need. It is the same is imperfect in some parts of the state space, and the opti-
analogy that we cannot expect a model trained on CIFAR mization over actions finds parts of the state space where
| (with 100 | classes) | to  | generalize | as  | well | as a model | trained |     |     |     |     |     |     |     |
| --------- | -------- | --- | ---------- | --- | ---- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- |
themodeliserroneouslyoptimistic.Thiscanresultinpoor
on ImageNet (with 1,000 classes). This is also true for action selection. Although this challenge is real, we have
| robotics.                                        | If we | want | to generalize |     | to any | objects, | we may |             |              |         |          |       |     |          |
| ------------------------------------------------ | ----- | ---- | ------------- | --- | ------ | -------- | ------ | ----------- | ------------ | ------- | -------- | ----- | --- | -------- |
|                                                  |       |      |               |     |        |          |        | found that, | in practice, | we have | multiple | tools | for | mitigat- |
| needtocollectdatawiththousandsofthem.Ifwewantthe |       |      |               |     |        |          |        | ingit.      |              |         |          |       |     |          |
policy to be agnostic to the robot arm geometry, we may First, we have found that optimization under the model
needtotrainwiththousandsofarmvariations,etc. is successfulwhenthedata distribution consists of particu-
A lot of recent work has leveraged domain randomiza- larly broad distributions over actions and states (Finn and
| tion in simulation |     | to  | get good | sim-to-real |     | transfer, | because |         |            |         |        |            |     |         |
| ------------------ | --- | --- | -------- | ----------- | --- | --------- | ------- | ------- | ---------- | ------- | ------ | ---------- | --- | ------- |
|                    |     |     |          |             |     |           |         | Levine, | 2017; Yang | et al., | 2020). | In problem |     | domains |
they cared about generalization to a new environment. where this is not possible, one effective tool is data aggre-
Thereisatradeoffhereasmoreenvironmentdiversitymay gation, which interleaves the data collection and model
cause the policies to have lower performance. Often this learning, similar to DAGGER (Ross et al., 2011).
can be alleviated with larger and better neural network Wheneverthemodelisinaccurateandgetsexploited,more
architectures. As an example, a larger and deeper than data in the real world is collected to retrain the model.
usual neural network was required in Kalashnikov et al. Another tool is to represent and account for model uncer-
(2018) for the Q-function to deal with the large variety of tainty (Deisenroth and Rasmussen, 2011). Acquiring accu-
objectsandtoachievegoodperformanceontestobjects. rate uncertainty estimates when using neural network

712 TheInternationalJournalofRoboticsResearch40(4-5)
models is particularly challenging, though there has been continuous operation of the robots, and (3) dealing with
some success on physical robots (Nagabandi et al., 2020). non-stationarityowingtoenvironmentchanges.
If we cannot obtain uncertainty estimates, then we can
alternativelymodelthedatadistributionthatthemodelwas
4.7.1. Experiment design. The experimental set-up itself,
fit, and constrain the optimization to that distribution. We
i.e., how a particular robot is set up to tackle a specific
have found this approach to be particularly effective when
task, is an important and often overlooked aspect of a suc-
using models fit locally around a relatively small number
cessful experiment. Oftentimes the set-up has been care-
oftrajectories(Chebotaretal.,2017b;Levineetal.,2016).
fully engineered or the task has been chosen such that the
We canachieve a similareffect,butwithout havingtorefit
robotcanresetthescenetofacilitateunattendedandpoten-
models from scratch, by learning to adapt models to local
tiallyround-the-clockoperation.Forexample,in(Pintoand
contexts from a few transitions (Clavera et al., 2019): this
Gupta 2016; Levine et al. 2018; Kalashnikov et al. 2018;
approachallowsustoautomatically constructlocalmodels
Zeng et al. 2018; Cabi et al. 2019; Dasari et al. 2019), the
from short windows of experience. These local models
workspaces are convex, the objects involved allow for safe
have been demonstrated on a variety of robotic manipula-
interaction, and action-spaces are mostly restricted to top-
tionandlocomotionproblems.
down combined with either intrinsic compliance of the
Even if the learned model is accurate for a single-step
robot itself and/or a wrist mounted force-torque sensor to
prediction, error can accumulate over the a long-horizon
detect and stop unsafe motions. Ideally, the experimental
plan. For example, the predicted and real trajectories can
set-up is as unconstrained as possible, but, in practice, is
quicklydivergeafteracontactevent,evenifthesingle-step
restricted to create a safe action space for the robot (see
modelerrorissmall.Wefoundthatusingmulti-steplosses
Section4.11.1).
(FinnandLevine,2017;Yangetal.,2020),shorterhorizons
(whenapplicable)(Nagabandietal.,2018),andreplanning
(Finn and Levine, 2017; Nagabandi et al., 2018) are effec- 4.7.2. Facilitating continuous operation. Round-the-clock
tivestrategiesforlimitingtheerroraccumulation,andreco- operation will stress the robot itself as well as the experi-
veringfrommodelexploitation. mental set-up. Repeated potentially unintended contact of
the robot with objects and environment will wear out any
4.7. Robot operation at scale experimental set-up eventually and needs to be considered
upfront. The challenge for long-running experiments is to
Recent advances in deep learning have also contributed to
increase the mean time between failurewhile ensuring that
faster compute architectures and the availability of ever-
thedatathatisbeingcollectedisindeedusefulfortraining.
growing (labeled) datasets (Deng et al., 2009; Garofolo
The former requires to understand the root cause for each
et al., 1993). In addition, various open-source efforts, such
intervention and develop failsafe redundancies. We discuss
as those of Paszke et al. (2017) and Abadi et al. (2015),
this challenge more in Section 4.12. Similarly, to ensure
have contributed to minimizing the cost of entry.
that the collected data is not compromised, adding sanity
Importantly, progress was enabled also because the time it
checks is recommended along with actually using the data
took to train deep models and iterate on them became
early to train and retrain models. Despite simply acquiring
shorter and shorter. This holds true for robotic learning as
more data faster, running experiments around-the-clock
well. The faster training data can be collected and a
also ensures that robots are exposed tovarying amounts of
hypothesiscanbetested,thefasterprogresswillbemade.
lighting conditions allowing us to train more robust poli-
Despite advances in data efficiency (Section 4.2), deep
cies.However,spot-checkingthecollecteddataisimportant
RL still requires a fair amount of data, especially if visual
aswenoticed,forexample,thattheceilinglightsautomati-
information(images)ispartoftheobservation.Themajor-
callyturnedofffor partsofthenightresultinginvery dark
ity of robot learning experiments to date were conducted
imagescompromisingthedata.
on a single robot closely monitored by a single human
operator.Thisone-to-onerelationbetweenrobotandopera-
tor has been a tedious but effective way to ensure continu- 4.7.3. Non-stationarity owing to environment changes. A
ous and safe operation. The human can reset the scene, learnedpolicywillfailifenvironmentaspectshavesignifi-
stop the robot in unsafe situations, and simply restart and cantly changed since training. For example, the lighting
reset the robot on failures. However, to scale up data col- conditions may significantly shift at night if windows are
lection efforts and increase the throughput of evaluation present in the room, and evaluations done at night may
runs, robots need to run without human supervision. It is haveverydifferentresultsifnodatacollectionhappenedat
impracticaltoallocatemoreoperatorstoaset-upwithmul- that time. The underlying dynamics may have shifted sig-
tiplerobots,orwheneverasinglerobotismeanttorun24/ nificantly since training owing to hardware degradation.
7,andespeciallyboth.Inthefollowing,wediscussthepar- Hardware degradation, such as change of battery level,
ticular challenges that arise in those settings, namely (1) wearandtear,andhardwarefailure,arethemajorcausesof
designingtheexperimentalset-uptomaximizethroughput, dynamic changes. Traditional learning-based approaches,
i.e., the number of episodes/trials per hour, (2) facilitating which have distinctive training and testing phases,

| Ibarzetal. |     |     |     |     |     |     |     |     |     |     |     |     |     | 713 |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
assuming stationary distribution between phases, suffer algorithm.For model-free methods,oneapproachistoadd
from hardware degradation or environment changes not recurrence to the policy network and, in particular, include
captured in the collection phase. In extreme cases of loco- thepreviousactions takenbythepolicyaspart ofthestate
motion, a learned policy can stop working after merely a definition. The recurrent neural network could learn to
fewweeksowingtosignificantrobotdynamicchanges.To extrapolate the observation to when the action is applied,
|     |     |     |     |     |     |     | from the | memorized |     | previous |     | observations. |     | Another |
| --- | --- | --- | --- | --- | --- | --- | -------- | --------- | --- | -------- | --- | ------------- | --- | ------- |
addressthesechallenges,learningalgorithmsneedtoadjust
online (Yu et al., 2017), optimize for quick adaptation approach along the same line, which avoids the additional
(Finnetal.,2017a;Yangetal.,2019),orlearninalifelong cost of training recurrent neural networks, is to augment
fashion. the observation space with a window of previous observa-
This can also have consequences for evaluation proto- tionsandactions.Inpractice,wefindthatthelatterissim-
|     |     |     |     |     |     |     | pler and | equally | effective | (Haarnoja |     | et al., | 2018c; | Xiao |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------- | --------- | --------- | --- | ------- | ------ | ---- |
colswherecomparingtwolearnedpoliciesoreventhesame
| one at different                         |           | times. | We recently | found | that the  | best pol-    | etal.,2020). |           |     |            |         |             |     |          |
| ---------------------------------------- | --------- | ------ | ----------- | ----- | --------- | ------------ | ------------ | --------- | --- | ---------- | ------- | ----------- | --- | -------- |
| icy learned                              | in Levine | et     | al. (2018)  | was   | sensitive | to a hard-   |              |           |     |            |         |             |     |          |
| ware degradation                         |           | of the | fingers,    | which | caused    | a consistent |              |           |     |            |         |             |     |          |
|                                          |           |        |             |       |           |              | 4.9. Setting | goals     | and | specifying |         | rewards     |     |          |
| performancedropof5%inaslittleas800grasps |           |        |             |       |           | executed     |              |           |     |            |         |             |     |          |
|                                          |           |        |             |       |           |              | A critical   | component |     | required   | for any | application |     | of RL is |
onasinglerobot.Onewaytomitigatethisistouseproper
A/BtestingprotocolsasdescribedinTangetal.(2010). the reward function. In simulation or video game environ-
|     |     |     |     |     |     |     | ments,  | the reward | function    |     | is typically |           | easy to | specify, |
| --- | --- | --- | --- | --- | --- | --- | ------- | ---------- | ----------- | --- | ------------ | --------- | ------- | -------- |
|     |     |     |     |     |     |     | because | one has    | full access |     | to the       | simulator | or game | state,   |
4.8. Asynchronous control: thinking and acting at and can determine whether the task was successfully com-
|          |      |     |     |     |     |     | pleted or | access | the score | of  | the game. | In  | the real | world, |
| -------- | ---- | --- | --- | --- | --- | --- | --------- | ------ | --------- | --- | --------- | --- | -------- | ------ |
| the same | time |     |     |     |     |     |           |        |           |     |           |     |          |        |
however,assigningascoretoquantifyhowwellataskwas
TheMDPformulationassumessynchronousexecution:the
|          |       |         |           |       |     |        | completed | can | be a challenging |     | perceptual |     | problem | of its |
| -------- | ----- | ------- | --------- | ----- | --- | ------ | --------- | --- | ---------------- | --- | ---------- | --- | ------- | ------ |
| observed | state | remains | unchanged | until | the | action | is        |     |                  |     |            |     |         |        |
own.Inmostofourcasestudies,wesidestepthisdifficulty
| applied. | However, | onreal | robotic | systems, | theexecutionis |     |           |               |     |       |     |               |     |           |
| -------- | -------- | ------ | ------- | -------- | -------------- | --- | --------- | ------------- | --- | ----- | --- | ------------- | --- | --------- |
|          |          |        |         |          |                |     | in one of | the following |     | ways. | (1) | Instrumenting |     | the envi- |
asynchronous. The state of the robot is continuously evol- ronment with additional sensors that provide reward infor-
| ving as | the state | is measured, |     | transmitted, | the action | calcu- |         |              |     |             |     |             |     |          |
| ------- | --------- | ------------ | --- | ------------ | ---------- | ------ | ------- | ------------ | --- | ----------- | --- | ----------- | --- | -------- |
|         |           |              |     |              |            |        | mation. | For example, |     | an inertial |     | measurement |     | unit was |
lated and applied. Latency measures the delay from when used to measure the angle of the door and the handle to
| the observation |          | is measured |     | at the sensor, | to   | when the |         |              |        |         |          |         |              |          |
| --------------- | -------- | ----------- | --- | -------------- | ---- | -------- | ------- | ------------ | ------ | ------- | -------- | ------- | ------------ | -------- |
|                 |          |             |     |                |      |          | learn a | door-opening |        | task in | Chebotar | et      | al. (2017b), | or a     |
| action is       | actually | executed    | at  | the actuator.  | This | delay    | is      |              |        |         |          |         |              |          |
|                 |          |             |     |                |      |          | motion  | capture      | device | was     | used to  | measure | how          | fast the |
usuallyon theorder of millisecondsto seconds,depending quadruped robot walks (Haarnoja et al., 2019). (2) Simple
onthehardwareandthecomplexityofthepolicy.Theexis-
|     |     |     |     |     |     |     | heuristicssuch |     | as image | subtraction |     | or target | joint | encoder |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | -------- | ----------- | --- | --------- | ----- | ------- |
tence of latency means that the next state of the system values can be valuable in some cases. For example,
doesnotdirectlydependonthemeasuredstate,butinstead
|              |       |         |            |       |                  |     | Kalashnikov       | et  | al. (2018)                      | used | the | gripper | encoder | values |
| ------------ | ----- | ------- | ---------- | ----- | ---------------- | --- | ----------------- | --- | ------------------------------- | ---- | --- | ------- | ------- | ------ |
| on the state | after | a delay | of latency | after | the measurement, |     |                   |     |                                 |      |     |         |         |        |
|              |       |         |            |       |                  |     | anda comparisonof |     | imageswithandwithoutthegrasping |      |     |         |         |        |
which is not observable. Latency violates the most funda- in order to determine whether an object was successfully
| mental assumption |     | of  | MDP | (Xiao et al., | 2020), | and thus |          |              |     |          |            |       |     |            |
| ----------------- | --- | --- | --- | ------------- | ------ | -------- | -------- | ------------ | --- | -------- | ---------- | ----- | --- | ---------- |
|                   |     |     |     |               |        |          | grasped. | (3) Learning |     | a visual | prediction | model |     | as in Finn |
can cause failure to some RL algorithms. For example, we and Levine (2017) avoids the need to define reward func-
| tested SAC | (Haarnoja |     | et al., | 2018c) | and QT-Opt | (Xiao |          |          |       |          |     |        |              |     |
| ---------- | --------- | --- | ------- | ------ | ---------- | ----- | -------- | -------- | ----- | -------- | --- | ------ | ------------ | --- |
|            |           |     |         |        |            |       | tions at | training | time: | instead, | the | reward | is specified | at  |
et al., 2020), two state-of-the-art off-policy algorithms, to evaluation time based on a goal image or equivalent repre-
learn walking on a simulated quadruped robot or grasping sentation.However,noneofthesemethodsnecessarilygen-
objectswithanarm,withdifferentlatencies.Althoughboth
|        |         |     |                   |      |     |         | eralizes    | to any | possible | robot | task | one might | wish | to solve |
| ------ | ------- | --- | ----------------- | ---- | --- | ------- | ----------- | ------ | -------- | ----- | ---- | --------- | ---- | -------- |
| QT-Opt | and SAC | can | learn efficiently | when | the | latency | is usingRL. |        |          |       |      |           |      |          |
zero,theyfailedwhenweincreasethelatency.
|     |     |     |     |     |     |     | Learning | the | reward | function | itself | is a | promising | ave- |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | ------ | -------- | ------ | ---- | --------- | ---- |
Clearly, we need special treatments to combat the non- nue for addressing this problem. It can be learned expli-
Markovianness introduced by latency. For model-based citly,fromdemonstrations(Finnetal.,2016a),fromhuman
methods, the planning component is often computationally annotation (Cabi et al., 2019), from human preferences
expensive, and incurs additional latency. For example, the (Sadigh et al. 2017; Christiano et al. 2017), or from multi-
| popular | sample-based |     | planner, | cross-entropy |     | method |             |     |       |          |        |     |        |           |
| ------- | ------------ | --- | -------- | ------------- | --- | ------ | ----------- | --- | ----- | -------- | ------ | --- | ------ | --------- |
|         |              |     |          |               |     |        | ple sources | of  | human | feedback | (B?y?k |     | et al. | 2020). In |
(CEM)(DeBoeretal.,2005),needstorolloutmanytrajec- these examples, reward function learning is typically done
tories and update the underlying distribution of optimal in parallel with the RL process, because new experience
actionsequences.EvenifCEMisparallelizedusingthelat- data helps train a better reward function approximation.
estGPU,planningalonecanstilltake tens ofmilliseconds. However, large amounts of demonstrations or annotations
To accommodate such latency, in Yang et al. (2020), we may be required. The process of learning reward functions
plan the optimal action sequence based on a future state, from demonstrations, called inverse RL is an underspeci-
which is predicted using the learned dynamic model, to fied problem Ziebart et al. (2008), making it difficult to
compensate for the latency caused by the planning scale toimage observations, and exploitationof thereward

714 TheInternationalJournalofRoboticsResearch40(4-5)
can happen even with in-the-loop reward learning. There 4.11. Safe learning
are promising techniques to try to address some of these
Safety is critical when we apply RL on real robots.
problems, including using metalearned priors (Xie et al.
Although sufficient exploration leads to more efficient
2018) or active queries (Singh et al. 2019), but learning
learning, directly exploring in the real world is not always
rewards with minimal human supervision in the general
safe. Repeated falling, self-collisions, jerky actuation, and
caseremainsanunsolvedproblem.
collisionswithobstaclesmaydamagetherobotanditssur-
roundings, which will require costly repairs and manual
interventions(Section4.12).
4.10. Multi-task learning and meta-learning
One promising approach towards enabling robots to learn
4.11.1. Designing safe action spaces. One simple way to
tasks efficiently is to leverage previous experience from
avoid unsafe behaviors is to restrict the action space such
other tasks rather than training for a task completely from
that any action that a learned policy can take is safe. This
scratch. Multi-task learning approaches aim to do exactly
isusuallyveryrestrictiveandcannotbeappliedtoallappli-
this by learning multiple tasks at once, rather than training
cations. However, there are many cases, particularly in
for a single task. Similarly, meta-learning algorithms train
semi-static environments and tasks, such as grasping and
across multiple tasks such that learning a new future task
manipulation, where this is the right approach. Grasping
can be done very efficiently. Although these approaches
objectsinabinisaverycommontaskinlogistics.Inthese
have shown considerable promise in enabling robots to
settings, safety can typically be enforced by restricting the
quickly adapt to new object configurations (Duan et al.,
work space. For example, in Levine et al. (2018) and
2017),newobjects(Finnetal.,2017b;Jamesetal.,2018),
Kalashnikov et al. (2018), all actions are selected through
andnew terrains or environment conditions (Clavera et al.,
sampling, and unsafe samples are rejected. This allows us
2019; Yu et al., 2019), a number of challenges remain in
to perform safety checks or add constraints to the action
order to make them practical for learning across many dif-
space. By using a geometric model of the robot and the
ferentroboticcontroltasksintherealworld.
world,wecanrejectactionsthatareoutsidethe3Dvolume
The first challenge is to specify the task collection.
above the bin, and reject actions that violate kinematic or
These algorithms assume a collection of training tasks that
geometric constraints. We can also enforce constraints on
are representative of the kinds of tasks that the robot must
the velocity of the arm. Although this allows us to handle
generalize or adapt to at test time. However, specifying a
safety for parts of the robot and environment that can be
reward function for a single task already presents a major
modeled, it does not dealwith anything that is unmodeled,
challenge (Section 4.9), let alone for tens or hundreds of
suchasobjectsinthescenethatwemightwanttograspor
tasks. Some prior works have proposed solutions to this
push aside before grasping. We can mitigate this issue by
problem by deriving goals or skills in an unsupervised
usingaforce-torquesensorattheend-effectortodetectand
manner (Gregor et al., 2017; Jabri et al., 2019). However,
stop motion when an impact occurs. From the point of
we have yet to see these approaches show significant suc-
view of the RL agent, this action appears to have a trun-
cessinreal-worldsettings.
catedeffect. This combinationof strategies canprovide for
Another significant challenge lies in the optimization
aworkablelevelofsafetyinasimpleandeffectivewayfor
landscape of multiple tasks. Learning multiple tasks at
tasksthatarequasi-staticinnature.
oncecanpresentachallengeevenforsupervisedlearning
problems owing to different tasks being learned at differ- 4.11.2. Smooth actions. Typically, exploration strategies
ent rates (Chen et al., 2018; Schaul et al., 2019) or the are realized by adding random noise to the actions.
challenges in determining how to resolve conflicting gra- Uncorrelated random noise injected in the action space for
dient signals between tasks (Sener and Koltun, 2018). exploration can cause jerky motions, which may damage
These optimization challenges can be exacerbated in RL thegearboxandtheactuators,andthusisunsafetoexecute
settings, where they are confounded with challenges in on the robot. Options for smoothing out jerky actions dur-
tradingoffexplorationandexploitation.Thesechallenges ing exploration include: reward shaping by penalizing jer-
are less severe for similar tasks (Duan et al., 2016; Finn kiness of the motion, mimicking smooth reference
etal.,2017a;Rakellyetal.,2019),butposeamajorchal- trajectories (Peng et al., 2018a), learning an additive feed-
lenge for more distinct tasks (Parisotto et al., 2016; Rusu back together with a trajectory generator (Iscen et al.,
etal.,2015). 2018), sampling temporal coherent noise (Haarnoja et al.,
Finally, as we scale learning algorithms towards many 2019;Yangetal.,2020),orsmoothingtheactionsequence
different tasks, all of the existing challenges discussed with low-pass filters. All these techniques work well,
above remain and can be even more tricky, including the although additional manual tuning or user-specified data
need for resetting the environment towards state that are mayberequired.
relevant for the current task 4.12, operating robots at scale In the locomotion case study (Section 3.3), because the
4.7,andhandlingnon-stationarity4.7.3. learning algorithm can freely explore the policy space, the

| Ibarzetal. |     |     |     |     |     |     |     | 715 |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
converged gait may not be periodic, may be jerky or may (Altman, 1999). For example, TRPO (Schulman et al.,
use too much energy, which can damage the robot and its 2015) ensures a stable learning using a Kullback–Leibler
surroundings. They usually do not resemble the gaits of (KL) divergence constraint. More recently, Achiam et al.
animals that we are familiar with in nature. Although it is (2017)andBohezetal.(2019)havealsoappliedconstraint-
possible to mitigate these problems by shaping the reward based optimization to model safety as a set of hard con-
function, we find that a better alternative that requires less straints. In our locomotion projects, we formulated a C-
tuning is to incorporate a periodic and smooth trajectory MDP that has inequality constraints on the roll and the
generator into the learning process. We develop a novel pitch of the robot base, which constitutes a rough measure
neural network architecture, policies modulated trajectory of balance. If the state of the robot stays within the con-
generator (PMTG) (Iscen et al., 2018), which can effec- straints throughout the entire training process, the robot is
tivelyincorporatepriorknowledgeoflocomotionandregu- guaranteed to stay upright. This minimizes the chance of
larize the learned gait. PMTG subdivides the controller fallingwhen the robot is learning towalk. The constrained
into an open-loop and a feedback component. The open- formulation usually performs better because as long as the
loop trajectory generator creates smooth and periodic leg constraints are met, no gradients is generated, and thus no
motion, whereas the feedback policy, represented by a interference can happen between the safety constraints and
neural network, can be learned to modulate this trajectory therewardobjective.However,toostringentconstraintswill
generator,tochangewalkingspeed,direction,andstyle.As limitexplorationandcanleadtoslowlearning.
| a result, | the PMTG policies | are safe | to be deployed or |     |     |     |     |     |
| --------- | ----------------- | -------- | ----------------- | --- | --- | --- | --- | --- |
directlylearnedontherealrobot.
|     |     |     |     | 4.11.5.     | Robustness to unseen | observations.    | Last, but         | not |
| --- | --- | --- | --- | ----------- | -------------------- | ---------------- | ----------------- | --- |
|     |     |     |     | least, even | if the training      | process is safe, | the final learned |     |
4.11.3. Recognizing unsafe situations. It is crucial to policy can execute unexpected, and potentially unsafe,
recognize that unsafe situations is about to happen, so that actions when encountering unseen observations. To
arecoveringpolicycanbedeployedtokeeptherobotsafe, improve the generalization of the policy to unseen situa-
or to shutdown the robot completely. Heuristic-based tions, we adopted a robust control approach. We use
approaches can be designed to recognize these unsafe domain randomization, which samples different physical
states or actions by checking whether the action will parameters, or add perturbation forces, either randomly or
causecollision,orwhetherthepowerandthetorqueexceed adversarially (Pinto et al., 2017), to the robot during train-
the limit. Performing these rule-based safety checks often ing, to force it to learn to react under a wide variety of
require careful tuning and a rich set of onboard sensors. observations.Beforedeployingthepolicyontherobots,we
Furthermore, we can also employ learning to recognize also perform extensive evaluations in simulation about the
unsafe situations. These approaches can use ensemble safety and the performance of the controller on untrained
models to estimate uncertainty (Deisenroth and scenarios. Occasionally, the robot, which is trained to be
Rasmussen, 2011; Eysenbach et al., 2018) of certain pre- robust and passed all the safety checks in simulation, can
dictions,whichcanbeagoodindicatorwhetheranyunsafe still misbehave in the real world. In these rare situations,
behavior may happen, or can directly learn the probability the model-based or heuristic-based safety checks, such as
of future unsafe behaviors from experience (Gandhi et al. self-collision detection, power/torque limit, or acceleration
2017; Srinivasan et al. 2020). Once a precarious situation threshold,willtriggerandshutdowntherobot.
isrecognized,arecoveringpolicycanbedeployedtomove
| the robot  | back to a safe     | state. The task policy, | the recover-       |             |             |     |     |     |
| ---------- | ------------------ | ----------------------- | ------------------ | ----------- | ----------- | --- | --- | --- |
|            |                    |                         |                    | 4.12. Robot | persistence |     |     |     |
| ing policy | and the classifier | for safety              | can all be learned |             |             |     |     |     |
simultaneously(Eysenbachetal.,2018;Thananjeyanetal., We use theterm robot persistenceto refer tothecapability
2020). For example, in a locomotion task, when the robot of the robot to persist in collecting data and training with
is in a balance state, the task policy (walking) is executed minimal human intervention. Persistence is crucial for
andupdated.Whentherobot isabout to fall,which ispre- larger-scale robotic learning, because the effectiveness of
dicted by the learned Q-function, the recovering policy modern machine learning models (i.e., deep neural net-
(stand up) takes over. The data collected in this mode is works) is critically dependenton the quantity and diversity
usedtoupdatetherecoveringpolicy.Weshowedthatlearn- of training data, and persistence is required to collect large
ing them simultaneously can dramatically reduce the num- training sets. We can divide the problem of robot persis-
beroffallsduringtraining. tence into two main categories: (1) self-persistence, the
|                                     |           |                       |              | robot must   | avoid damaging  | itself during  | training; (2)         | task |
| ----------------------------------- | --------- | --------------------- | ------------ | ------------ | --------------- | -------------- | --------------------- | ---- |
|                                     |           |                       |              | persistence, | the robot must  | act so that    | it can continue       | to   |
| 4.11.4.Constraininglearnedpolicies. |           | Oneobviouswayto       |              |              |                 |                |                       |      |
|                                     |           |                       |              | perform      | the task. Robot | persistence is | critical for enabling |      |
| avoid unsafe                        | behaviors | is to penalize unsafe | actions each |              |                 |                |                       |      |
autonomousdatacollectionsafelyandatscale.
| time they  | are taken. However, | this can be     | hard in practice, |     |     |     |     |     |
| ---------- | ------------------- | --------------- | ----------------- | --- | --- | --- | --- | --- |
| as careful | tuning is needed    | for the weights | of this penalty   |     |     |     |     |     |
term. A more effective alternative is to formulate safe RL 4.12.1 Self-persistence. We define self-persistence as the
as a constrained Markov decision process (C-MDP) ability for the robot to keep its full range of motion while

716 TheInternationalJournalofRoboticsResearch40(4-5)
performing a task. If the robot were to collide with itself, scene. Previous work such as that of Pinto and Gupta
ortheenvironment,andendupdamagingitself,itmayend (2016) and Finn and Levine (2017) limited the task and
uplosingcertainabilities,requiringhumanintervention.In action space to bewithin a bin, which helped keep objects
Section 4.11, we provide a few strategies to improve self- initbyhavingraisedsidewallsaswellastackledtasksthat
persistence. requireda simplereset:justopenthegripperabove thebin
and bring it back to a home position which can easily be
scripted. Because task persistence was resolved to some
4.12.2 Task persistence. Task persistence is the capability
extent, some of those work managed to collect millions of
oftheroboticset-uptoaccomplisharangeoftasks,repeat-
trials (Kalashnikov et al., 2018; Levine et al., 2018).
edly, in the case of grasping, hundreds of thousands of
Unfortunately, many tasks do not have these nice proper-
times to learn the task. Being able to retry a task is tightly
ties. For example, Chebotar et al. (2017a) leveraged a
coupled with the environment itself andis, to this day, still
human to perform thereset by bringing the puck back to a
anunsolvedproblemforalargerangeoftasks.
positionwherethehockeystickcouldhititagain.Haarnoja
Challengescanoccurwheretherobotworkspaceislim-
etal.(2019)hadtobringtheleggedrobotbacktoitsinitial
ited, and thus objects required to accomplish a task may
startingpositioneverytimetherobotreachedtheendofthe
accidentally be thrown out of reach. In this case, we need
limited 5 m workspace. In both cases, task persistencewas
to find exploration strategies that avoid ending up in such
not achieved and humans were performing the reset proce-
states, in avery limited data regime, to avoid human inter-
dure.Thismakesdatacollectionhardtoscalebecause(1)it
ventions that are needed every time such an unrecoverable
was very time consuming for a human and (2) in both
state is encountered. In high-dimensional states, such as
cases, they stopped because they started to feel back pain
images,thisbecomesachallengingproblemasevendefin-
while performing the environment reset. As such, only a
ing those states becomes a challenge on its own: how do
few hours of data, and less than 1,000 trials were
we know from an image that an object has fallen off the
performed.
bin?
More recently, work such as that of Eysenbach et al.
Anotherclassofchallengesthatwealsoputinthiscate-
(2018) tried to tackle this issue of task persistence by inte-
gory is what is often called ‘‘environment reset.’’ In many
gratingenvironmentresetaspartofthelearningprocedure,
cases, once the task is accomplished, changes in the envi-
in a task-agnostic way. However, this work only explored
ronment may need to happen before another trial can be
tasks which have a unique starting point, that can be
done.Thisiseasytodoinsimulation:justresetthestateof
reachedfrommoststates.Thisstrategyisnotalwayspossi-
the environment. In the real world, this can often be much
ble such as in self-driving cars, where going backward to
harder to accomplish, as resetting the environment is a
comebacktothestartingpointisgenerallynotsafe.
sequence of robotic tasks, which may be as hard or harder
than the task we are trying to learn itself. An example is
learningtoscrewthecapofabottleagain,wemayhaveto
5. Discussion and conclusions
unscrew it to be able to try to screw it again. Pouring or
assembly tasks are also examples where resetting the envi- In this article, we discussed how deep RL algorithms can
ronment may be as challenging or may require many steps be approached in a robotics context. We provided a brief
to accomplish. Automating the whole process of environ- reviewofrecentworkonthistopic,amorein-depthdiscus-
ment reset is required if we want the robot to persist to sion focusing on a set of case studies, and a discussion of
learn the task. It becomes a challenge of identifying the themajorchallengesindeepRLasitpertainstoreal-world
rightsetofsub-taskswhoseresetactionwealreadylearned robotic control. Our aim was to present the reader with a
howtodowitharobot. high-level summary of the capabilities of current deep RL
Onoccasion,sometasksarephysicallyirreversible,such methodsintheroboticsdomain,discusswhichissuesmake
as welding two pieces of metal, cutting food with a knife, deployment of deep RL methods difficult, and provide a
cutting paper with scissors, or writing with a marker. In perspective on how some of those difficulties can be miti-
those cases, other robots may have to bring newobjects to gatedoravoided.
the robot trying to learn those tasks, which may be much AlthoughdeepRLisoftenregardedasbeingtooineffi-
harderthantryingtoaccomplishthetaskitself. cientforreal-worldlearningscenarios,describedinSection
Solving task persistence remains mostly an open prob- 4.2, we discuss how, in fact, deep RL methods have been
lem. Although guided policy search methods that can han- applied successfully on tasks ranging from quadrupedal
dlerandominitialstateshavebeendeveloped(Montgomery walking, to grasping novel objects, to learning varied and
etal.,2017;MontgomeryandLevine,2016),theystillrely complex manipulation skills. These case studies illustrate
onclusteringtheinitialstatesintoadiscretesetof‘‘similar’’ that deep RL can, in fact, be used to learn directly in the
states,whichmaybeimpracticalinsomecases,suchasthe real wold, can learn to utilize raw sensory modalities such
diverse grasping task discussed in Section 3.2 and the as camera images, and can learn tasks that present a sub-
diverse pushing task in Section 3.1.3, where the ‘‘state’’ stantial physical challenge, such as walking and dexterous
includes the positions and identities of all objects in the manipulation.Mostimportantly,thesecasestudiesillustrate

| Ibarzetal. |     |     |     |     |     |     |     |     |     |     |     | 717 |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
that policies trained with deep RL can generalize effec- reward function or reward signal is an external signal that
tively, such as in the case of the robotic grasping experi- is provided by the environment, in robotic learning this
mentsdiscussedinSection3.2. function must itself be programmed, or otherwise learned
However, utilizing deep RL does present a number of by the robot. As we expand the number of tasks we want
significant challenges, and though these challenges do not our robots to accomplish via techniques such as multi-task
|          |         |              |     |         |       |           |      | or meta-learning | discussed | in Section | 4.10, | the efforts in |
| -------- | ------- | ------------ | --- | ------- | ----- | --------- | ---- | ---------------- | --------- | ---------- | ----- | -------------- |
| preclude | current | applications |     | of deep | RL in | robotics, | they |                  |           |            |       |                |
dolimititsimpact.Someofthesechallengeshavepartialor defining those reward functions will continue to increase.
completecurrentsolutions,whereassomedonot.Although This can serve as a major barrier to deployment of RL
current deep RL methods are not as inefficient as often algorithms in practice, though it can be mitigated with a
believed,providedthatanappropriatealgorithmisusedand varietyofautomaticandsemi-automaticrewardacquisition
the hyperparameters are chosen correctly, efficiency and methods,asdiscussedinSection4.9.
stability remain major challenges, and additional research We believe that these challenges, though addressed in
onRLalgorithmdesignshouldfocusonfurther improving part over thepast few years, offera fruitful rangeof topics
both. The use of simulation can further reduce challenges forfutureresearch.Addressingthemwillbringuscloserto
owing to sample efficiency, though simulation alone does a future where RL can enable any robot to learn any task.
not solve all issues with robotic learning. Exploration can This would lead to an explosive growth in the capabilities
poseamajorchallengeinroboticRL,butweoutlineavari- of autonomous robots: when the capabilities of robots are
|             |     |       |             |            |     |        |       | limited | primarily by the | amount of robot | time | available to |
| ----------- | --- | ----- | ----------- | ---------- | --- | ------ | ----- | ------- | ---------------- | --------------- | ---- | ------------ |
| ety of ways | in  | which | exploration | challenges |     | can be | side- |         |                  |                 |      |              |
steppedinpracticalroboticcontrolproblems,fromutilizing learn skills, rather than the amount of engineering time
demonstrations to baseline hand-engineered controllers. Of necessary to program them, robots will be able to acquire
course, not all exploration challenges can be overcome in large skill repertoires. A suitable goal for robotic deep RL
thisway,but‘‘solving’’thedifficultRLexplorationproblem research would be to make robotic RL as natural and scal-
|     |     |     |     |     |     |     |     | able as | the learning performed | by  | humans | and animals, |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ---------------------- | --- | ------ | ------------ |
shouldnotbeaprerequisiteforeffectiveapplicationofdeep
RLinrobotics.Generalizationpresentsachallengefordeep where any behavior can be acquired without manual scaf-
|     |     |     |     |     |     |     |     | folding | or instrumentation, | provided | that the | task is speci- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------------------- | -------- | -------- | -------------- |
RL,butincontrasttoargumentsmadeinmanypriorworks,
we do not believe that this issue is any more pronounced fied precisely, is physically possible, and does not pose an
than in anyother machine learning field, and the availabil- unreasonableexplorationchallenge.
ityoflargeanddiversedatacanenableRLpoliciestogen-
| eralize | in the | same | way as | it enables | generalization |     | for | Funding |     |     |     |     |
| ------- | ------ | ---- | ------ | ---------- | -------------- | --- | --- | ------- | --- | --- | --- | --- |
supervised models. Indeed, deep RL is likely to have an Thisresearchreceivednospecificgrantfromanyfundingagency
advantage here: if generalization is limited primarily by inthepublic,commercial,ornot-for-profitsectors.
| data quantity |     | and diversity, |     | automatically | labeled | robotic |     |     |     |     |     |     |
| ------------- | --- | -------------- | --- | ------------- | ------- | ------- | --- | --- | --- | --- | --- | --- |
ORCIDiDs
| experience | can | likely | be collected | in  | much larger | amounts |     |     |     |     |     |     |
| ---------- | --- | ------ | ------------ | --- | ----------- | ------- | --- | --- | --- | --- | --- | --- |
thanhand-labeleddata. JulianIbarz https://orcid.org/0000-0002-9920-6978
Beyond the algorithmic challenges in deep RL, robotic MrinalKalakrishnan https://orcid.org/0000-0003-4292-9857
| deep RL  | also         | presents | a number        | of       | challenges | that    | are    |            |     |     |     |     |
| -------- | ------------ | -------- | --------------- | -------- | ---------- | ------- | ------ | ---------- | --- | --- | --- | --- |
| unique   | to the       | robotics | setting:        | learning | complex    |         | skills | References |     |     |     |     |
| requires | considerable |          | data collection |          | by the     | robots, | which  |            |     |     |     |     |
AbadiM,AgarwalA,BarhamP,etal.(2015)TensorFlow:Large-
requirestheabilitytokeeptherobotsoperationalwithmin-
|            |               |     |            |     |          |         |      | scale | machine learning | on heterogeneous | systems. | http://ten- |
| ---------- | ------------- | --- | ---------- | --- | -------- | ------- | ---- | ----- | ---------------- | ---------------- | -------- | ----------- |
| imal human | intervention. |     | Conducting |     | training | without | per- |       |                  |                  |          |             |
sorflow.org/.
| sistent human |     | oversight | is itself | a significant |     | engineering |     |        |                  |              |          |             |
| ------------- | --- | --------- | --------- | ------------- | --- | ----------- | --- | ------ | ---------------- | ------------ | -------- | ----------- |
|               |     |           |           |               |     |             |     | Achiam | J, Held D, Tamar | A and Abbeel | P (2017) | Constrained |
challenges, and requires certain best practices, as we dis- policyoptimization.In:International Conference on Machine
| cussinSection4.7.Thislastchallengeistightlyconnected |     |     |     |     |     |     |     | Learning. |     |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- |
to designing persistent robots, aswe desirefor therobot to AgarwalR,Schuurmans D andNorouziM (2020)Anoptimistic
be an autonomous agent in the real world, there are many perspectiveonofflinereinforcementlearning.In:International
challenges that are often overlooked in simulated environ- ConferenceonMachineLearning.
AltmanE(1999)ConstrainedMarkovDecisionProcesses,Vol.7.
| mentswhichwe |     | discuss | inSection4.12.Asrobotsexist |     |     |     | in  |     |     |     |     |     |
| ------------ | --- | ------- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
BocaRaton,FL:CRCPress.
| the real | world, | they | must also | obey | real-time | constraints, |     |     |     |     |     |     |
| -------- | ------ | ---- | --------- | ---- | --------- | ------------ | --- | --- | --- | --- | --- | --- |
AndrychowiczM,WolskiF,RayA,etal.(2017)Hindsightexpe-
whichmeansthatpoliciesmustbeevaluatedinparalleland
|        |         |      |        |           |            |     |        | rience | replay. In: Advances | in Neural | Information | Processing |
| ------ | ------- | ---- | ------ | --------- | ---------- | --- | ------ | ------ | -------------------- | --------- | ----------- | ---------- |
| with a | limited | time | budget | alongside | the motion |     | of the |        |                      |           |             |            |
Systems,pp.5048–5058.
robot: this presents challenges in the classically synchro- BellemareM,SrinivasanS,OstrovskiG,SchaulT,SaxtonDand
| nous MDP | model | (Section | 4.8). | Finally, | and | importantly, |     |     |     |     |     |     |
| -------- | ----- | -------- | ----- | -------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
MunosR(2016)Unifyingcount-basedexplorationandintrin-
| real-world | RL  | requires | to  | define | a reward | function. |     |     |     |     |     |     |
| ---------- | --- | -------- | --- | ------ | -------- | --------- | --- | --- | --- | --- | --- | --- |
sicmotivation.In:AdvancesinNeuralInformationProcessing
Although it is common in RL research to assume that the Systems,pp.1471–1479.

718 TheInternationalJournalofRoboticsResearch40(4-5)
BohezS,AbdolmalekiA,NeunertM,BuchliJ,HeessNandHad- DeisenrothMP,NeumannGandPetersJ(2013)Asurveyonpol-
sellR(2019)Valueconstrainedmodel-freecontinuouscontrol. icy search for robotics. In: Foundations and Trends in
arXivpreprintarXiv:1902.04623. Robotics,Vol.2.NowPublishers,Inc.,pp.1–142.
Bojarski M, Del Testa D, Dworakowski D, et al. (2016) End to DengJ,DongW,SocherR,LiLJ,LiKandFei-FeiL(2009)Ima-
end learning for self-driving cars. arXiv preprint genet: A large-scale hierarchical image database. In: Confer-
arXiv:1604.07316. ence onComputerVisionandPattern Recognition. IEEE,pp.
BousmalisK,IrpanA,WohlhartP,etal.(2018)Usingsimulation 248–255.
and domain adaptation to improve efficiency of deep robotic DevlinJ,ChangMW,LeeKandToutanovaK(2019)BERT:Pre-
grasping. In:International Conference onRobotics andAuto- trainingofdeepbidirectionaltransformersforlanguageunder-
mation.IEEE,pp.4243–4250. standing.In:NAACL-HLT.
Bousmalis K, Silberman N, Dohan D, Erhan D and Krishnan D Draeger A, Engell S and Ranke H (1995) Model predictive con-
(2017) Unsupervised pixel-level domain adaptation with gen- trol using neural networks. Control Systems Magazine 15(5):
erative adversarial networks. In: Conference on Computer 61–66.
VisionandPatternRecognition. DuanY,AndrychowiczM,StadieB,etal.(2017)One-shotimita-
BrockmanG,CheungV,PetterssonL,etal.(2016)OpenAIGym. tion learning. In: Advances in Neural Information Processing
arXivpreprintarXiv:1606.01540. Systems,pp.1087–1098.
Burda Y, Edwards H, Storkey A and Klimov O (2019) Explora- DuanY,SchulmanJ,ChenX,BartlettPL,SutskeverIandAbbeel
tion by random network distillation. In: International Confer- P(2016)RL2:Fastreinforcementlearningviaslowreinforce-
enceonLearningRepresentations. mentlearning.arXivpreprintarXiv:1611.02779.
Byravan A, Leeb F, Meier F and Fox D (2018) SE3-Pose-Nets: Ebert F, Finn C, Dasari S, Xie A, Lee A and Levine S (2018)
Structured deep dynamics models for visuomotor control. In: Visualforesight:Model-baseddeepreinforcementlearningfor
InternationalConferenceonRoboticsandAutomation. vision-basedroboticcontrol.arXivpreprintarXiv:1812.00568.
Cabi S,ColmenarejoSG,NovikovA,etal.(2019)A framework EysenbachB,GuS,IbarzJandLevineS(2018)Leavenotrace:
fordata-drivenrobotics.arXivpreprintarXiv:1909.12200. Learning to reset for safe and autonomous reinforcement
Chebotar Y, Hausman K, Zhang M, Sukhatme G, Schaal S and learning. In: International Conference on Learning
Levine S (2017a) Combining model-based and model-free Representations.
updatesfortrajectory-centricreinforcementlearning.In:Inter- Finn C, Abbeel P and Levine S (2017a) Model-agnostic meta-
nationalConferenceonMachineLearning,pp.703–711. learningforfastadaptationofdeepnetworks.In:International
ChebotarY,KalakrishnanM,YahyaA,LiA,SchaalSandLevine ConferenceonMachineLearning.
S(2017b)Pathintegralguidedpolicysearch.In:International Finn C and Levine S (2017) Deep visual foresight for planning
Conference on Robotics and Automation. IEEE, pp. 3381– robot motion. In: International Conference on Robotics and
3388. Automation.IEEE.
Chen Z, Badrinarayanan V, Lee CY and Rabinovich A (2018) Finn C, Levine S and Abbeel P (2016a) Guided cost learning:
GradNorm:Gradientnormalizationforadaptivelossbalancing Deepinverseoptimalcontrolviapolicyoptimization.In:Inter-
in deep multitask networks. In: International Conference on nationalConferenceonMachineLearning,pp.49–58.
MachineLearning. Finn C, Tan XY, Duan Y, Darrell T, Levine S and Abbeel P
Chiang HTL, Faust A, Fiser M and Francis A (2019) Learning (2016b)DeepSpatialAutoencodersforVisuomotorLearning.
navigationbehaviorsend-to-endwithAutoRL.IEEERobotics In: International Conference on Robotics and Automation.
andAutomationLetters4(2):2007–2014. IEEE,pp.512–519.
ClaveraI,NagabandiA,LiuS,etal.(2019)Learningtoadaptin FinnC,YuT,ZhangT,AbbeelPandLevineS(2017b)One-shot
dynamic,real-worldenvironmentsthroughmeta-reinforcement visual imitation learning via meta-learning. Proceedings of
learning. In: International Conference on Learning MachineLearningResearch78:357–368.
Representations. FoxR,PakmanAandTishbyN(2016)Tamingthenoiseinrein-
Clegg A, Yu W, Tan J, Liu CK and Turk G (2018) Learning to forcementlearningviasoftupdates.In:ConferenceonUncer-
dress:Synthesizinghumandressingmotionviadeepreinforce- taintyinArtificialIntelligence.AUAIPress.
ment learning. In: SIGGRAPH Asia 2018 Technical Papers. Fu J, Co-Reyes J and Levine S (2017) Ex2: Exploration with
NewYork:ACMPress. exemplar models for deep reinforcement learning. In:
CoumansEandBaiY(2016)PyBullet,aPythonmoduleforphy- Advances in Neural Information Processing Systems, pp.
sics simulation, games, robotics and machine learning. http:// 2577–2587.
pybullet.org/. FujimotoS,MegerDandPrecupD(2019)Off-policydeeprein-
DanielC,NeumannG,KroemerO andPetersJ(2013)Learning forcementlearningwithoutexploration.In:InternationalCon-
sequential motor tasks. In: International Conference on ferenceonMachineLearning.
RoboticsandAutomation.IEEE. FujimotoS,vanHoofHandMegerD(2018)Addressingfunction
DeA(2017)ModularHoppingandRunningviaParallelCompo- approximation error in actor–critic methods. In: International
sition.PhDThesis,UniversityofPennsylvania. ConferenceonMachineLearning.
DeBoer PT, KroeseDP, Mannor S andRubinstein RY (2005)A Garofolo JS, Lamel LF, Fisher WM, Fiscus JG and Pallett DS
tutorial on the cross-entropy method. Annals of Operations (1993) DARPA TIMIT acoustic–phonetic continous speech
Research134(1):19–67. corpus CD-ROM. NIST speech disc 1-1.1. NASA STI/Recon
DeisenrothMandRasmussenC(2011)Pilco:Amodel-basedand TechnicalReport93.
data-efficientapproachtopolicysearch.In:InternationalCon- GhadirzadehA,MakiA,KragicDandBjo¨rkmanM(2017)Deep
ferenceonMachineLearning.Omnipress,pp.465–472. predictive policy training using reinforcement learning. In:

Ibarzetal. 719
International Conference on Intelligent Robots and Systems. learning. In: Advances in Neural Information Processing Sys-
IEEE,pp.2351–2358. tems,pp.10519–10530.
GoodfellowI,Pouget-AbadieJ,MirzaM,etal.(2014)Generative JainD,LiA,SinghalS,RajeswaranA,KumarVandTodorovE
adversarial nets. In:Advances inNeuralInformation Process- (2019) Learning deep visuomotor policies for dexterous hand
ingSystems,pp.2672–2680. manipulation. In: International Conference on Robotics and
GregorK,RezendeDJandWierstraD(2017)Variationalintrinsic Automation.IEEE,pp.3636–3643.
control.In:InternationalConferenceonLearningRepresenta- JamesS,BloeschMandDavisonAJ(2018)Task-embeddedcon-
tions,WorkshopTrackProceedings. trol networks for few-shot imitation learning. In: Conference
Gu S, Holly E, Lillicrap Tand Levine S (2017) Deep reinforce- onRobotLearning.
mentlearningforroboticmanipulationwithasynchronousoff- JamesS,DavisonAJandJohnsE(2017)Transferringend-to-end
policy updates. In: International Conference on Robotics and visuomotor control from simulation to realworld for a multi-
Automation.IEEE,pp.3389–3396. stagetask.In:ConferenceonRobotLearning.
Gu S, Lillicrap T, Sutskever I and Levine S (2016) Continuous James S, Wohlhart P, Kalakrishnan M, et al. (2019) Sim-to-real
deep Q-learning with model-based acceleration. In: Interna- via sim-to-sim: Data-efficient robotic grasping via
tionalConferenceonMachineLearning,pp.2829–2838. randomized-to-canonical adaptation networks. In: Conference
HaS,KimJandYamaneK(2018)Automateddeepreinforcement onComputerVisionandPatternRecognition.
learningenvironmentforhardwareofamodularleggedrobot. JohanninkT,BahlS,NairA,etal.(2019)Residualreinforcement
In:InternationalConferenceonUbiquitousRobots.IEEE. learning for robot control. In: International Conference on
HaarnojaT,HaS,ZhouA,TanJ,TuckerGandLevineS(2019) RoboticsandAutomation.IEEE.
Learning to walk via deep reinforcement learning. In: Kakade SM (2002) A natural policy gradient. In: Advances in
Robotics:ScienceandSystems. NeuralInformationProcessingSystems,pp.1531–1538.
Haarnoja T, Pong V, Zhou A, Dalal M, Abbeel P and Levine S KalashnikovD,IrpanA,PastorP,etal.(2018)Scalabledeeprein-
(2018a) Composable deep reinforcement learning for robotic forcement learning for vision-based robotic manipulation. In:
manipulation. In: International Conference on Robotics and Conference on Robot Learning, Proceedings of Machine
Automation.IEEE. LearningResearch.
Haarnoja T, Tang H, Abbeel P and Levine S (2017) Reinforce- KhadkaS,MajumdarS,NassarT,etal.(2019)Collaborativeevo-
ment learning with deep energy-based policies. In: Interna- lutionaryreinforcementlearning.In:InternationalConference
tionalConferenceonMachineLearning,pp.1352–1361. onMachineLearning.
HaarnojaT,ZhouA,AbbeelPandLevineS(2018b)Softactor– Kober J, Bagnell JA and Peters J (2013) Reinforcement learning
critic:Off-policymaximumentropydeepreinforcementlearn- in robotics: A survey. The International Journal of Robotics
ing with a stochastic actor. In: International Conference on Research32(11):1238–1274.
MachineLearning. KohlNandStoneP(2004)Policygradientreinforcementlearning
HaarnojaT,ZhouA,HartikainenK,etal.(2018c)Softactor–critic forfastquadrupedallocomotion.In:InternationalConference
algorithmsandapplications.arXivpreprintarXiv:1812.05905. onRoboticsandAutomation.IEEE.
Ha¨ma¨la¨inen P, Rajama¨ki J and Liu CK (2015) Online control of Konidaris G, Kuindersma S, Grupen R and Barto A (2012)
simulated humanoids using particle belief propagation. ACM Robot learning from demonstration by constructing skill
TransactionsonGraphics34(4):81. trees.TheInternationalJournalofRoboticsResearch31(3):
HausmanK,ChebotarY,KroemerO,SukhatmeGSandSchaalS 360–375.
(2017)Regraspingusingtactileperceptionandsupervisedpol- KroemerO,NiekumSandKonidarisG(2019)Areviewofrobot
icylearning.In:AAAISymposiumonInteractiveMulti-Sensory learning for manipulation: Challenges, representations, and
ObjectPerceptionforEmbodiedAgents. algorithms.CoRRabs/1907.03146.
Heess N, Sriram S, Lemmon J, et al. (2017) Emergence of loco- KumarA,FuJ,SohM,TuckerGandLevineS(2019)Stabilizing
motion behaviours in rich environments. arXiv preprint off-policy Q-learning via bootstrapping error reduction. In:
arXiv:1707.02286. Advances in Neural Information Processing Systems, Vol. 32.
Hester T, Vecerk M, Pietquin O, et al. (2018) Deep Q-learning CurranAssociates,Inc.
fromdemonstrations.In:ConferenceonArtificialIntelligence. Kurutach T, Clavera I, Duan Y, Tamar A and Abbeel P (2018)
HwangboJ,LeeJ,DosovitskiyA,etal.(2019)Learningagileand Model-ensemble trust-region policy optimization. In: Interna-
dynamic motor skills for legged robots. Science Robotics 4: tionalConferenceonLearningRepresentations.
26. KuznetsovaA,RomH,AlldrinN,etal.(2020)Theopenimages
Ijspeert A, Nakanishi J and Schaal S (2002) Movement imita- datasetV4:Unifiedimageclassification,objectdetection,and
tion with nonlinear dynamical systems in humanoid robots. visual relationship detection at scale. International Journal of
In: International Conference on Robotics and Automation. ComputerVision128(7):1956–1981.
IEEE. LeeJ,HwangboJ,WellhausenL,KoltunVandHutterM(2020)
Irpan A (2018) Deep reinforcement learning doesn’t work yet. Learning quadrupedal locomotion over challenging terrain.
https://www.alexirpan.com/2018/02/14/rl-hard.html. ScienceRobotics5(47):eabc5986.
IscenA,CaluwaertsK,TanJ,etal.(2018)Policiesmodulatingtra- Lee MA, Zhu Y, Srinivasan K, et al. (2019) Making sense of
jectorygenerators.In:ConferenceonRobotLearning. vision and touch: Self-supervised learning of multimodal
Jabri A, Hsu K, Gupta A, Eysenbach B, Levine S and Finn C representationsforcontact-richtasks.In:InternationalConfer-
(2019) Unsupervised curricula for visual meta-reinforcement enceonRoboticsandAutomation.IEEE.

720 TheInternationalJournalofRoboticsResearch40(4-5)
Lenz I, Knepper RA and Saxena A (2015) DeepMPC: Learning demonstrations.In:InternationalConferenceonRoboticsand
deeplatentfeaturesformodelpredictivecontrol.In:Robotics: Automation.IEEE,pp.6292–6299.
ScienceandSystems,Rome,Italy. Osband I, Blundell C, Pritzel A and Van Roy B (2016) Deep
LevineSandAbbeelP(2014)Learningneuralnetworkpolicieswith exploration via bootstrapped DQN. In: Advances in Neural
guided policy search under unknown dynamics. In: Advances in InformationProcessingSystems,pp.4026–4034.
NeuralInformationProcessingSystems,pp.1071–1079. ParisottoE,BaJandSalakhutdinovR(2016)Actor-Mimic:Deep
Levine S, Finn C, Darrell T and Abbeel P (2016) End-to-end multitaskandtransferreinforcementlearning.CoRR.
trainingofdeepvisuomotor policies.TheJournalofMachine PaszkeA,GrossS,ChintalaS,etal.(2017)Automaticdifferentia-
LearningResearch17(1):1334–1373. tioninPyTorch.In:AdvancesinNeuralInformationProcess-
LevineSandKoltunV(2013)Guidedpolicysearch.In:Interna- ingSystemsWorkshoponAutodiff.
tionalConferenceonMachineLearning. Pathak D, Agrawal P, Efros AA and Darrell T (2017) Curiosity-
Levine S, Pastor P, Krizhevsky A, Ibarz J and Quillen D (2018) driven exploration by self-supervised prediction. In: Confer-
Learning hand–eye coordination for robotic grasping with enceonComputerVisionandPatternRecognitionWorkshops.
deep learning and large-scale data collection. The Interna- IEEE,pp.16–17.
tionalJournalofRoboticsResearch37(4–5):421–436. PengXB,AbbeelP,LevineS,vandeandPanneM(2018a)Deep-
LevineS,WagenerNandAbbeelP(2015)Learningcontact-rich Mimic: Example-guided deep reinforcement learning of
manipulationskillswithguidedpolicysearch.In:International physics-basedcharacterskills.ACMTransactionsonGraphics
ConferenceonRoboticsandAutomation. 37(4):143.
Lillicrap TP, Hunt JJ, Pritzel A, et al. (2015) Continuous control Peng XB, Andrychowicz M, Zaremba Wand Abbeel P (2018b)
with deep reinforcement learning. arXiv preprint Sim-to-realtransferofroboticcontrolwithdynamicsrandomi-
arXiv:1509.02971. zation.In:InternationalConferenceonRoboticsandAutoma-
Mahajan D, Girshick R, Ramanathan V, et al. (2018) Exploring tion.IEEE.
thelimitsofweaklysupervisedpretraining.In:EuropeanCon- Peng XB, Kumar A, Zhang G and Levine S (2019) Advantage-
ferenceonComputerVision. weightedregression:Simpleandscalableoff-policyreinforce-
MahlerJ,MatlM,LiuX,LiA,GealyDandGoldbergK(2018) mentlearning.arXivpreprintarXiv:1910.00177.
Dex-Net 3.0: Computing robust vacuum suction grasp Peters J, Mu¨lling K and Altu¨n Y (2010) Relative entropy policy
targets in point clouds using a new analytic model and deep search.In:AAAIConferenceonArtificialIntelligence.
learning. In: International Conference on Robotics and PetersJandSchaalS(2006)Policygradientmethodsforrobotics.
Automation. In: International Conference on Intelligent Robots and Sys-
Mania H, Guy A and Recht B (2018) Simple random search of tems.IEEE,pp.2219–2225.
staticlinearpoliciesiscompetitiveforreinforcementlearning. Peters J and Schaal S (2008) Reinforcement learning of motor
In:AdvancesinNeuralInformationProcessingSystems. skillswithpolicygradients.NeuralNetworks21(4):682–697.
ManschitzS,KoberJ,GiengerMandPetersJ(2014)Learningto Pinto L, Davidson J, Sukthankar R and Gupta A (2017) Robust
sequencemovementprimitivesfromdemonstrations.In:Inter- adversarial reinforcement learning. In: International Confer-
nationalConferenceonIntelligentRobotsandSystems. enceonMachineLearning.
MnihV,KavukcuogluK,SilverD,etal.(2013)PlayingAtariwith PintoLandGuptaA(2016)Supersizingself-supervision:Learn-
deepreinforcementlearning.In:AdvancesinNeuralInforma- ingtograspfrom50Ktriesand700robothours.In:Interna-
tionProcessingSystems,DeepLearningWorkshop. tionalConferenceonRoboticsandAutomation.IEEE.
Montgomery W, Ajay A,FinnC, Abbeel PandLevine S (2017) Raibert MH (1986) Legged Robots That Balance. Cambridge,
Reset-free guided policy search: Efficient deep reinforcement MA:MITPress.
learningwithstochasticinitialstates.In:InternationalConfer- RakellyK,ZhouA,FinnC,LevineSandQuillenD(2019)Effi-
enceonRoboticsandAutomation.IEEE,pp.3373–3380. cient off-policy meta-reinforcement learning via probabilistic
Montgomery WHandLevineS (2016)Guidedpolicy searchvia context variables. In: International Conference on Machine
approximate mirror descent. In: Advances in Neural Informa- Learning.
tionProcessingSystems,pp.4008–4016. Rao K, Harris C, Irpan A, Levine S, Ibarz J and Khansari M
Morrison D, Corke P andLeitner J (2018a) Closing the loop for (2020) RL-CycleGAN: Reinforcement learning awaresimula-
robotic grasping: A real-time, generative grasp synthesis tion-to-real. In: Conference on Computer Vision and Pattern
approach.In:Robotics:ScienceandSystems. Recognition.
MorrisonD,TowAW,McTaggartM,etal.(2018b)Cartman:The RawlikK, Toussaint M andVijayakumar S (2013)Onstochastic
low-costCartesianManipulatorthatwontheAmazonRobotics optimal control and reinforcement learning by approximate
Challenge.In:InternationalConferenceonRoboticsandAuto- inference. In: International Joint Conference on Artificial
mation.IEEE. Intelligence.
Nagabandi A, Konolige K, Levine S and Kumar V (2020) Deep RiedmillerM,HafnerR,LampeT,etal.(2018)Learningbyplay-
dynamics models for learning dexterous manipulation. In: ingsolvingsparserewardtasksfromscratch.In:International
ConferenceonRobotLearning. ConferenceonMachineLearning.
Nagabandi A, Yang G, Asmar T, et al. (2018) Learning image- RossS,GordonGandBagnellD(2011)Areductionofimitation
conditioned dynamics models for control of underactuated learningandstructuredpredictiontono-regretonlinelearning.
leggedmillirobots.In:InternationalConferenceonIntelligent In: International Conference on Artificial Intelligence and
RobotsandSystems.IEEE,pp.4606–4613. Statistics.
NairA,McGrewB,AndrychowiczM,ZarembaWandAbbeelP RusuAA,ColmenarejoSG,GulcehreC,etal.(2015)Policydistil-
(2018)Overcomingexplorationinreinforcementlearningwith lation.arXivpreprintarXiv:1511.06295.

Ibarzetal. 721
SadeghiFandLevineS(2017)CAD2RL:Realsingle-imageflight networks from simulation to the real world. In: International
withoutasinglerealimage.In:Robotics:ScienceandSystems. ConferenceonIntelligentRobotsandSystems.IEEE.
Schaal S (2006) Dynamic movement primitives-a framework for Toussaint M (2009) Robottrajectoryoptimizationusing approxi-
motorcontrolinhumansandhumanoidrobotics.In:Adaptive mate inference. In: International Conference on Machine
motion of animals and machines. Berlin: Springer, pp. 261– Learning.NewYork:ACMPress,pp.1049–1056.
280. Vecˇer´ık M, Hester T, Scholz J, et al. (2017) Leveraging demon-
SchaulT,BorsaD,ModayilJandPascanuR(2019)Rayinterfer- strationsfordeepreinforcementlearningonroboticsproblems
ence:Asourceofplateausindeepreinforcementlearning.In: withsparserewards.arXivpreprintarXiv:1707.08817.
Multidisciplinary Conference on Reinforcement Learning and Viereck U, ten Pas A, Saenko K and Platt R (2017) Learning
DecisionMaking. a visuomotor controller for real world robotic grasping
Schoettler G, Nair A, Luo J, et al. (2019) Deep reinforcement using simulated depth images. In: Conference on Robot
learning for industrial insertion tasks with visual inputs and Learning.
natural rewards. In: International Conference on Intelligent WuYH,CharoenphakdeeN,BaoH,TangkarattVandSugiyama
RobotsandSystems. M(2019)Imitationlearningfromimperfectdemonstration.In:
Schulman J, Levine S, Abbeel P, Jordan M and Moritz P (2015) International Conference on Machine Learning, Proceedings
Trustregionpolicyoptimization.In:InternationalConference ofMachineLearningResearch.
onMachineLearning. XiaoT,JangE,KalashnikovD,etal.(2020)Thinkingwhilemov-
Schulman J, Wolski F, Dhariwal P, Radford A and Klimov O ing: Deep reinforcement learning with concurrent control. In:
(2017) Proximal policy optimization algorithms. arXiv pre- InternationalConferenceonLearningRepresentations.
printarXiv:1707.06347. XieA,EbertF,LevineSandFinnC(2019)Improvisationthrough
SchwabD,SpringenbergTJ,MartinsFM,etal.(2019)Simultane- physicalunderstanding:usingnovelobjectsastoolswithvisual
ously learning vision and feature-based control policies for foresight.arXivpreprintarXiv:1904.05538.
real-worldball-in-a-cup.In:Robotics:ScienceandSystems. XieA,SinghA,LevineSandFinnC(2018)Few-shotgoalinfer-
Sener O and Koltun V (2018) Multi-task learning as multi- ence for visuomotor learning and planning. Proceedings of
objective optimization. In: Advances in Neural Information MachineLearningResearch87:40–52.
ProcessingSystems,pp.527–538. XieQ,LuongMT,HovyEandLeQV(2020)Self-trainingwith
ShrivastavaA,PfisterT,TuzelO,SusskindJ,WangWandWebb noisystudentimprovesImageNetclassification.In:Conference
R (2017) Learning from simulated and unsupervised images onComputerVisionandPatternRecognition.
through adversarial training. In: Conference on Computer YangY,CaluwaertsK,IscenA,TanJandFinnC(2019)NoRML:
VisionandPatternRecognition. No-rewardmetalearning.In:AAMAS.
SilverT,AllenK,TenenbaumJandKaelblingL(2018)Residual YangY,CaluwaertsK,IscenA,ZhangT,TanJandSindhwaniV
policylearning.arXivpreprintarXiv:1812.06298. (2020)Dataefficientreinforcementlearningforleggedrobots.
SinghA,YangL,FinnCandLevineS(2019)End-to-endrobotic In:ConferenceonRobotLearning.
reinforcement learning without reward engineering. In: Yen-Chen L, Bauza M and Isola P (2020) Experience-embedded
Robotics:ScienceandSystems. visualforesight.In:ConferenceonRobotLearning.
Su¨nderhaufN,BrockO,ScheirerWJ,etal.(2018)Thelimitsand YuKandRodriguezA(2018)Realtimestateestimationwithtac-
potentials of deep learning for robotics. The International tileandvisualsensing.Applicationtoplanarmanipulation.In:
JournalofRoboticsResearch37(4–5):405–420. InternationalConferenceonRoboticsandAutomation.IEEE.
TanJ,GuY,LiuCKandTurkG(2014)Learningbicyclestunts. Yu W, Tan J, Bai Y, Coumans E and Ha S (2019) Learning fast
ACMTransactionsonGraphics33(4):50. adaptation with meta strategy optimization. arXiv preprint
Tan J, Zhang T, Coumans E, et al. (2018) Sim-to-real: Learning arXiv:1909.12995.
agile locomotion for quadruped robots. In: Robotics: Science Yu W, Tan J, Liu CK and Turk G (2017) Preparing for the
andSystems. unknown: Learning a universal policy with online system
TangD,AgarwalA,O’BrienDandMeyerM(2010)Overlapping identification.In:Robotics:ScienceandSystems.
experimentinfrastructure:More,better,fasterexperimentation. Yu W, Turk G and Liu CK (2018) Learning symmetric and low-
In: International Conference on Knowledge Discovery and energylocomotion.ACMTransactionsonGraphics37(4):144.
DataMining.NewYork:ACMPress. ZengA,SongS,WelkerS,LeeJ,RodriguezAandFunkhouserT
TedrakeR,ZhangTWandSeungHS(2015)Learningtowalkin (2018)Learningsynergiesbetweenpushingandgraspingwith
20minutes.In:WorkshoponAdaptiveandLearningSystems. self-supervised deep reinforcement learning. In: International
tenPasA,GualtieriM,SaenkoKandPlattR(2017)Grasppose ConferenceonIntelligentRobotsandSystems,pp.4238–4245.
detection in point clouds. The International Journal of Zhu H, Gupta A, Rajeswaran A, Levine S and Kumar V (2019)
RoboticsResearch36(13–14):1455–1473. Dexterous manipulation with deep reinforcement learning:
ThananjeyanB,BalakrishnaA,NairS,etal.(2020)RecoveryRL: Efficient, general, and low-cost. In: International Conference
Safereinforcementlearningwithlearnedrecoveryzones.arXiv onRoboticsandAutomation.IEEE.
preprintarXiv:2010.15920. ZiebartBD,MaasA,BagnellJA andDeyAK(2008)Maximum
Tobin J, Fong R, Ray A, Schneider J, Zaremba Wand Abbeel P entropy inverse reinforcement learning. In: National Confer-
(2017) Domain randomization for transferring deep neural enceonArtificialIntelligence.