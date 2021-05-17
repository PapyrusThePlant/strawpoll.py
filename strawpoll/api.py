"""
:copyright: 2016 PapyrusThePlant
:license: MIT, see LICENSE for more details.
"""

import asyncio
import re

import strawpoll.poll
from .errors import *
from .http import HTTPClient, RequestsPolicy


class API:
    """Represents the strawpoll API.

    :param loop: The event loop to use for the asynchronous calls. Defaults to \
    `None`, which will grab the default event loop instead.
    """

    _BASE_URL = 'https://www.strawpoll.me'
    _BASE_API = _BASE_URL + '/api/v2'
    _POLLS = _BASE_API + '/polls'

    _url_re = re.compile('^{}\/(?P<id>[0-9]+)(/r)?$'.format(_BASE_URL.replace('/', '\/')))

    def __init__(self, *, loop=None, requests_policy=RequestsPolicy.asynchronous):
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self._http_client = HTTPClient(loop, requests_policy=requests_policy)

    def __del__(self):
        del self._http_client

    @property
    def requests_policy(self):
        return self._http_client.requests_policy

    def get_poll(self, arg, *, request_policy=None):
        """Retrieves a poll from strawpoll.

        :param arg: Either the ID of the poll or its strawpoll url.
        :param request_policy: Overrides :attr:`API.requests_policy` for that \
        request.
        :type request_policy: Optional[:class:`RequestsPolicy`]

        :raises HTTPException: Requesting the poll failed.

        :returns: A poll constructed with the requested data.
        :rtype: :class:`Poll`
        """
        if isinstance(arg, str):
            # Maybe we received an url to parse
            match = self._url_re.match(arg)
            if match:
                arg = match.group('id')

        return self._http_client.get('{}/{}'.format(self._POLLS, arg),
                                     request_policy=request_policy,
                                     cls=strawpoll.Poll)

    def submit_poll(self, poll, *, request_policy=None):
        """Submits a poll on strawpoll.

        :param poll: The poll to submit.
        :type poll: :class:`Poll`
        :param request_policy: Overrides :attr:`API.requests_policy` for that \
        request.
        :type request_policy: Optional[:class:`RequestsPolicy`]

        :raises ExistingPoll: This poll instance has already been submitted.
        :raises HTTPException: The submission failed.

        :returns: The given poll updated with the data sent back from the submission.
        :rtype: :class:`Poll`

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

        return self._http_client.post(self._POLLS,
                                      data=data,
                                      request_policy=request_policy,
                                      cls=strawpoll.Poll)
