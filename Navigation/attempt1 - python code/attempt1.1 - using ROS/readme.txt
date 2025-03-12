Prerequisites
- Install required libraries:
    pip install rplidar matplotlib numpy rospy
- Connect your LiDAR via USB.

How It Works
    The first code plots LiDAR data in polar coordinates, which gives a bird's-eye view of the environment.
    The second code continuously scans for nearby obstacles and prints warnings if something is detected within 500 mm.

Next Steps
    Integrate the obstacle detection with motor controllers.
    Use SLAM algorithms with ROS to generate live maps.
    Combine LiDAR with IMU (Inertial Measurement Unit) for better localization.