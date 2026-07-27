from setup.driver_setup import driver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import json


def fetchDeck():

    load_dotenv()
    url = os.getenv(
        "TARGET_URL",  # change target to your mtgGoldfish list
        "https://localhost8000.com/"
    )

    driver.get(url)
    rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-card-name]")

    deck = {}
    for row in rows:
        quantity = row.get_attribute("data-card-quantity")
        name = row.get_attribute("data-card-name")
        image = row.get_attribute("data-card-image")
        url = row.get_attribute("data-card-url")

        tds = row.find_elements(By.TAG_NAME, "td")

        mana_cost = tds[2].text
        price = tds[3].text

        # name is the key value
        deck[name] = {
            "quantity": quantity,
            "mana_cost": mana_cost,
            "price": price,
            "image": image,
            "url": url,
        }
    return deck

if os.path.exists("deck.json"):
    try:
        with open("deck.json", "r", encoding="utf-8") as f:
            deck = json.load(f)
    except json.JSONDecodeError:
        deck = fetchDeck()
        with open("deck.json", "w", encoding="utf-8") as f:
            json.dump(deck, f, indent=4, ensure_ascii=False)
else:
    deck = fetchDeck()
    if deck :
        with open("deck.json", "w", encoding="utf-8") as f:
            json.dump(deck, f, indent=4, ensure_ascii=False)
