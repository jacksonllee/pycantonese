import unittest

import pytest
from pylangacq.tests.test_chat import BaseTestCHATReader

import pycantonese


_HKCANCOR = pycantonese.hkcancor()

skip_because_tokens_are_different = pytest.mark.skip(
    reason=(
        "PyCantonese's Token class has the extra ``jyutping`` and ``gloss``"
        "attributes and "
        "turns meaningless ``mor`` into ``None`` (not done at ``pylangacq.Reader``)."
    ),
)


def test_hkcancor_word_count():
    assert len(_HKCANCOR.words()) == 153_654


def test_hkcancor_character_count():
    assert len(_HKCANCOR.characters()) == 191_851


class TestPyCantoneseCHATReader(BaseTestCHATReader, unittest.TestCase):
    """Test the CHAT reader methods by using ``pycantonese.CHATReader``."""

    reader_class = pycantonese.CHATReader

    @skip_because_tokens_are_different
    def test_ipsyn(self):
        pass

    @skip_because_tokens_are_different
    def test_tokens(self):
        pass

    @skip_because_tokens_are_different
    def test_tokens_by_utterances(self):
        pass

    @skip_because_tokens_are_different
    def test_utterances(self):
        pass
