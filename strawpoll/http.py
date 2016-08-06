"""
:copyright: 2016 Papyrus
:license: MIT, see LICENSE for more details.
"""

import aiohttp
import asyncio
import json
import logging
from sys import version_info

from . import __title__, __version__, __url__
from .errors import HTTPException

log = logging.getLogger(__name__)


class HTTPClient:
    """Simplistic HTTP client to send requests to an url."""
    def __init__(self, loop=None):
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        fmt = '{0}/{1} ({2}) Python/{3.major}.{3.minor}.{3.micro} aiohttp/{4}'
        self.user_agent = fmt.format(__title__, __version__, __url__, version_info, aiohttp.__version__)
        self.session = aiohttp.ClientSession(loop=loop, headers={'User-Agent': self.user_agent})

    def __del__(self):
        self.session.close()

    @asyncio.coroutine
    def request(self, method, url, **kwargs):
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'], separators=(',', ':'))

        resp = yield from self.session.request(method, url, **kwargs)
        try:
            # Strawpoll's API is supposed to always return json data, but whatever
            if 'application/json' in resp.headers['content-type']:
                rdata = yield from resp.json()
            else:
                rdata = yield from resp.text()

            data = kwargs['data'] if 'data' in kwargs else 'no data'
            log.debug('{} on {} with {} returned {}: {}'.format(method, url, resp.status, data, rdata))
            if resp.status != 200:
                raise HTTPException(resp, rdata)
            else:
                return rdata
        finally:
            resp.release()

    def delete(self, *args, **kwargs):
        return self.request('DELETE', *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)

    def head(self, *args, **kwargs):
        return self.request('HEAD', *args, **kwargs)

    def options(self, *args, **kwargs):
        return self.request('OPTIONS', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request('PATCH', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request('PUT', *args, **kwargs)
