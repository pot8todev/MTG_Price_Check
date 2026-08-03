import os
import json
from datetime import datetime
from OCR.OCR import get_price
from scraper import get_stores_data
from setup.deck_setup import deck
from setup.driver_setup import driver

for card_name in deck.keys():
    # card name is its own folder's name
    folderName = card_name.title().replace(" ", "")
    card_folder = f"out/{folderName}"
    screenshots_folder = f"{card_folder}/screenshots"

    os.makedirs(card_folder)  # ensure exists
    store_names = get_stores_data(card_name, screenshots_folder)
    count_total, count_errors, qnts, prices = get_price(screenshots_folder)

    print(len(store_names))
    print(len(qnts))
    print(len(prices))

    data = []
    for i in range(len(prices)):
        data.append(
            {
                "store_name": store_names[i],
                "price": prices[i],
                "qnt": qnts[i],
                "timestamp": datetime.now().isoformat(),
            }
        )
    json_path = f"{card_folder}/stores_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    data = []

    # print(f"\nerros: {count_errors}/{count_total}")
    print("pulando pra o fim")
    break
print("encerrando processo")
driver.quit()
