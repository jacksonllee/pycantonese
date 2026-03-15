from __future__ import annotations

import dataclasses
import re

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
    "v",
    "",
}

NUCLEI = {"aa", "a", "i", "yu", "u", "oe", "e", "eo", "o", "m", "ng"}

CODAS = {"p", "t", "k", "m", "n", "ng", "i", "u", ""}

TONES = {"1", "2", "3", "4", "5", "6"}

# Two-char alternatives are listed before single-char ones (e.g., "aa" before "a",
# "ng" before "n"). Python's NFA regex engine tries alternatives left-to-right and
# backtracks on failure, which correctly resolves ambiguities like "m4" (onset="m"
# fails -> backtracks to nucleus="m") and "hng6" (onset="h", nucleus="ng").
_JYUTPING_SYLLABLE_RE = re.compile(
    r"(?P<onset>gw|kw|ng|[bdgzptkcmnfhslwjv])?"
    r"(?P<nucleus>aa|oe|eo|yu|ng|[aeioumn])"
    r"(?P<coda>ng|[iptkmnu])?"
    r"(?P<tone>[1-6])"
)


@dataclasses.dataclass
class Jyutping:
    """Jyutping representation of a Chinese/Cantonese character.

    Attributes:
        onset (str): Onset
        nucleus (str): Nucleus
        coda (str): Coda
        tone (str): Tone
    """

    __slots__ = ("onset", "nucleus", "coda", "tone")
    onset: str
    nucleus: str
    coda: str
    tone: str

    def __str__(self):
        """Combine onset + nucleus + coda + tone."""
        return f"{self.onset}{self.nucleus}{self.coda}{self.tone}"

    def __hash__(self):
        return hash(self.__str__())

    @property
    def final(self):
        """Return the final (= nucleus + coda)."""
        return f"{self.nucleus}{self.coda}"


def parse_jyutping(jp_str) -> list[Jyutping]:
    """Parse Jyutping romanization into onset, nucleus, coda, and tone.

    Args:
        jp_str (str): Jyutping romanization for one or multiple characters.

    Returns:
        list[Jyutping]

    Raises:
        ValueError: If the Jyutping romanization is illegal (e.g., with
            unrecognized elements).

    Examples:
        >>> parse_jyutping("gwong2dung1waa2")  # 廣東話, Cantonese
        [Jyutping(onset='gw', nucleus='o', coda='ng', tone='2'),
         Jyutping(onset='d', nucleus='u', coda='ng', tone='1'),
         Jyutping(onset='w', nucleus='aa', coda='', tone='2')]
    """
    if not jp_str:
        return []

    if not isinstance(jp_str, str):
        raise ValueError("argument needs to be a string -- " + repr(jp_str))
    jp_str = jp_str.lower()

    # Split into individual syllables at tone digits
    jp_list = []
    jp_current = ""
    for c in jp_str:
        jp_current = jp_current + c
        if c.isdigit():
            jp_list.append(jp_current)
            jp_current = ""

    if not jp_str[-1].isdigit():
        raise ValueError("tone error -- " + repr(jp_str[-1]))

    jp_parsed_list = []

    for jp in jp_list:
        if len(jp) < 2:
            raise ValueError(
                "jyutping string has fewer than 2 characters -- " + repr(jp)
            )

        match = _JYUTPING_SYLLABLE_RE.fullmatch(jp)
        if match:
            jp_parsed_list.append(
                Jyutping(
                    match.group("onset") or "",
                    match.group("nucleus"),
                    match.group("coda") or "",
                    match.group("tone"),
                )
            )
        else:
            _raise_detailed_error(jp)

    return jp_parsed_list


def _raise_detailed_error(jp: str) -> None:
    """Analyze a failed Jyutping syllable and raise a descriptive ValueError."""
    tone = jp[-1]
    if tone not in TONES:
        raise ValueError("tone error -- " + repr(jp))

    cvc = jp[:-1]

    if cvc[-1] not in "ieaouptkmng":
        raise ValueError("coda error -- " + repr(jp))

    # Try to extract onset by stripping vowels from the right
    cv = cvc
    if cvc[-2:] == "ng":
        cv = cvc[:-2]
    elif cvc[-1] in "ptkmn" or cvc[-1] in "iu":
        cv = cvc[:-1]

    nucleus = ""
    while cv and cv[-1] in "ieaouy":
        nucleus = cv[-1] + nucleus
        cv = cv[:-1]

    if not nucleus:
        raise ValueError("nucleus error -- " + repr(jp))

    if cv not in ONSETS:
        raise ValueError("onset error -- " + repr(jp))

    raise ValueError("invalid jyutping -- " + repr(jp))


def _parse_final(final):
    """Parse a final into its nucleus and coda.

    Args:
        final (str): The final to parse.

    Returns:
        tuple[str]
    """
    for i in range(1, len(final) + 1):
        possible_nucleus = final[:i]
        possible_coda = final[i:]

        if (possible_nucleus in NUCLEI) and (possible_coda in CODAS):
            return possible_nucleus, possible_coda
    return None
