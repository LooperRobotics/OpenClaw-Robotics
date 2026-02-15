# OpenClaw-Robotics

**The Unified Execution Layer for Embodied AI: From Messaging to Motion.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Hardware](https://img.shields.io/badge/Hardware-Unitree-orange.svg)](https://www.unitree.com/)

## 🚀 Overview

**OpenClaw-Robotics** is a high-performance, unified control framework designed for the **Embodied AI** era. It bridges the gap between high-level communication interfaces and physical execution, providing a standardized "Action Layer" for complex robotic platforms.

This release focuses on providing robust, out-of-the-box support for **Unitree robots** (GO1, GO2, G1) via WhatsApp, with a modular architecture ready for expansion to other platforms.

### ✨ Key Features
* **WhatsApp Teleop**: Real-time robot maneuvering via ubiquitous messaging.
* **Multi-Robot Support**: Unified interface for quadruped and humanoid robots.
* **Extensible Architecture**: Designed to support other robot brands and future SLAM capabilities.
* **OpenClaw Integration**: Seamless connection to perception agents and LLM planners.

---

## 🤖 Supported Robots

### ✅ Currently Supported (v1.0.x)

| Robot | Type | Status | Features |
|-------|------|--------|----------|
| **GO1** | Quadruped | ✅ Ready | Basic locomotion, predefined actions |
| **GO2** | Quadruped | ✅ Ready | Enhanced locomotion, running gait |
| **G1** | Humanoid | ✅ Ready | Bipedal walk, humanoid-specific actions |

### 🚧 Coming Soon (v1.1.x)

| Robot | Type | Status | ETA |
|-------|------|--------|-----|
| **B2** | Quadruped | In Progress | Q2 2026 |
| **H1** | Humanoid | Planned | Q3 2026 |

### 🎯 Future Support (v2.0+)

| Brand | Robot | Priority | Status |
|-------|-------|----------|--------|
| Boston Dynamics | Spot | High | Researching |
| Agility Robotics | Cassie | Medium | Researching |
| ANYbotics | ANYmal | Medium | Researching |

---

## 🛠 Project Structure

```bash
OpenClaw-Robotics/
├── src/
│   ├── robot_controller.py      # Core controller (v1.0)
│   │   ├── GO1Driver           # GO1 support
│   │   ├── GO2Driver           # GO2 support  
│   │   └── G1Driver            # G1 support
│   ├── whatsapp_handler.py      # Message parsing
│   ├── whatsapp_integration.py   # WhatsApp API
│   └── openclaw_interface.py    # OpenClaw integration
├── examples/                     # Usage examples
├── tests/                       # Unit tests
├── docs/                        # Documentation
│   ├── ROADMAP.md             # Development roadmap
│   └── QUICK_START.md         # 5-min quick start
└── configs/                    # Configuration files
```

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python 3.8+**
- **Unitree Python SDK** (for real robot control)
- **WhatsApp Business Account** (for messaging)

### 2. Installation
```bash
git clone https://github.com/LooperRobotics/OpenClaw-Robotics.git
cd OpenClaw-Robotics
pip install -r requirements.txt
```

### 3. Connect to Robot
```python
from src.robot_controller import UnitreeRobotController

# For GO1
controller = UnitreeRobotController(robot_type="go1")

# For GO2
controller = UnitreeRobotController(robot_type="go2")

# For G1 (Humanoid)
controller = UnitreeRobotController(robot_type="g1")

# Connect
if controller.connect():
    print("Connected!")
```

### 4. Control via WhatsApp
```
# Basic Movement
forward 0.5     # Move forward at 50% speed
backward 0.3    # Move backward
left 0.6        # Move left
right 0.6       # Move right
rotate left 90   # Rotate left 90°
rotate right 45  # Rotate right 45°
stop            # Stop all movement

# Predefined Actions
action wave        # Wave gesture
action dance       # Dance routine
action walk_around # Walk around area

# G1 Humanoid Specific
action walk        # Bipedal walking
action squat       # Squat movement
action turn_around # Turn around in place
```

---

## 📖 Documentation

- **[README.md](README.md)** - This file
- **[docs/QUICK_START.md](docs/QUICK_START.md)** - 5-minute quick start
- **[docs/ROADMAP.md](docs/ROADMAP.md)** - Detailed development roadmap

---

## 🗺 Roadmap

### Version 1.0.x ✅ Current
Focus: Core functionality and GO1/GO2/G1 support
- [x] Basic movement control
- [x] WhatsApp integration
- [x] Predefined actions
- [x] GO1 support
- [x] GO2 support
- [x] G1 humanoid support

### Version 1.1.x 🚧 Next
Focus: B2/H1 support and architecture improvements
- [ ] Unitree B2 driver
- [ ] Unitree H1 driver
- [ ] Code refactoring
- [ ] Performance optimization
- [ ] Enhanced test coverage

### Version 2.0.x 🎯 Future
Focus: Multi-brand expansion
- [ ] Abstract hardware layer
- [ ] Boston Dynamics Spot driver
- [ ] Agility Robotics driver
- [ ] Generic robot interface

### Version 3.0.x 🚀 Vision
Focus: SLAM and autonomous navigation
- [ ] Lidar SLAM integration
- [ ] Visual SLAM support
- [ ] Map building and storage
- [ ] Autonomous navigation
- [ ] Task scheduling

---

## 📊 Robot Capabilities

### GO1 / GO2 (Quadruped)
```
✅ Forward/Backward/Left/Right
✅ Rotation (Left/Right)
✅ Speed control (0-100%)
✅ Predefined actions (wave, bow, dance, etc.)
✅ GO2 enhanced: running gait, enhanced speed
```

### G1 (Humanoid)
```
✅ All quadruped movements
✅ Bipedal walking
✅ Humanoid actions:
   - Wave, Bow, Stretch
   - Sit, Stand
   - Turn around
   - Squat
```

---

## 🔌 Integration

### OpenClaw Integration
```python
from src.openclaw_interface import OpenClawRobotInterface

interface = OpenClawRobotInterface(
    controller=robot_controller,
    predefined_actions=actions,
    message_handler=handler
)

# Execute via OpenClaw tools
result = interface.execute_tool("move_forward", speed=0.7)
```

### WhatsApp Setup
1. Create WhatsApp Business Account
2. Configure webhooks
3. Set environment variables:
   ```bash
   export WHATSAPP_ACCESS_TOKEN="your_token"
   export WHATSAPP_PHONE_NUMBER_ID="your_phone_id"
   ```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_robot_control.py::TestGO1Driver -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/LooperRobotics/OpenClaw-Robotics/issues)
- **Discussions**: [GitHub Discussions](https://github.com/LooperRobotics/OpenClaw-Robotics/discussions)
- **Docs**: [docs/](docs/)

---

**Built with ❤️ for the Embodied AI community**

*Last updated: 2026-02-15*
