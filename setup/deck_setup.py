from setup.driver_setup import Scraper
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from setup.objects.classes import Wish_card
import os
import json


def fetch_wish_deck(driver)->dict[str,Wish_card]:

    load_dotenv()
    url = os.getenv(
        "TARGET_URL",
        "https://www.ligamagic.com.br/?view=cards/card&card=",
    )

    driver.get(url)
    rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-card-name]")

    wish_deck = {}

    for row in rows:
        quantity = row.get_attribute("data-card-quantity")
        name = row.get_attribute("data-card-name")
        image = row.get_attribute("data-card-image")
        url = row.get_attribute("data-card-url")

        tds = row.find_elements(By.TAG_NAME, "td")

        mana_cost = tds[2].text
        price = tds[3].text

        wish_deck[name] = Wish_card(
            quantity=int(quantity),
            mana_cost=mana_cost,
            price=price,
            image=image,
            url=url,
        )

    return wish_deck

json_path = "setup/deck.json"





def _fetch_Wish_Deck()->dict[str,Wish_card]| None:
    scraper = Scraper()
    try:
        return fetch_wish_deck(scraper.driver)
    finally:
        scraper.close()


# if there is a json, then  skip _fetch_Wish_Deck and export as an object
if os.path.exists(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            deck_data = json.load(f)
            wish_deck = {
                name: Wish_card(
                    quantity=int(wish_card_data["quantity"]),
                    mana_cost=wish_card_data["mana_cost"],
                    price=wish_card_data["price"],
                    image=wish_card_data["image"],
                    url=wish_card_data["url"],
                )
                for name, wish_card_data in deck_data.items()
            }
            
    except json.JSONDecodeError:
        wish_deck = _fetch_Wish_Deck()
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(wish_deck, f, indent=4, ensure_ascii=False)
else:
    wish_deck = _fetch_Wish_Deck()
    if wish_deck:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(wish_deck, f, indent=4, ensure_ascii=False)
