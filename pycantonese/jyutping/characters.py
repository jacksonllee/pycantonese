from collections import Counter, defaultdict
from functools import lru_cache

from pycantonese.corpus import hkcancor
from pycantonese.data.rime_cantonese import (
    CHARS_TO_JYUTPING,
    LETTERED,
)
from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.word_segmentation import segment
from pycantonese.util import split_characters_with_alphanum, _deprecate


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
        # The ordering of the following dicts matters. The rime-cantonese
        # data may contain what's been re-segmented by this repo, and may
        # contain jyutping pronunciations for particular characters that
        # are only used in those contexts. The data from HKCanCor should comes
        # last to act as the default to override such cases.
        **{
            k: v
            for k, v in LETTERED.items()
            if len(split_characters_with_alphanum(k)) > 1
        },
        **{k: v for k, v in CHARS_TO_JYUTPING.items() if len(k) > 1},
        **words_to_jyutping,
    }

    # TODO: Extract characters from CHARS_TO_JYUTPING and LETTERED
    #    and add them to characters_to_jyutping
    characters_to_jyutping = {
        # The ordering of the following dicts matters. The rime-cantonese
        # data may contain what's been re-segmented by this repo, and may
        # contain jyutping pronunciations for particular characters that
        # are only used in those contexts. The data from HKCanCor should comes
        # last to act as the default to override such cases.
        **{k: v for k, v in LETTERED.items() if len(k) == 1},
        **{k: v for k, v in CHARS_TO_JYUTPING.items() if len(k) == 1},
        **characters_to_jyutping,
    }

    return words_to_jyutping, characters_to_jyutping


def characters_to_jyutping(chars):
    """Convert Cantonese characters into Jyutping romanization.

    The conversion model is based on the HKCanCor corpus and rime-cantonese
    data. Any unseen Cantonese character (or punctuation mark,
    for that matter) is represented by `None` in the output.

    The output is a list of segmented words, where each word is a 2-tuple of
    (Cantonese characters, Jyutping romanization).

    .. versionadded:: 3.0.0
        This function replaces the deprecated equivalent
        ``characters2jyutping``.

    .. versionchanged:: 3.0.0
        The returned valued is now a list of segmented words,
        where each word is a 2-tuple of (Cantonese characters, Jyutping).
        Previously, it was a list of Jyutping strings for the individual
        Cantonese characters.

    Parameters
    ----------
    chars : str
        A string of Cantonese characters.

    Returns
    -------
    list[tuple[str]]

    Examples
    --------
    >>> characters_to_jyutping("香港人講廣東話。")  # Hongkongers speak Cantonese.
    [('香港人', 'hoeng1gong2jan4'), ('講', 'gong2'), ('廣東話', 'gwong2dung1waa2'), ('。', None)]
    """  # noqa: E501
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


@_deprecate("characters2jyutping", "characters_to_jyutping", "3.0.0", "4.0.0")
def characters2jyutping(*args, **kwargs):
    """Same as characters_to_jyutping.

    .. deprecated:: 3.0.0
    """
    return characters_to_jyutping(*args, **kwargs)
