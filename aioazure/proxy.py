from .auth import Authentication

from simple_rest_client.resource import AsyncResource

from abc import ABCMeta
from abc import abstractmethod
from functools import partial


class Proxy(metaclass=ABCMeta):
    @abstractmethod
    async def __call__(self, method_name: str, *args, **kwargs):
        return NotImplemented

    @abstractmethod
    def __getattr__(self, method_name: str):
        return NotImplemented


class ResourceProxy(Proxy):
    def __init__(self, auth: Authentication, resource: AsyncResource) -> None:
        self.auth = auth
        self.resource = resource

    async def __call__(self, method_name: str, *args, **kwargs):
        token = await self.auth.get_token()
        headers = {"Authorization": token}
        awaitable_method = getattr(self.resource, method_name)
        if self.resource.actions[method_name]['method'] in ('GET',):
            return await awaitable_method(*args, headers=headers, params=kwargs)
        else:
            return await awaitable_method(*args, headers=headers, body=kwargs)

    def __getattr__(self, method_name: str):
        return partial(self, method_name)
