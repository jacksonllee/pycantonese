# -*- coding: utf-8 -*-

# PyCantonese
#
# Copyright (C) 2014-2016 PyCantonese Project
# Author: Jackson Lee <jsllee.phon@gmail.com>
# URL: <http://pycantonese.org/>
# For license information, see LICENSE.TXT

"""
PyCantonese: Cantonese Linguistics and NLP in Python

Developer: Jackson Lee

http://pycantonese.org

"""

import os

from pycantonese.util import ENCODING
from pycantonese.corpus import CantoneseCHATReader
from pycantonese.jyutping import (  # noqa
    parse_jyutping, jyutping2tipa, jyutping2yale)

# -----------------------------------------------------------------------------
# METADATA
# -----------------------------------------------------------------------------

# Version
version_filename = os.path.join(os.path.dirname(__file__), 'VERSION')
try:
    with open(version_filename) as f:
        __version__ = f.read().strip()
except FileNotFoundError:
    __version__ = 'unknown version; VERSION file not found'


def hkcancor():
    """
    Create the corpus object for the Hong Kong Cantonese Corpus.
    """
    data_path = os.path.join(os.path.dirname(__file__),
                             'data', 'hkcancor', '*.cha')
    return CantoneseCHATReader(data_path, encoding='utf8')


def read_chat(*filenames, encoding=ENCODING):
    """
    Create a corpus object based on *filenames*.

    :param filenames: one or multiple filenames (absolute-path or relative to
        the current directory; with or without glob matching patterns)

    :param encoding: file encoding; defaults to 'utf8'.
    """
    return CantoneseCHATReader(*filenames, encoding=encoding)
