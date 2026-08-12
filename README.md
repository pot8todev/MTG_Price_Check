# MTG Deck Scraper
A Python scraper for extracting Magic: The Gathering decklists from MTGGoldfish.

## 📦 Setup (macOS / Linux)
Create and activate a virtual environment:


``` bash
python -m venv venv
source "$(pwd)/.venv/bin/activate"
```

Install dependencies:

```bash
pip install -r setup/requirements.txt
```


## ⚙️ Configuration
### 🌐 Using your Chrome profile with Selenium
To allow Selenium to reuse your logged-in Chrome session
(for example, to bypass repeated logins or Cloudflare checks),
start Chrome with remote debugging enabled.


```bash
BASE_URL="https://www.ligamagic.com.br/?view=cards/card&card="
TARGET_URL=<yourMtgGoldfishURLhere>
```

Notes:
BASE_URL → used for card lookup (LigaMagic integration)

TARGET_URL → MTGGoldfish deck or archetype page to scrape
## 🚀 Running the scraper
Run the project with:

```
python index.py
```




