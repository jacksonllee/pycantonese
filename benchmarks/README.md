# Benchmarks

Performance benchmarks comparing the current PyCantonese (v4.0.0, Rust-backed via
`rustling`) against the last pure-Python release (v3.4.0, backed by `pylangacq`).

## Results

Measured on Apple M1 Pro, Python 3.14. Times are the mean of multiple runs.

### Corpus loading and access (`run_corpus.py`)

| Benchmark | Current | v3.4.0 | Speedup |
|---|---|---|---|
| `hkcancor()` cold load | 0.086s | 0.554s | 6.5x |
| `utterances()` | 0.0001s | 0.001s | 9.3x |
| `tokens()` | 0.002s | 0.006s | 3.2x |

### POS tagging (`run_pos_tagging.py`)

| Benchmark | Current | v3.4.0 | Speedup |
|---|---|---|---|
| Single sentence (8 words) | 0.00004s | 0.0002s | 3.4x |
| All HKCanCor utterances | 0.528s | 2.354s | 4.5x |

### Word segmentation (`run_word_segmentation.py`)

PyCantonese v3.4.0 uses a longest string matching algorithm for word segmentation,
while v4.0.0 uses a DAG+HMM hybrid approach for improved accuracy.

| Benchmark | Current | v3.4.0 | Speedup |
|---|---|---|---|
| Short text (7 chars) | 0.00002s | 0.0001s | 6.5x |
| Long text (75 chars) | 0.0001s | 0.0001s | 1.3x |
| Bulk (all HKCanCor utterances) | 0.272s | 0.925s | 3.4x |

## Setup

Install the v3.4.0 baseline for comparison:

```bash
bash benchmarks/setup_baseline.sh
```

This installs `pycantonese==3.4.0` (and its dependencies) into `benchmarks/_baseline/`.
The directory is `.gitignore`'d. To reinstall, delete `benchmarks/_baseline/` and re-run.

## Running benchmarks

```bash
uv run python benchmarks/run_corpus.py
uv run python benchmarks/run_pos_tagging.py
uv run python benchmarks/run_word_segmentation.py
```

Each script prints a comparison table. If the baseline is not set up, only current
version results are shown.

For machine-readable output (JSON to stdout):

```bash
uv run python benchmarks/run_corpus.py --json
```

## How the comparison works

Each benchmark script can be run standalone -- it benchmarks whatever `pycantonese` is
importable. When run without `--json`, it also invokes itself as a subprocess with
`PYTHONPATH` set so that `_baseline/` is found first. This gives clean process isolation
with no import conflicts between the two versions.

## Writing a new benchmark

1. Create `benchmarks/run_<name>.py`.
2. Import the shared utilities:

   ```python
   from _utils import bench, print_comparison, run_baseline
   ```

3. Define a `benchmark()` function that returns a dict mapping benchmark names to
   timing results. Use `bench(func, n=N)` for timing -- it returns
   `{"min": ..., "mean": ..., "max": ...}`:

   ```python
   def benchmark():
       import pycantonese

       results = {}
       results["my_benchmark"] = bench(lambda: pycantonese.some_func(), n=10)
       return results
   ```

4. Define `main()` with the `--json` / normal-mode pattern:

   ```python
   def main():
       if "--json" in sys.argv:
           print(json.dumps(benchmark()))
           return

       print("My benchmark")
       current = benchmark()
       baseline = run_baseline(__file__)
       print_comparison(current, baseline)
   ```

5. If the v3.4.0 API differs from the current API (e.g., `by_utterance` vs.
   `by_utterances`), use a compatibility helper in `_utils.py` so the same code
   works with both versions. See `words_by_utterance()` for an example.
