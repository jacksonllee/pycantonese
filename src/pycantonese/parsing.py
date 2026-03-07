import concurrent.futures as cf
import functools
import multiprocessing as mp
import re
import sys
from string import ascii_uppercase

from pycantonese.corpus import CHAT
from pycantonese.jyutping.characters import characters_to_jyutping
from pycantonese.pos_tagging.tagger import pos_tag

# Punctuation marks for utterance segmentation.
_UTTERANCE_PUNCT_MARKS = frozenset(("。", "！", "？"))
_ASCII_UPPERCASE = frozenset(ascii_uppercase)

_UNKNOWN_PARTICIPANT = "X"

_IS_WASM = sys.platform == "emscripten"
_CPU_COUNT = mp.cpu_count()
_CHUNK_SIZE = 4


def _parse_text(text: str, pos_tag_kwargs):
    chars_jps = characters_to_jyutping(text)
    segmented, jyutping = [], []
    for chars, jps in chars_jps:
        segmented.append(chars)
        jyutping.append(jps)
    tags = [pos for _, pos in pos_tag(segmented, **(pos_tag_kwargs or {}))]
    return segmented, tags, jyutping


def _get_utterance(unparsed_sent, pos_tag_kwargs, participant):
    """Parse text into (participant, words_str, mor_str) tuple."""
    if participant is None:
        participant = _UNKNOWN_PARTICIPANT

    if not unparsed_sent:
        return (str(participant), "", "")

    if isinstance(unparsed_sent, tuple):
        participant, unparsed_sent, *_ = unparsed_sent

    participant = str(participant)

    words, tags, jps = _parse_text(unparsed_sent, pos_tag_kwargs)

    words_str = " ".join(words)
    mor_items = []
    for word, pos, jp in zip(words, tags, jps):
        if pos == "PUNCT" or pos[0].upper() not in _ASCII_UPPERCASE:
            mor_items.append(word)
        else:
            mor_items.append(f"{pos}|{jp or ''}")
    mor_str = " ".join(mor_items)

    return (participant, words_str, mor_str)


def parse_text(
    data,
    *,
    pos_tag_kwargs=None,
    participant: str | None = None,
    parallel: bool = True,
) -> CHAT:
    """Parse raw Cantonese text.

    Parameters
    ----------
    data : str or Iterable[str] or Iterable[tuple[str, str]]
        Raw Cantonese text data, in one of the following formats:

        - A single string, e.g.,
          ``"廣東話好難學？都唔係吖！"`` (which would be two utterances).
          Basic utterance segmentation
          (i.e., splitting by the end-of-line character ``\\n``
          or one of the Chinese full-width punctuation marks from {"。", "！", "？"})
          will be applied to this string, and
          each segmented utterance will be an utterance in the resulting CHAT reader.
        - An iterable of strings, e.g.,
          ``["廣東話好難學？", "都唔係吖！"]``.
          No utterance segmentation will be done. Use this
          option to pass in data that's utterance-segmented to your liking.
        - An iterable of tuples, where each tuple has two strings, one for the
          participant and the other for the utterance, e.g.,
          ``[("小芬", "你食咗飯未呀？"), ("小明", "我食咗喇。")]``.

        if an empty input or ``None`` is provided,
        then an empty :class:`~pycantonese.CHAT` instance is returned.

    pos_tag_kwargs : dict, optional
        To customize part-of-speech tagging,
        provide a dictionary here which would then be passed as keyword arguments to
        :func:`~pycantonese.pos_tag`.
    participant : str, optional
        If provided, this will be the participant in the output CHAT-formatted data
        (and will override all the particpants if your input to ``data`` is an iterable
        of tuples).
        If not provided, a default dummy participant ``"X"`` is used when your ``data``
        is either a single string or an iterable of strings.
    parallel : bool, optional
        If ``True`` (the default), this function attempts to parallelize parsing
        for speed-up.
        (In case the data volume is very small, the parsing is not parallelized
        even if you pass in ``True``.)
        Under certain circumstances (e.g., your application is already parallelized and
        further parallelization from within this function might be undesirable),
        you may like to consider setting this parameter to ``False``.

    Returns
    -------
    :class:`~pycantonese.CHAT`
    """

    if not data:
        return CHAT()

    if isinstance(data, str):
        # Perform basic sentence segmentation.
        for punct in _UTTERANCE_PUNCT_MARKS:
            data = data.replace(punct, f"{punct}\n")
        data = data.replace("\r\n", "\n")
        data = re.sub(r"\n{2,}", "\n", data)
        data = data.strip().split("\n")

    # Disable parallelization in Pyodide (no subprocess/thread support).
    if _IS_WASM:
        parallel = False

    # If there's not much data, don't bother with parallelization.
    if parallel and len(data) < (_CPU_COUNT * _CHUNK_SIZE):
        parallel = False

    if parallel:
        func = functools.partial(
            _get_utterance,
            pos_tag_kwargs=pos_tag_kwargs,
            participant=participant,
        )
        with cf.ProcessPoolExecutor() as executor:
            utterances = list(executor.map(func, data, chunksize=_CHUNK_SIZE))
    else:
        utterances = [
            _get_utterance(sent, pos_tag_kwargs, participant) for sent in data
        ]

    # Build CHAT-format string
    all_participants = sorted(set(p for p, _, _ in utterances))
    lines = ["@Begin"]
    parts = ", ".join(f"{p} Other" for p in all_participants)
    lines.append(f"@Participants:\t{parts}")
    for p, words_str, mor_str in utterances:
        lines.append(f"*{p}:\t{words_str}")
        if mor_str:
            lines.append(f"%mor:\t{mor_str}")
    lines.append("@End")

    return CHAT.from_strs(["\n".join(lines)], strict=False)
