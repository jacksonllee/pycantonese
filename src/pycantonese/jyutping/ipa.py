from functools import lru_cache
from typing import Dict, List, Optional, Union

from .parse_jyutping import parse_jyutping


_ONSETS = {
    "b": "p",
    "d": "t",
    "g": "k",
    "gw": "kʷ",
    "z": "ts",
    "p": "pʰ",
    "t": "tʰ",
    "k": "kʰ",
    "kw": "kʷʰ",
    "c": "tsʰ",
    "m": "m",
    "n": "n",
    "ng": "ŋ",
    "f": "f",
    "h": "h",
    "s": "s",
    "l": "l",
    "w": "w",
    "j": "j",
    "": "",
}

_NUCLEI = {
    "aa": "aː",
    "a": "ɐ",
    "i": "i",  # ɪ before ng, k
    "yu": "y",
    "u": "u",  # ʊ before ng, k
    "oe": "œ",
    "e": "ɛ",  # e before i
    "eo": "ɵ",
    "o": "ɔ",  # o before u
    "m": "m",
    "n": "n",
    "ng": "ŋ",
}

_CODAS = {
    "p": "p̚",
    "t": "t̚",
    "k": "k̚",
    "m": "m",
    "n": "n",
    "ng": "ŋ",
    "i": "i",  # y after eo, u, o
    "u": "u",
    "": "",
}

_TONES = {
    "1": "55",
    "2": "25",
    "3": "33",
    "4": "21",
    "5": "23",
    "6": "22",
}


@lru_cache
def _replace(current, parsed, part_to_match, matches, default):
    if getattr(parsed, part_to_match) in matches:
        return default
    else:
        return current


def jyutping_to_ipa(
    jp_str: str,
    as_list: bool = True,
    *,
    onsets: Optional[Dict[str, str]] = None,
    nuclei: Optional[Dict[str, str]] = None,
    codas: Optional[Dict[str, str]] = None,
    tones: Optional[Dict[str, str]] = None,
) -> Union[List[str], str]:
    """Convert Jyutping romanization into IPA.

    The Jyutping-to-IPA mapping is based on Matthews and Yip (2011: 461-463).

    Parameters
    ----------
    jp_str : str
        Jyutping romanization for one or multiple characters
    as_list : bool, optional
        If ``True`` (the default), the returned value is a list of strings
        where each string is the IPA representation of each Cantonese / Chinese
        character based on the input Jyutping.
    onsets : dict[str, str], optional
        If provided, it must be a dictionary that maps Jyutping onsets to
        the desired IPA symbols for customization. For example, Jyutping "z"
        maps to IPA /ts/ by default. Passing in ``{"z": "tʃ"}`` would map
        "z" to /tʃ/ instead.
    nuclei : dict[str, str], optional
        If provided, it must be a dictionary that maps Jyutping nuclei to
        the desired IPA symbols for customization. For example, Jyutping "i"
        maps to IPA /i/ by default. Passing in ``{"i": "iː"}`` would map
        "i" to /iː/ instead.
    codas : dict[str, str], optional
        If provided, it must be a dictionary that maps Jyutping codas to
        the desired IPA symbols for customization. For example, Jyutping "p"
        maps to IPA /p̚/ by default. Passing in ``{"p": "p"}`` would map
        "p" to /p/ instead.
    tones : dict[str, str], optional
        If provided, it must be a dictionary that maps Jyutping tones to
        the desired IPA symbols for customization. For example, Jyutping "2"
        (high-rising tone)
        maps to IPA /25/ by default. Passing in ``{"2": "35"}`` would map
        Jyutping "2" to /35/ instead.

    Returns
    -------
    list[str] | str

    Examples
    --------
    >>> jyutping_to_ipa('gwong2dung1waa2')  # 廣東話 Cantonese
    ['kʷɔŋ25', 'tʊŋ55', 'waː25']
    >>> jyutping_to_ipa('gwong2dung1waa2', as_list=False)
    'kʷɔŋ25 tʊŋ55 waː25'
    >>> jyutping_to_ipa('ci1', onsets={'c': "tʃ'"})
    ["tʃ'i55"]
    >>> jyutping_to_ipa('ci1', tones={'1': "˥"})
    ['tsʰi˥']
    """
    jp_parsed_list = parse_jyutping(jp_str)
    ipa_list = []

    for jp_parsed in jp_parsed_list:
        onset = _ONSETS[jp_parsed.onset]
        nucleus = _NUCLEI[jp_parsed.nucleus]
        coda = _CODAS[jp_parsed.coda]
        tone = _TONES[jp_parsed.tone]

        if (n := jp_parsed.nucleus) == "i":
            nucleus = _replace(nucleus, jp_parsed, "coda", ("ng", "k"), "ɪ")
        elif n == "u":
            nucleus = _replace(nucleus, jp_parsed, "coda", ("ng", "k"), "ʊ")
        elif n == "e":
            nucleus = _replace(nucleus, jp_parsed, "coda", ("i",), "e")
        elif n == "o":
            nucleus = _replace(nucleus, jp_parsed, "coda", ("u",), "o")

        if jp_parsed.coda == "i":
            coda = _replace(coda, jp_parsed, "nucleus", ("eo", "u", "o"), "y")

        onset = (onsets or {}).get(jp_parsed.onset, onset)
        nucleus = (nuclei or {}).get(jp_parsed.nucleus, nucleus)
        coda = (codas or {}).get(jp_parsed.coda, coda)
        tone = (tones or {}).get(jp_parsed.tone, tone)

        ipa_list.append(onset + nucleus + coda + tone)

    if as_list:
        return ipa_list
    else:
        return " ".join(ipa_list)
