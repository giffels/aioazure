from aioazure.resources import azure_resources

from unittest import TestCase


class TestAzureComputeVirtualmachinesResource(TestCase):
    def setUp(self) -> None:
        for service_name, resources in azure_resources.items():
            for resource in resources:
                resource_class = resource["resource_class"]
                if resource_class.__name__ == "AzureComputeVirtualmachinesResource":
                    self.virtualmachines = resource_class(api_root_url='https://test.azure.com')
                    break

    def test_actions(self) -> None:
        expected_actions = {'create_or_update': {'method': 'PUT',
                                                 'url': 'Microsoft.Compute/virtualMachines/{}'},
                            'delete': {'method': 'DELETE', 'url': 'Microsoft.Compute/virtualMachines/{}'},
                            'instance_view': {'method': 'GET',
                                              'url': 'Microsoft.Compute/virtualMachines/{}/instanceView'},
                            'power_off': {'method': 'POST',
                                          'url': 'Microsoft.Compute/virtualMachines/{}/powerOff'}}
        self.assertEqual(self.virtualmachines.actions, expected_actions)

    def test_get_action(self) -> None:
        self.assertEqual(self.virtualmachines.get_action('power_off'),
                         {'method': 'POST', 'url': 'Microsoft.Compute/virtualMachines/{}/powerOff'})

    def test_get_action_full_url(self) -> None:
        self.assertEqual(self.virtualmachines.get_action_full_url('power_off', 'test_vm_name'),
                         'https://test.azure.com/Microsoft.Compute/virtualMachines/test_vm_name/powerOff')

    def test_get_action_method(self) -> None:
        self.assertEqual(self.virtualmachines.get_action_method('power_off'), 'POST')

    def test_api_version_param(self) -> None:
        self.assertEqual(self.virtualmachines.params, {"api-version": "2018-06-01"})
