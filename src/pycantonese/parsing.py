import collections
import concurrent.futures as cf
import functools
import multiprocessing as mp
import re
import uuid
from string import ascii_uppercase

from pylangacq.chat import _File, Utterance

from pycantonese.corpus import CHATReader, Token
from pycantonese.jyutping.characters import characters_to_jyutping
from pycantonese.pos_tagging.tagger import pos_tag


# Punctuation marks for utterance segmentation.
_UTTERANCE_PUNCT_MARKS = frozenset(("。", "！", "？"))
_ASCII_UPPERCASE = frozenset(ascii_uppercase)

_UNKNOWN_PARTICIPANT = "X"

_CPU_COUNT = mp.cpu_count()
_CHUNK_SIZE = 4


def _parse_text(text: str, segment_kwargs, pos_tag_kwargs):
    chars_jps = characters_to_jyutping(text, **(segment_kwargs or {}))
    segmented, jyutping = [], []
    for chars, jps in chars_jps:
        segmented.append(chars)
        jyutping.append(jps)
    tags = [pos for _, pos in pos_tag(segmented, **(pos_tag_kwargs or {}))]
    return segmented, tags, jyutping


def _get_utterance(
    unparsed_sent, segment_kwargs, pos_tag_kwargs, participant
) -> Utterance:
    if participant is not None:
        pass
    elif isinstance(unparsed_sent, str):
        participant = _UNKNOWN_PARTICIPANT
    elif isinstance(unparsed_sent, tuple):
        participant, unparsed_sent, *_ = unparsed_sent
    else:
        raise TypeError(
            "Utterance must be either a string or "
            f"a tuple of (participant, utterance): {unparsed_sent}"
        )
    participant = str(participant)

    if not unparsed_sent:
        return Utterance(
            participant=participant, tokens=[], time_marks=None, tiers={participant: ""}
        )
    words, tags, jps = _parse_text(unparsed_sent, segment_kwargs, pos_tag_kwargs)

    tokens = [
        Token(word, pos, jp, None, None, None)
        for word, pos, jp in zip(words, tags, jps)
    ]

    return Utterance(
        participant=participant,
        tokens=tokens,
        time_marks=None,
        tiers={
            # TODO or question: Convert full-width punct to CHAT-styled punct?
            participant: " ".join(words),
            "%mor": " ".join(
                word
                if pos == "PUNCT" or pos[0].upper() not in _ASCII_UPPERCASE
                else f"{pos}|{jp or ''}"
                for word, pos, jp in zip(words, tags, jps)
            ),
        },
    )


def parse_text(
    data,
    *,
    segment_kwargs=None,
    pos_tag_kwargs=None,
    participant: str = None,
    parallel: bool = True,
) -> CHATReader:
    """Parse raw Cantonese text.

    Parameters
    ----------
    data : str or Iterable[str] or Iterable[Tuple[str, str]]
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

        if an empty input or ``None`` is provided, then ``None`` is returned.

    segment_kwargs : dict, optional
        To customize word segmentation,
        provide a dictionary here which would then be passed as keyword arguments to
        :func:`~pycantonese.segment`.
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
    :class:`~pycantonese.CHATReader`
    """

    if not data:
        return None

    if isinstance(data, str):
        # Perform basic sentence segmentation.
        for punct in _UTTERANCE_PUNCT_MARKS:
            data = data.replace(punct, f"{punct}\n")
        data = data.replace("\r\n", "\n")
        data = re.sub(r"\n{2,}", "\n", data)
        data = data.strip().split("\n")

    # Internally, word segmentation is actually going to be done by
    # `characters_to_jyutping` instead of `segment`.
    # `characters_to_jyutping`'s segmenter kwarg is called `segmenter`,
    # while that of `segment` is called `cls`.
    segment_kwargs = segment_kwargs or {}
    if "cls" in segment_kwargs:
        segment_kwargs["segmenter"] = segment_kwargs["cls"]
        del segment_kwargs["cls"]

    # If there's not much data, don't bother with parallelization.
    if parallel and len(data) < (_CPU_COUNT * _CHUNK_SIZE):
        parallel = False

    if parallel:
        func = functools.partial(
            _get_utterance,
            segment_kwargs=segment_kwargs,
            pos_tag_kwargs=pos_tag_kwargs,
            participant=participant,
        )
        with cf.ProcessPoolExecutor() as executor:
            utterances = list(executor.map(func, data, chunksize=_CHUNK_SIZE))
    else:
        utterances = [
            _get_utterance(sent, segment_kwargs, pos_tag_kwargs, participant)
            for sent in data
        ]

    f = _File(
        file_path=str(uuid.uuid4()),
        header={},
        utterances=utterances,
    )
    reader = CHATReader()
    reader._files = collections.deque([f])
    return reader
