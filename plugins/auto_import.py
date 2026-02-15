#!/usr/bin/env python3
"""
Auto-import System for OpenClaw-Robotics

让用户像导入Python库一样简单地使用机器人插件

Usage:
    from openclaw_robotics.robots import auto_connect
    from openclaw_robotics.sensors import Insight9Pro
    from openclaw_robotics.slam import auto_init_slam
"""

import os
import sys
import importlib
from typing import Dict, List, Type, Any

# 插件注册表
ROBOTS_REGISTRY = {
    "go1": "openclaw_robotics.robots.go1",
    "go2": "openclaw_robotics.robots.go2",
    "g1": "openclaw_robotics.robots.g1",
}

SENSORS_REGISTRY = {
    "insight9_v1": "openclaw_robotics.sensors.insight9",
    "insight9_pro": "openclaw_robotics.sensors.insight9",
    "insight9_max": "openclaw_robotics.sensors.insight9",
}

SLAM_REGISTRY = {
    "orb_slam3": "openclaw_robotics.slam",
    "vins_fusion": "openclaw_robotics.slam",
}

NAVIGATION_REGISTRY = {
    "tinynav": "openclaw_robotics.navigation",
}


def auto_import(registry: Dict[str, str], name: str = None) -> Any:
    """
    自动导入并返回插件类
    
    Args:
        registry: 插件注册表
        name: 插件名称 (可选，自动检测)
    
    Returns:
        插件类
    
    Example:
        # 自动检测
        Robot = auto_import(ROBOTS_REGISTRY)
        
        # 指定型号
        Robot = auto_import(ROBOTS_REGISTRY, "go2")
    """
    if name:
        # 指定名称导入
        if name not in registry:
            raise ImportError(f"Unknown plugin: {name}")
        
        module_path = registry[name]
        try:
            module = importlib.import_module(module_path)
            return getattr(module, f"{name.title().replace('_', '')}Driver")
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Failed to import {name}: {e}")
    else:
        # 尝试所有可用的插件
        for name, module_path in registry.items():
            try:
                module = importlib.import_module(module_path)
                driver_class = getattr(module, f"{name.title().replace('_', '')}Driver")
                return driver_class
            except (ImportError, AttributeError):
                continue
        
        raise ImportError("No available plugins found")


def list_available_plugins(registry: Dict[str, str]) -> List[str]:
    """列出所有可用的插件"""
    available = []
    for name, module_path in registry.items():
        try:
            module = importlib.import_module(module_path)
            available.append(name)
        except ImportError:
            pass
    return available


# ==================== 机器人自动导入 ====================

def get_robot_driver(name: str = None):
    """
    获取机器人驱动类
    
    Args:
        name: 机器人型号 (go1, go2, g1)
    
    Returns:
        机器人驱动类
    
    Example:
        GO2Driver = get_robot_driver("go2")
        robot = GO2Driver()
    """
    return auto_import(ROBOTS_REGISTRY, name)


def list_available_robots() -> List[str]:
    """列出所有可用的机器人"""
    return list_available_plugins(ROBOTS_REGISTRY)


# ==================== 传感器自动导入 ====================

def get_sensor_driver(name: str = "insight9_pro"):
    """
    获取传感器驱动类
    
    Args:
        name: 传感器型号
    
    Returns:
        传感器驱动类
    """
    return auto_import(SENSORS_REGISTRY, name)


def list_available_sensors() -> List[str]:
    """列出所有可用的传感器"""
    return list_available_plugins(SENSORS_REGISTRY)


# ==================== SLAM自动导入 ====================

def get_slam_driver(name: str = "orb_slam3"):
    """
    获取SLAM驱动类
    
    Args:
        name: SLAM算法名称
    
    Returns:
        SLAM驱动类
    """
    return auto_import(SLAM_REGISTRY, name)


def list_available_slam() -> List[str]:
    """列出所有可用的SLAM算法"""
    return list_available_plugins(SLAM_REGISTRY)


# ==================== 导航自动导入 ====================

def get_navigation_driver(name: str = "tinynav"):
    """
    获取导航驱动类
    
    Args:
        name: 导航算法名称
    
    Returns:
        导航驱动类
    """
    return auto_import(NAVIGATION_REGISTRY, name)


def list_available_navigation() -> List[str]:
    """列出所有可用的导航算法"""
    return list_available_plugins(NAVIGATION_REGISTRY)


# ==================== 便捷函数 ====================

def auto_connect_robot() -> Any:
    """
    自动检测并连接机器人
    
    Returns:
        已连接的机器人实例
    
    Example:
        from openclaw_robotics.plugins import auto_connect_robot
        robot = auto_connect_robot()
        robot.forward(0.5)
    """
    # 尝试所有可用的机器人
    for name in ROBOTS_REGISTRY.keys():
        try:
            DriverClass = get_robot_driver(name)
            robot = DriverClass()
            if robot.connect():
                return robot
        except Exception as e:
            continue
    
    raise ConnectionError("Could not connect to any robot")


def auto_init_slam(sensor: str = "insight9_pro") -> Any:
    """
    自动初始化SLAM系统
    
    Args:
        sensor: 传感器名称
    
    Returns:
        已初始化的SLAM实例
    
    Example:
        from openclaw_robotics.plugins import auto_init_slam
        slam = auto_init_slam(sensor="insight9_pro")
        pose = slam.get_pose()
    """
    # 获取SLAM驱动
    SLAMClass = get_slam_driver()
    
    # 获取传感器驱动并创建实例
    SensorClass = get_sensor_driver(sensor)
    camera = SensorClass()
    
    # 初始化
    slam = SLAMClass()
    return slam


# ==================== 批量导入 ====================

__all__ = [
    # 机器人
    'get_robot_driver',
    'list_available_robots',
    'auto_connect_robot',
    
    # 传感器
    'get_sensor_driver',
    'list_available_sensors',
    
    # SLAM
    'get_slam_driver',
    'list_available_slam',
    'auto_init_slam',
    
    # 导航
    'get_navigation_driver',
    'list_available_navigation',
    
    # 便捷函数
    'auto_import',
]


if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("OpenClaw-Robotics Auto-Import Demo")
    print("=" * 60)
    
    # 列出可用的插件
    print("\n📦 Available Robots:")
    for name in list_available_robots():
        print(f"  - {name}")
    
    print("\n📷 Available Sensors:")
    for name in list_available_sensors():
        print(f"  - {name}")
    
    print("\n🗺️ Available SLAM:")
    for name in list_available_slam():
        print(f"  - {name}")
    
    print("\n🧭 Available Navigation:")
    for name in list_available_navigation():
        print(f"  - {name}")
    
    print("\n" + "=" * 60)
    print("✅ Auto-import system ready!")
    print("\nUsage examples:")
    print('  from openclaw_robotics.plugins import auto_connect_robot')
    print('  robot = auto_connect_robot()')
    print("")
