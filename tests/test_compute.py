from aioazure.resources.compute import AzureComputeResource

from unittest import TestCase


class TestAzureComputeResource(TestCase):
    def setUp(self) -> None:
        self.compute = AzureComputeResource()
