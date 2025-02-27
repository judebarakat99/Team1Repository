import rclpy
from rclpy.node import Node
import cv2
import numpy as np
import pyrealsense2 as rs
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge

class ColorDetectionPublisher(Node):
    def __init__(self):
        super().__init__('color_detection_publisher')

        # ROS 2 Publishers
        self.image_pub = self.create_publisher(Image, '/camera/color/image_raw', 10)
        self.data_pub = self.create_publisher(Float32MultiArray, '/object_center_distance', 10)
        self.bridge = CvBridge()

        # RealSense pipeline setup
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.pipeline.start(config)

        # Timer for processing frames
        self.timer = self.create_timer(0.1, self.process_frame)  # 10 Hz

    def process_frame(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            return

        # Convert frame to NumPy array
        color_image = np.asanyarray(color_frame.get_data())

        # Detect colors and objects
        self.detect_objects(color_image, depth_frame)

    def detect_objects(self, color_image, depth_frame):
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
                    depth_value = depth_frame.get_distance(center_x, center_y)

                    # Publish data
                    msg.data = [float(center_x), float(center_y), float(depth_value)]
                    self.data_pub.publish(msg)

                    # Draw rectangle and text
                    cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(color_image, f"{color} {depth_value:.3f}m", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Publish processed image
        ros_image = self.bridge.cv2_to_imgmsg(color_image, "bgr8")
        self.image_pub.publish(ros_image)

    def destroy_node(self):
        self.pipeline.stop()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ColorDetectionPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down publisher...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
