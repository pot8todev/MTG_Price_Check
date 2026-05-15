
import os
import shutil
from setup.driver_setup import driver
from scraper import get_images
from OCR.OCR import get_price
from setup.deck_setup import fetchDeck

OUTPUT_DIR = "/out"


def reset_folder(out_path):
    # deletes and recreate a folder
    if os.path.exists(out_path):
        shutil.rmtree(out_path)
    os.makedirs(out_path)


reset_folder(OUTPUT_DIR)

deck = fetchDeck()
card_name = list(deck.keys())


for card_name in deck.keys():
    # card name is the namme of its own folder
    folderName = card_name.title().replace(" ", "")
    card_path = f"out/{folderName}"
    screenshots_path = f"{card_path}/screenshots"

    os.makedirs(card_path)  # ensure exists
    get_images(card_name, screenshots_path)
    get_price(card_path)

driver.quit()
