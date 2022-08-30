import pytest

from pycantonese import characters_to_jyutping
from pycantonese.word_segmentation import Segmenter


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
            ["香港", "人", "講", "廣東", "話", "。"],
            [
                ("香港", "hoeng1gong2"),
                ("人", "jan4"),
                ("講", "gong2"),
                ("廣東", "gwong2dung1"),
                ("話", "waa6"),
                ("。", None),
            ],
        ),
        (
            "佢成日呃like",
            [("佢", "keoi5"), ("成日", "seng4jat6"), ("呃like", "aak1lai1")],
        ),
        ("蛋", [("蛋", "daan2")]),
        ("蛋糕", [("蛋糕", "daan6gou1")]),
    ],
)
def test_characters_to_jyutping(chars, expected):
    actual = characters_to_jyutping(chars)
    assert actual == expected


@pytest.mark.parametrize(
    "chars, segmenter, expected",
    [
        ("噉樣嘅2", Segmenter(allow={"嘅2": "ge2"}), [("噉樣", "gam2joeng2"), ("嘅2", "ge2")]),
        (
            "講廣東話",
            Segmenter(allow={"廣東話": "gong2dung1waa2"}),
            [("講", "gong2"), ("廣東話", "gong2dung1waa2")],
        ),
    ],
)
def test_characters_to_jyutping_with_segmenter(chars, segmenter, expected):
    actual = characters_to_jyutping(chars, segmenter=segmenter)
    assert actual == expected
