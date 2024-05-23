import re
from functools import lru_cache
from itertools import chain
from typing import List

from wordseg import LongestStringMatching

from pycantonese.corpus import hkcancor
from pycantonese.data.rime_cantonese import CHARS_TO_JYUTPING, LETTERED
from pycantonese.util import _split_chars_with_alphanum


_MAX_WORD_LENGTH = 5

_WHITESPACE_AROUND_ALPHANUM_REGEX = re.compile(r"(?<=[a-z0-9-])\s+|\s+(?=[a-z0-9-])")


class Segmenter(LongestStringMatching):
    """A customizable word segmentation model.

    .. versionadded:: 3.0.0
    """

    def __init__(
        self,
        *,
        max_word_length=_MAX_WORD_LENGTH,
        allow=None,
        disallow=None,
    ):
        """Initialize a Segmenter object.

        Parameters
        ----------
        max_word_length : int, optional
            Maximum word length this model allows.
        allow : iterable[str], optional
            Words to allow in word segmentation.
        disallow : iterable[str], optional
            Words to disallow in word segmentation.
        """
        super(Segmenter, self).__init__(max_word_length=max_word_length)

        # Train with HKCanCor data.
        self.fit(hkcancor().words(by_utterances=True))

        # Train with rime-cantonese data.
        self._words |= CHARS_TO_JYUTPING.keys()
        self._words |= LETTERED.keys()

        # Adjust with the allowed and disallowed words.
        self._words |= allow or set()
        self._words -= disallow or set()

        # Turn everything from strings to tuples due to alphanumeric chars.
        self._words = {_split_chars_with_alphanum(x) for x in self._words}

    def _predict_sent(self, sent_str):
        chars = _split_chars_with_alphanum(sent_str)
        segmented = super(Segmenter, self)._predict_sent(chars)
        # Turn the result back from tuples to strings.
        return map("".join, segmented)


@lru_cache(maxsize=1)
def _get_default_segmenter():
    return Segmenter()


def segment(unsegmented: str, cls: Segmenter = None) -> List[str]:
    """Segment the unsegmented input.

    The word segmentation model is the longest string matching approach,
    trained by (i) the HKCanCor corpus included in this library and
    (ii) the rime-cantonese data.
    The segmented sentence does not contain words longer than five
    characters.

    Parameters
    ----------
    unsegmented : str
        Unsegmented input.
    cls: Segmenter, optional
        A custom :class:`~pycantonese.word_segmentation.Segmenter` instance
        for setting the maximal
        word length (default = 5) and words to allow or disallow.
        If not provided, a default segmenter is used, with maximum word
        length = 5.

    Returns
    -------
    List[str]

    Examples
    --------
    >>> segment("廣東話容唔容易學？")  # "Is Cantonese easy to learn?"
    ['廣東話', '容', '唔', '容易', '學', '？']
    >>>
    >>> # Customizing the segmentation behavior.
    >>> from pycantonese.word_segmentation import Segmenter
    >>> segmenter = Segmenter(allow={"容唔容易"})
    >>> segment("廣東話容唔容易學？", cls=segmenter)
    ['廣東話', '容唔容易', '學', '？']
    """
    if not unsegmented:
        return []
    if cls is None:
        cls = _get_default_segmenter()
    elif not isinstance(cls, Segmenter):
        raise TypeError(f"`segmenter` must be a Segmenter object: {cls}")
    parts_to_segment = map(
        lambda x: x.replace(" ", ""),
        _WHITESPACE_AROUND_ALPHANUM_REGEX.split(unsegmented.strip()),
    )
    return list(
        chain.from_iterable(map(lambda x: next(cls.predict([x])), parts_to_segment))
    )
