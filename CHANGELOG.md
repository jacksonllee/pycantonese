# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Characters-to-Jyutping conversion:
  The `characters_to_jyutping` function now has the `segmenter` kwarg for
  customizing word segmentation.
- Added `pyproject.toml`. Related to preferring `setup.cfg` for specifying
  build metadata and options.

### Changed
- Characters-to-Jyutping conversion:
    For the `characters_to_jyutping` function,
    in case rime-cantonese and HKCanCor don't agree,
    rime-cantonese data (more accurate) is preferred.
- Updated the rime-cantonese data to the latest `2021.05.16` release,
  improving both characters-to-Jyutping conversion and word segmentation.
- Updated the PyLangAcq dependency to v0.15.0, allowing PyCantonese's `CHATReader`
  to use the new methods `to_strs` and `to_chat`.
* Switched to `setup.cfg` to fully specify build metadata and options,
  while keeping a minimal `setup.py` for backward compatibility.
  Related to the new `pyproject.toml`.

### Deprecated
### Removed
### Fixed
### Security

## [3.3.1] - 2021-05-14

### Fixed
- Allowed PyLangAcq v0.14.* for real.

## [3.3.0] - 2021-05-14

### Changed
- Allowed PyLangAcq v0.14.*, thereby adding the new features of the `filter` method to `CHATReader`
  and optional parallelization for CHAT data processing.

### Fixed
- Fixed the `search` method of `CHATReader` when `by_tokens` is `False`.

## [3.2.4] - 2021-05-07

### Fixed
- Fixed the previously inoperational methods `append`, `append_left`, `extend`, and `extend_left`
  of the class `CHATReader` through the upstream PyLangAcq package.
- Retrained the part-of-speech tagger, after the minor character fix from v3.2.3.
- Raised `NotImplementedError` for the method `ipsyn` of `CHATReader`,
  since the upstream method works only for English.

## [3.2.3] - 2021-04-12

### Fixed
* Fixed character issues in the built-in HKCanCor data: 𥄫

## [3.2.2] - 2021-03-23

### Fixed
* Fixed a CHAT parsing issue when correction and repetition are combined,
  by bumping the pylangacq dependency from v0.13.0 to v0.13.1.

## [3.2.1] - 2021-03-21

### Fixed
* Fixed character issues in the built-in HKCanCor data: 𠮩𠹌, 𠻗

## [3.2.0] - 2021-03-20

Note: The underlying CHAT parser, the PyLangAcq package, has been bumped to v0.13.0.
All of the updates of PyLangAcq's CHAT reader apply to this PyCantonese release
as well. The details are in
[PyLangAcq's changelog for v0.13.0](https://github.com/jacksonllee/pylangacq/releases/tag/v0.13.0).
The changelog entries below only document updates specific to PyCantonese.

### Added
* Defined the `Jyutping` class to better represent parsed Jyutping romanization.

### Changed
* Bumped the PyLangAcq dependency to v0.13.0.
* The function `parse_jyutping` now returns a list of `Jyutping` objects,
  rather than tuples of strings.

### Deprecated

* The following methods in the ``CHATReader`` class have been deprecated:
  - `character_sents` (use `characters` with `by_utterances=True` instead)
  - `jyutping_sents` (use `jyutping` with `by_utterances=True` instead)

* The following arguments of the ``search`` method of ``CHATReader`` have been deprecated:
  - `sent_range` (use `utterance_range` instead)
  - `tagged` (use `by_tokens` instead)
  - `sents` (use `by_utterances` instead)

### Fixed
* Fixed the character issues in the built-in HKCanCor data: 𠺢, 𠺝, 𡁜, 𧕴, 𥊙, 𡃓, 𠴕, 𡀔

## [3.1.1] - 2021-03-18

### Fixed
* Pinned pylangacq at 0.12.0 (the new 0.13.0 has breaking changes).

## [3.1.0] - 2021-02-21

### Added
* Part-of-speech tagging:
   - Added the function `pos_tag` that takes a segmented sentence or phrase
     and returns its part-of-speech tags.
   - Added the function `hkcancor_to_ud` that maps a part-of-speech tag
     from the original HKCanCor annotated data to one of the tags from the
     Universal Dependencies v2 tagset.
* Word segmentation:
   - Improved segmentation quality by revising the underlying wordlist data.
* The test suite now covers code snippets in both the docstrings and `.rst` doc files.

### Fixed
* Fixed the issue of not opening text files with UTF-8 encoding
  (a possible issue on Windows).
* `jyutping_to_yale` and `parse_jyutping` now return a null value
  (rather than raise an error) when the input is null.
* The word segmentation function `segment` now strips all whitespace
  from the input unsegmented string before segmenting it.

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
