from playwright.sync_api import sync_playwright
from typing import List, Dict

BASE_URL = "https://voila.ca/categories"

def get_main_categories(page):
    page.goto(BASE_URL)
    page.wait_for_selector('ul li a[data-test="root-category-link"]')

    category_elements = page.query_selector_all('ul li a[data-test="root-category-link"]')

    categories = []
    for el in category_elements:
        name = el.inner_text().strip()
        if name != "Pets":
            continue  # Only consider "Pets" for testing
        href = el.get_attribute("href")
        full_url = "https://voila.ca" + href
        categories.append({
            "name": name,
            "url": full_url
        })
    return categories

def get_all_subcategories(page, category_url: str, depth: int = 0) -> List[Dict]:
    indent = "   " * depth
    try:
        page.goto(category_url)
        page.wait_for_selector('ul li a[data-test="root-category-link"]', timeout=5000)
    except:
        return []

    subcategories = []
    sub_elements = page.query_selector_all('ul li a[data-test="root-category-link"]')
    sub_data = []

    for el in sub_elements:
        try:
            name = el.inner_text().strip()
            href = el.get_attribute("href")
            full_url = "https://voila.ca" + href
            sub_data.append((name, full_url))
        except:
            continue

    for name, full_url in sub_data:
        print(f"{indent}↳ {name}")
        nested_subcategories = get_all_subcategories(page, full_url, depth + 1)
        subcategories.append({
            "name": name,
            "url": full_url,
            "subcategories": nested_subcategories
        })

    return subcategories

def scrape_all_categories():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        all_data = []
        main_categories = get_main_categories(page)

        for category in main_categories:
            print(f"\n📦 Categoria: {category['name']}")
            subcategories = get_all_subcategories(page, category["url"])
            all_data.append({
                "name": category["name"],
                "url": category["url"],
                "subcategories": subcategories
            })

        browser.close()
        return all_data
