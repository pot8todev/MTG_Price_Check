
import os
import json
from datetime import datetime
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
            json_path = f"{path}/prices.json"
            if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
                with open(json_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []

# Append dictionary entry
            data.append({
                "price": price,
                "store_name" : " ",
                "qnt" : 0,
                "timestamp": datetime.now().isoformat()
            })

            message = f"{file} -> {price}"

            print(f"\033[34m{message}\033[0m")

                # Save back to the JSON file
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

        except ValueError:
            count_value_error += 1
            message = f"{file} -> {text.strip()}"
            # red to show error
            print(f"\033[31m{message}\033[0m")

            continue
    return count_total, count_value_error
