#!/bin/bash
source /home/hci-student/projects/pinn_franka/ros2_ws/set_pinn_env.sh
source /opt/ros/jazzy/setup.bash
source /home/hci-student/projects/pinn_franka/ros2_ws/install/setup.bash
ros2 launch pinn_franka_controller pinn_controller.launch.py \
    urdf_path:=/home/hci-student/projects/pinn_franka/pinocchio_baseline/panda.urdf \
    checkpoint_path:=/home/hci-student/projects/pinn_franka/models/run_20260716_121302/greybox_best.pt
