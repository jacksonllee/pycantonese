"""This script trains a part-of-speech tagger."""

import logging

from pycantonese import hkcancor
from pycantonese.pos_tagging import POSTagger
from pycantonese.pos_tagging.tagger import _PICKLE_PATH


_TAGGER_PARAMETERS = {
    "frequency_threshold": 10,
    "ambiguity_threshold": 0.9,
    "n_iter": 10,
}


def _get_tagged_sents(corpus):
    return [
        [(word, tag) for word, tag, _, _ in tagged_sent]
        for tagged_sent in corpus.tagged_sents()
    ]


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    tagger = POSTagger(**_TAGGER_PARAMETERS)
    tagger.train(_get_tagged_sents(hkcancor()), save=_PICKLE_PATH)
