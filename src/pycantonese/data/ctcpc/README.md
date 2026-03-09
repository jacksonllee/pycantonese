Cantonese-Traditional Chinese Parallel Corpus (CTCPC)
=====================================================

The CTCPC Cantonese sentence data (CC0 1.0 Universal) is
incorporated into PyCantonese for word segmentation model training
(unsupervised EM refinement).

Data source:

- HuggingFace: https://huggingface.co/datasets/raptorkwok/cantonese-traditional-chinese-parallel-corpus

License: CC0 1.0 Universal. A copy is included at
`src/pycantonese/data/ctcpc/LICENSE.txt` (path from the PyCantonese repository root).

The script `download.py` downloads Cantonese (yue) sentences from the source above
and outputs `sents.json` (a JSON array of sentence strings)
used by PyCantonese during training.
The trained model is persisted as a zst-compressed FlatBuffers binary.
