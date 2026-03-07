rime-cantonese
==============

The rime-cantonese data (CC BY 4.0 license) is
incorporated into PyCantonese for word segmentation and
characters-to-Jyutping conversion.

Data sources:

- rime-cantonese-upstream: https://github.com/CanCLID/rime-cantonese-upstream/tree/bea0d7a366627506eb214d82b80780b5db4b05a1
- rime-cantonese: https://github.com/rime/rime-cantonese/tree/33f7d81bc7ef5eb2f69538a2d3d5fc109529e2dd

License: CC BY 4.0. A copy is included at
`src/pycantonese/data/rime_cantonese/LICENSE.txt` (path from the PyCantonese repository root).

The script `download.py` downloads data from the sources above
and outputs two files used by PyCantonese during runtime:

- `chars_to_jyutping.json`: words/characters mapped to Jyutping,
  used for characters-to-Jyutping conversion and as the word dictionary
  for supervised word segmentation training.
- `phrase_fragments.json`: multi-word phrase fragments (array of strings),
  used exclusively for unsupervised EM refinement of the word segmenter.
  These entries are intentionally excluded from supervised training because
  they are stored as unsegmented strings and would corrupt word boundary labels.

Source files:

| Source | File | Output | Contents |
| --- | --- | --- | --- |
| rime-cantonese-upstream | `word.csv` | `chars_to_jyutping.json` | Words |
| rime-cantonese-upstream | `proper_nouns.csv` | `chars_to_jyutping.json` | Proper nouns |
| rime-cantonese-upstream | `onomatopoeia.csv` | `chars_to_jyutping.json` | Onomatopoeia |
| rime-cantonese-upstream | `fixed_expressions.csv` | `chars_to_jyutping.json` | Fixed expressions and idioms |
| rime-cantonese-upstream | `char.csv` | `chars_to_jyutping.json` | Single characters (only default/預設 pronunciations) |
| rime-cantonese | `jyut6ping3.lettered.dict.yaml` | `chars_to_jyutping.json` | Words with letters/numbers mapped to Jyutping |
| rime-cantonese-upstream | `phrase_fragment.csv` | `phrase_fragments.json` | Multi-word phrase fragments (unsupervised word segmentation training only) |
