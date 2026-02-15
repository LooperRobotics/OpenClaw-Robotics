#!/usr/bin/env python3
"""
Example: Predefined Actions Demo
Demonstrates predefined robot actions

Usage:
    python3 examples/predefined_actions.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot_controller import UnitreeRobotController, PredefinedActions


def main():
    print("=" * 60)
    print("Unitree Robot - Predefined Actions Demo")
    print("=" * 60)
    
    # Create controller
    controller = UnitreeRobotController(robot_type="go1")
    controller.connect()
    
    # Create predefined actions manager
    actions = PredefinedActions(controller)
    
    # Show available actions
    print("\n[1] Available Predefined Actions:")
    print("-" * 60)
    available_actions = actions.list_actions()
    for i, action in enumerate(available_actions, 1):
        print(f"  {i}. {action}")
    
    # Demo each action
    print("\n[2] Running actions demo...")
    print("-" * 60)
    
    action_list = [
        ("wave", "Waving gesture"),
        ("bow", "Bow gesture"),
        ("sit", "Sit down"),
        ("stand", "Stand up"),
    ]
    
    for action_name, description in action_list:
        if action_name in actions.actions:
            print(f"\n→ Executing: {description}")
            print(f"  Command: action {action_name}")
            actions.execute_action(action_name)
            input("Press Enter to continue...")
    
    # Demo dance
    print("\n→ Executing: Dance routine")
    print("  Command: action dance")
    actions.execute_action("dance")
    input("Press Enter to continue...")
    
    print("\n✅ All predefined actions demo completed!")
    controller.disconnect()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
