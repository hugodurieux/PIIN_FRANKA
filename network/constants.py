"""
Franka Panda physical constants.

Single source of truth for every physics-related value in stage 1.
Agents (implementer, physics-validator) reference TORQUE_LIMITS from here.
"""

import torch

N_JOINTS = 7

# Absolute torque limits per joint [Nm] (Franka Panda datasheet)
TORQUE_LIMITS = torch.tensor([87.0, 87.0, 87.0, 87.0, 12.0, 12.0, 12.0])

# Max joint velocities [rad/s]
VELOCITY_LIMITS = torch.tensor([2.175, 2.175, 2.175, 2.175, 2.610, 2.610, 2.610])

# Target control rate [Hz]
CONTROL_RATE = 1000

# Payloads used during data collection [kg]
PAYLOADS = (0.0, 1.0, 3.0)

# Network input dimension: sin(q)[7] + cos(q)[7] + qdot[7] + delta[1]
INPUT_DIM = 3 * N_JOINTS + 1  # = 22
OUTPUT_DIM = N_JOINTS         # = 7

# FrictionNet sub-module hidden dimension (novelty N2, Liu et al. 2024)
FRICTION_NET_HIDDEN = 64   # hidden dim for the FrictionNet sub-module
