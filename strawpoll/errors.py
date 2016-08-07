"""
:copyright: 2016 PapyrusThePlant
:license: MIT, see LICENSE for more details.
"""


class StrawpollException(Exception):
    """Base class of all the other exceptions in strawpoll.py"""
    pass


class ExistingPoll(StrawpollException):
    """Exception thrown when an attempt to submit a poll that already has been submitted is made."""
    def __init__(self):
        super().__init__('This poll has already been submitted.')


class HTTPException(StrawpollException):
    """Exception thrown when an HTTP request failed.

    :cvar response: The failed HTTP request's response.
    :vartype response: `aiohttp.ClientResponse <http://aiohttp.readthedocs.org/en/stable/client_reference.html#aiohttp.ClientResponse>`_
    :cvar str text: The error message extracted from the response. Can be an empty string.
    :cvar int code: The error code extracted from the response. Can be 0 if no error code was found.
    """
    def __init__(self, response, data):
        self.response = response

        # Strawpoll's API is supposed to always return json data, but whatever
        if isinstance(data, dict):
            self.text = data.get('errorMessage', '')
            self.code = data.get('errorCode', 0)
        else:
            self.text = data

        fmt = '{0.reason} (status code: {0.status})'
        if len(self.text):
            fmt += ': {1}'

        super().__init__(fmt.format(self.response, self.text))