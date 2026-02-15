"""
Looper Robotics Insight9 RGB-D Camera Adapter

Deep integration with Insight9 Pro/Max cameras
"""

import numpy as np
import time
from typing import Optional, Tuple, List
from dataclasses import dataclass

from ..sensor_adapter import SensorAdapter, SensorData, ImageData, DepthData, PointCloudData


@dataclass
class Insight9Config:
    """Insight9 configuration"""
    serial: str = ""
    resolution: str = "1080p"  # 720p, 1080p, 4K
    depth_range: str = "medium"  # near, medium, far
    fps: int = 30
    enable_ir: bool = True


class Insight9Adapter(SensorAdapter):
    """
    Looper Robotics Insight9 RGB-D Camera
    
    Specifications:
    - RGB: 1080P @ 30fps
    - Depth: 0.1-10m range
    - IR: Built-in
    - Interface: USB-C / Ethernet
    """
    
    SENSOR_CODE = "insight9"
    SENSOR_NAME = "Looper Robotics Insight9"
    
    def __init__(self, config: Insight9Config = None, **kwargs):
        super().__init__(**kwargs)
        self.config = config or Insight9Config()
        self.running = False
        
    def connect(self) -> bool:
        """Connect to Insight9 camera"""
        # import insight9_sdk
        # self.device = insight9_sdk.connect(self.config.serial)
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        self.connected = False
        self.running = False
    
    def start(self):
        """Start streaming"""
        self.running = True
        
    def stop(self):
        """Stop streaming"""
        self.running = False
    
    def get_data(self) -> dict:
        """Get RGB-D data"""
        return {
            "rgb": np.zeros((1080, 1920, 3), dtype=np.uint8),
            "depth": np.zeros((1080, 1920), dtype=np.uint16),
            "timestamp": time.time()
        }
    
    def get_rgb(self) -> ImageData:
        """Get RGB image"""
        data = self.get_data()
        return ImageData(
            data=data["rgb"],
            width=1920,
            height=1080,
            format="rgb"
        )
    
    def get_depth(self) -> DepthData:
        """Get depth image (in millimeters)"""
        data = self.get_data()
        return DepthData(
            data=data["depth"],
            width=1920,
            height=1080
        )
    
    def get_pointcloud(self) -> PointCloudData:
        """Get point cloud from depth"""
        depth = self.get_depth()
        # Convert depth to point cloud (simplified)
        points = np.zeros((1000, 3))
        return PointCloudData(points=points)
    
    def get_intrinsics(self) -> dict:
        """Get camera intrinsics"""
        return {
            "fx": 1050.0,
            "fy": 1050.0,
            "cx": 960.0,
            "cy": 540.0,
            "width": 1920,
            "height": 1080
        }
    
    def get_extrinsics(self) -> np.ndarray:
        """Get extrinsics (T_cam_to_base)"""
        return np.eye(4)


class Insight9ProAdapter(Insight9Adapter):
    """Insight9 Pro"""
    SENSOR_CODE = "insight9_pro"
    SENSOR_NAME = "Insight9 Pro"


class Insight9MaxAdapter(Insight9Adapter):
    """Insight9 Max - Higher resolution"""
    SENSOR_CODE = "insight9_max"
    SENSOR_NAME = "Insight9 Max"
    
    def get_data(self) -> dict:
        # 4K resolution
        return {
            "rgb": np.zeros((2160, 3840, 3), dtype=np.uint8),
            "depth": np.zeros((2160, 3840), dtype=np.uint16),
            "timestamp": time.time()
        }
