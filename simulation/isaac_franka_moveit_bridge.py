#!/usr/bin/env python3
"""
isaac_franka_moveit_bridge.py

Stage 2/3 -- Isaac Sim standalone script: the "simulated hardware" half of the
first end-to-end MoveIt2 + PINN-controller pipeline (Path B, see SESSION.md).

WHAT THIS IS
------------
Loads the Franka Panda into Isaac Sim and wires up Isaac's ROS2 bridge
(isaacsim.ros2.bridge) via an OmniGraph action graph so an external ROS2
system can read joint states and command joint efforts. This is a close
adaptation of NVIDIA's own reference example
(~/isaac-sim/standalone_examples/api/isaacsim.ros2.bridge/moveit.py),
using the same corrected Franka USD asset path as generate_isaac_dataset.py.

Topics (fixed names -- these are what isaac_moveit and pinn_controller_node
are configured to use):
    isaac_joint_states    (sensor_msgs/JointState, published every tick)
    isaac_joint_commands  (sensor_msgs/JointState, subscribed; position,
                           velocity, and effort fields are all wired through
                           to IsaacArticulationController, which applies
                           whichever fields are populated -- effort-only
                           commands, as sent by pinn_controller_node, work
                           directly with no extra configuration)

MILESTONE 1 (current): run this script, then `ros2 launch isaac_moveit
isaac_moveit.launch.py` (from github.com/isaac-sim/IsaacSim-ros_workspaces,
jazzy_ws) to confirm MoveIt2 can plan and execute against this bridge at all
-- isaac_moveit's default execution path drives isaac_joint_commands with
position commands directly, bypassing pinn_controller_node. This validates
the ROS2 Jazzy + MoveIt2 + Isaac Sim wiring in isolation.

MILESTONE 2 (follow-up): reroute the planned trajectory into
pinn_controller_node's /pinn_controller/desired_trajectory topic instead, so
the Stage 3 PINN computed-torque + PD controller is what actually publishes
to isaac_joint_commands (as effort, not position). No changes to this script
should be needed for that -- it already exposes effort commands.

USAGE -- run from inside Isaac Sim's Python environment (not system Python):

    cd /path/to/isaac-sim-root
    ./python.sh /path/to/pinn_franka/simulation/isaac_franka_moveit_bridge.py

Then in a separate terminal (system ROS2 Jazzy):

    ros2 launch isaac_moveit isaac_moveit.launch.py

PREREQUISITES:
    - Isaac Sim 6.0.1 installed (same as generate_isaac_dataset.py)
    - ROS2 Jazzy + MoveIt2 installed system-wide (not inside Isaac Sim's Python)
    - isaacsim.ros2.bridge extension available (bundled with Isaac Sim)
"""

import argparse
import sys

import numpy as np
from isaacsim import SimulationApp

parser = argparse.ArgumentParser()
parser.add_argument("--test", default=False, action="store_true", help="Run in test mode (exit after a few frames)")
args, _ = parser.parse_known_args()

# Same asset path as generate_isaac_dataset.py -- keep these in sync.
FRANKA_STAGE_PATH = "/Franka"
FRANKA_USD_REL = "/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd"
BACKGROUND_STAGE_PATH = "/background"
BACKGROUND_USD_REL = "/Isaac/Environments/Simple_Room/simple_room.usd"

CONFIG = {"renderer": "RealTimePathTracing", "headless": False}

simulation_app = SimulationApp(CONFIG)

import carb
import isaacsim.core.experimental.utils.app as app_utils
import isaacsim.core.experimental.utils.stage as stage_utils
import omni.graph.core as og
import usdrt.Sdf
from isaacsim.core.experimental.utils.prim import get_prim_at_path
from isaacsim.core.rendering_manager import ViewportManager
from isaacsim.core.simulation_manager import SimulationManager
from isaacsim.storage.native import get_assets_root_path
from pxr import Gf, UsdGeom

# Enable the ROS2 bridge extension.
app_utils.enable_extension("isaacsim.ros2.bridge")
simulation_app.update()

stage_utils.set_stage_units(meters_per_unit=1.0)

assets_root_path = get_assets_root_path()
if assets_root_path is None:
    carb.log_error("Could not find Isaac Sim assets folder")
    simulation_app.close()
    sys.exit(1)

ViewportManager.set_camera_view("/OmniverseKit_Persp", eye=np.array([1.2, 1.2, 0.8]), target=np.array([0, 0, 0.5]))

stage_utils.add_reference_to_stage(assets_root_path + BACKGROUND_USD_REL, BACKGROUND_STAGE_PATH)

stage_utils.add_reference_to_stage(assets_root_path + FRANKA_USD_REL, FRANKA_STAGE_PATH)
robot = get_prim_at_path(FRANKA_STAGE_PATH)
xform_api = UsdGeom.XformCommonAPI(robot)
xform_api.SetTranslate(Gf.Vec3d(0, -0.64, 0))
xform_api.SetRotate((0, 0, 90), UsdGeom.XformCommonAPI.RotationOrderXYZ)

robot.GetVariantSet("Gripper").SetVariantSelection("AlternateFinger")
robot.GetVariantSet("Mesh").SetVariantSelection("Quality")

simulation_app.update()

# Action graph: publish joint state every tick, subscribe to joint commands
# (position/velocity/effort -- pinn_controller_node uses effort only), and
# drive the articulation controller from whichever fields are populated.
try:
    og.Controller.edit(
        {"graph_path": "/ActionGraph", "evaluator_name": "execution"},
        {
            og.Controller.Keys.CREATE_NODES: [
                ("OnPlaybackTick", "omni.graph.action.OnPlaybackTick"),
                ("ReadSimTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),
                ("ReadJointState", "isaacsim.sensors.physics.IsaacReadJointState"),
                ("Context", "isaacsim.ros2.bridge.ROS2Context"),
                ("PublishJointState", "isaacsim.ros2.bridge.ROS2PublishJointState"),
                ("SubscribeJointState", "isaacsim.ros2.bridge.ROS2SubscribeJointState"),
                ("ArticulationController", "isaacsim.core.nodes.IsaacArticulationController"),
                ("PublishClock", "isaacsim.ros2.bridge.ROS2PublishClock"),
            ],
            og.Controller.Keys.CONNECT: [
                ("OnPlaybackTick.outputs:tick", "ReadJointState.inputs:execIn"),
                ("ReadJointState.outputs:execOut", "PublishJointState.inputs:execIn"),
                ("ReadJointState.outputs:jointNames", "PublishJointState.inputs:jointNames"),
                ("ReadJointState.outputs:jointPositions", "PublishJointState.inputs:jointPositions"),
                ("ReadJointState.outputs:jointVelocities", "PublishJointState.inputs:jointVelocities"),
                ("ReadJointState.outputs:jointEfforts", "PublishJointState.inputs:jointEfforts"),
                ("ReadJointState.outputs:jointDofTypes", "PublishJointState.inputs:jointDofTypes"),
                ("ReadJointState.outputs:stageMetersPerUnit", "PublishJointState.inputs:stageMetersPerUnit"),
                ("ReadJointState.outputs:sensorTime", "PublishJointState.inputs:sensorTime"),
                ("OnPlaybackTick.outputs:tick", "SubscribeJointState.inputs:execIn"),
                ("OnPlaybackTick.outputs:tick", "PublishClock.inputs:execIn"),
                ("OnPlaybackTick.outputs:tick", "ArticulationController.inputs:execIn"),
                ("Context.outputs:context", "PublishJointState.inputs:context"),
                ("Context.outputs:context", "SubscribeJointState.inputs:context"),
                ("Context.outputs:context", "PublishClock.inputs:context"),
                ("ReadSimTime.outputs:simulationTime", "PublishClock.inputs:timeStamp"),
                ("SubscribeJointState.outputs:jointNames", "ArticulationController.inputs:jointNames"),
                (
                    "SubscribeJointState.outputs:positionCommand",
                    "ArticulationController.inputs:positionCommand",
                ),
                (
                    "SubscribeJointState.outputs:velocityCommand",
                    "ArticulationController.inputs:velocityCommand",
                ),
                ("SubscribeJointState.outputs:effortCommand", "ArticulationController.inputs:effortCommand"),
            ],
            og.Controller.Keys.SET_VALUES: [
                ("ArticulationController.inputs:robotPath", FRANKA_STAGE_PATH),
                ("ReadJointState.inputs:prim", [usdrt.Sdf.Path(FRANKA_STAGE_PATH)]),
                ("PublishJointState.inputs:topicName", "isaac_joint_states"),
                ("SubscribeJointState.inputs:topicName", "isaac_joint_commands"),
            ],
        },
    )
except Exception as e:
    print(e)

simulation_app.update()

SimulationManager.setup_simulation(dt=1.0 / 60.0, device="cpu")

app_utils.play()
simulation_app.update()

frame_count = 0
while simulation_app.is_running():
    simulation_app.update()
    frame_count += 1
    if args.test and frame_count >= 10:
        break

app_utils.stop()
simulation_app.close()
