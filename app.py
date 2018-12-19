import pandas as pd
from flask import Flask, render_template, redirect

from utils import load_data

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    order_values = items[['order_id', 'price']].groupby('order_id').sum()
    summed_orders = pd.merge(orders[['order_id', 'order_purchase_timestamp']], order_values, on='order_id')
    # creating purchase feature
    summed_orders['order_purchase_date'] = summed_orders['order_purchase_timestamp'].dt.date.apply(
        lambda x: x.strftime('%Y-%m-%d'))
    summed_orders['order_purchase_week'] = summed_orders['order_purchase_timestamp'].dt.date.apply(
        lambda x: x.strftime('%A'))
    # creating aggregations
    sales_per_purchase_date = summed_orders.groupby('order_purchase_date', as_index=False).sum()
    sales_per_purchase_date['price'] = sales_per_purchase_date['price'].apply(lambda x: float('%.2f' % x))
    sales_per_purchase_week = summed_orders.groupby('order_purchase_week', as_index=False).sum()
    sales_per_purchase_week['price'] = sales_per_purchase_week['price'].apply(lambda x: float('%.2f' % (x / 1000)))
    list_sorted = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sales_per_purchase_week['order_purchase_week'] = sales_per_purchase_week['order_purchase_week'].astype(
        'category').cat.set_categories(list_sorted)
    sales_per_purchase_week = sales_per_purchase_week.sort_values(by=['order_purchase_week'], ascending=True)

    merged_reviews = pd.merge(reviews[['order_id', 'review_score']], items[['order_id', 'product_id']], how='left',
                              on='order_id')
    merged_reviews = pd.merge(merged_reviews, products[['product_id', 'product_category_name']], how='left',
                              on='product_id')
    # creating an aggregation
    avg_score_per_category = merged_reviews.groupby('product_category_name', as_index=False).agg(
        {'review_score': ['count', 'mean']})
    avg_score_per_category.columns = ['product_category_name', 'review_score_count', 'review_score_mean']
    # filtering to show only categories with more than 50 reviews
    avg_score_per_category = avg_score_per_category[avg_score_per_category['review_score_count'] > 50]
    avg_score_per_category['product_category_name'] = avg_score_per_category['product_category_name'].apply(
        lambda x: x.replace('_', ' '))
    avg_score_per_category['review_score_mean'] = avg_score_per_category['review_score_mean'].apply(
        lambda x: float('%.2f' % x))

    payments_values = payments[['order_id', 'payment_type']].drop_duplicates()
    payments_values = payments_values.groupby('payment_type', as_index=False).agg({'order_id': ['count']})
    payments_values.columns = ['payment_type', 'payment_type_count']
    payments_values['payment_type'] = payments_values['payment_type'].apply(lambda x: x.replace('_', ' '))
    return render_template('dashboard.html', sales_per_purchase_date=sales_per_purchase_date,
                           sales_per_purchase_week=sales_per_purchase_week,
                           avg_score_per_category=avg_score_per_category, payments_values=payments_values)


@app.route('/orders')
def orders():
    return render_template('orders.html')


@app.route('/reviews')
def reviews():
    return render_template('reviews.html')


@app.route('/maps')
def maps():
    return render_template('maps.html')


if __name__ == '__main__':
    customers, sellers, products, orders, items, payments, reviews, geolocations = load_data()
    app.run(debug=True)
