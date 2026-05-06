import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "invoices.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id TEXT PRIMARY KEY,
            invoice_number TEXT,
            vendor TEXT,
            date TEXT,
            amount REAL,
            category TEXT,
            anomaly BOOLEAN,
            anomaly_reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
