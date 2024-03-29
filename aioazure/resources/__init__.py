from simple_rest_client.resource import AsyncResource

import os
import yaml

azure_resources = {}


class AzureResource(AsyncResource):
    def __init__(self, api_root_url=None, resource_name=None, params=None, headers=None, timeout=None,
                 append_slash=False, json_encode_body=False, ssl_verify=None,):
        params = params or {}
        params.update({'api-version': self.api_version})
        super().__init__(api_root_url, resource_name, params, headers,
                         timeout, append_slash, json_encode_body, ssl_verify)


for dirpath, _, filenames in os.walk(os.path.join(os.path.dirname(__file__), 'models')):
    for filename in filenames:
        service_name = os.path.splitext(filename)[0]
        with open(os.path.join(dirpath, filename), 'r') as f:
            for resource_group, resources in yaml.safe_load(f).items():
                resource_class = type(f"Azure{service_name.capitalize()}{resource_group.capitalize()}Resource",
                                      (AzureResource,),
                                      {key: value for key, value in resources.items()})
                # noinspection PyArgumentList
                resource_class.__init__ = lambda self, *args, **kwargs: super(resource_class, self).__init__(*args,
                                                                                                             **kwargs)
                azure_resources.setdefault(service_name, []).append(
                    dict(resource_name=resource_group, resource_class=resource_class))

__all__ = ['azure_resources']
