"""
Unitree robot adapters (GO1, GO2, G1, H1)
"""

import numpy as np
import time
from typing import Optional, List

from ..robot_abc import RobotBase, RobotState, TaskResult


class UnitreeGO2Adapter(RobotBase):
    """Unitree GO2 Quadruped Robot Adapter"""
    
    ROBOT_CODE = "unitree_go2"
    ROBOT_NAME = "Unitree GO2"
    BRAND = "Unitree"
    ROBOT_TYPE = "quadruped"
    JOINT_COUNT = 12
    
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
            orientation=np.array([0, 0, 0, 1]),
            joint_positions=np.zeros(self.JOINT_COUNT),
            joint_velocities=np.zeros(self.JOINT_COUNT),
            battery_level=85.0,
            temperature=35.0,
            timestamp=time.time()
        )
    
    def stand(self) -> TaskResult:
        return TaskResult(True, "Stand command executed")
    
    def sit(self) -> TaskResult:
        return TaskResult(True, "Sit command executed")
    
    def stop(self) -> TaskResult:
        return TaskResult(True, "Stop command executed")
    
    def move(self, vx: float, vy: float, yaw_rate: float) -> TaskResult:
        return TaskResult(True, f"Move: vx={vx}, vy={vy}, yaw_rate={yaw_rate}")
    
    def go_to(self, position: List[float], orientation: Optional[List[float]] = None) -> TaskResult:
        return TaskResult(True, f"Navigate to {position}")
    
    def play_action(self, action_name: str) -> TaskResult:
        actions = {"wave": "Wave hand", "handshake": "Handshake", "dance": "Dance"}
        if action_name in actions:
            return TaskResult(True, f"Play action: {actions[action_name]}")
        return TaskResult(False, f"Unknown action: {action_name}")


class UnitreeG1Adapter(RobotBase):
    """Unitree G1 Humanoid Robot Adapter"""
    
    ROBOT_CODE = "unitree_g1"
    ROBOT_NAME = "Unitree G1"
    BRAND = "Unitree"
    ROBOT_TYPE = "humanoid"
    JOINT_COUNT = 23
    
    def __init__(self, ip: str = "192.168.12.1", **kwargs):
        super().__init__(ip, **kwargs)
        
    def connect(self) -> bool:
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        self.connected = False
    
    def get_state(self) -> RobotState:
        return RobotState(
            position=np.array([0.0, 0.0, 0.0]),
            orientation=np.array([0, 0, 0, 1]),
            joint_positions=np.zeros(self.JOINT_COUNT),
            joint_velocities=np.zeros(self.JOINT_COUNT),
            battery_level=90.0,
            temperature=32.0,
            timestamp=time.time()
        )
    
    def stand(self) -> TaskResult:
        return TaskResult(True, "Stand command executed")
    
    def sit(self) -> TaskResult:
        return TaskResult(True, "Sit command executed")
    
    def stop(self) -> TaskResult:
        return TaskResult(True, "Stop command executed")
    
    def move(self, vx: float, vy: float, yaw_rate: float) -> TaskResult:
        return TaskResult(True, f"Move: vx={vx}, vy={vy}")
    
    def go_to(self, position: List[float], orientation: Optional[List[float]] = None) -> TaskResult:
        return TaskResult(True, f"Navigate to {position}")
    
    def move_arm(self, arm: str, target: List[float]) -> TaskResult:
        return TaskResult(True, f"Move {arm} arm to {target}")
    
    def grasp(self, arm: str = "right", force: float = 10.0) -> TaskResult:
        return TaskResult(True, f"Grasp with {arm} arm")
    
    def release(self, arm: str = "right") -> TaskResult:
        return TaskResult(True, f"Release {arm} arm")
    
    def play_action(self, action_name: str) -> TaskResult:
        return TaskResult(True, f"Play action: {action_name}")


# Aliases for different models
class UnitreeGO1Adapter(UnitreeGO2Adapter):
    ROBOT_CODE = "unitree_go1"
    ROBOT_NAME = "Unitree GO1"


class UnitreeH1Adapter(UnitreeG1Adapter):
    ROBOT_CODE = "unitree_h1"
    ROBOT_NAME = "Unitree H1"
    JOINT_COUNT = 20
