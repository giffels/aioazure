from .auth import Authenticator
from .resources import azure_resources
from .proxy import ApiProxy

from simple_rest_client.api import API


class AzureClient(object):
    def __init__(self, api_url: str, subscription_id: str, resource_group_name: str,
                 auth: Authenticator, timeout: int = 60) -> None:
        self.api_url = f"{api_url}/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers"

        for service_name, resources in azure_resources.items():
            api_proxy = ApiProxy(api=API(api_root_url=self.api_url,
                                         json_encode_body=True,
                                         headers={"Accept": "application/json",
                                                  "Content-Type": "application/json"},
                                         timeout=timeout),
                                 auth=auth)
            for resource in resources:
                api_proxy.add_resource(resource_name=resource["resource_name"],
                                       resource_class=resource["resource_class"])

            setattr(self, service_name, api_proxy)
