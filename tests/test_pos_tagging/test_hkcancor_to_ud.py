import pytest

from pycantonese.pos_tagging.hkcancor_to_ud import hkcancor_to_ud, _MAP

# # UD 2.0 tagset: https://universaldependencies.org/u/pos/index.html
_UD_TAGSET = frozenset(
    "ADJ ADV INTJ NOUN PROPN VERB "
    "ADP AUX CCONJ DET NUM PART PRON SCONJ "
    "PUNCT SYM X".split()
)


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


def test_hkcancor_to_ud_all_tags():
    assert hkcancor_to_ud() == _MAP


def test_hkcancor_to_ud_map_has_only_ud_tags():
    invalid_pairs = []
    for hkcancor_tag, ud_tag in _MAP.items():
        if ud_tag not in _UD_TAGSET:
            invalid_pairs.append((hkcancor_tag, ud_tag))
    if invalid_pairs:
        raise ValueError(f"Invalid pairs: {invalid_pairs}")
