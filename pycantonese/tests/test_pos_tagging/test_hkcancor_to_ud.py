import pytest

from pycantonese.pos_tagging.hkcancor_to_ud import hkcancor_to_ud


@pytest.mark.parametrize(
    "tag, expected",
    [
        ("V", "VERB"),
        ("v", "VERB"),
        ("V ", "VERB"),
        ("V1", "VERB"),
        ("foobar", "X"),
    ],
)
def test_hkcancor_to_ud(tag, expected):
    assert hkcancor_to_ud(tag) == expected
