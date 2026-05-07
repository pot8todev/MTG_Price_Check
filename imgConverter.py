
import os
import pytesseract

from PIL import Image

folder = "screenshots"

for file in os.listdir(folder):

    if file.endswith(".png"):

        path = os.path.join(folder, file)

        text = pytesseract.image_to_string(
            Image.open(path),
            config="--psm 10 digits"
        )

        print(file, "->", text.strip())
