Change log
==========

Current version: 1.0

- Version 1.1 in progress

    * Jyutping "eu" correctly converted to Yale "ew" (cf. issue [#6](https://github.com/pycantonese/pycantonese/issues/6))

    * For Jyutping-Yale conversion with codas "i/u" and low tones,
      the low-tone "h" in Yale now follows the gliding coda (cf. issue [#7](https://github.com/pycantonese/pycantonese/issues/7))

- Version 1.0 2015-09-06

    * Fixed the Jyutping-Yale conversion issue with "yu"
    * Added ``number_of_words()`` and ``number_of_characters()`` methods for corpus access
    * Forced all part-of-speech tags (both in searches and internal to corpus objects)
      in caps, in line with the NLTK convention

- Version 1.0dev 2015-09-02

    * Overall code restructuring
    * Only Python 3.x is supported from this point onwards
    * Used generators instead of lists for corpus access methods
    * Added the part-of-speech search criterion
    * Added Jyutping-to-Yale conversion
    * Added Jyutping-to-TIPA conversion
    * Disabled the function for reading a custom corpus dataset (it will come back)

- Version 0.2.1 2015-01-25

    * Fixed corpus access path issues

- Version 0.2 2015-01-22

    * [The Hong Kong Cantonese Corpus](http://compling.hss.ntu.edu.sg/hkcancor/) is included in the package.
    * A general-purpose ``search()`` function is defined, replacing the
      element-specific search functions from version 0.1.

- Version 0.1 2014-12-17

    * Basic functions available, including...
    * Parsing Jyutping romanization
    * Reading a tagged corpus data folder
    * Searching by a given element (onset/initial, nucleus, coda, final, character)
    * Searching by a character plus a range
