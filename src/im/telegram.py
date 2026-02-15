"""Telegram adapter"""

from .im_adapter import IMAdapter, IMMessage


class TelegramAdapter(IMAdapter):
    """Telegram Bot adapter"""
    
    CHANNEL_NAME = "telegram"
    
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.bot_token = config.get("bot_token", "") if config else ""
        
    def connect(self) -> bool:
        # 初始化 Telegram Bot
        # import telegram
        # self.bot = telegram.Bot(token=self.bot_token)
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        self.connected = False
        
    def send_message(self, user_id: str, message: str) -> bool:
        return True
        
    def send_image(self, user_id: str, image_path: str) -> bool:
        return True
