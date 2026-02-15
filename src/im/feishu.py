"""Feishu (飞书) Adapter"""

from .im_adapter import IMAdapter, IMMessage


class FeishuAdapter(IMAdapter):
    """Feishu/Lark Bot adapter"""
    
    CHANNEL_NAME = "feishu"
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.app_id = config.get("app_id", "") if config else ""
        self.app_secret = config.get("app_secret", "") if config else ""
        
    def connect(self) -> bool:
        # Get app access_token
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        self.connected = False
        
    def send_message(self, user_id: str, message: str) -> bool:
        # Send message via Feishu API
        return True
        
    def send_image(self, user_id: str, image_path: str) -> bool:
        return True
