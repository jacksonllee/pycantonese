Common Voice Cantonese
======================

The Common Voice Cantonese (yue) sentence data (Mozilla Public License 2.0) is
incorporated into PyCantonese for word segmentation model training
(unsupervised EM refinement).

Data source:

- common-voice: https://github.com/common-voice/common-voice/tree/release-v1.157.0

License: Mozilla Public License 2.0. A copy is included at
`src/pycantonese/data/common_voice/LICENSE.txt` (path from the PyCantonese repository root).

The script `download.py` downloads Cantonese (yue) sentences from the source above
and outputs `sents.json` (a JSON array of sentence strings)
used by PyCantonese during training.
