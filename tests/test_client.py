from aioazure.client import AzureClient
from aioazure.resources.compute import AzureComputeResource

from .utilities.utilities import async_return
from .utilities.utilities import run_async

from unittest import TestCase
from unittest.mock import patch


class TestAzureClient(TestCase):
    mock_auth_patcher = None
    mock_api_patcher = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_auth_patcher = patch('aioazure.client.Authentication')
        cls.mock_auth = cls.mock_auth_patcher.start()

        cls.mock_api_patcher = patch('aioazure.client.API')
        cls.mock_api = cls.mock_api_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mock_auth_patcher.stop()
        cls.mock_api_patcher.stop()

    def setUp(self) -> None:
        api_url = "https://test.azure.com"
        subscription_id = "Subscription123"
        resource_group_name = "ResourceGroup123"
        self.auth = self.mock_auth.return_value
        self.auth.get_credentials.return_value = async_return()
        self.auth.token = "T0ken123"
        self.auth.is_token_valid = True

        self.mock_api.return_value.compute = "Compute123"

        self.client = AzureClient(api_url=api_url, subscription_id=subscription_id,
                                  resource_group_name=resource_group_name, auth=self.auth)

    def test_init_api(self):
        run_async(self.client.init_api)
        api_root_url = 'https://test.azure.com/subscriptions/Subscription123/resourceGroups/ResourceGroup123/providers'
        self.mock_api.assert_called_with(
            api_root_url=api_root_url,
            headers={'Accept': 'application/json', 'Authorization': self.auth.token,
                     'Content-Type': 'application/json'},
            json_encode_body=True, timeout=60)
        self.mock_api.return_value.add_resource.assert_called_with(resource_class=AzureComputeResource,
                                                                   resource_name='compute')
        self.mock_api.reset_mock()

        # test repeated call with initialized api and valid token does not re-initialize API
        run_async(self.client.init_api)
        self.assertFalse(self.mock_api.called)
        self.assertFalse(self.mock_api.return_value.add_resource.called)

        self.mock_api.reset_mock()

        # test repeated call with initialized api and non valid token does re-initialize API
        self.auth.is_token_valid = False
        run_async(self.client.init_api)
        self.assertTrue(self.mock_api.called)
        self.assertTrue(self.mock_api.return_value.add_resource.called)

    def test_get_attr(self):
        run_async(self.client.init_api)
        self.assertEqual(self.client.compute, "Compute123")
