from pycantonese.jyutping.parse_jyutping import ONSETS, NUCLEI, CODAS
from pycantonese.jyutping.yale import ONSETS_YALE, NUCLEI_YALE, CODAS_YALE


def test_correct_onset_set():
    assert set(ONSETS_YALE.keys()) == ONSETS


def test_correct_nucleus_set():
    assert set(NUCLEI_YALE.keys()) == NUCLEI


def test_correct_coda_set():
    assert set(CODAS_YALE.keys()) == CODAS
