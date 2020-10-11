import unicodedata

from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.util import endswithoneof, startswithoneof


ONSETS_YALE = {
    "b": "b",
    "d": "d",
    "g": "g",
    "gw": "gw",
    "z": "j",
    "p": "p",
    "t": "t",
    "k": "k",
    "kw": "k",
    "c": "ch",
    "m": "m",
    "n": "n",
    "ng": "ng",
    "f": "f",
    "h": "h",
    "s": "s",
    "l": "l",
    "w": "w",
    "j": "y",
    "": "",
}

NUCLEI_YALE = {
    "aa": "aa",
    "a": "a",
    "i": "i",
    "yu": "yu",
    "u": "u",
    "oe": "eu",
    "e": "e",
    "eo": "eu",
    "o": "o",
    "m": "m",
    "ng": "ng",
}

CODAS_YALE = {
    "p": "p",
    "t": "t",
    "k": "k",
    "m": "m",
    "n": "n",
    "ng": "ng",
    "i": "i",
    "u": "u",
    "": "",
}


def jyutping2yale(jp_str, as_list=False):
    """
    Convert *jp_str* to Yale.

    :param as_list: If True (default: False), return a list of Yale strings
        for individual syllables.
    """
    jp_parsed_list = parse_jyutping(jp_str)
    yale_list = []

    for jp_parsed in jp_parsed_list:
        onset = ONSETS_YALE[jp_parsed[0]]
        nucleus = NUCLEI_YALE[jp_parsed[1]]
        coda = CODAS_YALE[jp_parsed[2]]
        tone = jp_parsed[3]  # still in parse_jyutping

        # jyutping2yale system uses "h" to mark the three low tones
        if tone in {"4", "5", "6"}:
            low_tone_h = "h"
        else:
            low_tone_h = ""

        # in jyutping2yale, long "aa" vowel with no coda is denoted by "a"
        if nucleus == "aa" and coda == "":
            nucleus = "a"

        # when nucleus is "yu"...
        # 1. disallow "yyu" (when onset is "y")
        # 2. change nucleus "yu" into "u" -- this is a hack for adding tone
        #       diacritic, since we don't want "y" to bear the diacritic
        if nucleus == "yu":
            if onset == "y":
                onset = ""
            nucleus = "u"

        # when nucleus is "ng"
        # the tone diacritic has to be on "g" but not "n"
        # now we pretend that the nucleus is "g", and will prepend the "n" back
        # at the end
        if nucleus == "ng":
            nucleus = "g"

        # add the jyutping2yale tone diacritic to the first nucleus letter
        # parse_jyutping tone 1      --> add macron
        # parse_jyutping tone 2 or 5 --> add acute
        # parse_jyutping tone 4      --> add grave
        # parse_jyutping tone 3 or 6 --> (no diacritic)
        # If the accented letter doesn't exist in unicode, use the combining
        # accent instead.

        letter = nucleus[0]  # nucleus 1st letter
        unicode_letter_name = unicodedata.name(letter)
        if tone == "1":
            try:
                letter_with_diacritic = unicodedata.lookup(
                    unicode_letter_name + " WITH MACRON"
                )
            except KeyError:
                letter_with_diacritic = letter + "\u0304"
        elif tone in {"2", "5"}:
            try:
                letter_with_diacritic = unicodedata.lookup(
                    unicode_letter_name + " WITH ACUTE"
                )
            except KeyError:
                letter_with_diacritic = letter + "\u0301"
        elif tone == "4":
            try:
                letter_with_diacritic = unicodedata.lookup(
                    unicode_letter_name + " WITH GRAVE"
                )
            except KeyError:
                letter_with_diacritic = letter + "\u0300"
        else:
            # either tone 3 or tone 6
            letter_with_diacritic = letter
        nucleus = letter_with_diacritic + nucleus[1:]

        # add back "y" if the nucleus is "yu"
        # ("y" was taken away for convenience in adding tone diacritic)
        if jp_parsed[1] == "yu":
            nucleus = "y" + nucleus

        # add back "n" if the nucleus is "ng"
        # ('n' was taken away so that tone diacritic is on "g" but not "n")
        if jp_parsed[1] == "ng":
            nucleus = "n" + nucleus

        # parse_jyutping final "eu" should be jyutping2yale "ew" (not "eu")
        if coda == "u" and nucleus == "e":
            coda = "w"

        # save the resultant jyutping2yale
        if coda in {"i", "u", "w"} and tone in {"4", "5", "6"}:
            yale = onset + nucleus + coda + low_tone_h
        else:
            yale = onset + nucleus + low_tone_h + coda
        yale_list.append(yale)

    if as_list:
        return yale_list

    # Output yale_list as a string
    # Check if there's potential ambiguity when Yale strings are concatenated

    # Ambiguity case 1:
    #   1st syllable coda is one of the "ambiguous_consonants"
    #   and 2nd syllable starts with a vowel *letter*

    # Ambiguity case 2:
    #   1st syllable has no coda and 2nd syllable starts with one of the
    #   "ambiguous_consonants"
    #   e.g., hei3hau6 'climate' --> heihauh
    #   (middle "h" for tone in 1st syllable or being onset of 2nd syllable?)

    if len(yale_list) == 1:
        return yale_list[0]

    ambiguous_consonants = {"h", "p", "t", "k", "m", "n", "ng"}
    vowel_letters = {
        "a",
        "e",
        "i",
        "o",
        "u",
        "á",
        "é",
        "í",
        "ó",
        "ú",
        "à",
        "è",
        "ì",
        "ò",
        "ù",
        "ā",
        "ē",
        "ī",
        "ō",
        "ū",
    }

    output_str = ""

    for i in range(len(yale_list) - 1):
        yale1 = yale_list[i]
        yale2 = yale_list[i + 1]

        ambiguous = False

        # test case 1:
        if endswithoneof(yale1, ambiguous_consonants) and startswithoneof(
            yale2, vowel_letters
        ):
            ambiguous = True

        # test case 2:
        if (
            not ambiguous
            and not endswithoneof(yale1, ambiguous_consonants)
            and startswithoneof(yale2, ambiguous_consonants)
        ):
            ambiguous = True

        output_str += yale1

        if ambiguous:
            output_str += "'"

    output_str += yale_list[-1]

    return output_str
