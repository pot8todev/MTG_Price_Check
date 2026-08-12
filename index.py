import os
import json

from pathlib import Path
from dataclasses import asdict
from scraper.scraper import get_stores_data
from setup.deck_setup import deck
from setup.driver_setup import start_driver
from setup.aux_functions import start_timer, mark_timer


start = start_timer()

out_path = Path("out")

if  out_path.exists():
    print("skipping scraping...")
else:
    out_path.mkdir()  # create path
    driver = start_driver() #start wedriver
    for card_name in deck:
        # card name is its own folder's name
        folderName = card_name.title().replace(" ", "")
        card_folder = f"out/{folderName}"
        start2 = start_timer()
        stores_data = get_stores_data(card_name, card_folder, driver)
        mark_timer(start2, "scraping this page took:")

        json_path = f"{card_folder}/stores_data.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(
                [asdict(store) for store in stores_data],
                f,
                indent=4,
                ensure_ascii=False
            )
    mark_timer(start, "whole scraping took")

print("encerrando processo")
driver.quit()
