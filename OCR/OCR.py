
import os
import pytesseract
from natsort import natsorted

from PIL import Image


def get_price(file_path):

    for file in natsorted(os.listdir(file_path)):

        if file.endswith(".png"):

            path = os.path.join(file_path, file)

        text = pytesseract.image_to_string(
            Image.open(path),
            config="--psm 10 -c tessedit_char_whitelist=0123456789"
        )
        message = f"{file} -> {text.strip()}"
        try:
            price = float(text.strip())

            # # hard coded
            # if price > 50:
            #     price = price / 100
            #     print(file, "->", price)
            print(f"\033[34m{message}\033[0m")
            with open(f"{file_path}/prices.txt", "a", encoding="utf-8") as f:
                f.write(f"{price/100}" + "\n")
        except ValueError:
            # red to show error
            print(f"\033[31m{message}\033[0m")
            continue
