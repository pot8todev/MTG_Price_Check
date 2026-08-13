from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()


class Scraper:
    def __init__(self):
        self.driver = webdriver.Firefox(options=options)

    def close(self):
        self.driver.quit()
