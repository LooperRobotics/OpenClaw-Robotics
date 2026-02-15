<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-blue?style=for-the-badge&logo=robot" alt="OpenClaw Skill">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/Version-2.1.0-orange?style=for-the-badge" alt="Version">
</p>

<h1 align="center">🤖 OpenClaw Robotics Skill</h1>

<p align="center">
  <strong>Control mobile robots via instant messaging (IM) platforms</strong>
</p>

---

## 🎯 Project Vision

This project aims to **democratize robot control** by allowing anyone to control mobile robots through familiar messaging apps. 

**Our Goal:** Make robot control as simple as sending a text message.

```
User (IM App) ──► OpenClaw Skill ──► Robot
   ↑                                    │
   └───────── Response/Feedback ────────┘
```

### Target Users

- **Researchers** - Quickly test robot behaviors without coding
- **Educators** - Teach robotics through intuitive IM commands  
- **Hobbyists** - Control personal robots via familiar apps
- **Enterprises** - Deploy customer service robots with IM integration

---

## 🚀 Features

### ✅ Currently Supported

| Feature | Description |
|---------|-------------|
| **Multi-IM Platforms** | WeCom, Feishu, DingTalk, WhatsApp |
| **Quadruped Robots** | Unitree GO1, GO2 |
| **Bipedal Robots** | Unitree G1, H1 |
| **Natural Language** | Parse commands like "forward 1m then turn left" |
| **Visual SLAM** | Basic VSLAM framework with Insight9 support |

### 🔜 Coming Soon

| Feature | Description |
|---------|-------------|
| **Insight9 Camera** | Looper Robotics AI Stereo Camera integration |
| **TinyNav** | Open source navigation library |
| **Wheeled Robots** | Indoor/outdoor wheeled platforms |
| **Aerial Robots** | Drones and UAVs |
| **Multi-robot** | Coordinate multiple robots |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    IM Adapters (src/im/)                    │
│  ┌────────┐ ┌────────┐ ┌──────────┐ ┌────────────┐        │
│  │ WeCom  │ │ Feishu │ │ DingTalk │ │ WhatsApp   │        │
│  └────────┘ └────────┘ └──────────┘ └────────────┘        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Skill Handler                            │
│              (Natural Language Parser)                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
┌─────────────────┐ ┌───────────────┐ ┌─────────────────┐
│ Robot Adapters  │ │SensorAdapter │ │    SLAM/Nav    │
│ • quadruped     │ │  • Insight9  │ │  • Visual SLAM │
│ • humanoid      │ │              │ │  • TinyNav     │
│ • wheeled ⏳    │ │              │ │                 │
└─────────────────┘ └───────────────┘ └─────────────────┘
```

---

## 📦 Supported Hardware

### Robots

| Brand | Model | Type | Status |
|-------|-------|------|--------|
| Unitree | GO1 | Quadruped | ✅ |
| Unitree | GO2 | Quadruped | ✅ |
| Unitree | G1 | Bipedal/Humanoid | ✅ |
| Unitree | H1 | Bipedal/Humanoid | ✅ |
| * | Wheeled robots | Wheeled | ⏳ |
| * | Drones | Aerial | ⏳ |

### Sensors

| Sensor | Type | Status |
|--------|------|--------|
| **Insight9** | RGB-D AI Stereo Camera | ⏳ |
| LiDAR | Distance | ⏳ |
| IMU | Inertial | ⏳ |

---

## 🛠️ Installation

### Method 1: ClawHub (Recommended)

```bash
# Install directly from GitHub
npx skills add LooperRobotics/OpenClaw-Robotics

# Or use specific version
npx skills add LooperRobotics/OpenClaw-Robotics@2.1.0
```

### Method 2: Manual

```bash
# Clone repository
git clone https://github.com/LooperRobotics/OpenClaw-Robotics.git

# Copy to OpenClaw skills directory
cp -r OpenClaw-Robotics ~/.openclaw/skills/unitree-robot

# Restart OpenClaw gateway
openclaw gateway restart
```

---

## 💬 Usage

### Initialize

```python
from unitree_robot_skill import initialize, execute

# Connect to robot and IM
result = initialize(
    robot="unitree_go2",      # robot code
    robot_ip="192.168.12.1",  # robot IP
    im="wecom",               # IM platform
    config={                  # IM-specific config
        "corp_id": "your_corp_id",
        "agent_id": "your_agent_id"
    }
)
print(result)
# {'success': True, 'robot': 'Unitree GO2', 'im': 'wecom', 'connected': True}
```

### Execute Commands

```python
# Basic movement
execute("forward 1m")
execute("backward 0.5m")
execute("turn left 45")
execute("turn right 90")

# Posture control
execute("stand")
execute("sit")

# Actions
execute("wave")
execute("handshake")

# Navigation
execute("go to position 5,3")

# Query status
status = get_status()
print(status)
# {'robot': 'Unitree GO2', 'connected': True, 'battery': '85%', 'temperature': '35°C'}
```

### Command Reference

| Command (EN) | Command (CN) | Action |
|--------------|--------------|--------|
| `forward Xm` | `往前走X米` | Move forward X meters |
| `backward Xm` | `后退X米` | Move backward X meters |
| `turn left X` | `左转X度` | Turn left X degrees |
| `turn right X` | `右转X度` | Turn right X degrees |
| `stand` | `站立` / `起来` | Stand up |
| `sit` | `坐下` | Sit down |
| `stop` | `停止` / `停下` | Emergency stop |
| `wave` | `挥手` | Wave hand |
| `handshake` | `握手` | Handshake |
| `go to X,Y` | `去X,Y` | Navigate to coordinates |

### SLAM & Navigation

```python
from unitree_robot_skill import start_slam, navigate

# Start VSLAM with Insight9
start_slam(sensor="insight9")

# Navigate to position (x, y, yaw)
navigate(goal=(5.0, 3.0, 0))

# Save/load map
save_map("office_map.bin")
load_map("office_map.bin")
```

---

## 🔧 Configuration

### Config File (config.json)

```json
{
  "robot": {
    "code": "unitree_go2",
    "ip": "192.168.12.1"
  },
  "im": {
    "platform": "wecom",
    "corp_id": "your_corp_id",
    "corp_secret": "your_corp_secret",
    "agent_id": "your_agent_id"
  },
  "slam": {
    "enabled": true,
    "sensor": "insight9"
  },
  "navigation": {
    "enabled": true,
    "planner": "tinynav"
  }
}
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting PRs.

### Adding New Robots

```python
from robot_adapters.base import RobotAdapter, RobotState, TaskResult, RobotType

class MyRobotAdapter(RobotAdapter):
    ROBOT_CODE = "myrobot_x1"
    ROBOT_NAME = "My Robot X1"
    BRAND = "MyBrand"
    ROBOT_TYPE = RobotType.WHEELED  # or QUADRUPED, AERIAL, etc.
    
    def connect(self) -> bool:
        # Implement SDK connection
        return True
    
    def move(self, x: float, y: float, yaw: float) -> TaskResult:
        # Implement movement
        return TaskResult(True, "Moved")
    
    # ... implement other abstract methods

# Register
from robot_adapters.factory import RobotFactory
RobotFactory.register("myrobot_x1")(MyRobotAdapter)
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 👨‍💻 Authors

- **LooperRobotics** - [github.com/LooperRobotics](https://github.com/LooperRobotics)

---

<p align="center">
  <sub>Built with ❤️ by LooperRobotics | Powered by OpenClaw</sub>
</p>
