This code is taken from this github repository: https://github.com/muye1202/who_stole_my_pen

# PincherX-150 Object Gripping

This project demonstrates how to use the PincherX-150 robot arm to detect and grasp a pen using visual information from an Intel RealSense camera and motion planning algorithms. The code can be adapted for the PincherX-150 robot arm with minor adjustments.

## Installation

### Prerequisites

- **ROS (Robot Operating System)**: Follow the [ROS Installation Guide](http://wiki.ros.org/ROS/Installation) to install ROS on your system.
- **Python 3.x**
- **Required Libraries**:
  - `dynamixel_sdk`
  - `numpy`
  - `opencv-python`
  - `modern_robotics`

### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/pincherx-object-gripping.git
    cd pincherx-object-gripping
    ```

2. **Install Python Dependencies**

    ```bash
    pip install dynamixel-sdk numpy opencv-python modern_robotics
    ```

3. **Install ROS Dependencies**

    Ensure that you have installed necessary ROS packages, such as `rospy`.

4. **Connect the Hardware**

    - Connect the PincherX-100 (or PincherX-150) robot arm to your computer via USB.
    - Connect the Intel RealSense camera to your computer.

## Usage

### Running the Script

1. **Start ROS Core**

    Open a new terminal and start ROS core:
    ```bash
    roscore
    ```

2. **Run the Python Script**

    In another terminal, navigate to the project directory and run the script:
    ```bash
    python pen.py
    ```

### How the Code Works

1. **Initialization**:
    - The script imports necessary libraries and initializes the PincherX-150 robot arm.
    - It sets up the ROS node for communication.

2. **Image Processing**:
    - Captures color and depth images using the Intel RealSense camera.
    - Applies color thresholding and contour detection to locate the pen.
    - Calculates the pen's centroid coordinates.

3. **Depth Calculation**:
    - Retrieves the depth at the pen's centroid to get its 3D coordinates.
    - Converts the pen's coordinates to the robot's base frame.

4. **Robot Movement**:
    - Moves the robot's end effector (gripper) to the pen's position in steps.
    - Aligns and adjusts the robot's position to grasp the pen.

5. **Grasping**:
    - Sets the gripper's pressure.
    - Commands the gripper to close and grasp the pen.

6. **Reset**:
    - Moves the robot back to its sleep pose and releases the pen.

### Functions Overview

- **grasp_pen()**: Controls the PincherX-150 arm to detect and grasp the pen.
- **ee_pose()**: Computes the end effector's rotation and translation components using forward kinematics.

### Example Usage

To run the script and make the robot grasp a pen:
```bash
python pen.py
```

### Troubleshooting

- Ensure ROS is properly installed and running.
- Verify that the PincherX-100 (or PincherX-150) and Intel RealSense camera are correctly connected.
- Check that all dependencies are installed.