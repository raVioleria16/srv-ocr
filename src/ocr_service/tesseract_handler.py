import pytesseract
from PIL import Image
import io
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
from typing import List, Optional

class TesseractHandler:
    def __init__(self):
        self.tesseract_config = r'--oem 3 --psm 6'

    def process_image(self, image_bytes: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image, config=self.tesseract_config)
            return text.strip()
        except Exception as e:
            raise Exception(f"OCR processing error: {str(e)}")

    def process_pdf(self, pdf_bytes: bytes) -> List[str]:
        try:
            # First try to extract text directly from PDF
            pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
            text_results = []
            
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text.strip():  # If we got meaningful text
                    text_results.append(text.strip())
                else:  # If no text found, try OCR
                    images = convert_from_bytes(pdf_bytes, fmt='png')
                    for image in images:
                        text = pytesseract.image_to_string(image, config=self.tesseract_config)
                        if text.strip():
                            text_results.append(text.strip())

            return text_results
        except Exception as e:
            raise Exception(f"PDF processing error: {str(e)}")

    def process_file(self, file_bytes: bytes, content_type: str) -> dict:
        if content_type.startswith('image/'):
            text = self.process_image(file_bytes)
            return {"text": text, "pages": 1}
        elif content_type == 'application/pdf':
            texts = self.process_pdf(file_bytes)
            return {
                "text": "\n\n".join(texts),
                "pages": len(texts),
                "pages_content": texts
            }
        else:
            raise Exception("Unsupported file type. Please provide an image or PDF file.")
