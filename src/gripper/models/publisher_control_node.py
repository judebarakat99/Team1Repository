import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import time

class PublisherControlNode(Node):
    def __init__(self):
        super().__init__('publisher_control_node')

        # 创建话题发布者
        self.arm_control_publisher = self.create_publisher(
            PoseStamped,
            '/px150/pose_command',
            10
        )
        self.get_logger().info('Publishing to /px150/pose_command...')

        # 定义目标位姿列表，让机械臂自动移动到不同的目标点
        self.target_poses = [
            (0.3, 0.0, 0.2, 0.0, 0.0, 0.0, 1.0),  # 目标 1
            (0.2, 0.1, 0.2, 0.0, 0.0, 0.0, 1.0),  # 目标 2
            (0.3, -0.1, 0.25, 0.0, 0.0, 0.0, 1.0) # 目标 3
        ]
        self.pose_index = 0  # 当前目标位姿索引

        # 定时器：每 5 秒发布一次新的目标位姿
        self.timer = self.create_timer(5.0, self.publish_target_pose)

    def publish_target_pose(self):
        # 获取当前目标位姿
        x, y, z, ox, oy, oz, ow = self.target_poses[self.pose_index]

        # 创建 PoseStamped 消息
        pose = PoseStamped()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        pose.pose.orientation.x = ox
        pose.pose.orientation.y = oy
        pose.pose.orientation.z = oz
        pose.pose.orientation.w = ow

        # 发布目标位姿
        self.arm_control_publisher.publish(pose)
        self.get_logger().info(f'Published target pose {self.pose_index + 1}: X={x}, Y={y}, Z={z}')

        # 更新目标索引，循环切换
        self.pose_index = (self.pose_index + 1) % len(self.target_poses)

def main(args=None):
    rclpy.init(args=args)
    node = PublisherControlNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
