import io

import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
from starlette import status

from rv16_lib.exceptions import RV16Exception

from config import PairedServices
from providers.base_provider import Provider
from providers.entities import LocalProviderConfig


class LocalProvider(Provider):

    def __init__(self, provider_config: LocalProviderConfig, paired_services: PairedServices):
        self.tesseract_config = provider_config.tesseract

    def process_image(self, image_bytes: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image, config=self.tesseract_config)
            return text.strip()
        except Exception as e:
            raise Exception(f"OCR processing error: {str(e)}")

    def process_pdf(self, pdf_bytes: bytes) -> list[str]:
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

        if not (content_type.startswith('image/') or content_type == 'application/pdf'):
            raise RV16Exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Unsupported file type. Please provide an image or PDF file."
            )

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
