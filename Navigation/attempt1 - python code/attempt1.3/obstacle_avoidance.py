import time
from rplidar import RPLidar

# Set up LiDAR
PORT = "/dev/ttyUSB0"
lidar = RPLidar(PORT, baudrate=256000)

DANGER_DISTANCE = 500  # Distance threshold in mm

def detect_obstacles():
    print("Scanning for obstacles...")
    try:
        time.sleep(2)  # 🛠️ Let the LiDAR initialize
        lidar.start_motor()

        for scan in lidar.iter_scans():
            for _, angle, distance in scan:
                if 0 < distance < DANGER_DISTANCE:  # Ignore invalid readings
                    print(f"⚠️ Obstacle detected at {distance}mm (Angle: {angle:.1f}°)")
                    return True
        return False
    except KeyboardInterrupt:
        print("Stopping obstacle detection...")
    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == "__main__":
    detect_obstacles()
