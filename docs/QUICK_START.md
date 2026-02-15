# Quick Start Guide

This guide will help you get up and running with the Unitree Robot WhatsApp Control system in just a few minutes.

## 🚀 5-Minute Setup

### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/yourusername/unitree-whatsapp-control.git
cd unitree-whatsapp-control

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure (Optional - Simulation Mode)

For testing without a real robot, you can skip configuration and run in simulation mode:

```bash
python3 main.py --mode simulation
```

### Step 3: Test Basic Commands

```bash
# Run basic control demo
python3 examples/basic_control.py

# Run predefined actions demo
python3 examples/predefined_actions.py

# Run WhatsApp handler demo
python3 examples/whatsapp_demo.py

# Run OpenClaw integration demo
python3 examples/openclaw_demo.py
```

## 📱 WhatsApp Setup (15 minutes)

### 1. Create WhatsApp Business Account

1. Go to [Facebook for Developers](https://developers.facebook.com/)
2. Create a new app (Business type)
3. Add WhatsApp product to your app
4. Get your credentials:
   - **Access Token**
   - **Phone Number ID**

### 2. Set Up Webhook

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

Fill in these values:
```bash
WHATSAPP_ACCESS_TOKEN=your_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_id_here
WHATSAPP_VERIFY_TOKEN=your_random_token_here
WHATSAPP_APP_SECRET=your_app_secret_here
```

### 3. Configure Webhook URL

1. Use a tool like ngrok for local testing:
   ```bash
   ngrok http 8080
   ```

2. Copy your ngrok URL (e.g., `https://abc123.ngrok.io`)

3. Set up webhook in Facebook Developer Portal:
   ```
   Webhook URL: https://abc123.ngrok.io/webhook
   Verify Token: your_verification_token
   ```

### 4. Start the Server

```bash
python3 main.py --whatsapp --port 8080
```

### 5. Test with WhatsApp

Send a message to your WhatsApp number:
- `forward 0.5` - Move forward
- `rotate left 90` - Rotate left
- `action wave` - Wave gesture
- `status` - Check robot status

## 🤖 Real Robot Setup (30 minutes)

### 1. Install Unitree SDK

```bash
git clone https://github.com/unitreerobotics/unitree_sdk2.git
cd unitree_sdk2
pip install .
```

### 2. Configure Robot Connection

Edit `config/config.json`:
```json
{
  "robot": {
    "type": "go1",
    "default_speed": 0.5
  }
}
```

### 3. Test Connection

```bash
python3 main.py --status
```

Should show:
```
✅ Robot connected successfully!
```

## 🔧 OpenClaw Integration

### 1. Install OpenClaw

Follow the [OpenClaw installation guide](https://docs.openclaw.ai/)

### 2. Register as OpenClaw Skill

```bash
# Copy skill files to OpenClaw skills directory
cp -r src/openclaw_interface.py /path/to/openclaw/skills/
```

### 3. Use in OpenClaw Agent

```python
from src.openclaw_interface import OpenClawRobotInterface

# Create interface
interface = OpenClawRobotInterface(
    controller=robot_controller,
    predefined_actions=actions,
    message_handler=handler
)

# Use in your agent
result = interface.execute_tool("move_forward", speed=0.7)
```

## 📖 Common Commands

### Basic Movement
```bash
forward 0.8        # Move forward at 80% speed
backward 0.5       # Move backward at 50% speed
left 0.6           # Move left at 60% speed
right 0.6         # Move right at 60% speed
rotate left 90     # Rotate left 90 degrees
rotate right 45    # Rotate right 45 degrees
stop               # Stop all movement
```

### Predefined Actions
```bash
action wave        # Wave gesture
action bow         # Bow gesture
action dance       # Dance routine
action walk_around # Walk around
action circle      # Move in circle
action sit         # Sit down
action stand       # Stand up
```

### Settings
```bash
speed = 0.7        # Set default speed to 70%
status             # Check robot status
help               # Show help message
```

## 🐛 Troubleshooting

### Robot Won't Connect

```bash
# Check robot is powered on
# Verify network connection
# Check robot IP address
ping 192.168.1.100

# Test SDK
python3 -c "from unitree_sdk2py import Robot; print('SDK OK')"
```

### WhatsApp Webhook Not Working

```bash
# Check webhook is publicly accessible
curl https://your-domain.com/webhook

# Verify Facebook configuration
# Check webhook logs
tail -f logs/robot_control.log
```

### Permission Errors

```bash
# Linux: Add user to dialout group
sudo usermod -aG dialout $USER

# macOS/Windows: Run as administrator (not recommended)
```

## 📚 Next Steps

1. **Read the full README**: [README.md](README.md)
2. **Explore examples**: Check the `examples/` directory
3. **Customize actions**: Add your own predefined actions
4. **Set up automation**: Use cron or OpenClaw for scheduled tasks
5. **Contribute**: Submit issues and pull requests

## 💡 Tips

- Start with simulation mode to test commands
- Use `help` command to see all available commands
- Set speed limits for safety in `config/config.json`
- Enable logging for debugging: `LOG_LEVEL=DEBUG`
- Backup your configuration regularly

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/unitree-whatsapp-control/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/unitree-whatsapp-control/discussions)

Happy controlling! 🤖🎉
