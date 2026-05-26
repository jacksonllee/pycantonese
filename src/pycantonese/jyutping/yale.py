from __future__ import annotations

import unicodedata

from pycantonese.jyutping.parse_jyutping import parse_jyutping

ONSETS_YALE = {
    "b": "b",
    "d": "d",
    "g": "g",
    "gw": "gw",
    "z": "j",
    "p": "p",
    "t": "t",
    "k": "k",
    "kw": "kw",
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
    "v": "v",
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


def jyutping_to_yale(jp: str | list[str]) -> list[str]:
    """Convert Jyutping romanization into Yale romanization.

    Args:
        jp (str or list[str]): A Jyutping romanization string for a single
            word (any number of syllables, optionally separated by spaces),
            or a list of such strings carrying explicit word segmentation
            (one word per element).

    Returns:
        list[str]: A list with one element per input word. Each element is
        the Yale romanization of that word, with syllables separated by a
        single space.

    Raises:
        ValueError: If the Jyutping romanization is illegal (e.g., with
            unrecognized elements).

    Examples:
        >>> jyutping_to_yale("gwong2dung1waa2")  # 廣東話, Cantonese
        ['gwóng dūng wá']
        >>> jyutping_to_yale(["gwong2dung1", "waa2"])
        ['gwóng dūng', 'wá']
        >>> jyutping_to_yale("hei3hau6")  # 氣候, climate
        ['hei hauh']
    """
    if not jp:
        return []
    words = [jp] if isinstance(jp, str) else jp
    return [" ".join(_word_to_yale_syllables(word)) for word in words]


def _word_to_yale_syllables(word: str) -> list[str]:
    jp_parsed_list = parse_jyutping(word)
    yale_list = []

    for jp_parsed in jp_parsed_list:
        onset = ONSETS_YALE[jp_parsed.onset]
        nucleus = NUCLEI_YALE[jp_parsed.nucleus]
        coda = CODAS_YALE[jp_parsed.coda]
        tone = jp_parsed.tone  # still in parse_jyutping

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
        if jp_parsed.nucleus == "yu":
            nucleus = "y" + nucleus

        # add back "n" if the nucleus is "ng"
        # ('n' was taken away so that tone diacritic is on "g" but not "n")
        if jp_parsed.nucleus == "ng":
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

    return yale_list


# Inverse mapping tables for Yale -> Jyutping.
# Yale onsets and codas have unique inverses once kw->kw is corrected above.
_ONSETS_JYUTPING = {v: k for k, v in ONSETS_YALE.items()}
_CODAS_JYUTPING = {v: k for k, v in CODAS_YALE.items()}

# Yale nucleus "eu" maps from both Jyutping "oe" and "eo"; resolved by coda
# at parse time (see _resolve_eu). Other Yale nuclei invert cleanly.
_NUCLEI_JYUTPING_UNAMBIGUOUS = {
    "aa": "aa",
    "a": "a",  # Jyutping "aa" with no coda is written "a" in Yale; reversed below
    "i": "i",
    "yu": "yu",
    "u": "u",
    "e": "e",
    "o": "o",
    "m": "m",
    "ng": "ng",
}

# Yale onsets ordered longest-first for greedy matching.
_YALE_ONSETS_ORDERED = (
    "ch",
    "gw",
    "kw",
    "ng",
    "b",
    "d",
    "g",
    "j",
    "p",
    "t",
    "k",
    "m",
    "n",
    "f",
    "h",
    "s",
    "l",
    "w",
    "y",
    "v",
)

# Yale nuclei ordered longest-first (base-letter form, no diacritic).
_YALE_NUCLEI_ORDERED = ("aa", "eu", "yu", "ng", "a", "e", "i", "o", "u", "m")

_YALE_VOWEL_LETTERS = set("aeiou")

# Map a base vowel letter + combining-accent character to (vowel, tone-marker).
# tone-marker: "macron" -> tone 1; "acute" -> tone 2 or 5; "grave" -> tone 4;
# None -> tone 3 or 6 (disambiguated by trailing "h").
_DIACRITIC_TO_MARK = {
    "̄": "macron",
    "́": "acute",
    "̀": "grave",
}


def _strip_diacritic(nucleus_chars):
    """Given an NFD-decomposed nucleus string (base letters + combining marks),
    return (base_nucleus_str, tone_mark) where tone_mark is one of
    {"macron", "acute", "grave", None}. Raises ValueError on unknown marks.
    """
    base = []
    mark = None
    for ch in nucleus_chars:
        if unicodedata.category(ch) == "Mn":
            found = _DIACRITIC_TO_MARK.get(ch)
            if found is None:
                raise ValueError("unrecognized diacritic in nucleus -- " + repr(ch))
            if mark is not None and mark != found:
                raise ValueError("multiple tone diacritics in one syllable")
            mark = found
        else:
            base.append(ch)
    return "".join(base), mark


def _tone_from(mark, has_h):
    if mark == "macron":
        return "1"
    if mark == "acute":
        return "5" if has_h else "2"
    if mark == "grave":
        if not has_h:
            raise ValueError("grave (tone 4) requires 'h' low-tone marker")
        return "4"
    return "6" if has_h else "3"


def _resolve_eu(coda_yale):
    """For nucleus 'eu', pick Jyutping 'oe' or 'eo' based on Yale coda."""
    if coda_yale in {"n", "t", "i"}:
        return "eo"
    return "oe"


def _split_word_syllables(word):
    """Split a Yale word into a list of raw syllable strings. Both apostrophe
    `'` and whitespace are honored as explicit syllable-break hints inside
    the word."""
    # Normalize apostrophes to spaces, then split on any whitespace.
    pieces = [p for p in word.replace("'", " ").split() if p]
    syllables = []
    for piece in pieces:
        syllables.extend(_split_piece(piece))
    return syllables


def _split_piece(piece):
    """Split a Yale string with no apostrophes into syllables."""
    nfd = unicodedata.normalize("NFD", piece)
    syllables = []
    i = 0
    n = len(nfd)
    while i < n:
        end = _find_syllable_end(nfd, i)
        syllables.append(nfd[i:end])
        i = end
    return syllables


def _find_syllable_end(s, start):
    """Find the end index (exclusive) of the syllable starting at s[start].

    Yale low-tone 'h' placement depends on coda type:
    - stop/nasal coda (p/t/k/m/n/ng): h comes BEFORE coda  -> nucleus + h + coda
    - glide coda (i/u/w):             h comes AFTER  coda  -> nucleus + coda + h
    - no coda:                        h comes at end       -> nucleus + h
    """
    i = start
    n = len(s)

    # ---- onset ----
    onset = ""
    for cand in _YALE_ONSETS_ORDERED:
        if s.startswith(cand, i):
            onset = cand
            break
    nucleus_start = i + len(onset)

    # Backtrack: 'm'/'ng' may be a syllabic nasal nucleus, not an onset.
    if nucleus_start >= n or s[nucleus_start] not in _YALE_VOWEL_LETTERS:
        if onset in ("m", "ng") and _looks_like_syllabic(s, i, onset):
            onset = ""
            nucleus_start = i
        elif onset == "" and i < n and s[i] in _YALE_VOWEL_LETTERS:
            pass  # vowel-initial syllable
        else:
            if onset == "":
                raise ValueError(
                    "cannot parse Yale syllable starting at "
                    + repr(unicodedata.normalize("NFC", s[i:]))
                )

    # Backtrack onset "y" if it's really the prefix of nucleus "yu" (Jyutping
    # "jyu"). The "yu" nucleus only combines with codas in {"", "n", "t"} in
    # real Cantonese, so only backtrack when the rest fits that shape.
    if onset == "y":
        test_end, test_raw = _consume_nucleus(s, i)
        test_base = "".join(c for c in test_raw if unicodedata.category(c) != "Mn")
        if test_base == "yu" and _yu_compatible_tail(s, test_end):
            onset = ""
            nucleus_start = i

    # ---- nucleus ----
    nuc_end, nuc_raw = _consume_nucleus(s, nucleus_start)
    if nuc_end == nucleus_start:
        raise ValueError(
            "cannot find nucleus in Yale syllable -- "
            + repr(unicodedata.normalize("NFC", s[i:]))
        )

    # Syllabic nasals (onset-less "m" and "ng") never take a coda in Yale/Jyutping.
    nuc_base = "".join(c for c in nuc_raw if unicodedata.category(c) != "Mn")
    is_syllabic_nasal = onset == "" and nuc_base in ("m", "ng")

    # ---- coda + h-marker, accounting for h placement ----
    pos = nuc_end

    if is_syllabic_nasal and (pos >= n or s[pos] != "h"):
        # No 'h' follows: definitely no coda (prevents greedily consuming the
        # next syllable's onset/nucleus as a coda, e.g. ng3+ng5 -> "ngnǵh").
        return pos

    if pos < n and s[pos] == "h":
        # h before stop/nasal coda (low-tone case), or h at syllable end
        after_h = pos + 1
        for cand in ("ng", "p", "t", "k", "m", "n"):
            if s.startswith(cand, after_h):
                return after_h + len(cand)  # h + stop/nasal coda
        # No stop/nasal coda after h: h is either a low-tone marker (end of
        # syllable) or the onset of the next syllable (followed by a vowel).
        if after_h >= n or s[after_h] not in _YALE_VOWEL_LETTERS:
            return after_h  # low-tone h, no coda
        return pos  # h is the next syllable's onset
    else:
        # Try glide coda (h follows the coda for low tones)
        for cand in ("i", "u", "w"):
            if s.startswith(cand, pos):
                coda_end = pos + len(cand)
                if coda_end < n and s[coda_end] == "h":
                    after_h = coda_end + 1
                    if after_h >= n or s[after_h] not in _YALE_VOWEL_LETTERS:
                        return after_h  # glide coda + low-tone h
                return coda_end  # glide coda, no h
        # Try stop/nasal coda without h (tones 1-3)
        for cand in ("ng", "p", "t", "k", "m", "n"):
            if s.startswith(cand, pos):
                return pos + len(cand)
        return pos  # no coda


def _yu_compatible_tail(s, pos):
    """True iff s[pos:] is a possible tail after a Yale "yu" nucleus.

    The Jyutping "yu" nucleus only combines with codas in {"", "n", "t"}.
    May be preceded by 'h' (low-tone marker) for codas "n"/"t" (h before
    stop/nasal) or alone (no coda)."""
    n = len(s)
    if pos >= n:
        return True  # bare "yu" nucleus
    ch = s[pos]
    if ch == "h":
        after = pos + 1
        if after >= n:
            return True  # low-tone, no coda
        if s[after] == "t":
            return True
        if s[after] == "n":
            return after + 1 >= n or s[after + 1] != "g"
        return False
    if ch == "t":
        return True
    if ch == "n":
        return pos + 1 >= n or s[pos + 1] != "g"
    return False


def _looks_like_syllabic(s, start, onset):
    """Return True if the onset 'm' or 'ng' at s[start:] is really a syllabic
    nasal nucleus (e.g., 'm̀h' or 'ǹgh'). True when the next char after the
    onset letters is either end-of-string, a combining diacritic, an 'h', or
    an apostrophe; i.e., not another vowel/consonant that would form a real
    onset+rime."""
    end = start + len(onset)
    if end >= len(s):
        return True
    nxt = s[end]
    if unicodedata.category(nxt) == "Mn":
        return True
    if nxt == "h":
        return True
    if nxt in _YALE_VOWEL_LETTERS:
        return False  # m + vowel = onset + nucleus
    # Another consonant means this is the boundary; treat as syllabic.
    return True


def _consume_nucleus(s, start):
    """Consume nucleus characters (vowels/syllabic-nasal base letters with at
    most one combining diacritic on the first base letter) starting at
    s[start]. Returns (end_index, base_nucleus_string_with_diacritic_attached).

    The base_nucleus_string returned includes the combining diacritic
    (preserving NFD form) so the caller can extract tone via _strip_diacritic.
    """
    n = len(s)
    if start >= n:
        return start, ""

    # Try multi-letter nuclei first (only against base letters, ignoring marks).
    base_seq = []
    spans = []  # parallel: end index after each base letter (including its mark)
    j = start
    while j < n and len(base_seq) < 2:
        ch = s[j]
        if unicodedata.category(ch) == "Mn":
            # standalone mark with no preceding base — error
            if not base_seq:
                raise ValueError("orphan combining mark at start of nucleus")
            j += 1
            continue
        if ch not in _YALE_VOWEL_LETTERS and ch not in ("m", "n", "g", "y"):
            break
        base_seq.append(ch)
        k = j + 1
        while k < n and unicodedata.category(s[k]) == "Mn":
            k += 1
        spans.append(k)
        j = k

    if not base_seq:
        return start, ""

    base_str = "".join(base_seq)

    # Choose the longest matching nucleus from the longest-first list.
    for cand in _YALE_NUCLEI_ORDERED:
        L = len(cand)
        if base_str.startswith(cand):
            # Special: "ng" and "m" as nuclei are syllabic; only allowed as
            # nucleus when nothing follows that could be a vowel (caller
            # already enforces vowel-or-syllabic structure).
            end = spans[L - 1]
            return end, s[start:end]

    # No multi-letter match: only fall back to single-letter nuclei.
    if base_seq[0] in {"a", "e", "i", "o", "u", "m"}:
        end = spans[0]
        return end, s[start:end]
    # 'y', 'n', 'g' alone are not valid nuclei.
    return start, ""


def _build_jyutping(onset_yale, nucleus_yale, coda_yale, tone):
    """Convert decomposed Yale pieces to a Jyutping syllable string."""
    if onset_yale not in _ONSETS_JYUTPING:
        raise ValueError("unknown Yale onset -- " + repr(onset_yale))
    if coda_yale not in _CODAS_JYUTPING and coda_yale != "w":
        raise ValueError("unknown Yale coda -- " + repr(coda_yale))

    onset_jp = _ONSETS_JYUTPING[onset_yale]

    # Convention: bare nucleus "yu" with no Yale onset corresponds to Jyutping
    # onset "j" + nucleus "yu" (real Cantonese has no /yu/ without a preceding
    # /j/; the Yale form "yū" is shared by Jyutping "jyu1" and "yu1").
    if onset_yale == "" and nucleus_yale == "yu":
        onset_jp = "j"

    # Yale coda "w" comes from Jyutping coda "u" with nucleus "oe" -> "ew".
    if coda_yale == "w":
        coda_jp = "u"
    else:
        coda_jp = _CODAS_JYUTPING[coda_yale]

    # Nucleus resolution.
    if nucleus_yale == "eu":
        nucleus_jp = _resolve_eu(coda_yale)
    elif nucleus_yale == "a" and coda_jp == "":
        # Yale "a" with no coda corresponds to Jyutping "aa".
        # But Yale also writes Jyutping "a" + coda as "a" + coda, so only
        # promote to "aa" when there's no coda.
        nucleus_jp = "aa"
    elif nucleus_yale in _NUCLEI_JYUTPING_UNAMBIGUOUS:
        nucleus_jp = _NUCLEI_JYUTPING_UNAMBIGUOUS[nucleus_yale]
    else:
        raise ValueError("unknown Yale nucleus -- " + repr(nucleus_yale))

    return f"{onset_jp}{nucleus_jp}{coda_jp}{tone}"


def _convert_syllable(raw):
    """Convert a single NFD-form Yale syllable into a Jyutping string."""
    n = len(raw)

    # ---- onset ----
    onset = ""
    for cand in _YALE_ONSETS_ORDERED:
        if raw.startswith(cand):
            onset = cand
            break
    nucleus_start = len(onset)

    # Backtrack: 'm'/'ng' may be a syllabic nasal nucleus.
    if nucleus_start >= n or raw[nucleus_start] not in _YALE_VOWEL_LETTERS:
        if onset in ("m", "ng") and _looks_like_syllabic(raw, 0, onset):
            onset = ""
            nucleus_start = 0
        elif onset == "" and raw and raw[0] in _YALE_VOWEL_LETTERS:
            pass
        else:
            if onset == "":
                raise ValueError(
                    "cannot parse Yale syllable -- "
                    + repr(unicodedata.normalize("NFC", raw))
                )

    # Backtrack onset "y" if it's really the prefix of nucleus "yu".
    if onset == "y":
        test_end, test_raw = _consume_nucleus(raw, 0)
        test_base = "".join(c for c in test_raw if unicodedata.category(c) != "Mn")
        if test_base == "yu" and _yu_compatible_tail(raw, test_end):
            onset = ""
            nucleus_start = 0

    # ---- nucleus ----
    nuc_end, nuc_chars = _consume_nucleus(raw, nucleus_start)
    if nuc_end == nucleus_start:
        raise ValueError(
            "cannot parse Yale syllable -- " + repr(unicodedata.normalize("NFC", raw))
        )
    base_nucleus, mark = _strip_diacritic(nuc_chars)

    # ---- coda + h-marker ----
    # Yale low-tone 'h' placement: BEFORE stop/nasal coda, AFTER glide coda.
    # Syllabic nasals (no onset) never take a coda.
    is_syllabic_nasal = onset == "" and base_nucleus in ("m", "ng")
    pos = nuc_end
    has_h = False
    coda = ""

    if is_syllabic_nasal and (pos >= n or raw[pos] != "h"):
        # No 'h' follows: no coda (e.g. ng3 or m3 standalone syllables).
        tone = _tone_from(mark, has_h)
        return _build_jyutping(onset, base_nucleus, coda, tone)

    if pos < n and raw[pos] == "h":
        after_h = pos + 1
        for cand in ("ng", "p", "t", "k", "m", "n"):
            if raw.startswith(cand, after_h):
                has_h = True
                coda = cand
                break
        else:
            has_h = True
            coda = ""
    else:
        for cand in ("i", "u", "w"):
            if raw.startswith(cand, pos):
                coda = cand
                coda_end = pos + len(cand)
                if coda_end < n and raw[coda_end] == "h":
                    has_h = True
                break
        else:
            for cand in ("ng", "p", "t", "k", "m", "n"):
                if raw.startswith(cand, pos):
                    coda = cand
                    break

    tone = _tone_from(mark, has_h)
    return _build_jyutping(onset, base_nucleus, coda, tone)


def yale_to_jyutping(yale: str | list[str]) -> list[str]:
    """Convert Yale romanization into Jyutping romanization.

    The inverse of :func:`jyutping_to_yale`. Accepts Yale in the diacritic +
    ``h`` low-tone style (same form produced by ``jyutping_to_yale``).

    Args:
        yale (str or list[str]): A Yale romanization string for a single word,
            or a list of such strings carrying explicit word segmentation
            (one word per element). Inside a single-word string, both
            whitespace and apostrophes ``'`` are accepted as syllable-boundary
            hints; neither creates a word boundary. Pass a ``list[str]`` to
            mark word boundaries.

    Returns:
        list[str]: A list with one element per input word. Each element is
        the Jyutping representation of that word, with syllables separated
        by a single space.

    Raises:
        ValueError: If the Yale romanization is illegal (e.g., with
            unrecognized elements or a missing low-tone marker on a tone-4
            grave-accented syllable).

    Examples:
        >>> yale_to_jyutping("gwóngdūngwá")  # 廣東話, Cantonese
        ['gwong2 dung1 waa2']
        >>> yale_to_jyutping(["gāmyaht", "góng", "gwóngdūngwá"])
        ['gam1 jat6', 'gong2', 'gwong2 dung1 waa2']
    """
    if not yale:
        return []

    words = [yale] if isinstance(yale, str) else yale

    result = []
    for word in words:
        syllables = _split_word_syllables(word)
        jp_parts = [_convert_syllable(s) for s in syllables]
        result.append(" ".join(jp_parts))
    return result
