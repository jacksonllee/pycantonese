"""Shared benchmark utilities."""

import json
import os
import subprocess
import sys
import time

import pycantonese

# v3.4.0 uses "by_utterances" (with 's'); v4.0.0+ uses "by_utterance".
_BY_UTT_KWARG = (
    "by_utterance"
    if pycantonese.__version__ >= "4"
    else "by_utterances"
)


def words_by_utterance(corpus):
    """Call corpus.words() grouped by utterance, compatible across versions."""
    return corpus.words(**{_BY_UTT_KWARG: True})


def bench(func, n=5):
    """Run func n times, return timing dict with min/mean/max."""
    times = []
    for _ in range(n):
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    return {"min": min(times), "mean": sum(times) / len(times), "max": max(times)}


def run_baseline(script_path):
    """Run a benchmark script against the v3.4.0 baseline via subprocess.

    The script is invoked with --json flag and PYTHONPATH set so that
    the _baseline/ directory (containing pycantonese v3.4.0) is found
    before the installed current version.

    Returns the parsed JSON results dict, or None if baseline is not set up.
    """
    baseline_dir = os.path.join(os.path.dirname(script_path), "_baseline")
    if not os.path.isdir(os.path.join(baseline_dir, "pycantonese")):
        print(
            "WARNING: Baseline not found. Run setup_baseline.sh first.\n"
            "  Skipping v3.4.0 comparison.\n"
        )
        return None

    env = os.environ.copy()
    env["PYTHONPATH"] = baseline_dir + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [sys.executable, script_path, "--json"],
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0:
        print(f"WARNING: Baseline run failed (exit code {result.returncode}):")
        print(result.stderr[:500])
        return None

    return json.loads(result.stdout)


def print_comparison(results_current, results_baseline):
    """Print a formatted comparison table.

    Each results dict maps benchmark names to {"min", "mean", "max"} dicts.
    """
    header = f"{'Benchmark':<30s}  {'Current (mean)':>14s}  {'v3.4.0 (mean)':>14s}  {'Speedup':>8s}"
    print(header)
    print("-" * len(header))
    for name, current in results_current.items():
        c_mean = current["mean"]
        if results_baseline and name in results_baseline:
            b_mean = results_baseline[name]["mean"]
            speedup = b_mean / c_mean if c_mean > 0 else float("inf")
            print(
                f"  {name:<28s}  {c_mean:>13.4f}s  {b_mean:>13.4f}s  {speedup:>7.1f}x"
            )
        else:
            print(f"  {name:<28s}  {c_mean:>13.4f}s  {'n/a':>14s}  {'n/a':>8s}")
