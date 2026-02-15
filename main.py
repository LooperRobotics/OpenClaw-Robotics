#!/usr/bin/env python3
"""
Unitree Robot WhatsApp Control - Main Entry Point

This script provides the main entry point for running the
Unitree robot control system with WhatsApp integration.

Usage:
    python3 main.py --mode normal
    python3 main.py --mode simulation
    python3 main.py --whatsapp --port 8080

Author: OpenClaw Contributors
License: MIT
"""

import os
import sys
import json
import argparse
import logging
from typing import Dict, Optional

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.robot_controller import UnitreeRobotController, PredefinedActions
from src.whatsapp_handler import WhatsAppMessageHandler
from src.whatsapp_integration import (
    WhatsAppWebhookHandler,
    WhatsAppWebhookServer,
    WhatsAppAPIClient,
    create_whatsapp_integration
)
from src.openclaw_interface import OpenClawRobotInterface


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UnitreeWhatsAppController:
    """
    Main controller class for Unitree robot with WhatsApp control
    
    This class integrates all components and provides a unified
    interface for controlling the robot through WhatsApp.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the controller
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        
        # Initialize components
        self.controller: Optional[UnitreeRobotController] = None
        self.actions: Optional[PredefinedActions] = None
        self.message_handler: Optional[WhatsAppMessageHandler] = None
        self.openclaw_interface: Optional[OpenClawRobotInterface] = None
        self.webhook_handler: Optional[WhatsAppWebhookHandler] = None
        self.webhook_server: Optional[WhatsAppWebhookServer] = None
        self.api_client: Optional[WhatsAppAPIClient] = None
        
        # Load configuration
        self._load_config()
        
        logger.info("Unitree WhatsApp Controller initialized")
    
    def _load_config(self):
        """Load configuration from file or environment"""
        config_file = self.config.get('config_file', 'config.json')
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
    
    def initialize(self, simulation_mode: bool = False):
        """
        Initialize all components
        
        Args:
            simulation_mode: Whether to run in simulation mode
        """
        logger.info("Initializing components...")
        
        # Initialize robot controller
        robot_type = self.config.get('robot_type', 'go1')
        self.controller = UnitreeRobotController(
            robot_type=robot_type,
            enable_logging=not simulation_mode
        )
        
        if not simulation_mode:
            if not self.controller.connect():
                logger.warning("Failed to connect to robot. Running in simulation mode.")
        
        # Initialize predefined actions
        self.actions = PredefinedActions(self.controller)
        
        # Initialize message handler
        self.message_handler = WhatsAppMessageHandler(
            self.controller,
            self.actions
        )
        
        # Initialize OpenClaw interface
        self.openclaw_interface = OpenClawRobotInterface(
            self.controller,
            self.actions,
            self.message_handler
        )
        
        # Initialize WhatsApp integration
        self._init_whatsapp()
        
        logger.info("All components initialized successfully")
    
    def _init_whatsapp(self):
        """Initialize WhatsApp integration"""
        # Get WhatsApp credentials
        whatsapp_token = os.environ.get('WHATSAPP_ACCESS_TOKEN', '')
        verify_token = os.environ.get('WHATSAPP_VERIFY_TOKEN', 'unitree_bot')
        app_secret = os.environ.get('WHATSAPP_APP_SECRET', '')
        phone_number_id = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '')
        
        # Create integration
        self.webhook_handler, self.webhook_server, self.api_client = create_whatsapp_integration(
            self.controller,
            self.actions,
            whatsapp_token=whatsapp_token,
            verify_token=verify_token,
            app_secret=app_secret
        )
        
        # Update API client if credentials available
        if phone_number_id and whatsapp_token:
            self.api_client = WhatsAppAPIClient(phone_number_id, whatsapp_token)
    
    def start(self, port: int = 8080, blocking: bool = True):
        """
        Start the webhook server
        
        Args:
            port: Port to listen on
            blocking: Whether to block the main thread
        """
        if not self.webhook_server:
            logger.error("Webhook server not initialized")
            return
        
        logger.info(f"Starting webhook server on port {port}...")
        
        try:
            self.webhook_server.start(blocking=blocking)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.stop()
    
    def start_background(self, port: int = 8080):
        """Start the server in background"""
        if not self.webhook_server:
            logger.error("Webhook server not initialized")
            return
        
        self.webhook_server.start_background()
        logger.info(f"Server started in background on port {port}")
    
    def stop(self):
        """Stop all components"""
        logger.info("Stopping components...")
        
        if self.controller:
            self.controller.disconnect()
        
        if self.webhook_server:
            self.webhook_server.stop()
        
        logger.info("All components stopped")
    
    def get_status(self) -> Dict:
        """Get system status"""
        return {
            "controller": self.controller.get_robot_status() if self.controller else None,
            "openclaw_tools": self.openclaw_interface.get_all_tools() if self.openclaw_interface else [],
            "available_actions": self.actions.list_actions() if self.actions else []
        }
    
    def send_message(self, to: str, text: str) -> Dict:
        """
        Send a message through WhatsApp
        
        Args:
            to: Recipient phone number
            text: Message text
            
        Returns:
            Dict containing send result
        """
        if self.api_client:
            return self.api_client.send_message(to, text)
        else:
            logger.warning("API client not configured")
            return {"success": False, "error": "API client not configured"}
    
    def execute_command(self, command: str) -> str:
        """
        Execute a command directly
        
        Args:
            command: Command string
            
        Returns:
            str: Command response
        """
        if self.message_handler:
            return self.message_handler.process_message(command, "cli")
        return "Message handler not initialized"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Unitree Robot WhatsApp Control System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --mode simulation
    %(prog)s --whatsapp --port 8080
    %(prog)s --execute "forward 0.5"
    %(prog)s --status
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['normal', 'simulation'],
        default='simulation',
        help='Operation mode (default: simulation)'
    )
    parser.add_argument(
        '--config',
        default='config.json',
        help='Configuration file path'
    )
    parser.add_argument(
        '--whatsapp',
        action='store_true',
        help='Enable WhatsApp webhook server'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port for webhook server (default: 8080)'
    )
    parser.add_argument(
        '--execute',
        '-e',
        help='Execute a single command'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show system status'
    )
    parser.add_argument(
        '--list-actions',
        action='store_true',
        help='List available actions'
    )
    parser.add_argument(
        '--list-tools',
        action='store_true',
        help='List available OpenClaw tools'
    )
    
    args = parser.parse_args()
    
    # Create controller
    config = {'config_file': args.config}
    app = UnitreeWhatsAppController(config)
    
    # Initialize
    simulation_mode = args.mode == 'simulation'
    app.initialize(simulation_mode)
    
    # Handle commands
    if args.execute:
        response = app.execute_command(args.execute)
        print(f"\nResponse: {response}")
    
    elif args.status:
        status = app.get_status()
        print("\n🤖 System Status:")
        print(json.dumps(status, indent=2))
    
    elif args.list_actions:
        if app.actions:
            print("\nAvailable Actions:")
            for action in app.actions.list_actions():
                print(f"  - {action}")
    
    elif args.list_tools:
        if app.openclaw_interface:
            print("\nAvailable OpenClaw Tools:")
            tools = app.openclaw_interface.get_all_tools()
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
    
    elif args.whatsapp:
        print(f"\nStarting WhatsApp webhook server on port {args.port}...")
        print("Press Ctrl+C to stop")
        app.start(port=args.port, blocking=True)
    
    else:
        # Interactive mode
        print("\n🤖 Unitree Robot WhatsApp Control System")
        print("=" * 50)
        print("Mode:", "Simulation" if simulation_mode else "Normal")
        print("\nAvailable commands:")
        print("  --execute <command>  : Execute a command")
        print("  --status              : Show system status")
        print("  --list-actions        : List available actions")
        print("  --list-tools          : List available tools")
        print("  --whatsapp --port <N> : Start WhatsApp webhook server")
        print("\nInteractive mode. Type 'quit' to exit.")
        print("=" * 50)
        
        while True:
            try:
                command = input("\nEnter command: ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not command:
                    continue
                
                response = app.execute_command(command)
                print(f"\n→ {response}")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break
    
    # Cleanup
    app.stop()
    print("\nGoodbye! 👋")


if __name__ == "__main__":
    main()
