import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge
import cv2

class ColorDetectionSubscriber(Node):
    def __init__(self):
        super().__init__('color_detection_subscriber')
        
        self.subscription_image = self.create_subscription(
            Image, '/camera/color/image_raw', self.image_callback, 10
        )
        self.subscription_data = self.create_subscription(
            Float32MultiArray, '/object_center_distance', self.data_callback, 10
        )

        self.bridge = CvBridge()
        self.last_detection = None

    def image_callback(self, msg):
        self.get_logger().info("Receiving image...")
        image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        if self.last_detection:
            x, y, distance = self.last_detection
            cv2.putText(image, f"Dist: {distance:.2f}m", (int(x), int(y) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)

        cv2.imshow("Detected Objects", image)
        cv2.waitKey(10)

    def data_callback(self, msg):
        if len(msg.data) == 3:
            self.last_detection = msg.data  # Store latest detection data

def main(args=None):
    rclpy.init(args=args)
    node = ColorDetectionSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down subscriber...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
