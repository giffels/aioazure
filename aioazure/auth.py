import aiohttp
from time import time


class Authenticator(object):
    def __init__(self, app_id: str, password: str, tenant_id: str) -> None:
        self.data = {"grant_type": "client_credentials",
                     "client_id": f"{app_id}",
                     "client_secret": f"{password}",
                     "resource": "https://management.azure.com/"}
        self.token = None
        self.token_expires_on = 0
        self._url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"

    async def get_token(self) -> str:  # Should be replace by async properties once available
        if self.token and self.is_token_valid:
            return self.token
        else:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self._url, data=self.data) as response:
                    authentication_data = await response.json()
                    self.token = authentication_data.get("access_token")
                    self.token_expires_on = authentication_data.get("expires_on", 0)

    @property
    def is_token_valid(self) -> float:
        return self.token_expires_on - time() > 0
