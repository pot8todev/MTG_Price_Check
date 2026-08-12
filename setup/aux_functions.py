from setup.driver_setup import driver
from selenium.webdriver.common.by import By
from setup.objects.classes import Card,Stock,Store
import time


def hide_cookie():
    driver.execute_script(
        "document.getElementById('lgpd-cookie').style.display = 'none';"
    )

def is_new_store(stores_data:list[Store], name:str):
    for store in stores_data:
        if store.name == name:
            return False
    return True

