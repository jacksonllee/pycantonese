rime-cantonese
==============

The rime-cantonese data (release 2020.09.09, with a CC BY 4.0 license) is
incorporated into PyCantonese for word segmentation and
characters-to-Jyutping conversion.

Data source: https://github.com/rime/rime-cantonese/tree/2020.09.09

License: CC BY 4.0. A copy is included at `pycantonese/data/rime_cantonese/LICENSE.txt` (path from the PyCantonese
repository root).

The script `download_and_resegment.py` downloads the rime-cantonese data files
listed below, resegments the data to improve quality according to `resegmented.txt`,
and outputs JSON files used by PyCantonese during runtime.

| Source file from rime-cantonese | JSON file in PyCantonese  | Contents in the JSON file |
| ------------------------------- | ------------------------- | ------------------------- |
| [`jyut6ping3.dict.yaml`](https://github.com/rime/rime-cantonese/blob/2020.09.09/jyut6ping3.dict.yaml) | `chars_to_jyutping.json` | Words mapped to Jyutping |
| [`jyut6ping3.lettered.dict.yaml`](https://github.com/rime/rime-cantonese/blob/2020.09.09/jyut6ping3.lettered.dict.yaml) | `lettered.json` | Words with letters/numbers mapped to Jyutping |
