import sqlite3

DATABASE = 'delivery_app.db'

def create_tables():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Create the users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Create the orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                items TEXT NOT NULL,
                delivery_address TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

if __name__ == '__main__':
    create_tables()
