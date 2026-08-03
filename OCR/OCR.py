import os
import pytesseract
from natsort import natsorted
from PIL import Image


count_total = 0
count_value_error = 0


def get_price(path):
    global count_total, count_value_error
    prices = []
    qnts = []

    prices_path = os.path.join(path, "prices")
    qnts_path = os.path.join(path, "quantities")

    for file in natsorted(os.listdir(prices_path)):
        count_total += 1

        if file.endswith(".png"):
            img_path = os.path.join(prices_path, file)

        text = pytesseract.image_to_string(
            Image.open(img_path),
            config="--psm 10 -c tessedit_char_whitelist=0123456789",
        )

        # try to figure the number
        try:
            price = float(text.strip()) / 100

            # Append dictionary entry
            prices.append(price)

            message = f"{file} -> {price}"

            print(f"\033[34m{message}\033[0m")

            # Save back to the JSON file

        except ValueError:
            prices.append("?")  # signaling error

            count_value_error += 1
            message = f"{file} -> {text.strip()}"
            # red to show error
            print(f"\033[31m{message}\033[0m")
            continue

    for file in natsorted(os.listdir(qnts_path)):
        count_total += 1

        if file.endswith(".png"):
            img_path = os.path.join(qnts_path, file)

        text = pytesseract.image_to_string(
            Image.open(img_path),
            config="--psm 10 -c tessedit_char_whitelist=0123456789",
        )

        try:
            qnt = int(text.strip())
            # Append dictionary entry
            qnts.append(qnt)

            message = f"{file} -> {qnt}"
            print(f"\033[34m{message}\033[0m")
        except ValueError:
            qnts.append("?")  # signaling error
            count_value_error += 1
            message = f"{file} -> {text.strip()}"
            # red to show error
            print(f"\033[31m{message}\033[0m")

            continue
        # try to figure the number
    return count_total, count_value_error, qnts, prices
