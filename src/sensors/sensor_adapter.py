"""
Sensor Adapter Base Class
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import numpy as np
import time


@dataclass
class SensorData:
    """Sensor data"""
    timestamp: float = field(default_factory=time.time)
    data: any = None


@dataclass
class ImageData(SensorData):
    """Image data"""
    width: int = 0
    height: int = 0
    format: str = "rgb"


@dataclass
class DepthData(SensorData):
    """Depth image data"""
    width: int = 0
    height: int = 0


@dataclass
class PointCloudData(SensorData):
    """Point cloud data"""
    points: np.ndarray = None


class SensorAdapter(ABC):
    """Base class for sensors"""
    
    SENSOR_CODE: str = ""
    SENSOR_NAME: str = ""
    
    def __init__(self, **kwargs):
        self.connected = False
        
    @abstractmethod
    def connect(self) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        pass
    
    @abstractmethod
    def get_data(self) -> SensorData:
        pass
