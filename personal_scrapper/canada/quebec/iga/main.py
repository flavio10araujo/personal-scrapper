import json
from personal_scrapper.canada.quebec.iga.scrapperV2 import scrape_all_categories

if __name__ == "__main__":
    data = scrape_all_categories()
    with open("voila_categories_pets.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

