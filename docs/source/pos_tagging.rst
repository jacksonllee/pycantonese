.. _pos_tagging:

Part-of-Speech Tagging
======================

.. versionadded:: 3.1.0

.. warning::
    As of November 2020, PyCantonese v3.1.0 hasn't been released yet.
    All functionality related to part-of-speech tagging
    is available only through the GitHub repository for early testers.
    Everything (what functions are provided, how they behave) is subject to
    change while it is still under active development.
    To download and install this (unstable) version of PyCantonese
    (the ``--pre`` flag means a pre-release version):

    .. code-block:: bash

        $ pip install --pre --upgrade pycantonese

    Running ``import pycantonese as pc; print(pc.__version__)`` will show a
    version number similar to ``3.1.0.dev2``.

    If you notice any issues, please don't hesitate to
    `report them <https://pycantonese.org/#links>`_.

    While the documentation below is minimal for now, it is going to be updated
    and expanded once the part-of-speech tagging functionality is finalized
    in a new PyCantonese release.

:func:`~pycantonese.pos_tag`
tags words in a segmented sentence or phrase for their parts of speech.

:func:`~pycantonese.pos_tagging.hkcancor_to_ud`
maps a part-of-speech tag from HKCanCor to Universal Dependencies v2.
