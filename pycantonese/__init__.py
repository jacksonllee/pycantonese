# -*- coding: utf-8 -*-

# PyCantonese
#
# Copyright (C) 2014-2017 PyCantonese Project
# Author: Jackson Lee <jacksonlunlee@gmail.com>
# URL: <http://pycantonese.org/>
# For license information, see LICENSE.TXT

# flake8: noqa

"""PyCantonese: Cantonese Linguistics and NLP in Python

Developer: Jackson Lee

http://pycantonese.org

"""

import os

from pycantonese.corpus import hkcancor, read_chat
from pycantonese.jyutping import parse_jyutping, jyutping2tipa, jyutping2yale


with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    __version__ = f.read().strip()
