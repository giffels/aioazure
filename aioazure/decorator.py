from .auth import Authenticator
from .proxy import Proxy

from abc import ABCMeta
from abc import abstractmethod
from functools import partial
from typing import Callable


class ProxyDecorator(Proxy, metaclass=ABCMeta):
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @abstractmethod
    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        return NotImplemented

    def __getattr__(self, method_name: str):
        return partial(self, getattr(self.proxy, method_name))


class AuthDecorator(ProxyDecorator):
    def __init__(self, proxy: Proxy, auth: Authenticator):
        super().__init__(proxy)
        self.auth = auth

    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        kwargs.setdefault("headers", {}).update({"Authorization": await self.auth.get_token()})
        return await awaitable_method(*args, **kwargs)


class ResponseDecorator(ProxyDecorator):
    def __init__(self, proxy: Proxy):
        super().__init__(proxy)

    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        return await awaitable_method(*args, **kwargs)
