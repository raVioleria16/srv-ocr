from typing import Optional
from pydantic import BaseModel

from providers.entities import LocalProviderConfig


class PairedServices(BaseModel):    # it should be a dict[str, ExtSrvConfig], but srv-ocr has no PairedServices
    pass

class ProvidersConfig(BaseModel):
    local: LocalProviderConfig

class SrvConfig(BaseModel):
    name: str
    providers_config: ProvidersConfig
    paired_services: Optional[PairedServices] = None
