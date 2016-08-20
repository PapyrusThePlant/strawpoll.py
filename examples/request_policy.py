import asyncio
import strawpoll


async def main():
    async_api = strawpoll.API()  # Default policy is asynchronous
    p1 = await async_api.get_poll(10915632)
    p2 = async_api.get_poll(10915632, request_policy=strawpoll.RequestsPolicy.synchronous)  # Override for one request
    assert(p1 == p2)

    sync_api = strawpoll.API(requests_policy=strawpoll.RequestsPolicy.synchronous)  # Override default policy
    p3 = sync_api.get_poll(10915632)
    p4 = await sync_api.get_poll(10915632, request_policy=strawpoll.RequestsPolicy.asynchronous)  # Override for one request
    assert(p3 == p4)

    assert(p1 == p3)


asyncio.get_event_loop().run_until_complete(main())
