PyCantonese: Cantonese Linguistics and NLP in Python
====================================================

.. start-raw-directive

.. raw:: html

    <img src="https://jacksonllee.com/logos/pycantonese-logo.png" width="250px">

.. end-raw-directive

Full Documentation: https://pycantonese.org

|

.. image:: https://badge.fury.io/py/pycantonese.svg
   :target: https://pypi.python.org/pypi/pycantonese
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pycantonese.svg
   :target: https://pypi.python.org/pypi/pycantonese
   :alt: Supported Python versions

.. image:: https://circleci.com/gh/jacksonllee/pycantonese/tree/master.svg?style=svg
   :target: https://circleci.com/gh/jacksonllee/pycantonese/tree/master
   :alt: Build

|

.. start-sphinx-website-index-page

PyCantonese is a Python library for Cantonese linguistics and natural language
processing (NLP). Currently implemented features (more to come!):

- Accessing and searching corpus data
- Parsing and conversion tools for Jyutping romanization
- Stop words
- Word segmentation
- Part-of-speech tagging

Quick Examples
--------------

With PyCantonese imported:

.. code-block:: python

    >>> import pycantonese as pc

1. Word segmentation

.. code-block:: python

    >>> pc.segment("廣東話好難學？")  # Is Cantonese difficult to learn?
    ['廣東話', '好', '難', '學', '？']

2. Conversion from Cantonese characters to Jyutping

.. code-block:: python

    >>> pc.characters_to_jyutping('香港人講廣東話')  # Hongkongers speak Cantonese
    [("香港人", "hoeng1gong2jan4"), ("講", "gong2"), ("廣東話", "gwong2dung1waa2")]

3. Finding all verbs in the HKCanCor corpus

   In this example,
   we search for the regular expression ``'^V'`` for all words whose
   part-of-speech tag begins with "V" in the original HKCanCor annotations:

.. code-block:: python

    >>> corpus = pc.hkcancor() # get HKCanCor
    >>> all_verbs = corpus.search(pos='^V')
    >>> len(all_verbs)  # number of all verbs
    29012
    >>> from pprint import pprint
    >>> pprint(all_verbs[:10])  # print 10 results
    [('去', 'V', 'heoi3', ''),
     ('去', 'V', 'heoi3', ''),
     ('旅行', 'VN', 'leoi5hang4', ''),
     ('有冇', 'V1', 'jau5mou5', ''),
     ('要', 'VU', 'jiu3', ''),
     ('有得', 'VU', 'jau5dak1', ''),
     ('冇得', 'VU', 'mou5dak1', ''),
     ('去', 'V', 'heoi3', ''),
     ('係', 'V', 'hai6', ''),
     ('係', 'V', 'hai6', '')]

4. Parsing Jyutping for (onset, nucleus, coda, tone)

.. code-block:: python

    >>> pc.parse_jyutping('gwong2dung1waa2')  # 廣東話
    [('gw', 'o', 'ng', '2'), ('d', 'u', 'ng', '1'), ('w', 'aa', '', '2')]

Download and Install
--------------------

PyCantonese requires Python 3.6 or above.
To download and install the stable, most recent version::

    $ pip install --upgrade pycantonese

To test your installation in the Python interpreter:

.. code-block:: python

    >>> import pycantonese as pc
    >>> pc.__version__  # show version number

Links
-----

* Source code: https://github.com/jacksonllee/pycantonese
* Bug tracker, feature requests: https://github.com/jacksonllee/pycantonese/issues
* Email: Please contact `Jackson Lee <https://jacksonllee.com>`_.
* Social media: Updates, tips, and more are posted on the Facebook page below.

.. start-raw-directive

.. raw:: html

    <div id="fb-root"></div>
    <script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v8.0" nonce="4Dv3gcYx"></script>
    <div class="fb-page" data-href="https://www.facebook.com/pycantonese/" data-tabs="timeline" data-width="" data-height="" data-small-header="true" data-adapt-container-width="true" data-hide-cover="false" data-show-facepile="true">
        <blockquote cite="https://www.facebook.com/pycantonese/" class="fb-xfbml-parse-ignore"><a href="https://www.facebook.com/pycantonese/">PyCantonese: Cantonese Linguistics and NLP in Python</a></blockquote>
    </div>

.. end-raw-directive

|

How to Cite
-----------

PyCantonese is authored and mainteined by `Jackson L. Lee <https://jacksonllee.com>`_.

A talk introducing PyCantonese:

Lee, Jackson L. 2015. PyCantonese: Cantonese linguistic research in the age of big data.
Talk at the Childhood Bilingualism Research Centre, Chinese University of Hong Kong. September 15. 2015.
`Notes+slides <https://pycantonese.org/papers/Lee-pycantonese-2015.html>`_

License
-------

MIT License. Please see ``LICENSE.txt`` in the GitHub source code for details.

The HKCanCor dataset included in PyCantonese is substantially modified from
its source in terms of format. The original dataset has a CC BY license.
Please see ``pycantonese/data/hkcancor/README.md``
in the GitHub source code for details.

The rime-cantonese data (release 2020.09.09) is
incorporated into PyCantonese for word segmentation and
characters-to-Jyutping conversion.
This data has a CC BY 4.0 license.
Please see ``pycantonese/data/rime_cantonese/README.md``
in the GitHub source code for details.

Logo
----

The PyCantonese logo is the Chinese character 粵 meaning Cantonese,
with artistic design by albino.snowman (Instagram handle).

Acknowledgments
---------------

Individuals who have contributed feedback, bug reports, etc.
(in alphabetical order of last names if known):

- @cathug
- Litong Chen
- @g-traveller
- Rachel Han
- Ryan Lai
- Charles Lam
- Hill Ma
- @richielo
- @rylanchiu
- Stephan Stiller
- Tsz-Him Tsui

.. end-sphinx-website-index-page

Changelog
---------

Please see ``CHANGELOG.md``.

Setting up a Development Environment
------------------------------------

The latest code under development is available on Github at
`jacksonllee/pycantonese <https://github.com/jacksonllee/pycantonese>`_.
You need to have `Git LFS <https://git-lfs.github.com/>`_ installed on your system.
To obtain this version for experimental features or for development:

.. code-block:: bash

   $ git clone https://github.com/jacksonllee/pycantonese.git
   $ cd pycantonese
   $ git lfs pull
   $ pip install -r dev-requirements.txt
   $ pip install -e .

To run tests and styling checks:

.. code-block:: bash

   $ pytest -vv --doctest-modules --cov=pycantonese pycantonese docs
   $ flake8 pycantonese
   $ black --check --line-length=79 pycantonese

To build the documentation website files:

.. code-block:: bash

    $ python build_docs.py
