from playwright.sync_api import sync_playwright
from typing import List, Dict
import re

BASE_URL = "https://voila.ca/categories"

def get_main_categories(page):
    page.goto(BASE_URL)
    page.wait_for_selector('ul li a[data-test="root-category-link"]')

    category_elements = page.query_selector_all('ul li a[data-test="root-category-link"]')

    allowed_categories = [
    #    "Fresh Fruits & Vegetables",
    #    "Meat & Seafood",
    #    "Dairy & Eggs",
    #    "Cheese",
    #    "Bread & Bakery",
    #    "Deli",
    #    "Prepared Meals & Sides",
    #    "Frozen Foods",
    #    "Pantry",
    #    "Snacks & Candy",
    #    "Beverages",
    #    "Plant Based",
    #    "Baby",
    #    "Health & Beauty",
    #    "Household Products",
        "Pets"
    #    "Floral & Garden"
    ]

    categories = []
    for el in category_elements:
        name = el.inner_text().strip()
        if name not in allowed_categories:
            continue
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

    subcategories = []
    for name, full_url in sub_data:
        print(f"{indent}↳ {name}")
        nested = get_all_subcategories(page, full_url, depth + 1)
        products = extract_products_from_category(page, full_url)
        subcategories.append({
            "id": extract_category_id(full_url),
            "name": name,
            "url": full_url,
            "subcategories": nested,
            "products": products
        })

    return subcategories

def extract_category_id(url: str) -> str:
    match = re.search(r'/WEB(\d+)', url)
    return f"WEB{match.group(1)}" if match else ""

def extract_products_from_category(page, category_url: str, max_scrolls: int = 10) -> List[Dict]:
    page.goto(category_url)
    products = set()
    last_height = 0

    for _ in range(max_scrolls):
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(1000)  # aguarda carregar

        product_elements = page.query_selector_all('a[href^="/products/"]')
        for el in product_elements:
            href = el.get_attribute("href")
            if href and href.startswith("/products/"):
                products.add("https://voila.ca" + href)

        # Verifica se chegou ao fim (não carrega mais)
        height = page.evaluate("document.body.scrollHeight")
        if height == last_height:
            break
        last_height = height

    product_data = []
    for url in sorted(products):
        try:
            page.goto(url)
            page.wait_for_selector("h1", timeout=5000)

            name_el = page.query_selector("h1")
            quantity_el = page.query_selector('div[data-test="size-container"] span[aria-hidden="true"]')
            price_el = page.query_selector('div[data-test="price-container"] span')

            brand_label = page.query_selector('h2:text("Brand")')
            brand_el = brand_label.evaluate_handle("el => el.nextElementSibling") if brand_label else None

            if not name_el or not quantity_el or not price_el:
                print(f"⚠️ Dados incompletos: {url}")
                continue

            name = name_el.inner_text().strip()
            quantity = quantity_el.inner_text().strip()
            price = price_el.inner_text().strip()
            brand = brand_el.inner_text().strip() if brand_el else ""

            sku = url.strip("/").split("/")[-1]

            product_data.append({
                "url": url,
                "sku": sku,
                "name": name,
                "quantity": quantity,
                "price": price,
                "brand": brand
            })
        except Exception as e:
            print(f"Erro ao extrair produto: {url} -> {e}")

    return product_data

def scrape_all_categories():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        all_data = []
        main_categories = get_main_categories(page)

        for category in main_categories:
            print(f"\n📦 Categoria: {category['name']}")
            subcategories = get_all_subcategories(page, category["url"])
            products = extract_products_from_category(page, category["url"])

            all_data.append({
                "id": extract_category_id(category["url"]),
                "name": category["name"],
                "url": category["url"],
                "subcategories": subcategories,
                "products": products
            })

        browser.close()
        return { "categories": all_data }
