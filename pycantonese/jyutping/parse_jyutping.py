ONSETS = {
    "b",
    "d",
    "g",
    "gw",
    "z",
    "p",
    "t",
    "k",
    "kw",
    "c",
    "m",
    "n",
    "ng",
    "f",
    "h",
    "s",
    "l",
    "w",
    "j",
    "",
}

NUCLEI = {"aa", "a", "i", "yu", "u", "oe", "e", "eo", "o", "m", "ng"}

CODAS = {"p", "t", "k", "m", "n", "ng", "i", "u", ""}

TONES = {"1", "2", "3", "4", "5", "6"}


def parse_jyutping(jp_str):
    """
    Parse *jp_str* as a string of Cantonese Jyutping romanization for one or
    multiple characters
    and return a list of 4-tuples, each as (onset, nucleus, coda, tone)
    """
    # check jp_str as a valid argument string
    if not isinstance(jp_str, str):
        raise ValueError("argument needs to be a string -- " + repr(jp_str))
    jp_str = jp_str.lower()

    # parse jp_str as multiple jp strings
    jp_list = []
    jp_current = ""
    for c in jp_str:
        jp_current = jp_current + c
        if c.isdigit():
            jp_list.append(jp_current)
            jp_current = ""

    if not jp_str[-1].isdigit():
        # TODO: erro msg should be "no invalid tone detected" or something?
        raise ValueError("tone error -- " + repr(jp_str[-1]))

    jp_parsed_list = []

    for jp in jp_list:

        if len(jp) < 2:
            raise ValueError(
                "jyutping string has fewer than " "2 characters -- " + repr(jp)
            )

        tone = jp[-1]
        cvc = jp[:-1]

        # tone
        if tone not in TONES:
            raise ValueError("tone error -- " + repr(jp))

        # coda
        if not (cvc[-1] in "ieaouptkmng"):
            raise ValueError("coda error -- " + repr(jp))

        if cvc in ["m", "n", "ng", "i", "e", "aa", "o", "u"]:
            jp_parsed_list.append(("", cvc, "", tone))
            continue
        elif cvc[-2:] == "ng":
            coda = "ng"
            cv = cvc[:-2]
        elif (
            (cvc[-1] in "ptkmn")
            or ((cvc[-1] == "i") and (cvc[-2] in "eaou"))
            or ((cvc[-1] == "u") and (cvc[-2] in "ieao"))
        ):
            coda = cvc[-1]
            cv = cvc[:-1]
        else:
            coda = ""
            cv = cvc

        # nucleus, and then onset
        nucleus = ""

        while cv[-1] in "ieaouy":
            nucleus = cv[-1] + nucleus
            cv = cv[:-1]
            if not cv:
                break

        if not nucleus:
            raise ValueError("nucleus error -- " + repr(jp))

        onset = cv

        if onset not in ONSETS:
            raise ValueError("onset error -- " + repr(jp))

        jp_parsed_list.append((onset, nucleus, coda, tone))

    return jp_parsed_list


def parse_final(final):
    """
    Parse *final* as (nucleus, coda).
    """
    for i in range(1, len(final) + 1):
        possible_nucleus = final[:i]
        possible_coda = final[i:]

        if (possible_nucleus in NUCLEI) and (possible_coda in CODAS):
            return possible_nucleus, possible_coda
    return None
