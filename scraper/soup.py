from bs4 import BeautifulSoup
from setup.driver_setup import driver


# to get addresses
def tooltip_scrape():

    soup = BeautifulSoup(driver.page_source, "html.parser")
    stores = soup.select(".container-tooltip-store-information")
    store_data = []

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

    print(store_data)
