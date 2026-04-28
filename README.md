# Autonomous Inspection Robot

A differential-drive autonomous robot built for industrial-style inspection using a Raspberry Pi 4B, ROS 2 Humble, computer vision, and a local LLM.

The system navigates autonomously, captures images from its environment, and reports defects such as cracks, leaks, corrosion, and debris in natural language.

## Project Goals
- Run fully locally without cloud dependencies  
- Support voice and natural language commands  
- Detect anomalies in real time using a vision-language model  
- Perform SLAM and waypoint-based navigation  
- Keep the design modular and easy to 3D print  

## Current Status (April 2026)
- [x] Raspberry Pi 4B running Ubuntu 22.04  
- [x] USB webcam with OpenCV pipeline  
- [x] Local vision LLM pipeline (Llava-Phi3 via Ollama)  
- [ ] Motor control and chassis integration  
- [ ] ROS 2 integration and SLAM  
- [ ] Natural language command interface  

## Features
- Real-time defect detection (cracks, leaks, corrosion, debris)  
- Local multimodal LLM-based analysis  
- Modular design for easy iteration and 3D printing  
- ROS 2-based architecture (in progress)  

## Hardware
- Raspberry Pi 4B (8GB)  
- USB webcam  
- TT geared DC motors with hall encoders (12V)  
- RPLIDAR A1 or C1  
- L298N or TB6612 motor driver  
- 12V LiPo battery with buck converter  

See `hardware/bom.md` for the full list.

## Software Stack
- Ubuntu Server 22.04 LTS  
- ROS 2 Humble  
- OpenCV (YOLO integration planned)  
- Ollama with Llava-Phi3  
- ros2_control and Nav2 (planned)  

## Quick Start (Vision Only)

```bash
# Clone the repository
git clone https://github.com/YOURUSERNAME/autonomous-inspection-robot.git
cd autonomous-inspection-robot

# Install dependencies
pip install -r requirements.txt

# Run camera test
python3 src/vision/test_camera.py

# Run inspection pipeline
python3 src/vision/inspect_vision.py