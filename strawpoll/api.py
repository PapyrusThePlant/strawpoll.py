"""
:copyright: 2016 PapyrusThePlant
:license: MIT, see LICENSE for more details.
"""

import asyncio
import re

import strawpoll.poll
from .errors import *
from .http import HTTPClient


class API:
    """Represents the strawpoll API.

    :param loop: The event loop to use for the asynchronous calls. Defaults to \
    `None`, which will grab the default event loop instead.
    """

    _BASE_URL = 'http://www.strawpoll.me'
    _BASE_API = _BASE_URL + '/api/v2'
    _POLLS = _BASE_API + '/polls'

    _url_re = re.compile('^{}\/(?P<id>[0-9]+)(/r)?$'.format(_BASE_URL.replace('/', '\/')))

    def __init__(self, *, loop=None):
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self._http_client = HTTPClient(loop)

    def __del__(self):
        del self._http_client

    @asyncio.coroutine
    def get_poll(self, arg):
        """|coroutine|

        Retrieves a poll from strawpoll.

        :param arg: Either the ID of the poll or its strawpoll url.

        :raises HTTPException: Requesting the poll failed.

        :returns: A poll constructed with the requested data.
        :rtype: Poll
        """
        if isinstance(arg, str):
            # Maybe we received an url to parse
            match = self._url_re.match(arg)
            if match:
                arg = match.group('id')

        data = yield from self._http_client.get('{}/{}'.format(self._POLLS, arg))
        return strawpoll.poll.Poll(**data)

    @asyncio.coroutine
    def submit_poll(self, poll):
        """|coroutine|

        Submits a poll on strawpoll.

        :param Poll poll: The poll to submit.

        :raises ExistingPoll: This poll instance has already been submitted.
        :raises HTTPException: The submission failed.

        :returns: The poll updated with the data sent back from the submission.
        :rtype: Poll

        .. note::
            Only polls that have a non empty title and between 2 and 30 options
            can be submitted.
        """
        if poll.id is not None:
            raise ExistingPoll()

        options = poll.options
        data = {
            'title': poll.title,
            'options': options,
            'multi': poll.multi,
            'dupcheck': poll.dupcheck,
            'captcha': poll.captcha
        }

        data = yield from self._http_client.post(self._POLLS, data=data)
        poll.id = data['id']
