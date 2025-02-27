import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='your_package_name',  # Replace with your actual package name
            executable='color_detection_subscriber',  # Match this with the name in setup.py
            name='color_detection_subscriber',
            output='screen'
        )
    ])
