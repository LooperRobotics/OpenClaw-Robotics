"""
OpenClaw Robotics Skill - Main Entry Point

Control robots via IM (WeChat, WeCom, WhatsApp, Telegram)
"""

from typing import Optional, Callable
from .robot_factory import RobotFactory
from .robots.robot_adapter import RobotState, TaskResult
from .slam.visual_slam import VisualSLAM, Navigator


class RoboticsSkill:
    """
    Main skill for robot control via IM messages
    
    Usage:
        skill = RoboticsSkill()
        skill.initialize(robot="unitree_go2", im="wecom")
        skill.execute("往前走1米")
    """
    
    def __init__(self):
        self.robot = None
        self.im_adapter = None
        self.slam: Optional[VisualSLAM] = None
        self.navigator: Optional[Navigator] = None
        
    def initialize(self, robot: str = "unitree_go2", im: str = "wecom", 
                   robot_ip: str = "192.168.12.1", config: dict = None):
        """
        Initialize robot and IM connection
        
        Args:
            robot: Robot code (unitree_go2, etc.)
            im: IM channel (wechat, wecom, whatsapp, telegram)
            robot_ip: Robot IP
            config: Additional config
        """
        # Create robot
        self.robot = RobotFactory.create(robot, robot_ip)
        if not self.robot or not self.robot.connect():
            return {"success": False, "error": "Failed to connect robot"}
        
        # Create IM adapter
        if im == "wecom":
            from .im.wecom import WeComAdapter
            self.im_adapter = WeComAdapter(config)
        elif im == "whatsapp":
            from .im.whatsapp import WhatsAppAdapter
            self.im_adapter = WhatsAppAdapter(config)
        # ... other IM
        
        if self.im_adapter:
            self.im_adapter.connect()
        
        return {
            "success": True,
            "robot": self.robot.ROBOT_NAME,
            "im": im,
            "connected": True
        }
    
    def execute(self, command: str) -> dict:
        """
        Execute natural language command
        
        Args:
            command: Natural language command
            
        Returns:
            dict: Execution result
        """
        if not self.robot:
            return {"success": False, "error": "Not initialized"}
        
        # Parse command
        parsed = self._parse_command(command)
        
        # Execute
        return self._execute_action(parsed["action"], parsed["params"])
    
    def _parse_command(self, command: str) -> dict:
        """Parse natural language to action"""
        import re
        
        # Simple parser (can be enhanced with LLM)
        patterns = [
            (r"(向前|前进|往前走)(\d+(?:\.\d+)?)米?", "forward", "distance"),
            (r"(向后|后退)(\d+(?:\.\d+)?)米?", "backward", "distance"),
            (r"左转(\d+(?:\.\d+)?)度?", "turn_left", "angle"),
            (r"右转(\d+(?:\.\d+)?)度?", "turn_right", "angle"),
            (r"(站起?|起来|站立)", "stand", None),
            (r"坐下", "sit", None),
            (r"停止", "stop", None),
            (r"挥手", "wave", None),
            (r"握手", "handshake", None),
        ]
        
        for pattern, action, param_name in patterns:
            match = re.search(pattern, command)
            if match:
                params = {}
                if param_name and match.group(1):
                    try:
                        params[param_name] = float(match.group(1))
                    except:
                        params[param_name] = 1.0 if param_name == "distance" else 45
                return {"action": action, "params": params}
        
        return {"action": "unknown", "params": {}}
    
    def _execute_action(self, action: str, params: dict) -> dict:
        """Execute action on robot"""
        try:
            if action == "forward":
                d = params.get("distance", 1.0)
                result = self.robot.move(d, 0, 0)
                
            elif action == "backward":
                d = params.get("distance", 1.0)
                result = self.robot.move(-d, 0, 0)
                
            elif action == "turn_left":
                a = params.get("angle", 45)
                self.robot.move(0, 0, 0.5)
                import time
                time.sleep(abs(a) / 45)
                result = self.robot.stop()
                
            elif action == "turn_right":
                a = abs(params.get("angle", 45))
                self.robot.move(0, 0, -0.5)
                import time
                time.sleep(a / 45)
                result = self.robot.stop()
                
            elif action == "stand":
                result = self.robot.stand()
                
            elif action == "sit":
                result = self.robot.sit()
                
            elif action == "stop":
                result = self.robot.stop()
                
            elif action == "wave":
                result = self.robot.play_action("wave")
                
            elif action == "handshake":
                result = self.robot.play_action("handshake")
                
            elif action == "unknown":
                return {"success": False, "error": f"Unknown: {action}"}
                
            else:
                result = TaskResult(False, f"Not implemented: {action}")
            
            return {"success": result.success, "message": result.message}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def start_slam(self, sensor: str = "insight9") -> dict:
        """Start SLAM with sensor"""
        from .sensors.insight9.insight9_adapter import Insight9Adapter
        
        sensor_adapter = Insight9Adapter()
        if sensor_adapter.connect():
            self.slam = VisualSLAM(sensor_adapter)
            self.slam.start()
            return {"success": True, "message": "SLAM started"}
        return {"success": False, "error": "Sensor failed"}
    
    def get_status(self) -> dict:
        """Get robot status"""
        if not self.robot:
            return {"connected": False}
        
        state = self.robot.get_state()
        result = {
            "robot": self.robot.ROBOT_NAME,
            "connected": self.robot.connected,
            **state.to_dict()
        }
        
        if self.slam:
            pose = self.slam.get_pose()
            result["pose"] = pose.position.tolist()
            
        return result


# Global instance and convenience functions
_skill = RoboticsSkill()

initialize = _skill.initialize
execute = _skill.execute
start_slam = _skill.start_slam
get_status = _skill.get_status
list_robots = RobotFactory.list_supported
