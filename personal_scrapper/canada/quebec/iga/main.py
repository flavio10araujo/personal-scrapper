from personal_scrapper.canada.quebec.iga.scrapper import get_main_categories

if __name__ == "__main__":
    categories = get_main_categories()
    for cat in categories:
        print(f"{cat['name']} -> {cat['url']}")
