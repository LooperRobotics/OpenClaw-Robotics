"""
Robot Base Class - Abstract interface for multi-brand robot control.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List
import numpy as np
import time


@dataclass
class RobotState:
    """Robot state data structure"""
    position: np.ndarray      # [x, y, z] in meters
    orientation: np.ndarray   # quaternion [x, y, z, w]
    joint_positions: np.ndarray
    joint_velocities: np.ndarray
    battery_level: float      # 0-100
    temperature: float        # celsius
    timestamp: float
    
    def to_dict(self) -> dict:
        return {
            "position": self.position.tolist() if hasattr(self.position, 'tolist') else list(self.position),
            "battery": f"{self.battery_level}%",
            "temperature": f"{self.temperature}°C"
        }


@dataclass
class TaskResult:
    """Task execution result"""
    success: bool
    message: str
    data: Optional[dict] = None


class RobotBase(ABC):
    """Abstract base class for robot adapters"""
    
    ROBOT_CODE: str = ""
    ROBOT_NAME: str = ""
    BRAND: str = ""
    ROBOT_TYPE: str = "quadruped"  # quadruped/humanoid/manipulator
    JOINT_COUNT: int = 12
    
    def __init__(self, ip: str = "192.168.12.1", **kwargs):
        self.ip = ip
        self.connected = False
        self.state = None
        
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to robot"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from robot"""
        pass
    
    @abstractmethod
    def get_state(self) -> RobotState:
        """Get current robot state"""
        pass
    
    # --- Standard Action Interface ---
    
    @abstractmethod
    def stand(self) -> TaskResult:
        """Stand up"""
        pass
    
    @abstractmethod
    def sit(self) -> TaskResult:
        """Sit down"""
        pass
    
    @abstractmethod
    def stop(self) -> TaskResult:
        """Stop all motion"""
        pass
    
    @abstractmethod
    def move(self, vx: float, vy: float, yaw_rate: float) -> TaskResult:
        """Move robot (base frame)"""
        pass
    
    @abstractmethod
    def go_to(self, position: List[float], orientation: Optional[List[float]] = None) -> TaskResult:
        """Navigate to position"""
        pass
    
    # --- Arm Interface (for humanoid/manipulator) ---
    
    def move_arm(self, arm: str, target: List[float]) -> TaskResult:
        """Move arm to target position"""
        return TaskResult(False, f"{self.ROBOT_CODE} does not support arm control")
    
    def grasp(self, arm: str = "right", force: float = 10.0) -> TaskResult:
        """Grasp object"""
        return TaskResult(False, f"{self.ROBOT_CODE} does not support grasping")
    
    def release(self, arm: str = "right") -> TaskResult:
        """Release object"""
        return TaskResult(False, f"{self.ROBOT_CODE} does not support releasing")
    
    # --- Predefined Actions ---
    
    def play_action(self, action_name: str) -> TaskResult:
        """Play predefined action"""
        return TaskResult(False, f"Action {action_name} not defined")
    
    def get_info(self) -> dict:
        """Get robot information"""
        return {
            "code": self.ROBOT_CODE,
            "name": self.ROBOT_NAME,
            "brand": self.BRAND,
            "type": self.ROBOT_TYPE,
            "ip": self.ip,
            "connected": self.connected
        }
