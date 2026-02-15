#!/usr/bin/env python3
"""
Unitree Robot WhatsApp Control - Test Suite
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot_controller import (
    UnitreeRobotController, 
    PredefinedActions, 
    MovementType, 
    MovementCommand
)
from src.whatsapp_handler import (
    WhatsAppMessageHandler, 
    CommandType, 
    ParsedCommand
)


class TestRobotController(unittest.TestCase):
    """Test cases for UnitreeRobotController"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.controller = UnitreeRobotController(robot_type="go1", enable_logging=False)
    
    def test_initialization(self):
        """Test controller initialization"""
        self.assertEqual(self.controller.robot_type, "go1")
        self.assertEqual(self.controller.connected, False)
        self.assertEqual(self.controller.current_speed, 0.5)
    
    def test_movement_command_forward(self):
        """Test forward movement command"""
        command = MovementCommand(MovementType.FORWARD, speed=0.5)
        self.assertEqual(command.movement_type, MovementType.FORWARD)
        self.assertEqual(command.speed, 0.5)
    
    def test_movement_command_rotation(self):
        """Test rotation command"""
        command = MovementCommand(MovementType.ROTATE_RIGHT, speed=0.5, angle=90)
        self.assertEqual(command.movement_type, MovementType.ROTATE_RIGHT)
        self.assertEqual(command.angle, 90)
    
    def test_get_movement_values_forward(self):
        """Test movement value conversion for forward"""
        command = MovementCommand(MovementType.FORWARD, speed=0.5)
        values = self.controller._get_movement_values(command)
        self.assertEqual(values, (0.5, 0.0, 0.0))
    
    def test_get_movement_values_backward(self):
        """Test movement value conversion for backward"""
        command = MovementCommand(MovementType.BACKWARD, speed=0.5)
        values = self.controller._get_movement_values(command)
        self.assertEqual(values, (-0.5, 0.0, 0.0))
    
    def test_get_movement_values_left(self):
        """Test movement value conversion for left"""
        command = MovementCommand(MovementType.LEFT, speed=0.5)
        values = self.controller._get_movement_values(command)
        self.assertEqual(values, (0.0, 0.5, 0.0))
    
    def test_get_movement_values_rotate_right(self):
        """Test movement value conversion for right rotation"""
        command = MovementCommand(MovementType.ROTATE_RIGHT, speed=0.5)
        values = self.controller._get_movement_values(command)
        self.assertEqual(values, (0.0, 0.0, 0.5))
    
    def test_get_movement_values_stop(self):
        """Test movement value conversion for stop"""
        command = MovementCommand(MovementType.STOP)
        values = self.controller._get_movement_values(command)
        self.assertEqual(values, (0.0, 0.0, 0.0))
    
    def test_set_speed(self):
        """Test speed setting"""
        self.controller.set_speed(0.8)
        self.assertEqual(self.controller.current_speed, 0.8)
        
        # Test speed limits
        self.controller.set_speed(1.5)
        self.assertEqual(self.controller.current_speed, 1.0)
        
        self.controller.set_speed(-0.5)
        self.assertEqual(self.controller.current_speed, 0.0)
    
    def test_get_robot_status(self):
        """Test robot status retrieval"""
        status = self.controller.get_robot_status()
        
        self.assertIn('connected', status)
        self.assertIn('robot_type', status)
        self.assertIn('current_speed', status)
        self.assertIn('timestamp', status)
        self.assertEqual(status['robot_type'], 'go1')


class TestPredefinedActions(unittest.TestCase):
    """Test cases for PredefinedActions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.controller = UnitreeRobotController(robot_type="go1", enable_logging=False)
        self.controller.connect()  # Simulation mode
        self.actions = PredefinedActions(self.controller)
    
    def test_default_actions_registered(self):
        """Test that default actions are registered"""
        expected_actions = [
            'wave', 'bow', 'dance', 'walk_around', 
            'circle', 'sit', 'stand'
        ]
        
        for action in expected_actions:
            self.assertIn(action, self.actions.actions)
    
    def test_list_actions(self):
        """Test action listing"""
        action_list = self.actions.list_actions()
        self.assertIsInstance(action_list, list)
        self.assertGreater(len(action_list), 0)
    
    def test_execute_nonexistent_action(self):
        """Test executing non-existent action"""
        result = self.actions.execute_action("nonexistent_action")
        self.assertFalse(result)
    
    def test_register_custom_action(self):
        """Test registering custom action"""
        def custom_action():
            pass
        
        self.actions.register_action("custom", custom_action)
        self.assertIn("custom", self.actions.actions)


class TestWhatsAppMessageHandler(unittest.TestCase):
    """Test cases for WhatsAppMessageHandler"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.controller = UnitreeRobotController(robot_type="go1", enable_logging=False)
        self.controller.connect()
        self.actions = PredefinedActions(self.controller)
        self.handler = WhatsAppMessageHandler(self.controller, self.actions)
    
    def test_parse_forward_command(self):
        """Test parsing forward command"""
        parsed = self.handler.parse_command("forward 0.5")
        self.assertEqual(parsed.command_type, CommandType.MOVE_FORWARD)
        self.assertEqual(parsed.args['speed'], 0.5)
    
    def test_parse_backward_command(self):
        """Test parsing backward command"""
        parsed = self.handler.parse_command("后退 0.8")
        self.assertEqual(parsed.command_type, CommandType.MOVE_BACKWARD)
        self.assertEqual(parsed.args['speed'], 0.8)
    
    def test_parse_rotate_command(self):
        """Test parsing rotate command"""
        parsed = self.handler.parse_command("rotate left 45")
        self.assertEqual(parsed.command_type, CommandType.ROTATE)
        self.assertEqual(parsed.args['direction'], 'left')
        self.assertEqual(parsed.args['angle'], 45)
    
    def test_parse_stop_command(self):
        """Test parsing stop command"""
        parsed = self.handler.parse_command("停止")
        self.assertEqual(parsed.command_type, CommandType.STOP)
    
    def test_parse_status_command(self):
        """Test parsing status command"""
        parsed = self.handler.parse_command("状态")
        self.assertEqual(parsed.command_type, CommandType.STATUS)
    
    def test_parse_help_command(self):
        """Test parsing help command"""
        parsed = self.handler.parse_command("帮助")
        self.assertEqual(parsed.command_type, CommandType.HELP)
    
    def test_parse_unknown_command(self):
        """Test parsing unknown command"""
        parsed = self.handler.parse_command("random text")
        self.assertEqual(parsed.command_type, CommandType.UNKNOWN)
        self.assertFalse(parsed.is_valid)
    
    def test_process_forward_command(self):
        """Test processing forward command"""
        response = self.handler.process_message("forward 0.5", "test_user")
        self.assertIn("forward", response.lower())
        self.assertIn("0.5", response)
    
    def test_process_stop_command(self):
        """Test processing stop command"""
        response = self.handler.process_message("stop", "test_user")
        self.assertIn("stop", response.lower())
    
    def test_process_status_command(self):
        """Test processing status command"""
        response = self.handler.process_message("status", "test_user")
        self.assertIn("Robot Status", response)
    
    def test_process_help_command(self):
        """Test processing help command"""
        response = self.handler.process_message("help", "test_user")
        self.assertIn("Basic Movement", response)
    
    def test_command_history(self):
        """Test command history recording"""
        self.handler.process_message("forward 0.5", "user1")
        self.handler.process_message("stop", "user2")
        
        history = self.handler.get_command_history(10)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['sender'], 'user1')
        self.assertEqual(history[1]['sender'], 'user2')
    
    def test_get_available_commands(self):
        """Test getting available commands"""
        commands = self.handler.get_available_commands()
        self.assertIsInstance(commands, list)
        self.assertGreater(len(commands), 0)


class TestOpenClawInterface(unittest.TestCase):
    """Test cases for OpenClawInterface"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.controller = UnitreeRobotController(robot_type="go1", enable_logging=False)
        self.controller.connect()
        self.actions = PredefinedActions(self.controller)
        self.message_handler = WhatsAppMessageHandler(self.controller, self.actions)
        self.interface = OpenClawRobotInterface(
            self.controller, 
            self.actions, 
            self.message_handler
        )
    
    def test_get_all_tools(self):
        """Test getting all tools"""
        tools = self.interface.get_all_tools()
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)
    
    def test_get_specific_tool(self):
        """Test getting specific tool"""
        tool = self.interface.get_tool("move_forward")
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "move_forward")
    
    def test_get_nonexistent_tool(self):
        """Test getting non-existent tool"""
        tool = self.interface.get_tool("nonexistent_tool")
        self.assertIsNone(tool)
    
    def test_execute_move_forward_tool(self):
        """Test executing move_forward tool"""
        result = self.interface.execute_tool("move_forward", speed=0.5)
        self.assertIn('success', result)
        self.assertIn('action', result)
    
    def test_execute_rotate_tool(self):
        """Test executing rotate tool"""
        result = self.interface.execute_tool("rotate", direction="right", angle=45)
        self.assertIn('success', result)
    
    def test_execute_nonexistent_tool(self):
        """Test executing non-existent tool"""
        result = self.interface.execute_tool("nonexistent_tool")
        self.assertFalse(result['success'])
        self.assertIn('Unknown tool', result['message'])
    
    def test_generate_agent_prompt(self):
        """Test generating agent prompt"""
        prompt = self.interface.generate_agent_prompt()
        self.assertIsInstance(prompt, str)
        self.assertIn('Unitree robot', prompt)
        self.assertIn('Available tools', prompt)


if __name__ == '__main__':
    unittest.main()
