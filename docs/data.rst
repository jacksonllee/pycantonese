..  _data:

Corpus Data
===========

CHAT Format
-----------

For a corpus dataset to be useful for modeling work beyond search queries,
its source data has to be available in a machine-readable format.
For Cantonese, several corpora that meet this criterion
are those from CHILDES and TalkBank,
thanks to research on Cantonese language acquisition in recent years.
More generally, given the nature of Cantonese, many of its corpora are transcribed data
from naturalistic speech.
For these reasons, PyCantonese adopts the `CHAT <https://talkbank.org/0info/manuals/CHAT.pdf>`_
corpus format from CHILDES and TalkBank.
CHAT is widely used, well-documented, and rich for linguistic annotations.
PyCantonese uses the library
`Rustling <https://docs.rustling.io/stable/chat.html>`_ to parse CHAT data files.
For a primer on the CHAT data format, please see
`here <https://docs.rustling.io/stable/chat/transcriptions.html#chat-format>`_.


Built-in Data
-------------

PyCantonese ships with two built-in corpora: HKCanCor and CantoMap.

HKCanCor
^^^^^^^^

The `Hong Kong Cantonese Corpus <https://github.com/fcbond/hkcancor>`_
(HKCanCor; license: CC BY) is available via the function :func:`~pycantonese.hkcancor`:

.. code-block:: python

    import pycantonese
    hkcancor = pycantonese.hkcancor()
    hkcancor.n_files  # number of data files
    # 58
    len(hkcancor.words()) # number of words as segmented from all the utterances
    # 153656

HKCanCor is word-segmented and annotated for both Jyutping romanization
and part-of-speech tags.

The original HKCanCor source files are in an XML format.
They have been converted to CHAT for incorporation into PyCantonese.
On the format conversion, please consult this
`readme <https://github.com/jacksonllee/pycantonese/blob/main/src/pycantonese/data/hkcancor/README.md>`_.

CantoMap
^^^^^^^^

The `CantoMap <https://github.com/gwinterstein/CantoMap>`_ corpus
(license: GPL-3.0) is a collection of contemporary Hong Kong Cantonese
conversation recordings from MapTask exercises.
It is available via the function :func:`~pycantonese.cantomap`:

.. code-block:: python

    import pycantonese
    cantomap = pycantonese.cantomap()
    cantomap.n_files  # number of data files
    # 99
    len(cantomap.words())  # number of words as segmented from all the utterances
    # 118572

CantoMap is word-segmented and annotated for Jyutping romanization.
Part-of-speech tags (HKCanCor tagset) are added by PyCantonese's POS tagger
during the conversion from ELAN to CHAT format.

The original CantoMap source files are in the ELAN annotation format (``.eaf``).
Because the CHAT format inherently requires word-segmented data,
it is a natural fit for the word-segmented, Jyutping-annotated CantoMap data.
The ELAN files have been converted to CHAT for incorporation into PyCantonese.
On the format conversion, please consult this
`readme <https://github.com/jacksonllee/pycantonese/blob/main/src/pycantonese/data/cantomap/README.md>`_.


CHILDES and TalkBank Data
-------------------------

For corpora beyond the built-in ones, PyCantonese provides the function :func:`~pycantonese.read_chat`
to read in Cantonese data in the CHAT format.

As of 2026, CHAT datasets are publicly available from `TalkBank <https://talkbank.org/>`_.
If you visit the webpage of a specific dataset, you'll have to logged in (account setup is free)
before you can download the full transcripts as a ZIP archive to your local drive.

.. note::
    All publicly available TalkBank datasets are associated with
    the CC BY-NC-SA 3.0 license.

Here are the Cantonese-related TalkBank datasets (in alphabetical order):

* `Child Heritage Chinese Corpus <https://talkbank.org/childes/access/Biling/CHCC.html>`_

* `Guthrie Bilingual Corpus <https://talkbank.org/childes/access/Biling/Guthrie.html>`_

* `HKU-70 Corpus <https://talkbank.org/childes/access/Chinese/Cantonese/HKU.html>`_

* `Lee-Wong-Leung Corpus <https://talkbank.org/childes/access/Chinese/Cantonese/LeeWongLeung.html>`_

* `Mandarin-Cantonese-English EACMC Corpus <https://talkbank.org/childes/access/Biling/EACMC.html>`_

* `Yip-Matthews Bilingual Corpus <https://talkbank.org/childes/access/Biling/YipMatthews.html>`_


Custom Data
-----------

If you have your own CHAT data,
:func:`~pycantonese.read_chat` accepts a local ZIP archive,
a local directory, or a single ``.cha`` file path.

For more control over how data is read, the :class:`~pycantonese.CHAT` class
provides the following class methods:

* :py:meth:`~pycantonese.CHAT.from_zip` -- local ZIP archive
* :py:meth:`~pycantonese.CHAT.from_dir` -- local directory
* :py:meth:`~pycantonese.CHAT.from_files` -- one or more local file paths
* :py:meth:`~pycantonese.CHAT.from_strs` -- in-memory strings
* :py:meth:`~pycantonese.CHAT.from_git` -- Git repository (cloned and cached)
* :py:meth:`~pycantonese.CHAT.from_url` -- URL to a ZIP archive (downloaded and cached)

The CHAT parser is powered by `Rustling <https://docs.rustling.io/stable/chat.html>`_,
with Cantonese-specific additions for Jyutping romanization, Chinese characters,
and a general corpus search function.

If your data is in one of the
`formats supported by Rustling <https://docs.rustling.io/stable/>`_,
you can use Rustling to parse it, apply any processing you need,
and create a :class:`~pycantonese.CHAT` object via :py:meth:`~pycantonese.CHAT.from_strs`.
For an example of this workflow, see how the CantoMap ELAN data is
`converted for use in PyCantonese <https://github.com/jacksonllee/pycantonese/blob/main/src/pycantonese/data/cantomap/README.md>`_.
