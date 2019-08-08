from aioazure.decorator import ProxyDecorator
from aioazure.decorator import AuthDecorator
from aioazure.decorator import ResponseDecorator

from .utilities.utilities import async_return
from .utilities.utilities import run_async

from functools import partial
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


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


class TestAuthDecorator(TestCase):
    mock_auth_patcher = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_auth_patcher = patch('aioazure.decorator.Authentication')
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
        self.assertEqual(run_async(self.proxy_decorator, lambda: async_return(return_value="Test")), "Test")


class TestResponseDecorator(TestCase):
    def setUp(self) -> None:
        self.proxy = MagicMock()
        self.proxy_decorator = ResponseDecorator(self.proxy)

    def test_call_decorator(self):
        self.assertEqual(run_async(self.proxy_decorator, lambda: async_return(return_value="Test")), "Test")