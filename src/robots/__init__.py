#!/usr/bin/env python3
"""
OpenClaw-Robotics Robot Plugins

Available robot drivers:
- GO1: Consumer quadruped robot
- GO2: Professional quadruped robot
- G1: Humanoid robot

Usage:
    from openclaw_robotics.robots import GO1, GO2, G1
    
    robot = GO1.connect()
    robot.forward(0.5)
"""

from .go1 import GO1Driver, GO1Config
from .go2 import GO2Driver, GO2Config
from .g1 import G1Driver, G1Config

__all__ = [
    'GO1Driver', 'GO1Config',
    'GO2Driver', 'GO2Config',
    'G1Driver', 'G1Config',
]
