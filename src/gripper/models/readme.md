# PX150 Robotic Arm Control Nodes

This project contains two ROS2 nodes: `publisher_control_node.py` and `subscriber_control_node.py`, designed for controlling the Interbotix PincherX-150 (PX150) robotic arm.

## File Overview

### 1. `publisher_control_node.py` - Target Pose Publisher Node

This node publishes target pose messages for the robotic arm. Key functionalities include:
- Publishing `PoseStamped` messages to the `/px150/pose_command` topic, defining the target position and orientation for the robotic arm.
- Defining a sequence of predefined target poses and cyclically publishing them every 5 seconds.
- Target poses are defined as `(x, y, z, ox, oy, oz, ow)`, where:
  - `(x, y, z)` represents position coordinates (in meters).
  - `(ox, oy, oz, ow)` represents orientation in quaternion format.

### 2. `subscriber_control_node.py` - Robotic Arm Control Subscriber Node

This node subscribes to the `/px150/pose_command` topic and controls the PX150 robotic arm to execute the received pose commands. Key functionalities include:
- Parsing the received `PoseStamped` messages and moving the end-effector to the specified target position.
- Performing a sequence of actions: grasping an object, moving to a drop location, and releasing the object.
- The robotic arm control is implemented using the `InterbotixManipulatorXS` class, which supports gripper control.

## Dependencies

This project is based on ROS2 and requires the Interbotix PX150 robotic arm. The following dependencies must be installed:

### 1. Install ROS2 (Foxy/Galactic/Humble)
Refer to the [ROS2 Official Documentation](https://docs.ros.org/en/) for installation instructions.

### 2. Install Interbotix ROS2 Driver

```bash
sudo apt install ros-${ROS_DISTRO}-interbotix-xsarm-control
