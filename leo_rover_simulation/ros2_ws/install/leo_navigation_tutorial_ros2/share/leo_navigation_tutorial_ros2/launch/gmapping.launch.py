"""import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import SetParameter
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    ld = LaunchDescription()

    # Specify the name of the package and path to xacro file in external package
    pkg_name = 'gui_controller_leo'

    # Start simulation
    launch_sim_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(pkg_name), 'launch'),
            '/simulation_bringup.launch.py'])
    )

    # Start SLAM Toolbox with default parameters
    launch_slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'), 'launch'),
            '/online_async_launch.py'])
    )

    # Add actions to LaunchDescription
    # SLAM Toolbox
    ld.add_action(launch_slam_toolbox)
    # Use simulation time for SLAM
    ld.add_action(SetParameter(name='use_sim_time', value=True))
    # SLAM Toolbox
    ld.add_action(launch_sim_world)

    return ld"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node, SetParameter
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    ld = LaunchDescription()

    # Specify the name of the package and path to xacro file in external package
    pkg_name = 'gui_controller_leo'

    # Start simulation
    launch_sim_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(pkg_name), 'launch'),
            '/simulation_bringup.launch.py'])
    )

    # Path to the slam_gmapping.yaml file
    slam_gmapping_config = os.path.join(
        get_package_share_directory(pkg_name),  # Adjust pkg_name if needed
        'config',
        'slam_gmapping.yaml'
    )

    # Start SLAM Toolbox with slam_gmapping.yaml parameters
    launch_slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'), 'launch'),
            '/online_async_launch.py']),
        launch_arguments={'params_file': slam_gmapping_config}.items()  # Pass the YAML file
    )

    # Add actions to LaunchDescription
    # Use simulation time
    ld.add_action(SetParameter(name='use_sim_time', value=True))
    # Add SLAM Toolbox
    ld.add_action(launch_slam_toolbox)
    ld.add_action(launch_sim_world)

    return ld
