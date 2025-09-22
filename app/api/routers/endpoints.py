"""API Router for various endpoints."""
from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from rv16_lib.srv_ocr.entities import OCRRequest

from service import service as srv

# Create an API Router
router = APIRouter()

# Example endpoint
@router.get("/health")
def health_check():
    response = {"health": "alive"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@router.post("/health")
def health_check(request_body: dict):
    response = {"health": "alive", "request_body": request_body}
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.post("/ocr")
# async def perform_ocr(file: UploadFile = File(...)):
async def ocr(request_body: OCRRequest) -> JSONResponse:
    if not srv or srv.providers == {}:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is not available",
        )

    provider = srv.get_provider(request_body.provider)
    file_content = request_body.file_content
    content_type = request_body.content_type


    if not (content_type.startswith('image/') or content_type == 'application/pdf'):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Unsupported file type. Please provide an image or PDF file."
        )
    
    # content = await file_content.read()
    try:
        response = provider.process_file(file_content, content_type)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
