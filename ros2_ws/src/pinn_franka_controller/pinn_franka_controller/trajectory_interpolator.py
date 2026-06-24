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

    Raises
    ------
    ValueError
        If the trajectory is empty or a waypoint has fewer positions than
        ``n_joints``.
    """

    def __init__(
        self, trajectory: JointTrajectory, n_joints: int = 7
    ) -> None:
        points = trajectory.points
        if len(points) == 0:
            raise ValueError("Cannot interpolate an empty trajectory.")

        self._n_joints = n_joints
        n_pts = len(points)

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
            self._positions[i, :] = pt.positions[:n_joints]

            # Velocities (optional)
            if len(pt.velocities) >= n_joints:
                self._velocities[i, :] = pt.velocities[:n_joints]

            # Accelerations (optional)
            if len(pt.accelerations) >= n_joints:
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

    print("TrajectoryInterpolator smoke test passed.")
