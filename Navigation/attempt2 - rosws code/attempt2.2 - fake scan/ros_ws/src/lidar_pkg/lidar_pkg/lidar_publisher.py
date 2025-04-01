import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np


class LidarPublisher(Node):
    def __init__(self):
        super().__init__('lidar_publisher')
        self.publisher_ = self.create_publisher(LaserScan, 'scan', 10)
        self.timer = self.create_timer(1.0, self.publish_fake_scan)

    def publish_fake_scan(self):
        msg = LaserScan()
        msg.header.frame_id = 'lidar_frame'
        msg.angle_min = 0.0
        msg.angle_max = 2 * np.pi
        msg.angle_increment = np.pi / 180.0
        msg.time_increment = 0.0
        msg.scan_time = 0.1
        msg.range_min = 0.1
        msg.range_max = 10.0
        msg.ranges = [np.random.uniform(1.0, 5.0) for _ in range(360)]

        self.publisher_.publish(msg)
        self.get_logger().info('Published fake LiDAR scan')


def main(args=None):
    rclpy.init(args=args)
    node = LidarPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
