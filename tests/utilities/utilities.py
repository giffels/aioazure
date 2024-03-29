import asyncio
from unittest.mock import MagicMock


class AsyncContextManagerMock(MagicMock):
    async def __aenter__(self):
        return self.aenter

    async def __aexit__(self, *args):
        pass


def async_return(*args, return_value=None, **kwargs):
    f = asyncio.Future()
    f.set_result(return_value)
    return f


def run_async(coroutine, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine(*args, **kwargs))
