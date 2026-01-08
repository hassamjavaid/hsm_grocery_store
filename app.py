from flask import Flask, render_template, request, redirect, url_for, session
import random

# Tell Flask that HTML files are in the same folder
app = Flask(__name__, template_folder='.')

# Secure key for session management
app.secret_key = 'inu_21304_hassam_grocery'

# Mock Database
inventory = [
    {"id": 1, "name": "Organic Red Apples", "price": 180, "category": "Fresh Produce", "img": "🍎"},
    {"id": 2, "name": "Premium Basmati Rice", "price": 450, "category": "Packaged Goods", "img": "🌾"},
    {"id": 3, "name": "Fresh Farm Milk", "price": 210, "category": "Dairy", "img": "🥛"},
    {"id": 4, "name": "Natural Dish Soap", "price": 140, "category": "Household", "img": "🧼"}
]

@app.route('/')
def index():
    return render_template('index.html', products=inventory)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    product = next((item for item in inventory if item["id"] == product_id), None)
    if product:
        session['cart'].append(product)
        session.modified = True

    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', items=cart_items, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    session['customer_name'] = request.form.get('name')
    session['address'] = request.form.get('address')
    session['order_id'] = random.randint(1000, 9999)
    session.pop('cart', None)
    return redirect(url_for('track_order'))

@app.route('/track')
def track_order():
    order_info = {
        "id": session.get('order_id', '0000'),
        "name": session.get('customer_name', 'Customer'),
        "address": session.get('address', 'Peshawar'),
        "status": "Out for Delivery"
    }
    return render_template('track.html', order=order_info)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
