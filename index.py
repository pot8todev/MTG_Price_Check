import json
from pathlib import Path
from dataclasses import asdict
from scraper.scraper import get_stores_data
from setup.deck_setup import deck
from setup.driver_setup import Scraper
from setup.aux_functions import start_timer, mark_timer


start = start_timer()

out_path = Path("out")

if  out_path.exists():
    print("skipping scraping...")
else:
    scraper = Scraper()  # start webdriver
    for card_name in deck:
        card_folder = card_name.title().replace(" ", "")
        card_folder_path = Path("out") / card_folder

        # Create the card's folder
        card_folder_path.mkdir(parents=True, exist_ok=True)

        json_path = card_folder_path / "stores_data.json"
        start2 = start_timer()
        stores_data = get_stores_data(scraper.driver, card_name, card_folder_path)
        mark_timer(start2, "scraping this page took:")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(
                [asdict(store) for store in stores_data],
                f,
                indent=4,
                ensure_ascii=False
            )
    mark_timer(start, "whole scraping took")
    scraper.close()

print("encerrando processo")
