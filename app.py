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

    payments_values = payments[['payment_type', 'payment_value']].groupby('payment_type', as_index=False).sum()
    payments_values['payment_value'] = (
                payments_values['payment_value'] / payments_values['payment_value'].sum()).apply(
        lambda x: float('%.2f' % x))
    payments_values['payment_type'] = payments_values['payment_type'].apply(lambda x: x.replace('_', ' '))

    payments_numbers = payments[['order_id', 'payment_type']].drop_duplicates()
    payments_numbers = payments_numbers.groupby('payment_type', as_index=False).agg({'order_id': ['count']})
    payments_numbers.columns = ['payment_type', 'payment_type_count']
    payments_numbers['payment_type_count'] = (payments_numbers['payment_type_count'] / payments_numbers[
        'payment_type_count'].sum()).apply(lambda x: float('%.2f' % x))
    payments_numbers['payment_type'] = payments_numbers['payment_type'].apply(lambda x: x.replace('_', ' '))

    count_state = geolocations['geolocation_state'].value_counts()
    count_city = geolocations['geolocation_city'].value_counts()
    # fix the data error, the two rows are the single one same city
    count_city['sao paulo'] = count_city['são paulo'] + count_city['sao paulo']
    del count_city['são paulo']
    count_city['others'] = count_city[count_city < 10000].sum()
    count_city = count_city[count_city >= 10000]
    return render_template('dashboard.html', sales_per_purchase_date=sales_per_purchase_date,
                           sales_per_purchase_week=sales_per_purchase_week, payments_values=payments_values,
                           avg_score_per_category=avg_score_per_category, payments_numbers=payments_numbers,
                           count_state=count_state, count_city=count_city)


@app.route('/orders')
def orders():
    return render_template('orders.html')


@app.route('/reviews')
def reviews():
    return render_template('reviews.html')


@app.route('/maps')
def maps():
    # Removing some outliers
    # Brazils most Northern spot is at 5 deg 16′ 27.8″ N latitude.
    geo = geolocations[geolocations['geolocation_lat'] <= 5.27438888]
    # It’s most Western spot is at 73 deg, 58′ 58.19″W Long.
    geo = geo[geo['geolocation_lng'] >= -73.98283055]
    # It’s most Southern spot is at 33 deg, 45′ 04.21″ S Latitude.
    geo = geo[geo['geolocation_lat'] >= -33.75116944]
    # It’s most Eastern spot is 34 deg, 47′ 35.33″ W Long.
    geo = geo[geo['geolocation_lng'] <= -34.79314722]
    # fix the data error, the two rows are the single one same city
    geo['geolocation_city'].replace(['são paulo'], ['sao paulo'], inplace=True)
    return render_template('maps.html')


if __name__ == '__main__':
    customers, sellers, products, orders, items, payments, reviews, geolocations = load_data()
    app.run(debug=True)
