PyCantonese: Cantonese Linguistics and NLP in Python
====================================================

.. image:: https://jacksonllee.com/logos/pycantonese-logo.png
   :width: 250px

Full Documentation: https://pycantonese.org

|

.. image:: https://badge.fury.io/py/pycantonese.svg
   :target: https://pypi.python.org/pypi/pycantonese
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pycantonese.svg
   :target: https://pypi.python.org/pypi/pycantonese
   :alt: Supported Python versions

.. image:: https://circleci.com/gh/jacksonllee/pycantonese.svg?style=shield
   :target: https://circleci.com/gh/jacksonllee/pycantonese
   :alt: CircleCI Builds

|

.. start-sphinx-website-index-page

PyCantonese is a Python library for Cantonese linguistics and natural language
processing (NLP). Currently implemented features (more to come!):

- Accessing and searching corpus data
- Parsing and conversion tools for Jyutping romanization
- Parsing Cantonese text
- Stop words
- Word segmentation
- Part-of-speech tagging

.. _download_install:

Download and Install
--------------------

To download and install the stable, most recent version::

    $ pip install --upgrade pycantonese

Ready for more?
Check out the `Quickstart <https://pycantonese.org/quickstart.html>`_ page.

Consulting
----------

If your team would like professional assistance in using PyCantonese,
freelance consulting and training services are available for both academic and commercial groups.
Please email `Jackson L. Lee <https://jacksonllee.com>`_.

Support
-------

If you have found PyCantonese useful and would like to offer support,
`buying me a coffee <https://www.buymeacoffee.com/pycantonese>`_ would go a long way!

Links
-----

* Source code: https://github.com/jacksonllee/pycantonese
* Bug tracker: https://github.com/jacksonllee/pycantonese/issues
* Social media:
  `Facebook <https://www.facebook.com/pycantonese>`_
  and `Twitter <https://twitter.com/pycantonese>`_

How to Cite
-----------

PyCantonese is authored and maintained by `Jackson L. Lee <https://jacksonllee.com>`_.

Lee, Jackson L., Litong Chen, Charles Lam, Chaak Ming Lau, and Tsz-Him Tsui. 2022.
`PyCantonese: Cantonese Linguistics and NLP in Python <https://jacksonllee.com/papers/pycantonese_lrec_2022-05-06.pdf>`_.
*Proceedings of the 13th Language Resources and Evaluation Conference*.

.. code-block:: latex

      @inproceedings{lee-etal-2022-pycantonese,
         title = "PyCantonese: Cantonese Linguistics and NLP in Python",
         author = "Lee, Jackson L.  and
            Chen, Litong  and
            Lam, Charles  and
            Lau, Chaak Ming  and
            Tsui, Tsz-Him",
         booktitle = "Proceedings of The 13th Language Resources and Evaluation Conference",
         month = june,
         year = "2022",
         publisher = "European Language Resources Association",
         language = "English",
      }

License
-------

MIT License. Please see ``LICENSE.txt`` in the GitHub source code for details.

The HKCanCor dataset included in PyCantonese is substantially modified from
its source in terms of format. The original dataset has a CC BY license.
Please see ``pycantonese/data/hkcancor/README.md``
in the GitHub source code for details.

The rime-cantonese data (release 2021.05.16) is
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

Wonderful resources with a permissive license that have been incorporated into PyCantonese:

- HKCanCor
- rime-cantonese

Individuals who have contributed feedback, bug reports, etc.
(in alphabetical order of last names):

- @cathug
- Jenny Chim
- @g-traveller
- Rachel Han
- Ryan Lai
- @ZhanruiLiang
- Hill Ma
- @richielo
- @rylanchiu
- Stephan Stiller
- Robin Yuen

.. end-sphinx-website-index-page

Changelog
---------

Please see ``CHANGELOG.md``.

Setting up a Development Environment
------------------------------------

This section is only relevant
if you would like to mess with the PyCantonese source code itself.
Most users of PyCantonese shouldn't need this section, and should find
``pip install --upgrade pycantonese`` sufficient as a way to install PyCantonese.

The latest code under development is available on GitHub at
https://github.com/jacksonllee/pycantonese.
You need to have `Git LFS <https://git-lfs.github.com/>`_ installed on your system
(e.g., run ``brew install git-lfs`` if you have Homebrew installed on MacOS,
or run ``sudo apt-get install git-lfs`` if you're on Ubuntu).
To obtain this version for experimental features or for development:

.. code-block:: bash

   $ git clone https://github.com/jacksonllee/pycantonese.git
   $ cd pycantonese
   $ git lfs pull
   $ pip install -r dev-requirements.txt
   $ pip install -e .

To run tests and styling checks:

.. code-block:: bash

   $ pytest
   $ flake8 src tests
   $ black --check src tests

To build the documentation website files:

.. code-block:: bash

    $ python docs/source/build_docs.py
