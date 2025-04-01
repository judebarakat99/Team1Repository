from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Launch RPLIDAR
        Node(
            package='rplidar_ros',
            executable='rplidar_composition',
            name='rplidar_node',
            output='screen',
            parameters=[
                {'serial_port': '/dev/ttyUSB0'},
                {'serial_baudrate': 256000},     # Set correct baud rate for A2M12
                {'frame_id': 'lidar_frame'},
                {'angle_compensate': True}
            ]
        ),
        # Launch lidar subscriber
        Node(
            package='lidar_pkg',
            executable='lidar_subscriber',
            name='lidar_subscriber',
        ),
    ])
