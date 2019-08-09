from simple_rest_client.resource import BaseResource
from simple_rest_client.resource import AsyncResource

from abc import ABCMeta
from abc import abstractmethod
from functools import partial
from inspect import signature


class Proxy(metaclass=ABCMeta):
    @abstractmethod
    async def __call__(self, method_name: str, *args, **kwargs):
        return NotImplemented

    @abstractmethod
    def __getattr__(self, method_name: str):
        return NotImplemented


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
