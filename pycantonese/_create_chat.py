import collections
import uuid
from string import ascii_uppercase

from pylangacq.chat import _File, Utterance

from pycantonese.corpus import CHATReader, Token
from pycantonese.jyutping.characters import characters_to_jyutping
from pycantonese.pos_tagging.tagger import pos_tag


# Punctuation marks for sentence segmentation.
_SENT_PUNCT_MARKS = frozenset(("。", "！", "？"))
_ASCII_UPPERCASE = frozenset(ascii_uppercase)

_UNKNOWN_PARTICIPANT = "XXX"


def _analyze_text(text, segmenter, tagset):
    chars_jps = characters_to_jyutping(text, segmenter)
    segmented, jyutping = [], []
    for chars, jps in chars_jps:
        segmented.append(chars)
        jyutping.append(jps)
    tags = [pos for _, pos in pos_tag(segmented, tagset)]
    return segmented, tags, jyutping


def _create_chat(data, segmenter=None, tagset="universal") -> CHATReader:
    """Create a CHAT reader by analyzing raw Cantonese text.

    Parameters
    ----------
    data : str or Iterable[str] or Iterable[Tuple[str, str]]
        Raw Cantonese text data, in one of the following formats:

        - A single string, e.g.,
          ``"廣東話好難學？都唔係吖！"`` (which would be two utterances).
          Simple utterance segmentation (i.e., splitting by
          {"。", "！", "？"}) will be applied to this string, and
          each segmented utterance will be an utterance in the resulting CHAT reader.
        - An iterable of strings, e.g.,
          ``["廣東話好難學？", "都唔係吖！"]``.
          No utterance segmentation will be done. Use this
          option to pass in data that's utterance-segmented to your liking.
        - An iterable of tuples, where each tuple has two strings, one for the
          participant and the other for the utterance, e.g.,
          ``[("小芬", "你食咗飯未呀？"), ("小明", "我食咗喇。")]``.

    segmenter : pycantonese.word_segmentation.Segmenter, optional
        If not provided or if ``None`` is given, the default word segmentation behavior
        is applied.
        For custom behavior, pass in a custom
        :class:`~pycantonese.word_segmentation.Segmenter` object.
    tagset : str, {"universal", "hkcancor"}, optional
        The part-of-speech tagset that the returned tags are in.
        This is the same argument for :func:`~pycantonese.pos_tag`.

    Returns
    -------
    :class:`~pycantonese.CHATReader`
    """

    if isinstance(data, str):
        # Perform simple sentence segmentation.
        for punct in _SENT_PUNCT_MARKS:
            data = data.replace(punct, f"{punct}\n")
        data = data.split("\n")

    utterances = []

    for i, raw_sent in enumerate(data, 1):
        if isinstance(raw_sent, str):
            participant = _UNKNOWN_PARTICIPANT
        elif isinstance(raw_sent, tuple):
            participant, raw_sent, *_ = raw_sent
            participant = participant or _UNKNOWN_PARTICIPANT
        else:
            raise ValueError(
                f"Error at the {i}-th utterance. It must be either a string or a "
                f"tuple of (participant, utterance): {raw_sent}"
            )
        if not raw_sent:
            continue
        words, tags, jps = _analyze_text(raw_sent, segmenter, tagset)
        tokens = [
            Token(word, pos, jp, None, None) for word, pos, jp in zip(words, tags, jps)
        ]
        u = Utterance(
            participant=participant,
            tokens=tokens,
            time_marks=None,
            tiers={
                # TODO: Convert punct to CHAT-styled punct? Could be an optional arg.
                f"*{participant}": " ".join(words),
                "%mor": " ".join(
                    word
                    if pos == "PUNCT" or pos[0].upper() not in _ASCII_UPPERCASE
                    else f"{pos}|{jp or ''}"
                    for word, pos, jp in zip(words, tags, jps)
                ),
            },
        )
        utterances.append(u)
    f = _File(
        file_path=str(uuid.uuid4()),
        header={},
        utterances=utterances,
    )
    reader = CHATReader()
    reader._files = collections.deque([f])
    return reader
