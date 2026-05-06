# Autonomous Inspection Robot

An autonomous inspection robot built on a Raspberry Pi 4, with live webcam streaming, obstacle avoidance, and a web-based control dashboard.

## Hardware

| Component | Spec |
|---|---|
| Raspberry Pi 4 Model B | 8GB RAM |
| Webcam | USB |
| TT DC Gearbox Motors (×4) | 3–6V, 200RPM, 1:48 ratio |
| L298N Motor Driver (×2) | Dual H-bridge |
| HC-SR04 Ultrasonic Sensor (×2) | Front + rear |
| Power Bank | USB-C PD, 20000mAh |
| Chassis | 3D printed |

## Wiring

### Motor Driver 1 (left motors)
```
Pi GPIO 17 -> L298N IN1
Pi GPIO 27 -> L298N IN2
Pi GPIO 18 -> L298N ENA (PWM)
```

### Motor Driver 2 (right motors)
```
Pi GPIO 22 -> L298N IN3
Pi GPIO 23 -> L298N IN4
Pi GPIO 24 -> L298N ENB (PWM)
```

### HC-SR04 Ultrasonic Sensor (front)
```
Pi 5V      -> HC-SR04 VCC
Pi GND     -> HC-SR04 GND
Pi GPIO 5  -> HC-SR04 TRIG
HC-SR04 ECHO -> 1kΩ -> Pi GPIO 6
              1kΩ -> GND       <- voltage divider (5V->3.3V)
```

### Power
```
Power bank USB-C -> Raspberry Pi (5V/3A)
Power bank USB-A -> L298N 12V input (motors run at 5V fine)
```

## Installation

```bash
# 1. clone onto Pi
cd ~
mkdir robot && cd robot

# 2. install system dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-opencv -y

# 3. install Python dependencies
pip3 install -r requirements.txt

# 4. enable camera (if using Pi Camera instead of USB webcam)
# sudo raspi-config -> Interface Options -> Camera -> Enable
```

## Usage

### Manual control (web dashboard)
```bash
python3 app.py
```
open `http://<your-pi-ip>:5000` in a browser on any device on the same WiFi network.

**Keyboard controls:** Arrow keys to drive, Space to stop.

### Autonomous mode
```bash
python3 auto_mode.py
```
robot drives forward and steers around obstacles automatically. Press `Ctrl+C` to stop.

### Find your Pi's IP address
```bash
hostname -I
```

## Configuration

edit the pin numbers at the top of `motors.py` and `sensor.py` if your wiring differs:

```python
# motors.py
IN1, IN2, ENA = 17, 27, 18   # left motors
IN3, IN4, ENB = 22, 23, 24   # right motors

# sensor.py
TRIG = 5
ECHO = 6
```

## Tuning

- **Motor speed:** Change the `speed` parameter in `auto_mode.py` (0–100)
- **Obstacle distance:** Change `SAFE_DISTANCE_CM` in `auto_mode.py` (default: 25cm)
- **Camera resolution:** Change `CAP_PROP_FRAME_WIDTH/HEIGHT` in `app.py`
- **Stream quality:** Change JPEG quality value in `app.py` (default: 70, range: 1–100)