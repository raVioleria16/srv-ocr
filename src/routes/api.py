from fastapi import APIRouter, UploadFile, HTTPException
from src.ocr_service.tesseract_handler import TesseractHandler

router = APIRouter()
ocr_handler = TesseractHandler()

@router.post("/ocr")
async def perform_ocr(file: UploadFile):
    if not (file.content_type.startswith('image/') or file.content_type == 'application/pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Unsupported file type. Please provide an image or PDF file."
        )
    
    content = await file.read()
    try:
        result = ocr_handler.process_file(content, file.content_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
