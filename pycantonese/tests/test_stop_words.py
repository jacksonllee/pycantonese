from pycantonese import stop_words


_DEFAULT_STOP_WORDS = stop_words()


def test_stop_words():
    _stop_words = stop_words()
    assert "唔" in _stop_words


def test_stop_words_add_one_word():
    _stop_words = stop_words(add="foobar")
    assert "foobar" in _stop_words
    assert len(_stop_words) - len(_DEFAULT_STOP_WORDS) == 1


def test_stop_words_remove_one_word():
    _stop_words = stop_words(remove="唔")
    assert "唔" not in _stop_words
    assert len(_DEFAULT_STOP_WORDS) - len(_stop_words) == 1


def test_stop_words_add_multiple_words():
    _stop_words = stop_words(add=["foo", "bar", "baz"])
    assert {"foo", "bar", "baz"}.issubset(_stop_words)
    assert len(_stop_words) - len(_DEFAULT_STOP_WORDS) == 3


def test_stop_words_remove_multiple_words():
    _stop_words = stop_words(remove=["唔", "乜嘢", "其他"])
    assert not {"唔", "乜嘢", "其他"}.issubset(_stop_words)
    assert len(_DEFAULT_STOP_WORDS) - len(_stop_words) == 3
