import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from bs4 import BeautifulSoup as bs

import requests

options = Options()
options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=options)
url = "https://www.ligamagic.com.br/?view=cards/card&card=Lightning+Bolt"


driver.get(url)
time.sleep(5)

html = driver.page_source

soup = bs(html, "html.parser")

stores = soup.find_all("div", class_="store")

prices = driver.find_elements(By.CLASS_NAME, "price-with-image")


for i, p in enumerate(prices):
    if p:
        p.screenshot(f'pictures/price{i}.png')


driver.quit()
