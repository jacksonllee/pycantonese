"""POS tagset mapping between HKCanCor and Universal Dependencies."""

from pycantonese._punctuation_marks import _PUNCTUATION_MARKS

# The Python dictionary below maps the HKCanCor tagset to the Universal
# Dependencies (UD) 2.0 tagset.
#
# HKCanCor tagset: https://github.com/fcbond/hkcancor
# UD 2.0 tagset: https://universaldependencies.org/u/pos/index.html
#
# The HKCanCor paper describes 46 tags in its tagset, but the
# actual data (as included in this pycantonese library) has 112 tags,
# all of which are listed as keys in the Python dictionary below.
#
# For convenience, if HKCanCor has a brief part-of-speech tag description,
# the description appears as a comment together with the key in the
# dictionary below, e.g., the key "a" has the comment "HKCanCor: Adjective".

_MAP = {
    "!": "PUNCT",
    '"': "PUNCT",
    "#": "X",
    "'": "PUNCT",
    ",": "PUNCT",
    "-": "PUNCT",
    ".": "PUNCT",
    "...": "PUNCT",
    "?": "PUNCT",
    "a": "ADJ",  # HKCanCor: Adjective
    "ad": "ADV",  # HKCanCor: Adjective as Adverbial
    "Ag": "ADJ",  # HKCanCor: Adjective Morpheme
    "an": "NOUN",  # HKCanCor: Adjective with Nominal Function
    "b": "ADJ",  # HKCanCor: Non-predicate Adjective
    "Bg": "ADJ",  # HKCanCor: Non-predicate Adjective Morpheme
    "c": "CCONJ",  # HKCanCor: Conjunction
    "Cg": "CCONJ",
    "d": "ADV",  # HKCanCor: Adverb
    "d1": "ADV",  # Most instances are gwai2 "ghost".
    "Dg": "ADV",  # HKCanCor: Adverb Morpheme
    "e": "INTJ",  # HKCanCor: Interjection
    "f": "ADV",  # HKCanCor: Directional Locality
    "g": "X",  # HKCanCor: Morpheme
    "g1": "VERB",  # The first A in the "A-not-AB" pattern, where AB is a verb.
    "g2": "ADJ",  # The first A in "A-not-AB", where AB is an adjective.
    "h": "PROPN",  # HKCanCor: Prefix (aa3 阿 followed by a person name)
    "i": "X",  # HKCanCor: Idiom
    "Ig": "X",
    "j": "NOUN",  # HKCanCor: Abbreviation
    "jb": "ADJ",
    "jm": "NOUN",
    "jn": "NOUN",
    "jns": "PROPN",
    "jnt": "PROPN",
    "JNTg": "PROPN",
    "jnz": "PROPN",
    "k": "X",  # HKCanCor: Suffix (sing3 性 for nouns; dei6 地 for adverbs)
    "l": "X",  # Fixed Expression
    "l1": "X",
    "Lg": "X",
    "m": "NUM",  # HKCanCor: Numeral
    "Mg": "X",
    "n": "NOUN",  # Common Noun
    "n1": "DET",  # HKCanCor: only used for ne1 呢 determiner in the upstream data https://github.com/fcbond/hkcancor/blob/41f0631acda4f6a45460483ae23cad880edaacc8/data/utf8/FC-035_v2#L3455  # noqa: E501
    "Ng": "NOUN",
    "nr": "PROPN",  # HKCanCor: Personal Name
    "ns": "PROPN",  # HKCanCor: Place Name
    "Nsg": "PROPN",
    "nt": "PROPN",  # HKCanCor: Organization Name
    "NTg": "PROPN",
    "nx": "NOUN",  # HKCanCor: Nominal Character String
    "nz": "PROPN",  # HKCanCor: Other Proper Noun
    "NZg": "PROPN",
    "o": "X",  # HKCanCor: Onomatopoeia
    "p": "ADP",  # HKCanCor: Preposition
    "q": "NOUN",  # HKCanCor: Classifier
    "Qg": "NOUN",  # HKCanCor: Classifier Morpheme
    "r": "PRON",  # HKCanCor: Pronoun
    "Rg": "PRON",  # HKCanCor: Pronoun Morpheme
    "s": "NOUN",  # HKCanCor: Space Word
    "t": "ADV",  # HKCanCor: Time Word
    "Tg": "ADV",  # HKCanCor: Time Word Morpheme
    "u": "PART",  # HKCanCor: Auxiliary (e.g., ge3 嘅 after an attributive adj)
    "Ug": "PART",  # HKCanCor: Auxiliary Morpheme
    "v": "VERB",  # HKCanCor: Verb
    "v1": "VERB",
    "vd": "ADV",  # HKCanCor: Verb as Adverbial
    "Vg": "VERB",
    "vk": "VERB",
    "vn": "NOUN",  # HKCanCor: Verb with Nominal Function
    "vu": "AUX",
    "Vug": "AUX",
    "w": "PUNCT",  # HKCanCor: Punctuation
    "x": "X",  # HKCanCor: Unclassified Item
    "xa": "ADJ",
    "xb": "ADJ",
    "xc": "CCONJ",
    "xd": "ADV",
    "xe": "INTJ",
    "xj": "X",
    "xja": "ADJ",  # HKCanCor: Only for "A" (= additional) as in "A Maths" in the upstream data https://github.com/fcbond/hkcancor/blob/41f0631acda4f6a45460483ae23cad880edaacc8/data/utf8/FC-027_v2#L4712  # noqa: E501
    "xjb": "PROPN",
    "xjn": "NOUN",
    "xjnt": "PROPN",
    "xjnz": "PROPN",
    "xjv": "VERB",
    "xl1": "INTJ",
    "xm": "NUM",
    "xn": "NOUN",
    "xNg": "NOUN",
    "xnr": "PROPN",
    "xns": "PROPN",
    "xnt": "PROPN",
    "xnx": "NOUN",
    "xnz": "PROPN",
    "xo": "NOUN",  # HKCanCor: Only for Gik1lik1gu4 in the upstream data https://github.com/fcbond/hkcancor/blob/41f0631acda4f6a45460483ae23cad880edaacc8/data/utf8/FC-R006_v2#L881  # noqa: E501
    "xp": "ADP",
    "xq": "NOUN",
    "xr": "PRON",
    "xs": "PROPN",
    "xt": "NOUN",
    "xv": "VERB",
    "xVg": "VERB",
    "xvn": "NOUN",
    "xx": "X",
    "y": "PART",  # HKCanCor: Modal Particle
    "Yg": "PART",  # HKCanCor: Modal Particle Morpheme
    "y1": "PART",
    "z": "ADJ",  # HKCanCor: Descriptive
}

# Add the Chinese full-length punctuation marks.
_MAP = {**_MAP, **{punct: "PUNCT" for punct in _PUNCTUATION_MARKS}}


def hkcancor_to_ud(tag: str | None = None):
    """Map a part-of-speech tag from HKCanCor to Universal Dependencies.

    HKCanCor uses a part-of-speech tagset of over 100 tags (46 of which
    are described at https://github.com/fcbond/hkcancor).
    For applications that would benefit from a less granular part-of-speech
    tagset (e.g., cross-linguistic natural language processing tasks),
    we can map the HKCanCor tagset to the Universal Dependencies v2 tagset
    with 17 tags (https://universaldependencies.org/u/pos/index.html)
    -- the purpose of this function.

    Any unrecognized tag is mapped to ``"X"``.

    .. versionadded:: 3.1.0

    Parameters
    ----------
    tag : str, optional
        A tag from the original HKCanCor annotated data.
        If not provided or ``None``, this function returns the entire
        dictionary of the tagset mapping from HKCanCor to UD.

    Returns
    -------
    str or dict[str, str]
        A tag from the Universal Dependencies v2 tagset, or a dictioary
        from HKCanCor to UD tags if no input is given.

    Examples
    --------
    >>> hkcancor_to_ud("v")
    'VERB'
    """
    if tag is None:
        return _MAP
    else:
        return _MAP.get(tag.strip()) or "X"
