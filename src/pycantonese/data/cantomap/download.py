#!/usr/bin/env python3
"""Download CantoMap .eaf files and extract word/Jyutping data as CHAT (.cha)."""

from __future__ import annotations

import collections
import logging
import os
import re
import shutil
import subprocess
import tempfile

from rustling.elan import ELAN, Tier

from pycantonese.corpus import CHAT
from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.pos_tagging.tagger import pos_tag

CANTOMAP_REPO = "https://github.com/gwinterstein/CantoMap.git"
CANTOMAP_COMMIT = "9f03a43827c7a75e095b0bfd6ef539c11115f2cf"

logger = logging.getLogger(__name__)


def _check_git() -> None:
    if not shutil.which("git"):
        raise RuntimeError("The 'git' command line tool is required but not found.")


def _clone_cantomap(dest: str) -> None:
    """Clone CantoMap repo and checkout pinned commit."""
    # CantoMap's .wav audio files are tracked via Git LFS and are large.
    # Setting GIT_LFS_SKIP_SMUDGE tells Git to skip downloading LFS
    # objects, since we only need the .eaf annotation text files.
    env = {**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"}
    subprocess.run(
        ["git", "clone", "--no-checkout", CANTOMAP_REPO, dest],
        check=True,
        env=env,
    )
    subprocess.run(
        ["git", "checkout", CANTOMAP_COMMIT],
        cwd=dest,
        check=True,
        env=env,
    )


def _is_jyutping(s: str) -> bool:
    """Check if a string is valid Jyutping romanization."""
    try:
        parse_jyutping(s)
        return True
    except ValueError:
        return False


_TONE_CHANGE_RE = re.compile(r"\d\*(\d)")
_SKIP_TOKEN = object()

# Mapping from Jyutping (with tone) to the conventional Chinese character
# for common Cantonese sentence-final particles, fillers, etc.  Used when
# the source word tier has an &-prefixed romanization instead of a character.
# A few cases in the source data omit tones.
# Some of the key-value pairs are wrong at first blush -- these are the best guesses
# based on context, so they might well be slips of tongue,
# or they may be further corrected later.
_PARTICLE_CHAR: dict[str, str] = {
    "aa1": "吖",
    "aa2": "啞",
    "aa3": "啊",
    "aa4": "呀",
    "aa5": "咓",
    "aa6": "𠻺",
    "aai1": "哎",
    "aai2": "唉",
    "aai3": "唉",
    "aak1": "呃",
    "aak3": "呃",
    "aam3": "啱",
    "aam6": "啱",
    "aat6": "呃",
    "ai1": "哎",
    "ai2": "哎",
    "ai3": "哎",
    "ai6": "哎",
    "ak3": "呃",
    "am3": "啱",
    "am4": "啱",
    "am6": "啱",
    "ang3": "呃",
    "bat1": "𡃓",
    "bo3": "𡃓",
    "caa2": "咋",
    "caa5": "扠",
    "co3": "咗",
    "cyt3": "啜",
    "dong1": "端",
    "doeng1": "啄",
    "dou2": "到",
    "duk1": "篤",
    "e1": "誒",
    "e2": "誒",
    "e3": "誒",
    "e4": "誒",
    "e6": "誒",
    "ei1": "誒",
    "ei2": "誒",
    "ei3": "誒",
    "ek3": "誒",
    "ek4": "誒",
    "ek6": "誒",
    "em": "唔",
    "em3": "唔",
    "em4": "唔",
    "em6": "唔",
    "ep3": "誒",
    "f3": "噴",
    "gaa1": "𠺢",
    "gaa3": "𡃉",
    "gaa4": "㗎",
    "gaa6": "㗎",
    "gaak3": "𠺝",
    "ge1": "嘅",
    "ge2": "𠸏",
    "ge3": "嘅",
    "ge4": "嘅",
    "ge5": "𠸏",
    "ge6": "嘅",
    "go3": "嗰",
    "gwaa3": "啩",
    "haa2": "吓",
    "haa3": "吓",
    "haa4": "吓",
    "haa5": "吓",
    "haa6": "吓",
    "haak1": "嚇",
    "haak3": "嚇",
    "haak4": "嚇",
    "haak6": "嚇",
    "hi2": "咦",
    "hm2": "嗯",
    "hm6": "嗯",
    "hn1": "嗯",
    "ho2": "呵",
    "ho3": "呵",
    "ik1": "唧",
    "ik3": "唧",
    "it3": "唧",
    "jaa1": "吖",
    "jaa2": "啊",
    "jaa3": "啊",
    "jaa4": "呀",
    "jaak3": "啊",
    "jat6": "啊",
    "je5": "嘢",
    "ji1": "咦",
    "ji2": "咦",
    "ji5": "咦",
    "jo1": "咗",
    "k": "噃",
    "ke4": "嘅",
    "kwaang2": "莖",
    "laa": "嚹",
    "laa1": "喇",
    "laa3": "嚹",
    "laa4": "嗱",
    "laa5": "哪",
    "laa6": "嚹",
    "laak": "嘞",
    "laak1": "嘞",
    "laak3": "嘞",
    "laak4": "嘞",
    "laak5": "嘞",
    "laak6": "嘞",
    "laam1": "啦",
    "laat2": "嘞",
    "laat3": "嘞",
    "laat6": "嘞",
    "lai4": "嚟",
    "lak3": "嘞",
    "lak6": "嘞",
    "lat1": "啦",
    "lau1": "右",
    "le": "呢",
    "le1": "呢",
    "le2": "𠻗",
    "le3": "呢",
    "le4": "𠻗",
    "lei4": "嚟",
    "lek6": "呢",
    "lin3": "連",
    "ling6": "擰",
    "liu2": "繞",
    "lo": "嘍",
    "lo1": "囖",
    "lo3": "嘍",
    "m": "唔",
    "m1": "唔",
    "m2": "唔",
    "m3": "唔",
    "m4": "唔",
    "m5": "唔",
    "m6": "唔",
    "ma3": "嗎",
    "maa1": "嗎",
    "maa2": "嘛",
    "maa3": "嗎",
    "maa5": "嘛",
    "maa6": "嗎",
    "maai6": "咪",
    "maang1": "掹",
    "mai4": "咪",
    "me1": "咩",
    "me2": "歪",
    "mun5": "門",
    "naa4": "嗱",
    "ng6": "嗯",
    "o1": "哦",
    "o2": "哦",
    "o3": "哦",
    "o4": "哦",
    "o5": "哦",
    "o6": "哦",
    "oi2": "喺",
    "ok2": "哦",
    "ok3": "哦",
    "ok6": "哦",
    "om3": "唔",
    "ou2": "噢",
    "ou5": "噢",
    "ou6": "噢",
    "pat1": "噗",
    "pei3": "畀",
    "sai3": "晒",
    "si4": "時",
    "sip3": "𤗈",
    "soe4": "瀡",
    "syut2": "𠽌",
    "taat3": "笪",
    "ten3": "停",
    "tim1": "𠻹",
    "tun3": "噋",
    "waa1": "話",
    "waa2": "話",
    "waa3": "嘩",
    "waa4": "嘩",
    "waa5": "畫",
    "waa6": "話",
    "waak3": "嘩",
    "wai3": "喂",
    "wai6": "喂",
    "we6": "枉",
    "wo": "喎",
    "wo1": "喎",
    "wo2": "喎",
    "wo3": "喎",
    "wo4": "啝",
    "wo6": "喎",
    "wr3": "枉",
    "wu3": "嗚",
    "zaa1": "咋",
    "zaa3": "咋",
    "zaa4": "喳",
    "zaa6": "咋",
    "zak1": "即",
    "ze1": "啫",
    "zek1": "唧",
    "zep1": "啫",
    # # Compound particles
    # "aa1maa3": "吖嘛",
}


# Overrides for individual word-tier tokens.
# Key: raw word-tier token.
# Value: (new_word, new_jp) to replace both, or None to skip the token.
# If new_jp is None, the jp from the jyutping tier is used (after standard cleanup).
# Need original audio data to verify some/all of the mapping.
_WORD_OVERRIDES: dict[str, tuple[str, str | None] | None] = {
    # Word + jp overrides
    "&cyt3": ("樹", "cyut3"),
    # "&co3": ("左", "co3"),
    "&gr1": ("𠺢", "ga1"),
    "&gr2": ("𠿪", "ga2"),
    "&gr3": ("𡃉", "ga3"),
    "&gr6": ("㗎", "ga6"),
    "&hr1": ("吓", "ha1"),
    "&hr2": ("吓", "ha2"),
    "&hr3": ("吓", "ha3"),
    "&hr4": ("吓", "ha4"),
    "&hr6": ("吓", "ha6"),
    "&jr1": ("吖", "ja1"),
    "&laa": ("嚹", "laa3"),
    "&laak": ("嘞", "laak3"),
    "&le": ("呢", "le1"),
    "&lo": ("嘍", "lo1"),
    "&lr": ("嘞", "la3"),
    "&lr1": ("喇", "la1"),
    "&lr3": ("嚹", "la3"),
    "&lr4": ("嗱", "la4"),
    "&lr5": ("嘞", "la5"),
    "&lr6": ("嚹", "la6"),
    "&lrk": ("嘞", "lak3"),
    "&lrk3": ("嘞", "lak3"),
    "&m": ("唔", "m4"),
    "&r": ("啊", "a3"),
    "&r1": ("吖", "a1"),
    "&r2": ("啞", "a2"),
    "&r3": ("啊", "a3"),
    "&r4": ("呀", "a4"),
    "&r6": ("𠻺", "a6"),
    "&wo": ("喎", "wo3"),
    "&wr3": ("枉", "wong2"),
    "&zr1": ("咋", "za3"),
    "&zr3": ("咋", "za3"),
    "*aa4": ("呀", "aa4"),
    # Mid-word & overrides
    "左&jaau1": ("左㕭", None),
    "右&jaau1": ("右㕭", None),
    "圓&dum4&dum4": ("圓揼揼", None),
    "尖&doeng1": ("尖啄", None),
    # Deletions
    "&f3": None,
    "&k": None,
    "唙": None,
    # Typos from source data
    "&Ie6": ("呢", "le6"),
    # Mandarin?
    "hao4": ("好", "hou2"),
    "de3": ("嘅", "ge3"),
    "(Mandarin)": None,
}

# Merge rules for consecutive word-tier tokens.
# Key: tuple of raw word-tier tokens. Value: (word, jp).
# Merged tokens bypass _normalize_token entirely.
_SEQUENCE_MERGES: dict[tuple[str, ...], tuple[str, str]] = {
    # 3-token merges
    ("尖", "&bat1", "&lat1"): ("尖筆甩", "zim1bat1lat1"),
    # 2-token merges
    ("尖", "&doeng1"): ("尖啄", "zim1doeng1"),
    ("&ke4", "&le4"): ("騎呢", "ke4le4"),
    ("&lai1", "尾"): ("孻尾", "lai1mei1"),
    ("&pat1", "&pat1"): ("噼噼", "pat1pat1"),
}

_MAX_MERGE_LEN = max(len(k) for k in _SEQUENCE_MERGES)


def _particle_word(jp: str) -> str:
    """Get the Chinese character for a particle given its Jyutping.

    Falls back to the Jyutping itself if no mapping is found.
    """
    return _PARTICLE_CHAR.get(jp, jp)


def _normalize_token(word: str, jp: str) -> tuple[str, str] | object:
    """Normalize a word/Jyutping pair.

    Returns a (word, jyutping) tuple,
    or _SKIP_TOKEN for tokens that should be dropped (``xxx``, ``?``).
    """
    if word == "#" or jp == "#":
        return ("#", "#")

    # Drop unintelligible / uncertain tokens.
    if word in ("xxx", "XXX", "?") or jp in ("xxx", "XXX", "?"):
        return _SKIP_TOKEN

    # Check word-level overrides before standard normalization.
    if word in _WORD_OVERRIDES:
        override = _WORD_OVERRIDES[word]
        if override is None:
            return _SKIP_TOKEN
        new_word, new_jp = override
        if new_jp is not None:
            return (new_word, new_jp)
        # new_jp is None → clean up the jp from the tier.
        if "|" in jp:
            jp = jp.split("|")[0]
        if jp.startswith("&"):
            jp = jp[1:]
        jp = _TONE_CHANGE_RE.sub(r"\1", jp)
        return (new_word, jp)

    # hao4_(Mandarin) → 好 hou2
    if jp == "hao4_(Mandarin)":
        return ("好", "hou2")

    # Pipe-separated alternatives: take the first
    if "|" in jp:
        jp = jp.split("|")[0]

    # &-prefixed particles: strip the & from jyutping, and if the word
    # is also &-prefixed (romanization instead of a character), replace
    # it with the conventional Chinese character.
    if jp.startswith("&"):
        jp = jp[1:]
    if word.startswith("&"):
        jp_for_lookup = word[1:]
        word = _particle_word(jp_for_lookup)
    elif "&" in word:
        # Mid-word &: characters followed by romanization, e.g. 尖&doeng1 → 尖啄
        prefix, rom = word.split("&", 1)
        word = prefix + _particle_word(rom)

    # A bare "&" with nothing after it — skip.
    if not jp or not word:
        return _SKIP_TOKEN

    # *N tone-change notation: e.g. gin3dou3*2 → gin3dou2
    jp = _TONE_CHANGE_RE.sub(r"\1", jp)

    return (word, jp)


def _find_tier_pairs(tiers: dict) -> list[tuple[str, Tier, Tier]]:
    """Find matching *-word / *-Jyutping tier pairs by prefix.

    Returns a list of ``(prefix, word_tier, jyutping_tier)`` tuples.
    """
    word_tiers: dict = {}
    jyutping_tiers: dict = {}
    for tier_id, tier in tiers.items():
        if tier_id.endswith("-word"):
            prefix = tier_id[: -len("-word")]
            word_tiers[prefix] = tier
        elif tier_id.endswith("-jyutping"):
            prefix = tier_id[: -len("-jyutping")]
            jyutping_tiers[prefix] = tier

    pairs: list[tuple[str, Tier, Tier]] = []
    for prefix in sorted(word_tiers.keys()):
        if prefix in jyutping_tiers:
            pairs.append((prefix, word_tiers[prefix], jyutping_tiers[prefix]))
        else:
            logger.warning("No Jyutping tier for prefix %r", prefix)

    for prefix in sorted(jyutping_tiers.keys()):
        if prefix not in word_tiers:
            logger.warning("No word tier for prefix %r", prefix)

    return pairs


def _speaker_code(prefix: str) -> str:
    """Convert a tier prefix to a 3-character CHAT participant code.

    Pads with leading ``X`` characters, e.g. ``E`` -> ``XXE``,
    ``E1`` -> ``XE1``, ``S11`` -> ``S11``.
    """
    return prefix.rjust(3, "X")


def _extract_file(
    elan_file: ELAN, quirk_counts: collections.Counter
) -> list[tuple[str, list[dict[str, str]], tuple[int, int] | None]]:
    """Extract word/Jyutping pairs from a single-file ELAN object.

    Returns a time-sorted list of ``(speaker_prefix, tokens, time_marks)``
    tuples, where *time_marks* is ``(start_ms, end_ms)`` or ``None``.
    """
    tiers = elan_file.tiers()[0]
    pairs = _find_tier_pairs(tiers)
    # (start_time, speaker, tokens, time_marks) for chronological sorting
    raw: list[tuple[int | None, str, list[dict[str, str]], tuple[int, int] | None]] = []

    for prefix, word_tier, jp_tier in pairs:
        word_anns = word_tier.annotations
        jp_anns = jp_tier.annotations

        # Annotations in sibling tiers may be stored in different orders,
        # so align them by matching (start_time, end_time) timestamps.
        jp_by_time = {(a.start_time, a.end_time): a for a in jp_anns}

        for word_ann in word_anns:
            key = (word_ann.start_time, word_ann.end_time)
            jp_ann = jp_by_time.get(key)
            if jp_ann is None:
                logger.warning(
                    "No jyutping annotation for %s time %s-%s",
                    word_tier.id,
                    word_ann.start_time,
                    word_ann.end_time,
                )
                continue

            words = word_ann.value.split()
            jyutpings = jp_ann.value.split()

            if len(words) != len(jyutpings):
                logger.warning(
                    "Token count mismatch in %s at %s-%s: "
                    "%d words vs %d jyutping tokens",
                    word_tier.id,
                    word_ann.start_time,
                    word_ann.end_time,
                    len(words),
                    len(jyutpings),
                )

            length = min(len(words), len(jyutpings))
            tokens: list[dict[str, str]] = []
            start_time = word_ann.start_time
            end_time = word_ann.end_time
            time_marks: tuple[int, int] | None = None
            if start_time is not None and end_time is not None:
                time_marks = (start_time, end_time)
            i = 0
            while i < length:
                # Try sequence merges (longest match first).
                merged = False
                for merge_len in range(_MAX_MERGE_LEN, 1, -1):
                    if i + merge_len > length:
                        continue
                    word_seq = tuple(words[i : i + merge_len])
                    if word_seq in _SEQUENCE_MERGES:
                        new_word, new_jp = _SEQUENCE_MERGES[word_seq]
                        if not _is_jyutping(new_jp):
                            quirk_counts[new_jp] += 1
                        tokens.append({"word": new_word, "jyutping": new_jp})
                        i += merge_len
                        merged = True
                        break
                if merged:
                    continue

                w, jp = words[i], jyutpings[i]
                normalized = _normalize_token(w, jp)
                if normalized is _SKIP_TOKEN:
                    i += 1
                    continue
                assert isinstance(normalized, tuple)
                w, jp = normalized
                if not _is_jyutping(jp):
                    quirk_counts[jp] += 1
                tokens.append({"word": w, "jyutping": jp})
                i += 1

            if tokens:
                raw.append((word_ann.start_time, prefix, tokens, time_marks))

    raw.sort(key=lambda x: (x[0],))
    return [(speaker, tokens, tm) for _, speaker, tokens, tm in raw]


def _build_cha_str(
    utterances: list[tuple[str, list[dict[str, str]], tuple[int, int] | None]],
) -> str:
    """Build a CHAT-formatted string from utterances."""
    # Collect speakers in order of first appearance.
    seen: dict[str, None] = {}
    for prefix, _, _ in utterances:
        seen.setdefault(prefix, None)
    prefixes = list(seen)

    lines: list[str] = []
    lines.append("@UTF8")
    lines.append("@Begin")
    lines.append("@Languages:\tyue")

    codes = [_speaker_code(p) for p in prefixes]
    participants = " , ".join(
        f"{code} {prefix} Adult" for code, prefix in zip(codes, prefixes)
    )
    lines.append(f"@Participants:\t{participants}")

    for code in codes:
        lines.append(f"@ID:\tyue|CantoMap|{code}||||||Adult|||")

    for prefix, tokens, time_marks in utterances:
        code = _speaker_code(prefix)
        words_line = " ".join(t["word"] for t in tokens) + " ."
        if time_marks is not None:
            start, end = time_marks
            words_line += f" \x15{start}_{end}\x15"
        words = [t["word"] for t in tokens]
        tagged = pos_tag(words, tagset="hkcancor")
        mor_parts = []
        for i, (_, tag) in enumerate(tagged):
            jp = tokens[i]["jyutping"]
            if jp == "#":
                mor_parts.append("#")
            else:
                mor_parts.append(tag + "|" + jp)
        mor_line = " ".join(mor_parts) + " ."
        lines.append(f"*{code}:\t{words_line}")
        lines.append(f"%mor:\t{mor_line}")

    lines.append("@End")
    return "\n".join(lines) + "\n"


def _cantomap_elan_to_pycantonese_chat(
    elan: ELAN,
    base_dir: str | None = None,
) -> tuple[CHAT, collections.Counter]:
    """Convert CantoMap ELAN data to a pycantonese CHAT object.

    This function performs CantoMap-specific normalization of ELAN annotation
    data (particle mapping, tone change cleanup, utterance splitting, etc.)
    and produces a :class:`~pycantonese.CHAT` object.

    This is an example of how one might convert non-CHAT data into
    ``pycantonese.CHAT`` using ``rustling.elan.ELAN`` as the source.

    Args:
        elan: A ``rustling.elan.ELAN`` object containing CantoMap ``.eaf`` data.
        base_dir: If given, file identifiers are derived from paths relative
            to this directory (with separators replaced by ``__``).  Otherwise
            the basename of each ``.eaf`` file is used.

    Returns:
        A tuple of ``(chat, quirk_counts)`` where *chat* is a
        :class:`~pycantonese.CHAT` object and *quirk_counts* is a
        :class:`~collections.Counter` of non-Jyutping tokens encountered.
    """
    quirk_counts: collections.Counter = collections.Counter()
    strs: list[str] = []
    ids: list[str] = []

    for elan_file in elan:
        file_path = elan_file.file_paths[0]
        if base_dir is not None:
            rel = os.path.relpath(file_path, base_dir)
            stem = os.path.splitext(rel)[0].replace(os.sep, "__")
        else:
            stem = os.path.splitext(os.path.basename(file_path))[0]

        utterances = _extract_file(elan_file, quirk_counts)
        if not utterances:
            logger.info("Skipping %s (no utterances)", stem)
            continue
        strs.append(_build_cha_str(utterances))
        ids.append(f"{stem}.cha")

    chat = CHAT.from_strs(strs, ids=ids)
    return chat, quirk_counts


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    _check_git()

    this_dir = os.path.dirname(os.path.abspath(__file__))
    extracted_dir = os.path.join(this_dir, "extracted")
    if os.path.isdir(extracted_dir):
        shutil.rmtree(extracted_dir)

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = os.path.join(tmpdir, "CantoMap")
        print("Cloning CantoMap repo (skipping LFS audio files)...")
        _clone_cantomap(clone_dir)

        conv_dir = os.path.join(clone_dir, "ConversationData")
        print(f"Loading .eaf files from {conv_dir}...")
        elan = ELAN.from_dir(conv_dir)
        print(f"Loaded {elan.n_files} files")

        chat, quirk_counts = _cantomap_elan_to_pycantonese_chat(elan, base_dir=conv_dir)

    print(f"\nTotal: {chat.n_files} files")
    chat.to_files(extracted_dir)
    print(f"Extracted data written to {extracted_dir}")

    if quirk_counts:
        print(f"\nNon-Jyutping tokens found ({len(quirk_counts)} unique):")
        for token, count in quirk_counts.most_common():
            print(f"  {token!r}: {count}")


if __name__ == "__main__":
    main()
