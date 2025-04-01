import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarSubscriber(Node):
    def __init__(self):
        super().__init__('lidar_subscriber')
        self.subscription = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10)
        self.subscription  # prevent unused variable warning

    def scan_callback(self, msg):
        min_distance = min(msg.ranges)
        self.get_logger().info(f'Minimum distance: {min_distance:.2f} meters')


def main(args=None):
    rclpy.init(args=args)
    node = LidarSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
