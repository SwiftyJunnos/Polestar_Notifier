import telegram

from .secret import (
    TELEGRAM_TOKEN, TELEGRAM_ID
)

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.bot = telegram.Bot(token=self.token)

    def sendImage(
        self,
        chat_id: str,
        img_url: str
    ):
        self.bot.send_photo(chat_id, img_url)
    
    def sendMessage(
        self,
        chat_id: str,
        message: str
    ):
        self.bot.send_message(chat_id, message)
