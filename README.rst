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

.. image:: https://anaconda.org/conda-forge/pycantonese/badges/version.svg
   :target: https://anaconda.org/conda-forge/pycantonese
   :alt: Conda version

|

.. start-sphinx-website-index-page

PyCantonese is a Python library for Cantonese linguistics and natural language
processing (NLP). Currently implemented features:

- Accessing and searching corpus data
- Parsing and conversion tools for Jyutping romanization
- Parsing Cantonese text
- Stop words
- Word segmentation
- Part-of-speech tagging

The design of PyCantonese prioritizes ease of use and linguistic knowledge.
It has been successfully used by both academic and commercial organizations,
including major US tech companies.

.. _download_install:

Download and Install
--------------------

To download and install the stable, most recent version::

   # Through pip
   pip install --upgrade pycantonese

   # Through conda-forge
   conda install -c conda-forge pycantonese

For Pyodide users, PyCantonese now ships a WASM wheel, attached to a
`GitHub release <https://github.com/jacksonllee/pycantonese/releases>`_
(find the ``.whl`` with ``emscripten`` in the name).

Ready for more?
Check out the `Quickstart <https://pycantonese.org/quickstart.html>`_ page.

Links
-----

* Author: `Jackson L. Lee <https://jacksonllee.com>`_
* Source code: https://github.com/jacksonllee/pycantonese
* Social media:
  `Facebook <https://www.facebook.com/pycantonese>`_

How to Cite
-----------

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
         month = jun,
         year = "2022",
         publisher = "European Language Resources Association",
      }

License
-------

MIT License. Please see ``LICENSE.txt`` in the GitHub source code for details.

PyCantonese includes data from the following sources
(please see `src/pycantonese/data <https://github.com/jacksonllee/pycantonese/tree/main/src/pycantonese/data>`_
for details):

- Hong Kong Cantonese Corpus (CC BY)
- rime-cantonese (CC BY 4.0)
- Common Voice Cantonese (Mozilla Public License 2.0)
- Cantonese-Traditional Chinese Parallel Corpus (CC0 1.0 Universal)

Logo
----

The PyCantonese logo is the Chinese character 粵 meaning Cantonese,
with artistic design by albino.snowman (Instagram handle).

.. end-sphinx-website-index-page

Changelog
---------

Please see ``CHANGELOG.md``.
