"""
:copyright: 2016 PapyrusThePlant
:license: MIT, see LICENSE for more details.
"""

import aiohttp
import asyncio
import json
import logging
import requests
from enum import Enum
from sys import version_info

from . import __title__, __version__, __url__
from .errors import HTTPException

log = logging.getLogger(__name__)


class RequestsPolicy(Enum):
    """An enumeration representing the """
    asynchronous = 0
    synchronous = 1


class HTTPClient:
    """Simplistic HTTP client to send requests to an url."""
    def __init__(self, loop=None, requests_policy=RequestsPolicy.asynchronous):
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.requests_policy = requests_policy

        # Build our default headers
        fmt = '{0}/{1} ({2}) Python/{3.major}.{3.minor}.{3.micro} aiohttp/{4} requests/{5}'
        user_agent = fmt.format(__title__, __version__, __url__, version_info, aiohttp.__version__, requests.__version__)
        self.default_headers = {'User-Agent': user_agent}

        # Prepare the sessions
        self.session_async = aiohttp.ClientSession(loop=loop, headers=self.default_headers)
        self.session_sync = requests.Session()
        self.session_sync.headers = self.default_headers

    def __del__(self):
        self.session_async.close()
        self.session_sync.close()

    @asyncio.coroutine
    def request_async(self, method, url, **kwargs):
        cls = kwargs.pop('cls', None)
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'], separators=(',', ':'))

        resp = yield from self.session_async.request(method, url, **kwargs)
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
            elif cls is not None:
                return cls(**rdata)
            else:
                return rdata
        finally:
            resp.release()

    def request_sync(self, method, url, **kwargs):
        cls = kwargs.pop('cls', None)
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'], separators=(',', ':'))

        resp = self.session_sync.request(method, url, **kwargs)
        try:
            # Strawpoll's API is supposed to always return json data, but whatever
            if 'application/json' in resp.headers['content-type']:
                rdata = resp.json()
            else:
                rdata = resp.text()

            data = kwargs['data'] if 'data' in kwargs else 'no data'
            log.debug('{} on {} with {} returned {}: {}'.format(method, url, resp.status_code, data, rdata))
            if resp.status_code != 200:
                raise HTTPException(resp, rdata)
            elif cls is not None:
                return cls(**rdata)
            else:
                return rdata
        finally:
            resp.close()

    def request(self, *args, **kwargs):
        request_policy = kwargs.pop('request_policy') or self.requests_policy

        if request_policy == RequestsPolicy.asynchronous:
            return self.request_async(*args, **kwargs)
        elif request_policy == RequestsPolicy.synchronous:
            return self.request_sync(*args, **kwargs)
        else:
            raise ValueError('Invalid request policy.')

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
