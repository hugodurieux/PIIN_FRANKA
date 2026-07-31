"""
Stage 4 diagnostic -- bypass MoveIt2 (OMPL/KDL IK + collision-aware planning)
entirely for the home -> pre-approach leg, the exact leg where panda_joint4/6/7
have intermittently frozen (SESSION.md, 2026-07-23/24).

WHY THIS SCRIPT EXISTS (2026-07-28): every fix tried so far (self-collision
excludes, floor registration, gain retuning) targeted the EXECUTION/physics
side and none fully explained the freeze's intermittency. But
test_grasp_pick.py's own 2026-07-24 comment already recorded direct evidence
that MoveIt2's OMPL/KDL IK returns a DIFFERENT joint-space solution for the
SAME Cartesian target on different calls ("the freeze recurred ... with a
DIFFERENT IK solution for the same pre-approach target"). This script removes
that variable completely: instead of asking MoveGroup to plan (which invokes
OMPL/KDL and can pick any of several valid IK solutions for the same pose), it
computes ONE joint target via a plain, deterministic numerical IK solve
(Pinocchio damped least-squares on the same URDF used everywhere else in this
project -- see arm_motion_client.py's _FlangeFK), reuses that EXACT joint
target across every trial, and publishes a hand-built JointTrajectory directly
to /pinn_controller/desired_trajectory -- no MoveGroup action, no OMPL, no
collision-aware planning, no /apply_planning_scene calls anywhere in this path.

What a result means:
  - If the freeze now NEVER recurs across repeated trials (same fixed joint
    path every time): strong evidence the freeze was driven by WHICH IK
    solution/configuration MoveIt2 happened to choose, not by Stage 3's
    execution layer per se -- the real fix belongs in Stage 2 (constrain/seed
    OMPL's IK, or add a redundancy-resolution rule) not Stage 3 gains/physics.
  - If the freeze STILL recurs, intermittently, on this exact same fixed path
    every time: rules out IK-solution variability entirely. Combined with the
    earlier raw-torque bypass evidence (joint4 barely moved under three
    different torque regimes, SESSION.md 2026-07-24 point 7), this would point
    at something non-deterministic in the physics/execution stack itself
    (e.g. MuJoCo solver timing, a race in the ROS2 control loop) rather than
    at planning at all.
  - If it now converges every time, cleanly: the specific joint configuration
    this IK solve lands on is simply a "good" one; rerun with a different seed
    (e.g. a different q_seed passed to _solve_ik) to sample other solutions
    and see if some are reliably bad.

Prerequisites (same live stack as test_grasp_pick.py, gripper NOT required
since this script never grasps):
  - mujoco_franka_moveit.launch.py running (move_group + MuJoCo + ros2_control).
    NOTE: move_group does not need to be healthy for THIS script (it is never
    called), but the launch file brings up MuJoCo + ros2_control together, so
    it is still the simplest way to get a live sim.
  - pinn_controller_node running (bash ros2_ws/launch_pinn_controller.sh).
  - panda_effort_controller ACTIVE (bash ros2_ws/switch_to_effort.sh).

Usage:
    source /opt/ros/jazzy/setup.bash
    source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash
    source /home/hci-student/projects/pinn_franka/ros2_ws/set_pinn_env.sh
    python3 stage4/test_direct_joint_bypass.py [--seed home|neutral]

--seed selects the IK STARTING GUESS handed to the damped-least-squares
solve (see _solve_ik) -- NOT randomness (there is none anywhere in this
script). A 7-DOF arm has a 1-parameter family of valid joint solutions for
a given 6-DOF flange pose (elbow redundancy); Newton-style local descent
converges to whichever solution is nearest the seed. "home" (default)
seeds from the live 'home' keyframe reading, landing on the SAME solution
tested first (target: joint4=-2.356, joint6=2.353, joint7=-0.0002, all 5
trials froze identically). "neutral" seeds from pin.neutral(model) (all
joint angles 0), a very different starting point that Newton descent is
likely to resolve to a qualitatively different elbow configuration for
the SAME Cartesian target -- run this after the default to test whether
the freeze is specific to the first solution's configuration or universal
for this Cartesian target regardless of which valid joint solution is used.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time

import numpy as np
import pinocchio as pin
import rclpy
from mujoco_ros2_control_msgs.srv import ResetWorld
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from stage4.arm_motion_client import _DEFAULT_URDF_PATH, _JOINT_NAMES, _FlangeFK
from stage4.demo_targets import get_target

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("test_direct_joint_bypass")

# Matches GraspConfig.pre_approach_height's default -- this script targets the
# same home -> pre-approach leg GraspExecutor.pick() exercises first, since
# that is the leg where the freeze has always been observed.
_PRE_APPROACH_HEIGHT = 0.10

# Number of repeated trials over the SAME fixed joint target, each starting
# from a fresh reset_world("home"). Intermittency needs repeats to detect.
_N_TRIALS = 5

# Trajectory timing: kept in the same ballpark as MoveIt2's own historically
# observed scaled trajectories (0.71-1.15s, SESSION.md) so this is a fair
# comparison -- the only thing that should differ from the real pipeline is
# WHICH joint solution is being tracked, not how fast.
_TRAJ_DURATION_S = 1.2
_TRAJ_WAYPOINTS = 13

# Total post-publish observation window and hold-refresh interval. Refresh
# must stay under pinn_controller_node's 2.0s staleness cutoff (same pattern
# as ArmMotionClient._HOLD_REFRESH_INTERVAL).
_OBSERVE_S = 8.0
_HOLD_REFRESH_INTERVAL = 1.5

_CARTESIAN_TOLERANCE = 0.04  # matches GraspConfig.pre_approach_cartesian_tolerance


def _solve_ik(
    fk: _FlangeFK,
    target_pose: np.ndarray,
    q_seed: np.ndarray,
    max_iters: int = 1000,
    eps: float = 1e-4,
    dt: float = 0.3,
    damp: float = 1e-10,
) -> tuple[np.ndarray, bool, int]:
    """Deterministic damped-least-squares IK (Pinocchio's standard CLIK
    recipe, frame version) -- NO randomness anywhere, so the SAME q_seed and
    target_pose always produce the SAME q, unlike MoveIt2's OMPL/KDL solver.
    """
    model, data, frame_id = fk.model, fk.data, fk.frame_id
    oMdes = pin.SE3(
        np.asarray(target_pose[:3, :3], dtype=float),
        np.asarray(target_pose[:3, 3], dtype=float),
    )
    q = q_seed.copy()
    for i in range(max_iters):
        pin.forwardKinematics(model, data, q)
        pin.updateFramePlacements(model, data)
        dMf = data.oMf[frame_id].actInv(oMdes)
        err = pin.log(dMf).vector
        if np.linalg.norm(err) < eps:
            return q, True, i
        J = pin.computeFrameJacobian(model, data, q, frame_id, pin.LOCAL)
        J = -pin.Jlog6(dMf.inverse()) @ J
        v = -J.T @ np.linalg.solve(J @ J.T + damp * np.eye(6), err)
        q = pin.integrate(model, q, v * dt)
    return q, False, max_iters


def _q_from_dict(fk: _FlangeFK, joint_dict: dict) -> np.ndarray:
    q = pin.neutral(fk.model)
    for name, val in joint_dict.items():
        if fk.model.existJointName(name):
            q[fk.model.idx_qs[fk.model.getJointId(name)]] = val
    return q


def _q_to_positions(fk: _FlangeFK, q: np.ndarray, names: list[str]) -> list[float]:
    return [float(q[fk.model.idx_qs[fk.model.getJointId(n)]]) for n in names]


def _build_trajectory(
    names: list[str], start: list[float], end: list[float], n_wp: int, duration_s: float
) -> JointTrajectory:
    traj = JointTrajectory()
    traj.joint_names = list(names)
    points = []
    for k in range(n_wp):
        frac = k / (n_wp - 1) if n_wp > 1 else 1.0
        t = frac * duration_s
        pt = JointTrajectoryPoint()
        pt.positions = [(1.0 - frac) * s + frac * e for s, e in zip(start, end)]
        pt.time_from_start.sec = int(t)
        pt.time_from_start.nanosec = int((t - int(t)) * 1e9)
        points.append(pt)
    traj.points = points
    return traj


def _build_hold(names: list[str], positions: list[float]) -> JointTrajectory:
    traj = JointTrajectory()
    traj.joint_names = list(names)
    pt = JointTrajectoryPoint()
    pt.positions = list(positions)
    traj.points = [pt]
    return traj


class _DirectBypassNode(Node):
    def __init__(self) -> None:
        super().__init__("stage4_direct_joint_bypass")
        self._pub = self.create_publisher(JointTrajectory, "/pinn_controller/desired_trajectory", 10)
        self._joint_state: JointState | None = None
        self.create_subscription(JointState, "/joint_states", self._on_joint_state, 10)
        self._reset_client = self.create_client(ResetWorld, "/mujoco_ros2_control_node/reset_world")

    def _on_joint_state(self, msg: JointState) -> None:
        self._joint_state = msg

    def wait_for_joint_state(self, timeout_s: float = 5.0) -> dict:
        deadline = time.monotonic() + timeout_s
        self._joint_state = None
        while self._joint_state is None and time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.05)
        if self._joint_state is None:
            raise RuntimeError("No /joint_states received within timeout")
        return dict(zip(self._joint_state.name, self._joint_state.position))

    def reset_world_home(self, timeout_s: float = 5.0) -> None:
        if not self._reset_client.wait_for_service(timeout_sec=timeout_s):
            raise RuntimeError("/mujoco_ros2_control_node/reset_world service not available")
        req = ResetWorld.Request()
        req.keyframe = "home"
        future = self._reset_client.call_async(req)
        deadline = time.monotonic() + timeout_s
        while not future.done() and time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.05)
        if not future.done():
            raise RuntimeError("reset_world call timed out")
        # Give the sim a moment to settle at the keyframe before reading state.
        for _ in range(20):
            rclpy.spin_once(self, timeout_sec=0.05)
        time.sleep(0.3)


def _run_trial(node: _DirectBypassNode, fk: _FlangeFK, q_target: np.ndarray, target_position: np.ndarray, trial_idx: int) -> dict:
    log.info("=== Trial %d/%d: resetting world to 'home' ===", trial_idx + 1, _N_TRIALS)
    node.reset_world_home()
    current_by_name = node.wait_for_joint_state()

    start_positions = [current_by_name[n] for n in _JOINT_NAMES]
    end_positions = _q_to_positions(fk, q_target, _JOINT_NAMES)

    traj = _build_trajectory(_JOINT_NAMES, start_positions, end_positions, _TRAJ_WAYPOINTS, _TRAJ_DURATION_S)
    node._pub.publish(traj)
    publish_time = time.monotonic()
    # DDS discovery grace, same pattern as ArmMotionClient.move_to().
    for _ in range(20):
        rclpy.spin_once(node, timeout_sec=0.05)
    time.sleep(0.5)

    # Let the ramp actually play out (anchored on publish_time, matching
    # ArmMotionClient's 2026-07-27 fix) BEFORE starting the hold-refresh loop
    # below -- otherwise the hold-refresh's immediate first republish would
    # overwrite the smooth multi-waypoint ramp with a single-point step
    # command before it ever got to interpolate through its waypoints.
    ramp_deadline = publish_time + _TRAJ_DURATION_S
    while time.monotonic() < ramp_deadline:
        rclpy.spin_once(node, timeout_sec=0.05)

    hold_traj = _build_hold(_JOINT_NAMES, end_positions)
    last_refresh = 0.0
    last_log = time.monotonic()
    deadline = publish_time + _OBSERVE_S
    last_diffs: dict = {}
    last_cart_err = None

    while time.monotonic() < deadline:
        now = time.monotonic()
        if now - last_refresh >= _HOLD_REFRESH_INTERVAL:
            node._pub.publish(hold_traj)
            last_refresh = now
        rclpy.spin_once(node, timeout_sec=0.05)
        if node._joint_state is not None:
            current_by_name = dict(zip(node._joint_state.name, node._joint_state.position))
            last_diffs = {
                n: current_by_name[n] - t
                for n, t in zip(_JOINT_NAMES, end_positions)
                if n in current_by_name
            }
            try:
                cur_pos = fk.flange_position(current_by_name)
                last_cart_err = float(np.linalg.norm(cur_pos - target_position))
            except Exception:  # noqa: BLE001
                pass

            if now - last_log >= 1.0:
                worst = max(last_diffs, key=lambda n: abs(last_diffs[n])) if last_diffs else "n/a"
                cart_str = f", flange_err={last_cart_err:.4f} m" if last_cart_err is not None else ""
                log.info(
                    "  t=%.1fs worst=%s diff=%+.4f rad, diffs=%s%s",
                    now - publish_time,
                    worst,
                    last_diffs.get(worst, float("nan")),
                    {n: round(d, 4) for n, d in last_diffs.items()},
                    cart_str,
                )
                last_log = now

    converged = last_cart_err is not None and last_cart_err < _CARTESIAN_TOLERANCE
    worst = max(last_diffs, key=lambda n: abs(last_diffs[n])) if last_diffs else "n/a"
    log.info(
        "Trial %d/%d RESULT: converged=%s final_flange_err=%s worst_joint=%s diffs=%s",
        trial_idx + 1,
        _N_TRIALS,
        converged,
        f"{last_cart_err:.4f} m" if last_cart_err is not None else "n/a",
        worst,
        {n: round(d, 4) for n, d in last_diffs.items()},
    )
    return {
        "trial": trial_idx + 1,
        "converged": converged,
        "final_flange_err": last_cart_err,
        "worst_joint": worst,
        "diffs": last_diffs,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seed",
        choices=["home", "neutral"],
        default="home",
        help="IK starting guess (see module docstring). Default: home.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    rclpy.init()
    node = _DirectBypassNode()
    try:
        fk = _FlangeFK(_DEFAULT_URDF_PATH, tip_link="panda_link8")

        target_pose = get_target("grasp_object")
        z_axis = target_pose[:3, 2]
        pre_approach_pose = target_pose.copy()
        pre_approach_pose[:3, 3] -= _PRE_APPROACH_HEIGHT * z_axis
        target_position = pre_approach_pose[:3, 3]

        log.info("Resetting world to 'home' before computing the fixed IK target...")
        node.reset_world_home()
        home_by_name = node.wait_for_joint_state()

        if args.seed == "neutral":
            q_seed = pin.neutral(fk.model)
            log.info("IK seed: 'neutral' (all joint angles 0) -- expect a DIFFERENT solution than the 'home'-seeded run.")
        else:
            q_seed = _q_from_dict(fk, home_by_name)
            log.info("IK seed: 'home' (live keyframe reading).")

        log.info("Solving deterministic IK for the pre-approach pose (seed=%s)...", args.seed)
        q_target, ik_converged, iters = _solve_ik(fk, pre_approach_pose, q_seed)
        if not ik_converged:
            log.error("IK did NOT converge after %d iterations -- aborting, target is unreliable.", iters)
            return 1
        log.info(
            "IK converged in %d iterations. Fixed target joint angles [rad]: %s",
            iters,
            dict(zip(_JOINT_NAMES, _q_to_positions(fk, q_target, _JOINT_NAMES))),
        )

        results = [
            _run_trial(node, fk, q_target, target_position, i) for i in range(_N_TRIALS)
        ]

        log.info("=" * 70)
        log.info("SUMMARY (%d trials, SAME fixed joint target, MoveIt2/OMPL bypassed):", _N_TRIALS)
        n_converged = sum(1 for r in results if r["converged"])
        for r in results:
            log.info(
                "  trial %d: converged=%s final_flange_err=%s worst_joint=%s",
                r["trial"],
                r["converged"],
                f"{r['final_flange_err']:.4f} m" if r["final_flange_err"] is not None else "n/a",
                r["worst_joint"],
            )
        log.info("%d/%d trials converged.", n_converged, _N_TRIALS)
        if n_converged == _N_TRIALS:
            log.info(
                "ALL converged on a FIXED path -> the freeze is NOT explained by "
                "static geometry/physics at this configuration; suspect IK-solution "
                "variability (Stage 2/OMPL) as the driver when it happens live."
            )
        elif n_converged == 0:
            log.info(
                "ALL froze on a FIXED, deterministic path -> IK-solution variability "
                "is ruled out; the fault is downstream of planning (execution/physics)."
            )
        else:
            log.info(
                "MIXED result on a FIXED path -> the freeze is intermittent even with "
                "IK variability removed; suspect non-deterministic execution/physics "
                "timing, not which solution was chosen."
            )
        return 0
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    sys.exit(main())
