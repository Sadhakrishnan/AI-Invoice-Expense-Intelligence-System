import cv2
import pytesseract
import numpy as np

def extract_text_from_image(image_bytes: bytes) -> str:
    """Extracts text from an image using OpenCV and PyTesseract."""
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Could not decode image.")

    # Preprocessing
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    # Using adaptive thresholding for better results on invoices
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Remove noise
    kernel = np.ones((1, 1), np.uint8)
    img_processed = cv2.dilate(thresh, kernel, iterations=1)
    img_processed = cv2.erode(img_processed, kernel, iterations=1)
    
    # Run Tesseract OCR
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img_processed, config=custom_config)
    
    return text.strip()
