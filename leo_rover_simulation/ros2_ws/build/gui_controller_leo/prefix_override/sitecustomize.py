import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mscrobotics2425laptop35/leo_rover_simulation/ros2_ws/install/gui_controller_leo'
