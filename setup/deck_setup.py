from setup.driver_setup import Scraper
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import json


def fetchDeck(driver):

    load_dotenv()
    url = os.getenv(
        "TARGET_URL",  # change target to your mtgGoldfish list
        "https://localhost8000.com/",
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


json_path = "setup/deck.json"


def _fetch_deck():
    scraper = Scraper()
    try:
        return fetchDeck(scraper.driver)
    finally:
        scraper.close()


if os.path.exists(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            deck = json.load(f)
    except json.JSONDecodeError:
        deck = _fetch_deck()
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(deck, f, indent=4, ensure_ascii=False)
else:
    deck = _fetch_deck()
    if deck:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(deck, f, indent=4, ensure_ascii=False)
