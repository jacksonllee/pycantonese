import pytest

from pycantonese.jyutping import parse_jyutping


def test_parse_jyutping_wrong_data_type():
    with pytest.raises(ValueError):
        parse_jyutping(123)


def test_parse_jyutping_syllabic_nasals():
    # TODO assert parse_jyutping('hm4') == [('h', 'm', '', '4')]
    assert parse_jyutping('ng5') == [('', 'ng', '', '5')]
    assert parse_jyutping('m4') == [('', 'm', '', '4')]
    assert parse_jyutping('n3') == [('', 'n', '', '3')]
