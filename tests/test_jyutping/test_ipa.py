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
def test_jyutping_to_ipa(jp_str, expected):
    assert jyutping_to_ipa(jp_str, as_list=False) == expected
