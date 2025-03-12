from rplidar import RPLidar

PORT = "/dev/ttyUSB0"

lidar = RPLidar(PORT, baudrate=256000)  # must be 256000

for i, scan in enumerate(lidar.iter_scans()):
    print(scan)
    if i > 5:  # Stop after 5 scans
        break

lidar.stop()
lidar.disconnect()
