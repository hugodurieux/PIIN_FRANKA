#!/bin/bash
# Stage 3 debug -- sibling of test_joint4_raw_torque.sh (2026-07-23/24),
# written 2026-07-28. Bypasses pinn_controller_node entirely and publishes a
# raw, constant, unambiguous torque directly to
# /panda_effort_controller/commands, this time isolating panda_joint7 alone.
#
# WHY: same rationale as test_joint6_raw_torque.sh -- panda_joint7 has only
# ever been observed frozen alongside panda_joint4 in a multi-joint move,
# never tested completely alone. This checks whether it shares joint4's
# confirmed isolated-immobility property.
#
# 10 Nm: safely under panda_joint7's +/-12 Nm ctrlrange. Its gravity-comp
# torque near 'home' is close to 0 Nm (see pinn_controller_node's [DEBUG tau]
# logs, rnea~=-0.000 Nm for j7 near home), so 10 Nm here is almost entirely
# unopposed -- an even more decisive test than joint4/6's, if the joint is
# actually free to move.
#
# PREREQUISITE, SAME AS test_joint4_raw_torque.sh: panda_effort_controller
# must be ACTIVE (bash ros2_ws/switch_to_effort.sh) and pinn_controller_node
# must NOT be running (verify with `ros2 node list` -- confirmed live
# 2026-07-28 that a still-running pinn_controller_node silently invalidates
# this style of test by overwriting it on the same topic at 1kHz).
#
# Usage: bash ros2_ws/switch_to_effort.sh && bash ros2_ws/test_joint7_raw_torque.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

echo "Publishing 10 Nm to panda_joint7 only, 0 to all others, for 5 seconds..."
timeout 5 ros2 topic pub -r 50 /panda_effort_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0]}"
echo "Done."
