.. _word_segmentation:

Word Segmentation
=================

By convention, Cantonese is not written with word boundaries (like spaces in English).
However, in many natural language processing tasks, it is often necessary to
work with a segmented form of Cantonese data.
PyCantonese provides the function ``segment()`` that takes an
unsegmented string in Cantonese characters and returns
the segmented version:

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.segment("廣東話容唔容易學？")  # "Is Cantonese easy to learn?"
    ['廣東話', '容', '唔容易', '學', '？']

Currently, the underlying word segmentation model is a simple longest string
matching algorithm, trained by
(i) the HKCanCor corpus data included in this library and
(ii) the rime-cantonese data (the 2020.09.09 release, CC BY license).
The segmentation is constrained such that the resulting words
contain no more than five characters.
Given the current implementation, any multi-character words unseen in the training data
would not be segmented as such.
