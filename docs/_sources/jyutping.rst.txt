..  _jyutping:

.. _NLTK: http://www.nltk.org

.. _TIPA: https://www.ctan.org/pkg/tipa?lang=en

Jyutping Romanization: Parsing and Conversion
=============================================

Among the most common tasks in handling Cantonese corpus data are those that
involve the processing of `Jyutping romanization
<http://lshk.org/node/47>`_, e.g., searching for words by a
particular Jyutping element (an onset, a tone, or something else).
It is necessary,
therefore, to parse a string of Jyutping romanization into
its phonological components. Moreover, several other Cantonese romanization
schemes are actively used alongside Jyutping. PyCantonese provides
tools for converting Jyutping to some of these romanization systems.


Parsing Jyutping Strings
------------------------

The function ``parse_jyutping()`` parses a string of Jyutping romanization
and returns a list of tuples; the string may contain romanization for multiple
Chinese characters. The parsed romanization for a character is a 4-tuple:
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

The function ``jyutping()`` is able to detect invalid Jyutping romanization:

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
``jyutping2yale()``
function which reads a valid Jyutping string and returns the Yale equivalent:

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.jyutping2yale('m4goi1')
    'm̀hgōi'
    >>> pc.jyutping2yale('gwong2dung1waa2')
    'gwóngdūngwá'

In cases of potential ambiguity where a consonant letter could be part of
the syllable on the left or the right,
the quote ``'`` is used as a separator:

.. code-block:: python

    >>> pc.jyutping2yale('hei3hau6')  # 氣候; Yale "h" in 2nd syllable onset w/o separator would be ambiguous
    "hei'hauh"

``jyutping2yale()`` has the optional parameter ``as_list`` for returning a list
of Yale strings instead:

.. code-block:: python

    >>> pc.jyutping2yale('gwong2dung1waa2', as_list=True)
    ['gwóng', 'dūng', 'wá']


Jyutping-to-TIPA Conversion
---------------------------

PyCantonese also offers the ``jyutping2tipa()`` function for the
`LaTeX TIPA <https://www.ctan.org/pkg/tipa?lang=en>`_ users::

    >>> import pycantonese as pc
    >>> pc.jyutping2tipa('m4goi1')
    ['\\s{m}21', 'kOY55']
    >>> pc.jyutping2tipa('gwong2dung1waa2')
    ['k\\super w ON25', 'tUN55', 'wa25']

Currently, tones are output as Chao tone letters (= the numbers from 1 to 5)
directly suffixed to the individual syllable string.
(This may change in a future
release if this behavior proves to be inconvenient.)

