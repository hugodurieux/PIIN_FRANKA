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

TARGETS: dict[str, np.ndarray] = {
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
