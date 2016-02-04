# -*- coding: utf-8 -*-

# PyCantonese
#
# Copyright (C) 2014-2016 PyCantonese Project
# Author: Jackson Lee <jsllee.phon@gmail.com>
# URL: <http://pycantonese.org/>
# For license information, see LICENSE.TXT

import re

from pycantonese.util import (ALL_PARTICIPANTS, get_jyutping_from_mor)
from pycantonese.jyutping import (parse_jyutping, parse_final)


def _jp_element_match(search_element, current_element):
    if search_element is None or re.fullmatch(search_element, current_element):
        return True
    else:
        return False


def perform_search(fn_to_tagged_sents,
                   onset=None, nucleus=None, coda=None, tone=None,
                   initial=None, final=None, jyutping=None,
                   character=None, pos=None,
                   words_left=0, words_right=0, sents_left=0, sents_right=0,
                   tagged=True, sents=True,
                   participant=ALL_PARTICIPANTS, by_files=False):
    """
    overall strategy: deal with jp (and all jp-related elements) first, and
                      then the character

    1. jp

    hierarchy of jp and associated search elements:
                      jp
                 /     |    \
      onset/initial  final  tone
                     /   \
                nucleus  coda

    lower search elements cannot be used together with dominating higher
    elements
    """
    # ensure int type: words_left, words_right, sents_left, sents_right
    if not (type(words_left) == type(words_right) == 
            type(sents_left) == type(sents_right) == int):
        raise ValueError('int required for {words, sents}_{left, right}')

    if sents_left > 0 or sents_right > 0:
        sents = True

    # determine what kinds of search we are doing
    character_search = False
    jp_search = False
    pos_search = False

    if character:
        character_search = True
    if onset or nucleus or coda or tone or final or jyutping:
        jp_search = True
    if pos:
        pos_search = True
    if not (character_search or jp_search or pos_search):
        raise ValueError('no search elements')

    # check if jyutping search is valid
    jp_search_tuple = None

    if jp_search:

        # ensure compatible jyutping search elements
        if final and (nucleus or coda):
            raise ValueError('final cannot be used together with '
                             'either nucleus or coda (or both)')
        if jyutping and (onset or final or nucleus or coda or tone):
            raise ValueError('jyutping cannot be used together with other '
                             'Jyutping elements')
        if (onset != initial) and onset and initial:
            raise ValueError('onset conflicts with initial')

        # onset/initial
        if initial:
            onset = initial

        # determine jp_search_tuple
        if jyutping:
            try:
                jp_search_list = parse_jyutping(jyutping)
            except ValueError:
                raise ValueError('invalid jyutping -- %s' % (repr(jyutping)))
            if len(jp_search_list) > 1:
                raise ValueError('only jyutping for one character is allowed')
            else:
                jp_search_tuple = jp_search_list[0]
        else:
            if final:
                nucleus, coda = parse_final(final)
            jp_search_tuple = (onset, nucleus, coda, tone)

    fn_to_results = dict()

    for fn, tagged_sents in fn_to_tagged_sents.items():
        results_list = list()
        sent_word_index_pairs = list()

        for i_sent, tagged_sent in enumerate(tagged_sents):

            for i_word, tagged_word in enumerate(tagged_sent):
                c_characters, c_pos, c_mor, _ = tagged_word  # c = current
                c_jyutping = get_jyutping_from_mor(c_mor)

                # determine character_search and pos_search
                if character_search:
                    character_match = character in c_characters
                else:
                    character_match = True

                if pos_search:
                    pos_match = re.fullmatch(pos, c_pos)
                else:
                    pos_match = True

                if not (character_match and pos_match):
                    continue

                # determine if jyutping matches c_jyutping
                try:
                    c_parsed_jyutpings = parse_jyutping(c_jyutping)
                except ValueError:
                    continue

                jyutping_match = False
                for c_parsed_jyutping in c_parsed_jyutpings:

                    booleans = [_jp_element_match(search_, current_)
                                for search_, current_ in
                                zip(jp_search_tuple, c_parsed_jyutping)]

                    if all(booleans):
                        jyutping_match = True
                        break

                if jyutping_match:
                    sent_word_index_pairs.append((i_sent, i_word))

        for i_sent, i_word in sent_word_index_pairs:
            if not sents:
                tagged_sent = tagged_sents[i_sent]
                i_word_start = i_word - words_left
                i_word_end = i_word + words_right + 1

                if i_word_start < 0:
                    i_word_start = 0
                if i_word_end > len(tagged_sent):
                    i_word_end = len(tagged_sent)

                words_wanted = tagged_sent[i_word_start: i_word_end]

                if not tagged:
                    words_wanted = [x[0] for x in words_wanted]

                if len(words_wanted) == 1:
                    words_wanted = words_wanted[0]

                results_list.append(words_wanted)
            else:
                pass

        fn_to_results[fn] = results_list

    return fn_to_results
