from abc import abstractmethod

from rv16_lib.architecture.base_provider import BaseProvider
from rv16_lib.srv_ocr.entities import OCRServiceParams


class Provider(BaseProvider):
    """
    Implementation of a base provider class for the specific service.
    """

    @abstractmethod
    def process_image(self, image_bytes: bytes) -> str:
        pass

    @abstractmethod
    def process_pdf(self, pdf_bytes: bytes) -> list[str]:
        pass

    @abstractmethod
    def process_file(self, params: OCRServiceParams) -> dict:
        pass

    @abstractmethod
    def build_params(self, file_bytes: bytes, content_type: str) -> OCRServiceParams:
        pass