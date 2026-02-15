# OpenClaw-Robotics

**The Unified Execution Layer for Embodied AI: From Messaging to Motion.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Hardware](https://img.shields.io/badge/Hardware-Unitree-orange.svg)](https://www.unitree.com/)

## 🚀 Overview

**OpenClaw-Robotics** is a high-performance, unified control framework designed for the **Embodied AI** era. It bridges the gap between high-level communication interfaces and physical execution, providing a standardized "Action Layer" for complex robotic platforms.

While the current release focuses on providing robust, out-of-the-box support for the **entire Unitree robotics lineup** (Go2, B2, H1, G1, etc.) via WhatsApp, the framework is architected to be hardware-agnostic. Our goal is to expand into a universal control stack supporting diverse configurations and major robotics brands across the industry.

### ✨ Key Features
* **WhatsApp Teleop**: Real-time robot maneuvering (Forward, Rotate, Jump, etc.) via ubiquitous messaging.
* **Unitree Full-Stack Support**: Deeply optimized for Unitree Quadrupeds and Humanoids.
* **Multi-Platform Architecture**: Designed to be extended to other robot brands (e.g., Boston Dynamics, Agility Robotics) and custom configurations.
* **OpenClaw Standard**: A "source of truth" for connecting perception agents to OpenClaw-compatible hardware.
* **Embodied-Ready**: Built-in support for low-latency command parsing, ready for LLM/VLM planning agents.

---

## 🛠 Project Structure

```bash
OpenClaw-Robotics/
├── bridge/                # WhatsApp API integration & Message webhooks
├── core/                  # Intent parser & Hardware Abstraction Layer (HAL)
├── drivers/
│   ├── unitree/           # Optimized wrappers for Unitree SDK (Current Focus)
│   └── generic/           # Interface templates for future brand expansions
├── configs/               # Robot-specific motion parameters & constraints
└── examples/              # Quick start: `python3 run_teleop.py`
```

---

## ⚡ Quick Start

### 1. Prerequisites
* **Unitree Python SDK**: Ensure the SDK is installed and the robot is reachable via network.
* **OpenClaw Bridge**: Setup a Twilio or WhatsApp Business API endpoint to receive webhooks.
* **Environment**: Python 3.8+

### 2. Installation
```bash
git clone [https://github.com/YourUsername/OpenClaw-Robotics.git](https://github.com/YourUsername/OpenClaw-Robotics.git)
cd OpenClaw-Robotics
pip install -r requirements.txt
```

### 3. Basic Command Mapping
The framework maps natural language intents from WhatsApp to robot-specific primitives:

| WhatsApp Message | Robot Action (Unitree Example) | Intent Category |
| :--- | :--- | :--- |
| `"Forward"` | `robot.move(vx=0.5, vy=0)` | Navigation |
| `"Spin"` | `robot.rotate(yaw_speed=1.0)` | Navigation |
| `"Backflip"` | `robot.execute(Special_Action)` | Special Maneuver |
| `"Stop"` | `robot.stop()` | Safety |

---

## 🗺 Roadmap

- [x] **Phase 1**: Full WhatsApp-based control for Unitree Quadruped series (Go2/B2).
- [ ] **Phase 2**: Integration for Unitree Humanoid series (H1/G1) and visual feedback.
- [ ] **Phase 3**: **Hardware Expansion** — Adding drivers for other major robotics brands and custom 6-DOF configurations.
- [ ] **Phase 4**: **Cross-Platform Standardization** — Establishing a universal HAL for multi-brand fleet management via OpenClaw.

---

## 📄 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details. This makes it compatible with the original OpenClaw project and allows for broad community and commercial adoption.

---

**Developed with ❤️ for the Embodied AI community.**
