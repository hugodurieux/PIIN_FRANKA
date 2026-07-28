"""
Hardcoded grasp and place targets for Stage 4 demo (no vision required).

All poses are (4, 4) homogeneous transforms expressed in the Franka Panda
base frame (origin at the robot base, z pointing up).

Coordinate convention:
  - x: forward (away from the robot base)
  - y: left
  - z: up
  - Gripper approach axis: -z of the grasp frame (fingers point down)

How to use:
    from stage4.demo_targets import TARGETS, get_target
    pose = get_target("box_center")
    result = executor.pick(pose)

To add a new target: copy an existing entry and adjust the translation
column (last column of the 4x4 matrix). The rotation block (top-left 3x3)
encodes the gripper orientation — TOP_DOWN is the standard pick orientation
(fingers pointing straight down).
"""

from __future__ import annotations
import numpy as np


def _pose(x: float, y: float, z: float, rotation: np.ndarray) -> np.ndarray:
    """Build a (4, 4) homogeneous transform from position and rotation matrix."""
    T = np.eye(4)
    T[:3, :3] = rotation
    T[:3, 3]  = [x, y, z]
    return T


# Standard gripper orientations (rotation of the grasp frame in base frame)
# TOP_DOWN: approach from above, fingers pointing straight down (-z of grasp = world -z)
_TOP_DOWN = np.array([
    [1,  0,  0],
    [0, -1,  0],
    [0,  0, -1],
], dtype=float)

# 2026-07-29: TOP_DOWN with the hand's own 45 deg mounting twist compensated.
#
# WHY. The IK/grasp target is panda_link8, but the FINGERS slide along
# panda_hand's y-axis, and panda_hand is mounted on panda_link8 with a pure
# -45 deg twist (pinocchio_baseline/panda.urdf:
#     <joint name="panda_hand_joint"> parent panda_link8, child panda_hand,
#         origin rpy="0 0 -0.785398163397" xyz="0 0 0"
# -- zero translation, rotation only). So commanding plain _TOP_DOWN on link8
# presents the fingers at 45 deg to the world axes: square to the cube by eye in
# RViz, but diagonal across it in reality.
#
# CONFIRMED LIVE, test_grasp_pick_run29.log -- the first run to make real
# contact with the cube. Every waypoint converged (final grasp 0.0120 m against
# a 0.0200 m tolerance) and the gripper closed onto the object, but stopped at
#     0.0526 m
# rather than the cube's 0.040 m width. That is the CUBE'S DIAGONAL
# (0.04 * sqrt(2) = 0.0566 m), less a little corner squeeze at 20 N: the fingers
# were pinching two opposite corners instead of two flat faces. Contrast run28,
# where the fingers closed clean through empty air to 0.0336 m -- so 0.0526 is
# genuine contact, just on the wrong geometry.
#
# THE CORRECTION. Right-multiplying by Rz(+45 deg) means
#     R_hand = R_link8 @ Rz(-45) = (_TOP_DOWN @ Rz(+45)) @ Rz(-45) = _TOP_DOWN
# i.e. the HAND ends up axis-aligned (fingers opening along world y) even though
# link8 itself is now the one carrying the 45 deg twist. The approach axis is
# untouched: the z column stays (0, 0, -1), straight down.
_Rz45 = np.array([
    [np.cos(np.pi / 4), -np.sin(np.pi / 4), 0],
    [np.sin(np.pi / 4),  np.cos(np.pi / 4), 0],
    [0,                  0,                 1],
], dtype=float)
_TOP_DOWN_FINGERS_ALIGNED = _TOP_DOWN @ _Rz45

# TILTED_30: approach at 30° tilt (useful for objects near the table edge)
_c, _s = np.cos(np.radians(30)), np.sin(np.radians(30))
_TILTED_30 = np.array([
    [1,   0,    0 ],
    [0,  _c,  -_s ],
    [0,  _s,   _c ],
], dtype=float) @ _TOP_DOWN


# ---------------------------------------------------------------------------
# Named targets
# All positions in metres relative to Franka base frame.
# Typical reachable workspace: x in [0.3, 0.7], y in [-0.4, 0.4], z in [0.0, 0.6]
# ---------------------------------------------------------------------------

# 2026-07-23: flange-to-fingertip offset used to correct grasp_object below.
# ArmMotionClient's IK target is panda_link8 (the flange), not the fingertip
# contact point -- computed directly from panda_arm_mujoco.xml's own body
# chain (all offsets along the flange's local Z, which stays approach-axis-
# aligned since the hand's mounting quat is a pure Z-axis twist):
#   panda_link8 -> panda_hand               0.0     m  (see correction below)
#   panda_hand  -> panda_leftfinger origin  0.0584  m
#   finger origin -> fingertip pad contact  0.0445  m  (mean of the 5
#     fingertip_pad_collision box z-centers/spans; 0.0445 is
#     both pad_1's own center AND the midpoint of the full pad span
#     0.036-0.053, so it's a reasonable "grasp contact height" regardless
#     of which interpretation is used)
#   total: 0.0 + 0.0584 + 0.0445 = 0.1029 m
#
# 2026-07-29 CORRECTION, 0.2099 -> 0.1029. The original chain opened with
# "panda_link8 -> panda_hand = 0.107 m", read off the MJCF body tree. That
# 0.107 is the panda_link7 -> panda_link8 offset, NOT link8 -> hand. Confirmed
# in pinocchio_baseline/panda.urdf -- the very model ArmMotionClient runs FK
# against:
#     <joint name="panda_joint8">      link7 -> link8   xyz="0 0 0.107"
#     <joint name="panda_hand_joint">  link8 -> hand    xyz="0 0 0"
#                                                       rpy="0 0 -0.785398"
# The hand is mounted on link8 with a PURE -45 deg rotation and ZERO
# translation. Since the IK target is panda_link8 itself, that 0.107 was being
# counted twice, commanding the flange 0.107 m too high and holding the
# fingertips ~10 cm above the cube.
#
# CONFIRMED LIVE, test_grasp_pick_run28.log -- the first run in this project to
# reach grasp() at all: every arm waypoint converged (final approach 0.0168 m
# against a 0.0200 m tolerance), then the gripper closed to 0.0336 m against a
# 0.040 m target, i.e. straight through empty air, with the fingers visibly
# about 10 cm above the cube. Both the observed height error and the arithmetic
# error are 0.107 m. This is the flange-vs-fingertip offset that this test's own
# module docstring was written to expose; it is now measured, not assumed.
_FLANGE_TO_FINGERTIP_Z = 0.1029

TARGETS: dict[str, np.ndarray] = {
    # The actual grasp_object cube added to the MuJoCo scene 2026-07-22
    # (mujoco/franka_emika_panda/panda_arm_mujoco.xml): a 4cm cube resting on
    # the floor at x=0.65, y=0, center height z=0.02. z here is the panda_link8
    # (flange) IK target, corrected by _FLANGE_TO_FINGERTIP_Z above so the
    # FINGERTIP contact point (not the flange itself) lands at the cube's
    # center height. Before this correction (raw z=0.02 for the flange), the
    # commanded fingertip position was ~0.02 - 0.2099 = -0.19m -- 19cm BELOW
    # the floor, physically unreachable -- which is the most likely root cause
    # of both the "arm never gets near the object" symptom AND the severe
    # (0.2+ rad, plateaued, not shrinking) joint tracking errors seen
    # 2026-07-23 during the approach-phase move: MoveIt2's IK can still
    # "solve" for the flange alone to reach z=0.02 (a valid point on its own),
    # but likely only via a contorted, near-limit configuration that Stage 3's
    # controller genuinely cannot hold, not a normal PD steady-state droop.
    # 2026-07-29: x moved 0.5 -> 0.65 to test the pick at a significantly farther
    # reach. Must stay in sync with panda_arm_mujoco.xml's grasp_object body pos
    # AND its 'home' keyframe freejoint qpos, and with test_grasp_pick.py's
    # planning-scene registration -- four places, all 0.65 now. If they disagree,
    # MoveIt2 plans to one location while MuJoCo puts the cube at another.
    # rotation: _TOP_DOWN_FINGERS_ALIGNED (not plain _TOP_DOWN) so the FINGERS,
    # not just panda_link8, are square to the cube -- see that constant's comment
    # and run29's 0.0526 m diagonal-corner grasp.
    "grasp_object": _pose(
        x=0.65,
        y=0.0,
        z=0.02 + _FLANGE_TO_FINGERTIP_Z,
        rotation=_TOP_DOWN_FINGERS_ALIGNED,
    ),

    # A small box placed roughly in front of the robot at table height
    "box_center": _pose(x=0.45, y=0.0,  z=0.12, rotation=_TOP_DOWN),

    # Same box, slightly to the left
    "box_left":   _pose(x=0.45, y=0.15, z=0.12, rotation=_TOP_DOWN),

    # Same box, slightly to the right
    "box_right":  _pose(x=0.45, y=-0.15, z=0.12, rotation=_TOP_DOWN),

    # Place target: a tray or bin to the side of the workspace
    "place_tray": _pose(x=0.35, y=0.35, z=0.20, rotation=_TOP_DOWN),

    # Home / retract pose (arm extended safely above workspace)
    "home":       _pose(x=0.30, y=0.0,  z=0.45, rotation=_TOP_DOWN),
}


def get_target(name: str) -> np.ndarray:
    """
    Return the (4, 4) pose for a named target.

    Args:
        name: Key in TARGETS dict.

    Returns:
        (4, 4) numpy array, a copy (safe to modify).

    Raises:
        KeyError: if name is not in TARGETS.
    """
    if name not in TARGETS:
        raise KeyError(
            f"Unknown target '{name}'. Available: {list(TARGETS.keys())}"
        )
    return TARGETS[name].copy()


def list_targets() -> list[str]:
    """Return all available target names."""
    return list(TARGETS.keys())
