"""API Router for various endpoints."""
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from rv16_lib.exceptions import RV16Exception
from starlette import status
from starlette.responses import JSONResponse


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
async def ocr(
        provider: Annotated[str, Form(description="The OCR provider to use.")],
        pdf_file: UploadFile = File(..., description="The PDF file to upload.")
) -> JSONResponse:

    if not srv or srv.providers == {}:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is not available",
        )

    try:
        provider = srv.get_provider(provider)
        file_content = await pdf_file.read()
        content_type = pdf_file.content_type

        response = provider.process_file(file_content, content_type)
        return response

    except RV16Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

