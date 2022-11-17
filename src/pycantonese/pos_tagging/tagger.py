import collections
import functools
import json
import logging
import os
import random

from typing import Dict, Iterable, List, Hashable

import numpy

from pycantonese._punctuation_marks import _PUNCTUATION_MARKS
from pycantonese.pos_tagging.hkcancor_to_ud import hkcancor_to_ud


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_JSON_PATH = os.path.join(_THIS_DIR, "tagger.json")

# Features prefixes.
_F_BIAS = "bias"
_F_CUR_WORD_FIRST_CHAR = "i word's first char"
_F_CUR_WORD_FINAL_CHAR = "i word's final char"
_F_PREV_WORD_FIRST_CHAR = "i-1 word's first char"
_F_PREV_WORD_FINAL_CHAR = "i-1 word's final char"
_F_PREV_TAG = "i-1 tag"
_F_PREV2_WORD_FIRST_CHAR = "i-2 word's first char"
_F_PREV2_WORD_FINAL_CHAR = "i-2 word's final char"
_F_PREV2_TAG = "i-2 tag"
_F_NEXT_WORD_FIRST_CHAR = "i+1 word's first char"
_F_NEXT_WORD_FINAL_CHAR = "i+1 word's final char"
_F_NEXT2_WORD_FIRST_CHAR = "i+2 word's first char"
_F_NEXT2_WORD_FINAL_CHAR = "i+2 word's final char"


class _AveragedPerceptron:
    """An averaged perceptron.

    This is a modified version based on the textblob-aptagger codebase
    (MIT license), with original implementation by Matthew Honnibal:
    https://github.com/sloria/textblob-aptagger/blob/266fa1c22daaff7c60577efa8577f1b6ce2f7f70/textblob_aptagger/_perceptron.py
    """

    def __init__(self):
        self.classes: List[str] = []
        self.features: List[Hashable] = []
        # Maps class/label into row index of the weights matrix.
        self._class_to_index: Dict[str, int] = {}
        # Maps feature into column index of the weights matrix.
        self._feature_to_index: Dict[Hashable, int] = {}
        # Matrix represented by 2D array of shape (n_classes, n_features).
        self._weights = numpy.zeros(1)

        # The following attributes are only used for trainning

        # The accumulated values, for the averaging. Has same shape as _weights.
        self._totals = numpy.zeros(1)
        # The last iteration the feature was changed, for the averaging.
        # Has same shape as _weights.
        # (tstamps is short for timestamps)
        self._tstamps = numpy.zeros(1)
        # Number of instances seen
        self.i = 0

    def rescope(self, features: Iterable[Hashable], classes: Iterable[str]):
        """ "Change the features and classes.

        Assume they won't change until next call.
        """
        self.features = list(features)
        self.classes = sorted(classes)
        self._weights = numpy.zeros(
            (len(self.classes), len(self.features)), dtype=numpy.float64
        )
        self._totals = self._weights.copy()
        self._tstamps = numpy.zeros(self._weights.shape, dtype=numpy.int32)
        self._feature_to_index = {f: i for i, f in enumerate(self.features)}
        self._class_to_index = {c: i for i, c in enumerate(self.classes)}

    def predict(self, features: Dict[Hashable, float]):
        """Return the best label for the given features.

        It's computed based on the dot-product between the features and
        current weights.
        """
        fs, vs = zip(*(i for i in features.items() if i[0] in self._feature_to_index))
        # The feature values vector.
        fvec = numpy.array(vs)
        weights = self._weights[:, [self._feature_to_index[f] for f in fs]]
        return self.classes[weights.dot(fvec).argmax()]

    def update(self, truth: str, guess: str, features: Iterable[Hashable]):
        """Update the feature weights."""

        def upd_feat(ci: int, fi: int, v: float):
            w = self._weights[ci, fi]
            self._totals[ci, fi] += (self.i - self._tstamps[ci, fi]) * w
            self._tstamps[ci, fi] = self.i
            self._weights[ci, fi] += v

        self.i += 1
        if truth == guess:
            return None
        truth_i = self._class_to_index[truth]
        guess_i = self._class_to_index[guess]
        for f in features:
            fi = self._feature_to_index[f]
            upd_feat(truth_i, fi, 1.0)
            upd_feat(guess_i, fi, -1.0)

    def average_weights(self):
        """Average weights from all iterations."""
        for fi, weights in enumerate(self._weights.T):
            total = self._totals[:, fi] + (self.i - self._tstamps[:, fi]) * weights
            self._weights[:, fi] = numpy.round(total / self.i, 3)


class POSTagger:
    """A part-of-speech tagger.

    This is a modified version based on the textblob-aptagger codebase
    (MIT license), with original implementation by Matthew Honnibal:
    https://github.com/sloria/textblob-aptagger/blob/266fa1c22daaff7c60577efa8577f1b6ce2f7f70/textblob_aptagger/taggers.py
    """

    START = ["-START-", "-START2-"]
    END = ["-END-", "-END2-"]

    def __init__(self, *, frequency_threshold=10, ambiguity_threshold=0.95, n_iter=5):
        """Initialize a part-of-speech tagger.

        Parameters
        ----------
        frequency_threshold : int, optional
            A good number of words are almost unambiguously associated with
            a given tag. If these words have a frequency of occurrence above
            this threshold in the training data, they are directly associated
            with their tag in the model.
        ambiguity_threshold : float, optional
            A good number of words are almost unambiguously associated with
            a given tag. If the ratio of (# of occurrences of this word with
            this tag) / (# of occurrences of this word) in the training data
            is equal to or greater than this threshold, then this word is
            directly associated with the tag in the model.
        n_iter : int, optional
            Number of times the training phase iterates through the data.
            At each new iteration, the data is randomly shuffled.
        """
        self.frequency_threshold = frequency_threshold
        self.ambiguity_threshold = ambiguity_threshold
        self.n_iter = n_iter

        self.model = _AveragedPerceptron()
        self.tagdict = {}
        self.classes = set()
        self.features = set()

        # HKCanCor doesn't have the Chinese full-width punctuation marks.
        self.tagdict.update({punct: punct for punct in _PUNCTUATION_MARKS})

    def tag(self, words):
        """Tag the words.

        Parameters
        ----------
        words : list[str]
            A segmented sentence or phrase, where each word is Cantonese
            characters.

        Returns
        -------
        list[str]
            The list of predicted tags.
        """
        tags = []
        if not words:
            return tags
        prev2, prev = self.START
        context = self.START + words + self.END
        for i, word in enumerate(words):
            tag = self.tagdict.get(word)
            if not tag:
                features = self._get_features(i, word, context, prev, prev2)
                tag = self.model.predict(features)
            tags.append(tag)
            prev2 = prev
            prev = tag
        return tags

    def train(self, tagged_sents, save=None):
        """Train a model.

        Parameters
        ----------
        tagged_sents : list[list[tuple[str, str]]]
            A list of segmented and tagged sentences for training.
        save : str, optional
            If given, save the trained model as a JSON file at this path.
        """
        self._make_tagdict(tagged_sents)
        model = self.model
        model.rescope(self.features, self.classes)

        for iter_ in range(self.n_iter):
            c = 0
            n = 0
            for tagged_sent in tagged_sents:
                prev2, prev = self.START
                context = self.START + [w for w, _ in tagged_sent] + self.END
                for i, (word, tag) in enumerate(tagged_sent):
                    try:
                        guess = self.tagdict[word]
                    except KeyError:
                        feats = self._get_features(i, word, context, prev, prev2)
                        guess = model.predict(feats)
                        model.update(tag, guess, feats)
                    prev2, prev = prev, guess
                    c += guess == tag
                    n += 1
            random.shuffle(tagged_sents)
            logging.info("Iter %d: %d / %d = %f", iter_, c, n, c / n)
        model.average_weights()

        if save is not None:
            json.dump(
                {
                    "weights": model._weights,
                    "tagdict": self.tagdict,
                    "classes": model.classes,
                    "features": model.features,
                },
                open(save, "w", encoding="utf-8"),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )

    def load(self, path):
        """Load a model from a JSON file.

        Parameters
        ----------
        path : str
            The path where the model, stored as a JSON file, is located.
        """
        try:
            data = json.load(open(path, "r", encoding="utf-8"))
        except IOError:
            raise FileNotFoundError(f"Can't locate tagger model {path}")
        except:  # noqa
            raise EnvironmentError(
                f"A file is detected at {path}, but it cannot be read as a "
                "a tagger model. "
                "The tagger model JSON file may be corrupted for some reason."
            )
        self.tagdict = data['tagdict']
        weights = data['weights']
        classes = data['classes']
        features = data['features']
        self.classes = set(classes)
        self.features = set(features)
        self.model.rescope(features, classes)
        self.model._weights = weights
        self.model._totals = None
        self.model._tstamps = None

    def _get_features(self, i, word, context: List[str], prev, prev2):
        """Map tokens into a feature representation, implemented as a
        {hashable: float} dict. If the features change, a new model must be
        trained.
        """

        def add(name, *args):
            features[" ".join((name,) + tuple(args))] += 1

        i += len(self.START)
        features = collections.defaultdict(int)

        # It's useful to have a constant feature,
        # which acts sort of like a prior.
        add(_F_BIAS)

        add(_F_CUR_WORD_FIRST_CHAR, word[0])
        add(_F_CUR_WORD_FINAL_CHAR, word[-1])

        add(_F_PREV_WORD_FIRST_CHAR, context[i - 1][0])
        add(_F_PREV_WORD_FINAL_CHAR, context[i - 1][-1])
        add(_F_PREV_TAG, prev)

        add(_F_PREV2_WORD_FIRST_CHAR, context[i - 2][0])
        add(_F_PREV2_WORD_FINAL_CHAR, context[i - 2][-1])
        add(_F_PREV2_TAG, prev2)

        add(_F_NEXT_WORD_FIRST_CHAR, context[i + 1][0])
        add(_F_NEXT_WORD_FINAL_CHAR, context[i + 1][-1])

        # Prev impl has copy-paste error.
        add(_F_NEXT2_WORD_FIRST_CHAR, context[i + 2][0])
        add(_F_NEXT2_WORD_FINAL_CHAR, context[i + 2][-1])

        return features

    def _make_tagdict(self, tagged_sents):
        """Make a tag dictionary for single-tag words."""
        counts = collections.defaultdict(lambda: collections.defaultdict(int))
        for tagged_sent in tagged_sents:
            for word, tag in tagged_sent:
                counts[word][tag] += 1
                self.classes.add(tag)
        words = set()
        for word, tag_freqs in counts.items():
            words.add(word)
            tag, mode = max(tag_freqs.items(), key=lambda item: item[1])
            n = sum(tag_freqs.values())
            above_freq_threshold = n >= self.frequency_threshold
            unambiguous = (mode / n) >= self.ambiguity_threshold
            if above_freq_threshold and unambiguous:
                self.tagdict[word] = tag

        self.features.add(_F_BIAS)
        for word in words | set(self.START) | set(self.END):
            self.features.add(f"{_F_CUR_WORD_FIRST_CHAR} {word[0]}")
            self.features.add(f"{_F_CUR_WORD_FINAL_CHAR} {word[-1]}")
            self.features.add(f"{_F_PREV_WORD_FIRST_CHAR} {word[0]}")
            self.features.add(f"{_F_PREV_WORD_FINAL_CHAR} {word[-1]}")
            self.features.add(f"{_F_PREV2_WORD_FIRST_CHAR} {word[0]}")
            self.features.add(f"{_F_PREV2_WORD_FINAL_CHAR} {word[-1]}")
            self.features.add(f"{_F_NEXT_WORD_FIRST_CHAR} {word[0]}")
            self.features.add(f"{_F_NEXT_WORD_FINAL_CHAR} {word[-1]}")
            self.features.add(f"{_F_NEXT2_WORD_FIRST_CHAR} {word[0]}")
            self.features.add(f"{_F_NEXT2_WORD_FINAL_CHAR} {word[-1]}")
        for tag in self.classes:
            for prefix in (_F_PREV2_TAG, _F_PREV_TAG):
                self.features.add(f"{prefix} {tag}")
        self.features.add(f"{_F_PREV2_TAG} {self.START[0]}")
        self.features.add(f"{_F_PREV_TAG} {self.START[1]}")
        self.features.add(f"{_F_PREV2_TAG} {self.START[1]}")

        logging.info("%d unique words in the training data", len(words))
        logging.info("%d tags in this tagset", len(self.classes))
        logging.info("%d features populated for the training data", len(self.features))
        logging.info("%d words are treated as having a unique tag", len(self.tagdict))


@functools.lru_cache(maxsize=1)
def _get_tagger():
    tagger = POSTagger()
    tagger.load(_JSON_PATH)
    return tagger


def pos_tag(words, tagset="universal"):
    """Tag the words for their parts of speech.

    The part-of-speech tagger uses an averaged perceptron model,
    and is trained by the HKCanCor data.

    .. versionadded:: 3.1.0

    Parameters
    ----------
    words : list[str]
        A segmented sentence or phrase, where each word is a string of
        Cantonese characters.
    tagset : str, {"universal", "hkcancor"}
        The part-of-speech tagset that the returned tags are in.
        Supported options:

        * ``"hkcancor"``, for the tagset used by the original HKCanCor data.
          There are over 100 tags, 46 of which are described at
          http://compling.hss.ntu.edu.sg/hkcancor/.
        * ``"universal"`` (default option), for the Universal Dependencies v2
          tagset. There are 17 tags; see
          https://universaldependencies.org/u/pos/index.html.
          Internally, this option applies
          :func:`~pycantonese.pos_tagging.hkcancor_to_ud` to convert HKCanCor
          tags to UD tags.

    Returns
    -------
    list[tuple[str, str]]
        The segmented sentence/phrase where each word is paired with its
        predicted POS tag.

    Raises
    ------
    TypeError
        If the input is a string (e.g., an unsegmented string of Cantonese).
    ValueError
        If the ``tagset`` argument is not one of the allowed options from
        ``{"universal", "hkcancor"}``.

    Examples
    --------
    >>> words = ['我', '噚日', '買', '嗰', '對', '鞋', '。']  # I bought that pair of shoes yesterday.
    >>> pos_tag(words)
    [('我', 'PRON'), ('噚日', 'ADV'), ('買', 'VERB'), ('嗰', 'PRON'), ('對', 'NOUN'), ('鞋', 'NOUN'), ('。', 'PUNCT')]
    >>> pos_tag(words, tagset="hkcancor")
    [('我', 'R'), ('噚日', 'T'), ('買', 'V'), ('嗰', 'R'), ('對', 'Q'), ('鞋', 'N'), ('。', '。')]
    """  # noqa: E501
    if type(words) == str:
        raise TypeError(
            f"Input must be a list of segmented words, not a string: {words}"
        )
    tags = _get_tagger().tag(words)
    if tagset == "universal":
        tags = [hkcancor_to_ud(tag) for tag in tags]
    elif tagset != "hkcancor":
        raise ValueError(f"tagset must be one of {{'universal', 'hkcancor'}}: {tagset}")
    return list(zip(words, tags))
