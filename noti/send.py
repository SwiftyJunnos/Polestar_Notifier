import telegram

from noti.polestar_DTO import Polestar

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

    def sendInfo(
        self,
        num_available: int,
        availables: list[Polestar]
    ):
        self.sendMessage(TELEGRAM_ID, f"현재 구매 가능한 {num_available}개의 옵션이 있습니다.")
        for available in availables:
            self.sendImage(TELEGRAM_ID, available["image"])
            self.sendMessage(TELEGRAM_ID, (
                f"{available['model']}\n"
                f"{available['name']}\n\n"
                f"예상 인도: {available['estimated']}\n"
                f"출력: {available['power']}\n"
                f"0➡️100km/h: {available['zero_to_hundred']}\n"
                f"패키지: {available['packages']}\n"
                f"1회 충전 주행거리: {available['drive_time_per_charge']}\n"
                f"{format(available['price'], ',d')}원"
                )
            )
