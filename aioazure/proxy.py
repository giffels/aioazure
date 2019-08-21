from .auth import Authenticator
from .decorator import AuthDecorator
from .decorator import ResponseDecorator
from .interfaces import Proxy

from simple_rest_client.api import API
from simple_rest_client.resource import BaseResource
from simple_rest_client.resource import AsyncResource

from functools import partial
from inspect import signature


class ApiProxy(Proxy):
    def __init__(self, api: API, auth: Authenticator):
        self.api = api
        self.auth = auth

    def add_resource(self, api_root_url=None, resource_name=None, resource_class=None, params=None,
                     headers=None, timeout=None, append_slash=False, json_encode_body=False):
        return self.api.add_resource(api_root_url=api_root_url, resource_name=resource_name,
                                     resource_class=resource_class, params=params, headers=headers,
                                     timeout=timeout, append_slash=append_slash, json_encode_body=json_encode_body)

    def __call__(self, method_name: str, *args, **kwargs):
        raise TypeError(f"{self.__class__.__name__} object is not callable!")

    def __getattr__(self, item):
        return AuthDecorator(ResponseDecorator(ResourceProxy(resource=getattr(self.api, item))), auth=self.auth)


class ResourceProxy(Proxy):
    pass_through_parameters = [parameter for parameter in signature(BaseResource.__init__).parameters
                               if not parameter == "self"]

    def __init__(self, resource: AsyncResource) -> None:
        self.resource = resource

    async def __call__(self, method_name: str, *args, **kwargs):
        awaitable_method = getattr(self.resource, method_name)

        pass_through_kwargs = {key: value for key, value in kwargs.items() if key in self.pass_through_parameters}
        remaining_kwargs = {key: value for key, value in kwargs.items() if key not in self.pass_through_parameters}

        if self.resource.actions[method_name]['method'] in ('GET',):
            return await awaitable_method(*args, **pass_through_kwargs, params=remaining_kwargs)
        else:
            return await awaitable_method(*args, **pass_through_kwargs, body=remaining_kwargs)

    def __getattr__(self, method_name: str):
        return partial(self, method_name)
