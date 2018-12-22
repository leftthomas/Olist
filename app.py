from flask import Flask, render_template, redirect

from utils import load_data

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', sales_per_purchase_date=sales_per_purchase_date,
                           sales_per_purchase_week=sales_per_purchase_week, payments_values=payments_values,
                           avg_score_per_category=avg_score_per_category, payments_numbers=payments_numbers,
                           count_state=count_state, count_city=count_city, count_product=count_product,
                           count_comment=count_comment)


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
    sales_per_purchase_date, sales_per_purchase_week, payments_values, avg_score_per_category, payments_numbers, \
    count_state, count_city, count_product, count_comment, geo, merged_customers, merged_sellers, merged_orders, \
    merged_sp_customers, merged_spc_customers = load_data()
    app.run(debug=True)
