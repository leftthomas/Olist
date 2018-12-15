from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/orders')
def orders():
    return render_template('orders.html')


@app.route('/reviews')
def reviews():
    return render_template('reviews.html')


@app.route('/maps')
def maps():
    return render_template('maps.html')


# @app.route('/hello/<name>')
# def show_user_profile(name):
#     return render_template('dashboard.html', name=name)


if __name__ == '__main__':
    app.run()