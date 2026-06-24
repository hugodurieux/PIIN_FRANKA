"""
Stage 2 -- ROS2 Humble package setup for pinn_franka_controller.

This package provides the ROS2 node that bridges MoveIt2 trajectory planning
with the Stage 3 computed-torque + PD controller backed by the PINN dynamics
model trained in Stage 1.
"""

import os
from glob import glob

from setuptools import find_packages, setup

package_name = "pinn_franka_controller"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        # Register the package with ament index
        (
            os.path.join("share", "ament_index", "resource_index", "packages"),
            [os.path.join("resource", package_name)],
        ),
        # Install package.xml
        (os.path.join("share", package_name), ["package.xml"]),
        # Install launch files
        (
            os.path.join("share", package_name, "launch"),
            glob(os.path.join("launch", "*launch.[pxy][yma]*")),
        ),
        # Install config files
        (
            os.path.join("share", package_name, "config"),
            glob(os.path.join("config", "*.yaml")),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Hugo Durieux",
    maintainer_email="hugodurieuxh@gmail.com",
    description="PINN-based torque controller node for Franka Panda (ROS2 Humble)",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "pinn_controller_node = pinn_franka_controller.pinn_controller_node:main",
        ],
    },
)
