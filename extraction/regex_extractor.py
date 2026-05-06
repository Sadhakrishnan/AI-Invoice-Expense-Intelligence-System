import re
from typing import Dict, Any
from datetime import datetime

def extract_fields_with_regex(text: str) -> Dict[str, Any]:
    """Fallback extraction mechanism using Regex."""
    data = {
        "invoice_number": None,
        "vendor": "Unknown Vendor",
        "date": None,
        "total_amount": 0.0
    }

    # Extract Invoice Number
    invoice_match = re.search(r'(?i)invoice\s*(?:no\.?|number|#)\s*[:\-]?\s*([A-Z0-9\-]+)', text)
    if invoice_match:
        data["invoice_number"] = invoice_match.group(1)

    # Extract Date
    date_match = re.search(r'(?i)date\s*[:\-]?\s*(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}|\d{4}[/\-\.]\d{1,2}[/\-\.]\d{1,2})', text)
    if date_match:
        data["date"] = date_match.group(1)
        # Try to standardize date format
        try:
            parsed_date = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"):
                try:
                    parsed_date = datetime.strptime(data["date"], fmt).strftime("%Y-%m-%d")
                    break
                except ValueError:
                    pass
            if parsed_date:
                data["date"] = parsed_date
        except Exception:
            pass

    # Extract Total Amount
    # Looking for 'Total' followed by currency and numbers
    total_match = re.search(r'(?i)total[^\d]*?[\$€£₹]?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', text)
    if total_match:
        amount_str = total_match.group(1).replace(',', '')
        try:
            data["total_amount"] = float(amount_str)
        except ValueError:
            pass

    return data
