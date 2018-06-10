import pycantonese


HKCANCOR = pycantonese.hkcancor()


def almost_equal(x, y, tolerance):
    # Don't bother to import numpy's assert_almost_equal just for testing
    return abs(x - y) <= tolerance


def test_hkcancor_word_count():
    assert almost_equal(len(HKCANCOR.words()), 149781, tolerance=3)


def test_hkcancor_character_count():
    assert almost_equal(len(HKCANCOR.characters()), 186888, tolerance=3)
