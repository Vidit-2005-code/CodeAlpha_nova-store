# NOVA Store — Django E-commerce Demo

A beginner-friendly full-stack e-commerce project built with Django, SQLite, HTML, CSS and JavaScript.

## Features
- Product catalogue, search and product detail pages
- Session-based shopping cart (add, update, remove)
- Registration, login and logout
- Checkout form and database-backed order processing
- Stock reduction when an order is placed
- Customer order history
- Django admin for products and order management
- Responsive layout

## Requirements
- Python 3.10 or newer
- VS Code (recommended)
- Internet connection for remote sample product photos and Google Fonts

## Run on Windows (VS Code terminal)
Open this project folder in VS Code, then run:

```powershell
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_products
py manage.py createsuperuser
py manage.py runserver
```

Open http://127.0.0.1:8000/

If `py` is not recognized, use `python` instead.

## Run on macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py createsuperuser
python manage.py runserver
```

## Admin panel
Visit http://127.0.0.1:8000/admin/ and sign in with the superuser created above. Add/edit products and review orders.

## Test the checkout
1. Register a customer account.
2. Add products to the cart.
3. Open Cart → Proceed to checkout.
4. Enter delivery details and place the order.
5. Check My orders and the admin panel.

## Important notes
- This is a local internship/demo project. It does **not** process real payments.
- Product photos are remote Unsplash images; the site can still run if images are unavailable.
- `DEBUG=True` and the development secret key are for local development only. Do not deploy this configuration publicly.
- Before submission, personalize the store name, styling, sample products and README so you can explain the implementation yourself.
