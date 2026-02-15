"""Robot adapters"""

from .robot_adapter import RobotAdapter, RobotState, TaskResult, RobotType

# Quadruped
from .quadruped.unitree import UnitreeGO1Adapter, UnitreeGO2Adapter, UnitreeAliAdapter

# Humanoid
from .humanoid.unitree import UnitreeG1Adapter, UnitreeH1Adapter

__all__ = [
    "RobotAdapter", "RobotState", "TaskResult", "RobotType",
    "UnitreeGO1Adapter", "UnitreeGO2Adapter", "UnitreeAliAdapter",
    "UnitreeG1Adapter", "UnitreeH1Adapter"
]
