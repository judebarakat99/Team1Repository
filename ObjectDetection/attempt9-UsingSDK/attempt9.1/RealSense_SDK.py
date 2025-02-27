import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# The RealSense SDK is a powerful tool for working with Intel RealSense cameras. 
# It provides access to the camera's color and depth streams, as well as other features like point clouds, depth filters, and more. 
# In this example, we'll use the RealSense SDK to detect colors and shapes in the camera's field of view. 
# We'll process the color image to detect objects of different colors, and then use the depth information to calculate the distance to each object. 
# We'll also perform shape detection based on the aspect ratio of the bounding box of each object. 
# This example demonstrates how to use the RealSense SDK to perform color and depth processing with an Intel RealSense camera.

class ColorDepthSubscriber(Node):
    def __init__(self):
        super().__init__('color_depth_subscriber')

        # Subscribe to color and depth topics
        self.sub_color = self.create_subscription(
            Image, '/camera/color/image_raw', self.color_callback, 10
        )
        self.sub_depth = self.create_subscription(
            Image, '/camera/aligned_depth_to_color/image_raw', self.depth_callback, 10
        )

        self.cv_bridge = CvBridge()
        self.depth_image = None  # Store the latest depth image

        # Define color ranges in HSV (Red, Blue, Pink, Yellow)
        self.color_ranges = {
            "Red": ([0, 120, 70], [10, 255, 255]),
            "Blue": ([90, 100, 100], [140, 255, 255]),
            "Pink": ([140, 50, 50], [170, 255, 255]),
            "Yellow": ([20, 100, 100], [40, 255, 255]),
        }

    def color_callback(self, msg):
        """Processes the color image and detects objects."""
        self.get_logger().info("Receiving color image")

        # Convert ROS image to OpenCV format
        color_image = self.cv_bridge.imgmsg_to_cv2(msg, 'bgr8')

        # Convert image to HSV
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        # Process each color range
        for color, (lower, upper) in self.color_ranges.items():
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)

            # Create mask for the current color
            mask = cv2.inRange(hsv, lower, upper)

            # Find contours of the detected color
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) > 500:  # Filter out small contours
                    x, y, w, h = cv2.boundingRect(contour)
                    center_x, center_y = x + w // 2, y + h // 2

                    # Get depth information if available
                    if self.depth_image is not None:
                        distance_mm = self.depth_image[center_y, center_x]
                        distance_m = distance_mm / 1000.0  # Convert to meters
                    else:
                        distance_m = -1  # No depth data available

                    # Shape detection based on aspect ratio
                    aspect_ratio = float(w) / h
                    shape = "Square" if 0.9 <= aspect_ratio <= 1.1 else "Rectangle"

                    # Draw bounding box and text
                    cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(color_image, f"{color}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.putText(color_image, f"Dist: {distance_m:.2f}m", (x, y + h + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.putText(color_image, f"{shape}", (x, y + h + 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Show the processed image
        cv2.imshow("Color Detection", color_image)
        cv2.waitKey(1)

    def depth_callback(self, msg):
        """Stores the latest depth image."""
        self.get_logger().info("Receiving depth image")
        self.depth_image = self.cv_bridge.imgmsg_to_cv2(msg, '16UC1')  # Convert depth image

def main(args=None):
    rclpy.init(args=args)
    node = ColorDepthSubscriber()
    rclpy.spin(node)

    # Cleanup
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
