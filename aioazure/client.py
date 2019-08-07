from .auth import Authentication
from .resources import resource_classes
from .resources import resource_names

from simple_rest_client.api import API
from typing import Any


class AzureClient(object):
    def __init__(self, api_url: str, subscription_id: str, resource_group_name: str,
                 auth: Authentication, timeout: int = 60) -> None:
        self.api_url = f"{api_url}/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers"
        self.api = None
        self.auth = auth
        self.timeout = timeout

    async def init_api(self) -> None:
        if not (self.api and self.auth.is_token_valid):
            await self.auth.get_credentials()
            self.api = API(api_root_url=self.api_url,
                           json_encode_body=True,
                           headers={"Accept": "application/json",
                                    "Authorization": self.auth.token,
                                    "Content-Type": "application/json"},
                           timeout=self.timeout)
            for resource_name, resource_class in zip(resource_names, resource_classes):
                self.api.add_resource(resource_name=resource_name, resource_class=resource_class)

    def __getattr__(self, item: str) -> Any:
        return getattr(self.api, item)
