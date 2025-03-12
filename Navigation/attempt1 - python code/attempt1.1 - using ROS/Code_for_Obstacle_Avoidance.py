import numpy as np
from rplidar import RPLidar

PORT = '/dev/ttyUSB0'
SAFE_DISTANCE = 500  # mm

def detect_obstacles(scan):
    for (_, angle, distance) in scan:
        if distance < SAFE_DISTANCE and distance > 0:
            print(f"Obstacle detected at {angle}° | Distance: {distance} mm")
            return True
    return False

def main():
    lidar = RPLidar(PORT)
    print("Starting Obstacle Detection...")

    try:
        for scan in lidar.iter_scans():
            if detect_obstacles(scan):
                print("STOP! Obstacle detected.")
            else:
                print("Path Clear.")
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        lidar.stop()
        lidar.disconnect()

if __name__ == '__main__':
    main()
