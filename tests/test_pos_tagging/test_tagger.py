import pytest

from pycantonese import pos_tag


def test_pos_tag():
    expected = [("我", "PRON")]
    assert pos_tag(["我"]) == expected
    assert pos_tag(["我"], tagset="universal") == expected


def test_pos_tag_hkcancor_tagset():
    assert pos_tag(["我"], tagset="hkcancor") == [("我", "R")]


def test_pos_tag_wrong_input_type():
    with pytest.raises(TypeError):
        pos_tag("我")


def test_pos_tag_unknown_tagset():
    with pytest.raises(ValueError):
        pos_tag(["我"], tagset="unknown tagset")
