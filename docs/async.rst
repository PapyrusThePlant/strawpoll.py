.. _coroutineAnchor:

A note on coroutines
====================

A coroutine is a function that is either decorated with ``@asyncio.coroutine`` for
python 3.4 or defined with ``async def`` in python 3.5+.

Coroutines are not like regular functions, if you invoke it as usual, it will
not be executed. The proper way to call a coroutine is to use ``yield from`` in
python 3.4 or ``await`` in python 3.5+, like so: ::

    # With python 3.4
    @asyncio.coroutine
    def my_coro():
        yield from another_coro()

    # With python 3.5+
    async def my_coro():
        await another_coro()


As you can see async programming has slight syntax nuances between python 3.4
and python 3.5+. **It is highly recommended to use python 3.5+.**
