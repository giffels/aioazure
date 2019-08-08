from aioazure.client import AzureClient
from aioazure.resources.compute import AzureComputeResource

from unittest import TestCase
from unittest.mock import patch


class TestAzureClient(TestCase):
    mock_auth_patcher = None
    mock_api_patcher = None
    mock_resource_proxy_patcher = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_auth_patcher = patch('aioazure.client.Authentication')
        cls.mock_auth = cls.mock_auth_patcher.start()

        cls.mock_api_patcher = patch('aioazure.client.API')
        cls.mock_api = cls.mock_api_patcher.start()

        cls.mock_resource_proxy_patcher = patch('aioazure.client.ResourceProxy')
        cls.mock_resource_proxy = cls.mock_resource_proxy_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mock_auth_patcher.stop()
        cls.mock_api_patcher.stop()
        cls.mock_resource_proxy_patcher.stop()

    def setUp(self) -> None:
        self.api_url = "https://test.azure.com"
        self.subscription_id = "Subscription123"
        self.resource_group_name = "ResourceGroup123"
        self.auth = self.mock_auth.return_value

        self.mock_api.return_value.compute = "Compute123"

        self.client = AzureClient(api_url=self.api_url, subscription_id=self.subscription_id,
                                  resource_group_name=self.resource_group_name, auth=self.auth)

    def test_create_client(self):
        api_root_url = 'https://test.azure.com/subscriptions/Subscription123/resourceGroups/ResourceGroup123/providers'
        self.mock_api.assert_called_with(
            api_root_url=api_root_url,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            json_encode_body=True, timeout=60)
        self.mock_api.return_value.add_resource.assert_called_with(resource_class=AzureComputeResource,
                                                                   resource_name='compute')

    def test_get_attr(self):
        _ = self.client.compute
        self.mock_resource_proxy.assert_called_with(auth=self.auth, resource="Compute123")
