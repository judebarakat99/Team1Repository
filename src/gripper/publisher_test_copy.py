import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import time

class PublisherControlNode(Node):
    def __init__(self):
        super().__init__('publisher_control_node')

        self.arm = InterbotixManipulatorXS(robot_model='px150', group_name='arm', gripper_name='gripper')
        self.is_busy = False
        self.pending_msg = None

        self.subscription = self.create_subscription(
            String,
            'color_detection',
            self.color_callback,
            10)

        self.state_publisher = self.create_publisher(String, 'arm_ready', 10)

        self.timer = self.create_timer(0.1, self.process_message)
        self.publish_arm_state("ready")

        self.get_logger().info('Subscribed to color_detection topic.')

    def color_callback(self, msg):
        if self.pending_msg is None:
            self.get_logger().info(f'New color detection data received: {msg.data}')
            self.pending_msg = msg
        else:
            self.get_logger().info('Previous data still processing, ignoring new data.')

    def process_message(self):
        if self.is_busy or self.pending_msg is None:
            return

        self.is_busy = True
        msg = self.pending_msg
        self.pending_msg = None
        self.publish_arm_state("pause")

        try:
            parts = msg.data.split(';')
            if len(parts) != 2:
                raise ValueError("Invalid message format")

            color, position_data = parts
            x_3d, y_3d, z_3d = map(float, position_data.split(','))

            x = max(0.05, min(0.4, z_3d))
            y = max(0.05, min(0.4, -y_3d))
            z = max(0.05, min(0.3, abs(x_3d)))

            self.move_arm_to_target(x, y, z)
        except Exception as e:
            self.get_logger().error(f'Error in processing: {e}')
        finally:
            self.is_busy = False
            self.publish_arm_state("ready")

    def move_arm_to_target(self, x, y, z):
        x_d = x + 0.10
        z_a = z - 0.03
        z_d = z_a + 0.05
        y_d = y - 0.0185

        self.get_logger().info(f'Moving to x={x_d}, y={y_d}, z={z_d}')
        self.arm.gripper.release()

        self.arm.arm.set_ee_pose_components(x=x_d, y=y_d, z=z_d, roll=0, pitch=1.47, yaw=0)
        time.sleep(1)

        self.arm.arm.set_ee_pose_components(x=x_d, y=y_d, z=z_a, roll=0, pitch=1.47, yaw=0)
        time.sleep(1)

        self.get_logger().info('Grasping object...')
        self.arm.gripper.grasp()
        time.sleep(2)

        self.get_logger().info('Returning to home...')
        self.arm.arm.go_to_home_pose()
        self.arm.arm.go_to_sleep_pose()

    def publish_arm_state(self, state):
        msg = String()
        msg.data = state
        self.state_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PublisherControlNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
