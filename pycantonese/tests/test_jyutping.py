import pytest

from pycantonese.jyutping import parse_jyutping


def test_parse_jyutping_wrong_data_type():
    with pytest.raises(ValueError):
        parse_jyutping(123)
