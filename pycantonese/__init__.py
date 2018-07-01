# PyCantonese
#
# Copyright (C) 2014-2018 PyCantonese Project
# Author: Jackson Lee <jacksonlunlee@gmail.com>
# URL: <http://pycantonese.org/>
# For license information, see LICENSE.TXT

"""PyCantonese: Cantonese Linguistics and NLP in Python

Developer: Jackson Lee

http://pycantonese.org

"""

# flake8: noqa

from pycantonese._version import __version__
from pycantonese.corpus import hkcancor, read_chat
from pycantonese.jyutping import parse_jyutping, jyutping2tipa, jyutping2yale
from pycantonese.stop_words import stop_words
