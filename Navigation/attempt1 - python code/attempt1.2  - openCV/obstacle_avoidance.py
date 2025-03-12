import numpy as np
from rplidar import RPLidar

# Set up the Lidar
PORT_NAME = "/dev/ttyUSB0"  # Change accordingly
lidar = RPLidar(PORT_NAME)

DANGER_DISTANCE = 500  # Distance threshold in mm

def detect_obstacles():
    print("Scanning for obstacles...")
    try:
        for scan in lidar.iter_scans():
            for _, angle, distance in scan:
                if distance < DANGER_DISTANCE:
                    print(f"⚠️ Obstacle detected at {distance}mm (Angle: {angle:.1f}°)")
    except KeyboardInterrupt:
        print("Stopping obstacle detection...")
        lidar.stop()
        lidar.disconnect()

detect_obstacles()
