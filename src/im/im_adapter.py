"""
IM (Instant Messaging) Adapter Base Class
Supports WeChat, WeCom, WhatsApp, Telegram, etc.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Callable


@dataclass
class IMMessage:
    """IM Message"""
    msg_id: str
    user_id: str
    content: str
    timestamp: float
    channel: str  # wechat/wecom/whatsapp/telegram


@dataclass
class IMUser:
    """IM User"""
    user_id: str
    name: str
    avatar: Optional[str] = None


class IMAdapter(ABC):
    """Base class for IM adapters"""
    
    CHANNEL_NAME: str = ""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.handlers = []
        
    @abstractmethod
    def connect(self) -> bool:
        """Connect to IM service"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from IM service"""
        pass
    
    @abstractmethod
    def send_message(self, user_id: str, message: str) -> bool:
        """Send message to user"""
        pass
    
    @abstractmethod
    def send_image(self, user_id: str, image_path: str) -> bool:
        """Send image to user"""
        pass
    
    def register_handler(self, handler: Callable[[IMMessage], str]):
        """Register message handler"""
        self.handlers.append(handler)
    
    def handle_message(self, message: IMMessage) -> str:
        """Handle incoming message"""
        for handler in self.handlers:
            try:
                response = handler(message)
                if response:
                    return response
            except Exception as e:
                print(f"Handler error: {e}")
        return "消息已收到"
