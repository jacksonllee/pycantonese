from pycantonese import characters2jyutping


def test_characters2jyutping():
    actual = characters2jyutping("香港人講廣東話")
    expected = ["hoeng1", "gong2", "jan4", "gong2", "gwong2", "dung1", "waa2"]
    assert actual == expected
