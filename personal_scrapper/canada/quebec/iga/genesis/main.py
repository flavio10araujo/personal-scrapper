import json
from datetime import datetime
from personal_scrapper.canada.quebec.iga.genesis.scrapper import scrape_all_categories

if __name__ == "__main__":
    data = scrape_all_categories()
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    filename = f"{timestamp}-iga.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

