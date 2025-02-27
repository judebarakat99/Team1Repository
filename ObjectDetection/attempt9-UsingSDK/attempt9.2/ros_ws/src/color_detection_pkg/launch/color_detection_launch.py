import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='color_detection_pkg',
            executable='color_detection_publisher',
            name='color_detection_publisher',
            output='screen'
        ),
        launch_ros.actions.Node(
            package='color_detection_pkg',
            executable='color_detection_subscriber',
            name='color_detection_subscriber',
            output='screen'
        ),
    ])
