# OpenClaw-Robotics

**The Unified Execution Layer for Embodied AI: From Messaging to Motion.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Hardware](https://img.shields.io/badge/Hardware-Unitree%20Go2%2FB2%2FH1-orange.svg)](https://www.unitree.com/)

## 🚀 Overview

**OpenClaw-Robotics** is a high-performance, unified control framework designed for the **Embodied AI** era. It bridges the gap between high-level communication interfaces and physical execution, providing a standardized "Action Layer" for complex robotic platforms.

Currently, this repository enables seamless teleoperation of **Unitree Quadrupeds (Go2/B2)** and **Humanoids (H1/G1)** via **WhatsApp**. By leveraging the **OpenClaw** ecosystem and **Unitree Python SDK**, it translates simple messaging intents into high-dynamic robotic maneuvers.

### ✨ Key Features
* **WhatsApp Control**: Real-time robot maneuvering (Forward, Rotate, Jump, etc.) via ubiquitous messaging.
* **Unified Kinematics**: Designed to handle various configurations, from 4-legged gaits to humanoid bipedal motion.
* **OpenClaw Standard**: A "source of truth" for connecting perception agents to OpenClaw-compatible hardware.
* **Embodied-Ready**: Built-in support for low-latency command parsing, ready to be integrated with LLM/VLM planning agents.

---

## 🛠 Project Structure

```bash
OpenClaw-Robotics/
├── bridge/                # WhatsApp API integration & Message webhooks
├── core/                  # Intent parser & Task priority scheduler
├── drivers/
│   └── unitree/           # Optimized wrappers for Unitree SDK (Go2, B2, H1)
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
The framework maps natural language intents from WhatsApp to Unitree SDK primitives. For example:

| WhatsApp Message | Robot Action (Unitree SDK) | Description |
| :--- | :--- | :--- |
| `"Forward"` | `robot.move(vx=0.5, vy=0)` | Linear movement |
| `"Left"` | `robot.move(vx=0, vy=0.5)` | Lateral movement |
| `"Spin"` | `robot.rotate(yaw_speed=1.0)` | Yaw rotation |
| `"Backflip"` | `robot.execute(Special_Action_Backflip)` | High-dynamic maneuver |
| `"Stop"` | `robot.stop()` | Immediate damping/emergency stop |

### 4. Running the Teleop Bridge
```python
# Quick example to start the control loop
from bridge.whatsapp import MessageListener
from drivers.unitree import QuadrupedController

robot = QuadrupedController(robot_type="Go2")
listener = MessageListener(api_key="YOUR_WHATSAPP_KEY")

while True:
    cmd = listener.get_latest_command()
    if cmd:
        robot.handle_intent(cmd)
```

---

## 🗺 Roadmap
- [ ] **Phase 1**: Robust WhatsApp-based control for Unitree Go2 (Current).
- [ ] **Phase 2**: Visual Feedback — Robot streams environmental snapshots back to WhatsApp via OpenClaw bridge.
- [ ] **Phase 3**: Full Humanoid support (Unitree H1/G1) with Whole-Body Control (WBC).
- [ ] **Phase 4**: Autonomous task execution via VLM (Vision-Language Models) and multi-modal feedback.

---

## 📄 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details. This makes it compatible with the original OpenClaw project and allows for broad community and commercial adoption.

---

**Developed with ❤️ for the Embodied AI community.**
