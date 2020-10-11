from pycantonese import jyutping2yale
from pycantonese.jyutping.parse_jyutping import ONSETS, NUCLEI, CODAS
from pycantonese.jyutping.yale import (
    ONSETS_YALE,
    NUCLEI_YALE,
    CODAS_YALE,
)


def test_correct_onset_set():
    assert set(ONSETS_YALE.keys()) == ONSETS


def test_correct_nucleus_set():
    assert set(NUCLEI_YALE.keys()) == NUCLEI


def test_correct_coda_set():
    assert set(CODAS_YALE.keys()) == CODAS


def test_jyutping2yale_m4goi1():
    assert jyutping2yale("m4goi1") == "m̀hgōi"


def test_jyutping2yale_gwong2dung1waa2():
    assert jyutping2yale("gwong2dung1waa2") == "gwóngdūngwá"
