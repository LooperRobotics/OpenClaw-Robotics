"""WeCom (企业微信) adapter"""

from .im_adapter import IMAdapter, IMMessage


class WeComAdapter(IMAdapter):
    """Enterprise WeChat adapter"""
    
    CHANNEL_NAME = "wecom"
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.corp_id = config.get("corp_id", "") if config else ""
        self.corp_secret = config.get("corp_secret", "") if config else ""
        self.agent_id = config.get("agent_id", "") if config else ""
        
    def connect(self) -> bool:
        # 获取access_token
        # self.token = self._get_token()
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        self.connected = False
        
    def send_message(self, user_id: str, message: str) -> bool:
        # 调用企业微信API发送消息
        return True
        
    def send_image(self, user_id: str, image_path: str) -> bool:
        return True
