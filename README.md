<!-- PROJECT Badge -->
<div align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Robotics-v2.0-blue?style=for-the-badge&logo=robot" alt="OpenClaw Robotics">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge" alt="Python">
</div>

<br>

<p align="center">
  <strong>Control robots via instant messaging platforms</strong>
  <br>
  Built on OpenClaw framework for embodied AI robotics
</p>

---

## Overview

OpenClaw-Robotics enables natural robot control through IM (Instant Messaging) platforms. Send commands via WeCom, Feishu, DingTalk, or WhatsApp, and the robot executes them in real-time.

```
User (IM App) ──► OpenClaw Gateway ──► Skill ──► Robot ──► Physical Robot
                     │                                        │
                     └────────────────────────────────────────┘
                           (Response/Feedback)
```

### Key Features

- **Multi-IM Support**: WeCom, Feishu, DingTalk, WhatsApp
- **Multi-Robot Support**: Quadrupeds, Humanoids, extensible architecture
- **Deep Insight9 Integration**: Native RGB-D camera support for VSLAM
- **VSLAM & Navigation**: Visual SLAM, path planning, obstacle avoidance
- **Natural Language Control**: Parse commands like "forward 1m then turn left"

---

## Supported Hardware

### Robots

| Brand | Model | Type | Status |
|-------|-------|------|--------|
| Unitree | GO1 | Quadruped | ✅ |
| Unitree | GO2 | Quadruped | ✅ |
| Unitree | Ali | Quadruped | ✅ |
| Unitree | G1 | Humanoid | ✅ |
| Unitree | H1 | Humanoid | ✅ |

### Sensors

| Sensor | Type | Status |
|--------|------|--------|
| **Insight9** | RGB-D Camera | ✅ |
| LiDAR | Distance | ⏳ |
| IMU | Inertial | ⏳ |

### IM Channels

| Channel | Status |
|---------|--------|
| WeCom (企业微信) | ✅ |
| Feishu (飞书) | ✅ |
| DingTalk (钉钉) | ✅ |
| WhatsApp | ✅ |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    IM Adapters (src/im/)                    │
│  ┌────────┐ ┌────────┐ ┌──────────┐ ┌────────────┐        │
│  │ WeCom  │ │Feishu  │ │ DingTalk │ │ WhatsApp   │        │
│  └────────┘ └────────┘ └──────────┘ └────────────┘        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Skill (src/skill.py)                     │
│              Command Parser + Task Executor                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
┌─────────────────┐ ┌───────────────┐ ┌─────────────────┐
│ Robots (src/    │ │ Sensors (src/ │ │ SLAM (src/     │
│   robots/)      │ │   sensors/)   │ │   slam/)       │
│                 │ │               │ │                 │
│ • quadruped     │ │ • Insight9    │ │ • Visual SLAM  │
│ • humanoid      │ │ • LiDAR       │ │ • Navigation   │
│                 │ │ • IMU         │ │ • Mapping      │
└─────────────────┘ └───────────────┘ └─────────────────┘
```

---

## Project Structure

```
OpenClaw-Robotics/
├── README.md                    # This file
├── main.py                      # Main entry point
├── configs/
│   └── config.example.json      # Configuration template
│
├── src/
│   ├── skill.py                 # Main skill entry
│   ├── robot_factory.py         # Robot factory
│   │
│   ├── im/                      # IM adapters
│   │   ├── im_adapter.py        # Base class
│   │   ├── wecom.py             # WeCom
│   │   ├── feishu.py            # Feishu
│   │   ├── dingtalk.py          # DingTalk
│   │   └── whatsapp.py          # WhatsApp
│   │
│   ├── robots/                  # Robot adapters
│   │   ├── robot_adapter.py     # Base class
│   │   ├── quadruped/           # Quadruped robots
│   │   │   └── unitree.py       # GO1, GO2, Ali
│   │   └── humanoid/            # Humanoid robots
│   │       └── unitree.py       # G1, H1
│   │
│   ├── sensors/                 # Sensor adapters
│   │   ├── sensor_adapter.py    # Base class
│   │   └── insight9/            # Insight9 camera
│   │       └── insight9_adapter.py
│   │
│   └── slam/                    # SLAM & Navigation
│       └── visual_slam.py       # VSLAM + Navigator
│
├── examples/                    # Usage examples
│   └── basic_control.py
│
└── tests/                       # Tests
    └── test_robot_control.py
```

---

## Quick Start

### 1. Installation

```bash
git clone https://github.com/LooperRobotics/OpenClaw-Robotics.git
cd OpenClaw-Robotics
pip install -r requirements.txt
```

### 2. Configuration

```bash
cp configs/config.example.json configs/config.json
# Edit config.json with your settings
```

### 3. Initialize Robot + IM

```python
from src.skill import initialize, execute, get_status

# Initialize
result = initialize(
    robot="unitree_go2",
    robot_ip="192.168.12.1", 
    im="wecom",
    config={"corp_id": "your_corp_id", ...}
)
print(result)
```

### 4. Control Robot via IM

Send commands through your IM platform:

| Command | Action |
|---------|--------|
| `往前走1米` / `forward 1m` | Move forward 1m |
| `左转45度` / `turn left 45` | Turn left 45° |
| `站立` / `stand` | Stand up |
| `坐下` / `sit` | Sit down |
| `挥手` / `wave` | Wave hand |
| `往前走然后左转` / `forward then turn left` | Compound command |

---

## Adding New Robots

```python
from src.robot_adapter import RobotAdapter, RobotState, TaskResult, RobotType

class MyRobotAdapter(RobotAdapter):
    ROBOT_CODE = "myrobot_x1"
    ROBOT_NAME = "MyRobot X1"
    BRAND = "MyBrand"
    ROBOT_TYPE = RobotType.QUADRUPED
    
    def connect(self) -> bool:
        # Implement connection
        return True
    
    # ... implement abstract methods
```

Register it:

```python
from src.robot_factory import RobotFactory
RobotFactory.register("myrobot_x1")(MyRobotAdapter)
```

---

## Roadmap

See [ROADMAP.md](docs/ROADMAP.md) for detailed development plan.

### 2026 Q1-Q2
- [ ] Insight9 VSLAM integration
- [ ] Navigation (A* + DWA)
- [ ] Multi-robot coordination

### 2026 Q3-Q4
- [ ] Additional robot support (wheeled, aerial)
- [ ] Advanced SLAM algorithms
- [ ] Fleet management

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT License - See [LICENSE](LICENSE)

---

## Authors

- **LooperRobotics** - [github.com/LooperRobotics](https://github.com/LooperRobotics)

---

<div align="center">
  <sub>Built with ❤️ by LooperRobotics | Powered by OpenClaw</sub>
</div>
