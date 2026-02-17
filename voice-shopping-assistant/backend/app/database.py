import sqlite3
from contextlib import contextmanager
from app.config import Config

DATABASE = Config.DATABASE

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Table 1: Shopping List
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shopping_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            quantity REAL DEFAULT 1,
            unit TEXT,
            price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed BOOLEAN DEFAULT 0
        )
    ''')
    # Table 2: Purchase History
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            frequency INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def add_shopping_item(item_name, category, quantity=1):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO shopping_list (item_name, category, quantity)
            VALUES (?, ?, ?)
        ''', (item_name, category, quantity))
        return cursor.lastrowid

def get_shopping_list():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM shopping_list WHERE completed = 0')
        return [dict(row) for row in cursor.fetchall()]

def remove_shopping_item(item_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shopping_list WHERE id = ?', (item_id,))
        return cursor.rowcount > 0

def remove_item_by_name(item_name):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shopping_list WHERE LOWER(item_name) = LOWER(?)', (item_name.strip(),))
        return cursor.rowcount > 0

def mark_item_complete(item_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE shopping_list SET completed = 1 WHERE id = ?', (item_id,))
        return cursor.rowcount > 0

def add_to_history(item_name, category):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, frequency FROM purchase_history WHERE item_name = ?', (item_name,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute('UPDATE purchase_history SET frequency = frequency + 1 WHERE id = ?', (existing['id'],))
        else:
            cursor.execute('INSERT INTO purchase_history (item_name, category) VALUES (?, ?)', (item_name, category))

def get_purchase_history():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM purchase_history ORDER BY frequency DESC LIMIT 20')
        return [dict(row) for row in cursor.fetchall()]