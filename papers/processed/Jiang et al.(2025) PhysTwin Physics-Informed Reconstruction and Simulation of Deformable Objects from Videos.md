|     | PhysTwin: |     | Physics-Informed |            |     | Reconstruction |      | and    | Simulation |     | of  |     |
| --- | --------- | --- | ---------------- | ---------- | --- | -------------- | ---- | ------ | ---------- | --- | --- | --- |
|     |           |     |                  | Deformable |     | Objects        | from | Videos |            |     |     |     |
HanxiaoJiang1,2 Hao-YuHsu2 KaifengZhang1 Hsin-NiYu2 ShenlongWang2 YunzhuLi1
|     |     |     | 1ColumbiaUniversity |     |     | 2UniversityofIllinoisUrbana-Champaign |     |     |     |     |     |     |
| --- | --- | --- | ------------------- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --- |
Teleoperation
5202 raM 32  ]VC.sc[  1v37971.3052:viXra
Digital Twin
Overlay
Model-Based Robot Planning
Right Hand
|     |     |     |     | Left Hand |     | Real-Time |     |     |     |     |     |     |
| --- | --- | --- | --- | --------- | --- | --------- | --- | --- | --- | --- | --- | --- |
Physical Simulation
& Rendering
t
| Input Video |     | PhysTwin |     |     |     | Simulation |     |     |     | Applications in Robotics |     |     |
| ----------- | --- | -------- | --- | --- | --- | ---------- | --- | --- | --- | ------------------------ | --- | --- |
Figure1.PhysTwintakessparsevideos(threecameraviews)ofdeformableobjectsunderinteractionasinputandreconstructsasimulatable
digitaltwinwithcompletegeometry,high-fidelityappearance,andaccuratephysicalparameters.Thisenablesmultipleapplications,suchas
real-timeinteractivesimulationusingkeyboardsandroboticteleoperationdevices,aswellasmodel-basedrobotplanning.
|     |     | Abstract |     |     |     |     | 1.Introduction |     |     |     |     |     |
| --- | --- | -------- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- |
Theconstructionofinteractivedigitaltwinsisessentialfor
Creatingaphysicaldigitaltwinofareal-worldobjecthas
|         |           |              |         |           |     |         | modeling | the world and | simulating | future | states, | with ap- |
| ------- | --------- | ------------ | ------- | --------- | --- | ------- | -------- | ------------- | ---------- | ------ | ------- | -------- |
| immense | potential | in robotics, | content | creation, |     | and XR. |          |               |            |        |         |          |
plicationsinvirtualreality,augmentedreality,androbotic
| In this paper, |         | we present | PhysTwin, | a novel    | framework  |        |               |              |         |               |         |              |
| -------------- | ------- | ---------- | --------- | ---------- | ---------- | ------ | ------------- | ------------ | ------- | ------------- | ------- | ------------ |
|                |         |            |           |            |            |        | manipulation. | A physically |         | realistic     | digital | twin (PhysT- |
| that uses      | sparse  | videos of  | dynamic   | objects    | under      | inter- |               |              |         |               |         |              |
|                |         |            |           |            |            |        | win) should   | accurately   | capture | the geometry, |         | appearance,  |
| action to      | produce | a photo-   | and       | physically | realistic, | real-  |               |              |         |               |         |              |
andphysicalpropertiesofanobject,allowingsimulations
| time interactive |             | virtual replica. |                    | Our approach | centers     | on  |                                             |     |     |     |     |          |
| ---------------- | ----------- | ---------------- | ------------------ | ------------ | ----------- | --- | ------------------------------------------- | --- | --- | --- | --- | -------- |
|                  |             |                  |                    |              |             |     | thatcloselymatchobservationsintherealworld. |     |     |     |     | However, |
| two key          | components: | (1)              | a physics-informed |              | representa- |     |                                             |     |     |     |     |          |
constructingsucharepresentationfromsparseobservations
tionthatcombinesspring-massmodelsforrealisticphysi-
remainsasignificantchallenge.
calsimulation,generativeshapemodelsforgeometry,and
Thecreationofdigitaltwinsfordeformableobjectshas
Gaussiansplatsforrendering;and(2)anovelmulti-stage,
|     |     |     |     |     |     |     | long been | a challenging | topic | in the | vision | community. |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------------- | ----- | ------ | ------ | ---------- |
optimization-basedinversemodelingframeworkthatrecon-
Whiledynamic3Dmethods(e.g.,dynamicNeRFs[2,5,8,
| structs complete |     | geometry, | infers | dense physical |     | proper- |     |     |     |     |     |     |
| ---------------- | --- | --------- | ------ | -------------- | --- | ------- | --- | --- | --- | --- | --- | --- |
13,14,17,27,29–31,39–41,43,55,56,58,61],dynamic
| ties,andreplicatesrealisticappearancefromvideos. |     |     |     |     |     | Our |     |     |     |     |     |     |
| ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
3DGaussians[10,20,24,33,34,59,65,66,68])captureob-
| method integrates |     | an inverse | physics | framework |     | with vi- |     |     |     |     |     |     |
| ----------------- | --- | ---------- | ------- | --------- | --- | -------- | --- | --- | --- | --- | --- | --- |
servedmotion,appearance,andgeometryfromvideos,they
sualperceptioncues,enablinghigh-fidelityreconstruction
omittheunderlyingphysicsandarethusunsuitableforsimu-
| evenfrompartial,occluded,andlimitedviewpoints. |     |     |     |     |     | PhysT- |                                     |     |     |     |                    |     |
| ---------------------------------------------- | --- | --- | --- | --- | --- | ------ | ----------------------------------- | --- | --- | --- | ------------------ | --- |
|                                                |     |     |     |     |     |        | latingoutcomesinunseeninteractions. |     |     |     | Whilerecentneural- |     |
winsupportsmodelingvariousdeformableobjects,includ-
basedmodels[4,11,28,32,36,42,49,51,52,60,64,69]
| ing ropes, | stuffed | animals, | cloth, | and delivery | packages. |     |     |     |     |     |     |     |
| ---------- | ------- | -------- | ------ | ------------ | --------- | --- | --- | --- | --- | --- | --- | --- |
learnintuitivephysicsmodelsfromvideos,theyrequirelarge
| Experiments | show | that PhysTwin |     | outperforms | competing |     |         |             |                |     |             |            |
| ----------- | ---- | ------------- | --- | ----------- | --------- | --- | ------- | ----------- | -------------- | --- | ----------- | ---------- |
|             |      |               |     |             |           |     | amounts | of data and | remain limited |     | to specific | objects or |
methodsinreconstruction,rendering,futureprediction,and
motions,whereasphysics-drivenapproaches[9,12,27,44,
| simulation | under | novel interactions. |     | We  | further | demon- |     |     |     |     |     |     |
| ---------- | ----- | ------------------- | --- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- |
63,71,72]oftenrelyonpre-scannedshapesordenseobser-
| strate its      | applications | in      | interactive | real-time | simulation |       |                                 |     |     |               |     |            |
| --------------- | ------------ | ------- | ----------- | --------- | ---------- | ----- | ------------------------------- | --- | --- | ------------- | --- | ---------- |
|                 |              |         |             |           |            |       | vationstomitigateill-posedness. |     |     | Additionally, |     | itrequires |
| and model-based |              | robotic | motion      | planning. | Project    | Page: |                                 |     |     |               |     |            |
denseviewpointcoverageandsupportsonlylimitedmotion
https://jianghanxiao.github.io/phystwin-web/

types,makingitunsuitableforgeneraldynamicsmodeling. ondynamicscenesbyoptimizingadeformablefield. Simi-
In this work, we aim to build an interactive PhysTwin larly,Deformable3D-GS[66]optimizesadeformationfield
fromsparse-viewpointRGB-Dvideosequences,capturing ofeachGaussiankernel.Dynamic3D-GS[34]optimizesthe
object geometry, non-rigid dynamic physics, and appear- motionofGaussiankernelsforeachframetocapturescene
ance for realistic physical simulation and rendering. We dynamics. 4D-GS [59] modulates 3D Gaussians with 4D
modeldeformableobjectdynamicswithaspring-mass-based neuralvoxelsfordynamicmulti-viewsynthesis. Although
representation, enabling efficient physical simulation and thesemethodsachievehigh-fidelityresultsindynamicmulti-
handling a wide range of common objects, such as ropes, viewsynthesis,theyprimarilyfocusonreconstructingscene
stuffed animals, cloth, and delivery packages. To address appearanceandgeometrywithoutcapturingreal-worlddy-
the challenges posed by sparse observations, we leverage namics,limitingtheirabilitytosupportaction-conditioned
shapepriorsandmotionestimationfromadvanced3Dgener- futurepredictionsandinteractivesimulations.
ativemodels[62]andvisionfoundationmodels[23,46,48]
|     |     |     |     |     | Physics-BasedSimulationofDeformableObjects. |     |     |     |     | An- |
| --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- |
to estimate the topology, geometry, and physical parame- otherlineofworkincorporatesphysicalsimulatorstoper-
| ters of our physical | representation.     | Since some  | physical |      |                 |                |         |         |                     |             |
| -------------------- | ------------------- | ----------- | -------- | ---- | --------------- | -------------- | ------- | ------- | ------------------- | ----------- |
|                      |                     |             |          |      | form system     | identification |         | of      | physical parameters | during      |
| parameters (such     | as topology-related | properties) | are      | non- |                 |                |         |         |                     |             |
|                      |                     |             |          |      | reconstruction. |                | Earlier | methods | relied on           | pre-scanned |
differentiableandoptimizingthemefficientlyisnon-trivial, static objects and required clean point cloud observa-
wedesignahierarchicalsparse-to-denseoptimizationstrat-
|                    |                       |              |     |      | tions[9,15,19,21,35,44,47,57]. |     |     |     | Mostrecentapproaches |     |
| ------------------ | --------------------- | ------------ | --- | ---- | ------------------------------ | --- | --- | --- | -------------------- | --- |
| egy. This strategy | integrates zero-order | optimization |     | [18] |                                |     |     |     |                      |     |
builduponSDF[45],NeRF[3,12,27]orGaussianSplat-
fornon-differentiabletopologyandsparsephysicalparam-
ting[22,63,71,72]tosupportmoreflexiblephysicaldigital
| eters (e.g., collision | parameters | and homogeneous |     | spring |                      |     |         |     |                |              |
| ---------------------- | ---------- | --------------- | --- | ------ | -------------------- | --- | ------- | --- | -------------- | ------------ |
|                        |            |                 |     |        | twin reconstruction. |     | Several |     | works [12, 22, | 63] manually |
stiffness),whileemployingfirst-ordergradient-basedopti- specifyphysicsparameters,resultinginamismatchbetween
mizationtorefinedensespringstiffnessandfurtheroptimize
|                      |                        |     |         |     | the simulation | and | real-world |     | video observations. | Other |
| -------------------- | ---------------------- | --- | ------- | --- | -------------- | --- | ---------- | --- | ------------------- | ----- |
| collisionparameters. | Forappearancemodeling, |     | weadopt |     |                |     |            |     |                     |       |
works[3,27,45,71,72]attempttoestimatephysicalparam-
| a Gaussian blending | strategy, initializing | static | Gaussians |     |                  |     |                                   |     |     |     |
| ------------------- | ---------------------- | ------ | --------- | --- | ---------------- | --- | --------------------------------- | --- | --- | --- |
|                     |                        |        |           |     | etersfromvideos. |     | However,theyareoftenconstrainedto |     |     |     |
fromsparseobservationsinthefirstframeusingshapepri-
syntheticdata,limitedmotion,ortheneedfordenseview-
orsanddeformingthemwithalinearblendingalgorithmto points to accurately reconstruct static geometry, limiting
generaterealisticdynamicappearances.
|     |     |     |     |     | theirpracticalapplicability. |     |     | Theclosestrelatedworktoours |     |     |
| --- | --- | --- | --- | --- | ---------------------------- | --- | --- | --------------------------- | --- | --- |
Ourinversemodelingframeworkeffectivelyconstructsin-
isSpring-Gaus[72],whichalsoutilizesa3DSpring-Mass
teractivePhysTwinfromvideosofobjectsunderinteraction.
|     |     |     |     |     | model for | learning | from | videos. | However, | their physical |
| --- | --- | --- | --- | --- | --------- | -------- | ---- | ------- | -------- | -------------- |
Wecreateareal-worlddeformableobjectinteractiondataset
modelisoverlyregularizedandviolatesreal-worldphysics,
andevaluateourmethodonthreekeytasks: reconstruction lackingmomentumconservationandrealisticgravity. More-
| and resimulation, | future prediction, | and generalization |     | to  |     |     |     |     |     |     |
| ----------------- | ------------------ | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
over,Spring-Gausrequiresdenseviewpointcoveragetore-
| unseeninteractions. | Bothquantitativeandqualitativeresults |     |     |     |     |     |     |     |     |     |
| ------------------- | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
constructthefullgeometryattheinitialstate,whichisim-
demonstrate that our reconstructed PhysTwin aligns accu- practicalinmanyreal-worldsettings. Themotionsarealso
ratelywithreal-worldobservations,achievesprecisefuture
limitedtotabletopcollisionsandlackactioninputs,making
predictions,andgeneratesrealisticsimulationsunderdiverse Spring-Gaus unsuitable as a general dynamics model for
| unseeninteractions. | Furthermore,thehighcomputationalef- |     |     |     |     |     |     |     |     |     |
| ------------------- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
downstreamapplications.
ficiencyofourphysicssimulatorenablesreal-timedynamics
|     |     |     |     |     | Learning-Based |     | Simulation |     | of Deformable | Objects. |
| --- | --- | --- | --- | --- | -------------- | --- | ---------- | --- | ------------- | -------- |
andrenderingofourconstructedPhysTwin,facilitatingmul-
Analyticallymodelingthedynamicsofdeformableobjects
tipleapplications,includingreal-timeinteractivesimulation
andmodel-basedroboticmotionplanning. is challenging due to the high complexity of the state
|     |     |     |     |     | space and | the variability |     | of  | physical properties. | Recent |
| --- | --- | --- | --- | --- | --------- | --------------- | --- | --- | -------------------- | ------ |
works[4,11,36,60,64]havechosentouseneuralnetwork-
2.RelatedWorks
|     |     |     |     |     | based simulators |     | to model | object | dynamics. | Specifically, |
| --- | --- | --- | --- | --- | ---------------- | --- | -------- | ------ | --------- | ------------- |
Dynamic Scene Reconstruction. Dynamic scene recon- graph-basednetworkseffectivelylearnthedynamicsofvari-
structionaimstorecovertheunderlyingrepresentationof oustypesofobjectssuchasplasticine[51,52],cloth[32,42],
dynamicscenesfrominputslikedepthscans[6,26],RGBD fluid[28,49],andstuffedanimals[69]. GS-Dynamics[69]
videos[38],ormonocularormulti-viewvideos[1,5,24,31, attemptedtolearnobjectdynamicsdirectlyfromreal-world
34, 39, 40, 43, 56, 58, 61, 67, 68]. Recent advancements videosusingtrackingandappearancepriorsfromDynamic
in dynamic scene modeling have involved the adaptation Gaussians[34],andgeneralizedwelltounseenactions.How-
ofnovelscenerepresentations,includingNeuralRadiance ever,theselearnedmodelsneedextensivetrainingsamples
Fields(NeRF)[2,5,8,13,14,16,17,27,29,30,30,31,39– andareoftenlimitedtospecificenvironmentswithlimited
41,43,55,56,58,61]and3DGaussiansplats[10,20,24,33, motionranges. Incontrast, ourmethodrequiresonlyone
34,59,65,66,68]. D-NeRF[43]extendsacanonicalNeRF interactiontrialwhileachievingabroaderrangeofmotions.

Observation … t<latexit sha1_base64="kvnpK4lZp9Z/I3K0EOxbh4N68Y8=">AAAB6nicbVBNS8NAEJ34WetX1aOXxSJ4sSQi1WPRi8eK9gPaUDbbTbt0swm7E6GE/gQvHhTx6i/y5r9x2+agrQ8GHu/NMDMvSKQw6Lrfzsrq2vrGZmGruL2zu7dfOjhsmjjVjDdYLGPdDqjhUijeQIGStxPNaRRI3gpGt1O/9cS1EbF6xHHC/YgOlAgFo2ilBzz3eqWyW3FnIMvEy0kZctR7pa9uP2ZpxBUySY3peG6CfkY1Cib5pNhNDU8oG9EB71iqaMSNn81OnZBTq/RJGGtbCslM/T2R0ciYcRTYzoji0Cx6U/E/r5NieO1nQiUpcsXmi8JUEozJ9G/SF5ozlGNLKNPC3krYkGrK0KZTtCF4iy8vk+ZFxatWqveX5dpNHkcBjuEEzsCDK6jBHdShAQwG8Ayv8OZI58V5dz7mrStOPnMEf+B8/gC9IY11</latexit> 1 t<latexit sha1_base64="QhaWXmnGoOlgmZu6DZZxvnONEzE=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KolI9Vj04rEF+wFtKJvtpl272YTdiVBCf4EXD4p49Sd589+4bXPQ1gcDj/dmmJkXJFIYdN1vZ219Y3Nru7BT3N3bPzgsHR23TJxqxpsslrHuBNRwKRRvokDJO4nmNAokbwfju5nffuLaiFg94CThfkSHSoSCUbRSA/ulsltx5yCrxMtJGXLU+6Wv3iBmacQVMkmN6Xpugn5GNQom+bTYSw1PKBvTIe9aqmjEjZ/ND52Sc6sMSBhrWwrJXP09kdHImEkU2M6I4sgsezPxP6+bYnjjZ0IlKXLFFovCVBKMyexrMhCaM5QTSyjTwt5K2IhqytBmU7QheMsvr5LWZcWrVqqNq3LtNo+jAKdwBhfgwTXU4B7q0AQGHJ7hFd6cR+fFeXc+Fq1rTj5zAn/gfP4A47uNAw==</latexit> t<latexit sha1_base64="seHr22W9wgx4F2HIx+USZQdIUf0=">AAAB6nicbVBNS8NAEJ34WetX1aOXxSIIQklEqseiF48V7Qe0oWy2m3bpZhN2J0IJ/QlePCji1V/kzX/jts1BWx8MPN6bYWZekEhh0HW/nZXVtfWNzcJWcXtnd2+/dHDYNHGqGW+wWMa6HVDDpVC8gQIlbyea0yiQvBWMbqd+64lrI2L1iOOE+xEdKBEKRtFKD3ju9Uplt+LOQJaJl5My5Kj3Sl/dfszSiCtkkhrT8dwE/YxqFEzySbGbGp5QNqID3rFU0YgbP5udOiGnVumTMNa2FJKZ+nsio5Ex4yiwnRHFoVn0puJ/XifF8NrPhEpS5IrNF4WpJBiT6d+kLzRnKMeWUKaFvZWwIdWUoU2naEPwFl9eJs2LiletVO8vy7WbPI4CHMMJnIEHV1CDO6hDAxgM4Ble4c2Rzovz7nzMW1ecfOYI/sD5/AG6F41z</latexit> +1 …
 
PseudoTrack GTObservation
Reconstruction
Tracking
PhysTwin C<latexit sha1_base64="ggB6U2di6KWSE9LXieRzAyxVonQ=">AAACInicbVDLSgNBEJz1bXxFPXoZDIIghF0RHwdBzMWjgjGBJITZSScOzmOZ6RXDkm/x4q948aCoJ8GPcRKDRGPBQFFVTU9XnEjhMAw/gonJqemZ2bn53MLi0vJKfnXtypnUcihzI42txsyBFBrKKFBCNbHAVCyhEt+U+n7lFqwTRl9iN4GGYh0t2oIz9FIzf1Six7TUrCPcYdYBowBtt0d3fjRl+sFRxYJuge0184WwGA5Ax0k0JAUyxHkz/1ZvGZ4q0Mglc64WhQk2MmZRcAm9XD11kDB+wzpQ81QzBa6RDU7s0S2vtGjbWP800oE6OpEx5VxXxT6pGF67v15f/M+rpdg+bGRCJymC5t+L2qmkaGi/L9oSFjjKrieMW+H/Svk1s4yjbzXnS4j+njxOrnaL0X5x/2KvcHI6rGOObJBNsk0ickBOyBk5J2XCyT15JM/kJXgInoLX4P07OhEMZ9bJLwSfX08FpDk=</latexit> = C +C +C
Stiffness geometry motion render
Simulation
Contact Rendering
*
Optimization
Topology Geometry
*ControlPoint Gaussians Simulated Geometry and Motion Gaussian Rendering
Figure2.OverviewofOurPhysTwinFramework.WepresentanoverviewofourPhysTwinframework,wherethecorerepresentation
includesgeometry,topology,physicalparameters(associatedwithspringsandcontacts),andGaussiankernels. TooptimizePhysTwin,
weminimizetherenderinglossandthediscrepancybetweensimulatedandobservedgeometry/motion.Therenderinglossoptimizesthe
Gaussiankernels,whilethegeometryandmotionlossesrefinetheoverallgeometry,topology,andphysicalparametersinPhysTwin.
(cid:16) (cid:17)
3.Preliminary: Spring-MassModel foralli,vt+1 =δ vt+∆t Fi , xt+1 =xt+∆tvt+1,
i i mi i i i
where X represents the system state at time t, and δ rep-
Spring-mass models are widely used for simulating de- t
resents the drag damping. In this formulation, α denotes
formableobjectsduetotheirsimplicityandcomputational
allphysicalparametersofthespring-massmodel,including
efficiency. A deformable object is represented as a set of
springstiffness,collisionparameters,anddamping. Italso
spring-connected mass nodes, forming a graph structure
encompassestheparametersrelatedtothecontrolinteraction.
= ( , ),where isthesetofmasspointsand isthe
G set of V spr E ings. Eac V h mass node i has a position x E R3 0 representsthe“canonical”geometryandtopologyforthe
i G
and velocity v R3, which evolve over time acco ∈ rding spring-masssystem1,anda t representstheactionattimet.
i
∈
toNewtoniandynamics. Springsareconstructedbetween
4.Method
neighboringnodesbasedonapredefinedtopology,defining
theelasticstructureoftheobject.
Inthissection,weformulatetheconstructionofPhysTwin
Theforceonnodeiistheresultofthecombinedeffects
asanoptimizationproblem. Wethenpresentourtwo-stage
ofadjacentnodesconnectedbysprings:
strategy,wherethefirststageaddressesthephysics-related
(cid:88) optimization,followedbytheappearance-basedoptimiza-
F = Fspring+Fdashpot+Fext, (1)
i i,j i,j i tioninthesecondstage. Finally,wedemonstratethecapabil-
(i,j)∈E ityofourframeworktoperformreal-timesimulationusing
theconstructedPhysTwin.
wherethespringforceanddashpotdampingforcebetween
nodes i and j are given by Fs i p ,j ring = k ij ( ∥ x j − x i ∥ − 4.1.ProblemFormulation
l ) xj−xi andFdashpot = γ(v v ),respectively. Here,
ij ∥xj−xi∥ i,j − i − j GiventhreeRGBDvideosofadeformableobjectunderin-
k is the spring stiffness, l is the rest length, and γ is
ij ij teraction,ourobjectiveistoconstructaPhysTwinmodelthat
the dashpot damping coefficient. The external force Fext
i capturesthegeometry,appearance,andphysicalparameters
accountsforfactorssuchasgravity,collisions,anduserin-
of the object over time. At each time frame t, we denote
teractions. Thespringforcerestoresthesystemtoitsrest
theRGBDobservationsfromthei-thcameraasO ,where
t,i
shape, while the dashpot damping dissipates energy, pre-
O=(I,D)representstheRGBimageIanddepthmapD.
ventingoscillations. Forcollisions,weuseimpulse-based
Thegoalofouroptimizationproblemistominimizethe
collisionhandlingwhentwomasspointsareveryclose,in- discrepancybetweenthepredictedobservationOˆ andthe
t,i
cluding collisions between the object and the collider, as
actualobservationO .Thepredictedobservationisderived
t,i
wellasbetweentwoobjectpoints. byprojectingandrenderingthepredictedstateXˆ ontoim-
t
Thespring-massmodelupdatesthesystemstatewithady-
agesthroughafunctiong ,whereθencodestheappearance
θ
namicmodelX =f (X ,a )byapplyingexplicitEu-
t+1 α,G0 t t
lerintegrationtobothvelocityandposition. Moreformally, 1Inpractice,weusethefirst-frameobjectstateasthecanonicalstate.

oftheobjectsrepresentedbyGaussiansplats. The3Dstate (2)jointoptimizationofboththediscretetopologyandphysi-
Xˆ evolvesovertimeaccordingtotheSpring-Massmodel, calparameters;and(3)discontinuitiesinthedynamicmodel,
t
which captures the deformable object’s dynamics and up- alongwiththelongtimehorizonanddenseparameterspace,
datesthestateusingtheexplicitEulerintegrationmethod. whichmakecontinuousoptimizationdifficult. Toaddress
Theoptimizationproblemisformulatedas: thesechallenges,wehandlethegeometryandotherparam-
|     |     |     |     |     |     |     | eters separately. |     | Specifically, | we first | leverage | generative |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | ------------- | -------- | -------- | ---------- |
(cid:88)
min C(Oˆ ,O ) shape initialization to obtain the full geometry, then em-
t,i t,i
α,G0,θ
t,i (2) ployourtwo-stagesparse-to-denseoptimizationtorefinethe
|      | Oˆ  | (Xˆ  | Xˆ  |     | (Xˆ |       | remainingparameters. |     |              |        |         |               |
| ---- | --- | ---- | --- | --- | --- | ----- | -------------------- | --- | ------------ | ------ | ------- | ------------- |
| s.t. | =g  | ,i), |     | =f  |     | ,a ), |                      |     |              |        |         |               |
|      | t,i | θ t  |     | t+1 | α,G | t t   |                      |     |              |        |         |               |
|      |     |      |     |     |     |       | Generative           |     | Shape Prior. | Due to | partial | observations, |
whereα, ,θcapturesthephysics,geometry,topologyand recoveringthefullgeometryischallenging. Weleveragea
0
|     | G   |     |     |     |     |     | shapepriorfromtheimage-to-3DgenerativemodelTREL- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- |
appearanceparameters(Sec.3);thecostfunctionquantifies
thedifferencebetweenthepredictedobservationOˆ andthe LIS[62]togenerateacompletemeshconditionedonasin-
t,i
actualobservationO . Thiscostfunctionisdecomposed gle RGB observation of the masked object. To improve
t,i
intothreecomponents:C =C +C +C , meshquality,theinputtoTRELLISisfirstenhancedusing
|     |     |     | geometry |     | motion | render |     |     |     |     |     |     |
| --- | --- | --- | -------- | --- | ------ | ------ | --- | --- | --- | --- | --- | --- |
eachcapturingthediscrepancybetweentheinferredsystem asuper-resolutionmodel[48]thatupscalesthesegmented
|     |     |     |     |     |     |     | foreground(obtainedviaGrounded-SAM2[46]). |     |     |     |     | Whilethe |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | -------- |
statesandthecorrespondingobservationsfrom3Dgeometry,
3Dmotiontracking,and2Dcolor,respectively(wedeferthe resultingmeshcorrespondsreasonablywellwiththecamera
detailsofeachcostcomponenttoSec.4.2.1andSec.4.2.2). observation, we can still observe inconsistencies in scale,
The function g is the observation model, describing the pose,anddeformation.
θ
projectionfromthepredictedstatetotheimageplaneand Toaddressthis,wedesignaregistrationmodulethatuses
rendering image-space sensory observation from the i-th 2Dmatchingforscaleestimation,rigidregistration,andnon-
camera. The f models the dynamic evolution of the rigiddeformation. Acoarse-to-finestrategyfirstestimates
α,G
object’sstateundertheSpring-Massmodel(Sec.3). initialrotationvia2DcorrespondencesmatchedusingSu-
perGlue[50],followedbyrefinementwiththePerspective-n-
4.2.PhysTwinFramework Point(PnP)[25]algorithm. Weresolvescaleandtranslation
Given the complexity of the overall optimization defined ambiguitiesbyoptimizingthedistancesbetweenmatched
|     |     |     |     |     |     |     | points | in the | camera coordinate | system. | After | applying |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------ | ----------------- | ------- | ----- | -------- |
inEq.2,ourPhysTwinframeworkdecomposesitintotwo
thesetransformations,theobjectsarealignedinpose,with
stages. Thefirststagefocusesonoptimizingthegeometry
andphysicalparameters,whilethesecondstageisdedicated somedeformationshandledbyas-rigid-as-possibleregistra-
|     |     |     |     |     |     |     | tion [53]. | Finally, | ray-casting | alignment | ensures | that ob- |
| --- | --- | --- | --- | --- | --- | --- | ---------- | -------- | ----------- | --------- | ------- | -------- |
tooptimizingtheappearance-relatedparameters.
servedpointsmatchthedeformedmeshwithoutocclusions.
4.2.1.PhysicsandGeometryOptimization These steps yield a shape prior aligned with the first-
AsoutlinedinouroptimizationformulationinSec.4.1,the frameobservations,whichservesasacrucialinitialization
objective is to minimize the discrepancy between the pre- fortheinversephysicsandappearanceoptimizationstages.
| dictedobservationOˆ |     | andtheactualobservationO |     |     |     | .First, |                                                 |     |     |     |     |     |
| ------------------- | --- | ------------------------ | --- | --- | --- | ------- | ----------------------------------------------- | --- | --- | --- | --- | --- |
|                     |     | t,i                      |     |     |     | t,i     | Sparse-to-DenseOptimization.TheSpring-Massmodel |     |     |     |     |     |
weconvertthedepthobservationsD ateachtimeframet consistsofboththetopologicalstructure(i.e.,theconnec-
t
intotheobservedpartial3DpointcloudX .Inthefirststage, tivityofthesprings)andthephysicalparametersdefinedon
t
weconsiderthefollowingformulationfortheoptimization: thesprings. AsmentionedinSec.3,wealsoincludecontrol
parameterstoconnectspringsbetweencontrolpointsand
|     | (cid:88)(cid:16) |     |     |     |     | (cid:17) |     |     |     |     |     |     |
| --- | ---------------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
|     |                  | (Xˆ |     |     | (Xˆ |          |     |     |     |     |     |     |
min C t ,X t )+C t ,X t ) objectpoints,definedbyaradiusandamaximumnumberof
|     | α,G0 | geometry |     | motion |     |     |            |                                            |     |     |     |     |
| --- | ---- | -------- | --- | ------ | --- | --- | ---------- | ------------------------------------------ | --- | --- | --- | --- |
|     | t    |          |     |        |     | (3) | neighbors. | Similarly,fortopologyoptimization,weemploy |     |     |     |     |
aheuristicapproachthatconnectsnearest-neighborpoints,
|     | s.t. Xˆ | =f (Xˆ | ,a ), |     |     |     |     |     |     |     |     |     |
| --- | ------- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | t+1     | α,G0   | t t   |     |     |     |     |     |     |     |     |     |
alsoparameterizedbyaconnectionradiusandamaximum
wheretheC functionquantifiesthesingle-direction numberofneighbors,therebycontrollingthedensityofthe
geometry
Chamferdistancebetweenthepartiallyobservedpointcloud springs. Toextractcontrolpointsfromvideodata,weuti-
X andtheinferredstateXˆ ,andC quantifiesthetrack- lizeGrounded-SAM2[46]tosegmentthehandmaskand
| t   |     |     | t   | motion |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
ingerrorbetweenthepredictedpointxˆtanditscorrespond- CoTracker3[23]totrackhandmovements. Afterliftingthe
i
ingobservedtrackingxt. Theobservedtrackingisobtained pointsto3D,weapplyfarthest-pointsamplingtoobtainthe
i
using the vision foundation model CoTracker3 [23], fol- finalsetofcontrolpoints.
lowedbyliftingtheresultto3Dviadepthmapunprojection. Alltheaforementionedcomponentsconstitutetheparam-
There are three main challenges in the first-stage opti- eterspaceweaimtooptimize. Thetwomainchallengesare:
mization: (1)partialobservationsfromsparseviewpoints; (1)someparametersarenon-differentiable(e.g.,theradius

andmaximumnumberofneighbors);and(2)torepresenta 4.3.CapabilitiesofPhysTwin
widerangeofobjects,wemodeldensespringstiffness,lead-
OurconstructedPhysTwinsupportsreal-timesimulationof
ingtoaparameterspacewithtensofthousandsofsprings.
deformableobjectsundervariousmotionswhilemaintaining
| To address                              | these challenges, | we introduce | a hierarchi-    |                      |                                     |     |     |
| --------------------------------------- | ----------------- | ------------ | --------------- | -------------------- | ----------------------------------- | --- | --- |
|                                         |                   |              |                 | realisticappearance. | Thisreal-time,photorealisticsimula- |     |     |
| calsparse-to-denseoptimizationstrategy. |                   |              | Initially,weem- |                      |                                     |     |     |
tionenablesinteractiveexplorationofobjectdynamics.
| ploy zero-order, | sampling-based | optimization | to estimate |     |     |     |     |
| ---------------- | -------------- | ------------ | ----------- | --- | --- | --- | --- |
Byintroducingcontrolpointsanddynamicallyconnect-
| the parameters, | which naturally | circumvents | the issue of |     |     |     |     |
| --------------- | --------------- | ----------- | ------------ | --- | --- | --- | --- |
ingthemtoobjectpointsviasprings,oursystemcansimulate
| differentiability.                          | However,zero-orderoptimizationbecomes |     |            |                                       |     |                   |     |
| ------------------------------------------- | ------------------------------------- | --- | ---------- | ------------------------------------- | --- | ----------------- | --- |
|                                             |                                       |     |            | diversemotionpatternsandinteractions. |     | Thesecapabilities |     |
| inefficientwhentheparameterspaceistoolarge. |                                       |     | Therefore, |                                       |     |                   |     |
makePhysTwinapowerfulrepresentationforreal-timeinter-
inthefirststage,weassumehomogeneousstiffness,allow-
activesimulationandmodel-basedroboticmotionplanning,
ingthetopologyandotherphysicalparameterstoachieve
whicharefurtherdescribedinSec.5.3.
| agoodinitialization. | Inthesecondstage,wefurtherrefine |     |     |     |     |     |     |
| -------------------- | -------------------------------- | --- | --- | --- | --- | --- | --- |
theparametersusingfirst-ordergradientdescent,leveraging
5.Experiments
| ourcustom-builtdifferentiablespring-masssimulator. |           |           | This             |     |     |     |     |
| -------------------------------------------------- | --------- | --------- | ---------------- | --- | --- | --- | --- |
| stage simultaneously                               | optimizes | the dense | spring stiffness |     |     |     |     |
Inthissection,weevaluatetheperformanceofourPhysT-
andcollisionparameters. winframeworkacrossthreedistincttasksinvolvingdifferent
| Beyondtheoptimizationstrategy, |     | weincorporateaddi- |     |                 |                                       |     |     |
| ------------------------------ | --- | ------------------ | --- | --------------- | ------------------------------------- | --- | --- |
|                                |     |                    |     | typesofobjects. | Ourprimaryobjectiveistoaddressthefol- |     |     |
tionalsupervisionbyutilizingtrackingpriorsfromvision
|     |     |     |     | lowingthreequestions: | (1)Howaccuratelydoesourframe- |     |     |
| --- | --- | --- | --- | --------------------- | ----------------------------- | --- | --- |
foundationmodels. Weliftthe2Dtrackingpredictioninto workreconstructandresimulatedeformableobjectsandpre-
3Dtoobtainpseudo-ground-truthtrackingdataforthe3D
|     |     |     |     | dicttheirfuturestates? | (2)Howwelldoestheconstructed |     |     |
| --- | --- | --- | --- | ---------------------- | ---------------------------- | --- | --- |
points,whichformsacrucialcomponentofourcostfunction PhysTwingeneralizetounseeninteractions? (3)Whatisthe
asmentionedinEq.(3).
utilityofPhysTwinindownstreamtasks?
Byintegratingouroptimizationstrategywithacostfunc-
tionthatleveragesadditionaltrackingpriors,ourPhysTwin 5.1.ExperimentSettings
frameworkcaneffectivelyandefficientlymodelthedynam-
|     |     |     |     | Dataset. WecollectadatasetofRGBDvideoscapturing |     |     |     |
| --- | --- | --- | --- | ----------------------------------------------- | --- | --- | --- |
icsofdiverseinteractableobjectsfromvideos.
|     |     |     |     | human interactions | with various | deformable objects | with |
| --- | --- | --- | --- | ------------------ | ------------ | ------------------ | ---- |
4.2.2.AppearanceOptimization differentphysicalproperties,suchasropes,stuffedanimals,
Forthesecond-stageappearanceoptimization,tomodelob- cloth,anddeliverypackages. ThreeRealSense-D455RGBD
|                  |              |                 |             | camerasareusedtorecordtheinteractions. |     | Eachvideois1 |     |
| ---------------- | ------------ | --------------- | ----------- | -------------------------------------- | --- | ------------ | --- |
| ject appearance, | we construct | a set of static | 3D Gaussian |                                        |     |              |     |
to10secondslongandcapturesdifferentinteractions,includ-
kernelsparameterizedbyθ,witheachGaussiandefinedby
a3Dcenterpositionµ,arotationmatrixrepresentedbya ing quick lifting, stretching, pushing, and squeezing with
|             |                                      |     |     | oneorbothhands. | Wecollect22scenariosencompassing |     |     |
| ----------- | ------------------------------------ | --- | --- | --------------- | -------------------------------- | --- | --- |
| quaternionq | SO(3),ascalingmatrixrepresentedbya3D |     |     |                 |                                  |     |     |
∈
vectors, anopacityvalueα, andcolorcoefficientsc. We variousobjecttypes,interactiontypes,andhandconfigura-
tions. Foreachscenario,theRGBDvideosaresplitintoa
optimizeθherevia
trainingsetandatestsetfollowinga7:3ratio,whereonly
(cid:88)
min C (ˆI ,I )s.t.ˆI =g (Xˆ ,i), (4) the training set is used to construct PhysTwin. We manu-
|     | render i,t | i,t i,t | θ t |                                                     |     |     |     |
| --- | ---------- | ------- | --- | --------------------------------------------------- | --- | --- | --- |
| θ   |            |         |     | allyannotate9ground-truthtrackingpointsforeachvideo |     |     |     |
t,i
|                                                  |     |     |     | to evaluate tracking | performance | with the semi-auto | tool |
| ------------------------------------------------ | --- | --- | --- | -------------------- | ----------- | ------------------ | ---- |
| whereXˆ istheoptimizedsystemstatesattimet,iisthe |     |     |     | introducedin[7].     |             |                    |      |
t
|                  | ,ˆI     |                           |     | Tasks.ToassesstheeffectivenessofourPhysTwinframe- |     |     |     |
| ---------------- | ------- | ------------------------- | --- | ------------------------------------------------- | --- | --- | --- |
| cameraindex,andI | i,t i,t | arethegroundtruthimageand |     |                                                   |     |     |     |
renderedimagefromcameraviewiattimet,respectively. workandthequalityofourconstructedPhysTwin,weformu-
C computesthe losswithaD-SSIMtermbetween latethreetasks: (1)Reconstruction&Resimulation;(2)Fu-
| render | 1   |     |     |     |     |     |     |
| ------ | --- | --- | --- | --- | --- | --- | --- |
L
the rendering and ground truth image. For simplicity, we turePrediction;and(3)GeneralizationtoUnseenActions.
sett=0tooptimizeappearanceonlyatthefirstframe. We FortheReconstruction&Resimulationtask,theobjective
istoconstructPhysTwinsuchthatitcanaccuratelyrecon-
restricttheGaussianshapetobeisotropictopreventspiky
artifactsduringdeformation. structandresimulatethemotionofdeformableobjectsgiven
Toensurerealisticrenderingunderdeformation,weneed theactionsrepresentedbythecontrolpointpositions.
todynamicallyadjusteachGaussianateachtimesteptbased FortheFuturePredictiontask,weaimtoassesswhether
onthetransitionbetweenstatesXˆ andXˆ . Toachieve PhysTwincanperformwellonunseenfutureframesduring
|     |     | t   | t+1 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
this,weadoptaGaussianupdatingalgorithmusingLinear itsconstruction. FortheGeneralizationtoUnseenInterac-
BlendSkinning(LBS)[20,54,69],whichinterpolatesthe tionstask,thegoalistoassesswhetherPhysTwincanadapt
motionsof3DGaussiansusingthemotionsofneighboring todifferentinteractions. Toevaluatethis,weconstructagen-
massnodes. Pleaserefertothesupplementaryfordetails. eralizationdatasetconsistingofinteractionpairsperformed

Reconstruction & Resimulation Future Prediction
noitavresbO
)sruO(
niwTsyhP
scimanyD-SG
suaG-gnirpS
noitavresbO
niwTsyhP
scimanyD-SG
suaG-gnirpS
noitavresbO
)sruO(
niwTsyhP
scimanyD-SG
suaG-gnirpS
t t
Figure3.QualitativeResultsonReconstruction&ResimulationandFuturePrediction.Wevisualizetherenderingresultsofdifferent
methodsontwotasks.Forthereconstruction&resimulationtask,ourmethodachievesabettermatchwiththeobservations.Forthefuture
predictiontask,ourmethodaccuratelypredictsthefuturestateoftheobjects.Incontrast,thebaselinesfailinmostcases:GS-Dynamics[69]
tendstoremainstatic,whileSpring-Gauss[72]frequentlycausesthephysicalmodeltocrash.

Observation Future Prediction t
)sruO(
niwTsyhP
scimanyD-SG
)sruO(
niwTsyhP
scimanyD-SG
Figure4.QualitativeResultsonGeneralizationtoUnseenInteractions.Wevisualizethesimulationofadeformableobjectunderunseen
interactionsusingourmethodandGS-Dynamics[69].Theleftmostimageshowstheinteractionusedtotrainthedynamicsmodels,while
theimagesontherightdemonstratetheirgeneralizationtounseeninteractions.OurPhysTwinsignificantlyoutperformspriorwork.
Table1.QuantitativeResultsonReconstruction&ResimulationandFuturePrediction.Wecomparetheperformanceofourmethod
withtwopriorwork,GS-Dynamics[69]andSpring-Gaus[72],ontwotasks: reconstruction&resimulationandfutureprediction. Our
PhysTwinframeworkconsistentlyoutperformsthebaselinesacrossallmetrics.
Task Reconstruction&Resimulation FuturePrediction
Method CD TrackError IoU% PSNR SSIM LPIPS CD TrackError IoU% PSNR SSIM LPIPS
↓ ↓ ↑ ↑ ↑ ↓ ↓ ↓ ↑ ↑ ↑ ↓
Spring-Gaus[72] 0.041 0.050 57.6 23.445 0.928 0.102 0.062 0.094 46.4 22.488 0.924 0.113
GS-Dynamics[69] 0.014 0.022 72.1 26.260 0.940 0.052 0.041 0.070 49.8 22.540 0.924 0.097
PhysTwin(Ours) 0.005 0.009 84.4 28.214 0.945 0.034 0.012 0.022 72.5 25.617 0.941 0.055
Table 2. Quantitative Results on Generalization to Unseen The second baseline is a learning-based simulation ap-
Interactions. WecompareourmethodwithGS-Dynamics[69] proach,GS-Dynamics[69],whichemploysaGNN-based
ongeneralizationtounseeninteractions.Bothmethodsaretrained
neuraldynamicsmodeltolearnsystemdynamicsdirectly
onthesamevideowithaspecificinteractionandtestedonunseen
frompartialobservations. Intheiroriginalsetting,videopre-
interactions.Ourmethodachievessignificantlybetterresults.
processingwithDyn3DGS[34]isrequiredtoobtaintrack-
Method CD TrackError IoU% PSNR SSIM LPIPS inginformation. Forafairercomparison,westrengthened
↓ ↓ ↑ ↑ ↑ ↓
GS-Dynamics[69] 0.029 0.038 63.4 25.053 0.934 0.067 itbyusingour3D-liftingtrackerbasedonCoTracker3[23],
PhysTwin(Ours) 0.013 0.018 72.18 26.199 0.938 0.047
whichprovidesmoreefficientandaccuratesupervisionfor
trainingtheneuraldynamicsmodelusedbyGS-Dynamics.
onthesameobjectbutwithvaryingmotions,includingdif-
Evaluation. Tobetterunderstandwhetherourprediction
ferencesinhandconfigurationandinteractiontype.
matchestheobservations,weevaluatepredictionsinboth3D
Baselines. To the best of our knowledge, there is cur- and2D.Forthe3Devaluation,weusethesingle-direction
rentlynoexistingworkthatdemonstratesgoodperformance ChamferDistance(partialgroundtruthwithourfull-state
acrossallthreetasks.Therefore,weselecttwomainresearch prediction)andthetrackingerror(basedonourmanually
directionsasbaselinesandfurtheraugmentthemtomatch annotated ground-truth tracking points). For the 2D eval-
thetasksinoursetting(fulldetailsinthesupplementary). uation, we assess image quality using PSNR, SSIM, and
Thefirstbaselineweconsiderisaphysics-basedsimu- LPIPS[70],andsilhouettealignmentusingIoU.Weperform
lationmethodforidentifyingthematerialpropertiesofde- 2Devaluationonlyatthecenterviewpointduetooptimal
formableobjects,Spring-Gaus[72]. Theirworkhasdemon- visibilityofobjects,withmetricsaveragedacrossallframes
strated strong capabilities in reconstruction, resimulation, andscenarios. Specially,fortheSpring-Gaus[72]baseline,
andfuturepredictioninitsoriginalsetting. However,their itsoptimizationprocessisunstableduetoinaccuratephysics
frameworkdoesnotsupportexternalcontrolinputs,sowe modeling. Therefore,wereporttheabovemetricsonlyfor
augmentitwithadditionalcontrolcapabilities. itssuccessfulcases.

Figure5.ApplicationsofourPhysTwin.OurconstructedPhysTwinsupportsavarietyoftasks,includingreal-timeinteractivesimulation,
whichcanacceptinputfromeitherakeyboardorarobotteleoperationsetup.Meanwhile,PhysTwinalsoenablesmodel-basedrobotplanning
toaccomplishtaskssuchasliftingaropeintosomespecificconfiguration.
5.2.Results ourmethodacrossdifferentactions. Incontrast,theneural
dynamicsmodelstrugglestoadapttoenvironmentalchanges
Toassesstheperformanceofourframeworkandthequality
anddiverseinteractionsaseffectivelyasourapproach.More-
of our constructed PhysTwin, we compare with two aug-
over,inunseeninteractionscenarios,ourmethodachieves
mentedbaselinesacrossthreetasksettings. Ourquantitative
performancecomparabletothatonthefuturepredictiontask,
analysisrevealsthatthePhysTwinframeworkconsistently
highlightingtherobustnessandgeneralizationcapabilityof
outperformsthebaselinesacrossvarioustasks.
ourconstructedPhysTwin.
Reconstruction &Resimulation. The quantitative re-
sults in Tab. 1 Reconstruction & Resimulation column
5.3.Application
demonstrate the superior performance of our PhysTwin
methodoverbaselines. Ourapproachsignificantlyimproves TheefficientforwardsimulationcapabilitiesofourSpring-
all evaluated metrics, including Chamfer Distance, track- Mass simulator, implemented using Warp [37], enable a
ing error, and 2D IoU, confirming that our reconstruction varietyofdownstreamapplications. Fig.5showcaseskey
and resimulation align more closely with the original ob- applicationsenabledbyourPhysTwin: (1)InteractiveSim-
servations. Thishighlightstheeffectivenessofourmodel ulation: Userscaninteractwithobjectsinrealtimeusing
inlearningamoreaccuratedynamicsmodelundersparse keyboardcontrols,eitherwithoneorbothhands. Thesys-
observations. Additionally, rendering metrics show that temalsosupportsreal-timesimulationofanobject’sfuture
ourmethodproducesmorerealistic2Dimages,benefiting state during human teleoperation with robotic arms. This
fromtheGaussianblendingstrategyandenhanceddynamic featureservesasavaluabletoolforpredictingobjectdynam-
modeling. Fig.3furtherprovidesqualitativevisualizations icsduringmanipulation. (2)Model-BasedRoboticPlanning:
acrossdifferentobjects,illustratingprecisealignmentwith OwingtothehighfidelityofourconstructedPhysTwin,it
originalobservations. Notably,ourphysics-basedrepresen- canbeusedasadynamicmodelinplanningpipelines. By
tation inherently improves point tracking. After physics- integratingitwithmodel-basedplanningtechniques,wecan
constrainedoptimization,ourtrackingsurpassestheoriginal generate effective motion plans for robots to complete a
CoTracker3[23]predictionsusedfortraining,achievingbet- varietyoftasks.
teralignmentafterglobaloptimization(Seesupplementfor
moredetails).
6.Conclusion
Future Prediction. Table 1, in the Future Prediction
column, demonstrates that our method achieves superior WeintroducedPhysTwin,anovelframeworkforconstruct-
performanceinpredictingunseenframes,excellinginboth ingphysicaldigitaltwinsfromsparsevideos,enablingeffec-
dynamics alignment and rendering quality. Fig. 3 further tivereconstructionandresimulationofdeformableobjects.
providesqualitativeresults,illustratingtheaccuracyofour Our approach excels in predicting future states and simu-
predictionsonunseenframes. latingobjectinteractionsthatgeneralizetounseenactions.
GeneralizationtoUnseenInteractions. Wealsoeval- Weshowedthesuperiorperformanceofourmethodacross
uatethegeneralizationperformancetounseeninteractions. various object types, control configurations, and task set-
Ourdatasetincludestransfersfromoneinteraction(e.g.,sin- tings, significantly outperforming prior work. PhysTwin
glelift)tosignificantlydifferentinteractions(e.g.,double enablesvariousdownstreamtasksthatdemandhigh-speed
stretch).WedirectlyuseourconstructedPhysTwinandlever- simulation and accurate future prediction. Moreover, our
ageourregistrationpipelinetoalignitwiththefirstframe approachprovidesvaluableinsightsforroboticmanipulation.
of the target case. Fig. 4 shows that our method closely Bybridgingperceptionandphysics-basedsimulation,Phys-
matchesthegroundtruthobservationsintermsofdynamics. Twinservesasacrucialtoolforguidingrobotinteractions,
Quantitative results further demonstrate the robustness of makingreal-worlddeploymentmoreefficientandreliable.

Acknowledgement [10] YuanxingDuan,FangyinWei,QiyuDai,YuhangHe,Wen-
|     |     |     |     |     | zhengChen,andBaoquanChen. |     |     | 4d-rotorgaussiansplatting: |     |
| --- | --- | --- | --- | --- | ------------------------- | --- | --- | -------------------------- | --- |
ThisworkispartiallysupportedbytheToyotaResearchIn- towardsefficientnovelviewsynthesisfordynamicscenes. In
stitute(TRI),theSonyGroupCorporation,Google,Dalus
ACMSIGGRAPH2024ConferencePapers,pages1–11,2024.
| AI, the DARPA | TIAMAT |     | program (HR0011-24-9-0430), |     |     |     |     |     |     |
| ------------- | ------ | --- | --------------------------- | --- | --- | --- | --- | --- | --- |
1,2
theIntelAISRSgift,Amazon-IllinoisAICEgrant,MetaRe- [11] BenEvans,AbithaThankaraj,andLerrelPinto. Contextis
searchGrant,IBMIIDAIGrant,andNSFAwards#2331878, everything:Implicitidentificationfordynamicsadaptation.In
2022InternationalConferenceonRoboticsandAutomation
| #2340254,#2312102,#2414227,and#2404385. |     |     |     | Wegreatly |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --------- | --- | --- | --- | --- | --- |
appreciate the NCSA for providing computing resources. (ICRA),pages2642–2648.IEEE,2022. 1,2
Thisarticlesolelyreflectstheopinionsandconclusionsof [12] YutaoFeng,YintongShang,XuanLi,TianjiaShao,Chen-
fanfuJiang,andYinYang.Pie-nerf:Physics-basedinteractive
itsauthorsandshouldnotbeinterpretedasnecessarilyrep-
|     |     |     |     |     | elastodynamicswithnerf. |     | InProceedingsoftheIEEE/CVF |     |     |
| --- | --- | --- | --- | --- | ----------------------- | --- | -------------------------- | --- | --- |
resentingtheofficialpolicies,eitherexpressedorimplied,of
|     |     |     |     |     | Conference | on Computer | Vision | and Pattern Recognition, |     |
| --- | --- | --- | --- | --- | ---------- | ----------- | ------ | ------------------------ | --- |
thesponsors.
|     |     |     |     |     | pages4450–4461,2024. |     | 1,2 |     |     |
| --- | --- | --- | --- | --- | -------------------- | --- | --- | --- | --- |
[13] SaraFridovich-Keil,GiacomoMeanti,FrederikRahbækWar-
References
|     |     |     |     |     | burg, Benjamin                                    | Recht, | and Angjoo | Kanazawa. K-planes: |     |
| --- | --- | --- | --- | --- | ------------------------------------------------- | ------ | ---------- | ------------------- | --- |
|     |     |     |     |     | Explicitradiancefieldsinspace,time,andappearance. |        |            |                     | In  |
[1] BenjaminAttal,Jia-BinHuang,ChristianRichardt,Michael
ProceedingsoftheIEEE/CVFConferenceonComputerVi-
Zollhoefer,JohannesKopf,MatthewO’Toole,andChangil
Kim. Hyperreel: High-fidelity 6-dof video with ray- sionandPatternRecognition,pages12479–12488,2023. 1,
| conditionedsampling. |     | InProceedingsoftheIEEE/CVFCon- |     |     | 2   |     |     |     |     |
| -------------------- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- |
ferenceonComputerVisionandPatternRecognition,pages [14] HangGao,RuilongLi,ShubhamTulsiani,BryanRussell,and
|                   |     |     |     |     | AngjooKanazawa. |     | Monoculardynamicviewsynthesis: |     | A   |
| ----------------- | --- | --- | --- | --- | --------------- | --- | ------------------------------ | --- | --- |
| 16610–16620,2023. |     | 2   |     |     |                 |     |                                |     |     |
AdvancesinNeuralInformationProcessing
| [2] AngCaoandJustinJohnson.Hexplane:Afastrepresentation |     |     |     |     | realitycheck. |     |     |     |     |
| ------------------------------------------------------- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- |
fordynamicscenes. InProceedingsoftheIEEE/CVFCon- Systems,35:33768–33780,2022. 1,2
ferenceonComputerVisionandPatternRecognition,pages [15] MoritzGeilinger,DavidHahn,JonasZehnder,MoritzBächer,
130–141,2023. 1,2 BernhardThomaszewski,andStelianCoros. Add: Analyt-
icallydifferentiabledynamicsformulti-bodysystemswith
| [3] Hsiao-yu | Chen, | Edith Tretschk, | Tuur Stuyck, | Petr Kadle- |     |     |     |     |     |
| ------------ | ----- | --------------- | ------------ | ----------- | --- | --- | --- | --- | --- |
cek,LadislavKavan,EtienneVouga,andChristophLassner. frictionalcontact. ACMTransactionsonGraphics(TOG),39
| Virtualelasticobjects. |     | InProceedingsoftheIEEE/CVFCon- |     |     | (6):1–15,2020. | 2   |     |     |     |
| ---------------------- | --- | ------------------------------ | --- | --- | -------------- | --- | --- | --- | --- |
ferenceonComputerVisionandPatternRecognition,pages [16] ShanyanGuan,HuayuDeng,YunboWang,andXiaokang
15827–15837,2022. 2 Yang. Neurofluid: Fluiddynamicsgroundingwithparticle-
|     |     |     |     |     | drivenneuralradiancefields. |     | InInternationalconferenceon |     |     |
| --- | --- | --- | --- | --- | --------------------------- | --- | --------------------------- | --- | --- |
[4] ZhenfangChen,KexinYi,YunzhuLi,MingyuDing,Antonio
Torralba,JoshuaBTenenbaum,andChuangGan. Comphy: machinelearning,pages7919–7929.PMLR,2022. 2
Compositionalphysicalreasoningofobjectsandeventsfrom [17] XiangGuo,JiadaiSun,YuchaoDai,GuanyingChen,Xiao-
videos. arXivpreprintarXiv:2205.01089,2022. 1,2 qingYe,XiaoTan,ErruiDing,YumengZhang,andJingdong
[5] MengyuChu,LingjieLiu,QuanZheng,ErikFranz,Hans- Wang. Forwardflowfornovelviewsynthesisofdynamic
scenes. InProceedingsoftheIEEE/CVFInternationalCon-
| PeterSeidel,ChristianTheobalt,andRhalebZayer. |     |     |     | Physics |     |     |     |     |     |
| --------------------------------------------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
informedneuralfieldsforsmokereconstructionwithsparse ferenceonComputerVision,pages16022–16033,2023. 1,
| data. | ACMTransactionsonGraphics,41(4):119:1–119:14, |     |     |     | 2   |     |     |     |     |
| ----- | --------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
2022. 1,2 [18] NikolausHansen. Thecmaevolutionstrategy:acomparing
[6] Brian Curless and Marc Levoy. A volumetric method for review. Towardsanewevolutionarycomputation:Advances
intheestimationofdistributionalgorithms,pages75–102,
| buildingcomplexmodelsfromrangeimages. |             |            |             | InProceedings |         |     |     |     |     |
| ------------------------------------- | ----------- | ---------- | ----------- | ------------- | ------- | --- | --- | --- | --- |
| of the                                | 23rd annual | conference | on Computer | graphics and  | 2006. 2 |     |     |     |     |
interactivetechniques,pages303–312,1996. 2 [19] Eric Heiden, Miles Macklin, Yashraj Narang, Dieter Fox,
[7] CarlDoersch,YiYang,MelVecerik,DilaraGokay,Ankush AnimeshGarg,andFabioRamos. Disect: Adifferentiable
Gupta,YusufAytar,JoaoCarreira,andAndrewZisserman. simulation engine for autonomous robotic cutting. arXiv
preprintarXiv:2105.12244,2021.
| TAPIR:Trackinganypointwithper-frameinitializationand |     |     |     |     |     |     |     | 2   |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
temporalrefinement. InProceedingsoftheIEEE/CVFIn- [20] Yi-HuaHuang, Yang-TianSun, ZiyiYang, XiaoyangLyu,
ternationalConferenceonComputerVision,pages10061– Yan-PeiCao,andXiaojuanQi.Sc-gs:Sparse-controlledgaus-
10072,2023. 5 siansplattingforeditabledynamicscenes. InProceedings
[8] DannyDriess,ZhiaoHuang,YunzhuLi,RussTedrake,and oftheIEEE/CVFconferenceoncomputervisionandpattern
MarcToussaint. Learningmulti-objectdynamicswithcom- recognition,pages4220–4230,2024. 1,2,5,12
positional neural radiance fields. In Conference on robot [21] Krishna Murthy Jatavallabhula, Miles Macklin, Florian
learning,pages1755–1768.PMLR,2023. 1,2 Golemo, VikramVoleti, LindaPetrini, MartinWeiss, Bre-
[9] Tao Du, Kui Wu, Pingchuan Ma, Sebastien Wah, Andrew andanConsidine,JérômeParent-Lévesque,KevinXie,Kenny
Spielberg,DanielaRus,andWojciechMatusik. Diffpd:Dif- Erleben, etal. gradsim: Differentiablesimulationforsys-
ferentiableprojectivedynamics.ACMTransactionsonGraph- tem identification and visuomotor control. arXiv preprint
| ics(ToG),41(2):1–21,2021. |     |     | 1,2 |     | arXiv:2104.02646,2021. |     | 2   |     |     |
| ------------------------- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- |

[22] Ying Jiang, Chang Yu, Tianyi Xie, Xuan Li, Yutao Feng, [35] Pingchuan Ma, Tao Du, Joshua B Tenenbaum, Wojciech
HuaminWang,MinchenLi,HenryLau,FengGao,YinYang, Matusik, and Chuang Gan. Risp: Rendering-invariant
etal. Vr-gs:Aphysicaldynamics-awareinteractivegaussian state predictor with differentiable simulation and render-
splattingsysteminvirtualreality. InACMSIGGRAPH2024 ingforcross-domainparameterestimation. arXivpreprint
| ConferencePapers,pages1–1,2024. | 2   | arXiv:2205.05678,2022. | 2   |     |
| ------------------------------- | --- | ---------------------- | --- | --- |
[23] Nikita Karaev, Iurii Makarov, Jianyuan Wang, Natalia [36] PingchuanMa, PeterYichenChen, BoleiDeng, JoshuaB
Neverova, Andrea Vedaldi, and Christian Rupprecht. Co- Tenenbaum, TaoDu, ChuangGan, andWojciechMatusik.
tracker3: Simpler and better point tracking by pseudo- Learningneuralconstitutivelawsfrommotionobservations
labellingrealvideos. arXivpreprintarXiv:2410.11831,2024. forgeneralizablepdedynamics. InInternationalConference
2,4,7,8,12,16 onMachineLearning,pages23279–23300.PMLR,2023. 1,
| [24] AgelosKratimenos,JiahuiLei,andKostasDaniilidis.Dynmf: |     | 2   |     |     |
| ---------------------------------------------------------- | --- | --- | --- | --- |
Neuralmotionfactorizationforreal-timedynamicviewsyn- [37] MilesMacklin.Warp:Ahigh-performancepythonframework
thesiswith3dgaussiansplatting. InEuropeanConferenceon for gpu simulation and graphics. https://github.com/
ComputerVision,pages252–269.Springer,2024. 1,2 nvidia/warp,2022. NVIDIAGPUTechnologyConference
| [25] VincentLepetit,FrancescMoreno-Noguer,andPascalFua. |     | (GTC). 8 |     |     |
| ------------------------------------------------------- | --- | -------- | --- | --- |
Ep n p: An accurate o (n) solution to the p n p problem. [38] RichardANewcombe,DieterFox,andStevenMSeitz. Dy-
Internationaljournalofcomputervision,81:155–166,2009. namicfusion:Reconstructionandtrackingofnon-rigidscenes
| 4   |     | inreal-time. | InProceedingsoftheIEEEconferenceoncom- |     |
| --- | --- | ------------ | -------------------------------------- | --- |
[26] HaoLi,RobertWSumner,andMarkPauly. Globalcorre- putervisionandpatternrecognition,pages343–352,2015.
| spondenceoptimizationfornon-rigidregistrationofdepth |     | 2   |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- |
scans. InComputergraphicsforum,pages1421–1430.Wiley [39] KeunhongPark,UtkarshSinha,JonathanTBarron,Sofien
OnlineLibrary,2008. 2 Bouaziz, Dan B Goldman, Steven M Seitz, and Ricardo
[27] XuanLi,Yi-LingQiao,PeterYichenChen,KrishnaMurthy Martin-Brualla. Nerfies:Deformableneuralradiancefields.
Jatavallabhula,MingLin,ChenfanfuJiang,andChuangGan. InProceedingsoftheIEEE/CVFinternationalconferenceon
Pac-nerf: Physics augmented continuum neural radiance computervision,pages5865–5874,2021. 1,2
fields for geometry-agnostic system identification. arXiv [40] KeunhongPark,UtkarshSinha,PeterHedman,JonathanT
preprintarXiv:2303.05512,2023. 1,2 Barron,SofienBouaziz,DanBGoldman,RicardoMartin-
[28] YunzhuLi,JiajunWu,RussTedrake,JoshuaBTenenbaum, Brualla, and Steven M Seitz. Hypernerf: A higher-
andAntonioTorralba. Learningparticledynamicsformanip- dimensionalrepresentationfortopologicallyvaryingneural
ulatingrigidbodies,deformableobjects,andfluids. arXiv radiancefields. arXivpreprintarXiv:2106.13228,2021. 2
preprintarXiv:1810.01566,2018. 1,2 [41] Yicong Peng, Yichao Yan, Shenqi Liu, Yuhao Cheng,
[29] YunzhuLi, ShuangLi, VincentSitzmann, PulkitAgrawal, ShanyanGuan,BowenPan,GuangtaoZhai,andXiaokang
andAntonioTorralba. 3dneuralscenerepresentationsfor Yang. Cagenerf:Cage-basedneuralradiancefieldsforgen-
visuomotorcontrol. InConferenceonRobotLearning,pages renlized3ddeformationandanimation. InThirty-SixthCon-
112–123.PMLR,2022. 1,2 ferenceonNeuralInformationProcessingSystems,2022. 1,
| [30] ZhengqiLi,SimonNiklaus,NoahSnavely,andOliverWang. |     | 2   |     |     |
| ------------------------------------------------------ | --- | --- | --- | --- |
Neural scene flow fields for space-time view synthesis of [42] Tobias Pfaff, Meire Fortunato, Alvaro Sanchez-Gonzalez,
dynamicscenes.InProceedingsoftheIEEE/CVFConference andPeterBattaglia. Learningmesh-basedsimulationwith
onComputerVisionandPatternRecognition,pages6498– graph networks. In International conference on learning
| 6508,2021. 2 |     | representations,2020. | 1,2 |     |
| ------------ | --- | --------------------- | --- | --- |
[31] ZhengqiLi,QianqianWang,ForresterCole,RichardTucker, [43] Albert Pumarola, Enric Corona, Gerard Pons-Moll, and
|                                                   |     | Francesc Moreno-Noguer. | D-nerf: Neural | radiance fields |
| ------------------------------------------------- | --- | ----------------------- | -------------- | --------------- |
| andNoahSnavely. Dynibar: Neuraldynamicimage-based |     |                         |                |                 |
rendering. InProceedingsoftheIEEE/CVFConferenceon fordynamicscenes. InProceedingsoftheIEEE/CVFcon-
ComputerVisionandPatternRecognition,pages4273–4284, ferenceoncomputervisionandpatternrecognition,pages
| 2023. 1,2 |     | 10318–10327,2021. | 1,2 |     |
| --------- | --- | ----------------- | --- | --- |
[32] XingyuLin, YufeiWang, ZixuanHuang, andDavidHeld. [44] Yi-LingQiao,JunbangLiang,VladlenKoltun,andMingC.
Learningvisibleconnectivitydynamicsforclothsmoothing. Lin. Differentiablesimulationofsoftmulti-bodysystems.
InConferenceonRobotLearning,pages256–266.PMLR, In Conference on Neural Information Processing Systems
| 2022. 1,2 |     | (NeurIPS),2021. | 1,2 |     |
| --------- | --- | --------------- | --- | --- |
[33] YoutianLin,ZuozhuoDai,SiyuZhu,andYaoYao.Gaussian- [45] Yi-LingQiao,AlexanderGao,andMingLin. Neuphysics:
flow: 4dreconstructionwithdynamic3dgaussianparticle. Editableneuralgeometryandphysicsfrommonocularvideos.
InProceedingsoftheIEEE/CVFConferenceonComputer Advances in Neural Information Processing Systems, 35:
VisionandPatternRecognition,pages21136–21145,2024. 12841–12854,2022. 2
| 1,2 |     | [46] TianheRen,ShilongLiu,AilingZeng,JingLin,Kunchang |     |     |
| --- | --- | ----------------------------------------------------- | --- | --- |
[34] JonathonLuiten,GeorgiosKopanas,BastianLeibe,andDeva Li,HeCao,JiayuChen,XinyuHuang,YukangChen,Feng
Ramanan. Dynamic 3d gaussians: Tracking by persistent Yan,etal. Groundedsam: Assemblingopen-worldmodels
dynamicviewsynthesis. In2024InternationalConference fordiversevisualtasks. arXivpreprintarXiv:2401.14159,
| on3DVision(3DV),pages800–809.IEEE,2024. | 1,2,7 | 2024. 2,4 |     |     |
| --------------------------------------- | ----- | --------- | --- | --- |

[47] JuniorRojas, EftychiosSifakis, andLadislavKavan. Dif- visionandpatternrecognition,pages20310–20320,2024. 1,
| ferentiable            | implicit soft-body | physics. | arXiv preprint |     | 2                                                      |     |     |     |     |
| ---------------------- | ------------------ | -------- | -------------- | --- | ------------------------------------------------------ | --- | --- | --- | --- |
| arXiv:2102.05791,2021. | 2                  |          |                |     |                                                        |     |     |     |     |
|                        |                    |          |                |     | [60] YilinWu,WilsonYan,ThanardKurutach,LerrelPinto,and |     |     |     |     |
[48] Robin Rombach, Andreas Blattmann, Dominik Lorenz, PieterAbbeel. Learningtomanipulatedeformableobjects
Patrick Esser, and Björn Ommer. High-resolution image withoutdemonstrations. arXivpreprintarXiv:1910.13439,
| synthesis | with latent diffusion | models. | In Proceedings | of  | 2019. 1,2 |     |     |     |     |
| --------- | --------------------- | ------- | -------------- | --- | --------- | --- | --- | --- | --- |
theIEEE/CVFconferenceoncomputervisionandpattern
|     |     |     |     |     | [61] WenqiXian,Jia-BinHuang,JohannesKopf,andChangilKim. |     |     |     |     |
| --- | --- | --- | --- | --- | ------------------------------------------------------- | --- | --- | --- | --- |
recognition,pages10684–10695,2022. 2,4 Space-timeneuralirradiancefieldsforfree-viewpointvideo.
[49] AlvaroSanchez-Gonzalez,JonathanGodwin,TobiasPfaff, InProceedingsoftheIEEE/CVFConferenceonComputer
RexYing,JureLeskovec,andPeterBattaglia. Learningto VisionandPatternRecognition(CVPR),pages9421–9431,
| simulatecomplexphysicswithgraphnetworks. |     |     | InInterna- |     | 2021. 1,2 |     |     |     |     |
| ---------------------------------------- | --- | --- | ---------- | --- | --------- | --- | --- | --- | --- |
tional conference on machine learning, pages 8459–8468. [62] JianfengXiang,ZelongLv,SichengXu,YuDeng,Ruicheng
| PMLR,2020. | 1,2 |     |     |     | Wang,BowenZhang,DongChen,XinTong,andJiaolong |     |     |     |     |
| ---------- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- |
[50] Paul-EdouardSarlin,DanielDeTone,TomaszMalisiewicz, Yang. Structured 3d latents for scalable and versatile 3d
andAndrewRabinovich. Superglue:Learningfeaturematch- generation. arXivpreprintarXiv:2412.01506,2024. 2,4,12
ing with graph neural networks. In Proceedings of the [63] TianyiXie,ZeshunZong,YuxingQiu,XuanLi,YutaoFeng,
IEEE/CVFconferenceoncomputervisionandpatternrecog- Yin Yang, and Chenfanfu Jiang. Physgaussian: Physics-
nition,pages4938–4947,2020. 4,12 integrated 3d gaussians for generative dynamics. In Pro-
[51] HaochenShi,HuazheXu,SamuelClarke,YunzhuLi,andJia- ceedingsoftheIEEE/CVFConferenceonComputerVision
|     |     |     |     |     | andPatternRecognition,pages4389–4398,2024. |     |     | 1,2 |     |
| --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- |
junWu.Robocook:Long-horizonelasto-plasticobjectmanip-
ulationwithdiversetools. arXivpreprintarXiv:2306.14447, [64] ZhenjiaXu,JiajunWu,AndyZeng,JoshuaBTenenbaum,
| 2023. 1,2 |     |     |     |     | andShuranSong. | Densephysnet: | Learningdensephysical |     |     |
| --------- | --- | --- | --- | --- | -------------- | ------------- | --------------------- | --- | --- |
[52] HaochenShi,HuazheXu,ZhiaoHuang,YunzhuLi,andJi- object representations via multi-step dynamic interactions.
|         |                                            |     |     |     | arXivpreprintarXiv:1906.03853,2019. |     | 1,2 |     |     |
| ------- | ------------------------------------------ | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- |
| ajunWu. | Robocraft: Learningtosee,simulate,andshape |     |     |     |                                     |     |     |     |     |
elasto-plasticobjectsin3dwithgraphnetworks. TheInterna- [65] ZeyuYang,HongyeYang,ZijiePan,andLiZhang.Real-time
tionalJournalofRoboticsResearch,43(4):533–549,2024. 1, photorealisticdynamicscenerepresentationandrendering
| 2   |     |     |     |     | with4dgaussiansplatting. |     | arXivpreprintarXiv:2310.10642, |     |     |
| --- | --- | --- | --- | --- | ------------------------ | --- | ------------------------------ | --- | --- |
2023. 1,2
| [53] OlgaSorkineandMarcAlexa. |     | As-rigid-as-possiblesurface |     |     |     |     |     |     |     |
| ----------------------------- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- |
modeling. In Symposium on Geometry processing, pages [66] Ziyi Yang, Xinyu Gao, Wen Zhou, Shaohui Jiao, Yuqing
109–116.Citeseer,2007. 4 Zhang,andXiaogangJin. Deformable3dgaussiansforhigh-
|                                                 |     |     |             |     | fidelitymonoculardynamicscenereconstruction. |            |             | InProceed- |     |
| ----------------------------------------------- | --- | --- | ----------- | --- | -------------------------------------------- | ---------- | ----------- | ---------- | --- |
| [54] RobertWSumner,JohannesSchmid,andMarkPauly. |     |     |             | Em- |                                              |            |             |            |     |
|                                                 |     |     |             |     | ings of the IEEE/CVF                         | conference | on computer | vision     | and |
| beddeddeformationforshapemanipulation.          |     |     | InSIGGRAPH, |     |                                              |            |             |            |     |
patternrecognition,pages20331–20341,2024.
| pages80–es.2007. | 5,12 |     |     |     |     |     |     | 1,2 |     |
| ---------------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
[55] EdgarTretschk,AyushTewari,VladislavGolyanik,Michael [67] HengYu,JoelJulin,ZoltanAMilacski,KoichiroNiinuma,
|                                                  |     |     |     |      | andLaszloAJeni.                            | Dylin: | Makinglightfieldnetworksdy- |     |     |
| ------------------------------------------------ | --- | --- | --- | ---- | ------------------------------------------ | ------ | --------------------------- | --- | --- |
| Zollhöfer,ChristophLassner,andChristianTheobalt. |     |     |     | Non- |                                            |        |                             |     |     |
|                                                  |     |     |     |      | namic. arXivpreprintarXiv:2303.14243,2023. |        |                             | 2   |     |
rigidneuralradiancefields:Reconstructionandnovelview
synthesis of a dynamic scene from monocular video. In [68] HengYu,JoelJulin,ZoltánÁMilacski,KoichiroNiinuma,
ProceedingsoftheIEEE/CVFInternationalConferenceon andLászlóAJeni. Cogs: Controllablegaussiansplatting.
ComputerVision,pages12959–12970,2021. 1,2 InProceedingsoftheIEEE/CVFConferenceonComputer
VisionandPatternRecognition,pages21624–21633,2024.
[56] EdgarTretschk,AyushTewari,VladislavGolyanik,Michael
1,2
| Zollhöfer,ChristophLassner,andChristianTheobalt. |     |     |     | Non- |     |     |     |     |     |
| ------------------------------------------------ | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
rigidneuralradiancefields:Reconstructionandnovelview [69] MingtongZhang,KaifengZhang,andYunzhuLi. Dynamic
synthesisofadynamicscenefrommonocularvideo. InIEEE 3dgaussiantrackingforgraph-basedneuraldynamicsmodel-
InternationalConferenceonComputerVision(ICCV).IEEE, ing. arXivpreprintarXiv:2410.18912,2024. 1,2,5,6,7,12,
14
2021. 1,2
[57] BinWang,LonghuaWu,KangKangYin,UriMAscher,Libin [70] RichardZhang,PhillipIsola,AlexeiAEfros,EliShechtman,
Liu,andHuiHuang. Deformationcaptureandmodelingof andOliverWang. Theunreasonableeffectivenessofdeep
|              |                                  |     |     |     | featuresasaperceptualmetric. |     | InCVPR,2018. | 7   |     |
| ------------ | -------------------------------- | --- | --- | --- | ---------------------------- | --- | ------------ | --- | --- |
| softobjects. | ACMTrans.Graph.,34(4):94–1,2015. |     |     | 2   |                              |     |              |     |     |
[58] ChaoyangWang,LachlanEwenMacDonald,LaszloAJeni, [71] TianyuanZhang,Hong-XingYu,RundiWu,BrandonYFeng,
and Simon Lucey. Flow supervision for deformable nerf. ChangxiZheng, NoahSnavely, JiajunWu, andWilliamT
InProceedingsoftheIEEE/CVFConferenceonComputer Freeman. Physdreamer: Physics-basedinteractionwith3d
|     |     |     |     |     | objects via video | generation. | In European | Conference | on  |
| --- | --- | --- | --- | --- | ----------------- | ----------- | ----------- | ---------- | --- |
VisionandPatternRecognition,pages21128–21137,2023.
|     |     |     |     |     | ComputerVision,pages388–406.Springer,2024. |     |     | 1,2 |     |
| --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- |
1,2
[59] GuanjunWu,TaoranYi,JieminFang,LingxiXie,Xiaopeng [72] LichengZhong,Hong-XingYu,JiajunWu,andYunzhuLi.
Zhang,WeiWei,WenyuLiu,QiTian,andXinggangWang. Reconstructionandsimulationofelasticobjectswithspring-
|     |     |     |     |     | mass3dgaussians. | InEuropeanConferenceonComputer |     |     |     |
| --- | --- | --- | --- | --- | ---------------- | ------------------------------ | --- | --- | --- |
4dgaussiansplattingforreal-timedynamicscenerendering.
|                |                 |            |             |     | Vision,pages407–423.Springer,2024. |     | 1,2,6,7,14 |     |     |
| -------------- | --------------- | ---------- | ----------- | --- | ---------------------------------- | --- | ---------- | --- | --- |
| In Proceedings | of the IEEE/CVF | conference | on computer |     |                                    |     |            |     |     |

| Supplement                             |     | Index |     |     |     |     |     |     |     |     |     |     |
| -------------------------------------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A.AdditionalDetailsfortheShapePrior    |     |       |     |     | 12  |     |     |     |     |     |     |     |
| B.AdditionalDetailsfor3DGaussianUpdate |     |       |     |     | 12  |     |     |     |     |     |     |     |
| C.AdditionalExperimentalDetails        |     |       |     |     | 12  |     |     |     |     |     |     |     |
| D.FutureWork                           |     |       |     |     | 16  |     |     |     |     |     |     |     |
Inthesupplement,weprovideadditionaldetailsofour
PhysTwinframework,morequalitativeresultsacrossdiffer-
|                                          |     |     |     |              |     | Figure6. | VisualizationofTrackingResults. |     |     |     | Wecomparethe |     |
| ---------------------------------------- | --- | --- | --- | ------------ | --- | -------- | ------------------------------- | --- | --- | --- | ------------ | --- |
| enttasks,andfurtheranalysisofourmethods. |     |     |     | Allthevideos |     |          |                                 |     |     |     |              |     |
trackingresultsproducedbyourPhysTwinwiththerawtracking
| showcasing | our | results | on various instances, | interactions, |     |     |     |     |     |     |     |     |
| ---------- | --- | ------- | --------------------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
resultsfromCoTracker3[23].OurPhysTwinachievesmorenatural
andtasksareavailableonourwebsite.
|     |     |     |     |     |     | and | smoother | movement | compared |     | to the raw predictions | from |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------- | -------- | --- | ---------------------- | ---- |
CoTracker3.
A.AdditionalDetailsfortheShapePrior
Asmentionedinthemainpaper,weleverageTRELLIS[62] nodeµˆt Xˆ . For3Dtranslations,weobtainthemfromthe
|             |     |           |                   |              |     |         | i   | t                    |     |                        |     |     |
| ----------- | --- | --------- | ----------------- | ------------ | --- | ------- | --- | -------------------- | --- | ---------------------- | --- | --- |
| to generate | the | full mesh | from a single RGB | observation. |     |         | ∈   |                      |     |                        |     |     |
|             |     |           |                   |              |     | predict | ed  | nod etranslationsTt. |     | For3Drotations,foreach |     |     |
i
However,thepotentialnon-rigidregistrationpresentsanon- vertex µˆt, we estimate a rigid local rotation Rt based on
|     |     |     |     |     |     |     | i   |     |     |     | i   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
trivialchallenge.
|     |     |     |     |     |     | motionsofitsneighbors |     |     |     | (i)fromtimettot+1: |     |     |
| --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | ------------------ | --- | --- |
N
Toaddresstheseissues,wedesignaregistrationmodule
(cid:88)
thatleverages2Dmatchingtohandlescaleestimation,rigid Rt R(µˆt µˆt) (µˆt+1 µˆt+1) 2.
|     |     |     |     |     |     |     | =arg | min |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
registration, andnon-rigid deformation. First, to estimate i R∈SO(3) ∥ j− i − j − i ∥
j∈N(i)
| theinitialrotation,weadoptacoarse-to-finestrategy. |     |     |     |     | We  |     |     |     |     |     |     | (5) |
| -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
useuniformlydistributedvirtualcamerasplacedonasphere
Inthenextstep,wetransformGaussiankernelsusingLinear
surroundingtheobjecttorenderimagesandmatch2Dcorre- BlendSkinning(LBS)[20,54,69]bylocallyinterpolating
spondencesusingSuperGlue[50]. Basedonthenumberof thetransformationsoftheirneighboringnodes. Specifically,
matches,weselecttheviewwiththemaximumnumberof
forthe3DcenterandrotationofeachGaussian:
| correspondences,providingaroughrotationestimate. |     |     |     |     | We  |     |     |     |     |     |     |     |
| ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:88)
then apply the Perspective-n-Point (PNP) algorithm to re- µt+1 = wt (Rt(µt µˆt)+µˆt +Tt) (6)
|     |     |     |     |     |     |     | j   |     | jk  | k j | k k | k   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
−
| finethe3Dmatchedpointsonthegeneratedmeshandthe |     |     |     |     |     |     |     | k∈N(j) |     |     |     |     |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- |
corresponding2Dpixelsintheobservation,estimatingthe
| preciserotationmatrix. |            |     |                       |           |     |     |     |      | (cid:88) |     |         |     |
| ---------------------- | ---------- | --- | --------------------- | --------- | --- | --- | --- | ---- | -------- | --- | ------- | --- |
|                        |            |     |                       |           |     |     |     | qt+1 | =(       | wt  | rt) qt, | (7) |
|                        |            |     |                       |           |     |     |     | j    |          | jk  | k j     |     |
| After                  | estimating | the | rotation, translation | and scale | am- |     |     |      |          |     | ⊗       |     |
k∈N(j)
| biguitiesmaystillexist.                             |     |     | Toresolvethese,weoptimizethe |     |     |         |     |      |       |     |                        |     |
| --------------------------------------------------- | --- | --- | ---------------------------- | --- | --- | ------- | --- | ---- | ----- | --- | ---------------------- | --- |
|                                                     |     |     |                              |     |     | whereRt |     | R3×3 | andrt | R4  | arethematrixandquater- |     |
| distancesbetweenmatchedpointpairstosolveforscaleand |     |     |                              |     |     |         | k   |      | k     |     |                        |     |
|                                                     |     |     |                              |     |     |         |     | ∈    |       | ∈   |                        |     |
translation. Thisissimplifiedinthecameracoordinatesys- nionformsoftherotationofvertexk; denotesthequater-
⊗
tem,asafterPNP,thematchedpointsinthegeneratedmesh nionmultiplyoperator; (j)representsK-nearestvertices
|     |     |     |     |     |     | ofaGaussiancenterµt;wt |     |     | N   |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- |
andthecorrespondingpointsintherealobservationpoint istheinterpolationweightsbe-
|     |     |     |     |     |     |     |     |     | j   | jk  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
cloudliealongthesamelineconnectingtheorigin. There- tweenaGaussianµt andacorrespondingvertexµˆt,which
|     |     |     |     |     |     |     |     |     | j   |     |     | k   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
fore,thescaleandtranslationoptimizationcanbereduced arederivedinverselyproportionaltotheir3Ddistance:
| to optimizing | only | the | scale. Once these | transformations |     |     |     |     |     |     |     |     |
| ------------- | ---- | --- | ----------------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
a re a pp l i e d , th e tw o o b je c ts s h o u ld b e i n s im il a r p o se s, w it h µt µˆ − 1
|     |     |     |     |     |     |     |     | t   |          | j   | k   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
|     |     |     |     |     |     |     |     | w = | (cid:80) | ∥ − | ∥   | (8) |
so m e p a r t s u n de rg oi n g n o n- r i g id d e fo r m a tio n s . T o h a nd l e j k µ t µˆ −1
|                                                       |     |     |     |     |     |     |     |     | k∈N(j)∥ |     | j k |     |
| ----------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- |
| suchdeformations,weuseanas-rigid-as-possibleregistra- |     |     |     |     |     |     |     |     |         |     | − ∥ |     |
tiontodeformthemeshintoanon-rigidposematchingthe toensurelargerweightsareassignedtothespatiallycloser
realobservation. Finally,weperformray-castingalignment, pairs. Finally, with the updated Gaussian parameters, we
shootingraysfromthecameratoensurethattheobserved are able to perform rendering at timestep with the
|     |     |     |     |     |     |     |     |     |     |     | t + 1 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- |
pointsalignwiththedeformedmeshandareneitheroccluded transformed3DGaussians.
noroccludethemesh.
C.AdditionalExperimentalDetails
B.AdditionalDetailsfor3DGaussianUpdate
|     |     |     |     |     |     | Due | to the | page limit | in the | main | paper, we provide | addi- |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---------- | ------ | ---- | ----------------- | ----- |
GiventhepreviousstateXˆ andthepredictedstateXˆ , tionalqualitativeresultsondifferentinstancesundervarious
|     |     |     | t   |     | t+1 |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
we first solve for the 6-DoF transformation of each mass interactions,aswellasfurtheranalysisexperiments.
12

noitavresbO
)sruO(
niwTsyhP
scimanyD-SG
suaG-gnirpS
noitavresbO
)sruO(
niwTsyhP
scimanyD-SG
suaG-gnirpS
noitavresbO
)sruO(
niwTsyhP
scimanyD-SG
suaG-gnirpS
Reconstruction & Resimulation t Future Prediction t
Figure7.AdditionalQualitativeResultsonReconstruction&ResimulationandFuturePrediction.

Table3.AblationsofOurSparse-to-DenseOptimization.Tobetterunderstandouroptimizationprocess,weconductablationexperiments
comparingresultswithonlyzero-orderoptimizationorfirst-orderoptimization.Theresultsdemonstratethatoursparse-to-denseoptimization
strategyiseffectiveinobtainingthemostaccuratephysicalparameters.
Task Reconstruction&Resimulation FuturePrediction
Method CD TrackError IoU% PSNR SSIM LPIPS CD TrackError IoU% PSNR SSIM LPIPS
↓ ↓ ↑ ↑ ↑ ↓ ↓ ↓ ↑ ↑ ↑ ↓
Zero-orderOnly 0.007 0.012 80.2 27.409 0.943 0.039 0.014 0.025 69.2 25.008 0.938 0.061
First-orderOnly 0.008 0.012 82.7 27.913 0.944 0.037 0.019 0.034 65.7 24.572 0.936 0.067
PhysTwin(Ours) 0.005 0.009 84.4 28.214 0.945 0.034 0.012 0.022 72.5 25.617 0.941 0.055
Observation Future Prediction t
)sruO(
niwTsyhP
scimanyD-SG
)sruO(
niwTsyhP
scimanyD-SG
)sruO(
niwTsyhP
scimanyD-SG
t
Figure8.AdditionalQualitativeResultsonGeneralizationtoUnseenInteractions.
Baselines. As described in the main paper, we select setup,weincorporateourshapepriorastheinitializationfor
twopriorworksforcomparison: Spring-Gaus[72]andGS- theirstaticGaussianconstruction. Sincetheirconstructed
Dynamics[69]. Gaussianslacktheabilitytogeneralizetodifferentinitial
ForSpring-Gaus,whileitdemonstratesreasonableperfor- conditions,weevaluatetheirapproachonlyonthefirsttwo
manceinmodelingobject-collisionvideos,itsapplicability tasks: reconstruction&resimulationandfutureprediction.
islimited torelativelysimplecaseswhere objectsprimar- ForGS-Dynamics,wecompareourmethodwiththeirs
ilydeformundergravity,restrictingtherangeofsupported acrossallthreetasks. ToenabletheGNN-baseddynamics
objecttypes. ToadaptSpring-Gaus[72]tooursetting,we modeltoproducerealisticrenderings,weaugmentitwithour
extenditbyintroducingsupportforcontrolpoints. Specif- Gaussianblendingstrategy,enhancingitsabilitytogenerate
ically, we add additional springs that connect the control high-qualityimages.
points to their neighboring object points within a prede- Tasks. PhysTwinisconstructedsolelyfromthetraining
fineddistance,enablingdirectoptimizationonourdataset. setofeachdatapoint,anditsperformanceisevaluatedbased
Furthermore,toensurecompatibilitywithoursparse-view onhowwellitmatchestheoriginalvideowithinthetestset.

1
tniopweiV
2
tniopweiV
3
tniopweiV
1
tniopweiV
2
tniopweiV
3
tniopweiV
1
tniopweiV
2
tniopweiV
3
tniopweiV
Reconstruction & Resimulation t Future Prediction t
Figure9.QualitativeResultsonReconstruction&ResimulationandFuturePredictionwithdifferentviewpoints.
Forthegeneralizationtask, wecreateadatasetconsisting setofthesourceinteractionbutisappliedacrosstheentire
ofinteractionpairsperformedonthesameobject. Forex- sequenceofthetargetinteraction.
ample, we construct PhysTwin for a sloth toy based on a
Qualitative Results. We present more qualitative re-
scenariowhereitisliftedwithonehandandthenevaluate
sults for different instances across various interactions on
its performance in a different scenario where its legs are
ourthreetasks: reconstruction&resimulation,futurepre-
stretched using both hands. The dataset includes 11 such
diction (Fig. 7), and generalization to unseen interactions
pairs, andsinceeachpairallowsfortwopossibletransfer
(Fig.8). Allresultsdemonstratethesuperiorperformanceof
directions(i.e.,fromoneinteractiontoanotherorviceversa),
ourmethodcomparedtopriorwork.
thisresultsinatotalof22generalizationexperiments.Inthis
DifferentViewpoints. Fig.9presentsthevisualization
task, PhysTwinisstillconstructedusingonlythetraining
oftherenderingresultsfromdifferentviewpoints,demon-

stratingtherobustnessofourPhysTwininhandlingvarious ios. Furthermore,whileourframeworkoptimizesphysical
viewpoints. parametersbasedonasingletypeofinteraction,expanding
AblationStudyonHierarchicalOptimization. Tobet- tomultipleactionmodalitiescouldfurtherenhancetheesti-
terunderstandtheimportanceofourhierarchicalsparse-to- mationofanobject’sintrinsicproperties. Learningfroma
denseoptimizationstrategy,weconductablationstudieswith broaderrangeofinteractionsmayrevealricherphysicalchar-
twovariants: oneusingonlyzero-orderoptimizationandthe acteristicsandimproverobustness. Beyondreconstruction
otherusingonlyfirst-orderoptimization. Theseexperiments andresimulation,ourmethodopensupexcitingpossibilities
areperformedonboththereconstruction&resimulationtask for downstream applications, particularly in robotics. By
andthefuturepredictiontask. Table3presentstheresults providingastructuredyetefficientdigitaltwin,ourapproach
of different variants. Our complete pipeline achieves the significantlysimplifiesreal-to-simtransfer,reducingthere-
bestperformanceacrossbothtasks. Thevariantwithonly lianceondomainrandomizationforreinforcementlearning.
zero-orderoptimizationfailstocapturefine-grainedmaterial Additionally,thehigh-speedsimulationandreal-timeren-
properties,limitingitsabilitytorepresentdifferentobjects. deringcapabilitiesofourframeworkpavethewayformore
On the other hand, the variant with only first-order dense effective model-based robotic planning. By bridging the
optimizationneglectstheoptimizationofnon-differentiable gapbetweenperceptionandphysics-basedsimulation,our
parameters, such as the spring connections. The default methodlaysasolidfoundationforfutureadvancementsin
connections fail to accurately model the real object struc- bothcomputervisionandrobotics.
| ture, and | the connection |     | distances | between | control | points |
| --------- | -------------- | --- | --------- | ------- | ------- | ------ |
andobjectpointscannotbeeffectivelyhandledwithafixed
initializationvalue.
| TrackingResults. |         | Fig.6showsthevisualizationofour  |           |          |         |      |
| ---------------- | ------- | -------------------------------- | --------- | -------- | ------- | ---- |
| tracking         | results | and the                          | pseudo-GT | tracking | results | from |
| CoTracker3[23].  |         | EventhoughourPhysTwinisoptimized |           |          |         |      |
withnoisyGTtracking,ourmodelachievesmuchbetterand
smoothertrackingresultsduringboththereconstruction&
resimulationandfuturepredictiontasks.
| Data | Efficiency | Experiment. |     | To  | further analyze | the |
| ---- | ---------- | ----------- | --- | --- | --------------- | --- |
performancedifferencebetweenourmethodandtheGNN-
basedapproach,wecollected29additionaldatapointson
thesamemotion(double-handstretchingandfoldingrope),
| bringing           | the total     | to 30                             | data points | for                     | training | the neural |
| ------------------ | ------------- | --------------------------------- | ----------- | ----------------------- | -------- | ---------- |
| dynamicsmodel.     |               | Incontrast,                       |             | ourmethodistrainedusing |          |            |
| only1datapoint.    |               | TheresultsshowthatGS-Dynamicsdoes |             |                         |          |            |
| not show           | a performance |                                   | boost       | even with               | 30 times | more       |
| datathanourmethod. |               | Thisindicatesthattheirapproachis  |             |                         |          |            |
data-hungry,whereasourmethoddemonstratessignificantly
betterdataefficiencyinlearningausefuldynamicsmodel.
Evenwith30timesmoredata,thelearning-basedmethod
stillstrugglestocaptureprecisedynamicsaseffectivelyas
ourapproach.
D.FutureWork
Ourworktakesanimportantsteptowardsconstructingan
effectivephysicaldigitaltwinfordeformableobjectsfrom
| sparse video | observations. |     | Unlike | existing | methods | that |
| ------------ | ------------- | --- | ------ | -------- | ------- | ---- |
primarilyfocusongeometricreconstruction,ourapproach
integratesphysicalproperties,enablingaccurateresimula-
tion,futureprediction,andgeneralizationtounseeninterac-
tions. DespiteusingthreeRGBDviewsinourcurrentsetup,
ourframeworkisinherentlyflexibleandcanextendtoeven
| sparserobservations. |       | Withappropriatepriors,asingleRGB |     |     |          |              |
| -------------------- | ----- | -------------------------------- | --- | --- | -------- | ------------ |
| video could          | serve | as a promising                   |     | and | scalable | alternative, |
makingourapproachmoreapplicabletoin-the-wildscenar-