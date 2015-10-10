# PyCantonese

PyCantonese is a Python library for working with Cantonese corpus data.
While it is under active development and many other features and
functions are forthcoming, 
it currently includes JyutPing parsing and conversion tools as well as general 
search functionalities for built-in or custom corpus data.

## Documentation and versions

The official documentation describes the latest release and is here:
[http://pycantonese.github.io/](http://pycantonese.github.io/)

The latest stable release is version **1.0**.

## Installation

The stable version is released on the
[Python Package Index](https://pypi.python.org/pypi/pycantonese).

The latest version under development and testing is available from the GitHub
repository here:

    git clone https://github.com/pycantonese/pycantonese.git
    cd pycantonese
    python3 setup.py install --user

For how this current latest version differs from the stable release version,
see the bug fixes and new features below.


## Bug fixes and new features

The current version from the GitHub source here is **1.1-alpha.1**.

Bugs fixes, as well as new features
(available at the GitHub source here, not yet in the release on PyPI):

* Jyutping "eu" correctly converted to Yale "ew" (cf. issue [#6](https://github.com/pycantonese/pycantonese/issues/6))

* For Jyutping-Yale conversion with codas "i/u" and low tones,
  the low-tone "h" in Yale now follows the gliding coda (cf. issue [#7](https://github.com/pycantonese/pycantonese/issues/7))



## Author

Developer: Jackson L. Lee

A talk introducing PyCantonese:

Lee, Jackson L. 2015. PyCantonese: Cantonese linguistic research in the age of big data. Talk at the Childhood Bilingualism Research Centre, Chinese University of Hong Kong. September 15. 2015.
([Notes+slides](http://jacksonllee.com/papers/Lee-pycantonese-2015.html))

A paper is being prepared:

Lee, Jackson L., Litong Chen, and Tsz-Him Tsui. PyCantonese: new perspectives on Cantonese linguistcs.

## Contributors

Comments, advice, and code contributed by the following individuals:

Charles Lam, Hill Ma, Stephan Stiller


