import pdfplumber
import io

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts text from a PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()
