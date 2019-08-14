from .auth import Authenticator
from .proxy import Proxy

from abc import ABCMeta
from abc import abstractmethod
from functools import partial
from typing import Callable

import aiohttp
import asyncio


class ProxyDecorator(Proxy, metaclass=ABCMeta):
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @abstractmethod
    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        return NotImplemented

    def __getattr__(self, method_name: str):
        return partial(self, getattr(self.proxy, method_name))


class AsyncOperationDecorator(ProxyDecorator):
    def __init__(self, proxy: Proxy):
        super().__init__(proxy)

    async def async_polling(self, url, retry_after):  # ToDo: Auth can be added by passing Authenticator as param.
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json"}
        async with aiohttp.ClientSession(headers=headers, raise_for_status=True) as session:
            async_operation_status = dict(status="Submitted")
            while async_operation_status["status"] not in ("Succeeded", "Failed", "Canceled"):
                await asyncio.sleep(retry_after)
                async with session.get(url=url) as response:
                    async_operation_status = await response.json()
            return async_operation_status

    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        response = await awaitable_method(*args, **kwargs)
        for url_key in ("Azure-AsyncOperation", "Location"):
            if url_key in response.headers.keys():
                response = response._replace(body=await self.async_polling(response.headers[url_key],
                                                                           response.headers.get("Retry-After", 10)),
                                             headers={key: response.headers[key] for key in response.headers.keys()
                                                      if key not in ("Azure-AsyncOperation",  # Remove async headers
                                                                     "Location", "Retry-After")})
        return response


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
    async def get_next_page(next_link: str):  # ToDo: auth can be added by passing Authenticator as param.
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
        if "nextLink" in response.body.keys():
            response = response._replace(body=[page async for page in self.get_pages(response.body)])
        return response


class ResponseDecorator(ProxyDecorator):
    def __init__(self, proxy: Proxy):
        super().__init__(proxy)

    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        return await awaitable_method(*args, **kwargs)
