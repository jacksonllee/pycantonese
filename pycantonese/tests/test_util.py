import pytest

from pycantonese.util import split_characters_with_alphanum


@pytest.mark.parametrize(
    "chars, expected",
    [
        ("廣東話", ("廣", "東", "話")),
        ("proposal", ("proposal",)),
        ("hap唔happy", ("hap", "唔", "happy")),
        ("high-tech唔好用", ("high-tech", "唔", "好", "用")),
        ("唔好成日開party", ("唔", "好", "成", "日", "開", "party")),
        ("死chur爛chur", ("死", "chur", "爛", "chur")),
    ],
)
def test_split_characters_with_english(chars, expected):
    assert split_characters_with_alphanum(chars) == expected
