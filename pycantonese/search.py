# PyCantonese
#
# Copyright (C) 2015 PyCantonese Project
# Author: Jackson Lee <jsllee.phon@gmail.com>
# URL: <http://pycantonese.github.io/>
# For license information, see LICENSE.TXT

from nltk.corpus.reader.api import CorpusReader

from pycantonese.util import *
from pycantonese.jyutping import *
from pycantonese.corpus import CantoneseCorpusReader

#------------------------------------------------------------------------------#
# search functions

def search(corpus, onset=None, nucleus=None, coda=None, tone=None,
           initial=None, final=None, jp=None,
           character=None, pos=None,
           word_left=0, word_right=0):
    '''
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
    '''

    # check if ``corpus`` is really a corpus object
    if not isinstance(corpus, CantoneseCorpusReader):
        raise SearchError('a corpus object is required')

    # check if search elements conflict with one another
    if (onset != initial) and onset and initial:
        raise SearchError('onset conflicts with initial')
    if initial:
        onset = initial
    if final and (nucleus or coda):
        raise SearchError('final cannot be used together with either nucleus or'
                          ' coda (or both)')
    if jp and (onset or final or nucleus or coda or tone):
        raise SearchError('jp cannot be used together with other Jyutping '
                          'elements')
    if not (type(word_left) == type(word_right) == int):
        raise SearchError('both word_left and word_right must be integers')
    if (word_left < 0) or (word_right < 0):
        raise SearchError('both word_left and word_right must be non-negative')

    # check what kinds of search we are doing
    character_search = False
    jp_search = False
    pos_search = False

    if character:
        character_search = True
    if onset or nucleus or coda or tone or final or jp:
        jp_search = True
    if pos:
        pos_search = True
        pos = pos.upper() # PoS tags in NLP research are in caps by convention
    if not (character_search or jp_search or pos_search):
        raise SearchError('no search element')

    # check if jyutping search is valid
    if jp_search:
        if jp:
            try:
                jp_search_list = jyutping(jp)
            except:
                raise SearchError('invalid jyutping -- %s' % (repr(jp)))
            if len(jp_search_list) > 1:
                raise SearchError('only jyutping for one character is allowed')
            else:
                jp_search_tuple = jp_search_list[0]
        else:
            jp_validate_tuples = [ (onset, ONSET),
                                   (nucleus, NUCLEUS),
                                   (coda, CODA),
                                   (tone, TONE),
                                   (final, FINAL),
                                 ]
            for jp_element, checkset in jp_validate_tuples:
                if jp_element is None:
                    continue
                if jp_element not in checkset:
                    raise SearchError('invalid jyutping -- %s' % (repr(what)))
            if final:
                nucleus, coda = parse_final(final)
            jp_search_tuple = (onset, nucleus, coda, tone)

    tagged_sents = corpus.tagged_sents()
    result_list = list()

    for tagged_sent in tagged_sents:
        len_tagged_sent = len(tagged_sent)

        for idx, (character_jpstring, tag) in enumerate(tagged_sent):
            character_match = False
            jp_match = False
            pos_match = False
            if tag:
                tag = tag.casefold()

            if character_jpstring.count('_') == 1:
                character_str, jp_string = character_jpstring.split('_')
            else:
                continue # the character_jpstring is problematic

            # set "start" and "end" for slicing found results from sent
            if word_left < 0:
                word_start = 0
            else:
                word_start = idx - word_left
                if word_start < 0:
                    word_start = 0

            if word_right < 0:
                word_end = len_tagged_sent
            else:
                word_end = idx + word_right + 1
                if word_end > len_tagged_sent:
                    word_end = len_tagged_sent

            # If the search for X (X = {character, jp, pos}) is just irrelevant
            #   or the search matches,
            # then pass (= this iteration goes on)
            # otherwise move on to the next iteration

            # character search
            if (not character_search) or \
               (character_search and character in character_str):
                character_match = True
            else:
                continue

            # pos search
            if (not pos_search) or \
               (pos_search and pos == tag):
                pos_match = True
            else:
                continue

            # jyutping search
            if not jp_search:
                jp_match = True
            else:
                try:
                    jp_string_parsed_list = jyutping(jp_string)
                except JyutpingError:
                    continue

                for jp_string_parsed in jp_string_parsed_list:
                    jp_match = True

                    # walk through the 4 elements of onset, nucleus, coda, tone
                    for idx_tuple, jp_element in enumerate(jp_search_tuple):
                        if jp_element is None:
                            continue
                        if jp_element != jp_string_parsed[idx_tuple]:
                            jp_match = False
                            break

                    if jp_match:
                        break

            # if all tests pass, save the result
            if jp_match and character_match and pos_match:
                result_list.append(tagged_sent[word_start: word_end])

    if word_left == word_right == 0:
        return sum(result_list, [])
    else:
        return result_list

