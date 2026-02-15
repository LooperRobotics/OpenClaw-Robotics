"""
Robot Factory - Creates robot adapters by code
"""

from typing import Optional, Dict, Type
from .robots.robot_adapter import RobotAdapter


class RobotFactory:
    """Factory for creating robot adapters"""
    
    _registry: Dict[str, Type[RobotAdapter]] = {}
    
    @classmethod
    def register(cls, robot_code: str):
        """Register robot adapter"""
        def decorator(adapter_class: Type[RobotAdapter]):
            cls._registry[robot_code] = adapter_class
            return adapter_class
        return decorator
    
    @classmethod
    def create(cls, robot_code: str, ip: str = "192.168.12.1", **kwargs) -> Optional[RobotAdapter]:
        """Create robot instance"""
        if robot_code not in cls._registry:
            raise ValueError(f"Unknown: {robot_code}. Available: {list(cls._registry.keys())}")
        return cls._registry[robot_code](ip=ip, **kwargs)
    
    @classmethod
    def list_supported(cls) -> list:
        """List all supported"""
        return list(cls._registry.keys())


# Register default robots
from .robots import UnitreeGO1Adapter, UnitreeGO2Adapter, UnitreeAliAdapter
from .robots import UnitreeG1Adapter, UnitreeH1Adapter

RobotFactory.register("unitree_go1")(UnitreeGO1Adapter)
RobotFactory.register("unitree_go2")(UnitreeGO2Adapter)
RobotFactory.register("unitree_ali")(UnitreeAliAdapter)
RobotFactory.register("unitree_g1")(UnitreeG1Adapter)
RobotFactory.register("unitree_h1")(UnitreeH1Adapter)
