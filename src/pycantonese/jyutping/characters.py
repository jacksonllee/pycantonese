from collections import Counter, defaultdict
from functools import lru_cache
from typing import List, Tuple

from pycantonese.corpus import hkcancor, Token
from pycantonese.data.rime_cantonese import CHARS_TO_JYUTPING, LETTERED
from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.word_segmentation import _get_default_segmenter, segment, Segmenter
from pycantonese.util import _split_chars_with_alphanum, _deprecate


@lru_cache(maxsize=1)
def _get_words_characters_to_jyutping():
    corpus = hkcancor()
    words_to_jyutping_counters = defaultdict(Counter)
    characters_to_jyutping_counters = defaultdict(Counter)

    for token in corpus.tokens(by_utterances=False):
        token: Token
        word = token.word
        jyutping = token.jyutping

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
            characters_to_jyutping_counters[char][str(jp)] += 1

    words_to_jyutping = {}
    for word, jyutping_counter in words_to_jyutping_counters.items():
        jp = jyutping_counter.most_common(1)[0][0]
        words_to_jyutping[word] = jp
    chars_to_jp = {}
    for character, jyutping_counter in characters_to_jyutping_counters.items():
        jp = jyutping_counter.most_common(1)[0][0]
        chars_to_jp[character] = jp

    words_to_jyutping = {
        # The ordering of the following dicts matters.
        # rime-cantonese (more accurate data) overrides HKCanCor if they don't agree.
        **words_to_jyutping,
        **{k: v for k, v in LETTERED.items() if len(_split_chars_with_alphanum(k)) > 1},
        **{k: v for k, v in CHARS_TO_JYUTPING.items() if len(k) > 1},
    }

    # TODO: Extract characters from CHARS_TO_JYUTPING and LETTERED
    #    and add them to characters_to_jyutping
    chars_to_jp = {
        # The ordering of the following dicts matters.
        # rime-cantonese (more accurate data) overrides HKCanCor if they don't agree.
        **chars_to_jp,
        **{k: v for k, v in LETTERED.items() if len(k) == 1},
        **{k: v for k, v in CHARS_TO_JYUTPING.items() if len(k) == 1},
    }

    return words_to_jyutping, chars_to_jp


def characters_to_jyutping(
    chars: str, segmenter: Segmenter = None
) -> List[Tuple[str, str]]:
    """Convert Cantonese characters into Jyutping romanization.

    The conversion model is based on the HKCanCor corpus and rime-cantonese
    data. Any unseen Cantonese character (or punctuation mark,
    for that matter) is represented by `None` in the output.

    This function also performs word segmentation, in order to resolve potential
    ambiguity in mapping characters to Jyutping.

    Parameters
    ----------
    chars : str
        A string of Cantonese characters.
    segmenter : Segmenter, optional
        A :class:`~pycantonese.word_segmentation.Segmenter` instance to customize
        word segmentation.
        If specified, this segmenter is passed to the ``cls`` keyword argument of
        :func:`~pycantonese.segment`.
        If ``None`` or not given, the default segmenter is used.

    Returns
    -------
    list[tuple[str, str]]
        A list of segmented words, where each word is a 2-tuple of
        (Cantonese characters, Jyutping romanization).

    Examples
    --------
    >>> characters_to_jyutping("香港人講廣東話。")  # Hongkongers speak Cantonese.
    [('香港人', 'hoeng1gong2jan4'), ('講', 'gong2'), ('廣東話', 'gwong2dung1waa2'), ('。', None)]
    """  # noqa: E501
    if not chars:
        return []
    words_to_jyutping, chars_to_jyutping = _get_words_characters_to_jyutping()
    result = []
    if segmenter is None:
        segmenter = _get_default_segmenter()
    for word in segment(chars, cls=segmenter):
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
