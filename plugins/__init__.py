#!/usr/bin/env python3
"""
OpenClaw-Robotics Plugins

This module provides easy access to all robot plugins.

Usage:
    from openclaw_robotics.robots import GO1, GO2, G1
    from openclaw_robotics.sensors import Insight9V1, Insight9Pro, Insight9Max
    from openclaw_robotics.plugins import auto_connect_robot, auto_init_slam

Example:
    # 自动连接机器人
    from openclaw_robotics.plugins import auto_connect_robot
    robot = auto_connect_robot()
    
    # 控制
    robot.forward(0.5)
    robot.rotate(45)
"""

from .auto_import import (
    # 便捷函数
    auto_connect_robot,
    auto_init_slam,
    
    # 机器人
    get_robot_driver,
    list_available_robots,
    
    # 传感器
    get_sensor_driver,
    list_available_sensors,
    
    # SLAM
    get_slam_driver,
    list_available_slam,
    
    # 导航
    get_navigation_driver,
    list_available_navigation,
)

__all__ = [
    # 便捷函数
    'auto_connect_robot',
    'auto_init_slam',
    
    # 机器人
    'get_robot_driver',
    'list_available_robots',
    
    # 传感器
    'get_sensor_driver',
    'list_available_sensors',
    
    # SLAM
    'get_slam_driver',
    'list_available_slam',
    
    # 导航
    'get_navigation_driver',
    'list_available_navigation',
]
