import rclpy
from rclpy.node import Node  # Correct import
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from rplidar import RPLidar
import time

# Set up LiDAR
PORT = "/dev/ttyUSB0"
lidar = RPLidar(PORT, baudrate=256000)  # Set lidar to None initially

DANGER_DISTANCE = 500  # Distance threshold in mm

class LidarObstacleAvoidance(Node):

    def __init__(self):
        super().__init__('lidar_obstacle_avoidance')
        
        # Publisher to send obstacle warnings
        self.obstacle_pub = self.create_publisher(String, '/obstacle_warning', 10)
        
        # Publisher for LaserScan
        self.scan_pub = self.create_publisher(LaserScan, '/scan', 10)
        
        # Create a timer to periodically check for obstacles
        self.timer = self.create_timer(1.0, self.detect_obstacles)
        
        # Initialize LiDAR motor and handle errors
        global lidar
        try:
            lidar = RPLidar(PORT, baudrate=256000)
            lidar.start_motor()
            self.get_logger().info("LiDAR motor started.")
        except Exception as e:
            self.get_logger().error(f"Error initializing LiDAR: {e}")
            lidar = None

    def detect_obstacles(self):
        if lidar is None:
            self.get_logger().error("LiDAR is not initialized. Skipping detection.")
            return
        
        try:
            time.sleep(3)  # Increased sleep time to give the LiDAR some time to initialize
            
            # Create and publish LaserScan message
            scan_msg = LaserScan()
            scan_msg.header.stamp = self.get_clock().now().to_msg()
            scan_msg.header.frame_id = "laser_frame"
            scan_msg.angle_min = -3.14
            scan_msg.angle_max = 3.14
            scan_msg.angle_increment = 0.01
            scan_msg.range_min = 0.02
            scan_msg.range_max = 12.0
            scan_msg.ranges = []  # Fill with data from LiDAR
            
            # Publish LaserScan message
            self.scan_pub.publish(scan_msg)
            print (scan_msg)
            # Try reading LiDAR scans
            # for scan in lidar.iter_scans():
            #     for _, angle, distance in scan:
            #         if 0 < distance < DANGER_DISTANCE:
            #             warning_message = f"⚠️ Obstacle detected at {distance}mm (Angle: {angle:.1f}°)"
            #             self.get_logger().warn(warning_message)
            #             obstacle_msg = String()
            #             obstacle_msg.data = warning_message
            #             self.obstacle_pub.publish(obstacle_msg)
            #             return
        except Exception as e:
            self.get_logger().error(f"Unexpected error occurred: {e}")
        finally:
            # Ensure the lidar is stopped and motor is turned off
            if lidar:
                try:
                    lidar.stop()
                    lidar.stop_motor()
                    lidar.disconnect()
                except Exception as e:
                    self.get_logger().error(f"Failed to stop or disconnect LiDAR: {e}")
                    return

def main(args=None):
    # Initialize ROS 2 Python client library
    rclpy.init(args=args)
    
    # Create and spin the LidarObstacleAvoidance node
    node = LidarObstacleAvoidance()
    rclpy.spin(node)
    
    # Shutdown ROS 2 when done
    rclpy.shutdown()

if __name__ == "__main__":
    main()
