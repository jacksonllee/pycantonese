import collections

from pylangacq.chat import _File, Utterance

from pycantonese.corpus import CHATReader, Token
from pycantonese.jyutping.characters import characters_to_jyutping
from pycantonese.pos_tagging.tagger import pos_tag


_PUNCTUATION_MARKS = frozenset(("。", "！", "？"))


def _analyze_text(text, segmemter, tagset):
    chars_jps = characters_to_jyutping(text, segmemter)
    segmented, jyutping = [], []
    for chars, jps in chars_jps:
        segmented.append(chars)
        jyutping.append(jps)
    tags = [pos for _, pos in pos_tag(segmented, tagset)]
    return segmented, tags, jyutping


def _create_chat(
    data, *, by_utterances=False, segmemter=None, tagset="universal"
) -> CHATReader:
    if not by_utterances:
        data = "".join(data.split())
        for punct in ("。", "！", "？"):
            data = data.replace(punct, f"{punct}\n")
        input_strs = data.split("\n")
    else:
        input_strs = data
    utterances = []
    for utterance in input_strs:
        if not utterance:
            continue
        words, tags, jps = _analyze_text(utterance, segmemter, tagset)
        tokens = [
            Token(word, pos, jp, None, None) for word, pos, jp in zip(words, tags, jps)
        ]
        u = Utterance(
            participant="XXA",
            tokens=tokens,
            time_marks=None,
            tiers={
                "*XXA": " ".join(words),
                "%mor": " ".join(f"{pos}|{jp or ''}" for pos, jp in zip(tags, jps)),
            },
        )
        utterances.append(u)
    f = _File(
        file_path="foobar",  # TODO
        header=None,  # TODO: breaks headers()?
        utterances=utterances,
    )
    reader = CHATReader()
    reader._files = collections.deque([f])
    return reader
