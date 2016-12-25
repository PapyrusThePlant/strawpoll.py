"""
:copyright: 2016 PapyrusThePlant
:license: MIT, see LICENSE for more details.
"""

import strawpoll.api
from .utils import OrderedCounter


class Poll:
    """Represents a poll from strawpoll.

    :param str title: The question that the poll is asking.
    :param iterable options: An iterable of elements accepting the ``str()`` \
    operation.

    :cvar int id: The poll ID on strawpoll. If the poll has not \
    been submitted on or retrieved from strawpoll, it's None instead.
    :cvar bool multi: Specifies if the polls accepts multiple votes \
    from one user. Defaults to ``False``.
    :cvar str dupcheck: Defines how to handle checking for \
    duplicate votes. Defaults to ``normal``.
    :cvar bool captcha: Specifies if the poll requires users to \
    pass a captcha to vote. Defaults to ``False``.
    """
    def __init__(self, title, options, **kwargs):
        self.title = title
        self._results = OrderedCounter()
        self.id = kwargs.pop('id', None)
        self.multi = kwargs.pop('multi', False)
        self.dupcheck = kwargs.pop('dupcheck', 'normal')
        self.captcha = kwargs.pop('captcha', False)

        for i, option in enumerate(options):
            self._results[str(option)] = kwargs['votes'][i] if 'votes' in kwargs else 0

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.id != other.id

    def __str__(self):
        return self.title

    @property
    def options(self):
        """Returns a list of strings to represent the options for the poll, in
        the order they were given when the poll was created.
        """
        return list(self._results.keys())

    @property
    def votes(self):
        """Return a list of integers that correspond to the same indexed option
        which specify the current votes for that option.
        """
        return list(self._results.values())

    @property
    def total_votes(self):
        """Returns the total number of votes on the poll."""
        return sum(self._results.values())

    @property
    def url(self):
        """Returns the url of the poll. If the poll has not been submitted yet,
        an empty string is returned instead.
        """
        if self.id is None:
            return ''
        return '{}/{}'.format(strawpoll.API._BASE_URL, self.id)

    def results(self, limit=None):
        """Returns a list of tuples each containing a string representing an
        option and an int which specify the current votes for that option,
        ordered by their votes count.

        :param int limit: The maximum number of results to return. If not \
        specified, every results will be returned.
        """
        return self._results.most_common(limit)

    def result_at(self, index):
        """Returns a tuple containing a string representing the option and an
        int which specify the current votes for that option.

        :param int index: The index of the wanted option in the options list.
        """
        return list(self._results.items())[index]
