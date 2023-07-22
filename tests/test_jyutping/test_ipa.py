import pytest

from pycantonese.jyutping.ipa import jyutping_to_ipa


@pytest.mark.parametrize(
    "jp_str, as_list, expected",
    [
        ("taa1", True, ["tʰaː55"]),
    ],
)
def test_jyutping_to_ipa(jp_str, as_list, expected):
    assert jyutping_to_ipa(jp_str, as_list) == expected
