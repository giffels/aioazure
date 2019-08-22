.. aioazure documentation master file, created by
   sphinx-quickstart on Mon Aug  5 10:26:52 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to aioazure's documentation!
====================================

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   Module Index <api/modules>

aioazure
========
aioazure is a simplistic python REST client for the Microsoft Azure REST API utilizing asyncio.
The client itself has been developed against the
`Microsoft Azure REST API documentation <https://docs.microsoft.com/en-us/rest/api/azure/>`_.

Installation
------------
The goal is to distribute this package via `PyPi <https://pypi.org/>`_, so a simple

.. code-block:: bash

   pip install aioazure

would be needed to install the package. The release will happen once the client has been tested with Azure.

How to use aioazure
-------------------

.. code-block:: python

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

   await client.compute.virtualmachines.create_or_update("my-vm-name",
                                                         location="Antarctica")

   await client.compute.virtualmachines.instance_view("my-vm-name")

   await client.compute.virtualmachines.power_off("my-vm-name")

   await client.compute.virtualmachines.delete("my-vm-name")


Currently supported Azure services, operation groups and operations
-------------------------------------------------------------------

* `Azure Compute <https://docs.microsoft.com/en-us/rest/api/compute/>`_
   * `Virtual Machines <https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines>`_
      * `create_or_update <https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/createorupdate>`_
      * `instance_view <https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/instanceview>`_
      * `power_off <https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/poweroff>`_
      * `delete <https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/delete>`_

Adding further Azure services, operation groups and operations
--------------------------------------------------------------

Each Azure service (compute, storage services, etc.) is represented by a ``yaml`` file in the
`models <https://github.com/giffels/aioazure/tree/master/aioazure/resources/models>`_ directory.
This ``yaml`` file contains mapping nodes for each operation group (virtualmachines, manageddisks, etc.).
Each operation group consists of two mapping nodes, the version of api to use (``api_version``) and the
supported operations (``actions``) in this operation group.

.. code-block:: yaml

      rest_operation_group:
        api_version: "2018-06-01"
        actions:
          action_1:
            method: GET
            url: Microsoft.Compute/rest_operations_group/{}
          ...
          action_n:
            method: POST
            url: Microsoft.Compute/rest_operations_group/{}
      rest_operation_group_2:
        ...

The Azure service, operation groups and operation can than be called in Python as described below.

.. code-block:: python

    await client.<service_name>.<rest_operation_group>.<action>(args, kwargs)

In case you add additional services, operation groups and operations, please submit a pull request
so that others can profit as well from the work you have done. Thank you!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
