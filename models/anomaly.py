from typing import Dict, Any, Tuple
import numpy as np
from sklearn.ensemble import IsolationForest
import sqlite3
import os

# We can load past expenses from DB to train IsolationForest, but for now we do simple z-score or static rules for immediate feedback if no history exists.

def detect_anomaly(amount: float, category: str, db_conn) -> Tuple[bool, str]:
    """
    Detect if an expense is anomalous.
    Returns (is_anomalous, reason)
    """
    if not amount or amount <= 0:
        return False, ""

    # Simple heuristic
    if amount > 10000:
        return True, "Unusually high absolute amount (> 10000)"

    # Get historical data for the category
    cursor = db_conn.cursor()
    cursor.execute("SELECT amount FROM invoices WHERE category = ?", (category,))
    rows = cursor.fetchall()
    
    if len(rows) < 5:
        return False, "Not enough historical data to detect anomaly"
        
    amounts = [row[0] for row in rows if row[0] is not None]
    
    # Fit Isolation Forest
    X = np.array(amounts).reshape(-1, 1)
    # Add current amount
    X_test = np.array([[amount]])
    
    clf = IsolationForest(contamination=0.1, random_state=42)
    clf.fit(X)
    
    prediction = clf.predict(X_test)[0] # -1 for anomaly, 1 for normal
    
    if prediction == -1:
        # Calculate z-score for better reasoning
        mean = np.mean(amounts)
        std = np.std(amounts)
        if std > 0:
            z_score = (amount - mean) / std
            if z_score > 2:
                return True, f"Unusually high amount compared to historical spending in '{category}' (z-score: {z_score:.2f})"
        return True, "Statistically anomalous amount for this category"
        
    return False, ""
