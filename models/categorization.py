import re

CATEGORIES = [
    "Travel",
    "Food",
    "Office Supplies",
    "Utilities",
    "Other"
]

def categorize_expense(vendor: str, text: str) -> str:
    """
    Classify the expense based on vendor name and text.
    Uses simple rule-based approach as baseline.
    """
    text_lower = text.lower()
    vendor_lower = vendor.lower() if vendor else ""

    # Keywords for categories
    travel_keywords = ["uber", "lyft", "airline", "hotel", "taxi", "flight"]
    food_keywords = ["restaurant", "cafe", "food", "doordash", "ubereats", "pizza", "coffee"]
    office_keywords = ["amazon", "staples", "paper", "desk", "computer", "software", "monitor"]
    utilities_keywords = ["electric", "water", "internet", "comcast", "verizon", "att"]

    if any(k in vendor_lower or k in text_lower for k in travel_keywords):
        return "Travel"
    elif any(k in vendor_lower or k in text_lower for k in food_keywords):
        return "Food"
    elif any(k in vendor_lower or k in text_lower for k in office_keywords):
        return "Office Supplies"
    elif any(k in vendor_lower or k in text_lower for k in utilities_keywords):
        return "Utilities"
    
    return "Other"
