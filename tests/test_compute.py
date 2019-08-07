from aioazure.resources.compute import AzureComputeResource

from unittest import TestCase


class TestAzureComputeResource(TestCase):
    def setUp(self) -> None:
        self.compute = AzureComputeResource(api_root_url='https://test.azure.com')

    def test_actions(self) -> None:
        expected_actions = {'create_or_update': {'method': 'PUT',
                                                 'url': 'Microsoft.Compute/virtualMachines/{}'},
                            'delete': {'method': 'DELETE', 'url': 'Microsoft.Compute/virtualMachines/{}'},
                            'instance_view': {'method': 'GET',
                                              'url': 'Microsoft.Compute/virtualMachines/{}/instanceView'},
                            'power_off': {'method': 'POST',
                                          'url': 'Microsoft.Compute/virtualMachines/{}/powerOff'}}
        self.assertEqual(self.compute.actions, expected_actions)

    def test_get_action(self) -> None:
        self.assertEqual(self.compute.get_action('power_off'),
                         {'method': 'POST', 'url': 'Microsoft.Compute/virtualMachines/{}/powerOff'})

    def test_get_action_full_url(self) -> None:
        self.assertEqual(self.compute.get_action_full_url('power_off', 'test_vm_name'),
                         'https://test.azure.com/Microsoft.Compute/virtualMachines/test_vm_name/powerOff')

    def test_get_action_method(self) -> None:
        self.assertEqual(self.compute.get_action_method('power_off'), 'POST')

    def test_api_version_param(self) -> None:
        self.assertEqual(self.compute.params, {"api-version": "2018-06-01"})
