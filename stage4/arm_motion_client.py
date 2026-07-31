"""
ArmMotionClient — Stage 4's arm-motion backend for GraspExecutor._move_arm().

Converts a Cartesian target_pose (a (4, 4) homogeneous transform in the
Franka base frame, see demo_targets.py's convention) into arm motion by:
  1. Planning a Cartesian-goal MoveGroup request. MoveIt2's own KDL IK
     solver (moveit_resources_panda_moveit_config's kinematics.yaml) handles
     the pose -> joint conversion internally -- no separate IK step needed.
  2. Handing the resulting trajectory to the already-running
     pinn_controller_node (Stage 3's ComputedTorquePDController) via
     /pinn_controller/desired_trajectory -- the exact same plan-then-handoff
     pattern ros2_ws/.../moveit_plan_bridge.py already validated during
     Milestone 2, just parameterized by pose instead of joint values, and
     wrapped as a reusable class (instantiate once, call move_to() many
     times across a pick sequence) instead of a one-shot CLI script.
  3. Waiting for the trajectory to actually play out (Stage 3's own 1 kHz
     loop, not this node) and confirming the arm's /joint_states converged
     near the planned trajectory's own last waypoint, not just that the
     handoff itself succeeded.

Requires a live ROS2 environment (move_group + pinn_controller_node already
running, see moveit_plan_bridge.py's own Usage docstring for the manual
launch sequence this depends on) and the caller to have already called
rclpy.init() -- this class does not call it itself, unlike
MuJoCoGripperController, since GraspExecutor's future ROS2 orchestration node
is expected to own one shared rclpy context across the arm client, the
gripper controller, and its own node.
"""

from __future__ import annotations

import os
import time
from typing import Optional

import numpy as np

# 2026-07-23 (Opus 4.8): pinocchio is used ONLY for a lightweight forward-
# kinematics (FK) convergence check (see move_to()'s docstring and the
# _FlangeFK helper). It is guarded exactly like pinocchio_baseline/
# rnea_wrapper.py's own optional import so this file still imports (and
# move_to() still runs, degrading to the old joint-space check) in an
# environment where pinocchio isn't installed -- e.g. a bare rclpy runtime
# without the Stage 1 training deps. pinocchio is NOT a new SYSTEM dependency:
# it is already required and imported elsewhere in this project's Python env
# (rnea_wrapper.py, controller/computed_torque_pd.py's RNEA path that
# pinn_controller_node.py loads); this is only a new import in THIS file, and
# it is FK-only (buildModel + one forwardKinematics call), not the heavier
# dynamics path.
try:
    import pinocchio as pin

    _HAS_PINOCCHIO = True
except ImportError:  # keep this file importable/usable without pinocchio
    _HAS_PINOCCHIO = False

import rclpy
from geometry_msgs.msg import Pose
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import (
    AttachedCollisionObject,
    CollisionObject,
    Constraints,
    MoveItErrorCodes,
    OrientationConstraint,
    PlanningScene,
    PositionConstraint,
)
from moveit_msgs.srv import ApplyPlanningScene
from rclpy.action import ActionClient
from rclpy.node import Node
from sensor_msgs.msg import JointState
from shape_msgs.msg import SolidPrimitive
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

# Matches pinocchio_baseline/panda.urdf and pinn_controller_node.py's own
# _JOINT_NAMES -- the arm's 7 joints, in canonical order (NOT /joint_states'
# own alphabetical-sort order, which puts the 2 finger joints first).
_JOINT_NAMES = [f"panda_joint{i}" for i in range(1, 8)]


def _rotation_matrix_to_quaternion(R: np.ndarray) -> tuple[float, float, float, float]:
    """Convert a 3x3 rotation matrix to a (x, y, z, w) quaternion (Shepperd's method)."""
    trace = np.trace(R)
    if trace > 0:
        s = 0.5 / np.sqrt(trace + 1.0)
        w = 0.25 / s
        x = (R[2, 1] - R[1, 2]) * s
        y = (R[0, 2] - R[2, 0]) * s
        z = (R[1, 0] - R[0, 1]) * s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = 2.0 * np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2])
        w = (R[2, 1] - R[1, 2]) / s
        x = 0.25 * s
        y = (R[0, 1] + R[1, 0]) / s
        z = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = 2.0 * np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2])
        w = (R[0, 2] - R[2, 0]) / s
        x = (R[0, 1] + R[1, 0]) / s
        y = 0.25 * s
        z = (R[1, 2] + R[2, 1]) / s
    else:
        s = 2.0 * np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1])
        w = (R[1, 0] - R[0, 1]) / s
        x = (R[0, 2] + R[2, 0]) / s
        y = (R[1, 2] + R[2, 1]) / s
        z = 0.25 * s
    return (x, y, z, w)


# Path to the same URDF pinocchio_baseline/rnea_wrapper.py builds its RNEA
# model from -- resolved relative to THIS file so it works regardless of the
# caller's cwd (a ROS2 orchestration node may launch from anywhere). This is
# the analytical Franka kinematic chain (base panda_link0 -> flange
# panda_link8), the exact chain MoveIt2 plans against for tip_link.
_DEFAULT_URDF_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "pinocchio_baseline", "panda.urdf")
)


class _FlangeFK:
    """
    Minimal pinocchio forward-kinematics helper: joint angles -> flange
    (panda_link8) position in the base frame.

    2026-07-23 (Opus 4.8): built to replace ArmMotionClient's old uniform
    per-joint radian convergence check with a physically meaningful CARTESIAN
    one. The old check applied ONE tolerance to the max abs joint error across
    all 7 joints -- crude, because a given angular error on a base joint
    (panda_joint1, ~0.8 m lever arm to the flange) moves the fingertip far
    more than the SAME error on a wrist joint (panda_joint5/6/7, ~0.14 m lever
    arm). No single radian number is simultaneously correct for both, so a
    tolerance tight enough to matter at the base spuriously times out on a
    wrist joint that is Cartesian-irrelevant. FK collapses all 7 joint errors
    into the one quantity that actually matters for a grasp: how far the flange
    is from where it should be, in metres.

    Reuses rnea_wrapper.py's exact model-reduction recipe: buildModelFromUrdf
    then buildReducedModel locking the 2 finger joints, so the configuration
    vector is the same 7-arm-joint vector everything else in this project uses.
    FK-only (forwardKinematics + updateFramePlacements) -- no dynamics, no
    data allocation per call beyond pinocchio's own reusable Data.
    """

    def __init__(self, urdf_path: str, tip_link: str) -> None:
        full_model = pin.buildModelFromUrdf(urdf_path)
        finger_joints = ["panda_finger_joint1", "panda_finger_joint2"]
        joints_to_lock = [
            full_model.getJointId(j)
            for j in finger_joints
            if full_model.existJointName(j)
        ]
        reference_q = pin.neutral(full_model)
        self.model = pin.buildReducedModel(full_model, joints_to_lock, reference_q)
        self.data = self.model.createData()
        if not self.model.existFrame(tip_link):
            raise ValueError(f"_FlangeFK: frame {tip_link!r} not found in {urdf_path}")
        self.frame_id = self.model.getFrameId(tip_link)

    def _update_frame(self, joint_values: dict) -> None:
        """Run FK for the given {joint_name: angle} mapping and update
        self.data.oMf[self.frame_id] in place. Shared by flange_position and
        flange_pose so both stay in sync with a single FK evaluation recipe.
        """
        q = pin.neutral(self.model)
        for name, val in joint_values.items():
            if self.model.existJointName(name):
                jid = self.model.getJointId(name)
                q[self.model.idx_qs[jid]] = val
        pin.forwardKinematics(self.model, self.data, q)
        pin.updateFramePlacements(self.model, self.data)

    def flange_position(self, joint_values: dict) -> np.ndarray:
        """
        Return the flange position [x, y, z] in the base frame for the given
        {joint_name: angle} mapping.

        Values are placed into the configuration vector BY NAME (via the
        model's own idx_qs), never by positional slice -- the same by-name
        discipline the rest of this class and pinn_controller_node use, so it
        is robust to /joint_states' 9-joint alphabetical ordering (extra
        finger joints in the dict are simply ignored; the 7 arm joints must
        all be present).
        """
        self._update_frame(joint_values)
        return np.asarray(self.data.oMf[self.frame_id].translation, dtype=float)

    def flange_pose(self, joint_values: dict) -> np.ndarray:
        """
        Return the full (4, 4) homogeneous transform of the flange in the
        base frame for the given {joint_name: angle} mapping (position +
        orientation, unlike flange_position which is translation-only).

        2026-07-24: added so GraspExecutor can interpolate a full SE(3) path
        (position AND orientation) from the arm's actual current pose to a
        target waypoint, instead of only ever interpolating position between
        two poses that already share an orientation (see
        GraspExecutor._interpolate_pose_waypoints's docstring for why this
        matters for the home->pre-approach leg specifically).
        """
        self._update_frame(joint_values)
        T = np.eye(4)
        T[:3, :3] = np.asarray(self.data.oMf[self.frame_id].rotation, dtype=float)
        T[:3, 3] = np.asarray(self.data.oMf[self.frame_id].translation, dtype=float)
        return T


class ArmMotionClient(Node):
    """
    Args:
        node_name: Name of the ROS2 node this class creates.
        group_name: MoveIt2 planning group, default "panda_arm".
        base_frame: Planning/base frame, matches demo_targets.py's convention.
        tip_link: IK reference link, matches panda.srdf's panda_arm chain
            tip_link (confirmed: base_link="panda_link0" tip_link="panda_link8").
            NOTE: this is the flange link, not necessarily the fingertip TCP --
            demo_targets.py's existing hardcoded poses were written before any
            real IK integration existed and may need recalibrating once a real
            pick is actually attempted; not resolved here.
        planning_time: allowed_planning_time per MoveGroup request [s].
        position_tolerance: radius [m] of the spherical position constraint region.
        orientation_tolerance: per-axis orientation tolerance [rad].
    """

    def __init__(
        self,
        node_name: str = "stage4_arm_motion",
        group_name: str = "panda_arm",
        base_frame: str = "panda_link0",
        tip_link: str = "panda_link8",
        planning_time: float = 5.0,
        position_tolerance: float = 0.01,
        orientation_tolerance: float = 0.05,
        urdf_path: Optional[str] = None,
    ) -> None:
        super().__init__(node_name)
        self._group_name = group_name
        self._base_frame = base_frame
        self._tip_link = tip_link
        self._planning_time = planning_time
        self._position_tolerance = position_tolerance
        self._orientation_tolerance = orientation_tolerance

        # 2026-07-23 (Opus 4.8): build the FK model once, guarded. If pinocchio
        # isn't importable, or the URDF can't be loaded for any reason, we log
        # ONCE here and fall back to the legacy joint-space convergence check in
        # move_to() (with a per-call warning), rather than crashing a live
        # pick. self._fk is None => fallback mode.
        self._fk: Optional[_FlangeFK] = None
        if _HAS_PINOCCHIO:
            try:
                self._fk = _FlangeFK(urdf_path or _DEFAULT_URDF_PATH, tip_link)
                self.get_logger().info(
                    "ArmMotionClient: FK-based Cartesian convergence check enabled "
                    f"(flange frame {tip_link!r}, model {urdf_path or _DEFAULT_URDF_PATH!r})"
                )
            except Exception as exc:  # noqa: BLE001 -- any FK build failure -> fallback
                self.get_logger().warning(
                    f"ArmMotionClient: FK model build failed ({exc!r}); falling back "
                    "to legacy joint-space (per-radian) convergence check"
                )
                self._fk = None
        else:
            self.get_logger().warning(
                "ArmMotionClient: pinocchio not available; falling back to legacy "
                "joint-space (per-radian) convergence check"
            )

        self._pub_trajectory = self.create_publisher(
            JointTrajectory, "/pinn_controller/desired_trajectory", 10
        )
        self._action_client = ActionClient(self, MoveGroup, "move_action")
        self._joint_state: Optional[JointState] = None
        self.create_subscription(JointState, "/joint_states", self._joint_state_cb, 10)

        # 2026-07-23 (Opus 4.8): MoveIt2 planning-scene client. NEW ROOT CAUSE
        # found live this date -- grasp_object (the 4cm cube) exists ONLY in
        # the MuJoCo physics world (panda_arm_mujoco.xml's <body
        # name="grasp_object">); it was NEVER registered as a MoveIt2 collision
        # object, so OMPL treated that volume as free space and planned the
        # home -> pre-approach move straight THROUGH the cube's real location.
        # MuJoCo's real physics then generated a genuine contact, the arm got
        # pinned against the cube, and its commanded torque was absorbed by the
        # contact constraint -- the EXACT same "substantial torque, zero
        # motion, joints frozen bit-for-bit" signature as the earlier (already
        # fixed) arm-self-collision bug, but confirmed live (viewer 'C' contact
        # viz) to be contacts clustered AROUND THE CUBE, not the arm's own
        # wrist. This is a PLANNING-scene problem (the planner is blind to the
        # obstacle), NOT a physics-model problem, and is fixed by
        # add_collision_box() below making MoveIt2 aware of the cube so it
        # routes every future plan around it.
        #
        # The /apply_planning_scene SERVICE is used (not a fire-and-forget
        # publish to the /planning_scene topic) because a grasp needs a
        # guaranteed "the scene is applied BEFORE I plan the next move"
        # ordering -- the service call returns only once move_group has
        # actually processed the diff, whereas a topic publish can race the
        # very next MoveGroup plan and silently not be in effect yet.
        # move_group serves /apply_planning_scene by default (its
        # PlanningSceneMonitor publishes it), so no launch/config change is
        # needed. NOT YET LIVE-VALIDATED (no simulator access during this pass).
        self._apply_scene_client = self.create_client(
            ApplyPlanningScene, "/apply_planning_scene"
        )

    def _joint_state_cb(self, msg: JointState) -> None:
        self._joint_state = msg

    def _current_joint_positions_by_name(self) -> Optional[dict]:
        """
        Return {joint_name: position} from the latest /joint_states message.

        Looked up BY NAME, not a fixed positional slice: /joint_states carries
        9 joints (7 arm + 2 fingers), alphabetically sorted by
        joint_state_broadcaster -- the exact class of bug already found and
        fixed in pinn_controller_node.py (2026-07-21) from assuming a fixed
        slice on this same topic.
        """
        if self._joint_state is None:
            return None
        return dict(zip(self._joint_state.name, self._joint_state.position))

    def get_current_pose(self) -> Optional[np.ndarray]:
        """
        Return the arm's CURRENT flange pose as a (4, 4) homogeneous transform,
        via FK on the latest /joint_states reading.

        Returns None if pinocchio/FK isn't available (_HAS_PINOCCHIO False) or
        no /joint_states message has been received yet -- callers (e.g.
        GraspExecutor's pre-approach waypoint split) must fall back to a
        single direct move_to() in that case, exactly like the Cartesian
        convergence check itself already falls back to the radian check when
        FK is unavailable.
        """
        if self._fk is None:
            return None
        # Same DDS-discovery grace pattern used elsewhere in this class
        # (e.g. move_to()'s post-publish wait): if no /joint_states message
        # has arrived yet (this can be the very first call this node makes,
        # before its own move_to() loop has had a chance to spin), give the
        # subscription a short, bounded window to receive one instead of
        # returning None immediately and silently losing the waypoint split.
        for _ in range(20):
            if self._joint_state is not None:
                break
            rclpy.spin_once(self, timeout_sec=0.05)
        current_by_name = self._current_joint_positions_by_name()
        if current_by_name is None:
            return None
        return self._fk.flange_pose(current_by_name)

    # ------------------------------------------------------------------
    # MoveIt2 planning-scene awareness (2026-07-23, Opus 4.8)
    #
    # These methods keep MoveIt2's collision world in sync with the physical
    # MuJoCo scene so OMPL routes around real obstacles instead of planning
    # through them. Stage-4-only: they call MoveIt2's public
    # /apply_planning_scene service exclusively -- no Stage 1/2/3 code, no
    # launch/xacro/config change. Kept deliberately GENERAL (any named box /
    # any attach) rather than hardcoding grasp_object's numbers here; the
    # cube's literal size/pose lives in the caller (test_grasp_pick.py /
    # a future orchestration node), matching demo_targets.py's own placement.
    # ------------------------------------------------------------------

    def _apply_planning_scene(
        self, scene: PlanningScene, description: str, timeout_sec: float = 5.0
    ) -> bool:
        """Send a PlanningScene diff via /apply_planning_scene, waiting for the
        service response so the caller can rely on it being in effect before
        the next plan. Returns True on success=True, False on any failure
        (service missing, timeout, or success=False) -- never raises, so a
        scene-sync hiccup degrades to a logged error rather than aborting a
        live pick mid-sequence."""
        if not self._apply_scene_client.wait_for_service(timeout_sec=timeout_sec):
            self.get_logger().error(
                f"{description}: /apply_planning_scene service not available "
                "(is move_group running?)"
            )
            return False
        request = ApplyPlanningScene.Request()
        request.scene = scene
        future = self._apply_scene_client.call_async(request)
        deadline = time.monotonic() + timeout_sec
        while not future.done():
            rclpy.spin_once(self, timeout_sec=0.05)
            if time.monotonic() > deadline:
                self.get_logger().error(
                    f"{description}: timed out waiting for /apply_planning_scene response"
                )
                return False
        response = future.result()
        success = bool(response is not None and response.success)
        if success:
            self.get_logger().info(f"{description}: applied to MoveIt2 planning scene")
        else:
            self.get_logger().error(
                f"{description}: /apply_planning_scene returned success=False"
            )
        return success

    def add_collision_box(
        self,
        name: str,
        position,
        size,
        frame_id: Optional[str] = None,
    ) -> bool:
        """Register (or replace) a box collision object in MoveIt2's world so
        every future plan routes around it.

        Args:
            name: unique object id (MoveIt uses this as the handle for later
                remove/attach/detach).
            position: (x, y, z) box CENTER in `frame_id` [m].
            size: (sx, sy, sz) FULL box extents [m] (not half-extents) -- for
                grasp_object pass (0.04, 0.04, 0.04), i.e. twice the MJCF geom
                half-size "0.02 0.02 0.02".
            frame_id: frame the position is expressed in; defaults to this
                client's base_frame (panda_link0), matching demo_targets.py's
                pose convention and the MJCF body pos of grasp_object.

        The pose is placed on the CollisionObject's top-level `pose` (with an
        explicit identity quaternion w=1) and the SolidPrimitive is given an
        identity `primitive_pose` -- both quaternions set explicitly because a
        default-constructed geometry_msgs/Pose has an ALL-ZERO orientation,
        which is an invalid quaternion MoveIt/tf2 will reject. is_diff=True so
        this only ADDS the object without wiping any other scene contents.
        """
        frame = frame_id or self._base_frame

        obj = CollisionObject()
        obj.header.frame_id = frame
        obj.id = name
        obj.operation = CollisionObject.ADD

        obj.pose.position.x = float(position[0])
        obj.pose.position.y = float(position[1])
        obj.pose.position.z = float(position[2])
        obj.pose.orientation.w = 1.0  # explicit valid quaternion (see docstring)

        primitive = SolidPrimitive()
        primitive.type = SolidPrimitive.BOX
        primitive.dimensions = [float(size[0]), float(size[1]), float(size[2])]
        obj.primitives.append(primitive)

        primitive_pose = Pose()
        primitive_pose.orientation.w = 1.0  # identity, relative to obj.pose
        obj.primitive_poses.append(primitive_pose)

        scene = PlanningScene()
        scene.is_diff = True
        scene.world.collision_objects.append(obj)
        return self._apply_planning_scene(
            scene, f"add_collision_box({name!r}, size={tuple(float(s) for s in size)})"
        )

    def remove_collision_object(self, name: str) -> bool:
        """Remove a previously-added collision object (by id) from the world."""
        obj = CollisionObject()
        obj.id = name
        obj.header.frame_id = self._base_frame
        obj.operation = CollisionObject.REMOVE
        scene = PlanningScene()
        scene.is_diff = True
        scene.world.collision_objects.append(obj)
        return self._apply_planning_scene(scene, f"remove_collision_object({name!r})")

    # Default links the attached object is allowed to touch without that
    # counting as a collision -- the hand + both fingers, matching panda.srdf's
    # own `hand` group (panda_hand / panda_leftfinger / panda_rightfinger),
    # plus panda_link8 (the flange, immediately above panda_hand -- a 4cm box
    # attached at the hand can poke up near it, and we don't want that read as
    # a self-collision). The attach LINK itself is auto-included by MoveIt, but
    # listing them explicitly is harmless and clearer.
    _DEFAULT_ATTACH_LINK = "panda_hand"
    _DEFAULT_TOUCH_LINKS = [
        "panda_hand",
        "panda_leftfinger",
        "panda_rightfinger",
        "panda_link8",
    ]

    def attach_object(
        self,
        name: str,
        link: Optional[str] = None,
        touch_links: Optional[list] = None,
    ) -> bool:
        """Attach an EXISTING world collision object to a gripper link.

        WHY THIS IS NEEDED, AND WHY IT IS CALLED BEFORE THE GRASP (2026-07-23,
        Opus 4.8): once grasp_object is a MoveIt2 world obstacle (via
        add_collision_box), MoveIt2 will refuse to plan a path whose finger
        links end up straddling / touching that obstacle -- which is EXACTLY
        what the final approach + grasp poses do (open fingers, 0.08 m, around
        a 0.04 m cube => ~0.02 m nominal side clearance, well inside default
        link padding). Left as a plain world obstacle, registering the cube
        would fix the reported home->pre-approach sweep-through bug but NEWLY
        break the approach/grasp descent that was previously working from a
        non-home start. Attaching converts the object from a world obstacle
        into part of the robot (rigidly fixed to `link`): it stops being a
        static obstacle the descent must avoid, its `touch_links` make finger
        contact allowed, AND it then moves WITH the arm during LIFT (so the
        lift is not blocked and the scene stays physically faithful once the
        cube is actually in hand).

        GraspExecutor calls this at the PRE_APPROACH -> APPROACH transition
        (after the gripper is positioned above the cube and committed to the
        grasp, but before descending). Sending operation=ADD for an id that
        already exists in the world makes MoveIt MOVE it from the world into
        the attached state; shapes are left EMPTY on purpose so MoveIt reuses
        the existing world object's own geometry rather than redefining it.

        NOTE (honest caveat): attaching just before the physical grasp means
        that, for the brief descent window, the planning-scene box is modeled
        at the gripper while the real MuJoCo cube is still on the floor. This
        is the standard MoveIt pick trick and is acceptable here -- nothing
        else is registered in the MoveIt world for the attached box to falsely
        collide with (no floor plane is registered in the planning scene), and
        the model becomes faithful again the instant the fingers close.
        NOT YET LIVE-VALIDATED.
        """
        attach_link = link or self._DEFAULT_ATTACH_LINK
        aco = AttachedCollisionObject()
        aco.link_name = attach_link
        aco.touch_links = list(touch_links or self._DEFAULT_TOUCH_LINKS)
        aco.object.id = name
        aco.object.header.frame_id = attach_link
        # ADD on an id already present in the world => MoveIt moves it from the
        # world into the attached state. Empty shapes => reuse existing geometry.
        aco.object.operation = CollisionObject.ADD

        scene = PlanningScene()
        scene.is_diff = True
        scene.robot_state.is_diff = True
        scene.robot_state.attached_collision_objects.append(aco)
        return self._apply_planning_scene(
            scene, f"attach_object({name!r} -> {attach_link})"
        )

    def detach_object(self, name: str, link: Optional[str] = None) -> bool:
        """Detach an attached object from `link`, returning it to the world as
        a plain collision object (operation=REMOVE on an AttachedCollisionObject
        is MoveIt's "detach" semantics). Called on release/place and on a
        failed grasp so the scene doesn't keep a phantom object stuck to the
        gripper. NOT YET LIVE-VALIDATED."""
        attach_link = link or self._DEFAULT_ATTACH_LINK
        aco = AttachedCollisionObject()
        aco.link_name = attach_link
        aco.object.id = name
        aco.object.operation = CollisionObject.REMOVE
        scene = PlanningScene()
        scene.is_diff = True
        scene.robot_state.is_diff = True
        scene.robot_state.attached_collision_objects.append(aco)
        return self._apply_planning_scene(scene, f"detach_object({name!r})")

    def _build_pose_constraints(self, target_pose: np.ndarray) -> Constraints:
        position = target_pose[:3, 3]
        qx, qy, qz, qw = _rotation_matrix_to_quaternion(target_pose[:3, :3])

        position_constraint = PositionConstraint()
        position_constraint.header.frame_id = self._base_frame
        position_constraint.link_name = self._tip_link
        position_constraint.constraint_region.primitives.append(
            SolidPrimitive(type=SolidPrimitive.SPHERE, dimensions=[self._position_tolerance])
        )
        region_pose = Pose()
        region_pose.position.x = float(position[0])
        region_pose.position.y = float(position[1])
        region_pose.position.z = float(position[2])
        region_pose.orientation.w = 1.0
        position_constraint.constraint_region.primitive_poses.append(region_pose)
        position_constraint.weight = 1.0

        orientation_constraint = OrientationConstraint()
        orientation_constraint.header.frame_id = self._base_frame
        orientation_constraint.link_name = self._tip_link
        orientation_constraint.orientation.x = qx
        orientation_constraint.orientation.y = qy
        orientation_constraint.orientation.z = qz
        orientation_constraint.orientation.w = qw
        orientation_constraint.absolute_x_axis_tolerance = self._orientation_tolerance
        orientation_constraint.absolute_y_axis_tolerance = self._orientation_tolerance
        orientation_constraint.absolute_z_axis_tolerance = self._orientation_tolerance
        orientation_constraint.weight = 1.0

        constraints = Constraints()
        constraints.position_constraints = [position_constraint]
        constraints.orientation_constraints = [orientation_constraint]
        return constraints

    # 2026-07-22, found live: MoveIt2's own default trajectory timing (no
    # velocity/acceleration scaling requested) is aggressive -- a first test
    # move produced a 5-point, 0.35s trajectory across several joints, which
    # Stage 3's PD controller could not track accurately in that little time;
    # the resulting error was still ~0.3 rad on one joint 28 SECONDS later
    # (waiting longer did not help -- confirmed this is not a "just needed
    # more time" situation, since pinn_controller_node's own 2s staleness
    # timeout falls back to a gravity-compensation HOLD at whatever position
    # it drifted to, no longer trying to reach the original target at all).
    #
    # That same 2s staleness cutoff is a fixed wall-clock window from receipt,
    # NOT tied to the trajectory's own declared duration -- so slowing down
    # too aggressively creates a DIFFERENT failure mode: a trajectory that
    # legitimately needs more than 2s to complete would get cut off by
    # staleness partway through, before ever reaching the target, which would
    # look like the exact same symptom (never converges). 0.3 is a first,
    # untested-at-this-exact-value guess intended to roughly halve or third
    # the original 0.35s duration (comfortably under 2s) while still being
    # meaningfully slower/smoother than the untrackable default -- confirm the
    # actual resulting trajectory duration empirically (this class now logs
    # it) and adjust if it's still not converging or if it's creeping close
    # to 2s on a larger move.
    _VELOCITY_SCALING = 0.3
    _ACCELERATION_SCALING = 0.3

    # 2026-07-22, found live (after fixing the above): with a 0.3-scaled,
    # 1.11s/13-point trajectory, 6 of 7 arm joints converged to within 0.04
    # rad, but panda_joint3 settled with a persistent ~0.14 rad (~8 deg)
    # residual that did not improve with more waiting time -- consistent with
    # ordinary PD steady-state tracking error under gravity load (a PD-only
    # controller with no integral term is expected to have some), not a bug.
    # 0.05 (the original guess) was simply tighter than what this controller
    # can actually achieve; 0.15 accepts this real, observed behavior while
    # still catching genuine failures (the earlier untuned-speed attempt had
    # errors up to 0.3 rad, well outside this). If steady-state error turns
    # out to matter for actually grasping objects, the real fix is Stage 3
    # gain/gravity-comp tuning, not further loosening this number.
    #
    # 2026-07-23 (Opus 4.8): _CONVERGENCE_TOLERANCE is now the FALLBACK-only
    # threshold (joint-space, radians), used solely when FK is unavailable.
    # The primary check is Cartesian (see _CARTESIAN_TOLERANCE below).
    _CONVERGENCE_TOLERANCE = 0.15

    # 2026-07-23 (Opus 4.8): the PRIMARY convergence threshold -- flange
    # position error in METRES, computed via FK (see _FlangeFK). Replaces the
    # crude uniform per-joint radian check for the reason spelled out in
    # _FlangeFK's docstring: one radian number can't be simultaneously right
    # for a base joint (long lever arm) and a wrist joint (short lever arm).
    #
    # WHY THIS SPECIFICALLY FIXES THE panda_joint5 TIMEOUT: the last honest
    # live steady-state data (keep-target-fresh fix confirmed working) had
    # panda_joint5 plateau at ~0.082 rad error while every other joint was
    # under 0.04 rad. Under the old 0.03 rad uniform check that is a guaranteed
    # timeout. BUT panda_joint5 sits ~0.14 m from the flange (from the URDF:
    # joint5->joint6 = 0, joint6->joint7 = 0.088 m, joint7->link8 = 0.107 m, so
    # ||offset|| ~= sqrt(0.088^2 + 0.107^2) ~= 0.14 m), so 0.082 rad there is
    # only ~0.082 * 0.14 ~= 0.011 m ~= 1.1 cm of flange error -- Cartesian-
    # small despite being the largest ANGLE. The base joints, though under
    # 0.04 rad, have ~0.6-0.8 m lever arms and dominate the true Cartesian
    # error. FK weighs each joint by its ACTUAL lever arm (exactly, per
    # configuration -- no hand-tuned constants), so panda_joint5's harmless
    # angular plateau no longer vetoes an otherwise well-placed flange.
    #
    # 0.03 m (3 cm) default for coarse moves. GraspConfig requests a tighter
    # value for the final grasp approach (approach_cartesian_tolerance, 0.02 m)
    # -- 2 cm bounds the lateral miss to inside the (0.08 m open - 0.04 m
    # object)/2 = 0.02 m half-gap that still captures grasp_object between the
    # pads. NOT YET LIVE-VALIDATED: if the controller genuinely cannot place
    # the flange this tightly, this surfaces as an honest ARM_TIMEOUT (with a
    # logged Cartesian error) rather than a silent multi-cm miss; loosen only
    # as far as the logged error shows is necessary.
    _CARTESIAN_TOLERANCE = 0.03

    # 2026-07-23 (Opus 4.8 investigation of the tight-tolerance approach-phase
    # timeout): the ROOT CAUSE of the "approach never converges to 0.03 rad,
    # and panda_joint3 actively drifts AWAY from target" symptom.
    #
    # pinn_controller_node treats a trajectory as STALE 2.0s after it was
    # RECEIVED (_TRAJECTORY_STALE_SEC, a fixed wall-clock window from receipt,
    # unrelated to the trajectory's own duration) and then STOPS tracking it
    # entirely -- it falls back to _publish_safe_fallback(), i.e. pure
    # gravity-compensation HOLD at wherever the arm currently is, with NO
    # position feedback toward the target.
    #
    # move_to() waits up to `timeout` (default 10s) for convergence, but the
    # controller abandons the target after only ~2s. Reconstructing the live
    # log timeline confirmed it exactly: with ~1.5s of DDS grace + a sub-second
    # scaled trajectory, the 2s staleness cutoff fires ~0.5s into the
    # convergence-check loop -- so during essentially the ENTIRE "still
    # converging" window the arm was under open-loop gravity-comp hold, NOT
    # being driven to the target. That directly explains BOTH anomalies:
    #   * panda_joint3 monotonically drifting away (-0.2928 -> -0.2960): a PD
    #     loop with a live target physically CANNOT drift monotonically in
    #     steady state (it holds at e_ss = disturbance/Kp); only an
    #     un-fed-back gravity-comp hold with a small RNEA-vs-MuJoCo gravity
    #     mismatch sags like that. NOT a sign error, NOT a coupling bug.
    #   * panda_joint5 frozen ~0.056 rad short: that is the tracking error at
    #     the instant the 2s window closed, then held. joints 3 and 5 have the
    #     two LOWEST arm Kp values (9.36 and 4.41 -- from DEFAULT_ERROR_BOUND
    #     via the Lyapunov critical-damping formula), so for a given model-
    #     mismatch torque they show the largest steady-state error AND the
    #     slowest transient -- physically expected to be the worst two joints,
    #     independent of any bug. Crucially the ~0.056 rad "floor" was measured
    #     DURING the gravity-comp hold, before the motion had settled, so it is
    #     NOT proof of the true actively-tracked steady-state error (which the
    #     arm never got enough live-tracked time to reach).
    #
    # FIX (Stage-4-only, touches NO Stage 1/2/3 code or gains): keep the target
    # FRESH. During the convergence wait, periodically republish a single-point
    # "hold at the planned final waypoint" trajectory (interval < 2.0s), which
    # resets pinn_controller_node's staleness clock and keeps its PD loop
    # actively driving toward the target for the full timeout instead of
    # bailing to gravity-comp hold after 2s. This eliminates the joint3 drift
    # and gives the PD its real chance to settle -- turning the tolerance check
    # into an honest test of the genuinely achievable error rather than a race
    # against a 2s cutoff. A SINGLE-POINT trajectory (not a republish of the
    # full one) is essential: TrajectoryInterpolator holds a 1-point trajectory
    # constant at that point, so this is a pure "hold at target" reference;
    # republishing the FULL trajectory would reset t_traj to 0 and yank the arm
    # back to the FIRST (pre-approach) waypoint. NOT YET LIVE-VALIDATED
    # (prepared without simulator access).
    _HOLD_REFRESH_INTERVAL = 1.5

    def _build_hold_trajectory(self, planned: JointTrajectory) -> JointTrajectory:
        """Build a single-point "hold at final waypoint" trajectory.

        Carries the SAME joint_names as the planned trajectory so
        pinn_controller_node's by-name reorder (TrajectoryInterpolator's
        expected_joint_names path) still lands each value on the right joint.
        velocities/accelerations are left empty -> the interpolator defaults
        them to zero, i.e. a static hold (qdot_des = qddot_des = 0), so the
        controller's RNEA feedforward reduces to gravity+Coriolis and the PD
        term drives the residual position error to the target.
        """
        hold = JointTrajectory()
        hold.joint_names = list(planned.joint_names)
        point = JointTrajectoryPoint()
        point.positions = list(planned.points[-1].positions)
        # time_from_start = 0: a 1-point trajectory is held constant regardless.
        hold.points = [point]
        return hold

    def move_to(
        self,
        target_pose: np.ndarray,
        speed: float,
        timeout: float = 10.0,
        convergence_tolerance: float | None = None,
        cartesian_tolerance: float | None = None,
    ) -> bool:
        """
        Plan a Cartesian-goal path to target_pose and execute it via Stage 3.

        speed [m/s] is accepted for interface compatibility with GraspConfig's
        *_speed fields but is NOT mapped to it literally: converting a desired
        Cartesian end-effector speed into MoveIt2's 0-1 joint-space velocity
        scaling factor isn't a direct unit conversion, and moveit_plan_bridge.py
        (this class's own reference pattern) doesn't attempt it either. Instead
        a fixed, conservative _VELOCITY_SCALING/_ACCELERATION_SCALING is applied
        to every request (see class-level comment for why this was necessary,
        not optional). Revisit with a real speed mapping if a pick sequence
        needs distinguishably different approach/lift speeds.

        `timeout` is a single overall budget covering planning AND execution
        (not split into separate phase timeouts) -- keep it generous;
        GraspConfig.arm_motion_timeout is the field this should come from.

        CONVERGENCE CRITERION (2026-07-23, Opus 4.8 -- now Cartesian):
        When FK is available (self._fk is not None, the normal case), success
        is decided in CARTESIAN space: the flange (panda_link8) position error
        between the live /joint_states configuration and the demanded
        target_pose, in metres, must fall below `cartesian_tolerance` (default
        _CARTESIAN_TOLERANCE = 0.03 m). This replaces the old uniform per-joint
        radian check, which was physically crude -- see _FlangeFK's and
        _CARTESIAN_TOLERANCE's docstrings for the full rationale and the
        panda_joint5-specific worked example (0.082 rad angular plateau =
        only ~1.1 cm at the flange, because that joint has a ~0.14 m lever
        arm, whereas a base joint's much smaller angular error dominates the
        Cartesian miss). Error is measured against target_pose's translation
        directly (not the planned IK waypoint), so it folds in MoveIt2's own
        <=1 cm IK position slack -- the honest total flange-to-goal distance.
        Orientation is deliberately NOT part of the convergence gate here (the
        plan already satisfies the orientation constraint); only position.

        `cartesian_tolerance` [m], if given, overrides _CARTESIAN_TOLERANCE for
        this call. GraspExecutor passes a tighter value (0.02 m) for the final
        grasp-approach step. NOT YET LIVE-VALIDATED: if the controller cannot
        place the flange this tightly, this surfaces as an honest ARM_TIMEOUT
        (with the logged Cartesian error) rather than a silent multi-cm miss;
        the real fix would then be Stage 3 gain/gravity-comp retuning, not
        loosening this number.

        `convergence_tolerance` [rad] is the FALLBACK-only threshold, used
        solely when FK is unavailable (pinocchio missing / URDF unloadable).
        If given it overrides _CONVERGENCE_TOLERANCE (0.15 rad). Prior context:
        0.15 rad was accepted for coarse moves but far too loose for the grasp
        approach (0.15 rad, lever-arm-amplified, is a 10-15 cm fingertip miss --
        the very artefact that motivated moving to the Cartesian check). In the
        fallback path this reverts to the old uniform max-abs-joint-error
        behaviour, with a warning that the crude check is in use.

        Returns True if planning succeeded, the trajectory was handed off,
        AND the arm converged (Cartesian flange error < cartesian_tolerance
        when FK is available; else max abs joint error < convergence_tolerance)
        within `timeout` seconds total. Returns False on any planning failure,
        handoff failure, or timeout.
        """
        joint_tolerance = (
            self._CONVERGENCE_TOLERANCE
            if convergence_tolerance is None
            else convergence_tolerance
        )
        cart_tolerance = (
            self._CARTESIAN_TOLERANCE
            if cartesian_tolerance is None
            else cartesian_tolerance
        )
        use_fk = self._fk is not None
        target_position = np.asarray(target_pose[:3, 3], dtype=float)
        deadline = time.monotonic() + timeout

        if not self._action_client.wait_for_server(timeout_sec=max(timeout, 0.1)):
            self.get_logger().error("move_to(): move_action server not available")
            return False

        goal = MoveGroup.Goal()
        goal.request.group_name = self._group_name
        # 2026-07-29: 1 -> 10. Each attempt re-samples the GOAL STATE via IK, and
        # the stock config gives that sampling almost no budget: MoveIt2 resolves
        # panda_arm with kdl_kinematics_plugin at kinematics_solver_timeout=0.05s
        # (moveit_resources_panda_moveit_config/config/kinematics.yaml). KDL is
        # iterative and randomly seeded, so near a singularity it converges only
        # some of the time within 50 ms -- and with a single attempt one unlucky
        # seed fails the whole move.
        #
        # Observed live on the last pre-approach sub-step, whose goal is
        # (0.5, 0.0, 0.3299) with the gripper pointing straight down: y=0 puts it
        # exactly on the robot's x-axis with a vertical wrist, right in the
        # Panda's singular region. Same goal pose, three runs, two outcomes:
        # test_grasp_pick_run20.log planned it fine; run21 and run22 both failed
        # with GOAL_STATE_INVALID after burning the full 5s planning budget, and
        # move_group's own log gives the mechanism outright --
        # "RRTConnect: Unable to sample any valid states for goal tree". That is
        # the IK sampler giving up, NOT a collision: a goal in collision is
        # rejected in milliseconds (cf. the 1.6ms attached-object rejection in
        # run20), whereas exhausting the sampler burns the whole budget first.
        # Scene geometry was ruled out separately -- shrinking the grasp_object
        # box 0.12 -> 0.06 and dropping the floor box 3cm changed nothing.
        goal.request.num_planning_attempts = 10
        goal.request.allowed_planning_time = self._planning_time
        goal.request.max_velocity_scaling_factor = self._VELOCITY_SCALING
        goal.request.max_acceleration_scaling_factor = self._ACCELERATION_SCALING
        goal.request.goal_constraints = [self._build_pose_constraints(target_pose)]
        goal.planning_options.plan_only = True

        send_goal_future = self._action_client.send_goal_async(goal)
        while not send_goal_future.done():
            rclpy.spin_once(self, timeout_sec=0.05)
            if time.monotonic() > deadline:
                self.get_logger().error("move_to(): timed out waiting for goal acceptance")
                return False
        goal_handle = send_goal_future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error("move_to(): MoveGroup goal rejected")
            return False

        result_future = goal_handle.get_result_async()
        while not result_future.done():
            rclpy.spin_once(self, timeout_sec=0.05)
            if time.monotonic() > deadline:
                self.get_logger().error("move_to(): timed out waiting for planning result")
                return False
        result = result_future.result().result
        if result.error_code.val != MoveItErrorCodes.SUCCESS:
            self.get_logger().error(f"move_to(): planning failed, error_code={result.error_code.val}")
            return False

        trajectory = result.planned_trajectory.joint_trajectory
        if not trajectory.points:
            self.get_logger().error("move_to(): planned trajectory has no points")
            return False

        target_by_name = dict(zip(trajectory.joint_names, trajectory.points[-1].positions))
        traj_duration = trajectory.points[-1].time_from_start
        traj_duration_s = traj_duration.sec + traj_duration.nanosec * 1e-9
        self.get_logger().info(
            f"move_to(): planning succeeded ({len(trajectory.points)} points, "
            f"{traj_duration_s:.2f}s trajectory duration, "
            f"{deadline - time.monotonic():.2f}s of overall timeout remaining) "
            f"-- handing off to Stage 3"
        )

        self._pub_trajectory.publish(trajectory)
        # 2026-07-27: pinn_controller_node measures trajectory time as
        # (now - receipt_time) and declares the trajectory STALE 2.0s after
        # receipt (_TRAJECTORY_STALE_SEC), so the playout window has to be
        # timed from the PUBLISH INSTANT, not from after the DDS grace period.
        publish_time = time.monotonic()
        # Same DDS-discovery grace period as moveit_plan_bridge.py's own
        # plan_and_handoff() -- without it, a freshly-created publisher's
        # first message can be silently dropped before pinn_controller_node's
        # subscriber has finished discovering it.
        for _ in range(20):
            rclpy.spin_once(self, timeout_sec=0.05)
        time.sleep(0.5)

        # Give the trajectory time to actually play out (Stage 3's own 1 kHz
        # control loop in pinn_controller_node, not this node) before checking
        # convergence.
        #
        # 2026-07-27 FIX: this used to be `time.monotonic() + traj_duration_s`,
        # evaluated AFTER the ~1.5s grace above, so it waited 1.5s + duration
        # from publish while the node stops tracking at 2.0s from receipt. For
        # every trajectory duration observed live (0.71s - 1.15s, see the
        # 2026-07-23/24 logs) that guaranteed a window -- 0.2s to 0.65s wide --
        # in which the node had already given up on the trajectory and reverted
        # to an open-loop gravity-compensation hold, BEFORE the keep-fresh
        # republish loop below had run even once. The arm drifted un-fed-back
        # through exactly the interval where it should have been settling, and
        # the first convergence sample was taken after that drift. Anchoring on
        # publish_time removes the gap: the wait now ends when the trajectory
        # itself ends, still inside the node's 2.0s tracking window, and the
        # hold-refresh republish (last_refresh_time = 0.0 forces it immediately)
        # takes over with no dead time in between.
        min_wait_deadline = min(publish_time + traj_duration_s, deadline)
        while time.monotonic() < min_wait_deadline:
            rclpy.spin_once(self, timeout_sec=0.05)
        self.get_logger().info(
            f"move_to(): trajectory should have finished playing out, "
            f"{deadline - time.monotonic():.2f}s left to confirm convergence"
        )

        # Periodic (not just final) diff logging: a single end-of-timeout diff
        # can't distinguish "still converging, just needed more time" (max diff
        # shrinking across samples) from "plateaued early" (max diff flat well
        # before the deadline, a genuine PD steady-state limit needing gain
        # retuning, not more waiting) -- found necessary 2026-07-23 when a
        # pre-approach move (a much larger reach than the previously-validated
        # "home" target) timed out with two joints >0.3 rad off and no way to
        # tell from the final-only diff which case this was.
        last_diffs_by_name: dict = {}
        last_log_time = time.monotonic()
        # 2026-07-23: keep the target FRESH so pinn_controller_node keeps
        # actively PD-tracking it instead of abandoning it to a gravity-comp
        # hold 2s after receipt (see _HOLD_REFRESH_INTERVAL's comment for the
        # full root-cause analysis). Republish a single-point hold-at-final-
        # waypoint trajectory now (immediately, so any gap between the end of
        # the playout wait and here is closed at once) and then every
        # _HOLD_REFRESH_INTERVAL (< the node's 2.0s staleness window).
        hold_trajectory = self._build_hold_trajectory(trajectory)
        last_refresh_time = 0.0  # forces an immediate first refresh below
        # 2026-07-23 (Opus 4.8): last computed Cartesian flange error [m], kept
        # for the timeout diagnostic even when FK is the success criterion.
        last_cart_err: float | None = None
        self.get_logger().info(
            "move_to(): convergence criterion = "
            + (
                f"Cartesian flange error < {cart_tolerance:.4f} m (FK)"
                if use_fk
                else f"max abs joint error < {joint_tolerance:.4f} rad (joint-space FALLBACK, "
                "FK unavailable)"
            )
        )
        while time.monotonic() < deadline:
            now_refresh = time.monotonic()
            if now_refresh - last_refresh_time >= self._HOLD_REFRESH_INTERVAL:
                self._pub_trajectory.publish(hold_trajectory)
                last_refresh_time = now_refresh
            rclpy.spin_once(self, timeout_sec=0.05)
            current_by_name = self._current_joint_positions_by_name()
            if current_by_name is not None:
                # Per-joint diffs are still computed unconditionally -- they are
                # the primary diagnostic on timeout (which joint is the outlier)
                # regardless of whether the SUCCESS gate is Cartesian or not.
                last_diffs_by_name = {
                    name: current_by_name[name] - target
                    for name, target in target_by_name.items()
                    if name in current_by_name
                }

                # Cartesian flange error via FK (primary success gate when
                # available). Guarded: any FK evaluation failure at runtime
                # (e.g. a transient partial /joint_states) disables FK for the
                # rest of this call and drops back to the joint-space gate,
                # rather than aborting the move.
                if use_fk:
                    try:
                        current_pos = self._fk.flange_position(current_by_name)
                        last_cart_err = float(
                            np.linalg.norm(current_pos - target_position)
                        )
                    except Exception as exc:  # noqa: BLE001
                        self.get_logger().warning(
                            f"move_to(): FK evaluation failed ({exc!r}); reverting "
                            "to joint-space convergence check for the rest of this move"
                        )
                        use_fk = False
                        last_cart_err = None

                if use_fk:
                    converged = last_cart_err is not None and last_cart_err < cart_tolerance
                else:
                    converged = bool(last_diffs_by_name) and max(
                        abs(d) for d in last_diffs_by_name.values()
                    ) < joint_tolerance

                if converged:
                    # 2026-07-23: log the final state on SUCCESS too, not just
                    # on timeout -- needed live data on how close to the
                    # tolerance boundary a "converged" result actually lands.
                    max_name = (
                        max(last_diffs_by_name, key=lambda n: abs(last_diffs_by_name[n]))
                        if last_diffs_by_name
                        else "n/a"
                    )
                    crit = (
                        f"Cartesian flange error={last_cart_err:.4f} m "
                        f"(tolerance={cart_tolerance:.4f} m)"
                        if use_fk
                        else f"max abs joint error (tolerance={joint_tolerance:.4f} rad)"
                    )
                    self.get_logger().info(
                        f"move_to(): converged -- {crit}. "
                        f"Per-joint diffs [rad]: {last_diffs_by_name} "
                        f"(worst joint: {max_name})"
                    )
                    return True

                now = time.monotonic()
                if last_diffs_by_name and now - last_log_time >= 1.0:
                    max_name = max(last_diffs_by_name, key=lambda n: abs(last_diffs_by_name[n]))
                    # 2026-07-23: log absolute current/target and the Cartesian
                    # error, not just the joint diff -- the joint diff alone
                    # can't distinguish "genuinely can't track" from "physically
                    # pinned at a joint limit" (both flat, non-shrinking), and
                    # the Cartesian error is what the success gate actually uses.
                    cart_str = (
                        f", flange err={last_cart_err:.4f} m"
                        if last_cart_err is not None
                        else ""
                    )
                    self.get_logger().info(
                        f"move_to(): still converging, "
                        f"{deadline - now:.2f}s left, worst joint "
                        f"{max_name}={last_diffs_by_name[max_name]:+.4f} rad "
                        f"(current={current_by_name[max_name]:+.4f}, "
                        f"target={target_by_name[max_name]:+.4f}){cart_str}"
                    )
                    last_log_time = now

        # Log the actual per-joint (current - target) diffs at timeout, not just
        # "didn't converge" -- this is the difference between "still mid-motion,
        # just needed more time/budget" (small, shrinking diffs) and "never
        # moved at all" (diffs close to the full initial error) or "moved but
        # to the wrong place" (large diffs on specific joints).
        cart_fail_str = (
            f" Final Cartesian flange error: {last_cart_err:.4f} m "
            f"(needed < {cart_tolerance:.4f} m)."
            if use_fk and last_cart_err is not None
            else ""
        )
        self.get_logger().warning(
            f"move_to(): trajectory handed off, but the arm did not converge to "
            f"the planned target within the timeout.{cart_fail_str} Final per-joint "
            f"(current - target) diffs [rad]: {last_diffs_by_name}"
        )
        # 2026-07-23: also log absolute current + target per joint, not just the
        # diff -- needed to tell "genuinely can't track" apart from "physically
        # pinned at a joint limit" (found live: panda_joint4/6/7 froze
        # bit-identical across two separate runs; only the absolute current
        # value can be checked against each joint's known MJCF range).
        final_current_by_name = self._current_joint_positions_by_name() or {}
        self.get_logger().warning(
            f"move_to(): absolute current positions at timeout [rad]: "
            f"{final_current_by_name}"
        )
        self.get_logger().warning(
            f"move_to(): absolute target positions [rad]: {target_by_name}"
        )
        return False
