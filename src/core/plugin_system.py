#!/usr/bin/env python3
"""
OpenClaw-Robotics Plugin System
Plugin-based architecture for extensible robot control

This module provides:
- Plugin Registry for automatic discovery
- Base classes for all plugin types
- Plugin lifecycle management
- Configuration management

Author: OpenClaw Contributors
License: MIT
"""

import os
import sys
import json
import logging
import importlib
import inspect
from typing import Dict, List, Optional, Any, Type, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PluginType(Enum):
    """Types of plugins supported"""
    ROBOT = "robot"
    SENSOR = "sensor"
    SLAM = "slam"
    NAVIGATION = "navigation"
    PERCEPTION = "perception"
    UTILITY = "utility"


@dataclass
class PluginMetadata:
    """Metadata for a plugin"""
    name: str
    version: str
    author: str
    description: str
    plugin_type: PluginType
    dependencies: List[str] = field(default_factory=list)
    compatible_robots: List[str] = field(default_factory=list)
    compatible_sensors: List[str] = field(default_factory=list)
    config_schema: Dict = field(default_factory=dict)
    entry_point: str = ""


class PluginBase(ABC):
    """Abstract base class for all plugins"""
    
    # Plugin metadata (to be overridden by subclasses)
    PLUGIN_NAME: str = "base_plugin"
    PLUGIN_VERSION: str = "1.0.0"
    PLUGIN_AUTHOR: str = "OpenClaw Contributors"
    PLUGIN_DESCRIPTION: str = "Base plugin"
    PLUGIN_TYPE: PluginType = PluginType.UTILITY
    
    # Dependencies
    DEPENDENCIES: List[str] = []
    COMPATIBLE_ROBOTS: List[str] = []
    COMPATIBLE_SENSORS: List[str] = []
    
    def __init__(self, config: Dict = None):
        """
        Initialize plugin with configuration
        
        Args:
            config: Plugin configuration dictionary
        """
        self.config = config or {}
        self._is_initialized = False
        self._is_running = False
        self._context: Dict = {}
        
        logger.info(f"Initializing plugin: {self.PLUGIN_NAME} v{self.PLUGIN_VERSION}")
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize plugin resources
        
        Returns:
            bool: True if initialization successful
        """
        pass
    
    @abstractmethod
    def shutdown(self):
        """Release plugin resources"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict:
        """Get plugin status"""
        pass
    
    def start(self) -> bool:
        """Start plugin operations"""
        if self._is_running:
            logger.warning(f"Plugin {self.PLUGIN_NAME} already running")
            return True
        
        self._is_running = True
        logger.info(f"Plugin {self.PLUGIN_NAME} started")
        return True
    
    def stop(self):
        """Stop plugin operations"""
        self._is_running = False
        logger.info(f"Plugin {self.PLUGIN_NAME} stopped")
    
    def set_context(self, key: str, value: Any):
        """Set shared context data"""
        self._context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get shared context data"""
        return self._context.get(key, default)
    
    def check_dependencies(self) -> bool:
        """Check if dependencies are available"""
        for dep in self.DEPENDENCIES:
            try:
                importlib.import_module(dep)
            except ImportError:
                logger.error(f"Missing dependency: {dep}")
                return False
        return True
    
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata"""
        return PluginMetadata(
            name=self.PLUGIN_NAME,
            version=self.PLUGIN_VERSION,
            author=self.PLUGIN_AUTHOR,
            description=self.PLUGIN_DESCRIPTION,
            plugin_type=self.PLUGIN_TYPE,
            dependencies=self.DEPENDENCIES,
            compatible_robots=self.COMPATIBLE_ROBOTS,
            compatible_sensors=self.COMPATIBLE_SENSORS
        )


class PluginRegistry:
    """
    Central registry for all plugins
    
    Features:
    - Automatic plugin discovery
    - Plugin lifecycle management
    - Dependency resolution
    - Conflict detection
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._plugins: Dict[str, PluginBase] = {}
        self._metadata: Dict[str, PluginMetadata] = {}
        self._callbacks: Dict[str, List[Callable]] = {
            'on_init': [],
            'on_start': [],
            'on_stop': [],
            'on_shutdown': []
        }
        self._initialized = True
        
        logger.info("PluginRegistry initialized")
    
    def register(self, plugin: PluginBase) -> bool:
        """
        Register a plugin
        
        Args:
            plugin: Plugin instance
            
        Returns:
            bool: True if registration successful
        """
        name = plugin.PLUGIN_NAME
        version = plugin.PLUGIN_VERSION
        full_name = f"{name}@{version}"
        
        if full_name in self._plugins:
            logger.warning(f"Plugin {full_name} already registered")
            return False
        
        # Check dependencies
        if not plugin.check_dependencies():
            logger.error(f"Plugin {full_name} has unmet dependencies")
            return False
        
        # Register
        self._plugins[full_name] = plugin
        self._metadata[full_name] = plugin.get_metadata()
        
        logger.info(f"Registered plugin: {full_name}")
        return True
    
    def unregister(self, name: str, version: str = None):
        """Unregister a plugin"""
        full_name = f"{name}@{version}" if version else name
        
        if full_name in self._plugins:
            plugin = self._plugins[full_name]
            if plugin._is_running:
                plugin.stop()
            if plugin._is_initialized:
                plugin.shutdown()
            
            del self._plugins[full_name]
            del self._metadata[full_name]
            logger.info(f"Unregistered plugin: {full_name}")
    
    def get(self, name: str, version: str = None) -> Optional[PluginBase]:
        """Get a registered plugin"""
        full_name = f"{name}@{version}" if version else name
        return self._plugins.get(full_name)
    
    def get_metadata(self, name: str, version: str = None) -> Optional[PluginMetadata]:
        """Get plugin metadata"""
        full_name = f"{name}@{version}" if version else name
        return self._metadata.get(full_name)
    
    def list_plugins(self, plugin_type: PluginType = None) -> List[Dict]:
        """List all registered plugins"""
        result = []
        for full_name, metadata in self._metadata.items():
            if plugin_type is None or metadata.plugin_type == plugin_type:
                result.append({
                    'name': metadata.name,
                    'version': metadata.version,
                    'type': metadata.plugin_type.value,
                    'author': metadata.author,
                    'description': metadata.description
                })
        return result
    
    def initialize_all(self) -> bool:
        """Initialize all registered plugins"""
        for full_name, plugin in self._plugins.items():
            try:
                if not plugin._is_initialized:
                    if plugin.initialize():
                        plugin._is_initialized = True
                        logger.info(f"Initialized plugin: {full_name}")
            except Exception as e:
                logger.error(f"Failed to initialize {full_name}: {e}")
                return False
        return True
    
    def start_all(self) -> bool:
        """Start all registered plugins"""
        for full_name, plugin in self._plugins.items():
            try:
                plugin.start()
            except Exception as e:
                logger.error(f"Failed to start {full_name}: {e}")
                return False
        return True
    
    def stop_all(self):
        """Stop all plugins"""
        for full_name, plugin in self._plugins.items():
            try:
                plugin.stop()
            except Exception as e:
                logger.error(f"Error stopping {full_name}: {e}")
    
    def shutdown_all(self):
        """Shutdown all plugins"""
        for full_name, plugin in self._plugins.items():
            try:
                if plugin._is_initialized:
                    plugin.shutdown()
                    plugin._is_initialized = False
            except Exception as e:
                logger.error(f"Error shutting down {full_name}: {e}")
    
    def discover_plugins(self, search_paths: List[str] = None):
        """
        Auto-discover plugins in specified paths
        
        Args:
            search_paths: List of paths to search for plugins
        """
        if search_paths is None:
            search_paths = [
                os.path.join(os.getcwd(), 'plugins'),
                os.path.join(os.path.dirname(__file__), 'plugins'),
                '/usr/share/openclaw/plugins',
                os.path.expanduser('~/.openclaw/plugins')
            ]
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
            
            logger.info(f"Searching for plugins in: {search_path}")
            
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.endswith('.py') and file.startswith('plugin_'):
                        plugin_file = os.path.join(root, file)
                        self._load_plugin_file(plugin_file)
    
    def _load_plugin_file(self, plugin_file: str):
        """Load a plugin from file"""
        try:
            # Add to path
            module_dir = os.path.dirname(plugin_file)
            module_name = os.path.splitext(os.path.basename(plugin_file))[0]
            
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
            
            # Import module
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find and register plugins
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, PluginBase) and obj != PluginBase:
                    if hasattr(obj, 'PLUGIN_NAME'):
                        plugin = obj()
                        self.register(plugin)
                        logger.info(f"Auto-discovered plugin: {obj.PLUGIN_NAME}")
            
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_file}: {e}")
    
    def on_init(self, callback: Callable):
        """Register init callback"""
        self._callbacks['on_init'].append(callback)
    
    def on_start(self, callback: Callable):
        """Register start callback"""
        self._callbacks['on_start'].append(callback)
    
    def on_stop(self, callback: Callable):
        """Register stop callback"""
        self._callbacks['on_stop'].append(callback)
    
    def on_shutdown(self, callback: Callable):
        """Register shutdown callback"""
        self._callbacks['on_shutdown'].append(callback)


class PluginConfigManager:
    """Manage plugin configurations"""
    
    def __init__(self, config_dir: str = None):
        """
        Initialize configuration manager
        
        Args:
            config_dir: Directory for config files
        """
        self.config_dir = config_dir or os.path.join(os.getcwd(), 'configs')
        self._configs: Dict[str, Dict] = {}
        self._config_cache: Dict[str, Any] = {}
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        logger.info(f"Config manager initialized: {self.config_dir}")
    
    def load_config(self, plugin_name: str, config_file: str = None) -> Dict:
        """
        Load configuration for a plugin
        
        Args:
            plugin_name: Name of the plugin
            config_file: Path to config file (optional)
            
        Returns:
            Dict: Configuration dictionary
        """
        if config_file is None:
            config_file = os.path.join(self.config_dir, f"{plugin_name}.json")
        
        # Check cache
        if config_file in self._config_cache:
            return self._config_cache[config_file]
        
        # Load from file
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self._config_cache[config_file] = config
                    logger.info(f"Loaded config for {plugin_name}: {config_file}")
                    return config
            except Exception as e:
                logger.error(f"Error loading config {config_file}: {e}")
        
        # Return default config
        return {}
    
    def save_config(self, plugin_name: str, config: Dict, config_file: str = None):
        """
        Save configuration for a plugin
        
        Args:
            plugin_name: Name of the plugin
            config: Configuration dictionary
            config_file: Path to config file (optional)
        """
        if config_file is None:
            config_file = os.path.join(self.config_dir, f"{plugin_name}.json")
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
                self._config_cache[config_file] = config
                logger.info(f"Saved config for {plugin_name}: {config_file}")
        except Exception as e:
            logger.error(f"Error saving config {config_file}: {e}")
    
    def merge_configs(self, base_config: Dict, override_config: Dict) -> Dict:
        """
        Merge two configurations
        
        Args:
            base_config: Base configuration
            override_config: Override values
            
        Returns:
            Dict: Merged configuration
        """
        result = base_config.copy()
        result.update(override_config)
        return result


# Convenience function for plugin registration
def register_plugin(plugin_class: Type[PluginBase]):
    """Decorator to register a plugin class"""
    registry = PluginRegistry()
    instance = plugin_class()
    registry.register(instance)
    return plugin_class


# Global registry instance
def get_registry() -> PluginRegistry:
    """Get the global plugin registry"""
    return PluginRegistry()


def init_plugins(auto_discover: bool = True) -> PluginRegistry:
    """
    Initialize all plugins
    
    Args:
        auto_discover: Whether to auto-discover plugins
        
    Returns:
        PluginRegistry: Initialized registry
    """
    registry = get_registry()
    
    if auto_discover:
        registry.discover_plugins()
    
    registry.initialize_all()
    registry.start_all()
    
    return registry


def shutdown_plugins():
    """Shutdown all plugins"""
    registry = get_registry()
    registry.stop_all()
    registry.shutdown_all()


# Example plugin implementations
class ExampleRobotPlugin(PluginBase):
    """Example robot plugin"""
    PLUGIN_NAME = "example_robot"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_AUTHOR = "OpenClaw"
    PLUGIN_DESCRIPTION = "Example robot plugin"
    PLUGIN_TYPE = PluginType.ROBOT
    
    def initialize(self) -> bool:
        """Initialize the robot"""
        logger.info("Initializing example robot")
        return True
    
    def shutdown(self):
        """Shutdown the robot"""
        logger.info("Shutting down example robot")
    
    def get_status(self) -> Dict:
        """Get robot status"""
        return {'connected': self._is_initialized}
    
    def move(self, velocity: tuple) -> bool:
        """Move the robot"""
        logger.info(f"Moving robot with velocity: {velocity}")
        return True


class ExampleSensorPlugin(PluginBase):
    """Example sensor plugin"""
    PLUGIN_NAME = "example_sensor"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_AUTHOR = "OpenClaw"
    PLUGIN_DESCRIPTION = "Example sensor plugin"
    PLUGIN_TYPE = PluginType.SENSOR
    
    def initialize(self) -> bool:
        """Initialize the sensor"""
        logger.info("Initializing example sensor")
        return True
    
    def shutdown(self):
        """Shutdown the sensor"""
        logger.info("Shutting down example sensor")
    
    def get_status(self) -> Dict:
        """Get sensor status"""
        return {'ready': self._is_initialized}
    
    def read(self) -> Dict:
        """Read sensor data"""
        return {'value': 0}


# Auto-register example plugins
if __name__ == "__main__":
    # Initialize registry
    registry = get_registry()
    
    # Register example plugins
    registry.register(ExampleRobotPlugin())
    registry.register(ExampleSensorPlugin())
    
    # Initialize and start
    registry.initialize_all()
    registry.start_all()
    
    # List plugins
    print("\nRegistered plugins:")
    for plugin_info in registry.list_plugins():
        print(f"  - {plugin_info['name']} v{plugin_info['version']}")
    
    # Shutdown
    print("\nShutting down...")
    shutdown_plugins()
