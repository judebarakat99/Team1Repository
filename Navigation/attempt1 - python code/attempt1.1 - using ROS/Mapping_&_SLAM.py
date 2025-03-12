import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar

PORT = '/dev/ttyUSB0'  # Change this to your USB port

def plot_scan(scan):
    angles = []
    distances = []
    
    for (_, angle, distance) in scan:
        angles.append(np.radians(angle))
        distances.append(distance)
    
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, distances, 'g.')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rmax(4000)  # Max range in mm
    plt.title("RPLIDAR Scan")
    plt.show()

def main():
    lidar = RPLidar(PORT)
    print("Starting Scan...")

    try:
        for i, scan in enumerate(lidar.iter_scans()):
            print(f'Scan {i}')
            plot_scan(scan)
            if i > 3:  # Stop after 3 scans
                break

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        lidar.stop()
        lidar.disconnect()

if __name__ == '__main__':
    main()
