"""Chinese full-length punctuation marks.

See: https://en.wikipedia.org/wiki/Chinese_punctuation
"""

_PUNCTUATION_MARKS = """
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
"""

_PUNCTUATION_MARKS = frozenset(_PUNCTUATION_MARKS.strip())
