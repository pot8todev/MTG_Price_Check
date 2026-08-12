from setup.driver_setup import driver
from setup.objects.classes import Card,Stock,Store
import time


def hide_cookie():
    driver.execute_script(
        "document.getElementById('lgpd-cookie').style.display = 'none';"
    )

def is_new_store(stores_data:list[Store], name:str):
    for store in stores_data:
        if store.name == name:
            return False
    return True
def parse_price(price_element) -> float | None:
    if not price_element:
        return None

    text = price_element.get_text(strip=True)
    text = text.replace("R$", "").strip()
    text = text.replace(".", "").replace(",", ".")
    text = text.split()[-1]
    text.find(" ")

    print(text)

    return float(text)
def parse_qnt(qnt_element) -> int | None:
    if not qnt_element:
        return None

    text = qnt_element.get_text(strip=True)
    text = text.replace("de", "").strip()
    text = text.replace(" ", "")
    text = text.split()[-1]
    text.find(" ")
    print(text)


    return int(text)
