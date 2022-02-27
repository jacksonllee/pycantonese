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
    # TODO assert parse_jyutping('hm4') == [('h', 'm', '', '4')]
    assert parse_jyutping("ng5") == [Jyutping("", "ng", "", "5")]
    assert parse_jyutping("m4") == [Jyutping("", "m", "", "4")]
    assert parse_jyutping("n3") == [Jyutping("", "n", "", "3")]


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


def test_no_noda():
    assert parse_jyutping("gaa1") == [Jyutping("g", "aa", "", "1")]
