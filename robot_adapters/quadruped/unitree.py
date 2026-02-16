"""Unitree Quadruped Robots (GO1, GO2)"""

import numpy as np
from typing import Optional, List

from ..base import RobotAdapter, RobotState, TaskResult, RobotType


class UnitreeGO2Adapter(RobotAdapter):
    """Unitree GO2 - Industrial Quadruped Robot"""
    
    ROBOT_CODE = "unitree_go2"
    ROBOT_NAME = "Unitree GO2"
    BRAND = "Unitree"
    ROBOT_TYPE = RobotType.QUADRUPED
    
    def __init__(self, ip: str = "192.168.12.1", **kwargs):
        super().__init__(ip, **kwargs)
        self._position = np.array([0.0, 0.0, 0.0])
        self._battery = 100.0
        
    def connect(self) -> bool:
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        self.connected = False
    
    def get_state(self) -> RobotState:
        return RobotState(
            position=self._position.copy(),
            battery_level=self._battery,
            temperature=35.0
        )
    
    def move(self, x: float, y: float, yaw: float) -> TaskResult:
        # Simulate movement
        self._position[0] += x
        self._position[1] += y
        # Simple yaw simulation not affecting x/y for now
        
        # Simulate battery drain
        drain = (abs(x) + abs(y)) * 0.1
        self._battery = max(0.0, self._battery - drain)
        
        return TaskResult(
            success=True, 
            message=f"Move: x={x}, y={y}, yaw={yaw}",
            data={
                "position": self._position.tolist(),
                "battery": self._battery
            }
        )
    
    def stop(self) -> TaskResult:
        return TaskResult(True, "Stopped", data={"velocity": [0,0,0]})
    
    def stand(self) -> TaskResult:
        self._position[2] = 0.4 # Stand height
        return TaskResult(True, "Stand executed", data={"height": 0.4})
    
    def sit(self) -> TaskResult:
        self._position[2] = 0.1 # Sit height
        return TaskResult(True, "Sit executed", data={"height": 0.1})
    
    def go_to(self, position: List[float]) -> TaskResult:
        target = np.array(position)
        dist = np.linalg.norm(target - self._position)
        self._position = target
        self._battery -= dist * 0.1
        return TaskResult(True, f"Go to {position}", data={"position": self._position.tolist()})
    
    def play_action(self, action_name: str) -> TaskResult:
        actions = {"wave": "Wave", "handshake": "Handshake", "dance": "Dance"}
        if action_name in actions:
            self._battery -= 1.0
            return TaskResult(True, f"Action: {actions[action_name]}", data={"action": action_name})
        return TaskResult(False, f"Unknown: {action_name}")


class UnitreeGO1Adapter(UnitreeGO2Adapter):
    """Unitree GO1 - Consumer Quadruped Robot"""
    ROBOT_CODE = "unitree_go1"
    ROBOT_NAME = "Unitree GO1"
