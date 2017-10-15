PyCantonese: Cantonese Linguistics and NLP in Python
====================================================

.. image:: https://travis-ci.org/pycantonese/pycantonese.svg?branch=master
   :target: https://travis-ci.org/pycantonese/pycantonese
   :alt: Build

Full documentation: http://pycantonese.org


Download and install
--------------------

PyCantonese supports Python 2.7 and 3.4+, and is available through pip:

.. code-block:: bash

   $ pip install pycantonese


Setting up a Development Environment
------------------------------------

The latest code under development is available on Github at
`pycantonese/pycantonese <https://github.com/pycantonese/pycantonese>`_.
To obtain this version for experimental features or for development:

.. code-block:: bash

   $ git clone https://github.com/pycantonese/pycantonese.git
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

Lee, Jackson L. 2015. PyCantonese: Cantonese linguistic research in the age of big data. Talk at the Childhood Bilingualism Research Centre, Chinese University of Hong Kong. September 15. 2015.
`Notes+slides <http://jacksonllee.com/papers/Lee-pycantonese-2015.html>`_

Collaborators: Litong Chen, Charles Lam, Tsz-Him Tsui


Contributors
------------

Many thanks to the following individuals for code, comments, bug reports, etc.:

Rachel Han, Hill Ma, Stephan Stiller
