# EV3 Robot Control System

Real-time control system for LEGO EV3 robots using MQTT protocol.

## Features

- Bidirectional MQTT communication between PC and EV3
- Motor control (drive and arm)
- Sensor integration (touch, color, infrared, Pixy camera)
- Beacon tracking and autonomous navigation
- Keyboard and GUI control interface

## Requirements

- LEGO EV3 running ev3dev
- Python 3.4+ 
- paho-mqtt 1.5+

## Installation

```
git clone https://github.com/yourusername/ev3-robot.git
cd ev3-robot

pip install paho-mqtt
```

## Usage

### EV3 Robot
python3 ev3_project.py
```

### PC Controller
```bash
python3 pc_project.py
```

## Demo Without Hardware

```
python robot_simulation.py
```

No dependencies required. This runs a complete simulation of all robot functions.

## Demo Screenshot
![Demo Output](/demo_a.png)
![](/demo_b.png)

## Controls

- Arrow Keys: Movement
- Space: Stop
- W/S: Arm up/down
- H: Calibrate arm
- Q: Quit program
- E: Exit and shutdown robot

## Project Structure

```
ev3-robot/
├── ev3_project.py
├── pc_project.py
├── standalone_demo.py
├── libs/
│   ├── mqtt_remote_method_calls.py
│   └── robot_controller.py
└── README.md
```

## Architecture

PC Client sends commands via MQTT to EV3 Robot. The robot executes commands through the robot_controller module and can send sensor data back.

## Configuration

Default MQTT broker: `mosquitto.csse.rose-hulman.edu`
Default robot number: `11`

To use a different broker or robot number, modify the connection parameters in the code.

## License

MIT