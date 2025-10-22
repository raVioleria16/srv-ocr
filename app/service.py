from rv16_lib import get_object_from_config
from rv16_lib.architecture.base_service import BaseService

from config import SrvConfig
from providers import ProviderType
from providers.local import LocalProvider


class Service(BaseService):

    def __init__(self):
        super().__init__()
        self.config = get_object_from_config(config_model=SrvConfig)
        self.service_name = self.config.name


    def initialize_service(self):

        self.providers = {
            ProviderType.LOCAL: LocalProvider(provider_config=self.config.providers_config.local,
                                              external_services=self.config.external_services)
        }


service = Service()
