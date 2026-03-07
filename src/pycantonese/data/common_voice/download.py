#!/usr/bin/env python3
"""Download Common Voice Cantonese sentences and generate sents.json."""

import json
import os
import shutil
import subprocess

COMMON_VOICE_TAG = "release-v1.157.0"
COMMON_VOICE_REPO = "common-voice/common-voice"
FILE_PATH = "server/data/yue/sentence-collector.txt"


def _check_gh() -> None:
    if not shutil.which("gh"):
        raise RuntimeError(
            "The 'gh' command line tool is required but not found. "
            "Please install it: https://cli.github.com/"
        )


def _download_file(repo: str, tag: str, filepath: str) -> str:
    """Download a file from a GitHub repo using gh."""
    result = subprocess.run(
        [
            "gh",
            "api",
            "-H",
            "Accept: application/vnd.github.raw+json",
            f"/repos/{repo}/contents/{filepath}?ref={tag}",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def main() -> None:
    _check_gh()

    this_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"Downloading {FILE_PATH}...")
    content = _download_file(COMMON_VOICE_REPO, COMMON_VOICE_TAG, FILE_PATH)

    sents = [line.strip() for line in content.splitlines() if line.strip()]
    print(f"  {len(sents)} sentences")

    output_path = os.path.join(this_dir, "sents.json")
    with open(output_path, "w", encoding="utf8") as f:
        json.dump(sents, f, ensure_ascii=False, indent=4)

    print(f"Written to {output_path}")


if __name__ == "__main__":
    main()
