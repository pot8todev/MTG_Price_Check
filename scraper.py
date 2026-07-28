import requests
import random
import shutil
import os
import time


from setup.driver_setup import driver
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    InvalidArgumentException,
    WebDriverException
)


def reset_folder(out_path):
    # recreate a folder for current scraping
    if os.path.exists(out_path):
        shutil.rmtree(out_path)
    os.makedirs(out_path)


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
        driver.set_page_load_timeout(50)
        driver.get(url)

        WebDriverWait(driver, 20).until(
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
    driver.execute_script(
        "document.getElementById('lgpd-cookie').style.display = 'none';"
)
    # prices = driver.find_elements(
    #     By.CLASS_NAME,
    #     "price-with-image"
    # )
    reset_folder(path)

    for i, p in enumerate(prices):

        time.sleep(2)
        
        # Role a página até o elemento p e coloque ele no centro da tela.
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            p
        )
        p.screenshot(
            f"{path}/price{i}.png"
        )


OUTPUT_DIR = "out"
reset_folder(OUTPUT_DIR)
