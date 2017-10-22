..  _download:

Download and install
====================

PyCantonese requires Python 3.4 or above.

Latest stable release
---------------------

The latest stable release (version |version|) is hosted at
`PyPI <https://pypi.python.org/pypi/pycantonese>`_
and therefore available via ``pip``::

    $ python3 -m pip install pycantonese

``python3`` is meant to point to your Python 3 interpreter.
Administrative privileges (e.g., ``sudo`` on Unix-like systems)
may be required.

To test your installation in the Python interpreter:

.. code-block:: python

    >>> import pycantonese
    >>> pycantonese.__version__  # show version number

The stable release version is what this documentation describes,
unless otherwise noted.

Under testing and development
-----------------------------

The version under testing and development is available at the
`GitHub repository <https://github.com/pycantonese/pycantonese>`_

This version likely contains experimental code not yet documented.
You may obtain it via ``git``::

    $ git clone https://github.com/pycantonese/pycantonese.git
    $ cd pycantonese
    $ python3 setup.py install

Administrative privileges may be required for the last command.

`Changelog <https://github.com/pycantonese/pycantonese/blob/master/changelog.md>`_ on GitHub

Dependencies
------------

PyCantonese depends on the following Python libraries.
If they are not detected on your system when you install PyCantonese,
they are automatically installed for you:

* `PyLangAcq <http://pylangacq.org>`_
