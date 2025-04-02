# Copyright 2023 Fictionlab sp. z o.o.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Setup project paths
    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")
    pkg_project_gazebo = get_package_share_directory("leo_gz_bringup")
    pkg_project_worlds = get_package_share_directory("leo_gz_worlds")

    sim_world = DeclareLaunchArgument(
        "sim_world",
        default_value=os.path.join(pkg_project_worlds, "worlds", "leo_empty.sdf"),
        description="Path to the Gazebo world file",
    )

    robot_ns = DeclareLaunchArgument(
        "robot_ns",
        default_value="",
        description="Robot namespace",
    )

    # Setup to launch the simulator and Gazebo world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": LaunchConfiguration("sim_world")}.items(),
    )

    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_project_gazebo, "launch", "spawn_robot.launch.py")
        ),
        launch_arguments={"robot_ns": LaunchConfiguration("robot_ns")}.items(),
    )


    # Bridge ROS topics and Gazebo messages for establishing communication
    topic_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=  [
                    '/clock'                           + '@rosgraph_msgs/msg/Clock'   + '[' + 'ignition.msgs.Clock',
                    '/model/leo_sim/cmd_vel'  + '@geometry_msgs/msg/Twist'   + '@' + 'ignition.msgs.Twist',
                    '/model/leo_sim/odometry' + '@nav_msgs/msg/Odometry'     + '[' + 'ignition.msgs.Odometry',
                    '/model/leo_sim/scan'     + '@sensor_msgs/msg/LaserScan' + '[' + 'ignition.msgs.LaserScan',
                    '/model/leo_sim/tf'       + '@tf2_msgs/msg/TFMessage'    + '[' + 'ignition.msgs.Pose_V',
                    '/model/leo_sim/imu'      + '@sensor_msgs/msg/Imu'       + '[' + 'ignition.msgs.IMU',
                    '/model/leo_sim/camera/image_raw' + '@sensor_msgs/msg/Image'       + '[' + 'ignition.msgs.Image',
                    '/world/empty/model/leo_sim/joint_state' + '@sensor_msgs/msg/JointState' + '[' + 'ignition.msgs.Model',
                    ],
        parameters= [{'qos_overrides./leo_sim.subscriber.reliability': 'reliable'}],
        remappings= [
                    ('/model/leo_sim/cmd_vel',  '/cmd_vel'),
                    ('/model/leo_sim/odometry', '/odom'   ),
                    ('/model/leo_sim/scan',     '/scan'   ),
                    ('/model/leo_sim/tf',       '/tf'     ),
                    ('/model/leo_sim/imu',      '/imu_raw'),
                    ('/model/leo_sim/camera/image_raw', '/camera'),
                    ('/world/empty/model/leo_sim/joint_state', 'joint_states')
                    ],
        output='screen'
    )
    node_joint_state_publisher = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
    )



    return LaunchDescription(
        [
            sim_world,
            robot_ns,
            gz_sim,
            spawn_robot,
            topic_bridge,
            node_joint_state_publisher,

        ]
    )
