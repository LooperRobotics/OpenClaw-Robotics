"""
Robot Factory - Creates robot adapters based on brand/model
"""

from typing import Optional, Dict, Type
from .robot_abc import RobotBase


class RobotFactory:
    """Factory for creating robot adapters"""
    
    _registry: Dict[str, Type[RobotBase]] = {}
    
    @classmethod
    def register(cls, robot_code: str):
        """Decorator to register robot adapter"""
        def decorator(adapter_class: Type[RobotBase]):
            cls._registry[robot_code] = adapter_class
            return adapter_class
        return decorator
    
    @classmethod
    def create(cls, robot_code: str, ip: str = "192.168.12.1", **kwargs) -> Optional[RobotBase]:
        """Create robot instance"""
        if robot_code not in cls._registry:
            raise ValueError(f"Unknown robot: {robot_code}. Available: {list(cls._registry.keys())}")
        
        adapter_class = cls._registry[robot_code]
        return adapter_class(ip=ip, **kwargs)
    
    @classmethod
    def list_supported(cls) -> list:
        """List all supported robots"""
        return list(cls._registry.keys())


# Register adapters
from .adapters import UnitreeGO1Adapter, UnitreeGO2Adapter, UnitreeG1Adapter, UnitreeH1Adapter

RobotFactory.register("unitree_go1")(UnitreeGO1Adapter)
RobotFactory.register("unitree_go2")(UnitreeGO2Adapter)
RobotFactory.register("unitree_g1")(UnitreeG1Adapter)
RobotFactory.register("unitree_h1")(UnitreeH1Adapter)
