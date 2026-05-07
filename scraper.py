import shutil
import os
import time

from setup.driver_setup import driver
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "price-with-image"))
)


def url_formatter(url_base, url_target):
    return (
        url_base +
        url_target.title().replace(" ", "+")
    )


def get_images(url_target, path):
    load_dotenv()

    url_base = os.getenv(
        "BASE_URL",
        "https://localhost8000.com/"
    )

    url = url_formatter(url_base, url_target)
    print(url)

    driver.set_page_load_timeout(5)
    driver.get(url)

    prices = driver.find_elements(
        By.CLASS_NAME,
        "price-with-image"
    )

    # reset folder
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)  # ensure exists

    for i, p in enumerate(prices):

        p.screenshot(
            f"{path}/price{i}.png"
        )

    driver.quit()
