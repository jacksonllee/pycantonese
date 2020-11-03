.. _stop_words:

Stop Words
==========

.. versionadded:: 2.2.0

In many natural language processing tasks, it is often necessary to filter
stop words, English examples of which include function words such as
pronouns and determiners. PyCantonese provides the function
:func:`~pycantonese.stop_words`
that returns a set of about 100 Cantonese stop words:

.. code-block:: python

    >>> import pycantonese as pc
    >>> stop_words = pc.stop_words()
    >>> len(stop_words)
    104
    >>> stop_words
    {'一啲', '一定', '不如', '不過', ...}

Depending on your use cases, you may like to add or remove stop words
from the default ones.
The :func:`~pycantonese.stop_words` function has the optional arguments of
``add`` and ``remove``.

``add`` can either be a string (e.g., treat ``"香港"`` as a stop word if your
data is all about Hong Kong) or an iterable of strings:

.. code-block:: python

    >>> import pycantonese as pc
    >>> stop_words_1 = pc.stop_words(add='香港')
    >>> len(stop_words_1)
    105
    >>> '香港' in stop_words_1
    True
    >>> stop_words_2 = pc.stop_words(add=['香港島', '九龍', '新界'])
    >>> len(stop_words_2)
    >>> 107
    >>> {'香港島', '九龍', '新界'}.issubset(stop_words_2)
    True

Similarly, the ``remove`` argument can also take either a string or an iterable
of strings.
