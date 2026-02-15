#!/usr/bin/env python3
"""
Insight9 Camera Driver for LooperRobotics Sensors

Provides drivers for Insight9 series cameras:
- Insight9-V1 (Entry-level)
- Insight9-Pro (Professional)
- Insight9-Max (Flagship)
- Insight9-Lidar (Fusion)

Author: OpenClaw Contributors
License: MIT
"""

import os
import sys
import time
import json
import logging
import threading
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Insight9Model(Enum):
    """Insight9 camera models"""
    V1 = "v1"
    PRO = "pro"
    MAX = "max"
    LIDAR = "lidar"


@dataclass
class Insight9Config:
    """Insight9 camera configuration"""
    model: Insight9Model = Insight9Model.PRO
    resolution: Tuple[int, int] = (1920, 1080)
    fps: int = 30
    enable_depth: bool = True
    enable_ir: bool = True
    enable_lidar: bool = False
    depth_mode: str = "medium"  # low, medium, high
    ir_power: int = 50  # 0-100
    exposure_mode: str = "auto"  # auto, manual
    manual_exposure: int = 33  # ms
    gain: int = 0  # 0-100
    hardware_sync: bool = False
    sync_master: bool = True


@dataclass
class Insight9Data:
    """Data from Insight9 camera"""
    rgb_image: np.ndarray = None
    depth_image: np.ndarray = None
    ir_image: np.ndarray = None
    lidar_points: np.ndarray = None  # (N, 3) XYZ points
    timestamp: float = 0.0
    sequence_id: int = 0
    intrinsics: Dict = field(default_factory=dict)
    extrinsics: Dict = field(default_factory=dict)


class Insight9Base:
    """Base class for Insight9 cameras"""
    
    PLUGIN_NAME = "insight9_base"
    PLUGIN_VERSION = "1.0.0"
    
    def __init__(self, config: Insight9Config = None):
        """
        Initialize Insight9 camera
        
        Args:
            config: Camera configuration
        """
        self.config = config or Insight9Config()
        self._connected = False
        self._streaming = False
        self._sequence_id = 0
        self._data_callback: Optional[Callable[[Insight9Data], None]] = None
        self._thread: threading.Thread = None
        self._stop_event = threading.Event()
        
        # Set model-specific defaults
        self._set_model_defaults()
        
        logger.info(f"Initializing Insight9 {self.config.model.value}")
    
    def _set_model_defaults(self):
        """Set default values based on model"""
        defaults = {
            Insight9Model.V1: Insight9Config(
                model=Insight9Model.V1,
                resolution=(1280, 720),
                fps=30,
                enable_depth=True
            ),
            Insight9Model.PRO: Insight9Config(
                model=Insight9Model.PRO,
                resolution=(1920, 1080),
                fps=30,
                enable_depth=True,
                enable_ir=True
            ),
            Insight9Model.MAX: Insight9Config(
                model=Insight9Model.MAX,
                resolution=(2560, 1440),
                fps=30,
                enable_depth=True,
                enable_ir=True,
                depth_mode="high"
            ),
            Insight9Model.LIDAR: Insight9Config(
                model=Insight9Model.LIDAR,
                resolution=(1920, 1080),
                fps=30,
                enable_depth=True,
                enable_ir=True,
                enable_lidar=True
            )
        }
        
        default = defaults.get(self.config.model)
        if default:
            # Merge with existing config
            for key, value in default.__dict__.items():
                if getattr(self.config, key) is None or getattr(self.config, key) == getattr(default, key):
                    setattr(self.config, key, value)
    
    def connect(self) -> bool:
        """
        Connect to camera
        
        Returns:
            bool: True if connection successful
        """
        logger.info(f"Connecting to Insight9 {self.config.model.value}")
        
        try:
            # Try to import Insight9 SDK
            # from insight9_sdk import Camera  # Uncomment when available
            
            # Simulation mode for testing
            logger.info("Running in simulation mode")
            self._connected = True
            return True
            
        except ImportError:
            logger.error("Insight9 SDK not found")
            return False
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from camera"""
        if self._streaming:
            self.stop_streaming()
        self._connected = False
        logger.info("Disconnected from Insight9")
    
    def start_streaming(self, callback: Callable[[Insight9Data], None] = None):
        """
        Start streaming data from camera
        
        Args:
            callback: Function to call with each frame
        """
        if not self._connected:
            logger.error("Camera not connected")
            return
        
        self._data_callback = callback
        self._streaming = True
        self._stop_event.clear()
        
        # Start streaming thread
        self._thread = threading.Thread(target=self._streaming_loop)
        self._thread.daemon = True
        self._thread.start()
        
        logger.info("Started streaming")
    
    def stop_streaming(self):
        """Stop streaming"""
        self._streaming = False
        self._stop_event.set()
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        
        logger.info("Stopped streaming")
    
    def _streaming_loop(self):
        """Main streaming loop"""
        while not self._stop_event.is_set():
            try:
                # Get data (real or simulated)
                data = self._read_data()
                
                if data:
                    self._sequence_id += 1
                    data.sequence_id = self._sequence_id
                    
                    # Call callback if registered
                    if self._data_callback:
                        self._data_callback(data)
            
            except Exception as e:
                logger.error(f"Streaming error: {e}")
                break
    
    def _read_data(self) -> Insight9Data:
        """
        Read data from camera
        
        Returns:
            Insight9Data: Camera data
        """
        # Simulation - generate dummy data
        h, w = self.config.resolution[1], self.config.resolution[0]
        
        # RGB image (random noise)
        rgb = np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)
        
        # Depth image (0-5 meters in mm)
        depth = np.random.randint(0, 5000, (h, w), dtype=np.uint16)
        
        data = Insight9Data(
            rgb_image=rgb,
            depth_image=depth,
            timestamp=time.time(),
            intrinsics=self._get_intrinsics(),
            extrinsics=self._get_extrinsics()
        )
        
        if self.config.enable_ir and np.random.random() > 0.9:
            data.ir_image = np.random.randint(0, 256, (h, w), dtype=np.uint8)
        
        if self.config.enable_lidar and np.random.random() > 0.5:
            # Generate dummy lidar points
            n_points = np.random.randint(1000, 5000)
            data.lidar_points = np.random.randn(n_points, 3) * 5.0  # 5m range
        
        return data
    
    def _get_intrinsics(self) -> Dict:
        """Get camera intrinsics"""
        w, h = self.config.resolution
        focal = max(w, h) * 0.8  # Approximate
        
        return {
            'width': w,
            'height': h,
            'fx': focal,
            'fy': focal,
            'cx': w / 2,
            'cy': h / 2,
            'distortion': [0.1, 0.01, 0.001, 0, 0]
        }
    
    def _get_extrinsics(self) -> Dict:
        """Get camera extrinsics (relative to robot)"""
        return {
            'translation': [0, 0, 0],
            'rotation': [0, 0, 0, 1]  # Quaternion
        }
    
    def get_latest_data(self) -> Insight9Data:
        """Get latest data frame"""
        data = self._read_data()
        data.sequence_id = self._sequence_id
        return data
    
    def get_specifications(self) -> Dict:
        """Get camera specifications"""
        return {
            'model': self.config.model.value,
            'resolution': self.config.resolution,
            'fps': self.config.fps,
            'depth_range': self._get_depth_range(),
            'ir_support': self.config.enable_ir,
            'lidar_support': self.config.enable_lidar
        }
    
    def _get_depth_range(self) -> Tuple[float, float]:
        """Get depth sensing range in meters"""
        ranges = {
            Insight9Model.V1: (0.2, 3.0),
            Insight9Model.PRO: (0.1, 10.0),
            Insight9Model.MAX: (0.05, 15.0),
            Insight9Model.LIDAR: (0.05, 50.0)
        }
        return ranges.get(self.config.model, (0.1, 10.0))
    
    def set_depth_mode(self, mode: str):
        """
        Set depth processing mode
        
        Args:
            mode: 'low', 'medium', or 'high'
        """
        self.config.depth_mode = mode
        logger.info(f"Depth mode set to: {mode}")
    
    def set_exposure(self, mode: str, value: int = None):
        """
        Set exposure settings
        
        Args:
            mode: 'auto' or 'manual'
            value: Manual exposure in ms (only for manual mode)
        """
        self.config.exposure_mode = mode
        if value:
            self.config.manual_exposure = value
        logger.info(f"Exposure set to: {mode}")
    
    def set_ir_power(self, power: int):
        """
        Set IR illumination power
        
        Args:
            power: 0-100
        """
        self.config.ir_power = max(0, min(100, power))
        logger.info(f"IR power set to: {self.config.ir_power}%")
    
    def get_status(self) -> Dict:
        """Get camera status"""
        return {
            'connected': self._connected,
            'streaming': self._streaming,
            'sequence_id': self._sequence_id,
            'model': self.config.model.value,
            'config': self.config.__dict__.copy()
        }


# Concrete implementations for each model
class Insight9V1(Insight9Base):
    """Insight9 V1 - Entry-level RGB-D camera"""
    
    PLUGIN_NAME = "insight9_v1"
    PLUGIN_VERSION = "1.0.0"
    
    def __init__(self, config: Insight9Config = None):
        if config is None:
            config = Insight9Config(model=Insight9Model.V1)
        super().__init__(config)


class Insight9Pro(Insight9Base):
    """Insight9 Pro - Professional RGB-D camera"""
    
    PLUGIN_NAME = "insight9_pro"
    PLUGIN_VERSION = "1.0.0"
    
    def __init__(self, config: Insight9Config = None):
        if config is None:
            config = Insight9Config(model=Insight9Model.PRO)
        super().__init__(config)


class Insight9Max(Insight9Base):
    """Insight9 Max - Flagship RGB-D camera"""
    
    PLUGIN_NAME = "insight9_max"
    PLUGIN_VERSION = "1.0.0"
    
    def __init__(self, config: Insight9Config = None):
        if config is None:
            config = Insight9Config(model=Insight9Model.MAX)
        super().__init__(config)


class Insight9Lidar(Insight9Base):
    """Insight9 Lidar - RGB-D + Lidar fusion camera"""
    
    PLUGIN_NAME = "insight9_lidar"
    PLUGIN_VERSION = "1.0.0"
    
    def __init__(self, config: Insight9Config = None):
        if config is None:
            config = Insight9Config(model=Insight9Model.LIDAR)
        super().__init__(config)
    
    def get_fusion_data(self) -> Dict:
        """Get RGB-D-Lidar fusion data"""
        data = self.get_latest_data()
        return {
            'rgb': data.rgb_image,
            'depth': data.depth_image,
            'lidar': data.lidar_points,
            'timestamp': data.timestamp,
            'intrinsics': data.intrinsics
        }


class Insight9Manager:
    """
    Manager for multiple Insight9 cameras
    
    Features:
    - Multi-camera synchronization
    - Hardware sync master/slave
    - Unified data access
    """
    
    def __init__(self):
        self._cameras: Dict[str, Insight9Base] = {}
        self._sync_mode = False
        self._master_id: str = None
        
        logger.info("Insight9Manager initialized")
    
    def add_camera(self, camera_id: str, model: Insight9Model, 
                   config: Insight9Config = None) -> bool:
        """
        Add a camera to the manager
        
        Args:
            camera_id: Unique identifier for camera
            model: Camera model
            config: Optional configuration
            
        Returns:
            bool: True if camera added successfully
        """
        if camera_id in self._cameras:
            logger.warning(f"Camera {camera_id} already exists")
            return False
        
        # Create camera based on model
        camera_classes = {
            Insight9Model.V1: Insight9V1,
            Insight9Model.PRO: Insight9Pro,
            Insight9Model.MAX: Insight9Max,
            Insight9Model.LIDAR: Insight9Lidar
        }
        
        camera_class = camera_classes.get(model)
        if not camera_class:
            logger.error(f"Unknown model: {model}")
            return False
        
        camera = camera_class(config)
        self._cameras[camera_id] = camera
        
        logger.info(f"Added camera {camera_id} ({model.value})")
        return True
    
    def remove_camera(self, camera_id: str):
        """Remove a camera from the manager"""
        if camera_id in self._cameras:
            camera = self._cameras[camera_id]
            if camera._streaming:
                camera.stop_streaming()
            camera.disconnect()
            del self._cameras[camera_id]
            logger.info(f"Removed camera {camera_id}")
    
    def connect_all(self) -> bool:
        """Connect all cameras"""
        for camera_id, camera in self._cameras.items():
            if not camera.connect():
                logger.error(f"Failed to connect camera {camera_id}")
                return False
        return True
    
    def disconnect_all(self):
        """Disconnect all cameras"""
        for camera in self._cameras.values():
            camera.disconnect()
    
    def start_all_streaming(self, callback: Callable[[str, Insight9Data], None] = None):
        """
        Start streaming from all cameras
        
        Args:
            callback: Function called with (camera_id, data)
        """
        def wrapped_callback(data: Insight9Data):
            if callback:
                callback(camera_id, data)
        
        for camera_id, camera in self._cameras.items():
            camera.start_streaming(wrapped_callback)
    
    def stop_all_streaming(self):
        """Stop streaming from all cameras"""
        for camera in self._cameras.values():
            camera.stop_streaming()
    
    def get_camera(self, camera_id: str) -> Optional[Insight9Base]:
        """Get a specific camera"""
        return self._cameras.get(camera_id)
    
    def get_all_cameras(self) -> Dict[str, Dict]:
        """Get status of all cameras"""
        return {
            camera_id: camera.get_status()
            for camera_id, camera in self._cameras.items()
        }
    
    def enable_sync(self, master_id: str) -> bool:
        """
        Enable hardware synchronization
        
        Args:
            master_id: ID of master camera
            
        Returns:
            bool: True if sync enabled
        """
        if master_id not in self._cameras:
            logger.error(f"Master camera {master_id} not found")
            return False
        
        self._sync_mode = True
        self._master_id = master_id
        
        # Configure master/slave relationships
        for camera_id, camera in self._cameras.items():
            if camera_id == master_id:
                camera.config.sync_master = True
            else:
                camera.config.sync_master = False
                camera.config.hardware_sync = True
        
        logger.info(f"Hardware sync enabled with master: {master_id}")
        return True
    
    def disable_sync(self):
        """Disable hardware synchronization"""
        self._sync_mode = False
        self._master_id = None
        
        for camera in self._cameras.values():
            camera.config.hardware_sync = False
        
        logger.info("Hardware sync disabled")


# Plugin registration helpers
def create_insight9_driver(model: str) -> Insight9Base:
    """
    Create Insight9 driver by model name
    
    Args:
        model: Model name (v1, pro, max, lidar)
        
    Returns:
        Insight9Base: Camera driver instance
    """
    model_map = {
        'v1': Insight9Model.V1,
        'pro': Insight9Model.PRO,
        'max': Insight9Model.MAX,
        'lidar': Insight9Model.LIDAR
    }
    
    model_enum = model_map.get(model.lower())
    if not model_enum:
        raise ValueError(f"Unknown Insight9 model: {model}")
    
    camera_classes = {
        Insight9Model.V1: Insight9V1,
        Insight9Model.PRO: Insight9Pro,
        Insight9Model.MAX: Insight9Max,
        Insight9Model.LIDAR: Insight9Lidar
    }
    
    return camera_classes[model_enum]()


# Demo usage
if __name__ == "__main__":
    print("=" * 60)
    print("LooperRobotics Insight9 Camera Driver Demo")
    print("=" * 60)
    
    # Create a Pro camera
    print("\nCreating Insight9 Pro camera...")
    camera = create_insight9_driver("pro")
    
    # Connect
    print("Connecting...")
    if camera.connect():
        print("✅ Connected!")
        
        # Get specs
        specs = camera.get_specifications()
        print(f"\nCamera Specifications:")
        for key, value in specs.items():
            print(f"  {key}: {value}")
        
        # Start streaming
        def callback(data):
            print(f"Frame {data.sequence_id}: RGB={data.rgb_image.shape}, Depth={data.depth_image.shape}")
        
        print("\nStarting streaming (3 frames)...")
        camera.start_streaming(callback)
        
        time.sleep(0.2)
        camera.stop_streaming()
        
        camera.disconnect()
        print("\n✅ Demo completed!")
    else:
        print("❌ Connection failed")
    
    print("\nDone!")
