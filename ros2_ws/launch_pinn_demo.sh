#!/bin/bash
# =====================================================================
# THE STAGE 4 DEMO LAUNCHER -- this is the shipped configuration.
#
# Terminal 2 of the startup sequence. See SESSION.md for the full order;
# in short: rebuild_and_relaunch_sim.sh, then THIS, then switch_to_effort.sh,
# then stage4/test_grasp_pick.py.
#
#   bash ros2_ws/launch_pinn_demo.sh            # margin 4.0 (validated)
#   bash ros2_ws/launch_pinn_demo.sh 4.0        # same, explicit
#
# WHY THE LEARNED RESIDUAL IS OFF HERE
# ------------------------------------
# Not an oversight, and not a leftover debug flag. It is what the measurements
# say. Phase F, 2026-07-29, x=0.55, margin 4.0, every other variable identical,
# 3 runs with the residual on against 2 with it off:
#
#     residual ON    joint5 bias -0.0337 rad    flange error 14.3 mm
#     residual OFF   joint5 bias -0.0015 rad    flange error  7.5 mm
#
# A 22x reduction in steady-state bias and a halved Cartesian error, with every
# joint improving by roughly an order of magnitude -- not just joint5. The gain
# confound pushes the OTHER way (a lower Kp would make e_ss = tau/Kp larger),
# so the result survives it.
#
# The cause is domain transfer, NOT a failure of the grey-box approach. The
# checkpoint below was trained on Isaac Sim and is being run in MuJoCo, so it
# adds the gap between RNEA and *Isaac's* dynamics to a simulator that does not
# have them. It is extrapolating outside its training domain and doing it badly.
#
# WHAT IT WOULD TAKE TO TURN IT BACK ON
# -------------------------------------
# generate_mujoco_dataset.py collects in-domain data from this very MJCF via
# mj_inverse (minutes, no Isaac needed). Retrain or fine-tune on it, then re-run
# the phase F comparison with launch_pinn_controller_ablation.sh as the control.
# The bar to clear is already measured and written above: beat 7.5 mm.
# Until something clears that bar, OFF is the honest configuration to demo.
#
# WHY THE MARGIN IS PASSED EXPLICITLY
# -----------------------------------
# gain_safety_margin_override=4.0 is NOT the default in lyapunov_gains.py, and
# every phase A/F run used it. Omitting it silently reverts Kp to the Lyapunov
# default and changes exactly the quantity the numbers above describe. That is
# the specific trap in launch_pinn_controller_no_residual.sh, which is why that
# script now forwards here instead of launching anything itself.
#
# Single-line ros2 launch on purpose: multi-line backslash continuations and
# long pasted commands have repeatedly been corrupted by terminal line-wrapping
# in this project (CLAUDE.md Lesson #2 -- it silently dropped checkpoint_path
# and invalidated run18).
# =====================================================================
source /home/hci-student/projects/pinn_franka/ros2_ws/set_pinn_env.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash

MARGIN="${1:-4.0}"

echo "====================================================================="
echo " STAGE 4 DEMO  --  shipped configuration"
echo "   tau_cmd = RNEA(q,qdot,qddot) + PD(error)      [learned residual OFF]"
echo "   gain_safety_margin_override = ${MARGIN}"
echo ""
echo " The residual is OFF deliberately: with the Isaac-trained checkpoint it"
echo " degrades MuJoCo tracking (joint5 bias 22x, flange error 2x). See this"
echo " script's header. To measure it ON, use launch_pinn_controller_ablation.sh"
echo " -- which is the SAME configuration plus the residual, so the two are"
echo " directly comparable."
echo "====================================================================="

ros2 launch pinn_franka_controller pinn_controller.launch.py urdf_path:=/home/hci-student/projects/pinn_franka/pinocchio_baseline/panda.urdf checkpoint_path:=/home/hci-student/projects/pinn_franka/models/run_20260716_121302/greybox_best.pt gain_safety_margin_override:=${MARGIN} disable_residual:=true
