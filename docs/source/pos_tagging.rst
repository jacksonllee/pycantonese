.. _pos_tagging:

Part-of-Speech Tagging
======================

A basic part-of-speech tagger is provided by :func:`~pycantonese.pos_tag`,
which takes a segmented phrase or sentence as the input:

.. code-block:: python

    >>> import pycantonese
    >>> unsegmented = '我噚日買嗰對鞋。'  # I bought that pair of shoes yesterday.
    >>> segmented = pycantonese.segment(unsegmented)
    >>> segmented
    ['我', '噚日', '買', '嗰', '對', '鞋', '。']
    >>> pycantonese.pos_tag(segmented)
    [('我', 'PRON'), ('噚日', 'ADV'), ('買', 'VERB'), ('嗰', 'PRON'), ('對', 'NOUN'), ('鞋', 'NOUN'), ('。', 'PUNCT')]

The part-of-speech tagger uses the averaged perceptron model trained on
HKCanCor data.
HKCanCor has already been annotated for part-of-speech tags,
with a tagset of over 100 tags
(`46 of which are described <http://compling.hss.ntu.edu.sg/hkcancor/>`_).
By default, :func:`~pycantonese.pos_tag` maps the HKCanCor tagset to the
Universal Dependencies v2 tagset
(`with 17 tags <https://universaldependencies.org/u/pos/index.html>`_),
for cross-linguistic natural language processing work.
If you would like the original HKCanCor tagset,
:func:`~pycantonese.pos_tag` accepts the keyword argument ``tagset``:

.. code-block:: python

    >>> pycantonese.pos_tag(segmented, tagset="hkcancor")
    [('我', 'R'), ('噚日', 'T'), ('買', 'V'), ('嗰', 'R'), ('對', 'Q'), ('鞋', 'N'), ('。', '。')]

The helper function :func:`~pycantonese.pos_tagging.hkcancor_to_ud`
exposes the tagset mapping from HKCanCor to Universal Dependencies.

Due to the statistical nature of part-of-speech tagging,
the quality of results from :func:`~pycantonese.pos_tag` depends on
(i) the training data,
(ii) the quality of word segmentation, since the function expects a *segmented* input.
Currently, a major limitation is the fact that HKCanCor is perhaps still
the only Cantonese corpus with a permissive license that comes annotated
with part-of-speech tags.
Its relatively small size (about 150,000 tagged words) means that models
more sophisticated than a standard averaged perceptron approach wouldn't be worth it.
If you think the results from :func:`~pycantonese.pos_tag` are odd,
it is potentially due to the HKCanCor training data
(e.g., specific occurrences of word + tag combinations might have thrown off the tagger),
or the quality of word segmentation, especially if your segmented input comes from
:func:`~pycantonese.segment`
-- please `get in touch <https://pycantonese.org/index.html#links>`_
if you would like further investigation.
