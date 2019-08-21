from aioazure.proxy import ApiProxy
from aioazure.proxy import ResourceProxy
from aioazure.interfaces import Proxy

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


class TestApiProxy(TestCase):
    mock_auth_patcher = None
    mock_api_patcher = None
    mock_resource_proxy_patcher = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_auth_patcher = patch('aioazure.proxy.Authenticator')
        cls.mock_auth = cls.mock_auth_patcher.start()

        cls.mock_api_patcher = patch('aioazure.proxy.API')
        cls.mock_api = cls.mock_api_patcher.start()

        cls.mock_resource_proxy_patcher = patch('aioazure.proxy.ResourceProxy')
        cls.mock_resource_proxy = cls.mock_resource_proxy_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mock_auth_patcher.stop()
        cls.mock_api_patcher.stop()
        cls.mock_resource_proxy_patcher.stop()

    def setUp(self) -> None:
        self.mock_api.virtualmachines = "Compute123"

        self.proxy = ApiProxy(api=self.mock_api, auth=self.mock_auth)

    def test_add_resources(self):
        resource_class = type("AzureComputeResource", (object,), {})
        resource_name = "compute"

        self.proxy.add_resource(resource_name=resource_name, resource_class=resource_class)

        self.mock_api.add_resource.assert_called_with(api_root_url=None, append_slash=False, headers=None,
                                                      json_encode_body=False, params=None,
                                                      resource_class=resource_class, resource_name=resource_name,
                                                      timeout=None)

    def test_call_proxy(self):
        with self.assertRaises(TypeError):
            self.proxy(method_name="test")

    def test_get_attr(self):
        _ = self.proxy.virtualmachines
        self.mock_resource_proxy.assert_called_with(resource="Compute123")


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
