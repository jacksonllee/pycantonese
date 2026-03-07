# AGENTS.md

## Project Overview

PyCantonese is a Python library for Cantonese linguistics and natural language
processing (NLP). It provides tools for:

- Accessing and searching the HKCanCor corpus (Hong Kong Cantonese Corpus)
- Jyutping romanization: parsing, and conversion to Yale/TIPA/IPA
- Characters-to-Jyutping mapping (via rime-cantonese data)
- Cantonese text parsing (word segmentation + POS tagging)
- Part-of-speech tagging (averaged perceptron tagger, HKCanCor-to-UD mapping)
- Stop words for Cantonese

Author/maintainer: Jackson L. Lee.
License: MIT (code), CC BY (HKCanCor data), CC BY 4.0 (rime-cantonese data).

## Repository Structure

```
├── src/
│   ├── pycantonese/           # Python package (src layout)
│   │   ├── __init__.py            # Public API exports
│   │   ├── corpus.py              # CHAT (wraps rustling), Token dataclass
│   │   ├── parsing.py             # parse_text() with ProcessPoolExecutor
│   │   ├── search.py              # Corpus search with Jyutping element matching
│   │   ├── word_segmentation.py   # DAG-HMM hybrid segmenter
│   │   ├── stop_words.py          # Cantonese stop words
│   │   ├── util.py                # Utilities and deprecation decorator
│   │   ├── _punctuation_marks.py  # Punctuation definitions
│   │   ├── jyutping/              # Jyutping romanization module
│   │   ├── pos_tagging/           # Part-of-speech tagging module
│   │   └── data/                  # Bundled data files (HKCanCor, rime-cantonese)
│   └── rust/                  # Rust source code (PyO3 extension)
│       ├── lib.rs
│       └── chat.rs
├── tests/                     # Test suite (mirrors src structure)
├── docs/source/               # Sphinx documentation (RST format)
├── Cargo.toml                 # Rust package configuration
└── pyproject.toml             # Python package configuration (maturin)
```

## Build Commands

`uv` manages the virtual environment.

```bash
uv run maturin develop                    # Build and install locally for development
uv run pytest                             # Run tests
uvx black --check src tests               # Check formatting
uvx black src tests                       # Auto-format
uvx flake8 src tests                      # Lint
uvx mypy src/                             # Type check
uv run python docs/source/build_docs.py   # Build documentation
pre-commit install                        # Install pre-commit hooks (one-time)
pre-commit run --all-files                # Run all hooks manually
```

## Code Style

- Formatter: **Black** (line length 88)
- Linter: **Flake8** (max line length 88, ignores E203)
- Type hints on all public API function signatures
- Docstrings: **NumPy style** (Parameters, Returns, Raises, Examples sections)
- Private names prefixed with `_`
- Constants in `ALL_CAPS`
- Public API exported via `__all__` in `__init__.py`

## Testing

- Framework: **pytest**
- Docstring examples are tested via **Sybil** (configured in `conftest.py`)
- Tests use `@pytest.mark.parametrize` extensively
- Test files in `tests/` mirror the `src/pycantonese/` structure

## CI/CD

GitHub Actions workflows in `.github/workflows/`:

- **python.yml**: lint (black + flake8), type check (mypy), security (pip-audit + bandit),
  test (pytest on Ubuntu + Windows, Python 3.10-3.14), build (sdist + wheels + wasm wheel)
- **release.yml**: builds wheels for Linux/macOS/Windows + wasm and publishes to PyPI
  via trusted publishing on release events

CI uses `uv` (via `astral-sh/setup-uv`) for fast dependency installation.

All jobs that compile Rust install the FlatBuffers compiler (`flatc`) before building.
The pinned version is `FLATC_VERSION: "25.12.19"` in each workflow file's `env` block.
Linux jobs download the binary from GitHub releases; macOS uses `brew install flatbuffers`;
Windows downloads from GitHub releases via PowerShell.
For manylinux wheel builds, `before-script-linux` in `maturin-action` installs `flatc`
inside the container.

## Key Dependencies

- `rustling` (>= 0.6.0): Rust-backed CHAT format corpus reading,
  part-of-speech tagging, and word segmentation

## Architecture Notes

- `Token` is a `dataclasses.dataclass` with fields: word, pos, jyutping,
  morphology, gloss, gra (grammatical relation).
- `Jyutping` is a `dataclasses.dataclass` with fields: onset, nucleus, coda, tone.
- `CHAT` wraps `rustling.chat.CHAT` via composition (rustling's CHAT cannot be subclassed).
- `parse_text()` uses `concurrent.futures.ProcessPoolExecutor` for parallel
  processing of large inputs.
- The segmenter and POS tagger use `@functools.lru_cache` for singleton patterns.
- **Model persistence**: all rustling models use **FlatBuffers binary** compressed with **zstd** (`.fb.zst` files).
  No JSON, no pickle, no gzip. Model floats are stored as **f32** on disk; internal
  computation stays f64. The f32→f64 widening cast on load is negligible overhead.
- Model files: `word_segmentation/segmenter.fb.zst`, `pos_tagging/tagger.fb.zst`.
- FlatBuffers schemas live alongside each module's `mod.rs` in rustling (e.g.
  `rustling/src/hmm/model.fbs`). Generated Rust code goes to Cargo's `OUT_DIR`
  via `build.rs` — generated files are NOT committed to git.
- Shared persistence helpers in `rustling/src/persistence.rs`:
  `read_all_bytes` and `flatbuffers_verifier_opts()`.

## Domain Context

Jyutping is the standard romanization system for Cantonese developed by the
Linguistic Society of Hong Kong. A Jyutping syllable has four components:
onset (initial consonant), nucleus (vowel), coda (final consonant/vowel), and
tone (1-6). Example: "gwong2" = onset "gw", nucleus "o", coda "ng", tone "2".

HKCanCor (Hong Kong Cantonese Corpus) is a transcribed corpus of spoken
Cantonese, stored in CHAT format (a format common in language acquisition
research, handled by the rustling library).
