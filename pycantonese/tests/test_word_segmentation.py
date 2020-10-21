import pytest

from pycantonese import segment


@pytest.mark.parametrize(
    "unsegmented, expected",
    [
        ("廣東話容唔容易學？", ["廣東話", "容", "唔容易", "學", "？"]),
        ("美國芝加哥", ["美國", "芝加哥"]),
    ],
)
def test_segment(unsegmented, expected):
    assert segment(unsegmented) == expected
