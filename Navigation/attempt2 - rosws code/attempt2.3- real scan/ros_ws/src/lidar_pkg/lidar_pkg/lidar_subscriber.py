import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import csv
import os


class LidarSubscriber(Node):
    def __init__(self):
        super().__init__('lidar_subscriber')
        
        # Subscribe to the /scan topic
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10)
        self.subscription  # prevent unused variable warning
        
        # Define CSV file path
        self.csv_file_path = os.path.expanduser('~/Documents/lidar_scan_data.csv')
        
        # Open CSV file for writing (overwrite if exists)
        self.csv_file = open(self.csv_file_path, mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        
        # Write CSV header
        self.csv_writer.writerow(['Angle (Degrees)', 'Distance (Meters)'])
        self.get_logger().info(f'Saving LiDAR scan data to: {self.csv_file_path}')

    def scan_callback(self, msg):
        # Get LiDAR data and write to CSV
        angle_increment_deg = msg.angle_increment * 180.0 / 3.14159  # Convert rad to deg

        self.get_logger().info(f'Received scan with {len(msg.ranges)} data points')

        # Loop through each range and save angle + distance
        for i, distance in enumerate(msg.ranges):
            angle_deg = i * angle_increment_deg
            if msg.range_min <= distance <= msg.range_max:
                self.csv_writer.writerow([round(angle_deg, 2), round(distance, 2)])

        # Flush CSV to ensure data is written immediately
        self.csv_file.flush()
        self.get_logger().info('Scan data written to CSV.')

    def destroy_node(self):
        # Close the CSV file when the node is destroyed
        self.csv_file.close()
        self.get_logger().info('CSV file closed. Shutting down...')

        
def main(args=None):
    rclpy.init(args=args)
    node = LidarSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()
