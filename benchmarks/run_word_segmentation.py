"""Benchmark word segmentation (the segment() function).

Compares current pycantonese against v3.4.0 baseline.

Usage:
    uv run python benchmarks/run_word_segmentation.py
    uv run python benchmarks/run_word_segmentation.py --json   # structured output
"""

import json
import sys

from _utils import bench, print_comparison, run_baseline, words_by_utterance

_SHORT_TEXT = "廣東話好難學？"
_LONG_TEXT = (
    "香港人講廣東話，"
    "廣東話係一種好有趣嘅語言。"
    "好多人覺得廣東話好難學，"
    "因為廣東話有六個聲調，"
    "而且有好多口語詞彙。"
    "不過如果你有興趣學廣東話，"
    "其實都唔係咁難嘅。"
)


def benchmark():
    import pycantonese

    results = {}

    # Warm up the segmenter (loads vocabulary on first call)
    pycantonese.segment("你好")

    # 1. Short string
    results["short_text"] = bench(lambda: pycantonese.segment(_SHORT_TEXT), n=50)

    # 2. Longer string
    results["long_text"] = bench(lambda: pycantonese.segment(_LONG_TEXT), n=20)

    # 3. Bulk: segment all hkcancor words joined into unsegmented strings
    corpus = pycantonese.hkcancor()
    utterance_words = words_by_utterance(corpus)
    unsegmented = ["".join(words) for words in utterance_words]

    def segment_bulk():
        for text in unsegmented:
            pycantonese.segment(text)

    results["bulk_hkcancor"] = bench(segment_bulk, n=3)

    return results


def main():
    if "--json" in sys.argv:
        print(json.dumps(benchmark()))
        return

    print("=" * 72)
    print("Word segmentation benchmark")
    print("=" * 72)

    current = benchmark()
    baseline = run_baseline(__file__)

    print()
    print_comparison(current, baseline)
    print()


if __name__ == "__main__":
    main()
