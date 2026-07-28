"""
Stage 2 -- Linear interpolator for ``trajectory_msgs/JointTrajectory`` messages.

PLAN (3 sentences):
TrajectoryInterpolator stores the waypoints of a JointTrajectory message and
provides linear interpolation of (q_des, qdot_des, qddot_des) at any query time,
serving goal.md objective #2 by supplying smooth reference signals to the 1 kHz
control loop.  It handles edge cases (single-point trajectory, query past the end)
by holding the last waypoint constant.  All arrays are float64 for ROS2 compatibility.
"""

from __future__ import annotations

import numpy as np
from trajectory_msgs.msg import JointTrajectory


class TrajectoryInterpolator:
    """Linear interpolator over a ``JointTrajectory`` message.

    Given a ROS2 ``JointTrajectory`` message, this class pre-extracts the
    position, velocity, and acceleration arrays from each waypoint and provides
    a ``interpolate(t)`` method that returns linearly-interpolated values at
    an arbitrary query time *t* (seconds from trajectory start).

    Parameters
    ----------
    trajectory : JointTrajectory
        A non-empty ``JointTrajectory`` message.  Each ``JointTrajectoryPoint``
        must have ``positions`` populated; ``velocities`` and ``accelerations``
        are optional (default to zero).
    n_joints : int
        Expected number of joints (default 7 for Franka Panda).
    expected_joint_names : list[str] | None
        The joint order the CALLER wants back from ``interpolate()`` (e.g.
        pinn_controller_node's own ``_JOINT_NAMES``, panda_joint1..7). If
        given, and ``trajectory.joint_names`` is present and non-empty, each
        waypoint's positions/velocities/accelerations are reordered BY NAME
        into this order before being stored -- NOT assumed to already match
        it positionally. If omitted (default None), falls back to the
        original positional-slice behavior (see the 2026-07-23 note below).

        2026-07-23: found live -- this class previously ALWAYS used a raw
        positional slice (``pt.positions[:n_joints]``), completely ignoring
        ``trajectory.joint_names``, silently assuming waypoint index i always
        corresponds to joint i. That held for every trajectory this node had
        received so far because all of them came from moveit_plan_bridge.py's
        joint-space goals, where MoveIt2 happens to preserve canonical
        1..7 order. ArmMotionClient (stage4/arm_motion_client.py) is the
        first CARTESIAN pose-goal path in this project, and Cartesian/IK-
        solved MoveIt2 requests are not guaranteed to return joint_names in
        that same order. Live symptom that led here: panda_joint4/6/7 froze
        bit-identical at their starting values across two separate pre-
        approach moves, while the other four joints moved -- consistent with
        those three receiving desired positions meant for different joints
        (or otherwise scrambled), not a controller/tuning limitation. This
        is the same bug CLASS already found and fixed once on the
        /joint_states INPUT side (see pinn_controller_node.py's own
        _arm_indices() and its docstring) -- just never applied to this
        second, independent place that also assumed positional order. NOT
        YET LIVE-VALIDATED (prepared without simulator access).

    Raises
    ------
    ValueError
        If the trajectory is empty, a waypoint has fewer positions than
        ``n_joints``, or ``expected_joint_names`` is given but a name in it
        is missing from ``trajectory.joint_names``.
    """

    def __init__(
        self,
        trajectory: JointTrajectory,
        n_joints: int = 7,
        expected_joint_names: list[str] | None = None,
    ) -> None:
        points = trajectory.points
        if len(points) == 0:
            raise ValueError("Cannot interpolate an empty trajectory.")

        self._n_joints = n_joints
        n_pts = len(points)

        # Build a by-name reorder index if the caller told us what order it
        # wants and the message actually carries names to look up -- same
        # pattern as pinn_controller_node.py's _arm_indices(). None means
        # "trust positional order" (the original, riskier behavior).
        reorder_idx: list[int] | None = None
        traj_joint_names = list(getattr(trajectory, "joint_names", []) or [])
        if expected_joint_names is not None and traj_joint_names:
            try:
                reorder_idx = [traj_joint_names.index(j) for j in expected_joint_names]
            except ValueError as exc:
                raise ValueError(
                    f"expected_joint_names={expected_joint_names} not all found "
                    f"in trajectory.joint_names={traj_joint_names}."
                ) from exc

        # Pre-allocate arrays: shape (n_pts, n_joints)
        self._times = np.empty(n_pts, dtype=np.float64)
        self._positions = np.zeros((n_pts, n_joints), dtype=np.float64)
        self._velocities = np.zeros((n_pts, n_joints), dtype=np.float64)
        self._accelerations = np.zeros((n_pts, n_joints), dtype=np.float64)

        for i, pt in enumerate(points):
            # Time from start (convert builtin_interfaces/Duration to seconds)
            self._times[i] = pt.time_from_start.sec + pt.time_from_start.nanosec * 1e-9

            # Positions (required)
            if len(pt.positions) < n_joints:
                raise ValueError(
                    f"Waypoint {i} has {len(pt.positions)} positions, "
                    f"expected >= {n_joints}."
                )
            if reorder_idx is not None:
                self._positions[i, :] = [pt.positions[j] for j in reorder_idx]
            else:
                self._positions[i, :] = pt.positions[:n_joints]

            # Velocities (optional)
            if len(pt.velocities) >= n_joints:
                if reorder_idx is not None:
                    self._velocities[i, :] = [pt.velocities[j] for j in reorder_idx]
                else:
                    self._velocities[i, :] = pt.velocities[:n_joints]

            # Accelerations (optional)
            if len(pt.accelerations) >= n_joints:
                if reorder_idx is not None:
                    self._accelerations[i, :] = [pt.accelerations[j] for j in reorder_idx]
                else:
                    self._accelerations[i, :] = pt.accelerations[:n_joints]

        self._t_start = self._times[0]
        self._t_end = self._times[-1]

    @property
    def duration(self) -> float:
        """Total trajectory duration in seconds."""
        return float(self._t_end - self._t_start)

    @property
    def n_points(self) -> int:
        """Number of waypoints."""
        return len(self._times)

    def interpolate(
        self, t_sec: float
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Linearly interpolate the trajectory at time *t_sec*.

        Parameters
        ----------
        t_sec : float
            Query time in seconds (relative to trajectory start, i.e. the same
            time base as ``time_from_start`` in the original message).

        Returns
        -------
        q_des : np.ndarray, shape (7,)
            Desired joint positions [rad].
        qdot_des : np.ndarray, shape (7,)
            Desired joint velocities [rad/s].
        qddot_des : np.ndarray, shape (7,)
            Desired joint accelerations [rad/s^2].

        Notes
        -----
        - If ``t_sec <= t_start``, the first waypoint is returned.
        - If ``t_sec >= t_end``, the last waypoint is returned (hold).
        - Between waypoints, linear interpolation is used.
        """
        n = self._n_joints

        # --- Clamp to first point ------------------------------------
        if t_sec <= self._t_start or len(self._times) == 1:
            return (
                self._positions[0].copy(),
                self._velocities[0].copy(),
                self._accelerations[0].copy(),
            )

        # --- Clamp to last point (hold) ------------------------------
        if t_sec >= self._t_end:
            return (
                self._positions[-1].copy(),
                self._velocities[-1].copy(),
                self._accelerations[-1].copy(),
            )

        # --- Find the surrounding segment [i, i+1] -------------------
        # np.searchsorted returns the index where t_sec would be inserted
        # to keep self._times sorted.  We want the segment before that.
        idx = int(np.searchsorted(self._times, t_sec, side="right"))
        idx = max(1, min(idx, len(self._times) - 1))  # safety clamp

        t0 = self._times[idx - 1]
        t1 = self._times[idx]
        dt = t1 - t0

        if dt < 1e-12:
            # Degenerate segment (two waypoints at the same time)
            alpha = 0.0
        else:
            alpha = (t_sec - t0) / dt

        q_des = (1.0 - alpha) * self._positions[idx - 1] + alpha * self._positions[idx]
        qdot_des = (1.0 - alpha) * self._velocities[idx - 1] + alpha * self._velocities[idx]
        qddot_des = (
            (1.0 - alpha) * self._accelerations[idx - 1]
            + alpha * self._accelerations[idx]
        )

        return q_des, qdot_des, qddot_des


# =====================================================================
# __main__ smoke test (runs with plain numpy only, no ROS2 required)
# =====================================================================
if __name__ == "__main__":
    # Minimal smoke test using a mock trajectory structure.
    # This avoids importing ROS2 message types so it can run anywhere.
    from types import SimpleNamespace

    def _make_duration(sec: int, nanosec: int = 0) -> SimpleNamespace:
        return SimpleNamespace(sec=sec, nanosec=nanosec)

    def _make_point(
        t_sec: float, positions: list[float]
    ) -> SimpleNamespace:
        return SimpleNamespace(
            time_from_start=_make_duration(int(t_sec), int((t_sec % 1) * 1e9)),
            positions=positions,
            velocities=[0.0] * len(positions),
            accelerations=[0.0] * len(positions),
        )

    fake_traj = SimpleNamespace(
        points=[
            _make_point(0.0, [0.0] * 7),
            _make_point(1.0, [1.0] * 7),
            _make_point(2.0, [2.0] * 7),
        ]
    )

    interp = TrajectoryInterpolator(fake_traj, n_joints=7)  # type: ignore[arg-type]

    q0, _, _ = interp.interpolate(0.0)
    assert np.allclose(q0, 0.0), f"Expected 0.0 at t=0, got {q0}"

    q_mid, _, _ = interp.interpolate(0.5)
    assert np.allclose(q_mid, 0.5), f"Expected 0.5 at t=0.5, got {q_mid}"

    q_end, _, _ = interp.interpolate(2.0)
    assert np.allclose(q_end, 2.0), f"Expected 2.0 at t=2.0, got {q_end}"

    q_past, _, _ = interp.interpolate(5.0)
    assert np.allclose(q_past, 2.0), f"Expected hold at 2.0 past end, got {q_past}"

    # 2026-07-23: regression test for the by-name reordering fix -- a
    # trajectory whose joint_names is NOT in canonical order (mimicking a
    # Cartesian-goal MoveIt2 plan) must still land each value on the right
    # joint once expected_joint_names is given.
    _CANONICAL = [f"panda_joint{i}" for i in range(1, 8)]
    _SCRAMBLED = [
        "panda_joint1", "panda_joint2", "panda_joint3",
        "panda_joint7", "panda_joint5", "panda_joint6", "panda_joint4",
    ]
    # position value == joint index * 10 (panda_joint1 -> 10.0, ..., panda_joint7 -> 70.0),
    # listed in _SCRAMBLED order so a positional (non-reordering) read would get this wrong.
    _scrambled_positions = [10.0, 20.0, 30.0, 70.0, 50.0, 60.0, 40.0]

    def _make_point_named(t_sec: float, positions: list[float]) -> SimpleNamespace:
        return SimpleNamespace(
            time_from_start=_make_duration(int(t_sec), int((t_sec % 1) * 1e9)),
            positions=positions,
            velocities=[0.0] * len(positions),
            accelerations=[0.0] * len(positions),
        )

    scrambled_traj = SimpleNamespace(
        joint_names=_SCRAMBLED,
        points=[_make_point_named(0.0, _scrambled_positions)],
    )

    interp_reordered = TrajectoryInterpolator(  # type: ignore[arg-type]
        scrambled_traj, n_joints=7, expected_joint_names=_CANONICAL
    )
    q_reordered, _, _ = interp_reordered.interpolate(0.0)
    expected = np.array([10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0])
    assert np.allclose(q_reordered, expected), (
        f"Reordering fix failed: expected {expected}, got {q_reordered}"
    )

    # Without expected_joint_names, behavior stays positional (unchanged,
    # backward compatible) -- confirm it does NOT match the reordered result,
    # i.e. the fix only activates when explicitly requested.
    interp_positional = TrajectoryInterpolator(  # type: ignore[arg-type]
        scrambled_traj, n_joints=7
    )
    q_positional, _, _ = interp_positional.interpolate(0.0)
    assert not np.allclose(q_positional, expected), (
        "Expected positional (non-reordered) read to differ from the "
        "reordered result on a scrambled trajectory."
    )

    print("TrajectoryInterpolator smoke test passed.")
