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

# Several POS tags in HKCanCor are odd ones for proper nouns.
_FIX_HKCANCOR_TAGS = {
    "AIRWAYS0": "XNT",
    "AND": "XNZ",  # In "Chilli and Pepper"
    "BEAN0": "XNZ",  # In one instance of "Mr Bean"
    "CENTRE0": "XNT",  # In one instance of "career centre"
    "ECHO0": "XNT",  # In one instance of "Big Echo"
    "HILL0": "XNZ",  # In "Benny Hill"
    "KONG": "XJNT",  # In "Hong Kong"
    "MONTY0": "XN",  # In "Full Monty"
    "MOUNTAIN0": "XNZ",  # In "Blue Mountain"
    "PEPPER0": "XNZ",  # In "Chilli and Pepper"
    "SOUND0": "XNZ",  # In "Manchester's Sound"
    "TELECOM0": "XNT",  # In "Hong Kong Telecom"
    "TOUCH0": "XNZ",  # In "Don't Touch" (a magazine)
    "U0": "XNT",  # U as in "Hong Kong U" (= The University of Hong Kong)
}


def _get_tagged_sents():
    return [
        [(word, _FIX_HKCANCOR_TAGS.get(tag, tag)) for word, tag, _, _ in tagged_sent]
        for tagged_sent in hkcancor().tagged_sents()
    ]


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    tagger = POSTagger(**_TAGGER_PARAMETERS)
    tagger.train(_get_tagged_sents(), save=_PICKLE_PATH)
