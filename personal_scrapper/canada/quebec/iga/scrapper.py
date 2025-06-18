from playwright.sync_api import sync_playwright

BASE_URL = "https://voila.ca/categories"

def get_main_categories(page):
    page.goto(BASE_URL)
    page.wait_for_selector('ul li a[data-test="root-category-link"]')

    category_elements = page.query_selector_all('ul li a[data-test="root-category-link"]')

    categories = []
    for el in category_elements:
        name = el.inner_text().strip()
        href = el.get_attribute("href")
        full_url = "https://voila.ca" + href
        categories.append({
            "name": name,
            "url": full_url
        })
    return categories

def get_subcategories(page, category_url):
    page.goto(category_url)
    try:
        page.wait_for_selector('ul li a[data-test="root-category-link"]', timeout=5000)
    except:
        return []  # Categoria sem subcategorias

    sub_elements = page.query_selector_all('ul li a[data-test="root-category-link"]')
    subcategories = []

    for el in sub_elements:
        name = el.inner_text().strip()
        href = el.get_attribute("href")
        full_url = "https://voila.ca" + href
        subcategories.append({
            "name": name,
            "url": full_url
        })

    return subcategories

def scrape_categories_and_subcategories():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        all_data = []
        categories = get_main_categories(page)

        for category in categories:
            print(f"📦 Categoria: {category['name']}")
            subcats = get_subcategories(page, category['url'])

            if not subcats:
                print(f"   ↳ (sem subcategorias)")
            else:
                for sub in subcats:
                    print(f"   ↳ {sub['name']} -> {sub['url']}")
            all_data.append({
                "name": category["name"],
                "url": category["url"],
                "subcategories": subcats
            })

        browser.close()
        return all_data
