import os
import json
from datetime import datetime
from scraper.scraper import get_stores_data
from setup.deck_setup import deck
from setup.driver_setup import driver

for card_name in deck:
    # card name is its own folder's name
    folderName = card_name.title().replace(" ", "")
    card_folder = f"out/{folderName}"
    os.makedirs(card_folder)  # ensure exists
    store_data = get_stores_data(card_name)

    json_path = f"{card_folder}/stores_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(store_data, f, indent=4, ensure_ascii=False)

print("encerrando processo")
driver.quit()
