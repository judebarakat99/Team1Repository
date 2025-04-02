import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node



def generate_launch_description():
    # Get package directories
    pkg_leo_simulator = get_package_share_directory("leo_simulator")

    # Include the existing Leo Rover simulation launch file
    leo_simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_leo_simulator, "leo_gz_bringup", "launch", "leo_gz.launch.py"))
    )
    #leo_simulation = IncludeLaunchDescription(
    #    PythonLaunchDescriptionSource(os.path.join(pkg_leo_gz_bringup, "launch", "leo_gz.launch.py"))
    #)

    """ 
    # Launch RViz
    rviz_config_path = os.path.join(pkg_leo_simulator, "rviz", "default.rviz")
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_path],
        output="screen",
    )
    """
    # Launch the GUI controller
    gui_controller = Node(
        package="gui_controller_leo",
        executable="gui_controller",
        name="gui_controller",
        output="screen",
    )

    return LaunchDescription([
        leo_simulation,  # Starts Gazebo with the Leo Rover
        #rviz_node,       # Starts RViz for visualisation
        gui_controller,  # Starts GUI for manual control
    ])
