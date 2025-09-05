import os
import io
import pytest
from PIL import Image, ImageDraw, ImageFont
from fastapi.testclient import TestClient

from src.app import app
from src.ocr_service.tesseract_handler import TesseractHandler

client = TestClient(app)

def create_test_image(text="Test Text"):
    """Create a test image with text for testing OCR"""
    # Create a new image with a white background
    img = Image.new('RGB', (400, 100), color='white')
    draw = ImageDraw.Draw(img)
    
    # Use a basic font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    # Draw the text in black
    draw.text((10, 10), text, fill='black', font=font)
    
    # Save to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

def create_test_pdf():
    """Create a test PDF for testing PDF processing"""
    from reportlab.pdfgen import canvas
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 100, "Test PDF Text")
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

class TestOCRService:
    def test_ocr_image_endpoint(self):
        """Test OCR endpoint with an image"""
        test_image = create_test_image()
        response = client.post(
            "/api/v1/ocr",
            files={"file": ("test.png", test_image, "image/png")}
        )
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert "pages" in data
        assert data["pages"] == 1

    def test_ocr_pdf_endpoint(self):
        """Test OCR endpoint with a PDF"""
        test_pdf = create_test_pdf()
        response = client.post(
            "/api/v1/ocr",
            files={"file": ("test.pdf", test_pdf, "application/pdf")}
        )
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert "pages" in data
        assert "pages_content" in data
        assert isinstance(data["pages_content"], list)

    def test_invalid_file_type(self):
        """Test OCR endpoint with invalid file type"""
        response = client.post(
            "/api/v1/ocr",
            files={"file": ("test.txt", b"test content", "text/plain")}
        )
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

class TestTesseractHandler:
    def setup_method(self):
        self.handler = TesseractHandler()

    def test_process_image(self):
        """Test direct image processing"""
        test_image = create_test_image()
        result = self.handler.process_file(test_image, "image/png")
        assert isinstance(result, dict)
        assert "text" in result
        assert "pages" in result
        assert result["pages"] == 1

    def test_process_pdf(self):
        """Test PDF processing"""
        test_pdf = create_test_pdf()
        result = self.handler.process_file(test_pdf, "application/pdf")
        assert isinstance(result, dict)
        assert "text" in result
        assert "pages" in result
        assert "pages_content" in result
        assert isinstance(result["pages_content"], list)

    def test_invalid_content_type(self):
        """Test handler with invalid content type"""
        with pytest.raises(Exception) as exc_info:
            self.handler.process_file(b"test content", "text/plain")
        assert "Unsupported file type" in str(exc_info.value)

if __name__ == "__main__":
    # Setup test environment variables if needed
    os.environ["TESTING"] = "1"
    
    # Run the tests with pytest
    import pytest
    pytest.main([__file__, "-v", "-s"])
    
    # Example of manual test run
    print("\nManual Test Run Example:")
    handler = TesseractHandler()
    
    # Test with an image
    print("\nTesting with an image:")
    test_image = create_test_image("Sample Text")
    result = handler.process_file(test_image, "image/png")
    print(f"Image OCR Result: {result}")
    
    # Test with a PDF
    print("\nTesting with a PDF:")
    test_pdf = create_test_pdf()
    result = handler.process_file(test_pdf, "application/pdf")
    print(f"PDF OCR Result: {result}")
