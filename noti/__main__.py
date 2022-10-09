from .const import (
    PRECONF_URL
)
from .crawl import Crawler
from .polestar_DTO import Polestar
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
    print(f"{availables} cars Availabe now.")
    if validate_stock(availables):
        print("Yes")
        infos = crawler.get_infos(driver, availables)
        print(infos)
    elif not validate_stock(availables):
        print("No")

if __name__ == "__main__":
    main()