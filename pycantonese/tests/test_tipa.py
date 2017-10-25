from pycantonese.jyutping.parse_jyutping import ONSETS, TONES
from pycantonese.jyutping.tipa import ONSETS_TIPA, TONES_TIPA


# TODO def test_correct_nucleus_set():
# TODO def test_correct_coda_set():


def test_correct_onset_set():
    assert set(ONSETS_TIPA.keys()) == ONSETS


def test_correct_tone_set():
    assert set(TONES_TIPA.keys()) == TONES
