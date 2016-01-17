# -*- coding: utf-8 -*-

# PyCantonese
#
# Copyright (C) 2015 PyCantonese Project
# Author: Jackson Lee <jsllee.phon@gmail.com>
# URL: <http://pycantonese.org/>
# For license information, see LICENSE.TXT

import os

#------------------------------------------------------------------------------#
# constants
#------------------------------------------------------------------------------#

# system-related stuff

ABSPATH = os.path.dirname(os.path.abspath(__file__))


#------------------------------------------------------------------------------#
# error classes
#------------------------------------------------------------------------------#

class JyutpingError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class SearchError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

