from bs4 import BeautifulSoup
from setup.driver_setup import driver


# to get addresses
def showcase_cards_per_store():
    cards = []

    soup = BeautifulSoup(driver.page_source, "html.parser")

    container = soup.select_one(".container-stock")

    if container is None:
        print("No stock container found")
        return cards

    for stock in container.select(".stock"):
        edition = stock.select_one(".name-ed")
        quality = stock.select_one(".quality")

        cards.append(
            {
                "edition": edition.get_text(strip=True) if edition else None,
                "quality": quality.get("title") if quality else None,
            }
        )

        print(cards[-1])

    return cards


def tooltip_scrape(store_data):

    soup = BeautifulSoup(driver.page_source, "html.parser")
    stores = soup.select(".container-tooltip-store-information")

    for store in stores:
        name = store.select_one(".store-name span")
        address = store.select_one(".store-address div:last-child")
        phone = store.select_one(".store-phone div:last-child")

        store_data.append(
            {
                "name": name.get_text(strip=True) if name else None,
                "address": address.get_text(strip=True) if address else None,
                "phone": phone.get_text(strip=True) if phone else None,
            }
        )

    return store_data
