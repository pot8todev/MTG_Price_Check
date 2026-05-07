import os

from setup.driver_setup import driver
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By


def url_formatter(url_base, url_target):
    return (
        url_base +
        url_target.title().replace(" ", "+")
    )


load_dotenv()

url_base = os.getenv(
    "BASE_URL",
    "https://localhost8000.com/"
)

url_target = "lightning bolt"

url = url_formatter(url_base, url_target)

print(url)

driver.set_page_load_timeout(5)
driver.get(url)

html = driver.page_source

soup = bs(html, "html.parser")

stores = soup.find_all("div", class_="store")

prices = driver.find_elements(
    By.CLASS_NAME,
    "price-with-image"
)

dir = url_target.title().replace(" ", "")

os.makedirs(f"out/{dir}/screenshots", exist_ok=True)  # ensure exists

for i, p in enumerate(prices):

    p.screenshot(
        f"out/{dir}/screenshots/price{i}.png"
    )

driver.quit()
