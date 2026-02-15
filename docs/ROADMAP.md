# OpenClaw-Robotics 发展路线图

## 📋 版本规划

### v1.0.x - 当前版本 ✅
**聚焦：核心功能与G1/GO2支持**
- [x] 基础移动控制（前后左右、旋转）
- [x] 预设动作系统
- [x] WhatsApp消息集成
- [x] OpenClaw接口层
- [x] 支持型号：
  - [x] Unitree GO1
  - [x] Unitree GO2
  - [x] Unitree G1

### v1.1.x - 下一步 🚧
**聚焦：B2/H1支持与架构优化**
- [ ] 优化代码架构
- [ ] 支持型号：
  - [ ] Unitree B2（工业版）
  - [ ] Unitree H1（人形机器人）
- [ ] 统一驱动接口
- [ ] 性能优化

### v2.0.x - 中期目标 🎯
**聚焦：多品牌扩展**
- [ ] 品牌抽象层
- [ ] 支持品牌：
  - [ ] Boston Dynamics (Spot)
  - [ ] Agility Robotics (Cassie)
  - [ ] ANYbotics (ANYmal)
- [ ] 通用HAL（硬件抽象层）
- [ ] 配置化驱动系统

### v3.0.x - 长期愿景 🚀
**聚焦：SLAM与导航**
- [ ] SLAM集成
  - [ ] Lidar SLAM
  - [ ] Visual SLAM
  - [ ] 传感器融合
- [ ] 地图系统
  - [ ] 地图创建与存储
  - [ ] 语义地图
  - [ ] 动态地图更新
- [ ] 导航功能
  - [ ] 路径规划 (A*, RRT)
  - [ ] 自主导航
  - [ ] 目标点导航
  - [ ] 避障系统
- [ ] 任务调度
  - [ ] 自主任务执行
  - [ ] 任务优先级
  - [ ] 任务状态管理

---

## 🤖 机器人支持矩阵

### Unitree 系列 ✅ 当前支持

| 型号 | 类型 | 状态 | 备注 |
|------|------|------|------|
| GO1 | 四足 | ✅ 已支持 | 基础型号 |
| GO2 | 四足 | ✅ 已支持 | 最新四足 |
| G1 | 人形 | ✅ 已支持 | 基础人形 |
| B2 | 四足 | ⏳ 待开发 | 工业级 |
| H1 | 人形 | ⏳ 待开发 | 通用人形 |
| A1 | 四足 | ⏳ 待开发 | 早期型号 |

### 其他品牌 ⏳ 计划中

| 品牌 | 型号 | 优先级 | 状态 |
|------|------|--------|------|
| Boston Dynamics | Spot | 高 | 调研中 |
| Agility Robotics | Cassie | 中 | 调研中 |
| ANYbotics | ANYmal | 中 | 调研中 |
| Xiaomi | CyberDog | 低 | 调研中 |

---

## 🗺️ SLAM与导航功能规划

### v3.0 - SLAM基础

#### 传感器支持
- **Lidar** (激光雷达)
  - RPLIDAR系列
  - Hokuyo系列
  - Velodyne系列
- **Camera** (深度相机)
  - Intel RealSense
  - Azure Kinect
  - Orbbec Astra
- **IMU** (惯性测量单元)
  - MPU6050
  - BMI160
  - VectorNav

#### SLAM算法
- **Laser SLAM**
  - GMapping
  - Cartographer
  - LOAM
- **Visual SLAM**
  - ORB-SLAM3
  - VINS-Fusion
  - RTAB-Map
- **Sensor Fusion**
  - LIO-SAM
  - LVI-SAM

### v3.1 - 地图系统

#### 地图类型
- **2D占用网格地图**
  - 室内导航
  - 障碍物检测
- **3D点云地图**
  - 环境建模
  - 空间感知
- **语义地图**
  - 物体识别
  - 场景理解

### v3.2 - 导航功能

#### 导航能力
- **路径规划**
  - 全局规划 (A*, D*, RRT)
  - 局部规划 (DWA, TEB)
- **自主导航**
  - 目标点导航
  - 巡航模式
  - 区域巡逻
- **任务系统**
  - 任务定义
  - 任务调度
  - 状态监控

---

## 🏗️ 架构演进

### 当前架构 (v1.0)
```
src/
├── robot_controller.py    # 统一控制器
├── whatsapp_handler.py     # 消息处理
├── whatsapp_integration.py # WhatsApp API
└── openclaw_interface.py  # OpenClaw接口
```

### 目标架构 (v2.0+)
```
src/
├── core/                 # 核心接口
│   ├── robot_base.py    # 机器人基类
│   └── navigation.py    # 导航接口
├── drivers/              # 驱动层
│   ├── unitree/         # Unitree驱动
│   │   ├── go1.py
│   │   ├── go2.py
│   │   ├── g1.py
│   │   ├── b2.py       # 待开发
│   │   └── h1.py       # 待开发
│   ├── boston_dynamics/ # 计划中
│   └── ...
├── slam/                # SLAM模块 (v3.0)
│   ├── lidar_slam.py
│   ├── visual_slam.py
│   └── sensor_fusion.py
├── navigation/          # 导航模块 (v3.0)
│   ├── path_planner.py
│   ├── local_planner.py
│   └── task_manager.py
├── whatsapp/            # WhatsApp集成
└── openclaw/           # OpenClaw集成
```

---

## 📈 开发里程碑

### Phase 1: 基础稳定化 (v1.0.x)
- [x] GO1/GO2/G1基础支持
- [x] 核心控制功能
- [x] WhatsApp集成
- [x] 文档完善

**时间**: 2026年2月 ✅ 已完成

### Phase 2: 扩展支持 (v1.1.x)
- [ ] B2/H1驱动开发
- [ ] 代码重构
- [ ] 统一接口
- [ ] 性能优化

**时间**: 2026年Q2 (预计)

### Phase 3: 多品牌扩展 (v2.0.x)
- [ ] 架构抽象化
- [ ] Boston Dynamics支持
- [ ] Agility Robotics支持
- [ ] 通用HAL开发

**时间**: 2026年Q3-Q4 (预计)

### Phase 4: SLAM与导航 (v3.0.x)
- [ ] SLAM集成
- [ ] 地图系统
- [ ] 自主导航
- [ ] 任务系统

**时间**: 2027年 (预计)

---

## 🔧 技术债务

### 当前待解决
- [ ] 单元测试覆盖不足 (当前~60%)
- [ ] 缺少集成测试
- [ ] 文档API部分缺失
- [ ] CI/CD流程待完善

### 计划解决
- [ ] 添加更多测试用例
- [ ] 集成GitHub Actions
- [ ] 自动文档生成
- [ ] 性能基准测试

---

## 📊 贡献者指南

### 如何参与
1. **选择任务**: 从上述清单中选择状态为"⏳"的任务
2. **创建分支**: `git checkout -b feature/xxx`
3. **开发实现**: 遵循项目编码规范
4. **提交PR**: 包含测试和文档
5. **代码审查**: 由维护者审核

### 编码规范
- Python 3.8+
- Type hints必需
- Docstrings必需
- 单元测试必需
- 遵循PEP 8

---

## 📞 联系

- **项目**: https://github.com/LooperRobotics/OpenClaw-Robotics
- **Issues**: GitHub Issues
- **讨论**: GitHub Discussions

---

*最后更新: 2026年2月15日*
*维护者: OpenClaw Contributors*
