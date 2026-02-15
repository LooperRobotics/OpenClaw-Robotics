# OpenClaw-Robotics

**2026: Visual SLAM + Insight9 Integration + TinyNav Navigation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)

## 🎯 Project Vision

**Robot control as simple as importing a Python library**

- ✅ **Plug & Play**: Different robot models like plugins, free to import
- 🚀 **2026 Goals**: Visual SLAM + Insight9 Deep Integration + TinyNav Navigation
- 🎯 **Zero Config**: Works out of the box, no core code modifications needed

---

## 🐾 Plugin-Based Robot Support

```python
# As simple as importing a Python library!
from openclaw_robotics.robots import GO1, GO2, G1

# Auto-detect and connect - no model specification needed
robot = GO1.auto_connect()

# Or manually select
robot = GO2.connect()
robot = G1.connect()

# Control
robot.forward(0.5)
robot.rotate(45)
robot.execute("wave")
```

### ✅ Supported Models

| Model | Type | Import Statement |
|-------|------|------------------|
| GO1 | Quadruped | `from openclaw_robotics.robots import GO1` |
| GO2 | Quadruped | `from openclaw_robotics.robots import GO2` |
| G1 | Humanoid | `from openclaw_robotics.robots import G1` |

---

## 📷 Insight9 Camera Integration (Q1-Q2)

```python
from openclaw_robotics.sensors import Insight9

# One line to enable SLAM
camera = Insight9.auto_connect()

# Depth data directly for SLAM
slam = camera.enable_slam()  # Built-in VSLAM from Insight 9
```
|

---

## 🗺️ Visual SLAM (Q1-Q2)

```python
from openclaw_robotics.slam import SLAM

# Auto-detect Insight9 and initialize SLAM
slam = SLAM.auto_init(sensor="insight9_pro")

# Get pose
pose = slam.get_pose()

# Save/load map
slam.save_map("office_map.bin")
slam.load_map("office_map.bin")
```


---

## 🧭 TinyNav Navigation (Q3-Q4)

```python
from openclaw_robotics.navigation import Navigator

# Create navigator
nav = Navigator(robot=robot, slam=slam)

# Point-to-point navigation
nav.navigate(goal=(3.0, 2.0, 0.0))  # x, y, theta

# Area cruise
nav.cruise(area="living_room")

# Semantic navigation
nav.semantic_navigate("go to kitchen")
```

### Navigation Features

- A* Global Planning
- DWA Local Obstacle Avoidance
- Semantic Label Navigation
- Task Sequences

---

## 🚀 Quick Start

### 1. Install
```bash
git clone https://github.com/LooperRobotics/OpenClaw-Robotics.git
cd OpenClaw-Robotics
pip install -r requirements.txt
```

### 2. Control Robot (One Line)
```python
from openclaw_robotics.robots import auto_connect

robot = auto_connect()  # Auto-detect model
robot.forward(0.5)
```

### 3. Enable SLAM (Q2)
```python
from openclaw_robotics.slam import auto_init_slam

slam = auto_init_slam()  # Auto-detect Insight9
pose = slam.get_pose()
```

### 4. Start Navigation (Q4)
```python
from openclaw_robotics.navigation import Navigator

nav = Navigator(robot, slam)
nav.navigate(goal=(5.0, 3.0, 0))
```

---

## 📁 Project Structure

```
OpenClaw-Robotics/
├── src/
│   ├── core/                    # Core framework
│   │   └── plugin_system.py     # Plugin system
│   ├── robots/                 # Robot plugins
│   │   ├── __init__.py        # Auto import
│   │   ├── go1/               # GO1 plugin
│   │   ├── go2/               # GO2 plugin
│   │   └── g1/                # G1 plugin
│   ├── sensors/                # Sensor plugins
│   │   └── insight9/          # Insight9 series
│   ├── slam/                   # SLAM module
│   │   └── visual_slam.py     # Visual SLAM
│   └── navigation/              # Navigation module
│       └── tinynav/           # TinyNav
├── plugins/
│   ├── __init__.py           # Auto register
│   └── auto_import.py        # Smart import
├── configs/                    # Config templates
├── examples/                   # Usage examples
└── docs/
    └── ROADMAP.md            # 2026 roadmap
```

---

## 📖 Documentation

- **[ROADMAP.md](docs/ROADMAP.md)** - Detailed 2026 roadmap
- **[examples/](examples/)** - Usage examples
- **API Docs** - Coming soon

---

## 🗓️ 2026 Timeline

### Q1-Q2: Visual SLAM
- [x] Base architecture
- [ ] ORB-SLAM3 integration
- [ ] Insight9 Pro/Max support
- [ ] Real-time map building

### Q3-Q4: TinyNav Navigation
- [ ] A* Path planning
- [ ] Obstacle avoidance
- [ ] Semantic navigation
- [ ] Complete navigation system

---

## 🤝 Contributing Guide

### Add New Robot Plugin
```python
# plugins/robots/my_robot.py
from openclaw_robotics.core import RobotPlugin

class MyRobotDriver(RobotPlugin):
    PLUGIN_NAME = "my_robot"
    # Implement connect(), move() methods
```

### Add New Sensor Plugin
```python
# plugins/sensors/my_sensor.py
from openclaw_robotics.core import SensorPlugin

class MySensorDriver(SensorPlugin):
    PLUGIN_NAME = "my_sensor"
    # Implement read(), calibrate() methods
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

**Making robot control simple** 🤖✨

*2026 Goals: Visual SLAM + Insight9 + TinyNav*
