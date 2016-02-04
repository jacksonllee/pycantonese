# -*- coding: utf-8 -*-

# PyCantonese
#
# Copyright (C) 2014-2016 PyCantonese Project
# Author: Jackson Lee <jsllee.phon@gmail.com>
# URL: <http://pycantonese.org/>
# For license information, see LICENSE.TXT


ALL_PARTICIPANTS = '**ALL**'
ENCODING = 'utf8'


class SearchError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class ListFromIterables(list):
    """
    A class like ``list`` that can be initialized with iterables.
    """
    def __init__(self, *iterables):
        super(ListFromIterables, self).__init__()
        self.input_iterables = iterables
        self.from_iterables()

    def from_iterables(self):
        for it in self.input_iterables:
            for element in it:
                self.append(element)


def get_jyutping_from_mor(mor):
    """
    Extract jyutping string from *mor*
    """
    jyutping, _, _ = mor.partition('=')
    jyutping, _, _ = jyutping.partition('-')
    jyutping, _, _ = jyutping.partition('&')
    return jyutping
