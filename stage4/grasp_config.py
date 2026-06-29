"""
Grasp configuration parameters for Stage 4 force-controlled grasping.

All physical constants and tuning knobs live here so they can be adjusted
without touching the control logic.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np


@dataclass
class GraspConfig:
    """
    Parameters for a single force-controlled grasp attempt.

    Franka Hand hardware limits:
      - Finger width range: 0 – 0.08 m (0 = fully closed, 0.08 = fully open)
      - Max grasp force:    70 N
      - Max finger speed:   0.1 m/s
    """

    # --- Gripper ---
    # Target finger width [m] at the moment of contact.
    # Set to the approximate object width; fingers close until force is reached.
    grasp_width: float = 0.04

    # Target grip force [N]. Franka Hand maintains this after contact.
    grasp_force: float = 20.0

    # Finger closing speed [m/s].
    grasp_speed: float = 0.05

    # Tolerance band around grasp_width for success check [m].
    # Inner: fingers may be this much more closed than grasp_width (object is thinner).
    # Outer: fingers may be this much more open than grasp_width (object is thicker).
    epsilon_inner: float = 0.005
    epsilon_outer: float = 0.010

    # Width [m] to open to before approaching the object.
    open_width: float = 0.08

    # Speed [m/s] to open the gripper.
    open_speed: float = 0.1

    # --- Arm motion (pre-grasp and lift) ---
    # Height [m] above the grasp pose for the pre-approach waypoint.
    pre_approach_height: float = 0.10

    # Descent speed [m/s] during the approach phase (arm moves down to grasp pose).
    approach_speed: float = 0.05

    # Height [m] to lift the object after a successful grasp.
    lift_height: float = 0.15

    # Lift speed [m/s].
    lift_speed: float = 0.05

    # --- Safety ---
    # Maximum torque error threshold [Nm] — if Stage 3 reports a torque error
    # above this value during approach, abort the grasp.
    max_torque_error: float = 5.0

    # Timeout [s] for each gripper action (open, grasp).
    gripper_timeout: float = 5.0

    # Timeout [s] for each arm motion primitive.
    arm_motion_timeout: float = 10.0

    # --- Payload accounting ---
    # Estimated object mass [kg] passed to the Stage 3 controller after grasping,
    # so the RNEA feedforward updates its gravity/inertia compensation.
    object_mass: float = 0.0
