from .auth import Authenticator
from .proxy import Proxy

from abc import ABCMeta
from abc import abstractmethod
import aiohttp
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


class PagingDecorator(ProxyDecorator):
    def __init__(self, proxy: Proxy):
        super().__init__(proxy)

    @staticmethod
    async def get_next_page(next_link):  # ToDo: if auth is necessary, can be added by passing Authenticator as param.
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json"}
        async with aiohttp.ClientSession(headers=headers, raise_for_status=True) as session:
            async with session.get(url=next_link) as response:
                return await response.json()

    async def get_pages(self, response):
        while "nextLink" in response.keys():
            for entry in response['value']:
                yield entry
            response = await self.get_next_page(next_link=response["nextLink"])
        yield response

    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        response = await awaitable_method(*args, **kwargs)
        if "nextLink" in response.keys():
            return [page async for page in self.get_pages(response)]
        else:
            return response


class ResponseDecorator(ProxyDecorator):
    def __init__(self, proxy: Proxy):
        super().__init__(proxy)

    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        return await awaitable_method(*args, **kwargs)
