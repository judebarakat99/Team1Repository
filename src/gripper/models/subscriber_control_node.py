import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS

class SubscriberControlNode(Node):
    def __init__(self):
        super().__init__('subscriber_control_node')


        self.bot = InterbotixManipulatorXS(
            robot_model='px150',
            group_name='arm',
            gripper_name='gripper'
        )

        # 订阅目标位姿
        self.pose_subscription = self.create_subscription(
            PoseStamped,
            '/px150/pose_command',
            self.position_callback,
            10
        )
        self.get_logger().info('Subscribed to /px150/pose_command')

    def position_callback(self, msg: PoseStamped):
        position = msg.pose.position
        x, y, z = position.x, position.y, position.z

        self.get_logger().info(f'Received target position: X={x}, Y={y}, Z={z}')

        # 移动 PX150 机械臂到目标位姿
        try:
            self.bot.arm.set_ee_pose_components(x=x, y=y, z=z)
            self.get_logger().info('PX150 moved to target position.')

            # 执行抓取动作
            self.perform_grasp()

            # 移动到放置位置
            self.move_to_drop_location()

            # 释放物体
            self.release_object()

        except Exception as e:
            self.get_logger().error(f'Failed to move PX150: {e}')

    def perform_grasp(self):
        """ 执行抓取动作 """
        try:
            self.get_logger().info('Closing gripper to grasp object...')
            self.bot.gripper.grasp()
            self.get_logger().info('Grasped the object successfully.')
        except Exception as e:
            self.get_logger().error(f'Failed to grasp object: {e}')

    def move_to_drop_location(self):
        """ 移动到物体放置位置 """
        try:
            drop_x, drop_y, drop_z = 0.3, -0.1, 0.2  # 预设放置点
            self.get_logger().info(f'Moving to drop location: X={drop_x}, Y={drop_y}, Z={drop_z}')
            self.bot.arm.set_ee_pose_components(x=drop_x, y=drop_y, z=drop_z)
            self.get_logger().info('Reached drop location.')
        except Exception as e:
            self.get_logger().error(f'Failed to move to drop location: {e}')

    def release_object(self):
        """ 释放物体 """
        try:
            self.get_logger().info('Opening gripper to release object...')
            self.bot.gripper.release()
            self.get_logger().info('Released the object successfully.')
        except Exception as e:
            self.get_logger().error(f'Failed to release object: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = SubscriberControlNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
