.. _parsing:

Parsing Cantonese Text
======================

To take advantage of the myriad of functions offered by :class:`~pycantonese.CHAT`,
the previous documentation pages (:ref:`data`, :ref:`reader`, :ref:`searches`) assume that
you have CHAT-formatted data that is already processed for word segmentation,
characters-to-Jyutping conversion, and part-of-speech tagging.
What if you have your own unprocessed Cantonese data?
This is where the :func:`~pycantonese.parse_text` function comes in handy.
:func:`~pycantonese.parse_text` takes raw Cantonese text as input
and returns a :class:`~pycantonese.CHAT` object containing the processed data.

Input 1: A Plain String
^^^^^^^^^^^^^^^^^^^^^^^

If you have unprocessed Cantonese text (prose, conversational data, etc.),
then you can simply pass in a plain Python string to :func:`~pycantonese.parse_text`:

.. code-block:: python

    import pycantonese
    data = "你食咗飯未呀？食咗喇！你聽日得唔得閒呀？"
    corpus = pycantonese.parse_text(data)
    corpus.head()
    # *X:    你          食          咗         飯           未         呀         ？
    # %mor:  PRON|nei5  VERB|sik6  PART|zo2  NOUN|faan6  ADV|mei6  PART|aa4  ？
    #
    # *X:    食          咗         喇          ！
    # %mor:  VERB|sik6  PART|zo2  PART|laa3  ！
    #
    # *X:    你          聽日             得         唔       得閒             呀         ？
    # %mor:  PRON|nei5  ADV|ting1jat6  AUX|dak1  ADV|m4  ADJ|dak1haan4  PART|aa4  ？
    #

Note:

* Because the output of :func:`~pycantonese.parse_text` is a :class:`~pycantonese.CHAT` object,
  all methods and attributes for :class:`~pycantonese.CHAT` will work
  (:func:`~pycantonese.CHAT.words`, :func:`~pycantonese.CHAT.tokens`,
  :func:`~pycantonese.CHAT.utterances`, :func:`~pycantonese.CHAT.search`, etc).
* Since CHAT is designed for conversational data and your input data is a string,
  :func:`~pycantonese.parse_text` attempts simple utterance segmentation
  (by the Chinese full-width punctuation marks ``{"。", "！", "？"}``
  as well as the end-of-line character ``"\n"``).
* By default, a dummy participant ``"X"`` is assigned to each utterance.
  To provide your own participant, pass it to the ``participant`` keyword argument of
  :func:`~pycantonese.parse_text`.

Since the input string data is a vanilla Python string,
we can also pipe raw Cantonese text from a local file into the :func:`~pycantonese.parse_text` function:

.. skip: start

.. code-block:: python

    import pycantonese
    # Suppose you have Cantonese text in data.txt.
    with open("data.txt") as f:
        corpus = pycantonese.parse_text(f.read())

.. skip: end

Input 2: A List of Strings
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to control utterance segmentation on your own,
you can provide :func:`~pycantonese.parse_text` with a list of strings instead of a single string.
Each string in the list will be treated as an utterance:

.. code-block:: python

    import pycantonese
    data = ["你食咗飯未呀？", "食咗喇！你聽日得唔得閒呀？"]
    corpus = pycantonese.parse_text(data)
    corpus.head()
    # *X:    你          食          咗         飯           未         呀         ？
    # %mor:  PRON|nei5  VERB|sik6  PART|zo2  NOUN|faan6  ADV|mei6  PART|aa4  ？
    #
    # *X:    食          咗         喇          ！    你          聽日             得         唔       得閒             呀         ？
    # %mor:  VERB|sik6  PART|zo2  PART|laa3  ！    PRON|nei5  ADV|ting1jat6  AUX|dak1  ADV|m4  ADJ|dak1haan4  PART|aa4  ？
    #

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

    import pycantonese
    data = [
        ("小麗", "你食咗飯未呀？"),
        ("小怡", "食咗喇！你聽日得唔得閒呀？"),
    ]
    corpus = pycantonese.parse_text(data)
    corpus.head()
    # *小麗:      你          食          咗         飯           未         呀         ？
    # %mor:     PRON|nei5  VERB|sik6  PART|zo2  NOUN|faan6  ADV|mei6  PART|aa4  ？
    #
    # *小怡:      食          咗         喇          ！    你          聽日             得         唔       得閒             呀         ？
    # %mor:     VERB|sik6  PART|zo2  PART|laa3  ！    PRON|nei5  ADV|ting1jat6  AUX|dak1  ADV|m4  ADJ|dak1haan4  PART|aa4  ？
    #

Customizing Part-of-Speech Tagging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:func:`~pycantonese.parse_text` has an optional argument called ``pos_tag_kwargs``.
You can pass in a dictionary here to customize the behavior of part-of-speech tagging.
The key-value pairs in this dictionary are passed as keyword arguments to the underlying
:func:`~pycantonese.pos_tag` function.

.. code-block:: python

    import pycantonese
    data = [
        ("小麗", "你食咗飯未呀？"),
        ("小明", "食咗喇！你聽日得唔得閒呀？"),
    ]
    corpus = pycantonese.parse_text(data, pos_tag_kwargs={"tagset": "hkcancor"})
    corpus.head()
    # *小麗:      你       食       咗      飯        未       呀      ？
    # %mor:     r|nei5  v|sik6  u|zo2  n|faan6  d|mei6  y|aa4  ？
    #
    # *小明:      食       咗      喇       ！    你       聽日           得        唔     得閒           呀      ？
    # %mor:     v|sik6  u|zo2  y|laa3  ！    r|nei5  t|ting1jat6  vu|dak1  d|m4  a|dak1haan4  y|aa4  ？
    #

Outputting CHAT Data
^^^^^^^^^^^^^^^^^^^^

Once you have created a :class:`~pycantonese.CHAT` object using your own data,
you may like to export the CHAT-formatted data to a local file.
This way, you can more easily share the processed data with your colleagues,
reload the data (see :ref:`data`) for further processing and analysis in your workflow,
and so forth.

With a :class:`~pycantonese.CHAT` object, simply call the :func:`~pycantonese.CHAT.to_files`
method with a local directory path.

.. skip: start

.. code-block:: python

    dir_path = "output"
    corpus.to_files(dir_path)

.. skip: end

More Customization
^^^^^^^^^^^^^^^^^^

Under the hood, :func:`~pycantonese.parse_text` calls the existing functions
from PyCantonese.
While :func:`~pycantonese.parse_text` is designed to cover the basic use cases,
you may create a custom workflow by putting
the various pieces together in your own way.
Please see the individual documentation pages for details
(:ref:`jyutping`, :ref:`word_segmentation`, :ref:`pos_tagging`).
