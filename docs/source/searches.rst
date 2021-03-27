..  _searches:

Corpus Search Queries
=====================

A common task in corpus-based linguistic work
is to search for specific elements of interest.
PyCantonese provides the general-purpose
:func:`~pycantonese.CHATReader.search`
as a corpus object method.
For a given corpus, it can search for specific Jyutping elements,
Chinese characters, part-of-speech tags, and any combinations of these.

:func:`~pycantonese.CHATReader.search`
is also capable of grabbing the
neighboring words and utterances
around the match word. This is
useful for a wide variety of purposes, e.g., syntax,
semantics, word collocation, discourse analysis, conversation analysis, etc.

By design, :func:`~pycantonese.CHATReader.search` targets a *single* match word.
If your use case needs to involve more, you'll have to write your custom code
to iterate through the data and keep track of whatever is of your interest.
For example, if you are to find all instances of [verb + verb particles]
because you'd like to study verb particles and their distribution with
particular verbs, then you can loop through the tokens
(from :func:`~pycantonese.CHATReader.tokens`) with a two-token sliding window and
keep instances where the first token is a verb and the second a particle
(tokens give you the part-of-speech information).

The following examples show how
:func:`~pycantonese.CHATReader.search`
works using its parameters.
We'll use the built-in HKCanCor corpus.

.. code-block:: python

    >>> import pycantonese
    >>> corpus = pycantonese.hkcancor()


.. _search_jyutping:

Searching by a Jyutping Element
-------------------------------

Search queries
by various parsed Jyutping elements are possible by specifying a Jyutping parameter
in the
:func:`~pycantonese.CHATReader.search` call.

The Jyutping parameters are:

* ``onset``
* ``nucleus``
* ``coda``
* ``tone``
* ``initial`` (聲母, equivalent to ``onset``)
* ``final`` (韻母, equivalent to nucleus + coda)
* ``jyutping`` (a complete Jyutping romanization, i.e., onset + nucleus + coda + tone)


For example, for the nucleus "aa":

.. code-block:: python

    >>> aa = corpus.search(nucleus='aa')
    >>> len(aa)  # number of matching results found
    22328
    >>> aa[: 5]  # show first 5 results
    [Token(word='啊', pos='Y', jyutping='aa3', mor=None, gra=None),
     Token(word='啊', pos='Y', jyutping='aa3', mor=None, gra=None),
     Token(word='淡季', pos='AN', jyutping='daam6gwai3', mor=None, gra=None),
     Token(word='𡃉', pos='Y', jyutping='gaa3', mor=None, gra=None),
     Token(word='嗱', pos='Y', jyutping='laa4', mor=None, gra=None)]

The ``tone`` parameter:

.. code-block:: python

    >>> tone2 = corpus.search(tone='2')
    >>> len(tone2)
    21167
    >>> tone2[: 5]
    [Token(word='講', pos='V', jyutping='gong2', mor=None, gra=None),
     Token(word='嗰個', pos='R', jyutping='go2go3', mor=None, gra=None),
     Token(word='嗰個', pos='R', jyutping='go2go3', mor=None, gra=None),
     Token(word='好', pos='D', jyutping='hou2', mor=None, gra=None),
     Token(word='抵', pos='A', jyutping='dai2', mor=None, gra=None)]

The parameters ``onset``, ``nucleus``, ``coda``, ``tone``, and ``initial``
may take a regular expression for more powerful search queries.
For instance, we may ask for all words that contain any of the codas {p, t, k}.
``[ptk]`` as regex means to match any of these letters,
and we set it to be the value of the ``coda`` parameter:

    >>> codas_ptk = corpus.search(coda='[ptk]')
    >>> len(codas_ptk)
    12715
    >>> codas_ptk[: 5]
    [Token(word='迪士尼', pos='NT', jyutping='dik6si6nei4', mor=None, gra=None),
     Token(word='直程', pos='D', jyutping='zik6cing4', mor=None, gra=None),
     Token(word='七', pos='M', jyutping='cat1', mor=None, gra=None),
     Token(word='八月', pos='T', jyutping='baat3jyut6', mor=None, gra=None),
     Token(word='日', pos='Q', jyutping='jat6', mor=None, gra=None)]

For regular expressions in Python, see
`here <https://docs.python.org/3/library/re.html>`_.


The search criteria can be mixed in a single
:func:`~pycantonese.CHATReader.search`
call, with the following constraints:

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
    195
    >>> machine[: 5]
    [Token(word='機票', pos='N', jyutping='gei1piu3', mor=None, gra=None),
     Token(word='機票', pos='N', jyutping='gei1piu3', mor=None, gra=None),
     Token(word='機票', pos='N', jyutping='gei1piu3', mor=None, gra=None),
     Token(word='飛機', pos='N', jyutping='fei1gei1', mor=None, gra=None),
     Token(word='機', pos='NG', jyutping='gei1', mor=None, gra=None)]

.. _search_pos:

Searching by a Part-of-speech Tag
---------------------------------

With the parameter ``pos`` in
:func:`~pycantonese.CHATReader.search`,
verbs which bear the part-of-speech tag "V" in HKCanCor
can be accessed as follows:

.. code-block:: python

    >>> verbs = corpus.search(pos='V')
    >>> len(verbs)
    29954
    >>> verbs[: 5]
    [Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
     Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
     Token(word='旅行', pos='VN', jyutping='leoi5hang4', mor=None, gra=None),
     Token(word='有冇', pos='V1', jyutping='jau5mou5', mor=None, gra=None),
     Token(word='要', pos='VU', jyutping='jiu3', mor=None, gra=None)]

The ``pos`` parameter may take a regular expression. For instance,
we can use ``'^V'`` to match any part-of-speech tags that begin with "V" for
different kinds of verbs annotated in HKCanCor:

.. code-block:: python

    >>> all_verbs = corpus.search(pos='^V')
    >>> len(all_verbs)  # number of all verbs -- more than just "V" alone above
    29726
    >>> all_verbs[:20]  # printing the first 20 results
    [Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
     Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
     Token(word='旅行', pos='VN', jyutping='leoi5hang4', mor=None, gra=None),
     Token(word='有冇', pos='V1', jyutping='jau5mou5', mor=None, gra=None),
     Token(word='要', pos='VU', jyutping='jiu3', mor=None, gra=None),
     Token(word='有得', pos='VU', jyutping='jau5dak1', mor=None, gra=None),
     Token(word='冇得', pos='VU', jyutping='mou5dak1', mor=None, gra=None),
     Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
     Token(word='係', pos='V', jyutping='hai6', mor=None, gra=None),
     Token(word='係', pos='V', jyutping='hai6', mor=None, gra=None),
     Token(word='聽', pos='V', jyutping='teng1', mor=None, gra=None),
     Token(word='講', pos='V', jyutping='gong2', mor=None, gra=None),
     Token(word='話', pos='V', jyutping='waa6', mor=None, gra=None),
     Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
     Token(word='玩', pos='V', jyutping='waan2', mor=None, gra=None),
     Token(word='可以', pos='VU', jyutping='ho2ji5', mor=None, gra=None),
     Token(word='住', pos='V', jyutping='zyu6', mor=None, gra=None),
     Token(word='話', pos='V', jyutping='waa6', mor=None, gra=None),
     Token(word='跟', pos='V', jyutping='gan1', mor=None, gra=None),
     Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None)]

For regular expressions in Python, see
`here <https://docs.python.org/3/library/re.html>`_.

For the part-of-speech tagset used by HKCanCor, see `here <http://compling.hss.ntu.edu.sg/hkcancor/>`_.

.. _search_range:

Searching by a Word or Utterance Range
--------------------------------------

It is possible to include in search results the neighboring words and utterances
around a match word. This functionality is useful for syntax,
semantics, and discourse-level research.

The parameters ``word_range`` and ``utterance_range`` each take a tuple of
(int, int).

``word_range`` defaults to ``(0, 0)``, for zeros words (the first ``0``)
to the left of a match word, and zeros words (the second ``0``)
to the right -- all within the same utterance.
Likewise, ``utterance_range`` defaults to ``(0, 0)`` for zero utterances
preceding the utterance containing the match word and zero utterances following it.

``word_range``:

.. code-block:: python

    >>> gwo3 = corpus.search(character='過', word_range=(1, 2))
    >>> len(gwo3)
    705
    >>> gwo3[:5]
    [[Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
      Token(word='過', pos='U', jyutping='gwo3', mor=None, gra=None),
      Token(word='喇', pos='Y', jyutping='laa1', mor=None, gra=None),
      Token(word='.', pos='.', jyutping=None, mor=None, gra=None)],
     [Token(word='不過', pos='C', jyutping='bat1gwo3', mor=None, gra=None),
      Token(word='幾', pos='M', jyutping='gei2', mor=None, gra=None),
      Token(word='日', pos='Q', jyutping='jat6', mor=None, gra=None)],
     [Token(word='去', pos='VK', jyutping='heoi3', mor=None, gra=None),
      Token(word='過', pos='V', jyutping='gwo3', mor=None, gra=None),
      Token(word='嗰邊', pos='R', jyutping='go2bin1', mor=None, gra=None),
      Token(word='瞓覺', pos='V', jyutping='fan3gaau3', mor=None, gra=None)],
     [Token(word='不過', pos='C', jyutping='bat1gwo3', mor=None, gra=None),
      Token(word='都', pos='D', jyutping='dou1', mor=None, gra=None),
      Token(word=',', pos=',', jyutping=None, mor=None, gra=None)],
     [Token(word=',', pos=',', jyutping=None, mor=None, gra=None),
      Token(word='不過', pos='C', jyutping='bat1gwo3', mor=None, gra=None),
      Token(word='真係', pos='D', jyutping='zan1hai6', mor=None, gra=None),
      Token(word='好', pos='D', jyutping='hou2', mor=None, gra=None)]]

``utterance_range``:

.. code-block:: python

    >>> laa1 = corpus.search(jyutping='laa1', utterance_range=(1, 1))
    >>> len(laa1)
    1681
    >>> laa1[0]  # print the 1st result
    [[Token(word='係', pos='V', jyutping='hai6', mor=None, gra=None),
      Token(word='唔係', pos='V', jyutping='m4hai6', mor=None, gra=None),
      Token(word='啊', pos='Y', jyutping='aa3', mor=None, gra=None),
      Token(word='?', pos='?', jyutping=None, mor=None, gra=None)],
     [Token(word='你', pos='R', jyutping='nei5', mor=None, gra=None),
      Token(word='都', pos='D', jyutping='dou1', mor=None, gra=None),
      Token(word='去', pos='V', jyutping='heoi3', mor=None, gra=None),
      Token(word='過', pos='U', jyutping='gwo3', mor=None, gra=None),
      Token(word='喇', pos='Y', jyutping='laa1', mor=None, gra=None),
      Token(word='.', pos='.', jyutping=None, mor=None, gra=None)],
     [Token(word='咪', pos='C', jyutping='mai6', mor=None, gra=None),
      Token(word='係', pos='V', jyutping='hai6', mor=None, gra=None),
      Token(word='囖', pos='Y', jyutping='lo1', mor=None, gra=None),
      Token(word='.', pos='.', jyutping=None, mor=None, gra=None)]]


If ``utterance_range`` is not ``(0, 0)``, ``word_range`` is ignored since full
utterances are already in the output.

.. _search_combination:

Searching by Multiple Criteria
------------------------------

:func:`~pycantonese.CHATReader.search`
is flexible and allows multiple parameters described
above to be specified at the same time.
For instance, if we are interested in *pinjam* ("changed tone") in Cantonese,
we may be interested in all words with coda {p, t, k} plus tone 2 (high-rising):

.. code-block:: python

    >>> ptk_tone2 = corpus.search(coda='[ptk]', tone='2')
    >>> len(ptk_tone2)
    71
    >>> ptk_tone2[: 10]
    [Token(word='雀', pos='N', jyutping='zoek2', mor=None, gra=None),
     Token(word='雀', pos='N', jyutping='zoek2', mor=None, gra=None),
     Token(word='綠', pos='A', jyutping='luk2', mor=None, gra=None),
     Token(word='賊', pos='N', jyutping='caak2', mor=None, gra=None),
     Token(word='dut2', pos='O', jyutping='dut2', mor=None, gra=None),
     Token(word='碟', pos='N', jyutping='dip2', mor=None, gra=None),
     Token(word='碟', pos='N', jyutping='dip2', mor=None, gra=None),
     Token(word='碟', pos='N', jyutping='dip2', mor=None, gra=None),
     Token(word='碟形', pos='N', jyutping='dip2jing4', mor=None, gra=None),
     Token(word='碟', pos='N', jyutping='dip2', mor=None, gra=None)]

.. _search_format:

Output Format of Search Results
-------------------------------

While
:func:`~pycantonese.CHATReader.search`
always returns a list, the format of the elements in the list
can be adjusted by the parameters ``by_tokens`` and ``by_utterances``.

If ``by_tokens`` is ``True`` (default), words are all represented in the token
format with Jyutping and part-of-speech tags,
as in all the examples above. Otherwise, words are text strings with
Chinese characters only.

If ``by_utterances`` is ``False`` (default), the elements in the output list are words
(or spans of words when ``word_range`` is used). Otherwise, all utterances
containing a match word are in the output list. If ``utterance_range`` is used,
``by_utterances`` is automatically ``True``.
