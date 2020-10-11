from collections import Counter, defaultdict
from functools import lru_cache

from pycantonese.corpus import hkcancor
from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.word_segmentation import segment


@lru_cache(maxsize=1)
def _get_words_characters_to_jyutping():
    corpus = hkcancor()
    words_to_jyutping_counters = defaultdict(Counter)
    characters_to_jyutping_counters = defaultdict(Counter)

    for word, _, jyutping, _ in corpus.tagged_words():
        if not jyutping or not word:
            continue
        words_to_jyutping_counters[word][jyutping] += 1
        try:
            parsed_jp = parse_jyutping(jyutping)
        except ValueError:
            continue
        if len(word) != len(parsed_jp):
            continue
        for char, jp in zip(word, parsed_jp):
            characters_to_jyutping_counters[char]["".join(jp)] += 1

    words_to_jyutping = {}
    for word, jyutping_counter in words_to_jyutping_counters.items():
        jp = jyutping_counter.most_common(1)[0][0]
        words_to_jyutping[word] = jp
    characters_to_jyutping = {}
    for character, jyutping_counter in characters_to_jyutping_counters.items():
        jp = jyutping_counter.most_common(1)[0][0]
        characters_to_jyutping[character] = jp

    return words_to_jyutping, characters_to_jyutping


def characters2jyutping(chars):
    """
    Convert Cantonese characters to Jyytping romanization.

    The conversion model is based on the HKCanCor corpus data included
    in this library. Any unseen Cantonese character (or punctuation mark,
    for that matter) is represented by None in the output.

    :param chars: A string of Cantonese characters

    :return: Jyutping romanization of the input string

    :rtype: list of str
    """
    if not chars:
        return []
    words_to_jyutping, chars_to_jyutping = _get_words_characters_to_jyutping()
    result = []
    for word in segment(chars):
        try:
            parsed_jp = parse_jyutping(words_to_jyutping[word])
            word_as_jp = ["".join(parsed) for parsed in parsed_jp]
        except (KeyError, ValueError):
            word_as_jp = []
            for char in word:
                try:
                    char_as_jp = chars_to_jyutping[char]
                except KeyError:
                    word_as_jp.append(None)
                else:
                    word_as_jp.append(char_as_jp)
        result.extend(word_as_jp)
    return result
