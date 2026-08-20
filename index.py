import json

from pathlib import Path
from dataclasses import asdict
from scraper.scraper import get_stores_data
from setup.deck_setup import wish_deck
from setup.driver_setup import Scraper
from setup.aux_functions import start_timer, mark_timer, sanitize_store_name

    


    

start = start_timer()

out_path = Path("out")

if  out_path.exists():
    print("skipping scraping...")
else:
    out_path.mkdir()  # create path
    scraper = Scraper()  # start webdriver
    if wish_deck:
        for wish_card_name in wish_deck:
            start2 = start_timer()
            #search for the card name in the stores
            stores_data = get_stores_data(scraper.driver, wish_card_name)
            mark_timer(start2, "scraping this page took:")

            #stores that have that card are updated/added
            for store in stores_data:
                json_path = out_path / f"{sanitize_store_name(store.name or 'unknown')}.json"
                stock = [asdict(item) for item in store.stock]

                
                if json_path.exists():
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if stock:
                            #if a store is called for having more than 1 card, inc their diversity
                            data["diversity"] += 1
                            #if it has the whole order os wish_deck, mark it
                            # if has_the_whole_card_order(wish_card_name,wish_deck[wish_card_name], store):
                            #     print("hello")

                    data["stock"].extend(stock)

                else:
                    data ={
                        "name": store.name,
                        "address": store.address,
                        "showcase_url": store.showcase_url,
                        "diversity": 1,
                        "stock": stock
                    }
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

    mark_timer(start, "whole scraping took")
    scraper.close()


print("encerrando processo")
