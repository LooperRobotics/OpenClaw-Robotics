"""
Unitree Quadruped Robots (GO1, GO2, Ali)
"""

import numpy as np
import time
from typing import Optional, List

from ..robot_adapter import RobotAdapter, RobotState, TaskResult, RobotType


class UnitreeGO2Adapter(RobotAdapter):
    """Unitree GO2"""
    
    ROBOT_CODE = "unitree_go2"
    ROBOT_NAME = "Unitree GO2"
    BRAND = "Unitree"
    ROBOT_TYPE = RobotType.QUADRUPED
    
    def __init__(self, ip: str = "192.168.12.1", **kwargs):
        super().__init__(ip, **kwargs)
        
    def connect(self) -> bool:
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        self.connected = False
    
    def get_state(self) -> RobotState:
        return RobotState(
            position=np.array([0.0, 0.0, 0.4]),
            battery_level=85.0,
            temperature=35.0
        )
    
    def stand(self) -> TaskResult:
        return TaskResult(True, "Stand executed")
    
    def sit(self) -> TaskResult:
        return TaskResult(True, "Sit executed")
    
    def stop(self) -> TaskResult:
        return TaskResult(True, "Stop executed")
    
    def move(self, x: float, y: float, yaw: float) -> TaskResult:
        return TaskResult(True, f"Move: x={x}, y={y}, yaw={yaw}")
    
    def go_to(self, position: List[float], orientation: Optional[List[float]] = None) -> TaskResult:
        return TaskResult(True, f"Go to {position}")
    
    def play_action(self, action_name: str) -> TaskResult:
        actions = {"wave": "Wave", "handshake": "Handshake", "dance": "Dance"}
        if action_name in actions:
            return TaskResult(True, f"Action: {actions[action_name]}")
        return TaskResult(False, f"Unknown: {action_name}")


class UnitreeGO1Adapter(UnitreeGO2Adapter):
    ROBOT_CODE = "unitree_go1"
    ROBOT_NAME = "Unitree GO1"


class UnitreeAliAdapter(UnitreeGO2Adapter):
    ROBOT_CODE = "unitree_ali"
    ROBOT_NAME = "Unitree Ali"
