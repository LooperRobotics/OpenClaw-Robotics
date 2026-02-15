<!-- PROJECT Badge -->
<div align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Robotics-v2.0-blue?style=for-the-badge&logo=robot" alt="OpenClaw Robotics">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge" alt="Python">
</div>

<br>

<p align="center">
  <strong>Control robots via instant messaging (WeChat, WhatsApp, Telegram)</strong>
  <br>
  One skill, infinite possibilities for embodied AI robots
</p>

---

## 🚀 Overview

**OpenClaw-Robotics** is a comprehensive framework for controlling robots through instant messaging apps using the OpenClaw ecosystem.

```
User (IM App) ──► OpenClaw Skill ──► Robot Adapter ──► Physical Robot
   ↑                        │
   └────────────────────────┘
        (Response/Feedback)
```

### Core Features

- 🌐 **Multi-IM Support**: WeChat, WeCom, WhatsApp, Telegram
- 🤖 **Multi-Robot Support**: Quadrupeds, Humanoids, Wheeled, Aerial, Surface
- 📷 **Sensor Integration**: RGB-D cameras, LiDAR, IMU (with deep Insight9 support)
- 🗺️ **VSLAM & Navigation**: Real-time mapping, path planning, obstacle avoidance
- 🎯 **Natural Language Control**: Parse commands like "forward 1m then turn left"

---

## 📦 Supported Hardware

### 🤖 Robots

| Brand | Model | Type | Status |
|-------|-------|------|--------|
| Unitree | GO1 | Quadruped | ✅ |
| Unitree | GO2 | Quadruped | ✅ |
| Unitree | Ali | Quadruped | ✅ |
| Unitree | G1 | Humanoid | ✅ |
| Unitree | H1 | Humanoid | ✅ |
| (More) | Coming... | Wheeled/Aerial | ⏳ |

### 📷 Sensors

| Sensor | Type | Status |
|--------|------|--------|
| **Insight9 Pro** | RGB-D Camera | ✅ |
| **Insight9 Max** | RGB-D Camera (4K) | ✅ |
| LiDAR | Distance | ⏳ |
| IMU | Inertial | ⏳ |

### 💬 IM Channels

| Channel | Status |
|---------|--------|
| WeChat (个人微信) | ✅ |
| WeCom (企业微信) | ✅ |
| WhatsApp | ✅ |
| Telegram | ✅ |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    IM Adapters (src/im/)                    │
│  ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐          │
│  │WeChat  │ │ WeCom  │ │ WhatsApp │ │ Telegram │          │
│  └────────┘ └────────┘ └──────────┘ └──────────┘          │
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
│ • wheeled       │ │ • IMU         │ │ • Mapping      │
│ • aerial        │ │               │ │                 │
│ • surface       │ │               │ │                 │
└─────────────────┘ └───────────────┘ └─────────────────┘
```

---

## 📁 Project Structure

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
│   │   ├── wechat.py            # WeChat
│   │   ├── wecom.py             # WeCom
│   │   ├── whatsapp.py          # WhatsApp
│   │   └── telegram.py          # Telegram
│   │
│   ├── robots/                  # Robot adapters
│   │   ├── robot_adapter.py     # Base class
│   │   ├── quadruped/           # Quadruped robots
│   │   │   └── unitree.py       # GO1, GO2, Ali
│   │   ├── humanoid/            # Humanoid robots
│   │   │   └── unitree.py       # G1, H1
│   │   ├── wheeled/             # Wheeled robots (future)
│   │   ├── aerial/              # Aerial robots (future)
│   │   └── surface/             # Surface vehicles (future)
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
│   ├── basic_control.py
│   └── im_integration.py
│
└── tests/                       # Tests
    └── test_robot_control.py
```

---

## 🛠️ Quick Start

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

Once configured, simply send commands through WeChat/WhatsApp:

| Command | Action |
|---------|--------|
| `往前走1米` | Move forward 1m |
| `左转45度` | Turn left 45° |
| `站立` | Stand up |
| `坐下` | Sit down |
| `挥手` | Wave hand |
| `往前走然后左转` | Compound command |

---

## 🔧 Adding New Robots

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

## 🎯 Roadmap

See [ROADMAP.md](docs/ROADMAP.md) for detailed development plan.

### 2026 Q1-Q2
- [ ] Insight9 VSLAM integration
- [ ] Navigation (A* + DWA)
- [ ] Multi-robot coordination

### 2026 Q3-Q4
- [ ] Wheeled robot support
- [ ] Aerial robot support
- [ ] Advanced SLAM algorithms

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 👨‍💻 Authors

- **LooperRobotics** - [github.com/LooperRobotics](https://github.com/LooperRobotics)

---

<div align="center">
  <sub>Built with ❤️ by LooperRobotics | Powered by OpenClaw</sub>
</div>
