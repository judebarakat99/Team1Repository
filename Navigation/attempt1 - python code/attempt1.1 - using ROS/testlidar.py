# from rplidar import RPLidar

# PORT = "/dev/ttyUSB0"

# lidar = RPLidar(PORT)
# health = lidar.get_health()
# print(f"LiDAR Health: {health}")
# lidar.disconnect()

from rplidar import RPLidar

PORT = "/dev/ttyUSB0"  # Change if needed

try:
    lidar = RPLidar(PORT, baudrate=256000)
    health = lidar.get_health()
    print(f"LiDAR Health: {health}")
    lidar.disconnect()
except Exception as e:
    print(f"Error: {e}")




