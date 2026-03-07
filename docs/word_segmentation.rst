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
