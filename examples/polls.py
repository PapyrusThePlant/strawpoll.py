import asyncio
import strawpoll


async def main(loop):
    api = strawpoll.API(loop=loop)

    # Retrieving a poll
    p1 = await api.get_poll(10915632)
    # Those will yield the same result:
    # p1 = await api.get_poll('http://www.strawpoll.me/10915632')
    # p1 = await api.get_poll('http://www.strawpoll.me/10915632/r')
    # p1 = await api.get_poll('10915632')

    # Displaying its info
    print(p1.id)                # 10915632
    print(p1.url)               # http://www.strawpoll.me/10915632
    print(p1.results())         # [('fuck yes', 1), ('yes', 0)]
    print(p1.options)           # ['yes', 'fuck yes']
    print(p1.votes)             # [0, 1]
    print(p1.total_votes)       # 1
    print(p1.results(limit=1))  # [('fuck yes', 1)]
    print(p1.result_at(0))      # ('yes', 0)
    print(p1.result_at(1))      # ('fuck yes', 1)
    print(p1.multi)             # False
    print(p1.dupcheck)          # normal
    print(p1.captcha)           # False

    # Creating a new poll
    p2 = strawpoll.Poll('lol?', ['ha', 'haha', 'hahaha', 'hahahaha', 'hahahahaha'])
    print(p2.id)                # None
    print(p2.url)               #

    # Submitting it on strawpoll
    await api.submit_poll(p2)
    print(p2.id)                # 10921552
    print(p2.url)               # http://www.strawpoll.me/10921552


l = asyncio.get_event_loop()
l.run_until_complete(main(l))
