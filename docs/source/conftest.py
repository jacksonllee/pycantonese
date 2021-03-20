"""Test code snippets embedded in the docs.

Reference: https://sybil.readthedocs.io/en/latest/use.html#pytest
"""

from doctest import NORMALIZE_WHITESPACE
from os import chdir, getcwd
from shutil import rmtree
from tempfile import mkdtemp

import pytest
from sybil import Sybil
from sybil.parsers.doctest import DocTestParser
from sybil.parsers.skip import skip


@pytest.fixture(scope="module")
def tempdir():
    path = mkdtemp()
    cwd = getcwd()
    try:
        chdir(path)
        yield path
    finally:
        chdir(cwd)
        rmtree(path)


pytest_collect_file = Sybil(
    parsers=[DocTestParser(optionflags=NORMALIZE_WHITESPACE), skip],
    pattern="*.rst",
    fixtures=["tempdir"],
).pytest()
