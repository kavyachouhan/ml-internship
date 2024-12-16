import requests
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from bs4 import BeautifulSoup
import numpy as np
from sklearn.linear_model import LinearRegression

# -------------------- MOCK DATA & CONFIG --------------------
VILLAGE_NAME = "Village The Soul of India"
VILLAGE_WEBSITE_URL = "https://villagesoulofindia.com/"
VILLAGE_ADDRESS = "184 Bethpage Rd, Hicksville, NY 11801"
VILLAGE_HOURS = [
    {"day": "Monday", "start": "11:30", "end": "22:00"},
    {"day": "Tuesday", "start": "11:30", "end": "22:00"},
]

MOCK_NEARBY_RESTAURANTS = [
    {
        "name": "Mock Indian Bistro",
        "address": "123 Mock St, Hicksville, NY 11801",
        "menu_items": [
            {"item": "Paneer Tikka Masala", "price": 11.99},
            {"item": "Chicken Biryani", "price": 14.50},
            {"item": "Naan Basket", "price": 5.99}
        ],
        "rating": 4.5
    },
    {
        "name": "Spicy Curry Palace",
        "address": "456 Curry Ave, Hicksville, NY 11801",
        "menu_items": [
            {"item": "Paneer Tikka Masala", "price": 12.50},
            {"item": "Chicken Biryani", "price": 13.99},
            {"item": "Naan Basket", "price": 6.50}
        ],
        "rating": 4.0
    }
]

MOCK_BUSY_FACTOR = 80  # %
MOCK_WEATHER = {
    "temperature_f": 42.0,
    "weather_description": "light rain",
    "raining": True,
    "snowing": False
}

# -------------------- SCRAPING FUNCTION --------------------
def scrape_village_menu():
    # Attempt to scrape actual menu; if fail, use mock
    try:
        response = requests.get(VILLAGE_WEBSITE_URL)
        if response.status_code != 200:
            raise Exception("Failed to load website.")
        soup = BeautifulSoup(response.text, 'html.parser')

        menu = []
        # Placeholder selectors, adjust to actual site structure:
        for item_div in soup.select('.menu-item'):
            name_tag = item_div.select_one('.item-name')
            price_tag = item_div.select_one('.item-price')
            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price_str = price_tag.get_text(strip=True).replace('$', '')
                try:
                    price = float(price_str)
                    menu.append({"item": name, "price": price})
                except ValueError:
                    continue

        if not menu:
            menu = [
                {"item": "Paneer Tikka Masala", "price": 12.99},
                {"item": "Chicken Biryani", "price": 13.99},
                {"item": "Naan Basket", "price": 6.99}
            ]
        return menu
    except Exception:
        return [
            {"item": "Paneer Tikka Masala", "price": 12.99},
            {"item": "Chicken Biryani", "price": 13.99},
            {"item": "Naan Basket", "price": 6.99}
        ]

# -------------------- SIMPLE ML MODEL --------------------
def train_dummy_model():
    X = [
        [30, 80, 1],
        [60, 50, 0],
        [40, 90, 1],
        [50, 30, 0],
        [45, 85, 1],
        [70, 10, 0]
    ]
    y = [
        1.2,
        1.0,
        1.2,
        1.0,
        1.2,
        1.0
    ]
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_price_factor(model, temp_f, busy_factor, raining, snowing):
    precip = 1 if (raining or snowing) else 0
    X_test = np.array([[temp_f, busy_factor, precip]])
    factor = model.predict(X_test)[0]
    factor = max(1.0, min(1.3, factor))
    return factor

# -------------------- VIEW --------------------
class VillagePricingView(View):
    def get(self, request):
        # Step 1: Get Village info
        menu_items = scrape_village_menu()
        village_info = {
            "name": VILLAGE_NAME,
            "address": VILLAGE_ADDRESS,
            "menu_items": menu_items,
            "opening_times": VILLAGE_HOURS
        }
        print("Step 1: Village Info:", village_info)

        # Step 2 & 3: Nearby restaurants & their menus
        nearby_restaurants = MOCK_NEARBY_RESTAURANTS
        print("Step 2 & 3: Nearby Restaurants:", nearby_restaurants)

        # Compute lowest local prices
        all_menus = [r["menu_items"] for r in nearby_restaurants] + [village_info["menu_items"]]
        all_items = {}
        for menu in all_menus:
            for m in menu:
                item_name = m["item"].lower()
                if item_name not in all_items:
                    all_items[item_name] = []
                all_items[item_name].append(m["price"])
        lowest_local_prices = {item: min(prices) for item, prices in all_items.items()}
        print("Lowest Local Prices by Item:", lowest_local_prices)

        # Busy factor (Step 4)
        busy_factor = MOCK_BUSY_FACTOR
        print("Step 4: Busy Factor:", busy_factor)

        # Weather (Step 5)
        weather = MOCK_WEATHER
        print("Step 5: Weather:", weather)

        # Train the ML model and predict (Step 6 & 7)
        model = train_dummy_model()

        base_village_menu = []
        for vi in village_info["menu_items"]:
            item_lower = vi["item"].lower()
            base_price = lowest_local_prices.get(item_lower, vi["price"])
            base_village_menu.append({"item": vi["item"], "price": base_price})

        factor = predict_price_factor(
            model,
            temp_f=weather["temperature_f"],
            busy_factor=busy_factor,
            raining=weather["raining"],
            snowing=weather["snowing"]
        )

        adjusted_menu = []
        for item in base_village_menu:
            adjusted_price = round(item["price"] * factor, 2)
            adjusted_menu.append({
                "item": item["item"],
                "base_price": item["price"],
                "adjusted_price": adjusted_price
            })
        print("Step 6 & 7: Adjusted Menu with Predicted Prices:", adjusted_menu)
        print("Price Factor Used:", factor)

        # Render results on a webpage
        context = {
            "village_info": {
                "name": village_info["name"],
                "address": village_info["address"],
                "opening_times": village_info["opening_times"],
                "original_menu": village_info["menu_items"]
            },
            "nearby_restaurants": nearby_restaurants,
            "lowest_local_prices_by_item": lowest_local_prices,
            "busy_factor": busy_factor,
            "weather": weather,
            "adjusted_village_menu": adjusted_menu,
            "price_factor_used": factor
        }

        return render(request, 'village_info.html', context)
