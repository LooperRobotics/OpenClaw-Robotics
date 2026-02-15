#!/usr/bin/env python3
"""
Unitree Robot Controller
Core module for controlling Unitree robots using Python SDK

This module provides the main interface for controlling Unitree robots
with basic movement commands and predefined actions.

Author: OpenClaw Contributors
License: MIT
"""

import time
import logging
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

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


@dataclass
class MovementCommand:
    """Data class for movement commands"""
    movement_type: MovementType
    speed: float = 0.5
    duration: float = 0.0  # 0 means continuous until stop command
    angle: float = 0.0  # for rotation


class UnitreeRobotController:
    """
    Main controller class for Unitree robots
    
    This class provides high-level interfaces for controlling
    Unitree robots including basic movements and predefined actions.
    
    Attributes:
        robot: The robot instance from Unitree SDK
        connected: Connection status
        current_speed: Current movement speed
    """
    
    def __init__(self, robot_type: str = "go1", enable_logging: bool = True):
        """
        Initialize the robot controller
        
        Args:
            robot_type: Type of Unitree robot (go1, a1, aliengo)
            enable_logging: Whether to enable logging
        """
        self.robot_type = robot_type
        self.robot = None
        self.connected = False
        self.current_speed = 0.5
        self.enable_logging = enable_logging
        
        if self.enable_logging:
            logger.info(f"Initializing Unitree {robot_type} controller")
    
    def connect(self) -> bool:
        """
        Establish connection to the robot
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            if self.enable_logging:
                logger.info(f"Connecting to Unitree {self.robot_type}...")
            
            # Import Unitree SDK
            try:
                from unitree_sdk2py import Robot
                from unitree_sdk2py.core.channel import ChannelFactory
                
                # Initialize communication channel
                ChannelFactory.Initialize()
                
                # Create robot instance
                self.robot = Robot()
                
                self.connected = True
                
                if self.enable_logging:
                    logger.info("Robot connected successfully!")
                
                return True
                
            except ImportError:
                if self.enable_logging:
                    logger.warning("Unitree SDK not found. Running in simulation mode.")
                self.connected = True  # Mark as connected in simulation mode
                return True
                
        except Exception as e:
            if self.enable_logging:
                logger.error(f"Failed to connect to robot: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the robot"""
        if self.connected:
            try:
                if self.robot and hasattr(self.robot, 'stop'):
                    self.robot.stop()
                if self.enable_logging:
                    logger.info("Robot disconnected successfully")
            except Exception as e:
                if self.enable_logging:
                    logger.error(f"Error during disconnect: {e}")
            finally:
                self.connected = False
    
    def move_forward(self, speed: float = 0.5, duration: float = 0.0) -> bool:
        """
        Move the robot forward
        
        Args:
            speed: Movement speed (0.0 to 1.0)
            duration: Movement duration in seconds (0 for continuous)
            
        Returns:
            bool: True if command executed successfully
        """
        return self._execute_movement(
            MovementCommand(MovementType.FORWARD, speed, duration)
        )
    
    def move_backward(self, speed: float = 0.5, duration: float = 0.0) -> bool:
        """
        Move the robot backward
        
        Args:
            speed: Movement speed (0.0 to 1.0)
            duration: Movement duration in seconds (0 for continuous)
            
        Returns:
            bool: True if command executed successfully
        """
        return self._execute_movement(
            MovementCommand(MovementType.BACKWARD, speed, duration)
        )
    
    def move_left(self, speed: float = 0.5, duration: float = 0.0) -> bool:
        """
        Move the robot left (lateral movement)
        
        Args:
            speed: Movement speed (0.0 to 1.0)
            duration: Movement duration in seconds (0 for continuous)
            
        Returns:
            bool: True if command executed successfully
        """
        return self._execute_movement(
            MovementCommand(MovementType.LEFT, speed, duration)
        )
    
    def move_right(self, speed: float = 0.5, duration: float = 0.0) -> bool:
        """
        Move the robot right (lateral movement)
        
        Args:
            speed: Movement speed (0.0 to 1.0)
            duration: Movement duration in seconds (0 for continuous)
            
        Returns:
            bool: True if command executed successfully
        """
        return self._execute_movement(
            MovementCommand(MovementType.RIGHT, speed, duration)
        )
    
    def rotate(self, angle: float, speed: float = 0.5) -> bool:
        """
        Rotate the robot by a specified angle
        
        Args:
            angle: Rotation angle in degrees (positive = right, negative = left)
            speed: Rotation speed (0.0 to 1.0)
            
        Returns:
            bool: True if command executed successfully
        """
        movement_type = MovementType.ROTATE_RIGHT if angle > 0 else MovementType.ROTATE_LEFT
        return self._execute_movement(
            MovementCommand(movement_type, speed, angle=abs(angle))
        )
    
    def rotate_left(self, angle: float = 90, speed: float = 0.5) -> bool:
        """
        Rotate the robot left
        
        Args:
            angle: Rotation angle in degrees
            speed: Rotation speed (0.0 to 1.0)
            
        Returns:
            bool: True if command executed successfully
        """
        return self._execute_movement(
            MovementCommand(MovementType.ROTATE_LEFT, speed, angle=angle)
        )
    
    def rotate_right(self, angle: float = 90, speed: float = 0.5) -> bool:
        """
        Rotate the robot right
        
        Args:
            angle: Rotation angle in degrees
            speed: Rotation speed (0.0 to 1.0)
            
        Returns:
            bool: True if command executed successfully
        """
        return self._execute_movement(
            MovementCommand(MovementType.ROTATE_RIGHT, speed, angle=angle)
        )
    
    def stop(self) -> bool:
        """
        Stop all robot movement
        
        Returns:
            bool: True if command executed successfully
        """
        return self._execute_movement(
            MovementCommand(MovementType.STOP)
        )
    
    def execute_movement(self, command: MovementCommand) -> bool:
        """
        Execute a movement command
        
        Args:
            command: MovementCommand instance
            
        Returns:
            bool: True if command executed successfully
        """
        return self._execute_movement(command)
    
    def _execute_movement(self, command: MovementCommand) -> bool:
        """
        Internal method to execute movement commands
        
        Args:
            command: MovementCommand instance
            
        Returns:
            bool: True if command executed successfully
        """
        if not self.connected:
            if self.enable_logging:
                logger.error("Not connected to robot")
            return False
        
        try:
            # Simulation mode
            if not hasattr(self.robot, 'move'):
                self._simulate_movement(command)
                return True
            
            # Real robot mode
            speed = command.speed
            duration = command.duration
            
            # Convert speed and angle based on movement type
            forward, lateral, rotation = self._get_movement_values(command)
            
            # Execute movement
            if hasattr(self.robot, 'move'):
                self.robot.move(forward, lateral, rotation)
            elif hasattr(self.robot, 'set_velocity'):
                self.robot.set_velocity(forward, lateral, rotation)
            
            # Handle duration
            if duration > 0:
                time.sleep(duration)
                if hasattr(self.robot, 'stop'):
                    self.robot.stop()
            
            if self.enable_logging:
                logger.info(f"Executed movement: {command.movement_type.value} "
                          f"(speed={speed}, duration={duration})")
            
            return True
            
        except Exception as e:
            if self.enable_logging:
                logger.error(f"Failed to execute movement: {e}")
            return False
    
    def _get_movement_values(self, command: MovementCommand) -> Tuple[float, float, float]:
        """
        Convert movement command to forward, lateral, rotation values
        
        Args:
            command: MovementCommand instance
            
        Returns:
            Tuple of (forward, lateral, rotation) values
        """
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
        else:  # STOP or unknown
            return 0.0, 0.0, 0.0
    
    def _simulate_movement(self, command: MovementCommand):
        """
        Simulate movement for testing without real robot
        
        Args:
            command: MovementCommand instance
        """
        if self.enable_logging:
            logger.info(f"[SIMULATION] Executing: {command.movement_type.value} "
                      f"(speed={command.speed}, duration={command.duration})")
        
        if command.duration > 0:
            time.sleep(command.duration)
    
    def get_robot_status(self) -> Dict:
        """
        Get current robot status
        
        Returns:
            Dict containing robot status information
        """
        status = {
            'connected': self.connected,
            'robot_type': self.robot_type,
            'current_speed': self.current_speed,
            'timestamp': time.time()
        }
        
        if self.robot and hasattr(self.robot, 'get_status'):
            try:
                status['robot_status'] = self.robot.get_status()
            except:
                pass
        
        return status
    
    def set_speed(self, speed: float):
        """
        Set default movement speed
        
        Args:
            speed: Speed value (0.0 to 1.0)
        """
        self.current_speed = max(0.0, min(1.0, speed))
        if self.enable_logging:
            logger.info(f"Speed set to {self.current_speed}")


class PredefinedActions:
    """
    Class for managing predefined robot actions
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
    
    def register_action(self, name: str, action_func):
        """
        Register a new predefined action
        
        Args:
            name: Action name
            action_func: Function that executes the action
        """
        self.actions[name.lower()] = action_func
        if self.controller.enable_logging:
            logger.info(f"Registered action: {name}")
    
    def execute_action(self, action_name: str, **kwargs) -> bool:
        """
        Execute a predefined action
        
        Args:
            action_name: Name of the action to execute
            **kwargs: Additional parameters for the action
            
        Returns:
            bool: True if action executed successfully
        """
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
        """
        List all available actions
        
        Returns:
            List of action names
        """
        return list(self.actions.keys())
    
    # Default action implementations
    
    def _action_wave(self, duration: float = 2.0):
        """Wave action"""
        self.controller.move_forward(0.3, duration)
    
    def _action_bow(self):
        """Bow action (simulated)"""
        self.controller.move_backward(0.2, 1.0)
        self.controller.stop()
    
    def _action_dance(self):
        """Dance action (random movements)"""
        import random
        movements = [
            (self.controller.move_forward, 0.4, 1.0),
            (self.controller.move_backward, 0.4, 1.0),
            (self.controller.rotate_left, 45),
            (self.controller.rotate_right, 45),
            (self.controller.move_left, 0.3, 1.0),
            (self.controller.move_right, 0.3, 1.0),
        ]
        
        for _ in range(2):
            for movement in movements:
                try:
                    movement[0](movement[1], movement[2])
                except:
                    movement[0](movement[1])
                time.sleep(0.5)
    
    def _action_walk_around(self, duration: float = 10.0):
        """Walk around action"""
        import random
        start_time = time.time()
        
        while time.time() - start_time < duration:
            direction = random.choice(['forward', 'left', 'right'])
            duration_step = min(2.0, duration - (time.time() - start_time))
            
            if direction == 'forward':
                self.controller.move_forward(0.4, duration_step)
            elif direction == 'left':
                self.controller.move_left(0.3, 1.0)
            elif direction == 'right':
                self.controller.move_right(0.3, 1.0)
    
    def _action_circle(self, direction: str = "left", radius: float = 1.0, duration: float = 5.0):
        """Circular movement action"""
        start_time = time.time()
        
        while time.time() - start_time < duration:
            if direction == "left":
                self.controller._execute_movement(
                    MovementCommand(MovementType.FORWARD, 0.3, angle=1.0)
                )
            else:
                self.controller._execute_movement(
                    MovementCommand(MovementType.FORWARD, 0.3, angle=-1.0)
                )
    
    def _action_sit(self):
        """Sit action (simulation)"""
        self.controller.stop()
        if self.controller.enable_logging:
            logger.info("Robot is now sitting (simulation)")
    
    def _action_stand(self):
        """Stand action (simulation)"""
        self.controller.stop()
        if self.controller.enable_logging:
            logger.info("Robot is now standing (simulation)")
