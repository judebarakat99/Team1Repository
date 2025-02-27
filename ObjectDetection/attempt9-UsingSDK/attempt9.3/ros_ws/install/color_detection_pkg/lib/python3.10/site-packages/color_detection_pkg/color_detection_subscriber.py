import rclpy
from rclpy.node import Node
import cv2
import numpy as np
import pyrealsense2 as rs
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge

class ColorDetectionSubscriber(Node):
    def __init__(self, name):
        super().__init__(name)
        self.sub_color = self.create_subscription(
            Image, '/camera/color/image_raw', self.listener_callback_color, 10
        )
        self.sub_depth = self.create_subscription(
            Image, '/camera/depth/image_rect_raw', self.listener_callback_depth, 10
        )
        self.cv_bridge = CvBridge()
        self.depth_image = None
        self.pub = self.create_publisher(Float32MultiArray, 'object_center_distance', 10)

        self.latest_color_image = None

    def listener_callback_color(self, msg):
        self.latest_color_image = self.cv_bridge.imgmsg_to_cv2(msg, "bgr8")
        if self.depth_image is not None:
            self.process_frame()

    def listener_callback_depth(self, msg):
        self.depth_image = self.cv_bridge.imgmsg_to_cv2(msg, "16UC1")
        if self.latest_color_image is not None:
            self.process_frame()

    def process_frame(self):
        color_image = self.latest_color_image
        depth_image = self.depth_image

        if color_image is None or depth_image is None:
            return

        self.detect_objects(color_image, depth_image)

    def detect_objects(self, color_image, depth_image):
        # Define color ranges (HSV)
        color_ranges = {
            "Red": ([0, 120, 70], [10, 255, 255]),
            "Blue": ([90, 100, 100], [140, 255, 255]),
            "Pink": ([140, 50, 50], [170, 255, 255]),
            "Yellow": ([20, 100, 100], [40, 255, 255]),
        }

        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
        msg = Float32MultiArray()

        for color, (lower, upper) in color_ranges.items():
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            mask = cv2.inRange(hsv, lower, upper)

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) > 500:
                    x, y, w, h = cv2.boundingRect(contour)
                    center_x = x + w // 2
                    center_y = y + h // 2
                    depth_value = depth_image[center_y, center_x] / 1000.0  # Convert mm to meters

                    # Publish data
                    msg.data = [float(center_x), float(center_y), float(depth_value)]
                    self.pub.publish(msg)

                    # Draw rectangle and text
                    cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(color_image, f"{color} {depth_value:.3f}m", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Display processed image
        cv2.imshow("Detected Objects", color_image)
        cv2.waitKey(1)

    def destroy_node(self):
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ColorDetectionSubscriber("color_detection_subscriber")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down subscriber...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
