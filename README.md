# OpenClaw-Robotics

**2026年实现Visual SLAM + Insight9深度集成 + TinyNav导航**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)

## 🎯 项目愿景

**让机器人控制像导入Python库一样简单**

- ✅ **即插即用**：不同型号机器人像插件一样自由导入
- 🚀 **2026目标**：Visual SLAM + Insight9深度集成 + TinyNav导航
- 🎯 **零配置**：无需修改核心代码，开箱即用

---

## 🐾 插件式机器人支持

```python
# 就像导入Python库一样简单！
from openclaw_robotics.robots import GO1, GO2, G1

# 自动检测连接 - 无需指定型号
robot = GO1.auto_connect()

# 或手动选择
robot = GO2.connect()
robot = G1.connect()

# 控制
robot.forward(0.5)
robot.rotate(45)
robot.execute("wave")
```

### ✅ 已支持型号

| 型号 | 类型 | 导入语句 |
|------|------|----------|
| GO1 | 四足 | `from openclaw_robotics.robots import GO1` |
| GO2 | 四足 | `from openclaw_robotics.robots import GO2` |
| G1 | 人形 | `from openclaw_robotics.robots import G1` |

---

## 📷 Insight9相机集成 (Q1-Q2)

```python
from openclaw_robotics.sensors import Insight9Pro

# 一行代码启用SLAM
camera = Insight9Pro.auto_connect()

# 深度数据直接给SLAM使用
slam = camera.enable_slam()  # 自动对接ORB-SLAM3
```

### Insight9系列

| 型号 | 分辨率 | 深度范围 | SLAM支持 |
|------|--------|----------|----------|
| V1 | 720P | 0.2-3m | ✅ |
| Pro | 1080P | 0.1-10m | ✅ |
| Max | 1440P | 0.05-15m | ✅ |

---

## 🗺️ Visual SLAM (Q1-Q2)

```python
from openclaw_robotics.slam import SLAM

# 自动检测Insight9并初始化SLAM
slam = SLAM.auto_init(sensor="insight9_pro")

# 获取位姿
pose = slam.get_pose()

# 保存/加载地图
slam.save_map("office_map.bin")
slam.load_map("office_map.bin")
```

### 支持的SLAM算法

- **ORB-SLAM3** - 特征点法，功能完整
- **VINS-Fusion** - 视觉惯性，紧凑高效

---

## 🧭 TinyNav导航 (Q3-Q4)

```python
from openclaw_robotics.navigation import Navigator

# 创建导航器
nav = Navigator(robot=robot, slam=slam)

# 点对点导航
nav.navigate(goal=(3.0, 2.0, 0.0))  # x, y, theta

# 区域巡航
nav.cruise(area="living_room")

# 语义导航
nav.semantic_navigate("go to kitchen")
```

### 导航特性

- A*全局规划
- DWA局部避障
- 语义标签导航
- 任务序列

---

## 🚀 快速开始

### 1. 安装
```bash
git clone https://github.com/LooperRobotics/OpenClaw-Robotics.git
cd OpenClaw-Robotics
pip install -r requirements.txt
```

### 2. 一行代码控制机器人
```python
from openclaw_robotics.robots import auto_connect

robot = auto_connect()  # 自动检测型号
robot.forward(0.5)
```

### 3. 启用SLAM (Q2)
```python
from openclaw_robotics.slam import auto_init_slam

slam = auto_init_slam()  # 自动检测Insight9
pose = slam.get_pose()
```

### 4. 开始导航 (Q4)
```python
from openclaw_robotics.navigation import Navigator

nav = Navigator(robot, slam)
nav.navigate(goal=(5.0, 3.0, 0))
```

---

## 📁 项目结构

```
OpenClaw-Robotics/
├── src/
│   ├── core/                    # 核心框架
│   │   └── plugin_system.py     # 插件系统
│   ├── robots/                 # 机器人插件
│   │   ├── __init__.py        # 自动导入
│   │   ├── go1/               # GO1插件
│   │   ├── go2/               # GO2插件
│   │   └── g1/                # G1插件
│   ├── sensors/                # 传感器插件
│   │   └── insight9/          # Insight9系列
│   ├── slam/                   # SLAM模块
│   │   └── visual_slam.py     # Visual SLAM
│   └── navigation/              # 导航模块
│       └── tinynav/            # TinyNav
├── plugins/
│   ├── __init__.py           # 自动注册
│   └── auto_import.py         # 智能导入
├── configs/                    # 配置模板
├── examples/                   # 使用示例
└── docs/
    └── ROADMAP.md            # 2026路线图
```

---

## 📖 文档

- **[ROADMAP.md](docs/ROADMAP.md)** - 2026年详细路线图
- **[examples/](examples/)** - 使用示例
- **API Docs** - 待发布

---

## 🗓️ 2026年时间表

### Q1-Q2: Visual SLAM
- [x] 基础架构
- [ ] ORB-SLAM3集成
- [ ] Insight9 Pro/Max支持
- [ ] 实时地图构建

### Q3-Q4: TinyNav导航
- [ ] A*路径规划
- [ ] 避障算法
- [ ] 语义导航
- [ ] 完整导航系统

---

## 🤝 贡献指南

### 添加新机器人插件
```python
# plugins/robots/my_robot.py
from openclaw_robotics.core import RobotPlugin

class MyRobotDriver(RobotPlugin):
    PLUGIN_NAME = "my_robot"
    # 实现 connect(), move() 等方法
```

### 添加新传感器插件
```python
# plugins/sensors/my_sensor.py
from openclaw_robotics.core import SensorPlugin

class MySensorDriver(SensorPlugin):
    PLUGIN_NAME = "my_sensor"
    # 实现 read(), calibrate() 等方法
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

**让机器人控制变得简单** 🤖✨

*2026年目标：Visual SLAM + Insight9 + TinyNav*
