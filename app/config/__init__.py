from typing import Optional
from pydantic import BaseModel

from providers.entities import LocalProviderConfig

class InternalServices(BaseModel):
    pass

class ExternalServices(BaseModel):
    pass

class ProvidersConfig(BaseModel):
    local: LocalProviderConfig

class SrvConfig(BaseModel):
    name: str
    providers_config: ProvidersConfig
    internal_services: Optional[InternalServices] = None
    external_services: Optional[ExternalServices] = None
