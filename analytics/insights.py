import pandas as pd
import sqlite3

def get_monthly_spending(db_conn) -> pd.DataFrame:
    query = """
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM invoices
        WHERE date IS NOT NULL
        GROUP BY month
        ORDER BY month
    """
    return pd.read_sql_query(query, db_conn)

def get_category_distribution(db_conn) -> pd.DataFrame:
    query = """
        SELECT category, SUM(amount) as total
        FROM invoices
        GROUP BY category
    """
    return pd.read_sql_query(query, db_conn)

def get_top_vendors(db_conn) -> pd.DataFrame:
    query = """
        SELECT vendor, SUM(amount) as total
        FROM invoices
        WHERE vendor IS NOT NULL
        GROUP BY vendor
        ORDER BY total DESC
        LIMIT 5
    """
    return pd.read_sql_query(query, db_conn)
