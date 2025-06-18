from playwright.sync_api import sync_playwright

BASE_URL = "https://voila.ca/categories"

def get_main_categories():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
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

        browser.close()
        return categories
