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

`http://pycantonese.org <http://pycantonese.org>`_


Download and install
--------------------

PyCantonese is available through pip:

.. code-block:: bash

   $ pip install -U pycantonese


Setting up a Development Environment
------------------------------------

The latest code under development is available on Github at
`jacksonllee/pycantonese <https://github.com/jacksonllee/pycantonese>`_.
To obtain this version for experimental features or for development:

.. code-block:: bash

   $ git clone https://github.com/jacksonllee/pycantonese.git
   $ cd pycantonese
   $ pip install -r requirements.txt
   $ pip install -r dev-requirements.txt
   $ python setup.py develop

To run tests:

.. code-block:: bash

   $ py.test -vv --cov pycantonese pycantonese
   $ flake8 pycantonese


Author
------

Developer: Jackson L. Lee

A talk introducing PyCantonese:

Lee, Jackson L. 2015. PyCantonese: Cantonese linguistic research in the age of big data.
Talk at the Childhood Bilingualism Research Centre, Chinese University of Hong Kong. September 15. 2015.
`Notes+slides <http://pycantonese.org/papers/Lee-pycantonese-2015.html>`_

Please also see ``CONTRIBUTORS.md``.


Change Log
----------

Please see ``CHANGELOG.md``.


License
-------

MIT License. Please see ``LICENSE.txt`` for details.

The HKCanCor dataset included in PyCantonese is substantially modified from
its source in terms of format. The original dataset has a CC BY license.
Please see ``pycantonese/data/hkcancor/readme.md`` for details.
