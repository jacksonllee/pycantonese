# -*- coding: utf-8 -*-

# PyCantonese
#
# Copyright (C) 2014-2017 PyCantonese Project
# Author: Jackson Lee <jacksonlunlee@gmail.com>
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
except FileNotFoundError:  # noqa F821 (py2 compatibility)
    __version__ = 'unknown version; VERSION file not found'


def hkcancor():
    """
    Create the corpus object for the Hong Kong Cantonese Corpus.
    """
    data_path = os.path.join(os.path.dirname(__file__),
                             'data', 'hkcancor', '*.cha')
    return CantoneseCHATReader(data_path, encoding='utf8')


def read_chat(*filenames, **kwargs):
    """
    Create a corpus object based on *filenames*.

    :param filenames: one or multiple filenames (absolute-path or relative to
        the current directory; with or without glob matching patterns)

    :param kwargs: Keyword arguments. Currently, only ``encoding`` is
        recognized, which defaults to 'utf8'.
    """
    encoding = kwargs.get('encoding', ENCODING)
    return CantoneseCHATReader(*filenames, encoding=encoding)
