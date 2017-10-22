from pycantonese.jyutping.parse_jyutping import ONSETS, NUCLEI, CODAS
from pycantonese.jyutping.yale import ONSETS_YALE, NUCLEI_YALE, CODAS_YALE


def test_correct_onset_set():
    assert ONSETS_YALE.keys() == ONSETS


def test_correct_nucleus_set():
    assert NUCLEI_YALE.keys() == NUCLEI


def test_correct_coda_set():
    assert CODAS_YALE.keys() == CODAS
