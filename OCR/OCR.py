
import os
import pytesseract
from natsort import natsorted
from PIL import Image


count_total = 0
count_value_error = 0


def get_price(path):
    global count_total, count_value_error

    screenshot_path = os.path.join(path, "screenshots")

    for file in natsorted(os.listdir(screenshot_path)):
        count_total += 1

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
            count_value_error += 1
            message = f"{file} -> {text.strip()}"
            # red to show error
            print(f"\033[31m{message}\033[0m")

            continue
    return count_total, count_value_error
