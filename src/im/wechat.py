"""WeChat adapter (个人微信 - 需要itchat或其他库)"""

from .im_adapter import IMAdapter, IMMessage


class WeChatAdapter(IMAdapter):
    """WeChat personal account adapter"""
    
    CHANNEL_NAME = "wechat"
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.bot = None
        
    def connect(self) -> bool:
        # 实现微信登录
        # import itchat
        # self.bot = itchat.login()
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        self.connected = False
        
    def send_message(self, user_id: str, message: str) -> bool:
        # self.bot.send(message, toUserName=user_id)
        return True
        
    def send_image(self, user_id: str, image_path: str) -> bool:
        return True
