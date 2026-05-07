
import os
import pytesseract

from PIL import Image


def get_price(folder):

    for file in os.listdir(folder):

        if file.endswith(".png"):

            path = os.path.join(folder, file)

            text = pytesseract.image_to_string(
                Image.open(path),
                config="--psm 10 digits"
            )

        text = pytesseract.image_to_string(
            Image.open(path),
            config="--psm 10 -c tessedit_char_whitelist=0123456789"
        )
        try:
            price = float(text.strip())

            if price > 50:
                price = price / 100
                print(file, "->", price)
        except ValueError:
            print(file, "->", "????")
            continue
