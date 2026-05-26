import pytest

from pycantonese import jyutping_to_yale, yale_to_jyutping
from pycantonese.jyutping.parse_jyutping import (
    ONSETS,
    NUCLEI,
    CODAS,
    TONES,
    parse_jyutping,
)
from pycantonese.jyutping.yale import (
    ONSETS_YALE,
    NUCLEI_YALE,
    CODAS_YALE,
)


def test_correct_onset_set():
    assert set(ONSETS_YALE.keys()) == ONSETS


def test_correct_nucleus_set():
    assert set(NUCLEI_YALE.keys()) == NUCLEI


def test_correct_coda_set():
    assert set(CODAS_YALE.keys()) == CODAS


@pytest.mark.parametrize("input_", ["", None, []])
def test_jyutping_to_yale__null_input(input_):
    assert jyutping_to_yale(input_) == []


def test_jyutping_to_yale_m4goi1():
    assert jyutping_to_yale("m4goi1") == ["m̀h gōi"]


def test_jyutping_to_yale_gwong2dung1waa2():
    assert jyutping_to_yale("gwong2dung1waa2") == ["gwóng dūng wá"]


def test_jyutping_to_yale_list_input():
    assert jyutping_to_yale(["gwong2dung1", "waa2"]) == ["gwóng dūng", "wá"]


def test_jyutping_to_yale_hei3hau6():
    # 氣候 climate -- spaces handle what the old apostrophe disambiguation did.
    assert jyutping_to_yale("hei3hau6") == ["hei hauh"]


@pytest.mark.parametrize("input_", ["", None, []])
def test_yale_to_jyutping__null_input(input_):
    assert yale_to_jyutping(input_) == []


@pytest.mark.parametrize(
    "yale, expected",
    [
        # str input -> single word; whitespace and apostrophes are syllable hints.
        ("gwóngdūngwá", ["gwong2 dung1 waa2"]),
        ("hei'hauh", ["hei3 hau6"]),
        ("hei hauh", ["hei3 hau6"]),
        ("sāam", ["saam1"]),
        ("yùhng", ["jung4"]),
        ("léuih", ["leoi5"]),
        # list[str] input -> one Jyutping word per element.
        (
            ["gāmyaht", "góng", "gwóngdūngwá"],
            ["gam1 jat6", "gong2", "gwong2 dung1 waa2"],
        ),
    ],
)
def test_yale_to_jyutping_basic(yale, expected):
    assert yale_to_jyutping(yale) == expected


def _is_valid_jyutping(onset, nucleus, coda, tone):
    """Exclude Jyutping combinations that jyutping_to_yale rejects, plus
    phonotactically impossible ones like syllabic-nasal + coda. The
    parse_jyutping regex over-accepts (e.g., 'ngp2', 'mk5') but no real
    Cantonese syllable pairs a syllabic 'm'/'ng' nucleus with a coda."""
    if nucleus in ("m", "ng") and coda != "":
        return False
    # Yale collapses Jyutping onset 'j' + nucleus 'yu' with bare nucleus 'yu'
    # (both -> "yū"). The inverse picks "jyu" by convention, so skip bare-yu.
    if onset == "" and nucleus == "yu":
        return False
    # Jyutping "yu" nucleus only combines with codas in {"", "n", "t"}.
    if nucleus == "yu" and coda not in ("", "n", "t"):
        return False
    # Nucleus "oe" only combines with codas in {"", "k", "ng"} in real
    # Cantonese; "eo" only with {"n", "t", "i"}. The regex over-accepts.
    if nucleus == "oe" and coda not in ("k", "ng"):
        return False
    if nucleus == "eo" and coda not in ("n", "t", "i"):
        return False
    # Yale "eu" is shared by Jyutping nuclei "oe"/"eo" and by "e"+coda "u".
    # The inverse picks "oe"/"eo" via the coda-disambiguation rule, so skip
    # Jyutping nucleus "e" with coda "u".
    if nucleus == "e" and coda == "u":
        return False
    # Jyutping "aa" with no coda is written as bare "a" in Yale (per the
    # forward special case), colliding with Jyutping nucleus "a" + no coda.
    # The inverse picks "aa".
    if nucleus == "a" and coda == "":
        return False
    # Jyutping onset "ng" doesn't combine with nuclei "yu", "ng", or "m" in
    # real Cantonese; the regex over-accepts. Yale would render these in
    # ways that genuinely collide with multi-syllable splittings.
    if onset in ("ng", "m") and nucleus in ("yu", "ng", "m"):
        return False
    # Jyutping "j" + nucleus "u" + coda in {"", "n", "t"} collides with
    # "j" + "yu" + same coda in Yale; the inverse picks "jyu" by convention.
    if onset == "j" and nucleus == "u" and coda in ("", "n", "t"):
        return False
    try:
        parse_jyutping(f"{onset}{nucleus}{coda}{tone}")
        return True
    except ValueError:
        return False


def test_round_trip():
    """For every valid Jyutping syllable, jyutping_to_yale then yale_to_jyutping
    should give back the original syllable."""
    failures = []
    for onset in ONSETS:
        for nucleus in NUCLEI:
            for coda in CODAS:
                for tone in TONES:
                    jp = f"{onset}{nucleus}{coda}{tone}"
                    if not _is_valid_jyutping(onset, nucleus, coda, tone):
                        continue
                    [yale] = jyutping_to_yale(jp)
                    result = yale_to_jyutping(yale)
                    if result != [jp]:
                        failures.append((jp, yale, result))
    if failures:
        lines = "\n".join(
            f"  jp={j!r} -> yale={y!r} -> got {r!r}" for j, y, r in failures[:20]
        )
        pytest.fail(f"{len(failures)} round-trip failures:\n{lines}")
