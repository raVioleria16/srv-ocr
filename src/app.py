from fastapi import FastAPI
from routes.api import router

app = FastAPI(title="OCR Service")
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6000)
