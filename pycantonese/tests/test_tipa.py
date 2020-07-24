from pycantonese.jyutping.parse_jyutping import ONSETS, TONES
from pycantonese.jyutping.tipa import ONSETS_TIPA, TONES_TIPA, jyutping2tipa


# TODO def test_correct_nucleus_set():
# TODO def test_correct_coda_set():


def test_correct_onset_set():
    assert set(ONSETS_TIPA.keys()) == ONSETS


def test_correct_tone_set():
    assert set(TONES_TIPA.keys()) == TONES


def test_jyutping2tipa():
    assert jyutping2tipa("m4goi1") == ["\\s{m}21", "kOY55"]
    assert jyutping2tipa("gwong2dung1waa2") == [
        "k\\super w ON25",
        "tUN55",
        "wa25",
    ]
