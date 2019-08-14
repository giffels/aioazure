from .auth import Authenticator
from .decorator import AuthDecorator
from .decorator import ResponseDecorator
from .resources import resource_classes
from .resources import resource_names
from .proxy import Proxy
from .proxy import ResourceProxy

from simple_rest_client.api import API


class AzureClient(object):
    def __init__(self, api_url: str, subscription_id: str, resource_group_name: str,
                 auth: Authenticator, timeout: int = 60) -> None:
        self.api_url = f"{api_url}/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers"
        self.api = API(api_root_url=self.api_url,
                       json_encode_body=True,
                       headers={"Accept": "application/json",
                                "Content-Type": "application/json"},
                       timeout=timeout)
        self.auth = auth

        for resource_name, resource_class in zip(resource_names, resource_classes):
            self.api.add_resource(resource_name=resource_name, resource_class=resource_class)

    def __getattr__(self, resource: str) -> Proxy:
        return AuthDecorator(ResponseDecorator(ResourceProxy(resource=getattr(self.api, resource))), auth=self.auth)
