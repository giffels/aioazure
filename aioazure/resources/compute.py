from simple_rest_client.resource import AsyncResource

import yaml


class AzureComputeResource(AsyncResource):
    api_version = None
    with open('models/compute.yaml', 'r') as f:
        for key, value in yaml.safe_load(f).items():
            vars()[key] = value

    def __init__(self, api_root_url=None, resource_name=None, params=None, headers=None, timeout=None,
                 append_slash=False, json_encode_body=False, ssl_verify=None,):
        params = params or {}
        params.update({'api-version': self.api_version})
        super().__init__(api_root_url, resource_name, params, headers,
                         timeout, append_slash, json_encode_body, ssl_verify)
