..  _reader:

Corpus reader methods
=====================

The sections :ref:`represent_words` and :ref:`note_on_methods` provide
background information for how to use the methods listed in
:ref:`metadata_methods` and :ref:`data_methods`.

.. WARNING::
   If you are running a script on **Windows**, be sure to put all your code
   under the scope of ``if __name__ == '__main__':``.
   (PyCantonese uses the ``multiprocessing`` module to read data files.)

.. _represent_words:

The representation of "words"
-----------------------------

The representation of "words" in PyCantonese comes in two flavors
(similar to NLTK):

1. The "simple" representation as a **string**,
   which is what appears as a word token (in Chinese characters)
   in a transcription line
   starting with ``*`` in the CHAT transcript.

2. The "tagged" representation as a **tuple** of
   (*word*, *pos*, *jyutping*, *rel*),
   which contains information from the transcription line and its ``%``-tiers:

   *word* (str) -- Chinese character(s)

   *pos* (str) -- part-of-speech tag from ``%mor`` (All PoS tags are rendered in uppercase.)

   *jyutping* (str) -- Jyutping romanization from ``%mor``
   (plus inflectional information, if any)

   *rel* -- dependency and grammatical relation from ``%gra``
   (no known datasets have made used of ``%gra`` yet)

To illustrate, let us consider the following CHAT utterance with its ``%mor``
tier::

    *XXA:	喂 遲 啲 去 唔 去 旅行 啊 ?
    %mor:	e|wai3 a|ci4 u|di1 v|heoi3 d|m4 v|heoi3 vn|leoi5hang4 y|aa3 ?

The list of "simple" words from this utterance are the list of word token
strings:

.. code-block:: python

    ['喂', '遲', '啲', '去', '唔', '去', '旅行', '啊', '?']

The list of "tagged" words from this utterance are a list of 4-tuples:

.. code-block:: python

    [('喂', 'E', 'wai3', ''),
     ('遲', 'A', 'ci4', ''),
     ('啲', 'U', 'di1', ''),
     ('去', 'V', 'heoi3', ''),
     ('唔', 'D', 'm4', ''),
     ('去', 'V', 'heoi3', ''),
     ('旅行', 'VN', 'leoi5hang4', ''),
     ('啊', 'Y', 'aa3', ''),
     ('?', '?', '', '')]

The distinction of "simple" versus "tagged" words is reflected in the data
access methods listed in :ref:`data_methods` below.

.. _note_on_methods:

A note on the access methods
----------------------------

.. code-block:: python

    >>> import pycantonese as pc
    >>> corpus = pc.hkcancor()

A corpus object, such as ``corpus`` as shown just above, has an array of
methods X(). An example is ``number_of_files()``:

.. code-block:: python

    >>> corpus.number_of_files()
    58

Many of these methods together with their documentation notes are
programmatically inherited from the library PyLangAcq for
language acquisition research. A few remarks here are necessary to
avoid confusion.

Many methods have the optional parameter ``participant``, which may safely be
ignored in PyCantonese. The parameter ``participant`` specifies
which participant(s) are of interest. This is important in the context of
language acquisition: ``'CHI'`` for the target child, ``'MOT'`` for the mother,
and so forth. In the CHAT format of HKCanCor that PyCantonese includes, the
participants are rendered as codes such ``'XXA'``, ``'XXB'`` etc based on
the original HKCanCor files. When ``participant`` is not specified,
all participants are automatically included.

Another optional parameter of interest is ``by_files``. Typically, a corpus
comes in the form of multiple CHAT files. If a method X() has ``by_files``,
this parameter is set to be ``False`` by default, so that X() returns whatever
it is for all the files *without* the file structure. If you are interested
in results for individual files, set ``by_files`` to be ``True`` and the return
object is dict(absolute-path filename: X() for that file) instead.


.. _metadata_methods:

Metadata methods
----------------

.. currentmodule:: pycantonese.corpus.CantoneseCHATReader

.. autosummary::

   filenames
   find_filename
   number_of_files
   number_of_utterances

.. _data_methods:

Data methods
------------

.. currentmodule:: pycantonese.corpus.CantoneseCHATReader

.. autosummary::

   utterances
   words
   tagged_words
   sents
   tagged_sents
   jyutpings
   jyutping_sents
   characters
   character_sents
   part_of_speech_tags
   word_frequency
   word_ngrams
   search
   update
   add
   remove
   clear

.. _reader_api:

Full reader API
---------------

.. autoclass:: pycantonese.corpus.CantoneseCHATReader
   :show-inheritance:
   :inherited-members:

