# -*- coding: utf-8 -*-

# PyCantonese
#
# Copyright (C) 2014-2016 PyCantonese Project
# Author: Jackson Lee <jsllee.phon@gmail.com>
# URL: <http://pycantonese.org/>
# For license information, see LICENSE.TXT

# corpus reader class for all Cantonese corpora in general


from pylangacq.chat import Reader

from pycantonese.util import (ENCODING, ALL_PARTICIPANTS,
                              get_jyutping_from_mor,
                              ListFromIterables)


class CantoneseCHATReader(Reader):
    """
    A class for reading Cantonese CHAT corpus files.
    """
    def __init__(self, *filenames, encoding=ENCODING):
        super(CantoneseCHATReader, self).__init__(*filenames, encoding=encoding)

    def _get_jyutping_sents(self, participant=ALL_PARTICIPANTS, sents=True):
        fname_to_tagged_sents = self.tagged_sents(participant=participant,
                                                  by_files=True)

        fn_to_jyutpings = dict()
        jyutpings_list = list()

        for fn in self.filenames():
            fn_to_jyutpings[fn] = list()
            tagged_sents = fname_to_tagged_sents[fn]

            for tagged_sent in tagged_sents:
                if sents:
                    jyutpings_list = list()

                for tagged_word in tagged_sent:
                    _, _, mor, _ = tagged_word
                    jyutping = get_jyutping_from_mor(mor)

                    if sents:
                        jyutpings_list.append(jyutping)
                    else:
                        fn_to_jyutpings[fn].append(jyutping)

                if sents:
                    fn_to_jyutpings[fn].append(jyutpings_list)

        return fn_to_jyutpings

    def jyutpings(self, participant=ALL_PARTICIPANTS, by_files=False):
        """
        Return a list of jyutping strings by *participant* in all files.

        :param participant: The participant(s) of interest (default is all
            participants if unspecified). This parameter is flexible.
            Set it to be ``'XXA'`` for this particular person, for example.
            If multiple participants are desired, this parameter can take
            a sequence such as ``{'XXA', 'XXB'}``.
            Underlyingly, this parameter actually performs
            regular expression matching.
            To include all participants except "XXA", use ``^(?!.*XXA).*$``.

        :param by_files: If True (default: False), return dict(absolute-path
            filename: X for that file) instead of X for all files altogether.

        :rtype: list(str), or dict(str: list(str))
        """
        fn_to_jyutpings = self._get_jyutping_sents(participant=participant,
                                                    sents=False)

        if by_files:
            return fn_to_jyutpings
        else:
            return ListFromIterables(*(v for _, v in
                                       sorted(fn_to_jyutpings.items())))

    def jyutping_sents(self, participant=ALL_PARTICIPANTS, by_files=False):
        """
        Return a list of sents of jyutping strings
        by *participant* in all files.

        :param participant: The participant(s) of interest (default is all
            participants if unspecified). This parameter is flexible.
            Set it to be ``'XXA'`` for this particular person, for example.
            If multiple participants are desired, this parameter can take
            a sequence such as ``{'XXA', 'XXB'}``.
            Underlyingly, this parameter actually performs
            regular expression matching.
            To include all participants except "XXA", use ``^(?!.*XXA).*$``.

        :param by_files: If True (default: False), return dict(absolute-path
            filename: X for that file) instead of X for all files altogether.

        :rtype: list(list(str)), or dict(str: list(list(str)))
        """
        fn_to_jyutpings = self._get_jyutping_sents(participant=participant,
                                                    sents=True)

        if by_files:
            return fn_to_jyutpings
        else:
            return ListFromIterables(*(v for _, v in
                                       sorted(fn_to_jyutpings.items())))

    def _get_character_sents(self, participant=ALL_PARTICIPANTS, sents=True):
        fname_to_tagged_sents = self.tagged_sents(participant=participant,
                                                  by_files=True)

        fn_to_characters = dict()
        characters_list = list()

        for fn in self.filenames():
            fn_to_characters[fn] = list()
            tagged_sents = fname_to_tagged_sents[fn]

            for tagged_sent in tagged_sents:
                if sents:
                    characters_list = list()

                for tagged_word in tagged_sent:
                    chs, _, _, _ = tagged_word

                    if chs and '\u4e00' <= chs[0] <= '\u9fff':
                        characters_in_word = list(chs)
                    else:
                        characters_in_word = [chs]

                    if sents:
                        characters_list.extend(characters_in_word)
                    else:
                        fn_to_characters[fn].extend(characters_in_word)

                if sents:
                    fn_to_characters[fn].append(characters_list)

        return fn_to_characters

    def characters(self, participant=ALL_PARTICIPANTS, by_files=False):
        """
        Return a list of Chinese characters by *participant* in all files.

        :param participant: The participant(s) of interest (default is all
            participants if unspecified). This parameter is flexible.
            Set it to be ``'XXA'`` for this particular person, for example.
            If multiple participants are desired, this parameter can take
            a sequence such as ``{'XXA', 'XXB'}``.
            Underlyingly, this parameter actually performs
            regular expression matching.
            To include all participants except "XXA", use ``^(?!.*XXA).*$``.

        :param by_files: If True (default: False), return dict(absolute-path
            filename: X for that file) instead of X for all files altogether.

        :rtype: list(str), or dict(str: list(str))
        """
        fn_to_characters = self._get_character_sents(participant=participant,
                                                     sents=False)

        if by_files:
            return fn_to_characters
        else:
            return ListFromIterables(*(v for _, v in
                                       sorted(fn_to_characters.items())))

    def character_sents(self, participant=ALL_PARTICIPANTS, by_files=False):
        """
        Return a list of sents of Chinese characters
        by *participant* in all files.

        :param participant: The participant(s) of interest (default is all
            participants if unspecified). This parameter is flexible.
            Set it to be ``'XXA'`` for this particular person, for example.
            If multiple participants are desired, this parameter can take
            a sequence such as ``{'XXA', 'XXB'}``.
            Underlyingly, this parameter actually performs
            regular expression matching.
            To include all participants except "XXA", use ``^(?!.*XXA).*$``.

        :param by_files: If True (default: False), return dict(absolute-path
            filename: X for that file) instead of X for all files altogether.

        :rtype: list(list(str)), or dict(str: list(list(str)))
        """
        fn_to_characters = self._get_character_sents(participant=participant,
                                                     sents=True)

        if by_files:
            return fn_to_characters
        else:
            return ListFromIterables(*(v for _, v in
                                       sorted(fn_to_characters.items())))
