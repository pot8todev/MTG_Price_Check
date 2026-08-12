
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from scraper.scraper import get_stores_data

options = Options()
# options.debugger_address = "127.0.0.1:9222"
#
# driver = webdriver.Chrome(options=options)
class Scraper:
    def __init__(self):
        self.driver = webdriver.Firefox(options=options)

    def get_stores_data(self, card_name, card_folder):
        self.driver.get(...)

    def get_price(self, ...):
        self.driver.find_element(...)

    def close(self):
        self.driver.quit()
