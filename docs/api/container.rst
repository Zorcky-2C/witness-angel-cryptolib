Container
==========

This module provides utilities to write and read encrypted containers, which themselves use
encryption/signing keys of the escrow system.


.. autofunction:: wacryptolib.container.encrypt_data_into_container

.. autofunction:: wacryptolib.container.decrypt_data_from_container

.. autoclass:: wacryptolib.container.ContainerStorage
    :members:

.. autoclass:: wacryptolib.container.TarfileAggregator
    :members:

.. autoclass:: wacryptolib.container.JsonAggregator
    :members:

