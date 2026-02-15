#!/usr/bin/env python3
"""
Example: Basic Robot Control
Demonstrates basic movement commands

Usage:
    python3 examples/basic_control.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot_controller import UnitreeRobotController


def main():
    print("=" * 60)
    print("Unitree Robot - Basic Control Demo")
    print("=" * 60)
    
    # Create controller
    controller = UnitreeRobotController(robot_type="go1")
    
    # Connect to robot
    print("\n[1] Connecting to robot...")
    if controller.connect():
        print("✅ Robot connected successfully!")
    else:
        print("❌ Failed to connect. Running in simulation mode.")
    
    # Demo sequence
    print("\n[2] Running movement demo...")
    print("-" * 60)
    
    # Move forward
    print("→ Moving forward at speed 0.5...")
    controller.move_forward(speed=0.5)
    input("Press Enter to continue...")
    
    # Move backward
    print("→ Moving backward...")
    controller.move_backward(speed=0.3)
    input("Press Enter to continue...")
    
    # Move left
    print("→ Moving left...")
    controller.move_left(speed=0.5)
    input("Press Enter to continue...")
    
    # Move right
    print("→ Moving right...")
    controller.move_right(speed=0.5)
    input("Press Enter to continue...")
    
    # Rotate
    print("→ Rotating left by 45 degrees...")
    controller.rotate_left(angle=45)
    input("Press Enter to continue...")
    
    print("→ Rotating right by 90 degrees...")
    controller.rotate_right(angle=90)
    input("Press Enter to continue...")
    
    # Stop
    print("→ Stopping robot...")
    controller.stop()
    
    # Show status
    print("\n[3] Robot Status:")
    print("-" * 60)
    status = controller.get_robot_status()
    print(f"Connected: {status['connected']}")
    print(f"Robot Type: {status['robot_type']}")
    print(f"Current Speed: {status['current_speed']}")
    
    # Disconnect
    print("\n[4] Disconnecting...")
    controller.disconnect()
    print("✅ Demo completed!")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
