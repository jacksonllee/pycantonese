from pathlib import Path

import pycantonese
from pycantonese.corpus import CHAT, Token, Utterance

_HKCANCOR = pycantonese.hkcancor()


def test_hkcancor_word_count():
    assert len(_HKCANCOR.words()) == 153_656


def test_hkcancor_character_count():
    assert len(_HKCANCOR.characters()) == 191_853


def test_utterances_returns_pycantonese_types():
    utts = _HKCANCOR.utterances()
    assert len(utts) > 0
    u = utts[0]
    assert isinstance(u, Utterance)
    assert isinstance(u.tokens[0], Token)


def test_utterances_tokens_have_jyutping():
    utts = _HKCANCOR.utterances()
    u = utts[0]
    # First token is 喂 with jyutping wai3
    assert u.tokens[0].word == "喂"
    assert u.tokens[0].jyutping == "wai3"


def test_utterances_preserve_fields():
    utts = _HKCANCOR.utterances()
    u = utts[0]
    assert isinstance(u.participant, str)
    assert u.audible is None or isinstance(u.audible, str)
    assert isinstance(u.tiers, dict)


def test_utterances_by_file():
    utts_by_file = _HKCANCOR.utterances(by_file=True)
    assert len(utts_by_file) > 0
    assert isinstance(utts_by_file[0], list)
    assert isinstance(utts_by_file[0][0], Utterance)
    assert isinstance(utts_by_file[0][0].tokens[0], Token)


_DATA_DIR = Path(pycantonese.__file__).parent / "data" / "hkcancor"


def test_from_dir_with_path():
    reader = CHAT.from_dir(_DATA_DIR)
    assert reader.n_files > 0


def test_from_files_with_path():
    paths = sorted(_DATA_DIR.glob("*.cha"))[:3]
    reader = CHAT.from_files(paths)
    assert reader.n_files == len(paths)


def test_to_files(tmp_path):
    reader = CHAT.from_strs(["@UTF8\n@Begin\n@End\n"], strict=False)
    out = tmp_path / "output"
    reader.to_files(out)
    reader2 = CHAT.from_dir(out)
    assert reader2.words() == reader.words()


def test_read_chat_with_path():
    reader = pycantonese.read_chat(_DATA_DIR)
    assert reader.n_files > 0


def test_from_utterances_round_trip():
    utts = _HKCANCOR.utterances()
    reader = CHAT.from_utterances(utts)
    assert reader.words() == _HKCANCOR.words()


def test_from_utterances_subset():
    utts = _HKCANCOR.utterances()
    subset = utts[:5]
    reader = CHAT.from_utterances(subset)
    reader_utts = reader.utterances()
    assert len(reader_utts) == 5
    for orig, new in zip(subset, reader_utts):
        assert orig.participant == new.participant
        assert len(orig.tokens) == len(new.tokens)
        for ot, nt in zip(orig.tokens, new.tokens):
            assert ot.word == nt.word
            assert ot.jyutping == nt.jyutping


def test_from_utterances_empty():
    reader = CHAT.from_utterances([])
    assert reader.words() == []
    assert reader.utterances() == []
