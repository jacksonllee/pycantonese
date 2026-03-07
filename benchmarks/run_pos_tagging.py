"""Benchmark POS tagging (predict only, not training).

Compares current pycantonese against v3.4.0 baseline.

Usage:
    uv run python benchmarks/run_pos_tagging.py
    uv run python benchmarks/run_pos_tagging.py --json   # structured output
"""

import json
import sys

from _utils import bench, print_comparison, run_baseline, words_by_utterance

_SINGLE_SENTENCE = ["我", "噚日", "買", "咗", "嗰", "對", "鞋", "。"]


def benchmark():
    import pycantonese

    results = {}

    # Warm up the tagger (loads model from JSON on first call)
    pycantonese.pos_tag(["我"])

    # 1. Single sentence
    results["single_sentence"] = bench(
        lambda: pycantonese.pos_tag(_SINGLE_SENTENCE), n=20
    )

    # 2. All utterances from hkcancor
    corpus = pycantonese.hkcancor()
    all_word_lists = words_by_utterance(corpus)

    def tag_all():
        for words in all_word_lists:
            pycantonese.pos_tag(words)

    results["all_hkcancor_utts"] = bench(tag_all, n=3)

    return results


def main():
    if "--json" in sys.argv:
        print(json.dumps(benchmark()))
        return

    print("=" * 72)
    print("POS tagging benchmark (predict only)")
    print("=" * 72)

    current = benchmark()
    baseline = run_baseline(__file__)

    print()
    print_comparison(current, baseline)
    print()


if __name__ == "__main__":
    main()
