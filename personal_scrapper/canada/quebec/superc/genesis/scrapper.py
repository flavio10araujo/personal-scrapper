from playwright.sync_api import sync_playwright, ViewportSize
from typing import List, Dict
import re

BASE_URL = "https://www.superc.ca"

# Global set to track seen SKUs
seen_skus = set()

def get_categories_structure():
    # Helper to build category dict
    def cat(name, url="", subcategories=None):
        return {
            "Category": name,
            "Url": url,
            "Subcategories": subcategories if subcategories is not None else []
        }

    return [
        [
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
            ])
        ],
        [
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
            ])
        ],
        [
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
            ])
        ],
        [
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
            ])
        ],
        [
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
            ])
        ],
        [
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
            ])
        ],
        [
            cat("Beer & Wine", "", [
                #<div class="aisles--subNav--lev3"><div class="aisles-all-link subNav--id--BV09 active--sub-nav"><a href="/en/aisles/beer-wine/wines-cocktails-coolers">View all  Wines, Cocktails &amp; Coolers</a></div><ul class="subNav--id--BV09 active--sub-nav"><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/red-wine" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Red Wine"><span>Red Wine</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/white-wine" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="White Wine"><span>White Wine</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/rose-wine" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Rosé Wine"><span>Rosé Wine</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/sparkling-wine" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Sparkling Wine"><span>Sparkling Wine</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/sangria" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Sangria"><span>Sangria</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/cocktails-other-wines" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Cocktails &amp; Other Wines"><span>Cocktails &amp; Other Wines</span></a></li><li><a href="/en/aisles/beer-wine/wines-cocktails-coolers/coolers" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Wines, Cocktails &amp; Coolers" data-grand-child-menu-name="Coolers"><span>Coolers</span></a></li></ul><div class="aisles-all-link subNav--id--BV10"><a href="/en/aisles/beer-wine/beer-cider">View all  Beer &amp; Cider</a></div><ul class="subNav--id--BV10"><li><a href="/en/aisles/beer-wine/beer-cider/classic-beer" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Classic Beer"><span>Classic Beer</span></a></li><li><a href="/en/aisles/beer-wine/beer-cider/classic-light-beer" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Classic Light Beer"><span>Classic Light Beer</span></a></li><li><a href="/en/aisles/beer-wine/beer-cider/specialty-flavoured-beer" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Specialty &amp; Flavoured Beer"><span>Specialty &amp; Flavoured Beer</span></a></li><li><a href="/en/aisles/beer-wine/beer-cider/imported-beer" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Imported Beer"><span>Imported Beer</span></a></li><li><a href="/en/aisles/beer-wine/beer-cider/artisanal-beer-microbrewery" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Artisanal Beer &amp; Microbrewery"><span>Artisanal Beer &amp; Microbrewery</span></a></li><li><a href="/en/aisles/beer-wine/beer-cider/cider" class=" dataLayerBigMenuLevelFour" data-menu-name="Aisles" data-sub-menu-name="Beer &amp; Wine" data-child-menu-name="Beer &amp; Cider" data-grand-child-menu-name="Cider"><span>Cider</span></a></li></ul></div>
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
            ])
        ],
        [
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
            ])
        ],
        [
            cat("Vegan & Vegetarian Food", "", [])
        ],
        [
            cat("Organic Groceries", "", [])
        ],
        [
            cat("Snacks", "", [])
        ],
        [
            cat("Frozen", "", [])
        ],
        [
            cat("Bread & Bakery Products", "", [])
        ],
        [
            cat("Deli & Prepared Meals", "", [])
        ],
        [
            cat("Fish & Seafood", "", [])
        ],
        [
            cat("World Cuisine", "", [])
        ],
        [
            cat("Household & Cleaning", "", [])
        ],
        [
            cat("Baby", "", [])
        ],
        [
            cat("Health & Beauty", "", [])
        ],
        [
            cat("Pet Care", "", [])
        ],
        [
            cat("Pharmacy", "", [])
        ],
        [
            cat("Nature's Signature", "", [])
        ],
        [
            cat("Lottery Tickets", "", [])
        ]
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
