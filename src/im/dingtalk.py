"""DingTalk (钉钉) Adapter"""

from .im_adapter import IMAdapter, IMMessage


class DingTalkAdapter(IMAdapter):
    """DingTalk Robot/Callback adapter"""
    
    CHANNEL_NAME = "dingtalk"
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.agent_id = config.get("agent_id", "") if config else ""
        self.app_key = config.get("app_key", "") if config else ""
        self.app_secret = config.get("app_secret", "") if config else ""
        
    def connect(self) -> bool:
        # Get access_token
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        self.connected = False
        
    def send_message(self, user_id: str, message: str) -> bool:
        # Send via DingTalk robot
        return True
        
    def send_image(self, user_id: str, image_path: str) -> bool:
        return True
