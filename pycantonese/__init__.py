# -*- coding: utf-8 -*-

# PyCantonese
#
# Copyright (C) 2014-2016 PyCantonese Project
# Author: Jackson Lee <jsllee.phon@gmail.com>
# URL: <http://pycantonese.org/>
# For license information, see LICENSE.TXT

"""
PyCantonese: Cantonese Linguistics in Python

Developer: Jackson Lee

http://pycantonese.org

"""

import os

from pycantonese.corpus import CantoneseCHATReader

# ------------------------------------------------------------------------------
# METADATA
# ------------------------------------------------------------------------------

# Version
version_filename = os.path.join(os.path.dirname(__file__), 'VERSION')
try:
    with open(version_filename) as f:
        __version__ = f.read().strip()
except FileNotFoundError:
    __version__ = 'unknown version; VERSION file not found'

# Copyright notice and license
__copyright__ = """\
Copyright (C) 2014-2016 PyCantonese Project.

Distributed and Licensed under the Apache License, Version 2.0,
which is included by reference.
"""
__license__ = 'Apache License, Version 2.0'

# Description
__description__ = 'PyCantonese'

# Long description
__long_description__ = 'PyCantonese: Cantonese Linguistics in Python'

# keywords
__keywords__ = ['computational linguistics', 'natural language processing',
                'NLP', 'Cantonese', 'linguistics', 'corpora', 'speech',
                'language', 'Chinese', 'Jyutping', 'tagging']

# URL
__url__ = "http://pycantonese.org/"

# maintainer
__maintainer__ = "Jackson Lee"
__maintainer_email__ = "jsllee.phon@gmail.com"
__author__ = __maintainer__
__author_email__ = __maintainer_email__

# trove classifiers for Python Package Index
__classifiers__ = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: Chinese (Traditional)',
    'Natural Language :: Cantonese',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Filters',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Indexing',
    'Topic :: Text Processing :: Linguistic'
]

__install_requires__ = ['pylangacq']

# ------------------------------------------------------------------------------
# CORPUS OBJECTS
# ------------------------------------------------------------------------------


def hkcancor():
    data_path = os.path.join(os.path.dirname(__file__),
                             'data', 'hkcancor', '*.cha')
    return CantoneseCHATReader(data_path, encoding='utf8')
