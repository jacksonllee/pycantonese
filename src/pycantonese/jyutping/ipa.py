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
    "i": "i",  # TODO ɪ before ng, k
    "yu": "y",
    "u": "u",  # TODO ʊ before ng, k
    "oe": "œ",
    "e": "ɛ",  # TODO e before i
    "eo": "ɵ",
    "o": "ɔ",  # TODO o before u
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
    "i": "i",  # TODO y after eo, u, o
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


def jyutping_to_ipa(
    jp_str: str,
    as_list: bool = True,
    *,
    onsets: Optional[Dict[str, str]] = None,
    nuclei: Optional[Dict[str, str]] = None,
    codas: Optional[Dict[str, str]] = None,
    tones: Optional[Dict[str, str]] = None
) -> Union[List[str], str]:
    jp_parsed_list = parse_jyutping(jp_str)
    ipa_list = []

    for jp_parsed in jp_parsed_list:
        onset = _ONSETS[jp_parsed.onset]
        nucleus = _NUCLEI[jp_parsed.nucleus]
        coda = _CODAS[jp_parsed.coda]
        tone = _TONES[jp_parsed.tone]

        ipa_list.append(onset + nucleus + coda + tone)

    if as_list:
        return ipa_list
    else:
        return " ".join(ipa_list)
