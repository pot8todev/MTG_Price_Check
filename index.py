
import os
from setup.driver_setup import driver
from scraper import get_stores_data
from OCR.OCR import get_price
from setup.deck_setup import deck

for card_name in deck.keys():

    # card name is its own folder's name
    folderName = card_name.title().replace(" ", "")
    card_path = f"out/{folderName}"
    screenshots_path = f"{card_path}/screenshots"

    os.makedirs(card_path)  # ensure exists
    get_stores_data(card_name, screenshots_path)
    count_total, count_value_error = get_price(card_path)

    print(f"\nerros: {count_value_error}/{count_total}")
print("encerrando processo")
driver.quit()
