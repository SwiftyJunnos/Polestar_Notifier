import telegram

from .secret import (
    TELEGRAM_TOKEN, TELEGRAM_ID
)

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.bot = telegram.Bot(token=self.token)
    
    def sendMessage(
        self,
        chat_id: str,
        message: str
    ):
        self.bot.send_message(chat_id, message)

def test():
    bot = TelegramBot(TELEGRAM_TOKEN)
    bot.sendMessage(TELEGRAM_ID, "Hello")