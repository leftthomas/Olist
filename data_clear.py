import pandas as pd

customers = pd.read_csv('data/olist_customers_dataset.csv')
geolocations = pd.read_csv('data/olist_geolocation_dataset.csv')
items = pd.read_csv('data/olist_order_items_dataset.csv')
payments = pd.read_csv('data/olist_order_payments_dataset.csv')
reviews = pd.read_csv('data/olist_order_reviews_dataset.csv')
orders = pd.read_csv('data/olist_orders_dataset.csv')
products = pd.read_csv('data/olist_products_dataset.csv')
sellers = pd.read_csv('data/olist_sellers_dataset.csv')
product_names_translations = pd.read_csv('data/product_category_name_translation.csv')

customers.to_csv('data/customers.csv')
geolocations.to_csv('data/geolocations.csv')
items.to_csv('data/items.csv')
payments.to_csv('data/payments.csv')
reviews.to_csv('data/reviews.csv')
orders.dropna(inplace=True)
orders.to_csv('data/orders.csv')
products.dropna(inplace=True)
products.to_csv('data/products.csv')
sellers.to_csv('data/sellers.csv')
product_names_translations.to_csv('data/translations.csv')
