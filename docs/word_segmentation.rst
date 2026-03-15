.. _word_segmentation:

Word Segmentation
=================

By convention, Cantonese is not written with word boundaries (like spaces in English).
However, in many natural language processing tasks, it is often necessary to
work with a segmented form of Cantonese data.
PyCantonese provides the function :func:`~pycantonese.segment` that takes an
unsegmented text string in Cantonese characters and returns
the segmented version:

.. code-block:: python

    import pycantonese
    pycantonese.segment("廣東話容唔容易學？")  # Is Cantonese easy to learn?
    # ['廣東話', '容', '唔', '容易', '學', '？']

The word segmentation is powered by a Jieba-styled, semi-supervised
hybrid approach that combines a directed acyclic graph and a hidden Markov model.
The segmenter is trained by HKCanCor, rime-cantonese, Common Voice Cantonese,
and Cantonese-Traditional Chinese Parallel Corpus.

Character Offsets
-----------------

Pass ``offsets=True`` to get each word paired with its ``(start, end)``
character offsets into the original string (exclusive end, like Python slices).
This is useful when you need to map segmented words back to their positions
in the source text:

.. code-block:: python

    pycantonese.segment("廣東話容唔容易學？", offsets=True)
    # [('廣東話', (0, 3)), ('容', (3, 4)), ('唔', (4, 5)),
    #  ('容易', (5, 7)), ('學', (7, 8)), ('？', (8, 9))]

The offsets reference the original input string, so you can recover
any word with a simple slice:

.. code-block:: python

    text = "廣東話容唔容易學？"
    for word, (start, end) in pycantonese.segment(text, offsets=True):
        assert text[start:end] == word
