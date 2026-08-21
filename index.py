import json
import csv

from pathlib import Path
from dataclasses import asdict
from scraper.scraper import get_stores_data
from setup.deck_setup import wish_deck
from setup.driver_setup import Scraper
from setup.aux_functions import start_timer, mark_timer, sanitize_store_name
from setup.objects.classes import Store,Stock,Card

    
def write_stock_csv( csv_path: Path):
    stores_data = []
    stores:list[Store]=[]

# Get all stores from JSON
    for json_file in csv_path.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            stores_data.append(json.load(f))

    if not stores_data:
        return

    for data in stores_data:
        stock = [
            Stock(
                card=Card(
                    name=item["card"]["name"],
                    price=item["card"].get("price"),
                    edition=item["card"].get("edition"),
                    quality=item["card"].get("quality"),
                    language=item["card"].get("language"),
                    url=item["card"].get("url"),
                ),
                qnt=item["qnt"],
            )
            for item in data.get("stock", [])
        ]

        stores.append(
            Store(
                name=data["name"],
                address=data["address"],
                tel_num=data["tel_num"],
                showcase_url=data["showcase_url"],
                diversity=data["diversity"],
                stock=stock,
            )
        )

    sorted_stores = sorted(
        stores,
        key=lambda store: store.diversity,
        reverse=True
    )

    stores = sorted_stores[:50]
    all_cards = set()
    store_quantities = {}

    for store in stores:
        quantities = {}

        for item in store.stock:
            card_name = item.card.name

            if not card_name:
                continue

            quantities[card_name] = quantities.get(card_name, 0) + item.qnt
            all_cards.add(card_name)

        store_quantities[store.name] = quantities

    cards = sorted(all_cards)


    csv_file = csv_path / "stock.csv"

    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            "store name",
            "store diversity",
            *cards
        ])

        # One row per store
        for store in stores:
            quantities = store_quantities[store.name]

            row = [
                store.name,
                store.diversity,
                *[quantities.get(card, 0) for card in cards]
            ]

            writer.writerow(row)



    

    

def write_json(store:Store, json_path):
    
    stock = [asdict(item) for item in store.stock]
    #if already exists a json with this stores name, then:
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if stock:
                #if a store is called for having more than 1 card, inc their diversity
                data["diversity"] += 1
                #if it has the whole order os wish_deck, mark it
                # if has_the_whole_card_order(wish_card_name,wish_deck[wish_card_name], store):
        data["stock"].extend(stock)

    else:
        data ={
            "name": store.name,
            "address": store.address,
            "tel_num":store.tel_num,
            "showcase_url": store.showcase_url,
            "diversity": 1,
            "stock": stock
        }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return data

start = start_timer()

out_path = Path("out")

all_stores_data = []
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
                if not json_path.exists():
                    all_stores_data.append(store)

                store_data = write_json(store,json_path)

    mark_timer(start, "whole scraping took")
    scraper.close()


write_stock_csv(out_path)



print("encerrando processo")
