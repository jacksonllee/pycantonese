#!/usr/bin/env python3
"""Download rime-cantonese data and generate chars_to_jyutping.json."""

import csv
import io
import json
import os
import shutil
import subprocess

UPSTREAM_COMMIT = "bea0d7a366627506eb214d82b80780b5db4b05a1"
UPSTREAM_REPO = "CanCLID/rime-cantonese-upstream"

RIME_CANTONESE_COMMIT = "33f7d81bc7ef5eb2f69538a2d3d5fc109529e2dd"
RIME_CANTONESE_REPO = "rime/rime-cantonese"

# Processing order matters: char.csv is last so its single-character
# pronunciations take priority over any single-char entries from other files.
# For char.csv, 預設 entries always win; for chars with no 預設, the last row wins.
CSV_FILES = [
    "word.csv",
    "proper_nouns.csv",
    # phrase_fragment.csv excluded here: it contains multi-word phrases that
    # confuse supervised word-boundary training. Downloaded separately below.
    "onomatopoeia.csv",
    "fixed_expressions.csv",
    "char.csv",
]


def _check_gh() -> None:
    if not shutil.which("gh"):
        raise RuntimeError(
            "The 'gh' command line tool is required but not found. "
            "Please install it: https://cli.github.com/"
        )


def _download_file(repo: str, commit: str, filename: str) -> str:
    """Download a file from a GitHub repo using gh."""
    result = subprocess.run(
        [
            "gh",
            "api",
            "-H",
            "Accept: application/vnd.github.raw+json",
            f"/repos/{repo}/contents/{filename}?ref={commit}",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def _process_csv(filename: str, content: str) -> dict[str, str]:
    """Process a CSV file and return a char-to-jyutping mapping."""
    reader = csv.DictReader(io.StringIO(content))
    mapping: dict[str, str] = {}
    preferred: dict[str, str] = {}
    for row in reader:
        char = row["char"]
        jyutping = row["jyutping"].replace(" ", "")
        if filename == "char.csv":
            if row["pron_rank"] == "預設":
                preferred[char] = jyutping
            else:
                mapping[char] = jyutping
        else:
            mapping[char] = jyutping
    if filename == "char.csv":
        mapping.update(preferred)
    return mapping


def _process_lettered_yaml(content: str) -> dict[str, str]:
    """Process jyut6ping3.lettered.dict.yaml and return a char-to-jyutping mapping.

    The YAML has a header ending with '...' followed by tab-separated data lines:
        chars<TAB>jyutping
    Some lines may have a third frequency field which is ignored.
    Only the first occurrence of each char is kept (file is sorted by weight).
    """
    mapping: dict[str, str] = {}
    past_header = False
    for line in content.splitlines():
        if not past_header:
            if line.strip() == "...":
                past_header = True
            continue
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        char = parts[0]
        jyutping = parts[1].replace(" ", "")
        # Keep first occurrence only (file is sorted by weight, so first = best).
        if char not in mapping:
            mapping[char] = jyutping
    return mapping


def main() -> None:
    _check_gh()

    this_dir = os.path.dirname(os.path.abspath(__file__))

    chars_to_jyutping: dict[str, str] = {}

    # Process CSV files from rime-cantonese-upstream.
    for filename in CSV_FILES:
        print(f"Downloading {filename}...")
        content = _download_file(UPSTREAM_REPO, UPSTREAM_COMMIT, filename)
        mapping = _process_csv(filename, content)
        print(f"  {len(mapping)} entries")
        chars_to_jyutping.update(mapping)

    # Process lettered YAML from rime-cantonese.
    lettered_filename = "jyut6ping3.lettered.dict.yaml"
    print(f"Downloading {lettered_filename}...")
    content = _download_file(
        RIME_CANTONESE_REPO, RIME_CANTONESE_COMMIT, lettered_filename
    )
    mapping = _process_lettered_yaml(content)
    print(f"  {len(mapping)} entries")
    chars_to_jyutping.update(mapping)

    print(f"Total: {len(chars_to_jyutping)} entries")

    # Sort by jyutping value.
    chars_to_jyutping = dict(sorted(chars_to_jyutping.items(), key=lambda x: x[1]))

    output_path = os.path.join(this_dir, "chars_to_jyutping.json")
    with open(output_path, "w", encoding="utf8") as f:
        json.dump(chars_to_jyutping, f, ensure_ascii=False, indent=4)

    print(f"Written to {output_path}")

    # Download phrase_fragment.csv separately — used only for unsupervised EM
    # training in word segmentation (not supervised boundary labeling).
    print("Downloading phrase_fragment.csv...")
    content = _download_file(UPSTREAM_REPO, UPSTREAM_COMMIT, "phrase_fragment.csv")
    reader = csv.DictReader(io.StringIO(content))
    phrase_fragments = sorted({row["char"] for row in reader if row["char"]})
    print(f"  {len(phrase_fragments)} phrases")

    phrase_fragments_path = os.path.join(this_dir, "phrase_fragments.json")
    with open(phrase_fragments_path, "w", encoding="utf8") as f:
        json.dump(phrase_fragments, f, ensure_ascii=False, indent=4)

    print(f"Written to {phrase_fragments_path}")


if __name__ == "__main__":
    main()
