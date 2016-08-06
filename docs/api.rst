.. module:: strawpoll

API reference
=============

A basic wrapper for the Strawpoll API.

Version info
------------

.. _vinfo:
.. py:data:: version_info

    A named tuple containing the five components of the version number in a
    similar manner as sys.version_info_.

    .. _sys.version_info: https://docs.python.org/3/library/sys.html#sys.version_info

.. py:data:: __version__

    A string representation of :data:`version_info`.

API
---

.. autoclass:: API
    :members:

Poll
----

.. autoclass:: Poll
    :members:

Exceptions
----------

.. autoexception:: StrawpollException
.. autoexception:: ExistingPoll
.. autoexception:: HTTPException
    :members:


.. |coroutine| replace:: This function is a |corolink|_.
.. |corolink| replace:: **coroutine**
.. _corolink: :ref:`coroutineAnchor_`
