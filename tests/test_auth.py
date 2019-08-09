from aioazure.auth import Authenticator

from .utilities.utilities import AsyncContextManagerMock
from .utilities.utilities import async_return
from .utilities.utilities import run_async

from math import inf
from unittest import TestCase
from unittest.mock import patch


class TestAuthenticator(TestCase):
    def setUp(self) -> None:
        self.auth = Authenticator(app_id="TestAppId123", password="p455w0rd", tenant_id="TestTenantId123")

    @patch('aiohttp.ClientSession.post', new_callable=AsyncContextManagerMock)
    def test_get_token(self, mock_post):
        mock_post.return_value.aenter.json.return_value = async_return(return_value={})
        run_async(self.auth.get_token)
        mock_post.assert_called_with(data={'grant_type': 'client_credentials',
                                           'client_id': 'TestAppId123',
                                           'client_secret': 'p455w0rd',
                                           'resource': 'https://management.azure.com/'},
                                     url='https://login.microsoftonline.com/TestTenantId123/oauth2/token')

    @patch('aiohttp.ClientSession.post', new_callable=AsyncContextManagerMock)
    def test_is_token_valid(self, mock_post):
        mock_post.return_value.aenter.json.return_value = async_return(return_value={"access_token": "T0ken123",
                                                                                     "expires_on": inf})
        self.assertFalse(self.auth.is_token_valid)
        run_async(self.auth.get_token)
        self.assertTrue(self.auth.is_token_valid)
        run_async(self.auth.get_token)
        self.assertEqual(mock_post.call_count, 1)
