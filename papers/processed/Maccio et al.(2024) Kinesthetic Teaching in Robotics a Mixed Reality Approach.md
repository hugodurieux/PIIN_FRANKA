|     | Kinesthetic |     |     | Teaching |     | in  | Robotics: | a   | Mixed | Reality | Approach |     |     |
| --- | ----------- | --- | --- | -------- | --- | --- | --------- | --- | ----- | ------- | -------- | --- | --- |
Simone Maccio`, Mohamad Shaaban, Alessandro Carf`ı, and Fulvio Mastrogiovanni
| Abstract—As   |           | collaborative |     | robots      | become    | more          | common in |     |     |     |     |     |     |
| ------------- | --------- | ------------- | --- | ----------- | --------- | ------------- | --------- | --- | --- | --- | --- | --- | --- |
| manufacturing |           | scenarios     | and | adopted     | in hybrid | human-robot   |           |     |     |     |     |     |     |
| teams,        | we should | develop       | new | interaction | and       | communication |           |     |     |     |     |     |     |
strategiestoensuresmoothcollaborationbetweenagents.Inthis
| paper, | we propose | a novel     | communicative |            |             | interface | that uses |     |     |     |     |     |     |
| ------ | ---------- | ----------- | ------------- | ---------- | ----------- | --------- | --------- | --- | --- | --- | --- | --- | --- |
| Mixed  | Reality    | as a medium |               | to perform | Kinesthetic |           | Teaching  |     |     |     |     |     |     |
| (KT)   | on any     | robotic     | platform.     | We         | evaluate    | our       | proposed  |     |     |     |     |     |     |
4202 peS 3  ]OR.sc[  1v50320.9042:viXra
| approach          | in                | a user study       |         | involving     | multiple   | subjects       | and      |     |     |     |     |     |     |
| ----------------- | ----------------- | ------------------ | ------- | ------------- | ---------- | -------------- | -------- | --- | --- | --- | --- | --- | --- |
| two different     |                   | robots, comparing  |         | traditional   |            | physical       | KT with  |     |     |     |     |     |     |
| holographic-based |                   | KT                 | through | user          | experience | questionnaires |          |     |     |     |     |     |     |
| and task-related  |                   | metrics.           |         |               |            |                |          |     |     |     |     |     |     |
| Index             | Terms—Human-Robot |                    |         | Interaction,  |            | Mixed          | Reality, |     |     |     |     |     |     |
| Kinesthetic       |                   | Teaching, Software |         | Architecture. |            |                |          |     |     |     |     |     |     |
I. INTRODUCTION
Insmartfactories,robotsareexpectedtocoexistandwork
alongside humans rather than replace them. This new manu- Fig. 1: An experimenter in the middle of a holographic
facturing paradigm has led to the development of collabora- KT session with the Tiago++ robot. By interacting with
tiverobots,whichareadaptiveandhighlyversatileplatforms andmanipulatingthegreyholographicsphere,superimposed
[1] that can work alongside human workers. Despite its on the digital robot’s wrist and here highlighted via a red
circle,theusercanteachactionstotherobotteammateusing
| growing | popularity, | Human-Robot |     |     | Collaboration |     | (HRC) is |     |     |     |     |     |     |
| ------- | ----------- | ----------- | --- | --- | ------------- | --- | -------- | --- | --- | --- | --- | --- | --- |
still far from reaching maturity, as multiple research facets gestures and voice.
| are yet      | to be | tackled.      | One such | aspect   | involves |     | developing |     |     |     |     |     |     |
| ------------ | ----- | ------------- | -------- | -------- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
| a structured |       | communication |          | enabling | agents   | to  | exchange   |     |     |     |     |     |     |
information intuitively [2]. As multiple social studies have previous work [9], we mainly focused on robot-to-human
shown[3],[4],effectivebi-directionalcommunicationiscru- communication, introducing the concept of communicative
cial for successful collaboration, as it allows agents to infer act and formalizing the communication for conveying the
| each | other’s | actions, | synchronize, |     | and receive |     | appropriate |                    |     |                 |       |     |     |
| ---- | ------- | -------- | ------------ | --- | ----------- | --- | ----------- | ------------------ | --- | --------------- | ----- | --- | --- |
|      |         |          |              |     |             |     |             | robot’s intentions |     | via holographic | cues. |     |     |
feedback from their teammates. Conversely, poor commu- In this paper, we investigate human-to-robot commu-
nication can lead to misunderstandings, failed interactions, teach
|     |     |     |     |     |     |     |     | nication | by leveraging |     | MR to allow | operators | to  |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------------- | --- | ----------- | --------- | --- |
and consequent distrust in the robot teammate [5]. robots through holographic communication. In particular,
Designing a comprehensive communication interface is we embrace the Learning from Demonstration (LfD) ap-
| a complex |     | task that requires |     | selecting | an  | appropriate | com- |              |             |     |                   |     |           |
| --------- | --- | ------------------ | --- | --------- | --- | ----------- | ---- | ------------ | ----------- | --- | ----------------- | --- | --------- |
|           |     |                    |     |           |     |             |      | proach [10], | postulating |     | that LfD sessions | can | be viewed |
municative channel. One of the most promising approaches as communication acts aimed at transferring skills from
combinesMixedReality(MR)withwearableHead-Mounted a human operator to a robot teammate through explicit
| Displays | (HMD), | enabling |     | the creation |     | of engaging | holo- |         |              |               |     |         |            |
| -------- | ------ | -------- | --- | ------------ | --- | ----------- | ----- | ------- | ------------ | ------------- | --- | ------- | ---------- |
|          |        |          |     |              |     |             |       | actions | or gestures. | Specifically, | our | work is | focused on |
graphic interfaces where users perceive 3D digital content one branch of LfD, namely Kinesthetic Teaching (KT), a
| superimposed |     | onto the | surrounding |     | scene | [6]. This | virtual |            |          |           |          |       |           |
| ------------ | --- | -------- | ----------- | --- | ----- | --------- | ------- | ---------- | -------- | --------- | -------- | ----- | --------- |
|              |     |          |             |     |       |           |         | well-known | teaching | technique | in which | human | operators |
layercanactasacommunicativechanneltoachieveintuitive manually drive the robot’s arm or end-effector, enabling the
human-robot communication.In thisregard, fewworks have machine to learn new actions from direct demonstration.
| focused | on  | using MR | to preview |     | a robot’s | intentions | and |                |     |               |          |      |               |
| ------- | --- | -------- | ---------- | --- | --------- | ---------- | --- | -------------- | --- | ------------- | -------- | ---- | ------------- |
|         |     |          |            |     |           |            |     | In the context |     | of this work, | we claim | that | such teaching |
upcoming actions [7], [8], [9], offering helpful visual feed- methodology can be framed into the communicative space
| back | to the | human teammate     |     | during       | collaboration. |                | In our |               |            |               |               |            |              |
| ---- | ------ | ------------------ | --- | ------------ | -------------- | -------------- | ------ | ------------- | ---------- | ------------- | ------------- | ---------- | ------------ |
|      |        |                    |     |              |                |                |        | introduced    | in [9].    | Therefore,    | throughout    | the paper, | we pro-      |
|      |        |                    |     |              |                |                |        | vide an       | analytical | formalization | of KT         | in         | the proposed |
| This | work   | has been supported | by  | the European |                | Union Erasmus+ | Pro-   |               |            |               |               |            |              |
|      |        |                    |     |              |                |                |        | communicative |            | framework     | and translate | it into    | a modular    |
grammeviatheJointMasterDegreeprogramEuropeanMasteronAdvanced
RoboticsPlus(EMARO+),andviatheItaliangovernmentsupportunderthe software component, which enables KT in human-robot
| National   | Recovery | and Resilience | Plan         | (NRRP), | Mission                | 4,  | Component | 2           |           |         |             |                |     |
| ---------- | -------- | -------------- | ------------ | ------- | ---------------------- | --- | --------- | ----------- | --------- | ------- | ----------- | -------------- | --- |
|            |          |                |              |         |                        |     |           | interactive | scenarios | through | holographic | communication. |     |
| Investment | 1.5,     | funded from    | the European |         | Union NextGenerationEU |     | and       |             |           |         |             |                |     |
awardedbytheItalianMinistryofUniversityandResearch.. Our proposed approach, while leveraging MR for intuitive
All the authors are with the Department of Informatics, Bioengi- and straightforward communication between humans and
| neering, | Robotics, | and Systems | Engineering, |     | University | of  | Genoa, Via |     |     |     |     |     |     |
| -------- | --------- | ----------- | ------------ | --- | ---------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
robots,adherestotheLfDparadigm,providingaholographic
| Opera | Pia 13, | 16145 Genoa, | Italy | (Corresponding |     | author | email: si- |     |     |     |     |     |     |
| ----- | ------- | ------------ | ----- | -------------- | --- | ------ | ---------- | --- | --- | --- | --- | --- | --- |
mone.maccio@edu.unige.it) tool to demonstrate skills to the robot teammate in HRC.

Furthermore,giventheunconstrainednatureoftheMRspace motions using passive observation of human actions [26],
where the KT session takes place, our proposed strategy [27], or make use of hand-tracking devices to teach skills
potentially opens up the possibility of performing KT on through teleoperation-based LfD [28]. While providing a
any robotic platform compatible with the Universal Robot straightforward communication interface to transfer skills
Description Format (URDF). to the robotic teammate, these approaches generally require
Inadditiontopresentingsuchaholographic-basedtoolfor a structured environment and complex calibration routines,
KT, we evaluate its effectiveness in demonstrating tasks to which may limit their application in real-world settings.
robots and its perceived user experience (UX). Specifically, On the contrary, adopting MR as a communication medium
we claim that the holographic-based KT approach can serve for LfD could mitigate these drawbacks, as MR-HMDs are
as a suitable alternative to traditional, hand-guided KT in naturally designed for unstructured environments and could
scenarioswherethelatterisnotavailableornotimplemented provide similar demonstration capabilities with minimum
for a particular robot platform. To test this hypothesis, we calibration and setup.
conductedapreliminaryuserstudywith12subjectsandtwo Focusing on the particular branch of KT, some of the
robots, comparing the two KT alternatives using task-based earliest attempts at combining KT and MR still relied on
metrics and UX questionnaires. the physical robot for hand guidance and demonstration and
The paper is organized as follows. Section II reports a employed the holographic medium only for later visualizing
reviewofrelevantliterature.SectionIIIformalizesKTinside the learned robot action and for adding constraints to the
the holographic communication space, whereas Section IV motion [29], [30]. MR-based communication to achieve KT
details the implementation ofthe software components. Sec- is foreshadowed in [31], where the authors exploit the hand-
tion V and Section VI respectively discuss the experimental tracking capabilities of MR-HMD devices to manually drive
scenariodevisedtotesttheholographicKTapproachandthe the individual joints of an industrial robotic manipulator,
user study results. Finally, Section VII provides conclusions teachingmotionstothemachineintheprocess.Similarly,in
| and possible | extensions | for | this work. |     |     |     |     |     |     |     |     |     |     |
| ------------ | ---------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[32]asystemispresentedwhereatabletopholographicrobot
|     |     |                |     |     |     |     | can be taught  | a simple | pick-and-place |      | task | via      | holographic |
| --- | --- | -------------- | --- | --- | --- | --- | -------------- | -------- | -------------- | ---- | ---- | -------- | ----------- |
|     |     | II. BACKGROUND |     |     |     |     |                |          |                |      |      |          |             |
|     |     |                |     |     |     |     | hand guidance. | Finally, | a recent       | work | [33] | proposed | an MR       |
Over the years, various communication strategies have interfaceforintuitivelyteachingtrajectoriestoaholographic
been explored and adopted in HRC, involving both explicit collaborative manipulator. All of the aforementioned works,
media (e.g., voice [11], upper limb gestures [12], [13], light however, lack a homogeneous, structured representation of
and visual cues [14], [15]) and implicit ones (e.g. gaze [16], the underlying communication acts allowing operators to
posture and body motions [17]). However, most of these transfer skills to the robotic teammate. Additionally, they
approacheshaveintrinsiclimitationsandcannotbeemployed lackanempiricalassessmentofthedemonstrationcapacities
fordevelopingabi-directionalcommunicationinterface,thus and perceived users’ experience of these solutions.
| limiting | their adoption | to  | a subset | of collaborative |     | appli- |            |        |          |           |     |             |         |
| -------- | -------------- | --- | -------- | ---------------- | --- | ------ | ---------- | ------ | -------- | --------- | --- | ----------- | ------- |
|          |                |     |          |                  |     |        | Therefore, | unlike | previous | research, | in  | the present | article |
cations. For example, human-like communication involving we aim at consistently framing KT inside the holographic
gestures and gaze may be expressive and intuitive, but most communication space introduced in [9] and present a stan-
| collaborative | platforms | physically | lack | the features |     | needed |                 |     |              |     |         |       |           |
| ------------- | --------- | ---------- | ---- | ------------ | --- | ------ | --------------- | --- | ------------ | --- | ------- | ----- | --------- |
|               |           |            |      |              |     |        | dalone approach |     | for MR-based | KT  | for any | robot | which can |
to replicate such cues. be described through the URDF format. Furthermore, we
With the introduction of Augmented Reality (AR) in provide an experimental evaluation of the communicative
mobile devices like smartphones and tablets, a new virtual capabilities offered by our MR-based KT tool, assessing
layercouldbeexploitedbyresearcherstoenableintuitiveand the learned robot skills in an interactive human-robot task.
| straightforward | communication |     | between | human | and | robot |     |     |     |     |     |     |     |
| --------------- | ------------- | --- | ------- | ----- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
Finally,theproposedframework,adheringtotheopen-source
teammates [18], [19], [20]. This approach has become even paradigm,ismadepubliclyavailabletootherresearchersand
morerelevantwiththeadoptionofMR-HMDdevices,which companies, who can employ it off-the-shelf as an alternative
offerawholenewlevelofimmersionandmakeitpossibleto to traditional KT with any URDF-compatible robot, with
developinterfacesforeitherprogrammingrobots’behaviours minimum hardware setup required1.
| [21], [22], | [23] | or getting | intuitive | feedback | throughout |     |     |     |     |     |     |     |     |
| ----------- | ---- | ---------- | --------- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
the interaction [24], [25]. In this context, researchers also III. FORMALIZATION
| focused | on conveying | robot’s | intentions | via | MR, evaluating |     |           |     |            |          |     |      |             |
| ------- | ------------ | ------- | ---------- | --- | -------------- | --- | --------- | --- | ---------- | -------- | --- | ---- | ----------- |
|         |              |         |            |     |                |     | Recalling | the | definition | provided | in  | [9], | we describe |
intuitive and expressive strategies for robots to anticipate communicationastheactofconveyingortransmittingpieces
| their actions | via | holographic | cues | during interactive |     | tasks |     |     |     |     |     |     |     |
| ------------- | --- | ----------- | ---- | ------------------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
ofinformation(I)throughoneormorecommunicativechan-
| efficiently | [7], [8], | [9]. |     |     |     |     |             |            |            |       |     |          |           |
| ----------- | --------- | ---- | --- | --- | --- | --- | ----------- | ---------- | ---------- | ----- | --- | -------- | --------- |
|             |           |      |     |     |     |     | nels. It is | noteworthy | to mention | that, | in  | general, | conveying |
Whileextensiveresearchcovershowrobotscaneffectively
|             |      |       |           |         |      |       | a single piece | of  | information | may | involve | simultaneously |     |
| ----------- | ---- | ----- | --------- | ------- | ---- | ----- | -------------- | --- | ----------- | --- | ------- | -------------- | --- |
| communicate | with | human | teammates | via MR, | only | a few |                |     |             |     |         |                |     |
multiplechannelstostrengthentheclarityofthecommunica-
works have explored how we can leverage this holographic tive act itself. For example, human-human communication
| medium         | for intuitive | and | straightforward |                  | human-to-robot |         |     |     |     |     |     |     |     |
| -------------- | ------------- | --- | --------------- | ---------------- | -------------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| communication, | particularly  |     | in LfD.         | In this context, |                | popular |     |     |     |     |     |     |     |
1https://github.com/TheEngineRoom-UniGe/RICO-MR/
| approachesatLfDrelyoncomputervisiontotransferdesired |     |     |     |     |     |     | tree/kt |     |     |     |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |

Human Wearing HMD
Device
ROS
Buffer
|     |     |     | Node |     | Start/Stop |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ---- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
KT
|     |     |     |     | Robot  |     |     |     |     | UE4 Mixed Reality |     |     |     |     |     |     |
| --- | --- | --- | --- | ------ | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | States |     |     |     |     | Application       |     |     |     |     |     |     |
External Storage
Inverse
|       |     |     |             |     | R O S        |     |     |     | Ki ne m a t | ics |            |     |       |     |     |
| ----- | --- | --- | ----------- | --- | ------------ | --- | --- | --- | ----------- | --- | ---------- | --- | ----- | --- | --- |
|       |     |     | R o b o t   |     |              |     |     |     | M o du l e  |     | U R D F    |     |       |     |     |
|       |     | Tra | j e c to ry |     | Int e rfa ce |     |     |     |             |     |            |     | Robot |     |     |
| Robot |     |     |             |     |              |     |     |     |             |     | P a rs e r |     |       |     |     |
Models
Vocal
Interface
Playback
Node
Fig. 2: Overview of the proposed architecture implementing holographic KT, extending the framework detailed in [34].
often combines verbal and gestural media to be meaningful where T(t ) describes the robot trajectory that is con-
gest
and unambiguous. Following this principle, and denoting veyedviagesturalguidanceduringtheintervalt spanning
gest
M ={m ,...,m }thesetofallpossiblecommunicative the KT session and is defined as
|                 | 1      | |M|    |           |      |        |         |     |     |     |     |     |     |     |     |     |
| --------------- | ------ | ------ | --------- | ---- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| media available | (e.g., | voice, | gestures, | gaze | and so | on), we |     |     |     |     |     |     |     |     |     |
provided the general formulation of a communicative act, T(t )={τ (t ),...,τ (t )} , (4)
|     |     |     |     |     |     |     |     |     | gest |     | gest,s |     | gest,e |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ------ | --- | ------ | --- | --- |
namely
|     |     |     |     |     |     |     | with | t gest,s | and | t gest,e | representing | the | temporal | endpoints |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | -------- | --- | -------- | ------------ | --- | -------- | --------- | --- |
N
|     |     |         | (cid:91) |        |     |     | of  | the taught | robot | trajectory. |     |     |     |     |     |
| --- | --- | ------- | -------- | ------ | --- | --- | --- | ---------- | ----- | ----------- | --- | --- | --- | --- | --- |
|     |     | C(I,t)= |          | C (I,t | ),  |     |     |            |       |             |     |     |     |     |     |
mi i (1) With this formalization in mind, we claim that KT can be
i=1
|     |     |     |     |     |     |     | translated |     | and framed |     | into the holographic |     | communication |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ---------- | --- | -------------------- | --- | ------------- | --- | --- |
where t represents the time interval associated with the space envisioned in [9] by letting users convey robots’
overall communication, whereas the intervals t i span the trajectories via gestural guidance on a virtual counterpart of
durationoftheindividualcomponentsofthecommunication the robot. As already mentioned, the unconstrained nature
act. of the MR space allows for such a form of KT while solely
Here, we leverage such formalization to frame KT inside relying on the built-in hand-tracking capabilities of the MR-
the holographic communication space developed for [9]. HMD device. Additionally, such decoupling between phys-
The first step requires identifying the relevant information ical and holographic layers could be particularly effective
exchanged during KT sessions. In particular, we argue that in production environments, as the operators could leverage
the act of KT implies teaching robots about their future thevirtualrobottoprogramorteachupcomingtasks,without
states, denoted as τ. Without loss of generality, such a halting the execution of real robotic chains.
notion of robot state includes the robot’s pose x(t) (that To further strengthen the communicative framework and
is, its position and orientation in the environment) and its ensure a more natural interaction, we postulate that adding
joint configuration q(t). Consequently, we can formalize the thevocalmediumwouldimproveusers’experience,enabling
robot’s state as them to control more detailed aspects of the KT session,
|     |     |                  |     |     |     |     | including |                 | the start      | and     | stop on   | the taught | robot   | trajectory, |      |
| --- | --- | ---------------- | --- | --- | --- | --- | --------- | --------------- | -------------- | ------- | --------- | ---------- | ------- | ----------- | ---- |
|     |     |                  |     |     |     |     | or        | the possibility |                | to open | and close | the        | robot’s | gripper     | for  |
|     |     | τ(t)={x(t),q(t)} |     |     | .   | (2) |           |                 |                |         |           |            |         |             |      |
|     |     |                  |     |     |     |     | teaching  |                 | pick-and-place |         | actions.  | According  |         | to such     | mod- |
This, in turn, provides us with a suitable representation elling, the holographic-based KT process is translated into a
of the set of information I which can be conveyed through communication act combining gestural and vocal interaction
KT, namely I = {τ(t)} . Having defined the set I, we and, as such, can be formalized as follows:
| observe that                                   | KT  | is achieved |     | by hand-guiding | the        | robot’s |     |            |     |     |           |       |      |     |     |
| ---------------------------------------------- | --- | ----------- | --- | --------------- | ---------- | ------- | --- | ---------- | --- | --- | --------- | ----- | ---- | --- | --- |
| wrist or end-effector.                         |     | According   |     | to our proposed | formalism, |         |     |            |     |     |           |       |      |     |     |
|                                                |     |             |     |                 |            |         |     | CKT(I,t)=C |     |     | (I,t      | ) ∪ C | (I,t | ).  | (5) |
|                                                |     |             |     |                 |            |         |     |            |     |     | gest gest |       | voc  | voc |     |
| thisactinvolvesagesture-mediatedcommunicationC |     |             |     |                 |            | that    |     |            |     |     |           |       |      |     |     |
gest
| enables users | to  | teach | robots | about their | future states | in  | a    |                |     |          |     |               |     |                |     |
| ------------- | --- | ----- | ------ | ----------- | ------------- | --- | ---- | -------------- | --- | -------- | --- | ------------- | --- | -------------- | --- |
|               |     |       |        |             |               |     | This | formalization, |     | combined |     | with equation |     | (3), describes |     |
simple way and can be described as follows: the building blocks of the communication act taking place
|     |     |     |     |     |     |     | during | the | proposed | holographic-based |     |     | KT process. |     | In the |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | -------- | ----------------- | --- | --- | ----------- | --- | ------ |
C (I,t )=T(t ), (3) following paragraph, these building blocks are translated
|     |     | gest | gest | gest |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ---- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Fig. 1, is spawned and superimposed on the robot’s wrist.
This sphere serves as a point of interaction between the
human and the robot. Using the hand-tracking capabilities
of the HMD, the human can directly manipulate the sphere
bycontrollingitsrotationandtranslationinspace.Therobot,
in turn, follows the sphere and aligns its wrist’s pose with
it by solving the Inverse Kinematics (IK). To this extent,
the Denavit-Hartenberg (DH) parameters necessary for the
computation of the IK are extracted from the robot model’s
URDF and fed to the IK Module, which continuously com-
putes the joint configuration needed to achieve the desired
pose of the wrist. Specifically, the IK computation occurs
with a rate of 30Hz. As such, by interacting with the
grey sphere and hand-guiding it, users can communicate
Fig. 3: An experimenter interacting with Baxter during futurerobot’sstatesand,consequently,teachtrajectoriesand
physical KT session. The operator drives the robot’s arm actions to the robot teammate.
through gestural interaction, teaching the sequence of pick- Consistently with the formalization given in Section III, a
and-place actions needed to complete the stacking task. voiceinterfaceisalsoactiveinsidetheMRapplication.Four
basiccommandsareavailable,ensuringthattheusercancon-
trol the start/stop of the KT session and the open/closed
into modular software components and integrated into a state of the robot’s gripper, offering the possibility to teach
preexisting MR-based architecture. more complex motions such as pick-and-place or handover
actions.
IV. SOFTWAREARCHITECTURE
B. Recording and Playback
The software components developed in the context of
this work constitute a modular extension of the open-source While the MR application provides the holographic in-
architecture, named Robot Intent Communication through terface to perform KT, recording and subsequent playback
MixedReality(RICO-MR),whichisintroducedanddetailed of the robot’s actions are respectively managed through
in[34].Thefeaturesdescribedinthisparagrapharepublicly Apache Kafka and the Robot Operating System (ROS) [35]
availableunderMITlicenceinaseparatebranchofthemain framework. On the one hand, we take advantage of Kafka,
RICO-MR repository. A link to the repository is included at anopen-source,high-performantdatastreamingplatform,for
the end of Section II.
input/outputdataexchangewiththeMRapplication.Kakfa
The proposed architecture exploits functionalities devel- provides numerous advantages for real-time data streaming
oped for RICO-MR to achieve the holographic KT envi- applications, including cloud integration and scalability, and
sioned in Section III. However, currently, the architecture it has been adopted for developing RICO-MR [34]. In this
allows holographic KT with fixed manipulators only. As context, we use Kafka to stream the robot’s states at a rate
such, we introduce a simplification in the formalization of 20Hz, beginning as soon as the user signals the start of
providedin(2),andwehereafterrefertothenotionofrobot the KT session through vocal command.
state to indicate its joint configuration q(t) only. On the other hand, two ROS nodes act respectively as
Buffer for the robot trajectory streamed through Kafka and
A. Mixed Reality Application Playbackoftherecordedmotion.TheBufferNodesubscribes
A MR Application, built with Unreal Engine 4.27 (UE4) to the Kafka topic to access the robot’s states, and it saves
and deployed on the embedded HMD device worn by the them to file for later execution. To this end, a ROS-Kafka
user,drivesthewholeholographicinterface.Ahand-attached Interface has been developed to convert incoming Kafka
menu enables the user to select robot models from a list messages into their equivalent ROS representation. Finally,
of predefined ones, making it possible to load and spawn the Playback Node forwards state commands to the internal
holographic robots in the environment. Aside from the pre- low-level controller of the robot at the same rate as the
loadedmodelsthatshipwiththecurrentarchitectureversion, recording to reproduce the desired motion.
the list of supported robots can be extended by uploading
V. EXPERIMENTALVALIDATION
relevant resources (i.e., URDF files) to a remote repository,
A. Hypotheses and Experimental Scenario
which can be customized in the application’s settings. As
such, it is possible to employ the proposed application to The experimental campaign carried out in this study aims
carry out KT with any URDF-compliant robot. to determine if our proposed holographic KT approach can
Upon selecting the robot model, users can spawn it in the act as a suitable alternative to standard, physical KT, both
environment using a QR code as a spatial anchor, taking in terms of demonstration capabilities and perceived user
advantage of Unreal’s marker detection capabilities. Along experience. To achieve our goal, we devised a human-robot
with the robot model, a grey holographic sphere, visible in interactivescenariotocomparetraditionalphysicalkinematic

100
75
50
25
0
1 2 3 4
]%[
ycneuqerF
(a) Cubes stacked in condition C1.
100
75
50
25
0
1 2 3 4
]%[
ycneuqerF
50
40
30
20
Tiago++ Baxter
(b) Cubes stacked in condition C2.
Fig. 4: Histograms depicting the number of cubes success-
fullystackedbytherobotsduringtheplaybackphase,inthe
two experimental conditions.
teaching (KT), where the operator manually controls the
robot’s kinematic chain, with our proposed holographic ap-
proach.Toensuremoregeneralizedresults,weconductedex-
periments using two different robots. In particular, we opted
for Baxter [36] from Rethink Robotics and Tiago++ [37]
fromPalRobotics,bothbeingwell-knownplatformsadopted
in relevant research studies [7], [9], [13], [25], [38] and
natively endowed with the necessary software and hardware
components to achieve physical KT. Similarly, the HMD
platform employed for rendering the holographic medium
is a Microsoft HoloLens 2, a popular MR headset offering
many features, including state-of-the-art hand tracking and
voice interaction.
From a formal point of view, to provide a thorough
comparison between physical KT and holographic KT, we
have come up with the following hypotheses, which have
been evaluated through preliminary user study:
H1 There is no observable difference between actions
taught through physical or holographic KT, namely
the two approaches provide equivalent communicative
power, leading to similar playback outcomes;
H2 No difference can be observed in terms of temporal
overhead when demonstrating actions through either
physical or holographic KT;
H3 No difference can be observed between the two ap-
proaches in terms of perceived UX during the demon-
stration process.
Regarding the interactive task employed to evaluate the
]s[
.ffiD
noitaruD
TK
Fig.5:Differentialdistributionsdepictingthetemporalover-
head introduced by the MR medium when performing KT
under C2.
twoKTalternatives,asimplestackingtaskhasbeendevised.
Specifically,thehumanshoulduseKTtoteachasequenceof
pick-and-place actions aimed at stacking four cubes on top
of each other according to a predefined order. Fig. 3 depicts
the experimental scenario, showing a user in the middle of
a physical KT session with the Baxter robot.
B. User Study
We carried out a within-subject experimental campaign
with K = 12 volunteers (9 males and 3 females), all aged
between 21-32 (Avg = 26.3, StdDev = 3.07) and having
limited or null experience with MR and HMD devices.
The subjects were divided into two groups. The first group
performed the experiment with Tiago++, while the second
group used Baxter. In both groups, subjects were asked
to perform the KT session in two different experimental
conditions, namely
C1 Without wearing the HMD and performing physical,
hand-guided KT.
C2 Wearing the HMD and performing holographic KT.
To avoid introducing unwanted biases, the starting ex-
perimental condition for each subject was randomized. Par-
ticipants were initially instructed on the stacking task and
assigned an arbitrary order for the cubes to be collected.
Then, they performed their first trial, in condition C1 or
C2. However, before beginning the experiment with HMD
on (i.e., condition C2), subjects were also briefly instructed
on how to interact with the HoloLens holographic menus
and interface. Then, once accustomed, they proceeded to
carry out their trial. Subsequently, each subject repeated the
experimentintheoppositecondition.Toachieveaconsistent
KTexperience,theholographicinterfaceinconditionC2also
includedfourvirtualcubesplacedcoherentlywiththeirreal-
world counterparts, as shown in Fig. 1. Such virtual cubes
were physics-enabled and behaved like the real ones, aiding
the participant in recording the holographic KT session. In
both cases, the voice interface was active for controlling the
start/stop of the KT session and the open/closed state of
therobot’sgripper.However,whileinconditionC2thevocal
interface was embedded into the MR application running on

the HoloLens 2, in condition C1 it was simulated thanks to holographic)ensureconsistentperformanceswhileexecuting
| a Wizard | of Oz | approach. |     |     |     |     |     | KT. |     |     |     |     |     |     |     |
| -------- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
After successfully completing each KT session, the play- Regarding the overall time needed to perform KT, we
| back phase | was | manually | triggered, |     | causing | the robot | to  |          |      |              |     |                 |     |      |        |
| ---------- | --- | -------- | ---------- | --- | ------- | --------- | --- | -------- | ---- | ------------ | --- | --------------- | --- | ---- | ------ |
|            |     |          |            |     |         |           |     | observed | that | in condition |     | C2 participants |     | were | always |
reproduce the taught action. This phase allowed us to rank slower because of their limited expertise with MR devices.
| the KT     | session | quantitatively |     | by combining |        | two     | distinct |            |          |                   |         |                |            |          |          |
| ---------- | ------- | -------------- | --- | ------------ | ------ | ------- | -------- | ---------- | -------- | ----------------- | ------- | -------------- | ---------- | -------- | -------- |
|            |         |                |     |              |        |         |          | As such,   | we chose | to                | perform | a differential |            | analysis | by       |
| variables, | useful  | in evaluating  |     | H1 and       | H2. On | the one | hand,    |            |          |                   |         |                |            |          |          |
|            |         |                |     |              |        |         |          | computing, | for      | each participant, |         | the            | difference | in       | terms of |
we counted the number of cubes successfully stacked by the timetakentocompletetheKTsessionbetweenconditionC2
robotduringplayback.Assuch,wewereabletoevaluatethe
|     |     |     |     |     |     |     |     | and C1. | These | results | are reported | in  | Fig. | 5. The | boxplots |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ----- | ------- | ------------ | --- | ---- | ------ | -------- |
communicativecapabilitiesofeachKTalternative,assessing highlight that, on average, holographic KT lasted, respec-
| how well   | the combination |               | of  | vocal | and gestural | interface |       |             |         |     |         |     |        |         |        |
| ---------- | --------------- | ------------- | --- | ----- | ------------ | --------- | ----- | ----------- | ------- | --- | ------- | --- | ------ | ------- | ------ |
|            |                 |               |     |       |              |           |       | tively, for | Tiago++ | and | Baxter, | 44  | and 32 | seconds | longer |
| translated | into the        | corresponding |     | robot | action.      | On the    | other |             |         |     |         |     |        |         |        |
thanthecorrespondingphysicalsessions.Comparedwiththe
hand,werecordedthedurationofeachdemonstrationsession averagetimesmeasuredtocompletethephysicalKTsessions
| and employed | such  | quantity | to        | compare | the       | two KT | tech-    |               |     |               |              |          |          |             |      |
| ------------ | ----- | -------- | --------- | ------- | --------- | ------ | -------- | ------------- | --- | ------------- | ------------ | -------- | -------- | ----------- | ---- |
|              |       |          |           |         |           |        |          | with the      | two | robots,       | the MR-based |          | approach | introduced, |      |
| niques in    | terms | of time  | necessary | to      | teach the | full   | stacking |               |     |               |              |          |          |             |      |
|              |       |          |           |         |           |        |          | respectively, | a   | mean temporal |              | overhead | of       | 37% and     | 33%. |
task.
|          |       |            |       |         |                  |     |     | Statistically, | this | result | is corroborated |                | by  | a one-tailed | t-      |
| -------- | ----- | ---------- | ----- | ------- | ---------------- | --- | --- | -------------- | ---- | ------ | --------------- | -------------- | --- | ------------ | ------- |
| Finally, | after | completing | their | trials, | each participant |     | was |                |      |        |                 |                |     |              |         |
|          |       |            |       |         |                  |     |     | test carried   | out  | on the | original        | distributions, |     | which        | yielded |
requiredtofillouttheUserExperienceQuestionnaire(UEQ) p-values < 0.05, therefore enabling us to reject the null
| [39], a | well-known | survey | useful | for | ranking | and | compar- |            |     |                   |     |          |       |             |     |
| ------- | ---------- | ------ | ------ | --- | ------- | --- | ------- | ---------- | --- | ----------------- | --- | -------- | ----- | ----------- | --- |
|         |            |        |        |     |         |     |         | hypothesis | for | H2. Nevertheless, |     | although | these | preliminary |     |
ing interactive products. In particular, such a questionnaire resultssuggestthattheholographicdemonstrationprocessis
allows grading the UX of a given product through six eval- slower than the physical one, we argue that the individuals’
| uation scales, | namely | attractiveness, |     |     | perspicuity, | efficiency, |     |                    |     |      |     |         |        |         |      |
| -------------- | ------ | --------------- | --- | --- | ------------ | ----------- | --- | ------------------ | --- | ---- | --- | ------- | ------ | ------- | ---- |
|                |        |                 |     |     |              |             |     | limited experience |     | with | MR  | devices | played | a major | role |
dependability, stimulation and novelty. In accordance with in increasing the time taken to teach the stacking task.
| hypothesis | H3, | to provide | a consistent |     | comparison |     | between |     |     |     |     |     |     |     |     |
| ---------- | --- | ---------- | ------------ | --- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
Consequently,furtherstudycouldbeundertakenwithamore
the two KT techniques, each participant compiled the UEQ expert population to corroborate or revisit this finding.
| twice, thus | evaluating |          | both physical |     | and holographic |     | KT  |              |     |        |       |                |     |            |     |
| ----------- | ---------- | -------- | ------------- | --- | --------------- | --- | --- | ------------ | --- | ------ | ----- | -------------- | --- | ---------- | --- |
|             |            |          |               |     |                 |     |     | Nonetheless, |     | Fig. 5 | shows | no significant |     | difference | be- |
| sessions    | from a     | UX point | of view.      |     |                 |     |     |              |     |        |       |                |     |            |     |
tweentemporaloverheadswhenusingonerobotortheother.
|     |     |     |     |     |     |     |     | This result | is also | confirmed |     | by a | one-tailed | t-test | on the |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ------- | --------- | --- | ---- | ---------- | ------ | ------ |
VI. RESULTS
|     |     |     |     |     |     |     |     | two differential |     | distributions, |     | which yielded |     | a p-value>0.2. |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | -------------- | --- | ------------- | --- | -------------- | --- |
We hereby report and discuss the results obtained from In other words, the overhead introduced by the MR medium
|                 |     |             |     |             |     |          |       | was consistent |     | among | the two | robots. |     |     |     |
| --------------- | --- | ----------- | --- | ----------- | --- | -------- | ----- | -------------- | --- | ----- | ------- | ------- | --- | --- | --- |
| our preliminary |     | user study. | In  | particular, | we  | observed | that, |                |     |       |         |         |     |     |     |
regardless of the robot, the two groups of subjects achieved Finally, Fig. 6 reports the results obtained from the UEQ
comparable results when teaching the stacking task in both questionnaires, grouped per evaluation scale and robot type.
experimental conditions. As such, Fig. 4 reports only the Here,scoresrangeintheinterval[−3,3],withpositivevalues
aggregatedresults,comparingconditionsC1andC2without
|     |     |     |     |     |     |     |     | indicating | features | that | users | appreciate | given | a particular |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | -------- | ---- | ----- | ---------- | ----- | ------------ | --- |
discerning the interactions occurred with Tiago++ or Baxter. interface. Specifically, Fig. 6c and 6b highlight that both
The histograms show the percentage of playback sessions KT approaches provided comparable results in terms of
where the robot successfully stacked a certain number of efficiency and perspicuity (i.e., how intuitive and pragmatic
cubes.Forexample,inbothexperimentalconditions,around the interface appeared to users), regardless of the robot
40% of the subjects achieved a flawless KT, resulting in the employed. Such results are corroborated by statistical analy-
robotsuccessfullystackingallfourcubeswhilereplayingthe sis performed through the Kruskal-Wallis test [42], a non-
taught trajectory. parametric ANOVA. The test yielded, for both scales, p-
ByobservingtheplotsofFig.4,itispossibletonotehow values > 0.05, indicating no significant difference between
physical and holographic KT yielded comparable results. the distributions. Again, this result could suggest that the
Keeping into account that such distributions could not be hypothesis H3 was correct, with both KT strategies leading
assumednormal,wechosetoperformastatisticalevaluation to similar perceived UX. It is also worth mentioning that
of the two conditions via a non-parametric test, namely holographic KT scored particularly well in terms of attrac-
through a one-tailed Wilcoxon signed-rank test [40]. The tiveness,stimulationandnovelty,suggestingthatparticipants
test provided a statistic W = 20, with p-value> 0.3. Such foundtheinteractionwiththeholographicenvironmentmore
result was compared with the critical value W obtained engaging and original compared to the physical one. The
c
from the literature [41] by fixing the population size K and only scale where holographic KT did a slightly worse job is
the significance level α=0.05. As such, the corresponding dependability, which measures how safe and predictable the
critical value was W c = 17. Observing the condition W > users perceive a given interface. In this case, physical KT
W , we could not reject the null hypothesis. This result may was still perceived as more predictable, particularly with the
c
indicatethatourinitialhypothesisH1wascorrect,suggesting robot Baxter, compared to the MR-based approach, which
that the two communicative interfaces (i.e., physical and nonetheless obtained positive scores with both robots.

3 3 3
2 2 2
1 1 1
0 0 0
−1 −1 −1
−2 −2 −2
−3 −3 −3
C1 C2 C1 C2 C1 C2 C1 C2 C1 C2 C1 C2
Tiago++ Baxter Tiago++ Baxter Tiago++ Baxter
(a) Attractiveness (b) Perspicuity (c) Efficiency
3 3 3
2 2 2
1 1 1
0 0 0
−1 −1 −1
−2 −2 −2
−3 −3 −3
C1 C2 C1 C2 C1 C2 C1 C2 C1 C2 C1 C2
Tiago++ Baxter Tiago++ Baxter Tiago++ Baxter
(d) Dependability (e) Stimulation (f) Novelty
Fig. 6: Measured UEQ scores on the six evaluation scales, grouped by robot type and experimental conditions. The median
value for each distribution is plotted as a red line.
VII. CONCLUSIONS human-robot interaction scenarios where the individual is
required to teach more complex tasks through holographic
In this paper, we proposed a novel communicative inter-
KT.
facebasedonMRtoachieveKTwithanyURDF-compatible
roboticmanipulatorplatform.Webuiltontopofourprevious
REFERENCES
works and expanded our communicative framework [9] to
account for holographic-based KT as a form of human- [1] L.Wang,S.Liu,H.Liu,andX.V.Wang,“Overviewofhuman-robot
collaboration in manufacturing,” in Proceedings of 5th International
to-robot communication. Then, we presented a software
Conference on the Industry 4.0 Model for Advanced Manufacturing
architecture translating the formalization into a practical (AMP2020),Belgrade,Serbia,June2020,pp.15–58.
MR application running on embedded HMD devices. We [2] R.Suzuki,A.Karim,T.Xia,H.Hedayati,andN.Marquardt,“Aug-
mentedrealityandrobotics:Asurveyandtaxonomyforar-enhanced
compared holographic KT with standard, physical KT in
human-robotinteractionandroboticinterfaces,”inProceedingsofthe
a preliminary user study involving multiple subjects and Conference on Human Factors in Computing Systems (CHI), New
two different robots. The results suggest that holographic Orleans,USA,Apr.2022,pp.1–33.
[3] B.Mutlu,F.Yamaoka,T.Kanda,H.Ishiguro,andN.Hagita,“Nonver-
KT behaves comparably to physical KT, achieving similar
balleakageinrobots:communicationofintentionsthroughseemingly
task-based performances and user experience. This finding unintentionalbehavior,”inProceedingsofthe4thACM/IEEEInterna-
suggests that the proposed methodology could be adopted tional Conference on Human-Robot Interaction (HRI), La Jolla CA,
USA,March2009,pp.69–76.
as a suitable alternative to physical KT in experimental
[4] E. Calisgan, A. Haddadi, H. M. Van der Loos, J. A. Alcazar, and
and manufacturing scenarios, decoupling the demonstration E. A. Croft, “Identifying nonverbal cues for automated human-robot
process and enabling operators to program robot tasks in turn-taking,”inProceedingsofthe21stIEEEInternationalSymposium
on Robot and Human Interactive Communication (RO-MAN), Paris,
the MR space, without halting the production flow of the
France,September2012,pp.418–423.
machine. [5] S. Ye, G. Neville, M. Schrum, M. Gombolay, S. Chernova, and
In future works, we will evaluate whether these findings A. Howard, “Human trust after robot mistakes: Study of the effects
of different forms of robot communication,” in Proceedings of the
can be generalized by conducting user studies on a wider
28thIEEEInternationalConferenceonRobotandHumanInteractive
population,consideringdifferentrobots,andmorestructured Communication(RO-MAN),NewDelhi,India,Oct.2019,pp.1–7.

[6] M.Ostanin,S.Mikhel,A.Evlampiev,V.Skvortsova,andA.Klimchik, physicallysharedmanufacturingtasks,”ACMTransactionsonHuman-
“Human-robot interaction for robotic manipulator programming in RobotInteraction(THRI),vol.11,no.3,pp.1–19,2022.
mixedreality,”inProceedingsofthe37thIEEEInternationalConfer- [24] T. Williams, M. Bussing, S. Cabrol, E. Boyle, and N. Tran, “Mixed
enceonRoboticsandAutomation(ICRA),May2020,pp.2805–2811. realitydeicticgestureformulti-modalrobotcommunication,”inPro-
ceedingsofthe14thACM/IEEEInternationalConferenceonHuman-
[7] E.Rosen,D.Whitney,E.Phillips,G.Chien,J.Tompkin,G.Konidaris,
andS.Tellex,“Communicatingandcontrollingrobotarmmotionin- RobotInteraction(HRI),Daegu,Korea,Mar.2019,pp.191–201.
tentthroughmixed-realityhead-mounteddisplays,”TheInternational [25] E.Rosen,D.Whitney,M.Fishman,D.Ullman,andS.Tellex,“Mixed
Journal of Robotics Research, vol. 38, no. 12-13, pp. 1513–1526, reality as a bidirectional communication interface for human-robot
interaction,”inProceedingsoftheIEEE/RSJInternationalConference
2019.
onIntelligentRobotsandSystems(IROS),LasVegas,USA,Oct.2020,
[8] R.Newbury,A.Cosgun,T.Crowley-Davis,W.P.Chan,T.Drummond,
| and E. | A. Croft, | “Visualizing |     | robot intent | for object | handovers | with | pp.11431–11438. |     |     |     |     |     |     |     |
| ------ | --------- | ------------ | --- | ------------ | ---------- | --------- | ---- | --------------- | --- | --- | --- | --- | --- | --- | --- |
augmented reality,” in Proceedings of the 31st IEEE International [26] Z.Qiu,T.Eiband,S.Li,andD.Lee,“Handpose-basedtasklearning
Conference on Robot and Human Interactive Communication (RO- from visual observations with semantic skill extraction,” in 2020
29thIEEEInternationalConferenceonRobotandHumanInteractive
MAN),Naples,Italy,Aug.2022,pp.1264–1270.
|                 |     |             |                    |     |        |         |         | Communication(RO-MAN). |        |                  | IEEE,2020,pp.596–603. |              |     |        |           |
| --------------- | --- | ----------- | ------------------ | --- | ------ | ------- | ------- | ---------------------- | ------ | ---------------- | --------------------- | ------------ | --- | ------ | --------- |
| [9] S. Maccio`, | A.  | Carf`ı, and | F. Mastrogiovanni, |     | “Mixed | reality | as com- |                        |        |                  |                       |              |     |        |           |
|                 |     |             |                    |     |        |         |         | [27] C. Eze            | and C. | Crick, “Learning |                       | by watching: | A   | review | of video- |
municationmediumforhuman-robotcollaboration,”inProceedingsof
the39thIEEEInternationalConferenceonRoboticsandAutomation based learning approaches for robot manipulation,” arXiv preprint
(ICRA),PhiladelphiaPA,USA,May2022,pp.2796–2802. arXiv:2402.07127,2024.
|     |     |     |     |     |     |     |     | [28] W. Si, | N. Wang, | and C. | Yang, | “A review | on  | manipulation | skill |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | ------ | ----- | --------- | --- | ------------ | ----- |
[10] H.Ravichandar,A.S.Polydoros,S.Chernova,andA.Billard,“Recent
acquisitionthroughteleoperation-basedlearningfromdemonstration,”
| advances | in robot | learning | from | demonstration,” |     | Annual | review of |     |     |     |     |     |     |     |     |
| -------- | -------- | -------- | ---- | --------------- | --- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
CognitiveComputationandSystems,vol.3,no.1,pp.1–16,2021.
control,robotics,andautonomoussystems,vol.3,pp.297–330,2020.
|     |     |     |     |     |     |     |     | [29] M. B. | Luebbers, | C. Brooks, | M.  | J. Kim, | D. Szafir, | and | B. Hayes, |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --------- | ---------- | --- | ------- | ---------- | --- | --------- |
[11] S.vanDelden,M.Umrysh,C.Rosario,andG.Hess,“Pick-and-place
applicationdevelopmentusingvoiceandvisualcommands,”Industrial “Augmentedrealityinterfaceforconstrainedlearningfromdemonstra-
|     |     |     |     |     |     |     |     | tion,” | in Proceedings | of the | 2nd | International | Workshop | on  | Virtual, |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | -------------- | ------ | --- | ------------- | -------- | --- | -------- |
Robot:AnInternationalJournal,vol.39,no.6,pp.592–600,2012.
|     |     |     |     |     |     |     |     | Augmented | and | Mixed Reality | for | HRI (VAM-HRI), |     | Daegu, | Korea, |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------------- | --- | -------------- | --- | ------ | ------ |
[12] A.Carfi,C.Motolese,B.Bruno,andF.Mastrogiovanni,“Onlinehu-
Mar.2019.
mangesturerecognitionusingrecurrentneuralnetworksandwearable
|           |                |     |        |           |               |     |           | [30] M. B. | Luebbers, | C. Brooks, | C. L.   | Mueller,        | D. Szafir, | and       | B. Hayes, |
| --------- | -------------- | --- | ------ | --------- | ------------- | --- | --------- | ---------- | --------- | ---------- | ------- | --------------- | ---------- | --------- | --------- |
| sensors,” | in Proceedings |     | of the | 27th IEEE | International |     | Symposium |            |           |            |         |                 |            |           |           |
|           |                |     |        |           |               |     |           | “Arc-lfd:  | Using     | augmented  | reality | for interactive |            | long-term | robot     |
onRobotandHumanInteractiveCommunication(RO-MAN),Nanjing skill maintenance via constrained learning from demonstration,” in
andTai’an,China,August2018,pp.188–195.
|                      |     |       |       |          |            |                 |     | Proceedings | of the | 38th IEEE | International |     | Conference | on  | Robotics |
| -------------------- | --- | ----- | ----- | -------- | ---------- | --------------- | --- | ----------- | ------ | --------- | ------------- | --- | ---------- | --- | -------- |
| [13] A. Bongiovanni, |     | A. De | Luca, | L. Gava, | L. Grassi, | M. Lagomarsino, |     |             |        |           |               |     |            |     |          |
andAutomation(ICRA),Xi’an,China,June2021,pp.3794–3800.
| M. Lapolla, | A.  | Marino, | P. Roncagliolo, |     | S. Maccio`, | A.  | Carf`ı, and |                                                                   |     |     |     |     |     |     |     |
| ----------- | --- | ------- | --------------- | --- | ----------- | --- | ----------- | ----------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|             |     |         |                 |     |             |     |             | [31] D.Puljiz,E.Sto¨hr,K.S.Riesterer,B.Hein,andT.Kro¨ger,“General |     |     |     |     |     |     |     |
F.Mastrogiovanni,“Gesturalandtouchscreeninteractionforhuman-
|     |     |     |     |     |     |     |     | hand guidance | framework |     | using | microsoft | hololens,” | in Proceedings |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --------- | --- | ----- | --------- | ---------- | -------------- | --- |
robot collaboration: a comparative study,” Proceedings of the 17th of the IEEE/RSJ International Conference on Intelligent Robots and
InternationalConferenceonIntelligentAutonomousSystems(IAS-17), Systems(IROS),Macau,China,Nov.2019,pp.5185–5190.
June2022.
|             |        |           |        |           |         |            |      | [32] A. R. | Pinto, J. | Kildal, and | E. Lazkano, |     | “Multimodal | mixed | reality |
| ----------- | ------ | --------- | ------ | --------- | ------- | ---------- | ---- | ---------- | --------- | ----------- | ----------- | --- | ----------- | ----- | ------- |
| [14] E. Cha | and M. | Mataric´, | “Using | nonverbal | signals | to request | help |            |           |             |             |     |             |       |         |
impactonahandguidingtaskwithaholographiccobot,”Multimodal
during human-robot collaboration,” in Proceedings of the IEEE/RSJ TechnologiesandInteraction,vol.4,no.4,p.78,2020.
International Conference on Intelligent Robots and Systems (IROS), [33] A. Rivera-Pinto, J. Kildal, and E. Lazkano, “Toward programming a
Daejeon,Korea,Otc.2016,pp.5070–5076. collaborativerobotbyinteractingwithitsdigitaltwininamixedreality
[15] S. Song and S. Yamada, “Bioluminescence-inspired human-robot in- environment,”InternationalJournalofHuman–ComputerInteraction,
teraction:designingexpressivelightsthataffecthuman’swillingnessto
pp.1–13,2023.
interactwitharobot,”inProceedingsof13thACM/IEEEInternational [34] S.Maccio`,M.Shaaban,A.Carf`ı,R.Zaccaria,andF.Mastrogiovanni,
ConferenceonHumanRobotInteraction(HRI),Chicago,USA,Mar. “RICO-MR: An open-source architecture for robot intent communi-
2018,pp.224–232. cationthroughmixedreality,”inProceedingsofthe32ndIEEEInter-
[16] A. Kalegina, G. Schroeder, A. Allchin, K. Berlin, and M. Cakmak, nationalConferenceonRobotandHumanInteractiveCommunication
“Characterizingthedesignspaceofrenderedrobotfaces,”inProceed- (RO-MAN),Busan,Korea,Aug.2023.
ings of 13th ACM/IEEE International Conference on Human Robot [35] M. Quigley, K. Conley, B. Gerkey, J. Faust, T. Foote, J. Leibs,
Interaction(HRI),Chicago,USA,Mar.2018,pp.96–104. R. Wheeler, and A. Y. Ng, “ROS: an open-source robot operating
[17] F.MohammadiAmin,M.Rezayati,H.W.vandeVenn,andH.Karim- system,” ICRA workshop on open source software, vol. 3, no. 3.2,
| pour,“Amixed-perceptionapproachforsafehuman–robotcollabora- |     |     |     |     |     |     |     | p.5,May2009. |     |     |     |     |     |     |     |
| ----------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
tioninindustrialautomation,”Sensors,vol.20,no.21,2020. [36] C. Fitzgerald, “Developing Baxter,” in Proceedings of the 5th IEEE
O¨. ConferenceonTechnologiesforPracticalRobotApplications(TePRA),
| [18] G. Michalos, |     | P. Karagiannis, | S.  | Makris, | Tokc¸alar, | and | G. Chrys- |     |     |     |     |     |     |     |     |
| ----------------- | --- | --------------- | --- | ------- | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
WoburnMA,USA,April2013,pp.1–6.
| solouris, | “Augmented | reality | (ar) | applications | for | supporting | human- |     |     |     |     |     |     |     |     |
| --------- | ---------- | ------- | ---- | ------------ | --- | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
robotinteractivecooperation,”ProcediaCIRP,vol.41,pp.370–375, [37] J.Pages,L.Marchionni,andF.Ferro,“Tiago:themodularrobotthat
2016. adaptstodifferentresearchneeds,”inInternationalworkshoponrobot
[19] S. M. Chacko and V. Kapila, “An augmented reality interface for modularity,IROS,vol.290,2016.
|     |     |     |     |     |     |     |     | [38] E.Ruffaldi,F.Brizzi,F.Tecchia,andS.Bacinelli,“Thirdpointofview |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
human-robotinteractioninunconstrainedenvironments,”inProceed-
|         |              |               |     |            |     |                |        | augmented | reality | for robot | intentions | visualization,” |     | in Proceedings |     |
| ------- | ------------ | ------------- | --- | ---------- | --- | -------------- | ------ | --------- | ------- | --------- | ---------- | --------------- | --- | -------------- | --- |
| ings of | the IEEE/RSJ | International |     | Conference |     | on Intelligent | Robots |           |         |           |            |                 |     |                |     |
andSystems(IROS),Macau,November2019,pp.3222–3228. of the 3rd International Conference on Augmented Reality, Virtual
[20] K.Chandan,V.Kudalkar,X.Li,andS.Zhang,“Arroch:Augmented RealityandComputerGraphics(AVR),Otranto,Italy,June2016,pp.
| reality | for robots | collaborating |     | with a | human,” | in Proceedings | of  | 471–478.         |     |                |     |        |           |               |     |
| ------- | ---------- | ------------- | --- | ------ | ------- | -------------- | --- | ---------------- | --- | -------------- | --- | ------ | --------- | ------------- | --- |
|         |            |               |     |        |         |                |     | [39] M. Schrepp, | J.  | Thomaschewski, |     | and A. | Hinderks, | “Construction | of  |
the38thIEEEInternationalConferenceonRoboticsandAutomation
|            |                                        |           |         |       |       |           |           | a benchmark | for        | the user    | experience | questionnaire |                | (UEQ),”       | Interna- |
| ---------- | -------------------------------------- | --------- | ------- | ----- | ----- | --------- | --------- | ----------- | ---------- | ----------- | ---------- | ------------- | -------------- | ------------- | -------- |
| (ICRA).    | Xi’an,China:IEEE,May2021,pp.3787–3793. |           |         |       |       |           |           |             |            |             |            |               |                |               |          |
|            |                                        |           |         |       |       |           |           | tional      | Journal of | Interactive | Multimedia |               | and Artificial | Intelligence, |          |
| [21] C. P. | Quintero,                              | S. Li, M. | K. Pan, | W. P. | Chan, | H. M. Van | der Loos, |             |            |             |            |               |                |               |          |
vol.4,no.4,pp.40–44,2017.
and E. Croft, “Robot programming through augmented trajectories F.Wilcoxon,“Individualcomparisonsbyrankingmethods,”inBreak-
| in augmented |     | reality,” | in Proceedings | of  | the IEEE/RSJ | International |     | [40]                  |     |                           |     |     |     |     |     |
| ------------ | --- | --------- | -------------- | --- | ------------ | ------------- | --- | --------------------- | --- | ------------------------- | --- | --- | --- | --- | --- |
|              |     |           |                |     |              |               |     | throughsinStatistics. |     | Springer,1992,pp.196–202. |     |     |     |     |     |
ConferenceonIntelligentRobotsandSystems(IROS),Madrid,Spain,
|     |     |     |     |     |     |     |     | [41] ——,“Probabilitytablesforindividualcomparisonsbyrankingmeth- |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
October2018,pp.1838–1844.
ods,”Biometrics,vol.3,no.3,pp.119–122,1947.
[22] X.V.Wang,L.Wang,M.Lei,andY.Zhao,“Closed-loopaugmented
|     |     |     |     |     |     |     |     | [42] W. H. | Kruskal | and W. | A. Wallis, | “Use | of ranks | in one-criterion |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | ------ | ---------- | ---- | -------- | ---------------- | --- |
reality towards accurate human-robot collaboration,” CIRP Annals, variance analysis,” Journal of the American statistical Association,
vol.69,no.1,pp.425–428,2020.
vol.47,no.260,pp.583–621,1952.
| [23] W. P. | Chan, G. | Hanks,         | M. Sakr, | H. Zhang,  | T.  | Zuo, H.      | M. Van der |     |     |     |     |     |     |     |     |
| ---------- | -------- | -------------- | -------- | ---------- | --- | ------------ | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
| Loos,      | and E.   | Croft, “Design | and      | evaluation | of  | an augmented | reality    |     |     |     |     |     |     |     |     |
head-mounteddisplayinterfaceforhumanrobotteamscollaboratingin