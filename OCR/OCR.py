
import os
import pytesseract
from natsort import natsorted
from PIL import Image

from setup.deck_setup import deck


def get_price(path):
    screenshot_path = os.path.join(path, "screenshots")

    for file in natsorted(os.listdir(screenshot_path)):

        if file.endswith(".png"):

            img_path = os.path.join(screenshot_path, file)

        text = pytesseract.image_to_string(
            Image.open(img_path),
            config="--psm 10 -c tessedit_char_whitelist=0123456789"
        )
        try:
            price = float(text.strip())/100

            message = f"{file} -> {price}"

            print(f"\033[34m{message}\033[0m")
            with open(f"{path}/prices.txt", "a", encoding="utf-8") as f:
                f.write(f"|{price:8.2f}|\n")

        except ValueError:
            message = f"{file} -> {text.strip()}"
            # red to show error
            print(f"\033[31m{message}\033[0m")
            continue
