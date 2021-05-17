import collections
import uuid

from pylangacq.chat import _File, Utterance

from pycantonese.corpus import CHATReader, Token
from pycantonese.jyutping.characters import characters_to_jyutping
from pycantonese.pos_tagging.tagger import pos_tag


_PUNCTUATION_MARKS = frozenset(("。", "！", "？"))


def _analyze_text(text, segmenter, tagset):
    chars_jps = characters_to_jyutping(text, segmenter)
    segmented, jyutping = [], []
    for chars, jps in chars_jps:
        segmented.append(chars)
        jyutping.append(jps)
    tags = [pos for _, pos in pos_tag(segmented, tagset)]
    return segmented, tags, jyutping


def _create_chat(data, segmenter=None, tagset="universal") -> CHATReader:

    data = "".join(data.split())
    for punct in _PUNCTUATION_MARKS:
        data = data.replace(punct, f"{punct}\n")
    input_strs = data.split("\n")

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
                # TODO: Convert punct to CHAT-styled punct.
                "*XXX": " ".join(words),
                # TODO: Show punct as itself instead of PUNCT|X.
                "%mor": " ".join(f"{pos}|{jp or ''}" for pos, jp in zip(tags, jps)),
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
