from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import os
import sys

# Ensure parent directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db_connection, init_db
from pdf_loader import extract_text_from_pdf
from ocr import extract_text_from_image
from extraction.llm_extractor import extract_fields_with_llm
from models.categorization import categorize_expense
from models.anomaly import detect_anomaly
from analytics.insights import get_monthly_spending, get_category_distribution, get_top_vendors

app = FastAPI(title="Invoice Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/upload_invoice")
async def upload_invoice(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename.lower()
        
        # 1. Extraction
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(contents)
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            text = extract_text_from_image(contents)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from document")

        # 2. Field Extraction
        parsed_data = extract_fields_with_llm(text)
        
        # 3. Categorization
        category = categorize_expense(parsed_data.get("vendor"), text)
        parsed_data["category"] = category
        
        # 4. Database Connection & Anomaly Detection
        conn = get_db_connection()
        amount = parsed_data.get("total_amount")
        is_anomaly, reason = detect_anomaly(amount, category, conn)
        
        parsed_data["anomaly"] = is_anomaly
        parsed_data["anomaly_reason"] = reason
        
        # 5. Store in DB
        invoice_id = str(uuid.uuid4())
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO invoices (id, invoice_number, vendor, date, amount, category, anomaly, anomaly_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                invoice_id,
                parsed_data.get("invoice_number"),
                parsed_data.get("vendor"),
                parsed_data.get("date"),
                amount,
                category,
                is_anomaly,
                reason
            )
        )
        conn.commit()
        conn.close()
        
        parsed_data["id"] = invoice_id
        return parsed_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/invoices")
def get_invoices():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/analytics")
def get_analytics():
    conn = get_db_connection()
    monthly = get_monthly_spending(conn).to_dict(orient="records")
    category = get_category_distribution(conn).to_dict(orient="records")
    vendors = get_top_vendors(conn).to_dict(orient="records")
    conn.close()
    
    return {
        "monthly_spending": monthly,
        "category_distribution": category,
        "top_vendors": vendors
    }

@app.get("/anomalies")
def get_anomalies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices WHERE anomaly = 1")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
