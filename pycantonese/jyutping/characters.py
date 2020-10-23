from collections import Counter, defaultdict
from functools import lru_cache

from pycantonese.corpus import hkcancor
from pycantonese.data.rime_cantonese import (
    CHARS_TO_JYUTPING,
    LETTERED,
)
from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.word_segmentation import segment
from pycantonese.util import split_characters_with_alphanum


@lru_cache(maxsize=1)
def _get_words_characters_to_jyutping():
    corpus = hkcancor()
    words_to_jyutping_counters = defaultdict(Counter)
    characters_to_jyutping_counters = defaultdict(Counter)

    for word, _, jyutping, _ in corpus.tagged_words():
        if not jyutping or not word:
            continue
        try:
            parsed_jp = parse_jyutping(jyutping)
        except ValueError:
            continue
        if len(word) != len(parsed_jp):
            continue
        words_to_jyutping_counters[word][jyutping] += 1
        for char, jp in zip(word, parsed_jp):
            characters_to_jyutping_counters[char]["".join(jp)] += 1

    words_to_jyutping = {}
    for word, jyutping_counter in words_to_jyutping_counters.items():
        jp = jyutping_counter.most_common(1)[0][0]
        words_to_jyutping[word] = jp
    characters_to_jyutping = {}
    for character, jyutping_counter in characters_to_jyutping_counters.items():
        jp = jyutping_counter.most_common(1)[0][0]
        characters_to_jyutping[character] = jp

    words_to_jyutping = {
        **words_to_jyutping,
        **{k: v for k, v in CHARS_TO_JYUTPING.items() if len(k) > 1},
        **{
            k: v
            for k, v in LETTERED.items()
            if len(split_characters_with_alphanum(k)) > 1
        },
    }

    # TODO: Extract characters from CHARS_TO_JYUTPING and LETTERED
    #    and add them to characters_to_jyutping
    characters_to_jyutping = {
        **characters_to_jyutping,
        **{k: v for k, v in CHARS_TO_JYUTPING.items() if len(k) == 1},
        **{k: v for k, v in LETTERED.items() if len(k) == 1},
    }

    return words_to_jyutping, characters_to_jyutping


def characters2jyutping(chars):
    """Convert Cantonese characters into Jyytping romanization.

    The conversion model is based on the HKCanCor corpus and rime-cantonese
    data. Any unseen Cantonese character (or punctuation mark,
    for that matter) is represented by `None` in the output.

    The output is organized by a word-segmented version of the input
    characters.
    Each word is a tuple of (word, jyutping).

    Parameters
    ----------
    chars : str
        A string of Cantonese characters.

    Returns
    -------
    list[tuple[str]]
    """
    if not chars:
        return []
    words_to_jyutping, chars_to_jyutping = _get_words_characters_to_jyutping()
    result = []
    for word in segment(chars):
        try:
            jp = words_to_jyutping[word]
        except KeyError:
            jp = ""
            for char in word:
                try:
                    jp += chars_to_jyutping[char]
                except KeyError:
                    jp = None
                    break
        result.append((word, jp))
    return result
