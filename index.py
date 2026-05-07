
from scraper import get_images
from imgConverter import get_price

target = "sneaky snacker"
folder = f"out/{target.title().replace(" ", "")}/screenshots"

get_images(target, folder)
get_price(folder)
