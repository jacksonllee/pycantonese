from __future__ import annotations

import os
import re
from functools import lru_cache
from itertools import chain
from typing import Literal, overload, Sequence

from rustling.seq_feature import seq_obs
from rustling.wordseg import DAGHMMSegmenter

from pycantonese._punctuation_marks import _PUNCTUATION_MARKS
from pycantonese.corpus import hkcancor
from pycantonese.data.rime_cantonese import CHARS_TO_JYUTPING
from pycantonese.util import _NOT_CANTONESE, _split_chars_with_alphanum

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH = os.path.join(_THIS_DIR, "segmenter.fb.zst")

_WHITESPACE_AROUND_ALPHANUM_REGEX = re.compile(r"(?<=[a-z0-9-])\s+|\s+(?=[a-z0-9-])")


class _Segmenter(DAGHMMSegmenter):
    """A word segmentation model.

    .. versionadded:: 3.0.0
    """

    _DEFAULT_FEATURES = [
        # Unigrams
        seq_obs(-1),
        seq_obs(0),
        seq_obs(1),
        # Bigrams
        seq_obs(-1, 0),
        seq_obs(0, 1),
        # Skip bigrams
        seq_obs(-1, 1),
    ]

    def __new__(cls):
        return super().__new__(
            cls,
            n_iter=2,
            gamma=0.5,
            tolerance=0.1,
            random_seed=42,
            features=cls._DEFAULT_FEATURES,
        )

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
        results = super().predict(encoded)
        for sent in results:
            yield [self._decode(word) for word in sent]

    def fit_unsegmented(self, sent_strs: Sequence[str]):
        """Refine the model with unsupervised EM on unsegmented sentences.

        Args:
            sent_strs (list[str]): A list of unsegmented sentence strings.
        """
        encoded = [self._encode(s) for s in sent_strs]
        super().fit_unsegmented(encoded)

    def save(self, path):
        """Save the model and PUA mapping as a single gzip-compressed JSON.

        Args:
            path (str): The path to save the combined data.
        """
        super().save(path, self._alphanum_to_pua)

    def load(self, path):
        """Load a model and PUA mapping from a gzip-compressed JSON.

        Args:
            path (str): The path where the combined data is located.
        """
        self._alphanum_to_pua = super().load(path)
        self._pua_to_alphanum = {v: k for k, v in self._alphanum_to_pua.items()}


@lru_cache(maxsize=1)
def _get_default_segmenter():
    # Call __new__ to create the Rust DAGHMMSegmenter base object,
    # but skip __init__ (PUA mapping comes from load(), avoiding
    # the expensive hkcancor corpus iteration).
    segmenter = _Segmenter.__new__(_Segmenter)
    segmenter._alphanum_to_pua = {}
    segmenter._pua_to_alphanum = {}
    segmenter.load(_MODEL_PATH)
    return segmenter


def _split_script_boundary(word):
    """Split a word at English-CJK boundaries, preserving known mixed words.

    For example, "course超" becomes ["course", "超"], but "IQ題" stays as
    ["IQ題"] because it is a known word in CHARS_TO_JYUTPING.
    """
    if len(word) <= 1 or word in CHARS_TO_JYUTPING:
        return [word]
    result = []
    current = word[0]
    for ch in word[1:]:
        if (current[-1] in _NOT_CANTONESE) != (ch in _NOT_CANTONESE):
            result.append(current)
            current = ch
        else:
            current += ch
    result.append(current)
    return result


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


def _segment_with_offsets(
    unsegmented: str,
) -> list[tuple[str, tuple[int, int]]]:
    """Segment and return words with character offsets into the original string."""
    if not unsegmented:
        return []
    segmenter = _get_default_segmenter()
    stripped = unsegmented.strip()
    strip_offset = unsegmented.index(stripped[0]) if stripped else 0
    result: list[tuple[str, tuple[int, int]]] = []
    # Split by whitespace around alphanumeric tokens, tracking spans.
    pos = 0
    parts: list[tuple[str, int]] = []
    for m in _WHITESPACE_AROUND_ALPHANUM_REGEX.finditer(stripped):
        if m.start() > pos:
            parts.append((stripped[pos : m.start()], strip_offset + pos))
        pos = m.end()
    if pos < len(stripped):
        parts.append((stripped[pos:], strip_offset + pos))
    if not parts and stripped:
        parts.append((stripped, strip_offset))
    for part, part_start in parts:
        # Remove spaces within each part, tracking original char positions.
        chars = []
        char_positions = []
        for i, ch in enumerate(part):
            if ch != " ":
                chars.append(ch)
                char_positions.append(part_start + i)
        if not chars:
            continue
        compact = "".join(chars)
        segmented = next(segmenter.predict([compact]))
        seg_offset = 0
        for word in segmented:
            for sub_word in chain.from_iterable(
                map(_split_script_boundary, _split_punct(word))
            ):
                word_len = len(sub_word)
                start_pos = char_positions[seg_offset]
                end_pos = char_positions[seg_offset + word_len - 1] + 1
                result.append((sub_word, (start_pos, end_pos)))
                seg_offset += word_len
    return result


@overload
def segment(unsegmented: str, *, offsets: Literal[False] = False) -> list[str]: ...


@overload
def segment(
    unsegmented: str, *, offsets: Literal[True]
) -> list[tuple[str, tuple[int, int]]]: ...


def segment(
    unsegmented: str, *, offsets: bool = False
) -> list[str] | list[tuple[str, tuple[int, int]]]:
    """Segment the unsegmented input.

    The word segmentation model is a Jieba-styled DAG+HMM hybrid segmenter,
    trained by HKCanCor, rime-cantonese, Common Voice Cantonese,
    and Cantonese-Traditional Chinese Parallel Corpus.

    Args:
        unsegmented (str): Unsegmented input.
        offsets (bool, optional): If True, return each word as a
            ``(word, (start, end))`` tuple where *start* and *end* are
            character offsets into the original *unsegmented* string
            (exclusive end, like Python slices). Defaults to False.

    Returns:
        list[str] or list[tuple[str, tuple[int, int]]]

    Examples:
        >>> segment("廣東話容唔容易學？")  # "Is Cantonese easy to learn?"
        ['廣東話', '容', '唔', '容易', '學', '？']
        >>> segment("廣東話容唔容易學？", offsets=True)
        [('廣東話', (0, 3)), ('容', (3, 4)), ('唔', (4, 5)),
         ('容易', (5, 7)), ('學', (7, 8)), ('？', (8, 9))]
    """
    if offsets:
        return _segment_with_offsets(unsegmented)
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
    return list(
        chain.from_iterable(
            map(
                _split_script_boundary,
                chain.from_iterable(map(_split_punct, words)),
            )
        )
    )
