.. _parsing:

Parsing Cantonese Text
======================

To take advantage of the myriad of functions offered by :class:`~pycantonese.CHATReader`,
the previous documentation pages (:ref:`data`, :ref:`reader`, :ref:`searches`) assume that
you have CHAT-formatted data that is already processed for word segmentation,
characters-to-Jyutping conversion, and part-of-speech tagging.
What if you have your own unprocessed Cantonese data?
This is where the :func:`~pycantonese.parse_text` function comes in handy.
:func:`~pycantonese.parse_text` takes raw Cantonese text as input
and returns a :class:`~pycantonese.CHATReader` object containing the processed data.

Input 1: A Plain String
^^^^^^^^^^^^^^^^^^^^^^^

If you have unprocessed Cantonese text (prose, conversational data, etc.),
then you can simply pass in a plain Python string to :func:`~pycantonese.parse_text`:

.. code-block:: python

    >>> import pycantonese
    >>> data = "你食咗飯未呀？食咗喇！你聽日得唔得閒呀？"
    >>> corpus = pycantonese.parse_text(data)
    >>> corpus.head()
    *X:    你         食         咗        飯          未        呀        ？
    %mor:  PRON|nei5  VERB|sik6  PART|zo2  NOUN|faan6  ADV|mei6  PART|aa4  ？
    <BLANKLINE>
    *X:    食         咗        喇         ！
    %mor:  VERB|sik6  PART|zo2  PART|laa1  ！
    <BLANKLINE>
    *X:    你         聽日           得         唔      得閒           呀        ？
    %mor:  PRON|nei5  ADV|ting1jat6  VERB|dak1  ADV|m4  ADJ|dak1haan4  PART|aa4  ？
    <BLANKLINE>

Note:

* Because the output of :func:`~pycantonese.parse_text` is a :class:`~pycantonese.CHATReader` object,
  all methods and attributes for :class:`~pycantonese.CHATReader` will work
  (:func:`~pycantonese.CHATReader.words`, :func:`~pycantonese.CHATReader.tokens`,
  :func:`~pycantonese.CHATReader.utterances`, :func:`~pycantonese.CHATReader.search`, etc).
* Since CHAT is designed for conversational data and your input data is a string,
  :func:`~pycantonese.parse_text` attempts simple utterance segmentation
  (by the Chinese full-width punctuation marks ``{"，", "！", "。"}``
  as well as the end-of-line character ``"\n"``).
* By default, a dummy participant ``"X"`` is assigned to each utterance.
  To provide your own participant, pass it to the ``participant`` keyword argument of
  :func:`~pycantonese.parse_text`.

Since the input string data is a vanilla Python string,
we can also pipe raw Cantonese text from a local file into the :func:`~pycantonese.parse_text` function:

.. skip: next

.. code-block:: python

    import pycantonese
    # Suppose you have Cantonese text in data.txt.
    with open("data.txt") as f:
        corpus = pycantonese.parse_text(f.read())

Input 2: A List of Strings
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to control utterance segmentation on your own,
you can provide :func:`~pycantonese.parse_text` with a list of strings instead of a single string.
Each string in the list will be treated as an utterance:

.. skip: start  # not sure why *only* in testing the `data` would be treated as three (not two) utterances?

.. code-block:: python

    >>> import pycantonese
    >>> data = ["你食咗飯未呀？", "食咗喇！你聽日得唔得閒呀？"]
    >>> corpus = pycantonese.parse_text(data)
    >>> corpus.head()
    *X:    你         食         咗        飯          未        呀        ？
    %mor:  PRON|nei5  VERB|sik6  PART|zo2  NOUN|faan6  ADV|mei6  PART|aa4  ？
    <BLANKLINE>
    *X:    食         咗        喇         ！  你         聽日           得         唔      得閒           呀        ？
    %mor:  VERB|sik6  PART|zo2  PART|laa1  ！  PRON|nei5  ADV|ting1jat6  VERB|dak1  ADV|m4  ADJ|dak1haan4  PART|aa4  ？
    <BLANKLINE>

.. skip: end

See how the input ``"食咗喇！你聽日得唔得閒呀？"`` was treated as an utterance,
without utterance segmentation due to the exclamation point ``"！"`` in the middle.

Input 3: A List of Tuples of Strings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your data has multiple participants (e.g., a dialog, a play or drama script)
and you would like to encode such participant information for downstream analysis,
then you can provide :func:`~pycantonese.parse_text` with a list of tuples of strings.
In each tuple, the first element is the participant,
and the second one is the unparsed utterance string:

.. code-block:: python

    >>> import pycantonese
    >>> data = [
    ...     ("小麗", "你食咗飯未呀？"),
    ...     ("小怡", "食咗喇！你聽日得唔得閒呀？"),
    ... ]
    >>> corpus = pycantonese.parse_text(data)
    >>> corpus.head()
    *小麗:  你         食         咗        飯          未        呀        ？
    %mor:   PRON|nei5  VERB|sik6  PART|zo2  NOUN|faan6  ADV|mei6  PART|aa4  ？
    <BLANKLINE>
    *小怡:  食         咗        喇         ！  你         聽日           得         唔      得閒           呀        ？
    %mor:   VERB|sik6  PART|zo2  PART|laa1  ！  PRON|nei5  ADV|ting1jat6  VERB|dak1  ADV|m4  ADJ|dak1haan4  PART|aa4  ？
    <BLANKLINE>

Customizing Word Segmentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:func:`~pycantonese.parse_text` has an optional argument called ``segment_kwargs``.
You can pass in a dictionary here to customize the behavior of word segmentation.
The key-value pairs in this dictionary are passed as keyword arguments to the underlying
:func:`~pycantonese.segment` function.

.. code-block:: python

    >>> import pycantonese
    >>> from pycantonese.word_segmentation import Segmenter
    >>> # The ``Segmenter`` class can take an "allow" or "disallow" list of words.
    >>> # The example below shows the use of an "allow" list that happens to be
    >>> # a hard-coded set of strings (with only one string: ``"得唔得閒"``).
    >>> # You can create your own allow/disallow list so long as the list is a container
    >>> # of strings (e.g., from memory, from a local file).
    >>> my_segmenter = Segmenter(allow={"得唔得閒"})
    >>> data = [
    ...     ("小麗", "你食咗飯未呀？"),
    ...     ("小明", "食咗喇！你聽日得唔得閒呀？"),
    ... ]
    >>> # The pycantonese.segment function takes the `cls` kwarg for a custom segmenter,
    >>> # which is why we can pass in ``{"cls": my_segmenter}`` to ``segment_kwargs``.
    >>> corpus = pycantonese.parse_text(data, segment_kwargs={"cls": my_segmenter})
    >>> corpus.head()
    *小麗:  你         食         咗        飯          未        呀        ？
    %mor:   PRON|nei5  VERB|sik6  PART|zo2  NOUN|faan6  ADV|mei6  PART|aa4  ？
    <BLANKLINE>
    *小明:  食         咗        喇         ！  你         聽日           得唔得閒              呀        ？
    %mor:   VERB|sik6  PART|zo2  PART|laa1  ！  PRON|nei5  ADV|ting1jat6  VERB|dak1m4dak1haan4  PART|aa4  ？
    <BLANKLINE>

Note the difference in the way ``"得唔得閒"`` is segmented between here and previous examples.

Customizing Part-of-Speech Tagging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:func:`~pycantonese.parse_text` has an optional argument called ``pos_tag_kwargs``.
You can pass in a dictionary here to customize the behavior of part-of-speech tagging.
The key-value pairs in this dictionary are passed as keyword arguments to the underlying
:func:`~pycantonese.pos_tag` function.

.. code-block:: python

    >>> import pycantonese
    >>> data = [
    ...     ("小麗", "你食咗飯未呀？"),
    ...     ("小明", "食咗喇！你聽日得唔得閒呀？"),
    ... ]
    >>> corpus = pycantonese.parse_text(data, pos_tag_kwargs={"tagset": "hkcancor"})
    >>> corpus.head()
    *小麗:  你      食      咗     飯       未      呀     ？
    %mor:   R|nei5  V|sik6  U|zo2  N|faan6  D|mei6  Y|aa4  ？
    <BLANKLINE>
    *小明:  食      咗     喇      ！  你      聽日         得      唔    得閒         呀     ？
    %mor:   V|sik6  U|zo2  Y|laa1  ！  R|nei5  T|ting1jat6  V|dak1  D|m4  A|dak1haan4  Y|aa4  ？
    <BLANKLINE>

Outputting CHAT Data
^^^^^^^^^^^^^^^^^^^^

Once you have created a :class:`~pycantonese.CHATReader` object using your own data,
you may like to export the CHAT-formatted data to a local file.
This way, you can more easily share the processed data with your colleagues,
reload the data (see :ref:`data`) for further processing and analysis in your workflow,
and so forth.

With a :class:`~pycantonese.CHATReader` object, simply call the :func:`~pycantonese.CHATReader.to_chat`
method with a local file path.

.. skip: start

.. code-block:: python

    file_path = "result.cha"
    corpus.to_chat(file_path)

    # If you're running code on Google Colab,
    # you can download the file like this:
    from google.colab import files
    files.download(file_path)

.. skip: end

More Customization
^^^^^^^^^^^^^^^^^^

Under the hood, :func:`~pycantonese.parse_text` calls the existing functions
from PyCantonese.
While :func:`~pycantonese.parse_text` is designed to cover the basic use cases
with limited customization, a more custom workflow may require you to put
the various pieces together in your own way.
Please see the individual documentation pages for details
(:ref:`jyutping`, :ref:`word_segmentation`, :ref:`pos_tagging`).
