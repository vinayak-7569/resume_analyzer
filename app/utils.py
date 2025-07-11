from io import BytesIO
from pdfminer.high_level import extract_text
from werkzeug.datastructures import FileStorage
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
from langdetect import detect

def extract_text_from_pdf(file: FileStorage) -> str:
    if not file.filename.lower().endswith('.pdf'):
        return "Error: Invalid file type. Please upload a PDF."

    max_file_size = 5 * 1024 * 1024  # 5 MB
    file.stream.seek(0, 2)
    file_size = file.stream.tell()
    file.stream.seek(0)

    if file_size > max_file_size:
        return "Error: File too large. Maximum allowed size is 5 MB."

    try:
        file_bytes = BytesIO(file.read())
        text = extract_text(file_bytes).strip().replace('\x00', '')

        if not text:
            images = convert_from_bytes(file_bytes.getvalue())
            ocr_text = ''
            for image in images:
                ocr_text += pytesseract.image_to_string(image)

            if not ocr_text.strip():
                return "Error: PDF contains images but no readable text (even via OCR)."
            return ocr_text.strip()

        return text
    except Exception as e:
        print(f"[PDF Extraction Error] {str(e)}")
        return "Error: Failed to extract text from PDF."

def is_english(text):
    try:
        if len(text) < 20:
            return False
        return detect(text) == 'en'
    except:
        return False
