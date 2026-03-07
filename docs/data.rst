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
`Rustling <https://rustling.readthedocs.io/stable/chat.html>`_ to parse CHAT data files.
For a primer on the CHAT data format, please see
`here <https://docs.pylangacq.org/stable/transcriptions.html#chat-format>`_.


Built-in Data
-------------

Currently, PyCantonese comes with one built-in corpus, the
`Hong Kong Cantonese Corpus <https://github.com/fcbond/hkcancor>`_
(HKCanCor; license: CC BY), via the function :func:`~pycantonese.hkcancor`:

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


CHILDES and TalkBank Data
-------------------------

For corpora other than HKCanCor, PyCantonese provides the function :func:`~pycantonese.read_chat`
to read in Cantonese data in the CHAT format.

As of 2026, CHAT datasets are publicly available from `TalkBank <https://talkbank.org/>`_.
If you visit the webpage of a specific dataset, you'll have to logged in (account setup is free)
before you can download the full transcripts as a ZIP archive to your local drive.

.. note::
    All publicly available TalkBank datasets are associated with
    the CC BY-NC-SA 3.0 license.

Here are the Cantonese-related TalkBank datasets (in alphabetical order):

* `Child Heritage Chinese Corpus <https://childes.talkbank.org/access/Biling/CHCC.html>`_

* `Guthrie Bilingual Corpus <https://childes.talkbank.org/access/Biling/Guthrie.html>`_

* `HKU-70 Corpus <https://childes.talkbank.org/access/Chinese/Cantonese/HKU.html>`_

* `Lee-Wong-Leung Corpus <https://childes.talkbank.org/access/Chinese/Cantonese/LeeWongLeung.html>`_

* `Mandarin-Cantonese-English EACMC Corpus <https://talkbank.org/childes/access/Biling/EACMC.html>`_

* `Yip-Matthews Bilingual Corpus <https://childes.talkbank.org/access/Biling/YipMatthews.html>`_


Custom Data
-----------

If you have your own CHAT data locally and would
like PyCantonese to handle it, :func:`~pycantonese.read_chat`
takes a path that can be a ZIP archive, a local directory, or a single CHAT file.

If more fine-grained control is needed when reading data, please check out
:class:`~pycantonese.CHAT`, particularly the following methods:

* :py:meth:`~pycantonese.CHAT.from_zip`
* :py:meth:`~pycantonese.CHAT.from_dir`
* :py:meth:`~pycantonese.CHAT.from_files`
* :py:meth:`~pycantonese.CHAT.from_strs`

The CHAT parser comes from `Rustling <https://rustling.readthedocs.io/stable/chat.html>`_,
which both PyCantonese and PyLangAcq use.
For more on reading CHAT data in general, please see
`PyLangAcq's documentation <https://docs.pylangacq.org/stable/read.html>`_.
