
import os
import shutil
from setup.driver_setup import driver
from scraper import get_images
from OCR.OCR import get_price
from setup.target_setup import fetchDeck


def reset_folder(out_path):
    # Reset folder
    if os.path.exists(out_path):
        shutil.rmtree(out_path)
    os.makedirs(out_path)


reset_folder("out/")

deck = fetchDeck()
targets = list(deck.keys())


for target in targets:
    # card name is the namme of its own folder
    folderName = target.title().replace(" ", "")
    path = f"out/{folderName}/screenshots"

    os.makedirs(path)  # ensure exists
    get_images(target, path)
    get_price(path)

driver.quit()
