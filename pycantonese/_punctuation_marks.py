from pylangacq._punctuation_marks import _PUNCTUATION_MARKS as _PYLANGACQ_PUNCT


# See: https://en.wikipedia.org/wiki/Chinese_punctuation
_CHINESE_PUNCT = """
，
。
！
？
；
：
（
）
「
」
［
］
【
】
《
》
〈
〉
、
‧
…
—
～
""".strip()

_PUNCTUATION_MARKS = frozenset().union(list(_CHINESE_PUNCT), _PYLANGACQ_PUNCT)
