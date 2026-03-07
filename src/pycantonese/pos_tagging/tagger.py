import functools
import os

from rustling.perceptron_pos_tagger import AveragedPerceptron

from pycantonese._punctuation_marks import _PUNCTUATION_MARKS
from pycantonese.pos_tagging.hkcancor_to_ud import hkcancor_to_ud

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH = os.path.join(_THIS_DIR, "tagger.fb.zst")


class _POSTagger:
    """A part-of-speech tagger.

    This class wraps ``rustling.perceptron_pos_tagger.AveragedPerceptron``
    and provides Cantonese-specific functionality such as
    Chinese full-width punctuation handling.
    """

    def __init__(
        self,
        *,
        frequency_threshold=10,
        ambiguity_threshold=0.95,
        n_iter=5,
        random_seed=None,
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
        random_seed : int | None, optional
            Random seed for reproducible training. If None, a random seed
            is used.
        """
        self._tagger = AveragedPerceptron(
            frequency_threshold=frequency_threshold,
            ambiguity_threshold=ambiguity_threshold,
            n_iter=n_iter,
            random_seed=random_seed,
        )
        # HKCanCor doesn't have the Chinese full-width punctuation marks,
        # so they must be handled outside of the rustling tagger.
        self._punctuation_tags = {punct: punct for punct in _PUNCTUATION_MARKS}

    def predict(self, sequences):
        """Predict the tags for the sequences.

        Parameters
        ----------
        sequences : list[list[str]]
            A list of segmented sentences, where each sentence is a list
            of words in Cantonese characters.

        Returns
        -------
        list[list[str]]
            The list of predicted tag sequences.
        """
        tags = self._tagger.predict(sequences)
        for seq_tags, seq_words in zip(tags, sequences):
            for i, word in enumerate(seq_words):
                if word in self._punctuation_tags:
                    seq_tags[i] = self._punctuation_tags[word]
        return tags

    def fit(self, sequences, tags):
        """Train a model.

        Parameters
        ----------
        sequences : list[list[str]]
            A list of segmented sentences for training.
        tags : list[list[str]]
            A list of tag sequences, parallel to ``sequences``.
        """
        self._tagger.fit(sequences, tags)

    def save(self, path):
        """Save the model as a binary model file.

        Parameters
        ----------
        path : str
            The path to save the model.
        """
        self._tagger.save(path)

    def load(self, path):
        """Load a model from a binary model file.

        Parameters
        ----------
        path : str
            The path where the binary model file is located.
        """
        self._tagger.load(path)


@functools.lru_cache(maxsize=1)
def _get_tagger():
    tagger = _POSTagger()
    tagger.load(_MODEL_PATH)
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
          https://github.com/fcbond/hkcancor.
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
    [('我', 'r'), ('噚日', 't'), ('買', 'v'), ('嗰', 'r'), ('對', 'q'), ('鞋', 'n'), ('。', '。')]
    """  # noqa: E501
    if isinstance(words, str):
        raise TypeError(
            f"Input must be a list of segmented words, not a string: {words}"
        )
    tags = _get_tagger().predict([words])[0]
    if tagset == "universal":
        tags = [hkcancor_to_ud(tag) for tag in tags]
    elif tagset != "hkcancor":
        raise ValueError(f"tagset must be one of {{'universal', 'hkcancor'}}: {tagset}")
    return list(zip(words, tags))
