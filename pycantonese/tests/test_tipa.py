import pytest

from pycantonese.jyutping.parse_jyutping import ONSETS, TONES
from pycantonese.jyutping.tipa import ONSETS_TIPA, TONES_TIPA, jyutping_to_tipa


# TODO def test_correct_nucleus_set():
# TODO def test_correct_coda_set():


def test_correct_onset_set():
    assert set(ONSETS_TIPA.keys()) == ONSETS


def test_correct_tone_set():
    assert set(TONES_TIPA.keys()) == TONES


@pytest.mark.parametrize("input_", ["", None])
def test_null_input(input_):
    assert jyutping_to_tipa(input_) == []


def test_jyutping_to_tipa():
    assert jyutping_to_tipa("m4goi1") == ["\\s{m}21", "kOY55"]
    assert jyutping_to_tipa("gwong2dung1waa2") == [
        "k\\super w ON25",
        "tUN55",
        "wa25",
    ]
