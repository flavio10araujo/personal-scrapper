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

def get_categories_structure():
    # Structure for Fruits & Vegetables and Dairy & Eggs with their subcategories
    return [
        [
            # Fruits & Vegetables
            [
                # Fruits
                [
                    f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/apples-pears",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/avocadoes-exotic-fruits",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/bananas-plantains",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/berries-cherries",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/grapes",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/citrus-fruits",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/peaches-nectarines-stone-fruits",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/watermelons-melons",
                ],
                # Vegetables
                [
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/tomatoes-cucumber",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/potatoes-carrots-celery",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/lettuce-leafy-vegetables",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/peppers-zucchini-eggplant",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/broccoli-cauliflower-cabbage",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/mushrooms",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/peas-beans-corn",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/onions-leeks",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/ginger-garlic-shallots",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/squash-pumpkin",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/asparagus-artichokes",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/root-vegetables",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/exotic-vegetables",
                ],
                # Fresh Herbs
                f"{BASE_URL}/en/aisles/fruits-vegetables/fresh-herbs",
                # Packaged Salads & Vegetables
                f"{BASE_URL}/en/aisles/fruits-vegetables/packaged-salads-vegetables",
                # Fresh-Cut Fruits & Vegetables
                f"{BASE_URL}/en/aisles/fruits-vegetables/fresh-cut-fruits-vegetables",
                # Organic Fruits & Vegetables
                f"{BASE_URL}/en/aisles/fruits-vegetables/organic-fruits-vegetables",
                # Dried Fruits & Nuts
                f"{BASE_URL}/en/aisles/fruits-vegetables/dried-fruits-nuts",
                # Vegan & Vegetarian
                [
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegan-vegetarian/tofu-tempeh",
                    f"{BASE_URL}/en/aisles/fruits-vegetables/vegan-vegetarian/vegan-proteins-cheese",
                ],
            ]
        ],
        [
            # Dairy & Eggs
            [
                # Milk, Cream & Butter
                [
                    f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/2-whole-milk",
                    f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/1-skim-milk",
                    f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/cream-creamers",
                    f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/flavoured-milk",
                    f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/lactose-free-non-dairy-milk",
                    f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/fermented-milk-kefir",
                    f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/butter-margarine",
                ],
                # Eggs
                [
                    f"{BASE_URL}/en/aisles/dairy-eggs/eggs/whole-eggs",
                    f"{BASE_URL}/en/aisles/dairy-eggs/eggs/liquid-eggs-egg-whites",
                    f"{BASE_URL}/en/aisles/dairy-eggs/eggs/organic-eggs",
                ],
                # Yogurt
                [
                    f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/yogurt-tubs",
                    f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/multipacks",
                    f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/greek-yogurts",
                    f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/drinkable-yogurts",
                    f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/probiotic-yogurts",
                    f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/single-serving-yogurts",
                ],
                # Packaged Cheese
                [
                    f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/fondue",
                    f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/shredded-cheese",
                    f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/cream-cheese-spreads",
                    f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/strings-snacks",
                    f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/cheese-blocks",
                    f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/sliced-cheese",
                    f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/cottage-cheese-ricotta",
                ],
                # Deli Cheese
                [
                    f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/soft-fresh",
                    f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/firm-semi-soft",
                    f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/mozzarella-feta",
                    f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/cheddar",
                    f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/parmesan",
                    f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/goat-sheep",
                    f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/swiss-gouda-jarlsberg",
                    f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/blue-cheese-rocquefort",
                    f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/grated-sliced",
                ],
                # Sour Cream & Dips
                [
                    f"{BASE_URL}/en/aisles/dairy-eggs/sour-cream-dips/sour-cream",
                    f"{BASE_URL}/en/aisles/dairy-eggs/sour-cream-dips/chilled-dips",
                ],
                # Chilled Desserts & Dough
                [
                    f"{BASE_URL}/en/aisles/dairy-eggs/chilled-desserts-dough/dessert-cups",
                    f"{BASE_URL}/en/aisles/dairy-eggs/chilled-desserts-dough/chilled-dough",
                    f"{BASE_URL}/en/aisles/dairy-eggs/chilled-desserts-dough/whipped-cream",
                ],
            ]
        ],
        # Other main categories as leaf URLs
        f"{BASE_URL}/en/aisle/000010",  # Pantry
        # ... add more as needed ...
    ]

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
