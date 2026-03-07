"""Test Jyutping parsing.

Some tests mirror what the documentation demonstrates.
If these tests fail, the documentation should probably be updated as well
(and the bugs should be fixed, if any).
"""

import pytest

from pycantonese import parse_jyutping
from pycantonese.jyutping.parse_jyutping import Jyutping


def test_basic_case_gwong2dung1waa2():
    assert parse_jyutping("gwong2dung1waa2") == [
        Jyutping("gw", "o", "ng", "2"),
        Jyutping("d", "u", "ng", "1"),
        Jyutping("w", "aa", "", "2"),
    ]


def test_wrong_data_type():
    with pytest.raises(ValueError):
        parse_jyutping(123)


@pytest.mark.parametrize("input_", ["", None])
def test_null_input(input_):
    assert parse_jyutping(input_) == []


def test_syllabic_nasals():
    assert parse_jyutping("ng5") == [Jyutping("", "ng", "", "5")]
    assert parse_jyutping("m4") == [Jyutping("", "m", "", "4")]
    assert parse_jyutping("n3") == [Jyutping("", "n", "", "3")]


def test_onset_with_syllabic_nasal_nucleus():
    assert parse_jyutping("hm4") == [Jyutping("h", "m", "", "4")]
    assert parse_jyutping("hng6") == [Jyutping("h", "ng", "", "6")]


def test_invalid_tone():
    with pytest.raises(ValueError) as e:
        parse_jyutping("lei7")
    assert "tone error" in str(e.value)


def test_no_tone():
    with pytest.raises(ValueError) as e:
        parse_jyutping("lei")
    assert "tone error" in str(e.value)


def test_fewer_than_2_characters():
    with pytest.raises(ValueError) as e:
        parse_jyutping("3")
    assert "fewer than 2 characters" in str(e.value)


def test_invalid_coda():
    with pytest.raises(ValueError) as e:
        parse_jyutping("leil3")
    assert "coda error" in str(e.value)


def test_invalid_nucleus():
    with pytest.raises(ValueError) as e:
        parse_jyutping("sk3")
    assert "nucleus error" in str(e.value)


def test_invalid_onset():
    with pytest.raises(ValueError) as e:
        parse_jyutping("shaa1")
    assert "onset error" in str(e.value)


def test_coda_ng():
    assert parse_jyutping("hoeng1") == [Jyutping("h", "oe", "ng", "1")]


def test_no_coda():
    assert parse_jyutping("gaa1") == [Jyutping("g", "aa", "", "1")]


def test_multi_syllable_nei5hou2():
    assert parse_jyutping("nei5hou2") == [
        Jyutping("n", "e", "i", "5"),
        Jyutping("h", "o", "u", "2"),
    ]


@pytest.mark.parametrize(
    "input_, expected",
    [
        ("baa1", Jyutping("b", "aa", "", "1")),
        ("gwai3", Jyutping("gw", "a", "i", "3")),
        ("kwong4", Jyutping("kw", "o", "ng", "4")),
        ("ngoi6", Jyutping("ng", "o", "i", "6")),
        ("jyu5", Jyutping("j", "yu", "", "5")),
        ("zoi3", Jyutping("z", "o", "i", "3")),
        ("ven1", Jyutping("v", "e", "n", "1")),  # as in van仔
    ],
)
def test_various_onsets(input_, expected):
    assert parse_jyutping(input_) == [expected]


def test_case_insensitivity():
    assert parse_jyutping("GWong2") == parse_jyutping("gwong2")


@pytest.mark.parametrize(
    "input_, expected",
    [
        ("aa3", Jyutping("", "aa", "", "3")),
        ("i1", Jyutping("", "i", "", "1")),
        ("o2", Jyutping("", "o", "", "2")),
        ("u1", Jyutping("", "u", "", "1")),
        ("e6", Jyutping("", "e", "", "6")),
    ],
)
def test_syllabic_vowels(input_, expected):
    assert parse_jyutping(input_) == [expected]
