"""Test code snippets embedded in the docs.

Reference: https://sybil.readthedocs.io/en/latest/use.html#pytest
"""

from doctest import ELLIPSIS
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
    # DocTestParser with the allow_tabs kwarg from my own fork's sybil package
    # to ignore tabs in CHAT transcriptions
    parsers=[DocTestParser(optionflags=ELLIPSIS, allow_tabs=True), skip],
    pattern="*.rst",
    fixtures=["tempdir"],
).pytest()
