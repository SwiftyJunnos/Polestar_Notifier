from .const import (
    PRECONF_URL
)
from .secret import (
    TELEGRAM_TOKEN,
    TELEGRAM_ID
)
from .polestar_DTO import Polestar
from .crawl import Crawler
from .validate import validate_stock
from .send import TelegramBot
from .log import get_logger

from selenium.webdriver.chrome.webdriver import WebDriver

import schedule
import time
import datetime

SEARCH_DURATION = 3

_LOGGER = get_logger("runtime_logger")

def main():
    crawler = Crawler(PRECONF_URL)
    driver = crawler.setup(10)
    bot = TelegramBot(TELEGRAM_TOKEN)
    updater = Updater(crawler, driver, bot)

    search_job = schedule.every(SEARCH_DURATION).minutes.do(
        updater.search_preconf,
        updater.crawler,
        updater.driver,
        updater.bot
    )

    _LOGGER.info("폴스타 알리미 프로그램 시작")
    while True:
        schedule.run_pending()
        time.sleep(SEARCH_DURATION * 60)

class Updater:
    availables: list[Polestar] = []
    num_availables: int = -1
    is_first_launch: bool = True

    def __init__(
        self,
        crawler: Crawler,
        driver: WebDriver,
        bot: TelegramBot
    ):
        self.crawler = crawler
        self.driver = driver
        self.bot = bot

    def compare(self):
        _LOGGER.info("이전과 옵션 개수가 같습니다.")
        

    def search_preconf(
        self,
        crawler: Crawler,
        driver: WebDriver,
        bot: TelegramBot
    ):
        currently_available_options = crawler.check_stock(driver)
        old_availables = self.availables

        if self.is_first_launch:
            bot.sendMessage(TELEGRAM_ID, f"""
                폴스타2 검색을 시작합니다.\n현재 검색 주기는 {SEARCH_DURATION}분 입니다.
            """)
            self.is_first_launch = False

        # 가능한 목록이 아예 없으면
        if not validate_stock(currently_available_options):
            self.availables = []
            self.num_availables = 0
            _LOGGER.info("현재 구매 가능한 옵션이 없습니다.")
            return
        # 개수가 전과 다르면
        elif self.num_availables != currently_available_options:
            # 현재 프리컨 목록 전송
            _LOGGER.info("새로운 옵션을 발견하였습니다. 텔레그램으로 전송합니다.")
            self.availables = crawler.get_infos(driver, currently_available_options)
            bot.sendInfo(currently_available_options, self.availables)
            self.num_availables = currently_available_options
        else:
            self.compare()
            # 개수가 전과 같으면
            # 비교해본 후 내용이 전과 다르면
            # 현재 프리컨 목록 전송
            # 내용이 같으면
            # 스킵

if __name__ == "__main__":
    main()