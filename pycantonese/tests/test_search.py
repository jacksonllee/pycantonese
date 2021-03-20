from pycantonese.corpus import Token
from pycantonese.tests.test_corpus import HKCANCOR


def test_find_verbs_in_hkcancor():
    all_verbs = HKCANCOR.search(pos="^V")
    assert len(all_verbs) == 29726
    assert all_verbs[:10] == [
        Token(word="去", pos="V", jyutping="heoi3", mor=None, gra=None),
        Token(word="去", pos="V", jyutping="heoi3", mor=None, gra=None),
        Token(word="旅行", pos="VN", jyutping="leoi5hang4", mor=None, gra=None),
        Token(word="有冇", pos="V1", jyutping="jau5mou5", mor=None, gra=None),
        Token(word="要", pos="VU", jyutping="jiu3", mor=None, gra=None),
        Token(word="有得", pos="VU", jyutping="jau5dak1", mor=None, gra=None),
        Token(word="冇得", pos="VU", jyutping="mou5dak1", mor=None, gra=None),
        Token(word="去", pos="V", jyutping="heoi3", mor=None, gra=None),
        Token(word="係", pos="V", jyutping="hai6", mor=None, gra=None),
        Token(word="係", pos="V", jyutping="hai6", mor=None, gra=None),
    ]
