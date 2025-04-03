import rclpy
from rclpy.node import Node
import pyrealsense2 as rs
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String

class RealSenseColorDetectionNode(Node):
    def __init__(self):
        super().__init__('realsense_color_detection')
        self.publisher_ = self.create_publisher(String, 'color_detection', 10)
        self.image_publisher_ = self.create_publisher(Image, 'color_image', 10)
        self.bridge = CvBridge()

        self.arm_ready = True
        self.create_subscription(String, 'arm_ready', self.arm_ready_callback, 10)

        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.pipeline.start(config)

        self.align = rs.align(rs.stream.color)
        self.timer = self.create_timer(0.5, self.process_frames)

        profile = self.pipeline.get_active_profile()
        self.depth_intrinsics = profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()

        self.last_detection = None
        self.stable_count = 0

    def arm_ready_callback(self, msg):
        if msg.data == 'ready':
            self.arm_ready = True
            self.get_logger().info("Arm is ready, color detection active.")
        elif msg.data == 'pause':
            self.arm_ready = False
            self.get_logger().info("Arm is busy, color detection paused.")

    def process_frames(self):
        if not self.arm_ready:
            return

        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            return

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.GaussianBlur(color_image, (5, 5), 0)
        hsv_img = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        lower_gray = np.array([0, 0, 50])
        upper_gray = np.array([180, 50, 255])
        gray_mask = cv2.inRange(hsv_img, lower_gray, upper_gray)
        hsv_img = cv2.bitwise_and(hsv_img, hsv_img, mask=cv2.bitwise_not(gray_mask))

        COLOR_RANGES = {
            'red': [(np.array([0, 100, 100]), np.array([10, 255, 255])),
                    (np.array([170, 100, 100]), np.array([180, 255, 255]))],
            'blue': [(np.array([100, 150, 150]), np.array([140, 255, 255]))],
            'green': [(np.array([35, 50, 50]), np.array([85, 255, 255]))],
            'yellow': [(np.array([20, 100, 100]), np.array([35, 255, 255]))]
        }
        COLOR_MAP = {
            'red': (0, 0, 255), 
            'blue': (255, 0, 0), 
            'green': (0, 255, 0),
            'yellow': (0, 255, 255)
        }

        detection_result = []
        for color, ranges in COLOR_RANGES.items():
            mask = np.zeros(hsv_img.shape[:2], dtype=np.uint8)
            for lower, upper in ranges:
                mask |= cv2.inRange(hsv_img, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                if cv2.contourArea(cnt) < 500:
                    continue
                x, y, w, h = cv2.boundingRect(cnt)
                center_x, center_y = int(x + w / 2), int(y + h / 2)
                depth_value = depth_frame.get_distance(center_x, center_y)
                result_point = rs.rs2_deproject_pixel_to_point(self.depth_intrinsics, [center_x, center_y], depth_value)
                x_3d, y_3d, z_3d = result_point  # 单位为米
                
                cv2.rectangle(color_image, (x, y), (x + w, y + h), COLOR_MAP[color], 2)
                cv2.putText(color_image, f"{color}: ({x_3d:.3f}, {y_3d:.3f}, {z_3d:.3f})m", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_MAP[color], 2)
                detection_result.append(f"{color};{x_3d:.3f},{y_3d:.3f},{z_3d:.3f}")

        if self.arm_ready and detection_result:
            current_detection = detection_result[0]
            if self.last_detection is None or current_detection != self.last_detection:
                self.stable_count = 1
                self.last_detection = current_detection
            else:
                self.stable_count += 1

            if self.stable_count >= 3:
                msg = String()
                msg.data = current_detection
                self.publisher_.publish(msg)
                self.get_logger().info(f"\u7a33\u5b9a\u76ee\u6807\u5df2\u53d1\u5e03: {current_detection}")
                self.stable_count = 0
        else:
            self.last_detection = None
            self.stable_count = 0

        img_msg = self.bridge.cv2_to_imgmsg(color_image, encoding="bgr8")
        self.image_publisher_.publish(img_msg)

        cv2.imshow('RealSense Color Detection', color_image)
        cv2.waitKey(1)

    def shutdown(self):
        self.pipeline.stop()
        cv2.destroyAllWindows()
        self.destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = RealSenseColorDetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down node.')
    finally:
        node.shutdown()
        rclpy.shutdown()


if __name__ == '__main__':
    main()