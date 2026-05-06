# 🧾 AI Invoice + Expense Intelligence System

An end-to-end system that processes invoices (PDFs & images), extracts structured data, categorizes expenses, detects anomalies, and visualizes insights through a dashboard.

---

## 🚀 Overview

This project automates the full invoice pipeline:

- Upload invoices (PDFs / images)
- OCR-based text extraction
- Convert unstructured text → structured JSON
- Categorize expenses
- Detect anomalies/fraud
- Store data in a database
- Visualize insights in a dashboard

---

## 🎯 Objective

Build a production-ready system that converts raw invoices into actionable financial insights.

---

## 🧠 System Architecture

```
User Upload (PDF/Image)
        ↓
OCR + Document Parsing
        ↓
Text Preprocessing
        ↓
Field Extraction (LLM + Rules)
        ↓
Structured JSON
        ↓
Expense Categorization
        ↓
Anomaly Detection
        ↓
Analytics Engine
        ↓
Database Storage
        ↓
Dashboard UI
```

---

## 🧩 Features

### 📥 Document Ingestion
- Supports:
  - PDF invoices
  - Scanned images (JPG, PNG)
- Tools:
  - pdfplumber, PyPDF2

---

### 🔍 OCR Layer
- Tesseract OCR / EasyOCR
- OpenCV preprocessing:
  - Grayscale
  - Thresholding
  - Noise removal

---

### 🧠 Field Extraction

#### Rule-Based
- Regex for:
  - invoice_number
  - date
  - total

#### LLM-Based (Recommended)
Extract structured JSON:

```json
{
  "invoice_number": "INV-101",
  "vendor": "Amazon",
  "date": "2025-01-10",
  "total_amount": 12500
}
```

---

### 🏷️ Expense Categorization
Categories:
- Travel
- Food
- Office Supplies
- Utilities

Approach:
- ML (Logistic Regression / XGBoost)
- LLM fallback (hybrid)

---

### 🚨 Anomaly Detection
- Isolation Forest
- Z-score

Example:

```json
{
  "anomaly": true,
  "reason": "Unusually high amount compared to historical spending"
}
```

---

### 📊 Analytics
- Monthly trends
- Category distribution
- Top vendors

---

### 🗄️ Database

SQLite / PostgreSQL

```sql
invoices(
  id,
  vendor,
  date,
  amount,
  category,
  anomaly
)
```

---

## ⚙️ Backend (FastAPI)

Endpoints:

- `POST /upload_invoice` → Upload & process invoice  
- `GET /invoices` → Get all invoices  
- `GET /analytics` → Insights  
- `GET /anomalies` → Flagged invoices  

---

## 🎨 Frontend Dashboard

Built with Streamlit or React

Features:
- Upload invoices
- Table view
- Filters (date, vendor, category)
- Charts:
  - Pie (categories)
  - Line (monthly trends)
- Anomaly alerts

---

## 📊 Visualization

- Plotly
- Matplotlib

---

## 🛠️ Tech Stack

- Python
- FastAPI
- OpenCV
- Tesseract / EasyOCR
- scikit-learn, XGBoost
- OpenAI / Mistral / LLaMA
- SQLite / PostgreSQL
- Streamlit / React

---

## 📁 Project Structure

```
invoice-intelligence/
│
├── ingestion/
│   ├── pdf_loader.py
│   ├── ocr.py
│
├── extraction/
│   ├── llm_extractor.py
│   ├── regex_extractor.py
│
├── models/
│   ├── categorization.py
│   ├── anomaly.py
│
├── analytics/
│   └── insights.py
│
├── main.py
│
├── app.py
│
└── README.md
```

---

## ⚡ Setup

```bash
git clone https://github.com/your-username/invoice-intelligence.git
cd invoice-intelligence

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

---

## ▶️ Run

### Backend
```bash
uvicorn api.main:app --reload
```

### Frontend
```bash
streamlit run frontend/app.py
```

---

## 📌 Example Output

```json
{
  "invoice_number": "INV-001",
  "vendor": "Amazon",
  "date": "2025-01-10",
  "total": 12500,
  "category": "Office Supplies",
  "anomaly": false
}
```

---

## 📈 Metrics

- OCR Accuracy
- Extraction Accuracy
- Categorization Accuracy
- Anomaly Detection Precision

---

## 🔥 Advanced Features

- Multi-invoice comparison
- Duplicate detection
- Line-item extraction
- Voice queries
- RAG-based invoice search

---

## 💡 Best Practices

- Modular design
- Valid JSON outputs
- Logging & error handling
- Optimize performance
- Reduce LLM hallucinations

---

## 🤝 Contributing

Pull requests are welcome.

---

## 📜 License

MIT License
