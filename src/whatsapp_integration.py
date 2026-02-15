#!/usr/bin/env python3
"""
WhatsApp Integration Module
Integrates the robot control system with WhatsApp messaging

This module provides WhatsApp webhook handling and message
processing for the Unitree robot control system.

Author: OpenClaw Contributors
License: MIT
"""

import os
import sys
import json
import hmac
import hashlib
import logging
import threading
from typing import Dict, List, Optional, Callable, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.whatsapp_handler import WhatsAppMessageHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WhatsAppWebhookHandler:
    """
    Handles incoming WhatsApp webhook messages
    
    This class processes webhook requests from WhatsApp Business API,
    validates signatures, and routes messages to the appropriate handler.
    """
    
    def __init__(self, message_handler: WhatsAppMessageHandler, 
                 verify_token: str = None, app_secret: str = None):
        """
        Initialize WhatsApp webhook handler
        
        Args:
            message_handler: WhatsAppMessageHandler instance
            verify_token: Token for webhook verification
            app_secret: WhatsApp App Secret for signature validation
        """
        self.message_handler = message_handler
        self.verify_token = verify_token or os.environ.get('WHATSAPP_VERIFY_TOKEN', 'your_verify_token')
        self.app_secret = app_secret or os.environ.get('WHATSAPP_APP_SECRET', '')
        
        # Callback for processed messages
        self.on_message_callback: Optional[Callable[[str, str], None]] = None
        
        logger.info("WhatsApp Webhook Handler initialized")
    
    def verify_webhook(self, mode: str, token: str, challenge: str) -> tuple:
        """
        Verify webhook endpoint
        
        Args:
            mode: Verification mode
            token: Verify token from request
            challenge: Challenge string to return
            
        Returns:
            Tuple of (status_code, response_body)
        """
        if mode == 'subscribe' and token == self.verify_token:
            logger.info("Webhook verification successful")
            return 200, challenge
        
        logger.warning("Webhook verification failed")
        return 403, "Verification failed"
    
    def process_webhook_payload(self, payload: Dict) -> List[Dict]:
        """
        Process incoming webhook payload
        
        Args:
            payload: Webhook payload from WhatsApp
            
        Returns:
            List of processed messages with responses
        """
        results = []
        
        try:
            # Extract message entries
            entries = payload.get('entry', [])
            
            for entry in entries:
                changes = entry.get('changes', [])
                
                for change in changes:
                    value = change.get('value', {})
                    
                    # Process messages
                    messages = value.get('messages', [])
                    for message in messages:
                        processed = self._process_single_message(message, value)
                        results.append(processed)
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing webhook payload: {e}")
            return [{"error": str(e)}]
    
    def _process_single_message(self, message: Dict, value: Dict) -> Dict:
        """
        Process a single message
        
        Args:
            message: Message data
            value: Full webhook value
            
        Returns:
            Dict containing processed message and response
        """
        message_id = message.get('id', '')
        from_number = message.get('from', '')
        message_type = message.get('type', 'text')
        timestamp = message.get('timestamp', '')
        
        # Extract message content
        content = ""
        if message_type == 'text':
            content = message.get('text', {}).get('body', '')
        elif message_type == 'button':
            content = message.get('button', {}).get('text', '')
        elif message_type == 'interactive':
            # Handle interactive messages (buttons, lists)
            interactive = message.get('interactive', {})
            button_reply = interactive.get('button_reply', {})
            content = button_reply.get('title', '')
        
        # Get display name if available
        contacts = value.get('contacts', [])
        display_name = ""
        if contacts:
            profile = contacts[0].get('profile', {})
            display_name = profile.get('name', '')
        
        # Process the message
        response = self.message_handler.process_message(content, from_number)
        
        result = {
            "message_id": message_id,
            "from": from_number,
            "display_name": display_name,
            "type": message_type,
            "content": content,
            "timestamp": timestamp,
            "response": response
        }
        
        # Trigger callback if set
        if self.on_message_callback:
            try:
                self.on_message_callback(from_number, content)
            except Exception as e:
                logger.error(f"Error in message callback: {e}")
        
        logger.info(f"Processed message from {from_number}: {content[:50]}...")
        
        return result
    
    def send_text_message(self, to: str, text: str, 
                         preview_url: bool = True) -> Dict:
        """
        Send a text message through WhatsApp
        
        Args:
            to: Recipient phone number
            text: Message text
            preview_url: Whether to show URL preview
            
        Returns:
            Dict containing send result
        """
        # This would integrate with WhatsApp Business API
        # Placeholder for actual implementation
        logger.info(f"Sending message to {to}: {text[:50]}...")
        
        # In a real implementation, you would:
        # 1. Get access token from WhatsApp Business API
        # 2. Make API call to send message
        # 3. Return result
        
        return {
            "success": True,
            "to": to,
            "message": "Message queued (placeholder)"
        }
    
    def send_template_message(self, to: str, template_name: str, 
                             language: str = "en_US",
                             components: List[Dict] = None) -> Dict:
        """
        Send a template message
        
        Args:
            to: Recipient phone number
            template_name: Name of the template
            language: Template language code
            components: Template components
            
        Returns:
            Dict containing send result
        """
        logger.info(f"Sending template {template_name} to {to}")
        
        return {
            "success": True,
            "to": to,
            "template": template_name,
            "message": "Template queued (placeholder)"
        }


class WhatsAppWebhookServer:
    """
    Simple HTTP server for handling WhatsApp webhooks
    
    This class provides a basic HTTP server that can receive
    webhook requests and process them.
    """
    
    def __init__(self, handler: WhatsAppWebhookHandler, port: int = 8080):
        """
        Initialize webhook server
        
        Args:
            handler: WhatsAppWebhookHandler instance
            port: Port to listen on
        """
        self.handler = handler
        self.port = port
        self.server = None
        self.thread = None
        
        logger.info(f"WhatsApp Webhook Server initialized on port {port}")
    
    def start(self, blocking: bool = True):
        """
        Start the webhook server
        
        Args:
            blocking: Whether to block the main thread
        """
        self.server = HTTPServer(('0.0.0.0', self.port), self._create_request_handler())
        
        logger.info(f"Server started. Listening on port {self.port}")
        
        if blocking:
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                logger.info("Server shutting down...")
                self.stop()
    
    def start_background(self):
        """Start the server in a background thread"""
        self.thread = threading.Thread(target=self.start, kwargs={'blocking': True})
        self.thread.daemon = True
        self.thread.start()
        logger.info("Server started in background")
    
    def stop(self):
        """Stop the webhook server"""
        if self.server:
            self.server.shutdown()
            logger.info("Server stopped")
    
    def _create_request_handler(self):
        """Create request handler class"""
        handler = self.handler
        
        class RequestHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                # Suppress default logging
                pass
            
            def do_GET(self):
                """Handle GET requests (webhook verification)"""
                try:
                    query = parse_qs(self.path.split('?')[1]) if '?' in self.path else {}
                    
                    mode = query.get('hub.mode', [''])[0]
                    token = query.get('hub.verify_token', [''])[0]
                    challenge = query.get('hub.challenge', [''])[0]
                    
                    status, body = handler.verify_webhook(mode, token, challenge)
                    
                    self.send_response(status)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(body.encode())
                    
                except Exception as e:
                    logger.error(f"Error in GET handler: {e}")
                    self.send_response(500)
                    self.end_headers()
            
            def do_POST(self):
                """Handle POST requests (webhook messages)"""
                try:
                    content_length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(content_length)
                    
                    # Validate signature if app secret is set
                    signature = self.headers.get('X-Hub-Signature-256', '')
                    if handler.app_secret:
                        if not self._validate_signature(body, signature):
                            logger.warning("Invalid webhook signature")
                            self.send_response(401)
                            self.end_headers()
                            return
                    
                    # Parse payload
                    payload = json.loads(body.decode('utf-8'))
                    
                    # Process messages
                    results = handler.process_webhook_payload(payload)
                    
                    # Send response
                    response = json.dumps({"success": True, "results": results})
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(response.encode())
                    
                except Exception as e:
                    logger.error(f"Error in POST handler: {e}")
                    self.send_response(500)
                    self.end_headers()
            
            def _validate_signature(self, body: bytes, signature: str) -> bool:
                """Validate webhook signature"""
                if not signature.startswith('sha256='):
                    return False
                
                expected = hmac.new(
                    handler.app_secret.encode(),
                    body,
                    hashlib.sha256
                ).hexdigest()
                
                return hmac.compare_digest(signature[7:], expected)
        
        return RequestHandler


class WhatsAppAPIClient:
    """
    Client for WhatsApp Business API
    
    This class provides methods for sending messages through
    the WhatsApp Business API.
    """
    
    def __init__(self, phone_number_id: str, access_token: str,
                 api_version: str = "v18.0"):
        """
        Initialize API client
        
        Args:
            phone_number_id: WhatsApp Phone Number ID
            access_token: WhatsApp Access Token
            api_version: WhatsApp API version
        """
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = f"https://graph.facebook.com/{api_version}"
        
        logger.info("WhatsApp API Client initialized")
    
    def _get_headers(self) -> Dict:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def send_message(self, to: str, text: str, 
                    preview_url: bool = True) -> Dict:
        """
        Send a text message
        
        Args:
            to: Recipient phone number
            text: Message text
            preview_url: Show URL preview
            
        Returns:
            Dict containing API response
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "body": text,
                "preview_url": preview_url
            }
        }
        
        return self._send_request(payload)
    
    def send_template(self, to: str, template_name: str,
                      language: str = "en_US",
                      components: List[Dict] = None) -> Dict:
        """
        Send a template message
        
        Args:
            to: Recipient phone number
            template_name: Template name
            language: Language code
            components: Template components
            
        Returns:
            Dict containing API response
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language},
                "components": components or []
            }
        }
        
        return self._send_request(payload)
    
    def _send_request(self, payload: Dict) -> Dict:
        """
        Send API request
        
        Args:
            payload: Request payload
            
        Returns:
            Dict containing API response
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload
            )
            
            result = response.json()
            
            if response.status_code in [200, 201]:
                logger.info("Message sent successfully")
                return {"success": True, "response": result}
            else:
                logger.error(f"Failed to send message: {result}")
                return {"success": False, "error": result}
                
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return {"success": False, "error": str(e)}


# Convenience functions for quick setup

def create_whatsapp_integration(
    robot_controller,
    predefined_actions,
    whatsapp_token: str = None,
    verify_token: str = None,
    app_secret: str = None
) -> tuple:
    """
    Create a complete WhatsApp integration
    
    Args:
        robot_controller: UnitreeRobotController instance
        predefined_actions: PredefinedActions instance
        whatsapp_token: WhatsApp Access Token
        verify_token: Webhook verification token
        app_secret: WhatsApp App Secret
        
    Returns:
        Tuple of (webhook_handler, webhook_server, api_client)
    """
    # Create message handler
    message_handler = WhatsAppMessageHandler(robot_controller, predefined_actions)
    
    # Create webhook handler
    webhook_handler = WhatsAppWebhookHandler(
        message_handler=message_handler,
        verify_token=verify_token,
        app_secret=app_secret
    )
    
    # Create webhook server
    webhook_server = WhatsAppWebhookServer(webhook_handler)
    
    # Create API client (optional)
    api_client = None
    if whatsapp_token:
        phone_number_id = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '')
        api_client = WhatsAppAPIClient(phone_number_id, whatsapp_token)
    
    return webhook_handler, webhook_server, api_client


if __name__ == "__main__":
    # Example usage
    from src.robot_controller import UnitreeRobotController, PredefinedActions
    
    print("Initializing WhatsApp integration...")
    
    # Create robot controller (will be in simulation mode)
    controller = UnitreeRobotController()
    controller.connect()
    
    # Create predefined actions
    actions = PredefinedActions(controller)
    
    # Create integration
    handler, server, client = create_whatsapp_integration(
        controller,
        actions,
        verify_token="my_verify_token"
    )
    
    print("Starting webhook server on port 8080...")
    print("Press Ctrl+C to stop")
    
    try:
        server.start(blocking=True)
    except KeyboardInterrupt:
        print("\nShutting down...")
        controller.disconnect()
