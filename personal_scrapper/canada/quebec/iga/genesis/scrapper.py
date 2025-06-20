from playwright.sync_api import sync_playwright, ViewportSize
from typing import List, Dict
import re

BASE_URL = "https://voila.ca/categories"

# Global set to track seen SKUs
seen_skus = set()

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
        products = extract_products_from_category(page, full_url, name)
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

def extract_products_from_category(page, category_url: str, category_name: str, max_scrolls: int = 100) -> List[Dict]:
    global seen_skus
    page.goto(category_url)
    page.wait_for_selector('.product-card-container', timeout=5000)

    products_temp = []
    product_data = []

    for _ in range(max_scrolls):
        wrappers = page.query_selector_all('.product-card-container')
        for wrapper in wrappers:
            try:
                link_el = wrapper.query_selector('a[data-test="fop-product-link"]')
                href = link_el.get_attribute("href") if link_el else ""
                if not href:
                    continue
                sku = href.strip("/").split("/")[-1]
                if sku in seen_skus:
                    continue
                seen_skus.add(sku)

                name_el = wrapper.query_selector('h3[data-test="fop-title"]')
                name = name_el.inner_text().strip() if name_el else ""

                url = "https://voila.ca" + href
                size_el = wrapper.query_selector('div[data-test="fop-size"] span')
                quantity = size_el.inner_text().strip() if size_el else ""

                price_el = wrapper.query_selector('span[data-test="fop-price"]')
                price = price_el.inner_text().strip() if price_el else ""

                products_temp.append({
                    "name": name,
                    "url": url,
                    "sku": sku,
                    "quantity": quantity,
                    "price": price
                })
            except Exception as e:
                print(f"⚠️ Erro na extração: {e}")

        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(1500)

        height = page.evaluate("document.body.scrollHeight")
        if hasattr(extract_products_from_category, "_last_height") and extract_products_from_category._last_height == height:
            break
        extract_products_from_category._last_height = height

    for prod in products_temp:
        try:
            brand = ""
            if prod["url"]:
                page.goto(prod["url"])
                page.wait_for_selector("h1", timeout=8000)

                brand_label = page.query_selector('h2:text("Brand")')
                brand_el = brand_label.evaluate_handle("el => el.nextElementSibling") if brand_label else None
                brand = brand_el.inner_text().strip() if brand_el else ""

            product_data.append({
                "name":  brand + " " + category_name,
                "language": "en",
                "brand": brand,
                "gpc_code": "",
                "variations": [
                    {
                        "name": prod["name"],
                        "url": prod["url"],
                        "sku": prod["sku"],
                        "quantity": prod["quantity"],
                        "price": prod["price"]
                    }
                ]
            })

            print(f"✔️ {prod['name']} | {prod['quantity']} | {prod['price']} | {brand} | {prod['sku']}")

        except Exception as e:
            print(f"⚠️ Erro no produto {prod['url']}: {e}")

    return product_data

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
            subcategories = get_all_subcategories(page, category["url"])
            products = extract_products_from_category(page, category["url"], category["name"])

            all_data.append({
                "id": extract_category_id(category["url"]),
                "name": category["name"],
                "url": category["url"],
                "subcategories": subcategories,
                "products": products
            })

        browser.close()
        return { "categories": all_data }
