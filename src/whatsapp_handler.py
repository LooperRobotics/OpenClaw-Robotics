#!/usr/bin/env python3
"""
WhatsApp Message Handler
Handles incoming WhatsApp messages and converts them to robot commands

This module processes WhatsApp messages, parses commands,
and delegates execution to the robot controller.

Author: OpenClaw Contributors
License: MIT
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from src.robot_controller import UnitreeRobotController, PredefinedActions


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CommandType(Enum):
    """Enum for command types"""
    MOVE_FORWARD = "move_forward"
    MOVE_BACKWARD = "move_backward"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    ROTATE = "rotate"
    STOP = "stop"
    ACTION = "action"
    STATUS = "status"
    HELP = "help"
    SPEED = "speed"
    UNKNOWN = "unknown"


@dataclass
class ParsedCommand:
    """Data class for parsed commands"""
    command_type: CommandType
    args: Dict[str, any]
    original_message: str
    is_valid: bool = True
    error_message: str = ""


class WhatsAppMessageHandler:
    """
    Handles incoming WhatsApp messages and converts them to robot commands
    
    This class is responsible for:
    - Parsing incoming messages
    - Extracting commands and parameters
    - Validating commands
    - Executing robot actions
    - Generating responses
    """
    
    # Command patterns (regex)
    COMMAND_PATTERNS = {
        CommandType.MOVE_FORWARD: [
            r'^forward(?:\s+(\d+(?:\.\d+)?))?$',
            r'^前进(?:\s+(\d+(?:\.\d+)?))?$',
            r'^前(?:\s+(\d+(?:\.\d+)?))?$',
            r'^go\s*forward(?:\s+(\d+(?:\.\d+)?))?$',
        ],
        CommandType.MOVE_BACKWARD: [
            r'^backward(?:\s+(\d+(?:\.\d+)?))?$',
            r'^后退(?:\s+(\d+(?:\.\d+)?))?$',
            r'^后(?:\s+(\d+(?:\.\d+)?))?$',
            r'^go\s*backward(?:\s+(\d+(?:\.\d+)?))?$',
        ],
        CommandType.MOVE_LEFT: [
            r'^left(?:\s+(\d+(?:\.\d+)?))?$',
            r'^左(?:\s+(\d+(?:\.\d+)?))?$',
            r'^向左(?:\s+(\d+(?:\.\d+)?))?$',
            r'^go\s*left(?:\s+(\d+(?:\.\d+)?))?$',
        ],
        CommandType.MOVE_RIGHT: [
            r'^right(?:\s+(\d+(?:\.\d+)?))?$',
            r'^右(?:\s+(\d+(?:\.\d+)?))?$',
            r'^向右(?:\s+(\d+(?:\.\d+)?))?$',
            r'^go\s*right(?:\s+(\d+(?:\.\d+)?))?$',
        ],
        CommandType.ROTATE: [
            r'^rotate\s*(left|right)?(?:\s*(\d+))?$',
            r'^旋转(?:\s*(左|右))?(?:\s*(\d+))?$',
            r'^转(?:\s*(左|右))?(?:\s*(\d+))?$',
            r'^turn\s*(left|right)?(?:\s*(\d+))?$',
        ],
        CommandType.STOP: [
            r'^stop$',
            r'^停止$',
            r'^停$',
            r'^halt$',
            r'^stand$',
        ],
        CommandType.ACTION: [
            r'^action\s+(\w+)(?:\s+(.+))?$',
            r'^动作\s+(\w+)(?:\s+(.+))?$',
            r'^执行\s+(\w+)(?:\s+(.+))?$',
        ],
        CommandType.STATUS: [
            r'^status$',
            r'^状态$',
            r'^机器人状态$',
        ],
        CommandType.HELP: [
            r'^help$',
            r'^帮助$',
            r'^使用说明$',
            r'^命令列表$',
        ],
        CommandType.SPEED: [
            r'^speed\s*=\s*(\d+(?:\.\d+)?)$',
            r'^速度\s*=\s*(\d+(?:\.\d+)?)$',
            r'^速度\s+(\d+(?:\.\d+)?)$',
        ],
    }
    
    def __init__(self, controller: UnitreeRobotController, predefined_actions: PredefinedActions):
        """
        Initialize the message handler
        
        Args:
            controller: UnitreeRobotController instance
            predefined_actions: PredefinedActions instance
        """
        self.controller = controller
        self.predefined_actions = predefined_actions
        self.command_history: List[Dict] = []
        self.max_history = 100
        
        logger.info("WhatsApp Message Handler initialized")
    
    def process_message(self, message: str, sender_id: str = "unknown") -> str:
        """
        Process an incoming WhatsApp message
        
        Args:
            message: The incoming message text
            sender_id: ID of the message sender
            
        Returns:
            str: Response message to send back
        """
        # Clean the message
        clean_message = message.strip()
        
        # Log incoming message
        logger.info(f"Received message from {sender_id}: {clean_message}")
        
        # Parse the command
        parsed = self.parse_command(clean_message)
        
        # Store in history
        self._add_to_history(sender_id, clean_message, parsed)
        
        # Execute command and generate response
        if parsed.is_valid:
            response = self._execute_command(parsed)
        else:
            response = self._generate_error_response(parsed)
        
        return response
    
    def parse_command(self, message: str) -> ParsedCommand:
        """
        Parse a message and extract command information
        
        Args:
            message: The message to parse
            
        Returns:
            ParsedCommand containing command details
        """
        # Try to match each command type
        for command_type, patterns in self.COMMAND_PATTERNS.items():
            for pattern in patterns:
                match = re.match(pattern, message, re.IGNORECASE)
                if match:
                    args = self._extract_args(command_type, match)
                    return ParsedCommand(
                        command_type=command_type,
                        args=args,
                        original_message=message
                    )
        
        # No match found
        return ParsedCommand(
            command_type=CommandType.UNKNOWN,
            args={},
            original_message=message,
            is_valid=False,
            error_message="Unknown command. Send 'help' for available commands."
        )
    
    def _extract_args(self, command_type: CommandType, match) -> Dict:
        """
        Extract arguments from regex match
        
        Args:
            command_type: The type of command
            match: Regex match object
            
        Returns:
            Dict containing extracted arguments
        """
        args = {}
        groups = match.groups()
        
        if command_type in [CommandType.MOVE_FORWARD, CommandType.MOVE_BACKWARD, 
                           CommandType.MOVE_LEFT, CommandType.MOVE_RIGHT]:
            # Extract speed if present
            if groups and groups[0]:
                args['speed'] = min(1.0, max(0.0, float(groups[0])))
            else:
                args['speed'] = 0.5  # Default speed
        
        elif command_type == CommandType.ROTATE:
            # Extract direction and angle
            if groups:
                if groups[0]:
                    direction = groups[0].lower()
                    args['direction'] = direction if direction in ['left', 'right'] else 'right'
                else:
                    args['direction'] = 'right'
                
                if groups[1]:
                    args['angle'] = int(groups[1])
                else:
                    args['angle'] = 90  # Default angle
            else:
                args['direction'] = 'right'
                args['angle'] = 90
        
        elif command_type == CommandType.ACTION:
            # Extract action name and parameters
            if groups:
                if groups[0]:
                    args['action_name'] = groups[0].lower()
                if groups[1]:
                    args['params'] = groups[1]
        
        elif command_type == CommandType.SPEED:
            # Extract speed value
            if groups and groups[0]:
                args['speed'] = min(1.0, max(0.0, float(groups[0])))
        
        return args
    
    def _execute_command(self, parsed: ParsedCommand) -> str:
        """
        Execute a parsed command
        
        Args:
            parsed: ParsedCommand instance
            
        Returns:
            str: Response message
        """
        command_type = parsed.command_type
        args = parsed.args
        
        # Check connection status
        if not self.controller.connected and command_type not in [CommandType.HELP, CommandType.STATUS]:
            return "❌ Robot is not connected! Please check the connection."
        
        # Execute based on command type
        try:
            if command_type == CommandType.MOVE_FORWARD:
                success = self.controller.move_forward(args.get('speed', 0.5))
                return f"✅ Moving forward (speed: {args.get('speed', 0.5)})"
            
            elif command_type == CommandType.MOVE_BACKWARD:
                success = self.controller.move_backward(args.get('speed', 0.5))
                return f"✅ Moving backward (speed: {args.get('speed', 0.5)})"
            
            elif command_type == CommandType.MOVE_LEFT:
                success = self.controller.move_left(args.get('speed', 0.5))
                return f"✅ Moving left (speed: {args.get('speed', 0.5)})"
            
            elif command_type == CommandType.MOVE_RIGHT:
                success = self.controller.move_right(args.get('speed', 0.5))
                return f"✅ Moving right (speed: {args.get('speed', 0.5)})"
            
            elif command_type == CommandType.ROTATE:
                direction = args.get('direction', 'right')
                angle = args.get('angle', 90)
                
                if direction == 'left':
                    success = self.controller.rotate_left(angle)
                else:
                    success = self.controller.rotate_right(angle)
                
                return f"✅ Rotating {direction} by {angle}°"
            
            elif command_type == CommandType.STOP:
                success = self.controller.stop()
                return "🛑 Robot stopped!"
            
            elif command_type == CommandType.ACTION:
                action_name = args.get('action_name', '')
                params = args.get('params', '')
                
                # Check if action exists
                if action_name not in self.predefined_actions.actions:
                    available = ', '.join(self.predefined_actions.list_actions())
                    return f"❌ Unknown action: {action_name}\nAvailable actions: {available}"
                
                # Parse parameters
                action_params = {}
                if params:
                    for param in params.split():
                        if '=' in param:
                            key, value = param.split('=', 1)
                            try:
                                action_params[key] = float(value) if value.replace('.', '', 1).isdigit() else value
                            except:
                                pass
                
                success = self.predefined_actions.execute_action(action_name, **action_params)
                
                if success:
                    return f"✅ Executed action: {action_name}"
                else:
                    return f"❌ Failed to execute action: {action_name}"
            
            elif command_type == CommandType.STATUS:
                status = self.controller.get_robot_status()
                connected = "✅ Connected" if status['connected'] else "❌ Disconnected"
                return (f"🤖 Robot Status\n"
                       f"━━━━━━━━━━━━━━━━━━━━━━\n"
                       f"Status: {connected}\n"
                       f"Type: {status.get('robot_type', 'Unknown')}\n"
                       f"Speed: {status.get('current_speed', 0.5)}\n"
                       f"━━━━━━━━━━━━━━━━━━━━━━")
            
            elif command_type == CommandType.HELP:
                return self._generate_help_message()
            
            elif command_type == CommandType.SPEED:
                speed = args.get('speed', 0.5)
                self.controller.set_speed(speed)
                return f"✅ Speed set to {speed}"
            
            else:
                return "❓ Unknown command. Send 'help' for available commands."
        
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return f"❌ Error: {str(e)}"
    
    def _generate_error_response(self, parsed: ParsedCommand) -> str:
        """
        Generate error response for invalid commands
        
        Args:
            parsed: ParsedCommand with error
            
        Returns:
            str: Error message
        """
        return f"❌ {parsed.error_message}\n\nSend 'help' for available commands."
    
    def _generate_help_message(self) -> str:
        """
        Generate help message with all available commands
        
        Returns:
            str: Help message
        """
        actions = ', '.join(self.predefined_actions.list_actions())
        
        return (f"🤖 Unitree Robot Control - Help\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📍 **Basic Movement**\n"
                f"• forward [0.1-1.0] / 前 / 前进 - Move forward\n"
                f"• backward [0.1-1.0] / 后 / 后退 - Move backward\n"
                f"• left [0.1-1.0] / 左 - Move left\n"
                f"• right [0.1-1.0] / 右 - Move right\n"
                f"• rotate [left|right] [angle] / 旋转 - Rotate\n"
                f"• stop / 停止 - Stop all movement\n\n"
                f"🎯 **Predefined Actions**\n"
                f"• action <name> [params] / 动作 <名称> - Execute predefined action\n"
                f"Available actions: {actions}\n\n"
                f"⚙️ **Settings**\n"
                f"• speed = 0.1-1.0 / 速度 - Set default speed\n"
                f"• status / 状态 - Check robot status\n\n"
                f"ℹ️ **Tips**\n"
                f"• Add number after command for speed (e.g., 'forward 0.8')\n"
                f"• Use Chinese or English commands\n"
                f"• Example: 'forward 0.5' or '前进 0.5'\n"
                f"━━━━━━━━━━━━━━━━━━━━━━")
    
    def _add_to_history(self, sender_id: str, message: str, parsed: ParsedCommand):
        """
        Add command to history
        
        Args:
            sender_id: ID of the sender
            message: Original message
            parsed: ParsedCommand result
        """
        self.command_history.append({
            'sender': sender_id,
            'message': message,
            'command': parsed.command_type.value,
            'success': parsed.is_valid,
            'timestamp': __import__('time').time()
        })
        
        # Trim history if needed
        if len(self.command_history) > self.max_history:
            self.command_history = self.command_history[-self.max_history:]
    
    def get_command_history(self, limit: int = 10) -> List[Dict]:
        """
        Get command history
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of command history entries
        """
        return self.command_history[-limit:]
    
    def get_available_commands(self) -> List[str]:
        """
        Get list of all available commands
        
        Returns:
            List of command descriptions
        """
        return [
            "forward [speed] - Move forward",
            "backward [speed] - Move backward", 
            "left [speed] - Move left",
            "right [speed] - Move right",
            "rotate [left|right] [angle] - Rotate robot",
            "stop - Stop all movement",
            "action <name> [params] - Execute predefined action",
            "speed = <value> - Set speed",
            "status - Check robot status",
            "help - Show help message",
        ]
