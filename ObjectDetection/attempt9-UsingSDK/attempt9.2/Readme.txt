colcon build
source install/setup.bash
ros2 launch color_detection_pkg color_detection_launch.py


*or* 

in one terminal:
colcon build
source install/setup.bash
ros2 run color_detection_pkg color_detection_publisher

in another terminal:
source install/setup.bash
ros2 run color_detection_pkg color_detection_subscriber
