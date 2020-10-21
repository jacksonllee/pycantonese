import pytest

from pycantonese import characters2jyutping


@pytest.mark.parametrize(
    "chars, expected",
    [
        (
            "香港人講廣東話。",
            [
                ("香港人", "hoeng1gong2jan4"),
                ("講", "gong2"),
                ("廣東話", "gwong2dung1waa2"),
                ("。", None),
            ],
        ),
        (
            "蛋",
            [("蛋", "daan2")],
        ),
        (
            "蛋糕",
            [("蛋糕", "daan6gou1")],
        ),
    ],
)
def test_characters2jyutping(chars, expected):
    actual = characters2jyutping(chars)
    assert actual == expected
