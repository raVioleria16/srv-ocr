import os
from typing import Optional, Any
from pydantic import BaseModel, model_validator
from rv16_lib import logger
from rv16_lib.architecture.base_service_connector import BaseServiceConfig


class SrvConfigurationManager(BaseServiceConfig):
    ...

class ExtSrvConfig(BaseModel):
    srv_configuration_manager: SrvConfigurationManager

class SrvConfig(BaseModel):
    hostname: str
    port: int

    ext_srv: Optional[ExtSrvConfig] = None

    @model_validator(mode="before")
    @classmethod
    def load_from_env_vars(cls, data: Any) -> Any:
        if isinstance(data, dict):
            try:
                data["hostname"] = os.environ["PRJ_NAME"]
                data["port"] = int(os.environ["PORT"])
            except KeyError:
                logger.error("Be sure to set the environment variables PRJ_NAME and PORT in set_env.sh")
                raise
        return data
