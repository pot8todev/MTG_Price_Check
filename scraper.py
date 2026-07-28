import requests
import random
import shutil
import os
import time

from bs4 import BeautifulSoup
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


def get_stores_data(url_target, path):

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

    html_content = driver.page_source
    soup= BeautifulSoup(html_content,"html.parser")

    #adding all  store names in paralel
    names_store = []
    for link in soup.select(" .store .name-ed"):
        clean_name = link.text.strip()
        names_store.append(clean_name)

    #hiding the cookie notification that clouds the view
    driver.execute_script(
        "document.getElementById('lgpd-cookie').style.display = 'none';"
    )

    prices = driver.find_elements( By.CSS_SELECTOR, ".store .price-with-image")
    qnts = driver.find_elements( By.CSS_SELECTOR, ".store .quantity-with-image")
    
    reset_folder(path)

    for i,(price,qnt)  in enumerate(zip(prices,qnts)):

        time.sleep(2)

        # Role a página até o elemento p e coloque ele no centro da tela.
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            price
        )
        price.screenshot( f"{path}/price{i}.png")
        qnt.screenshot( f"{path}/qnt{i}.png")

    return names_store 


OUTPUT_DIR = "out"
reset_folder(OUTPUT_DIR)
