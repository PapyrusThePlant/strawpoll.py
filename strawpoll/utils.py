"""
:copyright: 2016 PapyrusThePlant
:license: MIT, see LICENSE for more details.
"""

from collections import Counter, OrderedDict


class OrderedCounter(Counter, OrderedDict):
    """A counter that remembers the order elements are first encountered."""

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(OrderedDict(self)))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)
