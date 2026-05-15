
import os
from setup.driver_setup import driver
from scraper import get_images
from OCR.OCR import get_price
from setup.deck_setup import deck

for card_name in deck.keys():

    # card name is its own folder's name
    folderName = card_name.title().replace(" ", "")
    card_path = f"out/{folderName}"
    screenshots_path = f"{card_path}/screenshots"

    os.makedirs(card_path)  # ensure exists
    get_images(card_name, screenshots_path)
    get_price(card_path)

driver.quit()
