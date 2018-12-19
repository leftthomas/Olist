import pandas as pd


def load_data():
    customers = pd.read_csv('data/customers.csv')
    geolocations = pd.read_csv('data/geolocations.csv')
    items = pd.read_csv('data/items.csv')
    items['shipping_limit_date'] = pd.to_datetime(items['shipping_limit_date'])
    payments = pd.read_csv('data/payments.csv')
    reviews = pd.read_csv('data/reviews.csv')
    reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'])
    reviews['review_answer_timestamp'] = pd.to_datetime(reviews['review_answer_timestamp'])
    # remove fake data
    reviews = reviews[reviews['review_score'].isin(['1', '2', '3', '4', '5'])]
    reviews['review_score'] = reviews['review_score'].astype('int')
    orders = pd.read_csv('data/orders.csv')
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
    orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
    orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])
    products = pd.read_csv('data/products.csv')
    sellers = pd.read_csv('data/sellers.csv')
    product_names_translations = pd.read_csv('data/translations.csv')
    # merge product_names_translations to products and replace it
    products = pd.merge(products, product_names_translations, on='product_category_name')
    products.drop(['product_category_name'], axis=1, inplace=True)
    products.rename(columns={'product_category_name_english': 'product_category_name'}, inplace=True)

    return customers, sellers, products, orders, items, payments, reviews, geolocations

