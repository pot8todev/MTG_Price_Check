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

    # print(text)

    return float(text)
def parse_qnt(qnt_element) -> int :

    text = qnt_element.get_text(strip=True)
    text = text.replace("de", "").strip()
    text = text.replace(" ", "")
    text = text.split()[-1]
    text.find(" ")
    # print(text)

    text = int(text)
    text = text if text is not None else -1
    return text


def start_timer()->float:
    return time.perf_counter()
def mark_timer(start:float, message:str|None):
    print(f"{message} {time.perf_counter() - start:.4f}s")
def function_timer(f, message:str|None) :
    start = start_timer()
    out = f()
    mark_timer(start,message)
    return out
    




