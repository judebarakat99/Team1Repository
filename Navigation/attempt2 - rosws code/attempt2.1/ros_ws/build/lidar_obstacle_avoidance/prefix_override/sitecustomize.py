import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mscrobotics2425laptop37/Documents/SystemsDesignProject/Team1Repository/Navigation/attempt2 - rosws code/attempt2.1/ros_ws/install/lidar_obstacle_avoidance'
