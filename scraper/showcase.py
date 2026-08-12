from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from setup.driver_setup import driver
from setup.aux_functions import hide_cookie, start_timer, mark_timer
from scraper.soup import soup_stock

import time

# Find the link

new_tabs = []

def open_new_tab():
    driver.switch_to.new_window("tab")
    tab = driver.current_window_handle
    new_tabs.append(tab)


def close_tab(original_tab):
    new_tabs.pop()
    driver.close()
    driver.switch_to.window(original_tab)

def open_store_showcase(url:str):
    if not url:
        return
    driver.get(url)

    start = start_timer()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".container-stock"))
    )
    mark_timer(start,"page loaded in:")
    hide_cookie()

    print(".")
    stock = soup_stock()
    # Now close the store tab
    if stock :
        print(".")
        return stock
    
