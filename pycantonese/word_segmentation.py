from functools import lru_cache

from wordseg import LongestStringMatching

from pycantonese.corpus import hkcancor


@lru_cache(maxsize=1)
def _get_word_segmentation_model():
    corpus = hkcancor()
    model = LongestStringMatching(max_word_length=5)
    model.fit(corpus.sents())
    return model


def segment(sent_str):
    """
    Segment the unsegmented sentence.

    The word segmentation model is the longest string matching approach,
    trained by the HKCanCor corpus included in this library.
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
