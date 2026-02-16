<p align="center">
  <a href="https://github.com/LooperRobotics/OpenClaw-Robotics">
    <img src="https://img.shields.io/github/stars/LooperRobotics/OpenClaw-Robotics?style=social" alt="Stars">
  </a>
  <a href="https://github.com/LooperRobotics/OpenClaw-Robotics/fork">
    <img src="https://img.shields.io/github/forks/LooperRobotics/OpenClaw-Robotics?style=social" alt="Forks">
  </a>
  <a href="https://github.com/LooperRobotics/OpenClaw-Robotics/releases">
    <img src="https://img.shields.io/github/v/release/LooperRobotics/OpenClaw-Robotics?include_prereleases&style=social" alt="Version">
  </a>
  <img src="https://img.shields.io/github/license/LooperRobotics/OpenClaw-Robotics?style=social" alt="License">
</p>

<!-- SEO: Description for search engines and social media -->
<meta name="description" content="OpenClaw Robotics Skill - Control robots via instant messaging. Supports WeChat (企业微信), Feishu (飞书), DingTalk (钉钉), WhatsApp. For Unitree GO1/GO2/G1/H1 robots.">
<meta name="keywords" content="robot control, instant messaging, wechat robot, whatsapp robot, unitree robot, quadruped robot, bipedal robot, embodied AI, visual SLAM, python robotics, openclaw">

<!-- Open Graph / Social Media -->
<meta property="og:title" content="OpenClaw Robotics - Control Robots via Instant Messaging">
<meta property="og:description" content="Open source skill for controlling robots through IM platforms. Supports WeChat, Feishu, DingTalk, WhatsApp. For Unitree and other robots.">
<meta property="og:url" content="https://github.com/LooperRobotics/OpenClaw-Robotics">
<meta property="og:type" content="project">

# 🤖 OpenClaw Robotics Skill

[English](#english) | [中文](#中文)

---

## English

<p align="center">
  <strong>Control mobile robots via instant messaging platforms</strong>
</p>

### ⭐ Key Features

- **Multi-IM Support**: WeCom, Feishu, DingTalk, WhatsApp
- **Robot Types**: Quadruped (GO1, GO2), Bipedal/Humanoid (G1, H1)
- **Natural Language**: Control robots with text commands
- **VSLAM Ready**: Support for Insight9 RGB-D camera
- **Navigation**: TinyNav integration (coming soon)

### 📦 Installation

```bash
npx skills add LooperRobotics/OpenClaw-Robotics
```

### 💬 Quick Start

```python
from unitree_robot_skill import initialize, execute

# Connect robot to IM
initialize(robot="unitree_go2", im="wecom")

# Control via messaging
execute("forward 1m")
execute("turn left 45")
```

### 🔗 Links

- **GitHub**: https://github.com/LooperRobotics/OpenClaw-Robotics
- **Documentation**: See README.md for full guide

### 📊 Topics (for discovery)

robotics robot-control instant-messaging wechat whatsapp telegram dingtalk feishu unitree quadruped bipedal humanoid embodied-ai visual-slam python openclaw

---

## 中文

<p align="center">
  <strong>通过即时通讯平台控制移动机器人</strong>
</p>

### ⭐ 核心功能

- **多IM平台**: 企业微信、飞书、钉钉、WhatsApp
- **多机器人类型**: 四足(GO1/GO2)、双足/人形(G1/H1)
- **自然语言控制**: 文本命令控制机器人
- **视觉SLAM**: 支持 Insight9 RGB-D 相机
- **导航**: TinyNav 集成（规划中）

### 📦 安装

```bash
npx skills add LooperRobotics/OpenClaw-Robotics
```

### 💬 快速开始

```python
from unitree_robot_skill import initialize, execute

# 连接机器人和IM
initialize(robot="unitree_go2", im="wecom")

# 通过消息控制
execute("往前走1米")
execute("左转45度")
```

### 📋 相关搜索词

- 微信控制机器人
- 钉钉 机器人控制
- Python 机器人控制
- 四足机器人 开发
- 人形机器人 SDK
- 即时通讯 机器人

---

<p align="center">
  <sub>Built with ❤️ by LooperRobotics | License: MIT</sub>
</p>
