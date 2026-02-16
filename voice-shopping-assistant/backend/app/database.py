import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager
from app.config import Config

DATABASE = Config.DATABASE

def init_db():
    """Initialize database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Shopping list table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shopping_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            quantity REAL,
            unit TEXT,
            price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed BOOLEAN DEFAULT 0
        )
    ''')
    
    # History table for suggestions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            frequency INTEGER DEFAULT 1
        )
    ''')
    
    # Seasonal items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seasonal_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            season TEXT,
            availability BOOLEAN DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    """Context manager for database connections"""
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

def add_shopping_item(item_name, category, quantity=1, unit='', price=None):
    """Add item to shopping list"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO shopping_list (item_name, category, quantity, unit, price)
            VALUES (?, ?, ?, ?, ?)
        ''', (item_name, category, quantity, unit, price))
        return cursor.lastrowid

def get_shopping_list():
    """Get all items in shopping list"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM shopping_list WHERE completed = 0')
        items = cursor.fetchall()
        return [dict(item) for item in items]

def remove_shopping_item(item_id):
    """Remove item from shopping list"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shopping_list WHERE id = ?', (item_id,))

def mark_item_complete(item_id):
    """Mark item as purchased"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE shopping_list SET completed = 1 WHERE id = ?', (item_id,))

def add_to_history(item_name, category):
    """Add item to purchase history for suggestions"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, frequency FROM purchase_history 
            WHERE item_name = ?
        ''', (item_name,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute('''
                UPDATE purchase_history SET frequency = frequency + 1 
                WHERE id = ?
            ''', (existing['id'],))
        else:
            cursor.execute('''
                INSERT INTO purchase_history (item_name, category)
                VALUES (?, ?)
            ''', (item_name, category))

def get_purchase_history():
    """Get purchase history sorted by frequency"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT item_name, category, frequency 
            FROM purchase_history 
            ORDER BY frequency DESC LIMIT 20
        ''')
        items = cursor.fetchall()
        return [dict(item) for item in items]
