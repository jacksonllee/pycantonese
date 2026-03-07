from __future__ import annotations

import os
import re
from functools import lru_cache
from itertools import chain

from rustling.seq_feature import seq_obs
from rustling.wordseg import DAGHMMSegmenter

from pycantonese._punctuation_marks import _PUNCTUATION_MARKS
from pycantonese.corpus import hkcancor
from pycantonese.data.rime_cantonese import CHARS_TO_JYUTPING
from pycantonese.util import _NOT_CANTONESE, _split_chars_with_alphanum

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH = os.path.join(_THIS_DIR, "segmenter.fb.zst")

_WHITESPACE_AROUND_ALPHANUM_REGEX = re.compile(r"(?<=[a-z0-9-])\s+|\s+(?=[a-z0-9-])")


class _Segmenter:
    """A word segmentation model.

    .. versionadded:: 3.0.0
    """

    def __init__(self):
        """Initialize a _Segmenter object."""
        # Build word set from all sources (for PUA mapping).
        words = set()
        for utterance in hkcancor().words(by_utterance=True):
            words.update(utterance)
        words |= CHARS_TO_JYUTPING.keys()

        # Build PUA mapping: each unique alphanumeric sequence gets a single
        # Private Use Area character. This makes English words atomic (1 char)
        # so that the segmenter doesn't split English words into
        # individual letters.
        # Use sorted() for deterministic PUA assignments across
        # training and inference.
        self._alphanum_to_pua = {}
        self._pua_to_alphanum = {}
        for word in sorted(words):
            for token in _split_chars_with_alphanum(word):
                if token[0] in _NOT_CANTONESE and token not in self._alphanum_to_pua:
                    pua = chr(0xE000 + len(self._alphanum_to_pua))
                    self._alphanum_to_pua[token] = pua
                    self._pua_to_alphanum[pua] = token

        self._model = DAGHMMSegmenter(
            n_iter=2,
            gamma=0.5,
            tolerance=0.1,
            random_seed=42,
            features=[
                # Unigrams
                seq_obs(-1),
                seq_obs(0),
                seq_obs(1),
                # Bigrams
                seq_obs(-1, 0),
                seq_obs(0, 1),
                # Skip bigrams
                seq_obs(-1, 1),
            ],
        )

    def _encode(self, text):
        """Replace alphanumeric sequences with PUA characters."""
        tokens = _split_chars_with_alphanum(text)
        result = []
        for t in tokens:
            if t[0] in _NOT_CANTONESE:
                if t not in self._alphanum_to_pua:
                    pua = chr(0xE000 + len(self._alphanum_to_pua))
                    self._alphanum_to_pua[t] = pua
                    self._pua_to_alphanum[pua] = t
                result.append(self._alphanum_to_pua[t])
            else:
                result.append(t)
        return "".join(result)

    def _decode(self, text):
        """Replace PUA characters back with original alphanumeric sequences."""
        return "".join(self._pua_to_alphanum.get(c, c) for c in text)

    def predict(self, sents):
        """Segment sentences."""
        encoded = [self._encode(s) for s in sents]
        results = self._model.predict(encoded)
        for sent in results:
            yield [self._decode(word) for word in sent]

    def fit(self, sents: list[list[str]]):
        """Train the model.

        Parameters
        ----------
        sents : list[list[str]]
            A list of segmented sentences for training.
        """
        self._model.fit_segmented(sents)

    def fit_unsegmented(self, sent_strs: list[str]):
        """Refine the model with unsupervised EM on unsegmented sentences.

        Parameters
        ----------
        sent_strs : list[str]
            A list of unsegmented sentence strings.
        """
        encoded = [self._encode(s) for s in sent_strs]
        self._model.fit_unsegmented(encoded)

    def save(self, path):
        """Save the model and PUA mapping as a single gzip-compressed JSON.

        Parameters
        ----------
        path : str
            The path to save the combined data.
        """
        self._model.save(path, self._alphanum_to_pua)

    def load(self, path):
        """Load a model and PUA mapping from a gzip-compressed JSON.

        Parameters
        ----------
        path : str
            The path where the combined data is located.
        """
        self._alphanum_to_pua = self._model.load(path)
        self._pua_to_alphanum = {v: k for k, v in self._alphanum_to_pua.items()}


@lru_cache(maxsize=1)
def _get_default_segmenter():
    # Bypass the expensive __init__ corpus iteration — the PUA mapping is
    # embedded in the saved model file and returned by load().
    segmenter = object.__new__(_Segmenter)
    segmenter._alphanum_to_pua = {}
    segmenter._pua_to_alphanum = {}
    segmenter._model = DAGHMMSegmenter(
        n_iter=2,
        gamma=0.5,
        tolerance=0.1,
        random_seed=42,
        features=[
            seq_obs(-1),
            seq_obs(0),
            seq_obs(1),
            seq_obs(-1, 0),
            seq_obs(0, 1),
            seq_obs(-1, 1),
        ],
    )
    segmenter.load(_MODEL_PATH)
    return segmenter


def _split_punct(word):
    """Split leading/trailing punctuation off a word.

    For example, "dinner？" becomes ["dinner", "？"], and "學？" becomes
    ["學", "？"], but "呃like" stays as ["呃like"] because "呃" is not
    punctuation.
    """
    if len(word) <= 1:
        return [word]
    # Strip leading punctuation.
    i = 0
    while i < len(word) and word[i] in _PUNCTUATION_MARKS:
        i += 1
    # Strip trailing punctuation.
    j = len(word)
    while j > i and word[j - 1] in _PUNCTUATION_MARKS:
        j -= 1
    result = list(word[:i])
    if i < j:
        result.append(word[i:j])
    result.extend(word[j:])
    return result


def segment(unsegmented: str) -> list[str]:
    """Segment the unsegmented input.

    The word segmentation model is a Jieba-styled DAG+HMM hybrid segmenter,
    trained by HKCanCor, rime-cantonese, Common Voice Cantonese,
    and Cantonese-Traditional Chinese Parallel Corpus.

    Parameters
    ----------
    unsegmented : str
        Unsegmented input.

    Returns
    -------
    list[str]

    Examples
    --------
    >>> segment("廣東話容唔容易學？")  # "Is Cantonese easy to learn?"
    ['廣東話', '容', '唔', '容', '易', '學', '？']
    """
    if not unsegmented:
        return []
    segmenter = _get_default_segmenter()
    parts_to_segment = map(
        lambda x: x.replace(" ", ""),
        _WHITESPACE_AROUND_ALPHANUM_REGEX.split(unsegmented.strip()),
    )
    words = chain.from_iterable(
        map(lambda x: next(segmenter.predict([x])), parts_to_segment)
    )
    return list(chain.from_iterable(map(_split_punct, words)))
