import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import tkinter as tk
import threading
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


class GUIController(Node):
    def __init__(self):
        super().__init__('leo_rover_gui_controller')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.twist = Twist()

        # Start ROS spin in a background thread
        self.ros_thread = threading.Thread(target=rclpy.spin, args=(self,))
        self.ros_thread.start()

        # Start the GUI in the main thread
        self.create_gui()
        self.ld = LaunchDescription()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Leo Rover Controller")
        self.root.geometry("300x200")

        tk.Button(self.root, text="Forward", command=self.move_forward).pack()
        tk.Button(self.root, text="Backward", command=self.move_backward).pack()
        tk.Button(self.root, text="Left", command=self.turn_left).pack()
        tk.Button(self.root, text="Right", command=self.turn_right).pack()
        tk.Button(self.root, text="Stop", command=self.stop).pack()
        #slam
        #tk.Button(self.root, text="Start SLAM", command=self.toggle_slam).pack()
        #tk.Button(self.root, text="Start SLAM", command=self.toggle_slam).pack()

        self.root.mainloop()  # Keep Tkinter running in the main thread

    """def toggle_slam(self):
        # Start SLAM Toolbox with default parameters
        launch_slam_toolbox = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('slam_toolbox'), 'launch'),
                '/online_async_launch.py'])
        )
        # Add the action to the LaunchDescription
        self.ld.add_action(launch_slam_toolbox)

    def get_launch_description(self):
        # Return the LaunchDescription object that has SLAM Toolbox included
        return self.ld"""

    def move_forward(self):
        self.twist.linear.x = 0.5
        self.twist.angular.z = 0.0
        self.publisher_.publish(self.twist)

    def move_backward(self):
        self.twist.linear.x = -0.5
        self.twist.angular.z = 0.0
        self.publisher_.publish(self.twist)

    def turn_left(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 1.0
        self.publisher_.publish(self.twist)

    def turn_right(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = -1.0
        self.publisher_.publish(self.twist)

    def stop(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.publisher_.publish(self.twist)


def main():
    rclpy.init()
    gui_controller = GUIController()

    # Keep the GUI running in the main thread
    gui_controller.root.mainloop()

    # Cleanup when GUI is closed
    gui_controller.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()