import pytesseract
import numpy as np
import cv2
import fitz
from werkzeug.datastructures import FileStorage
from docx import Document

def get_text_from_pdf(file: FileStorage) -> str: 
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""

    for page in doc: 
        text += page.get_text()

    return text

def get_text_from_docx(file: FileStorage) -> str:
    text = ""
    doc = Document(file)

    for paragraph in doc.paragraphs: 
        text += paragraph.text + "\n"

    return text  

def get_text_from_image(file: FileStorage) -> str:
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return pytesseract.image_to_string(image)
