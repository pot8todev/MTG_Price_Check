import requests
import random
import shutil
import os
import time

from index import reset_folder
from setup.driver_setup import driver
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    InvalidArgumentException,
    WebDriverException
)


def url_formatter(url_base, url_target):
    return (
        url_base +
        url_target.title().replace(" ", "+")
    )


def fetch(url):
    print(url)
    session = requests.Session()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        )
    }
    time.sleep(random.uniform(2, 5))  # slow down

    response = session.get(
        url,
        headers=headers,
        timeout=20
    )

    print(response.status_code)

    if response.status_code == 429:
        print("Rate limited")
        time.sleep(60)

    return response


def get_images(url_target, path):

    load_dotenv()

    url_base = os.getenv(
        "BASE_URL",
        "https://localhost8000.com/"
    )

    url = url_formatter(url_base, url_target)

    try:
        fetch(url)
        driver.set_page_load_timeout(5)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "price-with-image"))
        )

    except TimeoutException:
        print("Page load timed out")

    except InvalidArgumentException:
        print("Invalid URL")

    except WebDriverException as e:
        print(f"WebDriver error: {e}")

    prices = driver.find_elements(
        By.CLASS_NAME,
        "price-with-image"
    )

    # reset folder
    reset_folder(path)

    for i, p in enumerate(prices):

        p.screenshot(
            f"{path}/price{i}.png"
        )
