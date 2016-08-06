#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
:copyright: 2016 Papyrus
:license: MIT, see LICENSE for more details.
"""

import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

about = {}
with open('strawpoll/__about__.py') as fp:
    exec(fp.read(), about)

# Utility aliases

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

if sys.argv[-1] == 'info':
    for k, v in about.items():
        print('{}: {}'.format(k, v))
    sys.exit()

# Call setup as usual

with open('requirements.txt') as fp:
    install_requires = fp.read().splitlines()

with open('README.rst') as fp:
    long_description = fp.read()

setup(name=about['__title__'],
      version=about['__version__'],
      description='An async python wrapper for the Strawpoll API.',
      long_description=long_description,
      author=about['__author__'],
      license=about['__license__'],
      url=about['__url__'],
      packages=['strawpoll'],
      include_package_data=True,
      install_requires=install_requires,
      keywords=about['__title__'],
      zip_safe = False,
      classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
      ]
)
