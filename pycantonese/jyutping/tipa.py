from pycantonese.jyutping.parse_jyutping import parse_jyutping


ONSETS_TIPA = {
    "b": "p",
    "d": "t",
    "g": "k",
    "gw": "k\\super w ",
    "z": "ts",
    "p": "p\\super h ",
    "t": "t\\super h ",
    "k": "k\\super h ",
    "kw": "k\\super w\\super h ",
    "c": "ts\\super h ",
    "m": "m",
    "n": "n",
    "ng": "N",
    "f": "f",
    "h": "h",
    "s": "s",
    "l": "l",
    "w": "w",
    "j": "j",
    "": "",
}

FINALS_TIPA = {
    "i": "i",
    "ip": "ip\\textcorner ",
    "it": "it\\textcorner ",
    "ik": "Ik\\textcorner ",
    "im": "im",
    "in": "in",
    "ing": "IN",
    "iu": "iu",
    "yu": "y",
    "yut": "yt\\textcorner ",
    "yun": "yn",
    "u": "u",
    "ut": "ut\\textcorner ",
    "uk": "Uk\\textcorner ",
    "un": "un",
    "ung": "UN",
    "ui": "uY",
    "e": "E",
    "ek": "Ek\\textcorner ",
    "eng": "EN",
    "ei": "eI",
    "eot": "8t\\textcorner ",
    "eon": "8n",
    "eoi": "8Y",
    "oe": "\\oe ",
    "oek": "\\oe k\\textcorner ",
    "oeng": "\\oe N",
    "o": "O",
    "ot": "Ot\\textcorner ",
    "ok": "Ok\\textcorner ",
    "on": "On",
    "ong": "ON",
    "oi": "OY",
    "ou": "ou",
    "ap": "5p\\textcorner ",
    "at": "5t\\textcorner ",
    "ak": "5k\\textcorner ",
    "am": "5m",
    "an": "5n",
    "ang": "5N",
    "ai": "5I",
    "au": "5u",
    "aa": "a",
    "aap": "ap\\textcorner ",
    "aat": "at\\textcorner ",
    "aak": "ak\\textcorner ",
    "aam": "am",
    "aan": "an",
    "aang": "aN",
    "aai": "aI",
    "aau": "au",
    "m": "\\s{m}",
    "ng": "\\s{N}",
}

TONES_TIPA = {
    "1": "55",
    "2": "25",
    "3": "33",
    "4": "21",
    "5": "23",
    "6": "22",
}


def jyutping2tipa(jp_str):
    """
    Convert *jp_str* to a list of LaTeX TIPA strings.
    """
    jp_parsed_list = parse_jyutping(jp_str)
    tipa_list = []

    for jp_parsed in jp_parsed_list:
        onset = jp_parsed[0]
        # TODO: Separate "final" as "nucleus" and "coda" instead?
        final = jp_parsed[1] + jp_parsed[2]
        tone = jp_parsed[3]
        tipa = ONSETS_TIPA[onset] + FINALS_TIPA[final]
        tipa = tipa.strip() + TONES_TIPA[tone]
        tipa_list.append(tipa)

    return tipa_list
