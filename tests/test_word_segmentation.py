import pytest

from pycantonese import segment


@pytest.mark.parametrize(
    "chars, expected",
    [
        ("廣東話容唔容易學？", ["廣東話", "容", "唔", "容易", "學", "？"]),
        ("佢淨係識呃like", ["佢", "淨係", "識", "呃", "like"]),
        # Whitespace in input string has no effect.
        ("廣東 話容唔容 易學？ ", ["廣東話", "容", "唔", "容易", "學", "？"]),
        ("\n 廣東話容唔容易學？ ", ["廣東話", "容", "唔", "容易", "學", "？"]),
        ("我今晚會 have dinner", ["我", "今晚", "會", "have", "dinner"]),
        ("我今晚會have dinner", ["我", "今晚", "會", "have", "dinner"]),
        (
            "我今晚會 have dinner 定係 go shopping?",
            ["我", "今晚", "會", "have", "dinner", "定係", "go", "shopping", "?"],
        ),
        ("我今晚會have dinner.", ["我", "今晚", "會", "have", "dinner", "."]),
        ("我今晚會have dinner？", ["我", "今晚", "會", "have", "dinner", "？"]),
    ],
)
def test_segment(chars, expected):
    actual = segment(chars)
    assert actual == expected
