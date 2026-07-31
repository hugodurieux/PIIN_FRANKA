"""
Grasp configuration parameters for Stage 4 force-controlled grasping.

All physical constants and tuning knobs live here so they can be adjusted
without touching the control logic.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
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
    # 2026-07-24: widened inner from 0.005 -> 0.008 after a live pick attempt
    # missed by ~1.6mm (final width 0.0334m vs a 0.035m floor at the old
    # epsilon_inner) despite the arm converging within its own tight approach
    # tolerance (0.0184m < 0.02m) -- a real, small, expected miss from residual
    # Cartesian tracking error, not a sign of a bad grasp. This does not
    # change how tightly the ARM must converge (that is
    # approach_cartesian_tolerance below); it only widens how much the
    # resulting gripper width is allowed to differ from the nominal target
    # before the grasp is called a failure.
    epsilon_inner: float = 0.008
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

    # Joint-space convergence tolerance [rad] for the approach (final descent)
    # move specifically -- overrides ArmMotionClient's default 0.15 rad, which
    # was accepted for coarse moves but proved far too loose for the precision
    # needed to align a 2cm-wide gripper pad against a 4cm object. See
    # ArmMotionClient.move_to()'s own 2026-07-23 docstring note for the full
    # reasoning and the live evidence (10-15cm fingertip miss at 0.15 rad).
    # 0.03 rad (~1.7 deg) is a first, untested-at-this-exact-value guess: an
    # order of magnitude tighter than 0.15, intended to bound the Cartesian
    # miss to roughly 0.03 * (arm reach ~0.8m) =~ 2.4cm in the worst case --
    # small enough to land within the fingers' own span. If Stage 3's
    # controller cannot actually track this tightly, expect ARM_TIMEOUT
    # instead of a silently-inaccurate "success" (a more honest failure mode
    # than before); if that happens, loosen this only as far as strictly
    # needed, and treat repeated failure here as a signal that a real Stage 3
    # gain/gravity-comp retune is now required, not optional.
    approach_convergence_tolerance: float = 0.03

    # 2026-07-23 (Opus 4.8): CARTESIAN convergence tolerance [m] for the final
    # grasp-approach move. ArmMotionClient.move_to() now checks convergence in
    # Cartesian space (flange position error via forward kinematics) instead of
    # a uniform per-joint radian threshold -- the joint threshold was physically
    # crude (a given radian error costs far more fingertip travel on a base
    # joint than on a wrist joint; see ArmMotionClient._FlangeFK's docstring).
    # This directly fixes the panda_joint5 spurious-timeout: joint5's ~0.082 rad
    # steady-state plateau is only ~1.1 cm at the flange (short ~0.14 m lever
    # arm), so a Cartesian check no longer lets that Cartesian-harmless angular
    # error veto convergence. approach_convergence_tolerance (radians) above is
    # now only the FALLBACK threshold used if FK is unavailable.
    # 0.02 m (2 cm): the lateral half-gap between an 0.08 m open gripper and the
    # 0.04 m object, i.e. the largest miss that still lands the object between
    # the pads. NOT YET LIVE-VALIDATED -- if the controller can't place the
    # flange within 2 cm this surfaces as an honest ARM_TIMEOUT (with the logged
    # Cartesian error) rather than a silent miss; loosen only as far as that
    # logged error shows is needed, and read repeated failure as a signal a real
    # Stage 3 gain/gravity-comp retune is now required.
    approach_cartesian_tolerance: float = 0.02

    # 2026-07-24: CARTESIAN tolerance [m] used for the home->pre-approach
    # sub-steps specifically (see pre_approach_num_waypoints below). These
    # moves only need to get the arm roughly hovering above the object before
    # the precision-critical descent (governed by approach_cartesian_tolerance
    # above, unchanged) takes over -- unlike the final grasp pose, a few extra
    # cm of miss here costs nothing. Loosened from ArmMotionClient's 0.03m
    # default after joint5 (one of the softer Lyapunov-gained joints) was
    # observed live to plateau at a real, small, non-shrinking ~0.032m error on
    # an intermediate pre-approach waypoint -- a normal PD steady-state limit,
    # not a bug (tried raising Kp/Kd project-wide instead first, but that
    # correlated with a reproducible return of the joint4 self-collision-like
    # freeze on the very next run, so it was reverted -- see
    # controller/lyapunov_gains.py's own 2026-07-24 comment). This tolerance
    # change is Stage-4-only and does not touch Stage 3's gains at all.
    pre_approach_cartesian_tolerance: float = 0.04

    # Number of sub-moves the pre-approach -> grasp descent is split into.
    # 2026-07-23 (Opus 4.8): a Stage-4-only companion to ArmMotionClient's
    # keep-target-fresh fix. Instead of one MoveIt2 pose-goal jump over the
    # full pre_approach_height (0.10m), the descent is broken into this many
    # smaller Cartesian sub-steps (each a straight-line position interpolation,
    # orientation held constant since pre-pose and grasp-pose share it). Two
    # benefits, both independent of any Stage 3 gain change: (1) each sub-step
    # is a short, easily-tracked trajectory that comfortably settles within the
    # keep-fresh window, and (2) it forces a clean, monotonic vertical descent
    # onto the object rather than whatever curved Cartesian path MoveIt2 might
    # pick for one larger jump near the object/floor. Only the FINAL sub-step
    # (the actual grasp pose) uses approach_convergence_tolerance; the
    # intermediate waypoints pass through at the looser default tolerance since
    # they don't need to be precise. 1 = original single-jump behavior.
    # NOTE: this does NOT reduce the final steady-state tracking error at the
    # grasp pose (that floor is set by the controller's Kp and the model
    # mismatch, unchanged here) -- it only removes the transient/path-quality
    # problems. NOT YET LIVE-VALIDATED.
    approach_num_waypoints: int = 2

    # 2026-07-24: Stage-4-only mitigation for the home->pre-approach move
    # timing out on panda_joint4/6/7 specifically. Root cause (traced via
    # live torque capture + code audit of the trajectory pipeline, self-
    # collision excludes, and actuator ranges -- all confirmed correct): the
    # Lyapunov-derived Kp for joints 4/6/7 (14.4, 5.7, 2.5 -- joint7's is the
    # SOFTEST of all seven) combined with this move asking those exact three
    # joints for a large ~45 degree swing each (unlike every previously-
    # validated move, whose deltas were all small) produces a genuine,
    # flat steady-state Cartesian error (~0.25m, unchanged across 6+ seconds
    # of active tracking) rather than a slow-but-progressing transient. This
    # does NOT touch Stage 3's gains (tied to the N3-Liu novelty claim) --
    # it splits the SE(3) path (position + orientation, via
    # GraspExecutor._interpolate_pose_waypoints) from the arm's actual
    # current pose to the pre-approach pose into this many smaller sub-steps,
    # so no single move asks joints 4/6/7 for the full ~45 degrees at once.
    # 1 = original single-jump behavior (falls back automatically if
    # ArmMotionClient.get_current_pose() is unavailable, e.g. no FK/pinocchio
    # or dry-run). NOT YET LIVE-VALIDATED.
    pre_approach_num_waypoints: int = 3

    # 2026-07-28: safe-transit-height margin [m] for the home -> pre-approach
    # leg. CONFIRMED LIVE (stage4/test_direct_joint_bypass.py, 5/5 reproducible
    # trials, contact marker observed directly on grasp_object): the previous
    # direct diagonal SE(3) interpolation from the arm's current pose to the
    # pre-approach pose has no guarantee about the height of the ELBOW/FOREARM
    # along the way (only the flange's own Cartesian path is controlled) --
    # this let the forearm sweep low across the workspace while still
    # horizontally far from the target, clipping grasp_object and producing
    # the exact "large real torque, zero motion" joint4/6/7 freeze signature
    # that was independently reproduced under three different conditions
    # (MoveIt2's own planned path, a fully deterministic bypass path, and
    # with the trained residual model removed entirely -- see
    # test_direct_joint_bypass.py's module docstring for the full
    # investigation). Fixed by routing via a safe transit height instead (see
    # GraspExecutor._transit_waypoints): lift straight up first, translate
    # horizontally at a height above both the start and target, then descend
    # straight down onto the pre-approach pose -- so the arm is never both
    # low AND horizontally far from the target at the same time.
    # transit_height_margin is added ON TOP OF max(current_z, target_z), so
    # the transit height is always at least this much above BOTH endpoints
    # regardless of where the arm starts. 0.10 m: comfortably clears
    # grasp_object's 4cm height plus this project's own observed steady-state
    # tracking error (a few cm on ordinary moves), without being so high it
    # risks other reachability issues. NOT YET LIVE-VALIDATED.
    transit_height_margin: float = 0.10

    # Pause [s] after the approach move reports convergence, before closing
    # the gripper. 2026-07-23: found live -- ArmMotionClient.move_to()
    # declares success the instant joint error first drops under its
    # tolerance, which can still be mid-settle (a PD controller doesn't stop
    # exactly at the tolerance boundary, it keeps correcting the last bit of
    # error for a short additional period). Observed live: the gripper closed
    # to near its free-space overtravel target (no real object resistance),
    # while the human visually confirmed the arm was still moving down when
    # grasp() fired -- i.e. pick() closed the fingers before the arm had
    # actually finished arriving at the object. This settle pause is a
    # Stage-4-only mitigation (does not touch Stage 3's controller/tuning);
    # NOT YET LIVE-VALIDATED.
    pre_grasp_settle_sec: float = 0.4

    # --- Payload accounting ---
    # Estimated object mass [kg] passed to the Stage 3 controller after grasping,
    # so the RNEA feedforward updates its gravity/inertia compensation.
    object_mass: float = 0.0

    # --- MoveIt2 planning-scene attachment (2026-07-23, Opus 4.8) ---
    # Id of the MoveIt2 collision object corresponding to the grasp target
    # (must match the id passed to ArmMotionClient.add_collision_box() by the
    # caller, e.g. "grasp_object"). When set AND the arm backend exposes
    # attach_object/detach_object (ArmMotionClient does; the Mock/dry-run arm
    # does not -- calls are hasattr-guarded exactly like update_payload),
    # GraspExecutor attaches this object to the gripper at the PRE_APPROACH ->
    # APPROACH transition and detaches it on release / failed grasp.
    #
    # WHY: once the cube is a MoveIt2 world obstacle (needed so the coarse
    # home->pre-approach move routes AROUND it instead of planning through it --
    # the 2026-07-23 root-cause bug), MoveIt2 would otherwise REFUSE to plan
    # the final descent whose open fingers straddle that same obstacle.
    # Attaching converts it from a static obstacle into part of the robot for
    # the descent/grasp/lift phases (fingers allowed to touch it; it rides with
    # the arm on lift). See ArmMotionClient.attach_object()'s docstring for the
    # full rationale. Leave None to disable attach/detach entirely (e.g. dry-run
    # or a scene with no registered object). NOT YET LIVE-VALIDATED.
    collision_object_name: Optional[str] = None

    # Gripper link the collision object is rigidly attached to (panda.srdf's
    # `hand` end-effector parent is panda_link8, but the hand BODY that closes
    # around the object is panda_hand -- the natural attach link).
    attach_link: str = "panda_hand"

    # 2026-07-27: real (bare) size/position of the grasp object, in the same
    # (position, size) form as ArmMotionClient.add_collision_box(). When both
    # are set, GraspExecutor._attach_object() re-registers the object at this
    # bare geometry immediately before attaching it to the gripper, instead of
    # carrying over whatever (possibly inflated) size it was registered at in
    # the world for pre-approach planning margin. See that method's own
    # 2026-07-27 comment: the inflated world box (needed so the coarse
    # home->pre-approach move keeps clearance) extends below the object's true
    # footprint, which after the floor collision box was added (2026-07-24)
    # put the ATTACHED copy in permanent, deterministic collision with the
    # floor -- failing every plan requested after attach with a generic
    # MoveIt2 FAILURE. Leave both None to skip the resize (old behavior).
    # NOT YET LIVE-VALIDATED.
    collision_object_bare_size: Optional[tuple] = None
    collision_object_position: Optional[tuple] = None
