from functools import lru_cache
from typing import List

from wordseg import LongestStringMatching

from .corpus import hkcancor
from .data.rime_cantonese import CHARS_TO_JYUTPING, LETTERED
from .util import _split_chars_with_alphanum


_MAX_WORD_LENGTH = 5


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
        allow : iterable[str] or Dict[str, str], optional
            Words to allow in word segmentation.
            If you pass in a dict, each key is a word to allow
            and its corresponding value is the desired Jyutping romanization.
            Passing in a dict is useful when you use :func:`~pycantonese.parse_text`
            or :func:`~pycantonese.characters_to_jyutping` and want
            to supply your own Jyutping.
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
        if isinstance(allow, dict):
            allow_words = set(allow.keys())
            self._allow_words_to_jp = allow
        else:
            allow_words = set(allow or [])
            self._allow_words_to_jp = None
        self._words |= allow_words or set()
        self._words -= disallow or set()

        # Turn everything from strings to tuples due to alphanumeric chars.
        self._words = {_split_chars_with_alphanum(x) for x in self._words}

    def _predict_sent(self, sent_str):
        chars = _split_chars_with_alphanum(sent_str)
        segmented = super(Segmenter, self)._predict_sent(chars)
        # Turn the result back from tuples to strings.
        segmented = ["".join(x) for x in segmented]
        return segmented


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
    elif type(cls) != Segmenter:
        raise TypeError(f"`segmenter` must be a Segmenter object: {cls}")
    # Strip all whitespace.
    unsegmented = "".join(unsegmented.split())
    segmented = list(cls.predict([unsegmented]))[0]
    return segmented
