cmake_minimum_required(VERSION 3.8)
project(leo_navigation_tutorial_ros2)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(rclpy REQUIRED)
find_package(robot_localization REQUIRED)
find_package(nav2_costmap_2d REQUIRED)
find_package(imu_filter_madgwick REQUIRED)
find_package(slam_toolbox REQUIRED)
find_package(nav2_map_server REQUIRED)
find_package(nav2_amcl REQUIRED)
find_package(nav2_planner REQUIRED)
find_package(nav2_behavior_tree REQUIRED)
find_package(twist_mux REQUIRED)
#find_package(launch REQUIRED)
#find_package(launch_ros REQUIRED)
#find_package(ament_index_python REQUIRED)
#find_package(Tkinter REQUIRED)  # Tkinter is usually included with Python, but mention it if needed
find_package(ament_lint_auto REQUIRED)
find_package(ament_lint_common REQUIRED)

install(
  DIRECTORY
    config
    launch
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
