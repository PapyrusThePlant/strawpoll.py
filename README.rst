============
strawpoll.py
============

..
    Note that the badges will lose the target url if kept in the .svg format,
    except readthedocs' one, because reasons.

.. image:: https://img.shields.io/pypi/pyversions/strawpoll.py.png
    :target: pypi_

.. image:: https://img.shields.io/pypi/v/strawpoll.py.png
    :target: pypi_

.. image:: https://img.shields.io/badge/license-MIT-blue.png
    :target: license_

.. image:: https://readthedocs.org/projects/strawpollpy/badge/
    :target: documentation_

strawpoll.py is an async wrapper for `strawpoll's API`_ written in Python.

For more info, take a look at the documentation_.

.. _documentation: http://strawpollpy.readthedocs.io/
.. _license: https://raw.githubusercontent.com/PapyrusThePlant/strawpoll.py/master/LICENSE
.. _pypi: https://pypi.python.org/pypi/strawpoll.py/
.. _strawpoll's API:  https://strawpoll.zendesk.com/hc/en-us/articles/218979828-Straw-Poll-API-Information

Installation
============

::

    $ pip install strawpoll.py

Usage
=====

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

