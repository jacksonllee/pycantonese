# PyCantonese: Working with Cantonese corpus data using Python


## Documentation and versions

The official documentation describes the latest stable release and is here:
[http://pycantonese.github.io/](http://pycantonese.github.io/)

The latest stable release is version 0.2.


## Current development

Version 0.3 is under development. New features/changes in future releases:

- search with sent ranges (analogous with word ranges available from version 0.2+)

- capabilities with regard to speaker info (gender etc.); this means adding
  relevant new search functions and augmenting existing ones for the new corpus
  data format

- Jyutping to (LaTeX TIPA styled) IPA conversion

- Jyutping to Yale conversion

See also the [wiki](https://github.com/pycantonese/pycantonese/wiki)
page for work
planned to be undertaken.


## Installation

The stable version is released on the
[Python Package Index](https://pypi.python.org/pypi):
(steps modeled on the
[installation guidelines for NLTK](http://www.nltk.org/install.html))

1. If you have not installed Setuptools, you need it:
[http://pypi.python.org/pypi/setuptools](http://pypi.python.org/pypi/setuptools)

2. If you have not installed Pip, you also need it:
   run ``sudo easy_install pip``

3. Install PyCantonese: run ``sudo pip install pycantonese``
   (PyCantonese depends on [NLTK](http://www.nltk.org/). If the system detects
   that NLTK is not installed, it will be automatically installed.)

4. Test installation: run ``python`` then type ``import pycantonese``

The latest version under development and testing is available from the GitHub
repository here:

    git clone https://github.com/pycantonese/pycantonese.git
    cd pycantonese
    python setup.py install --user

## Author

Developer: Jackson L. Lee

Grateful if the following is cited for using PyCantonese (a paper is being prepared):

Lee, Jackson L., Litong Chen, and Tsz-Him Tsui. 2015. PyCantonese: new perspectives on Cantonese linguistcs.
