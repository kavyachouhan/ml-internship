# Village Pricing Django App

This Django application demonstrates a workflow for retrieving and displaying a restaurant’s menu, comparing local prices, simulating busy times and weather conditions, and using a simple ML model to adjust prices accordingly. It shows how to:

1. Scrape the menu of a restaurant (e.g., Village The Soul of India) from its website (or use fallback data if scraping fails).
2. Display nearby restaurants (mocked data).
3. Compute the lowest local price for each menu item.
4. Show busy times (mocked data).
5. Show weather conditions (mocked data).
6. Use a simple, mocked machine learning model to predict a price adjustment factor based on temperature, busyness, and precipitation.
7. Display original and adjusted prices on a webpage and log intermediate steps to the console.

## Requirements

- Python 3.8+
- pip (Python package manager)
- Django 3.0+
- Requests, BeautifulSoup4 (for scraping)
- scikit-learn (for the mock ML model)

You can install the required packages by running:

```bash
pip install django requests beautifulsoup4 scikit-learn
```

## Project Structure

A sample structure might look like:

```
myproject/
    manage.py
    myproject/
        __init__.py
        settings.py
        urls.py
        wsgi.py
    village_app/
        __init__.py
        views.py
        urls.py
        templates/
            village_info.html
    README.md
```

**Key Files:**
- `village_app/views.py`: Contains the logic for scraping, mocking data, training the ML model, and rendering the results.
- `village_app/templates/village_info.html`: The template used to display the results on a webpage.
- `village_app/urls.py` and `myproject/urls.py`: URL configuration for accessing the page.
- `README.md`: This file.

## Setup

1. **Create and Initialize the Django Project**:
   ```bash
   django-admin startproject myproject
   cd myproject
   python manage.py startapp village_app
   ```
   
2. **Add the Provided Code**:
   - Place the `VillagePricingView` code in `village_app/views.py`.
   - Add `village_info.html` into `village_app/templates/`.
   - Update `myproject/urls.py` and `village_app/urls.py` accordingly.

3. **Settings Configuration**:
   In `myproject/settings.py`, ensure:
   ```python
   INSTALLED_APPS = [
       # ...
       'village_app',
   ]

   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [BASE_DIR / "templates"],
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
               ],
           },
       },
   ]
   ```
   `APP_DIRS = True` ensures Django looks inside each app’s `templates` directory.

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

## Running the Project

Start the development server:
```bash
python manage.py runserver
```

After starting, you should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Viewing the Outputs

- **On the Console**:  
  The `print()` statements in `views.py` output intermediate steps:
  - Original menu details
  - Nearby restaurants and their menus
  - Computed lowest local prices
  - Busy factor
  - Weather conditions
  - Adjusted menu and price factor

  Check your terminal/console where `runserver` is running to see these logs.

- **On the Webpage**:  
  Open `http://127.0.0.1:8000/village-pricing/` in your browser. You’ll see a webpage rendered from the `village_info.html` template that displays:
  - Village details and original menu
  - Nearby restaurants and their menus
  - Lowest local prices per item
  - Busy factor
  - Weather conditions
  - Adjusted menu prices after applying the ML model’s factor

## Notes

- The HTML scraping code in `views.py` may need adjustments depending on the actual HTML structure of `villagesoulofindia.com`. If scraping fails, a fallback menu is used.
- The data for Yelp, Google Maps, and OpenWeather is mocked to avoid external API calls.
- The ML model is a simple linear regression trained on mock data, purely for demonstration.

## Troubleshooting

- **Template Not Found**:  
  If you encounter `django.template.exceptions.TemplateDoesNotExist: village_info.html`, ensure that:
  - `village_info.html` is in `village_app/templates/`.
  - `APP_DIRS = True` in `settings.py`.
  - You have restarted the server after adding the template.

- **Scraping Issues**:  
  If the actual website structure changes, update the CSS selectors in the scraping code. Otherwise, the fallback menu will be used.

- **ML Model or Data Issues**:  
  If scikit-learn or other dependencies are missing, run `pip install scikit-learn` again. Ensure Python 3.8+ is used.

## License

This code is provided for demonstration and educational purposes. Modify as needed for your use case.
```