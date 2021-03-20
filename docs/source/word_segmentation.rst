.. _word_segmentation:

Word Segmentation
=================

.. versionadded:: 2.4.0

By convention, Cantonese is not written with word boundaries (like spaces in English).
However, in many natural language processing tasks, it is often necessary to
work with a segmented form of Cantonese data.
PyCantonese provides the function :func:`~pycantonese.segment` that takes an
unsegmented text string in Cantonese characters and returns
the segmented version:

.. code-block:: python

    >>> import pycantonese
    >>> pycantonese.segment("廣東話容唔容易學？")  # Is Cantonese easy to learn?
    ['廣東話', '容', '唔', '容易', '學', '？']

Currently, the underlying word segmentation model is a simple longest string
matching algorithm, trained by
(i) the HKCanCor corpus data included in this library and
(ii) the rime-cantonese data (the 2020.09.09 release, CC BY 4.0 license).
The segmentation is constrained such that the resulting words
contain no more than five characters.

Customizing Segmentation
------------------------

.. versionadded:: 3.0.0

Because the current implementation of word segmentation depends entirely on
whether a potential word is found in the training data,
there are situations where you would like to explicitly allow or disallow
certain potential words.
To this end, the :func:`~pycantonese.segment` function has the ``cls`` keyword argument
(think: the ``cls`` kwarg for ``json.load``)
that takes a :class:`~pycantonese.word_segmentation.Segmenter` object
for customizing in the following ways:

* To specify words to allow, pass an iterable of word strings to the
  ``allow`` keyword argument of :class:`~pycantonese.word_segmentation.Segmenter`:

    .. code-block:: python

        >>> import pycantonese
        >>> from pycantonese.word_segmentation import Segmenter
        >>> segmenter = Segmenter(allow={"容唔容易"})
        >>> pycantonese.segment("廣東話容唔容易學？", cls=segmenter)
        ['廣東話', '容唔容易', '學', '？']

* To specify words to disallow, pass an iterable of word strings to the
  ``disallow`` keyword argument of :class:`~pycantonese.word_segmentation.Segmenter`:

    .. code-block:: python

        >>> import pycantonese
        >>> from pycantonese.word_segmentation import Segmenter
        >>> segmenter = Segmenter(disallow={"廣東話"})
        >>> # 廣東 still exists as a word in the model, though 廣東話 is banned here.
        >>> pycantonese.segment("廣東話容唔容易學？", cls=segmenter)
        ['廣東', '話', '容', '唔', '容易', '學', '？']

* To control the maximum word length (default: 5), pass an integer to the
  ``max_word_length`` keyword argument of :class:`~pycantonese.word_segmentation.Segmenter`:

    .. code-block:: python

        >>> import pycantonese
        >>> from pycantonese.word_segmentation import Segmenter
        >>> segmenter = Segmenter(max_word_length=2)
        >>> pycantonese.segment("廣東話容唔容易學？", cls=segmenter)
        ['廣東', '話', '容', '唔', '容易', '學', '？']

The keyword arguments ``allow``, ``disallow``, and ``max_word_length``
of the :class:`~pycantonese.word_segmentation.Segmenter` class
can be concurrently used in the same :class:`~pycantonese.word_segmentation.Segmenter`
instance.
