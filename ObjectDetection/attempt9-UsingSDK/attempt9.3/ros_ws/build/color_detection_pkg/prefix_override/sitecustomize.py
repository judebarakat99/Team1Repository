import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mscrobotics2425laptop37/Documents/SystemsDesignProject/Team1Repository/objectDetection/attempt9-UsingSDK/attempt9.3/ros_ws/install/color_detection_pkg'
