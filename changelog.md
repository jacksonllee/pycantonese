Change log
==========

Current stable version: 2.0.0

Version 2.0.1 in progress

* Allow "n" to be a syllabic nasal.

Version 2.0.0 2016-02-06

* PyCantonese now requires Python 3.4 or above.
* Adopt the CHAT corpus format, piggybacking on [PyLangAcq](http://pylangacq.org/)
* Convert HKCanCor into the CHAT format
* Switch to transparent function names
  (cf. issue [#10](https://github.com/pycantonese/pycantonese/issues/10)): `parse_jyutping()`, `jyutping2yale()`, `jyutping2tipa()`
* Bug fixes: issues
  [#6](https://github.com/pycantonese/pycantonese/issues/6),
  [#7](https://github.com/pycantonese/pycantonese/issues/7),
  [#8](https://github.com/pycantonese/pycantonese/issues/8)
  [#9](https://github.com/pycantonese/pycantonese/issues/9)

Version 1.0 2015-09-06

* Fix the Jyutping-Yale conversion issue with "yu"
* Add ``number_of_words()`` and ``number_of_characters()`` for corpus access
* Force all part-of-speech tags
  (both in searches and internal to corpus objects)
  in caps, in line with the NLTK convention

Version 1.0dev 2015-09-02

* Overall code restructuring
* Only Python 3.x is supported from this point onwards
* Used generators instead of lists for corpus access methods
* Added the part-of-speech search criterion
* Added Jyutping-to-Yale conversion
* Added Jyutping-to-TIPA conversion
* Disabled the function for reading a custom corpus dataset (it will come back)

Version 0.2.1 2015-01-25

* Fixed corpus access path issues

Version 0.2 2015-01-22

* [The Hong Kong Cantonese Corpus](http://compling.hss.ntu.edu.sg/hkcancor/) is included in the package.
* A general-purpose ``search()`` function is defined, replacing the
  element-specific search functions from version 0.1.

Version 0.1 2014-12-17

* Basic functions available, including...
* Parsing Jyutping romanization
* Reading a tagged corpus data folder
* Searching by a given element (onset/initial, nucleus, coda, final, character)
* Searching by a character plus a range
