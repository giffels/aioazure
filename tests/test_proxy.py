from aioazure.proxy import ResourceProxy
from aioazure.proxy import Proxy

from .utilities.utilities import async_return
from .utilities.utilities import run_async

from unittest import TestCase
from unittest.mock import patch


class TestProxy(TestCase):
    @patch.multiple(Proxy, __abstractmethods__=set())
    def setUp(self) -> None:
        self.proxy = Proxy()

    def test_call_proxy(self):
        self.assertEqual(run_async(self.proxy, "test_method"), NotImplemented)

    def test_getattr(self):
        self.assertEqual(getattr(self.proxy, "test_method"), NotImplemented)


class TestResourceProxy(TestCase):
    mock_async_resource_patcher = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_async_resource_patcher = patch("aioazure.proxy.AsyncResource")
        cls.mock_async_resource = cls.mock_async_resource_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mock_async_resource_patcher.stop()

    def setUp(self) -> None:
        self.resource = self.mock_async_resource.return_value
        self.resource.test_method.return_value = async_return(return_value="Test123")
        self.resource.actions = {"test_method": {"method": "POST"}}
        self.proxy = ResourceProxy(resource=self.resource)

    def test_call_proxy(self):
        def run_test(**kwargs):
            self.assertEqual(run_async(self.proxy, "test_method", test="TestBody", **kwargs), "Test123")

        def check_results(**kwargs):
            self.resource.test_method.assert_called_with(**kwargs)
            self.mock_async_resource.reset_mock()

        run_test()
        check_results(body={'test': 'TestBody'})

        self.resource.actions = {"test_method": {"method": "GET"}}
        run_test()
        check_results(params={'test': 'TestBody'})

        run_test(headers={"TestHeader": "Test123"})
        check_results(params={'test': 'TestBody'}, headers={"TestHeader": "Test123"})

    def test_getattr(self):
        self.assertEqual(run_async(self.proxy.test_method, test="TestBody"), "Test123")
        self.resource.test_method.assert_called_with(body={'test': 'TestBody'})
