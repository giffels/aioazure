from aioazure.proxy import ResourceProxy

from .utilities.utilities import async_return
from .utilities.utilities import run_async

from unittest import TestCase
from unittest.mock import patch


class TestResourceProxy(TestCase):
    mock_auth_patcher = None
    mock_async_resource_patcher = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_auth_patcher = patch("aioazure.proxy.Authentication")
        cls.mock_auth = cls.mock_auth_patcher.start()

        cls.mock_async_resource_patcher = patch("aioazure.proxy.AsyncResource")
        cls.mock_async_resource = cls.mock_async_resource_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mock_auth_patcher.stop()
        cls.mock_async_resource_patcher.stop()

    def setUp(self) -> None:
        self.auth = self.mock_auth.return_value
        self.auth.get_token.return_value = async_return(return_value="T0ken123")
        self.resource = self.mock_async_resource.return_value
        self.resource.test_method.return_value = async_return(return_value="Test123")
        self.proxy = ResourceProxy(auth=self.auth, resource=self.resource)

    def test_call_proxy(self):
        self.assertEqual(run_async(self.proxy, "test_method", test="TestBody"), "Test123")
        self.resource.test_method.assert_called_with(body={'test': 'TestBody'}, header={'Authorization': 'T0ken123'})
        self.auth.get_token.assert_called_with()

    def test_getattr(self):
        self.assertEqual(run_async(self.proxy.test_method, test="TestBody"), "Test123")
        self.resource.test_method.assert_called_with(body={'test': 'TestBody'}, header={'Authorization': 'T0ken123'})
        self.auth.get_token.assert_called_with()