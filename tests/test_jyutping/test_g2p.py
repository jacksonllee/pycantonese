import pytest

from pycantonese import g2p


@pytest.mark.parametrize(
    "chars, expected",
    [
        (
            "香港人講廣東話。",
            [
                ("香港人", "hœŋ55 kɔŋ25 jɐn21"),
                ("講", "kɔŋ25"),
                ("廣東話", "kʷɔŋ25 tʊŋ55 waː25"),
                ("。", None),
            ],
        ),
        (
            ["廣東", "話"],
            [
                ("廣東", "kʷɔŋ25 tʊŋ55"),
                ("話", "waː22"),
            ],
        ),
        (
            "佢成日呃like",
            [
                ("佢", "kʰɵy23"),
                ("成日", "sɪŋ21 jɐt̚22"),
                ("呃", "ŋaːk̚55"),
                ("like", None),
            ],
        ),
        ("蛋", [("蛋", "taːn25")]),
        ("蛋糕", [("蛋糕", "taːn22 kou55")]),
    ],
)
def test_g2p(chars, expected):
    assert g2p(chars) == expected


@pytest.mark.parametrize("input_", ["", []])
def test_g2p__empty_input(input_):
    assert g2p(input_) == []


def test_g2p__custom_onsets():
    # Default for onset "ng" is "ŋ"; override to "".
    assert g2p("我", onsets={"ng": ""}) == [("我", "ɔ23")]


def test_g2p__custom_nuclei():
    # Default for "aa" is "aː"; override to "a".
    assert g2p("蛋糕", nuclei={"aa": "a"}) == [("蛋糕", "tan22 kou55")]


def test_g2p__custom_codas():
    # Default for "k" is "k̚"; override to plain "k".
    assert g2p("食", codas={"k": "k"}) == [("食", "sɪk22")]


def test_g2p__custom_tones():
    # Default for Jyutping tone 6 is "22"; override to Chao tone letter ˨˨.
    assert g2p("食", tones={"6": "˨˨"}) == [("食", "sɪk̚˨˨")]
