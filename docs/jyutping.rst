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
and returns its word-segmented version with Jyutping romanization.
Within each Jyutping string, syllables are separated by a single space:

.. code-block:: python

    import pycantonese
    pycantonese.characters_to_jyutping('香港人講廣東話')  # Hongkongers speak Cantonese
    # [('香港人', 'hoeng1 gong2 jan4'), ('講', 'gong2'), ('廣東話', 'gwong2 dung1 waa2')]

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
    # [('蛋糕', 'daan6 gou1')]

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
    pycantonese.parse_jyutping('gwong2 dung1 waa2')  # 廣東話 Cantonese
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
in phonetics and phonology. It accepts either a single Jyutping string (one
word) or a list of strings (one word per element). The output is a list with
one entry per input word; within each entry, syllables are separated by a
single space:

.. code-block:: python

    import pycantonese
    pycantonese.jyutping_to_ipa('gwong2dung1waa2')  # 廣東話 Cantonese
    # ['kʷɔŋ25 tʊŋ55 waː25']
    pycantonese.jyutping_to_ipa(['gwong2dung1', 'waa2'])  # word-segmented input
    # ['kʷɔŋ25 tʊŋ55', 'waː25']

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


Grapheme-to-Phoneme Conversion
------------------------------

If you want to go directly from Cantonese characters to IPA in a single call,
see :ref:`g2p` for the dedicated :func:`~pycantonese.g2p` function, which
composes :func:`~pycantonese.characters_to_jyutping` and
:func:`~pycantonese.jyutping_to_ipa`.


Jyutping-to-Yale Conversion
---------------------------

The Yale romanization is still a commonly used system, particularly in
dictionaries and pedagogical materials. PyCantonese provides the
:func:`~pycantonese.jyutping_to_yale`
function which reads a valid Jyutping string and returns the Yale equivalent.
Like :func:`~pycantonese.jyutping_to_ipa`, the function accepts either a
single string (one word) or a list of strings (one word per element). The
output is a list with one entry per input word; within each entry, syllables
are separated by a single space:

.. code-block:: python

    import pycantonese
    pycantonese.jyutping_to_yale('m4goi1')  # 唔該 thank you / please
    # ['m̀h gōi']
    pycantonese.jyutping_to_yale('gwong2dung1waa2')  # 廣東話 Cantonese
    # ['gwóng dūng wá']
    pycantonese.jyutping_to_yale(['gwong2dung1', 'waa2'])  # word-segmented input
    # ['gwóng dūng', 'wá']

The space between syllables also disambiguates Yale strings where a
consonant letter or the low-tone marker "h" could otherwise be read as either
an onset of the next syllable or part of the previous one:

.. code-block:: python

    import pycantonese
    pycantonese.jyutping_to_yale('hei3hau6')  # 氣候 climate
    # ['hei hauh']
    ## Without the space, 'heihauh' (Yale) would be ambiguous between hei3hau6 and hei6au6 (Jyutping).

If you need one combined string instead of a list of words, use
:func:`~pycantonese.stringify_yale`. Words are joined by spaces, and an
apostrophe ``'`` is inserted only at syllable boundaries that would
otherwise be ambiguous:

.. code-block:: python

    from pycantonese import jyutping_to_yale, stringify_yale
    stringify_yale(jyutping_to_yale('gwong2dung1waa2'))
    # 'gwóngdūngwá'
    stringify_yale(jyutping_to_yale('hei3hau6'))  # 氣候 climate
    # "hei'hauh"
    stringify_yale(jyutping_to_yale(['gwong2dung1', 'waa2']))
    # 'gwóngdūng wá'

Yale-to-Jyutping Conversion
---------------------------

The reverse of :func:`~pycantonese.jyutping_to_yale` is also available
as :func:`~pycantonese.yale_to_jyutping`, which reads Yale and returns the
Jyutping equivalent. As with the other conversion functions, pass a single
string for one word, or a list of strings to mark explicit word boundaries:

.. code-block:: python

    import pycantonese
    pycantonese.yale_to_jyutping('gwóngdūngwá')  # 廣東話 Cantonese
    # ['gwong2 dung1 waa2']
    pycantonese.yale_to_jyutping(['gāmyaht', 'góng', 'gwóngdūngwá'])  # word-segmented input
    # ['gam1 jat6', 'gong2', 'gwong2 dung1 waa2']

Inside a single-word string, both whitespace and apostrophes ``'`` are
accepted as syllable-boundary hints and do not create word boundaries:

.. code-block:: python

    import pycantonese
    pycantonese.yale_to_jyutping("hei'hauh")
    # ['hei3 hau6']
    pycantonese.yale_to_jyutping('hei hauh')
    # ['hei3 hau6']

Jyutping-to-TIPA Conversion
---------------------------

PyCantonese also offers the :func:`~pycantonese.jyutping_to_tipa` function for the
`LaTeX TIPA <https://www.ctan.org/pkg/tipa?lang=en>`_ users:

.. code-block:: python

    import pycantonese
    pycantonese.jyutping_to_tipa('m4goi1')  # 唔該 thank you / please
    # ['\\s{m}21 kOY55']
    pycantonese.jyutping_to_tipa('gwong2dung1waa2')  # 廣東話 Cantonese
    # ['k\\super w ON25 tUN55 wa25']

Currently, tones are output as Chao tone letters (= the numbers from 1 to 5)
directly suffixed to the individual syllable string.
(This may change in a future
release if this behavior proves to be inconvenient.)
