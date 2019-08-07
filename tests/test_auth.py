from aioazure.auth import Authentication

from unittest import TestCase


class TestAuthentication(TestCase):
    def setUp(self) -> None:
        self.auth = Authentication()
