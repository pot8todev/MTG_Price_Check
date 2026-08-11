from selenium import webdriver
from selenium.webdriver.common.by import By
from setup.driver_setup import driver
from setup.aux_functions import hide_cookie
from bs4 import BeautifulSoup

import time

# Find the link

tabs = []
curr_tab = driver.current_window_handle
tabs.append(curr_tab)


def open_store_showcase():
    link = driver.find_element(By.CSS_SELECTOR, "a.link-store")
    url = link.get_attribute("href")
    if  not url:  
        return

    # Save the current tab
    original_tab = driver.current_window_handle

    # Open the link in a new tab
    driver.switch_to.new_window("tab")
    curr_tab = driver.current_window_handle
    tabs.append(curr_tab)
    

    driver.get(url)

    time.sleep(3)
    hide_cookie()
    driver.switch_to.new_window(original_tab)
    # code here
    # ----#

    # ----#


def close_tab():
    if len(tabs)>0:
        driver.close()
        print("closing")
        # Return to the original tab
        original_tab = tabs[0]
        driver.switch_to.window(original_tab)
