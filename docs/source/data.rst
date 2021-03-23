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
For these reasons, PyCantonese adopts the `CHAT <https://talkbank.org/manuals/CHAT.pdf>`_
corpus format from CHILDES and TalkBank.
CHAT is widely used, well-documented, and rich for linguistic annotations.
PyCantonese uses the Python library
`PyLangAcq <https://pylangacq.org/>`_ to parse CHAT data files.
For a primer on CHAT, please see
`here <https://pylangacq.org/transcriptions.html#chat-format>`_.


Built-in Data
-------------

Currently, PyCantonese comes with one built-in corpus, the
`Hong Kong Cantonese Corpus <http://compling.hss.ntu.edu.sg/hkcancor/>`_
(HKCanCor; license: CC BY), via the function :func:`~pycantonese.hkcancor`:

.. code-block:: python

    >>> import pycantonese
    >>> hkcancor = pycantonese.hkcancor()
    >>> hkcancor.n_files()  # number of data files
    58
    >>> len(hkcancor.words()) # number of words as segmented from all the utterances
    153654

HKCanCor is word-segmented and annotated for both Jyutping romanization
and part-of-speech tags.

The original HKCanCor source files are in an XML format.
They have been converted to CHAT for incorporation into PyCantonese.
On the format conversion, please consult this
`readme <https://github.com/jacksonllee/pycantonese/blob/main/pycantonese/data/hkcancor/README.md>`_.


CHILDES and TalkBank Data
-------------------------

For corpora other than HKCanCor, PyCantonese provides the function :func:`~pycantonese.read_chat`
to read in Cantonese data in the CHAT format.

:func:`~pycantonese.read_chat` is designed to be able to read in CHAT data
from a URL that points to a ZIP file containing ``.cha`` CHAT files.
The availability of Cantonese CHAT data from CHILDES and TalkBank
means that it is possible to conveniently obtain and work with such data right from
your own Python code, without having to manually download or unzip anything.

All publicly available CHILDES and TalkBank datasets are associated with
the CC BY-NC-SA 3.0 license.

As of March 2021, the following Cantonese-related datasets are
available from CHILDES and TalkBank (in alphabetical order):

.. invisible-code-block: python

    >>> import os

.. skip: start if(os.getenv("CI") == "true", reason="certain CHILDES data pulls fail in some but not all python versions for unknown reasons")

* `Child Heritage Chinese Corpus <https://childes.talkbank.org/access/Biling/CHCC.html>`_

    .. code-block:: python

        >>> url = "https://childes.talkbank.org/data/Biling/CHCC.zip"
        >>> corpus = pycantonese.read_chat(url)
        >>> corpus.n_files()
        190
        >>> len(corpus.words())
        533877

* `Guthrie Bilingual Corpus <https://childes.talkbank.org/access/Biling/Guthrie.html>`_

    .. code-block:: python

        >>> url = "https://childes.talkbank.org/data/Biling/Guthrie.zip"
        >>> corpus = pycantonese.read_chat(url)
        >>> corpus.n_files()
        36
        >>> len(corpus.words())
        70438

* `HKU-70 Corpus <https://childes.talkbank.org/access/Chinese/Cantonese/HKU.html>`_

    .. code-block:: python

        >>> url = "https://childes.talkbank.org/data/Chinese/Cantonese/HKU.zip"
        >>> corpus = pycantonese.read_chat(url)
        >>> corpus.n_files()
        70
        >>> len(corpus.words())
        178270

* `Lee-Wong-Leung Corpus <https://childes.talkbank.org/access/Chinese/Cantonese/LeeWongLeung.html>`_

    .. code-block:: python

        >>> url = "https://childes.talkbank.org/data/Chinese/Cantonese/LeeWongLeung.zip"
        >>> corpus = pycantonese.read_chat(url)
        >>> corpus.n_files()
        161
        >>> len(corpus.words())
        1177307

* `Leo Corpus <https://childes.talkbank.org/access/Biling/Leo.html>`_

    .. code-block:: python

        >>> url = "https://childes.talkbank.org/data/Biling/Leo.zip"
        >>> corpus = pycantonese.read_chat(url)
        >>> corpus.n_files()
        54
        >>> len(corpus.words())
        223415

* `Paidologos Corpus: Cantonese <https://phonbank.talkbank.org/access/Chinese/Cantonese/PaidoCantonese.html>`_

    .. code-block:: python

        >>> url = "https://phonbank.talkbank.org/data/Chinese/Cantonese/PaidoCantonese.zip"
        >>> corpus = pycantonese.read_chat(url)
        >>> corpus.n_files()
        160
        >>> len(corpus.words())
        16730

* `Yip-Matthews Bilingual Corpus <https://childes.talkbank.org/access/Biling/YipMatthews.html>`_

    .. code-block:: python

        >>> url = "https://childes.talkbank.org/data/Biling/YipMatthews.zip"
        >>> corpus = pycantonese.read_chat(url)
        >>> corpus.n_files()
        501
        >>> len(corpus.words())
        1949480

.. skip: end


Custom Data
-----------

If you have a Cantonese corpus in the CHAT format in your local drive and would
like to use PyCantonese to handle it, :func:`~pycantonese.read_chat`
takes a path that can be a ZIP file, a local directory, or a single CHAT file.

If more fine-grained control is needed when reading data, please check out
:class:`~pycantonese.CHATReader`, particularly the following classmethods:

* :func:`~pycantonese.CHATReader.from_zip`
* :func:`~pycantonese.CHATReader.from_dir`
* :func:`~pycantonese.CHATReader.from_files`
* :func:`~pycantonese.CHATReader.from_strs`

Since PyCantonese uses PyLangAcq for CHAT data reading and parsing under the hood,
PyCantonese's :func:`~pycantonese.read_chat` and :class:`~pycantonese.CHATReader`
function the same way as their counterparts in PyLangAcq.
For more on reading CHAT data in general, please see
`PyLangAcq's documentation <https://pylangacq.org/read.html>`_.
