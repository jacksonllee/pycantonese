PyCantonese: Cantonese Linguistics and NLP in Python
====================================================

.. image:: https://badge.fury.io/py/pycantonese.svg
   :target: https://pypi.python.org/pypi/pycantonese
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pycantonese.svg
   :target: https://pypi.python.org/pypi/pycantonese
   :alt: Supported Python versions

.. image:: https://circleci.com/gh/jacksonllee/pycantonese/tree/master.svg?style=svg
   :target: https://circleci.com/gh/jacksonllee/pycantonese/tree/master
   :alt: Build


Documentation
-------------

`https://pycantonese.org <https://pycantonese.org>`_


Download and install
--------------------

PyCantonese is available through pip:

.. code-block:: bash

   $ pip install --upgrade pycantonese


Setting up a Development Environment
------------------------------------

The latest code under development is available on Github at
`jacksonllee/pycantonese <https://github.com/jacksonllee/pycantonese>`_.
To obtain this version for experimental features or for development:

.. code-block:: bash

   $ git clone https://github.com/jacksonllee/pycantonese.git
   $ cd pycantonese
   $ pip install -r requirements.txt
   $ python setup.py develop

To run tests and styling checks:

.. code-block:: bash

   $ py.test -vv --cov pycantonese pycantonese
   $ flake8 pycantonese
   $ black --check --line-length=79 pycantonese


Author
------

Developer: Jackson L. Lee

A talk introducing PyCantonese:

Lee, Jackson L. 2015. PyCantonese: Cantonese linguistic research in the age of big data.
Talk at the Childhood Bilingualism Research Centre, Chinese University of Hong Kong. September 15. 2015.
`Notes+slides <https://pycantonese.org/papers/Lee-pycantonese-2015.html>`_

Please also see ``CONTRIBUTORS.md``.


Change Log
----------

Please see ``CHANGELOG.md``.


License
-------

MIT License. Please see ``LICENSE.txt`` for details.

The HKCanCor dataset included in PyCantonese is substantially modified from
its source in terms of format. The original dataset has a CC BY license.
Please see ``pycantonese/data/hkcancor/README.md`` for details.

The rime-cantonese data (release 2020.09.09) is
incorporated into PyCantonese for word segmentation and
characters-to-Jyutping conversion.
This data has a CC BY 4.0 license.
Please see ``pycantonese/data/rime_cantonese/README.md`` for details.
