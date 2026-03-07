..  _jyutping:

Jyutping Romanization
=====================

Among the most common tasks in handling Cantonese corpus data are those that
involve the processing of `Jyutping romanization
<https://lshk.org/jyutping-scheme/>`_.
A common need is to convert Cantonese characters to Jyutping romanization.
Another functionality of interest is the ability to convert Jyutping into
IPA or another romanization scheme.
Whether you have :ref:`data in Jyutping from a corpus reader<jyutping_from_reader>`
or you have independently ingested Jyutping as Python strings,
PyCantonese provides tools for these use cases.

.. _chars_to_jp:

Characters-to-Jyutping Conversion
---------------------------------

The function :func:`~pycantonese.characters_to_jyutping`
takes a string of Cantonese characters
and returns its word-segmented version with Jyutping romanization:

.. code-block:: python

    import pycantonese
    pycantonese.characters_to_jyutping('香港人講廣東話')  # Hongkongers speak Cantonese
    # [('香港人', 'hoeng1gong2jan4'), ('講', 'gong2'), ('廣東話', 'gwong2dung1waa2')]

The characters-to-Jyutping conversion model is based on two data sources:
(i) the HKCanCor corpus data included in the PyCantonese library, and
(ii) the rime-cantonese data.
Any unseen character, Cantonese or otherwise, is represented by ``None`` in the output.

To further process the Jyutping strings,
please see `Parsing Jyutping Strings <parsing_jyutping_strings_>`_.

A Cantonese character may have multiple pronunciations,
most commonly due to *pinjam* (變音, "changed tone").
Whether the function :func:`~pycantonese.characters_to_jyutping`
can intelligently output
the correct, contextually dependent pronunciation depends on whether
the underlying data contains the relevant tokens. Example:

.. code-block:: python

    import pycantonese
    ## The correct pronunciation of 蛋 is with tone 2 (high-rising) as a standalone word.
    pycantonese.characters_to_jyutping('蛋')  # egg
    # [('蛋', 'daan2')]

    ## The correct pronunciation of 蛋 is with tone 6 (low-level) in 蛋糕.
    pycantonese.characters_to_jyutping('蛋糕')  # cake
    # [('蛋糕', 'daan6gou1')]

If you don't want :func:`~pycantonese.characters_to_jyutping` to perform
word segmentation, provide a list of strings instead with your desired
segmentation.

.. _parsing_jyutping_strings:

Parsing Jyutping Strings
------------------------

Converting Jyutping to other romanization schemes necessitates
the ability to parse Jyutping for the various phonological components
(onset, nucleus, coda, and tone). To this end, PyCantonese exposes
the function :func:`~pycantonese.parse_jyutping`
which parses a string of Jyutping romanization
and returns a list of :class:`~pycantonese.jyutping.Jyutping` objects;
the string may contain results for multiple
Chinese characters.:

.. code-block:: python

    import pycantonese
    pycantonese.parse_jyutping('hou2')  # 好 good
    # [Jyutping(onset='h', nucleus='o', coda='u', tone='2')]
    pycantonese.parse_jyutping('gwong2dung1waa2')  # 廣東話 Cantonese
    # [Jyutping(onset='gw', nucleus='o', coda='ng', tone='2'),
    #  Jyutping(onset='d', nucleus='u', coda='ng', tone='1'),
    #  Jyutping(onset='w', nucleus='aa', coda='', tone='2')]

Syllabic nasals are treated as nuclei:

.. code-block:: python

    import pycantonese
    pycantonese.parse_jyutping('m4goi1')  # 唔該 thank you / please
    # [Jyutping(onset='', nucleus='m', coda='', tone='4'),
    #  Jyutping(onset='g', nucleus='o', coda='i', tone='1')]

The function :func:`~pycantonese.parse_jyutping`
is able to detect invalid Jyutping romanization:

.. skip: start

.. code-block:: python

    import pycantonese
    pycantonese.parse_jyutping('hou7')
    # Traceback (most recent call last):
    #   ...
    # ValueError: tone error -- 'hou7'

.. skip: end


The :class:`~pycantonese.jyutping.Jyutping` class makes it easy to access
the onset, nucleus, coda, and tone using the attribute syntax.
It is also straightforward to retrieve the string representation
and final (= nucleus + coda; 韻母):

.. code-block:: python

    from pycantonese.jyutping import Jyutping
    jp = Jyutping(onset="j", nucleus="yu", coda="t", tone="6")
    jp.onset
    # 'j'
    jp.nucleus
    # 'yu'
    jp.coda
    # 't'
    jp.tone
    # '6'
    str(jp)
    # 'jyut6'
    jp.final
    # 'yut'


Jyutping-to-IPA Conversion
--------------------------

:func:`~pycantonese.jyutping_to_ipa` converts Jyutping into IPA
(International Phonetic Alphabet), the standard representation of speech sounds
in phonetics and phonology:

.. code-block:: python

    import pycantonese
    pycantonese.jyutping_to_ipa('gwong2dung1waa2')  # 廣東話 Cantonese
    # ['kʷɔŋ25', 'tʊŋ55', 'waː25']
    pycantonese.jyutping_to_ipa('gwong2dung1waa2', return_as="string")
    # 'kʷɔŋ25 tʊŋ55 waː25'

The mapping from Jyutping to IPA symbols is based on Matthews and Yip (2011: 461-463).
If you would like to customize the mapping of specific symbols,
:func:`~pycantonese.jyutping_to_ipa` accepts keyword arguments
``onsets``, ``nuclei``, ``codas``, and ``tones``, each of which
takes a dictionary that maps a Jyutping sound to your desired symbol:

.. code-block:: python

    import pycantonese
    pycantonese.jyutping_to_ipa('ci1')
    # ['tsʰi55']
    pycantonese.jyutping_to_ipa('ci1', onsets={'c': "tʃ'"})
    # ["tʃ'i55"]
    pycantonese.jyutping_to_ipa('ci1', tones={'1': "˥"})
    # ['tsʰi˥']


Jyutping-to-Yale Conversion
---------------------------

The Yale romanization is still a commonly used system, particularly in
dictionaries and pedagogical materials. PyCantonese provides the
:func:`~pycantonese.jyutping_to_yale`
function which reads a valid Jyutping string and returns the Yale equivalent:

.. code-block:: python

    import pycantonese
    pycantonese.jyutping_to_yale('m4goi1')  # 唔該 thank you / please
    # ['m̀h', 'gōi']
    pycantonese.jyutping_to_yale('gwong2dung1waa2')  # 廣東話 Cantonese
    # ['gwóng', 'dūng', 'wá']

:func:`~pycantonese.jyutping_to_yale` has the keyword argument ``return_as``.
When set to ``"string"``, it turns the returned value into a string.

.. code-block:: python

    import pycantonese
    pycantonese.jyutping_to_yale('gwong2dung1waa2', return_as="string")  # 廣東話 Cantonese
    # 'gwóngdūngwá'

While getting a string instead of a list might seem trivial enough without ``return_as``,
the argument helps to resolve potential confusion.
In Yale romanization, a consonant letter or
the low-tone marker "h" can be ambiguous as an onset of a syllable or as part
of the previous syllable. When such ambiguity is detected, ``return_as="string"``
automatically adds the quote character ``'`` as a separator to disambiguate:

.. code-block:: python

    import pycantonese
    pycantonese.jyutping_to_yale('hei3hau6', return_as="string")  # 氣候 climate
    # "hei'hauh"
    ## 'heihauh' would be ambiguous between hei3hau6 and hei6au6.

Jyutping-to-TIPA Conversion
---------------------------

PyCantonese also offers the :func:`~pycantonese.jyutping_to_tipa` function for the
`LaTeX TIPA <https://www.ctan.org/pkg/tipa?lang=en>`_ users:

.. code-block:: python

    import pycantonese
    pycantonese.jyutping_to_tipa('m4goi1')  # 唔該 thank you / please
    # ['\\s{m}21', 'kOY55']
    pycantonese.jyutping_to_tipa('gwong2dung1waa2')  # 廣東話 Cantonese
    # ['k\\super w ON25', 'tUN55', 'wa25']

Currently, tones are output as Chao tone letters (= the numbers from 1 to 5)
directly suffixed to the individual syllable string.
(This may change in a future
release if this behavior proves to be inconvenient.)
