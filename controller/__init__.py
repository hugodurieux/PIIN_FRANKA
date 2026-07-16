"""
Stage 3 -- Computed-torque + PD controller for the Franka Panda.

Exports the main controller class and supporting utilities.
"""

from controller.computed_torque_pd import ComputedTorquePDController
from controller.model_loader import load_grey_box_model
from controller.lyapunov_gains import (
    compute_lyapunov_gains,
    DEFAULT_KP,
    DEFAULT_KD,
    MANUAL_PD_KP,
    MANUAL_PD_KD,
)
from controller.payload_identification import identify_payload

__all__ = [
    "ComputedTorquePDController",
    "load_grey_box_model",
    "compute_lyapunov_gains",
    "DEFAULT_KP",
    "DEFAULT_KD",
    "MANUAL_PD_KP",
    "MANUAL_PD_KD",
    "identify_payload",
]
