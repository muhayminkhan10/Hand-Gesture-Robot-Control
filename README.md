# Hand Gesture Controlled Robot Simulation

A Python-based system that controls a simulated robot in Webots using real-time hand gestures detected via webcam.

## Features
- Real-time hand gesture recognition using OpenCV and MediaPipe
- Socket-based communication between gesture program and Webots simulation
- Gesture commands: 
  - 👋 Open Hand → Move Forward
  - ✊ Fist → Stop
  - 🤏 Pinch → Turn Left
  - Other gestures → Turn Right
  
## Project Structure
RoboticArm_GestureControl/
├── controllers/
│ └── my_controller/
│ └── my_controller.py
├── worlds/
│ └── gesture_robot.wbt
├── gesture_controller.py
├── requirements.txt
├── gesture_demo.mp4 
└── README.md

## Installation
1. Install Python 3.10
2. Install Webots (https://cyberbotics.com/)
3. Clone this repository:
   ```bash
   git clone https://github.com/muhayminkhan10/Robotic-Arm-Gesture-Control.git

Install Python dependencies:
pip install -r requirements.txt

Usage

1.Open worlds/gesture_robot.wbt in Webots
2.Run the simulation (Play button)
3.Run the gesture controller:
  python gesture_controller.py
4.Perform gestures in front of your webcam to control the robot

Technologies Used

Python 3.10
OpenCV
MediaPipe
Webots Robotics Simulator
Socket Programming

Author
Abdul Muhaymin Khan - www.linkedin.com/in/abdul-muhaymin-khan-18103b2a8

License
This project is open source and available under the MIT License.
