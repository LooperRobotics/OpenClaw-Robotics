# OpenClaw-Robotics 2026 路线图

## 🎯 核心目标 (2026年内完成)

### ✅ 当前已完成
- 基础架构
- GO1/GO2/G1 基础控制
- WhatsApp集成

### 🚀 Q1-Q2 (2026上半年) - Visual SLAM与地图
**重点：Visual SLAM + Insight9深度集成**

- [ ] **Visual SLAM核心**
  - [ ] ORB-SLAM3基础框架
  - [ ] VINS-Fusion支持
  - [ ] 实时地图构建
  - [ ] 地图存储/加载

- [ ] **Insight9相机深度集成**
  - [ ] Insight9-V1/Pro/Max驱动
  - [ ] 深度数据流SLAM
  - [ ] 多相机同步
  - [ ] 边缘计算优化

### 🎯 Q3-Q4 (2026下半年) - TinyNav导航
**重点：开源TinyNav导航集成 + 自主导航**

- [ ] **TinyNav导航集成**
  - [ ] A*路径规划
  - [ ] RRT实时规划
  - [ ] DWA/TEB避障
  - [ ] 语义导航

- [ ] **自主导航任务**
  - [ ] 点对点导航
  - [ ] 区域巡航
  - [ ] 多目标任务序列

---

## 🤖 支持设备矩阵

### 🐾 宇树机器人 (插件式)

| 型号 | 类型 | 状态 | 插件导入 |
|------|------|------|----------|
| GO1 | 四足 | ✅ | `from plugins.robots.go1 import GO1Driver` |
| GO2 | 四足 | ✅ | `from plugins.robots.go2 import GO2Driver` |
| G1 | 人形 | ✅ | `from plugins.robots.g1 import G1Driver` |

**用户无需修改核心代码，只需导入对应插件即可**

### 📷 Insight9传感器 (即插即用)

| 型号 | 类型 | 状态 | 使用方式 |
|------|------|------|----------|
| Insight9-V1 | RGB-D | ✅ | `from plugins.sensors.insight9 import Insight9V1` |
| Insight9-Pro | RGB-D | ✅ | `from plugins.sensors.insight9 import Insight9Pro` |
| Insight9-Max | RGB-D | ✅ | `from plugins.sensors.insight9 import Insight9Max` |

---

## 🗺️ 架构设计

### 插件系统
```python
# 用户只需导入即可自动使用
from openclaw_robotics import Robot

# 自动检测并连接
robot = Robot.auto_connect()  # 无需指定型号

# 或手动指定
robot = Robot.use_plugin("go2")  # 使用GO2插件
```

### Visual SLAM
```python
from openclaw_robotics.slam import SLAM

# 自动初始化
slam = SLAM.auto_init(sensor="insight9_pro")

# 获取位姿
pose = slam.get_pose()
```

### TinyNav导航
```python
from openclaw_robotics.navigation import Navigator

nav = Navigator(robot, slam)
nav.navigate(goal=(2.0, 1.5, 0.0))  # x, y, theta
```

---

## 📁 项目结构

```
OpenClaw-Robotics/
├── src/
│   ├── core/                    # 核心框架
│   │   └── plugin_system.py      # 插件系统
│   ├── robots/                   # 机器人插件
│   │   ├── go1/                 # GO1插件
│   │   ├── go2/                 # GO2插件
│   │   └── g1/                  # G1插件
│   ├── sensors/                  # 传感器插件
│   │   └── insight9/            # Insight9系列
│   ├── slam/                     # SLAM模块
│   │   └── visual_slam.py       # Visual SLAM
│   └── navigation/               # 导航模块 (Q3)
│       └── tinynav/              # TinyNav集成
├── plugins/                       # 插件入口
│   ├── __init__.py              # 自动注册所有插件
│   └── auto_import.py           # 自动导入工具
├── configs/                      # 配置模板
├── examples/                      # 使用示例
└── README.md
```

---

## 🚀 快速开始

### 1. 安装
```bash
git clone https://github.com/LooperRobotics/OpenClaw-Robotics.git
cd OpenClaw-Robotics
pip install -r requirements.txt
```

### 2. 使用机器人 (无需配置)
```python
from openclaw_robotics import Robot

# 自动检测并连接
robot = Robot.auto_connect()

# 控制机器人
robot.forward(0.5)
robot.rotate(45)
robot.execute("wave")
```

### 3. 使用SLAM (Q1-Q2)
```python
from openclaw_robotics.slam import SLAM

# 自动初始化Insight9 + SLAM
slam = SLAM.auto_init(sensor="insight9_pro")

# 获取位姿
pose = slam.get_pose()

# 保存地图
slam.save_map("my_map.bin")
```

### 4. 使用导航 (Q3-Q4)
```python
from openclaw_robotics.navigation import Navigator

nav = Navigator(robot, slam)
nav.navigate(goal=(3.0, 2.0, 0.0))  # 自动路径规划和避障
```

---

## 📊 开发时间表

### Q1 2026 (1-3月)
- [x] 基础架构
- [x] 插件系统设计
- [ ] **1月**: Visual SLAM接口标准化
- [ ] **2月**: Insight9 Pro驱动
- [ ] **3月**: ORB-SLAM3基础集成

### Q2 2026 (4-6月)
- [ ] **4月**: VINS-Fusion支持
- [ ] **5月**: Insight9全系列支持
- [ ] **6月**: SLAM地图功能

### Q3 2026 (7-9月)
- [ ] **7月**: TinyNav Basic
- [ ] **8月**: A* + RRT路径规划
- [ ] **9月**: 避障算法集成

### Q4 2026 (10-12月)
- [ ] **10月**: 语义导航
- [ ] **11月**: 性能优化
- [ ] **12月**: 完整版v2.0发布

---

## 🔌 插件开发指南

### 创建新机器人插件
```python
# plugins/robots/my_robot.py
from openclaw_robotics.core import RobotPlugin

class MyRobotDriver(RobotPlugin):
    PLUGIN_NAME = "my_robot"
    PLUGIN_VERSION = "1.0.0"
    
    def connect(self) -> bool:
        # 你的连接代码
        return True
    
    def move(self, cmd) -> bool:
        # 你的移动代码
        return True

# 自动注册 - 无需额外代码
```

### 创建新传感器插件
```python
# plugins/sensors/my_sensor.py
from openclaw_robotics.core import SensorPlugin

class MySensorDriver(SensorPlugin):
    PLUGIN_NAME = "my_sensor"
    
    def read(self) -> Dict:
        # 读取传感器数据
        return {"data": 0}
```

---

## 📞 联系

- **GitHub**: https://github.com/LooperRobotics/OpenClaw-Robotics
- **Issues**: GitHub Issues

---

*最后更新: 2026年2月15日*
*版本: v1.1.0*
