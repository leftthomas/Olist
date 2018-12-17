from flask import Flask, render_template, redirect

from utils import load_data

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', customer=customers.iloc[0])


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
    app.run()
