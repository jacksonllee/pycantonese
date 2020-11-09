import pytest

from pycantonese import pos_tag


# TODO: Write more test cases.
def test_pos_tag():
    assert pos_tag(["我"]) == [("我", "PRON")]


def test_pos_tag_wrong_input_type():
    with pytest.raises(TypeError):
        pos_tag("我")
