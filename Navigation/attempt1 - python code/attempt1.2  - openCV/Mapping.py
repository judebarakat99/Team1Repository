import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar

# Set up the Lidar (change the port accordingly)
PORT_NAME = "/dev/ttyUSB0"  # Change to your LiDAR's port (Windows: COM3, Linux: /dev/ttyUSBx)
lidar = RPLidar(PORT_NAME)

# Initialize plot
plt.ion()
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_ylim(0, 6000)  # Adjust range based on LiDAR capability

try:
    for scan in lidar.iter_scans():
        angles = []
        distances = []
        
        for _, angle, distance in scan:
            angles.append(np.deg2rad(angle))  # Convert degrees to radians
            distances.append(distance)
        
        ax.clear()
        ax.scatter(angles, distances, s=5, color="red")
        ax.set_title("Live LiDAR Mapping")
        ax.set_ylim(0, 6000)
        plt.pause(0.01)

except KeyboardInterrupt:
    print("Stopping LiDAR mapping...")
    lidar.stop()
    lidar.disconnect()
