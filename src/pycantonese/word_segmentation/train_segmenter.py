"""This script trains a word segmentation model."""

import itertools
import logging

from pycantonese import hkcancor
from pycantonese.data.common_voice import SENTS as COMMON_VOICE_SENTS
from pycantonese.data.ctcpc import SENTS as CTCPC_SENTS
from pycantonese.data.rime_cantonese import CHARS_TO_JYUTPING, PHRASE_FRAGMENTS
from pycantonese.word_segmentation.segmenter import _Segmenter
from pycantonese.word_segmentation.segmenter import _MODEL_PATH
from pycantonese._punctuation_marks import _CHINESE_PUNCT


def _get_segmented_sents(segmenter) -> list[list[str]]:
    """Get PUA-encoded segmented sentences from HKCanCor."""
    result = []
    for utterance in hkcancor().words(by_utterance=True):
        encoded_words = [segmenter._encode(word) for word in utterance]
        result.append(encoded_words)
    return result


def _get_unsegmented_sents(segmenter) -> list[str]:
    """Get PUA-encoded unsegmented sentences for EM refinement."""
    result = []
    chinese_punct = list(_CHINESE_PUNCT)
    data = itertools.chain(CHARS_TO_JYUTPING, COMMON_VOICE_SENTS, PHRASE_FRAGMENTS)
    for i, word in enumerate(data):
        punct = chinese_punct[i % len(chinese_punct)]
        result.append(segmenter._encode(word) + punct)
    # CTCPC data already ends with punctuation marks.
    result.extend([segmenter._encode(word) for word in CTCPC_SENTS])
    return result


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    segmenter = _Segmenter()

    # Phase 1: Supervised fit with HKCanCor + rime-cantonese.
    logging.info("Phase 1: Supervised fit...")
    sents = _get_segmented_sents(segmenter)
    segmenter.fit_segmented(sents)

    # Phase 2: Unsupervised EM refinement.
    logging.info("Phase 2: Unsupervised EM refinement...")
    unseg_sents = _get_unsegmented_sents(segmenter)
    segmenter.fit_unsegmented(unseg_sents)

    segmenter.save(_MODEL_PATH)
    logging.info("Done. Model saved to %s", _MODEL_PATH)
