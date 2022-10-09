from .const import (
    AVAILABLE_XPATH,
    IMAGE_XPATH
)

import re
import os
from urllib.request import urlopen

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By

class Crawler:
    save_path = "noti/images"

    def __init__(
        self,
        url: str
    ):
        self.url = url

    def setup(
        self,
        delay_time: int
    ) -> WebDriver:
        options = self.set_driver_option()
        driver = webdriver.Chrome("noti/chromedriver", options=options)
        driver.get(self.url)
        driver.implicitly_wait(delay_time)
        return driver

    def set_driver_option(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        return options

    def check_stock(
        self,
        driver: WebDriver
    ) -> int:
        result = driver.find_element(By.XPATH, AVAILABLE_XPATH).text
        if result == None:
            return 0
        number_of_stock = re.findall('\(([^)]+)', result)[0]
        return int(number_of_stock)

    def get_image(
        self,
        driver: WebDriver
    ):
        source_elements = driver.find_elements(By.XPATH, IMAGE_XPATH)
        for index, src in enumerate(source_elements[::2]):
            img_url = src.get_attribute('srcset').split()[0]
            t = urlopen(img_url).read()
            f = open(os.path.join(self.save_path, str(index + 1) + ".jpg"), "wb")
            f.write(t)
