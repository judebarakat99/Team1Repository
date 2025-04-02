from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare the 'three_d' launch argument
    three_d_arg = DeclareLaunchArgument(
        'three_d',
        default_value='false',
        description='Enable 3D mode'
    )

    # Define the 'imu_filter_node' with a condition
    imu_filter_node = Node(
        package='imu_filter_madgwick',
        executable='imu_filter_madgwick_node',
        name='imu_filter_node',
        parameters=[{'config': 'leo_navigation_tutorial_ros2/config/imu_filter_node.yaml'}],
        condition=IfCondition(LaunchConfiguration('three_d'))
    )

    # Define the 'ekf_localization_node' with conditional parameters
    ekf_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_localization_node',
        output='screen',
        parameters=[
            {
                'config': 'leo_navigation_tutorial_ros2/config/ekf_localization_node/ekf_2d.yaml'
            },
            {
                'config': 'leo_navigation_tutorial_ros2/config/ekf_localization_node/ekf_3d.yaml'
            }
        ],
        condition=IfCondition(LaunchConfiguration('three_d'))
    )

    # Combine all components into a LaunchDescription
    return LaunchDescription([
        three_d_arg,
        imu_filter_node,
        ekf_localization_node,
    ])
