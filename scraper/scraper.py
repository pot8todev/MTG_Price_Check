from selenium.common.exceptions import (
    TimeoutException,
    InvalidArgumentException,
    WebDriverException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from scraper.soup import tooltip_scrape
from setup.driver_setup import driver
from setup.aux_functions import hide_cookie
from scraper.showcase import open_showcase
from dotenv import load_dotenv
import requests
import random
import shutil
import time
import os


def assure_new_folder(out_path):
    # Recria a pasta principal
    if os.path.exists(out_path):
        shutil.rmtree(out_path)

    os.makedirs(out_path)

    # to reset folders properly
    if out_path != "out":
        # Cria as subpastas
        os.makedirs(os.path.join(out_path, "quantities"))
        os.makedirs(os.path.join(out_path, "prices"))


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


def get_stores_data(url_target, path):

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
    open_showcase()
    stores_data = tooltip_scrape()
    return 0

    prices_html = driver.find_elements(By.CSS_SELECTOR, ".store .price-with-image")
    qnts_html = driver.find_elements(By.CSS_SELECTOR, ".store .quantity-with-image")
    assure_new_folder(path)

    for i, (price, qnt) in enumerate(zip(prices_html, qnts_html)):
        time.sleep(1)

        # Role a página até o elemento p e coloque ele no centro da tela.
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", price)
        price.screenshot(f"{path}/prices/price{i}.png")
        qnt.screenshot(f"{path}/quantities/qnt{i}.png")

    # return edition_names


OUTPUT_DIR = "out"
assure_new_folder(OUTPUT_DIR)
