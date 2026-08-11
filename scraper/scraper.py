from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    InvalidArgumentException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from scraper.soup import tooltip_scrape
from setup.driver_setup import driver
from setup.aux_functions import hide_cookie, screenshot_data
from scraper.showcase import open_store_showcase
from dotenv import load_dotenv
import requests
import random
import shutil
import time
import os


OUTPUT_DIR = "out"
def assure_new_folder(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

    if dir != OUTPUT_DIR:
        os.makedirs(os.path.join(dir, "quantities"))
        os.makedirs(os.path.join(dir, "prices"))

assure_new_folder(OUTPUT_DIR)

def url_formatter(url_base, url_target):
    return url_base + url_target.title().replace(" ", "+")


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

    response = session.get(url, headers=headers, timeout=20)

    print(response.status_code)

    if response.status_code == 429:
        print("Rate limited")
        time.sleep(60)

    return response



def get_stores_data(url_target, output_folder):
    load_dotenv()

    url_base = os.getenv("BASE_URL", "https://localhost8000.com/")

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

    hide_cookie()
    # store name, address, tel_num, showcase_url
    stores_data = []
    tooltip_scrape(stores_data)
    original_tab = driver.current_window_handle
    for store in stores_data:
        url = store.get("showcase_url")

        if url:
            open_store_showcase(url, original_tab,output_folder)
    assure_new_folder(output_folder)

    return stores_data


