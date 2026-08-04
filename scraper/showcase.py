from selenium import webdriver
from selenium.webdriver.common.by import By
from setup.driver_setup import driver
from setup.aux_functions import hide_cookie
from scraper.soup import showcase_cards_per_store
from bs4 import BeautifulSoup

import time

# Find the link


def open_showcase():

    data = []
    link = driver.find_element(By.CSS_SELECTOR, "a.link-store")
    url = link.get_attribute("href")

    # Save the current tab
    original_tab = driver.current_window_handle

    # Open the link in a new tab
    driver.switch_to.new_window("tab")
    driver.get(url)

    print("worked!")
    time.sleep(3)
    hide_cookie()
    # code here
    # ----#
    showcase_cards_per_store()

    # ----#
    print("closing")
    # Close the new tab
    driver.close()

    # Return to the original tab
    driver.switch_to.window(original_tab)

    return data
