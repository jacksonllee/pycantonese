# CantoMap

Data extracted from the [CantoMap](https://github.com/gwinterstein/CantoMap) corpus,
a collection of contemporary Hong Kong Cantonese conversation recordings
from MapTask exercises.

- **Source repository:** https://github.com/gwinterstein/CantoMap
- **Pinned commit:** `9f03a43827c7a75e095b0bfd6ef539c11115f2cf`
- **License:** GPL-3.0 (see LICENSE.txt)

## Extracted data

The `extracted/` directory contains CHAT (`.cha`) files, one per source `.eaf`
(ELAN) file from CantoMap's `ConversationData/` directory. Filenames are derived
from the source path: `ConversationData/Subjects-1_2/160725_009_1_2_A1.eaf`
becomes `Subjects-1_2__160725_009_1_2_A1.cha` (directory separators replaced
with `__`).

Each `.cha` file contains utterances with a main tier and a `%mor`
(morphology) tier. Part-of-speech tags are assigned using PyCantonese's POS
tagger with the HKCanCor tagset (e.g., `a|hou2` where `a` = adjective).

```
*XXE:	好 咁樣 .
%mor:	a|hou2 d|gam2joeng2 .
*XXG:	起點 喺 引依湖 .
%mor:	n|hei2dim2 v|hai2 n|jan5ji1wu4 .
```

## EAF-to-CHAT conversion

`download.py` converts CantoMap's ELAN `.eaf` annotation files to CHAT format.
The conversion involves:

1. **Tier pairing:** Each `.eaf` file contains tiers named `<prefix>-word` and
   `<prefix>-jyutping` (e.g., `E-word` / `E-jyutping`). The script matches
   these by prefix, where each prefix corresponds to a speaker.

2. **Speaker codes:** Tier prefixes (e.g., `E`, `F`, `G`) become CHAT
   participant codes padded with leading `X`s to three characters
   (`E` -> `XXE`, `E1` -> `XE1`).

3. **Time alignment:** Word and Jyutping annotations are aligned by their
   `(start_time, end_time)` timestamps. Utterances from all speakers are then
   sorted by start time to produce a chronologically interleaved transcript.

4. **Jyutping normalization:** Several conventions in the source annotations
   are normalized during extraction:
   - **`#` (pause markers):** Treated as utterance boundaries, splitting a
     single annotation into multiple utterances.
   - **Pipe-separated alternatives** (e.g., `gam3|gam2`): The first variant
     is kept.
   - **`&`-prefixed particles** (e.g., `&le1`): The `&` is stripped, keeping
     the Jyutping (`le1`).
   - **`*N` tone-change notation** (e.g., `gin3dou3*2`): The tone digit
     before `*` is replaced by the digit after it (`gin3dou2`).
   - **`hao4_(Mandarin)`:** Replaced with word `好` and Jyutping `hou2`.

## Regenerating

Run `download.py` to re-download the source `.eaf` files and regenerate
the extracted `.cha` files:

```bash
python src/pycantonese/data/cantomap/download.py
```

Requires `git` to be installed. The script clones the CantoMap repo to a
temporary directory (skipping large audio files via Git LFS) and uses
`rustling.elan` to parse the ELAN annotation files.
