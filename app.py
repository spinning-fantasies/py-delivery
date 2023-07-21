from flask import Flask, render_template, request, redirect, url_for, session
from setup_database import create_tables
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to add a new user to the database
def add_user(username, password):
    with sqlite3.connect('delivery_app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()

# Function to find a user by username
def find_user(username):
    with sqlite3.connect('delivery_app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return cursor.fetchone()

# Function to add a new order to the database
def add_order(user_id, items, delivery_address, status):
    with sqlite3.connect('delivery_app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (user_id, items, delivery_address, status) VALUES (?, ?, ?, ?)',
                       (user_id, items, delivery_address, status))
        conn.commit()

# Function to get orders by user_id
def get_orders_by_user(user_id):
    with sqlite3.connect('delivery_app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE user_id = ?', (user_id,))
        return cursor.fetchall()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_user(username, password)
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = find_user(username)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            return redirect(url_for('place_order'))
        else:
            error_msg = 'Invalid username or password'
            return render_template('login.html', error_msg=error_msg)

    return render_template('login.html')

@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        items = request.form['items']
        delivery_address = request.form['delivery_address']
        status = 'Pending'
        add_order(session['user_id'], items, delivery_address, status)
        return redirect(url_for('order_status'))

    return render_template('place_order.html')

@app.route('/order_status')
def order_status():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    orders = get_orders_by_user(session['user_id'])
    return render_template('order_status.html', orders=orders)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
