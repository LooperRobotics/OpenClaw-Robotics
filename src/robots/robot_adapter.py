"""
Robot Adapter Base Class
Supports quadrupeds, humanoids, wheeled, aerial, and surface robots
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, List, Dict
import numpy as np
import time


@dataclass
class RobotState:
    """Robot state"""
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))
    orientation: np.ndarray = field(default_factory=lambda: np.array([0, 0, 0, 1]))
    joint_positions: np.ndarray = field(default_factory=lambda: np.zeros(12))
    joint_velocities: np.ndarray = field(default_factory=lambda: np.zeros(12))
    battery_level: float = 100.0
    temperature: float = 25.0
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> dict:
        return {
            "position": self.position.tolist(),
            "battery": f"{self.battery_level}%",
            "temperature": f"{self.temperature}°C"
        }


@dataclass  
class TaskResult:
    """Task execution result"""
    success: bool
    message: str = ""
    data: Optional[dict] = None


class RobotType:
    """Robot type constants"""
    QUADRUPED = "quadruped"      # 四足机器人
    HUMANOID = "humanoid"        # 人形机器人
    WHEELED = "wheeled"          # 轮式小车
    AERIAL = "aerial"            # 无人机
    SURFACE = "surface"          # 无人船/车
    MANIPULATOR = "manipulator"  # 机械臂


class RobotAdapter(ABC):
    """Abstract base class for robot adapters"""
    
    ROBOT_CODE: str = ""
    ROBOT_NAME: str = ""
    BRAND: str = ""
    ROBOT_TYPE: str = RobotType.QUADRUPED
    
    def __init__(self, ip: str = "192.168.12.1", **kwargs):
        self.ip = ip
        self.connected = False
        self.state = RobotState()
        
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        pass
    
    @abstractmethod
    def get_state(self) -> RobotState:
        pass
    
    # --- Basic Actions ---
    @abstractmethod
    def stand(self) -> TaskResult:
        pass
    
    @abstractmethod
    def sit(self) -> TaskResult:
        pass
    
    @abstractmethod
    def stop(self) -> TaskResult:
        pass
    
    # --- Movement ---
    @abstractmethod
    def move(self, x: float, y: float, yaw: float) -> TaskResult:
        """Move: x-forward, y-left, yaw-rotation"""
        pass
    
    @abstractmethod
    def go_to(self, position: List[float], orientation: Optional[List[float]] = None) -> TaskResult:
        """Navigate to position"""
        pass
    
    # --- Arm Control (for humanoid/manipulator) ---
    def move_arm(self, arm: str, target: List[float]) -> TaskResult:
        return TaskResult(False, "Not supported")
    
    def grasp(self, arm: str = "right") -> TaskResult:
        return TaskResult(False, "Not supported")
    
    def release(self, arm: str = "right") -> TaskResult:
        return TaskResult(False, "Not supported")
    
    # --- Predefined Actions ---
    def play_action(self, action_name: str) -> TaskResult:
        return TaskResult(False, f"Action {action_name} not defined")
    
    def get_info(self) -> dict:
        return {
            "code": self.ROBOT_CODE,
            "name": self.ROBOT_NAME,
            "brand": self.BRAND,
            "type": self.ROBOT_TYPE,
            "ip": self.ip,
            "connected": self.connected
        }
