#!/usr/bin/env python3
"""
Unitree Robot Controller
Core module for controlling Unitree robots using Python SDK

This module provides the main interface for controlling Unitree robots
with basic movement commands and predefined actions.

Supported Models:
- GO1: Consumer quadruped robot
- GO2: Professional quadruped robot  
- G1: Humanoid robot

Author: OpenClaw Contributors
License: MIT
"""

import time
import logging
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MovementType(Enum):
    """Enum for different movement types"""
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"
    ROTATE_LEFT = "rotate_left"
    ROTATE_RIGHT = "rotate_right"
    STOP = "stop"
    JUMP = "jump"  # For G1 humanoid
    WALK = "walk"  # For bipedal walking (G1/H1)


@dataclass
class MovementCommand:
    """Data class for movement commands"""
    movement_type: MovementType
    speed: float = 0.5
    duration: float = 0.0  # 0 means continuous until stop command
    angle: float = 0.0  # for rotation


@dataclass
class RobotCapabilities:
    """Data class for robot capabilities"""
    supports_jump: bool = False
    supports_bipedal_walk: bool = False
    max_speed: float = 1.0
    max_rotation_speed: float = 1.0
    has_arm: bool = False  # For manipulation tasks
    has_gripper: bool = False
    battery_capacity: float = 0.0  # Wh
    weight: float = 0.0  # kg


class RobotDriver(ABC):
    """Abstract base class for robot drivers"""
    
    def __init__(self, robot_type: str, capabilities: RobotCapabilities):
        self.robot_type = robot_type
        self.capabilities = capabilities
        self.robot = None
        self.connected = False
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the robot"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Disconnect from the robot"""
        pass
    
    @abstractmethod
    def move(self, forward: float, lateral: float, rotation: float) -> bool:
        """Execute movement command"""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """Stop all movement"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get robot status"""
        pass
    
    @abstractmethod
    def execute_action(self, action_name: str, **kwargs) -> bool:
        """Execute predefined action"""
        pass


class GO1Driver(RobotDriver):
    """Driver for Unitree GO1 quadruped robot"""
    
    def __init__(self):
        capabilities = RobotCapabilities(
            supports_jump=False,
            supports_bipedal_walk=False,
            max_speed=1.0,
            max_rotation_speed=1.0,
            has_arm=False,
            has_gripper=False,
            battery_capacity=15000,  # 15Wh
            weight=12.0  # kg
        )
        super().__init__("GO1", capabilities)
    
    def connect(self) -> bool:
        """Connect to GO1 robot"""
        try:
            from unitree_sdk2py import Robot
            from unitree_sdk2py.core.channel import ChannelFactory
            
            ChannelFactory.Initialize()
            self.robot = Robot()
            self.connected = True
            
            logger.info("GO1 connected successfully")
            return True
        except ImportError:
            logger.warning("Unitree SDK not found. Running in simulation mode.")
            self.connected = True  # Simulation mode
            return True
        except Exception as e:
            logger.error(f"Failed to connect to GO1: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from GO1"""
        if self.robot:
            try:
                self.robot.stop()
            except:
                pass
        self.connected = False
        logger.info("GO1 disconnected")
    
    def move(self, forward: float, lateral: float, rotation: float) -> bool:
        """Execute movement on GO1"""
        if not self.connected:
            logger.error("GO1 not connected")
            return False
        
        try:
            if hasattr(self.robot, 'move'):
                self.robot.move(forward, lateral, rotation)
            logger.debug(f"GO1 move: f={forward}, l={lateral}, r={rotation}")
            return True
        except Exception as e:
            logger.error(f"GO1 move failed: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop GO1"""
        try:
            if self.robot and hasattr(self.robot, 'stop'):
                self.robot.stop()
            logger.info("GO1 stopped")
            return True
        except Exception as e:
            logger.error(f"GO1 stop failed: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get GO1 status"""
        return {
            'robot_type': self.robot_type,
            'connected': self.connected,
            'capabilities': {
                'supports_jump': self.capabilities.supports_jump,
                'supports_bipedal_walk': self.capabilities.supports_bipedal_walk,
                'max_speed': self.capabilities.max_speed,
                'has_arm': self.capabilities.has_arm
            }
        }
    
    def execute_action(self, action_name: str, **kwargs) -> bool:
        """Execute predefined action on GO1"""
        # GO1 actions (quadruped specific)
        actions = {
            'wave': self._action_wave,
            'bow': self._action_bow,
            'dance': self._action_dance,
            'walk_around': self._action_walk_around,
            'circle': self._action_circle,
        }
        
        action = actions.get(action_name.lower())
        if action:
            return action(**kwargs)
        return False
    
    def _action_wave(self, duration: float = 2.0):
        """Wave gesture"""
        self.move(0.3, 0, 0)
        time.sleep(duration)
        self.stop()
        return True
    
    def _action_bow(self):
        """Bow gesture"""
        self.move(-0.2, 0, 0)
        time.sleep(1.0)
        self.stop()
        return True
    
    def _action_dance(self):
        """Dance routine"""
        import random
        for _ in range(4):
            directions = [(0.4, 0, 0), (-0.4, 0, 0), (0, 0.3, 0), (0, -0.3, 0)]
            for f, l, r in directions:
                self.move(f, l, r)
                time.sleep(0.5)
        self.stop()
        return True
    
    def _action_walk_around(self, duration: float = 10.0):
        """Walk around the area"""
        import random
        start = time.time()
        while time.time() - start < duration:
            f = 0.4 if random.random() > 0.3 else -0.2
            l = 0.3 if random.random() > 0.5 else -0.3
            self.move(f, l, 0)
            time.sleep(2.0)
        self.stop()
        return True
    
    def _action_circle(self, direction: str = "left", duration: float = 5.0):
        """Circular movement"""
        start = time.time()
        rotation = 0.3 if direction.lower() == "left" else -0.3
        while time.time() - start < duration:
            self.move(0.3, 0, rotation)
        self.stop()
        return True


class GO2Driver(GO1Driver):
    """Driver for Unitree GO2 quadruped robot
    
    GO2 is the professional version of GO1 with improved
    performance and additional features.
    """
    
    def __init__(self):
        super().__init__()
        self.robot_type = "GO2"
        # GO2 has slightly improved specs
        self.capabilities.max_speed = 1.2  # Faster
        self.capabilities.battery_capacity = 18000  # 18Wh
        self.capabilities.weight = 15.0  # kg
    
    def move(self, forward: float, lateral: float, rotation: float) -> bool:
        """Execute movement on GO2 with improved control"""
        # GO2 has better dynamic performance
        # Apply slight speed boost factor
        if abs(forward) > 0.1:
            forward *= 1.1  # GO2 can move slightly faster
        return super().move(forward, lateral, rotation)
    
    def execute_action(self, action_name: str, **kwargs) -> bool:
        """Execute predefined action on GO2 with enhanced movements"""
        # Add GO2-specific actions
        enhanced_actions = {
            'run': self._action_run,
            'jump': self._action_jump,
            'stretch': self._action_stretch,
        }
        
        # First try enhanced actions
        if action_name.lower() in enhanced_actions:
            return enhanced_actions[action_name.lower()](**kwargs)
        
        # Fall back to GO1 actions
        return super().execute_action(action_name, **kwargs)
    
    def _action_run(self, duration: float = 3.0):
        """Running gait (GO2 specific)"""
        start = time.time()
        while time.time() - start < duration:
            self.move(0.8, 0, 0)  # Higher speed for running
            time.sleep(0.5)
        self.stop()
        return True
    
    def _action_jump(self, height: float = 0.1):
        """Jump action (GO2 enhanced)"""
        if not self.capabilities.supports_jump:
            logger.warning("Jump not supported, using move instead")
            self.move(0.5, 0, 0)
            time.sleep(0.3)
            self.stop()
            return True
        return True
    
    def _action_stretch(self):
        """Stretch body (GO2 specific)"""
        # Simulated stretch movement
        self.move(0, 0.3, 0)
        time.sleep(0.5)
        self.move(0, -0.3, 0)
        time.sleep(0.5)
        self.stop()
        return True


class G1Driver(RobotDriver):
    """Driver for Unitree G1 humanoid robot
    
    G1 is a humanoid robot with bipedal locomotion
    and arm manipulation capabilities.
    """
    
    def __init__(self):
        capabilities = RobotCapabilities(
            supports_jump=True,
            supports_bipedal_walk=True,
            max_speed=0.8,  # Slower for bipedal
            max_rotation_speed=0.6,
            has_arm=True,
            has_gripper=False,  # Depends on configuration
            battery_capacity=  # 20Wh
            weight=35.0  # kg
        )
        super().__init__("G1", capabilities)
    
    def connect(self) -> bool:
        """Connect to G1 robot"""
        try:
            from unitree_sdk2py import Robot
            from unitree_sdk2py.core.channel import ChannelFactory
            
            ChannelFactory.Initialize()
            # G1 uses a different robot class
            try:
                self.robot = Robot("G1")
            except:
                self.robot = Robot()  # Fallback
            
            self.connected = True
            logger.info("G1 connected successfully")
            return True
        except ImportError:
            logger.warning("Unitree SDK not found. Running in simulation mode.")
            self.connected = True
            return True
        except Exception as e:
            logger.error(f"Failed to connect to G1: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from G1"""
        if self.robot:
            try:
                self.robot.stop()
            except:
                pass
        self.connected = False
        logger.info("G1 disconnected")
    
    def move(self, forward: float, lateral: float, rotation: float) -> bool:
        """Execute movement on G1
        
        G1 uses bipedal locomotion, so lateral movement
        is different from quadrupeds.
        """
        if not self.connected:
            logger.error("G1 not connected")
            return False
        
        try:
            if hasattr(self.robot, 'move'):
                # G1: forward/backward with slight side step
                self.robot.move(forward, lateral * 0.5, rotation)
            elif hasattr(self.robot, 'set_velocity'):
                self.robot.set_velocity(forward, lateral * 0.5, rotation)
            
            logger.debug(f"G1 move: f={forward}, l={lateral}, r={rotation}")
            return True
        except Exception as e:
            logger.error(f"G1 move failed: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop G1 with stable bipedal stance"""
        try:
            if self.robot and hasattr(self.robot, 'stop'):
                self.robot.stop()
            logger.info("G1 stopped")
            return True
        except Exception as e:
            logger.error(f"G1 stop failed: {e}")
            return False
    
    def execute_action(self, action_name: str, **kwargs) -> bool:
        """Execute humanoid-specific actions on G1"""
        human_actions = {
            'wave': self._action_wave,
            'bow': self._action_bow,
            'stretch': self._action_stretch,
            'sit': self._action_sit,
            'stand': self._action_stand,
            'walk': self._action_bipedal_walk,
            'turn_around': self._action_turn_around,
            'squat': self._action_squat,
        }
        
        action = human_actions.get(action_name.lower())
        if action:
            return action(**kwargs)
        return False
    
    def _action_wave(self, duration: float = 2.0):
        """Wave with arm"""
        # G1 can wave its arm
        self.move(0, 0, 0.3)
        time.sleep(0.5)
        self.stop()
        time.sleep(duration)
        return True
    
    def _action_bow(self):
        """Bow gesture (humanoid style)"""
        self.move(-0.1, 0, 0)
        time.sleep(0.5)
        self.stop()
        return True
    
    def _action_stretch(self):
        """Stretch body"""
        # Arm stretch simulation
        self.move(0, 0.2, 0)
        time.sleep(0.3)
        self.move(0, -0.2, 0)
        time.sleep(0.3)
        self.stop()
        return True
    
    def _action_sit(self):
        """Sit down"""
        self.stop()
        logger.info("G1 sitting down (simulation)")
        return True
    
    def _action_stand(self):
        """Stand up"""
        self.stop()
        logger.info("G1 standing up (simulation)")
        return True
    
    def _action_bipedal_walk(self, steps: int = 5, speed: float = 0.5):
        """Bipedal walking"""
        for _ in range(steps):
            self.move(speed, 0, 0)
            time.sleep(0.5)
        self.stop()
        return True
    
    def _action_turn_around(self, angle: float = 180):
        """Turn around in place"""
        rotation_speed = 0.3 if angle > 0 else -0.3
        rotations = abs(angle) / 90  # Each rotation ~90 degrees
        
        for _ in range(int(rotations)):
            self.move(0, 0, rotation_speed)
            time.sleep(0.5)
        self.stop()
        return True
    
    def _action_squat(self, duration: float = 2.0):
        """Squat movement"""
        self.move(-0.1, 0, 0)
        time.sleep(duration)
        self.move(0.1, 0, 0)
        self.stop()
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get G1 status with humanoid-specific info"""
        status = super().get_status()
        status['humanoid_specific'] = {
            'battery_capacity_wh': self.capabilities.battery_capacity,
            'has_arm': self.capabilities.has_arm,
            'has_gripper': self.capabilities.has_gripper,
            'weight_kg': self.capabilities.weight
        }
        return status


class UnitreeRobotController:
    """
    Main controller class for Unitree robots
    
    This class provides unified interfaces for controlling
    Unitree robots including basic movements and predefined actions.
    
    Supported Models:
        - GO1: Consumer quadruped robot
        - GO2: Professional quadruped robot
        - G1: Humanoid robot
    
    Attributes:
        robot: The robot instance
        connected: Connection status
        current_speed: Current movement speed
        robot_type: Type of robot being controlled
    """
    
    # Mapping from robot type to driver class
    ROBOT_DRIVERS = {
        "go1": GO1Driver,
        "go2": GO2Driver,
        "g1": G1Driver,
        # "b2": B2Driver,  # TODO: Implement
        # "h1": H1Driver,  # TODO: Implement
    }
    
    def __init__(self, robot_type: str = "go1", enable_logging: bool = True):
        """
        Initialize the robot controller
        
        Args:
            robot_type: Type of Unitree robot (go1, go2, g1)
            enable_logging: Whether to enable logging
        """
        self.robot_type = robot_type.lower()
        self.enable_logging = enable_logging
        
        # Get the appropriate driver
        if self.robot_type not in self.ROBOT_DRIVERS:
            raise ValueError(
                f"Unsupported robot type: {robot_type}. "
                f"Supported types: {list(self.ROBOT_DRIVERS.keys())}"
            )
        
        driver_class = self.ROBOT_DRIVERS[self.robot_type]
        self.driver = driver_class()
        
        # Delegate attributes
        self.robot = self.driver.robot
        self.connected = self.driver.connected
        self.current_speed = 0.5
        
        if self.enable_logging:
            logger.info(f"Initialized {self.robot_type.upper()} controller")
    
    def connect(self) -> bool:
        """
        Establish connection to the robot
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        if self.enable_logging:
            logger.info(f"Connecting to {self.robot_type.upper()}...")
        
        self.connected = self.driver.connect()
        self.robot = self.driver.robot
        
        return self.connected
    
    def disconnect(self):
        """Disconnect from the robot"""
        self.driver.disconnect()
        self.connected = False
    
    def move_forward(self, speed: float = 0.5, duration: float = 0.0) -> bool:
        """Move the robot forward"""
        return self._execute_movement(
            MovementCommand(MovementType.FORWARD, speed, duration)
        )
    
    def move_backward(self, speed: float = 0.5, duration: float = 0.0) -> bool:
        """Move the robot backward"""
        return self._execute_movement(
            MovementCommand(MovementType.BACKWARD, speed, duration)
        )
    
    def move_left(self, speed: float = 0.5, duration: float = 0.0) -> bool:
        """Move the robot left"""
        return self._execute_movement(
            MovementCommand(MovementType.LEFT, speed, duration)
        )
    
    def move_right(self, speed: float = 0.5, duration: float = 0.0) -> bool:
        """Move the robot right"""
        return self._execute_movement(
            MovementCommand(MovementType.RIGHT, speed, duration)
        )
    
    def rotate_left(self, angle: float = 90, speed: float = 0.5) -> bool:
        """Rotate the robot left"""
        return self._execute_movement(
            MovementCommand(MovementType.ROTATE_LEFT, speed, angle=angle)
        )
    
    def rotate_right(self, angle: float = 90, speed: float = 0.5) -> bool:
        """Rotate the robot right"""
        return self._execute_movement(
            MovementCommand(MovementType.ROTATE_RIGHT, speed, angle=angle)
        )
    
    def stop(self) -> bool:
        """Stop all robot movement"""
        return self.driver.stop()
    
    def _execute_movement(self, command: MovementCommand) -> bool:
        """Internal method to execute movement"""
        if not self.connected:
            if self.enable_logging:
                logger.error("Not connected to robot")
            return False
        
        # Get movement values
        forward, lateral, rotation = self._get_movement_values(command)
        
        # Execute
        success = self.driver.move(forward, lateral, rotation)
        
        # Handle duration
        if success and command.duration > 0:
            time.sleep(command.duration)
            self.driver.stop()
        
        if self.enable_logging and success:
            logger.info(f"Executed: {command.movement_type.value} "
                       f"(speed={command.speed})")
        
        return success
    
    def _get_movement_values(self, command: MovementCommand) -> Tuple[float, float, float]:
        """Convert movement command to forward, lateral, rotation values"""
        speed = command.speed
        
        if command.movement_type == MovementType.FORWARD:
            return speed, 0.0, 0.0
        elif command.movement_type == MovementType.BACKWARD:
            return -speed, 0.0, 0.0
        elif command.movement_type == MovementType.LEFT:
            return 0.0, speed, 0.0
        elif command.movement_type == MovementType.RIGHT:
            return 0.0, -speed, 0.0
        elif command.movement_type == MovementType.ROTATE_RIGHT:
            return 0.0, 0.0, speed
        elif command.movement_type == MovementType.ROTATE_LEFT:
            return 0.0, 0.0, -speed
        else:
            return 0.0, 0.0, 0.0
    
    def execute_action(self, action_name: str, **kwargs) -> bool:
        """Execute predefined action"""
        return self.driver.execute_action(action_name, **kwargs)
    
    def get_robot_status(self) -> Dict[str, Any]:
        """Get robot status"""
        return self.driver.get_status()
    
    def set_speed(self, speed: float):
        """Set default movement speed"""
        self.current_speed = max(0.0, min(1.0, speed))
    
    def get_capabilities(self) -> RobotCapabilities:
        """Get robot capabilities"""
        return self.driver.capabilities
    
    def get_supported_robots(self) -> List[str]:
        """Get list of supported robot types"""
        return list(self.ROBOT_DRIVERS.keys())


class PredefinedActions:
    """
    Class for managing predefined robot actions
    
    Actions are delegated to the appropriate driver based on robot type.
    """
    
    def __init__(self, controller: UnitreeRobotController):
        """
        Initialize predefined actions manager
        
        Args:
            controller: UnitreeRobotController instance
        """
        self.controller = controller
        self.actions = {}
        self._register_default_actions()
    
    def _register_default_actions(self):
        """Register default predefined actions"""
        self.register_action("wave", self._action_wave)
        self.register_action("bow", self._action_bow)
        self.register_action("dance", self._action_dance)
        self.register_action("walk_around", self._action_walk_around)
        self.register_action("circle", self._action_circle)
        self.register_action("sit", self._action_sit)
        self.register_action("stand", self._action_stand)
        
        # Humanoid-specific actions (only available on G1)
        if self.controller.robot_type == "g1":
            self.register_action("walk", self._action_walk)
            self.register_action("turn_around", self._action_turn_around)
            self.register_action("squat", self._action_squat)
    
    def register_action(self, name: str, action_func):
        """Register a new predefined action"""
        self.actions[name.lower()] = action_func
        if self.controller.enable_logging:
            logger.info(f"Registered action: {name}")
    
    def execute_action(self, action_name: str, **kwargs) -> bool:
        """Execute a predefined action"""
        action = self.actions.get(action_name.lower())
        
        if action is None:
            if self.controller.enable_logging:
                logger.error(f"Unknown action: {action_name}")
            return False
        
        try:
            if self.controller.enable_logging:
                logger.info(f"Executing action: {action_name}")
            
            action(**kwargs)
            
            if self.controller.enable_logging:
                logger.info(f"Action {action_name} completed")
            
            return True
            
        except Exception as e:
            if self.controller.enable_logging:
                logger.error(f"Failed to execute action {action_name}: {e}")
            return False
    
    def list_actions(self) -> List[str]:
        """List all available actions"""
        return list(self.actions.keys())
    
    # Default action implementations
    
    def _action_wave(self, duration: float = 2.0):
        self.controller.execute_action("wave", duration=duration)
    
    def _action_bow(self):
        self.controller.execute_action("bow")
    
    def _action_dance(self):
        self.controller.execute_action("dance")
    
    def _action_walk_around(self, duration: float = 10.0):
        self.controller.execute_action("walk_around", duration=duration)
    
    def _action_circle(self, direction: str = "left", duration: float = 5.0):
        self.controller.execute_action("circle", direction=direction, duration=duration)
    
    def _action_sit(self):
        self.controller.execute_action("sit")
    
    def _action_stand(self):
        self.controller.execute_action("stand")
    
    def _action_walk(self, steps: int = 5, speed: float = 0.5):
        self.controller.execute_action("walk", steps=steps, speed=speed)
    
    def _action_turn_around(self, angle: float = 180):
        self.controller.execute_action("turn_around", angle=angle)
    
    def _action_squat(self, duration: float = 2.0):
        self.controller.execute_action("squat", duration=duration)
