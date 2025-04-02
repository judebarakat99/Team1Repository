"""import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch_ros.actions import Node, SetParameter
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro
import os


def generate_launch_description():
    ld = LaunchDescription()

    # Specify the name of the package and path to the launch file
    pkg_name = 'leo_gz_bringup'
    launch_file_subpath = 'launch/leo_gz.launch.py'
    launch_file_path = os.path.join(get_package_share_directory(pkg_name), launch_file_subpath)

    # Include the simulation launch file
    simulation_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(launch_file_path)
    )

    # Add the simulation launch to the LaunchDescription
    ld.add_action(simulation_node)

    return ld

"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch_ros.actions import Node, SetParameter
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
import xacro


def generate_launch_description():
    ld = LaunchDescription()

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'gui_controller_leo'
    file_subpath = 'urdf/leo_sim.urdf.xacro'
    sdf_path = os.path.join(get_package_share_directory(pkg_name), 'worlds', 'tb3.sdf')

    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory('leo_description'), file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # Set ignition resource path (so it can find your world files)
    ign_resource_path = SetEnvironmentVariable(name='IGN_GAZEBO_RESOURCE_PATH',
                                               value=[os.path.join(get_package_share_directory(pkg_name), 'worlds')])

    if 'IGN_GAZEBO_RESOURCE_PATH' in os.environ:
        gz_world_path = os.environ['IGN_GAZEBO_RESOURCE_PATH'] + os.pathsep + os.path.join(
            get_package_share_directory(pkg_name), "worlds")
    else:
        gz_world_path = os.path.join(get_package_share_directory(pkg_name), "worlds")

    ign_resource_path_update = SetEnvironmentVariable(name='IGN_GAZEBO_RESOURCE_PATH', value=[gz_world_path])


    # Include the Gazebo launch file
    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('ros_gz_sim'), '/launch', '/gz_sim.launch.py']),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items(),
    )

    # Launch world
    gz_start_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory('ros_gz_sim'), '/launch', '/gz_sim.launch.py']),
        launch_arguments={
            'gz_args': '-r ' + 'empty.sdf'
        }.items(),
    )

    # Add features
    gz_spawn_objects = Node(package='ros_gz_sim', executable='create',
                            arguments=['-file', sdf_path,
                                       '-x', '2.0',
                                       '-y', '0.5',
                                       '-z', '0.0'],
                            output='both'
                            )

    # Run the spawner node from the gazebo_ros package.
    node_spawn_entity = Node(package='ros_gz_sim', executable='create',
                             arguments=['-topic', '/robot_description',
                                        '-z', '0.5'],
                             output='screen')

    # robot state publisher node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}]  # add other parameters here if required
    )

    # Bridge
    # https://github.com/gazebosim/ros_gz/tree/humble/ros_gz_bridge
    node_ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock",
            "/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry",
            "/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V",
            "/imu_raw@sensor_msgs/msg/Imu[ignition.msgs.IMU",
            "/camera/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo",
            "/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model",
            '/scan' + '@sensor_msgs/msg/LaserScan' + '[' + 'ignition.msgs.LaserScan',
        ],
        parameters=[{
            "qos_overrides./tf_static.publisher.durability": "transient_local",
        }],

        output='screen'
    )

    # Camera image bridge
    image_bridge = Node(
        package="ros_gz_image",
        executable="image_bridge",
        name="image_bridge",
        arguments=["/camera/image_raw"],
        output="screen",
    )

    # Rviz node
    node_rviz = Node(
        package='rviz2',
        namespace='',
        executable='rviz2',
        name='rviz2',
        arguments=['-d' + os.path.join(get_package_share_directory(pkg_name), 'rviz', 'view_model.rviz')]
    )

    # config_file_path = os.path.join(get_package_share_directory(pkg_name),
    #                                  'config', 'params.yaml')

    # Twist Mux node
    # twist_mux_node = Node(
    #     package='twist_mux',
    #     executable='twist_mux',
    #     name='twist_mux',
    #     output='screen',
    #     remappings={('/cmd_vel_out', '/promethium/cmd_vel')},
    #     parameters=[config_file_path, {'use_sim_time': True}],
    # )

    # Add actions to LaunchDescription
    ld.add_action(SetParameter(name='use_sim_time', value=True))
    ld.add_action(ign_resource_path)
    ld.add_action(ign_resource_path_update)
    ld.add_action(launch_gazebo)
    ld.add_action(gz_spawn_objects)
    ld.add_action(node_spawn_entity)
    ld.add_action(node_robot_state_publisher)
    ld.add_action(node_ros_gz_bridge)
    ld.add_action(image_bridge)
    ld.add_action(node_rviz)
    # ld.add_action(twist_mux_node)

    return ld
























