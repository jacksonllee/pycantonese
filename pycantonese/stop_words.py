"""Stop words for Cantonese."""

_STOP_WORDS = """
一啲
一定
不如
不過
之後
乜
乜嘢
人哋
但係
你
你哋
佢
佢哋
係
個
其他
冇
再
到
即
即係
原來
去
又
可以
可能
同
同埋
吖
呀
呢
咁
咗
咩
咪
哦
哩
哩個
哩啲
哩度
哩樣
唔
唔使
唔係
啊
啲
喎
喺
喺度
嗯
嗰
嗰個
嗰啲
嗰度
嘅
嘢
噉
噉樣
因為
多
太
好
如果
就
已經
幾
幾多
得
想
應該
成日
我
我哋
或者
所以
最
會
有
有冇
有啲
未
梗係
然之後
由
真係
睇
知
而
而家
自己
要
覺得
話
諗
講
譬如
跟住
返
過
邊個
都
點
點樣
點解
""".strip().split()


def stop_words(add=None, remove=None):
    """Return Cantonese stop words.

    .. versionadded:: 2.2.0

    Parameters
    ----------
    add : iterable[str], optional
        Stop words to add.
    remove : iterable[str], optional
        Stop words to remove.

    Returns
    -------
    set[str]

    Examples
    --------
    >>> stop_words_1 = stop_words()
    >>> len(stop_words_1)
    104
    >>> '香港' in stop_words_1
    False
    >>> stop_words_1  # doctest: +SKIP
    {'一啲', '一定', '不如', '不過', ...}
    >>>
    >>> stop_words_2 = stop_words(add='香港')
    >>> len(stop_words_2)
    105
    >>> '香港' in stop_words_2
    True
    """
    _stop_words = set(_STOP_WORDS)
    if add:
        if isinstance(add, str):
            _stop_words.add(add)
        else:
            # assume "add" is an iterable of strings
            _stop_words |= set(add)
    if remove:
        if isinstance(remove, str):
            _stop_words.remove(remove)
        else:
            # assume "remove" is an iterable of strings
            _stop_words -= set(remove)
    return _stop_words
