from time import time


class Authentication(object):
    def __init__(self) -> None:
        self.token = None
        self.token_expires_at = 0

    @property
    def is_token_valid(self):
        return self.token_expires_at - time() > 0

    async def get_credentials(self) -> None:
        self.token = None
