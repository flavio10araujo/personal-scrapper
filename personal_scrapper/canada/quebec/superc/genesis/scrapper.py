from playwright.sync_api import sync_playwright, ViewportSize
from typing import List, Dict
import re

BASE_URL = "https://www.superc.ca"

# Global set to track seen SKUs
seen_skus = set()

def get_main_categories(page):
    # Categories as per page1.html "Aisles" menu
    categories = [
        {"name": "Fruits & Vegetables", "url": f"{BASE_URL}/en/aisle/000006"},
        {"name": "Dairy & Eggs", "url": f"{BASE_URL}/en/aisle/000008"},
        {"name": "Pantry", "url": f"{BASE_URL}/en/aisle/000010"},
        {"name": "Cooked Meals", "url": f"{BASE_URL}/en/aisle/000025"},
        {"name": "Value Pack", "url": f"{BASE_URL}/en/aisle/000026"},
        {"name": "Beverages", "url": f"{BASE_URL}/en/aisle/000002"},
        {"name": "Beer & Wine", "url": f"{BASE_URL}/en/aisle/000018"},
        {"name": "Meat & Poultry", "url": f"{BASE_URL}/en/aisle/000001"},
        {"name": "Vegan & Vegetarian Food", "url": f"{BASE_URL}/en/aisle/000021"},
        {"name": "Organic Groceries", "url": f"{BASE_URL}/en/aisle/000017"},
        {"name": "Snacks", "url": f"{BASE_URL}/en/aisle/000013"},
        {"name": "Frozen", "url": f"{BASE_URL}/en/aisle/000011"},
        {"name": "Bread & Bakery Products", "url": f"{BASE_URL}/en/aisle/000012"},
        {"name": "Deli & Prepared Meals", "url": f"{BASE_URL}/en/aisle/000009"},
        {"name": "Fish & Seafood", "url": f"{BASE_URL}/en/aisle/000007"},
        {"name": "World Cuisine", "url": f"{BASE_URL}/en/aisle/000019"},
        {"name": "Household & Cleaning", "url": f"{BASE_URL}/en/aisle/000014"},
        {"name": "Baby", "url": f"{BASE_URL}/en/aisle/000020"},
        {"name": "Health & Beauty", "url": f"{BASE_URL}/en/aisle/000005"},
        {"name": "Pet Care", "url": f"{BASE_URL}/en/aisle/000003"},
        {"name": "Pharmacy", "url": f"{BASE_URL}/en/aisle/000015"},
        {"name": "Nature's Signature", "url": f"{BASE_URL}/en/aisle/000022"},
        {"name": "Lottery Tickets", "url": f"{BASE_URL}/en/aisle/LQ01"},
    ]
    return categories

def scrape_all_categories():
    global seen_skus
    seen_skus = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        viewport: ViewportSize = {"width": 32767, "height": 32767}
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            viewport=viewport
        )
        page = context.new_page()

        all_data = []
        main_categories = get_main_categories(page)

        for category in main_categories:
            print(f"\n📦 Category: {category['name']}")
            #subcategories = get_all_subcategories(page, category["url"])
            #products = extract_products_from_category(page, category["url"], category["name"])

            #all_data.append({
            #    "id": extract_category_id(category["url"]),
            #    "name": category["name"],
            #    "url": category["url"],
            #    "subcategories": subcategories,
            #    "products": products
            #})

        browser.close()
        return { "categories": all_data }
