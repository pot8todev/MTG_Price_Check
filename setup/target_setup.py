from setup.driver_setup import driver
from selenium.webdriver.common.by import By


# hard codded entry to get the deck list


def fetchDeck():

    url = "https://www.mtggoldfish.com/archetype/pauper-madness-burn#paper"
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
        }
    return deck
