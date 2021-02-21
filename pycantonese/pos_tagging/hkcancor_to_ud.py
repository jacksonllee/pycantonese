"""POS tagset mapping between HKCanCor and Universal Dependencies."""

from pycantonese.pos_tagging.punctuation_marks import _PUNCTUATION_MARKS


# The Python dictionary below maps the HKCanCor tagset to the Universal
# Dependencies (UD) 2.0 tagset.
#
# HKCanCor tagset: http://compling.hss.ntu.edu.sg/hkcancor/
# UD 2.0 tagset: https://universaldependencies.org/u/pos/index.html
#
# The HKCanCor paper describes 46 tags in its tagset, but the
# actual data (as included in this pycantonese library) has 112 tags,
# all of which are listed as keys in the Python dictionary below.
#
# For convenience, if HKCanCor has a brief part-of-speech tag description,
# the description appears as a comment together with the key in the
# dictionary below, e.g., the key "A" has the comment "HKCanCor: Adjective".

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
    "A": "ADJ",  # HKCanCor: Adjective
    "AD": "ADV",  # HKCanCor: Adjective as Adverbial
    "AG": "ADJ",  # HKCanCor: Adjective Morpheme
    "AIRWAYS0": "PROPN",
    "AN": "NOUN",  # HKCanCor: Adjective with Nominal Function
    "AND": "PROPN",  # In one instance of "Chilli and Pepper"
    "B": "ADJ",  # HKCanCor: Non-predicate Adjective
    "BG": "ADJ",  # HKCanCor: Non-predicate Adjective Morpheme
    "BEAN0": "PROPN",  # In one instance of "Mr Bean"
    "C": "CCONJ",  # HKCanCor: Conjunction
    "CENTRE0": "NOUN",  # In one instance of "career centre"
    "CG": "CCONJ",
    "D": "ADV",  # HKCanCor: Adverb
    "D1": "ADV",  # Most instances are gwai2 "ghost".
    "DG": "ADV",  # HKCanCor: Adverb Morpheme
    "E": "INTJ",  # HKCanCor: Interjection
    "ECHO0": "PROPN",  # In one instance of "Big Echo"
    "F": "ADV",  # HKCanCor: Directional Locality
    "G": "X",  # HKCanCor: Morpheme
    "G1": "V",  # The first A in the "A-not-AB" pattern, where AB is a verb.
    "G2": "ADJ",  # The first A in "A-not-AB", where AB is an adjective.
    "H": "PROPN",  # HKCanCor: Prefix (aa3 阿 followed by a person name)
    "HILL0": "PROPN",  # In "Benny Hill"
    "I": "X",  # HKCanCor: Idiom
    "IG": "X",
    "J": "NOUN",  # HKCanCor: Abbreviation
    "JB": "ADJ",
    "JM": "NOUN",
    "JN": "NOUN",
    "JNS": "PROPN",
    "JNT": "PROPN",
    "JNZ": "PROPN",
    "K": "X",  # HKCanCor: Suffix (sing3 性 for nouns; dei6 地 for adverbs)
    "KONG": "PROPN",  # In "Hong Kong"
    "L": "X",  # Fixed Expression
    "L1": "X",
    "LG": "X",
    "M": "NUM",  # HKCanCor: Numeral
    "MG": "X",
    "MONTY0": "PROPN",  # In "Full Monty"
    "MOUNTAIN0": "PROPN",  # In "Blue Mountain"
    "N": "NOUN",  # Common Noun
    "N1": "DET",  # HKCanCor: only used for ne1 呢 determiner in the upstream data https://github.com/fcbond/hkcancor/blob/41f0631acda4f6a45460483ae23cad880edaacc8/data/utf8/FC-035_v2#L3455  # noqa: E501
    "NG": "NOUN",
    "NR": "PROPN",  # HKCanCor: Personal Name
    "NS": "PROPN",  # HKCanCor: Place Name
    "NSG": "PROPN",
    "NT": "PROPN",  # HKCanCor: Organization Name
    "NX": "NOUN",  # HKCanCor: Nominal Character String
    "NZ": "PROPN",  # HKCanCor: Other Proper Noun
    "O": "X",  # HKCanCor: Onomatopoeia
    "P": "ADP",  # HKCanCor: Preposition
    "PEPPER0": "PROPN",  # In "Chilli and Pepper"
    "Q": "NOUN",  # HKCanCor: Classifier
    "QG": "NOUN",  # HKCanCor: Classifier Morpheme
    "R": "PRON",  # HKCanCor: Pronoun
    "RG": "PRON",  # HKCanCor: Pronoun Morpheme
    "S": "NOUN",  # HKCanCor: Space Word
    "SOUND0": "PROPN",  # In "Manchester's Sound"
    "T": "ADV",  # HKCanCor: Time Word
    "TELECOM0": "PROPN",  # In "Hong Kong Telecom"
    "TG": "ADV",  # HKCanCor: Time Word Morpheme
    "TOUCH0": "PROPN",  # In "Don't Touch" (a magazine)
    "U": "PART",  # HKCanCor: Auxiliary (e.g., ge3 嘅 after an attributive adj)
    "UG": "PART",  # HKCanCor: Auxiliary Morpheme
    "U0": "PROPN",  # U as in "Hong Kong U" (= The University of Hong Kong)
    "V": "VERB",  # HKCanCor: Verb
    "V1": "VERB",
    "VD": "ADV",  # HKCanCor: Verb as Adverbial
    "VG": "VERB",
    "VK": "VERB",
    "VN": "NOUN",  # HKCanCor: Verb with Nominal Function
    "VU": "AUX",
    "VUG": "AUX",
    "W": "PUNCT",  # HKCanCor: Punctuation
    "X": "X",  # HKCanCor: Unclassified Item
    "XA": "ADJ",
    "XB": "ADJ",
    "XC": "CCONJ",
    "XD": "ADV",
    "XE": "INTJ",
    "XJ": "X",
    "XJB": "PROPN",
    "XJN": "NOUN",
    "XJNT": "PROPN",
    "XJNZ": "PROPN",
    "XJV": "VERB",
    "XJA": "ADJ",  # HKCanCor: Only for "A" (= additional) as in "A Maths" in the upstream data https://github.com/fcbond/hkcancor/blob/41f0631acda4f6a45460483ae23cad880edaacc8/data/utf8/FC-027_v2#L4712  # noqa: E501
    "XL1": "INTJ",
    "XM": "NUM",
    "XN": "NOUN",
    "XNG": "NOUN",
    "XNR": "PROPN",
    "XNS": "PROPN",
    "XNT": "PROPN",
    "XNX": "NOUN",
    "XNZ": "PROPN",
    "XO": "NOUN",  # HKCanCor: Only for Gik1lik1gu4 in the upstream data https://github.com/fcbond/hkcancor/blob/41f0631acda4f6a45460483ae23cad880edaacc8/data/utf8/FC-R006_v2#L881  # noqa: E501
    "XP": "ADP",
    "XQ": "NOUN",
    "XR": "PRON",
    "XS": "PROPN",
    "XT": "NOUN",
    "XV": "VERB",
    "XVG": "VERB",
    "XVN": "NOUN",
    "XX": "X",
    "Y": "PART",  # HKCanCor: Modal Particle
    "YG": "PART",  # HKCanCor: Modal Particle Morpheme
    "Y1": "PART",
    "Z": "ADJ",  # HKCanCor: Descriptive
}

# Add the Chinese full-length punctuation marks.
_MAP = {**_MAP, **{punct: "PUNCT" for punct in _PUNCTUATION_MARKS}}


def hkcancor_to_ud(tag: str = None):
    """Map a part-of-speech tag from HKCanCor to Universal Dependencies.

    HKCanCor uses a part-of-speech tagset of over 100 tags (46 of which
    are described at http://compling.hss.ntu.edu.sg/hkcancor/).
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
    >>> hkcancor_to_ud("V")
    'VERB'
    """
    if tag is None:
        return _MAP
    else:
        return _MAP.get(tag.strip().upper()) or "X"
