============
strawpoll.py
============

|docbadge|_

strawpoll.py is an async wrapper for `strawpoll's API`_ written in Python.

For more info, take a look at the documentation_.

.. |docbadge| image:: https://readthedocs.org/projects/strawpollpy/badge/
.. _docbadge: documentation_

.. _strawpoll's API:  https://strawpoll.zendesk.com/hc/en-us/articles/218979828-Straw-Poll-API-Information
.. _documentation: http://strawpollpy.readthedocs.io/

Requirements
============

* Python 3.4.2+
* ``aiohttp`` library

Example
=======

::

    import asyncio
    import strawpoll

    async def main():
        api = strawpoll.API()

        p1 = await api.get_poll(10915632)
        print(p1.results())

        p2 = strawpoll.Poll('lol?', ['ha', 'haha', 'hahaha', 'hahahaha', 'hahahahaha'])
        await api.submit_poll(p2)
        print(p2.url)

    asyncio.get_event_loop().run_until_complete(main())

