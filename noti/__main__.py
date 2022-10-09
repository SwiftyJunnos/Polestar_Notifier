from .const import (
    PRECONF_URL
)
from .secret import (
    TELEGRAM_ID,
    TELEGRAM_TOKEN
)
from .crawl import Crawler
from .validate import validate_stock

import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def main():
    run()

def run():
    crawler = Crawler(PRECONF_URL)
    driver = crawler.setup(10)

    availables = crawler.check_stock(driver)
    if validate_stock(availables):
        print("Yes")
        crawler.get_image(driver)
    elif not validate_stock(availables):
        print("No")

if __name__ == "__main__":
    main()