# OpenClaw-Robotics 2026 Roadmap

## 🎯 Core Goals (Complete in 2026)

### ✅ Completed
- Base architecture
- GO1/GO2/G1 basic control
- WhatsApp integration

### 🚀 Q1-Q2 (H1 2026) - Visual SLAM & Mapping
**Focus: Visual SLAM + Insight9 Deep Integration**

- [ ] **Visual SLAM Core**
  - [ ] ORB-SLAM3 base framework
  - [ ] VINS-Fusion support
  - [ ] Real-time map building
  - [ ] Map save/load

- [ ] **Insight9 Camera Deep Integration**
  - [ ] Insight9-V1/Pro/Max drivers
  - [ ] Depth data stream for SLAM
  - [ ] Multi-camera sync
  - [ ] Edge compute optimization

### 🎯 Q3-Q4 (H2 2026) - TinyNav Navigation
**Focus: Open-source TinyNav Navigation Integration + Autonomous Navigation**

- [ ] **TinyNav Integration**
  - [ ] A* Path planning
  - [ ] RRT real-time planning
  - [ ] DWA/TEB Obstacle avoidance
  - [ ] Semantic navigation

- [ ] **Autonomous Navigation Tasks**
  - [ ] Point-to-point navigation
  - [ ] Area cruise
  - [ ] Multi-target task sequences

---

## 🤖 Supported Device Matrix

### 🐾 Unitree Robots (Plugin-Based)

| Model | Type | Status | Plugin Import |
|-------|------|--------|---------------|
| GO1 | Quadruped | ✅ | `from plugins.robots.go1 import GO1Driver` |
| GO2 | Quadruped | ✅ | `from plugins.robots.go2 import GO2Driver` |
| G1 | Humanoid | ✅ | `from plugins.robots.g1 import G1Driver` |

**Users don't need to modify core code, just import the corresponding plugin**

### 📷 Insight9 Sensors (Plug & Play)

| Model | Type | Status | Usage |
|-------|------|--------|-------|
| Insight9-V1 | RGB-D | ✅ | `from plugins.sensors.insight9 import Insight9V1` |
| Insight9-Pro | RGB-D | ✅ | `from plugins.sensors.insight9 import Insight9Pro` |
| Insight9-Max | RGB-D | ✅ | `from plugins.sensors.insight9 import Insight9Max` |

---

## 🗺️ Architecture Design

### Plugin System
```python
# Users just import, auto-use
from openclaw_robotics import Robot

# Auto-detect and connect - no model specification needed
robot = Robot.auto_connect()

# Or manually specify
robot = Robot.use_plugin("go2")  # Use GO2 plugin
```

### Visual SLAM
```python
from openclaw_robotics.slam import SLAM

# Auto-initialize
slam = SLAM.auto_init(sensor="insight9_pro")

# Get pose
pose = slam.get_pose()
```

### TinyNav Navigation
```python
from openclaw_robotics.navigation import Navigator

nav = Navigator(robot, slam)
nav.navigate(goal=(2.0, 1.5, 0.0))  # x, y, theta
```

---

## 📁 Project Structure

```
OpenClaw-Robotics/
├── src/
│   ├── core/                    # Core framework
│   │   └── plugin_system.py      # Plugin system
│   ├── robots/                   # Robot plugins
│   │   ├── go1/                 # GO1 plugin
│   │   ├── go2/                 # GO2 plugin
│   │   └── g1/                  # G1 plugin
│   ├── sensors/                  # Sensor plugins
│   │   └── insight9/            # Insight9 series
│   ├── slam/                     # SLAM module
│   │   └── visual_slam.py       # Visual SLAM
│   └── navigation/               # Navigation module (Q3)
│       └── tinynav/             # TinyNav integration
├── plugins/                       # Plugin entry
│   ├── __init__.py              # Auto register all plugins
│   └── auto_import.py           # Auto import utility
├── configs/                      # Config templates
├── examples/                      # Usage examples
└── README.md
```

---

## 🚀 Quick Start

### 1. Install
```bash
git clone https://github.com/LooperRobotics/OpenClaw-Robotics.git
cd OpenClaw-Robotics
pip install -r requirements.txt
```

### 2. Use Robot (No Config)
```python
from openclaw_robotics import Robot

# Auto-detect and connect
robot = Robot.auto_connect()

# Control robot
robot.forward(0.5)
robot.rotate(45)
robot.execute("wave")
```

### 3. Use SLAM (Q1-Q2)
```python
from openclaw_robotics.slam import SLAM

# Auto-initialize Insight9 + SLAM
slam = SLAM.auto_init(sensor="insight9_pro")

# Get pose
pose = slam.get_pose()

# Save map
slam.save_map("my_map.bin")
```

### 4. Use Navigation (Q3-Q4)
```python
from openclaw_robotics.navigation import Navigator

nav = Navigator(robot, slam)
nav.navigate(goal=(3.0, 2.0, 0.0))  # Auto path planning & obstacle avoidance
```

---

## 📊 Development Timeline

### Q1 2026 (Jan-Mar)
- [x] Base architecture
- [x] Plugin system design
- [ ] **Jan**: Visual SLAM interface standardization
- [ ] **Feb**: Insight9 Pro driver
- [ ] **Mar**: ORB-SLAM3 base integration

### Q2 2026 (Apr-Jun)
- [ ] **Apr**: VINS-Fusion support
- [ ] **May**: Insight9 full series support
- [ ] **Jun**: SLAM map functionality

### Q3 2026 (Jul-Sep)
- [ ] **Jul**: TinyNav Basic
- [ ] **Aug**: A* + RRT path planning
- [ ] **Sep**: Obstacle avoidance algorithm integration

### Q4 2026 (Oct-Dec)
- [ ] **Oct**: Semantic navigation
- [ ] **Nov**: Performance optimization
- [ ] **Dec**: Complete v2.0 release

---

## 🔌 Plugin Development Guide

### Create New Robot Plugin
```python
# plugins/robots/my_robot.py
from openclaw_robotics.core import RobotPlugin

class MyRobotDriver(RobotPlugin):
    PLUGIN_NAME = "my_robot"
    PLUGIN_VERSION = "1.0.0"
    
    def connect(self) -> bool:
        # Your connection code
        return True
    
    def move(self, cmd) -> bool:
        # Your movement code
        return True

# Auto-register - no extra code needed
```

### Create New Sensor Plugin
```python
# plugins/sensors/my_sensor.py
from openclaw_robotics.core import SensorPlugin

class MySensorDriver(SensorPlugin):
    PLUGIN_NAME = "my_sensor"
    
    def read(self) -> Dict:
        # Read sensor data
        return {"data": 0}
```

---

## 📞 Contact

- **GitHub**: https://github.com/LooperRobotics/OpenClaw-Robotics
- **Issues**: GitHub Issues

---

*Last Updated: February 15, 2026*
*Version: v1.1.0*
