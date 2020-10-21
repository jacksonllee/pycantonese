from functools import lru_cache

from wordseg import LongestStringMatching

from pycantonese.corpus import hkcancor
from pycantonese.data.rime_cantonese import (
    CHARS_TO_JYUTPING,
    LETTERED,
    PHRASES,
    MAPS,
)

_MAX_WORD_LENGTH = 5


@lru_cache(maxsize=1)
def _get_word_segmentation_model():
    model = LongestStringMatching(max_word_length=_MAX_WORD_LENGTH)
    corpus = hkcancor()
    # Train with HKCanCor data.
    model.fit(corpus.sents())
    # Train with rime-cantonese data.
    model._words |= CHARS_TO_JYUTPING.keys()
    model._words |= LETTERED.keys()
    model._words |= set(PHRASES)
    model._words |= set(MAPS)
    return model


def segment(sent_str):
    """
    Segment the unsegmented sentence.

    The word segmentation model is the longest string matching approach,
    trained by (i) the HKCanCor corpus included in this library and
    (ii) the rime-cantonese data.
    The segmented sentence does not contain words longer than five
    characters.

    :param sent_str: Unsegmented sentence string

    :return: Segmented sentence

    :rtype: list of str
    """
    if not sent_str:
        return []
    model = _get_word_segmentation_model()
    segmented = list(model.predict([sent_str]))[0]
    return segmented
