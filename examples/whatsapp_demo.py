#!/usr/bin/env python3
"""
Example: WhatsApp Message Handler Demo
Demonstrates how to use the WhatsApp message handler

Usage:
    python3 examples/whatsapp_demo.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot_controller import UnitreeRobotController, PredefinedActions
from src.whatsapp_handler import WhatsAppMessageHandler


def main():
    print("=" * 60)
    print("Unitree Robot - WhatsApp Message Handler Demo")
    print("=" * 60)
    
    # Create controller
    controller = UnitreeRobotController(robot_type="go1")
    controller.connect()
    
    # Create predefined actions
    actions = PredefinedActions(controller)
    
    # Create message handler
    handler = WhatsAppMessageHandler(controller, actions)
    
    # Show available commands
    print("\n[1] Available Commands:")
    print("-" * 60)
    commands = handler.get_available_commands()
    for cmd in commands:
        print(f"  • {cmd}")
    
    # Demo message processing
    print("\n[2] Testing Message Processing:")
    print("-" * 60)
    
    test_messages = [
        "forward 0.5",
        "rotate right 90",
        "action wave",
        "status",
        "help",
        "stop"
    ]
    
    for message in test_messages:
        print(f"\n📱 Incoming: '{message}'")
        response = handler.process_message(message, "demo_user")
        print(f"🤖 Response: {response}")
        print("-" * 40)
        input("Press Enter to continue...")
    
    print("\n✅ WhatsApp demo completed!")
    controller.disconnect()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
