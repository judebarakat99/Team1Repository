# RealSense D435 Object Detection with YOLO
This code has been retrieved from this github repository: https://github.com/Mazhichaoruya/Object-Detection-and-location-RealsenseD435/blob/master/Python/main.py 

This project uses the Intel RealSense D435 camera for real-time object detection using the YOLO (You Only Look Once) model.

## Getting Started

### Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- OpenCV
- Intel RealSense SDK 2.0 (`pyrealsense2`)
- NumPy

### Installation

Clone the repository and navigate to the project directory:

```sh
git clone https://github.com/your-username/RealSense-YOLO-Detection.git
cd RealSense-YOLO-Detection
```

Install the required Python packages:

```sh
pip install opencv-python-headless pyrealsense2 numpy
```

### Model Files

Download the YOLO model files and place them in the `Yolo_model` directory:

- `yolov3.weights`
- `yolov3.cfg`
- `object_detection_classes_yolov3.txt`

### Running the Code

Run the main script:

```sh
python main.py
```

### Code Explanation

The script connects to the Intel RealSense D435 camera, captures color and depth frames, processes them for object detection using the YOLO model, and displays the results.

#### Key Components

- **Initialization**: Sets up the camera and loads the YOLO model.
- **RealSense Configuration**: Starts the camera pipeline and opens display windows.
- **Object Detection**: Processes frames from the camera for object detection.
- **Display**: Shows the RGB and depth images with detected objects.

### Example Output

The script will display real-time video streams from the Intel RealSense D435 camera, highlighting detected objects with their positions.