
from setup.driver_setup import driver
from scraper import get_images
from OCR import get_price

targets = ["sneaky snacker", "lightning bolt",
           "fiery temper", "highway robbery"]

for target in targets:
    path = f"out/{target.title().replace(" ", "")}/screenshots"
    get_images(target, path)
    get_price(path)

driver.quit()
