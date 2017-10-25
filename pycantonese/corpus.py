# -*- coding: utf-8 -*-

# PyCantonese
#
# Copyright (C) 2014-2017 PyCantonese Project
# Author: Jackson Lee <jacksonlunlee@gmail.com>
# URL: <http://pycantonese.org/>
# For license information, see LICENSE.TXT


from pylangacq.chat import Reader

from pycantonese.search import perform_search
from pycantonese.util import (ENCODING, ALL_PARTICIPANTS,
                              get_jyutping_from_mor,
                              ListFromIterables)


class CantoneseCHATReader(Reader):
    """
    A class for reading Cantonese CHAT corpus files.
    """
    def __init__(self, *filenames, **kwargs):
        encoding = kwargs.get('encoding', ENCODING)
        super(CantoneseCHATReader, self).__init__(*filenames,
                                                  encoding=encoding)

    def MLU(self, participant='CHI'):
        raise NotImplementedError('method not applicable to PyCantonese')

    def MLUm(self, participant='CHI'):
        raise NotImplemented('method not applicable to PyCantonese')

    def MLUw(self, participant='CHI'):
        raise NotImplementedError('method not applicable to PyCantonese')

    def TTR(self, participant='CHI'):
        raise NotImplementedError('method not applicable to PyCantonese')

    def IPSyn(self, participant='CHI'):
        raise NotImplementedError('method not applicable to PyCantonese')

    def concordance(self, search_item, participant=ALL_PARTICIPANTS,
                    match_entire_word=True, lemma=False, by_files=False):
        raise NotImplementedError('method not applicable to PyCantonese')

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

        :param participant: Specify the participant(s); defaults to all
            participants.

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

        :param participant: Specify the participant(s); defaults to all
            participants.

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

        :param participant: Specify the participant(s); defaults to all
            participants.

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

        :param participant: Specify the participant(s); defaults to all
            participants.

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

    def search(self, onset=None, nucleus=None, coda=None, tone=None,
               initial=None, final=None, jyutping=None,
               character=None, pos=None,
               word_range=(0, 0), sent_range=(0, 0),
               tagged=True, sents=False,
               participant=ALL_PARTICIPANTS, by_files=False):
        """
        Search for the specified element(s).

        **Jyutping elements**

        Parameters are *onset*, *nucleus*, *coda*, *tone*, *initial*,
        *final*, *jyutping*.
        If *jyutping* is used, none of the other Jyutping elements can be.
        If *final* is used, neither *nucleus* nor *coda* can be.
        *onset* and *initial* cannot conflict, unless one or both of them are
        None.
        Regular expression matching applies to
        *onset*, *nucleus*, *coda*, *tone*, and *initial*.

        **Chinese character**

        Parameter: *character* (only one is allowed)

        **Part-of-speech tag**

        Parameter: *pos*

        Regular expression matching applies.

        **Word or sentence range**

        *word_range*: specify the span of words to the left and right
        of a match word; defaults to ``(0, 0)``.

        *sent_range*: specify the span of sents preceding and following
        the sent containing a match word; defaults to ``(0, 0)``.

        If *sent_range* is used, *word_range* is ignored.

        **Output formatting**

        If *sents* is True (the default), sents containing a match word are
        returned; otherwise just a word instead.

        If *tagged* is True (the default), words are tagged in the form of
        (word, pos, jyutping, rel); otherwise just word token strings.

        *by_files*: If False (the default), the return object is a list
        encompassing search results for all files. If True, the return object
        is dict(absolute-path filename: list of search results for that file)
        instead.

        **Others**

        *participant*: specify the participant(s) (default: all participants).
        """
        fn_to_results = perform_search(
            self.tagged_sents(participant=participant, by_files=True),
            onset=onset, nucleus=nucleus, coda=coda, tone=tone,
            initial=initial, final=final, jyutping=jyutping,
            character=character, pos=pos,
            word_range=word_range, sent_range=sent_range,
            tagged=tagged, sents=sents)

        if by_files:
            return fn_to_results
        else:
            return ListFromIterables(*(v for _, v in
                                       sorted(fn_to_results.items())))
