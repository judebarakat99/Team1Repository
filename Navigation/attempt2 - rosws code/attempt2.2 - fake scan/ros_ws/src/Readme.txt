4. Rebuild the Package

Run the following to rebuild:

# Go to workspace root
cd ~/Documents/SystemsDesignProject/Team1Repository/Navigation/attempt2\ -\ rosws\ code/attempt2.2/ros_ws

# Rebuild
colcon build --packages-select lidar_pkg

# Source the setup
source install/setup.bash

5. Run Nodes Individually

Test running the nodes:

# Run publisher
ros2 run lidar_pkg lidar_publisher

# Run subscriber
ros2 run lidar_pkg lidar_subscriber
