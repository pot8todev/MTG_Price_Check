from selenium import webdriver
from selenium.webdriver.common.by import By
from setup.driver_setup import driver
from setup.aux_functions import hide_cookie
from scraper.soup import soup_stock
from bs4 import BeautifulSoup

import time

# Find the link

tabs = []

def open_store_showcase(url, original_tab, out):
    if not url:
        return

    driver.switch_to.new_window("tab")
    store_tab = driver.current_window_handle

    driver.get(url)

    time.sleep(3)
    hide_cookie()
    soup_stock()

    # Go back to the original tab
    driver.switch_to.window(original_tab)

    # Now close the store tab
    driver.switch_to.window(store_tab)
    driver.close()

    # Return to original
    driver.switch_to.window(original_tab)
