#!/usr/bin/env python3
"""
OpenClaw Integration Module
Integrates the robot control system with OpenClaw framework

This module provides OpenClaw-compatible interfaces for controlling
the Unitree robot through OpenClaw agents and tools.

Author: OpenClaw Contributors
License: MIT
"""

import sys
import os
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot_controller import UnitreeRobotController, PredefinedActions
from src.whatsapp_handler import WhatsAppMessageHandler, CommandType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class OpenClawTool:
    """Data class for OpenClaw tool definition"""
    name: str
    description: str
    parameters: Dict[str, Any]
    required_params: List[str]
    function: callable


class OpenClawRobotInterface:
    """
    OpenClaw-compatible interface for Unitree robot control
    
    This class provides a set of tools that can be used by OpenClaw
    agents to control the robot through natural language commands.
    """
    
    def __init__(self, robot_controller: UnitreeRobotController, 
                 predefined_actions: PredefinedActions,
                 message_handler: WhatsAppMessageHandler):
        """
        Initialize OpenClaw interface
        
        Args:
            robot_controller: UnitreeRobotController instance
            predefined_actions: PredefinedActions instance
            message_handler: WhatsAppMessageHandler instance
        """
        self.controller = robot_controller
        self.actions = predefined_actions
        self.message_handler = message_handler
        
        # Define available tools
        self.tools = self._define_tools()
        
        logger.info("OpenClaw Robot Interface initialized")
    
    def _define_tools(self) -> List[OpenClawTool]:
        """Define available OpenClaw tools"""
        return [
            OpenClawTool(
                name="move_forward",
                description="Move the robot forward with specified speed",
                parameters={
                    "speed": {"type": "number", "description": "Movement speed (0.0-1.0)", "default": 0.5}
                },
                required_params=[],
                function=self._tool_move_forward
            ),
            OpenClawTool(
                name="move_backward",
                description="Move the robot backward with specified speed",
                parameters={
                    "speed": {"type": "number", "description": "Movement speed (0.0-1.0)", "default": 0.5}
                },
                required_params=[],
                function=self._tool_move_backward
            ),
            OpenClawTool(
                name="move_left",
                description="Move the robot left (lateral) with specified speed",
                parameters={
                    "speed": {"type": "number", "description": "Movement speed (0.0-1.0)", "default": 0.5}
                },
                required_params=[],
                function=self._tool_move_left
            ),
            OpenClawTool(
                name="move_right",
                description="Move the robot right (lateral) with specified speed",
                parameters={
                    "speed": {"type": "number", "description": "Movement speed (0.0-1.0)", "default": 0.5}
                },
                required_params=[],
                function=self._tool_move_right
            ),
            OpenClawTool(
                name="rotate",
                description="Rotate the robot by specified angle and direction",
                parameters={
                    "direction": {"type": "string", "description": "Direction (left/right)", "default": "right"},
                    "angle": {"type": "integer", "description": "Angle in degrees", "default": 90}
                },
                required_params=[],
                function=self._tool_rotate
            ),
            OpenClawTool(
                name="stop",
                description="Stop all robot movement immediately",
                parameters={},
                required_params=[],
                function=self._tool_stop
            ),
            OpenClawTool(
                name="execute_action",
                description="Execute a predefined robot action",
                parameters={
                    "action_name": {"type": "string", "description": "Name of the action to execute"},
                    "params": {"type": "string", "description": "Optional parameters", "default": ""}
                },
                required_params=["action_name"],
                function=self._tool_execute_action
            ),
            OpenClawTool(
                name="get_status",
                description="Get current robot status and information",
                parameters={},
                required_params=[],
                function=self._tool_get_status
            ),
            OpenClawTool(
                name="list_actions",
                description="List all available predefined actions",
                parameters={},
                required_params=[],
                function=self._tool_list_actions
            ),
            OpenClawTool(
                name="set_speed",
                description="Set the default movement speed",
                parameters={
                    "speed": {"type": "number", "description": "Speed value (0.0-1.0)", "default": 0.5}
                },
                required_params=[],
                function=self._tool_set_speed
            ),
            OpenClawTool(
                name="process_whatsapp_message",
                description="Process a WhatsApp message and generate response",
                parameters={
                    "message": {"type": "string", "description": "The incoming message text"},
                    "sender_id": {"type": "string", "description": "ID of the message sender", "default": "openclaw"}
                },
                required_params=["message"],
                function=self._tool_process_whatsapp
            ),
            OpenClawTool(
                name="get_command_history",
                description="Get recent command history",
                parameters={
                    "limit": {"type": "integer", "description": "Maximum entries to return", "default": 10}
                },
                required_params=[],
                function=self._tool_get_history
            ),
        ]
    
    # Tool implementation methods
    
    def _tool_move_forward(self, speed: float = 0.5) -> Dict:
        """Tool: Move forward"""
        success = self.controller.move_forward(speed)
        return {
            "success": success,
            "message": f"Moving forward at speed {speed}" if success else "Failed to move forward",
            "action": "move_forward",
            "parameters": {"speed": speed}
        }
    
    def _tool_move_backward(self, speed: float = 0.5) -> Dict:
        """Tool: Move backward"""
        success = self.controller.move_backward(speed)
        return {
            "success": success,
            "message": f"Moving backward at speed {speed}" if success else "Failed to move backward",
            "action": "move_backward",
            "parameters": {"speed": speed}
        }
    
    def _tool_move_left(self, speed: float = 0.5) -> Dict:
        """Tool: Move left"""
        success = self.controller.move_left(speed)
        return {
            "success": success,
            "message": f"Moving left at speed {speed}" if success else "Failed to move left",
            "action": "move_left",
            "parameters": {"speed": speed}
        }
    
    def _tool_move_right(self, speed: float = 0.5) -> Dict:
        """Tool: Move right"""
        success = self.controller.move_right(speed)
        return {
            "success": success,
            "message": f"Moving right at speed {speed}" if success else "Failed to move right",
            "action": "move_right",
            "parameters": {"speed": speed}
        }
    
    def _tool_rotate(self, direction: str = "right", angle: int = 90) -> Dict:
        """Tool: Rotate robot"""
        if direction.lower() == "left":
            success = self.controller.rotate_left(angle)
        else:
            success = self.controller.rotate_right(angle)
        
        return {
            "success": success,
            "message": f"Rotating {direction} by {angle}°" if success else "Failed to rotate",
            "action": "rotate",
            "parameters": {"direction": direction, "angle": angle}
        }
    
    def _tool_stop(self) -> Dict:
        """Tool: Stop robot"""
        success = self.controller.stop()
        return {
            "success": success,
            "message": "Robot stopped" if success else "Failed to stop",
            "action": "stop",
            "parameters": {}
        }
    
    def _tool_execute_action(self, action_name: str, params: str = "") -> Dict:
        """Tool: Execute predefined action"""
        # Check if action exists
        if action_name.lower() not in self.actions.actions:
            available = ', '.join(self.actions.list_actions())
            return {
                "success": False,
                "message": f"Unknown action: {action_name}",
                "available_actions": available,
                "action": "execute_action",
                "parameters": {"action_name": action_name}
            }
        
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
        
        success = self.actions.execute_action(action_name, **action_params)
        
        return {
            "success": success,
            "message": f"Executed action: {action_name}" if success else f"Failed to execute: {action_name}",
            "action": "execute_action",
            "parameters": {"action_name": action_name, "params": params}
        }
    
    def _tool_get_status(self) -> Dict:
        """Tool: Get robot status"""
        status = self.controller.get_robot_status()
        return {
            "success": True,
            "message": "Robot status retrieved",
            "status": status,
            "action": "get_status",
            "parameters": {}
        }
    
    def _tool_list_actions(self) -> Dict:
        """Tool: List available actions"""
        actions = self.actions.list_actions()
        return {
            "success": True,
            "message": f"Available actions: {', '.join(actions)}",
            "actions": actions,
            "action": "list_actions",
            "parameters": {}
        }
    
    def _tool_set_speed(self, speed: float = 0.5) -> Dict:
        """Tool: Set default speed"""
        self.controller.set_speed(speed)
        return {
            "success": True,
            "message": f"Speed set to {speed}",
            "action": "set_speed",
            "parameters": {"speed": speed}
        }
    
    def _tool_process_whatsapp(self, message: str, sender_id: str = "openclaw") -> Dict:
        """Tool: Process WhatsApp message"""
        response = self.message_handler.process_message(message, sender_id)
        return {
            "success": True,
            "message": response,
            "action": "process_whatsapp",
            "parameters": {"message": message, "sender_id": sender_id}
        }
    
    def _tool_get_history(self, limit: int = 10) -> Dict:
        """Tool: Get command history"""
        history = self.message_handler.get_command_history(limit)
        return {
            "success": True,
            "message": f"Retrieved {len(history)} history entries",
            "history": history,
            "action": "get_command_history",
            "parameters": {"limit": limit}
        }
    
    # Public methods for agent integration
    
    def get_tool(self, tool_name: str) -> Optional[OpenClawTool]:
        """
        Get a specific tool by name
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            OpenClawTool instance or None
        """
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        return None
    
    def get_all_tools(self) -> List[Dict]:
        """
        Get all available tools as dictionaries
        
        Returns:
            List of tool dictionaries
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
                "required": tool.required_params
            }
            for tool in self.tools
        ]
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict:
        """
        Execute a tool by name
        
        Args:
            tool_name: Name of the tool
            **kwargs: Tool parameters
            
        Returns:
            Dict containing execution result
        """
        tool = self.get_tool(tool_name)
        
        if tool is None:
            return {
                "success": False,
                "message": f"Unknown tool: {tool_name}",
                "available_tools": [t.name for t in self.tools]
            }
        
        # Check required parameters
        missing_params = [p for p in tool.required_params if p not in kwargs]
        if missing_params:
            return {
                "success": False,
                "message": f"Missing required parameters: {missing_params}",
                "required": tool.required_params
            }
        
        try:
            # Call the tool function
            result = tool.function(**kwargs)
            return result
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {
                "success": False,
                "message": f"Error executing {tool_name}: {str(e)}",
                "error": str(e)
            }
    
    def generate_agent_prompt(self) -> str:
        """
        Generate a system prompt for OpenClaw agent
        
        Returns:
            str: Agent system prompt
        """
        tools_list = '\n'.join([
            f"- **{tool.name}**: {tool.description}"
            for tool in self.tools
        ])
        
        return f"""You are a helpful assistant for controlling a Unitree robot through WhatsApp.
Your role is to:
1. Parse user messages and extract robot commands
2. Execute appropriate robot actions using the available tools
3. Provide clear feedback to users about command results

Available tools:
{tools_list}

Best practices:
- Always confirm actions before execution when possible
- Provide clear, concise feedback about what the robot is doing
- Help users understand what commands are available
- Handle errors gracefully and suggest alternatives

Remember: Safety first! Ensure the robot is in a safe environment before executing commands."""
