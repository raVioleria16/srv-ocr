from pydantic import BaseModel


class LocalProviderConfig(BaseModel):
    tesseract: str
