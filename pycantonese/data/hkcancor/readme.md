Hong Kong Cantonese Corpus
==========================


Introduction
------------

The Hong Kong Cantonese Corpus (HKCanCor) is a corpus of conversational
Hong Kong Cantonese compiled by Kang Kwong Luke based on data collected
in the late 1990's from local radio programs as well as other recordings.

HKCanCor as included in PyCantonese has been substantially modified from its
source in terms of data format. Please read below for details.

The HKCanCor source is here:
http://compling.hss.ntu.edu.sg/hkcancor/

HKCanCor is released under a CC BY license. A copy of the license
from the HKCanCor source
([here](http://compling.hss.ntu.edu.sg/hkcancor/data/LICENSE),
accessed October 2017) is included
at `pycantonese/data/hkcancor/license.txt` (path from the PyCantonese
repository root).

If this corpus is used, the following publication should be cited:

K. K. Luke and May L.Y. Wong (2015) The Hong Kong Cantonese Corpus: Design and Uses. Journal of Chinese Linguistics (to appear).


The CHAT format in PyCantonese
------------------------------

The choice of corpus data format in PyCantonese is the CHAT format
(as developed for CHILDES for language acquisition research). The CHAT format
is well-documented, rich for annotations, and designed mainly for
conversational data.

The version of HKCanCor incorporated in PyCantonese is in the CHAT format,
in compliance with the latest CHAT manual
(http://childes.psy.cmu.edu/manuals/CHAT.pdf)
dated 2015-09-22.
The following notes explain how this version differs from the source.

HKCanCor comes with 58 data files, which have been rendered as `.cha` files.
Following CHAT, each file has:

* headers (= lines beginning with `@`) for metadata
* transcriptions (= lines beginning with `*` for the
utterance and the accompanying annotations in the `@mor` tiers).

As an example, the data file `FC-001_v2.cha` begins as follows
(headers plus the first three utterances):

```
@UTF8
@Begin
@Languages:	yue , eng
@Participants:	XXA A Adult , XXB B Adult
@ID:	yue , eng|HKCanCor|XXA|34;|female|||Adult||origin:HK|
@ID:	yue , eng|HKCanCor|XXB|37;|female|||Adult||origin:HK|
@Date:	30-APR-1997
@Tape Number:	001
*XXA:	喂 遲 啲 去 唔 去 旅行 啊 ?
%mor:	e|wai3 a|ci4 u|di1 v|heoi3 d|m4 v|heoi3 vn|leoi5hang4 y|aa3	?
*XXA:	你 老公 有冇 平 機票 啊 ?
%mor:	r|nei5 n|lou5gung1 v1|jau5mou5 a|peng4 n|gei1piu3 y|aa3 ?
*XXB:	平 機票 要 淡季 先 有得 平 𡃉 喎 .
%mor:	a|peng4 n|gei1piu3 vu|jiu3 an|daam6gwai3 d|sin1 vu|jau5dak1	a|peng4 y|gaa3 y|wo3 .
```

* Languages:

  CHAT requires that the languages in question be specified. In all 58 CHAT
  files of HKCancor, the languages are set to be "yue, eng" for both the file
  (in the `@Languages` header) and the participants (in the `@ID` headers).

* Participants:

  *Code name:*
  In the HKCanCor source, participants are simply identified by letters "A",
  "B" etc.
  Because participant codes in CHAT are required to be three characters long,
  participants in the current CHAT format are denoted by "XXA", "XXB" etc.

  *Age:*
  In the HKCanCor source, certain participants' age is unclear, e.g., 25-30
  as a best-guess range.
  In cases like this, the smaller number is taken as the age
  (i.e., 25 in this example).

* Transcriptions and annotations:

  *The representation of words*:
  The HKCanCor source represents a word as something like "喂/e/wai3/". In the
  CHAT format, the Chinese character(s) are found on the utterance line (= the
  one that begins with `*` plus the participant code). The part-of-speech tag
  and Jyutping romanization are treated as morphological information and found
  in the `@mor` tier, e.g., `e|wai3`.

  *Punctuation marks*:
  All punctuation marks in the source files are converted into ASCII characters
  in the CHAT format. All Chinese-style delimiters
  (different kinds of parentheses, brackets, etc) are collapsed and
  represented by the double quote `"`.
  The colon is removed to avoid parsing problems.
