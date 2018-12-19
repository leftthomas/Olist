import pandas as pd
from flask import Flask, render_template, redirect

from utils import load_data

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    order_values = items.drop(['order_item_id', 'product_id', 'seller_id', 'shipping_limit_date'], axis=1)
    order_values = order_values.groupby('order_id').sum()
    summed_orders = pd.merge(orders, order_values, on='order_id')
    # creating purchase feature
    summed_orders = summed_orders[summed_orders['order_purchase_timestamp'] >= pd.datetime(2018, 1, 1)]
    summed_orders['order_purchase_month'] = summed_orders['order_purchase_timestamp'].dt.month
    # creating an aggregation
    sales_per_purchase_month = summed_orders.groupby('order_purchase_month', as_index=False).sum()
    sales_per_purchase_month["price"] = sales_per_purchase_month["price"] / 1000

    # # creating an aggregation
    # avg_score_per_category = df.groupby('product_category_name', as_index=False).agg(
    #     {'review_score': ['count', 'mean']})
    # avg_score_per_category.columns = ['product_category_name', 'count', 'mean']
    # # filtering to show only categories with more than 50 reviews
    # avg_score_per_category = avg_score_per_category[avg_score_per_category['count'] > 50]
    # avg_score_per_category = avg_score_per_category.sort_values(by='mean', ascending=False)
    # ax = sns.barplot(x="mean", y="product_category_name", data=avg_score_per_category)
    # ax.set_title('Categories Review Score')
    # plt.show()
    #
    # sns.distplot(df['total_value'], bins=800, kde=False, color='b')
    # plt.xlim([0, 600])
    # plt.show()

    return render_template('dashboard.html', sales_per_purchase_month=sales_per_purchase_month)


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
