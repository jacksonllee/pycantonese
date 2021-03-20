import pycantonese


HKCANCOR = pycantonese.hkcancor()


def test_hkcancor_word_count():
    assert len(HKCANCOR.words()) == 153_654


def test_hkcancor_character_count():
    assert len(HKCANCOR.characters()) == 191_851
