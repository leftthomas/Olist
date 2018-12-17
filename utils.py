import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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

    # add total_value feature
    items['total_value'] = items['price'].add(items['freight_value'])
    # merge product_names_translations to products and replace it
    products = pd.merge(products, product_names_translations, on='product_category_name')
    products.drop(['product_category_name'], axis=1, inplace=True)
    products.rename(columns={'product_category_name_english': 'product_category_name'}, inplace=True)

    return customers, sellers, products, orders, items, payments, reviews, geolocations


def other():
    sns.set(rc={'figure.figsize': (16, 9)})

    df = pd.read_csv('data/classified_orders.csv')

    # creating a purchase day feature
    df['order_purchase_date'] = df.order_purchase_timestamp.dt.date

    # creating an aggregation
    sales_per_purchase_date = df.groupby('order_purchase_date', as_index=False).order_products_value.sum()
    ax = sns.lineplot(x="order_purchase_date", y="order_products_value", data=sales_per_purchase_date)
    ax.set_title('Sales per day')
    plt.show()

    # creating an aggregation
    avg_score_per_category = df.groupby('product_category_name', as_index=False).agg(
        {'review_score': ['count', 'mean']})
    avg_score_per_category.columns = ['product_category_name', 'count', 'mean']
    # filtering to show only categories with more than 50 reviews
    avg_score_per_category = avg_score_per_category[avg_score_per_category['count'] > 50]
    avg_score_per_category = avg_score_per_category.sort_values(by='mean', ascending=False)
    ax = sns.barplot(x="mean", y="product_category_name", data=avg_score_per_category)
    ax.set_title('Categories Review Score')
    plt.show()

    #
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    sns.distplot(df['total_value'], bins=800, kde=False, color='b')
    plt.xlim([0, 600])
    plt.show()
