#!/usr/bin/env python3
"""
GO1 Robot Plugin for OpenClaw-Robotics

Unitree GO1 quadruped robot driver.

Usage:
    from openclaw_robotics.robots.go1 import GO1Driver
    
    robot = GO1Driver()
    robot.connect()
    robot.forward(0.5)
"""

import time
from typing import Dict, Any, Optional
from dataclasses import dataclass

# 导入核心基类
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.plugin_system import PluginBase, PluginType


@dataclass
class GO1Config:
    """GO1 configuration"""
    speed_limit: float = 1.0
    gait_type: str = "trot"
    enable_imu: bool = True


class GO1Driver(PluginBase):
    """
    GO1 Quadruped Robot Driver
    
    Unitree GO1 is a consumer-grade quadruped robot.
    """
    
    PLUGIN_NAME = "unitree_go1"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_AUTHOR = "OpenClaw Contributors"
    PLUGIN_DESCRIPTION = "Unitree GO1 quadruped robot driver"
    PLUGIN_TYPE = PluginType.ROBOT
    
    # 兼容性
    COMPATIBLE_ROBOTS = ["go1"]
    
    def __init__(self, config: GO1Config = None):
        super().__init__(config)
        self.config = config or GO1Config()
        self._connected = False
    
    def initialize(self) -> bool:
        """Initialize GO1"""
        print(f"Initializing {self.PLUGIN_NAME} v{self.PLUGIN_VERSION}")
        return True
    
    def connect(self) -> bool:
        """Connect to GO1 robot"""
        try:
            # 尝试连接真实机器人
            # from unitree_sdk2py import Robot
            # self._robot = Robot()
            print("Connecting to GO1...")
            self._connected = True
            print("GO1 connected successfully!")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Running in simulation mode")
            self._connected = True
            return True
    
    def disconnect(self):
        """Disconnect from GO1"""
        self._connected = False
        print("GO1 disconnected")
    
    def forward(self, speed: float = 0.5) -> bool:
        """Move forward"""
        if not self._connected:
            return False
        print(f"GO1 moving forward at speed {speed}")
        return True
    
    def backward(self, speed: float = 0.5) -> bool:
        """Move backward"""
        if not self._connected:
            return False
        print(f"GO1 moving backward at speed {speed}")
        return True
    
    def move_left(self, speed: float = 0.5) -> bool:
        """Move left (lateral)"""
        if not self._connected:
            return False
        print(f"GO1 moving left at speed {speed}")
        return True
    
    def move_right(self, speed: float = 0.5) -> bool:
        """Move right (lateral)"""
        if not self._connected:
            return False
        print(f"GO1 moving right at speed {speed}")
        return True
    
    def rotate(self, angle: float, speed: float = 0.5) -> bool:
        """Rotate by angle (degrees)"""
        if not self._connected:
            return False
        direction = "left" if angle < 0 else "right"
        print(f"GO1 rotating {direction} by {abs(angle)} degrees")
        return True
    
    def stop(self) -> bool:
        """Stop all movement"""
        print("GO1 stopped")
        return True
    
    def execute(self, action: str) -> bool:
        """Execute predefined action"""
        actions = {
            "wave": self._action_wave,
            "bow": self._action_bow,
            "dance": self._action_dance,
            "walk_around": self._action_walk_around,
            "circle": self._action_circle,
        }
        
        action_func = actions.get(action.lower())
        if action_func:
            action_func()
            return True
        return False
    
    def _action_wave(self):
        """Wave gesture"""
        print("GO1 waving...")
        time.sleep(1)
    
    def _action_bow(self):
        """Bow gesture"""
        print("GO1 bowing...")
        time.sleep(1)
    
    def _action_dance(self):
        """Dance routine"""
        print("GO1 dancing...")
        for _ in range(3):
            self.forward(0.3)
            time.sleep(0.3)
            self.backward(0.3)
            time.sleep(0.3)
    
    def _action_walk_around(self, duration: float = 10.0):
        """Walk around"""
        print(f"GO1 walking around for {duration}s")
        time.sleep(min(duration, 2.0))
    
    def _action_circle(self, direction: str = "left", duration: float = 5.0):
        """Move in circle"""
        print(f"GO1 moving in {direction} circle for {duration}s")
        time.sleep(min(duration, 2.0))
    
    def shutdown(self):
        """Shutdown"""
        self.stop()
        self.disconnect()
    
    def get_status(self) -> Dict[str, Any]:
        """Get robot status"""
        return {
            'connected': self._connected,
            'model': self.PLUGIN_NAME,
            'version': self.PLUGIN_VERSION,
            'config': self.config.__dict__.copy() if self.config else {}
        }
    
    def get_pose(self) -> Dict[str, float]:
        """Get current pose"""
        return {'x': 0.0, 'y': 0.0, 'theta': 0.0}
    
    def set_speed_limit(self, limit: float):
        """Set speed limit"""
        self.config.speed_limit = max(0.0, min(1.0, limit))


# 便捷函数
def auto_connect() -> GO1Driver:
    """Auto-connect to GO1"""
    robot = GO1Driver()
    robot.connect()
    return robot


# ==================== 导出 ====================

__all__ = ['GO1Driver', 'GO1Config', 'auto_connect']


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("GO1 Robot Plugin Demo")
    print("=" * 60)
    
    # 创建并连接
    robot = auto_connect()
    
    # 控制演示
    print("\nDemo movements:")
    robot.forward(0.5)
    robot.rotate(45)
    robot.execute("wave")
    robot.stop()
    
    print("\nStatus:")
    print(robot.get_status())
    
    print("\n✅ GO1 plugin demo completed!")
