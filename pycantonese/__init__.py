# PyCantonese
#
# Copyright (C) 2015 PyCantonese Project
# Author: Jackson Lee <jsllee.phon@gmail.com>
# URL: <http://pycantonese.github.io/>
# For license information, see LICENSE.TXT

'''
PyCantonese: A Python module for working with Cantonese corpus data

Developer: Jackson Lee

http://pycantonese.github.io

'''


#------------------------------------------------------------------------------#
# METADATA
#------------------------------------------------------------------------------#

# Version
__version__ = '1.1-alpha.1'

# Copyright notice and license
__copyright__ = """\
Copyright (C) 2015 PyCantonese Project.

Distributed and Licensed under the Apache License, Version 2.0,
which is included by reference.
"""
__license__ = "Apache License, Version 2.0"

# Description
__description__ = "PyCantonese"

# Long description
__long_description__ = """\
PyCantonese is a Python module for working with Cantonese corpus data.
PyCantonese requires Python 3.0 or higher."""

# keywords
__keywords__ = ['computational linguistics', 'natural language processing',
                'NLP', 'Cantonese', 'linguistics', 'corpora', 'speech',
                'language', 'Chinese', 'Jyutping', 'NLTK', 'tagging']

# URL
__url__ = "http://pycantonese.github.io/"

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
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
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

__install_requires__ = ["nltk"]

#------------------------------------------------------------------------------#
# PACKAGES
#------------------------------------------------------------------------------#

from pycantonese.util import *
from pycantonese.jyutping import *
from pycantonese.search import *
from pycantonese.corpus import *

