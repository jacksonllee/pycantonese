# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [3.0.0] - 2020-10-25

### Added
* Word segmentation:
   - Segmentation is customizable for the following:
      * Maximum word length
      * A user-supplied list of words to allow as words
      * A user-supplied list of words to disallow as words
   - The default segmentation model has been improved with the rime-cantonese data (CC BY 4.0 license).
* Characters-to-Jyutping conversion:
   - The conversion returns results in a word-segmented form.
   - The conversion model has been improved with the rime-cantonese data (CC BY 4.0 license).
* Added the following functions; they are equivalent to their (now deprecated)
  `x2y` counterparts:
    - `characters_to_jyutping`
    - `jyutping_to_tipa`
    - `jyutping_to_yale`
* Added support for Python 3.9.

### Changed

#### API-breaking Changes

* `jyutping_to_yale`: The default value of the keyword argument `as_list` has
  been changed from `False` to `True`, so that this function is now more in
  line with the other "jyutping_to_X" functions for returning a list.
* `characters_to_jyutping`: The returned valued is now a list of segmented words,
  where each is a 2-tuple of (Cantonese characters, Jyutping).
  Previously, it was a list of Jyutping strings for the individual
  Cantonese characters.

#### Non-API-breaking Changes

* Switched documentation to the readthedocs theme and numpydoc docstring style.
* Improved CircleCI builds with orbs.

### Deprecated
* The following `x2y` functions have been deprecated in favor of their
  equivalents named in the form of `x_to_y`.
    - `characters2jyutping`
    - `jyutping2tipa`
    - `jyutping2yale`
 
### Security
- Turned on HTTPS for the pycantonese.org domain.


## [2.4.1] - 2020-10-10
### Fixed
* Switched to the `wordseg` dependency to a PyPI source instead of a
  GitHub direct link.

## [2.4.0] - 2020-10-10

### Added
* Added the `characters2jyutping()` function for converting
  Cantonese characters to Jyutping romanization.
* Added the `segment()` function for word segmentation.

## [2.3.0] - 2020-07-24

### Added
* Added support for Python 3.7 and 3.8.

### Removed
* Dropped support for Python 3.4 and 3.5 (supporting 3.6, 3.7, and 3.8 now).

## [2.2.0] - 2018-06-30

### Added
* 104 stop words.

## [2.1.0] - 2018-06-11

### Added
* Exposed the `exclude` parameter in various reader methods
  for excluding specific participants. This parameter was implemented at
  pylangacq v0.10.0.

### Fixed
* Allowed "n" to be a syllabic nasal.
* Fixed corpus reader not picking up the characters.

## [2.0.0] - 2016-02-06

* PyCantonese now requires Python 3.4 or above.
* Adopted the CHAT corpus format, piggybacking on [PyLangAcq](http://pylangacq.org/)
* Converted HKCanCor into the CHAT format
* Switched to transparent function names
  (cf. issue [#10](https://github.com/pycantonese/pycantonese/issues/10)): `parse_jyutping()`, `jyutping2yale()`, `jyutping2tipa()`
* Bug fixes: issues
  [#6](https://github.com/pycantonese/pycantonese/issues/6),
  [#7](https://github.com/pycantonese/pycantonese/issues/7),
  [#8](https://github.com/pycantonese/pycantonese/issues/8)
  [#9](https://github.com/pycantonese/pycantonese/issues/9)

## [1.0] - 2015-09-06

* Fixed the Jyutping-Yale conversion issue with "yu"
* Added ``number_of_words()`` and ``number_of_characters()`` for corpus access
* Forced all part-of-speech tags
  (both in searches and internal to corpus objects)
  in caps, in line with the NLTK convention

## [1.0dev] - 2015-09-02

* Overall code restructuring
* Only Python 3.x is supported from this point onwards
* Used generators instead of lists for corpus access methods
* Added the part-of-speech search criterion
* Added Jyutping-to-Yale conversion
* Added Jyutping-to-TIPA conversion
* Disabled the function for reading a custom corpus dataset (it will come back)

## [0.2.1] - 2015-01-25

* Fixed corpus access path issues

## [0.2] - 2015-01-22

* [The Hong Kong Cantonese Corpus](http://compling.hss.ntu.edu.sg/hkcancor/) is included in the package.
* A general-purpose ``search()`` function is defined, replacing the
  element-specific search functions from version 0.1.

## [0.1] - 2014-12-17

* Basic functions available, including...
* Parsing Jyutping romanization
* Reading a tagged corpus data folder
* Searching by a given element (onset/initial, nucleus, coda, final, character)
* Searching by a character plus a range
