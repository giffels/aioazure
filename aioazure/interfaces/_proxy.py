from abc import ABCMeta
from abc import abstractmethod


class Proxy(metaclass=ABCMeta):
    @abstractmethod
    async def __call__(self, method_name: str, *args, **kwargs):
        return NotImplemented

    @abstractmethod
    def __getattr__(self, method_name: str):
        return NotImplemented
