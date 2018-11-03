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

customers.to_csv('data/customers.csv', index=False)
geolocations.to_csv('data/geolocations.csv', index=False)
items.to_csv('data/items.csv', index=False)
payments.to_csv('data/payments.csv', index=False)
reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'])
reviews['review_answer_timestamp'] = pd.to_datetime(reviews['review_creation_date'])
reviews.to_csv('data/reviews.csv', index=False)
orders.dropna(inplace=True)
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])
orders.to_csv('data/orders.csv', index=False)
products.dropna(inplace=True)
products.to_csv('data/products.csv', index=False)
sellers.to_csv('data/sellers.csv', index=False)
product_names_translations.to_csv('data/translations.csv', index=False)
