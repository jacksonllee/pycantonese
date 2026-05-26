import pytest

from pycantonese.jyutping.ipa import jyutping_to_ipa


@pytest.mark.parametrize(
    "jp_str, expected",
    [
        ("taa1", "tʰaː55"),
        ("zi1", "tsi55"),
        ("ging6", "kɪŋ22"),
        ("wu4", "wu21"),
        ("puk1", "pʰʊk̚55"),
        ("je5", "jɛ23"),
        ("sei3", "sei33"),
        ("ngo5", "ŋɔ23"),
        ("mou2", "mou25"),
        ("gui6", "kuy22"),
        ("baau3", "paːu33"),
        ("ngau4", "ŋɐu21"),
        ("syu1", "sy55"),
        ("goeng1", "kœŋ55"),
        ("geok3", "kɵk̚33"),
    ],
)
def test_jyutping_to_ipa__base_cases(jp_str, expected):
    assert jyutping_to_ipa(jp_str) == [expected]


def test_jyutping_to_ipa__multi_syllable_str():
    assert jyutping_to_ipa("gwong2dung1waa2") == ["kʷɔŋ25 tʊŋ55 waː25"]


def test_jyutping_to_ipa__list_input():
    assert jyutping_to_ipa(["gwong2dung1", "waa2"]) == ["kʷɔŋ25 tʊŋ55", "waː25"]


def test_jyutping_to_ipa__space_separated_str():
    assert jyutping_to_ipa("gwong2 dung1 waa2") == ["kʷɔŋ25 tʊŋ55 waː25"]


def test_jyutping_to_ipa__empty():
    assert jyutping_to_ipa("") == []
    assert jyutping_to_ipa([]) == []


def test_jyutping_to_ipa__custom_onsets():
    assert jyutping_to_ipa("ci1", onsets={"c": "tʃ'"}) == ["tʃ'i55"]


def test_jyutping_to_ipa__custom_nuclei():
    assert jyutping_to_ipa("ci1", nuclei={"i": "iː"}) == ["tsʰiː55"]


def test_jyutping_to_ipa__custom_tones():
    assert jyutping_to_ipa("ci2", tones={"2": "35"}) == ["tsʰi35"]


def test_jyutping_to_ipa__custom_codas():
    assert jyutping_to_ipa("sip3", codas={"p": "p"}) == ["sip33"]
