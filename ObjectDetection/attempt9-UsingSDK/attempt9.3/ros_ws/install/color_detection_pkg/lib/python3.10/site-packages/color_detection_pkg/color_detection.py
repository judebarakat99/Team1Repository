import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge

class ColorDetectionSubscriber(Node):
    def __init__(self):
        super().__init__('color_detection_subscriber')

        # ROS 2 Subscriptions
        self.sub_color = self.create_subscription(
            Image, '/camera/color/image_raw', self.listener_callback_color, 10
        )
        self.sub_depth = self.create_subscription(
            Image, '/camera/depth/image_rect_raw', self.listener_callback_depth, 10
        )

        # Publisher for processed data
        self.data_pub = self.create_publisher(Float32MultiArray, 'object_center_distance', 10)

        # OpenCV Bridge
        self.bridge = CvBridge()
        self.depth_image = None  # Stores latest depth image

        # Output file for logging detected colors
        self.output_file = "color_detection_output.txt"

    def listener_callback_color(self, data):
        """Callback function to process color image."""
        self.get_logger().info("Receiving color video frame")
        color_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        self.detect_colors(color_image)

    def listener_callback_depth(self, data):
        """Callback function to store latest depth image."""
        self.get_logger().info("Receiving depth video frame")
        self.depth_image = self.bridge.imgmsg_to_cv2(data, '16UC1')

    def detect_colors(self, color_image):
        """Detects colors and shapes in the image and retrieves depth information."""
        if self.depth_image is None:
            return  # Ensure we have depth data

        # Define color ranges (HSV)
        color_ranges = {
            "Red": ([0, 120, 70], [10, 255, 255]),
            "Blue": ([90, 100, 100], [140, 255, 255]),
            "Pink": ([140, 50, 50], [170, 255, 255]),
            "Yellow": ([20, 100, 100], [40, 255, 255]),
        }

        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
        detected_info = []
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

                    # Extract depth value safely
                    depth_value_mm = float(self.depth_image[center_y, center_x])
                    depth_value_m = depth_value_mm / 1000.0  # Convert mm to meters

                    # Aspect ratio range for square detection
                    aspect_ratio = float(w) / h
                    shape = "Square" if 0.8 <= aspect_ratio <= 1.2 else "Rectangle"

                    # Log detected object
                    detected_info.append(f"{color}, {shape}, Distance: {depth_value_m:.3f}m")

                    # Draw detection on image
                    cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(color_image, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.putText(color_image, f"Distance: {depth_value_m:.3f}m", (center_x - 50, center_y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.putText(color_image, shape, (x, y + h + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # Publish structured data (center_x, center_y, depth in meters)
                    msg.data.extend([float(center_x), float(center_y), float(depth_value_m)])

        # Publish detected objects' positions and distances
        if msg.data:
            self.data_pub.publish(msg)

        # Save to log file
        with open(self.output_file, "a") as file:
            for info in detected_info:
                file.write(info + "\n")

        self.get_logger().info(f"Detection results saved to {self.output_file}")

        # Display processed image
        cv2.imshow("Color Detection", color_image)
        cv2.waitKey(10)

def main(args=None):
    rclpy.init(args=args)
    node = ColorDetectionSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
