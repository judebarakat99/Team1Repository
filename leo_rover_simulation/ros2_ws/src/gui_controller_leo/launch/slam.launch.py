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


    # Start SLAM Toolbox with default parameters
    launch_slam_toolbox = IncludeLaunchDescription(
      PythonLaunchDescriptionSource([os.path.join(
         get_package_share_directory('slam_toolbox'), 'launch'),
         '/online_async_launch.py'])
      )




    # Add actions to LaunchDescription
    # Simulation
    ld.add_action(SetParameter(name='use_sim_time', value=True))
    ld.add_action(launch_sim_world)
    # SLAM Toolbox
    ld.add_action(launch_slam_toolbox)
    # Visualisation
    #ld.add_action(node_rviz)
    return ld

