import sqlite3
from datetime import datetime

DB_FILE = "expenses.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, item_name TEXT NOT NULL, category TEXT NOT NULL, amount REAL NOT NULL, date TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS budget 
                      (user_id INTEGER PRIMARY KEY, limit_amt REAL NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def register_user(username, password, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_expense(user_id, item_name, category, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (user_id, item_name, category, amount, date) VALUES (?, ?, ?, ?, ?)", 
                   (user_id, item_name, category, amount, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def clear_expenses(user_id):
    """Deletes all expense records for the specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_category_totals(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def set_budget(user_id, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO budget (user_id, limit_amt) VALUES (?, ?)", (user_id, amount))
    conn.commit()
    conn.close()

def get_budget(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT limit_amt FROM budget WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return float(row[0]) if row else 0.0

def get_total_spent(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return float(result) if result else 0.0

def get_all_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, category, amount, date FROM expenses WHERE user_id = ? ORDER BY date DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows