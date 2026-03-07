"""Benchmark HKCanCor corpus loading and access methods.

Compares current pycantonese against v3.4.0 baseline.

Usage:
    uv run python benchmarks/run_corpus.py
    uv run python benchmarks/run_corpus.py --json   # structured output
"""

import json
import sys

from _utils import bench, print_comparison, run_baseline


def benchmark():
    import pycantonese

    results = {}

    # 1. hkcancor() cold load
    def cold_load():
        pycantonese.hkcancor.cache_clear()
        return pycantonese.hkcancor()

    results["hkcancor_load"] = bench(cold_load, n=3)

    # Ensure corpus is loaded for subsequent benchmarks
    corpus = pycantonese.hkcancor()

    # 2. utterances()
    results["utterances"] = bench(corpus.utterances)

    # 3. tokens()
    results["tokens"] = bench(corpus.tokens)

    return results


def main():
    if "--json" in sys.argv:
        print(json.dumps(benchmark()))
        return

    print("=" * 72)
    print("Corpus benchmark: hkcancor load + access methods")
    print("=" * 72)

    current = benchmark()
    baseline = run_baseline(__file__)

    print()
    print_comparison(current, baseline)
    print()


if __name__ == "__main__":
    main()
