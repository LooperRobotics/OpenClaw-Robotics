"""
Multi-Brand Robot Controller Skill for OpenClaw

Supports controlling robots from different manufacturers via natural language.
"""

from .robot_factory import RobotFactory
from .command_parser import CommandParser
from .robot_abc import TaskResult

__version__ = "2.0.0"

_parser = None
_current_robot = None


def initialize(robot_code: str, ip: str = "192.168.12.1", **kwargs):
    """
    Initialize robot connection
    
    Args:
        robot_code: Robot code (e.g., "unitree_go2", "unitree_g1")
        ip: Robot IP address
        
    Returns:
        dict: Initialization result
    """
    global _parser, _current_robot
    
    _parser = CommandParser()
    
    try:
        _current_robot = RobotFactory.create(robot_code, ip, **kwargs)
        if _current_robot and _current_robot.connect():
            return {
                "skill": "robot-controller",
                "version": __version__,
                "robot": _current_robot.ROBOT_NAME,
                "code": robot_code,
                "ip": ip,
                "connected": True
            }
        return {"connected": False, "error": "Failed to connect"}
    except Exception as e:
        return {"connected": False, "error": str(e)}


def execute(command: str) -> dict:
    """
    Execute natural language command
    
    Args:
        command: User command in natural language
        
    Returns:
        dict: Execution result
    """
    global _parser, _current_robot
    
    if _parser is None:
        _parser = CommandParser()
    
    if _current_robot is None:
        return {"success": False, "error": "Initialize robot first: initialize('unitree_go2', '192.168.12.1')"}
    
    # Parse command
    parsed = _parser.parse(command, _current_robot.ROBOT_TYPE)
    
    if parsed.action == "unknown":
        return {"success": False, "error": f"Unknown command: {command}"}
    
    # Sequence or single
    if parsed.action == "sequence":
        return _execute_sequence(parsed.params.get("tasks", []))
    
    return _execute_single(parsed.action, parsed.params)


def _execute_single(action: str, params: dict) -> dict:
    """Execute single action"""
    try:
        if action == "forward":
            d = params.get("distance", 1.0)
            s = params.get("speed", 0.5)
            result = _current_robot.move(s, 0, 0)
            
        elif action == "backward":
            d = params.get("distance", 1.0)
            s = params.get("speed", 0.5)
            result = _current_robot.move(-s, 0, 0)
            
        elif action == "turn_left":
            angle = params.get("angle", 45)
            _current_robot.move(0, 0, 0.5)
            import time
            time.sleep(abs(angle) / 45)
            _current_robot.stop()
            result = TaskResult(True, f"Turned left {angle} degrees")
            
        elif action == "turn_right":
            angle = abs(params.get("angle", 45))
            _current_robot.move(0, 0, -0.5)
            import time
            time.sleep(abs(angle) / 45)
            _current_robot.stop()
            result = TaskResult(True, f"Turned right {angle} degrees")
            
        elif action == "stand":
            result = _current_robot.stand()
            
        elif action == "sit":
            result = _current_robot.sit()
            
        elif action == "lie_down":
            result = _current_robot.play_action("lie_down")
            
        elif action == "wave":
            result = _current_robot.play_action("wave")
            
        elif action == "handshake":
            result = _current_robot.play_action("handshake")
            
        elif action == "stop":
            result = _current_robot.stop()
            
        elif action == "go_to":
            pos = params.get("position", [0, 0, 0])
            result = _current_robot.go_to(pos)
            
        elif action == "get_battery":
            state = _current_robot.get_state()
            return {"success": True, "battery": f"{state.battery_level}%"}
            
        elif action == "get_pose":
            state = _current_robot.get_state()
            return {"success": True, "position": state.position.tolist()}
            
        else:
            result = TaskResult(False, f"Unknown action: {action}")
            
        return {"success": result.success, "message": result.message, "action": action}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def _execute_sequence(tasks: list) -> dict:
    """Execute task sequence"""
    results = []
    for task in tasks:
        result = _execute_single(task["action"], task.get("params", {}))
        results.append(result)
    
    return {
        "success": all(r.get("success", False) for r in results),
        "tasks": tasks,
        "results": results
    }


def list_robots() -> list:
    """List all supported robots"""
    return RobotFactory.list_supported()


def get_status() -> dict:
    """Get current robot status"""
    global _current_robot
    
    if _current_robot is None:
        return {"connected": False}
    
    if not _current_robot.connected:
        return {"connected": False}
    
    try:
        state = _current_robot.get_state()
        return {"connected": True, "robot": _current_robot.ROBOT_NAME, **state.to_dict()}
    except Exception as e:
        return {"connected": True, "error": str(e)}
