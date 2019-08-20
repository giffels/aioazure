[![Build Status](https://travis-ci.org/giffels/aioazure.svg?branch=master)](https://travis-ci.org/giffels/aioazure)
[![codecov](https://codecov.io/gh/giffels/aioazure/branch/master/graph/badge.svg)](https://codecov.io/gh/giffels/aioazure)
[![Documentation Status](https://readthedocs.org/projects/aioazure/badge/?version=latest)](https://aioazure.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/giffels/aioazure/blob/master/LICENSE.txt)

# aioazure
aioazure is a simplistic python REST client for the Microsoft Azure REST API utilizing asyncio.
The client itself has been developed against the 
[Microsoft Azure REST API documentation](https://docs.microsoft.com/en-us/rest/api/azure/). 

## Installation
The goal is to distribute this package via [PyPi](https://pypi.org/), so a simple 

`pip install aioazure`

would be needed to install the package. The release will happen once the client has been tested with Azure.

## How to use aioazure

```python
from aioazure.auth import Authenticator
from aioazure.client import AzureClient

auth = Authenticator(app_id="your_app_id", 
                     password="your_secret", 
                     tenant_id="your_tenant_id")

client = AzureClient(api_url="url_of_the_azure_api", 
                     subscription_id="your_subscription_id", 
                     resource_group_name="your_resource_group_name",
                     auth=auth, 
                     timeout=60)  # <- this is optional

client.compute.create_or_update("my-vm-name", 
                                location="Antarctica")

client.compute.instance_view("my-vm-name")

client.compute.power_off("my-vm-name")

client.compute.delete("my-vm-name")
```

## Currently supported Azure API calls
* [Azure Compute](https://docs.microsoft.com/en-us/rest/api/compute/)
  * [Virtual Machines](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines)
    * [create_or_update](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/createorupdate)
    * [instance_view](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/instanceview)
    * [power_off](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/poweroff)
    * [delete](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/delete)
    