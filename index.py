
from setup.driver_setup import driver
from scraper import get_images
from OCR import get_price
from setup.target_setup import fetchDeck

deck = fetchDeck()
targets = list(deck.keys())

for target in targets:
    # card name is the namme of its own folder
    folderName = target.title().replace(" ", "")

    path = f"out/{folderName}/screenshots"
    get_images(target, path)
    get_price(path)

driver.quit()
