
import os
import pytesseract

from PIL import Image


def get_price(folder):

    for file in os.listdir(folder):

        if file.endswith(".png"):

            path = os.path.join(folder, file)

        text = pytesseract.image_to_string(
            Image.open(path),
            config="--psm 10 -c tessedit_char_whitelist=0123456789"
        )
        try:
            price = float(text.strip())

            # hard coded
            if price > 50:
                price = price / 100
                print(file, "->", price)
            print(f"\033[34m{file} -> {text.strip()}\033[0m")
        except ValueError:
            # red to show error
            print(f"\033[31m{file} -> {text.strip()}\033[0m")
            continue
