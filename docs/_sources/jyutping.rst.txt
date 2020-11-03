..  _jyutping:

.. _NLTK: https://www.nltk.org/

.. _TIPA: https://www.ctan.org/pkg/tipa?lang=en

Jyutping Romanization
=====================

Among the most common tasks in handling Cantonese corpus data are those that
involve the processing of `Jyutping romanization
<https://www.lshk.org/jyutping>`_.
A common need is to convert Cantonese characters to Jyutping romanization.
Another functionality of interest is the ability to convert Jyutping into
other romanization schemes still used today.
PyCantonese provides tools for these use cases.

Characters-to-Jyutping Conversion
---------------------------------

.. versionadded:: 2.4.0

The function :func:`~pycantonese.characters_to_jyutping`
takes a string of Cantonese characters
and returns its word-segmented version with Jyutping romanization:

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.characters_to_jyutping('香港人講廣東話')  # "Hongkongers speak Cantonese"
    [("香港人", "hoeng1gong2jan4"), ("講", "gong2"), ("廣東話", "gwong2dung1waa2")]

The characters-to-Jyutping conversion model is based on two data sources:
(i) the HKCanCor corpus data included in the PyCantonese library, and
(ii) the rime-cantonese data (the 2020.09.09 release, CC BY 4.0 license).
Any unseen Cantonese character (or punctuation mark, for that matter) is
represented by ``None`` in the output.

To further process the Jyutping strings,
please see `Parsing Jyutping Strings <parsing_jyutping_strings_>`_.

A Cantonese character may have multiple pronunciations,
most commonly due to *pinjam* (變音, "changed tone").
Whether the function :func:`~pycantonese.characters_to_jyutping`
can intelligently output
the correct, contextually dependent pronunciation depends on whether
the HKCanCor data (which trains the conversion model) contains
the relevant tokens. Example:

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.characters_to_jyutping('蛋')  # egg
    [("蛋", "daan2")]  # correct pronunciation of 蛋 with tone 2 (high-rising) as a standalone word
    >>> pc.characters_to_jyutping('蛋糕')  # cake
    [("蛋糕", "daan6gou1")]  # correct pronunciation of 蛋 with tone 6 (low-level) in this context

.. _parsing_jyutping_strings:

Parsing Jyutping Strings
------------------------

Converting Jyutping to other romanization schemes necessitates
the ability to parse Jyutping for the various phonological components
(onset, nucleus, coda, and tone). To this end, PyCantonese exposes
the function :func:`~pycantonese.parse_jyutping`
which parses a string of Jyutping romanization
and returns a list of tuples; the string may contain romanization for multiple
Chinese characters. The parsed romanization for a character is a 4-tuple of
(onset, nucleus, coda, tone):

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.parse_jyutping('hou2')  # 好
    [('h', 'o', 'u', '2')]
    >>> pc.parse_jyutping('gwong2dung1waa2')  # 廣東話
    [('gw', 'o', 'ng', '2'), ('d', 'u', 'ng', '1'), ('w', 'aa', '', '2')]

Syllabic nasals are treated as nuclei:

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.parse_jyutping('m4goi1')  # 唔該
    [('', 'm', '', '4'), ('g', 'o', 'i', '1')]

The function :func:`~pycantonese.parse_jyutping`
is able to detect invalid Jyutping romanization:

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.parse_jyutping('hou7')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/local/lib/python3.4/dist-packages/pycantonese/jyutping.py", line 197, in parse_jyutping
        raise ValueError('tone error -- ' + repr(jp))
    ValueError: tone error -- 'hou7'

Jyutping-to-Yale Conversion
---------------------------

The Yale romanization is still a commonly used system, particularly in numerous
dictionaries and 
Cantonese language teaching resources. PyCantonese provides the
:func:`~pycantonese.jyutping_to_yale`
function which reads a valid Jyutping string and returns the Yale equivalent:

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.jyutping_to_yale('m4goi1')
    ['m̀h', 'gōi']
    >>> pc.jyutping_to_yale('gwong2dung1waa2')
    ['gwóng', 'dūng', 'wá']

:func:`~pycantonese.jyutping_to_yale` has the keyword argument ``as_list``.
When set to be ``False``, it turns the returned value into a string.

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.jyutping_to_yale('gwong2dung1waa2', as_list=False)
    'gwóngdūngwá'

While getting a string instead of a list might seem trivial enough that
``as_list`` would be necessary, its usefulness arises when
there is potential confusion. In Yale romanization, a consonant letter or
the low-tone marker "h" can be ambiguous as an onset of a syllable or as part
of the previous syllable. When such ambiguity is detected, ``as_list=False``
automatically adds the quote character ``'`` as a separator to disambiguate:

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.jyutping_to_yale('hei3hau6')  # 氣候, climate
    'hei'hauh'  # 'heihauh' would be ambiguous between hei3hau6 and hei6au6.

Jyutping-to-TIPA Conversion
---------------------------

PyCantonese also offers the :func:`~pycantonese.jyutping_to_tipa` function for the
`LaTeX TIPA <https://www.ctan.org/pkg/tipa?lang=en>`_ users::

    >>> import pycantonese as pc
    >>> pc.jyutping_to_tipa('m4goi1')
    ['\\s{m}21', 'kOY55']
    >>> pc.jyutping_to_tipa('gwong2dung1waa2')
    ['k\\super w ON25', 'tUN55', 'wa25']

Currently, tones are output as Chao tone letters (= the numbers from 1 to 5)
directly suffixed to the individual syllable string.
(This may change in a future
release if this behavior proves to be inconvenient.)
