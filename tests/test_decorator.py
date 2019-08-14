from aioazure.decorator import ProxyDecorator
from aioazure.decorator import AsyncOperationDecorator
from aioazure.decorator import AuthDecorator
from aioazure.decorator import PagingDecorator
from aioazure.decorator import ResponseDecorator

from .utilities.utilities import AsyncContextManagerMock
from .utilities.utilities import async_return
from .utilities.utilities import run_async

from collections import namedtuple
from functools import partial
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

MockedResponse = namedtuple("MockedResponse", ["body", "headers"])


class TestProxyDecorator(TestCase):
    @patch.multiple(ProxyDecorator, __abstractmethods__=set())
    def setUp(self) -> None:
        self.proxy = MagicMock()
        self.proxy_decorator = ProxyDecorator(proxy=self.proxy)

    def test_call_decorator(self):
        self.assertEqual(run_async(self.proxy_decorator, "test_method"), NotImplemented)

    def test_getattr(self):
        self.assertEqual(str(getattr(self.proxy_decorator, "test_method")), str(partial(self.proxy_decorator,
                                                                                self.proxy.test_method)))


class TestAsyncOperationDecorator(TestCase):
    def setUp(self) -> None:
        self.proxy = MagicMock()
        self.proxy_decorator = AsyncOperationDecorator(self.proxy)

    def test_call_decorator_pass_through(self):
        self.assertEqual(run_async(self.proxy_decorator, lambda: async_return(
            return_value=MockedResponse(body={"Test": "Test"},
                                        headers={"TestHeader": "TestHeader"}))),
                         MockedResponse(body={"Test": "Test"},
                                        headers={"TestHeader": "TestHeader"}))

    @patch('aiohttp.ClientSession.get', new_callable=AsyncContextManagerMock)
    def test_call_decorator_async_operation(self, mock_get):
        mock_get.return_value.aenter.json.return_value = async_return(return_value={"Test2": "Test2",
                                                                                    "status": "Succeeded"})
        self.assertEqual(run_async(self.proxy_decorator, lambda: async_return(
            return_value=MockedResponse(body={"Test": "Test"},
                                        headers={"Azure-AsyncOperation": "https://test.com",
                                                 "Retry-After": 0,
                                                 "TestHeader": "TestHeader"}))),
                         MockedResponse(body={"Test2": "Test2", "status": "Succeeded"},
                                        headers={"TestHeader": "TestHeader"}))
        mock_get.assert_called_with(url='https://test.com')

        self.assertEqual(run_async(self.proxy_decorator, lambda: async_return(
            return_value=MockedResponse(body={"Test": "Test"},
                                        headers={"Location": "https://test.com",
                                                 "Retry-After": 0,
                                                 "TestHeader": "TestHeader"}))),
                         MockedResponse(body={"Test2": "Test2", "status": "Succeeded"},
                                        headers={"TestHeader": "TestHeader"}))


class TestAuthDecorator(TestCase):
    mock_auth_patcher = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_auth_patcher = patch('aioazure.decorator.Authenticator')
        cls.mock_auth = cls.mock_auth_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mock_auth_patcher.stop()

    def setUp(self) -> None:
        self.proxy = MagicMock()
        self.auth = self.mock_auth.return_value
        self.auth.get_token.return_value = async_return(return_value="T0ken123")

        self.proxy_decorator = AuthDecorator(self.proxy, auth=self.auth)

    def test_call_decorator(self):
        self.assertEqual(run_async(self.proxy_decorator,
                                   lambda **kwargs: async_return(return_value="Test", **kwargs)), "Test")


class TestPagingDecorator(TestCase):
    def setUp(self) -> None:
        self.proxy = MagicMock()
        self.proxy_decorator = PagingDecorator(self.proxy)

    def test_call_decorator_pass_through(self):
        self.assertEqual(run_async(self.proxy_decorator, lambda: async_return(
            return_value=MockedResponse(body={"Test": "Test"}, headers={"TestHeader": "TestHeader"}))),
                         MockedResponse(body={"Test": "Test"}, headers={"TestHeader": "TestHeader"}))

    @patch('aiohttp.ClientSession.get', new_callable=AsyncContextManagerMock)
    def test_call_decorator_next_link(self, mock_get):
        mock_get.return_value.aenter.json.return_value = async_return(return_value={"Test2": "Test2"})
        self.assertEqual(run_async(self.proxy_decorator,
                                   lambda: async_return(
                                       return_value=MockedResponse(body={"nextLink": "https://test.com",
                                                                         "value": [{"Test": "Test"}]},
                                                                   headers={"TestHeader": "TestHeader"}))),
                         MockedResponse(body=[{"Test": "Test"}, {"Test2": "Test2"}],
                                        headers={"TestHeader": "TestHeader"}))
        mock_get.assert_called_with(url='https://test.com')


class TestResponseDecorator(TestCase):
    def setUp(self) -> None:
        self.proxy = MagicMock()
        self.proxy_decorator = ResponseDecorator(self.proxy)

    def test_call_decorator(self):
        self.assertEqual(run_async(self.proxy_decorator, lambda: async_return(return_value="Test")), "Test")
