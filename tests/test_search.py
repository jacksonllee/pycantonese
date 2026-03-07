import pycantonese
from pycantonese.corpus import Token

_NONES = {"mor": None, "gloss": None, "gra": None}

_HKCANCOR = pycantonese.hkcancor()


def test_find_verbs_in_hkcancor():
    all_verbs = _HKCANCOR.search(pos="^[Vv]")
    assert len(all_verbs) == 29726
    assert all_verbs[:10] == [
        Token(word="去", pos="v", jyutping="heoi3", **_NONES),
        Token(word="去", pos="v", jyutping="heoi3", **_NONES),
        Token(word="旅行", pos="vn", jyutping="leoi5hang4", **_NONES),
        Token(word="有冇", pos="v1", jyutping="jau5mou5", **_NONES),
        Token(word="要", pos="vu", jyutping="jiu3", **_NONES),
        Token(word="有得", pos="vu", jyutping="jau5dak1", **_NONES),
        Token(word="冇得", pos="vu", jyutping="mou5dak1", **_NONES),
        Token(word="去", pos="v", jyutping="heoi3", **_NONES),
        Token(word="係", pos="v", jyutping="hai6", **_NONES),
        Token(word="係", pos="v", jyutping="hai6", **_NONES),
    ]


def test_by_token_false():
    all_verbs = _HKCANCOR.search(pos="^[Vv]", by_token=False)
    assert len(all_verbs) == 29726
    expected = ["去", "去", "旅行", "有冇", "要", "有得", "冇得", "去", "係", "係"]
    assert all_verbs[:10] == expected


def test_by_utterance_true():
    all_verbs = _HKCANCOR.search(pos="^[Vv]", by_utterance=True)
    assert len(all_verbs) == 29726
    print(all_verbs[:2])
    assert all_verbs[:2] == [
        [
            Token(word="喂", pos="e", jyutping="wai3", **_NONES),
            Token(word="遲", pos="a", jyutping="ci4", **_NONES),
            Token(word="啲", pos="u", jyutping="di1", **_NONES),
            Token(word="去", pos="v", jyutping="heoi3", **_NONES),
            Token(word="唔", pos="d", jyutping="m4", **_NONES),
            Token(word="去", pos="v", jyutping="heoi3", **_NONES),
            Token(word="旅行", pos="vn", jyutping="leoi5hang4", **_NONES),
            Token(word="啊", pos="y", jyutping="aa3", **_NONES),
            Token(word="?", pos="", jyutping=None, **_NONES),
        ],
        [
            Token(word="喂", pos="e", jyutping="wai3", **_NONES),
            Token(word="遲", pos="a", jyutping="ci4", **_NONES),
            Token(word="啲", pos="u", jyutping="di1", **_NONES),
            Token(word="去", pos="v", jyutping="heoi3", **_NONES),
            Token(word="唔", pos="d", jyutping="m4", **_NONES),
            Token(word="去", pos="v", jyutping="heoi3", **_NONES),
            Token(word="旅行", pos="vn", jyutping="leoi5hang4", **_NONES),
            Token(word="啊", pos="y", jyutping="aa3", **_NONES),
            Token(word="?", pos="", jyutping=None, **_NONES),
        ],
    ]


def test_word_range():
    all_verbs = _HKCANCOR.search(pos="^[Vv]", word_range=(1, 2))
    assert len(all_verbs) == 29726
    assert all_verbs[:2] == [
        [
            Token(word="啲", pos="u", jyutping="di1", **_NONES),
            Token(word="去", pos="v", jyutping="heoi3", **_NONES),
            Token(word="唔", pos="d", jyutping="m4", **_NONES),
            Token(word="去", pos="v", jyutping="heoi3", **_NONES),
        ],
        [
            Token(word="唔", pos="d", jyutping="m4", **_NONES),
            Token(word="去", pos="v", jyutping="heoi3", **_NONES),
            Token(word="旅行", pos="vn", jyutping="leoi5hang4", **_NONES),
            Token(word="啊", pos="y", jyutping="aa3", **_NONES),
        ],
    ]


def test_utterance_range():
    all_verbs = _HKCANCOR.search(pos="^[Vv]", utterance_range=(0, 1))
    assert len(all_verbs) == 29726
    assert all_verbs[:2] == [
        [
            [
                Token(word="喂", pos="e", jyutping="wai3", **_NONES),
                Token(word="遲", pos="a", jyutping="ci4", **_NONES),
                Token(word="啲", pos="u", jyutping="di1", **_NONES),
                Token(word="去", pos="v", jyutping="heoi3", **_NONES),
                Token(word="唔", pos="d", jyutping="m4", **_NONES),
                Token(word="去", pos="v", jyutping="heoi3", **_NONES),
                Token(word="旅行", pos="vn", jyutping="leoi5hang4", **_NONES),
                Token(word="啊", pos="y", jyutping="aa3", **_NONES),
                Token(word="?", pos="", jyutping=None, **_NONES),
            ],
            [
                Token(word="你", pos="r", jyutping="nei5", **_NONES),
                Token(word="老公", pos="n", jyutping="lou5gung1", **_NONES),
                Token(word="有冇", pos="v1", jyutping="jau5mou5", **_NONES),
                Token(word="平", pos="a", jyutping="peng4", **_NONES),
                Token(word="機票", pos="n", jyutping="gei1piu3", **_NONES),
                Token(word="啊", pos="y", jyutping="aa3", **_NONES),
                Token(word="?", pos="", jyutping=None, **_NONES),
            ],
        ],
        [
            [
                Token(word="喂", pos="e", jyutping="wai3", **_NONES),
                Token(word="遲", pos="a", jyutping="ci4", **_NONES),
                Token(word="啲", pos="u", jyutping="di1", **_NONES),
                Token(word="去", pos="v", jyutping="heoi3", **_NONES),
                Token(word="唔", pos="d", jyutping="m4", **_NONES),
                Token(word="去", pos="v", jyutping="heoi3", **_NONES),
                Token(word="旅行", pos="vn", jyutping="leoi5hang4", **_NONES),
                Token(word="啊", pos="y", jyutping="aa3", **_NONES),
                Token(word="?", pos="", jyutping=None, **_NONES),
            ],
            [
                Token(word="你", pos="r", jyutping="nei5", **_NONES),
                Token(word="老公", pos="n", jyutping="lou5gung1", **_NONES),
                Token(word="有冇", pos="v1", jyutping="jau5mou5", **_NONES),
                Token(word="平", pos="a", jyutping="peng4", **_NONES),
                Token(word="機票", pos="n", jyutping="gei1piu3", **_NONES),
                Token(word="啊", pos="y", jyutping="aa3", **_NONES),
                Token(word="?", pos="", jyutping=None, **_NONES),
            ],
        ],
    ]
