import time
import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar

PORT = "/dev/ttyUSB0"
lidar = RPLidar(PORT, baudrate=256000)

# Initialize real-time plot
plt.ion()
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_ylim(0, 6000)

# Start LiDAR motor
lidar.start_motor()

# Allow time for the LiDAR to initialize
time.sleep(1)  # Reduced sleep time to 1 second

try:
    print("Starting LiDAR Mapping...")
    
    for i, scan in enumerate(lidar.iter_scans()):
        print(f"Scan {i}: {scan}")  # Debugging - Print the scans
        if i > 10:  # Limit the number of scans to avoid flooding
            break
        
        angles = []
        distances = []
        
        for _, angle, distance in scan:
            if distance > 0:  # Only process valid data
                angles.append(np.radians(angle))  # Convert to radians
                distances.append(distance)

        # Plot the data
        ax.clear()
        ax.scatter(angles, distances, s=5, color="red")
        ax.set_title("Live LiDAR Mapping")
        ax.set_ylim(0, 6000)
        plt.pause(0.1)  # Give time for the plot to update

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
