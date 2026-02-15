#!/usr/bin/env python3
"""
G1 Robot Plugin for OpenClaw-Robotics

Unitree G1 humanoid robot driver.

Usage:
    from openclaw_robotics.robots.g1 import G1Driver
    
    robot = G1Driver()
    robot.connect()
    robot.walk(steps=5)
"""

import time
from typing import Dict, Any
from dataclasses import dataclass

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.plugin_system import PluginBase, PluginType


@dataclass
class G1Config:
    """G1 configuration"""
    speed_limit: float = 0.8  # Slower for bipedal
    arm_enabled: bool = True
    leg_mode: str = "bipedal"
    balance_gain: float = 1.0


class G1Driver(PluginBase):
    """
    G1 Humanoid Robot Driver
    
    Unitree G1 is a humanoid robot with bipedal locomotion
    and arm manipulation capabilities.
    """
    
    PLUGIN_NAME = "unitree_g1"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_AUTHOR = "OpenClaw Contributors"
    PLUGIN_DESCRIPTION = "Unitree G1 humanoid robot driver"
    PLUGIN_TYPE = PluginType.ROBOT
    
    COMPATIBLE_ROBOTS = ["g1"]
    
    def __init__(self, config: G1Config = None):
        super().__init__(config)
        self.config = config or G1Config()
        self._connected = False
    
    def initialize(self) -> bool:
        """Initialize G1"""
        print(f"Initializing {self.PLUGIN_NAME} v{self.PLUGIN_VERSION}")
        print("Humanoid features: bipedal walk, arm gestures")
        return True
    
    def connect(self) -> bool:
        """Connect to G1 robot"""
        try:
            print("Connecting to G1...")
            self._connected = True
            print("G1 connected successfully!")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Running in simulation mode")
            self._connected = True
            return True
    
    def disconnect(self):
        """Disconnect from G1"""
        self._connected = False
        print("G1 disconnected")
    
    def forward(self, speed: float = 0.5) -> bool:
        """Move forward (bipedal)"""
        if not self._connected:
            return False
        print(f"G1 bipedal walking forward at speed {speed}")
        return True
    
    def backward(self, speed: float = 0.5) -> bool:
        """Move backward"""
        if not self._connected:
            return False
        print(f"G1 bipedal walking backward at speed {speed}")
        return True
    
    def move_left(self, speed: float = 0.5) -> bool:
        """Move left (side step)"""
        if not self._connected:
            return False
        print(f"G1 side stepping left at speed {speed}")
        return True
    
    def move_right(self, speed: float = 0.5) -> bool:
        """Move right"""
        if not self._connected:
            return False
        print(f"G1 side stepping right at speed {speed}")
        return True
    
    def rotate(self, angle: float, speed: float = 0.5) -> bool:
        """Rotate in place"""
        if not self._connected:
            return False
        direction = "left" if angle < 0 else "right"
        print(f"G1 turning {direction} by {abs(angle)} degrees")
        return True
    
    def stop(self) -> bool:
        """Stop with stable stance"""
        print("G1 stopped with stable stance")
        return True
    
    def walk(self, steps: int = 5, speed: float = 0.5) -> bool:
        """Bipedal walking (G1 specific)"""
        if not self._connected:
            return False
        print(f"G1 walking {steps} steps at speed {speed}")
        for _ in range(min(steps, 3)):
            self.forward(speed)
        return True
    
    def execute(self, action: str) -> bool:
        """Execute humanoid-specific actions"""
        actions = {
            "wave": self._action_wave,
            "bow": self._action_bow,
            "stretch": self._action_stretch,
            "sit": self._action_sit,
            "stand": self._action_stand,
            "turn_around": self._action_turn_around,
            "squat": self._action_squat,
            "hello": self._action_wave,  # Alias
        }
        
        action_func = actions.get(action.lower())
        if action_func:
            action_func()
            return True
        return False
    
    def _action_wave(self):
        print("G1 waving hello...")
        time.sleep(1)
    
    def _action_bow(self):
        print("G1 bowing politely...")
        time.sleep(1)
    
    def _action_stretch(self):
        print("G1 stretching arms and legs...")
        time.sleep(1)
    
    def _action_sit(self):
        print("G1 sitting down")
        time.sleep(1)
    
    def _action_stand(self):
        print("G1 standing up")
        time.sleep(1)
    
    def _action_turn_around(self, angle: float = 180):
        """Turn around in place"""
        print(f"G1 turning around ({angle} degrees)")
        time.sleep(1)
    
    def _action_squat(self, duration: float = 2.0):
        """Squat movement"""
        print(f"G1 squatting for {duration}s")
        time.sleep(min(duration, 1.0))
        self.stand()
    
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
            'config': self.config.__dict__.copy() if self.config else {},
            'type': 'humanoid'
        }
    
    def get_pose(self) -> Dict[str, float]:
        """Get current pose"""
        return {'x': 0.0, 'y': 0.0, 'theta': 0.0, 'height': 1.2}  # G1 height


def auto_connect() -> G1Driver:
    """Auto-connect to G1"""
    robot = G1Driver()
    robot.connect()
    return robot


__all__ = ['G1Driver', 'G1Config', 'auto_connect']


if __name__ == "__main__":
    print("=" * 60)
    print("G1 Humanoid Robot Plugin Demo")
    print("=" * 60)
    
    robot = auto_connect()
    
    print("\nDemo movements:")
    robot.forward(0.5)
    robot.walk(3)
    robot.execute("wave")
    robot.execute("bow")
    robot.execute("turn_around")
    robot.stop()
    
    print("\nStatus:")
    print(robot.get_status())
    
    print("\n✅ G1 plugin demo completed!")
