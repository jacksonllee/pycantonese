# Standard CHAT punctuation marks (from CHAT transcription format)
_CHAT_PUNCT = frozenset({".", "?", "!", ",", ";"})


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

_PUNCTUATION_MARKS = frozenset().union(list(_CHINESE_PUNCT), _CHAT_PUNCT)
