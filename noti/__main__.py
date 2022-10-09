from .const import (
    PRECONF_URL
)
from .secret import (
    TELEGRAM_TOKEN,
    TELEGRAM_ID
)
from .crawl import Crawler
from .validate import validate_stock
from .send import TelegramBot

from selenium.webdriver.chrome.webdriver import WebDriver

import schedule
import time

def main():
    crawler = Crawler(PRECONF_URL)
    driver = crawler.setup(10)
    bot = TelegramBot(TELEGRAM_TOKEN)
    search_job = schedule.every(5).minutes.do(search_preconf, crawler, driver, bot)

    while True:
        schedule.run_pending()
        time.sleep(1)

def search_preconf(
    crawler: Crawler,
    driver: WebDriver,
    bot: TelegramBot
):
    availables = crawler.check_stock(driver)
    print(f"{availables} cars Availabe now.")
    if validate_stock(availables):
        infos = crawler.get_infos(driver, availables)
        bot.sendImage(TELEGRAM_ID, infos[0]["image"])
        bot.sendMessage(TELEGRAM_ID, infos[0]["model"])
    elif not validate_stock(availables):
        print("No")

if __name__ == "__main__":
    main()