#!/bin/bash
# =====================================================================
# DEPRECATED 2026-08-13 -- this script now forwards to launch_pinn_demo.sh.
#
# It used to launch the controller with disable_residual:=true but WITHOUT
# gain_safety_margin_override, so it silently reverted Kp to the Lyapunov
# default while also switching the residual off. Steady-state error is
# e_ss = tau/Kp, so that changed two things at once and made every number it
# produced uninterpretable.
#
# That mattered little while it was one diagnostic among many. It matters a lot
# now that the demo ships with the residual OFF, because this is the most
# obvious name to reach for and it was the wrong script. Rather than delete it
# and leave a dangling reference in the notes, it forwards.
#
#   For the demo:        bash ros2_ws/launch_pinn_demo.sh
#   For the ablation:    bash ros2_ws/launch_pinn_controller_ablation.sh
#   For residual ON:     bash ros2_ws/launch_pinn_controller_boosted.sh 4.0
# =====================================================================
echo "NOTE: launch_pinn_controller_no_residual.sh is deprecated." >&2
echo "      It omitted gain_safety_margin_override, changing Kp and the" >&2
echo "      residual at once. Forwarding to launch_pinn_demo.sh, which is" >&2
echo "      the same intent with the gains held at the validated margin 4.0." >&2
echo "" >&2

exec bash /home/hci-student/projects/pinn_franka/ros2_ws/launch_pinn_demo.sh "$@"
