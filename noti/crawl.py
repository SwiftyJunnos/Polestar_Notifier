from .const import (
    AVAILABLE_XPATH,
    IMAGE_XPATH,
    ESTIMATE_XPATH,
    MODEL_XPATH,
    NAME_XPATH,
    INFO_XPATH,
    PRICE_XPATH
)
from .polestar_DTO import Polestar

import re
import os
from typing import TypedDict
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
        driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
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

    def get_images(
        self,
        driver: WebDriver
    ) -> list[str]:
        source_elements = driver.find_elements(By.XPATH, IMAGE_XPATH)
        polestar_images: list[str] = []
        for src in source_elements[::2]:
            img_url = src.get_attribute('srcset').split()[0]
            polestar_images.append(img_url)
            # t = urlopen(img_url).read()
            # f = open(os.path.join(self.save_path, str(index + 1) + ".jpg"), "wb")
            # f.write(t)
        return polestar_images

    def get_infos(
        self,
        driver: WebDriver,
        num_of_stock: int
    ) -> list[Polestar]:
        estimates = driver.find_elements(By.XPATH, ESTIMATE_XPATH)
        models = driver.find_elements(By.XPATH, MODEL_XPATH)
        names = driver.find_elements(By.XPATH, NAME_XPATH)
        infos = driver.find_elements(By.XPATH, INFO_XPATH)
        prices = driver.find_elements(By.XPATH, PRICE_XPATH)
        images = self.get_images(driver)

        availabes: list[Polestar] = []
        for index in range(0, num_of_stock):
            info_index = 4 * index
            price_digits = re.findall(r'\d+', prices[index].text)
            price = ""
            for digit in price_digits:
                price += digit
            available = Polestar(
                estimated=estimates[index].text,
                model=models[index].text,
                name=names[index].text,
                power=infos[info_index + 0].text,
                zero_to_hundred=infos[info_index + 1].text,
                packages=infos[info_index + 2].text,
                drive_time_per_charge=infos[info_index + 3].text,
                price=int(price),
                image=images[index]
            )
            availabes.append(available)

        return availabes