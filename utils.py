import pandas as pd
import seaborn as sns


def load_data():
    customers = pd.read_csv('data/customers.csv')
    geolocations = pd.read_csv('data/geolocation.csv')
    items = pd.read_csv('data/items.csv', parse_dates=['shipping_limit_date'])
    payments = pd.read_csv('data/payments.csv')
    reviews = pd.read_csv('data/reviews.csv', parse_dates=['review_creation_date', 'review_answer_timestamp'])
    orders = pd.read_csv('data/orders.csv',
                         parse_dates=['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
                                      'order_delivered_customer_date', 'order_estimated_delivery_date'])
    products = pd.read_csv('data/products.csv')
    sellers = pd.read_csv('data/sellers.csv')
    product_names_translations = pd.read_csv('data/translation.csv')

    # add total_value feature
    items['total_value'] = items['price'].add(items['freight_value'])
    # merge product_names_translations to products and replace it
    products = pd.merge(products, product_names_translations, on='product_category_name')
    products.drop(['product_category_name'], axis=1, inplace=True)
    products.rename(columns={'product_category_name_english': 'product_category_name'}, inplace=True)

    return customers, sellers, products, orders, items, payments, reviews, geolocations


def other():
    sns.set(rc={'figure.figsize': (16, 9)})
    import matplotlib.pyplot as plt

    df = pd.read_csv('data/classified_orders.csv')
    df.order_purchase_timestamp = pd.to_datetime(df.order_purchase_timestamp)
    df.order_aproved_at = pd.to_datetime(df.order_aproved_at)
    df.order_estimated_delivery_date = pd.to_datetime(df.order_estimated_delivery_date)
    df.order_delivered_customer_date = pd.to_datetime(df.order_delivered_customer_date)
    df.review_creation_date = pd.to_datetime(df.review_creation_date)
    df.review_answer_timestamp = pd.to_datetime(df.review_answer_timestamp)

    # creating a purchase day feature
    df['order_purchase_date'] = df.order_purchase_timestamp.dt.date

    # creating an aggregation
    sales_per_purchase_date = df.groupby('order_purchase_date', as_index=False).order_products_value.sum()
    ax = sns.lineplot(x="order_purchase_date", y="order_products_value", data=sales_per_purchase_date)
    ax.set_title('Sales per day')
    plt.show()

    # creating a purchase day feature
    df['order_purchase_week'] = df.order_purchase_timestamp.dt.to_period('W').astype(str)

    # creating an aggregation
    sales_per_purchase_month = df.groupby('order_purchase_week', as_index=False).order_products_value.sum()
    ax = sns.lineplot(x="order_purchase_week", y="order_products_value", data=sales_per_purchase_month)
    ax.set_title('Sales per week')
    plt.show()

    # creating an aggregation
    avg_score_per_date = df.groupby('order_purchase_week', as_index=False).review_score.mean()
    ax = sns.lineplot(x="order_purchase_week", y="review_score", data=avg_score_per_date)
    ax.set_title('Average score per week')
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
