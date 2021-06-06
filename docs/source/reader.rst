..  _reader:

Corpus Reader Methods
=====================

After you have created a corpus reader (see :ref:`data`),
the headers, transcriptions, and annotations are all accessible through
the methods of the corpus reader object.

Let's say we have a corpus reader with the built-in HKCanCor data.

.. code-block:: python

    >>> import pycantonese
    >>> corpus = pycantonese.hkcancor()


Headers
-------

A CHAT data file typically has metadata around the top of the file,
with lines that begin with ``@``.
The metadata include participants' demographics (age, gender, etc),
date of recording, and languages used in the data.

Specifically for HKCanCor, the participants in all the data files are anonymous.
In PyCantonese's rendition of HKCanCor,
their names are simply placeholders such as ``A``, ``B``, etc, and their
corresponding three-letter codes are ``XXA``, ``XXB``, etc.
In contrast, many CHILDES and TalkBank datasets have their participants identified.
By convention, the target child's code is ``CHI``, the child's mother's ``MOT``,
and the child's father's ``FAT``.

Since PyCantonese uses PyLangAcq to parse CHAT data files,
the way in which header information is accessed is identical between the
two packages. Please see `PyLangAcq's documentation on headers <https://pylangacq.org/headers.html>`_.

To see how a header from HKCanCor translates
to its representation in PyCantonese,
here is the header from ``FC-001_v2.cha``, the first (by filename) of the 58 CHAT files:

.. skip: start

.. code-block::

    @UTF8
    @Begin
    @Languages:	yue , eng
    @Participants:	XXA A Adult , XXB B Adult
    @ID:	yue , eng|HKCanCor|XXA|34;|female|||Adult||origin:HK|
    @ID:	yue , eng|HKCanCor|XXB|37;|female|||Adult||origin:HK|
    @Date:	30-APR-1997
    @Tape Number:	001

.. skip: end

In this example, this recording session was between two Hong Kong female speakers
(ages 34 and 37), recorded on April 30th, 1997. The languages in this data file
are both Cantonese and English (in that order of usage frequency;
the ordering in ``yue , eng`` is meaningful).

Through the corpus reader object ``corpus`` we've just created,
we see the same information by calling the method :func:`~pycantonese.CHATReader.headers`
(which returns a list of dicts; ``[0]`` gets the first dict that
corresponds to ``FC-001_v2.cha``):

.. code-block:: python

    >>> corpus.headers()[0]
    {'UTF8': '',
     'Languages': ['yue', 'eng'],
     'Participants': {'XXA': {'name': 'A',
                              'language': 'yue , eng',
                              'corpus': 'HKCanCor',
                              'age': '34;',
                              'sex': 'female',
                              'group': '',
                              'ses': '',
                              'role': 'Adult',
                              'education': '',
                              'custom': 'origin:HK'},
                      'XXB': {'name': 'B',
                              'language': 'yue , eng',
                              'corpus': 'HKCanCor',
                              'age': '37;',
                              'sex': 'female',
                              'group': '',
                              'ses': '',
                              'role': 'Adult',
                              'education': '',
                              'custom': 'origin:HK'}},
     'Date': {datetime.date(1997, 4, 30)},
     'Tape Number': '001'}


Here are the currently implemented methods for header information:

.. currentmodule:: pycantonese.CHATReader

.. autosummary::

    ages
    dates_of_recording
    headers
    languages
    participants

Whenever it is appropriate, these header information methods, as well as
the data access methods to be introduced below, have optional arguments
to (i) control the output data structure (``by_utterances`` and ``by_files``)
and (ii) filter by participants (``participants`` and ``exclude``).
The methods' hyperlinks point to more detailed documentation.


Transcriptions and Annotations
------------------------------

A PyCantonese corpus reader is an instance of the :class:`~pycantonese.CHATReader` class.
While this class inherits the CHAT handling capabilities from the underlying
PyLangAcq package, :class:`~pycantonese.CHATReader` has several
additional functionality to deal with Cantonese-specific elements,
particularly Jyutping romanization and Chinese characters.

Here are the major :class:`~pycantonese.CHATReader` methods to access data
at different levels of data structure:

.. currentmodule:: pycantonese.CHATReader

.. autosummary::

    words
    tokens
    utterances

Words are the usual text strings.
Think of tokens as words but with annotations
(part-of-speech tags, morphological information, etc).
An utterance is a a list of tokens plus associated information
(the participant of the utterance, time markers if there are associated
audio-visual materials, etc).

.. code-block:: python

    >>> corpus.words()[:10]
    ['喂', '遲', '啲', '去', '唔', '去', '旅行', '啊', '?', '你']
    >>>
    >>> corpus.tokens()[:10]
    [Token(word='喂', pos='E', jyutping='wai3', mor=None, gra=None),
     Token(word='遲', pos='A', jyutping='ci4', mor=None, gra=None),
     Token(word='啲', pos='U', jyutping='di1', mor=None, gra=None),
     Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
     Token(word='唔', pos='D', jyutping='m4', mor=None, gra=None),
     Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
     Token(word='旅行', pos='VN', jyutping='leoi5hang4', mor=None, gra=None),
     Token(word='啊', pos='Y', jyutping='aa3', mor=None, gra=None),
     Token(word='?', pos='?', jyutping=None, mor=None, gra=None),
     Token(word='你', pos='R', jyutping='nei5', mor=None, gra=None)]
    >>>
    >>> corpus.utterances()[:1]
    [Utterance(participant='XXA',
               tokens=[Token(word='喂', pos='E', jyutping='wai3', mor=None, gra=None),
                       Token(word='遲', pos='A', jyutping='ci4', mor=None, gra=None),
                       Token(word='啲', pos='U', jyutping='di1', mor=None, gra=None),
                       Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
                       Token(word='唔', pos='D', jyutping='m4', mor=None, gra=None),
                       Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
                       Token(word='旅行', pos='VN', jyutping='leoi5hang4', mor=None, gra=None),
                       Token(word='啊', pos='Y', jyutping='aa3', mor=None, gra=None),
                       Token(word='?', pos='?', jyutping=None, mor=None, gra=None)],
               time_marks=None,
               tiers={'XXA': '喂 遲 啲 去 唔 去 旅行 啊 ?',
                      '%mor': 'e|wai3 a|ci4 u|di1 v|heoi3 d|m4 v|heoi3 vn|leoi5hang4 y|aa3 ?'})]


PyCantonese has an augmented representation of tokens,
where Jyutping romanization has its own dedicated spot.


.. _jyutping_from_reader:

Jyutping Romanization
^^^^^^^^^^^^^^^^^^^^^

Tokens, as annotated words, are instances of the :class:`~pycantonese.corpus.Token` class.
A :class:`~pycantonese.corpus.Token` instance has the PyCantonese-specific attribute
``jyutping`` to accommodate Jyutping romanization.

To illustrate, below is the first utterance in ``FC-001_v2.cha``,
where Jyutping romanization is found in the ``%mor`` tier:

.. skip: start

.. code-block::

    *XXA:	喂 遲 啲 去 唔 去 旅行 啊 ?
    %mor:	e|wai3 a|ci4 u|di1 v|heoi3 d|m4 v|heoi3 vn|leoi5hang4 y|aa3 ?

.. skip: end

Here are the corresponding tokens from PyCantonese,
where the data in CHAT format has been parsed into :class:`~pycantonese.corpus.Token`
objects, with the attribute ``jyutping`` storing Jyutping romanization:

.. code-block:: python

    >>> some_tokens = corpus.tokens(by_utterances=True)[0]
    >>> some_tokens
    [Token(word='喂', pos='E', jyutping='wai3', mor=None, gra=None),
     Token(word='遲', pos='A', jyutping='ci4', mor=None, gra=None),
     Token(word='啲', pos='U', jyutping='di1', mor=None, gra=None),
     Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
     Token(word='唔', pos='D', jyutping='m4', mor=None, gra=None),
     Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
     Token(word='旅行', pos='VN', jyutping='leoi5hang4', mor=None, gra=None),
     Token(word='啊', pos='Y', jyutping='aa3', mor=None, gra=None),
     Token(word='?', pos='?', jyutping=None, mor=None, gra=None)]
    >>> for token in some_tokens:
    ...     print(token.jyutping)
    ...
    wai3
    ci4
    di1
    heoi3
    m4
    heoi3
    leoi5hang4
    aa3
    None

Given the ubiquitous status of Jyutping in the study of Cantonese,
the :func:`~pycantonese.CHATReader.jyutping` method is also defined for convenience:

.. code-block:: python

    >>> corpus.jyutping(by_utterances=True)[0]
    ['wai3', 'ci4', 'di1', 'heoi3', 'm4', 'heoi3', 'leoi5hang4', 'aa3', None]

For further processing Jyutping romanization, please see the :ref:`jyutping` page.


Chinese Characters
^^^^^^^^^^^^^^^^^^

Corpus data in the CHAT format is word-segmented,
and the same word segmentation is preserved in the output of
the :class:`~pycantonese.CHATReader` methods
:func:`~pycantonese.CHATReader.words`,
:func:`~pycantonese.CHATReader.tokens`,
and :func:`~pycantonese.CHATReader.utterances`.
For Cantonese data, a (segmented) word can be, say, 廣東話 ("Cantonese") with
three Chinese characters.
To work with data at the character level, :func:`~pycantonese.CHATReader.characters`
is available:

.. code-block:: python

    >>> corpus.characters(by_utterances=True)[0]
    ['喂', '遲', '啲', '去', '唔', '去', '旅', '行', '啊', '?']

If you independently have Cantonese data in Chinese characters,
PyCantonese has tools for
:ref:`word segmentation<word_segmentation>` and
:ref:`part-of-speech tagging<pos_tagging>`.


Word Frequencies and Ngrams
---------------------------

For word counts in various flavors, use the methods
:func:`~pycantonese.CHATReader.word_frequencies` and
:func:`~pycantonese.CHATReader.word_ngrams`:

.. code-block:: python

    >>> word_freq = corpus.word_frequencies()  # A collections.Counter object
    >>> word_freq.most_common(10)
    [('.', 13251),
     (',', 9282),
     ('係', 5019),
     ('啊', 4110),
     ('?', 2911),
     ('我', 2755),
     ('噉', 2741),
     ('呢', 2734),
     ('你', 2570),
     ('佢', 2259)]
    >>>
    >>> trigrams = corpus.word_ngrams(3)  # A collections.Counter object
    >>> trigrams.most_common(10)
    [(('係', '啊', '.'), 527),
     ((',', '誒', ','), 520),
     (('呢', ',', '就'), 219),
     (('係', '啊', ','), 209),
     (('係', '囖', '.'), 202),
     (('吖', '嗎', '.'), 202),
     (('𡃉', '喎', '.'), 186),
     (('𠺢', '嗎', '.'), 167),
     (('係', '喇', '.'), 140),
     (('係', '喇', ','), 134)]
