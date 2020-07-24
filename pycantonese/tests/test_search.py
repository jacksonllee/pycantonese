from pycantonese.tests.test_corpus import HKCANCOR


def test_find_verbs_in_hkcancor():
    all_verbs = HKCANCOR.search(pos="^V")
    assert len(all_verbs) == 29012
    assert all_verbs[:10] == [
        ("去", "V", "heoi3", ""),
        ("去", "V", "heoi3", ""),
        ("旅行", "VN", "leoi5hang4", ""),
        ("有冇", "V1", "jau5mou5", ""),
        ("要", "VU", "jiu3", ""),
        ("有得", "VU", "jau5dak1", ""),
        ("冇得", "VU", "mou5dak1", ""),
        ("去", "V", "heoi3", ""),
        ("係", "V", "hai6", ""),
        ("係", "V", "hai6", ""),
    ]
