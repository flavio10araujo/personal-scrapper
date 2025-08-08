from playwright.sync_api import sync_playwright, ViewportSize
from typing import List, Dict
import re

BASE_URL = "https://www.superc.ca"

# Global set to track seen SKUs
seen_skus = set()

whitelist_categories = ["Pet Care"]

def get_categories_structure():
    def cat(name, url="", subcategories=None):
        return {
            "Category": name,
            "Url": url,
            "Subcategories": subcategories if subcategories is not None else []
        }

    return [
        cat("Fruits & Vegetables", "", [
            cat("Fruits", "", [
                cat("Apples & Pears", f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/apples-pears"),
                cat("Avocadoes & Exotic Fruits", f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/avocadoes-exotic-fruits"),
                cat("Bananas & Plantains", f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/bananas-plantains"),
                cat("Berries & Cherries", f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/berries-cherries"),
                cat("Grapes", f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/grapes"),
                cat("Citrus Fruits", f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/citrus-fruits"),
                cat("Peaches, Nectarines & Stone Fruits", f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/peaches-nectarines-stone-fruits"),
                cat("Watermelons & Melons", f"{BASE_URL}/en/aisles/fruits-vegetables/fruits/watermelons-melons"),
            ]),
            cat("Vegetables", "", [
                cat("Tomatoes & Cucumber", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/tomatoes-cucumber"),
                cat("Potatoes, Carrots & Celery", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/potatoes-carrots-celery"),
                cat("Lettuce & Leafy Vegetables", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/lettuce-leafy-vegetables"),
                cat("Peppers, Zucchini & Eggplant", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/peppers-zucchini-eggplant"),
                cat("Broccoli, Cauliflower & Cabbage", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/broccoli-cauliflower-cabbage"),
                cat("Mushrooms", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/mushrooms"),
                cat("Peas, Beans & Corn", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/peas-beans-corn"),
                cat("Onions & Leeks", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/onions-leeks"),
                cat("Ginger, Garlic & Shallots", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/ginger-garlic-shallots"),
                cat("Squash & Pumpkin", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/squash-pumpkin"),
                cat("Asparagus & Artichokes", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/asparagus-artichokes"),
                cat("Root Vegetables", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/root-vegetables"),
                cat("Exotic Vegetables", f"{BASE_URL}/en/aisles/fruits-vegetables/vegetables/exotic-vegetables"),
            ]),
            cat("Fresh Herbs", f"{BASE_URL}/en/aisles/fruits-vegetables/fresh-herbs"),
            cat("Packaged Salads & Vegetables", f"{BASE_URL}/en/aisles/fruits-vegetables/packaged-salads-vegetables"),
            cat("Fresh-Cut Fruits & Vegetables", f"{BASE_URL}/en/aisles/fruits-vegetables/fresh-cut-fruits-vegetables"),
            cat("Organic Fruits & Vegetables", f"{BASE_URL}/en/aisles/fruits-vegetables/organic-fruits-vegetables"),
            cat("Dried Fruits & Nuts", f"{BASE_URL}/en/aisles/fruits-vegetables/dried-fruits-nuts"),
            cat("Vegan & Vegetarian", "", [
                cat("Tofu & Tempeh", f"{BASE_URL}/en/aisles/fruits-vegetables/vegan-vegetarian/tofu-tempeh"),
                cat("Vegan Proteins & Cheese", f"{BASE_URL}/en/aisles/fruits-vegetables/vegan-vegetarian/vegan-proteins-cheese"),
            ]),
        ]),
        cat("Dairy & Eggs", "", [
            cat("Milk, Cream & Butter", "", [
                cat("2% & Whole Milk", f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/2-whole-milk"),
                cat("1% & Skim Milk", f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/1-skim-milk"),
                cat("Cream & Creamers", f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/cream-creamers"),
                cat("Flavoured Milk", f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/flavoured-milk"),
                cat("Lactose-Free & Non-Dairy Milk", f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/lactose-free-non-dairy-milk"),
                cat("Fermented Milk Kefir", f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/fermented-milk-kefir"),
                cat("Butter & Margarine", f"{BASE_URL}/en/aisles/dairy-eggs/milk-cream-butter/butter-margarine"),
            ]),
            cat("Eggs", "", [
                cat("Whole Eggs", f"{BASE_URL}/en/aisles/dairy-eggs/eggs/whole-eggs"),
                cat("Liquid Eggs & Egg Whites", f"{BASE_URL}/en/aisles/dairy-eggs/eggs/liquid-eggs-egg-whites"),
                cat("Organic eggs", f"{BASE_URL}/en/aisles/dairy-eggs/eggs/organic-eggs"),
            ]),
            cat("Yogurt", "", [
                cat("Yogurt Tubs", f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/yogurt-tubs"),
                cat("Multipacks", f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/multipacks"),
                cat("Greek Yogurts", f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/greek-yogurts"),
                cat("Drinkable Yogurts", f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/drinkable-yogurts"),
                cat("Probiotic Yogurts", f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/probiotic-yogurts"),
                cat("Single Serving Yogurts", f"{BASE_URL}/en/aisles/dairy-eggs/yogurt/single-serving-yogurts"),
            ]),
            cat("Packaged Cheese", "", [
                cat("Fondue", f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/fondue"),
                cat("Shredded Cheese", f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/shredded-cheese"),
                cat("Cream Cheese & Spreads", f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/cream-cheese-spreads"),
                cat("Strings & Snacks", f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/strings-snacks"),
                cat("Cheese Blocks", f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/cheese-blocks"),
                cat("Sliced Cheese", f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/sliced-cheese"),
                cat("Cottage Cheese & Ricotta", f"{BASE_URL}/en/aisles/dairy-eggs/packaged-cheese/cottage-cheese-ricotta"),
            ]),
            cat("Deli Cheese", "", [
                cat("Soft & Fresh", f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/soft-fresh"),
                cat("Firm & Semi-Soft", f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/firm-semi-soft"),
                cat("Mozzarella & Feta", f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/mozzarella-feta"),
                cat("Cheddar", f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/cheddar"),
                cat("Parmesan", f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/parmesan"),
                cat("Goat & Sheep", f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/goat-sheep"),
                cat("Swiss, Gouda & Jarlsberg", f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/swiss-gouda-jarlsberg"),
                cat("Blue Cheese & Rocquefort", f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/blue-cheese-rocquefort"),
                cat("Grated & Sliced", f"{BASE_URL}/en/aisles/dairy-eggs/deli-cheese/grated-sliced"),
            ]),
            cat("Sour Cream & Dips", "", [
                cat("Sour Cream", f"{BASE_URL}/en/aisles/dairy-eggs/sour-cream-dips/sour-cream"),
                cat("Chilled Dips", f"{BASE_URL}/en/aisles/dairy-eggs/sour-cream-dips/chilled-dips"),
            ]),
            cat("Chilled Desserts & Dough", "", [
                cat("Dessert Cups", f"{BASE_URL}/en/aisles/dairy-eggs/chilled-desserts-dough/dessert-cups"),
                cat("Chilled Dough", f"{BASE_URL}/en/aisles/dairy-eggs/chilled-desserts-dough/chilled-dough"),
                cat("Whipped Cream", f"{BASE_URL}/en/aisles/dairy-eggs/chilled-desserts-dough/whipped-cream"),
            ]),
        ]),
        cat("Pantry", "", [
            cat("Baking Ingredients", "", [
                cat("Flour & Baking Essentials", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/flour-baking-essentials"),
                cat("Sugar & Sweeteners", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/sugar-sweeteners"),
                cat("Chocolate & Cocoa", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/chocolate-cocoa"),
                cat("Kits, Mixes & Fillings", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/kits-mixes-fillings"),
                cat("Canned & Powdered Milk", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/canned-powdered-milk"),
                cat("Decorations & Frosting", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/decorations-frosting"),
                cat("Doughs & Crusts", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/doughs-crusts"),
                cat("Extracts & Colouring", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/extracts-colouring"),
                cat("Fruit, Seeds & Nuts", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/fruit-seeds-nuts"),
                cat("Bread Crumbs & Stuffing", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/bread-crumbs-stuffing"),
                cat("Shortening & Fats", f"{BASE_URL}/en/aisles/pantry/baking-ingredients/shortening-fats"),
            ]),
            cat("Canned & Jarred", "", [
                cat("Vegetables", f"{BASE_URL}/en/aisles/pantry/canned-jarred/vegetables"),
                cat("Beans & Legumes", f"{BASE_URL}/en/aisles/pantry/canned-jarred/beans-legumes"),
                cat("Pasta & Pasta Sauces", f"{BASE_URL}/en/aisles/pantry/canned-jarred/pasta-pasta-sauces"),
                cat("Tomatoes & Paste", f"{BASE_URL}/en/aisles/pantry/canned-jarred/tomatoes-paste"),
                cat("Cooking Sauces", f"{BASE_URL}/en/aisles/pantry/canned-jarred/cooking-sauces"),
                cat("Fish & Seafood", f"{BASE_URL}/en/aisles/pantry/canned-jarred/fish-seafood"),
                cat("Meats", f"{BASE_URL}/en/aisles/pantry/canned-jarred/meats"),
                cat("Soups", f"{BASE_URL}/en/aisles/pantry/canned-jarred/soups"),
                cat("Canned Dinners", f"{BASE_URL}/en/aisles/pantry/canned-jarred/canned-dinners"),
                cat("Fruit", f"{BASE_URL}/en/aisles/pantry/canned-jarred/fruit"),
            ]),
            cat("Cereals, Spreads & Syrups", "", [
                cat("Family Cereals", f"{BASE_URL}/en/aisles/pantry/cereals-spreads-syrups/family-cereals"),
                cat("Granola & Healthier Cereals", f"{BASE_URL}/en/aisles/pantry/cereals-spreads-syrups/granola-healthier-cereals"),
                cat("Oatmeal & Hot Cereals", f"{BASE_URL}/en/aisles/pantry/cereals-spreads-syrups/oatmeal-hot-cereals"),
                cat("Breakfast Bars & Pastries", f"{BASE_URL}/en/aisles/pantry/cereals-spreads-syrups/breakfast-bars-pastries"),
                cat("Honey & Syrup", f"{BASE_URL}/en/aisles/pantry/cereals-spreads-syrups/honey-syrup"),
                cat("Nut & Seed Butters", f"{BASE_URL}/en/aisles/pantry/cereals-spreads-syrups/nut-seed-butters"),
                cat("Jams & Jellies", f"{BASE_URL}/en/aisles/pantry/cereals-spreads-syrups/jams-jellies"),
                cat("Chocolate & Sweet Spreads", f"{BASE_URL}/en/aisles/pantry/cereals-spreads-syrups/chocolate-sweet-spreads"),
                cat("Cheese & Savoury Spreads", f"{BASE_URL}/en/aisles/pantry/cereals-spreads-syrups/cheese-savoury-spreads"),
            ]),
            cat("Condiments & Toppings", "", [
                cat("Ketchup & Mustard", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/ketchup-mustard"),
                cat("Mayonnaise & Sandwich Spreads", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/mayonnaise-sandwich-spreads"),
                cat("Salad Dressing", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/salad-dressing"),
                cat("Croutons & Salad Toppings", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/croutons-salad-toppings"),
                cat("BBQ & Marinade Sauces", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/bbq-marinade-sauces"),
                cat("Hot & Chili Sauces", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/hot-chili-sauces"),
                cat("Relish, Chutney & Fruit Sauces", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/relish-chutney-fruit-sauces"),
                cat("Pickles & Antipasto", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/pickles-antipasto"),
                cat("Tartar & Seafood Sauces", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/tartar-seafood-sauces"),
                cat("Salsa & Guacamole", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/salsa-guacamole"),
                cat("International Condiments", f"{BASE_URL}/en/aisles/pantry/condiments-toppings/international-condiments"),
            ]),
            cat("Herbs, Spices & Sauces", "", [
                cat("Spices", f"{BASE_URL}/en/aisles/pantry/herbs-spices-sauces/spices"),
                cat("Herb & Spice Blends", f"{BASE_URL}/en/aisles/pantry/herbs-spices-sauces/herb-spice-blends"),
                cat("Salt & Pepper", f"{BASE_URL}/en/aisles/pantry/herbs-spices-sauces/salt-pepper"),
                cat("Stock & Gravy", f"{BASE_URL}/en/aisles/pantry/herbs-spices-sauces/stock-gravy"),
                cat("Cooking Sauces", f"{BASE_URL}/en/aisles/pantry/herbs-spices-sauces/cooking-sauces"),
                cat("Marinades & Cooking Pastes", f"{BASE_URL}/en/aisles/pantry/herbs-spices-sauces/marinades-cooking-pastes"),
                cat("Package Sauces & Seasonings", f"{BASE_URL}/en/aisles/pantry/herbs-spices-sauces/package-sauces-seasonings"),
                cat("Breading, Batters & Coatings", f"{BASE_URL}/en/aisles/pantry/herbs-spices-sauces/breading-batters-coatings"),
            ]),
            cat("Oils & Vinegars", "", [
                cat("Olive Oil", f"{BASE_URL}/en/aisles/pantry/oils-vinegars/olive-oil"),
                cat("Vegetable Oil", f"{BASE_URL}/en/aisles/pantry/oils-vinegars/vegetable-oil"),
                cat("Nut & Seed Oil", f"{BASE_URL}/en/aisles/pantry/oils-vinegars/nut-seed-oil"),
                cat("Cooking Spray", f"{BASE_URL}/en/aisles/pantry/oils-vinegars/cooking-spray"),
                cat("White Vinegar", f"{BASE_URL}/en/aisles/pantry/oils-vinegars/white-vinegar"),
                cat("Balsamic Vinegar", f"{BASE_URL}/en/aisles/pantry/oils-vinegars/balsamic-vinegar"),
                cat("Wine & Apple Cider Vinegar", f"{BASE_URL}/en/aisles/pantry/oils-vinegars/wine-apple-cider-vinegar"),
                cat("Specialty Oil & Vinegar", f"{BASE_URL}/en/aisles/pantry/oils-vinegars/specialty-oil-vinegar"),
            ]),
            cat("World Cuisine", "", [
                cat("Asian", f"{BASE_URL}/en/aisles/pantry/world-cuisine/asian"),
                cat("Mexican", f"{BASE_URL}/en/aisles/pantry/world-cuisine/mexican"),
                cat("Mediterranean", f"{BASE_URL}/en/aisles/pantry/world-cuisine/mediterranean"),
            ]),
            cat("Sides", "", [
                cat("Pasta Sides", f"{BASE_URL}/en/aisles/pantry/sides/pasta-sides"),
                cat("Potato & Rice Sides", f"{BASE_URL}/en/aisles/pantry/sides/potato-rice-sides"),
            ]),
            cat("Pasta, Rice & Beans", "", [
                cat("Pasta", f"{BASE_URL}/en/aisles/pantry/pasta-rice-beans/pasta"),
                cat("Rice", f"{BASE_URL}/en/aisles/pantry/pasta-rice-beans/rice"),
                cat("Dried Beans", f"{BASE_URL}/en/aisles/pantry/pasta-rice-beans/dried-beans"),
                cat("Canned Beans", f"{BASE_URL}/en/aisles/pantry/pasta-rice-beans/canned-beans"),
                cat("Noodles & Vermicelli", f"{BASE_URL}/en/aisles/pantry/pasta-rice-beans/noodles-vermicelli"),
                cat("Couscous & Polenta", f"{BASE_URL}/en/aisles/pantry/pasta-rice-beans/couscous-polenta"),
                cat("Quinoa & Specialty Grains", f"{BASE_URL}/en/aisles/pantry/pasta-rice-beans/quinoa-specialty-grains"),
            ]),
            cat("Donation Bags", f"{BASE_URL}/en/aisles/pantry/donation-bags"),
        ]),
        cat("Cooked Meals", "", [
            cat("Ready-to-Eat", "", [
                cat("Prepared Meals", f"{BASE_URL}/en/aisles/cooked-meals/ready-to-eat/prepared-meals"),
                cat("Sandwiches", f"{BASE_URL}/en/aisles/cooked-meals/ready-to-eat/sandwiches"),
                cat("Salads", f"{BASE_URL}/en/aisles/cooked-meals/ready-to-eat/salads"),
                cat("Soups, Sauces & Sides", f"{BASE_URL}/en/aisles/cooked-meals/ready-to-eat/soups-sauces-sides")
            ]),
            cat("Ready-to-Cook", "", [
                cat("Meal Kits", f"{BASE_URL}/en/aisles/cooked-meals/ready-to-cook/meal-kits"),
                cat("Meat & Poultry", f"{BASE_URL}/en/aisles/cooked-meals/ready-to-cook/meat-poultry"),
                cat("Pizza", f"{BASE_URL}/en/aisles/cooked-meals/ready-to-cook/pizza"),
                cat("Frozen Meals", f"{BASE_URL}/en/aisles/cooked-meals/ready-to-cook/frozen-meals")
            ]),
            cat("Value Pack", "", [
                cat("Ready-to-Cook", f"{BASE_URL}/en/aisles/cooked-meals/value-pack/ready-to-cook")
            ]),
        ]),
        cat("Value Pack", "", [
            cat("Fresh Market", "", [
                cat("Fruits & Vegetables", f"{BASE_URL}/en/aisles/value-pack/fresh-market/fruits-vegetables"),
                cat("Meat, Deli & Fish", f"{BASE_URL}/en/aisles/value-pack/fresh-market/meat-deli-fish"),
                cat("Dairy & Eggs", f"{BASE_URL}/en/aisles/value-pack/fresh-market/dairy-eggs"),
                cat("Bakery", f"{BASE_URL}/en/aisles/value-pack/fresh-market/bakery"),
                cat("Prepared Meals", f"{BASE_URL}/en/aisles/value-pack/fresh-market/prepared-meals"),
            ]),
            cat("Non-perishable", "", [
                cat("Breakfast & Snacks", f"{BASE_URL}/en/aisles/value-pack/non-perishable/breakfast-snacks"),
                cat("Baking & Cooking", f"{BASE_URL}/en/aisles/value-pack/non-perishable/baking-cooking"),
                cat("Bean, Grain & Pasta", f"{BASE_URL}/en/aisles/value-pack/non-perishable/bean-grain-pasta"),
                cat("Beverage", f"{BASE_URL}/en/aisles/value-pack/non-perishable/beverage"),
            ]),
            cat("Frozen", f"{BASE_URL}/en/aisles/value-pack/frozen"),
            cat("Home", "", [
                cat("Household", f"{BASE_URL}/en/aisles/value-pack/home/household"),
                cat("Pets", f"{BASE_URL}/en/aisles/value-pack/home/pets"),
            ]),
        ]),
        cat("Beverages", "", [
            cat("Coffee", "", [
                cat("Ground Coffee", f"{BASE_URL}/en/aisles/beverages/coffee/ground-coffee"),
                cat("Whole Bean", f"{BASE_URL}/en/aisles/beverages/coffee/whole-bean"),
                cat("Coffee Pods", f"{BASE_URL}/en/aisles/beverages/coffee/coffee-pods"),
                cat("Instant Coffee", f"{BASE_URL}/en/aisles/beverages/coffee/instant-coffee"),
                cat("Coffee Whiteners", f"{BASE_URL}/en/aisles/beverages/coffee/coffee-whiteners"),
                cat("Filters & Accessories", f"{BASE_URL}/en/aisles/beverages/coffee/filters-accessories")
            ]),
            cat("Tea & Hot Drinks", "", [
                cat("Black Tea", f"{BASE_URL}/en/aisles/beverages/tea-hot-drinks/black-tea"),
                cat("Green Tea", f"{BASE_URL}/en/aisles/beverages/tea-hot-drinks/green-tea"),
                cat("Herbal Tea", f"{BASE_URL}/en/aisles/beverages/tea-hot-drinks/herbal-tea"),
                cat("Specialty Teas", f"{BASE_URL}/en/aisles/beverages/tea-hot-drinks/specialty-teas"),
                cat("Hot Chocolate", f"{BASE_URL}/en/aisles/beverages/tea-hot-drinks/hot-chocolate"),
                cat("Variety Packs", f"{BASE_URL}/en/aisles/beverages/tea-hot-drinks/variety-packs")
            ]),
            cat("Juices & Drinks", "", [
                cat("Refrigerated Juices & Drinks", f"{BASE_URL}/en/aisles/beverages/juices-drinks/refrigerated-juices-drinks"),
                cat("Shelf Juices & Drinks", f"{BASE_URL}/en/aisles/beverages/juices-drinks/shelf-juices-drinks"),
                cat("Juice & Drinks Boxes", f"{BASE_URL}/en/aisles/beverages/juices-drinks/juice-drinks-boxes"),
                cat("Vegetable Juices", f"{BASE_URL}/en/aisles/beverages/juices-drinks/vegetable-juices"),
                cat("Smoothies & Nectars", f"{BASE_URL}/en/aisles/beverages/juices-drinks/smoothies-nectars"),
                cat("Sparkling Juices & Drinks", f"{BASE_URL}/en/aisles/beverages/juices-drinks/sparkling-juices-drinks")
            ]),
            cat("Soft Drinks", "", [
                cat("Cola", f"{BASE_URL}/en/aisles/beverages/soft-drinks/cola"),
                cat("Diet Cola", f"{BASE_URL}/en/aisles/beverages/soft-drinks/diet-cola"),
                cat("Citrus & Lemon-Lime", f"{BASE_URL}/en/aisles/beverages/soft-drinks/citrus-lemon-lime"),
                cat("Fruit Flavored & Cream Soda", f"{BASE_URL}/en/aisles/beverages/soft-drinks/fruit-flavored-cream-soda"),
                cat("Ginger Ale", f"{BASE_URL}/en/aisles/beverages/soft-drinks/ginger-ale"),
                cat("Iced Tea", f"{BASE_URL}/en/aisles/beverages/soft-drinks/iced-tea"),
                cat("Root Beer & Spruce Beer", f"{BASE_URL}/en/aisles/beverages/soft-drinks/root-beer-spruce-beer")
            ]),
            cat("Sports & Energy Drinks", "", [
                cat("Energy Drinks", f"{BASE_URL}/en/aisles/beverages/sports-energy-drinks/energy-drinks"),
                cat("Sports Drinks", f"{BASE_URL}/en/aisles/beverages/sports-energy-drinks/sports-drinks"),
                cat("Meal Replacements", f"{BASE_URL}/en/aisles/beverages/sports-energy-drinks/meal-replacements")
            ]),
            cat("Water", "", [
                cat("Sparkling Water", f"{BASE_URL}/en/aisles/beverages/water/sparkling-water"),
                cat("Tonic Water", f"{BASE_URL}/en/aisles/beverages/water/tonic-water"),
                cat("Bottled Water", f"{BASE_URL}/en/aisles/beverages/water/bottled-water"),
                cat("Flavoured Water", f"{BASE_URL}/en/aisles/beverages/water/flavoured-water"),
                cat("Coconut Water", f"{BASE_URL}/en/aisles/beverages/water/coconut-water")
            ]),
            cat("Iced Tea & Coffee", "", [
                cat("Iced Coffee", f"{BASE_URL}/en/aisles/beverages/iced-tea-coffee/iced-coffee"),
                cat("Iced Tea Mixes & Drinks", f"{BASE_URL}/en/aisles/beverages/iced-tea-coffee/iced-tea-mixes-drinks")
            ]),
            cat("Drink Mixes", "", [
                cat("Liquid Drink Mixes", f"{BASE_URL}/en/aisles/beverages/drink-mixes/liquid-drink-mixes"),
                cat("Powdered Drink Mixes", f"{BASE_URL}/en/aisles/beverages/drink-mixes/powdered-drink-mixes")
            ]),
            cat("Soy, Rice & Nut Beverages", "", [
                cat("Rice Milk", f"{BASE_URL}/en/aisles/beverages/soy-rice-nut-beverages/rice-milk"),
                cat("Nut & Seed Milk", f"{BASE_URL}/en/aisles/beverages/soy-rice-nut-beverages/nut-seed-milk"),
                cat("Soy Milk", f"{BASE_URL}/en/aisles/beverages/soy-rice-nut-beverages/soy-milk")
            ]),
            cat("Non-Alcoholic Beverages", "", [
                cat("Alcohol-Free Wine", f"{BASE_URL}/en/aisles/beverages/non-alcoholic-beverages/alcohol-free-wine"),
                cat("Non-Alcoholic Beer", f"{BASE_URL}/en/aisles/beverages/non-alcoholic-beverages/non-alcoholic-beer")
            ])
        ]),
        cat("Beer & Wine", "", [
            #<div class="aisles--subNav--lev3"><div class="aisles-all-link subNav--id--BV09 active--sub-nav"><a href="/en/aisles/beer-wine/wines-cocktails-coolers">View all  Wines, Cocktails &amp; Coolers</a></div><ul class="subNav--id--BV09 active--sub-nav"><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/red-wine" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Red Wine"><span>Red Wine</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/white-wine" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="White Wine"><span>White Wine</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/rose-wine" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Rosé Wine"><span>Rosé Wine</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/sparkling-wine" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Sparkling Wine"><span>Sparkling Wine</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/sangria" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Sangria"><span>Sangria</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/cocktails-other-wines" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Cocktails &amp; Other Wines"><span>Cocktails &amp; Other Wines</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/coolers" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Coolers"><span>Coolers</span></a></li></ul><div class="aisles-all-link subNav--id--BV10"><a href="/en/aisles/beer-wine/beer-cider">View all  Beer &amp; Cider</a></div><ul class="subNav--id--BV10"><li><a href="/en/aisles/beer-wine/beer-cider/classic-beer" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Classic Beer"><span>Classic Beer</span></a></li><li><a href="/en/aisles/beer-wine/beer-cider/classic-light-beer" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Classic Light Beer"><span>Classic Light Beer</span></a></li><li><a href="/en/aisles/beer-wine/beer-cider/specialty-flavoured-beer" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Specialty &amp; Flavoured Beer"><span>Specialty &amp; Flavoured Beer</span></a></li><li><a href="/en/aisles/beer-wine/beer-cider/imported-beer" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Imported Beer"><span>Imported Beer</span></a></li><li><a href="/en/aisles/beer-wine/beer-cider/artisanal-beer-microbrewery" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Artisanal Beer &amp; Microbrewery"><span>Artisanal Beer &amp; Microbrewery</span></a></li><a href="/en/aisles/beer-wine/beer-cider/cider" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Cider"><span>Cider</span></a></li></ul></div>
            cat("Wines, Cocktails & Coolers", "", [
                cat("Red Wine", f"{BASE_URL}/en/aisles/beer-wine/wines-cocktails-coolers/red-wine"),
                cat("White Wine", f"{BASE_URL}/en/aisles/beer-wine/wines-cocktails-coolers/white-wine"),
                cat("Rosé Wine", f"{BASE_URL}/en/aisles/beer-wine/wines-cocktails-coolers/rose-wine"),
                cat("Sparkling Wine", f"{BASE_URL}/en/aisles/beer-wine/wines-cocktails-coolers/sparkling-wine"),
                cat("Sangria", f"{BASE_URL}/en/aisles/beer-wine/wines-cocktails-coolers/sangria"),
                cat("Cocktails & Other Wines", f"{BASE_URL}/en/aisles/beer-wine/wines-cocktails-coolers/cocktails-other-wines"),
                cat("Coolers", f"{BASE_URL}/en/aisles/beer-wine/wines-cocktails-coolers/coolers")
            ]),
            cat("Beer & Cider", "", [
                cat("Classic Beer", f"{BASE_URL}/en/aisles/beer-wine/beer-cider/classic-beer"),
                cat("Classic Light Beer", f"{BASE_URL}/en/aisles/beer-wine/beer-cider/classic-light-beer"),
                cat("Specialty & Flavoured Beer", f"{BASE_URL}/en/aisles/beer-wine/beer-cider/specialty-flavoured-beer"),
                cat("Imported Beer", f"{BASE_URL}/en/aisles/beer-wine/beer-cider/imported-beer"),
                cat("Artisanal Beer & Microbrewery", f"{BASE_URL}/en/aisles/beer-wine/beer-cider/artisanal-beer-microbrewery"),
                cat("Cider", f"{BASE_URL}/en/aisles/beer-wine/beer-cider/cider")
            ]),
        ]),
        cat("Meat & Poultry", "", [
            cat("Beef & Veal", "", [
                cat("Steak Cuts", f"{BASE_URL}/en/aisles/meat-poultry/beef-veal/steak-cuts"),
                cat("Ground", f"{BASE_URL}/en/aisles/meat-poultry/beef-veal/ground"),
                cat("Roasts, Ribs & Racks", f"{BASE_URL}/en/aisles/meat-poultry/beef-veal/roasts-ribs-racks"),
                cat("Fondue, Cubes & Strips", f"{BASE_URL}/en/aisles/meat-poultry/beef-veal/fondue-cubes-strips"),
                cat("Marrow Soup Bone & Shank", f"{BASE_URL}/en/aisles/meat-poultry/beef-veal/marrow-soup-bone-shank"),
                cat("Blood Sausage & Giblets", f"{BASE_URL}/en/aisles/meat-poultry/beef-veal/blood-sausage-giblets")
            ]),
            cat("Chicken & Turkey", "", [
                cat("Breasts", f"{BASE_URL}/en/aisles/meat-poultry/chicken-turkey/breasts"),
                cat("Legs, Drumsticks & Wings", f"{BASE_URL}/en/aisles/meat-poultry/chicken-turkey/legs-drumsticks-wings"),
                cat("Ground, Strips & Fondue", f"{BASE_URL}/en/aisles/meat-poultry/chicken-turkey/ground-strips-fondue"),
                cat("Whole & Roasting", f"{BASE_URL}/en/aisles/meat-poultry/chicken-turkey/whole-roasting")
            ]),
            cat("Pork", "", [
                cat("Ham", f"{BASE_URL}/en/aisles/meat-poultry/pork/ham"),
                cat("Bacon", f"{BASE_URL}/en/aisles/meat-poultry/pork/bacon"),
                cat("Tenderloin", f"{BASE_URL}/en/aisles/meat-poultry/pork/tenderloin"),
                cat("Ground Pork", f"{BASE_URL}/en/aisles/meat-poultry/pork/ground-pork"),
                cat("Fondue, Cubes & Strips", f"{BASE_URL}/en/aisles/meat-poultry/pork/fondue-cubes-strips"),
                cat("Chops & Steaks", f"{BASE_URL}/en/aisles/meat-poultry/pork/chops-steaks"),
                cat("Ribs & Roasts", f"{BASE_URL}/en/aisles/meat-poultry/pork/ribs-roasts"),
                cat("Giblets", f"{BASE_URL}/en/aisles/meat-poultry/pork/giblets")
            ]),
            cat("Rabbit & Duck", "", [
                cat("Legs, Drumsticks & Wings", f"{BASE_URL}/en/aisles/meat-poultry/rabbit-duck/legs-drumsticks-wings")
            ]),
            cat("Lamb & Game Meat", "", [
                cat("Ground & Giblets", f"{BASE_URL}/en/aisles/meat-poultry/lamb-game-meat/ground-giblets"),
                cat("Roasts, Ribs & Racks", f"{BASE_URL}/en/aisles/meat-poultry/lamb-game-meat/roasts-ribs-racks"),
                cat("Chops & Steaks", f"{BASE_URL}/en/aisles/meat-poultry/lamb-game-meat/chops-steaks")
            ]),
            cat("Sausages & Bacon", "", [
                cat("Sausages & Hot Dogs", f"{BASE_URL}/en/aisles/meat-poultry/sausages-bacon/sausages-hot-dogs"),
                cat("Bacon", f"{BASE_URL}/en/aisles/meat-poultry/sausages-bacon/bacon"),
                cat("Ham", f"{BASE_URL}/en/aisles/meat-poultry/sausages-bacon/ham")
            ]),
            cat("Marinated & Prepared Meat", "", [
                cat("Kabob", f"{BASE_URL}/en/aisles/meat-poultry/marinated-prepared-meat/kabob"),
                cat("Stuffed & Wrapped", f"{BASE_URL}/en/aisles/meat-poultry/marinated-prepared-meat/stuffed-wrapped"),
                cat("Marinated Cuts", f"{BASE_URL}/en/aisles/meat-poultry/marinated-prepared-meat/marinated-cuts"),
                cat("Fresh Sausages", f"{BASE_URL}/en/aisles/meat-poultry/marinated-prepared-meat/fresh-sausages")
            ]),
            cat("Frozen Meat", "", [
                cat("Chicken & Turkey", f"{BASE_URL}/en/aisles/meat-poultry/frozen-meat/chicken-turkey"),
                cat("Burgers, Meatballs & Sausages", f"{BASE_URL}/en/aisles/meat-poultry/frozen-meat/burgers-meatballs-sausages"),
                cat("Pork", f"{BASE_URL}/en/aisles/meat-poultry/frozen-meat/pork"),
                cat("Lamb & Game Meat", f"{BASE_URL}/en/aisles/meat-poultry/frozen-meat/lamb-game-meat"),
                cat("Fondue", f"{BASE_URL}/en/aisles/meat-poultry/frozen-meat/fondue"),
                cat("Meat Pie", f"{BASE_URL}/en/aisles/meat-poultry/frozen-meat/meat-pie")
            ]),
        ]),
        cat("Vegan & Vegetarian Food", "", [
            cat("Tofu, Tempeh & Other Protein", f"{BASE_URL}/en/aisles/vegan-vegetarian-food/tofu-tempeh-other-protein"),
            cat("Beverages", f"{BASE_URL}/en/aisles/vegan-vegetarian-food/beverages"),
            cat("Pantry", f"{BASE_URL}/en/aisles/vegan-vegetarian-food/pantry"),
            cat("Snacks", f"{BASE_URL}/en/aisles/vegan-vegetarian-food/snacks"),
            cat("Refrigerated", f"{BASE_URL}/en/aisles/vegan-vegetarian-food/refrigerated"),
            cat("Frozen", "", [
                cat("Meals & Sides", f"{BASE_URL}/en/aisles/vegan-vegetarian-food/frozen/meals-sides"),
                cat("Desserts", f"{BASE_URL}/en/aisles/vegan-vegetarian-food/frozen/desserts")
            ])
        ]),
        cat("Organic Groceries", "", [
            cat("Fruits & Vegetables", "", [
                cat("Organic Milk & Cream", f"{BASE_URL}/en/aisles/organic-groceries/eggs-dairy-alternatives-product/organic-milk-cream"),
                cat("Organic Milk Substitutes", f"{BASE_URL}/en/aisles/organic-groceries/eggs-dairy-alternatives-product/organic-milk-substitutes")
            ]),
            cat("Bread & Bakery Products", "", [
                cat("Organic Bread", f"{BASE_URL}/en/aisles/organic-groceries/bread-bakery-products/organic-bread")
            ]),
            cat("Meats, Poultry & Ocean products", "", [
                cat("Organic Beef, Pork & Veal", f"{BASE_URL}/en/aisles/organic-groceries/meats-poultry-ocean-products/organic-beef-pork-veal"),
                cat("Organic Chicken", f"{BASE_URL}/en/aisles/organic-groceries/meats-poultry-ocean-products/organic-chicken"),
                cat("Organic Deli Meats & Ready Meals", f"{BASE_URL}/en/aisles/organic-groceries/meats-poultry-ocean-products/organic-deli-meats-ready-meals")
            ]),
            cat("Organic baby world", "", [
                cat("Organic Baby Food", f"{BASE_URL}/en/aisles/organic-groceries/organic-baby-world/organic-baby-food"),
                cat("Organic Baby Care", f"{BASE_URL}/en/aisles/organic-groceries/organic-baby-world/organic-baby-care")
            ]),
            cat("Eggs, Dairy & Alternatives product", "", [
                cat("Organic Milk & Cream", f"{BASE_URL}/en/aisles/organic-groceries/eggs-dairy-alternatives-product/organic-milk-cream"),
                cat("Organic Milk Substitutes", f"{BASE_URL}/en/aisles/organic-groceries/eggs-dairy-alternatives-product/organic-milk-substitutes")
            ]),
            cat("Pantry", "", [
                cat("Organic Nuts, Seeds & Dried Fruits", f"{BASE_URL}/en/aisles/organic-groceries/pantry/organic-nuts-seeds-dried-fruits"),
                cat("Organic Cereals, Spreads & Syrup", f"{BASE_URL}/en/aisles/organic-groceries/pantry/organic-cereals-spreads-syrup"),
                cat("Organic Sugar, Flour & Other Baking Ingredients", f"{BASE_URL}/en/aisles/organic-groceries/pantry/organic-sugar-flour-other-baking-ingredients"),
                cat("Organic Broth & Soup", f"{BASE_URL}/en/aisles/organic-groceries/pantry/organic-broth-soup"),
                cat("Organic Oil, Vinegar & Dressing", f"{BASE_URL}/en/aisles/organic-groceries/pantry/organic-oil-vinegar-dressing"),
                cat("Organic Pasta, Rice & Beans", f"{BASE_URL}/en/aisles/organic-groceries/pantry/organic-pasta-rice-beans"),
                cat("Organic Condiments & Sauces", f"{BASE_URL}/en/aisles/organic-groceries/pantry/organic-condiments-sauces"),
                cat("Organic Spices & Seasonings", f"{BASE_URL}/en/aisles/organic-groceries/pantry/organic-spices-seasonings")
            ]),
            cat("Snacks, Crackers & Chocolate", "", [
                cat("Organic Chewy Bars & Energy Bars", f"{BASE_URL}/en/aisles/organic-groceries/snacks-crackers-chocolate/organic-chewy-bars-energy-bars"),
                cat("Organic Nuts & Fruits Snacks", f"{BASE_URL}/en/aisles/organic-groceries/snacks-crackers-chocolate/organic-nuts-fruits-snacks"),
                cat("Organic Chips & Popcorn", f"{BASE_URL}/en/aisles/organic-groceries/snacks-crackers-chocolate/organic-chips-popcorn"),
                cat("Organic Crackers & Cookies", f"{BASE_URL}/en/aisles/organic-groceries/snacks-crackers-chocolate/organic-crackers-cookies"),
                cat("Organic Chocolate, Gums & Candies", f"{BASE_URL}/en/aisles/organic-groceries/snacks-crackers-chocolate/organic-chocolate-gums-candies")
            ]),
            cat("Beverages", "", [
                cat("Organic Juices & Kombucha", f"{BASE_URL}/en/aisles/organic-groceries/beverages/organic-juices-kombucha"),
                cat("Organic Milk Alternatives", f"{BASE_URL}/en/aisles/organic-groceries/beverages/organic-milk-alternatives"),
                cat("Organic Coffee & Tea", f"{BASE_URL}/en/aisles/organic-groceries/beverages/organic-coffee-tea"),
                cat("Organic Wines & Beers", f"{BASE_URL}/en/aisles/organic-groceries/beverages/organic-wines-beers")
            ]),
            cat("Frozen Food", "", [
                cat("Organic Fruits & Vegetables", f"{BASE_URL}/en/aisles/organic-groceries/frozen-food/organic-fruits-vegetables"),
                cat("Organic Pizza & Prepared Meals", f"{BASE_URL}/en/aisles/organic-groceries/frozen-food/organic-pizza-prepared-meals")
            ]),
            cat("Vegan & Vegetarian Food", "", [
                cat("Organic Tofu & Tempeh", f"{BASE_URL}/en/aisles/organic-groceries/vegan-vegetarian-food/organic-tofu-tempeh")
            ]),
            cat("Eco-Friendly Household Cleaning Products", f"{BASE_URL}/en/aisles/organic-groceries/eco-friendly-household-cleaning-products")
        ]),
        cat("Snacks", "", [
            cat("Salty Snacks", "", [
                cat("Chips",  f"{BASE_URL}/en/aisles/snacks/salty-snacks/chips"),
                cat("Corn & Tortilla Chips", f"{BASE_URL}/en/aisles/snacks/salty-snacks/corn-tortilla-chips"),
                cat("Pretzels, Cheese Puffs & Mixes", f"{BASE_URL}/en/aisles/snacks/salty-snacks/pretzels-cheese-puffs-mixes"),
                cat("Popcorn & Kernels", f"{BASE_URL}/en/aisles/snacks/salty-snacks/popcorn-kernels"),
                cat("Crackers", f"{BASE_URL}/en/aisles/snacks/salty-snacks/crackers"),
                cat("Rice & Gluten-free Snacks", f"{BASE_URL}/en/aisles/snacks/salty-snacks/rice-gluten-free-snacks"),
                cat("Flatbreads & Crisps", f"{BASE_URL}/en/aisles/snacks/salty-snacks/flatbreads-crisps"),
                cat("Nuts, Seeds & Jerky", f"{BASE_URL}/en/aisles/snacks/salty-snacks/nuts-seeds-jerky")
            ]),
            cat("Sweet Snacks & Candy", "", [
                cat("Candy & Gum", f"{BASE_URL}/en/aisles/snacks/sweet-snacks-candy/candy-gum"),
                cat("Chocolate", f"{BASE_URL}/en/aisles/snacks/sweet-snacks-candy/chocolate"),
                cat("Cookies & Cakes", f"{BASE_URL}/en/aisles/snacks/sweet-snacks-candy/cookies-cakes"),
                cat("Pudding & Jelly", f"{BASE_URL}/en/aisles/snacks/sweet-snacks-candy/pudding-jelly"),
                cat("Chewy Bars & Fruit Snacks", f"{BASE_URL}/en/aisles/snacks/sweet-snacks-candy/chewy-bars-fruit-snacks"),
                cat("Ice Cream Toppings & Cones", f"{BASE_URL}/en/aisles/snacks/sweet-snacks-candy/ice-cream-toppings-cones")
            ]),
            cat("Nuts, Seeds &  Fruit", "", [
                cat("Nuts & Seeds", f"{BASE_URL}/en/aisles/snacks/nuts-seeds-fruit/nuts-seeds"),
                cat("Dried Fruit", f"{BASE_URL}/en/aisles/snacks/nuts-seeds-fruit/dried-fruit"),
                cat("Canned or Preserved Fruit", f"{BASE_URL}/en/aisles/snacks/nuts-seeds-fruit/canned-or-preserved-fruit"),
                cat("Snack Bars", f"{BASE_URL}/en/aisles/snacks/nuts-seeds-fruit/snack-bars")
            ])
        ]),
        cat("Frozen", "", [
            cat("Appetizers & Snacks", "", [
                cat("Hors d'Oeuvres", f"{BASE_URL}/en/aisles/frozen/appetizers-snacks/hors-d-oeuvres"),
                cat("Pockets & Pies", f"{BASE_URL}/en/aisles/frozen/appetizers-snacks/pockets-pies"),
                cat("Corn Dogs & Burritos", f"{BASE_URL}/en/aisles/frozen/appetizers-snacks/corn-dogs-burritos")
            ]),
            cat("Bakery", "", [
                cat("Bread & Baked Goods", f"{BASE_URL}/en/aisles/frozen/bakery/bread-baked-goods"),
                cat("Cakes & Cheesecakes", f"{BASE_URL}/en/aisles/frozen/bakery/cakes-cheesecakes"),
                cat("Pies & Pastry", f"{BASE_URL}/en/aisles/frozen/bakery/pies-pastry"),
                cat("Pie Shells & Dough", f"{BASE_URL}/en/aisles/frozen/bakery/pie-shells-dough"),
                cat("Dessert Toppings", f"{BASE_URL}/en/aisles/frozen/bakery/dessert-toppings")
            ]),
            cat("Beverages & Ice", "", [
                cat("Juices", f"{BASE_URL}/en/aisles/frozen/beverages-ice/juices")
            ]),
            cat("Breakfast Foods", "", [
                cat("Waffles, Pancakes & French Toast", f"{BASE_URL}/en/aisles/frozen/breakfast-foods/waffles-pancakes-french-toast"),
                cat("Hashbrowns", f"{BASE_URL}/en/aisles/frozen/breakfast-foods/hashbrowns"),
                cat("Toaster Pastries & Muffins", f"{BASE_URL}/en/aisles/frozen/breakfast-foods/toaster-pastries-muffins"),
                cat("Breakfast Sandwiches", f"{BASE_URL}/en/aisles/frozen/breakfast-foods/breakfast-sandwiches")
            ]),
            cat("Fruit & Vegetables", "", [
                cat("Fruit", f"{BASE_URL}/en/aisles/frozen/fruit-vegetables/fruit"),
                cat("Vegetables", f"{BASE_URL}/en/aisles/frozen/fruit-vegetables/vegetables"),
                cat("Hashbrowns & Patties", f"{BASE_URL}/en/aisles/frozen/fruit-vegetables/hashbrowns-patties"),
                cat("French Fries & Onion Rings", f"{BASE_URL}/en/aisles/frozen/fruit-vegetables/french-fries-onion-rings"),
                cat("Blends & Edamame", f"{BASE_URL}/en/aisles/frozen/fruit-vegetables/blends-edamame")
            ]),
            cat("Ice Cream & Treats", "", [
                cat("Ice Cream", f"{BASE_URL}/en/aisles/frozen/ice-cream-treats/ice-cream"),
                cat("Frozen Yogurt & Gelato", f"{BASE_URL}/en/aisles/frozen/ice-cream-treats/frozen-yogurt-gelato"),
                cat("Sorbet & Non-Dairy", f"{BASE_URL}/en/aisles/frozen/ice-cream-treats/sorbet-non-dairy"),
                cat("Ice Cream Bars & Treats", f"{BASE_URL}/en/aisles/frozen/ice-cream-treats/ice-cream-bars-treats"),
                cat("Popsicles & Fruit Bars", f"{BASE_URL}/en/aisles/frozen/ice-cream-treats/popsicles-fruit-bars"),
                cat("Ice Cream Cakes", f"{BASE_URL}/en/aisles/frozen/ice-cream-treats/ice-cream-cakes"),
                cat("Frozen Desserts", f"{BASE_URL}/en/aisles/frozen/ice-cream-treats/frozen-desserts")
            ]),
            cat("Fish & Seafood", "", [
                cat("Shrimp & Seafood", f"{BASE_URL}/en/aisles/frozen/fish-seafood/shrimp-seafood"),
                cat("Fish Filets  & Steaks", f"{BASE_URL}/en/aisles/frozen/fish-seafood/fish-filets-steaks"),
                cat("Burgers & Sticks", f"{BASE_URL}/en/aisles/frozen/fish-seafood/burgers-sticks")
            ]),
            cat("Meat & Poultry", "", [
                cat("Chicken & Turkey", f"{BASE_URL}/en/aisles/frozen/meat-poultry/chicken-turkey"),
                cat("Burgers, Meatballs & Sausages", f"{BASE_URL}/en/aisles/frozen/meat-poultry/burgers-meatballs-sausages"),
                cat("Pork", f"{BASE_URL}/en/aisles/frozen/meat-poultry/pork"),
                cat("Lamb & Game Meat", f"{BASE_URL}/en/aisles/frozen/meat-poultry/lamb-game-meat"),
                cat("Fondue", f"{BASE_URL}/en/aisles/frozen/meat-poultry/frozen-meat/fondue"),
                cat("Meat Pie", f"{BASE_URL}/en/aisles/frozen/meat-poultry/meat-pie")
            ]),
            cat("Meals & Sides", "", [
                cat("Soups & Sides", f"{BASE_URL}/en/aisles/frozen/meals-sides/soups-sides"),
                cat("Beef & Veal Meals", f"{BASE_URL}/en/aisles/frozen/meals-sides/beef-veal-meals"),
                cat("Chicken & Turkey Meals", f"{BASE_URL}/en/aisles/frozen/meals-sides/chicken-turkey-meals"),
                cat("Pork & Lamb Meals", f"{BASE_URL}/en/aisles/frozen/meals-sides/pork-lamb-meals"),
                cat("Fish & Seafood Meals", f"{BASE_URL}/en/aisles/frozen/meals-sides/fish-seafood-meals"),
                cat("Vegetarian Meals", f"{BASE_URL}/en/aisles/frozen/meals-sides/vegetarian-meals")
            ]),
            cat("Pizza & Pasta", "", [
                cat("Meat & Chicken Pizza", f"{BASE_URL}/en/aisles/frozen/pizza-pasta/meat-chicken-pizza"),
                cat("Seafood Pizza", f"{BASE_URL}/en/aisles/frozen/pizza-pasta/seafood-pizza"),
                cat("Vegetarian Pizza", f"{BASE_URL}/en/aisles/frozen/pizza-pasta/vegetarian-pizza"),
                cat("Cheese Pizza", f"{BASE_URL}/en/aisles/frozen/pizza-pasta/cheese-pizza"),
                cat("Pizza Bites & Snacks", f"{BASE_URL}/en/aisles/frozen/pizza-pasta/pizza-bites-snacks"),
                cat("Specialty Pizza", f"{BASE_URL}/en/aisles/frozen/pizza-pasta/specialty-pizza"),
                cat("Frozen Pasta", f"{BASE_URL}/en/aisles/frozen/pizza-pasta/frozen-pasta")
            ])
        ]),
        cat("Bread & Bakery Products", "", [
            cat("Freshly Baked Bread & Baguettes", "", [
                cat("Fresh Loaves & Breads", f"{BASE_URL}/en/aisles/bread-bakery-products/freshly-baked-bread-baguettes/fresh-loaves-breads"),
                cat("Baguettes", f"{BASE_URL}/en/aisles/bread-bakery-products/freshly-baked-bread-baguettes/baguettes"),
                cat("Rye & Other Grains", f"{BASE_URL}/en/aisles/bread-bakery-products/freshly-baked-bread-baguettes/rye-other-grains"),
                cat("Première Moisson", f"{BASE_URL}/en/aisles/bread-bakery-products/freshly-baked-bread-baguettes/premiere-moisson")
            ]),
            cat("Packaged Bread", "", [
                cat("White", f"{BASE_URL}/en/aisles/bread-bakery-products/packaged-bread/white"),
                cat("Whole Wheat & Grain", f"{BASE_URL}/en/aisles/bread-bakery-products/packaged-bread/whole-wheat-grain"),
                cat("Rye & Other Grains", f"{BASE_URL}/en/aisles/bread-bakery-products/packaged-bread/rye-other-grains"),
                cat("Artisan & Specialty", f"{BASE_URL}/en/aisles/bread-bakery-products/packaged-bread/artisan-specialty"),
                cat("Gluten-Free & Special Dietary Needs", f"{BASE_URL}/en/aisles/bread-bakery-products/packaged-bread/gluten-free-special-dietary-needs")
            ]),
            cat("Buns & Rolls", "", [
                cat("Hot Dog & Hamburger", f"{BASE_URL}/en/aisles/bread-bakery-products/buns-rolls/hot-dog-hamburger"),
                cat("Small Buns", f"{BASE_URL}/en/aisles/bread-bakery-products/buns-rolls/small-buns"),
                cat("Sandwich Breads", f"{BASE_URL}/en/aisles/bread-bakery-products/buns-rolls/sandwich-breads")
            ]),
            cat("Tortillas & Flat Breads", "", [
                cat("Tortillas", f"{BASE_URL}/en/aisles/bread-bakery-products/tortillas-flat-breads/tortillas"),
                cat("Pita Bread", f"{BASE_URL}/en/aisles/bread-bakery-products/tortillas-flat-breads/pita-bread"),
                cat("Flat Bread & Naan", f"{BASE_URL}/en/aisles/bread-bakery-products/tortillas-flat-breads/flat-bread-naan"),
                cat("Pizza Dough & Bases", f"{BASE_URL}/en/aisles/bread-bakery-products/tortillas-flat-breads/pizza-dough-bases")
            ]),
            cat("Muffins,  Bagels & Baked Goods", "", [
                cat("Croissants & Chocolatines", f"{BASE_URL}/en/aisles/bread-bakery-products/muffins-bagels-baked-goods/croissants-chocolatines"),
                cat("Rolls, Danishes & Twists", f"{BASE_URL}/en/aisles/bread-bakery-products/muffins-bagels-baked-goods/rolls-danishes-twists"),
                cat("Bagels", f"{BASE_URL}/en/aisles/bread-bakery-products/muffins-bagels-baked-goods/bagels"),
                cat("Muffins", f"{BASE_URL}/en/aisles/bread-bakery-products/muffins-bagels-baked-goods/muffins"),
                cat("English Muffins & Crumpets", f"{BASE_URL}/en/aisles/bread-bakery-products/muffins-bagels-baked-goods/english-muffins-crumpets"),
                cat("Waffles, Pancakes & Crepes", f"{BASE_URL}/en/aisles/bread-bakery-products/muffins-bagels-baked-goods/waffles-pancakes-crepes")
            ]),
            cat("Desserts & Pastries", "", [
                cat("Brownies & Macarons", f"{BASE_URL}/en/aisles/bread-bakery-products/desserts-pastries/brownies-macarons"),
                cat("Cakes", f"{BASE_URL}/en/aisles/bread-bakery-products/desserts-pastries/cakes"),
                cat("Cookies & Scones", f"{BASE_URL}/en/aisles/bread-bakery-products/desserts-pastries/cookies-scones"),
                cat("Cupcakes", f"{BASE_URL}/en/aisles/bread-bakery-products/desserts-pastries/cupcakes"),
                cat("Pies & Tarts", f"{BASE_URL}/en/aisles/bread-bakery-products/desserts-pastries/pies-tarts"),
                cat("Frozen Baked Cakes and Tarts", f"{BASE_URL}/en/aisles/bread-bakery-products/desserts-pastries/frozen-baked-cakes-and-tarts"),
                cat("Pastries & Donuts", f"{BASE_URL}/en/aisles/bread-bakery-products/desserts-pastries/pastries-donuts"),
                cat("Pie Shells & Crusts", f"{BASE_URL}/en/aisles/bread-bakery-products/desserts-pastries/pie-shells-crusts")
            ])
        ]),
        cat("Deli & Prepared Meals", "", [
            cat("Deli Meats", "", [
                #<div class="aisles--subNav--lev3"><div class="aisles-all-link subNav--id--DP01 active--sub-nav"><a href="/en/aisles/deli-prepared-meals/deli-meats">View all  Deli Meats</a></div><ul class="subNav--id--DP01 active--sub-nav"><li><a href="/en/aisles/deli-prepared-meals/deli-meats/beef" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Deli Meats" data-grand-child-menu-name="Beef"><span>Beef</span></a></li><li><a href="/en/aisles/deli-prepared-meals/deli-meats/turkey-chicken" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Deli Meats" data-grand-child-menu-name="Turkey &amp; Chicken"><span>Turkey &amp; Chicken</span></a></li><li><a href="/en/aisles/deli-prepared-meals/deli-meats/ham-pork" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Deli Meats" data-grand-child-menu-name="Ham &amp; Pork"><span>Ham &amp; Pork</span></a></li><li><a href="/en/aisles/deli-prepared-meals/deli-meats/bologna-pastrami" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Deli Meats" data-grand-child-menu-name="Bologna &amp; Pastrami"><span>Bologna &amp; Pastrami</span></a></li><li><a href="/en/aisles/deli-prepared-meals/deli-meats/salami-pepperoni" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Deli Meats" data-grand-child-menu-name="Salami &amp; Pepperoni"><span>Salami &amp; Pepperoni</span></a></li><li><a href="/en/aisles/deli-prepared-meals/deli-meats/prosciutto-mortadella" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Deli Meats" data-grand-child-menu-name="Prosciutto &amp; Mortadella"><span>Prosciutto &amp; Mortadella</span></a></li><li><a href="/en/aisles/deli-prepared-meals/deli-meats/dry-sausages-smoked-meat" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Deli Meats" data-grand-child-menu-name="Dry Sausages &amp; Smoked Meat"><span>Dry Sausages &amp; Smoked Meat</span></a></li></ul><div class="aisles-all-link subNav--id--DP03"><a href="/en/aisles/deli-prepared-meals/antipasto-dips-pates">View all  Antipasto, Dips &amp; Pâtés</a></div><ul class="subNav--id--DP03"><li><a href="/en/aisles/deli-prepared-meals/antipasto-dips-pates/dips" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Antipasto, Dips &amp; Pâtés" data-grand-child-menu-name="Dips"><span>Dips</span></a></li><li><a href="/en/aisles/deli-prepared-meals/antipasto-dips-pates/hummus-spreads" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Antipasto, Dips &amp; Pâtés" data-grand-child-menu-name="Hummus &amp; Spreads"><span>Hummus &amp; Spreads</span></a></li><li><a href="/en/aisles/deli-prepared-meals/antipasto-dips-pates/pate-cretons" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Antipasto, Dips &amp; Pâtés" data-grand-child-menu-name="Pâté &amp; Cretons"><span>Pâté &amp; Cretons</span></a></li><li><a href="/en/aisles/deli-prepared-meals/antipasto-dips-pates/olives-antipasto" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Antipasto, Dips &amp; Pâtés" data-grand-child-menu-name="Olives &amp; Antipasto"><span>Olives &amp; Antipasto</span></a></li></ul><div class="aisles-all-link subNav--id--DP04"><a href="/en/aisles/deli-prepared-meals/ready-meals-sides">View all  Ready Meals &amp; Sides</a></div><ul class="subNav--id--DP04"><li><a href="/en/aisles/deli-prepared-meals/ready-meals-sides/appetizers-sides" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Ready Meals &amp; Sides" data-grand-child-menu-name="Appetizers &amp; Sides"><span>Appetizers &amp; Sides</span></a></li><li><a href="/en/aisles/deli-prepared-meals/ready-meals-sides/soups-stews" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Ready Meals &amp; Sides" data-grand-child-menu-name="Soups &amp; Stews"><span>Soups &amp; Stews</span></a></li><li><a href="/en/aisles/deli-prepared-meals/ready-meals-sides/meat-meals" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Ready Meals &amp; Sides" data-grand-child-menu-name="Meat Meals"><span>Meat Meals</span></a></li><li><a href="/en/aisles/deli-prepared-meals/ready-meals-sides/fish-seafood-meals" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Ready Meals &amp; Sides" data-grand-child-menu-name="Fish &amp; Seafood Meals"><span>Fish &amp; Seafood Meals</span></a></li><li><a href="/en/aisles/deli-prepared-meals/ready-meals-sides/noodle-pasta-rice-meals" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Ready Meals &amp; Sides" data-grand-child-menu-name="Noodle, Pasta &amp; Rice Meals"><span>Noodle, Pasta &amp; Rice Meals</span></a></li><li><a href="/en/aisles/deli-prepared-meals/ready-meals-sides/salads" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Ready Meals &amp; Sides" data-grand-child-menu-name="Salads"><span>Salads</span></a></li><a href="/en/aisles/deli-prepared-meals/ready-meals-sides/sandwiches-lunch-kits" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Ready Meals &amp; Sides" data-grand-child-menu-name="Sandwiches &amp; Lunch Kits"><span>Sandwiches &amp; Lunch Kits</span></a></li><li><a href="/en/aisles/deli-prepared-meals/ready-meals-sides/quiche-savoury-pies" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Ready Meals &amp; Sides" data-grand-child-menu-name="Quiche &amp; Savoury Pies"><span>Quiche &amp; Savoury Pies</span></a></li><li><a href="/en/aisles/deli-prepared-meals/ready-meals-sides/desserts-snacks" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Ready Meals &amp; Sides" data-grand-child-menu-name="Desserts &amp; Snacks"><span>Desserts &amp; Snacks</span></a></li><li><a href="/en/aisles/deli-prepared-meals/ready-meals-sides/prepared-dietary-meals" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Deli &amp; Prepared Meals" data-child-menu-name="Ready Meals &amp; Sides" data-grand-child-menu-name="Prepared Dietary Meals"><span>Prepared Dietary Meals</span></a></li></ul></div>
                cat("Beef", f"{BASE_URL}/en/aisles/deli-prepared-meals/deli-meats/beef"),
                cat("Turkey & Chicken", f"{BASE_URL}/en/aisles/deli-prepared-meals/deli-meats/turkey-chicken"),
                cat("Ham & Pork", f"{BASE_URL}/en/aisles/deli-prepared-meals/deli-meats/ham-pork"),
                cat("Bologna & Pastrami", f"{BASE_URL}/en/aisles/deli-prepared-meals/deli-meats/bologna-pastrami"),
                cat("Salami & Pepperoni", f"{BASE_URL}/en/aisles/deli-prepared-meals/deli-meats/salami-pepperoni"),
                cat("Prosciutto & Mortadella", f"{BASE_URL}/en/aisles/deli-prepared-meals/deli-meats/prosciutto-mortadella"),
                cat("Dry Sausages & Smoked Meat", f"{BASE_URL}/en/aisles/deli-prepared-meals/deli-meats/dry-sausages-smoked-meat")
            ]),
            cat("Antipasto, Dips & Pâtés", "", [
                cat("Dips", f"{BASE_URL}/en/aisles/deli-prepared-meals/antipasto-dips-pates/dips"),
                cat("Hummus & Spreads", f"{BASE_URL}/en/aisles/deli-prepared-meals/antipasto-dips-pates/hummus-spreads"),
                cat("Pâté & Cretons", f"{BASE_URL}/en/aisles/deli-prepared-meals/antipasto-dips-pates/pate-cretons"),
                cat("Olives & Antipasto", f"{BASE_URL}/en/aisles/deli-prepared-meals/antipasto-dips-pates/olives-antipasto")
            ]),
            cat("Ready Meals & Sides", "", [
                cat("Appetizers & Sides", f"{BASE_URL}/en/aisles/deli-prepared-meals/ready-meals-sides/appetizers-sides"),
                cat("Soups & Stews", f"{BASE_URL}/en/aisles/deli-prepared-meals/ready-meals-sides/soups-stews"),
                cat("Meat Meals", f"{BASE_URL}/en/aisles/deli-prepared-meals/ready-meals-sides/meat-meals"),
                cat("Fish & Seafood Meals", f"{BASE_URL}/en/aisles/deli-prepared-meals/ready-meals-sides/fish-seafood-meals"),
                cat("Noodle, Pasta & Rice Meals", f"{BASE_URL}/en/aisles/deli-prepared-meals/ready-meals-sides/noodle-pasta-rice-meals"),
                cat("Salads", f"{BASE_URL}/en/aisles/deli-prepared-meals/ready-meals-sides/salads"),
                cat("Sandwiches & Lunch Kits", f"{BASE_URL}/en/aisles/deli-prepared-meals/ready-meals-sides/sandwiches-lunch-kits"),
                cat("Quiche & Savoury Pies", f"{BASE_URL}/en/aisles/deli-prepared-meals/ready-meals-sides/quiche-savoury-pies"),
                cat("Desserts & Snacks", f"{BASE_URL}/en/aisles/deli-prepared-meals/ready-meals-sides/desserts-snacks"),
                cat("Prepared Dietary Meals", f"{BASE_URL}/en/aisles/deli-prepared-meals/ready-meals-sides/prepared-dietary-meals")
            ]),
            cat("Fresh Pizza, Pasta & Sauces", f"{BASE_URL}/en/aisles/deli-prepared-meals/fresh-pizza-pasta-sauces"),
            cat("Platters", f"{BASE_URL}/en/aisles/deli-prepared-meals/platters")
        ]),
        cat("Fish & Seafood", "", [
            cat("Fresh Fish", "", [
                cat("White Fish", f"{BASE_URL}/en/aisles/fish-seafood/fresh-fish/white-fish"),
                cat("Salmon, Trout & Tuna", f"{BASE_URL}/en/aisles/fish-seafood/fresh-fish/salmon-trout-tuna"),
                cat("Whole Fish", f"{BASE_URL}/en/aisles/fish-seafood/fresh-fish/whole-fish"),
                cat("Smoked Fish", f"{BASE_URL}/en/aisles/fish-seafood/fresh-fish/smoked-fish")
            ]),
            cat("Fresh Seafood", "", [
                cat("Scallops", f"{BASE_URL}/en/aisles/fish-seafood/fresh-seafood/scallops"),
                cat("Lobster, Crab & Pollock", f"{BASE_URL}/en/aisles/fish-seafood/fresh-seafood/lobster-crab-pollock"),
                cat("Shrimp & Scampi", f"{BASE_URL}/en/aisles/fish-seafood/fresh-seafood/shrimp-scampi"),
                cat("Mussels & Clams", f"{BASE_URL}/en/aisles/fish-seafood/fresh-seafood/mussels-clams"),
                cat("Squid & Calamari", f"{BASE_URL}/en/aisles/fish-seafood/fresh-seafood/squid-calamari"),
                cat("Oysters", f"{BASE_URL}/en/aisles/fish-seafood/fresh-seafood/oysters")
            ]),
            cat("Frozen Fish & Seafood", "", [
                cat("Seasoned & Breaded", f"{BASE_URL}/en/aisles/fish-seafood/frozen-fish-seafood/seasoned-breaded"),
                cat("Packages & Bulk", f"{BASE_URL}/en/aisles/fish-seafood/frozen-fish-seafood/packages-bulk"),
                cat("Appetizers & Hors d'Oeuvres", f"{BASE_URL}/en/aisles/fish-seafood/frozen-fish-seafood/appetizers-hors-d-oeuvres")
            ]),
            cat("Prepared Fish & Seafood", "", [
                cat("Prepared Fish & Seafood", f"{BASE_URL}/en/aisles/fish-seafood/prepared-fish-seafood/prepared-fish-seafood"),
                cat("Spreads, Mousse & Caviar", f"{BASE_URL}/en/aisles/fish-seafood/prepared-fish-seafood/spreads-mousse-caviar"),
                cat("Sushi", f"{BASE_URL}/en/aisles/fish-seafood/prepared-fish-seafood/sushi"),
                cat("Sushi & Fish Condiments", f"{BASE_URL}/en/aisles/fish-seafood/prepared-fish-seafood/sushi-fish-condiments")
            ])
        ]),
        cat("World Cuisine", "", [
            cat("Asian", f"{BASE_URL}/en/aisles/world-cuisine/asian"),
            cat("Latin", f"{BASE_URL}/en/aisles/world-cuisine/latin"),
            cat("Indian", f"{BASE_URL}/en/aisles/world-cuisine/indian"),
            cat("Mediterranean", f"{BASE_URL}/en/aisles/world-cuisine/mediterranean"),
            cat("Other International Products", f"{BASE_URL}/en/aisles/world-cuisine/other-international-products")
        ]),
        cat("Household & Cleaning", "", [
            cat("Paper", "", [
                cat("Paper Towels", f"{BASE_URL}/en/aisles/household-cleaning/paper/paper-towels"),
                cat("Bathroom Tissues", f"{BASE_URL}/en/aisles/household-cleaning/paper/bathroom-tissues"),
                cat("Facial Tissues", f"{BASE_URL}/en/aisles/household-cleaning/paper/facial-tissues"),
                cat("Paper Napkins", f"{BASE_URL}/en/aisles/household-cleaning/paper/paper-napkins")
            ]),
            cat("Laundry", "", [
                cat("Laundry Detergent", f"{BASE_URL}/en/aisles/household-cleaning/laundry/laundry-detergent"),
                cat("Softener", f"{BASE_URL}/en/aisles/household-cleaning/laundry/softener"),
                cat("Bleach", f"{BASE_URL}/en/aisles/household-cleaning/laundry/bleach")
            ]),
            cat("Dishwashing", "", [
                cat("Dishwashing Liquid", f"{BASE_URL}/en/aisles/household-cleaning/dishwashing/dishwashing-liquid"),
                cat("Dishwasher Detergents", f"{BASE_URL}/en/aisles/household-cleaning/dishwashing/dishwasher-detergents"),
                cat("Dishwasher Rinse Aid", f"{BASE_URL}/en/aisles/household-cleaning/dishwashing/dishwasher-rinse-aid")
            ]),
            cat("Household Cleaning", "", [
                cat("Multi-Purpose Cleaners", f"{BASE_URL}/en/aisles/household-cleaning/household-cleaning/multi-purpose-cleaners"),
                cat("Bathroom Cleaners", f"{BASE_URL}/en/aisles/household-cleaning/household-cleaning/bathroom-cleaners"),
                cat("Kitchen Cleaners", f"{BASE_URL}/en/aisles/household-cleaning/household-cleaning/kitchen-cleaners"),
                cat("Glass Cleaners", f"{BASE_URL}/en/aisles/household-cleaning/household-cleaning/glass-cleaners"),
                cat("Carpet & Fabric Cleaners", f"{BASE_URL}/en/aisles/household-cleaning/household-cleaning/carpet-fabric-cleaners"),
                cat("Other Cleaning Products", f"{BASE_URL}/en/aisles/household-cleaning/household-cleaning/other-cleaning-products"),
                cat("Cleaning Accessories", f"{BASE_URL}/en/aisles/household-cleaning/household-cleaning/cleaning-accessories")
            ]),
            cat("General Household", "", [
                cat("Garbage Bags", f"{BASE_URL}/en/aisles/household-cleaning/general-household/garbage-bags"),
                cat("Batteries", f"{BASE_URL}/en/aisles/household-cleaning/general-household/batteries"),
                cat("Air Fresheners", f"{BASE_URL}/en/aisles/household-cleaning/general-household/air-fresheners"),
                cat("Seasonal", f"{BASE_URL}/en/aisles/household-cleaning/general-household/seasonal"),
                cat("Others", f"{BASE_URL}/en/aisles/household-cleaning/general-household/others")
            ]),
            cat("Cooking & Kitchen Supplies", "", [
                cat("Food Bags & Containers", f"{BASE_URL}/en/aisles/household-cleaning/cooking-kitchen-supplies/food-bags-containers"),
                cat("Plastic Wrap", f"{BASE_URL}/en/aisles/household-cleaning/cooking-kitchen-supplies/plastic-wrap"),
                cat("Aluminium Foil & Plates", f"{BASE_URL}/en/aisles/household-cleaning/cooking-kitchen-supplies/aluminium-foil-plates"),
                cat("Cookware & Bakeware", f"{BASE_URL}/en/aisles/household-cleaning/cooking-kitchen-supplies/cookware-bakeware"),
                cat("Kitchen Tools & Utensils", f"{BASE_URL}/en/aisles/household-cleaning/cooking-kitchen-supplies/kitchen-tools-utensils"),
                cat("Disposable Tableware & Utensils", f"{BASE_URL}/en/aisles/household-cleaning/cooking-kitchen-supplies/disposable-tableware-utensils"),
                cat("Jars & Accessories for Preserves", f"{BASE_URL}/en/aisles/household-cleaning/cooking-kitchen-supplies/jars-accessories-for-preserves")
            ])
        ]),
        cat("Baby", "", [
            cat("Needs", "", [
                cat("Diapers & Training Pants", f"{BASE_URL}/en/aisles/baby/needs/diapers-training-pants"),
                cat("Wipes", f"{BASE_URL}/en/aisles/baby/needs/wipes"),
                cat("Health & Bathing", f"{BASE_URL}/en/aisles/baby/needs/health-bathing")
            ]),
            cat("Food & Formula", "", [
                cat("Formula", f"{BASE_URL}/en/aisles/baby/food-formula/formula"),
                cat("Food", f"{BASE_URL}/en/aisles/baby/food-formula/food"),
                cat("Cereal", f"{BASE_URL}/en/aisles/baby/food-formula/cereal"),
                cat("Snacks & Beverages", f"{BASE_URL}/en/aisles/baby/food-formula/snacks-beverages"),
                cat("Organic Food & Formula", f"{BASE_URL}/en/aisles/baby/food-formula/organic-food-formula")
            ])
        ]),
        cat("Health & Beauty", "", [
            cat("Face Care", "", [
                cat("Face Moisturizers", f"{BASE_URL}/en/aisles/health-beauty/face-care/face-moisturizers"),
                cat("Cleansers & Make Up Remover", f"{BASE_URL}/en/aisles/health-beauty/face-care/cleansers-make-up-remover"),
                cat("Cosmetics & Lip Care", f"{BASE_URL}/en/aisles/health-beauty/face-care/cosmetics-lip-care"),
                cat("Sun Care", f"{BASE_URL}/en/aisles/health-beauty/face-care/sun-care")
            ]),
            cat("Hair Care", "", [
                cat("Shampoos & Conditioners", f"{BASE_URL}/en/aisles/health-beauty/hair-care/shampoos-conditioners"),
                cat("Styling Products & Accessories", f"{BASE_URL}/en/aisles/health-beauty/hair-care/styling-products-accessories"),
                cat("Hair Colour & Treatments", f"{BASE_URL}/en/aisles/health-beauty/hair-care/hair-colour-treatments")
            ]),
            cat("Bath & Body Care", "", [
                cat("Soaps & Bodywash", f"{BASE_URL}/en/aisles/health-beauty/bath-body-care/soaps-bodywash"),
                cat("Salts, Soaks & Scrubs", f"{BASE_URL}/en/aisles/health-beauty/bath-body-care/salts-soaks-scrubs"),
                cat("Children's Bath Essentials", f"{BASE_URL}/en/aisles/health-beauty/bath-body-care/children-s-bath-essentials"),
                cat("Deodorant & Antiperspirant", f"{BASE_URL}/en/aisles/health-beauty/bath-body-care/deodorant-antiperspirant"),
                cat("Hand Soaps & Sanitizers", f"{BASE_URL}/en/aisles/health-beauty/bath-body-care/hand-soaps-sanitizers"),
                cat("Hand & Nail Care", f"{BASE_URL}/en/aisles/health-beauty/bath-body-care/hand-nail-care"),
                cat("Body & Foot Care", f"{BASE_URL}/en/aisles/health-beauty/bath-body-care/body-foot-care"),
                cat("Hair Removal", f"{BASE_URL}/en/aisles/health-beauty/bath-body-care/hair-removal"),
                cat("Cotton Balls & Swabs", f"{BASE_URL}/en/aisles/health-beauty/bath-body-care/cotton-balls-swabs"),
                cat("Sun Care", f"{BASE_URL}/en/aisles/health-beauty/bath-body-care/sun-care")
            ]),
            cat("Feminine Hygiene", "", [
                cat("Pads & Incontinence Products", f"{BASE_URL}/en/aisles/health-beauty/feminine-hygiene/pads-incontinence-products"),
                cat("Liners", f"{BASE_URL}/en/aisles/health-beauty/feminine-hygiene/liners"),
                cat("Tampons", f"{BASE_URL}/en/aisles/health-beauty/feminine-hygiene/tampons")
            ]),
            cat("Oral Care", "", [
                cat("Toothpaste", f"{BASE_URL}/en/aisles/health-beauty/oral-care/toothpaste"),
                cat("Toothbrushes", f"{BASE_URL}/en/aisles/health-beauty/oral-care/toothbrushes"),
                cat("Mouthwash & Dental Floss", f"{BASE_URL}/en/aisles/health-beauty/oral-care/mouthwash-dental-floss"),
                cat("Denture Care", f"{BASE_URL}/en/aisles/health-beauty/oral-care/denture-care")
            ]),
            cat("Men's Products", "", [
                cat("Antiperspirant & Deodorant", f"{BASE_URL}/en/aisles/health-beauty/men-s-products/antiperspirant-deodorant"),
                cat("Razors & Refills", f"{BASE_URL}/en/aisles/health-beauty/men-s-products/razors-refills"),
                cat("Shaving Cream & Aftershave", f"{BASE_URL}/en/aisles/healthy/men-s-products/shaving-cream-aftershave"),
                cat("Hair Care", f"{BASE_URL}/en/aisles/health-beauty/men-s-products/hair-care"),
                cat("Soaps & Bodywash", f"{BASE_URL}/en/aisles/health-beauty/men-s-products/soaps-bodywash")
            ])
        ]),
        cat("Pet Care", "", [
            cat("Dogs", "", [
                cat("Dry Dog Food", f"{BASE_URL}/en/aisles/pet-care/dogs/dry-dog-food"),
                cat("Canned Dog Food", f"{BASE_URL}/en/aisles/pet-care/dogs/canned-dog-food"),
                cat("Dog Treats & Care", f"{BASE_URL}/en/aisles/pet-care/dogs/dog-treats-care")
            ]),
            cat("Cats", "", [
                cat("Dry Cat Food", f"{BASE_URL}/en/aisles/pet-care/cats/dry-cat-food"),
                cat("Canned Cat Food", f"{BASE_URL}/en/aisles/pet-care/cats/canned-cat-food"),
                cat("Wet Cat Food & Care", f"{BASE_URL}/en/aisles/pet-care/cats/wet-cat-food-care")
            ]),
        ]),
        cat("Pharmacy", "", [
            cat("Healthcare Products", "", [
                cat("Cough, Cold & Flu", f"{BASE_URL}/en/aisles/pharmacy/healthcare-products/cough-cold-flu"),
                cat("Digestion & Nausea", f"{BASE_URL}/en/aisles/pharmacy/healthcare-products/digestion-nausea"),
                cat("First Aid", f"{BASE_URL}/en/aisles/pharmacy/healthcare-products/first-aid"),
                cat("Pain & Fever Relief", f"{BASE_URL}/en/aisles/pharmacy/healthcare-products/pain-fever-relief"),
                cat("Sleep & Snoring Aids", f"{BASE_URL}/en/aisles/pharmacy/healthcare-products/sleep-snoring-aids"),
                cat("Incontinence Products", f"{BASE_URL}/en/aisles/pharmacy/healthcare-products/incontinence-products")
            ]),
            cat("Vitamins, Supplements & Dietary Products", "", [
                cat("Single Vitamins & Minerals", f"{BASE_URL}/en/aisles/pharmacy/vitamins-supplements-dietary-products/single-vitamins-minerals"),
                cat("Natural Products", f"{BASE_URL}/en/aisles/pharmacy/vitamins-supplements-dietary-products/natural-products"),
                cat("Dietary Supplements", f"{BASE_URL}/en/aisles/pharmacy/vitamins-supplements-dietary-products/dietary-supplements"),
                cat("Meal Replacements & Bars", f"{BASE_URL}/en/aisles/pharmacy/vitamins-supplements-dietary-products/meal-replacements-bars")
            ])
        ]),
        cat("Nature's Signature", "", [
            cat("Pantry", "", [
                cat("Juice & Beverages", f"{BASE_URL}/en/aisles/nature-s-signature/pantry/juice-beverages")
            ])
        ])
    ]

def get_all_subcategories(page, categories, depth: int = 0) -> List[Dict]:
    indent = "   " * depth

    subcategories = []
    for category in categories:
        print(f"{indent}↳ {category['Category']}")
        products = extract_products_from_category(page, category["Url"], category["Category"])
        subcategories.append({
            "name": category["Category"],
            "gpc_code": "",
            "url": category["Url"],
            "subcategories": get_all_subcategories(page, category.get("Subcategories", []), depth + 1),
            "products": products
        })

    return subcategories

def extract_products_from_category(page, category_url: str, category_name: str) -> List[Dict]:
    if not category_url:
        return []

    global seen_skus
    page.goto(category_url)
    element = page.wait_for_selector('[data-total-results]', timeout=5000)

    product_data = []

    def calculate_total_pages(total_results_str: str) -> int:
        try:
            total = int(total_results_str)
            return (total // 30) + (1 if total % 30 > 0 else 0)
        except ValueError:
            return 1

    total_results = element.get_attribute('data-total-results')
    total_pages = calculate_total_pages(total_results)

    for page_number in range(1, total_pages + 1):
        if page_number > 1:
            page.goto(category_url + f"-page-{page_number}")
            page.wait_for_selector('[data-total-results]', timeout=5000)

        wrappers = page.query_selector_all('.default-product-tile')

        for wrapper in wrappers:
            try:
                link_el = wrapper.query_selector('a.product-details-link')
                href = link_el.get_attribute("href") if link_el else ""
                if not href:
                    continue

                sku = wrapper.get_attribute("data-product-code")
                if sku in seen_skus:
                    continue
                seen_skus.add(sku)

                name_el = wrapper.get_attribute("data-product-name")
                name = name_el.inner_text().strip() if name_el else ""

                quantity_el = wrapper.query_selector('span.head__unit-details')
                quantity = quantity_el.inner_text().strip() if quantity_el else ""

                price_el = wrapper.query_selector('div[data-main-price]')
                price = price_el.get_attribute("data-main-price") if price_el else ""

                brand_el = wrapper.query_selector('span.head__brand')
                brand = brand_el.inner_text().strip() if brand_el else ""

                product_data.append({
                    "name":  brand + " " + category_name,
                    "language": "en",
                    "company": "",
                    "brand": brand,
                    "gpc_code": "",
                    "variations": [
                        {
                            "name": name,
                            "url": BASE_URL + href,
                            "sku": sku,
                            "quantity": quantity,
                            "price": price
                        }
                    ]
                })

            except Exception as e:
                print(f"⚠️ Erro na extração: {e}")

    return product_data

def scrape_all_categories():
    global seen_skus
    seen_skus = set()

    categories = get_categories_structure()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        viewport: ViewportSize = {"width": 32767, "height": 32767}
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            viewport=viewport
        )
        page = context.new_page()
        all_data = []

        for category in categories:
            if category["Category"] not in whitelist_categories:
                continue

            print(f"\n📦 Category: {category['Category']}")
            subcategories = get_all_subcategories(page, category.get("Subcategories", []))
            products = extract_products_from_category(page, category["Url"], category["Category"])

            all_data.append({
                "name": category["Category"],
                "gpc_code": "",
                "url": category["Url"],
                "subcategories": subcategories,
                "products": products
            })

        browser.close()
        return { "categories": all_data }

