from bs4 import BeautifulSoup
from setup.driver_setup import driver


# to get edition and quality
def showcase_cards_info_soup():
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

def is_new_store(stores_data, name):
    for store in  stores_data:
        if store["name"] == name:
            return False
    return True

def tooltip_scrape(stores_data):

    soup = BeautifulSoup(driver.page_source, "html.parser")
    stores = soup.select(".container-tooltip-store-information")

    for store in stores:
        name = store.select_one(".store-name span")
        address = store.select_one(".store-address div:last-child")
        phone = store.select_one(".store-phone div:last-child")
        url = store.select_one(".btn-showcase a")

        name = name.get_text(strip=True) if name else ""

        if is_new_store(stores_data, name):
            if url:
                reduced_url = url.get("href")
                if isinstance(reduced_url, str):
                    showcase_url = "https://www.ligamagic.com.br" + reduced_url[1:]
                else:
                    showcase_url = None
            else:
                print("no url")
                showcase_url = None
            stores_data.append(
                {
                    "name": name,
                    "address": address.get_text(strip=True) if address else "",
                    "phone": phone.get_text(strip=True) if phone else "(xx)xxxx-xxx",
                    "showcase_url":showcase_url

                }
            )

    return stores_data
