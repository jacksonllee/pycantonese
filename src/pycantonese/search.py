import dataclasses
import re

from .jyutping.parse_jyutping import parse_jyutping, _parse_final, Jyutping


def _jp_element_match(search_element, current_element):
    if search_element is None or re.search(search_element, current_element):
        return True
    else:
        return False


def _perform_search(
    tagged_sents,
    onset=None,
    nucleus=None,
    coda=None,
    tone=None,
    initial=None,
    final=None,
    jyutping=None,
    character=None,
    pos=None,
    word_range=(0, 0),
    utterance_range=(0, 0),
    by_tokens=True,
    by_utterances=False,
):
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
    # ensure tuple type: word_range and sent_range
    if not (type(word_range) == type(utterance_range) == tuple):
        raise ValueError("word_range and sent_range must be tuples")

    words_left, words_right = word_range
    sents_left, sents_right = utterance_range

    # ensure int type: words_left, words_right, sents_left, sents_right
    if not (
        type(words_left)
        == type(words_right)
        == type(sents_left)
        == type(sents_right)
        == int
    ):
        raise ValueError("int required for {words, sents}_{left, right}")

    if sents_left > 0 or sents_right > 0:
        by_utterances = True

    if tone is None:
        pass
    elif str(tone) not in "123456":
        raise ValueError(
            f"tone is used, but it's not one of {{1, 2, 3, 4, 5, 6}}: {tone}"
        )
    else:
        tone = str(tone)

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
        raise ValueError("no search elements")

    # check if jyutping search is valid
    jp_search_tuple = (None, None, None, None)

    if jp_search:

        # ensure compatible jyutping search elements
        if final and (nucleus or coda):
            raise ValueError(
                "final cannot be used together with either nucleus or coda (or both)"
            )
        if jyutping and (onset or final or nucleus or coda or tone):
            raise ValueError(
                "jyutping cannot be used together with other Jyutping elements"
            )
        if (onset != initial) and onset and initial:
            raise ValueError("onset conflicts with initial")

        # onset/initial
        if initial:
            onset = initial

        # determine jp_search_tuple
        if jyutping:
            try:
                jp_search_list = parse_jyutping(jyutping)
            except ValueError:
                raise ValueError("invalid jyutping -- %s" % (repr(jyutping)))
            if len(jp_search_list) > 1:
                raise ValueError("only jyutping for one character is allowed")
            else:
                jp_search_tuple = jp_search_list[0]
        else:
            if final:
                nucleus, coda = _parse_final(final)
            jp_search_tuple = Jyutping(onset, nucleus, coda, tone)

    result = []

    for tagged_sents_for_file in tagged_sents:
        sent_word_index_pairs = []

        for i_sent, tagged_sent in enumerate(tagged_sents_for_file):

            for i_word, tagged_word in enumerate(tagged_sent):
                c_characters = tagged_word.word
                c_pos = tagged_word.pos
                c_jyutping = tagged_word.jyutping

                # determine character_search and pos_search
                if character_search:
                    character_match = character in c_characters
                else:
                    character_match = True

                # if 'V' in c_pos.upper():
                #     import pdb; pdb.set_trace()
                if pos_search:
                    pos_match = bool(re.search(pos, c_pos))
                else:
                    pos_match = True

                if not (character_match and pos_match):
                    continue

                # determine if jyutping matches c_jyutping
                jyutping_match = False

                if not jp_search:
                    jyutping_match = True
                elif not c_jyutping:
                    pass
                else:
                    try:
                        c_parsed_jyutpings = parse_jyutping(c_jyutping)
                    except ValueError:
                        continue

                    for c_parsed_jyutping in c_parsed_jyutpings:

                        booleans = [
                            _jp_element_match(search_, current_)
                            for search_, current_ in zip(
                                dataclasses.astuple(jp_search_tuple),
                                dataclasses.astuple(c_parsed_jyutping),
                            )
                        ]

                        if all(booleans):
                            jyutping_match = True
                        break

                if jyutping_match:
                    sent_word_index_pairs.append((i_sent, i_word))

        results_list = []

        for i_sent, i_word in sent_word_index_pairs:
            if not by_utterances:
                tagged_sent = tagged_sents_for_file[i_sent]
                i_word_start = i_word - words_left
                i_word_end = i_word + words_right + 1

                if i_word_start < 0:
                    i_word_start = 0
                if i_word_end > len(tagged_sent):
                    i_word_end = len(tagged_sent)

                words_wanted = tagged_sent[i_word_start:i_word_end]

                if not by_tokens:
                    words_wanted = [x.word for x in words_wanted]

                if len(words_wanted) == 1:
                    words_wanted = words_wanted[0]

                results_list.append(words_wanted)
            else:
                i_sent_start = i_sent - sents_left
                i_sent_end = i_sent + sents_right + 1

                if i_sent_start < 0:
                    i_sent_start = 0
                if i_sent_end > len(tagged_sents_for_file):
                    i_sent_end = len(tagged_sents_for_file)

                sents_wanted = tagged_sents_for_file[i_sent_start:i_sent_end]

                if not by_tokens:
                    for i, sent in enumerate(sents_wanted[:]):
                        sents_wanted[i] = [x.word for x in sent]

                if len(sents_wanted) == 1:
                    sents_wanted = sents_wanted[0]

                results_list.append(sents_wanted)

        result.append(results_list)

    return result
