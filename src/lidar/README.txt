# RPLIDAR A2M12 Object Detection and Segmentation

This project uses the RPLIDAR A2M12 to scan and visualize objects by segmenting LIDAR scan points and fitting lines to these segments in real-time.

## Requirements

- Python 3.x
- ROS (Robot Operating System)
- Matplotlib
- Numpy
- RPLidar Python package
- ROS `rospy` package

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/judebarakat99/team1repository.git
    cd src/lidar/main
    ```

2. **Install Python Dependencies**

    ```bash
    pip install numpy matplotlib RPLidar
    ```

3. **Install ROS**

    Follow the instructions to install ROS on your system: [ROS Installation Guide](http://wiki.ros.org/ROS/Installation)

4. **Run ROS Core**

    In a new terminal, start ROS core:
    ```bash
    roscore
    ```

## Running the Script

1. **Start the LIDAR Scan**

    Ensure that the RPLIDAR is connected to your computer via USB.

    ```bash
    python lidar_scan.py --s 150
    ```

2. **Script Parameters**

    - `--s`: Segment threshold distance in millimeters (default is 150 mm).

## Code Overview

1. **Initialization**:
    - Imports necessary libraries and initializes parameters like landmark positions, robot position, and segment threshold.

2. **ROS Topic Check**:
    - Checks if the `/scan` ROS topic exists and starts it if necessary.

3. **Main Loop**:
    - **Scans**: Collects scan data from the LIDAR.
    - **Segmentation**: Segments the scan points based on a threshold distance.
    - **Plotting**: Plots each segment in different colors.
    - **Line Fitting**: Fits lines to each segment and averages similar lines.
    - **Visualization**: Visualizes the LIDAR scan and fitted lines, updating in real-time.

4. **Performance Tracking**:
    - Prints the time taken for each loop iteration to the console.

### Key Components

- **RPLFunctions.py**: Contains functions for starting the LIDAR, getting scan data, segmenting data, and fitting lines.

### Example Usage

To run the script with a segment threshold of 150 mm:
```bash
python lidar_scan.py --s 150
```

This script will start the RPLIDAR, collect scan data, segment the points, fit lines to the segments, and visualize the results in real-time.

### Troubleshooting

If you encounter issues, ensure that:
- ROS is properly installed and running.
- The RPLIDAR is connected to the correct USB port.
- All dependencies are correctly installed.

## License

This project is licensed under the MIT License.