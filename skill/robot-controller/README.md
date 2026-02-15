# Robot Controller Skill

Multi-brand robot controller skill for OpenClaw. Control robots from different manufacturers via natural language commands.

## Supported Robots

| Brand | Model | Type | Code |
|-------|-------|------|------|
| Unitree | GO1 | Quadruped | `unitree_go1` |
| Unitree | GO2 | Quadruped | `unitree_go2` |
| Unitree | G1 | Humanoid | `unitree_g1` |
| Unitree | H1 | Humanoid | `unitree_h1` |

## Quick Start

```python
from skill.robot_controller import initialize, execute, list_robots

# List available robots
print(list_robots())

# Initialize connection
result = initialize("unitree_go2", "192.168.12.1")
print(result)

# Execute commands
execute("往前走1米")
execute("左转45度")
execute("挥手")
execute("往前走然后左转90度")
```

## Architecture

```
User Command (Natural Language)
         ↓
Command Parser (brand-agnostic)
         ↓
Task Decomposer
         ↓
Robot Adapter Layer (brand-specific)
         ↓
Robot Hardware
```

## Adding New Robots

```python
from skill.robot_controller import RobotFactory
from skill.robot_abc import RobotBase, TaskResult

class MyRobotAdapter(RobotBase):
    ROBOT_CODE = "myrobot_x1"
    ROBOT_NAME = "MyRobot X1"
    BRAND = "MyRobot"
    ROBOT_TYPE = "quadruped"
    
    def connect(self) -> bool:
        self.connected = True
        return True
    
    # ... implement abstract methods

RobotFactory.register("myrobot_x1")(MyRobotAdapter)
```
