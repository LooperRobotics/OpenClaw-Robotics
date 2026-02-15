# OpenClaw Robotics Skill

<p align="center">
  <strong>Control mobile robots via instant messaging</strong>
</p>

---

## Overview

An OpenClaw skill for controlling various mobile robots through IM platforms (WeCom, Feishu, DingTalk, WhatsApp). Send commands via your preferred messaging app, and the robot executes them in real-time.

```
User (IM) → OpenClaw Skill → Robot Control → Physical Robot
```

## Supported Robot Types

| Type | Status | Description |
|------|--------|-------------|
| **Quadruped** | ✅ | Four-legged robots (Unitree GO1, GO2) |
| **Bipedal** | ✅ | Humanoid robots (Unitree G1, H1) |
| **Wheeled** | ⏳ | Wheeled mobile robots (coming soon) |
| **Aerial** | ⏳ | Drones/UAVs (coming soon) |
| **Surface** | ⏳ | Surface vehicles (coming soon) |

## Supported Robots

### Quadruped (四足)
- Unitree GO1
- Unitree GO2

### Bipedal/Humanoid (双足/人形)
- Unitree G1
- Unitree H1

## Future Support

### Sensors
- **Insight9** - Looper Robotics AI Stereo Camera (RGB-D depth sensing)

### Navigation
- **TinyNav** - Open source navigation library for path planning and obstacle avoidance

## IM Channels

| Channel | Code |
|---------|------|
| WeCom (企业微信) | `wecom` |
| Feishu (飞书) | `feishu` |
| DingTalk (钉钉) | `dingtalk` |
| WhatsApp | `whatsapp` |

## Installation

```bash
# Copy to OpenClaw skills directory
cp -r . ~/.openclaw/skills/unitree-robot
```

## Usage

```python
from unitree_robot_skill import initialize, execute

# Initialize
result = initialize(
    robot="unitree_go2",
    robot_ip="192.168.12.1",
    im="wecom"
)

# Execute commands
execute("forward 1m")
execute("turn left 45")
execute("wave")
```

## Command Examples

| Command | Action |
|---------|--------|
| `forward 1m` | Move forward 1 meter |
| `turn left 45` | Turn left 45 degrees |
| `stand` | Stand up |
| `sit` | Sit down |
| `wave` | Wave hand |

## Architecture

```
┌─────────────┐
│   IM Apps   │ (WeCom/Feishu/DingTalk/WhatsApp)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Skill     │ (Command Parser)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Robot    │
│   Adapters  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Robot     │
└─────────────┘
```

## License

MIT
