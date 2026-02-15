#!/usr/bin/env python3
"""
Example: OpenClaw Integration Demo
Demonstrates how to integrate with OpenClaw framework

Usage:
    python3 examples/openclaw_demo.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot_controller import UnitreeRobotController, PredefinedActions
from src.whatsapp_handler import WhatsAppMessageHandler
from src.openclaw_interface import OpenClawRobotInterface


def main():
    print("=" * 60)
    print("Unitree Robot - OpenClaw Integration Demo")
    print("=" * 60)
    
    # Create components
    controller = UnitreeRobotController(robot_type="go1")
    controller.connect()
    
    actions = PredefinedActions(controller)
    message_handler = WhatsAppMessageHandler(controller, actions)
    
    # Create OpenClaw interface
    interface = OpenClawRobotInterface(
        controller=controller,
        predefined_actions=actions,
        message_handler=message_handler
    )
    
    # Show available tools
    print("\n[1] Available OpenClaw Tools:")
    print("-" * 60)
    tools = interface.get_all_tools()
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool['name']}")
        print(f"     {tool['description']}")
    
    # Demo tool execution
    print("\n[2] Testing Tool Execution:")
    print("-" * 60)
    
    # Test basic movements
    test_cases = [
        {
            "name": "Move Forward",
            "tool": "move_forward",
            "params": {"speed": 0.5}
        },
        {
            "name": "Rotate Right",
            "tool": "rotate",
            "params": {"direction": "right", "angle": 45}
        },
        {
            "name": "Execute Wave Action",
            "tool": "execute_action",
            "params": {"action_name": "wave"}
        },
        {
            "name": "Get Status",
            "tool": "get_status",
            "params": {}
        },
        {
            "name": "List Actions",
            "tool": "list_actions",
            "params": {}
        }
    ]
    
    for test in test_cases:
        print(f"\n→ Testing: {test['name']}")
        result = interface.execute_tool(test['tool'], **test['params'])
        print(f"Success: {result.get('success', False)}")
        print(f"Message: {result.get('message', 'N/A')}")
        print("-" * 40)
        input("Press Enter to continue...")
    
    # Show agent prompt
    print("\n[3] OpenClaw Agent Prompt:")
    print("-" * 60)
    prompt = interface.generate_agent_prompt()
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
    
    print("\n✅ OpenClaw integration demo completed!")
    controller.disconnect()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
