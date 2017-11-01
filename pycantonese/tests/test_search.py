import pycantonese


HKCANCOR = pycantonese.hkcancor()


def test_count_all_verbs():
    all_verbs = HKCANCOR.search(pos='^V')
    assert len(all_verbs) == 29012
