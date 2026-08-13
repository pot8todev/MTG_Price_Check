import os
import json
import re

from pathlib import Path
from dataclasses import asdict
from scraper.scraper import get_stores_data
from setup.deck_setup import deck
from setup.driver_setup import Scraper
from setup.aux_functions import start_timer, mark_timer


def sanitize_store_name(name):
    return re.sub(r"[^\w\s-]", "_", name, flags=re.UNICODE).strip()


start = start_timer()

out_path = Path("out")

if  out_path.exists():
    print("skipping scraping...")
else:
    out_path.mkdir()  # create path
    scraper = Scraper()  # start webdriver
    for card_name in deck:
        start2 = start_timer()
        stores_data = get_stores_data(scraper.driver, card_name)
        mark_timer(start2, "scraping this page took:")

        for store in stores_data:
            json_path = out_path / f"{sanitize_store_name(store.name or 'unknown')}.json"
            stock = [asdict(item) for item in store.stock]

            if json_path.exists():
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data.extend(stock)
            else:
                data = stock

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

    mark_timer(start, "whole scraping took")
    scraper.close()

print("encerrando processo")
