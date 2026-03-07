#!/usr/bin/env python3
"""Download CTCPC Cantonese sentences and generate sents.json."""

import json
import os
import tempfile
import urllib.request

_BASE_URL = (
    "https://huggingface.co/api/datasets/"
    "raptorkwok/cantonese-traditional-chinese-parallel-corpus/"
    "parquet/default/{split}/0.parquet"
)

_SPLITS = ["train", "validation", "test"]


def _check_pyarrow() -> None:
    try:
        import pyarrow  # type: ignore[import-not-found,import-untyped]  # noqa: F401
    except ImportError:
        raise RuntimeError(
            "The 'pyarrow' package is required but not found. "
            "Please install it: pip install pyarrow"
        )


def main() -> None:
    _check_pyarrow()
    import pyarrow.parquet as pq  # type: ignore[import-not-found,import-untyped]

    this_dir = os.path.dirname(os.path.abspath(__file__))
    all_sents: set[str] = set()

    for split in _SPLITS:
        url = _BASE_URL.format(split=split)
        print(f"Downloading {split} split...")
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            urllib.request.urlretrieve(url, tmp_path)
            table = pq.read_table(tmp_path)
        finally:
            os.unlink(tmp_path)

        translations = table.column("translation").to_pylist()
        split_sents = {
            t["yue"].strip() for t in translations if t["yue"] and t["yue"].strip()
        }
        print(f"  {len(split_sents)} sentences")
        all_sents |= split_sents

    sents = sorted(all_sents)
    print(f"Total: {len(sents)} unique sentences")

    output_path = os.path.join(this_dir, "sents.json")
    with open(output_path, "w", encoding="utf8") as f:
        json.dump(sents, f, ensure_ascii=False, indent=4)

    print(f"Written to {output_path}")


if __name__ == "__main__":
    main()
