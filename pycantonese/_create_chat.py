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
    data : str or Iterable[str]
        Raw Cantonese text data.
        If it's a string, simple sentence segmentation is applied
        (by {"。", "！", "？"}),
        and that each segmented sentence is treated as an utterance in the resulting
        CHAT reader.
        If it's not a string, it's assumed to be an iterable of strings,
        each of which is treated as a resulting utterance.
    segmenter : pycantonese.word_segmentation.Segmenter, optional
        If not provided or if ``None`` is given, the default word segmentation behavior.
        For custom behavior, pass in a custom
        :class:`~pycantonese.word_segmentation.Segmenter` object.
    tagset : str, {"universal", "hkcancor"}, optional
        The part-of-speech tagset that the returned tags are in.
        This is the same argument for :func:`~pycantonese.pos_tag`.

    Returns
    -------
    :class:`~pycantonese.CHATReader`
    """

    if issubclass(type(data), str):
        # Perform simple sentence segmentation.
        for punct in _SENT_PUNCT_MARKS:
            data = data.replace(punct, f"{punct}\n")
        input_strs = data.split("\n")
    else:
        # Assume sentence segmentation is given: `data` is an iterable of strings.
        input_strs = data

    utterances = []

    for input_str in input_strs:
        if not input_str:
            continue
        words, tags, jps = _analyze_text(input_str, segmenter, tagset)
        tokens = [
            Token(word, pos, jp, None, None) for word, pos, jp in zip(words, tags, jps)
        ]
        u = Utterance(
            participant="XXX",
            tokens=tokens,
            time_marks=None,
            tiers={
                # TODO: Convert punct to CHAT-styled punct? Could be an optional arg.
                "*XXX": " ".join(words),
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
