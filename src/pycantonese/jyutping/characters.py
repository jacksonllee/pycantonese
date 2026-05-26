from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache

from ..corpus import hkcancor, Token
from ..data.rime_cantonese import CHARS_TO_JYUTPING
from ..jyutping.parse_jyutping import parse_jyutping
from ..word_segmentation.segmenter import segment


@lru_cache(maxsize=1)
def _get_words_characters_to_jyutping():
    corpus = hkcancor()
    words_to_jyutping_counters = defaultdict(Counter)
    characters_to_jyutping_counters = defaultdict(Counter)

    for token in corpus.tokens():
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
        spaced = " ".join(str(jp) for jp in parsed_jp)
        words_to_jyutping_counters[word][spaced] += 1
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
        **CHARS_TO_JYUTPING,
    }

    chars_to_jp = {
        # The ordering of the following dicts matters.
        # rime-cantonese (more accurate data) overrides HKCanCor if they don't agree.
        **chars_to_jp,
        **{k: v for k, v in CHARS_TO_JYUTPING.items() if len(k) == 1},
    }

    return words_to_jyutping, chars_to_jp


def characters_to_jyutping(
    chars: str | list[str],
) -> list[tuple[str, str | None]]:
    """Convert Cantonese characters into Jyutping romanization.

    The conversion model is based on the HKCanCor corpus and rime-cantonese
    data. Any unseen Cantonese character (or punctuation mark,
    for that matter) is represented by ``None`` in the output.

    Args:
        chars (str or list[str]): A string of Cantonese characters, in which
            case word segmentation is also run on this input string
            (by :func:`~pycantonese.segment`) in order to resolve potential
            ambiguity in mapping characters to Jyutping. If you don't want
            word segmentation to be done, then provide a list of strings
            instead with your desired segmentation.

    Returns:
        list[tuple[str, str | None]]: A list of segmented words, where each
        word is a 2-tuple of (Cantonese characters, Jyutping romanization).
        Within the Jyutping string, syllables are separated by a single space.

    Examples:
        >>> characters_to_jyutping("香港人講廣東話。")  # Hongkongers speak Cantonese.
        [('香港人', 'hoeng1 gong2 jan4'), ('講', 'gong2'), ('廣東話', 'gwong2 dung1 waa2'), ('。', None)]

    See Also:
        :func:`~pycantonese.g2p`: One-shot grapheme-to-phoneme conversion that
        composes this function with :func:`~pycantonese.jyutping_to_ipa`.
    """  # noqa: E501
    if not chars:
        return []
    if isinstance(chars, list):
        segmented = chars
    else:
        segmented = segment(chars)
    words_to_jyutping, chars_to_jyutping = _get_words_characters_to_jyutping()
    result: list[tuple[str, str | None]] = []
    for word in segmented:
        try:
            jp: str | None = words_to_jyutping[word]
        except KeyError:
            parts: list[str] = []
            jp = None
            for char in word:
                try:
                    parts.append(chars_to_jyutping[char])
                except KeyError:
                    parts = []
                    break
            else:
                jp = " ".join(parts)
        result.append((word, jp))
    return result
