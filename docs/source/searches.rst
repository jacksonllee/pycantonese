..  _searches:

Corpus Search Queries
=====================

A common task in corpus-based linguistic work
is to search for specific elements of interest.
PyCantonese provides the general-purpose
:func:`~pycantonese.corpus.CantoneseCHATReader.search`
as a corpus object method.
For a given corpus, it can search for specific Jyutping elements,
Chinese characters, part-of-speech tags, and any combinations of these.

:func:`~pycantonese.corpus.CantoneseCHATReader.search`
is also capable of (so to speak) grabbing the
neighboring words and utterances
around the match word. This is
useful for a wide variety of purposes, e.g., syntax,
semantics, word collocation, discourse analysis, conversation analysis, etc.

All the following examples assume that a corpus object ``corpus`` for HKCanCor
has been created, and that ``pprint()`` is used for pretty print.

.. code-block:: python

    >>> from pprint import pprint
    >>> import pycantonese as pc
    >>> corpus = pc.hkcancor()
    >>> len(corpus.words())  # total number of words
    149781
    >>> len(corpus.characters())  # total number of Chinese characters
    186888

The following examples show how
:func:`~pycantonese.corpus.CantoneseCHATReader.search`
works using its array of parameters.

* :ref:`search_jyutping`
* :ref:`search_character`
* :ref:`search_pos`
* :ref:`search_range`
* :ref:`search_combination`
* :ref:`search_format`


.. _search_jyutping:

Searching by a Jyutping Element
-------------------------------

Search queries
by various parsed Jyutping elements are possible by passing a parameter
with its value to
:func:`~pycantonese.corpus.CantoneseCHATReader.search`.

The Jyutping parameters are:

* ``onset``
* ``nucleus``
* ``coda``
* ``tone``
* ``initial`` (聲母, equivalent to ``onset``)
* ``final`` (韻母, equivalent to nucleus+coda)
* ``jyutping`` (a complete Jyutping romanization, onset+nucleus+coda+tone)


For example, for the nucleus "aa":

.. code-block:: python

    >>> aa = corpus.search(nucleus='aa')
    >>> len(aa)  # number of matching results found
    21830
    >>> pprint(aa[: 5])  # show first 5 results
    [('啊', 'Y', 'aa3', ''),
     ('啊', 'Y', 'aa3', ''),
     ('淡季', 'AN', 'daam6gwai3', ''),
     ('𡃉', 'Y', 'gaa3', ''),
     ('嗱', 'Y', 'laa4', '')]

The ``tone`` parameter takes a str but not an int:

.. code-block:: python

    >>> tone2 = corpus.search(tone='2')
    >>> len(tone2)
    20579
    >>> pprint(tone2[: 5])
    [('講', 'V', 'gong2', ''),
     ('嗰個', 'R', 'go2go3', ''),
     ('嗰個', 'R', 'go2go3', ''),
     ('好', 'D', 'hou2', ''),
     ('抵', 'A', 'dai2', '')]

The parameters ``onset``, ``nucleus``, ``coda``, ``tone``, and ``initial``
may take a regular expression for more powerful search queries.
For instance, we may ask for all words that contain any of the codas {p, t, k}.
``[ptk]`` can be used for regular expression matching for any of these letters,
and we set it to be the value of the ``coda`` parameter:

    >>> codas_ptk = corpus.search(coda='[ptk]')
    >>> len(codas_ptk)
    12409
    >>> pprint(codas_ptk[: 5])
    [('迪士尼', 'NT', 'dik6si6nei4', ''),
     ('直程', 'D', 'zik6cing4', ''),
     ('七', 'M', 'cat1', ''),
     ('八月', 'T', 'baat3jyut6', ''),
     ('日', 'Q', 'jat6', '')]

For regular expressions in Python, see
`here <https://docs.python.org/3/library/re.html>`_.


The search criteria can be mixed in a single
:func:`~pycantonese.corpus.CantoneseCHATReader.search`
call.
However, in order to avoid possible conflicts,
restrictions are imposed on the combination of Jyutping-related search criteria:

* If ``jyutping`` is used, no other Jyutping search parameters can be used.
* If ``final`` is used, neither ``nucleus`` nor ``coda`` can be used.

.. _search_character:

Searching by a Chinese Character
--------------------------------

Search queries for a given Chinese character are performed by the ``character``
parameter:

.. code-block:: python

    >>> machine = corpus.search(character='機')
    >>> len(machine)
    184
    >>> pprint(machine[: 5])
    [('機票', 'N', 'gei1piu3', ''),
     ('機票', 'N', 'gei1piu3', ''),
     ('機票', 'N', 'gei1piu3', ''),
     ('飛機', 'N', 'fei1gei1', ''),
     ('機', 'NG', 'gei1', '')]

.. _search_pos:

Searching by a Part-of-speech Tag
---------------------------------

With the parameter ``pos`` in
:func:`~pycantonese.corpus.CantoneseCHATReader.search`,
verbs which bear the part-of-speech tag "V" in HKCanCor
can be accessed as follows:

.. code-block:: python

    >>> verbs = corpus.search(pos='V')
    >>> len(verbs)
    29229
    >>> pprint(verbs[: 5])
    [('去', 'V', 'heoi3', ''),
     ('去', 'V', 'heoi3', ''),
     ('旅行', 'VN', 'leoi5hang4', ''),
     ('有冇', 'V1', 'jau5mou5', ''),
     ('要', 'VU', 'jiu3', '')]

The ``pos`` parameter may take a regular expression. For instance,
we can use ``'^V'`` to match any part-of-speech tags that begin with "V" for
different kinds of verbs annotated in HKCanCor:

.. code-block:: python

    >>> all_verbs = corpus.search(pos='^V')
    >>> len(all_verbs)  # number of all verbs -- more than just "V" alone above
    29012
    >>> pprint(all_verbs[:20])  # printing the first 20 results
    [('去', 'V', 'heoi3', ''),
     ('去', 'V', 'heoi3', ''),
     ('旅行', 'VN', 'leoi5hang4', ''),
     ('有冇', 'V1', 'jau5mou5', ''),
     ('要', 'VU', 'jiu3', ''),
     ('有得', 'VU', 'jau5dak1', ''),
     ('冇得', 'VU', 'mou5dak1', ''),
     ('去', 'V', 'heoi3', ''),
     ('係', 'V', 'hai6', ''),
     ('係', 'V', 'hai6', ''),
     ('聽', 'V', 'teng1', ''),
     ('講', 'V', 'gong2', ''),
     ('話', 'V', 'waa6', ''),
     ('去', 'V', 'heoi3', ''),
     ('玩', 'V', 'waan2', ''),
     ('可以', 'VU', 'ho2ji5', ''),
     ('住', 'V', 'zyu6', ''),
     ('話', 'V', 'waa6', ''),
     ('跟', 'V', 'gan1', ''),
     ('去', 'V', 'heoi3', '')]

For regular expressions in Python, see
`here <https://docs.python.org/3/library/re.html>`_.

For the part-of-speech tagset used by HKCanCor, see `here <http://compling.hss.ntu.edu.sg/hkcancor/>`_.

.. _search_range:

Searching by a Word or Sentence Range
-------------------------------------

It is possible to include in search results the neighboring words and sentences
with respect to a match word. This functionality is useful for syntax,
semantics, and discourse-level research.

The parameters ``word_range`` and ``sent_range`` each take a tuple of
(int, int).

``word_range`` defaults to ``(0, 0)`` for 0 *words*
(the first ``0``)
on the left of a match word and 0 *words* (the second ``0``)
on the right -- all within the same sent (= sentence).
Likewise, ``sent_range`` defaults to ``(0, 0)`` for 0 *sents*
preceding the sent containing the match word and 0 *sents* following it.

For ``word_range``:

.. code-block:: python

    >>> gwo3 = corpus.search(character='過', word_range=(1, 2))  # use u'過' instead in python 2
    >>> len(gwo3)
    679
    >>> pprint(gwo3[:5])
    [[('去', 'V', 'heoi3', ''),
      ('過', 'U', 'gwo3', ''),
      ('喇', 'Y', 'laa1', ''),
      ('.', '.', '', '')],
     [('不過', 'C', 'bat1gwo3', ''), ('幾', 'M', 'gei2', ''), ('日', 'Q', 'jat6', '')],
     [('去', 'VK', 'heoi3', ''),
      ('過', 'V', 'gwo3', ''),
      ('嗰邊', 'R', 'go2bin1', ''),
      ('瞓覺', 'V', 'fan3gaau3', '')],
     [('不過', 'C', 'bat1gwo3', ''), ('都', 'D', 'dou1', ''), (',', ',', '', '')],
     [(',', ',', '', ''),
      ('不過', 'C', 'bat1gwo3', ''),
      ('真係', 'D', 'zan1hai6', ''),
      ('好', 'D', 'hou2', '')]]

Note that the return object is list(list(tagged words)) when ``word_range``
is used. Also, the words that ``word_range`` specifies do not
cross sentence boundaries.

For ``sent_range``:

.. code-block:: python

    >>> laa1 = corpus.search(jyutping='laa1', sent_range=(1, 1))
    >>> len(laa1)
    1601
    >>> pprint(laa1[0])  # print the 1st result
    [[('係', 'V', 'hai6', ''),
      ('唔係', 'V', 'm4hai6', ''),
      ('啊', 'Y', 'aa3', ''),
      ('?', '?', '', '')],
     [('你', 'R', 'nei5', ''),
      ('都', 'D', 'dou1', ''),
      ('去', 'V', 'heoi3', ''),
      ('過', 'U', 'gwo3', ''),
      ('喇', 'Y', 'laa1', ''),
      ('.', '.', '', '')],
     [('咪', 'C', 'mai6', ''),
      ('係', 'V', 'hai6', ''),
      ('囖', 'Y', 'lo1', ''),
      ('.', '.', '', '')]]

If ``sent_range`` is not ``(0, 0)``, ``word_range`` is ignored (as full
sentences are in the output anyway).

.. _search_combination:

Searching by Multiple Criteria
------------------------------

:func:`~pycantonese.corpus.CantoneseCHATReader.search`
is flexible and allows multiple parameters described
above to be specified at the same time.
For instance, if we are interested in *pinjam* ("tone change") in Cantonese,
we may be interested in all words with coda {p, t, k} plus tone 2 (high-rising):

.. code-block:: python

    >>> ptk_tone2 = corpus.search(coda='[ptk]', tone='2')
    >>> len(ptk_tone2)
    70
    >>> pprint(ptk_tone2[: 10])
    [('雀', 'N', 'zoek2', ''),
     ('雀', 'N', 'zoek2', ''),
     ('綠', 'A', 'luk2', ''),
     ('dut2', 'O', 'dut2', ''),
     ('碟', 'N', 'dip2', ''),
     ('碟', 'N', 'dip2', ''),
     ('碟', 'N', 'dip2', ''),
     ('碟形', 'N', 'dip2jing4', ''),
     ('碟', 'N', 'dip2', ''),
     ('soek2', 'O', 'soek2', '')]

.. _search_format:

Output Format of Search Results
-------------------------------

While
:func:`~pycantonese.corpus.CantoneseCHATReader.search`
always returns a list, the format of the elements in the list
can be adjusted by the parameters ``tagged`` and ``sents``.

If ``tagged`` is ``True`` (default), words are all represented in the "tagged"
format of (word, part-of-speech tag, Jyutping, rel),
as in all the examples above. Otherwise, words are word token strings with
Chinese characters only.

If ``sents`` is ``False`` (default), the elements in the output list are words
(or spans of words when ``word_range`` is used). Otherwise, all sents
containing a match word are in the output list. If ``sent_range`` is used,
``sents`` is automatically ``True``.
