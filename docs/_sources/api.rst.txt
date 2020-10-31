..  _api:

API Reference
=============

.. currentmodule:: pycantonese

Corpus Data
-----------

.. autosummary::
   :toctree: generated

    read_chat
    hkcancor
    corpus.CantoneseCHATReader
    corpus.CantoneseCHATReader.search

Jyutping Romanization
---------------------

.. autosummary::
   :toctree: generated

    characters_to_jyutping
    parse_jyutping
    jyutping_to_yale
    jyutping_to_tipa

Natural Language Processing
---------------------------

.. autosummary::
   :toctree: generated

    stop_words
    segment
    word_segmentation.Segmenter
    pos_tag
    pos_tagging.hkcancor_to_ud
