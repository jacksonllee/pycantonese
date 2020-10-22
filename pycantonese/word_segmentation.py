from functools import lru_cache

from wordseg import LongestStringMatching

from pycantonese.corpus import hkcancor
from pycantonese.data.rime_cantonese import (
    CHARS_TO_JYUTPING,
    LETTERED,
    PHRASES,
    MAPS,
)
from pycantonese.util import split_characters_with_alphanum


_MAX_WORD_LENGTH = 5

_ALLOWED_WORDS = None
_DISALLOWED_WORDS = None


class Segmenter(LongestStringMatching):
    """A customizable word segmentation model based on longest string match."""

    def __init__(
        self,
        *,
        max_word_length=_MAX_WORD_LENGTH,
        allow=None,
        disallow=None,
    ):
        """
        Initialize a Segmenter object.

        :param max_word_length: Maximum word length this model allows.
        :param allow: An iterable of word strings to allow as words.
        :param disallow: An iterable of word strings to disallow as words.
        """
        super(Segmenter, self).__init__(max_word_length=max_word_length)

        # Train with HKCanCor data.
        self.fit(hkcancor().sents())

        # Train with rime-cantonese data.
        self._words |= CHARS_TO_JYUTPING.keys()
        self._words |= LETTERED.keys()
        self._words |= set(PHRASES)
        self._words |= set(MAPS)

        # Adjust with the allowed and disallowed words.
        self._words |= allow or set()
        self._words -= disallow or set()

        # Turn everything from strings to tuples due to alphanumeric chars.
        self._words = {split_characters_with_alphanum(x) for x in self._words}

    def _predict_sent(self, sent_str):
        chars = split_characters_with_alphanum(sent_str)
        segmented = super(Segmenter, self)._predict_sent(chars)
        # Turn the result back from tuples to strings.
        segmented = ["".join(x) for x in segmented]
        return segmented


@lru_cache(maxsize=1)
def _get_default_segmenter():
    return Segmenter()


def segment(sent_str, cls=None):
    """
    Segment the unsegmented sentence.

    The word segmentation model is the longest string matching approach,
    trained by (i) the HKCanCor corpus included in this library and
    (ii) the rime-cantonese data.
    The segmented sentence does not contain words longer than five
    characters.

    :param sent_str: Unsegmented sentence string
    :param cls: A custom `Segmenter` class object for setting the maximal
        word length (default = 5) and words to allow or disallow.
        If not provided, a default segmenter is used, with maximum word
        length = 5.

    :return: Segmented sentence

    :rtype: list of str
    """
    if not sent_str:
        return []
    if cls is None:
        cls = _get_default_segmenter()
    if type(cls) != Segmenter:
        raise TypeError(f"`segmenter` must be a Segmenter object: {cls}")
    segmented = list(cls.predict([sent_str]))[0]
    return segmented
