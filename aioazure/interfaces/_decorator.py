from ._proxy import Proxy

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
