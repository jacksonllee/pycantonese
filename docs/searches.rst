..  _searches:

Corpus Search Queries
=====================

A common task in corpus-based linguistic work
is to search for specific elements of interest.
PyCantonese provides the general-purpose
:func:`~pycantonese.CHAT.search`
as a corpus object method.
For a given corpus, it can search for specific Jyutping elements,
Chinese characters, part-of-speech tags, and any combinations of these.

:func:`~pycantonese.CHAT.search`
is also capable of grabbing the
neighboring words and utterances
around the match word. This is
useful for a wide variety of purposes, e.g., syntax,
semantics, word collocation, discourse analysis, conversation analysis, etc.

The following examples show how
:func:`~pycantonese.CHAT.search`
works using its parameters.
We'll use the built-in HKCanCor corpus.

.. code-block:: python

    import pycantonese
    corpus = pycantonese.hkcancor()

Searching by a Jyutping Element
-------------------------------

Search queries
by various parsed Jyutping elements are possible by specifying a Jyutping parameter
in the
:func:`~pycantonese.CHAT.search` call.

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

    aa = corpus.search(nucleus='aa')
    len(aa)  # number of matching results found
    # 22328
    aa[: 5]  # show first 5 results
    # [Token(word='啊', pos='y', jyutping='aa3', mor=None, gloss=None, gra=None),
    #  Token(word='啊', pos='y', jyutping='aa3', mor=None, gloss=None, gra=None),
    #  Token(word='淡季', pos='an', jyutping='daam6gwai3', mor=None, gloss=None, gra=None),
    #  Token(word='𡃉', pos='y', jyutping='gaa3', mor=None, gloss=None, gra=None),
    #  Token(word='嗱', pos='y', jyutping='laa4', mor=None, gloss=None, gra=None)]

The ``tone`` parameter:

.. code-block:: python

    tone2 = corpus.search(tone='2')
    len(tone2)
    # 21167
    tone2[: 5]
    # [Token(word='講', pos='v', jyutping='gong2', mor=None, gloss=None, gra=None),
    #  Token(word='嗰個', pos='r', jyutping='go2go3', mor=None, gloss=None, gra=None),
    #  Token(word='嗰個', pos='r', jyutping='go2go3', mor=None, gloss=None, gra=None),
    #  Token(word='好', pos='d', jyutping='hou2', mor=None, gloss=None, gra=None),
    #  Token(word='抵', pos='a', jyutping='dai2', mor=None, gloss=None, gra=None)]

The parameters ``onset``, ``nucleus``, ``coda``, ``tone``, and ``initial``
may take a regular expression for more powerful search queries.
For instance, we may ask for all words that contain any of the codas {p, t, k}.
``[ptk]`` as regex means to match any of these letters,
and we set it to be the value of the ``coda`` parameter:

.. code-block:: python

    codas_ptk = corpus.search(coda='[ptk]')
    len(codas_ptk)
    # 12715
    codas_ptk[: 5]
    # [Token(word='迪士尼', pos='nt', jyutping='dik6si6nei4', mor=None, gloss=None, gra=None),
    #  Token(word='直程', pos='d', jyutping='zik6cing4', mor=None, gloss=None, gra=None),
    #  Token(word='七', pos='m', jyutping='cat1', mor=None, gloss=None, gra=None),
    #  Token(word='八月', pos='t', jyutping='baat3jyut6', mor=None, gloss=None, gra=None),
    #  Token(word='日', pos='q', jyutping='jat6', mor=None, gloss=None, gra=None)]

For regular expressions in Python, see
`here <https://docs.python.org/3/library/re.html>`_.


The search criteria can be mixed in a single
:func:`~pycantonese.CHAT.search`
call, with the following constraints:

* If ``jyutping`` is used, no other Jyutping search parameters can be used.
* If ``final`` is used, neither ``nucleus`` nor ``coda`` can be used.

Searching by a Chinese Character
--------------------------------

Search queries for a given Chinese character are performed by the ``character``
parameter:

.. code-block:: python

    machine = corpus.search(character='機')
    len(machine)
    # 195
    machine[: 5]
    # [Token(word='機票', pos='n', jyutping='gei1piu3', mor=None, gloss=None, gra=None),
    #  Token(word='機票', pos='n', jyutping='gei1piu3', mor=None, gloss=None, gra=None),
    #  Token(word='機票', pos='n', jyutping='gei1piu3', mor=None, gloss=None, gra=None),
    #  Token(word='飛機', pos='n', jyutping='fei1gei1', mor=None, gloss=None, gra=None),
    #  Token(word='機', pos='Ng', jyutping='gei1', mor=None, gloss=None, gra=None)]

Searching by a Part-of-speech Tag
---------------------------------

With the parameter ``pos`` in
:func:`~pycantonese.CHAT.search`,
verbs which bear the part-of-speech tag "v" in HKCanCor
can be accessed as follows:

.. code-block:: python

    verbs = corpus.search(pos='v')
    len(verbs)
    # 29884
    verbs[: 5]
    # [Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #  Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #  Token(word='旅行', pos='vn', jyutping='leoi5hang4', mor=None, gloss=None, gra=None),
    #  Token(word='有冇', pos='v1', jyutping='jau5mou5', mor=None, gloss=None, gra=None),
    #  Token(word='要', pos='vu', jyutping='jiu3', mor=None, gloss=None, gra=None)]

The ``pos`` parameter may take a regular expression. For instance,
we can use ``'^v'`` to match any part-of-speech tags that begin with "v" for
different kinds of verbs annotated in HKCanCor:

.. code-block:: python

    all_verbs = corpus.search(pos='^v')
    len(all_verbs)  ## number of all verbs -- more than just "v" alone above
    # 29663
    all_verbs[:20]  ## printing the first 20 results
    # [Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #  Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #  Token(word='旅行', pos='vn', jyutping='leoi5hang4', mor=None, gloss=None, gra=None),
    #  Token(word='有冇', pos='v1', jyutping='jau5mou5', mor=None, gloss=None, gra=None),
    #  Token(word='要', pos='vu', jyutping='jiu3', mor=None, gloss=None, gra=None),
    #  Token(word='有得', pos='vu', jyutping='jau5dak1', mor=None, gloss=None, gra=None),
    #  Token(word='冇得', pos='vu', jyutping='mou5dak1', mor=None, gloss=None, gra=None),
    #  Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #  Token(word='係', pos='v', jyutping='hai6', mor=None, gloss=None, gra=None),
    #  Token(word='係', pos='v', jyutping='hai6', mor=None, gloss=None, gra=None),
    #  Token(word='聽', pos='v', jyutping='teng1', mor=None, gloss=None, gra=None),
    #  Token(word='講', pos='v', jyutping='gong2', mor=None, gloss=None, gra=None),
    #  Token(word='話', pos='v', jyutping='waa6', mor=None, gloss=None, gra=None),
    #  Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #  Token(word='玩', pos='v', jyutping='waan2', mor=None, gloss=None, gra=None),
    #  Token(word='可以', pos='vu', jyutping='ho2ji5', mor=None, gloss=None, gra=None),
    #  Token(word='住', pos='v', jyutping='zyu6', mor=None, gloss=None, gra=None),
    #  Token(word='話', pos='v', jyutping='waa6', mor=None, gloss=None, gra=None),
    #  Token(word='跟', pos='v', jyutping='gan1', mor=None, gloss=None, gra=None),
    #  Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None)]

For regular expressions in Python, see
`here <https://docs.python.org/3/library/re.html>`_.

For the part-of-speech tagset used by HKCanCor, see `here <https://github.com/fcbond/hkcancor>`_.

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

    gwo3 = corpus.search(character='過', word_range=(1, 2))
    len(gwo3)
    # 705
    gwo3[:5]
    # [[Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #   Token(word='過', pos='u', jyutping='gwo3', mor=None, gloss=None, gra=None),
    #   Token(word='喇', pos='y', jyutping='laa1', mor=None, gloss=None, gra=None),
    #   Token(word='.', pos='', jyutping=None, mor=None, gloss=None, gra=None)],
    #  [Token(word='不過', pos='c', jyutping='bat1gwo3', mor=None, gloss=None, gra=None),
    #   Token(word='幾', pos='m', jyutping='gei2', mor=None, gloss=None, gra=None),
    #   Token(word='日', pos='q', jyutping='jat6', mor=None, gloss=None, gra=None)],
    #  [Token(word='去', pos='vk', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #   Token(word='過', pos='v', jyutping='gwo3', mor=None, gloss=None, gra=None),
    #   Token(word='嗰邊', pos='r', jyutping='go2bin1', mor=None, gloss=None, gra=None),
    #   Token(word='瞓覺', pos='v', jyutping='fan3gaau3', mor=None, gloss=None, gra=None)],
    #  [Token(word='不過', pos='c', jyutping='bat1gwo3', mor=None, gloss=None, gra=None),
    #   Token(word='都', pos='d', jyutping='dou1', mor=None, gloss=None, gra=None),
    #   Token(word=',', pos='', jyutping=None, mor=None, gloss=None, gra=None)],
    #  [Token(word=',', pos='', jyutping=None, mor=None, gloss=None, gra=None),
    #   Token(word='不過', pos='c', jyutping='bat1gwo3', mor=None, gloss=None, gra=None),
    #   Token(word='真係', pos='d', jyutping='zan1hai6', mor=None, gloss=None, gra=None),
    #   Token(word='好', pos='d', jyutping='hou2', mor=None, gloss=None, gra=None)]]

``utterance_range``:

.. code-block:: python

    laa1 = corpus.search(jyutping='laa1', utterance_range=(1, 1))
    len(laa1)
    # 1681
    laa1[0]  ## print the 1st result
    # [[Token(word='係', pos='v', jyutping='hai6', mor=None, gloss=None, gra=None),
    #   Token(word='唔係', pos='v', jyutping='m4hai6', mor=None, gloss=None, gra=None),
    #   Token(word='啊', pos='y', jyutping='aa3', mor=None, gloss=None, gra=None),
    #   Token(word='?', pos='', jyutping=None, mor=None, gloss=None, gra=None)],
    #  [Token(word='你', pos='r', jyutping='nei5', mor=None, gloss=None, gra=None),
    #   Token(word='都', pos='d', jyutping='dou1', mor=None, gloss=None, gra=None),
    #   Token(word='去', pos='v', jyutping='heoi3', mor=None, gloss=None, gra=None),
    #   Token(word='過', pos='u', jyutping='gwo3', mor=None, gloss=None, gra=None),
    #   Token(word='喇', pos='y', jyutping='laa1', mor=None, gloss=None, gra=None),
    #   Token(word='.', pos='', jyutping=None, mor=None, gloss=None, gra=None)],
    #  [Token(word='咪', pos='c', jyutping='mai6', mor=None, gloss=None, gra=None),
    #   Token(word='係', pos='v', jyutping='hai6', mor=None, gloss=None, gra=None),
    #   Token(word='囖', pos='y', jyutping='lo1', mor=None, gloss=None, gra=None),
    #   Token(word='.', pos='', jyutping=None, mor=None, gloss=None, gra=None)]]


If ``utterance_range`` is not ``(0, 0)``, ``word_range`` is ignored since full
utterances are already in the output.

Searching by Multiple Criteria
------------------------------

:func:`~pycantonese.CHAT.search`
is flexible and allows multiple parameters described
above to be specified at the same time.
For instance, if we are interested in *pinjam* ("changed tone") in Cantonese,
we may be interested in all words with coda {p, t, k} plus tone 2 (high-rising):

.. code-block:: python

    ptk_tone2 = corpus.search(coda='[ptk]', tone='2')
    len(ptk_tone2)
    # 71
    ptk_tone2[: 10]
    # [Token(word='雀', pos='n', jyutping='zoek2', mor=None, gloss=None, gra=None),
    #  Token(word='雀', pos='n', jyutping='zoek2', mor=None, gloss=None, gra=None),
    #  Token(word='綠', pos='a', jyutping='luk2', mor=None, gloss=None, gra=None),
    #  Token(word='賊', pos='n', jyutping='caak2', mor=None, gloss=None, gra=None),
    #  Token(word='dut2', pos='o', jyutping='dut2', mor=None, gloss=None, gra=None),
    #  Token(word='碟', pos='n', jyutping='dip2', mor=None, gloss=None, gra=None),
    #  Token(word='碟', pos='n', jyutping='dip2', mor=None, gloss=None, gra=None),
    #  Token(word='碟', pos='n', jyutping='dip2', mor=None, gloss=None, gra=None),
    #  Token(word='碟形', pos='n', jyutping='dip2jing4', mor=None, gloss=None, gra=None),
    #  Token(word='碟', pos='n', jyutping='dip2', mor=None, gloss=None, gra=None)]

Output Format of Search Results
-------------------------------

While
:func:`~pycantonese.CHAT.search`
always returns a list, the format of the elements in the list
can be adjusted by the parameters ``by_token`` and ``by_utterance``.

If ``by_token`` is ``True`` (default), words are all represented in the token
format with Jyutping and part-of-speech tags,
as in all the examples above. Otherwise, words are text strings with
Chinese characters only.

If ``by_utterance`` is ``False`` (default), the elements in the output list are words
(or spans of words when ``word_range`` is used). Otherwise, all utterances
containing a match word are in the output list. If ``utterance_range`` is used,
``by_utterance`` is automatically ``True``.

Complex Searches
----------------

By design, :func:`~pycantonese.CHAT.search` targets a *single* match word.
If your use case needs to involve more, you'll have to write your custom code
to iterate through the data and keep track of whatever is of your interest.
As you have complete control over the search logic,
the search can be as customized as desired,
to the extent that what you're after can be formulated in terms of
what the corpus data and annotations provide.

For examples of complex searches,
please check out the tutorials from :ref:`archives`.
