from flask import Flask, render_template, request, redirect, url_for, session, flash
from setup_database import create_tables
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager(app)

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

# Create a User class to store user information
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_id(self):
        return self.id

# Function to load a user from the database based on user_id
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        if find_user(username):
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('register'))

        # Add the new user to the database
        add_user(username, password)
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = find_user(username)
        if user and user[2] == password:
            user_obj = User(user[0])  # Create a User object
            login_user(user_obj)  # Log in the user
            return redirect(url_for('place_order'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    if request.method == 'POST':
        items = request.form['items']
        delivery_address = request.form['delivery_address']
        status = 'Pending'
        add_order(current_user.get_id(), items, delivery_address, status)
        return redirect(url_for('order_status'))

    return render_template('place_order.html')

@app.route('/order_status')
@login_required
def order_status():
    orders = get_orders_by_user(current_user.get_id())
    return render_template('order_status.html', orders=orders)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
