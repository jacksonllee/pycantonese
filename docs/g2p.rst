..  _g2p:

Grapheme-to-Phoneme Conversion
==============================

Grapheme-to-phoneme (G2P) conversion — mapping written characters to the
phonemes that pronounce them — is a foundational task in linguistics and
speech/NLP applications such as text-to-speech, pronunciation modeling,
and phonological analysis.
For Cantonese, that means going from Chinese characters straight to IPA
(the International Phonetic Alphabet).

The :func:`~pycantonese.g2p` function provides a one-call grapheme-to-phoneme
pipeline for Cantonese, composing
:func:`~pycantonese.characters_to_jyutping`
and :func:`~pycantonese.jyutping_to_ipa`:

.. code-block:: python

    import pycantonese
    pycantonese.g2p('香港人講廣東話。')  # Hongkongers speak Cantonese.
    # [('香港人', ['hœŋ55', 'kɔŋ25', 'jɐn21']),
    #  ('講', ['kɔŋ25']),
    #  ('廣東話', ['kʷɔŋ25', 'tʊŋ55', 'waː25']),
    #  ('。', None)]

The output is a list of segmented words, where each word is a 2-tuple of
(Cantonese characters, list of IPA syllables). The IPA list contains one IPA
string per character in the word.

When :func:`~pycantonese.g2p` receives a raw string, it runs word segmentation
internally (via :func:`~pycantonese.segment`) so that contextually
disambiguated pronunciations come through:

.. code-block:: python

    import pycantonese
    ## 蛋 alone is pronounced with tone 2 (high-rising).
    pycantonese.g2p('蛋')  # egg
    # [('蛋', ['taːn25'])]

    ## 蛋 in 蛋糕 is pronounced with tone 6 (low-level).
    pycantonese.g2p('蛋糕')  # cake
    # [('蛋糕', ['taːn22', 'kou55'])]

If you would rather supply your own segmentation, pass a list of words
instead of a string:

.. code-block:: python

    import pycantonese
    pycantonese.g2p(['廣東', '話'])  # Cantonese
    # [('廣東', ['kʷɔŋ25', 'tʊŋ55']), ('話', ['waː22'])]

Any word with no Jyutping mapping — an unseen Cantonese character, a
punctuation mark, or a non-Chinese token — yields ``None`` in place of the
IPA list, so callers can detect and handle out-of-vocabulary items
explicitly:

.. code-block:: python

    import pycantonese
    pycantonese.g2p('佢成日呃like')
    # [('佢', ['kʰɵy23']),
    #  ('成日', ['sɪŋ21', 'jɐt̚22']),
    #  ('呃', ['ŋaːk̚55']),
    #  ('like', None)]

The IPA mapping inherits the choices of :func:`~pycantonese.jyutping_to_ipa`,
which follows Matthews and Yip (2011: 461-463). To customize specific
IPA symbols, :func:`~pycantonese.g2p` accepts the keyword arguments
``onsets``, ``nuclei``, and ``codas``, each a dictionary that maps a Jyutping
sound to your desired IPA symbol:

.. code-block:: python

    import pycantonese
    pycantonese.g2p('我')
    # [('我', ['ŋɔ23'])]
    pycantonese.g2p('我', onsets={'ng': 'n'})
    # [('我', ['nɔ23'])]

For lower-level access — for example, if you want the intermediate Jyutping
output, or want to control tones, or want a single space-joined IPA string —
call :func:`~pycantonese.characters_to_jyutping` and
:func:`~pycantonese.jyutping_to_ipa` directly.
See :ref:`jyutping` for details.
