from simple_rest_client.resource import AsyncResource
from pkgutil import iter_modules
from importlib import import_module
import os

resource_classes = []
resource_names = []

for (_, name, _) in iter_modules([os.path.dirname(__file__)]):
    module = import_module(f".{name}", __package__)
    for str_item in dir(module):
        item = getattr(module, str_item)
        if item in AsyncResource.__subclasses__():
            resource_classes.append(item)
            resource_names.append(name)

__all__ = ['resource_classes', 'resource_names']
