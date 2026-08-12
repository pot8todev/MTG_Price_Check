from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    InvalidArgumentException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from setup.driver_setup import driver
from setup.aux_functions import hide_cookie ,start_timer, mark_timer
from scraper.soup import tooltip_scrape
from scraper.showcase import open_store_showcase, open_new_tab,close_tab
from dotenv import load_dotenv
from pathlib import Path
import requests
import random
import shutil
import time
import os





def url_formatter(url_base, url_target):
    return url_base + url_target.title().replace(" ", "+").replace("'","%27")


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

    response = session.get(url, headers=headers, timeout=20)

    print(response.status_code)

    if response.status_code == 429:
        print("Rate limited")
        time.sleep(60)

    return response



def get_stores_data(url_target:str, output_folder:str,driver):
    load_dotenv()

    url_base = os.getenv("BASE_URL", "https://localhost8000.com/")

    url = url_formatter(url_base, url_target)

    try:
        fetch(url)
        driver.set_page_load_timeout(50)
        driver.get(url)

        # TODO: change the waiting requirement
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
    # store_data: name, address, tel_num, showcase_url
    start = start_timer()
    stores = tooltip_scrape()
    mark_timer(start,"tooltip scrape in:")
    original_tab = driver.current_window_handle
    # TODO:slyghtly uneficient
    open_new_tab()

    for store in stores:
        url = store.showcase_url

        if url:
            stock = open_store_showcase( url)

            if stock is not None:
                store.stock.extend(stock)

    close_tab(original_tab)
    

    return stores


