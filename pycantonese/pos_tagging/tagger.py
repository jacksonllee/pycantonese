import collections
import functools
import logging
import os
import pickle
import random

from typing import Dict


# Use the highest pickle protocol version that's compatible for all supported
# Python versions.
# Protocol version 4 was added in Python 3.4.
# Protocol version 5 was added in Python 3.8.
# Reference: https://docs.python.org/3/library/pickle.html#data-stream-format
_PICKLE_PROTOCOL = 4

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PICKLE_PATH = os.path.join(_THIS_DIR, "tagger.pickle")

# Reference: https://en.wikipedia.org/wiki/Chinese_punctuation
_PUNCTUATIONS = """
，
。
！
？
；
：
（
）
「
」
［
］
【
】
《
》
〈
〉
、
‧
…
—
～
""".strip().strip(
    "\n"
)


class _AveragedPerceptron:
    """An averaged perceptron.

    This is a modified version based on the textblob-aptagger codebase
    (MIT license), with original implementation by Matthew Honnibal:
    https://github.com/sloria/textblob-aptagger/blob/266fa1c22daaff7c60577efa8577f1b6ce2f7f70/textblob_aptagger/_perceptron.py
    """

    def __init__(self):
        # Each feature (key) gets its own weight vector (value).
        self.weights: Dict[str, Dict[str, float]] = {}
        self.classes = set()
        # The accumulated values, for the averaging. These will be keyed by
        # feature/class tuples
        self._totals = collections.defaultdict(int)
        # The last time the feature was changed, for the averaging. Also
        # keyed by feature/class tuples
        # (tstamps is short for timestamps)
        self._tstamps = collections.defaultdict(int)
        # Number of instances seen
        self.i = 0

    def predict(self, features):
        """Return the best label for the given features.

        It's computed based on the dot-product between the features and
        current weights.
        """
        scores = collections.defaultdict(float)
        for feat, value in features.items():
            if feat not in self.weights or value == 0:
                continue
            weights = self.weights[feat]
            for label, weight in weights.items():
                scores[label] += value * weight
        # Do a secondary alphabetic sort, for stability
        return max(self.classes, key=lambda label: (scores[label], label))

    def update(self, truth, guess, features):
        """Update the feature weights."""

        def upd_feat(c, f, w, v):
            param = (f, c)
            self._totals[param] += (self.i - self._tstamps[param]) * w
            self._tstamps[param] = self.i
            self.weights[f][c] = w + v

        self.i += 1
        if truth == guess:
            return None
        for f in features:
            weights = self.weights.setdefault(f, {})
            upd_feat(truth, f, weights.get(truth, 0.0), 1.0)
            upd_feat(guess, f, weights.get(guess, 0.0), -1.0)

    def average_weights(self):
        """Average weights from all iterations."""
        for feat, weights in self.weights.items():
            new_feat_weights = {}
            for clas, weight in weights.items():
                param = (feat, clas)
                total = self._totals[param]
                total += (self.i - self._tstamps[param]) * weight
                averaged = round(total / float(self.i), 3)
                if averaged:
                    new_feat_weights[clas] = averaged
            self.weights[feat] = new_feat_weights


class POSTagger:
    """A part-of-speech tagger.

    This is a modified version based on the textblob-aptagger codebase
    (MIT license), with original implementation by Matthew Honnibal:
    https://github.com/sloria/textblob-aptagger/blob/266fa1c22daaff7c60577efa8577f1b6ce2f7f70/textblob_aptagger/taggers.py
    """

    START = ["-START-", "-START2-"]
    END = ["-END-", "-END2-"]

    def __init__(
        self, *, frequency_threshold=10, ambiguity_threshold=0.95, n_iter=5
    ):
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

        # HKCanCor doesn't have the Chinese full-width punctuation marks.
        self.tagdict.update({punct: "PUNCT" for punct in _PUNCTUATIONS})

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
        prev, prev2 = self.START
        tags = []
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
            If given, save the trained model as a pickle at this path.
        """
        self._make_tagdict(tagged_sents)
        self.model.classes = self.classes

        prev, prev2 = self.START
        for iter_ in range(self.n_iter):
            c = 0
            n = 0
            for tagged_sent in tagged_sents:
                context = self.START + [w for w, _ in tagged_sent] + self.END
                for i, (word, tag) in enumerate(tagged_sent):
                    try:
                        guess = self.tagdict[word]
                    except KeyError:
                        feats = self._get_features(
                            i, word, context, prev, prev2
                        )
                        guess = self.model.predict(feats)
                        self.model.update(tag, guess, feats)
                    prev2 = prev
                    prev = guess
                    c += guess == tag
                    n += 1
            random.shuffle(tagged_sents)
            logging.info("Iter %d: %d / %d = %f", iter_, c, n, c / n)
        self.model.average_weights()

        if save is not None:
            pickle.dump(
                (self.model.weights, self.tagdict, self.classes),
                open(save, "wb"),
                protocol=_PICKLE_PROTOCOL,
            )

    def load(self, path):
        """Load a pickled model.

        Parameters
        ----------
        path : str
            The path where the pickled model is located.
        """
        try:
            w_td_c = pickle.load(open(path, "rb"))
        except IOError:
            raise FileNotFoundError(f"Can't locate tagger model {path}")
        except:  # noqa
            raise EnvironmentError(
                f"A file is detected at {path}, but it cannot be read as a "
                "a tagger model. The likely cause is that you do not have "
                "Git LFS installed on your system -- please install it "
                "(https://git-lfs.github.com/) and re-install pycantonese "
                "with this command: "
                "pip install git+https://github.com/jacksonllee/pycantonese.git@master#egg=pycantonese"  # noqa: E501
            )
        self.model.weights, self.tagdict, self.classes = w_td_c
        self.model.classes = self.classes

    def _get_features(self, i, word, context, prev, prev2):
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
        add("bias")

        add("i word's first char", word[0])
        add("i word's final char", word[-1])

        add("i-1 word's first char", context[i - 1][0])
        add("i-1 word's final char", context[i - 1][-1])
        add("i-1 tag", prev)

        add("i-2 word's first char", context[i - 2][0])
        add("i-2 word's final char", context[i - 2][-1])
        add("i-2 tag", prev2)

        add("i+1 word's first char", context[i + 1][0])
        add("i+1 word's final char", context[i + 1][-1])

        add("i+2 word's first char", context[i - 2][0])
        add("i+2 word's final char", context[i - 2][-1])

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
        logging.info("%d unique words in the training data", len(words))
        logging.info("%d tags in this tagset", len(self.classes))
        logging.info(
            "%d words are treated as having a unique tag", len(self.tagdict)
        )


@functools.lru_cache(maxsize=1)
def _get_tagger():
    tagger = POSTagger()
    tagger.load(_PICKLE_PATH)
    return tagger


# TODO: Write tests.
def pos_tag(words):
    """Tag the words for their parts of speech.

    The part-of-speech tagger is trained by the HKCanCor data.
    While HKCanCor uses a part-of-speech tagset of over 100 tags (46 of which
    are described at http://compling.hss.ntu.edu.sg/hkcancor/),
    these tags have been mapped to the much smaller Universal Dependencies v2
    tagset of 17 tags (https://universaldependencies.org/u/pos/index.html)
    for training this POS tagger.

    .. versionadded:: 3.1.0

    .. warning::
        As of November 2020, PyCantonese v3.1.0 hasn't been released yet.
        The availability and behavior of this function are subject to change
        in the upcoming release.

    Parameters
    ----------
    words : list[str]
        A segmented sentence or phrase, where each word is a string of
        Cantonese characters.

    Returns
    -------
    list[tuple[str, str]]
        The segmented sentence/phrase where each word is paired with its
        predicted POS tag.

    Raises
    ------
    TypeError
        If the input is a string (e.g., an unsegmented string of Cantonese).

    Examples
    --------
    >>> words = ['我', '噚日', '買', '嗰', '對', '鞋', '。']
    >>> pos_tag(words)  # I bought those shoes yesterday.
    [('我', 'PRON'), ('噚日', 'ADV'), ('買', 'VERB'), ('嗰', 'PRON'), ('對', 'ADP'), ('鞋', 'NOUN'), ('。', 'PUNCT')]
    """  # noqa: E501
    if type(words) == str:
        raise TypeError(
            f"Input must be a list of segmented words, not a string: {words}"
        )
    tags = _get_tagger().tag(words)
    return list(zip(words, tags))
