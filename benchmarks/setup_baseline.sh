#!/usr/bin/env bash
# Install pycantonese v3.4.0 into benchmarks/_baseline/ for comparison benchmarks.
#
# Usage:
#     bash benchmarks/setup_baseline.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="$SCRIPT_DIR/_baseline"

if [ -d "$TARGET/pycantonese" ]; then
    echo "_baseline/ already exists. Remove it first to reinstall."
    exit 0
fi

echo "Installing pycantonese==3.4.0 into $TARGET ..."
uv pip install --target "$TARGET" pycantonese==3.4.0
# v3.4.0's wordseg dependency needs pkg_resources from setuptools.
# Modern setuptools (70+) removed pkg_resources as a top-level module.
uv pip install --target "$TARGET" 'setuptools<70'
echo "Done. Installed pycantonese v3.4.0 to $TARGET"
