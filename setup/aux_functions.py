from setup.driver_setup import driver
from selenium.webdriver.common.by import By
import time


def hide_cookie():
    driver.execute_script(
        "document.getElementById('lgpd-cookie').style.display = 'none';"
    )


def screenshot_data(out):
    prices_html = driver.find_elements(By.CSS_SELECTOR,
                                       ".store .price-with-image")
    qnts_html = driver.find_elements(By.CSS_SELECTOR,
                                     ".store .quantity-with-image")

    for i, (price, qnt) in enumerate(zip(prices_html, qnts_html)):
        time.sleep(1)

        # Role a página até o elemento p e coloque ele no centro da tela.
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", price)
        price.screenshot(f"{out}/prices/price{i}.png")
        qnt.screenshot(f"{out}/quantities/qnt{i}.png")
