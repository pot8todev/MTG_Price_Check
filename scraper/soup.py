
from bs4 import BeautifulSoup
from setup.driver_setup import driver
from setup.objects.classes import Store, Stock, Card
from setup.aux_functions import is_new_store




def tooltip_scrape()  :
    stores_data:list[Store] = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    stores_tooltip = soup.select(".container-tooltip-store-information")

    for store in stores_tooltip:
        name = store.select_one(".store-name span")
        address = store.select_one(".store-address div:last-child")
        phone = store.select_one(".store-phone div:last-child")
        url = store.select_one(".btn-showcase a")

        name = name.get_text(strip=True) if name else ""

        if is_new_store(stores_data, name):
            if url:
                reduced_url = url.get("href")

                if isinstance(reduced_url, str):
                    showcase_url = (
                        "https://www.ligamagic.com.br" + reduced_url[1:]
                    )
                else:
                    showcase_url = None
            else:
                print("no url")
                showcase_url = None

            stores_data.append(
                Store(
                    name=name,
                    address=address.get_text(strip=True) if address else None,
                    tel_num=phone.get_text(strip=True) if phone else None,
                    showcase_url=showcase_url
                )
            )

    return stores_data

# to get cards in stores, stock
def soup_stock():
    stocks:list[Stock] = []
    soup = BeautifulSoup(driver.page_source, "html.parser")

    container = soup.select_one(".container-stock")
    name = soup.select_one(".name-en")
    name = name.get_text(strip=True)if name else ""

    if container is None:
        print("No stock container found")
        return stocks

    for stock in container.select(".stock"):
        price = stock.select_one(".price")
        qnt = stock.select_one(".qnt")
        edition = stock.select_one(".name-ed")
        quality = stock.select_one(".quality")
        language = stock.select_one("img[title]")

        card = Card(
            name=name,
            price=float(price.get_text(strip=True)) if price else None,
            edition=edition.get_text(strip=True) if edition else None,
            quality=str(quality.get("title")) if quality else None,
            language=str(language.get("title")) if language else None
        )

        # XXX: returns -1 if qnt not found, dangerous
        stocks.append(
            Stock(
                card=card,
                qnt=int(qnt.get_text(strip=True)[3:]) if qnt else -1
            )
        )


    return stocks
    return stores_data
