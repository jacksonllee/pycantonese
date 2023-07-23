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
    CHATReader
    CHATReader.search


Jyutping Romanization
---------------------

.. autosummary::
    :toctree: generated

    characters_to_jyutping
    parse_jyutping
    jyutping_to_ipa
    jyutping_to_yale
    jyutping_to_tipa


Natural Language Processing
---------------------------

.. autosummary::
    :toctree: generated

    stop_words
    parse_text
    segment
    word_segmentation.Segmenter
    pos_tag
    pos_tagging.hkcancor_to_ud


:class:`~pycantonese.CHATReader`
--------------------------------

.. autoclass:: pycantonese.CHATReader
   :members:
   :inherited-members:


:class:`~pycantonese.corpus.Token`
----------------------------------

.. autoclass:: pycantonese.corpus.Token


:class:`~pycantonese.jyutping.Jyutping`
---------------------------------------

.. autoclass:: pycantonese.jyutping.Jyutping
   :members:
   :special-members:
