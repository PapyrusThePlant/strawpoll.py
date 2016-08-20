"""
An async python wrapper for the Strawpoll API.

:copyright: 2016 PapyrusThePlant
:license: MIT, see LICENSE for more details.
"""

from collections import namedtuple

from .__about__ import __title__, __description__, __version__, __author__, __license__, __url__, __copyright__
from .api import API
from .errors import *
from .http import RequestsPolicy
from .poll import Poll

VersionInfo = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial'))
VersionInfo.__new__.__defaults__ = ('final', 0)
version_info = VersionInfo(*__version__.replace('-', '.').split('.'))
